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
def importBuilder(dataset, moduleName):
    # This function should build the top section of the mtpl.
    # Mainly it'll build the "Import" section
    
    importList = [];

    testPlan = "TestPlan " + moduleName + ";\n";
    uservar = "Import " + moduleName + ".usrv;\n";
    timing = "#Import " + moduleName + "_timings.tcg;\n";

    importSet = set(dataset.TemplateLookup);

    for template in importSet:
        if("COMPOSITE" in template):
            continue;
        if template.startswith("iC"):
            template = template.replace("iC","OASIS_");
            template = template.replace("Test","_tt");
        importList.append("Import " + template + ".xml;");


    importSection = importBegin + testPlan + "\n" + uservar + timing + "\n" + "\n".join(importList);
    #importSection = importBegin + testPlan + uservar + "\n" + "\n".join(importList);
    return importSection;