import pandas
from . import FlowComposite
from . import FlowTestInstance

##################
##### BASICS #####
##################
flowBegin = """<?xml version="1.0" encoding="utf-8"?>
<!--File is auto-generated, any manual edits can be overwritten.-->
<!DOCTYPE HDMTFlowItemCoor []>
<HDMTFlowItemCoor>
""";

flowEnd = """
</HDMTFlowItemCoor>
"""

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
                "SDTSTRESS",
                "SDTEND",
                "DEDC",
                "SDTDEDC",
                "TESTPLANSTARTFLOW",
                "TESTPLANENDFLOW",
                "DUTCHANGEFLOW",
                "LOTSTARTFLOW",
                "LOTENDFLOW"];


#############################
##### RECURSION MACHINE #####
#############################
def flowFileCursion(dataset, rowCount, parent):
    ##################
    ##### BASICS #####
    ##################
    flowDict = {};
    flowSection = "";

    i = rowCount;
    contentList = [];

    currComposite = FlowComposite.FlowComposite();
    currComposite.CompositeName = dataset.TestName[i].rstrip("_");
    currComposite.flowX = dataset.flowX[i];
    currComposite.flowY = dataset.flowY[i];
    currComposite.Contents = [];
    currComposite.Module = dataset.Module[i];
    currComposite.Parent = parent;


    i = i+1;
    
    while (i < len(dataset.Template)):
        # If we have a nested composite, need to start recursion
        if ("COMPOSITE_BEGIN" in dataset.Template[i]):
            (subComposite, i) = flowFileCursion(dataset, i,currComposite.CompositeName);
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

        currTest = FlowTestInstance.FlowTestInstance();
        # Assuming this is a chain ender - we need to assign ports
        currTest.TestName = dataset.TestName[i].rstrip("_");
        currTest.flowX = dataset.flowX[i];
        currTest.flowY = dataset.flowY[i];
        currTest.Module = dataset.Module[i];
        currTest.parentComposite = currComposite.CompositeName;

        currComposite.Contents.append(currTest);

        i = i+1;

    return currComposite


##############################
##### INSTANCE PRINT OUT #####
##############################
def printASmolBoiFlow(currTest, currModule):
    
    parentComposite = currTest.parentComposite;
    testInstance = currTest.TestName.rstrip("_");
    x = str(int(float(currTest.flowX) * 150));
    y = str(int(float(currTest.flowY) * 250));
    
    if(parentComposite in protectedFlows):
        parentComposite = currModule + "_" + parentComposite;
    
    flowPrint = "  <FlowItem name=\"{currModule}::{parentComposite}.{testInstance}\" X=\"{x}\" Y=\"{y}\" />\n".format(
        currModule=currModule,
        parentComposite=parentComposite,
        testInstance=testInstance,
        x=x,
        y=y)

    return flowPrint;

#############################
##### COMPOSITE WRAPPER #####
#############################
def printABigBoiFlow(currComp, currModule):
    
    parentComposite = currComp.Parent;
    testInstance = currComp.CompositeName;
    x = str(int(float(currComp.flowX) * 150));
    y = str(int(float(currComp.flowY) * 250));
    
    if(parentComposite in protectedFlows):
        parentComposite = currModule + "_" + parentComposite;

    flowPrint = "  <FlowItem name=\"{currModule}::{parentComposite}.{testInstance}\" X=\"{x}\" Y=\"{y}\" />\n".format(
        currModule=currModule,
        parentComposite=parentComposite,
        testInstance=testInstance,
        x=x,
        y=y)
    
    return flowPrint;

#############################
##### PRINT OUT MACHINE #####
#############################
def printMeBaby(flowComposite, superString, currModule):
    
    compositeContents = "";
    for flowItem in flowComposite.Contents:
        
        if (isinstance(flowItem, type(FlowComposite.FlowComposite()))):
            compositeContents = compositeContents + printABigBoiFlow(flowItem,currModule);
        if (isinstance(flowItem, type(FlowTestInstance.FlowTestInstance()))):
            compositeContents = compositeContents + printASmolBoiFlow(flowItem, currModule);  
    fullComposite = superString + compositeContents;

    for flowItem in flowComposite.Contents:
        if (isinstance(flowItem, type(FlowComposite.FlowComposite()))):
            #print("composite found!");
            #print(flowItem.CompositeName);
            # subCompositeString = printMeBaby(flowItem, "");
            # superString = superString + subCompositeString;
    
            fullComposite = printMeBaby(flowItem, fullComposite, currModule);
            

    # superString = superString + fullComposite;

    return fullComposite;

####################
##### FUNCTION #####
####################
def flowFileBuilder(dataset, currModule):
    # This function should build the flow file
    # Input file expectation is that each test will have an associated flowX/flowY.
    
    flowComposite = flowFileCursion(dataset, 0, "NA");
    outstring = flowBegin;
    
    for flow in flowComposite.Contents:
        outstring = outstring + printMeBaby(flow, "", currModule);
    
    outstring = outstring + flowEnd;
    return outstring;