import pandas as pd


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
            for test in testPrintOutList:
                newRow = {};
                
                if test in compositeDict[module].keys():
                    i=0
                elif test in testInstanceDict[module].keys():
                    for col in addedColsList:
                        if col in testInstanceDict[module][test].bonusCols.keys():
                            newRow[col] = testInstanceDict[module][test].bonusCols[col];
                        else:
                            try:
                                newRow[col] = getattr(testInstanceDict[module][test],col);
                            except:
                                continue;
                    df = df.append(pd.DataFrame(newRow), ignore_index = True);
        
            # add some formulas to make life easier :)
            # df['Template'] = df.apply(testNameReplace, axis=1)
            
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            worksheet = writer.sheets[module];

            rows = df.shape[0]
            for i, (testName, flow) in enumerate(zip(df['TestName'], df['Flow']), start=1):
                if flow not in ["TP_BEGIN","COMPOSITE_BEGIN","COMPOSITE_END","TP_END"]:
                    formula_to_write = 'D{0}&"_"&E{0}&"_"&F{0}&"_"&A{0}&"_"&G{0}&"_"&H{0}&"_"&I{0}&"_"&J{0}&"_"&K{0}&"_"&L{0}&"_"&M{0}'.format(i+1) 
                    worksheet.write_formula(i, df.columns.get_loc('TestName'), formula_to_write);