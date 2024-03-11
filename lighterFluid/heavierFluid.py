
from pickle import BUILD
import pandas as pd
import os
import subprocess
from functions import parseMtpl
from functions import parseFlw
from functions import BackConvertTestInstance
from functions import BackConvertComposite
from functions import BuildTestList
from functions import BuildTemplates
from functions import ExcelWriter
from datetime import datetime
import shutil


#########################
##### CONFIGURATION #####
#########################
definitionDir = r"C:\Users\adambyrn\source\repos\applications.manufacturing.ate-test.torch.client.ptl.sort.ptl-cdie484\Modules";
#definitionDir = r"C:\Users\adambyrn\source\repos\LNL_CPU_SORT\Modules";
userName = "adambyrn";
definitionDir = r"C:\Users\eoghanoc\source\repos\torch\lnl-cpu-v3\Modules";
definitionDir = r"C:\Users\eoghanoc\source\repos\lighterFluid\lighterFluid";
userName = "eoghanoc";

file = "lnlBackConvert.xlsm";
product = "ptl";
#product = "lnl442";

powerShellPath = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe";

moduleList = [];
# moduleList.append("arr_gfx");
# moduleList.append("arr_atom");
# moduleList.append("arr_ccf");
# moduleList.append("arr_core");
# moduleList.append("arr_soc");
# moduleList.append("arr_vpu");
moduleList.append("arr_common");
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

moduleFlowList = ["TESTPLANSTARTFLOW",
                  "TESTPLANENDFLOW",
                  "DUTCHANGEFLOW",
                  "LOTSTARTFLOW",
                  "LOTENDFLOW",
                  "INIT",
                  "START",
                  "BEGIN",
                  "PREHVQK",
                  "STRESS",
                  "SDTSTART",
                  "SDTBEGIN",
                  "HOTSTRESS",
                  "SDTEND",
                  "SDTFINAL",
                  "RETURN",
                  "POSTHVQK",
                  "END",
                  "ENDTFM",
                  "ENDXFM",
                  "EXVF",
                  "FINAL",
                  "ALARM",
                  "STARTFAILFLOW",
                  ];

# outDir = "heavierFluidOutputs\\" + timeStamp + "\\";
outDir = "heavierFluidOutputs\\";
templateDir = "heavierFluidTemplates\\" + product + "\\";

fileToUse = outDir + file;
if not os.path.exists(outDir):
    os.makedirs(outDir);

if not os.path.exists(templateDir):
    os.makedirs(templateDir);

testInstanceDict = {}
compositeDict = {};
flowList = {};

#####################
##### EXECUTION #####
#####################

# First we want to read all the test templates, flows, counters etc.
for module in moduleList:
    # doTheThing
    currMtpl = definitionDir + "\\" + module.upper() + "\\" + module.upper() + ".mtpl";
    currFlw = definitionDir + "\\" + module.upper() + "\\" + module.upper() + ".flw";
    
    currTestInstanceDict, currCompositeDict = parseMtpl.parseMtpl(currMtpl, module, moduleFlowList);
    currTestInstanceDict, currCompositeDict = parseFlw.parseFlw(currFlw, currTestInstanceDict, currCompositeDict);

    testInstanceDict[module] = currTestInstanceDict;
    compositeDict[module] = currCompositeDict;


# Next we want to create the templates we will use - with the unique vals
addedColsList = BuildTemplates.BuildTemplates(testInstanceDict,templateDir);

# Next we want to create the order of how we'll write down the tests/composites in Excel
for module in moduleList:
    flowList[module] = BuildTestList.BuildTestList(module, testInstanceDict, compositeDict, moduleFlowList);

# Finally we want to create the actual Excel

outFile = outDir + "heavierExcel_PTL.xlsx";
#outFile = outDir + "heavierExcel_LNL.xlsx";
ExcelWriter.WriteToExcel(outFile, moduleList, addedColsList, compositeDict, testInstanceDict, flowList);


print("done");
