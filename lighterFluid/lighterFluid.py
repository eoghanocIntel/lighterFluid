import subprocess

try:
    import pandas
except :
    print("need to import pandas using pip");
    subprocess.call('python -m pip install --upgrade pip --proxy="http://proxy-chain.intel.com:911"')
    subprocess.call('python -m pip install pandas --proxy="http://proxy-chain.intel.com:911"');
    import pandas

try:
    import openpyxl
except :
    print("need to import openpyxl using pip");
    subprocess.call('python -m pip install --upgrade pip --proxy="http://proxy-chain.intel.com:911"')
    subprocess.call('python -m pip install openpyxl --proxy="http://proxy-chain.intel.com:911"');
    import openpyxl


from functions import importBuilder
from functions import counterBuilder
from functions import testBuilder
from functions import dutflowBuilder
from functions import flowFileBuilder



#########################
##### CONFIGURATION #####
#########################
definitionFile = r"C:\Users\cmichel1\TorchTPs\gnrdio_sort\Modules\FUN_NAC\InputFiles\Func_Sheet.xlsx";
definitionList = [];
definitionList.append("rst_dfx");
definitionList.append("rst_reset");
definitionList.append("fun_uncore");
definitionList.append("fun_nac");
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