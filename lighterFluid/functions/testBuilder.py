import pandas

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
        currTestName = dataset.TestName[i];
        currModule = dataset.Module[i];
        currLevels = dataset.Levels[i];
        currTimings = dataset.Timings[i];
        currPlist = dataset.plist[i];
        currPwr = dataset.PowerRail[i];

        fileToOpen = "testTemplates\\" + currTemplate + ".txt"

        with open(fileToOpen, 'r') as file:
            currTest = file.read();

        for key,value in findAndReplaceDict.items():
            #print(dataset[value][i])
            currTest = currTest.replace(key,str(dataset[value][i]));

        testList.append(currTest);

    testListSection = "\r\n".join(testList);
    return testListSection;