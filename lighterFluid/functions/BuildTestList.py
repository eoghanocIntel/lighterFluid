
####################
##### FUNCTION #####
####################
def compositeContents(module, contents):
    testList = [];
    
    for flowItem in contents:
        testList.append(flowItem);
        if flowItem in module.keys():
            testList = testList + compositeContents(module,module[flowItem].Contents);
            testList.append("endComp_" + flowItem);

    return testList

def BuildTestList(module, testInstanceDict, compositeDict, moduleFlowList):
    # This function should build the test list.
    testList = ["TP_BEGIN"];
    currDict = compositeDict[module];

    for flow in moduleFlowList:
        if flow in currDict.keys():
            testList.append(flow);
            testList = testList + compositeContents(currDict, currDict[flow].Contents);
            testList.append("endSubflow_" + flow);
    testList = ["TP_END"];
    
    return testList