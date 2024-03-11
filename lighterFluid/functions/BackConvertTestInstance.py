class my_class(object):
    pass




class BackConvertTestInstance:
    
    def __init__(self):

        # In the flow we're going to have "mandatory" items defined. 
        # These are columns that are guaranteed to exist in the Excel.

        # Needed for test name
        self.Flow = "";
        self.Template = "";
        self.TestName = "";
        self.IP = "";
        self.Module = "";
        self.TestType = "";
        self.EdcKill = "";
        self.DFT = "";
        self.PowerRail = "";
        self.VoltageCorner = "";
        self.FreqCorner = "";
        self.FreqNum = "";
        self.NameEnding = "";
        
        # Default params always needed
        self.Levels = "x";
        self.Timings = "x";
        self.plist = "x";
        self.IB = "";
        self.FB = "";
        self.Counter = "";
        self.bypassGlobal = "";
        self.killEnabled = "";
        
        # Flow items, porting and the like
        self.flowX = "0";
        self.flowY = "0";
        self.portCount = "";
        self.passPorts = [];
        self.PortList = [];

        # Finally, the bonus params :D
        self.bonusCols = {};