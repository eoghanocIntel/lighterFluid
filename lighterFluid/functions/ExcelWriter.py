import pandas as pd
import win32com.client
import os



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
                        if col in testInstanceDict[module][test].bonusColsStrings.keys():
                            newRow[col] = testInstanceDict[module][test].bonusColsStrings[col].strip("\"");
                        elif col in testInstanceDict[module][test].bonusColsIntegers.keys():
                            newRow[col] = testInstanceDict[module][test].bonusColsIntegers[col];
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
            df.to_excel(writer, sheet_name=sheet_name, freeze_panes=(1,3), index=False)
            workbook  = writer.book
            worksheet = writer.sheets[module];
            
            #START_STYLE
            #Style Section! Create a style format object for each flow type. We then apply each based on the flow name in the first column of each sheet
            #Composite_BEGIN/END and FLOW_BEGIN/END have bolder colours
            #https://htmlcolorcodes.com/color-names/
            #https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties
            header_format = workbook.add_format({
                #'fg_color': 'yellow', # You can change the background color here
                'bold': True,
                'underline':True,
                'border': 1})
            
            init_format = workbook.add_format({
                'fg_color': '#F5F5F5', # Light grey
                'border': 1}) 
            start_format = workbook.add_format({
                'fg_color': '#E5E4E2', # Platinum?
                'border': 1}) 
            
            begin_format = workbook.add_format({
                'fg_color': '#F0FFFF', # Light blue
                'border': 1})
            
            prehvqk_format = workbook.add_format({
                'fg_color': '#F0FFF0', # Light green
                'border': 1})  
            
            posthvqk_format = workbook.add_format({
                'fg_color': '#E6E6FA', # Lavender
                'border': 1})   
            
            stress_format = workbook.add_format({
                'fg_color': '#FFE4E1', # Light red
                'border': 1})
            
            end_format = workbook.add_format({
                'fg_color': '#E0FFFF', # Light cyan
                'border': 1}) 
            
            sdtend_format = workbook.add_format({
                'fg_color': '#FFF5EE', # Light orange
                'border': 1})
            
            exvf_format = workbook.add_format({
                'fg_color': '#FFFFE0', # Light yellow
                'border': 1}) 
            
            flow_begin_format = workbook.add_format({
                'fg_color': 'FDDA0D', # Yellow
                'bold': True,
                'underline':True,
                'border': 1}) 
            
            flow_end_format = workbook.add_format({
                'fg_color': 'FFA500', # Orange
                'bold': True,
                'underline':True,
                'border': 1})         
            
            # Write the column headers with the defined format.
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
                # Only works if XLSXWRITER version is greater than or equal to 3.0.6
                # Mine is 3.0.3 ;(
                # worksheet.autofit()

            ###END_STYLE                

            rows = df.shape[0]
            # for i, (testName, template) in enumerate(zip(df['TestName'], df['Template']), start=1):
            #     if template not in ["TP_BEGIN","COMPOSITE_BEGIN","COMPOSITE_END","TP_END"]:
            #         formula_to_write = 'D{0}&"_"&E{0}&"_"&F{0}&"_"&A{0}&"_"&G{0}&"_"&H{0}&"_"&I{0}&"_"&J{0}&"_"&K{0}&"_"&L{0}&"_"&M{0}'.format(i+1) 
            #         worksheet.write_formula(i, df.columns.get_loc('TestName'), formula_to_write);
            
            #Apply row colours based on the flow name in the first column. Xlsxwriter row numbers begin at 1, so we need to target row+1 with the cell_format to keep evrything in line
            for row_num in range(rows):
                row_values = df.values[row_num]
                row_value = row_values[0]
                template_value = row_values[1]
                
                if row_value == 'INIT':
                    worksheet.set_row(row_num+1, cell_format=init_format)
                
                if row_value == 'START':
                    worksheet.set_row(row_num+1, cell_format=start_format)  
                    
                if row_value == 'BEGIN':
                    worksheet.set_row(row_num+1, cell_format=begin_format)  
                    
                if row_value == 'PREHVQK':
                    worksheet.set_row(row_num+1, cell_format=prehvqk_format)  
                    
                if row_value == 'STRESS':
                    worksheet.set_row(row_num+1, cell_format=stress_format)  
                    
                if row_value == 'SDTEND':
                    worksheet.set_row(row_num+1, cell_format=sdtend_format)   
                    
                if row_value == 'POSTHVQK':
                    worksheet.set_row(row_num+1, cell_format=posthvqk_format)  
                    
                if row_value == 'END':
                    worksheet.set_row(row_num+1, cell_format=end_format)  
                    
                if row_value == 'EXVF':
                    worksheet.set_row(row_num+1, cell_format=exvf_format)
                    
                if template_value == 'COMPOSITE_BEGIN':
                    worksheet.set_row(row_num+1, cell_format=flow_begin_format)  
                    
                if template_value == 'COMPOSITE_END':
                    worksheet.set_row(row_num+1, cell_format=flow_end_format)      
                 
            for i, (passPort) in enumerate(df['passPorts'], start=1):
                formula_to_write = 'COUNTA(AA{0}:AJ{0})'.format(i+1) 
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
    # tempOutFile = "C:\\Users\\eoghanoc\\source\\repos\\lighterFluid\\lighterFluid\\heavierFluidOutputs\\lnlBackConvert.xlsx"
    # workbook = excel.Workbooks.open(tempOutFile)
    cwd = os.getcwd()
    workbook = excel.Workbooks.open(cwd + "\\" + outFile)
    workbook.Save()
    excel.Quit()