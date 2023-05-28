#! /bin/python3

import json
import gzip
import base64
from cryptography.fernet import Fernet

from HexaLibPython import HexaLog as HL
from Source.Settings import *


class Data:
	DataVersion = None # This is for backward compatibility, so that an old conversation can be parsed after updating HexaPA in case the Data structure changes...
	DataType = None # Can be "Message" or "Rule"
	Title = None # Rule presets require a title.
	Rules = None # Block ID of the block containing the rules sent with this message. OR String of text containing the rules when type is set to Rule.
	Context = None # A list of block IDs sent for context to the AI.
	Name = None # Name of the author.
	Message = None # String of text containing the message.
	Rating = None # This is for marking the message as context or bad answer that should never be context...
	BlockID = None # This is just an easy way to get back the index of the block when saving... (No need to init or store...)
	
	
	
	def __init__ (self, Rules = "", Context = [], Name = "", Message = "", DataType = "Message"):
		self.DataVersion = Settings.DataVersion
		self.DataType = DataType
		self.Title = ""
		self.Rules = Rules
		self.Context = Context
		self.Name = Name
		self.Message = Message
		self.Rating = 0
	
	
	
	def Parse (self, Key, EncryptedCompressedData, BlockID, Rating = 0): # Rating is not used for Rules block
		self.BlockID = BlockID
		F = Fernet (Key)
		Data = json.loads (gzip.decompress (F.decrypt (EncryptedCompressedData)).decode ())
		
		# Parse 0.1v data.
		if Data["DataVersion"] == 0.1:
			self.DataVersion = Data["DataVersion"]
			self.DataType = Data["DataType"]
			self.Title = Data["Title"]
			self.Rules = Data["Rules"]
			self.Context = Data["Context"]
			self.Name = Data["Name"]
			self.Message = Data["Message"]
			self.Rating = Data["Rating"]
		
		# Parse 0.2v data.
		elif Data["DataVersion"] == 0.2:
			self.DataVersion = Data["DataVersion"]
			self.DataType = Data["DataType"]
			self.Title = Data["Title"]
			self.Rules = Data["Rules"]
			self.Context = Data["Context"]
			self.Name = Data["Name"]
			self.Message = Data["Message"]
			# Upon further consideration Rating is subject to change, and must not influence block validity...
			self.Rating = Rating # This must be kept part of the Data object, but loaded from the block directly rather then parsed from the hashed string. (Make sure to save it!)
		
		# Default (if the data is no longer supported, or created with a newer version it should be initialized with default values.)
		else:
			HL.Log ("Data.py: Block content can not be parsed! Either no longer supported, or created with a newer version. DO NOT USE --renew-data option! (That may overwrite any data in this block!)", 'E', 7)
			self.DataVersion = Settings.DataVersion
			self.DataType = "Message"
			self.Title = ""
			self.Rules = ""
			self.Context = []
			self.Name = "ERROR"
			self.Message = "Unknown data version. Either very old data (no longer supported) or created with a newer version of the program(not yet available in this version...)\nDO NOT USE --renew-data option! (That may overwrite any data in this block!)"
			self.Rating = "Normal"
	
	
	
	def Dump (self, Key): # This should always dump data according to the latest version.
		F = Fernet (Key)
		Data = {"DataVersion": self.DataVersion, "DataType": self.DataType, "Title": self.Title, "Rules": self.Rules, "Context": self.Context, "Name": self.Name, "Message": self.Message}
		return F.encrypt (gzip.compress (json.dumps (Data).encode ()))
