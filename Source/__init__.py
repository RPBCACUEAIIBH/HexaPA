#! /bin/python3
print (__file__)

import os
import glob

# Dynamic import order in inconsistent! This needs to be imported first, otherwise it cause attribute errors...
from .LogTrace import *

DirectoryPath = os.path.dirname (__file__)
for ModulePath in glob.glob (os.path.join (DirectoryPath, "*.py")):
	if ModulePath == __file__ or os.path.basename (ModulePath).startswith ("_"):
		continue
	ModuleName = os.path.basename (ModulePath)[:-3]
	try:
		#print (f"Debug: Importing {ModuleName}...")
		exec (f"from .{ModuleName} import *")
	except Exception as e:
		print (__file__)
		print (f"Failed to import module {ModuleName}: {e}")
