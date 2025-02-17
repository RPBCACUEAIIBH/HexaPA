#! /bin/python3

import os
import glob
import re
import webbrowser
import tkinter as tk
import datetime
import platform

from HexaLibPython import HexaLog as HL
import Source.LogTrace as LogT
from Source.Window import *
from Source.Keys import *
from Source.Theme import *
from Source.Communicate import *
from Source.Tokenizer import *
from Source.BlockChain import *
from Source.Data import *
from Source.Settings import *
from Source.Options import *
from Source.Commands import *
from Source.TTS import *
from Source.STT import *


class GUI:
	PWD = None
	
	
	
	def __init__ (self, SettingsObject):
		self.S = SettingsObject
		self.Window = tk.Tk (className = "HexaPA") # Not sure why the className is displayed as "HexaPA" instead of "HexaPA" as I set it... (on ubuntu)
		self.Window.title ("HexaPA")
		self.WinWidth = 720
		self.WinHeight = self.Window.winfo_screenheight ()
		self.WinPosX = self.Window.winfo_screenwidth () - self.WinWidth
		self.WinPosY = 0
		HL.Log ("GUI.py: WindowSize: " + str (self.WinWidth) + " x " + str (self.WinHeight) + "; PosX: " + str (self.WinPosX) + "; PosY: " + str (self.WinPosY), 'D', LogT.GUI)
		self.Window.geometry (f"{self.WinWidth}x{self.WinHeight}+{self.WinPosX}+{self.WinPosY}")
		self.Window.resizable (True, True)
		self.Window.configure (bg = Theme.BGColor)
		self.Window.columnconfigure (0, weight = 1)
		self.Window.rowconfigure (0, weight = 1)
		self.SVGFile_OSRCLogo = "Images/LogoOSRC.svg"
		# self. is important for self.OSRCLogo otherwise the data is discarded before displaying so you get no error but no image either!
		self.OSRCLogo = ImageTk.PhotoImage (Image.open (io.BytesIO (cairosvg.svg2png (bytestring = open(self.SVGFile_OSRCLogo, "rb").read (), scale = 1)))) # Either use: "scale = 1" OR "output_width = 150, output_height = 150"
		self.Window.iconphoto (True, self.OSRCLogo)
		self.SVGFile_SpeakerIcon = "Images/Speaker.svg"
		self.SVGFile_MicIcon = "Images/Microphone.svg"
		self.EnterBinding = None
		self.SpaceBinding = None
		self.EscBinding = None
		self.RBinding = None
		self.CtrlEnterBinding = None
		self.CtrlRBinding = None
		self.CtrlShiftRBinding = None
		self.CtrlShiftHBinding = None
		self.CtrlABinding = None # [Ctrl] + [A] for selecting all text in focused textbox... (everywhere...)
		self.VoiceInitialized = False
	
	
	
	def SetKeys (self, KeysObject): # Called once after password request screen. This destroys the first window to do something outside the GUI class.
		try:
			self.Window.destroy ()
		except:
			pass
		if KeysObject.UserKey:
			self.K = KeysObject
			self.Window = tk.Tk (className = "HexaPA") # Not sure why the className is displayed as "HexaPA" instead of "HexaPA" as I set it... (on ubuntu)
			self.Window.title ("HexaPA")
			self.Window.geometry (f"{self.WinWidth}x{self.WinHeight}+{self.WinPosX}+{self.WinPosY}")
			self.Window.resizable (True, True)
			self.Window.configure (bg = Theme.BGColor)
			self.Window.columnconfigure (0, weight = 1)
			self.Window.rowconfigure (0, weight = 1)
			# self. is important for self.OSRCLogo otherwise the data is discarded before displaying so you get no error but no image either!
			self.OSRCLogo = ImageTk.PhotoImage (Image.open (io.BytesIO (cairosvg.svg2png (bytestring = open (self.SVGFile_OSRCLogo, "rb").read (), scale = 1)))) # Either use: "scale = 1" OR "output_width = 150, output_height = 150"
			self.Window.iconphoto (True, self.OSRCLogo) # Must reload the image before passing it to the second window, otherwise it crashes... Maybe the destructor if the first window breaks it.
			self.PWD = None
	
	
	
	def InitChain (self):
		self.Conversation = BlockChain (LogT.BlockChain)
		return self.Conversation
	
	
	
	def Link_OSRC (self):
		webbrowser.open_new_tab ("osrc.rip")
	
	
	
	def Link_OpenAI_API (self):
		webbrowser.open_new_tab ("https://platform.openai.com/overview")
	
	
	
	def Link_DeepSeek_API (self):
		webbrowser.open_new_tab ("https://platform.deepseek.com/sign_in")
	
	
	
	def InitVoice (self):
		self.VoiceInitialized = True
		HL.Log ("GUI.py: TTS WDir: " + self.S.WorkDir.TTSDir, 'I', LogT.GUI)
		TTS (self.S.API, self.S.TTSModel, self.S.WorkDir.TTSDir, self.S.KeepAudio, self.K.Key_Lookup.get ("OpenAI"))
		STT (self.S.API, self.S.STTModel, self.K.Key_Lookup.get ("OpenAI"))
	
	
	
	def PasswordRequestSubmitAction (self):
		if self.S.UserName == "" and self.PasswordRequestWindow.UserNameEntry.get ().strip () != "":
			self.S.UserName = self.PasswordRequestWindow.UserNameEntry.get ().strip ()
			self.S.SaveSettings ()
		self.PWD = self.PasswordRequestWindow.PasswordEntry.get ().strip ()
		self.WinWidth = self.Window.winfo_width ()
		self.WinHeight = self.Window.winfo_height ()
		self.WinPosX = self.Window.winfo_x ()
		self.WinPosY = self.Window.winfo_y ()
		self.Window.unbind ('<Return>', self.EnterBinding)
		self.Window.unbind ('<Escape>', self.EscBinding)
		self.Window.unbind ('<Control-H>', self.CtrlShiftHBinding)
		if platform.system () != 'Darwin':
			self.Window.unbind ('<Control-a>', self.CtrlABinding)
		else:
			self.Window.unbind ('<Command-a>', self.CtrlABinding)
		self.Window.destroy ()
	
	
	
	def TogglePassword (self):
		if self.PasswordRequestWindow.ShowPassword.get():
			self.PasswordRequestWindow.PasswordEntry.config (show = "")
		else:
			self.PasswordRequestWindow.PasswordEntry.config (show = "*")
	
	
	
	def PasswordRequest (self):
		self.PasswordRequestWindow = Window (self.Window)
		self.PasswordRequestWindow.Base.columnconfigure (0, weight = 1)
		
		### Title
		self.PasswordRequestWindow.TitleFrame (self.PasswordRequestWindow.Base, 0, 0, Command = self.Link_OSRC)
		
		### Password Frame
		self.PasswordRequestWindow.PasswordFrame = None
		self.PasswordRequestWindow.PasswordFrame = Window.Frame (self.PasswordRequestWindow.Base, Row = 1, Column = 0, Sticky = "N")
		self.PasswordRequestWindow.PasswordFrame.columnconfigure (0, weight = 1)
		self.PasswordRequestWindow.PasswordInfoLabel = None
		self.PasswordRequestWindow.PasswordInfoLabel = Window.Label (self.PasswordRequestWindow.PasswordFrame, 0, 0, "EW", "Your username and password is used to encrypt / decrypt your API credentials and\nconversations, to prevent others from using your API key(s) for free or accessing\nyour data. If you don't yet have one, it will be created. (Make sure it's correct!)\nCurrently this can only handle a single user.", Theme.BGColor, Theme.SmallText, Theme.SmallTextSize, Width = None, PadX = None, PadY = None)
		self.PasswordRequestWindow.RequestLabel = None
		self.PasswordRequestWindow.UserNameEntry = None
		if self.S.UserName == "":
			self.PasswordRequestWindow.RequestLabel = Window.Label (self.PasswordRequestWindow.PasswordFrame, 1, 0, "EW", "Please enter your username!", Theme.BGColor, Theme.Text, Theme.TextSize, Width = None, PadX = None, PadY = None)
			self.PasswordRequestWindow.UserNameEntry = Window.Entry (self.PasswordRequestWindow.PasswordFrame, 2, 0, None, Width = 50, PadX = None)
			self.PasswordRequestWindow.UserNameEntry.focus ()
		else:
			self.PasswordRequestWindow.RequestLabel = Window.Label (self.PasswordRequestWindow.PasswordFrame, 1, 0, "EW", "Username:", Theme.BGColor, Theme.Text, Theme.TextSize, Width = None, PadX = None, PadY = None)
			self.PasswordRequestWindow.UserNameEntry = Window.Entry (self.PasswordRequestWindow.PasswordFrame, 2, 0, None, self.S.UserName, Width = None, PadX = None, Justify = "center")
			self.PasswordRequestWindow.UserNameEntry.configure (state = tk.DISABLED)
		self.PasswordRequestWindow.RequestLabel = None
		self.PasswordRequestWindow.RequestLabel = Window.Label (self.PasswordRequestWindow.PasswordFrame, 3, 0, "EW", "Please enter your password!", Theme.BGColor, Theme.Text, Theme.TextSize, Width = None, PadX = None, PadY = None)
		self.PasswordRequestWindow.EntryFrame = None
		self.PasswordRequestWindow.EntryFrame = Window.Frame (self.PasswordRequestWindow.PasswordFrame, Row = 4, Column = 0, Sticky = "EW")
		self.PasswordRequestWindow.EntryFrame.columnconfigure (0, weight = 1)
		self.PasswordRequestWindow.PasswordEntry = None
		self.PasswordRequestWindow.PasswordEntry = Window.Entry (self.PasswordRequestWindow.EntryFrame, 0, 0, None, Width = 50, PadX = None, Show = "*")
		if self.S.UserName != "":
			self.PasswordRequestWindow.PasswordEntry.focus ()
		self.PasswordRequestWindow.ShowPassword = tk.BooleanVar ()
		self.PasswordRequestWindow.ShowPassword.set (False)
		self.PasswordRequestWindow.ShowButton = None
		self.PasswordRequestWindow.ShowButton = Window.CheckButton (self.PasswordRequestWindow.EntryFrame, 0, 1, "E", "Show", self.PasswordRequestWindow.ShowPassword, self.TogglePassword, Height = 1)
		self.PasswordRequestWindow.WinInfoLabel = None
		self.PasswordRequestWindow.WinInfoLabel = Window.Label (self.PasswordRequestWindow.PasswordFrame, 5, 0, "EW", "The window will close briefly while processing your input and while\ndecrypting and testing your API key(s) if your API key(s) is/are already set.", Theme.BGColor, Theme.SmallText, Theme.SmallTextSize, Width = None, PadX = None, PadY = None)
		self.PasswordRequestWindow.SubmitButton = None
		self.PasswordRequestWindow.SubmitButton = Window.Button (self.PasswordRequestWindow.PasswordFrame, 6, 0, None, "Submit", self.PasswordRequestSubmitAction, Width = 10, Height = 2)
		
		# Key bindings
		self.EnterBinding = self.Window.bind ('<Return>', lambda event: self.PasswordRequestWindow.SubmitButton.invoke ())
		self.EscBinding = self.Window.bind ('<Escape>', lambda event: self.Window.destroy ())
		self.CtrlShiftHBinding = self.Window.bind ('<Control-H>', lambda event: self.PasswordRequestWindow.ShowButton.invoke ())
		if platform.system () != 'Darwin':
			self.CtrlABinding = self.Window.bind ('<Control-a>', lambda event: event.widget.select_range (0, 'end')) # [Ctrl / Cmd] + [A]
		else:
			self.CtrlABinding = self.Window.bind ('<Command-a>', lambda event: event.widget.select_range (0, 'end')) # [Ctrl / Cmd] + [A]
	
	
	
	
	
	
	
	def KeyRequestSubmitAction (self):
		self.KeyRequestWindow.SubmitButton.configure (state = tk.DISABLED)
		self.K.Key_OpenAI = self.KeyRequestWindow.KeyEntry_OpenAI.get ().strip ()
		self.K.Key_DeepSeek = self.KeyRequestWindow.KeyEntry_DeepSeek.get ().strip ()
		if self.K.Key_OpenAI:
			self.K.Key_Lookup[Communicate.API_Lookup.get (self.S.OpenAI_DefaultModel)] = self.K.Key_OpenAI
			Communicate (Communicate.API_Lookup.get (self.S.OpenAI_DefaultModel), self.S.OpenAI_DefaultModel, self.K.Key_Lookup.get (Communicate.API_Lookup.get (self.S.OpenAI_DefaultModel))) # Test key
		if self.K.Key_DeepSeek: # Invalid or no Open AI key...
			self.K.Key_Lookup[Communicate.API_Lookup.get (self.S.DeepSeek_DefaultModel)] = self.K.Key_DeepSeek
			Communicate (Communicate.API_Lookup.get (self.S.DeepSeek_DefaultModel), self.S.DeepSeek_DefaultModel, self.K.Key_Lookup.get (Communicate.API_Lookup.get (self.S.DeepSeek_DefaultModel))) # Test key
			if self.K.Key_OpenAI == "": # OpenAI is default, so if it's key not given, but DeepSeek key is, then default to Deepsek API and Model
				self.S.API = Communicate.API_Lookup.get (self.S.DeepSeek_DefaultModel)
				self.S.AIModel = self.S.DeepSeek_DefaultModel
		self.S.SaveSettings ()
		
		if Communicate.Disabled_OpenAI != True or Communicate.Disabled_DeepSeek != True:
			self.Window.unbind ('<Return>', self.EnterBinding)
			self.Window.unbind ('<Escape>', self.EscBinding)
			if platform.system () != 'Darwin':
				self.Window.unbind ('<Control-a>', self.CtrlABinding)
			else:
				self.Window.unbind ('<Command-a>', self.CtrlABinding)
			self.K.SaveKeys ()
			self.KeyRequestWindow.Base.grid_forget ()
			self.Main ()
		else: # Neither Key accepted
			self.KeyRequestWindow.ErrorLabel.config (text = "Error: All keys key is invalid or missing! Please try again!")
			self.KeyRequestWindow.SubmitButton.configure (state = tk.NORMAL)
	
	
	
	def KeyRequestSkipAction (self):
		self.Window.unbind ('<Return>', self.EnterBinding)
		self.Window.unbind ('<Escape>', self.EscBinding)
		if platform.system () != 'Darwin':
			self.Window.unbind ('<Control-a>', self.CtrlABinding)
		else:
			self.Window.unbind ('<Command-a>', self.CtrlABinding)
		self.KeyRequestWindow.Base.grid_forget ()
		self.Main ()
	
	
	
	def RequestKey (self, Error = None):
		self.KeyRequestWindow = Window (self.Window)
		self.KeyRequestWindow.Base.columnconfigure (0, weight = 1)
		
		### Title
		self.KeyRequestWindow.TitleFrame (self.KeyRequestWindow.Base, 0, 0, Command = self.Link_OSRC)
		
		### OpenAI frame
		self.KeyRequestWindow.OpenAIFrame = None
		self.KeyRequestWindow.OpenAIFrame = Window.Frame (self.KeyRequestWindow.Base, Row = 1, Column = 0, Sticky = "N")
		self.KeyRequestWindow.OpenAIFrame.columnconfigure (0, weight = 1)
		self.KeyRequestWindow.PoweredByLogo = None
		self.KeyRequestWindow.PoweredByLogo = Window.Frame (self.KeyRequestWindow.OpenAIFrame, Row = 0, Column = 0, Sticky = "EW")
		self.KeyRequestWindow.PoweredByLogo.columnconfigure (0, weight = 1)
		self.KeyRequestWindow.PoweredByLogo.rowconfigure (0, weight = 1)
		self.KeyRequestWindow.PoweredByLabel = None
		self.KeyRequestWindow.PoweredByLabel = Window.Label (self.KeyRequestWindow.PoweredByLogo, 0, 0, "NSE", "Powered by:", Theme.BGColor, TextSize = 24, Anchor = "center", Width = None)
		self.OpenAILogo = ImageTk.PhotoImage (Image.open (io.BytesIO (cairosvg.svg2png (bytestring = open ("Images/openai-white-lockup.svg", "rb").read (), scale = 0.225)))) # Either use: "scale = 1" OR "output_width = 150, output_height = 150"
		self.KeyRequestWindow.OpenAILogo = None
		self.KeyRequestWindow.OpenAILogo = Window.ImageLabel (self.KeyRequestWindow.PoweredByLogo, 0, 1, "W", self.OpenAILogo, PadX = 15, PadY = 20, Command = self.Link_OpenAI_API)
		Text = "Please enter your OpenAI API key!\nIf you don't have one clik here and get one."
		self.KeyRequestWindow.OpenAIRequestLabel = None
		self.KeyRequestWindow.OpenAIRequestLabel = Window.Label (self.KeyRequestWindow.OpenAIFrame, 1, 0, "EW", Text, Theme.BGColor, Width = None, PadX = None, PadY = None)
		self.KeyRequestWindow.OpenAIRequestLabel.bind ("<Button-1>", lambda e: self.Link_OpenAI_API ())
		Text = "(You will need to register. Once you're logged in, got to API keys on the left and create one.\nIt's affordable, but you may also want to set a monthly limit, just in case.\nThey only train the AI on Chat GPT data but not on API data.)"
		self.KeyRequestWindow.OpenAIGuideLabel = None
		self.KeyRequestWindow.OpenAIGuideLabel = Window.Label (self.KeyRequestWindow.OpenAIFrame, 2, 0, "EW", Text, Theme.BGColor, Theme.SmallText, Theme.SmallTextSize, Width = None, PadX = None, PadY = None)
		self.KeyRequestWindow.OpenAIGuideLabel.bind ("<Button-1>", lambda e: self.Link_OpenAI_API ())
		self.KeyRequestWindow.KeyEntry_OpenAI = None
		self.KeyRequestWindow.KeyEntry_OpenAI = Window.Entry (self.KeyRequestWindow.OpenAIFrame, 3, 0, "EW", Width = 50, PadX = None)
		self.KeyRequestWindow.KeyEntry_OpenAI.focus ()
		
		### DeepSeek frame
		self.KeyRequestWindow.DeepSeekFrame = None
		self.KeyRequestWindow.DeepSeekFrame = Window.Frame (self.KeyRequestWindow.Base, Row = 2, Column = 0, Sticky = "N")
		self.KeyRequestWindow.DeepSeekFrame.columnconfigure (0, weight = 1)
		self.KeyRequestWindow.PoweredByLogo = None
		self.KeyRequestWindow.PoweredByLogo = Window.Frame (self.KeyRequestWindow.DeepSeekFrame, Row = 0, Column = 0, Sticky = "EW")
		self.KeyRequestWindow.PoweredByLogo.columnconfigure (0, weight = 1)
		self.KeyRequestWindow.PoweredByLogo.rowconfigure (0, weight = 1)
		self.KeyRequestWindow.PoweredByLabel = None
		
		self.KeyRequestWindow.PoweredByLabel = Window.Label (self.KeyRequestWindow.PoweredByLogo, 0, 0, "NSE", "Powered by:", Theme.BGColor, TextSize = 24, Anchor = "center", Width = None)
		self.DeepSeekLogo = ImageTk.PhotoImage (Image.open (io.BytesIO (cairosvg.svg2png (bytestring = open ("Images/DeepSeek-Logo.svg", "rb").read (), scale = 1.1)))) # Either use: "scale = 1" OR "output_width = 150, output_height = 150"
		self.KeyRequestWindow.DeepSeekLogo = None
		self.KeyRequestWindow.DeepSeekLogo = Window.ImageLabel (self.KeyRequestWindow.PoweredByLogo, 0, 1, "W", self.DeepSeekLogo, PadX = 15, PadY = 20, Command = self.Link_DeepSeek_API)
		
		Text = "Please enter your DeepSeek API key!\nIf you don't have one clik here and get one."
		self.KeyRequestWindow.DeepSeekRequestLabel = None
		self.KeyRequestWindow.DeepSeekRequestLabel = Window.Label (self.KeyRequestWindow.DeepSeekFrame, 1, 0, "EW", Text, Theme.BGColor, Width = None, PadX = None, PadY = None)
		self.KeyRequestWindow.DeepSeekRequestLabel.bind ("<Button-1>", lambda e: self.Link_DeepSeek_API ())
		Text = "(You will need to register. Once you're logged in, got to API keys on the left and create one.\nIt's affordable, but you may also want to set a monthly limit, just in case.\nNote that they do train the AI on API data as far as I know.)"
		self.KeyRequestWindow.DeepSeekGuideLabel = None
		self.KeyRequestWindow.DeepSeekGuideLabel = Window.Label (self.KeyRequestWindow.DeepSeekFrame, 2, 0, "EW", Text, Theme.BGColor, Theme.SmallText, Theme.SmallTextSize, Width = None, PadX = None, PadY = None)
		self.KeyRequestWindow.DeepSeekGuideLabel.bind ("<Button-1>", lambda e: self.Link_DeepSeek_API ())
		self.KeyRequestWindow.KeyEntry_DeepSeek = None
		self.KeyRequestWindow.KeyEntry_DeepSeek = Window.Entry (self.KeyRequestWindow.DeepSeekFrame, 3, 0, "EW", Width = 50, PadX = None)
		
		### Common frame
		self.KeyRequestWindow.CommonFrame = None
		self.KeyRequestWindow.CommonFrame = Window.Frame (self.KeyRequestWindow.Base, Row = 3, Column = 0, Sticky = "EW")
		self.KeyRequestWindow.CommonFrame.columnconfigure (0, weight = 1)
		self.KeyRequestWindow.CommonFrame.rowconfigure (0, weight = 1)
		if Error == None:
			Error = ""
		self.KeyRequestWindow.ErrorLabel = None
		self.KeyRequestWindow.ErrorLabel = Window.Label (self.KeyRequestWindow.CommonFrame, 0, 0, "EW", Error, Theme.BGColor, Theme.Error, Width = None, PadX = None, PadY = None)
		self.KeyRequestWindow.ButtonsFrame = None
		self.KeyRequestWindow.ButtonsFrame = Window.Frame (self.KeyRequestWindow.CommonFrame, Row = 1, Column = 0, Sticky = None)
		self.KeyRequestWindow.SubmitButton = None
		self.KeyRequestWindow.SubmitButton = Window.Button (self.KeyRequestWindow.ButtonsFrame, 0, 0, None, "Submit", self.KeyRequestSubmitAction, Width = 10, Height = 2)
		self.KeyRequestWindow.SkipButton = None
		self.KeyRequestWindow.SkipButton = Window.Button (self.KeyRequestWindow.ButtonsFrame, 0, 1, None, "Skip", self.KeyRequestSkipAction, Width = 10, Height = 2)
		
		# Key bindings
		self.EnterBinding = self.Window.bind ('<Return>', lambda event: self.KeyRequestWindow.SubmitButton.invoke ())
		self.EscBinding = self.Window.bind ('<Escape>', lambda event: self.KeyRequestWindow.SkipButton.invoke ())
		if platform.system () != 'Darwin':
			self.CtrlABinding = self.Window.bind ('<Control-a>', lambda event: event.widget.select_range (0, 'end')) # [Ctrl / Cmd] + [A]
		else:
			self.CtrlABinding = self.Window.bind ('<Command-a>', lambda event: event.widget.select_range (0, 'end')) # [Ctrl / Cmd] + [A]
	
	
	
	
	
	
	
	def CreateNewChat (self):
		self.Window.unbind ('<Return>', self.EnterBinding)
		self.S.AIModel = self.MainWindow.Model.get ()
		self.S.API = Communicate.API_Lookup.get (self.S.AIModel)
		HL.Log ("GUI.py: Selected API: " + self.S.API, 'D', LogT.GUI)
		HL.Log ("GUI.py: Selected model: " + self.S.AIModel, 'D', LogT.GUI)
		self.S.MaxContextMsg = int (self.MainWindow.MaxContextMsgEntry.get ())
		self.S.MaxTokens = int (self.MainWindow.MaxTokensEntry.get ())
		self.S.MaxOTokens = int (self.MainWindow.MaxOTokensEntry.get ())
		self.S.Temperature = float (self.MainWindow.TempEntry.get ())
		self.S.TopP = float (self.MainWindow.TopPEntry.get ())
		self.S.PresencePenalty = float (self.MainWindow.PresPEntry.get ())
		self.S.FrequencyPenalty = float (self.MainWindow.FreqPEntry.get ())
		self.Conversation.Subject = self.MainWindow.Subject.get ()
		if self.Conversation.Subject != "Enter the subject here... (optional)" and self.Conversation.Subject != "":
			HL.Log ("GUI.py: Creating new conversation with subject: " + self.Conversation.Subject, 'I', LogT.GUI)
		else:
			HL.Log ("GUI.py: Creating new conversation with unknown subject.", 'I', LogT.GUI)
		self.MainWindow.Base.grid_forget ()
		self.Chat ()
	
	
	
	def ContinueExistingChat (self, ArgList):
		self.Window.unbind ('<Return>', self.EnterBinding)
		self.S.AIModel = self.MainWindow.Model.get ()
		self.S.API = Communicate.API_Lookup.get (self.S.AIModel)
		HL.Log ("GUI.py: Selected API: " + self.S.API, 'D', LogT.GUI)
		HL.Log ("GUI.py: Selected model: " + self.S.AIModel, 'D', LogT.GUI)
		self.S.MaxContextMsg = int (self.MainWindow.MaxContextMsgEntry.get ())
		self.S.MaxTokens = int (self.MainWindow.MaxTokensEntry.get ())
		self.S.MaxOTokens = int (self.MainWindow.MaxOTokensEntry.get ())
		self.S.Temperature = float (self.MainWindow.TempEntry.get ())
		self.S.TopP = float (self.MainWindow.TopPEntry.get ())
		self.S.PresencePenalty = float (self.MainWindow.PresPEntry.get ())
		self.S.FrequencyPenalty = float (self.MainWindow.FreqPEntry.get ())
		HL.Log ("GUI.py: Loading: " + str (self.MainWindow.ConversationList[ArgList[0]].File), 'I', LogT.GUI)
		self.Conversation.Load (self.MainWindow.ConversationList[ArgList[0]].File)
		self.MainWindow.Base.grid_forget ()
		self.Chat ()
		self.Window.update ()
		self.MainWindow.Base.destroy ()
	
	
	
	def DeleteChat (self, ArgList):
		try:
			os.remove(self.MainWindow.ConversationList[ArgList[0]].File)
			HL.Log ("GUI.py: Deleted: " + str (self.MainWindow.ConversationList[ArgList[0]].File), 'I', LogT.GUI)
		except OSError as e:
			HL.Log ("GUI.py: Error deleting " + str (self.MainWindow.ConversationList[ArgList[0]].File) + f": {e}", 'E', LogT.GUI)
		self.MainWindow.Base.grid_forget ()
		self.Main ()
	
	
	
	def Main (self):
		self.MainWindow = Window (self.Window)
		self.MainWindow.Base.columnconfigure (0, weight = 1)
		self.MainWindow.Base.rowconfigure (1, weight = 1) # Set row 1 to expand not 0 here...
		
		### Title
		self.MainWindow.TitleFrame (self.MainWindow.Base, 0, 0, Command = self.Link_OSRC)
		
		### Tooltip label
		self.MainWindow.TooltipFrame = None
		self.MainWindow.TooltipFrame = Window.Frame (self.MainWindow.Base, Row = 3, Column = 0, Sticky = "EW", PadX = 0, PadY = 0)
		self.MainWindow.TooltipFrame.columnconfigure (0, weight = 1)
		self.MainWindow.TooltipLabel = None
		self.MainWindow.TooltipLabel = Window.Label (self.MainWindow.TooltipFrame, 0, 0, "NSEW", "", Theme.BGColor, Theme.SmallText, Theme.SmallTextSize, Anchor = "w", PadX = 0, PadY = 0, Height = 2) # Hight must be limited otherwise the label may push other widgets out from beneath the mouse, and it oscillates between Tooltip and no Tooltip...
		
		### Conversation list
		self.MainWindow.Canvas = None
		self.MainWindow.CanvasInnerFrame = None
		self.MainWindow.Canvas, self.MainWindow.CanvasInnerFrame = Window.ScrollCanvas (self.MainWindow.Base, 1, 0, "NSEW")
		
		## New Chat
		self.MainWindow.NewChatFrame = None
		self.MainWindow.NewChatFrame = Window.Frame (self.MainWindow.CanvasInnerFrame, Theme.PromptBG, Packed = True)
		self.MainWindow.Subject = None
		self.MainWindow.Subject = Window.Entry (self.MainWindow.NewChatFrame, 0, 0, "EW", Text = "Enter the subject here... (optional)", TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = "Optional but if no subject is given, it will be generated from the first prompt, just like ChatGPT does. (Using extra ~100 tokens for instructions + first message worth of tokens at your expense. :P)\nHotkey/combination: [Space]")
		self.MainWindow.Subject.bind ("<FocusIn>", lambda event: self.MainWindow.Subject.delete (0, 'end')) # click event that clears the field.
		self.MainWindow.Subject.bind ("<FocusOut>", lambda event: self.MainWindow.Subject.insert (0, "Enter the subject here... (optional)")) # click event that clears the field.
		self.MainWindow.NewChatButton = None
		self.MainWindow.NewChatButton = Window.Button (self.MainWindow.NewChatFrame, 0, 1, "E", "Start new conversation", self.CreateNewChat, Width = 18, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = "Start new conversation (Only saved after first prompt.)\nHotkey/combination: [Enter]")
		
		## Existing conversations
		self.MainWindow.ConversationList = []
		ConversationDir = "Conversations"
		for BinFile in glob.glob (os.path.join (ConversationDir, "*.bin")):
			X = BlockChain (LogT.BlockChain)
			X.Load (BinFile)
			Index = len (self.MainWindow.ConversationList) # A new object is being added to the list so the index should be it's former length...
			if Index % 2 == 0:
				self.MainWindow.ConversationList.append (Window (self.MainWindow.CanvasInnerFrame, BGColor = Theme.ResponseBG, Packed = True))
			else:
				self.MainWindow.ConversationList.append (Window (self.MainWindow.CanvasInnerFrame, BGColor = Theme.PromptBG, Packed = True))
			self.MainWindow.ConversationList[Index].Base.columnconfigure (1, weight = 1)
			self.MainWindow.ConversationList[Index].Base.rowconfigure (0, weight = 1)
			self.MainWindow.ConversationList[Index].File = None
			self.MainWindow.ConversationList[Index].File = BinFile
			self.MainWindow.ConversationList[Index].DeleteButton = None
			self.MainWindow.ConversationList[Index].ContinueButton = Window.Button (self.MainWindow.ConversationList[Index].Base, 0, 0, "E", "Delete", self.DeleteChat, [Index], 5)
			self.MainWindow.ConversationList[Index].Label = None
			if Index % 2 == 0:
				self.MainWindow.ConversationList[Index].Label = Window.Label (self.MainWindow.ConversationList[Index].Base, 0, 1, "EW", X.Subject + " (Created at " + X.CreationTime + ")", Theme.ResponseBG, Anchor = "w")
			else:
				self.MainWindow.ConversationList[Index].Label = Window.Label (self.MainWindow.ConversationList[Index].Base, 0, 1, "EW", X.Subject + " (Created at " + X.CreationTime + ")", Theme.PromptBG, Anchor = "w")
			self.MainWindow.ConversationList[Index].ContinueButton = None
			self.MainWindow.ConversationList[Index].ContinueButton = Window.Button (self.MainWindow.ConversationList[Index].Base, 0, 2, "E", "Continue conversation", self.ContinueExistingChat, [Index], 18)
		
		## Update canvas scroll region...
		self.MainWindow.CanvasInnerFrame.update_idletasks ()
		self.MainWindow.Canvas.configure (scrollregion = self.MainWindow.Canvas.bbox ('all'))
		
		### Settings
		self.MainWindow.SettingsFrame = None
		self.MainWindow.SettingsFrame = Window.Frame (self.MainWindow.Base, Row = 2, Column = 0, PadX = 0, PadY = 0, Sticky = "EW")
		self.MainWindow.SettingsFrame.columnconfigure (0, weight = 1)
		self.MainWindow.SettingsLabel = None
		self.MainWindow.SettingsLabel = Window.Label (self.MainWindow.SettingsFrame, 0, 0, "W", "Settings:", Theme.BGColor, Anchor = "w", Width = None)
		
		## Model
		self.MainWindow.ModelFrame = None
		self.MainWindow.ModelFrame = Window.Frame (self.MainWindow.SettingsFrame, Row = 1, Column = 0, PadY = 0, Sticky = "W")
		self.MainWindow.ModelFrame.columnconfigure (1, weight = 1)
		self.MainWindow.ModelFrame.columnconfigure (3, weight = 1)
		self.MainWindow.ModelLabel1 = None
		self.MainWindow.ModelLabel1 = Window.Label (self.MainWindow.ModelFrame, 0, 0, "W", "Model Options:", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.ModelLabel1 = None
		self.MainWindow.ModelLabel1 = Window.Label (self.MainWindow.ModelFrame, 1, 0, "W", "OpenAI:", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.ModelLabel2 = None
		self.MainWindow.ModelLabel2 = Window.Label (self.MainWindow.ModelFrame, 2, 0, "W", "Deepseek:", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.Model = tk.StringVar ()
		self.MainWindow.GPT4oMiniButton = None
		self.MainWindow.SpacerLabel = None
		self.MainWindow.GPT4oButton = None
		self.MainWindow.Spacer2Label = None
		self.MainWindow.GPT4Button = None
		self.MainWindow.DSChatButton = None
		GPT4oMiniTooltip = "Cheaper, faster, fairly capable, available to eveyone, with 128K context length but 16k output.\n(Successor of GPT 3.5 Turbo, Training Data: Oct 2023, Output Token Limit 16384.)"
		GPT4oTooltip = "More expensive, slower then 4o Mini but faster and cheaper then 4 Turbo, with 128K context length.\n(Successor of GPT 4 Turbo, Training Data: Oct 2023, Output Token Limit 4096.)"
		GPT4Tooltip = "More expensive, slower, very capable, available after first payment of $1, with 128K context length.\n(Training Data: Dec 2023, Output Token Limit 4096.)"
		DSChatTooltip = "Advanced and cheap Chinese alternative, with 64K context length. They use API data for training!\n(Training Data: ???, Output Token Limit 8000.)"
		self.MainWindow.GPT4oMiniButton = Window.RadioButton (self.MainWindow.ModelFrame, 1, 1, "W", "GPT-4o Mini", self.MainWindow.Model, "gpt-4o-mini", Default = (self.S.AIModel == "gpt-4o-mini"), Width = 12, Height = 1, PadX = 0, PadY = 0, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = GPT4oMiniTooltip)
		self.MainWindow.SpacerLabel = Window.Label (self.MainWindow.ModelFrame, 1, 2, "W", "", Theme.BGColor, Anchor = "w", Width = 1)
		self.MainWindow.GPT4oButton = Window.RadioButton (self.MainWindow.ModelFrame, 1, 3, "W", "GPT-4o", self.MainWindow.Model, "gpt-4o", Default = (self.S.AIModel == "gpt-4o"), Width = 8, Height = 1, PadX = 0, PadY = 0, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = GPT4oTooltip)
		self.MainWindow.Spacer2Label = Window.Label (self.MainWindow.ModelFrame, 1, 4, "W", "", Theme.BGColor, Anchor = "w", Width = 1)
		self.MainWindow.GPT4Button = Window.RadioButton (self.MainWindow.ModelFrame, 1, 5, "W", "GPT-4 Turbo", self.MainWindow.Model, "gpt-4-turbo", Default = (self.S.AIModel == "gpt-4-turbo"), Width = 12, Height = 1, PadX = 0, PadY = 0, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = GPT4Tooltip)
		self.MainWindow.DSChatButton = Window.RadioButton (self.MainWindow.ModelFrame, 2, 1, "W", "Chat", self.MainWindow.Model, "deepseek-chat", Default = (self.S.AIModel == "deepseek-chat"), Width = 12, Height = 1, PadX = 0, PadY = 0, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = DSChatTooltip)
		if Communicate.Disabled_OpenAI == True:
			self.MainWindow.GPT4oMiniButton.config (state = tk.DISABLED)
			self.MainWindow.GPT4oButton.config (state = tk.DISABLED)
			self.MainWindow.GPT4Button.config (state = tk.DISABLED)
		elif Communicate.Disabled_DeepSeek == True:
			self.MainWindow.DSChatButton.config (state = tk.DISABLED)
		
		## Max Input Tokens
		self.MainWindow.MaxTokensFrame = None
		self.MainWindow.MaxTokensFrame = Window.Frame (self.MainWindow.SettingsFrame, Row = 2, Column = 0, PadY = 0, Sticky = "W")
		self.MainWindow.MaxTokensFrame.columnconfigure (1, weight = 1)
		self.MainWindow.MaxTokensLabel = None
		self.MainWindow.MaxTokensLabel = Window.Label (self.MainWindow.MaxTokensFrame, 0, 0, "W", "Max Input Tokens (Rules + Context + Prompt):", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.MaxTokensEntry = None
		if self.S.AIModel == "gpt-4o-mini":
			self.MainWindow.MaxTokensEntry = Window.Entry (self.MainWindow.MaxTokensFrame, 0, 1, "EW", Text = str (self.S.MaxTokens), Width = 7, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = "Limits input tokens you pay for, but may also cripples the AI's ability to \"remember\" previous messages.\n(Max 128k total tokens but max 16K output is part of that.)")
		else: # both 4o and 4-turbo
			self.MainWindow.MaxTokensEntry = Window.Entry (self.MainWindow.MaxTokensFrame, 0, 1, "EW", Text = str (self.S.MaxTokens), Width = 7, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = "Limits intput tokens you pay for, but may also cripples the AI's ability to \"remember\" previous messages.\n(Max 128k total tokens but max 4K output is part of that.)")
		
		## Max Context Messages
		self.MainWindow.MaxContextMsgFrame = None
		self.MainWindow.MaxContextMsgFrame = Window.Frame (self.MainWindow.SettingsFrame, Row = 3, Column = 0, PadY = 0, Sticky = "W")
		self.MainWindow.MaxContextMsgFrame.columnconfigure (1, weight = 1)
		self.MainWindow.MaxContextMsgLabel = None
		self.MainWindow.MaxContextMsgLabel = Window.Label (self.MainWindow.MaxContextMsgFrame, 0, 0, "W", "Max Context Messages (Even numbers recommended.):", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.MaxContextMsgEntry = None
		self.MainWindow.MaxContextMsgEntry = Window.Entry (self.MainWindow.MaxContextMsgFrame, 0, 1, "EW", Text = str (self.S.MaxContextMsg), Width = 5, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = "The last n messages included as context, influences how far back the AI \"remembers\" the conversation.\n(Even numbers recommended.)")
		
		## Max Output Tokens
		self.MainWindow.MaxOTokensFrame = None
		self.MainWindow.MaxOTokensFrame = Window.Frame (self.MainWindow.SettingsFrame, Row = 4, Column = 0, PadY = 0, Sticky = "W")
		self.MainWindow.MaxOTokensFrame.columnconfigure (1, weight = 1)
		self.MainWindow.MaxOTokensLabel = None
		self.MainWindow.MaxOTokensLabel = Window.Label (self.MainWindow.MaxOTokensFrame, 0, 0, "W", "Max Output Tokens (AI generated):", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.MaxOTokensEntry = None
		self.MainWindow.MaxOTokensEntry = Window.Entry (self.MainWindow.MaxOTokensFrame, 0, 1, "EW", Text = str (self.S.MaxOTokens), Width = 7, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = "Limits output tokens you pay for, but may also cut the AI's response short.\n(Automatically reduced when rules + context + prompt tokens exceed 128k - max output tokens.)")
		
		## Temperature
		self.MainWindow.TempFrame = None
		self.MainWindow.TempFrame = Window.Frame (self.MainWindow.SettingsFrame, Row = 5, Column = 0, PadY = 0, Sticky = "W")
		self.MainWindow.TempFrame.columnconfigure (1, weight = 1)
		self.MainWindow.TempLabel = None
		self.MainWindow.TempLabel = Window.Label (self.MainWindow.TempFrame, 0, 0, "W", "Temperature (Float):", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.TempEntry = None
		self.MainWindow.TempEntry = Window.Entry (self.MainWindow.TempFrame, 0, 1, "EW", Text = str (self.S.Temperature), Width = 5, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = "Determines the likelyness of same result twice for the same question. Range 0.0 to 2.0 (Default = 1.0, Deterministic = 0.0, Random = 2.0, Recommended to adjust either this or top percentage.)")
		
		## TopP
		self.MainWindow.TopPFrame = None
		self.MainWindow.TopPFrame = Window.Frame (self.MainWindow.SettingsFrame, Row = 6, Column = 0, PadY = 0, Sticky = "W")
		self.MainWindow.TopPFrame.columnconfigure (1, weight = 1)
		self.MainWindow.TopPLabel = None
		self.MainWindow.TopPLabel = Window.Label (self.MainWindow.TopPFrame, 0, 0, "W", "Top Percentage (Float):", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.TopPEntry = None
		self.MainWindow.TopPEntry = Window.Entry (self.MainWindow.TopPFrame, 0, 1, "EW", Text = str (self.S.TopP), Width = 5, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = "The AI considers top percentage of most probable answers. Range 0.0 to 1.0 (Default = 1.0, Deterministic = 0.0, Random = 1.0, Recommended to adjust either this or temperature.)")
		
		## Presence Penalty
		self.MainWindow.PresPFrame = None
		self.MainWindow.PresPFrame = Window.Frame (self.MainWindow.SettingsFrame, Row = 7, Column = 0, PadY = 0, Sticky = "W")
		self.MainWindow.PresPFrame.columnconfigure (1, weight = 1)
		self.MainWindow.PresPLabel = None
		self.MainWindow.PresPLabel = Window.Label (self.MainWindow.PresPFrame, 0, 0, "W", "Presence Penalty (Float):", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.PresPEntry = None
		self.MainWindow.PresPEntry = Window.Entry (self.MainWindow.PresPFrame, 0, 1, "EW", Text = str (self.S.PresencePenalty), Width = 5, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = "Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. Range -2.0 to 2.0 (Default = 0.0)")
		
		## Frequency Penalty
		self.MainWindow.FreqPFrame = None
		self.MainWindow.FreqPFrame = Window.Frame (self.MainWindow.SettingsFrame, Row = 8, Column = 0, PadY = 0, Sticky = "W")
		self.MainWindow.FreqPFrame.columnconfigure (1, weight = 1)
		self.MainWindow.FreqPLabel = None
		self.MainWindow.FreqPLabel = Window.Label (self.MainWindow.FreqPFrame, 0, 0, "W", "Frequency Penalty (Float):", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.FreqPEntry = None
		self.MainWindow.FreqPEntry = Window.Entry (self.MainWindow.FreqPFrame, 0, 1, "EW", Text = str (self.S.FrequencyPenalty), Width = 5, TooltipLabel = self.MainWindow.TooltipLabel, TooltipText = "Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim. Range -2.0 to 2.0 (Default = 0.0)")
		
		### Key bindings
		self.SpaceBinding = self.Window.bind ('<space>', lambda event: self.MainWindow.Subject.focus ())
		self.EnterBinding = self.Window.bind ('<Return>', lambda event: self.MainWindow.NewChatButton.invoke ())
		if platform.system () != 'Darwin':
			self.CtrlABinding = self.Window.bind ('<Control-a>', lambda event: event.widget.select_range (0, 'end')) # [Ctrl / Cmd] + [A]
		else:
			self.CtrlABinding = self.Window.bind ('<Command-a>', lambda event: event.widget.select_range (0, 'end')) # [Ctrl / Cmd] + [A]
		
		### TTS and STT
		if not self.VoiceInitialized:
			self.InitVoice ()
	
	
	
	
	
	
	
	def ChatBackAction (self):
		self.Window.unbind ('<space>', self.SpaceBinding)
		self.Window.unbind ('<Escape>', self.EscBinding)
		if platform.system () != 'Darwin':
			self.Window.unbind ('<Control-Return>', self.CtrlEnterBinding)
			self.Window.unbind ('<Control-r>', self.CtrlRBinding)
			self.Window.unbind ('<Control-R>', self.CtrlShiftRBinding)
			self.Window.unbind ('<Control-a>', self.CtrlABinding)
		else:
			self.Window.unbind ('<Command-Return>', self.CtrlEnterBinding)
			self.Window.unbind ('<Command-r>', self.CtrlRBinding)
			self.Window.unbind ('<Command-R>', self.CtrlShiftRBinding)
			self.Window.unbind ('<Command-a>', self.CtrlABinding)
		if self.Conversation.File:
			HL.Log ("GUI.py: Saving conversation!", 'I', LogT.GUI)
			# Update ratings so the conversation is loaded as left on exit. (This will only work if you return to Main before exiting.)
			for Index in range (0, len (self.ChatWindow.Messages)):
				if self.ChatWindow.Messages[Index].Exclude.get () == True:
					self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = -1
				elif self.ChatWindow.Messages[Index].Include.get () == True:
					self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = 1
				else:
					self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = 0
			self.Conversation.Save ()
		self.Conversation.Clear ()
		self.ChatWindow.Base.grid_forget ()
		self.Main ()
		self.Window.update ()
		self.ChatWindow.Base.destroy () # This may take some time if the conversation is long, so better refresh the Main window, to let user decide the next action this way the freezing doesn't seem as long while these objects are destroyed. (Python is terribly slow at this...)
	
	
	
	def ChatRulesAction (self):
		self.Window.unbind ('<space>', self.SpaceBinding)
		self.Window.unbind ('<Escape>', self.EscBinding)
		if platform.system () != 'Darwin':
			self.Window.unbind ('<Control-Return>', self.CtrlEnterBinding)
			self.Window.unbind ('<Control-r>', self.CtrlRBinding)
			self.Window.unbind ('<Control-R>', self.CtrlShiftRBinding)
			self.Window.unbind ('<Control-a>', self.CtrlABinding)
		else:
			self.Window.unbind ('<Command-Return>', self.CtrlEnterBinding)
			self.Window.unbind ('<Command-r>', self.CtrlRBinding)
			self.Window.unbind ('<Command-R>', self.CtrlShiftRBinding)
			self.Window.unbind ('<Command-a>', self.CtrlABinding)
		self.ChatWindow.Base.grid_forget ()
		self.Rules ()
	
	
	
	def ChatCountTokensAction (self):
		# Update ratings for all previous messages. (The user may have changed it...)
		if len (self.ChatWindow.Messages) > 1:
			for Index in range (0, len (self.ChatWindow.Messages)):
				if self.ChatWindow.Messages[Index].Exclude.get () == True:
					self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = -1
				elif self.ChatWindow.Messages[Index].Include.get () == True:
					self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = 1
				else:
					self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = 0
		
		### Construct Rules for sending... (Required by the API)
		if self.Conversation.LatestRules != None:
			Rules = {"role": "system", "content": self.Conversation.Rules.Rules}
		else:
			Rules = {"role": "system", "content": ""}
		
		### Construct Prompt for sending... (Required by the API)
		if self.Conversation.LatestRules != None:
			Prompt = {"role": "user", "content": self.Conversation.Rules.Message + "\n" + self.ChatWindow.UserInputTextBox.get ("1.0", "end").strip ()}
		else:
			Prompt = {"role": "user", "content": self.ChatWindow.UserInputTextBox.get ("1.0", "end").strip ()}
		
		### Generate context... (Optional for the API, but AI doesn't "remember" previous prompt/answer without it...)
		Context = None
		ContextIDs = None
		Messages = []
		Messages.append (Rules)
		Messages.append (Prompt)
		
		# Calculate remaining tokens for context
		T = Tokenizer (self.S.API, self.S.AIModel, Messages)
		MaxContextTokens = self.S.MaxTokens - T.TokenCount_Rules - T.TokenCount_Prompt
		HL.Log ("GUI.py: MaxTokens allowed: " + str (self.S.MaxTokens) + ", Estimated rules tokens: " + str (T.TokenCount_Rules) + ", Estimated prompt tokens: " + str (T.TokenCount_Prompt) + " --> MaxContextTokens " + str (MaxContextTokens) + ", MaxContextMessages: " + str (self.S.MaxContextMsg), 'D', LogT.GUI)
		
		# Generate Context
		ContextIDs, Context = Commands.GenerateContext (self.K.UserKey, self.S, self.Conversation.Blocks, MaxContextTokens)
		
		# Context token estimation
		Messages = []
		Messages.append (Rules)
		if Context != None:
			Messages.extend (Context)
		Messages.append (Prompt)
		T = Tokenizer (self.S.API, self.S.AIModel, Messages)
		self.ChatWindow.StatsLabel.config (text = "Token estimations:   Total to send: " + str (T.TokenCount_Total) + "\nRules: " + str (T.TokenCount_Rules) + "   Context: " + str (T.TokenCount_Context) + "   Prompt: " + str (T.TokenCount_Prompt))
		self.ChatWindow.StatsLabel.lift ()
		self.Window.update ()
	
	
	
	def ChatAutoScroll (self):
		self.ChatWindow.CanvasInnerFrame.update_idletasks ()
		self.ChatWindow.Canvas.configure (scrollregion = self.ChatWindow.Canvas.bbox ('all'))
		self.ChatWindow.Canvas.yview_moveto (1)
	
	
	
	def DisplayMessage (self, UserName = "???", Content = "", MsgData = None): # Either UserName + Content or MsgData must be given!
		if UserName == "???" and MsgData != None:
			UserName = MsgData.Name
		if Content == "" and MsgData != None:
			Content = MsgData.Message
		if len (self.ChatWindow.Messages) > 0:
			if self.ChatWindow.Messages[0].AuthorName == "Developer": # This is just a note from the developer, not part of the conversation, so it should be removed...
				self.ChatWindow.Messages = []
				for Widget in self.ChatWindow.CanvasInnerFrame.winfo_children ():
				        Widget.destroy ()
		Index = len (self.ChatWindow.Messages) # A new object is being added to the list so the index should be it's former length...
		if UserName == self.S.UserName: # This makes the background color difference between prompt and answer frames...
			self.ChatWindow.Messages.append (Window (self.ChatWindow.CanvasInnerFrame, BGColor = Theme.PromptBG, Packed = True))
			self.ChatWindow.Messages[Index].Base.columnconfigure (0, weight = 1)
			self.ChatWindow.Messages[Index].Base.rowconfigure (1, weight = 1)
			self.ChatWindow.Messages[Index].AuthorFrame = None
			self.ChatWindow.Messages[Index].AuthorFrame = Window.Frame (self.ChatWindow.Messages[Index].Base, Theme.PromptBG, 0, 0, 0, 0, "EW")
			self.ChatWindow.Messages[Index].AuthorFrame.columnconfigure (0, weight = 1)
			self.ChatWindow.Messages[Index].Author = None
			self.ChatWindow.Messages[Index].Author = Window.Label (self.ChatWindow.Messages[Index].AuthorFrame, 0, 0, "EW", UserName, Theme.PromptBG, Anchor = "w", Width = None, PadY = Theme.PadY + 3)
			self.ChatWindow.Messages[Index].ButtonFrame = None
			self.ChatWindow.Messages[Index].ButtonFrame = Window.Frame (self.ChatWindow.Messages[Index].AuthorFrame, Theme.PromptBG, 0, 1, Sticky = "NSE")
			self.ChatWindow.Messages[Index].ButtonFrame.rowconfigure (0, weight = 1)
			self.ChatWindow.Messages[Index].RephraseButton = None
			self.ChatWindow.Messages[Index].RephraseButton = Window.Button (self.ChatWindow.Messages[Index].ButtonFrame, 0, 0, "NS", "Rephrase", lambda: (self.ChatWindow.UserInputTextBox.insert ('end', self.ChatWindow.Messages[Index].TextBox.get ("1.0", "end").strip ()), setattr (self.ChatWindow.Messages[Index].MessageData, 'Rating', -1), self.ChatWindow.Messages[Index].Exclude.set (True), self.ChatWindow.Messages[Index].Include.set (False), setattr (self.ChatWindow.Messages[Index + 1].MessageData, 'Rating', -1), self.ChatWindow.Messages[Index + 1].Exclude.set (True), self.ChatWindow.Messages[Index + 1].Include.set (False), self.ChatWindow.UserInputTextBox.focus ()), Width = 6, PadX = 0, PadY = 0, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Shortcut for [Ctrl] + [C], [Ctrl] + [V] and exclusion of this prompt and following response.\nKind of a \"regenerate response\" button with optioal editing before sending. Hotkey/combination(for the last prompt): [Ctrl] + [R]")
		else:
			self.ChatWindow.Messages.append (Window (self.ChatWindow.CanvasInnerFrame, BGColor = Theme.ResponseBG, Packed = True))
			self.ChatWindow.Messages[Index].Base.columnconfigure (0, weight = 1)
			self.ChatWindow.Messages[Index].Base.rowconfigure (1, weight = 1)
			self.ChatWindow.Messages[Index].AuthorFrame = None
			self.ChatWindow.Messages[Index].AuthorFrame = Window.Frame (self.ChatWindow.Messages[Index].Base, Theme.ResponseBG, 0, 0, 0, 0, "EW")
			self.ChatWindow.Messages[Index].AuthorFrame.columnconfigure (0, weight = 1)
			self.ChatWindow.Messages[Index].Author = None
			self.ChatWindow.Messages[Index].Author = Window.Label (self.ChatWindow.Messages[Index].AuthorFrame, 0, 0, "EW", UserName, Theme.ResponseBG, Anchor = "w", Width = None, PadY = Theme.PadY + 3)
			self.ChatWindow.Messages[Index].ButtonFrame = None
			self.ChatWindow.Messages[Index].ButtonFrame = Window.Frame (self.ChatWindow.Messages[Index].AuthorFrame, Theme.ResponseBG, 0, 1, Sticky = "NSE")
			self.ChatWindow.Messages[Index].ButtonFrame.rowconfigure (0, weight = 1)
		self.ChatWindow.Messages[Index].MessageData = None
		if MsgData != None:
			self.ChatWindow.Messages[Index].MessageData = MsgData # Existing message.
		else:
			self.ChatWindow.Messages[Index].MessageData = Data (Name = UserName, Message = Content) # New message.
		self.ChatWindow.Messages[Index].Wrap = tk.BooleanVar (value = 1)
		self.ChatWindow.Messages[Index].WrapButton = None
		self.ChatWindow.Messages[Index].WrapButton = Window.CheckButton (self.ChatWindow.Messages[Index].ButtonFrame, 0, 1, "NS", "Wrap", self.ChatWindow.Messages[Index].Wrap, lambda: self.ChatWindow.Messages[Index].TextBox.configure (wrap = ("word" if self.ChatWindow.Messages[Index].Wrap.get () else "none")), PadY = 0, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Wrap text in the textbox.\n(Wrapping long text is usually desirable, wrapping code may not be. Hance the up-down and left-right scroll bars.)")
		self.ChatWindow.Messages[Index].Exclude = tk.BooleanVar (value = 0)
		self.ChatWindow.Messages[Index].Include = tk.BooleanVar (value = 0)
		self.ChatWindow.Messages[Index].ExcludeButton = None
		self.ChatWindow.Messages[Index].ExcludeButton = Window.CheckButton (self.ChatWindow.Messages[Index].ButtonFrame, 0, 2, "NS", "Exclude", self.ChatWindow.Messages[Index].Exclude, lambda: self.ChatWindow.Messages[Index].Include.set (False), Width = 7, PadX = 0, PadY = 0, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Exclude this message from context.\n(If exclude is checked, the AI will not take it into consideration. It never existed...)")
		self.ChatWindow.Messages[Index].IncludeButton = None
		self.ChatWindow.Messages[Index].IncludeButton = Window.CheckButton (self.ChatWindow.Messages[Index].ButtonFrame, 0, 3, "NS", "Inlcude", self.ChatWindow.Messages[Index].Include, lambda: self.ChatWindow.Messages[Index].Exclude.set (False), Width = 6, PadY = 0, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Include message even if the auto context management is disabled.")
		if self.ChatWindow.Messages[Index].MessageData.Rating > 0:
			self.ChatWindow.Messages[Index].Include.set (True)
		elif self.ChatWindow.Messages[Index].MessageData.Rating < 0:
			self.ChatWindow.Messages[Index].Exclude.set (True)
		self.ChatWindow.Messages[Index].TextBoxFrame = None
		self.ChatWindow.Messages[Index].ScrollX = None
		self.ChatWindow.Messages[Index].ScrollY = None
		self.ChatWindow.Messages[Index].TextBox = None
		self.ChatWindow.Messages[Index].TextBoxFrame, self.ChatWindow.Messages[Index].ScrollX, self.ChatWindow.Messages[Index].ScrollY, self.ChatWindow.Messages[Index].TextBox = Window.TextBox (self.ChatWindow.Messages[Index].Base, 1, 0, PadY = 0, Sticky = "EW")
		if len (self.ChatWindow.Messages) == 1:
			self.ChatWindow.Messages[Index].TextBox.bind ("<FocusIn>", lambda event: (self.ChatWindow.Messages[Index].TextBox.config (height = 18), self.ChatAutoScroll ()) if Index == (len (self.ChatWindow.Messages) - 1) else self.ChatWindow.Messages[Index].TextBox.config (height = 18)) # click event that enlarges the field.
			self.ChatWindow.Messages[Index].TextBox.bind ("<FocusOut>", lambda event: (self.ChatWindow.Messages[Index].TextBox.config (height = 3), self.ChatAutoScroll ()) if Index == (len (self.ChatWindow.Messages) - 1) else self.ChatWindow.Messages[Index].TextBox.config (height = 3)) # click away event that shrinks the field.
		else:
			self.ChatWindow.Messages[Index].TextBox.bind ("<FocusIn>", lambda event: (self.ChatWindow.Messages[Index].TextBox.config (height = 18), self.ChatAutoScroll ()) if Index >= (len (self.ChatWindow.Messages) - 2) else self.ChatWindow.Messages[Index].TextBox.config (height = 18)) # click event that enlarges the field.
			self.ChatWindow.Messages[Index].TextBox.bind ("<FocusOut>", lambda event: (self.ChatWindow.Messages[Index].TextBox.config (height = 3), self.ChatAutoScroll ()) if Index >= (len (self.ChatWindow.Messages) - 2) else self.ChatWindow.Messages[Index].TextBox.config (height = 3)) # click away event that shrinks the field.
		self.ChatWindow.Messages[Index].TextBox.insert ('end', Content)
		self.ChatWindow.Messages[Index].TextBox.configure (state = "disabled")
		self.ChatWindow.Messages[0].AuthorName = UserName
		
		if UserName == "Developer":
			self.ChatWindow.Messages[Index].TextBox.unbind ("<FocusIn>")
			self.ChatWindow.Messages[Index].TextBox.unbind ("<FocusOut>")
			self.ChatWindow.Messages[Index].TextBox.configure (height = 35)
			self.ChatWindow.Messages[Index].IncludeButton.config (state = tk.DISABLED)
			self.ChatWindow.Messages[Index].ExcludeButton.config (state = tk.DISABLED)
		else:
			self.ChatWindow.Messages[Index].ReadButton = None
			self.ChatWindow.Messages[Index].ReadButton = Window.ImageButton (self.ChatWindow.Messages[Index].ButtonFrame, 0, 4, "NS", self.SVGFile_SpeakerIcon, lambda: TTS.Read (self.ChatWindow.Messages[Index].TextBox.get ("1.0", "end").strip (), self.S.TTSVoiceMale, Title = "Message", ID = Index, Key = self.K.Key_Lookup.get ("OpenAI")), Width = 30, PadX = 0, PadY = 0, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Reads the message aloud using AI text to speech function.")
			if Communicate.Disabled_OpenAI == True: # Key rejected or no key so not available...
				self.ChatWindow.Messages[Index].ReadButton.configure (state = tk.DISABLED)
		self.ChatWindow.Messages[Index].TextBox.focus ()
		
		# Refresh canvas scroll region
		if len (self.ChatWindow.Messages) > 5: # That many will most likely fit on the screen, so no need to scroll. (Otherwise the first prompt goes off screen before the screen is full.)
			self.ChatAutoScroll ()
		self.Window.update ()
	
	
	
	def ChatSendAction (self):
		self.ChatWindow.SendButton.configure (state = tk.DISABLED)
		
		# Update ratings for all previous messages. (The user may have changed it...)
		if len (self.ChatWindow.Messages) > 1:
			for Index in range (0, len (self.ChatWindow.Messages)):
				if self.ChatWindow.Messages[Index].Exclude.get () == True:
					self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = -1
				elif self.ChatWindow.Messages[Index].Include.get () == True:
					self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = 1
				else:
					self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = 0
		
		### Display Prompt
		Text = self.ChatWindow.UserInputTextBox.get ("1.0", "end").strip ()
		self.ChatWindow.UserInputTextBox.delete ('1.0', "end") # For some odd reason if this is after the DisplayMessage call, the User input may not get immediately cleared...
		self.DisplayMessage (self.S.UserName, Text)
		PromptIndex = len (self.ChatWindow.Messages) - 1 # Last displayed message...
		
		### Construct Rules for sending... (Required by the API)
		if self.Conversation.LatestRules != None:
			Rules = {"role": "system", "content": self.Conversation.Rules.Rules}
			self.ChatWindow.Messages[PromptIndex].MessageData.Rules = self.Conversation.LatestRules
		else:
			Rules = {"role": "system", "content": ""}
		
		### Construct Prompt for sending... (Required by the API)
		if self.Conversation.LatestRules != None:
			Prompt = {"role": "user", "content": self.Conversation.Rules.Message + "\n" + self.ChatWindow.Messages[PromptIndex].MessageData.Message}
		else:
			Prompt = {"role": "user", "content": self.ChatWindow.Messages[PromptIndex].MessageData.Message}
		
		### Generate context... (Optional for the API, but AI doesn't "remember" previous prompt/answer without it...)
		Context = None
		ContextIDs = None
		Messages = []
		Messages.append (Rules)
		Messages.append (Prompt)
		
		# Calculate remaining tokens for context
		if self.S.API == "OpenAI": # Only available with Open AI at this time...
			T = Tokenizer (self.S.API, self.S.AIModel, Messages)
			MaxContextTokens = 128000 # Since gpt-4-turbo, gpt-4o, gpt-4o-mini all have the same large context window. (Earlier models had far less, and different sizes...)
			if self.S.MaxTokens == 0:
				MaxContextTokens = MaxContextTokens - self.S.MaxOTokens - T.TokenCount_Rules - T.TokenCount_Prompt
			else:
				MaxContextTokens = self.S.MaxTokens - T.TokenCount_Rules - T.TokenCount_Prompt
			
			HL.Log ("GUI.py: MaxTokens allowed: " + str (self.S.MaxTokens) + ", Estimated rules tokens: " + str (T.TokenCount_Rules) + ", Estimated prompt tokens: " + str (T.TokenCount_Prompt) + ", MaxOTokens allowed: " + str (self.S.MaxOTokens) +  " --> MaxContextTokens " + str (MaxContextTokens) + ", MaxContextMessages: " + str (self.S.MaxContextMsg), 'D', LogT.GUI)
		
		elif self.S.API == "DeepSeek":
			MaxContextTokens = 64000
		
		# Generate Context
		ContextIDs, Context = Commands.GenerateContext (self.K.UserKey, self.S, self.Conversation.Blocks, MaxContextTokens)
		
		if ContextIDs != None:
			self.ChatWindow.Messages[PromptIndex].MessageData.Context = ContextIDs
		
		# Context token estimation
		Messages = []
		Messages.append (Rules)
		if Context != None:
			Messages.extend (Context)
		Messages.append (Prompt)
		if self.S.API == "OpenAI": # Only available with Open AI at this time...
			T = Tokenizer (self.S.API, self.S.AIModel, Messages)
			self.ChatWindow.StatsLabel.config (text = "Token estimations:   Total to send: " + str (T.TokenCount_Total) + "\nRules: " + str (T.TokenCount_Rules) + "   Context: " + str (T.TokenCount_Context) + "   Prompt: " + str (T.TokenCount_Prompt))
		self.Window.update ()

		# This is for testing only... ForceLargeContext should be False for release!
		if self.S.API == "DeepSeek":
			ForceLargeContext = True # There's no token estimation yet...
		else:
			ForceLargeContext = False
		
		if ForceLargeContext == True:
			EstimatedTokens = MaxContextTokens
		else:
			EstimatedTokens = T.TokenCount_Total
		
		# Debug
#		if Context != None and Args.debug:
#			for Item in Context:
#				print (Item)
#		HL.Log ("GUI.py: Estimated context tokens: " + str (T.TokenCount_Context) + " --> Estimated total tokens: " + str (T.TokenCount_Total), 'D', LogT.GUI)
		
		### Record promt into a new block.
		self.Conversation.NewBlock (self.ChatWindow.Messages[PromptIndex].MessageData.Dump (self.K.UserKey))
		self.ChatWindow.Messages[PromptIndex].MessageData.BlockID = self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID
		
		Key = self.K.Key_Lookup.get (self.S.API)
		HL.Log ("GUI.py: Communicating with API: " + self.S.API + "   Model: " + self.S.AIModel + "   Key: " + Key, 'D', LogT.GUI)
		
		### Send message then display and recod response to new block
		Response = Communicate.AskTheAI (self.S.API, self.S.AIModel, Key, Rules, Context, Prompt, self.S.MaxOTokens, self.S.Temperature, self.S.TopP, self.S.PresencePenalty, self.S.FrequencyPenalty, EstimatedTokens) # Arguments: API, AIModel, Rules, Context, Prompt, MaxTokens = 128, Temperature = 0.2, TopP = 0.95, PresencePenalty = 0.0, FrequencyPenalty = 0.0, ContextTokens = 4096
		ErrorText = None
		if (Response.object != "chat.completion"):
			ErrorText = Response.ErrorMessage
			self.DisplayMessage ("HexaPA", ErrorText)
			self.ChatWindow.StatsLabel.config (text = "An error occurred! The propmpt reloaded and first try excluded, you may try re-sending.")
		else:
			self.DisplayMessage ("HexaPA", Response.choices[0].message.content)
			self.ChatWindow.StatsLabel.config (text = "Actual token usage:   Total: " + str (Response.usage.total_tokens) + "\nRules + Context + Prompt: " + str (Response.usage.prompt_tokens) + "   Response: " + str (Response.usage.completion_tokens))
		Index = len (self.ChatWindow.Messages) - 1
		self.Conversation.NewBlock (self.ChatWindow.Messages[Index].MessageData.Dump (self.K.UserKey))
		if ErrorText != None:
			self.ChatWindow.Messages[Index].MessageData.Rating = -1
			self.ChatWindow.Messages[Index].Exclude.set (True)
			self.ChatWindow.Messages[Index - 1].MessageData.Rating = -1
			self.ChatWindow.Messages[Index - 1].Exclude.set (True)
			self.ChatWindow.UserInputTextBox.insert ('end', self.ChatWindow.Messages[Index - 1].MessageData.Message) # Allow the user to try again by simply clicking send again.
		self.ChatWindow.Messages[Index].MessageData.BlockID = self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID
		self.ChatWindow.SendButton.configure (state = tk.NORMAL)
		
		# Update ratings again... (If the gui is closed by the user anything in self.ChatWindow will be lost, self.Conversation survives and gets saved before exit unless the SIGKILL is given.)
		for Index in range (0, len (self.ChatWindow.Messages)):
			if self.ChatWindow.Messages[Index].Exclude.get () == True:
				self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = -1
			elif self.ChatWindow.Messages[Index].Include.get () == True:
				self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = 1
			else:
				self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = 0
		
		### Generate subject if not set by the user.
		BlockID = 0
		FirstMsg = self.ChatWindow.Messages[PromptIndex].MessageData
		for ID in range (0, len (self.Conversation.Blocks)): # This should not be a long loop unless you've edited the rules 100s of thousands of times before even starting the conversation.
			FirstMsg = Data ()
			FirstMsg.Parse (self.K.UserKey, self.Conversation.Blocks[ID].Data, ID)
			if FirstMsg.DataType == "Message":
				BlockID = ID
				break
		self.Conversation.CreationTime = self.Conversation.Blocks[BlockID].TimeStamp
		if self.Conversation.Subject == "Enter the subject here... (optional)" or self.Conversation.Subject == "":
			SubjectDetectionRules = {"role": "system", "content": "Your task is to determine what is the subject of messages in a very short sentences. Never return more then one sentence."}
			Context = [{"role": "user", "content": "What is the subject of the following message?\n\nMessage:\nGive me a sentence for testing my application."}, {"role": "assistant", "content": "Sentence request for testing."}] # This works with Content = None, but more reliable with an example. Otherwise it may start with "Subject: ", or "The subject of this..." which is not desirable.
			Prompt = {"role": "user", "content": "What is the subject of the following message?\n\nMessage:\n" + FirstMsg.Message}
			HL.Log ("GUI.py: Unspecified Subject! --> Asking the AI to summarize it in a sentence.", 'I', LogT.GUI)
			Response = Communicate.AskTheAI (self.S.API, self.S.AIModel, Key, SubjectDetectionRules, Context, Prompt) # Arguments: API, AIModel, Rules, Context, Prompt, MaxTokens = 2048
			if (Response.object == "chat.completion"): # AI Respose
				self.Conversation.Subject = Response.choices[0].message.content
				HL.Log ("GUI.py: AI said the subject is: " + self.Conversation.Subject, "I", LogT.GUI)
				self.ChatWindow.SubjectLabel.config (text = self.Conversation.Subject + " (Created at " + self.Conversation.CreationTime + ")")
		elif PromptIndex == BlockID:
			self.ChatWindow.SubjectLabel.config (text = self.Conversation.Subject + " (Created at " + self.Conversation.CreationTime + ")")
		
		### Generate filename if does not exist...
		if self.Conversation.File == None:
			self.Conversation.File = "Conversations/" + re.sub ('[\W_]+', '_', self.Conversation.CreationTime) + ".bin"
			HL.Log ("GUI.py: Chat will be saved to: " + self.Conversation.File, 'D', LogT.GUI)
	
	
	
	def UnincludeAction (self):
		for Index in range (0, len (self.ChatWindow.Messages)):
			if self.ChatWindow.Messages[Index].Include.get () == True:
				self.ChatWindow.Messages[Index].Include.set (False)
	
	
	
	def ExportAction (self):
		Commands.ExportChatJSON (self.K.UserKey, self.Conversation)
	
	
	
	def Chat (self, Stats = None):
		self.ChatWindow = Window (self.Window)
		self.ChatWindow.Base.columnconfigure (0, weight = 1)
		self.ChatWindow.Base.rowconfigure (1, weight = 1) # Set row 1 to expand not 0 here...
		
		### Tooltip label
		self.ChatWindow.TooltipFrame = None
		self.ChatWindow.TooltipFrame = Window.Frame (self.ChatWindow.Base, Row = 3, Column = 0, Sticky = "EW", PadX = 0, PadY = 0)
		self.ChatWindow.TooltipFrame.columnconfigure (0, weight = 1)
		self.ChatWindow.TooltipLabel = None
		self.ChatWindow.TooltipLabel = Window.Label (self.ChatWindow.TooltipFrame, 0, 0, "NSEW", "", Theme.BGColor, Theme.SmallText, Theme.SmallTextSize, Anchor = "w", PadX = 0, PadY = 0, Height = 2) # Hight must be limited otherwise the label may push other widgets out from beneath the mouse, and it oscillates between Tooltip and no Tooltip...
		
		### Subject label and Back to Main / Edit Rules buttons
		self.ChatWindow.SubjectFrame = None
		self.ChatWindow.SubjectFrame = Window.Frame (self.ChatWindow.Base, Row = 0, Column = 0, PadX = 0, PadY = 0, Sticky = "NEW")
		self.ChatWindow.SubjectFrame.columnconfigure (1, weight = 1)
		self.ChatWindow.BackButton = None
		self.ChatWindow.BackButton = Window.Button (self.ChatWindow.SubjectFrame, 0, 0, "W", "Back", self.ChatBackAction, Height = 1, PadX = 0, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Save and exit to main.\nHotkey/combination: [Esc]")
		self.ChatWindow.BackButton.configure (state = tk.DISABLED) # Every button should be disabled until the conversation is loaded...
		if self.Conversation.Subject != "Enter the subject here... (optional)" and self.Conversation.Subject != "":
			if self.Conversation.CreationTime != None:
				Text = self.Conversation.Subject + " (Created at " + self.Conversation.CreationTime + ")"
			else:
				Text = self.Conversation.Subject
		else:
			Text = "(Subject will be generated from prompt.)"
		self.ChatWindow.SubjectLabel = None
		self.ChatWindow.SubjectLabel = Window.Label (self.ChatWindow.SubjectFrame, 0, 1, "EW", Text, Theme.BGColor, Anchor = "w", Width = None)
		self.ChatWindow.ExportButton = None
		self.ChatWindow.ExportButton = Window.Button (self.ChatWindow.SubjectFrame, 0, 2, "E", "Export", self.ExportAction, Width = 5, Height = 1, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Export conversation data. (Unlike in ChatGPT you can see which rule block and which context blocks ware sent with any given prompt when you export the conversation, just in case you want to analyze it.)\n(JSON only! ...for now. Recommended to export important data before upgrading HexaPA to new version for now... It's in early alpha, it may not be stable.)")
		self.ChatWindow.ExportButton.configure (state = tk.DISABLED) # Every button should be disabled until the conversation is loaded...
		self.ChatWindow.RulesButton = None
		self.ChatWindow.RulesButton = Window.Button (self.ChatWindow.SubjectFrame, 0, 3, "E", "Rules", self.ChatRulesAction, Width = 5, Height = 1, PadX = 0, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Edit rules... (Experimental... The AI will use this as context but treats it more as recommendations. Examples help, old context may contain bad example to a radical change in rules, so use the exclude checkboxes or disable auto context for a while...)\nHotkey/combination: [Ctrl] + [Shift] + [R]")
		self.ChatWindow.RulesButton.configure (state = tk.DISABLED) # Every button should be disabled until the conversation is loaded...
		
		### Conversation canvas (This should be populated after the UI is fully constructed, otherwise autoscroll does not seem to scroll all the way to the bottom when continuig conversation...)
		self.ChatWindow.Canvas = None
		self.ChatWindow.CanvasInnerFrame = None
		self.ChatWindow.Canvas, self.ChatWindow.CanvasInnerFrame = Window.ScrollCanvas (self.ChatWindow.Base, 1, 0, "NSEW")
		self.ChatWindow.Messages = []
		
		### UserInput
		self.ChatWindow.UserInputFrame = None
		self.ChatWindow.UserInputFrame = Window.Frame (self.ChatWindow.Base, Row = 2, Column = 0, PadX = 0, PadY = 0, Sticky = "EW")
		self.ChatWindow.UserInputFrame.columnconfigure (0, weight = 1)
		self.ChatWindow.UserInputTextBoxFrame = None
		self.ChatWindow.UserInputScrollX = None
		self.ChatWindow.UserInputScrollY = None
		self.ChatWindow.UserInputTextBox = None
		self.ChatWindow.UserInputTextBoxFrame, self.ChatWindow.UserInputScrollX, self.ChatWindow.UserInputScrollY, self.ChatWindow.UserInputTextBox = Window.TextBox (self.ChatWindow.UserInputFrame, 0, 0, PadX = 0, Sticky = "EW", TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Enter text...\nHotkey/combination: [Space]")
		self.ChatWindow.UserInputTextBox.bind ("<FocusIn>", lambda event: self.ChatWindow.UserInputTextBox.config (height = 12)) # click event that enlarges the field.
		self.ChatWindow.UserInputTextBox.bind ("<FocusOut>", lambda event: self.ChatWindow.UserInputTextBox.config (height = 3)) # click away event that shriks the field.
		self.ChatWindow.UserInputButtons = None
		self.ChatWindow.UserInputButtons = Window.Frame (self.ChatWindow.UserInputFrame, Row = 1, Column = 0, PadX = 0, PadY = 0, Sticky = "EW")
		self.ChatWindow.UserInputButtons.columnconfigure (2, weight = 1)
		self.ChatWindow.AutoContext = tk.BooleanVar (value = 1)
		self.S.AutoContext = True # Auto context should be on by default, it's only for special cases like asking the AI something totally unrelated, or if you want it to work with specific context within the conversation...
		self.ChatWindow.AutoContextButton = None
		self.ChatWindow.AutoContextButton = Window.CheckButton (self.ChatWindow.UserInputButtons, 0, 0, "NSW", "Auto Context", self.ChatWindow.AutoContext, lambda: setattr (self.S, 'AutoContext', bool (self.ChatWindow.AutoContext.get ())), Width = 11, Height = 1, PadX = 0, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "When enabled all but explicitly excluded messages, when disabled only explicitly included messages will be sent as context.\n(Enabled by default. Limits apply! You can see what's getting sent in the terminal by running HexaPA with --verbose option.)")
		self.ChatWindow.AutoContextButton.configure (state = tk.DISABLED) # Every button should be disabled until the conversation is loaded...
		self.ChatWindow.UnincludeButton = None
		self.ChatWindow.UnincludeButton = Window.Button (self.ChatWindow.UserInputButtons, 0, 1, "NSW", "Uninclude All", self.UnincludeAction, Width = 10, Height = 1, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Shortcut for scrolling back an unchecking every \"Include\" checkmark for a new selection...")
		self.ChatWindow.UnincludeButton.configure (state = tk.DISABLED) # Every button should be disabled until the conversation is loaded...
		self.ChatWindow.UserInputWrap = tk.BooleanVar (value = 1)
		self.ChatWindow.SpacerFrame = None
		self.ChatWindow.SpacerFrame = Window.Frame (self.ChatWindow.UserInputButtons, Row = 0, Column = 2, PadX = 0, PadY = 0, Sticky = "NSEW")
#		self.ChatWindow.VoiceInputButton = None
#		self.ChatWindow.VoiceInputButton = Window.ImageButton (self.ChatWindow.UserInputButtons, 0, 3, "NSE", self.SVGFile_MicIcon, lambda: self.ChatWindow.UserInputTextBox.insert ('end', STT.Transcribe ("Audio/TTS/TestTTS.mp3"), self.K.Key_Lookup.get ("OpenAI")), PadX = 0, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Voice recording and transcription to text input.")
#		self.ChatWindow.VoiceInputButton.configure (state = tk.DISABLED)
		self.ChatWindow.InputReadButton = None
		self.ChatWindow.InputReadButton = Window.ImageButton (self.ChatWindow.UserInputButtons, 0, 4, "NSE", self.SVGFile_SpeakerIcon, lambda: TTS.Read (self.ChatWindow.UserInputTextBox.get ("1.0", "end").strip (), self.S.TTSVoiceMale, "UserInput", ID = 0, Key = self.K.Key_Lookup.get ("OpenAI")), TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Reads text from input using AI text to speech function.")
		self.ChatWindow.InputReadButton.configure (state = tk.DISABLED)
		self.ChatWindow.WrapButton = None
		self.ChatWindow.WrapButton = Window.CheckButton (self.ChatWindow.UserInputButtons, 0, 5, "NSE", "Wrap", self.ChatWindow.UserInputWrap, lambda: self.ChatWindow.UserInputTextBox.configure (wrap = ("word" if self.ChatWindow.UserInputWrap.get () else "none")), Height = 1, PadX = 0, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Wrap/not wrap text in the prompt textbox.\n(Text is readable wrapped, however this may not be desirable for code.)")
		self.ChatWindow.WrapButton.configure (state = tk.DISABLED) # Every button should be disabled until the conversation is loaded...
		self.ChatWindow.TokenButton = None
		self.ChatWindow.TokenButton = Window.Button (self.ChatWindow.UserInputButtons, 0, 6, "NSE", "Count Tokens", self.ChatCountTokensAction, Width = 11, Height = 1, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Estimate input tokens for rules, context, and prompt.\n(May not be entirely accurate...)")
		self.ChatWindow.TokenButton.configure (state = tk.DISABLED) # Every button should be disabled until the conversation is loaded...
		self.ChatWindow.SendButton = None
		self.ChatWindow.SendButton = Window.Button (self.ChatWindow.UserInputButtons, 0, 7, "NSE", "Send", lambda: self.ChatSendAction () if self.ChatWindow.UserInputTextBox.get ("1.0", "end-1c") else None, Height = 1, PadX = 0, TooltipLabel = self.ChatWindow.TooltipLabel, TooltipText = "Send text to the AI, and wait for response.\nHotkey/combination: [Ctrl] + [Enter]")
		self.ChatWindow.SendButton.configure (state = tk.DISABLED) # Every button should be disabled until the conversation is loaded...
		if Stats == None:
			Stats = ""
		self.ChatWindow.StatsLabel = None
		self.ChatWindow.StatsLabel = Window.Label (self.ChatWindow.TooltipFrame, 0, 0, "NSEW", Stats, Theme.BGColor, Theme.Text, Theme.TextSize, "w", None, 0, 0, Height = 2)
		
		### Load conversation
		try:
			if len (self.Conversation.Blocks) == 0: # Reminder, in case there is no content yet...
				Text = "Remember:\n- Clicking on a message enlarges it for easier reading.\n- It does not have the ability to remember! The rules and context you send, is all it has to work with!\n- It does not think! It simply reacts to the given text, generating a response.\n- Do not ask for a numerical answer, the AI is simply terrible at math! It guesses the answer based on it's probablility, rather then calculating it. (The current model at least...)\n- The model is somewhat biased towards leftist ideologies... Do not rely on it's answer in moral, religious, legal or financial questions!\n- Be concise, don't argue with the AI if it doesn't give you the answer you want, because you pay for your argument as well as the AI's apology, and it may still not give you an acceptable answer! Instead tweak what rules, context, and prompt you send next and perhaps other settings!\n- It does not feel, so praising or cursing it only cost you money! (Still it's a good idea to be polite, just to avoid developing bad habits...)\n\n- OpenAI's current policy (as of 5th of May 2023) says that they don't use data form API calls for training. (...but off course every company leaves a clause in it's ToS to change anything anytime, so I advise against feeding it any sensitive information or code! Treat it with an \"Anything you say can be used against you!\" attitude!)\n\nRecent changes:\n- [Ctrl/Cmd] + [A] selects text in the focused text/enry box.\n- [Ctrl/Cmd] + [R] now set to rephrase last prompt, and instead [Ctrl/Cmd] + [Shift] + [R] to enter the rules section.\n- [Ctrl/Cmd] + [Shift] + [H] can now be used to show/hide password.\n\n- HexaPA is free and open source software, if you find it helpful please donate at: www.osrc.rip/Support.html"
				self.DisplayMessage ("Developer", Text)
			else: # Conversation
				if Args.renew_data: # Renew data...
					TempConversation = BlockChain (LogT.BlockChain)
					TempConversation.Subject = self.Conversation.Subject
					TempConversation.File = self.Conversation.File
				
				if self.Conversation.Validate () == True:
					HL.Log ("GUI.py: Chain validation complete!", 'D', LogT.GUI)
				else:
					HL.Log ("GUI.py: Chain validation failed! >> Attempting to display read-only data! (This may fail...)", 'E', LogT.GUI)
					HL.Log ("", 'E', LogT.GUI)
				for Block in self.Conversation.Blocks:
					MessageData = Data ()
					MessageData.Parse (self.K.UserKey, Block.Data, Block.BlockID, Block.Rating)
					if not Args.renew_data and MessageData.DataVersion < Settings.DataVersion: # Warn... This should not change saved data, even if it's no longer supported...
						HL.Log ("GUI.py: Block contains old data. Some functionality may be unavailable during this conversation. (You can specify --renew-data option to renew the chain when continuing conversation.)", 'W', LogT.GUI)
					elif Args.renew_data: # Renew data... (Don't check for old data, if this option is specified, the data must be added whether it's new or old, as the chain may contain different version data in each block...)
						HL.Log ("GUI.py: Saving block with new version data. (--renew-data specified)", 'I', LogT.GUI)
						MessageData.DataVersion = Settings.DataVersion
						TempConversation.NewBlock (MessageData.Dump (self.K.UserKey))
					if MessageData.DataType == "Message":
						#MessageData.BlockID = Block.BlockID
						self.DisplayMessage (MsgData = MessageData)
					elif MessageData.DataType == "Rules":
						self.Conversation.LatestRules = Block.BlockID
						HL.Log ("GUI.py: Latest rule: " + str (Block.BlockID), 'D', LogT.GUI)
				if Args.renew_data: # Renew data...
					TempConversation.Save ()
					self.Conversation.Clear ()
					self.Conversation.Load (TempConversation.File) # Reload with new data...
					TempConversation.Clear ()
			
			### Load Rules
			if self.Conversation.LatestRules != None:
				self.Conversation.Rules = Data ()
				self.Conversation.Rules.Parse (self.K.UserKey, self.Conversation.Blocks[self.Conversation.LatestRules].Data, self.Conversation.LatestRules)
			
			# Enable buttons
			self.ChatWindow.BackButton.configure (state = tk.NORMAL)
			self.ChatWindow.ExportButton.configure (state = tk.NORMAL)
			self.ChatWindow.RulesButton.configure (state = tk.NORMAL)
			self.ChatWindow.AutoContextButton.configure (state = tk.NORMAL)
			self.ChatWindow.WrapButton.configure (state = tk.NORMAL)
			self.ChatWindow.UnincludeButton.configure (state = tk.NORMAL)
			if Communicate.Disabled_OpenAI == False or Communicate.Disabled_DeepSeek == False: # Key rejected or no key
				self.ChatWindow.SendButton.configure (state = tk.NORMAL)
				#self.ChatWindow.VoiceInputButton.configure (state = tk.NORMAL)
				self.ChatWindow.InputReadButton.configure (state = tk.NORMAL)
			if Communicate.Disabled_OpenAI == False and self.S.API == "OpenAI": # Only available with Open AI at this time...
				self.ChatWindow.TokenButton.configure (state = tk.NORMAL)
				
		
		except Exception:
			HL.Log ("GUI.py: Could not parse block content! It can be corrupted or encrypted with other username and password combination... (This can happen when .Keys.bin and .Settings.bin has been deleted, and new credentials entered. If that's the case and block validation was successful, the conversation can still be decrypted with the initial username and password combination.)", 'E', LogT.GUI)
		
		# Key binding...
		self.SpaceBinding = self.Window.bind ('<space>', lambda event: self.ChatWindow.UserInputTextBox.focus ())
		self.EscBinding = self.Window.bind ('<Escape>', lambda event: self.ChatWindow.BackButton.invoke ())
		if platform.system () != 'Darwin':
			self.CtrlEnterBinding = self.Window.bind ('<Control-Return>', lambda event: self.ChatWindow.SendButton.invoke ()) # [Ctrl / Cmd] + [Enter]
			self.CtrlRBinding = self.Window.bind ('<Control-r>', lambda event: self.ChatWindow.Messages[len (self.ChatWindow.Messages) - 2].RephraseButton.invoke ()) # [Ctrl / Cmd] + [R]
			self.CtrlShiftRBinding = self.Window.bind ('<Control-R>', lambda event: self.ChatWindow.RulesButton.invoke ()) # [Ctrl / Cmd] + [Shift] + [R]
			self.CtrlABinding = self.Window.bind ('<Control-a>', lambda event: event.widget.tag_add ('sel', '1.0', 'end')) # [Ctrl / Cmd] + [A]
		else:
			self.CtrlEnterBinding = self.Window.bind ('<Command-Return>', lambda event: self.ChatWindow.SendButton.invoke ()) # [Ctrl / Cmd] + [Enter]
			self.CtrlRBinding = self.Window.bind ('<Command-r>', lambda event: self.ChatWindow.Messages[len (self.ChatWindow.Messages) - 2].RephraseButton.invoke ()) # [Ctrl / Cmd] + [R]
			self.CtrlShiftRBinding = self.Window.bind ('<Command-R>', lambda event: self.ChatWindow.RulesButton.invoke ()) # [Ctrl / Cmd] + [Shift] + [R]
			self.CtrlABinding = self.Window.bind ('<Command-a>', lambda event: event.widget.tag_add ('sel', '1.0', 'end')) # [Ctrl / Cmd] + [A]
	
	
	
	
	
	
	
	def SaveRules (self): # used by RulesBackAction, and RulesExportPresetAction...
		NewRules = Data (self.RulesWindow.RulesInputTextBox.get ("1.0", "end").strip (), Message = self.RulesWindow.RulesMessageInjectionTextBox.get ("1.0", "end").strip (), DataType = "Rules")
		if self.Conversation.LatestRules == None and NewRules.Rules != "" and NewRules.Rules != self.RulesWindow.Reminder: # New conversation with no rules defined yet. (exclude reminder text)
			self.Conversation.NewBlock (NewRules.Dump (self.K.UserKey))
			self.Conversation.LatestRules = self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID # Last block's ID where the rules have just been saved.
			HL.Log ("GUI.py: First rules saved to block: " + str (self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID), 'D', LogT.GUI)
			self.Conversation.Rules = Data () # If there ware no rules defined yet this shoud still be None
			self.Conversation.Rules.Parse (self.K.UserKey, self.Conversation.Blocks[self.Conversation.LatestRules].Data, self.Conversation.LatestRules)
		elif self.Conversation.LatestRules != None:
			if NewRules.Rules != self.Conversation.Rules.Rules and NewRules.Rules != self.RulesWindow.Reminder or NewRules.Rules != "" and NewRules.Message != self.Conversation.Rules.Message and NewRules.Message != self.RulesWindow.InjectionReminder: # If the rules have changed. (exclude reminder text)
				self.Conversation.NewBlock (NewRules.Dump (self.K.UserKey))
				self.Conversation.LatestRules = self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID # Last block's ID where the rules have just been saved.
				HL.Log ("GUI.py: New rules saved to block: " + str (self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID), 'D', LogT.GUI)
				self.Conversation.Rules.Parse (self.K.UserKey, self.Conversation.Blocks[self.Conversation.LatestRules].Data, self.Conversation.LatestRules)
	
	
	
	def RulesBackAction (self):
		self.RulesUnbindSpace ()
		self.Window.unbind ('<Escape>', self.EscBinding)
		if platform.system () != 'Darwin':
			self.Window.unbind ('<Control-a>', self.CtrlABinding)
		else:
			self.Window.unbind ('<Command-a>', self.CtrlABinding)
		self.SaveRules ()
		self.RulesWindow.Base.grid_forget ()
		self.ChatWindow.Base.grid (padx = Theme.PadX, pady = Theme.PadY, sticky = "NSEW") # No need to generate the chat content each time... it's slow, and already generated...
		self.Window.update ()
		self.SpaceBinding = self.Window.bind ('<space>', lambda event: self.ChatWindow.UserInputTextBox.focus ())
		self.EscBinding = self.Window.bind ('<Escape>', lambda event: self.ChatWindow.BackButton.invoke ())
		if platform.system () != 'Darwin':
			self.CtrlEnterBinding = self.Window.bind ('<Control-Return>', lambda event: self.ChatWindow.SendButton.invoke ()) # [Ctrl / Cmd] + [Enter]
			self.CtrlRBinding = self.Window.bind ('<Control-r>', lambda event: self.ChatWindow.Messages[len (self.ChatWindow.Messages) - 2].RephraseButton.invoke ()) # [Ctrl / Cmd] + [R]
			self.CtrlShiftRBinding = self.Window.bind ('<Control-R>', lambda event: self.ChatWindow.RulesButton.invoke ()) # [Ctrl / Cmd] + [Shift] + [R]
			self.CtrlABinding = self.Window.bind ('<Control-a>', lambda event: event.widget.tag_add ('sel', '1.0', 'end')) # [Ctrl / Cmd] + [A]
		else:
			self.CtrlEnterBinding = self.Window.bind ('<Command-Return>', lambda event: self.ChatWindow.SendButton.invoke ()) # [Ctrl / Cmd] + [Enter]
			self.CtrlRBinding = self.Window.bind ('<Command-r>', lambda event: self.ChatWindow.Messages[len (self.ChatWindow.Messages) - 2].RephraseButton.invoke ()) # [Ctrl / Cmd] + [R]
			self.CtrlShiftRBinding = self.Window.bind ('<Command-R>', lambda event: self.ChatWindow.RulesButton.invoke ()) # [Ctrl / Cmd] + [Shift] + [R]
			self.CtrlABinding = self.Window.bind ('<Command-a>', lambda event: event.widget.tag_add ('sel', '1.0', 'end')) # [Ctrl / Cmd] + [A]
		self.RulesWindow.Base.destroy ()
	
	
	
	def RulesExportPresetAction (self):
		if self.RulesWindow.PresetTitle.get ().strip () != "" and self.RulesWindow.PresetTitle.get ().strip () != self.RulesWindow.PresetTitleText:
			self.RulesWindow.ErrorLabel.config (text = "") # This should get rid of prevous error message...
			self.SaveRules ()
			Commands.ExportRulesJSON (self.K.UserKey, self.Conversation, self.Conversation.LatestRules, self.RulesWindow.PresetTitle.get ().strip ())
		else:
			self.RulesWindow.ErrorLabel.config (text = "Preset Title REQUIRED for exporting!")
			self.RulesWindow.ErrorLabel.lift ()
	
	
	
	def ClearReminder (self, event):
		self.RulesUnbindSpace ()
		self.RulesWindow.RulesInputTextBox.unbind ("<FocusIn>")
		self.RulesWindow.RulesMessageInjectionTextBox.unbind ("<FocusIn>")
		if self.RulesWindow.RulesInputTextBox.get ("1.0", "end").strip () == self.RulesWindow.Reminder or self.RulesWindow.RulesInputTextBox.get ("1.0", "end").strip () == "":
			self.RulesWindow.RulesInputTextBox.delete ('1.0', 'end')
			self.RulesWindow.RulesInputTextBox.config (fg = Theme.Text)
		if self.RulesWindow.RulesMessageInjectionTextBox.get ("1.0", "end").strip () == self.RulesWindow.InjectionReminder or self.RulesWindow.RulesMessageInjectionTextBox.get ("1.0", "end").strip () == "":
			self.RulesWindow.RulesMessageInjectionTextBox.delete ('1.0', 'end')
			self.RulesWindow.RulesMessageInjectionTextBox.config (fg = Theme.Text)
	
	
	
	def RulesUnbindSpace (self):
		if self.Window.bind ('<space>'): # When focusing from 1 textbox/input to another, space is alredy unbound, so need to check...
			self.Window.unbind ('<space>', self.SpaceBinding)
	
	
	
	def Rules (self, Stats = None):
		self.RulesWindow = Window (self.Window)
		self.RulesWindow.Base.columnconfigure (0, weight = 1)
		self.RulesWindow.Base.rowconfigure (1, weight = 1) # Set row 1 to expand not 0 here...
		
		### Tooltip label
		self.RulesWindow.TooltipFrame = None
		self.RulesWindow.TooltipFrame = Window.Frame (self.RulesWindow.Base, Row = 4, Column = 0, Sticky = "EW", PadX = 0, PadY = 0)
		self.RulesWindow.TooltipFrame.columnconfigure (0, weight = 1)
		self.RulesWindow.TooltipLabel = None
		self.RulesWindow.TooltipLabel = Window.Label (self.RulesWindow.TooltipFrame, 0, 0, "NSEW", "", Theme.BGColor, Theme.SmallText, Theme.SmallTextSize, Anchor = "w", PadX = 0, PadY = 0, Height = 2) # Hight must be limited otherwise the label may push other widgets out from beneath the mouse, and it oscillates between Tooltip and no Tooltip...
		self.RulesWindow.ErrorLabel = None
		self.RulesWindow.ErrorLabel = Window.Label (self.RulesWindow.TooltipFrame, 0, 0, "NSEW", "", Theme.BGColor, Theme.Error, Theme.TextSize, Anchor = "w", PadX = 0, PadY = 0, Height = 2) # Hight must be limited otherwise the label may push other widgets out from beneath the mouse, and it oscillates between Tooltip and no Tooltip...
		
		### Subject label and Back to Main / Edit Rules buttons
		self.RulesWindow.TitleFrame = None
		self.RulesWindow.TitleFrame = Window.Frame (self.RulesWindow.Base, Row = 0, Column = 0, PadX = 0, PadY = 0, Sticky = "NEW")
		self.RulesWindow.TitleFrame.columnconfigure (1, weight = 1)
		self.RulesWindow.BackButton = None
		self.RulesWindow.BackButton = Window.Button (self.RulesWindow.TitleFrame, 0, 0, "W", "Back", self.RulesBackAction, Height = 1, PadX = 0, TooltipLabel = self.RulesWindow.TooltipLabel, TooltipText = "Save rule block, and go back to chat screen. (If you change something and push the back button, a new rule block is created, the old one is preserved.)\nHotkey/combination: [Esc]")
		Text = "Rules for the AI"
		self.RulesWindow.SubjectLabel = None
		self.RulesWindow.SubjectLabel = Window.Label (self.RulesWindow.TitleFrame, 0, 1, "EW", Text, Theme.BGColor, Anchor = "w", Width = None)
		
		
		### UserInput
		self.RulesWindow.RulesContentFrame = None
		self.RulesWindow.RulesContentFrame = Window.Frame (self.RulesWindow.Base, Row = 1, Column = 0, PadX = 0, PadY = 0, Sticky = "NSEW")
		self.RulesWindow.RulesContentFrame.columnconfigure (0, weight = 1)
		self.RulesWindow.RulesContentFrame.rowconfigure (0, weight = 4)
		self.RulesWindow.RulesContentFrame.rowconfigure (1, weight = 1)
		
		# Rules
		self.RulesWindow.RulesInputFrame = None
		self.RulesWindow.RulesInputFrame = Window.Frame (self.RulesWindow.RulesContentFrame, Theme.PromptBG, 0, 0, PadX = 0, PadY = 0, Sticky = "NSEW")
		self.RulesWindow.RulesInputFrame.columnconfigure (0, weight = 1)
		self.RulesWindow.RulesInputFrame.rowconfigure (1, weight = 1)
		self.RulesWindow.RulesLabel = None
		self.RulesWindow.RulesLabel = Window.Label (self.RulesWindow.RulesInputFrame, 0, 0, "EW", "Rules:", Theme.PromptBG, Anchor = "w", Width = None, PadX = 0)
		self.RulesWindow.RulesInputTextBoxFrame = None
		self.RulesWindow.RulesInputScrollX = None
		self.RulesWindow.RulesInputScrollY = None
		self.RulesWindow.RulesInputTextBox = None
		self.RulesWindow.Reminder = "This text is just a reminder to you, it is not sent to the AI! (Don't worry you don't pay for it! This text will disappear as soon as you click here to input your rules.)\n\nRemember:\n- Apparently you pay for the tags every time for every message sent, whether it's rules, context or prompt since the token counter(tiktoken) gives the most accurate result with those tags included. It means that even if this section is left empty, and you do not include any context, the token counter will estimate a few tokens for the rules, since the API requires this line(which takes a few tokenst) to be sent: \"role\": \"system\", \"content\": \"\"\n- Try to be as short as possible with the rules, since you will pay for anything you put here every time you press the \"Send\" button in the chat. That being said this section is important to tweak the AI response for your productivity.\n- The rules (if changed) will be saved for the conversation when you go back to the chat screen, but you must export it as preset to become availabe in other conversations, however presets are stored separately and any changes to the rule will only be local unless you export the changed verstion again to a preset."
		self.RulesWindow.RulesTooltipText = "Enter the rules here.\nHotkey/combination: [Space]"
		
		# Reference:
		self.RulesWindow.InjectionInputFrame = None
		self.RulesWindow.InjectionInputFrame = Window.Frame (self.RulesWindow.RulesContentFrame, Theme.ResponseBG, 1, 0, PadX = 0, PadY = 0, Sticky = "NSEW")
		self.RulesWindow.InjectionInputFrame.columnconfigure (0, weight = 1)
		self.RulesWindow.InjectionInputFrame.rowconfigure (1, weight = 1)
		self.RulesWindow.PromptInjectionLabel = None
		self.RulesWindow.PromptInjectionLabel = Window.Label (self.RulesWindow.InjectionInputFrame, 0, 0, "EW", "Prompt Injection:", Theme.ResponseBG, Anchor = "w", Width = None, PadX = 0)
		self.RulesWindow.RulesMessageInjectionTextBoxFrame = None
		self.RulesWindow.RulesMessageInjectionScrollX = None
		self.RulesWindow.RulesMessageInjectionScrollY = None
		self.RulesWindow.RulesMessageInjectionTextBox = None
		self.RulesWindow.InjectionReminder = "From my intaractions with the AI, I have the impression that the AI is likely to ignore previous messages unless you refer to them, thus it is likely to ignore the rules. I added this field to sort of auto reference the rules, by injecting a reference into the prompt every time...\n\nAnything you specify here will be injected into the prompt. It is intended to remind the AI to follow the rules. Recommended use:\n\nIn the above textbox put something like:\nRules for you (the AI language model):\n- Text in [] are direct instructions, that you strictly follow!\n- Some other rule(s) the AI should follow...\n\nIn this textbox:\n[Act according to the rules set at the beginning!]"
		self.RulesWindow.MessageInjectionTooltipText = "Refer to the rules here.\n(Optional. Increases the likelyhood of the AI following the rules.)"
		self.RulesWindow.RuleData = Data (DataType = "Rules")
		if self.Conversation.LatestRules == None: # If no rules have been defined yet.
			# Rules
			HL.Log ("GUI.py: No Latest Rules ID: ", 'D', LogT.GUI)
			self.RulesWindow.RulesInputTextBoxFrame, self.RulesWindow.RulesInputScrollX, self.RulesWindow.RulesInputScrollY, self.RulesWindow.RulesInputTextBox = Window.TextBox (self.RulesWindow.RulesInputFrame, 1, 0, PadY = 0, Sticky = "NSEW", Text = self.RulesWindow.Reminder, TooltipLabel = self.RulesWindow.TooltipLabel, TooltipText = self.RulesWindow.RulesTooltipText)
			self.RulesWindow.RulesInputTextBox.config (fg = Theme.SmallText)
			self.RulesWindow.RulesInputTextBox.bind ("<FocusIn>", self.ClearReminder) # click event that clears the field.
			
			# Prompt injection
			self.RulesWindow.RulesMessageInjectionTextBoxFrame, self.RulesWindow.RulesMessageInjectionScrollX, self.RulesWindow.RulesMessageInjectionScrollY, self.RulesWindow.RulesMessageInjectionTextBox = Window.TextBox (self.RulesWindow.InjectionInputFrame, 1, 0, PadY = 0, Sticky = "NSEW", Text = self.RulesWindow.InjectionReminder, TooltipLabel = self.RulesWindow.TooltipLabel, TooltipText = self.RulesWindow.MessageInjectionTooltipText)
			self.RulesWindow.RulesMessageInjectionTextBox.config (fg = Theme.SmallText)
			self.RulesWindow.RulesMessageInjectionTextBox.bind ("<FocusIn>", self.ClearReminder) # click event that clears the field.
		else:
			self.RulesWindow.RuleData.Parse (self.K.UserKey, self.Conversation.Blocks[self.Conversation.LatestRules].Data, self.Conversation.LatestRules)
			HL.Log ("GUI.py: Latest Rules ID: " + str (self.Conversation.LatestRules), 'D', LogT.GUI)
			# Rules
			if self.RulesWindow.RuleData.DataType == "Rules" and self.RulesWindow.RuleData.Rules == "": # If the rules have been deleted.
				self.RulesWindow.RulesInputTextBoxFrame, self.RulesWindow.RulesInputScrollX, self.RulesWindow.RulesInputScrollY, self.RulesWindow.RulesInputTextBox = Window.TextBox (self.RulesWindow.RulesInputFrame, 1, 0, PadY = 0, Sticky = "NSEW", Text = self.RulesWindow.Reminder, TooltipLabel = self.RulesWindow.TooltipLabel, TooltipText = self.RulesWindow.RulesTooltipText)
				self.RulesWindow.RulesInputTextBox.config (fg = Theme.SmallText)
				self.RulesWindow.RulesInputTextBox.bind ("<FocusIn>", self.ClearReminder) # click event that clears the field.
			else:
				self.RulesWindow.RulesInputTextBoxFrame, self.RulesWindow.RulesInputScrollX, self.RulesWindow.RulesInputScrollY, self.RulesWindow.RulesInputTextBox = Window.TextBox (self.RulesWindow.RulesInputFrame, 1, 0, PadY = 0, Sticky = "NSEW", Text = self.RulesWindow.RuleData.Rules, TooltipLabel = self.RulesWindow.TooltipLabel, TooltipText = self.RulesWindow.RulesTooltipText)
			
			# Prompt injection
			if self.RulesWindow.RuleData.DataType == "Rules" and self.RulesWindow.RuleData.Message == "": # If the rules have been deleted.
				self.RulesWindow.RulesMessageInjectionTextBoxFrame, self.RulesWindow.RulesMessageInjectionScrollX, self.RulesWindow.RulesMessageInjectionScrollY, self.RulesWindow.RulesMessageInjectionTextBox = Window.TextBox (self.RulesWindow.InjectionInputFrame, 1, 0, PadY = 0, Sticky = "NSEW", Text = self.RulesWindow.InjectionReminder, TooltipLabel = self.RulesWindow.TooltipLabel, TooltipText = self.RulesWindow.MessageInjectionTooltipText)
				self.RulesWindow.RulesMessageInjectionTextBox.config (fg = Theme.SmallText)
				self.RulesWindow.RulesMessageInjectionTextBox.bind ("<FocusIn>", self.ClearReminder) # click event that clears the field.
			else:
				self.RulesWindow.RulesMessageInjectionTextBoxFrame, self.RulesWindow.RulesMessageInjectionScrollX, self.RulesWindow.RulesMessageInjectionScrollY, self.RulesWindow.RulesMessageInjectionTextBox = Window.TextBox (self.RulesWindow.InjectionInputFrame, 1, 0, PadY = 0, Sticky = "NSEW", Text = self.RulesWindow.RuleData.Message, TooltipLabel = self.RulesWindow.TooltipLabel, TooltipText = self.RulesWindow.MessageInjectionTooltipText)
		
		self.RulesWindow.RulesInputButtons = None
		self.RulesWindow.RulesInputButtons = Window.Frame (self.RulesWindow.Base, Row = 3, Column = 0, Sticky = "EW")
		self.RulesWindow.RulesInputButtons.columnconfigure (0, weight = 1)
#		self.RulesWindow.PresetTitle = None
#		self.RulesWindow.PresetTitleText = "Preset Title (Only required for exporting...)"
#		self.RulesWindow.PresetTitle = Window.Entry (self.RulesWindow.RulesInputButtons, 0, 0, "EW", Text = self.RulesWindow.PresetTitleText, PadX = 0, TooltipLabel = self.RulesWindow.TooltipLabel, TooltipText = "Preset title is also the file name...\n(Alpha-numeric characters, and spaces allowed!)")
#		self.RulesWindow.PresetTitle.bind ("<FocusIn>", lambda event: (self.RulesWindow.PresetTitle.delete (0, 'end'), self.RulesUnbindSpace ())) # click event that clears the field.
#		self.RulesWindow.ExportPresetButton = None
#		self.RulesWindow.ExportPresetButton = Window.Button (self.RulesWindow.RulesInputButtons, 0, 1, "NSE", "Export Preset", self.RulesExportPresetAction, Width = 11, Height = 1, TooltipLabel = self.RulesWindow.TooltipLabel, TooltipText = "Exporting a set of rules allows you to use it as preset in other conversations.\n(By default a rule block only applies to a given conversation, when it is edited a new block is created, and the new one is used for further promts.)")
		self.RulesWindow.RulesInputWrap = tk.BooleanVar (value = 1)
		self.RulesWindow.WrapButton = None
		self.RulesWindow.WrapButton = Window.CheckButton (self.RulesWindow.RulesInputButtons, 0, 2, "NSE", "Wrap", self.RulesWindow.RulesInputWrap, lambda: (self.RulesWindow.RulesInputTextBox.configure (wrap = ("word" if self.RulesWindow.RulesInputWrap.get () else "none")), self.RulesWindow.RulesMessageInjectionTextBox.configure (wrap = ("word" if self.RulesWindow.RulesInputWrap.get () else "none"))), PadX = 0, Height = 1, TooltipLabel = self.RulesWindow.TooltipLabel, TooltipText = "Wrap text in the textbox...")
		
		# Key binding...
		self.SpaceBinding = self.Window.bind ('<space>', lambda event: self.RulesWindow.RulesInputTextBox.focus ())
		self.EscBinding = self.Window.bind ('<Escape>', lambda event: self.RulesWindow.BackButton.invoke ())
		if platform.system () != 'Darwin':
			self.CtrlABinding = self.Window.bind ('<Control-a>', lambda event: event.widget.tag_add ('sel', '1.0', 'end')) # [Ctrl / Cmd] + [A]
		else:
			self.CtrlABinding = self.Window.bind ('<Command-a>', lambda event: event.widget.tag_add ('sel', '1.0', 'end')) # [Ctrl / Cmd] + [A]
	
	
	
	
	
	
	def OpenWindow (self):
		self.Window.mainloop ()
