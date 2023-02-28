import pandas
from functions import importBuilder
from functions import counterBuilder
from functions import testBuilder
from functions import dutflowBuilder
from functions import flowFileBuilder



#########################
##### CONFIGURATION #####
#########################
definitionFile = "inputs\\lnlArrayMasterSheet.xlsx";
definitionPage = "arr_atom";
findAndReplaceFile = "inputs\\findAndReplaceFile.csv";
outputMtpl = "outputs\\module.mtpl";



#####################
##### EXECUTION #####
#####################

### read in File
dataset = pandas.read_excel(definitionFile, sheet_name=definitionPage);

importSection = importBuilder.importBuilder(dataset);
counterSection = counterBuilder.counterBuilder(dataset);
testSection = testBuilder.testBuilder(dataset,findAndReplaceFile);
dutFlowSection = dutflowBuilder.dutflowBuilder(dataset);

overallOutput = importSection + "\n" + counterSection + "\n" + testSection + "\n" + dutFlowSection;

outFile = open(outputMtpl, "w");
outFile.write(overallOutput);
outFile.close();

print("done");