from poplib import CR
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
    testInstance.Flow = nameComponents[3];
    testInstance.EdcKill = nameComponents[4];
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
            value = flowItems[1];
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
        
    composite.Flow = flow;
    composite.Template = "COMPOSITE";
    composite.TestName = flow;
    composite.Module = module;
    
    return composite

def parseFlowItem(name, module):
    composite = BackConvertComposite.BackConvertComposite();
    
    composite.Template = "COMPOSITE";
    composite.TestName = name;
    composite.Module = module;
    
    return composite

def parseMtpl(inputFile, module):
    # This function should open the mtpl and parse it line by line.
    # We should be able to ignore the top sections (version, imports, counters) - they can be generated from later info.
    # The 2x sections we care about are;
    # The "Test" section (blocks starting with Test)
    # The "DUTFlow section (blocks starting with DUTFlow)
    
    testInstanceDict = {};
    compositeDict = {};
    
    with open(inputFile, 'r') as file:
        text = file.read();
    
    block_lines = [];

    binsplitterRegex = ".*::n(\d\d)(\d\d)(\d\d\d)\d_.*";   

    setTestSection = 0;
    setFlowItemSection = 0;
    setFlowSection = 0;
    setResultSection = 0;
    isTest = 0;
    isComposite = 0;

    currPort = "";
    
    for line in text.split('\n'):
        line = line.strip(); # cleanup any junk
        
        # First priority - we need to know which block of text we are currently reading!!
        # We are either reading:
        # 1. A Test (instance)
        # 2. A Flow Item (This is really the rest of our test instance info, like porting and bins)
        # 3. A Flow (Either a composite or a full on flow like PREHVQK)
        # 4. A Result (This is the actual porting and bin info from our test - I have it split out because it's easier to distinguish section enders that way)
        if (line.startswith('Test') and not line.startswith("TestPlan")):
            setTestSection = 1;
            _, value1, value2 = line.strip().split(' ')

            currTemplate = value1;
            currName = value2;
            
        # This is where we parse the test section
        if (setTestSection):
            if line.startswith("{"):
                continue;
            if line.startswith("}"):
                setTestSection = 0;
                testInstanceDict[currName] = parseTestInstanceItem(currName, currTemplate, block_lines);
                block_lines = [];
                continue;
            else:
                block_lines.append(line);
                continue;
        
        # Now we move on to our flows! 
        if (line.startswith('DUTFlow') and not line.startswith("DUTFlowItem")):
            setFlowSection = 1;
            flowItems = line.strip().split(' ');
            currComp = flowItems[1];
            if (len(flowItems) == 3 and flowItems[2].endswith("_SubFlow")):
                currSubFlow = flowItems[2].lstrip("@").rstrip("_SubFlow");
                compositeDict[currComp] = parseSubFlowItem(currSubFlow, module);
            else:
                compositeDict[currComp] = parseFlowItem(currComp, module);
            
        
        elif line.startswith('DUTFlowItem'):
            setFlowItemSection = 1;
            flowItems = line.strip().split(' ');
            
            compositeDict[currComp].Contents.append(flowItems[1]);
            # compositeDict[currComp].Flow = currSubFlow;

            # This is how we know it's a test, otherwise it's another composite!
            if(flowItems[1] in testInstanceDict.keys()):
                isTest = 1;
                currTest = flowItems[1];
                if (len(flowItems) == 3):
                    if (flowItems[2] == "@EDC"):
                        testInstanceDict[currTest].killEnabled == "FALSE";
                    else:
                        testInstanceDict[currTest].killEnabled == "TRUE";
                else:
                    testInstanceDict[currTest].killEnabled == "TRUE";
            else:
                isComposite = 1;
                currTest = flowItems[1];
                compositeDict[currTest] = parseFlowItem(currTest, module);
            
        elif line.startswith('Result'):
            setResultSection = 1;
            _, currPort = line.strip().rstrip(";").split(' ')
            if(currPort in ["-2", "-1"]):
                continue
        
        
        # I'm structuring the code so it uses "}" as a key trigger. 
        # That means i need to make sure the priorities make sense.
        # For this to work - the lowest level of the composite flow is "Result". 
        # The next level is "DUTFlowItem"
        # The final (top) level is DutFlow
        
        # DutFlow handling
        if(setFlowSection and not setFlowItemSection and not setResultSection):
            if line.startswith("{"):
                continue;
            if line.startswith("}"):
                setFlowSection = 0;
                continue;
        
        # DutFlowItem handling
        if(setFlowSection and setFlowItemSection and not setResultSection):
            if line.startswith("{"):
                continue;
            if line.startswith("}"):
                setFlowItemSection = 0;
                isTest = 0;
                isComposite = 0;
                continue;
            
        # Result handling
        if(setFlowSection and setFlowItemSection and setResultSection):
            if line.startswith("{"):
                continue;
            if line.startswith("}"):
                setResultSection = 0;
                continue;
            if line.startswith("Property"):
                tempLine = line.split(" = ")[1].rstrip(";").rstrip("\"").lstrip("\"");
                
                if tempLine == "Pass":
                    passPort = True;
                else:
                    passPort = False;
                
                if isTest and passPort:
                    testInstanceDict[currTest].passPorts.append(currPort);
                    
                if isComposite and passPort:
                    compositeDict[currTest].passPorts.append(currPort);
            
            if line.startswith("IncrementCounters"):
                binDeetz = re.search(binsplitterRegex,line);
                testInstanceDict[currTest].IB = binDeetz.group(1);
                testInstanceDict[currTest].FB = binDeetz.group(2);
                testInstanceDict[currTest].Counter = binDeetz.group(3);
    
            if (line.startswith("GoTo") or line.startswith("Return")):
                tempLine = line.split(" ")[1].strip(";");
                tempGoTo = tempLine;
                
                if isTest:
                    testInstanceDict[currTest].PortList.append(tempGoTo);
                    
                if isComposite:
                    compositeDict[currTest].PortList.append(tempGoTo);


    return testInstanceDict, compositeDict;
