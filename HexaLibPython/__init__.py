#! /bin/python3


import os
import glob

DirectoryPath = os.path.dirname (__file__)
for ModulePath in glob.glob(os.path.join (DirectoryPath, "*.py")):
    if ModulePath == __file__ or os.path.basename (ModulePath).startswith ("_"):
        continue
    ModuleName = os.path.basename (ModulePath)[:-3]
    exec (f"from .{ModuleName} import *")
