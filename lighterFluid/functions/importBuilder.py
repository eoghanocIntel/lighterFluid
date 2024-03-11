import pandas

##################
##### BASICS #####
##################
importBegin = """
Version 1.0;

ProgramStyle = Modular;
""";

####################
##### FUNCTION #####
####################
def importBuilder(dataset, timeStamp, currModule):
    # This function should build the top section of the mtpl.
    # Mainly it'll build the "Import" section
    
    importList = [];

    importTimeStamp = "# " + timeStamp + "\n";
    
    #currModule = list(set(dataset.Module.dropna()))[0];
    # currModule = dataset.Module[0];

    #if len(currModule) > 0:
    #    currModule = "COMMON";
    testPlan = "TestPlan " + currModule + ";\n";
    uservar = "Import " + currModule + ".usrv;\n";
    
    importSection = importBegin + importTimeStamp + testPlan + uservar + "\n";
    
    timingsList = list(filter(None, dataset.Timings.dropna()))
    levelsList = list(filter(None, dataset.Levels.dropna()))

    for timing in timingsList:
        if (timing.startswith("BASE") or timing == "x"):
            continue
        else:
            importSection = importSection + "Import " + currModule + "_timings.tcg;\n";
            break
        
    for level in levelsList:
        if (level.startswith("BASE") or level == "x"):
            continue
        else:
            importSection = importSection + "Import " + currModule + "_levels.tcg;\n";
            break

    importSet = set(dataset.Template);

    for template in sorted(importSet):
        if("COMPOSITE" in template):
            continue;
        if("TP_BEGIN" in template):
            continue;
        if("TP_END" in template):
            continue;
        if template.startswith("iC"):
            template = template.replace("iC","OASIS_");
            template = template.replace("Test","_tt");
        importList.append("Import " + template + ".xml;");

        
    importSection = importSection + "\n".join(importList);
    return importSection;