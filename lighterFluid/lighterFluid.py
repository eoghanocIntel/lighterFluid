import pandas
from functions import importBuilder
from functions import counterBuilder
from functions import testBuilder
from functions import dutflowBuilder
from functions import flowFileBuilder



#########################
##### CONFIGURATION #####
#########################
definitionFile = r"C:\Users\cmichel1\source\repos\lighterFluid\lighterFluid\inputs\Func_Sheet.xlsx";
definitionList = [];
definitionList.append("rst_dfx");
definitionList.append("rst_reset");
findAndReplaceFile = "inputs\\findAndReplaceFile.csv";



#####################
##### EXECUTION #####
#####################
for definitionPage in definitionList:
    ### read in File
    overallOutput = "";
    dataset = pandas.read_excel(definitionFile, sheet_name=definitionPage);

    moduleName = str(definitionPage).upper()

    importSection = importBuilder.importBuilder(dataset, moduleName);
    counterSection = counterBuilder.counterBuilder(dataset);
    testSection = testBuilder.testBuilder(dataset,findAndReplaceFile);
    dutFlowSection = dutflowBuilder.dutflowBuilder(dataset, moduleName);

    overallOutput = importSection + "\n" + counterSection + "\n" + testSection + "\n" + dutFlowSection;
    
    currModule = definitionPage.upper();
    outputMtpl = "outputs\\"+ currModule +".mtpl"; 
    outFile = open(outputMtpl, "w");
    outFile.write(overallOutput);
    outFile.close();

print("done");