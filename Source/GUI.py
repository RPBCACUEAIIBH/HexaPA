#! /bin/python3

import os
import glob
import re
import webbrowser
import tkinter as tk
import datetime
import platform

from HexaLibPython import HexaLog as HL
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


class GUI:
	PWD = None
	
	
	
	def __init__ (self, SettingsObject):
		self.S = SettingsObject
		self.Window = tk.Tk (className = "HexaPA") # Not sure why the className is displayed as "HexaPA" instead of "HexaPA" as I set it... (on ubuntu)
		self.Window.title ("HexaPA")
		WinWidth = 640
		WinHeight = self.Window.winfo_screenheight()
		PosX = self.Window.winfo_screenwidth() - WinWidth
		PosY = 0
		HL.Log ("GUI.py: WindowSize: " + str (WinWidth) + " x " + str (WinHeight) + "; PosX:" + str (PosX) + "; PosY" + str (PosY), 'D', 2)
		self.Window.geometry (f"{WinWidth}x{WinHeight}+{PosX}+{PosY}")
		self.Window.resizable (True, True)
		self.Window.configure (bg = Theme.BGColor)
		self.Window.columnconfigure (0, weight = 1)
		self.Window.rowconfigure (0, weight = 1)
		self.SVGFile_OSRCLogo = "Images/LogoOSRC.svg"
		# self. is important for self.OSRCLogo otherwise the data is discarded before displaying so you get no error but no image either!
		self.OSRCLogo = ImageTk.PhotoImage (Image.open (io.BytesIO (cairosvg.svg2png (bytestring = open(self.SVGFile_OSRCLogo, "rb").read (), scale = 1)))) # Either use: "scale = 1" OR "output_width = 150, output_height = 150"
		self.Window.iconphoto (True, self.OSRCLogo)
		self.EnterBinding = None
		self.SpaceBinding = None
		self.EscBinding = None
		self.RBinding = None
		self.CtrlEnterBinding = None
		self.CtrlRBinding = None
		
	
	
	
	def SetKeys (self, KeysObject): # Called once after password request screen. This destroys the first window to do something outside the GUI class.
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
		self.Conversation = BlockChain (6)
		return self.Conversation
	
	
	
	def Link_OSRC (self):
		webbrowser.open_new_tab ("osrc.rip")
	
	
	
	def Link_OpenAI_API (self):
		webbrowser.open_new_tab ("https://platform.openai.com/overview")
	
	
	
	
	
	
	
	def PasswordRequestSubmitAction (self):
		if self.S.UserName == "" and self.PasswordRequestWindow.UserNameEntry.get ().strip () != "":
			self.S.UserName = self.PasswordRequestWindow.UserNameEntry.get ().strip ()
			self.S.SaveSettings ()
		self.PWD = self.PasswordRequestWindow.PasswordEntry.get ().strip ()
		self.WinWidth = None
		self.WinWidth = self.Window.winfo_width ()
		self.WinHeight = None
		self.WinHeight = self.Window.winfo_height ()
		self.WinPosX = None
		self.WinPosX = self.Window.winfo_x ()
		self.WinPosY = None
		self.WinPosY = self.Window.winfo_y ()
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
		# Due credits turned to corporate joke when I went to check if the logo is allowd to be used, after I wrote this section... ;)
		# I worked on this code, so I'm not removing it, and not beging for written permission either! Update the ToS! :P
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
	
	
	
	
	
	
	
	def KeyRequestSubmitAction (self):
		self.K.Key_OpenAI = self.KeyRequestWindow.KeyEntry_OpenAI.get ().strip ()
		if self.K.Key_OpenAI:
			self.KeyRequestWindow.SubmitButton.configure (state = tk.DISABLED)
			Communicate ("OpenAI", self.K.Key_OpenAI) # Test key
			if Communicate.Disabled_OpenAI != True: # Key accepted
				self.Window.unbind ('<Return>', self.EnterBinding)
				self.Window.unbind ('<Escape>', self.EscBinding)
				self.K.SaveKeys ()
				self.KeyRequestWindow.Base.grid_forget ()
				self.Main ()
			else: # Key not accepted
				self.KeyRequestWindow.ErrorLabel.config (text = "Error: The OpenAI key is invalid! Please try another!")
				self.KeyRequestWindow.SubmitButton.configure (state = tk.NORMAL)
	
	
	
	def KeyRequestSkipAction (self):
		self.Window.unbind ('<Return>', self.EnterBinding)
		self.Window.unbind ('<Escape>', self.EscBinding)
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
		Text = "(You will need to register. Once you're logged in, find manage account in the\ntop right corner and set up payment method at billing, then generate an API key.\nIt's affordable, but you may also want to set a monthly limit, just in case.)"
		self.KeyRequestWindow.OpenAIGuideLabel = None
		self.KeyRequestWindow.OpenAIGuideLabel = Window.Label (self.KeyRequestWindow.OpenAIFrame, 2, 0, "EW", Text, Theme.BGColor, Theme.SmallText, Theme.SmallTextSize, Width = None, PadX = None, PadY = None)
		self.KeyRequestWindow.OpenAIGuideLabel.bind ("<Button-1>", lambda e: self.Link_OpenAI_API ())
		self.KeyRequestWindow.KeyEntry_OpenAI = None
		self.KeyRequestWindow.KeyEntry_OpenAI = Window.Entry (self.KeyRequestWindow.OpenAIFrame, 3, 0, "EW", Width = 50, PadX = None)
		self.KeyRequestWindow.KeyEntry_OpenAI.focus ()
		
		# OpenAssistant, Google, and perhaps other alternatives...
		# No APIs yet... (Don't forget to increment common frame row for the Common frame below...)
		
		### Common frame
		self.KeyRequestWindow.CommonFrame = None
		self.KeyRequestWindow.CommonFrame = Window.Frame (self.KeyRequestWindow.Base, Row = 2, Column = 0, Sticky = "EW")
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
	
	
	
	
	
	
	
	def CreateNewChat (self):
		self.Window.unbind ('<Return>', self.EnterBinding)
		self.S.MaxContextMsg = int (self.MainWindow.MaxContextMsgEntry.get ())
		self.S.MaxTokens = int (self.MainWindow.MaxTokensEntry.get ())
		self.Conversation.Subject = self.MainWindow.Subject.get ()
		if self.Conversation.Subject != "Enter the subject here... (optional)" and self.Conversation.Subject != "":
			HL.Log ("GUI.py: Creating new conversation with subject: " + self.Conversation.Subject, 'I', 2)
		else:
			HL.Log ("GUI.py: Creating new conversation with unknown subject.", 'I', 2)
		self.MainWindow.Base.grid_forget ()
		self.Chat ()
	
	
	
	def ContinueExistingChat (self, ArgList):
		self.Window.unbind ('<Return>', self.EnterBinding)
		self.S.MaxContextMsg = int (self.MainWindow.MaxContextMsgEntry.get ())
		self.S.MaxTokens = int (self.MainWindow.MaxTokensEntry.get ())
		HL.Log ("GUI.py: Loading: " + str (self.MainWindow.ConversationList[ArgList[0]].File), 'I', 2)
		self.Conversation.Load (self.MainWindow.ConversationList[ArgList[0]].File)
		self.MainWindow.Base.grid_forget ()
		self.Chat ()
		self.Window.update ()
		self.MainWindow.Base.destroy ()
	
	
	
	def DeleteChat (self, ArgList):
		try:
			os.remove(self.MainWindow.ConversationList[ArgList[0]].File)
			HL.Log ("GUI.py: Deleted: " + str (self.MainWindow.ConversationList[ArgList[0]].File), 'I', 2)
		except OSError as e:
			HL.Log ("GUI.py: Error deleting " + str (self.MainWindow.ConversationList[ArgList[0]].File) + f": {e}", 'E', 2)
		self.MainWindow.Base.grid_forget ()
		self.Main ()
	
	
	
	def Main (self):
		self.MainWindow = Window (self.Window)
		self.MainWindow.Base.columnconfigure (0, weight = 1)
		self.MainWindow.Base.rowconfigure (1, weight = 1) # Set row 1 to expand not 0 here...
		
		### Title
		self.MainWindow.TitleFrame (self.MainWindow.Base, 0, 0, Command = self.Link_OSRC)
		
		### Conversation list
		self.MainWindow.Canvas = None
		self.MainWindow.CanvasInnerFrame = None
		self.MainWindow.Canvas, self.MainWindow.CanvasInnerFrame = Window.ScrollCanvas (self.MainWindow.Base, 1, 0, "NSEW")
		
		## New Chat
		self.MainWindow.NewChatFrame = None
		self.MainWindow.NewChatFrame = Window.Frame (self.MainWindow.CanvasInnerFrame, Theme.PromptBG, Packed = True)
		self.MainWindow.Subject = None
		self.MainWindow.Subject = Window.Entry (self.MainWindow.NewChatFrame, 0, 0, "EW", Text = "Enter the subject here... (optional)")
		self.MainWindow.Subject.bind ("<FocusIn>", lambda event: self.MainWindow.Subject.delete (0, 'end')) # click event that clears the field.
		self.MainWindow.Subject.bind ("<FocusOut>", lambda event: self.MainWindow.Subject.insert (0, "Enter the subject here... (optional)")) # click event that clears the field.
		self.MainWindow.NewChatButton = None
		self.MainWindow.NewChatButton = Window.Button (self.MainWindow.NewChatFrame, 0, 1, "E", "Start new conversation", self.CreateNewChat, Width = 18)
		
		## Existing conversations
		self.MainWindow.ConversationList = []
		ConversationDir = "Conversations"
		for BinFile in glob.glob (os.path.join (ConversationDir, "*.bin")):
			X = BlockChain (6)
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
		
		## Max Context Messages
		self.MainWindow.MaxContextMsgFrame = None
		self.MainWindow.MaxContextMsgFrame = Window.Frame (self.MainWindow.SettingsFrame, Row = 1, Column = 0, PadY = 0, Sticky = "W")
		self.MainWindow.MaxContextMsgFrame.columnconfigure (1, weight = 1)
		self.MainWindow.MaxContextMsgLabel = None
		self.MainWindow.MaxContextMsgLabel = Window.Label (self.MainWindow.MaxContextMsgFrame, 0, 0, "W", "Max Context Messages (Even numbers recommended.):", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.MaxContextMsgEntry = None
		self.MainWindow.MaxContextMsgEntry = Window.Entry (self.MainWindow.MaxContextMsgFrame, 0, 1, "EW", Text = str (self.S.MaxContextMsg), Width = 5)
		self.MainWindow.MaxTokensFrame = None
		self.MainWindow.MaxTokensFrame = Window.Frame (self.MainWindow.SettingsFrame, Row = 2, Column = 0, PadY = 0, Sticky = "W")
		self.MainWindow.MaxTokensFrame.columnconfigure (1, weight = 1)
		self.MainWindow.MaxTokensLabel = None
		self.MainWindow.MaxTokensLabel = Window.Label (self.MainWindow.MaxTokensFrame, 0, 0, "W", "Max Tokens (Rules + Context + Prompt combined):", Theme.BGColor, Anchor = "w", Width = None)
		self.MainWindow.MaxTokensEntry = None
		self.MainWindow.MaxTokensEntry = Window.Entry (self.MainWindow.MaxTokensFrame, 0, 1, "EW", Text = str (self.S.MaxTokens), Width = 5)
		
		### Key bindings
		self.SpaceBinding = self.Window.bind ('<space>', lambda event: self.MainWindow.Subject.focus ())
		self.EnterBinding = self.Window.bind ('<Return>', lambda event: self.MainWindow.NewChatButton.invoke ())
	
	
	
	
	
	
	
	def ChatBackAction (self):
		self.Window.unbind ('<space>', self.SpaceBinding)
		self.Window.unbind ('<Escape>', self.EscBinding)
		if platform.system () != 'Darwin':
			self.Window.unbind ('<Control-Return>', self.CtrlEnterBinding)
			self.Window.unbind ('<Control-R>', self.CtrlRBinding)
		else:
			self.Window.unbind ('<Command-Return>', self.CtrlEnterBinding)
			self.Window.unbind ('<Command-R>', self.CtrlRBinding)
		if self.Conversation.File:
			HL.Log ("GUI.py: Saving conversation!", 'I', 2)
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
			self.Window.unbind ('<Control-R>', self.CtrlRBinding)
		else:
			self.Window.unbind ('<Command-Return>', self.CtrlEnterBinding)
			self.Window.unbind ('<Command-R>', self.CtrlRBinding)
		self.ChatWindow.Base.grid_forget ()
		self.Rules ()
	
	
	
	def ChatCountTokensAction (self):
		if self.Conversation.LatestRules != None:
			MessageData = Data (self.Conversation.LatestRules, [], Message = self.ChatWindow.UserInputTextBox.get ("1.0", "end").strip ())
			Rules = {"role": "system", "content": self.Conversation.Rules.Rules}
		else:
			MessageData = Data ("", [], Message = self.ChatWindow.UserInputTextBox.get ("1.0", "end").strip ())
			Rules = {"role": "system", "content": ""}
		Context = None
		Prompt = {"role": "user", "content": self.ChatWindow.UserInputTextBox.get ("1.0", "end").strip ()}
		Messages = [Rules]
		if Context != None:
			Messages.extend (Context)
		Messages.append (Prompt)
		T = Tokenizer ("OpenAI", "gpt-3.5-turbo", Messages)
		self.ChatWindow.StatsLabel.config (text = "Token estimations:   Rules: " + str (T.TokenCount_Rules) + "   Context: " + str (T.TokenCount_Context) + "   Prompt: " + str (T.TokenCount_Prompt) + "   Total to send: " + str (T.TokenCount_Total))
	
	
	
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
		if UserName == "HexaPA": # This makes the background color difference between prompt and answer frames...
			self.ChatWindow.Messages.append (Window (self.ChatWindow.CanvasInnerFrame, BGColor = Theme.ResponseBG, Packed = True))
			self.ChatWindow.Messages[Index].Base.columnconfigure (0, weight = 1)
			self.ChatWindow.Messages[Index].Base.rowconfigure (1, weight = 1)
			self.ChatWindow.Messages[Index].AuthorFrame = None
			self.ChatWindow.Messages[Index].AuthorFrame = Window.Frame (self.ChatWindow.Messages[Index].Base, Theme.ResponseBG, 0, 0, 0, 0, "EW")
			self.ChatWindow.Messages[Index].AuthorFrame.columnconfigure (0, weight = 1)
			self.ChatWindow.Messages[Index].Author = None
			self.ChatWindow.Messages[Index].Author = Window.Label (self.ChatWindow.Messages[Index].AuthorFrame, 0, 0, "EW", UserName, Theme.ResponseBG, Anchor = "w", Width = None)
		else:
			self.ChatWindow.Messages.append (Window (self.ChatWindow.CanvasInnerFrame, BGColor = Theme.PromptBG, Packed = True))
			self.ChatWindow.Messages[Index].Base.columnconfigure (0, weight = 1)
			self.ChatWindow.Messages[Index].Base.rowconfigure (1, weight = 1)
			self.ChatWindow.Messages[Index].AuthorFrame = None
			self.ChatWindow.Messages[Index].AuthorFrame = Window.Frame (self.ChatWindow.Messages[Index].Base, Theme.PromptBG, 0, 0, 0, 0, "EW")
			self.ChatWindow.Messages[Index].AuthorFrame.columnconfigure (0, weight = 1)
			self.ChatWindow.Messages[Index].Author = None
			self.ChatWindow.Messages[Index].Author = Window.Label (self.ChatWindow.Messages[Index].AuthorFrame, 0, 0, "EW", UserName, Theme.PromptBG, Anchor = "w", Width = None)
		self.ChatWindow.Messages[Index].MessageData = None
		if MsgData != None:
			self.ChatWindow.Messages[Index].MessageData = MsgData # Existing message.
		else:
			self.ChatWindow.Messages[Index].MessageData = Data (Name = UserName, Message = Content) # New message.
		self.ChatWindow.Messages[Index].Wrap = tk.BooleanVar (value = 1)
		self.ChatWindow.Messages[Index].WrapButton = None
		self.ChatWindow.Messages[Index].WrapButton = Window.CheckButton (self.ChatWindow.Messages[Index].AuthorFrame, 0, 1, "E", "Wrap", self.ChatWindow.Messages[Index].Wrap, lambda: self.ChatWindow.Messages[Index].TextBox.configure (wrap = ("word" if self.ChatWindow.Messages[Index].Wrap.get () else "none")))
		self.ChatWindow.Messages[Index].Exclude = tk.BooleanVar (value = 0)
		self.ChatWindow.Messages[Index].Include = tk.BooleanVar (value = 0)
		self.ChatWindow.Messages[Index].ExcludeButton = None
		self.ChatWindow.Messages[Index].ExcludeButton = Window.CheckButton (self.ChatWindow.Messages[Index].AuthorFrame, 0, 2, "E", "Exclude", self.ChatWindow.Messages[Index].Exclude, lambda: self.ChatWindow.Messages[Index].Include.set (False), Width = 7)
		self.ChatWindow.Messages[Index].IncludeButton = None
		self.ChatWindow.Messages[Index].IncludeButton = Window.CheckButton (self.ChatWindow.Messages[Index].AuthorFrame, 0, 3, "E", "Inlcude", self.ChatWindow.Messages[Index].Include, lambda: self.ChatWindow.Messages[Index].Exclude.set (False), Width = 7)
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
		self.ChatWindow.Messages[Index].TextBox.focus ()
		
		# Refresh canvas scroll region
		if len (self.ChatWindow.Messages) > 5: # That many will most likely fit on the screen, so no need to scroll. (Otherwise the first prompt goes off screen before the screen is full.)
			self.ChatAutoScroll ()
		self.Window.update ()
	
	
	
	def ChatSendAction (self):
		self.ChatWindow.SendButton.configure (state = tk.DISABLED)
		
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
		Prompt = {"role": "user", "content": self.ChatWindow.Messages[PromptIndex].MessageData.Message}
		
		### Generate context... (Optional for the API, but AI doesn't "remember" previous prompt/answer without it...)
		Context = None
		ContextIDs = None
		Messages = []
		Messages.append (Rules)
		Messages.append (Prompt)
		T = Tokenizer ("OpenAI", "gpt-3.5-turbo", Messages)
		MaxContextTokens = self.S.MaxTokens - T.TokenCount_Rules - T.TokenCount_Prompt
		HL.Log ("GUI.py: MaxTokens allowed: " + str (self.S.MaxTokens) + ", Estimated rules tokens: " + str (T.TokenCount_Rules) + ", Estimated prompt tokens: " + str (T.TokenCount_Prompt) + " --> MaxContextTokens " + str (MaxContextTokens) + ", MaxContextMessages: " + str (self.S.MaxContextMsg), 'D', 2)
		# Create list of messages...
		Offset = 1 # The last context message is len (self.ChatWindow.Messages) - 2 since len (self.ChatWindow.Messages) - 1 is the prompt...
		ContextCount = 0
		HL.Log ("GUI.py: Exclusion compensation loop...", 'D', 2)
		for i in range (1, len (self.ChatWindow.Messages)): # This loop compensates for excluded messages, otherwise if you exclude messages, less then max allowd messages are even considered...
			Index = len (self.ChatWindow.Messages) - i
			if Index < 0: # New conversation -> less then max allowed messages...
				HL.Log ("GUI.py: Loop exitted at Index: " + str (Index) + ", i: " + str (i) + ", FinalContextCount: " + str (ContextCount), 'D', 2)
				break
			HL.Log ("GUI.py: Message Exclude: " + str (self.ChatWindow.Messages[Index].Exclude.get ()) + ", Include: " + str (self.ChatWindow.Messages[Index].Include.get ()), 'D', 2)
			if self.ChatWindow.Messages[Index].Exclude.get () == True: # Exclude message from context...
				HL.Log ("GUI.py: Excluded message.", 'D', 2)
				if self.S.MaxContextMsg + Offset < len (self.ChatWindow.Messages) - 1:
					HL.Log ("GUI.py: Increasing offset because: self.S.MaxContextMsg + Offset < len (self.ChatWindow.Messages) - 1  --> New offset: " + str (Offset + 1), 'D', 2)
					Offset += 1
				continue
			elif self.S.AutoContext == False and self.ChatWindow.Messages[Index].Include.get () == False:
				HL.Log ("GUI.py: Neither excluded nor included message in manual inclusion mode.", 'D', 2)
				if self.S.MaxContextMsg + Offset < len (self.ChatWindow.Messages) - 1:
					HL.Log ("GUI.py: Increasing offset because: self.S.MaxContextMsg + Offset < len (self.ChatWindow.Messages) - 1  --> New offset: " + str (Offset + 1), 'D', 2)
					Offset += 1
				continue
			else:
				ContextCount += 1
				HL.Log ("GUI.py: ContextCount: " + str (ContextCount), 'D', 2)
				if ContextCount == self.S.MaxContextMsg:
					HL.Log ("GUI.py: Loop exitted at Index: " + str (Index) + ", i: " + str (i) + ", FinalContextCount: " + str (ContextCount), 'D', 2)
					break
		HL.Log ("GUI.py: Context generation loop...", 'D', 2)
		for i in range (2, self.S.MaxContextMsg + Offset + 2): # +1 because range counts from min to i < max and the prompt is excluded
			Index = len (self.ChatWindow.Messages) - i
			if Index < 0: # New conversation -> less then max allowed messages...
				HL.Log ("GUI.py: Loop exitted at Index: " + str (Index) + ", i: " + str (i), 'D', 2)
				break
			HL.Log ("GUI.py: Message Exclude: " + str (self.ChatWindow.Messages[Index].Exclude.get ()) + ", Include: " + str (self.ChatWindow.Messages[Index].Include.get ()), 'D', 2)
			if self.ChatWindow.Messages[Index].Exclude.get () == True: # Excluded message
				HL.Log ("GUI.py: Excluded message.", 'D', 2)
				continue
			elif self.S.AutoContext == False and self.ChatWindow.Messages[Index].Include.get () == False: # Neither excluded nor included message in manual inclusion mode.
				HL.Log ("GUI.py: Neither excluded nor included message in manual inclusion mode.", 'D', 2)
				continue
			else: # Included message
				HL.Log ("GUI.py: Considering message at index: " + str (Index), 'D', 2)
				if self.ChatWindow.Messages[Index].MessageData.Name == self.S.UserName:
					ContextMessage = {"role": "user", "content": self.ChatWindow.Messages[Index].MessageData.Message}
				else:
					ContextMessage = {"role": "assistant", "content": self.ChatWindow.Messages[Index].MessageData.Message}
				HL.Log ("GUI.py: Message: " + str (ContextMessage), 'D', 2)
				if MaxContextTokens >= Tokenizer.Count ("OpenAI", "gpt-3.5-turbo", "role: " + ContextMessage["role"] + ", content: " + ContextMessage["content"]):
					HL.Log ("GUI.py: Message included!", 'D', 2)
					if Context == None:
						Context = []
						ContextIDs = []
					Context.insert (0, ContextMessage)
					ContextIDs.insert (0, self.ChatWindow.Messages[Index].MessageData.BlockID)
					ContextCount -= 1
					HL.Log ("GUI.py: Remaining ContextCount: " + str (ContextCount), 'D', 2)
				else:
					HL.Log ("GUI.py: Message too large!", 'D', 2)
					HL.Log ("GUI.py: Loop exitted at Index: " + str (Index) + ", i: " + str (i), 'D', 2)
					break
		
		if ContextIDs != None:
			self.ChatWindow.Messages[PromptIndex].MessageData.Context = ContextIDs
		HL.Log ("GUI.py: FinalContextCount: " + str (self.S.MaxContextMsg - ContextCount), 'D', 2)
		
		# Context token estimation
		Messages = []
		Messages.append (Rules)
		if Context != None:
			Messages.extend (Context)
		Messages.append (Prompt)
		T = Tokenizer ("OpenAI", "gpt-3.5-turbo", Messages)
		self.ChatWindow.StatsLabel.config (text = "Token estimations:   Rules: " + str (T.TokenCount_Rules) + "   Context: " + str (T.TokenCount_Context) + "   Prompt: " + str (T.TokenCount_Prompt) + "   Total to send: " + str (T.TokenCount_Total))
		self.Window.update ()
		
		# Debug
		if Context != None and Args.debug:
			for Item in Context:
				print (Item)
		HL.Log ("GUI.py: Estimated context tokens: " + str (T.TokenCount_Context) + " --> Estimated total tokens: " + str (T.TokenCount_Total), 'D', 2)
		
		### Record promt into a new block.
		self.Conversation.NewBlock (self.ChatWindow.Messages[PromptIndex].MessageData.Dump (self.K.UserKey))
		self.ChatWindow.Messages[PromptIndex].MessageData.BlockID = self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID
		
		### Send message then display and recod response to new block
		Response = Communicate.AskTheAI ("OpenAI", "gpt-3.5-turbo", Rules, Context, Prompt) # Arguments: API, AIModel, Rules, Context, Prompt, MaxTokens = 2048
		ErrorText = None
		if not isinstance (Response, openai.openai_object.OpenAIObject):
			ErrorText = "Error: API did not respond. The servere is probably overloaded... If this problem persist, check the Log.log file for more information."
			self.DisplayMessage ("HexaPA", ErrorText)
			self.ChatWindow.StatsLabel.config (text = "An error occurred! The propmpt reloaded and first try excluded, you may try re-sending.")
		else:
			self.DisplayMessage ("HexaPA", Response['choices'][0]['message']['content'])
			self.ChatWindow.StatsLabel.config (text = "Actual token usage:   Rules + Context + Prompt: " + str (Response['usage']['prompt_tokens']) + "   Response: " + str (Response['usage']['completion_tokens']) + "   Total: " + str (Response['usage']['total_tokens']))
		Index = len (self.ChatWindow.Messages) - 1
		self.Conversation.NewBlock (self.ChatWindow.Messages[Index].MessageData.Dump (self.K.UserKey))
		if ErrorText != None:
			self.ChatWindow.Messages[Index].MessageData.Rating = -1
			self.ChatWindow.Messages[Index].Exclude.set (True)
			self.ChatWindow.Messages[Index - 1].MessageData.Rating = -1
			self.ChatWindow.Messages[Index - 1].Exclude.set (True)
			self.ChatWindow.UserInputTextBox.insert ('end', self.ChatWindow.Messages[Index - 1].MessageData.Message) # Allow the user to try again by simply clicking send again.
		self.ChatWindow.Messages[Index].MessageData.BlockID = self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID
		
		# Update ratings block ratings. (If the gui is closed by the user anything in self.ChatWindow will be lost, self.Conversation survives and gets saved before exit unless the SIGKILL is given.)
		for Index in range (0, len (self.ChatWindow.Messages)):
			if self.ChatWindow.Messages[Index].Exclude.get () == True:
				self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = -1
			elif self.ChatWindow.Messages[Index].Include.get () == True:
				self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = 1
			else:
				self.Conversation.Blocks[self.ChatWindow.Messages[Index].MessageData.BlockID].Rating = 0
		self.ChatWindow.SendButton.configure (state = tk.NORMAL)
		
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
			HL.Log ("GUI.py: Unspecified Subject! --> Asking the AI to summarize it in a sentence.", 'I', 2)
			Response = Communicate.AskTheAI ("OpenAI", "gpt-3.5-turbo", SubjectDetectionRules, Context, Prompt) # Arguments: API, AIModel, Rules, Context, Prompt, MaxTokens = 2048
			if isinstance (Response, openai.openai_object.OpenAIObject): # AI Respose
				self.Conversation.Subject = Response['choices'][0]['message']['content']
				HL.Log ("GUI.py: AI said the subject is: " + self.Conversation.Subject, "I", 2)
				self.ChatWindow.SubjectLabel.config (text = self.Conversation.Subject + " (Created at " + self.Conversation.CreationTime + ")")
		elif PromptIndex == BlockID:
			self.ChatWindow.SubjectLabel.config (text = self.Conversation.Subject + " (Created at " + self.Conversation.CreationTime + ")")
		
		### Generate filename if does not exist...
		if self.Conversation.File == None:
			self.Conversation.File = "Conversations/" + re.sub ('[\W_]+', '_', self.Conversation.CreationTime) + ".bin"
			HL.Log ("GUI.py: Chat will be saved to: " + self.Conversation.File, 'D', 2)
	
	
	
	def UnincludeAction (self):
		for Index in range (0, len (self.ChatWindow.Messages)):
			if self.ChatWindow.Messages[Index].Include.get () == True:
				self.ChatWindow.Messages[Index].Include.set (False)
	
	
	
	def ExportAction (self):
		Commands.Export (self.K.UserKey, self.Conversation)
	
	
	
	def Chat (self, Stats = None):
		self.ChatWindow = Window (self.Window)
		self.ChatWindow.Base.columnconfigure (0, weight = 1)
		self.ChatWindow.Base.rowconfigure (1, weight = 1) # Set row 1 to expand not 0 here...
		
		### Subject label and Back to Main / Edit Rules buttons
		self.ChatWindow.SubjectFrame = None
		self.ChatWindow.SubjectFrame = Window.Frame (self.ChatWindow.Base, Row = 0, Column = 0, PadX = 0, PadY = 0, Sticky = "NEW")
		self.ChatWindow.SubjectFrame.columnconfigure (1, weight = 1)
		self.ChatWindow.BackButton = None
		self.ChatWindow.BackButton = Window.Button (self.ChatWindow.SubjectFrame, 0, 0, "W", "Back", self.ChatBackAction, Height = 1, PadX = 0)
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
		self.ChatWindow.ExportButton = Window.Button (self.ChatWindow.SubjectFrame, 0, 2, "E", "Export", self.ExportAction, Width = 5, Height = 1)
		self.ChatWindow.RulesButton = None
		self.ChatWindow.RulesButton = Window.Button (self.ChatWindow.SubjectFrame, 0, 3, "E", "Edit Rules", self.ChatRulesAction, Width = 8, Height = 1, PadX = 0)
		
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
		self.ChatWindow.UserInputTextBoxFrame, self.ChatWindow.UserInputScrollX, self.ChatWindow.UserInputScrollY, self.ChatWindow.UserInputTextBox = Window.TextBox (self.ChatWindow.UserInputFrame, 0, 0, PadX = 0, Sticky = "EW")
		self.ChatWindow.UserInputTextBox.bind ("<FocusIn>", lambda event: self.ChatWindow.UserInputTextBox.config (height = 12)) # click event that enlarges the field.
		self.ChatWindow.UserInputTextBox.bind ("<FocusOut>", lambda event: self.ChatWindow.UserInputTextBox.config (height = 3)) # click away event that shriks the field.
		self.ChatWindow.UserInputButtons = None
		self.ChatWindow.UserInputButtons = Window.Frame (self.ChatWindow.UserInputFrame, Row = 1, Column = 0, PadX = 0, PadY = 0, Sticky = "EW")
		self.ChatWindow.UserInputButtons.columnconfigure (1, weight = 1)
		self.ChatWindow.AutoContext = tk.BooleanVar (value = 1)
		self.S.AutoContext = True # Auto context should be on by default, it's only for special cases like asking the AI something totally unrelated, or if you want it to work with specific context within the conversation...
		self.ChatWindow.AutoContextButton = None
		self.ChatWindow.AutoContextButton = Window.CheckButton (self.ChatWindow.UserInputButtons, 0, 0, "NSW", "Auto Context", self.ChatWindow.AutoContext, lambda: setattr (self.S, 'AutoContext', bool (self.ChatWindow.AutoContext.get ())), Width = 11, Height = 1, PadX = 0)
		self.ChatWindow.Uninclude = None
		self.ChatWindow.Uninclude = Window.Button (self.ChatWindow.UserInputButtons, 0, 1, "NSW", "Uninclude All", self.UnincludeAction, Width = 10, Height = 1)
		self.ChatWindow.UserInputWrap = tk.BooleanVar (value = 1)
		self.ChatWindow.SpacerFrame = None
		self.ChatWindow.SpacerFrame = Window.Frame (self.ChatWindow.UserInputButtons, Row = 0, Column = 2, PadX = 0, PadY = 0, Sticky = "NSEW")
		self.ChatWindow.WrapButton = None
		self.ChatWindow.WrapButton = Window.CheckButton (self.ChatWindow.UserInputButtons, 0, 3, "NSE", "Wrap", self.ChatWindow.UserInputWrap, lambda: self.ChatWindow.UserInputTextBox.configure (wrap = ("word" if self.ChatWindow.UserInputWrap.get () else "none")), Height = 1, PadX = 0)
		self.ChatWindow.TokenButton = None
		self.ChatWindow.TokenButton = Window.Button (self.ChatWindow.UserInputButtons, 0, 4, "NSE", "Count Tokens", self.ChatCountTokensAction, Width = 11, Height = 1)
		self.ChatWindow.SendButton = None
		self.ChatWindow.SendButton = Window.Button (self.ChatWindow.UserInputButtons, 0, 5, "NSE", "Send", lambda: self.ChatSendAction () if self.ChatWindow.UserInputTextBox.get ("1.0", "end-1c") else None, Height = 1, PadX = 0)
		if Stats == None:
			Stats = ""
		self.ChatWindow.StatsLabel = None
		self.ChatWindow.StatsLabel = Window.Label (self.ChatWindow.UserInputFrame, 2, 0, "W", Stats, Theme.BGColor, Theme.SmallText, Theme.SmallTextSize, "center", None, 0, 0)
		
		# Disable Send button in case the key was rejected
		if Communicate.Disabled_OpenAI == True: # Key rejected or no key
			self.ChatWindow.SendButton.configure (state = tk.DISABLED)
		
		### Load conversation
		try:
			self.ChatWindow.BackButton.configure (state = tk.DISABLED)
			if len (self.Conversation.Blocks) == 0: # Reminder, in case there is no content yet...
				Text = "Remember:\n- Use [Enter] for new line (as in text editors), [Ctrl/Cmd]+[Enter] to send the message, [Ctrl/Cmd]+[R] to edit Rules. [Esc] to go back to main and [Alt]+[F4] to save and exit. (Not tested on mac!)\n- Clicking on a message enlarges it for easier reading.\n- Click on the input textbox or use [space] key in the chat and rules screen to focus on user input and start writing.\n- Your prompt + the rules you set + the context you select must be less then 2048 tokens!\n- The AI's answer may or may not fit into 2048 tokens, but it is limited to that by OpenAI!\n- It does not remember! The rules and context you send, is all it has to work with!\n- It does not think! It simply reacts to the given text, generating a response.\n- Do not ask for a numerical answer, the AI is simply terrible at math! It guesses the answer based on it's probablility, rather then calculating it. (The current model at least...)\n- Be concise, don't argue with the AI if it doesn't give you the answer you want, because you pay for your argument as well as the AI's apology, and it may still not give you an acceptable answer! Instead tweak what rules, context, and prompt you send next!\n- It does not feel, so praising or cursing it only cost you money! (Still it's a good to be polite, just to avoid developing bad habits...)\n\n- OpenAI's current policy (as of 5th of May 2023) says that they don't use data form API calls for training. (...but off course every company leaves a clause in it's ToS to change anything anytime, so I advise against feeding it any sensitive information or code! Treat it with an \"Anything you say can be used against you!\" attitude!)\n\n- HexaPA is free and open source software, if you find it helpful please donate at: www.osrc.rip/Support.html"
				self.DisplayMessage ("Developer", Text)
			else: # Conversation
				if Args.renew_data: # Renew data...
					TempConversation = BlockChain (6)
					TempConversation.Subject = self.Conversation.Subject
					TempConversation.File = self.Conversation.File
				
				if self.Conversation.Validate () == True:
					HL.Log ("GUI.py: Chain validation complete!", 'D', 2)
				else:
					HL.Log ("GUI.py: Chain validation failed! >> Attempting to display read-only data! (This may fail...)", 'E', 2)
					HL.Log ("", 'E', 2)
					self.ChatWindow.SendButton.configure (state = tk.DISABLED)
				for Block in self.Conversation.Blocks:
					MessageData = Data ()
					MessageData.Parse (self.K.UserKey, Block.Data, Block.BlockID, Block.Rating)
					if not Args.renew_data and MessageData.DataVersion < Settings.DataVersion: # Warn... This should not change saved data, even if it's no longer supported...
						HL.Log ("GUI.py: Block contains old data. Some functionality may be unavailable during this conversation. (You can specify --renew-data option to renew the chain when continuing conversation.)", 'W', 2)
					elif Args.renew_data: # Renew data... (Don't check for old data, if this option is specified, the data must be added whether it's new or old, as the chain may contain different version data in each block...)
						HL.Log ("GUI.py: Saving block with new version data. (--renew-data specified)", 'I', 2)
						MessageData.DataVersion = Settings.DataVersion
						TempConversation.NewBlock (MessageData.Dump (self.K.UserKey))
					if MessageData.DataType == "Message":
						#MessageData.BlockID = Block.BlockID
						self.DisplayMessage (MsgData = MessageData)
					elif MessageData.DataType == "Rules":
						self.Conversation.LatestRules = Block.BlockID
						HL.Log ("GUI.py: Latest rule: " + str (Block.BlockID), 'D', 2)
				if Args.renew_data: # Renew data...
					TempConversation.Save ()
					self.Conversation.Clear ()
					self.Conversation.Load (TempConversation.File) # Reload with new data...
					TempConversation.Clear ()
			
			### Load Rules
			if self.Conversation.LatestRules != None:
				self.Conversation.Rules = Data ()
				self.Conversation.Rules.Parse (self.K.UserKey, self.Conversation.Blocks[self.Conversation.LatestRules].Data, self.Conversation.LatestRules)
		except Exception:
			HL.Log ("GUI.py: Could not parse block content! It can be corrupted or encrypted with other username and password combination... (This can happen when .Keys.bin and .Settings.bin has been deleted, and new credentials entered. If that's the case and block validation was successful, the conversation can still be decrypted with the initial username and password combination.)", 'E', 2)
			self.ChatWindow.SendButton.configure (state = tk.DISABLED)
		self.ChatWindow.BackButton.configure (state = tk.NORMAL)
		
		# Key binding...
		self.SpaceBinding = self.Window.bind ('<space>', lambda event: self.ChatWindow.UserInputTextBox.focus ())
		self.EscBinding = self.Window.bind ('<Escape>', lambda event: self.ChatWindow.BackButton.invoke ())
		if platform.system () != 'Darwin':
			self.CtrlEnterBinding = self.Window.bind ('<Control-Return>', lambda event: self.ChatWindow.SendButton.invoke ()) # [Ctrl / Cmd] + [Enter]
			self.CtrlRBinding = self.Window.bind ('<Control-r>', lambda event: self.ChatWindow.RulesButton.invoke ()) # [Ctrl / Cmd] + [R]
		else:
			self.CtrlEnterBinding = self.Window.bind ('<Command-Return>', lambda event: self.ChatWindow.SendButton.invoke ()) # [Ctrl / Cmd] + [Enter]
			self.CtrlRBinding = self.Window.bind ('<Command-r>', lambda event: self.ChatWindow.RulesButton.invoke ()) # [Ctrl / Cmd] + [R]
	
	
	
	
	
	
	
	def RulesBackAction (self):
		self.Window.unbind ('<space>', self.SpaceBinding)
		self.Window.unbind ('<Escape>', self.EscBinding)
		NewRules = Data (self.RulesWindow.RulesInputTextBox.get ("1.0", "end").strip (), DataType = "Rules")
		if self.Conversation.LatestRules == None and NewRules.Rules != "" and NewRules.Rules != self.RulesWindow.Reminder: # New conversation with no rules defined yet. (exclude reminder text)
			self.Conversation.NewBlock (NewRules.Dump (self.K.UserKey))
			self.Conversation.LatestRules = self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID # Last block's ID where the rules have just been saved.
			HL.Log ("GUI.py: First rules saved to block: " + str (self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID), 'D', 2)
			self.Conversation.Rules = Data () # If there ware no rules defined yet this shoud still be None
			self.Conversation.Rules.Parse (self.K.UserKey, self.Conversation.Blocks[self.Conversation.LatestRules].Data, self.Conversation.LatestRules)
		elif NewRules.Rules != self.RulesWindow.RuleData.Rules and NewRules.Rules != self.RulesWindow.Reminder: # If the rules have changed. (exclude reminder text)
			self.Conversation.NewBlock (NewRules.Dump (self.K.UserKey))
			self.Conversation.LatestRules = self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID # Last block's ID where the rules have just been saved.
			HL.Log ("GUI.py: New rules saved to block: " + str (self.Conversation.Blocks[len (self.Conversation.Blocks) - 1].BlockID), 'D', 2)
			self.Conversation.Rules.Parse (self.K.UserKey, self.Conversation.Blocks[self.Conversation.LatestRules].Data, self.Conversation.LatestRules)
		self.RulesWindow.Base.grid_forget ()
		self.ChatWindow.Base.grid (padx = Theme.PadX, pady = Theme.PadY, sticky = "NSEW") # No need to generate the chat content each time... it's slow, and already generated...
		self.Window.update ()
		self.SpaceBinding = self.Window.bind ('<space>', lambda event: self.ChatWindow.UserInputTextBox.focus ())
		self.EscBinding = self.Window.bind ('<Escape>', lambda event: self.ChatWindow.BackButton.invoke ())
		if platform.system () != 'Darwin':
			self.CtrlEnterBinding = self.Window.bind ('<Control-Return>', lambda event: self.ChatWindow.SendButton.invoke ()) # [Ctrl / Cmd] + [Enter]
			self.CtrlRBinding = self.Window.bind ('<Control-r>', lambda event: self.ChatWindow.RulesButton.invoke ()) # [Ctrl / Cmd] + [R]
		else:
			self.CtrlEnterBinding = self.Window.bind ('<Command-Return>', lambda event: self.ChatWindow.SendButton.invoke ()) # [Ctrl / Cmd] + [Enter]
			self.CtrlRBinding = self.Window.bind ('<Command-r>', lambda event: self.ChatWindow.RulesButton.invoke ()) # [Ctrl / Cmd] + [R]
		self.RulesWindow.Base.destroy ()
	
	
	
	def RulesExportPresetAction (self):
		pass
	
	
	
	def ClearReminder (self, event):
		self.RulesWindow.RulesInputTextBox.delete ('1.0', 'end')
		self.RulesWindow.RulesInputTextBox.config (fg = Theme.Text)
		self.RulesWindow.RulesInputTextBox.unbind ("<FocusIn>")
	
	
	
	def Rules (self, Stats = None):
		self.RulesWindow = Window (self.Window)
		self.RulesWindow.Base.columnconfigure (0, weight = 1)
		self.RulesWindow.Base.rowconfigure (1, weight = 1) # Set row 1 to expand not 0 here...
		
		### Subject label and Back to Main / Edit Rules buttons
		self.RulesWindow.TitleFrame = None
		self.RulesWindow.TitleFrame = Window.Frame (self.RulesWindow.Base, Row = 0, Column = 0, PadX = 0, PadY = 0, Sticky = "NEW")
		self.RulesWindow.TitleFrame.columnconfigure (1, weight = 1)
		self.RulesWindow.BackButton = None
		self.RulesWindow.BackButton = Window.Button (self.RulesWindow.TitleFrame, 0, 0, "W", "Back", self.RulesBackAction, Height = 1, PadX = 0)
		Text = "Rules for the AI"
		self.RulesWindow.SubjectLabel = None
		self.RulesWindow.SubjectLabel = Window.Label (self.RulesWindow.TitleFrame, 0, 1, "EW", Text, Theme.BGColor, Anchor = "w", Width = None)
		#self.RulesWindow.RulesButton = None
		#self.RulesWindow.RulesButton = Window.Button (self.RulesWindow.TitleFrame, 0, 2, "E", "Edit Rules", self.PresetsAction, Width = 10, Height = 1, PadX = 0)
		
		
		### UserInput
		self.RulesWindow.RulesInputFrame = None
		self.RulesWindow.RulesInputFrame = Window.Frame (self.RulesWindow.Base, Row = 2, Column = 0, PadX = 0, PadY = 0, Sticky = "EW")
		self.RulesWindow.RulesInputFrame.columnconfigure (0, weight = 1)
		self.RulesWindow.RulesInputTextBoxFrame = None
		self.RulesWindow.RulesInputScrollX = None
		self.RulesWindow.RulesInputScrollY = None
		self.RulesWindow.RulesInputTextBox = None
		self.RulesWindow.Reminder = "This text is just a reminder to you, it is not sent to the AI! (Don't worry you don't pay for it! This text will disappear as soon as you click here to input your rules.)\n\nRemember:\n- Apparently you pay for the tags every time for every message sent, whether it's rules, context or prompt since the token counter(tiktoken) gives the most accurate result with those tags included. It means that even if this section is left empty, and you do not include any context, the token counter will estimate a few tokens for the rules, since the API requires this line(which takes a few tokenst) to be sent: \"role\": \"system\", \"content\": \"\"\n- Try to be as short as possible with the rules, since you will pay for anything you put here every time you press the \"Send\" button in the chat. That being said this section is important to tweak the AI response for your productivity.\n- The rules (if changed) will be saved for the conversation when you go back to the chat screen, but you must export it as preset to become availabe in other conversations, however presets are stored separately and any changes to the rule will only be local unless you export the changed verstion again to a preset."
		self.RulesWindow.RuleData = Data (DataType = "Rules")
		if self.Conversation.LatestRules == None: # If no rules have been defined yet.
			HL.Log ("GUI.py: No Latest Rules ID: ", 'D', 2)
			self.RulesWindow.RulesInputTextBoxFrame, self.RulesWindow.RulesInputScrollX, self.RulesWindow.RulesInputScrollY, self.RulesWindow.RulesInputTextBox = Window.TextBox (self.RulesWindow.RulesInputFrame, 0, 0, PadX = 0, Sticky = "EW", Height = 42, Text = self.RulesWindow.Reminder)
			self.RulesWindow.RulesInputTextBox.config (fg = Theme.SmallText)
			self.RulesWindow.RulesInputTextBox.bind ("<FocusIn>", self.ClearReminder) # click event that clears the field.
		else:
			self.RulesWindow.RuleData.Parse (self.K.UserKey, self.Conversation.Blocks[self.Conversation.LatestRules].Data, self.Conversation.LatestRules)
			HL.Log ("GUI.py: Latest Rules ID: " + str (self.Conversation.LatestRules), 'D', 2)
			if self.RulesWindow.RuleData.DataType == "Rules" and self.RulesWindow.RuleData.Rules == "": # If the rules have been deleted.
				self.RulesWindow.RulesInputTextBoxFrame, self.RulesWindow.RulesInputScrollX, self.RulesWindow.RulesInputScrollY, self.RulesWindow.RulesInputTextBox = Window.TextBox (self.RulesWindow.RulesInputFrame, 0, 0, PadX = 0, Sticky = "EW", Height = 42, Text = self.RulesWindow.Reminder)
				self.RulesWindow.RulesInputTextBox.config (fg = Theme.SmallText)
				self.RulesWindow.RulesInputTextBox.bind ("<FocusIn>", self.ClearReminder) # click event that clears the field.
			else:
				self.RulesWindow.RulesInputTextBoxFrame, self.RulesWindow.RulesInputScrollX, self.RulesWindow.RulesInputScrollY, self.RulesWindow.RulesInputTextBox = Window.TextBox (self.RulesWindow.RulesInputFrame, 0, 0, PadX = 0, Sticky = "EW", Height = 42, Text = self.RulesWindow.RuleData.Rules)
		self.RulesWindow.RulesInputButtons = None
		self.RulesWindow.RulesInputButtons = Window.Frame (self.RulesWindow.RulesInputFrame, Row = 1, Column = 0, PadX = 0, PadY = 0, Sticky = "E")
		self.RulesWindow.RulesInputWrap = tk.BooleanVar (value = 1)
		self.RulesWindow.WrapButton = None
		self.RulesWindow.WrapButton = Window.CheckButton (self.RulesWindow.RulesInputButtons, 0, 0, "NSE", "Wrap", self.RulesWindow.RulesInputWrap, lambda: self.RulesWindow.RulesInputTextBox.configure (wrap = ("word" if self.RulesWindow.RulesInputWrap.get () else "none")), Height = 1)
		self.RulesWindow.ExportPresetButton = None
		self.RulesWindow.ExportPresetButton = Window.Button (self.RulesWindow.RulesInputButtons, 0, 1, "NSE", "Export Preset", self.RulesExportPresetAction, Width = 11, Height = 1)
		
		# Key binding...
		self.SpaceBinding = self.Window.bind ('<space>', lambda event: self.RulesWindow.RulesInputTextBox.focus ())
		self.EscBinding = self.Window.bind ('<Escape>', lambda event: self.RulesWindow.BackButton.invoke ())
	
	
	
	
	
	
	
	def OpenWindow (self):
		self.Window.mainloop ()
