import sys
import xml.etree.ElementTree
import os
import csv
import subprocess
from os.path import expanduser
 
python_exe = sys.executable
 
print("need to import pandas using pip");
subprocess.call(python_exe + ' -m pip install openpyxl --proxy="http://proxy-chain.intel.com:911"')