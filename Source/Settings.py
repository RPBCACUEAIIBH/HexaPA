#! /bin/python3

import os
import pickle

from HexaLibPython import HexaLog as HL


class Settings:
	SettingsFile = ".Settings.bin"
	SoftwareVersion = 0.1 # These should not be loaded, to avoid using old version when updated...
	DataVersion = 0.2 # These should not be loaded, to avoid using old version when updated...
	UserName = None
	MaxContextMsg = 10 # Max Number of messages to send to the AI. (Multiples of 2 recommended.)
	MaxTokens = 1000 # Max amount of total tokens.
	AutoContext = True # Auto / selected context inclusion.
	
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
			else:
				HL.Log ("Settings.py: " + self.SettingsFile + " not found!", 'W', 8)
	
	
	
	def SaveSettings (self):
		TempObj = Settings (self.UserName)
		TempObj.MaxContextMsg = self.MaxContextMsg
		TempObj.MaxTokens = self.MaxTokens
		TempObj.AutoContext = self.AutoContext
		HL.Log ("Settings.py: Saving settings!", 'I', 8)
		with open (self.SettingsFile, "wb") as File:
			pickle.dump (TempObj, File)
