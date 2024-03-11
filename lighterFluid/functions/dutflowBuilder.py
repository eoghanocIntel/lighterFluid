import pandas
from . import Composite
from . import TestInstance
import inspect



#############################
##### RECURSION MACHINE #####
#############################
def flowCursion(dataset, rowCount):
    ##################
    ##### BASICS #####
    ##################
    flowDict = {};
    flowSection = "";

    i = rowCount;
    contentList = [];

    currComposite = Composite.Composite();
    currComposite.CompositeName = dataset.TestName[i];
    currComposite.portCount = dataset.portCount[i];
    currComposite.passPorts = dataset.passPorts[i];
    currComposite.PortList.append(dataset.Port0[i]);
    currComposite.PortList.append(dataset.Port1[i]);
    currComposite.PortList.append(dataset.Port2[i]);
    currComposite.Contents = [];
    currComposite.Module = dataset.Module[i];

    i = i+1;
    
    while (i < len(dataset.Template)):
        # If we have a nested composite, need to start recursion
        if ("COMPOSITE_BEGIN" in dataset.Template[i]):
            (subComposite, i) = flowCursion(dataset, i);
            currComposite.Contents.append(subComposite);
            i = i+1;
            continue;

        # Exit the nested composite
        if ("COMPOSITE_END" in dataset.Template[i]):
            #currComposite.Contents.append(contentList);
            return currComposite, i;
        
        # Exit the nested composite
        if ("TP_END" in dataset.Template[i]):
            #currComposite.Contents.append(contentList);
            return currComposite;

        currTest = TestInstance.TestInstance();
        # Assuming this is a chain ender - we need to assign ports
        currTest.TestName = dataset.TestName[i];
        currTest.passPorts = dataset.passPorts[i];
        currTest.portCount = dataset.portCount[i];
        currTest.Module = dataset.Module[i];
        currTest.IB = dataset.IB[i];
        currTest.FB = dataset.FB[i];
        currTest.Counter = dataset.Counter[i];
        currTest.WritePassCounter = dataset.WritePassCounter[i];
        currTest.KillEnabled = dataset.killEnabled[i];

        # This is ugly and I hate it but I'm doing it to get this done quick.
        # I'm certain a better coder will look at this and vomit.
        # Lol I made that pleb vomit.
        currTest.PortList.append(dataset.Port0[i]);
        currTest.PortList.append(dataset.Port1[i]);
        currTest.PortList.append(dataset.Port2[i]);
        currTest.PortList.append(dataset.Port3[i]);
        currTest.PortList.append(dataset.Port4[i]);
        currTest.PortList.append(dataset.Port5[i]);
        currTest.PortList.append(dataset.Port6[i]);
        currTest.PortList.append(dataset.Port7[i]);
        currTest.PortList.append(dataset.Port8[i]);
        currTest.PortList.append(dataset.Port9[i]);
        
        currComposite.Contents.append(currTest);

        i = i+1;

    return currComposite


##############################
##### INSTANCE PRINT OUT #####
##############################
def printASmolBoi(currTest, currModule):

    currKill = currTest.KillEnabled;
    killOrEdc = "";
    if (not currKill or currKill == "FALSE"):
        killOrEdc = "@EDC";
    

    header = """
	DUTFlowItem {name} {name} {killOrEdc}
	{{
		Result -2
		{{
			Property PassFail = "Fail";
			SetBin SoftBins.b99010001_fail_FAIL_DPS_ALARM;
			Return -2;
		}}		
		Result -1
		{{
			Property PassFail = "Fail";
			SetBin SoftBins.b98010001_fail_FAIL_SYSTEM_SOFTWARE;
			Return -1;
		}}""".format(name = currTest.TestName, killOrEdc = killOrEdc);
    footer = "\n\t}";
    body = "";


    
    currIb =        str(int(currTest.IB));
    currFb =        str(int(currTest.FB));
    currCounter =   int(currTest.Counter)*10;
    
    #currPheoBin = currIb.zfill(2) + currFb.zfill(2) + currCounter.zfill(4);
    for i in range(0,int(currTest.portCount)):
        nextTest = "";
        try:
            float(currTest.PortList[i]);
            nextTest = "Return " + str(int(float(currTest.PortList[i])));
        except:
            nextTest = "GoTo " + currTest.PortList[i];

        if (str(i) in str(currTest.passPorts)):
            if currTest.WritePassCounter == "FALSE":
                body = body + """
		Result {portNo}
		{{
			Property PassFail = "Pass";
			{nextTest};
		}}""".format(portNo=i, nextTest=nextTest);
            else:    
                currPheoBin = currIb.zfill(2) + currFb.zfill(2) + str(currCounter + i).zfill(4);
                dummyCounter = "p" + currPheoBin + "_pass_" + currTest.TestName + "_" + str(i); 
                body = body + """
		Result {portNo}
		{{
			Property PassFail = "Pass";
	        IncrementCounters {currModule}::{dummyCounter};
			{nextTest};
		}}""".format(portNo=i, currModule=currModule, dummyCounter=dummyCounter, nextTest=nextTest);


        else:
            currPheoBin = currIb.zfill(2) + currFb.zfill(2) + str(currCounter + i).zfill(4);
            sharedBin = "SetBin SoftBins.b" + currPheoBin + "_fail_" + currModule + "_" + currTest.TestName;
            if (not currKill or currKill == "FALSE"):
                sharedBin = "##EDC## " + sharedBin;

            dummyCounter = "n" + currPheoBin + "_fail_" + currTest.TestName + "_" + str(i);
            body = body + """
        Result {portNo}
        {{
	        Property PassFail = "Fail";
	        IncrementCounters {currModule}::{dummyCounter};
	        {sharedBin};
			{nextTest};
        }}""".format(portNo=i, currModule=currModule, dummyCounter=dummyCounter, nextTest=nextTest, sharedBin=sharedBin);


    return header + body + footer;

