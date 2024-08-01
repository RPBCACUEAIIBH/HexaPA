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
	Disabled_OpenAI = True
	Response_OpenAI = None
	
	
	
	@classmethod
	def __init__ (cls, API, AIModel, Key): # Support for other APIs are planned, for now it's only for OpenAI...
		if API == "OpenAI":
			try:
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
				cls.Response_OpenAI = openai.chat.completions.create (
					model = "gpt-3.5-turbo-0125",
					messages = Messages,
					temperature = 0, # Only give me what I asked for...
					top_p = 0.1, # Consider only top 10% probabilities.
					n = 1, # generate 1 answer. (I think this is default anyway...)
					max_tokens = 1, # no need to waste much tokens, although may not work properly... Not sure about the exact range, it usually consumes 19-23 tokens even when set to 1.
					frequency_penalty = -2.0 # Focus on the task (hopefully...)
				)
				HL.Log ("Communicate.py: Key accepted! The AI's test answer(Model: gpt-3.5-turbo-0125): " + cls.Response_OpenAI.choices[0].message.content, 'D', LogT.Communicate)
				
# This works, but the latest gpt-3.5-turbo-0125 chat model is cheaper then the completion model.
#				openai.api_key = Key
#				# This should be 2 tokens in, 3 out, total 5 with the cheapest model, this should also be the fastest, and actually respects the token limit.
#				cls.Response_OpenAI = openai.completions.create (
#					model = "gpt-3.5-turbo-instruct",
#					prompt = "testing hello",
#					temperature = 0,
#					max_tokens = 1,
#					top_p = 1,
#					frequency_penalty = 0,
#					presence_penalty = 0
#				)
#				Text = cls.Response_OpenAI.choices[0].text
#				HL.Log ("Communicate.py: Key accepted! The AI's test answer(Model: gpt-3.5-turbo-instruct): " + Text, 'D', LogT.Communicate)
			except Exception as e:
				HL.Log (f"Communicate.py: An error occurred: {e}", 'E', LogT.Communicate)
				if AIModel == "gpt-3.5-turbo":
					HL.Log ("Falling back to gpt-3.5-turbo-instruct", 'I', LogT.Communicate)
				else:
					HL.Log ("Falling back to " + AIModel + "-preview", 'I', LogT.Communicate)
				HL.Log ("", 'I', LogT.Communicate) # HexaLog keeps the last line if the Log file is not finished to compress multiple of the same messages, so a different line flushes the error to file...
				HL.LogToFile ("Log.log", False)
				try: # Fallback option. More expensive, but still a fraction of a cent... Just in case they remove gpt-3.5-turbo-instruct model. (which is cheap and fast but not very useful...)
					openai.api_key = Key
					# gpt-3.5-turbo-0125 is a chat model, and it's currently the latest and cheapest therefore now used for key testing by default, so if it's down, and was also user selected try the instruct instead.
					if AIModel == "gpt-3.5-turbo":
						# This should be 2 tokens in, 3 out, total 5 with the cheapest model, this should also be the fastest, and actually respects the token limit.
						cls.Response_OpenAI = openai.completions.create (
							model = "gpt-3.5-turbo-instruct",
							prompt = "testing hello",
							temperature = 0,
							max_tokens = 1,
							top_p = 1,
							frequency_penalty = 0,
							presence_penalty = 0
						)
						Text = cls.Response_OpenAI.choices[0].text
						HL.Log ("Communicate.py: Key accepted! The AI's test answer(Model: gpt-3.5-turbo-instruct): " + Text, 'D', LogT.Communicate)
					else:
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
						Model = AIModel + "-preview"
						cls.Response_OpenAI = openai.chat.completions.create (
							model = Model, # Latest
							messages = Messages,
							temperature = 0, # Only give me what I asked for...
							top_p = 0.1, # Consider only top 10% probabilities.
							n = 1, # generate 1 answer. (I think this is default anyway...)
							max_tokens = 1, # no need to waste much tokens, although may not work properly... Not sure about the exact range, it usually consumes 19-23 tokens even when set to 1.
							frequency_penalty = -2.0 # Focus on the task (hopefully...)
						)
						HL.Log ("Communicate.py: Key accepted! The AI's test answer(" + AIModel + "-preview): " + cls.Response_OpenAI.choices[0].message.content, 'D', LogT.Communicate)
				except Exception as e:
					HL.Log (f"Communicate.py: An error occurred: {e}", 'E', LogT.Communicate)
					HL.Log ("", 'E', LogT.Communicate) # HexaLog keeps the last line if the Log file is not finished to compress multiple of the same messages, so a different line flushes the error to file...
					HL.LogToFile ("Log.log", False)
					return
			cls.Disabled_OpenAI = False
	
	
	
	@classmethod
	def AskTheAI (cls, API, AIModel, Rules, Context, Prompt, MaxTokens = 128, Temperature = 0.2, TopP = 0.95, PresencePenalty = 0.0, FrequencyPenalty = 0.0, ContextTokens = 4096): # Rules and Context can be None...
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
				if AIModel == "gpt-3.5-turbo":
					if MaxTokens == 0:
						MaxTokens = 16384 - ContextTokens
						Model = AIModel + "-16k" # Large context forced.
					elif (MaxTokens + ContextTokens) > 4000:
						Model = AIModel + "-16k" # Legacy model... Available, but not updated anymore.
						if MaxTokens > 16384:
							MaxTokens = 16384
					else:
						Model = AIModel + "-0125" # Latest
				elif AIModel == "gpt-4-turbo":
					Model = AIModel + "-preview"
					if MaxTokens > 4096 or MaxTokens == 0:
						MaxTokens = 4096
				else:
					HL.Log ("Communicate.py: Unknown AI model: " + AIModel, 'E', LogT.Communicate)
					
				HL.Log ("Communicate.py: Using AI Model: " + Model, 'D', LogT.Communicate)
				cls.Response_OpenAI = openai.chat.completions.create (
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
