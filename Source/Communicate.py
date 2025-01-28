#! /bin/python3

import openai
import json

from HexaLibPython import HexaLog as HL
from Source.Options import *
from Source.Keys import *
import Source.LogTrace as LogT


class APIError:
	ErrorMessage = ""
	object = "Error"
	usage = {"completion_tokens": 0,"prompt_tokens": 0,"total_tokens": 0}


class Communicate:
	API_Lookup = {
		"gpt-4o-mini": "OpenAI",
		"gpt-4o": "OpenAI",
		"gpt-4-turbo": "OpenAI",
		"deepseek-chat": "DeepSeek"
	}
	Disabled_OpenAI = True
	Disabled_DeepSeek = True
	Response_OpenAI = None
	OpenAIBaseURL = openai.base_url
	
	
	
	@classmethod
	def __init__ (cls, API, AIModel, Key): # Support for other APIs are planned, for now it's only for OpenAI...
		if API == "OpenAI" or API == "DeepSeek":
			openai.api_key = Key
			if API == "DeepSeek":
				openai.base_url = "https://api.deepseek.com"
				Model = "deepseek-chat"
			else:
				openai.base_url = cls.OpenAIBaseURL
				Model = "gpt-4o-mini"
			Messages = [
				{
					"role": "system",
					"content": ""
				},
				{
					"role": "user",
					"content": "a number please" # The AI should return a single number, not a long line of text. This is the shortest prompt-response I could get out of it. ;)
				}
			]
			try:
				cls.Response_OpenAI = openai.chat.completions.create (
					model = Model,
					messages = Messages,
					temperature = 0, # Only give me what I asked for...
					top_p = 0.1, # Consider only top 10% probabilities.
					n = 1, # generate 1 answer. (I think this is default anyway...)
					max_tokens = 1, # no need to waste much tokens.
					frequency_penalty = -2.0 # Focus on the task (hopefully...)
				)
				HL.Log ("Communicate.py: Key accepted! The AI's test answer(Model: " + Model + "): " + cls.Response_OpenAI.choices[0].message.content, 'D', LogT.Communicate)
			except Exception as e:
				HL.Log (f"Communicate.py: An error occurred: {e}", 'E', LogT.Communicate)
				if API == "OpenAI":
					HL.Log ("Falling back to " + AIModel, 'I', LogT.Communicate)
					HL.Log ("", 'I', LogT.Communicate) # HexaLog keeps the last line if the Log file is not finished to compress multiple of the same messages, so a different line flushes the error to file...
					HL.LogToFile ("Log.log", False)
					try: # Fallback option. More expensive, but still a fraction of a cent... Just in case they gpt-4o-mini model is down.
						cls.Response_OpenAI = openai.chat.completions.create (
							model = AIModel, # Latest
							messages = Messages,
							temperature = 0, # Only give me what I asked for...
							top_p = 0.1, # Consider only top 10% probabilities.
							n = 1, # generate 1 answer. (I think this is default anyway...)
							max_tokens = 1, # no need to waste much tokens, although may not work properly... Not sure about the exact range, it usually consumes 19-23 tokens even when set to 1.
							frequency_penalty = -2.0 # Focus on the task (hopefully...)
						)
						HL.Log ("Communicate.py: Key accepted! The AI's test answer(" + AIModel + "): " + cls.Response_OpenAI.choices[0].message.content, 'D', LogT.Communicate)
					except Exception as e:
						HL.Log (f"Communicate.py: An error occurred: {e}", 'E', LogT.Communicate)
						HL.Log ("", 'E', LogT.Communicate) # HexaLog keeps the last line if the Log file is not finished to compress multiple of the same messages, so a different line flushes the error to file...
						HL.LogToFile ("Log.log", False)
						return
				else:
					HL.Log ("", 'I', LogT.Communicate) # HexaLog keeps the last line if the Log file is not finished to compress multiple of the same messages, so a different line flushes the error to file...
					return
			if API == "OpenAI":
				cls.Disabled_OpenAI = False
			if API == "DeepSeek":
				cls.Disabled_DeepSeek = False
	
	
	
	@classmethod
	def AskTheAI (cls, API, AIModel, Key, Rules, Context, Prompt, MaxOTokens = 128, Temperature = 0.2, TopP = 0.95, PresencePenalty = 0.0, FrequencyPenalty = 0.0, ContextTokens = 128000): # Rules and Context can be None...
		if API == "OpenAI" or API == "DeepSeek": # Other APIs are planned to be supported, for now it's only for OpenAI...
			openai.api_key = Key
			if API == "DeepSeek":
				openai.base_url = "https://api.deepseek.com"
			else:
				openai.base_url = cls.OpenAIBaseURL
			
			Messages = []
			if Rules == None:
				Messages.append ({"role": "system", "content": ""})
			else:
				Messages.append (Rules)
			if Context != None:
				for i in Context:
					Messages.append (i)
			Messages.append (Prompt)
			if Args.debug or Args.verbose: # This is a more detailed response, that doesn't fit into a single line log message...
				print ("")
				print ("Communicate.py: Sending list of messages:")
				for Message in Messages:
					print (Message)
				print ("")
			try: # Just in case the key is deleted, or the service is down...
				# I initially misunderstood... it's not an even split, the total tokens Input + Output tokens is capped at 4096 for gtp-3.5-turbo, and 16384 for the new gpt-3.5-turbo-16k
				Model = ""
				ContextWindow = 128000 # Currently all models have this context window...
				if AIModel == "gpt-4o-mini":
					Model = AIModel
					if MaxOTokens > 16384 or MaxOTokens == 0:
						if (ContextWindow - ContextTokens) < 16384:
							MaxOTokens = ContextWindow - ContextTokens
						else:
							MaxOTokens = 16384
				elif AIModel == "gpt-4o":
					Model = AIModel
					if MaxOTokens == 0:
						if (ContextWindow - ContextTokens) < 4096:
							MaxOTokens = ContextWindow - ContextTokens
						else:
							MaxOTokens = 4096
					elif MaxOTokens > 4096:
						Model = AIModel + "-mini" # The mini has larger output token allowance.
						HL.Log ("Communicate.py: gpt-4o model has an output token cap of 4096. -> Prompting gpt-4o-mini!", 'W', LogT.Communicate)
						if MaxOTokens > 16384:
							if (ContextWindow - ContextTokens) < 16384:
								MaxOTokens = ContextWindow - ContextTokens
							else:
								MaxOTokens = 16384
				elif AIModel == "gpt-4-turbo":
					Model = AIModel
					if MaxOTokens > 4096 or MaxOTokens == 0:
						if (ContextWindow - ContextTokens) < 4096:
							MaxOTokens = ContextWindow - ContextTokens
						else:
							MaxOTokens = 4096
				
				elif AIModel == "deepseek-chat":
					Model = AIModel
					if ContextTokens > 64000:
						ContextTokens = 64000 # Deepseek models currently have smaller context window.
					if MaxOTokens > 8000 or MaxOTokens == 0:
						MaxOTokens = 8000
				#elif AIModel == "deepseek-reasoner":
				#	Model = AIModel
				#	ContextTokens = 64000
				#	elif MaxOTokens > 4000 or MaxOTokens == 0:
				#		MaxOTokens = 8000
				else:
					HL.Log ("Communicate.py: Unknown AI model: " + AIModel, 'E', LogT.Communicate)
					
				HL.Log ("Communicate.py: Using AI Model: " + Model, 'D', LogT.Communicate)
				cls.Response_OpenAI = openai.chat.completions.create (
					model = Model,
					messages = Messages,
					temperature = Temperature, # float, Range 0 to 2; 0 = Deterministic; 2 = Random
					top_p = TopP, # float, Range 0 to 1; 0.1 = top 10% of probability mass considered... 1 = anything goes
					n = 1, # int, How many messages to generate
					max_tokens = MaxOTokens, # int, Range 1 - 2048
					presence_penalty = PresencePenalty, # float, Range -2 to 2; Loop rejection
					frequency_penalty = FrequencyPenalty # float, Range -2 to 2; -2 = ASD (Hyperfocus) vs 2 = ADHD (Creativity)
					#user = "Unspecified" # optional, (I guess it's for companies with multiple users using the same account. May cost some extra tokens multiple times / message...)
				)
				HL.Log ("Communicate.py: The AI responded!", 'D', LogT.Communicate)
				if Args.debug or Args.verbose: # This is a more detailed response, that doesn't fit into a single line log message...
					print ("Communicate.py: The AI returned:")
					print (cls.Response_OpenAI.model_dump_json (indent=2))
					print ("")
				return cls.Response_OpenAI
			except Exception as e:
				HL.Log (f"Communicate.py: An error occurred: {e}", 'E', LogT.Communicate)
				HL.Log ("", 'E', LogT.Communicate) # HexaLog keeps the last line if the Log file is not finished to compress multiple of the same messages, so this makes the error visible in the file...
				HL.LogToFile ("Log.log", False)
				print (dir (e))
				Error = APIError ()
				Error.ErrorMessage = e.body["message"]
				return Error
