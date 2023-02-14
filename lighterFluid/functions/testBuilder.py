import pandas

##################
##### BASICS #####
##################
testList = [];

####################
##### FUNCTION #####
####################
def testBuilder(dataset):
    # This function should build the test list.

    for i in range(0,len(dataset.Template)):
        # ignore composites
        if("COMPOSITE" in dataset.Template[i]):
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

        currTest = currTest.replace("###TestName###",currTestName);
        currTest = currTest.replace("###Levels###",currLevels);
        currTest = currTest.replace("###Timings###",currTimings);
        currTest = currTest.replace("###Patlist###",currPlist);
        currTest = currTest.replace("###PowerTarget###",currPwr);
        currTest = currTest.replace("###PowerHighLimit###",currPwr+"HighLimit");
        currTest = currTest.replace("###Module###",currModule);

        testList.append(currTest);

    testListSection = "\r\n".join(testList);
    return testListSection;