#! /bin/python3

import os
import pickle

from HexaLibPython import HexaLog as HL
import Source.LogTrace as LogT
import Source.TempDir


class Settings:
	SettingsFile = ".Settings.bin"
	SoftwareVersion = 0.5 # These should not be loaded, to avoid using old version when updated, but must be saved to check for old...
	DataVersion = 0.2 # These should not be loaded, to avoid using old version when updated...
	UserName = None
	MaxContextMsg = 100 # Max Number of messages to send to the AI. (Multiples of 2 recommended.)
	MaxTokens = 2048 # Max amount of Input tokens.
	MaxOTokens = 512 # Max amount of Output tokens.
	AutoContext = True # Auto / selected context inclusion.
	API = "OpenAI"
	AIModel = "gpt-4o-mini" # For now...
	OpenAI_DefaultModel = "gpt-4o-mini"
	DeepSeek_DefaultModel = "deepseek-chat"
	WorkDir = Source.TempDir.TempDir ()
	TTSModel = "tts-1"
	TTSVoiceMale = "onyx"
	TTSVoiceFemale = "nova"
	KeepAudio = False
	Temperature = 0.2
	TopP = 0.95
	PresencePenalty = 0.0
	FrequencyPenalty = 0.0
	STTModel = "whisper-1"
	
	def __init__ (self, UserName = None):
		if UserName != None:
			self.UserName = UserName
		else:
			self.UserName = ""
			if os.path.isfile (self.SettingsFile):
				HL.Log ("Settings.py: Loading settings!", 'I', LogT.Settings)
				with open (self.SettingsFile, "rb") as File:
					TempObj = pickle.load (File)
					self.UserName = TempObj.UserName
					self.MaxContextMsg = TempObj.MaxContextMsg
					self.MaxTokens = TempObj.MaxTokens
					self.AutoContext = TempObj.AutoContext
					try:
						if TempObj.SoftwareVersion == 0.2:
							HL.Log ("Settings.py: HexaPA version: v" + str (self.SoftwareVersion), 'I', LogT.Settings)
							self.API = TempObj.API
							self.AIModel = TempObj.AIModel
						
						if TempObj.SoftwareVersion == 0.3:
							HL.Log ("Settings.py: HexaPA version: v" + str (self.SoftwareVersion), 'I', LogT.Settings)
							self.API = TempObj.API
							self.AIModel = TempObj.AIModel
							HL.Log ("Settings.py: Loaded AIModel: " + self.AIModel, 'D', LogT.Settings)
							self.Temperature = TempObj.Temperature
							self.TopP = TempObj.TopP
							self.PresencePenalty = TempObj.PresencePenalty
							self.FrequencyPenalty = TempObj.PresencePenalty
							self.MaxOTokens = TempObj.MaxOTokens
						
						if TempObj.SoftwareVersion == 0.4 or TempObj.SoftwareVersion == 0.5:
							HL.Log ("Settings.py: HexaPA version: v" + str (self.SoftwareVersion), 'I', LogT.Settings)
							self.API = TempObj.API
							self.AIModel = TempObj.AIModel
							self.Temperature = TempObj.Temperature
							self.TopP = TempObj.TopP
							self.PresencePenalty = TempObj.PresencePenalty
							self.FrequencyPenalty = TempObj.PresencePenalty
							self.MaxOTokens = TempObj.MaxOTokens
							self.TTSModel = TempObj.TTSModel
							self.TTSVoiceMale = TempObj.TTSVoiceMale
							self.TTSVoiceFemale = TempObj.TTSVoiceFemale
							self.KeepAudio = TempObj.KeepAudio
							self.STTModel = TempObj.STTModel
							# for V0.5 I only added default models here, which should be constant, no need to add another entry...
					except:
						pass
			else:
				HL.Log ("Settings.py: " + self.SettingsFile + " not found!", 'W', LogT.Settings)
	
	
	
	def SaveSettings (self):
		TempObj = Settings (self.UserName)
		TempObj.MaxContextMsg = self.MaxContextMsg
		TempObj.MaxTokens = self.MaxTokens
		TempObj.MaxOTokens = self.MaxOTokens
		TempObj.AutoContext = self.AutoContext
		TempObj.SoftwareVersion = self.SoftwareVersion
		TempObj.API = self.API
		TempObj.AIModel = self.AIModel
		TempObj.Temperature = self.Temperature
		TempObj.TopP = self.TopP
		TempObj.PresencePenalty = self.PresencePenalty
		TempObj.PresencePenalty = self.FrequencyPenalty
		TempObj.TTSModel = self.TTSModel
		TempObj.TTSVoiceMale = self.TTSVoiceMale
		TempObj.TTSVoiceFemale = self.TTSVoiceFemale
		TempObj.KeepAudio = self.KeepAudio
		TempObj.STTModel = self.STTModel
		HL.Log ("Settings.py: Saving settings!", 'I', LogT.Settings)
		with open (self.SettingsFile, "wb") as File:
			pickle.dump (TempObj, File)
