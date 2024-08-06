#! /bin/python3

import openai
import json
import os
import datetime
import pydub
import pydub.playback

from HexaLibPython import HexaLog as HL
from Source.Options import *
from Source.Keys import *
import Source.LogTrace as LogT


class APIError:
	ErrorMessage = ""
	object = "Error"
	usage = {"completion_tokens": 0,"prompt_tokens": 0,"total_tokens": 0}


class TTS:
	API = None
	Disabled_OpenAI = True
	Response_OpenAI = None
	WorkDir = None
	Model = None
	Record = False
	
	
	
	@classmethod
	def __init__ (cls, API, TTSModel, WDir = "Audio/TTS", Record = False, Key = None): # Key should already be applied right after testing it with the text model.
		if API == "OpenAI":
			if Key is not None:
				openai.api_key = Key
			cls.API = API
			cls.WorkDir = WDir
			cls.Model = TTSModel
			cls.Record = Record
			Disabled_OpenAI = False
	
	
	
	@classmethod
	def Read (cls, Text, TTSVoice, Title, ID = 0): # Support for other APIs are planned, for now it's only for OpenAI...
		if cls.API == "OpenAI":
			try:
				if cls.Record:
					cls.Response_OpenAI = "Audio/TTS" + "/" + str (ID) + " - " + Title + " - " + datetime.datetime.now ().strftime ("%Y-%m-%d %H:%M:%S") + ".mp3"
				else:
					cls.Response_OpenAI = cls.WorkDir + "/" + Title + ".mp3"
				Response = openai.audio.speech.create (
				  model = cls.Model,
				  voice = TTSVoice,
				  input = Text
				)
				Response.stream_to_file (cls.Response_OpenAI)
				HL.Log ("TTS.py: The AI's answer (by Model: " + cls.Model + ") saved to: " + cls.Response_OpenAI, 'D', LogT.TTS)
				Sound = pydub.AudioSegment.from_mp3 (cls.Response_OpenAI)
				pydub.playback.play (Sound)
			except Exception as e:
				HL.Log (f"TTS.py: An error occurred: {e}", 'E', LogT.TTS)
