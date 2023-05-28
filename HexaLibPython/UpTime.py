#! /bin/python3

# Import Builtin modules
import time


class UTime:
	def __init__ (self):
		self.Hours = 0 # 0-35535
		self.Minutes = 0 # 0-59
		self.Seconds = 0.0 # 0-59
		self.LastChecked = time.time ()



class UpTime:
	UpT = None
	
	
	
	@classmethod
	def Refresh (cls):
		if cls.UpT == None:
			cls.UpT = UTime () # Initialize
		Now = time.time ()
		TimeSpan = Now - cls.UpT.LastChecked
		cls.UpT.LastChecked = Now
		cls.UpT.Seconds += TimeSpan
		cls.UpT.Minutes += int (cls.UpT.Seconds / 60)
		while cls.UpT.Seconds >= 60.0:
			cls.UpT.Seconds -= 60.0
		cls.UpT.Hours += int (cls.UpT.Minutes / 60)
		cls.UpT.Minutes %= 60
		cls.UpT.Hours %= 65536 # Just for consistency. The earlier C++ version of HexaLib goes to 65535 only. Not many program runs for more then 4 years continuously anyway. :)
