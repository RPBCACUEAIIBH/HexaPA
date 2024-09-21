#! /bin/python3

import openai
import json
import os
import datetime

from HexaLibPython import HexaLog as HL
from Source.Options import *
from Source.Keys import *
import Source.LogTrace as LogT



class STT:
	API = None
	Disabled_OpenAI = True
	Response_OpenAI = None
	Model = None
	
	
	
	@classmethod
	def __init__ (cls, API, STTModel, Key = None): # Key should already be applied right after testing it with the text model.
		if API == "OpenAI":
			if Key is not None:
				openai.api_key = Key
			cls.API = API
			cls.Model = STTModel
			Disabled_OpenAI = False
	
	
	
	@classmethod
	def Transcribe (cls, AudioFile): # Support for other APIs are planned, for now it's only for OpenAI...
		if cls.API == "OpenAI":
			try:
				Response = openai.audio.transcriptions.create (
					model = cls.Model,
					file = open (AudioFile, "rb")
					#prompt = "text from prevous transcription", # This may help with consistency, but it will only use the last 244 tokens.
				)
				# It can also be post processed with text model... https://platform.openai.com/docs/guides/speech-to-text/improving-reliability
				# Translation can only be done from another language to English. Syntax is the same, but call openai.audio.translation.create ()
				cls.Response_OpenAI = Response.text
				HL.Log ("STT.py: The AI's answer (by Model: " + cls.Model + ") saved to: " + cls.Response_OpenAI, 'D', LogT.STT)
				return cls.Response_OpenAI
			except:
				HL.Log (f"STT.py: An error occurred: {e}", 'E', LogT.STT)
