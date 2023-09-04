import pandas
import math


####################
##### FUNCTION #####
####################
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
            if (value in ["baseNumber","bypassGlobal","StartIndex"]):
                if math.isnan(dataset[value][i]):
                    currValue = "";
                else:
                    currValue = int(dataset[value][i]);
                    currValue = str(currValue);
            # This section is for strings
            elif (value in ["SetPointsPreInstance",
                            "RegEx",
                            "printToItuff",
                            "DtsConfigName",
                            "SetPointsPostInstance",
                            "SetPointsPlistMode",
                            "ifpmFile",
                            "ifpmFile",
                            "ifpmMod",
                            "iTuffExt",
                            "preinstance",
                            "postinstance",
                            "RecString"]):
                try:
                    if math.isnan(dataset[value][i]):
                        currValue = "";
                except:
                    currValue = str(dataset[value][i]);
            else:
                currValue = str(dataset[value][i]);

                
            if value == "RecString":
                currValue = currValue.replace('"', '')
            currTest = currTest.replace(replaceStr,currValue);

        testList.append(currTest);

    testListSection = "\r\n".join(testList);
    return testListSection;