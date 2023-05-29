#! /bin/python3

import os
import re
import json

from HexaLibPython import HexaLog as HL
from Source.Options import *


class Commands:
	@staticmethod
	def Export (Key, Chain):
		if len (Chain.Blocks) > 0:
			### Create Export dir and filename...
			if not os.path.exists ("Export"):
				os.makedirs ("Export")
			JSONFile = "Export/" + re.sub ('[\W_]+', '_', Chain.CreationTime) + ".json"
			HL.Log ("GUI.py: Exporting conversation to: " + JSONFile, 'I', 2)
			
			### Export
			Extract = {"Subject": Chain.Subject, "CreationTime": Chain.CreationTime, "Blocks": []}
			for Block in Chain.Blocks:
				Extract["Blocks"].append (Block.DumpDict (Key))
			
			### Display
			if Args.verbose or Args.debug:
				print (json.dumps (Extract, indent = 4))
			
			### Save to file
			with open (JSONFile, 'w') as File:
				json.dump (Extract, File, indent = 4)
