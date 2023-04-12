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
definitionList = [];
definitionList.append("arr_vpu");
definitionList.append("arr_core");
#definitionList.append("arr_atom");
#definitionList.append("arr_ccf");
#definitionList.append("arr_gfx");
#definitionList.append("arr_soc");
findAndReplaceFile = "inputs\\findAndReplaceFile.csv";



#####################
##### EXECUTION #####
#####################
for definitionPage in definitionList:
    ### read in File
    overallOutput = "";
    dataset = pandas.read_excel(definitionFile, sheet_name=definitionPage);

    importSection = importBuilder.importBuilder(dataset);
    counterSection = counterBuilder.counterBuilder(dataset);
    testSection = testBuilder.testBuilder(dataset,findAndReplaceFile);
    dutFlowSection = dutflowBuilder.dutflowBuilder(dataset);

    overallOutput = importSection + "\n" + counterSection + "\n" + testSection + "\n" + dutFlowSection;
    
    currModule = definitionPage.upper();
    outputMtpl = "outputs\\"+ currModule +".mtpl"; 
    outFile = open(outputMtpl, "w");
    outFile.write(overallOutput);
    outFile.close();

print("done");