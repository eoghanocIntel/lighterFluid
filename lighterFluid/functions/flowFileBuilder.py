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
        if("COMPOSITE" in dataset.Template[i]):
            continue;
        
        currTest = dataset.TestName[i];

        for j in range(0,int(dataset.portCount[i])):
            # we need to check if the current port is in the pass port list (ignore if so)
            if str(j) in dataset.passPorts[i]:
                continue;
            else:
                counterData = dummyCounter + currTest + "_" + str(j); 
                counterList.append(counterData);

    counterSection = counterBegin + ",\r\n".join(counterList) + counterEnd;
    return counterSection;