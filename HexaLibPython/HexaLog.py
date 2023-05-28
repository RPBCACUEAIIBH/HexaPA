#! /bin/python3

# Import Builtin modules
import time
import sys

# Import Custom modules
from HexaLibPython.UpTime import *
from HexaLibPython.Misc import *


class LogEntry:
	def __init__ (self):
		self.TimeStamp = UTime ()
		self.Message = ""
		self.Repetition = 0 # A minimal log compression -> How many times the same line is repeated.
		AvgInterval = UTime () #  Average time between repeating messages.



class HexaLog:
	LogLevel = 4 # Set it with LogSettings! 'S' = Silent, 'E' = Errors, 'W' Errors and  Warnings, 'I' = Errors, Warnings, and Info 'D' everything including debug messages.
	TraceFocus = 0 # 0 = Silent, Trace>0 = focus that trace, 65535 = Default trace(if no Trace specified...)
	LogMessages = []
	AppendFile = False
	
	
	
	@classmethod
	def LogSettings (cls, Level, Trace = 0): # Trace filter off
		if Level == 'S':
			cls.LogLevel = 0
		elif Level == 'F':
			cls.LogLevel = 1
		elif Level == 'E':
			cls.LogLevel = 2
		elif Level == 'W':
			cls.LogLevel = 3
		elif Level == 'I':
			cls.LogLevel = 4
		elif Level == 'D':
			cls.LogLevel = 5
		else: 
			cls.LogLevel = 5
		cls.TraceFocus = Trace
	
	
	
	@classmethod
	def Log (cls, Arg1 = None, Arg2 = None, Arg3 = None, Arg4 = None, Arg5 = 0xFFFF): # The shuffling of variables is for compliance with C++ version, where the function is overloaded. This may be optimized for HexaLib 2.0 in both...
		Line = None
		File = None
		Message = None
		Level = None
		Trace = Arg5
		if Arg1 != None and Arg2 != None and Arg4 == None:
			Message = Arg1
			Level = Arg2
			if Arg3 != None:
				Trace = Arg3
		else:
			Line = Arg1
			File = Arg2
			Message = Arg3
			Level = Arg4
		NewEntry = LogEntry ()
		UpTime.Refresh ()
		NewEntry.TimeStamp.Hours = UpTime.UpT.Hours
		NewEntry.TimeStamp.Minutes = UpTime.UpT.Minutes
		NewEntry.TimeStamp.Seconds = UpTime.UpT.Seconds
		NewEntry.Message += " [ Trace "
		NewEntry.Message += Misc.LeadingCharacters (Trace, ' ', 5)
		NewEntry.Message += " --> "
		MessageLevel = ""
		OutputSwitch = 2
		if Level == 'F':
			NewEntry.Message += "  Fatal"
			MessageLevel = 1
			OutputSwitch = 1
		elif Level == 'E':
			NewEntry.Message += "  Error"
			MessageLevel = 2
			OutputSwitch = 1
		elif Level == 'W':
			NewEntry.Message += "Warning"
			MessageLevel = 3
		elif Level == 'I':
			NewEntry.Message += "   Info"
			MessageLevel = 4
		elif Level == 'D':
			NewEntry.Message += "  Debug"
			MessageLevel = 5
		else: 
			NewEntry.Message += "    ???"
			MessageLevel = 5
		NewEntry.Message += " ]: "
		NewEntry.Message += Message
		if File and Line:
			NewEntry.Message += " (At line "
			NewEntry.Message += str (Line)
			NewEntry.Message += " in "
			NewEntry.Message += File
			NewEntry.Message += ")"
		if len (cls.LogMessages) > 0:
			if cls.LogMessages[len(cls.LogMessages) - 1].Message != NewEntry.Message:
				cls.LogMessages.append (NewEntry)
			else:
				cls.LogMessages[len(cls.LogMessages) - 1].Repetition += 1
		else:
			cls.LogMessages.append (NewEntry)
		# This part goes to the terminal filtered.
		TS = Misc.LeadingCharacters (NewEntry.TimeStamp.Hours, '0', 5)
		TS += ":" + Misc.LeadingCharacters (NewEntry.TimeStamp.Minutes, '0', 2)
		TS += ":" + Misc.LeadingCharacters (int (NewEntry.TimeStamp.Seconds), '0', 2)
		TS += "." + Misc.LeadingCharacters (int (NewEntry.TimeStamp.Seconds * 1000000.0) % 1000000, '0', 6)
		if MessageLevel <= cls.LogLevel and cls.LogLevel > 0 or cls.TraceFocus == Trace and Trace > 0:
			if OutputSwitch == 1:
				sys.stderr.write (TS + NewEntry.Message + "\n") # buffered standard error stream
				sys.stderr.flush ()
			elif OutputSwitch == 2:
				sys.stdout.write (TS + NewEntry.Message + "\n") # buffered standard out stream
				sys.stdout.flush ()
	
	
	
	@classmethod
	def LogToFile (cls, File, Finish):
		LogFile = open (File, "a")
		while len (cls.LogMessages) > 0:
			# Keep the last entry to see whether or not the next line is the same.
			if not Finish and len (cls.LogMessages) == 1:
				break
			TS = Misc.LeadingCharacters (cls.LogMessages[0].TimeStamp.Hours, '0', 5)
			TS += ":" + Misc.LeadingCharacters (cls.LogMessages[0].TimeStamp.Minutes, '0', 2)
			TS += ":" + Misc.LeadingCharacters (int (cls.LogMessages[0].TimeStamp.Seconds), '0', 2)
			TS += "." + Misc.LeadingCharacters (int (cls.LogMessages[0].TimeStamp.Seconds * 1000000.0) % 1000000, '0', 6)
			if cls.LogMessages[0].Repetition > 0:
				print (TS + cls.LogMessages[0].Message + " <-- " + str (cls.LogMessages[0].Repetition + 1) + " instances!", file=LogFile)
			else:
				print (TS + cls.LogMessages[0].Message, file=LogFile)
			cls.LogMessages.pop (0)
		LogFile.close ()
