#! /bin/python3

import os
import pickle

from HexaLibPython import HexaLog as HL


class Settings:
	SettingsFile = ".Settings.bin"
	SoftwareVersion = 0.3 # These should not be loaded, to avoid using old version when updated, but must be saved to check for old...
	DataVersion = 0.2 # These should not be loaded, to avoid using old version when updated...
	UserName = None
	MaxContextMsg = 100 # Max Number of messages to send to the AI. (Multiples of 2 recommended.)
	MaxTokens = 1900 # Max amount of total tokens.
	AutoContext = True # Auto / selected context inclusion.
	API = "OpenAI"
	AIModel = "gpt-3.5-turbo" # For now...
	Temperature = 0.2
	TopP = 0.95
	PresencePenalty = 0.0
	FrequencyPenalty = 0.0
	
	def __init__ (self, UserName = None):
		if UserName != None:
			self.UserName = UserName
		else:
			self.UserName = ""
			if os.path.isfile (self.SettingsFile):
				HL.Log ("Settings.py: Loading settings!", 'I', 8)
				with open (self.SettingsFile, "rb") as File:
					TempObj = pickle.load (File)
					self.UserName = TempObj.UserName
					self.MaxContextMsg = TempObj.MaxContextMsg
					self.MaxTokens = TempObj.MaxTokens
					self.AutoContext = TempObj.AutoContext
					try:
						if TempObj.SoftwareVersion == 0.2:
							HL.Log ("Settings.py: HexaPA version: v" + str (self.SoftwareVersion), 'I', 8)
							self.API = TempObj.API
							self.AIModel = TempObj.AIModel
						
						if TempObj.SoftwareVersion == 0.3:
							HL.Log ("Settings.py: HexaPA version: v" + str (self.SoftwareVersion), 'I', 8)
							self.API = TempObj.API
							self.AIModel = TempObj.AIModel
							Temperature = TempObj.Temperature
							TopP = TempObj.TopP
							PresencePenalty = TempObj.PresencePenalty
							FrequencyPenalty = TempObj.PresencePenalty
					except:
						pass
			else:
				HL.Log ("Settings.py: " + self.SettingsFile + " not found!", 'W', 8)
	
	
	
	def SaveSettings (self):
		TempObj = Settings (self.UserName)
		TempObj.MaxContextMsg = self.MaxContextMsg
		TempObj.MaxTokens = self.MaxTokens
		TempObj.AutoContext = self.AutoContext
		TempObj.SoftwareVersion = self.SoftwareVersion
		TempObj.API = self.API
		TempObj.AIModel = self.AIModel
		TempObj.Temperature = self.Temperature
		TempObj.TopP = self.TopP
		TempObj.PresencePenalty = self.PresencePenalty
		TempObj.PresencePenalty = self.FrequencyPenalty
		HL.Log ("Settings.py: Saving settings!", 'I', 8)
		with open (self.SettingsFile, "wb") as File:
			pickle.dump (TempObj, File)
