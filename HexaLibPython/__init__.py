#! /bin/python3


import os
import glob

DirectoryPath = os.path.dirname (__file__)
for ModulePath in glob.glob (os.path.join (DirectoryPath, "*.py")):
	if ModulePath == __file__ or os.path.basename (ModulePath).startswith ("_"):
		continue
	ModuleName = os.path.basename (ModulePath)[:-3]
	print (f"Debug: Importing {ModuleName}...")
	try:
		exec (f"from .{ModuleName} import *")
	except Exception as e:
		print (__file__)
		print (f"Failed to import module {ModuleName}: {e}")
