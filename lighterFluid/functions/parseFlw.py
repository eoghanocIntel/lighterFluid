from . import BackConvertTestInstance
from . import BackConvertComposite
import re

#####################
##### FUNCTIONS #####
#####################

def parseFlw(inputFile, testInstanceDict, compositeDict):
    # This function should open the flw file and parse it line by line.
    # We basically want to pull the instance/composite name, and it's X/Y loc vals
   
    with open(inputFile, 'r') as file:
        text = file.read();
    
    instanceSplitRegex = ".*\.([A-Z0-9_]+)\"\sX=\"(\d+)\"\sY=\"(\d+)\"";   

    for line in text.split('\n'):
        line = line.strip(); # cleanup any junk
        
        flowDeetz = re.search(instanceSplitRegex,line);
        
        if flowDeetz:
            currTest = flowDeetz.group(1);
            currX = int(flowDeetz.group(2));
            currY = int(flowDeetz.group(3));
        
            tempX = round(currX/150);
            tempY = round(currY/250);

            if (currTest in testInstanceDict):
                testInstanceDict[currTest].flowX = str(tempX);
                testInstanceDict[currTest].flowY = str(tempY);
            elif (currTest in compositeDict):
                compositeDict[currTest].flowX = str(tempX);
                compositeDict[currTest].flowY = str(tempY);
            else:
                print("Almost certainly a bug - this test isnt in Test/Comp list " + currTest);
    
    return testInstanceDict, compositeDict;
