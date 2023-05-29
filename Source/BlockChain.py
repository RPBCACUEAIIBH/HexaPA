#! /bin/python3

import os
import pickle
import datetime

from HexaLibPython.HexaLog import HexaLog as HL
from Source.DataBlock import DataBlock


class BlockChain:
	LogTrace = 0xFFFF
	File = None
	Subject = None # Subject of the conversation.
	CreationTime = None # Time when the conversation started.
	LatestRules = None # BlockID containing latest rules. (No need to load here. Found anyway while iterating to display / export the conversation.)
	Rules = None # Data object containing latest rules. (Latest rules should be loaded during displaying / exporting the conversation.)
	
	
	
	def __init__ (self, Trace = None):
		self.Blocks = []
		if Trace != None:
			self.LogTrace = Trace
	
	
	
	def Clear (self, Trace = None):
		self.Blocks = []
		self.File = None
		self.Subject = None
		self.CreationTime = None
		self.LatestRules = None
		self.Rules = None
	
	
	
	def NewBlock (self, Data = ""): # Create new conversation
		if len (self.Blocks) == 0:
			self.Blocks.append (DataBlock (len (self.Blocks), datetime.datetime.now ().strftime ("%Y-%m-%d %H:%M:%S"), Data, ""))
		else:
			Validity = self.Validate ()
			if Validity == True:
				self.Blocks.append (DataBlock (len (self.Blocks), datetime.datetime.now ().strftime ("%Y-%m-%d %H:%M:%S"), Data, self.Blocks[len (self.Blocks) - 1].Hash ()))
		self.Blocks[0].Sign ()
		HL.Log ("BlockChain.py: New block created!", "D", self.LogTrace)
	
	
	
	def Validate (self):
		for i in range (0, len (self.Blocks)):
			if self.Blocks[i].BlockID > 0:
				if self.Blocks[i].PreviousHash != self.Blocks[i - 1].Hash ():
					HL.Log ("BlockChain.py: Chain validation failed at block: " + str (self.Blocks[i].BlockID) + " Data is corrupt and can not be trusted!", "E", self.LogTrace)
					HL.Log (str (self.Blocks[i].PreviousHash) + " != " + str(self.Blocks[i - 1].Hash ()), "E", self.LogTrace)
					return False
		return True
	
	
	
	def Load (self, ChainFile): # Load existing conversation
		self.File = ChainFile
		if os.path.isfile (self.File):
			with open (self.File, "rb") as F:
				Chain = pickle.load (F)
				self.Blocks = Chain.Blocks
				self.Subject = Chain.Subject
				self.CreationTime = Chain.CreationTime
				# Validate here
				HL.Log ("BlockChain.py: Blocks loaded!", 'D', self.LogTrace)
		else:
			HL.Log ("BlockChain.py: " + self.File + " not found!", 'E', self.LogTrace)
	
	
	
	def Save (self, ChainFile = None): # Save conversation
		if ChainFile != None:
			self.File = ChainFile
		if self.File != None:
			HL.Log ("BlockChain.py: Saving blocks to " + self.File, 'D', self.LogTrace)
			with open (self.File, "wb") as F:
				pickle.dump (self, F)
