#! /bin/python3

import tiktoken

from HexaLibPython import HexaLog as HL
import Source.LogTrace as LogT


class Tokenizer:
	TokenCount_Rules = 0
	TokenCount_Context = 0
	TokenCount_Prompt = 0
	TokenCount_Total = 0
	
	def __init__ (self, API, Model, Messages):
		if API == "OpenAI":
			Encoding = tiktoken.encoding_for_model (Model)
			for i in Messages:
				if i == Messages[len (Messages) - 1]:
					self.TokenCount_Prompt = len (Encoding.encode ("role: user, content: " + i["content"]))
				elif i["role"] == "user":
					self.TokenCount_Context += len (Encoding.encode ("role: user, content: " + i["content"]))
				elif i["role"] == "assistant":
					self.TokenCount_Context += len (Encoding.encode ("role: assistant, content: " + i["content"]))
				elif i["role"] == "system":
					self.TokenCount_Rules = len (Encoding.encode ("role: system, content:" + i["content"]))
				else:
					HL.Log ("Tokenizer.py: Unknown role: " + i["role"] + " >> Omitting message...", 'E', LogT.Tokenizer)
			self.TokenCount_Total = self.TokenCount_Rules + self.TokenCount_Context + self.TokenCount_Prompt
	
	
	
	@staticmethod
	def Tokenize (API, Model, Text):
		if API == "OpenAI":
			Encoding = tiktoken.encoding_for_model (Model)
			return Encoding.encode (Text)
	
	
	
	@staticmethod
	def Count (API, Model, Text):
		if API == "OpenAI":
			Encoding = tiktoken.encoding_for_model (Model)
			return len (Encoding.encode (Text))
