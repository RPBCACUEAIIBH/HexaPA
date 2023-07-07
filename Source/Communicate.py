#! /bin/python3

import openai

from HexaLibPython import HexaLog as HL
from Source.Options import *
from Source.Keys import *



class Communicate:
	Disabled_OpenAI = True
	Response_OpenAI = None
	
	
	
	@classmethod
	def __init__ (cls, API, AIModel, Key): # Support for other APIs are planned, for now it's only for OpenAI...
		if API == "OpenAI":
			try:
				openai.api_key = Key
				# This should be 2 tokens in, 3 out, total 5 with the cheapest model, this should also be the fastest, and actually respects the token limit.
				cls.Response_OpenAI = openai.Completion.create (
					model = "text-ada-001",
					prompt = "testing hello",
					temperature = 0,
					max_tokens = 3,
					top_p = 1,
					frequency_penalty = 0,
					presence_penalty = 0
				)
				Text = cls.Response_OpenAI['choices'][0]['text'].replace ('\n', '')
				HL.Log ("Communicate.py: Key accepted! The AI's test answer(Model: text-ada-001): " + Text, 'D', 4)
			except Exception as e:
				HL.Log (f"Communicate.py: An error occurred: {e}", 'E', 4)
				HL.Log ("Falling back to " + AIModel, 'I', 4)
				HL.Log ("", 'I', 4) # HexaLog keeps the last line if the Log file is not finished to compress multiple of the same messages, so a different line flushes the error to file...
				HL.LogToFile ("Log.log", False)
				try: # Fallback option. More expensive, but still a fraction of a cent... Just in case they remove text-ada-001 model. (which is cheap and fast but not very useful...)
					openai.api_key = Key
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
					cls.Response_OpenAI = openai.ChatCompletion.create (
						model = AIModel,
						messages = Messages,
						temperature = 0, # Only give me what I asked for...
						top_p = 0.1, # Consider only top 10% probabilities.
						n = 1, # generate 1 answer. (I think this is default anyway...)
						max_tokens = 25, # no need to waste much tokens, although may not work properly... Not sure about the exact range, it usually consumes 19-23 tokens even when set to 1.
						frequency_penalty = -2.0 # Focus on the task (hopefully...)
					)
					HL.Log ("Communicate.py: Key accepted! The AI's test answer(" + AIModel + "): " + cls.Response_OpenAI['choices'][0]['message']['content'], 'D', 4)
				except Exception as e:
					HL.Log (f"Communicate.py: An error occurred: {e}", 'E', 4)
					HL.Log ("", 'E', 4) # HexaLog keeps the last line if the Log file is not finished to compress multiple of the same messages, so a different line flushes the error to file...
					HL.LogToFile ("Log.log", False)
					return
			cls.Disabled_OpenAI = False
	
	
	
	@classmethod
	def AskTheAI (cls, API, AIModel, Rules, Context, Prompt, MaxTokens = 2048, Temperature = 0.2, TopP = 0.95, PresencePenalty = 0.0, FrequencyPenalty = 0.0): # Rules and Context can be None...
		if API == "OpenAI": # Other APIs are planned to be supported, for now it's only for OpenAI...
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
				if MaxTokens > 2048: # FOR NOW! >> If the token limit is above half of max, it will switch to the new gtp-3.5-turbo-16k model. (It is more expensive, but allows 4x the amount of tokens.)
					Model = AIModel + "-16k-0613"
					if MaxTokens > 8192:
						MaxTokens = 8192
				else:
					Model = AIModel + "-0613"
				HL.Log ("Communicate.py: Using AI Model: " + Model, 'D', 4)
				cls.Response_OpenAI = openai.ChatCompletion.create (
					model = Model,
					messages = Messages,
					temperature = Temperature, # float, Range 0 to 2; 0 = Deterministic; 2 = Random
					top_p = TopP, # float, Range 0 to 1; 0.1 = top 10% of probability mass considered... 1 = anything goes
					n = 1, # int, How many messages to generate
					max_tokens = MaxTokens, # int, Range 1 - 2048
					presence_penalty = PresencePenalty, # float, Range -2 to 2; Loop rejection
					frequency_penalty = FrequencyPenalty # float, Range -2 to 2; -2 = ASD (Hyperfocus) vs 2 = ADHD (Creativity)
					#user = "Unspecified" # optional, (I guess it's for companies with multiple users using the same account. May cost some extra tokens multiple times / message...)
				)
				HL.Log ("Communicate.py: The AI responded!", 'D', 4)
				if Args.debug or Args.verbose: # This is a more detailed response, that doesn't fit into a single line log message...
					print ("Communicate.py: The AI returned:")
					print (cls.Response_OpenAI)
					print ("")
				return cls.Response_OpenAI
#			except openai.error.APIError as e:
#				print(f"OpenAI API returned an API Error: {e}")
#				return
#			except openai.error.APIConnectionError as e:
#				print(f"Failed to connect to OpenAI API: {e}")
#				return
#			except openai.error.RateLimitError as e:
#				print(f"OpenAI API request exceeded rate limit: {e}")
#				return
			except Exception as e:
				HL.Log (f"Communicate.py: An error occurred: {e}", 'E', 4)
				HL.Log ("", 'E', 4) # HexaLog keeps the last line if the Log file is not finished to compress multiple of the same messages, so this makes the error visible in the file...
				HL.LogToFile ("Log.log", False)
				print(dir(e))
				return e
