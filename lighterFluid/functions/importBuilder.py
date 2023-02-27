import pandas

##################
##### BASICS #####
##################
importBegin = """
Version 1.0;

ProgramStyle = Modular;
""";

importList = [];

####################
##### FUNCTION #####
####################
def importBuilder(dataset):
    # This function should build the top section of the mtpl.
    # Mainly it'll build the "Import" section

    currModule = list(set(dataset.Module.dropna()))[0];
    testPlan = "TestPlan ARR_" + currModule + ";\n";
    uservar = "Import ARR_" + currModule + ".usrv;\n";

    importSet = set(dataset.TemplateLookup);

    for template in importSet:
        if("COMPOSITE" in template):
            continue;
        if template.startswith("iC"):
            template = template.replace("iC","OASIS_");
            template = template.replace("Test","_tt");
        importList.append("Import " + template + ".xml;");


    importSection = importBegin + testPlan + uservar + "\n" + "\n".join(importList);
    return importSection;