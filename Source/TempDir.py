#! /bin/python3

import os
import random
import tempfile
import shutil

from HexaLibPython import HexaLog as HL
import Source.LogTrace as LogT


class TempDir:
	TMPDir = None
	TTSDir = None
	
	@classmethod
	def __init__ (cls):
		try:
			TempInRAM = "/run/user/" + str (os.getuid ()) # user accessible location in RAM memory on Linux. (Prefer this for speed and to avoid excessive write on SSDs.)
			if os.path.exists (TempInRAM) and os.access (TempInRAM, os.W_OK):
				cls.TMPDir = TempInRAM + "/HexaPA_" + str (random.randint (1000, 9999))
				while os.path.exists (cls.TMPDir):
					cls.TMPDir = TempInRAM + "/HexaPA_" + str (random.randint (1000, 9999))
				os.makedirs (cls.TMPDir)
			else:
				cls.TMPDir = tempfile.gettempdir () + "/HexaPA_" + str (random.randint (1000, 9999))
				os.makedirs (cls.TMPDir)
			cls.TTSDir = cls.TMPDir + "/TTS"
			os.makedirs (cls.TTSDir)
			HL.Log ("TempDir: Created TMPDir at: " + cls.TMPDir, 'I', LogT.TempDir)
		except:
			cls.TMPDir = None
			HL.Log ("TempDir: Failed to create work directory!", 'E', LogT.TempDir)
	@classmethod
	def Discard (cls):
		if cls.TMPDir is not None:
			shutil.rmtree (cls.TMPDir)
			HL.Log ("TempDir: Deleted TMPDir!", 'I', LogT.TempDir)
