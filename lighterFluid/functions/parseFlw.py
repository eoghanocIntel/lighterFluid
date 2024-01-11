from . import BackConvertTestInstance
from . import BackConvertComposite
import re

#####################
##### FUNCTIONS #####
#####################
def parseTestInstanceItem(name, template, block_lines):
    testInstance = BackConvertTestInstance.BackConvertTestInstance();
    
    testInstance.Template = template;
    testInstance.TestName = name;
    
    nameComponents = name.split("_");

    testInstance.IP = nameComponents[0];
    testInstance.Module = nameComponents[1];
    testInstance.TestType = nameComponents[2];
    testInstance.EdcKill  = nameComponents[3];
    testInstance.Flow = nameComponents[4];
    testInstance.DFT = nameComponents[5];
    testInstance.PowerRail = nameComponents[6];
    testInstance.VoltageCorner = nameComponents[7];
    testInstance.FreqCorner = nameComponents[8];
    testInstance.FreqNum = nameComponents[9];
    testInstance.NameEnding = "_".join(nameComponents[10:]);
    
    for line in block_lines:
        flowItems = line.strip().rstrip(";").split(' = ');
        if len(flowItems) == 2:
            key = flowItems[0];
            value = str(flowItems[1].strip("\""));
        else:
            # The first item should be "Test BLABLABLA", which doesn't split).
            continue
        
        if (key in ["LevelsTc","level"]):
            testInstance.Levels = value;
        elif(key in ["TimingsTc","timings"]):
            testInstance.Timings = value;
        elif(key in ["Patlist","patlist"]):
            testInstance.plist = value;
        elif(key in ["BypassPort","bypass_global"]):
            testInstance.bypassGlobal = value;
        else:
            testInstance.bonusCols[key] = value;

    return testInstance;

def parseSubFlowItem(flow, module):
    composite = BackConvertComposite.BackConvertComposite();
        
    flow = flow.lstrip(module.upper() + "_");
    composite.Flow = flow;
    composite.Template = "COMPOSITE";
    composite.TestName = flow;
    tempModule = module.split('_');
    module = tempModule[1].upper();
    composite.Module = module;
    
    return composite

def parseFlowItem(name, module):
    composite = BackConvertComposite.BackConvertComposite();
    
    composite.Template = "COMPOSITE";
    composite.TestName = name;
    tempModule = module.split('_');
    module = tempModule[1].upper();
    composite.Module = module;
    
    return composite

def CompositeFlowFixer(compositeDict, subcomp, currFlow):
    
    for instance in subcomp.Contents:
        if instance in compositeDict.keys():
            compositeDict[instance].Flow = currFlow;
            compositeDict = CompositeFlowFixer(compositeDict, compositeDict[instance], currFlow);

    

    return compositeDict;

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
