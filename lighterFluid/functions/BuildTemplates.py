###################
###### SETUP ######
###################


####################
##### FUNCTION #####
####################

def checkParamExistsInAllTestsOfTheSameTemplate(testInstances, template, param):
    instanceDict = {};
    for module in testInstances:
        for instance_name, testInstance in testInstances[module].items():
            currTemplate = testInstance.Template
            if currTemplate == template:
                instanceDict[testInstance.TestName] = testInstances[module][instance_name];
        
    for testInstanceName, testInstance in instanceDict.items():
        if param not in testInstance.bonusCols:
            return False
    return True

def BuildTemplates(testInstanceDict, templateDir):
    # This function should build the test templates and .
    columnList = ["Flow",
                     "Template",
                     "TestName",
                     "IP",
                     "Module",
                     "TestType",
                     "EdcKill",
                     "DFT",
                     "PowerRail",
                     "VoltageCorner",
                     "FreqCorner",
                     "FreqNum",
                     "NameEnding",
                     "Levels",
                     "Timings",
                     "plist",
                     "IB",
                     "FB",
                     "Counter",
                     "bypassGlobal",
                     "killEnabled",
                     "flowX",
                     "flowY",
                     "portCount",
                     "passPorts",
                     "Port0",
                     "Port1",
                     "Port2",
                     "Port3",
                     "Port4",
                     "Port5",
                     "Port6",
                     "Port7",
                     "Port8",
                     "Port9",
                     ];
    combinedTestList = {};
    templateSet = set();
    templateDict = {}
    
    # Build the list of templates
    for module in testInstanceDict:
        for instance in testInstanceDict[module].values():
            currTemplate = instance.Template;
            templateSet.add(currTemplate);
            
            if currTemplate not in templateDict.keys():
                templateDict[currTemplate] = {};
                if currTemplate.startswith("i"):
                    templateDict[currTemplate]["code"] = "evg";
                else:
                    templateDict[currTemplate]["code"] = "prime";
                
                # We need to check if these are always set to their initial values.
                # If they are it means they aren't required to be added to the final template.
                # Simple example - AUX tests don't need them.
                templateDict[currTemplate]["bypassGlobal"] = set([instance.bypassGlobal]);
                templateDict[currTemplate]["Levels"] = set([instance.Levels]);
                templateDict[currTemplate]["Timings"] = set([instance.Timings]);
                templateDict[currTemplate]["plist"] = set([instance.plist]);
                templateDict[currTemplate]["bonusCols"] = {};
                
                for bonusCol in instance.bonusCols:
                    templateDict[currTemplate]["bonusCols"][bonusCol] = set([instance.bonusCols[bonusCol]]);

            else:
                templateDict[currTemplate]["Levels"].add(instance.Levels);
                templateDict[currTemplate]["Timings"].add(instance.Timings);
                templateDict[currTemplate]["plist"].add(instance.plist);
                
                for bonusCol in instance.bonusCols:
                    if bonusCol in templateDict[currTemplate]["bonusCols"].keys():
                        templateDict[currTemplate]["bonusCols"][bonusCol].add(instance.bonusCols[bonusCol]);
                    else:
                        templateDict[currTemplate]["bonusCols"][bonusCol] = set([instance.bonusCols[bonusCol]]);
    
    # Build the list of parameters called in each template.
    for template in templateDict:
        testStart = """Test {0} ###TestName###
{{
    """.format(template);
        testEnd = """
}""";
        
        paramList = []
        if templateDict[template]["code"] in ["evg"]:
            paramList.append("bypass_global = \"###bypassGlobal###\";");
            
            if (len(templateDict[template]["Levels"]) == 1):
                [element] = templateDict[template]["Levels"];
                if element != "x":
                    paramList.append("level = \"###Levels###\";");
            else:
                paramList.append("level = \"###Levels###\";");
            
            if (len(templateDict[template]["Timings"]) == 1):
                [element] = templateDict[template]["Timings"];
                if element != "x":
                    paramList.append("timings = \"###Timings###\";");
            else:
                paramList.append("timings = \"###Timings###\";");
            
            if (len(templateDict[template]["plist"]) == 1):
                [element] = templateDict[template]["plist"];
                if element != "x":
                    paramList.append("patlist = \"###plist###\";");
            else:
                paramList.append("patlist = \"###plist###\";");
        else:
            paramList.append("BypassPort = ###bypassGlobal###;");
            
            if (len(templateDict[template]["Levels"]) == 1):
                [element] = templateDict[template]["Levels"];
                if element != "x":
                   paramList.append("LevelsTc = \"###Levels###\";");
            else:
                paramList.append("LevelsTc = \"###Levels###\";");

            if (len(templateDict[template]["Timings"]) == 1):
                [element] = templateDict[template]["Timings"];
                if element != "x":
                    paramList.append("TimingsTc = \"###Timings###\";");
            else:
                paramList.append("TimingsTc = \"###Timings###\";");
            
            if (len(templateDict[template]["plist"]) == 1):
                [element] = templateDict[template]["plist"];
                if element != "x":
                    paramList.append("Patlist = \"###plist###\";");
            else:
                paramList.append("Patlist = \"###plist###\";");
        
        for param in templateDict[template]["bonusCols"]:
            
            if (len(templateDict[template]["bonusCols"][param]) > 1):
                paramList.append("{0} = \"###{0}###\";".format(param));
                if param not in columnList:
                    columnList.append(param);
            else:
                [element] = templateDict[template]["bonusCols"][param]

                isCommon = checkParamExistsInAllTestsOfTheSameTemplate(testInstanceDict, template, param)                

                if isCommon:
                    paramList.append("{0} = {1};".format(param,element));
                else:
                    paramList.append("{0} = \"###{0}###\";".format(param));
                    if param not in columnList:
                        columnList.append(param);
                    

        testMiddle = "\n    ".join(paramList);
        finalTest = testStart + testMiddle + testEnd;

        outFile = templateDir + template + ".txt";
        with open(outFile, 'w') as file:
            file.write(finalTest + "\n");       
        
    return columnList