###############################
##### COMPOSITE PRINT OUT #####
###############################
def printABigBoi(currComp):

    header = """
    DUTFlowItem {name} {name}
	{{
		Result -2
		{{
			Property PassFail = "Fail";
			Return -2;
		}}		
		Result -1
		{{
			Property PassFail = "Fail";
			Return -1;
		}}""".format(name = currComp.CompositeName);
    footer = "\n\t}";

    body = "";
    for i in range(0,int(currComp.portCount)):

        nextTest = "";
        try:
            float(currComp.PortList[i]);
            nextTest = "Return " + str(int(float(currComp.PortList[i])));
        except:
            nextTest = "GoTo " + currComp.PortList[i];

        if (str(i) in str(currComp.passPorts)):
            body = body + """
		Result {portNo}
		{{
			Property PassFail = "Pass";
			{nextTest};
		}}""".format(portNo=i, nextTest=nextTest);
        else:
            body = body + """
        Result {portNo}
        {{
	        Property PassFail = "Fail";
			{nextTest};
		}}""".format(portNo=i, nextTest=nextTest);

    return header + body + footer;

#############################
##### COMPOSITE WRAPPER #####
#############################
def printAHugeBoi(currComp, body, currModule):

    protectedFlows = ["INIT",
                      "START",
                      "BEGIN",
                      "PREHVQK",
                      "STRESS",
                      "POSTHVQK",
                      "END",
                      "ENDXFM",
                      "ENDTFM",
                      "EXVF",
                      "FINAL",
                      "SDTSTART",
                      "SDTBEGIN",
                      "HOTSTRESS",
                      "SDTEND",
                      "DEDC",
                      "SDTDEDC",
                      "TESTPLANSTARTFLOW",
                      "TESTPLANENDFLOW",
                      "DUTCHANGEFLOW",
                      "LOTSTARTFLOW",
                      "LOTENDFLOW"];

    currName = currComp.CompositeName;
    if currComp.CompositeName in protectedFlows:
        currName = currModule + "_" + currName + " @" + currName + "_SubFlow";
    header = """
DUTFlow {name}
{{""".format(name = currName);
    footer = "\n}";
    
    return header + body + footer;

#############################
##### PRINT OUT MACHINE #####
#############################
def printMeBaby(flowComposite, superString, currModule):
    
    compositeContents = "";
    for flowItem in flowComposite.Contents:
        
        if (isinstance(flowItem, type(Composite.Composite()))):
            compositeContents = compositeContents + printABigBoi(flowItem);
        if (isinstance(flowItem, type(TestInstance.TestInstance()))):
            compositeContents = compositeContents + printASmolBoi(flowItem, currModule);  
    fullComposite = printAHugeBoi(flowComposite, compositeContents, currModule);
    
    for flowItem in flowComposite.Contents:
        if (isinstance(flowItem, type(Composite.Composite()))):
            #print("composite found!");
            #print(flowItem.CompositeName);
            subCompositeString = printMeBaby(flowItem, "", currModule);
            superString = superString + subCompositeString;
            

    superString = superString + fullComposite;

    return superString;

####################
##### FUNCTION #####
####################
def dutflowBuilder(dataset, currModule):

    flowList = set(dataset.Flow);
    
    flowComposite = flowCursion(dataset, 0);
    outstring = "";
    for flow in flowComposite.Contents:
        outstring = outstring + printMeBaby(flow, "", currModule);

    return outstring;