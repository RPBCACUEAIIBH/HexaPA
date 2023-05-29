#! /bin/python3

import hashlib

from Source.Data import *


class DataBlock:
	Rating = None # This is a block specific variable, it subject to change and thus must not influence block validity.
	
	
	
	def __init__ (self, BlockID, TimeStamp, Data, PreviousHash):
		self.BlockID = BlockID
		self.TimeStamp = TimeStamp
		self.Data = Data
		self.PreviousHash = PreviousHash
		self.Signature = 0
	
	
	
	def Hash (self):
		if type (self.Data) != 'str':
			BlockData = str (self.BlockID) + self.TimeStamp + ", " + self.Data.decode () + ", " + self.PreviousHash + ", " + str (self.Signature)
		else:
			BlockData = str (self.BlockID) + self.TimeStamp + ", " + self.Data + ", " + self.PreviousHash + ", " + str (self.Signature)
		return hashlib.sha256 (BlockData.encode ()).hexdigest ()
	
	
	
	def Sign (self):
		if self.Rating == None: # While it is only used for "Message" type data, without a rating value the block may not be loaded properly on next start...
			self.Rating = 0
		self.Signature = 0
		Chararray1 = tuple ("000")
		Run = True
		while Run:
			Chararray2 = tuple (self.Hash ())
			Run = False
			for i in range (0, 3):
				if Chararray1[i] != Chararray2[i]:
					Run = True
					break
			if Run:
				self.Signature += 1
	
	
	
	def DumpDict (self, Key):
		MessageData = Data ()
		MessageData.Parse (Key, self.Data)
		return {"ID": self.BlockID, "TimeStamp": self.TimeStamp, "Data": MessageData.DumpDict (), "Rating": self.Rating}
