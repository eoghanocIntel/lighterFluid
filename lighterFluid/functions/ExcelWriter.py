import pandas as pd
import win32com.client



def WriteToExcel(outFile, moduleList, addedColsList, compositeDict, testInstanceDict, testPrintOutList):

    with pd.ExcelWriter(outFile, engine='xlsxwriter') as writer:
        for module in moduleList:
            # doTheThing
    
            sheet_name = f'{module}';
        
            tableData = {};
            for col in addedColsList:
                tableData[col] = [];
    
            df = pd.DataFrame(tableData)
    
            # df.to_excel(outFile, index=False)

            # Build the basic table
            for lineNo, test in enumerate(testPrintOutList[module]):
                newRow = {};
                
                if test.startswith("endComp"):
                    newRow["Template"] = "COMPOSITE_END";
                    actualCompName = test[8:];
                    newRow["Flow"] = compositeDict[module][actualCompName].Flow;
                    newRow["TestName"] = test;
                    tempModule = module.split('_')[1].upper();
                    newRow["Module"] = tempModule;
                
                elif test.startswith("endSubflow"):
                    newRow["Template"] = "COMPOSITE_END";
                    actualCompName = test[11:];
                    newRow["Flow"] = compositeDict[module][actualCompName].Flow;
                    newRow["TestName"] = test;
                    tempModule = module.split('_')[1].upper();
                    newRow["Module"] = tempModule;
                
                elif test in compositeDict[module].keys():
                    for col in addedColsList:
                        if col in ["passPorts"]:
                            newRow[col] = ",".join(compositeDict[module][test].passPorts).strip("\"")
                            continue;
                        try:
                            newRow[col] = getattr(compositeDict[module][test],col).strip("\"");
                        except:
                            continue;   

                    # Overwrite COMPOSITE_BEGIN, clean up ports
                    newRow["Template"] = ["COMPOSITE_BEGIN"];
                    for i, port in enumerate(compositeDict[module][test].PortList):
                        newRow["Port" + str(i)] = port;
                
                elif test in testInstanceDict[module].keys():
                    for col in addedColsList:
                        if col in testInstanceDict[module][test].bonusCols.keys():
                            newRow[col] = testInstanceDict[module][test].bonusCols[col].strip("\"");
                        else:
                            if col in ["passPorts"]:
                                newRow[col] = ",".join(testInstanceDict[module][test].passPorts).strip("\"");  
                                continue;
                            try:
                                newRow[col] = getattr(testInstanceDict[module][test],col).strip("\"");
                            except:
                                continue;
                    for i, port in enumerate(testInstanceDict[module][test].PortList):
                        newRow["Port" + str(i)] = port;
                    newRow["TestName"] = '=D{0}&"_"&E{0}&"_"&F{0}&"_"&G{0}&"_"&A{0}&"_"&H{0}&"_"&I{0}&"_"&J{0}&"_"&K{0}&"_"&L{0}&"_"&M{0}'.format(lineNo+2);

                elif test in ["TP_BEGIN","TP_END"]:
                    newRow["Flow"] = "TP";
                    newRow["Template"] = test;
                    newRow["TestName"] = "TP";
                    tempModule = module.split('_')[1].upper();
                    newRow["Module"] = tempModule;
                
                df = pd.concat([df,pd.DataFrame(newRow, index = [0])], ignore_index = True);
                    
        
            # add some formulas to make life easier :)
            # df['Template'] = df.apply(testNameReplace, axis=1)
            
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            worksheet = writer.sheets[module];

            rows = df.shape[0]
            # for i, (testName, template) in enumerate(zip(df['TestName'], df['Template']), start=1):
            #     if template not in ["TP_BEGIN","COMPOSITE_BEGIN","COMPOSITE_END","TP_END"]:
            #         formula_to_write = 'D{0}&"_"&E{0}&"_"&F{0}&"_"&A{0}&"_"&G{0}&"_"&H{0}&"_"&I{0}&"_"&J{0}&"_"&K{0}&"_"&L{0}&"_"&M{0}'.format(i+1) 
            #         worksheet.write_formula(i, df.columns.get_loc('TestName'), formula_to_write);
                    
            for i, (passPort) in enumerate(df['passPorts'], start=1):
                formula_to_write = 'COUNTA(Z{0}:AI{0})'.format(i+1) 
                worksheet.write_formula(i, df.columns.get_loc('portCount'), formula_to_write);
            
            for i in range(0,10):
                for j, (port) in enumerate(df['Port' + str(i)], start=1):
                    if port in testPrintOutList[module]:
                        rowLookup = testPrintOutList[module].index(port);
                        # adding 2, 1 for 0 index (excel isn't), 1 for the row header
                        formula_to_write = '$C{0}'.format(rowLookup+2) 
                        worksheet.write_formula(j, df.columns.get_loc('Port' + str(i)), formula_to_write);

    # After all is said and done we need to do something painful... Open the Excel and Close it again - so that the formulas save properly...
    excel = win32com.client.Dispatch("Excel.Application")
   # workbook = excel.Workbooks.open("C:\\Users\\adambyrn\\source\\repos\\lighterFluid\\lighterFluid\\heavierFluidOutputs\\heavierExcel_LNL.xlsx")
    workbook = excel.Workbooks.open("C:\\Users\\adambyrn\\source\\repos\\lighterFluid\\lighterFluid\\heavierFluidOutputs\\heavierExcel_PTL.xlsx")
    workbook.Save()
    excel.Quit()