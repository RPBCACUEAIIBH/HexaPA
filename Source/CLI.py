#! /bin/python3

from HexaLibPython.HexaLog import HexaLog as HL
import Source.LogTrace as LogT
from Source.Keys import *
from Source.Commands import *
from Source.Settings import *
from Source.Options import *
from Source.BlockChain import *

import sys
import getpass



class CLI:
	S = None
	K = None
	PasswordAccepted = False
	
	
	
	def __init__ (self, SettingsObj):
		self.S = SettingsObj
	
	
	
	def RequestPassword (self):
		if self.S.UserName == "":
			self.S.UserName = input ("Please enter your username: ")
			self.S.SaveSettings ()
		
		try:
			HL.Log ("CLI.py: Loading API Key(s)...", 'D', LogT.CLI)
			self.K = Keys (self.S.UserName, getpass.getpass ("Please enter password for " + self.S.UserName + ": "))
			if self.K.UserKey != self.K.IllegalKey:
				self.PasswordAccepted = True
		except:
			HL.Log ("CLI.py: Wrong password! Try again. :P", 'E', LogT.CLI)
	
	
	
	def Options (self):
		if Args.version:
			print (Designation + " - AI Chat using OpenAI API, Version: v" + str (Settings.SoftwareVersion) + "\n")
			print (License + "\n")
			print (Copyright)
			print (BSD3CL_Details)
			self.S.WorkDir.Discard ()
			sys.exit ()
		
		if Args.user:
			self.S.UserName = Args.user
			self.S.SaveSettings ()
		
		if Args.password:
			try:
				HL.Log ("CLI.py: Loading API Key(s)...", 'D', LogT.CLI)
				self.K = Keys (self.S.UserName, Args.password)
				if self.K.UserKey != self.K.IllegalKey:
					self.PasswordAccepted = True
			except:
				HL.Log ("CLI.py: Wrong password! Try again. :P", 'E', LogT.CLI)
				sys.exit ()
		
		if Args.openai_key:
			if self.K == None:
				self.RequestPassword ()
			self.K.Key_OpenAI = Args.openai_key
			self.K.SaveKeys ()
		
		if Args.import_chat:
			if self.K == None:
				self.RequestPassword ()
			NewChain = BlockChain (10)
			Commands.ImportChatJSON (self.K.UserKey, NewChain, Args.import_chat)
			NewChain.Save ()
