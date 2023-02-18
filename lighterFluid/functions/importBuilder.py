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
    uservar = "Import ARR_" + currModule + ".usvr;\n";

    importSet = set(dataset.Template);

    for template in importSet:
        if("COMPOSITE" in template):
            continue;
        importList.append("Import " + template + ".xml;");


    importSection = importBegin + testPlan + uservar + "\n" + "\n".join(importList);
    return importSection;