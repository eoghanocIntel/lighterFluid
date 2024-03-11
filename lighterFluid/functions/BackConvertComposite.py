class my_class(object):
    pass




class BackConvertComposite:
    
    def __init__(self):

        # In the flow we're going to have "mandatory" items defined. 
        # These are columns that are guaranteed to exist in the Excel.

        # Needed for test name
        self.Flow = "";
        self.Template = "";
        self.TestName = "";
        self.Module = "";
        
        # Flow items, porting and the like
        self.flowX = "0";
        self.flowY = "0";
        self.portCount = "";
        self.passPorts = [];
        self.PortList = [];

        self.Contents = [];
