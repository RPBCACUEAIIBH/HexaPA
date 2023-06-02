#! /bin/python3


import tkinter as tk

from HexaLibPython import HexaLog as HL
from Source.Theme import *

class Tooltip:
	def __init__ (self, TooltipLabel, TooltipText):
		self.Label = TooltipLabel
		self.Text = TooltipText
		self.Flags = {"Visibility": False}
	
	
	
	def ShowTooltip (self, event):
		if self.Flags["Visibility"] == False:
			self.Label.config (text = self.Text)
			self.Label.lift ()
			self.Flags["Visibility"] = True
	
	
	
	def HideTooltip (self, event):
		self.Label.config (text = "")
		self.Label.lower ()
		self.Flags["Visibility"] = False
