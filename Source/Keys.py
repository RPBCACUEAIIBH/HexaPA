#! /bin/python3

import os
import pickle
import base64
import hashlib
from cryptography.fernet import Fernet

from HexaLibPython import HexaLog as HL
import Source.LogTrace as LogT
from Source.Settings import *


class Keys:
	KeyFile = ".Keys.bin"
	Key_OpenAI = None
	Key_DeepSeek = None
	Key_Lookup = None
	UserKey = None
	IllegalKey = None
	
	
	
	def __init__ (self, UserName = None, Password = None):
		if self.Key_OpenAI == None and UserName != None and Password != None:
			# This is not meant for high security encryption, just enough to deny access to your data for anyone but advanced hackers. (Anyway this is way better then most apps with no encryption.)
			# (This is just an AI chat application using 3rd party API, you shouldn't disclose anything vital anyway, and you should have already set a monthly cap on your API usage.)
			# I prefer not using salt since if a random salt is lost, knowing the password is not enough, which can be used to deny acces to the user's own data simply by deleting ".Keys.bin"...
			String = Password + UserName
			self.UserKey = base64.urlsafe_b64encode (hashlib.pbkdf2_hmac ("sha256", String.encode (), b"", 100000, 32))
			self.IllegalKey = base64.urlsafe_b64encode (hashlib.pbkdf2_hmac ("sha256", UserName.encode (), b"", 100000, 32)) # Since this still generates a key, I shall reject this...
			if os.path.isfile (self.KeyFile):
				with open (self.KeyFile, "rb") as File:
					TempKeys = pickle.load (File)
					F = Fernet (self.UserKey)
					self.Key_OpenAI = F.decrypt (TempKeys.Key_OpenAI).decode ()
					self.Key_DeepSeek = F.decrypt (TempKeys.Key_DeepSeek).decode ()
				if self.Key_OpenAI == None:
					HL.Log ("Keys.py: OpenAI key not found!", 'E', LogT.Keys)
				if self.Key_DeepSeek == None:
					HL.Log ("Keys.py: DeepSeek key not found!", 'E', LogT.Keys)
			else:
				HL.Log ("Keys.py: " + self.KeyFile + " not found!", 'W', LogT.Keys)
		
		# Constructing lookup table... This is kind of a bodge... All keys and APIs should be accessed from this lookup table...
		self.Key_Lookup = {
			"OpenAI": self.Key_OpenAI,
			"DeepSeek": self.Key_DeepSeek
		}
	
	
	
	def SaveKeys (self):
		F = Fernet (self.UserKey)
		TempKeys = Keys ()
		UserKey = None # This should never be recoverable from Keys.bin even by accident, since it can be extracted and used to decrypt user data without password!
		if self.Key_OpenAI != None:
			TempKeys.Key_OpenAI = F.encrypt (self.Key_OpenAI.encode ()) # Good idea to encrypt the API key(s) as well, because they could be extracted and used by others while you pay for it.
		if self.Key_DeepSeek != None:
			TempKeys.Key_DeepSeek = F.encrypt (self.Key_DeepSeek.encode ())
		with open (self.KeyFile, "wb") as File:
			pickle.dump (TempKeys, File)
		HL.Log ("Keys.py: Keys saved!", 'I', LogT.Keys)
