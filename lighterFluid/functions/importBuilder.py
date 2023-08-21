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
def importBuilder(dataset, timeStamp):
    # This function should build the top section of the mtpl.
    # Mainly it'll build the "Import" section
    
    importList = [];

    importTimeStamp = "# " + timeStamp + "\n";
    
    #currModule = list(set(dataset.Module.dropna()))[0];
    currModule = dataset.Module[0];

    #if len(currModule) > 0:
    #    currModule = "COMMON";
    testPlan = "TestPlan ARR_" + currModule + ";\n";
    uservar = "Import ARR_" + currModule + ".usrv;\n";
    
    importSection = importBegin + importTimeStamp + testPlan + uservar + "\n";
    
    for timing in dataset.Timings.dropna():
        if timing.startswith("BASE"):
            continue
        else:
            importSection = importSection + "Import ARR_" + currModule + "_timings.tcg;\n";
            break
        
    for level in dataset.Levels.dropna():
        if level.startswith("BASE"):
            continue
        else:
            importSection = importSection + "Import ARR_" + currModule + "_levels.tcg;\n";
            break

    importSet = set(dataset.TemplateLookup);

    for template in sorted(importSet):
        if("COMPOSITE" in template):
            continue;
        if template.startswith("iC"):
            template = template.replace("iC","OASIS_");
            template = template.replace("Test","_tt");
        importList.append("Import " + template + ".xml;");

        
    importSection = importSection + "\n".join(importList);
    return importSection;