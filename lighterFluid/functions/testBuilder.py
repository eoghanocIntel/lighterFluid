import pandas
import math


####################
##### FUNCTION #####
####################
def testBuilder(dataset,findAndReplaceFile, product):
    # This function should build the test list.

    ##################
    ##### BASICS #####
    ##################
    testList = [];

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

        fileToOpen = "testTemplates\\" + product + "\\" + currTemplate + ".txt"

        with open(fileToOpen, 'r') as file:
            currTest = file.read();

        for key,value in findAndReplaceDict.items():
            if value in dataset.columns.values.tolist():
                #print(dataset[value][i])
                
                # This section is for numbers
                if (key in ["###baseNumber###","###bypassGlobal###"]):
                    if math.isnan(dataset[value][i]):
                        currValue = "";
                    else:
                        currValue = int(dataset[value][i]);
                        currValue = str(currValue);
                # This section is for strings
                elif (key in ["###SetPointsPreInstance###",
                              "###printToItuff###",
                              "###ifpmFile###",
                              "###ifpmMod###",
                              "###preinstance###",
                              "###postinstance###"]):
                    try:
                        if math.isnan(dataset[value][i]):
                            currValue = "";
                    except:
                        currValue = str(dataset[value][i]);
                else:
                    currValue = str(dataset[value][i]);

                currTest = currTest.replace(key,currValue);

        testList.append(currTest);

    testListSection = "\r\n".join(testList);
    return testListSection;

def testBuilder(dataset, product):
    # This function should build the test list.

    ##################
    ##### BASICS #####
    ##################
    testList = [];
    
    for i in range(0,len(dataset.Template)):
        # ignore composites
        if(("COMPOSITE" in dataset.Template[i]) or ("TP_BEGIN" in dataset.Template[i]) or ("TP_END" in dataset.Template[i])):
            continue;
        
        currTemplate = dataset.Template[i];

        fileToOpen = "testTemplates\\" + product + "\\" + currTemplate + ".txt"

        with open(fileToOpen, 'r') as file:
            currTest = file.read();

        for value in dataset.columns.values.tolist():

            replaceStr = "###" + value + "###";
            currValue = "";
            
            # This section is for numbers
            if (value in ["baseNumber","bypassGlobal"]):
                if math.isnan(dataset[value][i]):
                    currValue = "";
                else:
                    currValue = int(dataset[value][i]);
                    currValue = str(currValue);
            # This section is for strings
            elif (value in ["SetPointsPreInstance",
                            "printToItuff",
                            "SetPointsPostInstance",
                            "ifpmFile",
                            "ifpmFile",
                            "ifpmMod",
                            "preinstance",
                            "postinstance"]):
                try:
                    if math.isnan(dataset[value][i]):
                        currValue = "";
                except:
                    currValue = str(dataset[value][i]);
            else:
                currValue = str(dataset[value][i]);

                

            currTest = currTest.replace(replaceStr,currValue);

        testList.append(currTest);

    testListSection = "\r\n".join(testList);
    return testListSection;