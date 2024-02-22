import pandas
import os
import subprocess
from functions import importBuilder
from functions import counterBuilder
from functions import testBuilder
from functions import dutflowBuilder
from functions import flowFileBuilder
from datetime import datetime
import shutil



#########################
##### CONFIGURATION #####
#########################
#definitionDir = r"C:\Users\lsuareza\OneDrive - Intel Corporation\ARRAY\lighterFluidFiles";
#userName = "lsuareza";
#definitionDir = r"C:\Users\eoghanoc\OneDrive - Intel Corporation\ARRAY\lighterFluidFiles";
#userName = "eoghanoc";
#definitionDir = r"C:\Users\brownm1\OneDrive - Intel Corporation\ARRAY\lighterFluidFiles";
#userName = "brownm1";
# definitionDir = r"C:\Users\dgiardin\OneDrive - Intel Corporation\ARRAY\lighterFluidFiles";
# userName = "dgiardin";
#definitionDir = r"C:\Users\rbilei\OneDrive - Intel Corporation\ARRAY\lighterFluidFiles";
#userName = "rbilei";
#definitionDir = r"C:\Users\adambyrn\OneDrive - Intel Corporation\Array - Panther Lake Sort Development\LF";
definitionDir = r"C:\Users\adambyrn\source\repos\lighterFluid\lighterFluid\heavierFluidOutputs";
userName = "adambyrn";

#file = "PTLArrayMasterSheet.xlsm";
file = "heavierExcel_PTL.xlsx";
product = "ptl";


#definitionDir = r"C:\Users\eoghanoc\OneDrive - Intel Corporation\Documents\CLIENT\LNL\Array\WW32";
#userName = "eoghanoc";
#file = "lnlArrayCommon.xlsx";

powerShellPath = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe";

definitionList = [];
definitionList.append("arr_common");
definitionList.append("arr_atom");
definitionList.append("arr_ccf");
definitionList.append("arr_core");
definitionList.append("arr_gfx");
definitionList.append("arr_soc");
definitionList.append("arr_npu");
#definitionList.append("arr_doe");
#findAndReplaceFile = "inputs\\findAndReplaceFile.csv";


#########################
########## SETUP ########
#########################

currSecond = str(datetime.now().second).zfill(2);
currMinute = str(datetime.now().minute).zfill(2);
currHour =   str(datetime.now().hour).zfill(2);

currDay =   str(datetime.now().day).zfill(2);
currMonth = str(datetime.now().month).zfill(2);
currYear =  str(datetime.now().year).zfill(4);

timeStamp = "_".join([userName, currYear, currMonth, currDay, currHour, currMinute, currSecond]);

outDir = "outputs\\" + timeStamp + "\\";
fileToUse = outDir + file;
if not os.path.exists(outDir):
    os.makedirs(outDir);

shutil.copyfile(definitionDir + "\\" + file, fileToUse)
#inFile = "heavierFluidOutputs\\heavierExcel.xlsx";
inFile = definitionDir + "\\" + file;


#subprocess.call(["dir"], shell=True);
pwrShlCmd = powerShellPath + " cp '" + inFile + "' '" + fileToUse + "'";
subprocess.call(pwrShlCmd, shell=True);

#####################
##### EXECUTION #####
#####################
for definitionPage in definitionList:
    ### read in File
    overallOutput = "";
    currModule = definitionPage.upper();
    
    dataset = pandas.read_excel(fileToUse, sheet_name=definitionPage, keep_default_na=False);
    
    importSection = importBuilder.importBuilder(dataset, timeStamp);
    counterSection = counterBuilder.counterBuilder(dataset);
    testSection = testBuilder.testBuilder(dataset,product);
    dutFlowSection = dutflowBuilder.dutflowBuilder(dataset);
    flowFileSection = flowFileBuilder.flowFileBuilder(dataset);

    overallOutput = importSection + "\n" + counterSection + "\n" + testSection + "\n" + dutFlowSection;
    
    currModule = definitionPage.upper();
    
    moduleDir = outDir + currModule + "\\"; 
    if not os.path.exists(moduleDir):
        os.makedirs(moduleDir);
    outputMtpl = moduleDir + currModule + ".mtpl"; 
    outFile = open(outputMtpl, "w");
    outFile.write(overallOutput);
    outFile.close();
    
    outputMtpl = moduleDir + currModule + ".flw"; 
    outFile = open(outputMtpl, "w");
    outFile.write(flowFileSection);
    outFile.close();

print("done");
