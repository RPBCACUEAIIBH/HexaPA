#! /bin/python3

import os
import re
import json

from HexaLibPython import HexaLog as HL
from Source.Options import *
from Source.Tokenizer import *
from Source.Data import *


class Commands:
	@staticmethod
	def Export (Key, Chain):
		if len (Chain.Blocks) > 0:
			### Create Export dir and filename...
			if not os.path.exists ("Export"):
				os.makedirs ("Export")
			JSONFile = "Export/" + re.sub ('[\W_]+', '_', Chain.CreationTime) + ".json"
			HL.Log ("Commands.py: Exporting conversation to: " + JSONFile, 'I', 9)
			
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
	
	
	
	@staticmethod
	def GenerateContext (Key, SettingsObj, MsgList, MaxContextTokens):
		# Init...
		Context = None
		ContextIDs = None
		Offset = 1
		ContextCount = 0
		MessageData = Data ()
		ContextTokens = 0
		
		# Compensate for excluded messages...
		for i in range (1, len (MsgList) + 1): # This loop compensates for excluded messages, otherwise if you exclude messages, less then max allowd messages are even considered...
			Index = len (MsgList) - i
			if Index < 0: # New conversation -> less then max allowed messages...
				HL.Log ("Commands.py: Loop exiting at Index: " + str (Index) + ", i: " + str (i) + ", FinalContextCount: " + str (ContextCount), 'D', 9)
				break
			MessageData.Parse (Key, MsgList[Index].Data, MsgList[Index].BlockID)
			if MessageData.DataType != "Message":
				Offset += 1
				HL.Log ("Commands.py: Skipping non-\"Message\" type block at index: " + str (Index), 'D', 9)
				continue
			elif MsgList[Index].Rating >= 0 and SettingsObj.AutoContext == True or MsgList[Index].Rating > 0:
				ContextCount += 1
				if ContextCount == SettingsObj.MaxContextMsg:
					HL.Log ("Commands.py: Loop exiting at Index: " + str (Index) + ", i: " + str (i) + ", FinalContextCount: " + str (ContextCount), 'D', 9)
					break
			else:
				HL.Log ("Commands.py: Message to be excluded at index: " + str (Index), 'D', 9)
				Offset += 1
		
		# Create list of messages...
		for i in range (1, SettingsObj.MaxContextMsg + Offset + 1):
			Index = len (MsgList) - i
			if Index < 0: # New conversation -> less then max allowed messages...
				HL.Log ("Commands.py: Loop exitted at Index: " + str (Index) + ", i: " + str (i), 'D', 9)
				break
			MessageData.Parse (Key, MsgList[Index].Data, MsgList[Index].BlockID)
			if MessageData.DataType != "Message":
				HL.Log ("Commands.py: Skipping non-\"Message\" type block at index: " + str (Index), 'D', 9)
				continue
			elif MsgList[Index].Rating >= 0:
				HL.Log ("Commands.py: Considering message at index: " + str (Index), 'D', 9)
				if SettingsObj.AutoContext == False and MsgList[Index].Rating < 1:
					HL.Log ("Commands.py: Skipping message not marked for inclusion in selective inclusion mode.", 'D', 9)
					continue
				if MessageData.Name == SettingsObj.UserName:
					ContextMessage = {"role": "user", "content": MessageData.Message}
				else:
					ContextMessage = {"role": "assistant", "content": MessageData.Message}
				if MaxContextTokens >= ContextTokens + Tokenizer.Count ("OpenAI", "gpt-3.5-turbo", "role: " + ContextMessage["role"] + ", content: " + ContextMessage["content"]):
					ContextTokens += Tokenizer.Count ("OpenAI", "gpt-3.5-turbo", "role: " + ContextMessage["role"] + ", content: " + ContextMessage["content"])
					HL.Log ("Commands.py: Message included!", 'D', 9)
					if Context == None:
						Context = []
						ContextIDs = []
					Context.insert (0, ContextMessage)
					ContextIDs.insert (0, MessageData.BlockID)
					ContextCount -= 1
					HL.Log ("Commands.py: Remaining ContextCount: " + str (ContextCount), 'D', 9)
				else:
					HL.Log ("Commands.py: Message too large!", 'D', 9)
					HL.Log ("Commands.py: Loop exiting at Index: " + str (Index) + ", i: " + str (i), 'D', 9)
					break
		
		HL.Log ("Commands.py: FinalContextCount: " + str (SettingsObj.MaxContextMsg - ContextCount), 'D', 9)
		return ContextIDs, Context