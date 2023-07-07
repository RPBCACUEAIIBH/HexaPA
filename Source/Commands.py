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
	def ExportChatJSON (Key, Chain):
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
			
			### Save to file
			with open (JSONFile, 'w') as File:
				json.dump (Extract, File, indent = 4)
			
			### Display
			#if Args.verbose or Args.debug: # FIX THIS !!! I cloned another instance of HexaPA on the same machine, same OS, same user, neither is running in venv, and the second instance gives an Args is not defined error, the first one doesn't, no difference in the code I'm at the same branch, same commit for both... (I put this at the end so that at least it should save the file before error...)
			#	print (json.dumps (Extract, indent = 4))
	
	
	
	@staticmethod
	def ImportChatJSON (Key, Chain, JSONFile): # This can load an entire chain, or an extracted portion as long as order is kept, and all referenced blocks are found.
		# Initial stuff...
		with open (JSONFile) as File:
			RawData = json.load (File)
		
		Blocks = RawData["Blocks"]
		BlockMapping = {}
		
		# Subject, CreationTime, and File
		Chain.Subject = RawData["Subject"]
		Chain.CreationTime = RawData["CreationTime"]
		if Chain.File == None:
			Chain.File = "Conversations/" + re.sub ('[\W_]+', '_', Chain.CreationTime) + ".bin"
			if os.path.exists (Chain.File):
				HL.Log ("Commands.py: File " + Chain.File + " already exists. Aborting import operation!", 'E', 9)
				Chain.File = None
				return
			else:
				HL.Log ("Commands.py: Chat will be saved to: " + Chain.File, 'D', 9)
		
		for Block in Blocks:
			# Map old IDs to new IDs
			BlockMapping[Block["ID"]] = len (Chain.Blocks)
			
			# Import Data
			BlockData = Data ()
			BlockData.ImportDict (Block["Data"])
			
			# Set new Rules ID
			if BlockData.DataType == "Message" and BlockData.Name != "HexaPA":
				BlockData.Rules = Chain.LatestRules
			
			# Set new context IDs
			NewList = []
			for ContextID in BlockData.Context:
				NewList.append (BlockMapping[ContextID])
			BlockData.Context = NewList
			
			# Add to chain...
			Chain.ImportBlock (Block["TimeStamp"], BlockData.Dump (Key), Block["Rating"])
			#Chain.Blocks[len (Chain.Blocks) - 1].Sign ()
			
			# Update LatestRules ID...
			if BlockData.DataType == "Rules":
				Chain.LatestRules = Chain.Blocks[len (Chain.Blocks) - 1].BlockID
	
	
	
	@staticmethod
	def ExportRulesJSON (Key, Chain, BlockID, PresetTitle):
		if len (Chain.Blocks) > 0:
			# Create Export dir and filename...
			if not os.path.exists ("Presets/UserPresets"):
				os.makedirs ("Presets/UserPresets")
			JSONFile = "Presets/UserPresets/" + re.sub ('[\W_]+', '_', PresetTitle) + ".json"
			HL.Log ("Commands.py: Exporting rules to: " + JSONFile, 'I', 9)
			
			# Export
			Extract = {"Title": PresetTitle, "Description": "", "Blocks": []} # Originally I planned to define just a Rules type block, but example context should be added as well.
			Extract["Blocks"].append (Chain.Blocks[BlockID].DumpDict (Key))
			
			# Save to file
			with open (JSONFile, 'w') as File:
				json.dump (Extract, File, indent = 4)
			
			# Display
			#if Args.verbose or Args.debug: # FIX THIS !!! I cloned another instance of HexaPA on the same machine, same OS, same user, neither is running in venv, and the second instance gives an Args is not defined error, the first one doesn't, no difference in the code I'm at the same branch, same commit for both... (I put this at the end so that at least it should save the file before error...)
			#	print (json.dumps (Extract, indent = 4))
	
	
	
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
