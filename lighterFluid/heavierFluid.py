
import pandas
import os
import subprocess
from functions import parseMtpl
from functions import BackConvertTestInstance
from functions import BackConvertComposite
from datetime import datetime
import shutil



#########################
##### CONFIGURATION #####
#########################
definitionDir = r"C:\Users\eoghanoc\source\repos\torch\lnl-cpu-v3\Modules";
userName = "eoghanoc";

file = "lnlBackConvert.xlsm";
product = "lnl442";

powerShellPath = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe";

moduleList = [];
# moduleList.append("arr_atom");
# moduleList.append("arr_ccf");
# moduleList.append("arr_core");
moduleList.append("arr_gfx");
# moduleList.append("arr_soc");
# moduleList.append("arr_vpu");
# moduleList.append("arr_common");
# moduleList.append("arr_doe");

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

# outDir = "heavierFluidOutputs\\" + timeStamp + "\\";
outDir = "heavierFluidOutputs\\";

fileToUse = outDir + file;
if not os.path.exists(outDir):
    os.makedirs(outDir);

testInstanceDict = {}
compositeDict = {};

#####################
##### EXECUTION #####
#####################

# First we want to read all the test templates, flows, counters etc.
for module in moduleList:
    # doTheThing
    currMtpl = definitionDir + "\\" + module.toUpper() + "\\" + module.toUpper() + ".mtpl";
    
    currTestInstanceDict, currCompositeDict = parseMtpl(currMtpl, module);

    testInstanceDict[module] = currTestInstanceDict;
    compositeDict[module] = currCompositeDict;




# Next we want to create the templates we will use - with the unique vals


# Finally we want to create the actual Excel

outFile = outDir + "heavierExcel.xlsm";
for module in moduleList:
    # doTheThing

    i=0;


print("done");
