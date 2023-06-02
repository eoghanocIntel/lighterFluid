import pandas
import os
from functions import importBuilder
from functions import counterBuilder
from functions import testBuilder
from functions import dutflowBuilder
from datetime import datetime
import shutil



#########################
##### CONFIGURATION #####
#########################
#definitionDir = r"C:\Users\adambyrn\OneDrive - Intel Corporation\ARRAY\lighterFluidFiles";
#definitionDir = r"C:\Users\lsuareza\OneDrive - Intel Corporation\ARRAY\lighterFluidFiles";
definitionDir = r"C:\Users\eoghanoc\OneDrive - Intel Corporation\ARRAY\lighterFluidFiles";
file = "lnlArrayMasterSheet.xlsx";

definitionList = [];
definitionList.append("arr_atom");
definitionList.append("arr_ccf");
definitionList.append("arr_core");
definitionList.append("arr_gfx");
definitionList.append("arr_soc");
definitionList.append("arr_vpu");
#findAndReplaceFile = "inputs\\findAndReplaceFile.csv";

currSecond = str(datetime.now().second).zfill(2);
currMinute = str(datetime.now().minute).zfill(2);
currHour =   str(datetime.now().hour).zfill(2);

currDay =   str(datetime.now().day).zfill(2);
currMonth = str(datetime.now().month).zfill(2);
currYear =  str(datetime.now().year).zfill(4);

folderName = "_".join([currYear, currMonth, currDay, currHour, currMinute, currSecond]);

outDir = "outputs\\" + folderName + "\\";
fileToUse = outDir + "\\" + file;
if not os.path.exists(outDir):
    os.makedirs(outDir);

shutil.copyfile(definitionDir + "\\" + file, fileToUse)

#####################
##### EXECUTION #####
#####################
for definitionPage in definitionList:
    ### read in File
    overallOutput = "";
    currModule = definitionPage.upper();
    
    dataset = pandas.read_excel(fileToUse, sheet_name=definitionPage);
    
    moduleDir = outDir + currModule + "\\"; 
    if not os.path.exists(moduleDir):
        os.makedirs(moduleDir);
    outputMtpl = outDir + currModule + "\\" + currModule + ".mtpl"; 


    importSection = importBuilder.importBuilder(dataset);
    counterSection = counterBuilder.counterBuilder(dataset);
    testSection = testBuilder.testBuilder(dataset);
    dutFlowSection = dutflowBuilder.dutflowBuilder(dataset);

    overallOutput = importSection + "\n" + counterSection + "\n" + testSection + "\n" + dutFlowSection;
    
    currModule = definitionPage.upper();

    moduleDir = "outputs\\" + currModule + "\\";
    if not os.path.exists(moduleDir):
        os.makedirs(moduleDir);
    outputMtpl = "outputs\\" + currModule + "\\" + currModule + ".mtpl"; 
    outFile = open(outputMtpl, "w");
    outFile.write(overallOutput);
    outFile.close();

print("done");
