import pandas
import math

##################
##### BASICS #####
##################
testList = [];

####################
##### FUNCTION #####
####################
def testBuilder(dataset,findAndReplaceFile):
    # This function should build the test list.

    findAndReplaceDict = {};
    with open(findAndReplaceFile, 'r') as file:
        for line in file:
            splitLine = line.strip().split(",");
            findAndReplaceDict[splitLine[0]] = splitLine[1];

    for i in range(0,len(dataset.Template)):
        # ignore composites
        if(("COMPOSITE" in dataset.Template[i]) or ("TP_BEGIN" in dataset.Template[i]) or ("TP_END" in dataset.Template[i])):
            continue;
        
        currTemplate = dataset.Template[i];

        fileToOpen = "testTemplates\\" + currTemplate + ".txt"

        with open(fileToOpen, 'r') as file:
            currTest = file.read();

        for key,value in findAndReplaceDict.items():
            if value in dataset.columns.values.tolist():
                #print(dataset[value][i])
                if (key in ["###baseNumber###","###bypassGlobal###"]):
                    if math.isnan(dataset[value][i]):
                        currValue = "";
                    else:
                        currValue = int(dataset[value][i]);
                        currValue = str(currValue);
                else:
                    currValue = str(dataset[value][i]);

                currTest = currTest.replace(key,currValue);

        testList.append(currTest);

    testListSection = "\r\n".join(testList);
    return testListSection;