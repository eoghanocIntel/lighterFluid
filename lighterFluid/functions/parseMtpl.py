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
    testInstance.EdcKill  = nameComponents[3];
    testInstance.Flow = nameComponents[4];
    testInstance.DFT = nameComponents[5];
    testInstance.PowerRail = nameComponents[6];
    testInstance.VoltageCorner = nameComponents[7];
    testInstance.FreqCorner = nameComponents[8];
    
    if len(nameComponents) < 9:
        testInstance.FreqNum = "X";
    else:
        testInstance.FreqNum = nameComponents[9];
    if len(nameComponents) < 10:
        testInstance.NameEnding = "";
    else:
        testInstance.NameEnding = "_".join(nameComponents[10:]);
    
    for line in block_lines:
        tempLine = re.sub(r';\s*#.*',";",line);
        
        flowItems = tempLine.strip().rstrip(";").split(' = ');
        if len(flowItems) == 2:
            key = flowItems[0];
            value = str(flowItems[1]);
        else:
            # The first item should be "Test BLABLABLA", which doesn't split).
            continue
        
        if key.startswith("#"):
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
            if(value.startswith("\"")):
                testInstance.bonusColsStrings[key] = value;
            else:
                try:
                    testInstance.bonusColsIntegers[key] = int(value);
                except :
                    try:
                        testInstance.bonusColsIntegers[key] = float(value);
                    except :
                        # This should only happen if we are using a Uservar to define an Int (eg startVoltage)
                        testInstance.bonusColsIntegers[key] = value;
                

    return testInstance;

#Via Chip Chat
def parseSubFlowItem(flow, module):
    composite = BackConvertComposite.BackConvertComposite()
    module_upper = module.upper()
    if flow.startswith(module_upper + "_"):
        flow = flow[len(module_upper) + 1:]  # remove the module name and underscore
    
    composite.Flow = flow
    composite.Template = "COMPOSITE"
    composite.TestName = flow
    tempModule = module.split('_')
    if len(tempModule) > 1:
        module = tempModule[1].upper()  # This assumes the format always has two parts
    else:
        module = tempModule[0].upper()
    composite.Module = module

    return composite

"""
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
"""        

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

def parseMtpl(inputFile, module, moduleFlowList):
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

    binsplitterRegex = ".*::([np])(\d\d)(\d\d)(\d\d\d)\d_.*";   
    b9899Regex = ".*SoftBins.b9[89]\d\d(\d\d\d\d)_fail.*";   

    setTestSection = 0;
    setFlowItemSection = 0;
    setFlowSection = 0;
    setResultSection = 0;
    setAlarmPort = 0;
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
        if (line.startswith('Test') and not line.startswith("TestPlan") and not "=" in line):
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
        if ((line.startswith('DUTFlow') or line.startswith('Flow')) and not (line.startswith("DUTFlowItem") or line.startswith("FlowItem"))):
            setFlowSection = 1;
            flowItems = line.strip().split(' ');
            if (len(flowItems) == 3 and flowItems[2].endswith("_SubFlow")):
                currComp = flowItems[2].lstrip("@")[:-8];
                compositeDict[currComp] = parseSubFlowItem(currComp, module);
            elif(len(flowItems) == 3 and flowItems[2].startswith("@")):
                currComp = flowItems[2].lstrip("@");
                compositeDict[currComp] = parseSubFlowItem(currComp, module);
            else:
                currComp = flowItems[1];
                compositeDict[currComp] = parseFlowItem(currComp, module);
            
        
        elif (line.startswith('DUTFlowItem') or line.startswith('FlowItem')):
            setFlowItemSection = 1;
            flowItems = line.strip().split(' ');
            
            compositeDict[currComp].Contents.append(flowItems[1]);
            # compositeDict[currComp].Flow = currSubFlow;

            # This is how we know it's a test, otherwise it's another composite!
            if(flowItems[1] in testInstanceDict.keys()):
                isTest = 1;
                currTest = flowItems[1];
                if (len(flowItems) == 4):
                    if (flowItems[3] == "@EDC"):
                        testInstanceDict[currTest].killEnabled = "FALSE";
                    else:
                        testInstanceDict[currTest].killEnabled = "TRUE";
                else:
                    testInstanceDict[currTest].killEnabled = "TRUE";
            else:
                isComposite = 1;
                currTest = flowItems[1];
                # compositeDict[currTest] = parseFlowItem(currTest, module);
            
        elif line.startswith('Result'):
            setResultSection = 1;

            lineContents = line.strip().split(' ');
            
            # This is the "standard" format, where we have the result called and then the routing and binning etc later
            if len(lineContents) == 2:
                _, currPort = line.strip().rstrip(";").split(' ')
                if(currPort in ["-2", "-1"]):
                    setAlarmPort = 1;
                    continue;
                else:
                    setAlarmPort = 0;
            
            # This is the inline workaround format, where we have all info on one line (typically used for alarms)
            # Until I see other use-cases I am only setting up a WA for alarms...
            elif ("Return" in line):
                setResultSection
                continue;
                
        
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
                if (currTest in ["ALL_CCF_PATMOD_K_BEGIN_X_X_X_X_X_RESET_FREQ","ALL_CORE_PATMOD_K_BEGIN_X_X_X_X_X_RESET_FREQ"]):
                    blablabla = 1;
                binDeetz = re.search(binsplitterRegex,line);
                if (binDeetz.group(1) == "p"):
                    testInstanceDict[currTest].WritePassCounter = "TRUE";
                testInstanceDict[currTest].IB = binDeetz.group(2);
                testInstanceDict[currTest].FB = binDeetz.group(3);
                testInstanceDict[currTest].Counter = binDeetz.group(4);
    
            if line.startswith("SetBin") and setAlarmPort:
                if ("FAIL_DPS_ALARM" in line) or ("FAIL_SYSTEM_SOFTWARE" in line):
                    continue;
                alarmDeetz = re.search(b9899Regex,line);
                testInstanceDict[currTest].b9899Counter = alarmDeetz.group(1);
                
            if (line.startswith("GoTo") or line.startswith("Return")):
                tempList = list(filter(None, line.split(" ")));
                tempLine = tempList[1].strip(";");
                tempGoTo = tempLine;
                
                if not setAlarmPort:
                    if isTest:
                        testInstanceDict[currTest].PortList.append(tempGoTo);
                    
                    if isComposite:
                        compositeDict[currTest].PortList.append(tempGoTo);


    for subComp in compositeDict:
        if subComp in moduleFlowList:
            compositeDict = CompositeFlowFixer(compositeDict, compositeDict[subComp], subComp);
    
    return testInstanceDict, compositeDict;
