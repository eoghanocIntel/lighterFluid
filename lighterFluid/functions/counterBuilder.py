import pandas

##################
##### BASICS #####
##################
counterBegin = """
Counters
{
""";

counterEnd = """
} # End of Test Counter Definition
"""

counterList = [];
dummyCounter = "\tn60000000_fail_";

####################
##### FUNCTION #####
####################
def counterBuilder(dataset):
    # This function should build the counter list.
    # Input file expectation is that each test will have an associated number of ports, some of whom will be fail ports.
    # Composites will have Test names and ports, but no counters.

    for i in range(0,len(dataset.TestName)):
        # ignore composites
        if(("COMPOSITE" in dataset.Template[i]) or ("TP_BEGIN" in dataset.Template[i]) or ("TP_END" in dataset.Template[i])):
            continue;

        currTest = dataset.TestName[i];
        currIb = str(int(dataset.IB[i]));
        currFb = str(int(dataset.FB[i]));
        currCounter = str(int(dataset.Counter[i]));
        currPheoBin = currIb.zfill(2) + currFb.zfill(2) + currCounter.zfill(4);

        for j in range(0,int(dataset.portCount[i])):
            # we need to check if the current port is in the pass port list (ignore if so)
            if str(j) in str(dataset.passPorts[i]):
                continue;
            else:
                counterData = "\tn" + currPheoBin + "_fail_" + currTest + "_" + str(j); 
                counterList.append(counterData);

    counterSection = counterBegin + ",\n".join(counterList) + counterEnd;
    return counterSection;