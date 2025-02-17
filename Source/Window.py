#! /bin/python3

import io
import cairosvg
from PIL import Image, ImageTk
import tkinter as tk

from HexaLibPython import HexaLog as HL
from Source.Theme import *
from Source.Tooltip import *


class Window:
	SVGFile_OSRCLogo = "Images/LogoOSRC.svg"
	
	
	
	def __init__ (self, Parent, PadX = Theme.PadX, PadY = Theme.PadY, BGColor = Theme.BGColor, Packed = False):
		self.Base = tk.Frame (Parent, bg = BGColor)
		if Packed == True: # this is used for generated canvas content
			self.Base.pack (padx = PadX, pady = PadY, side = "top", fill = "both", expand = True)
		else: # This is used for base frame for each screen.
			self.Base.grid (padx = PadX, pady = PadY, sticky = "NSEW")
	
	
	
	@staticmethod
	def ScrollCanvas (Parent, Row, Column, Sticky, RowSpan = None, ColumnSpan = None):
		
		CanvasFrame = tk.Frame (Parent, bg = Theme.BGColor)
		CanvasFrame.grid (row = Row, column = Column, sticky = Sticky, rowspan = RowSpan, columnspan = ColumnSpan)
		CanvasFrame.columnconfigure (0, weight = 1)
		CanvasFrame.rowconfigure (0, weight = 1)
		
		Canvas = tk.Canvas (CanvasFrame, bg = Theme.BGColor, highlightthickness = 0)
		Canvas.grid (row = 0, column = 0, pady = Theme.PadY, sticky = "NSEW")
		Canvas.columnconfigure (0, weight = 1)
		Canvas.rowconfigure (0, weight = 1)
		
		InnerFrame = tk.Frame (Canvas, bg = Theme.BGColor, border = 0)
		InnerFrame.columnconfigure (0, weight = 1)
		InnerFrame.rowconfigure (0, weight = 1)
		InnerFrame.grid (sticky = 'NSEW')
		Canvas.create_window ((0,0), window = InnerFrame, anchor = 'nw')
		
		CanvasScrollbar = tk.Scrollbar (CanvasFrame, orient = "vertical", bg = Theme.BGColor, activebackground = Theme.ActiveButtonBG, width = 17, command = Canvas.yview)
		CanvasScrollbar.grid (row = 0, column = 1, pady = Theme.PadY, sticky = "NSE")
		Canvas.configure (yscrollcommand = CanvasScrollbar.set)
		Canvas.bind ("<Configure>", lambda e: Canvas.itemconfigure (Canvas.create_window (0, 0, window = InnerFrame, anchor = "nw", width = Canvas.winfo_width ())))
		
		return Canvas, InnerFrame
	
	
	
	@staticmethod
	def Frame (Parent, BGColor = Theme.BGColor, Row = 0, Column = 0, PadX = Theme.PadX, PadY = Theme.PadY, Sticky = "NSEW", RowSpan = None, ColumnSpan = None, Packed = False): # This is used for specific canvas content
		Frame = tk.Frame (Parent, bg = BGColor)
		if Packed == True:
			Frame.pack (side = "top", fill = "both", expand = True)
			Frame.columnconfigure (0, weight = 1)
			Frame.rowconfigure (0, weight = 1)
		else:
			Frame.grid (row = Row, column = Column, padx = PadX, pady = PadY, sticky = Sticky, rowspan = RowSpan, columnspan = ColumnSpan)
		return Frame
	
	
	
	@staticmethod
	def Entry (Parent, Row, Column, Sticky, Text = None, Width = 30, PadX = Theme.PadX, PadY = Theme.PadY, Show = "", Justify = "left", TooltipLabel = None, TooltipText = ""):
		Entry = tk.Entry (Parent, font = (Theme.Font, Theme.TextSize), justify = Justify, show = Show, width = Width, bg = Theme.UserInputBG, fg = Theme.UserInputText, insertbackground = Theme.CursorColor, borderwidth = 0, highlightbackground = Theme.BGColor, selectbackground = Theme.UserInputText, selectforeground = Theme.UserInputBG, disabledbackground = Theme.BGColor, disabledforeground = Theme.SmallText)
		if Text != None:
			Entry.insert (0, Text)
		Entry.grid (row = Row, column = Column, padx = PadX, pady = PadY, sticky = Sticky)
		if TooltipLabel != None:
			Entry.Tooltip = None
			Entry.Tooltip = Tooltip (TooltipLabel, TooltipText)
			Entry.bind ("<Enter>", Entry.Tooltip.ShowTooltip)
			Entry.bind ("<Leave>", Entry.Tooltip.HideTooltip)
		return Entry
		""" Color related arguments for tk.Entry() / tk.Text
		bg: sets the background color of the widget.
		fg: sets the foreground (text) color of the widget.
		disabledbackground: sets the background color of the widget when it is disabled.
		disabledforeground: sets the foreground (text) color of the widget when it is disabled.
		highlightbackground: sets the background color of the widget's highlight region.
		highlightcolor: sets the color of the widget's highlight border.
		selectbackground: sets the background color of the selected text in the widget.
		selectforeground: sets the foreground color of the selected text in the widget.
		insertbackground: sets the color of the insertion cursor in the widget.
		"""
	
	
	
	@staticmethod
	def Label (Parent, Row, Column, Sticky, Text, BGColor, TextColor = Theme.Text, TextSize = Theme.TextSize, Anchor = None, Width = 30, PadX = Theme.PadX, PadY = Theme.PadY, Height = None):
		Label = tk.Label (Parent, text = Text, font = (Theme.Font, TextSize), anchor = Anchor, justify = 'left', bg = BGColor, fg = TextColor, width = Width, height = Height)
		Label.grid (row = Row, column = Column, padx = PadX, pady = PadY, sticky = Sticky)
		return Label
	
	
	
	@staticmethod
	def ImageLabel (Parent, Row, Column, Sticky, Image, BGColor = Theme.BGColor, PadX = Theme.PadX, PadY = Theme.PadY, Command = None):
		ImageLabel = tk.Label (Parent, image = Image, bg = BGColor, fg = Theme.Error)
		ImageLabel.grid (row = Row, column = Column, padx = PadX, pady = PadY, sticky = Sticky)
		if Command != None:
			ImageLabel.bind ("<Button-1>", lambda e: Command ())
		return ImageLabel
	
	
	@staticmethod
	def Button (Parent, Row, Column, Sticky, Text, Command, ArgList = None, Width = 4, Height = 1, PadX = Theme.PadX, PadY = Theme.PadY, TooltipLabel = None, TooltipText = ""):
		if ArgList == None:
			Button = tk.Button (Parent, text = Text, font = (Theme.Font, Theme.TextSize), command = Command, bg = Theme.ButtonBG, fg = Theme.ButtonText, activebackground = Theme.ActiveButtonBG, activeforeground = Theme.ActiveButtonText, borderwidth = 0, highlightthickness = 0, relief = "flat", width = Width, height = Height)
		else:
			Button = tk.Button (Parent, text = Text, font = (Theme.Font, Theme.TextSize), command = lambda: Command (ArgList), bg = Theme.ButtonBG, fg = Theme.ButtonText, activebackground = Theme.ActiveButtonBG, activeforeground = Theme.ActiveButtonText, borderwidth = 0, highlightthickness = 0, relief = "flat", width = Width, height = Height)
		Button.configure (disabledforeground = Theme.SmallText) # This one only seems to works when configured...
		Button.grid (row = Row, column = Column, padx = PadX, pady = PadY, sticky = Sticky)
		if TooltipLabel != None:
			Button.Tooltip = None
			Button.Tooltip = Tooltip (TooltipLabel, TooltipText)
			Button.bind ("<Enter>", Button.Tooltip.ShowTooltip)
			Button.bind ("<Leave>", Button.Tooltip.HideTooltip)
		return Button
	
	
	
	@staticmethod
	def CheckButton (Parent, Row, Column, Sticky, Text, BoolVar, Command, Width = 5, Height = 1, PadX = Theme.PadX, PadY = Theme.PadY, TooltipLabel = None, TooltipText = ""): # This is smaler then other buttons, make sure to set sticky to "SN", and PadY to 0 to make it the same height as other buttons.
		CheckButton = tk.Checkbutton (Parent, text = Text, font = (Theme.Font, Theme.TextSize), anchor = "w", variable = BoolVar, command = Command, bg = Theme.ButtonBG, fg = Theme.ButtonText, activebackground = Theme.ActiveButtonBG, activeforeground = Theme.ActiveButtonText, borderwidth = 0, highlightthickness = 0, disabledforeground = Theme.SmallText, relief = "flat", indicatoron = True, selectcolor = Theme.PromptBG, width = Width, height = Height)
		CheckButton.grid (row = Row, column = Column, padx = PadX, pady = PadY, sticky = Sticky)
		if TooltipLabel != None:
			CheckButton.Tooltip = None
			CheckButton.Tooltip = Tooltip (TooltipLabel, TooltipText)
			CheckButton.bind ("<Enter>", CheckButton.Tooltip.ShowTooltip)
			CheckButton.bind ("<Leave>", CheckButton.Tooltip.HideTooltip)
		return CheckButton
	
	
	
	def RadioButton (Parent, Row, Column, Sticky, Text, StrVar, Value, Default = False, Width = 5, Height = 1, PadX = Theme.PadX, PadY = Theme.PadY, TooltipLabel = None, TooltipText = ""):
		RadioButton = tk.Radiobutton (Parent, text = Text, font = (Theme.Font, Theme.TextSize), anchor = "w", variable = StrVar, value = Value, bg = Theme.ButtonBG, fg = Theme.ButtonText, activebackground = Theme.ActiveButtonBG, activeforeground = Theme.ActiveButtonText, borderwidth = 0, highlightthickness = 0, disabledforeground = Theme.SmallText, relief = "flat", width = Width, height = Height)
		RadioButton.grid (row = Row, column = Column, padx = PadX, pady = PadY, sticky = Sticky)
		if Default == True:
			StrVar.set (Value)
		if TooltipLabel != None:
			RadioButton.Tooltip = None
			RadioButton.Tooltip = Tooltip (TooltipLabel, TooltipText)
			RadioButton.bind ("<Enter>", RadioButton.Tooltip.ShowTooltip)
			RadioButton.bind ("<Leave>", RadioButton.Tooltip.HideTooltip)
		return RadioButton
	
	
	
	@staticmethod
	def ImageButton (Parent, Row, Column, Sticky, Img, Command, ArgList = None, Width = 30, Height = 1, PadX = Theme.PadX, PadY = Theme.PadY, TooltipLabel = None, TooltipText = ""):
		if ArgList == None:
			ImageButton = tk.Button (Parent, command = Command, bg = Theme.ButtonBG, activebackground = Theme.ActiveButtonBG, borderwidth = 0, highlightthickness = 0, relief = "flat", width = Width, height = Height, compound = tk.CENTER)
		else:
			ImageButton = tk.Button (Parent, command = lambda: Command (ArgList), bg = Theme.ButtonBG, activebackground = Theme.ActiveButtonBG, borderwidth = 0, highlightthickness = 0, relief = "flat", width = Width, height = Height, compound = tk.CENTER)
		ImageButton.Image = None
		ImageButton.Image = ImageTk.PhotoImage (Image.open (io.BytesIO (cairosvg.svg2png (bytestring = open(Img, "rb").read (), scale = 0.32))))
		ImageButton.configure (image = ImageButton.Image, disabledforeground = Theme.SmallText) # This one only seems to works when configured...
		ImageButton.grid (row = Row, column = Column, padx = PadX, pady = PadY, sticky = Sticky)
		if TooltipLabel != None:
			ImageButton.Tooltip = None
			ImageButton.Tooltip = Tooltip (TooltipLabel, TooltipText)
			ImageButton.bind ("<Enter>", ImageButton.Tooltip.ShowTooltip)
			ImageButton.bind ("<Leave>", ImageButton.Tooltip.HideTooltip)
		return ImageButton
	
	
	
	@staticmethod
	def TextBox (Parent, Row, Column, PadX = Theme.PadX, PadY = Theme.PadY, Sticky = None, Height = 3, Text = None, Wrap = "word", TooltipLabel = None, TooltipText = ""):
		Frame = tk.Frame (Parent, bg = Theme.BGColor)
		Frame.grid (row = Row, column = Column, padx = PadX, pady = PadY, sticky = Sticky)
		Frame.columnconfigure (0, weight = 1)
		Frame.rowconfigure (0, weight = 1)
		ScrollX = tk.Scrollbar (Frame, orient = "horizontal", bg = Theme.BGColor, activebackground = Theme.ActiveButtonBG)
		ScrollX.pack (side = tk.BOTTOM, fill = tk.X)
		ScrollY = tk.Scrollbar (Frame, orient = "vertical", bg = Theme.BGColor, activebackground = Theme.ActiveButtonBG)
		ScrollY.pack (side = tk.RIGHT, fill = tk.Y)
		TextBox = tk.Text (Frame, font = (Theme.Font, Theme.TextSize), wrap = Wrap, height = Height, bg = Theme.UserInputBG, fg = Theme.UserInputText, insertbackground = Theme.CursorColor, borderwidth = 0, highlightbackground = Theme.BGColor, selectbackground = Theme.UserInputText, selectforeground = Theme.UserInputBG)
		TextBox.pack (side = tk.LEFT, fill = tk.BOTH, expand = True)
		TextBox.config (yscrollcommand = ScrollY.set, xscrollcommand = ScrollX.set)
		if Text != None:
			TextBox.insert ('end', Text)
		ScrollX.config (command = TextBox.xview)
		ScrollY.config (command = TextBox.yview)
		if TooltipLabel != None:
			TextBox.Tooltip = None
			TextBox.Tooltip = Tooltip (TooltipLabel, TooltipText)
			TextBox.bind ("<Enter>", TextBox.Tooltip.ShowTooltip)
			TextBox.bind ("<Leave>", TextBox.Tooltip.HideTooltip)
		return Frame, ScrollX, ScrollY, TextBox
	
	
	
	def TitleFrame (self, Parent, Row, Column, Command = None):
		self.Title = tk.Frame (Parent, bg = Theme.BGColor)
		self.Title.grid (row = Row, column = Column, padx = Theme.PadX, pady = Theme.PadY * 2, sticky = "N")
		self.Title.columnconfigure (0, weight = 1)
		self.Title.rowconfigure (0, weight = 1)
		# self. is important for self.OSRCLogo otherwise the data is discarded before displaying so you get no error but no image either!
		self.OSRCLogo = ImageTk.PhotoImage (Image.open (io.BytesIO (cairosvg.svg2png (bytestring = open (self.SVGFile_OSRCLogo, "rb").read (), scale = 1.2)))) # Either use: "scale = 1" OR "output_width = 150, output_height = 150"
		Logo = tk.Label (self.Title, image = self.OSRCLogo, bg = Theme.BGColor, fg = Theme.Error)
		Logo.grid (row = 0, column = 0, sticky = "NSEW")
		if Command != None:
			Logo.bind ("<Button-1>", lambda e: Command ())
		TextFrame = tk.Frame (self.Title, bg = Theme.BGColor)
		TextFrame.grid (row = 0, column = 1, sticky = "NSEW")
		TextFrame.columnconfigure (0, weight = 1)
		TextFrame.rowconfigure (0, weight = 1)
		Label = tk.Label (TextFrame, text = "HexaPA", font = (Theme.Font, 42, 'bold'), bg = Theme.BGColor, fg = Theme.Text)
		Label.grid (row = 0, column = 0, padx = 25, sticky = "EW")
		Label = tk.Label (TextFrame, text = "Productivity Accelerator", font = (Theme.Font, Theme.SmallTextSize * 2 - 2, 'bold'), bg = Theme.BGColor, fg = Theme.Text)
		Label.grid (row = 1, column = 0, padx = 25, sticky = "EW")
		if Command != None:
			Label.bind ("<Button-1>", lambda e: Command ())
		Text = "License: BSD 3-Clause License\nCopyright (c) 2023, Tibor Áser Veres\nAll rights reserved."
		Label_Credits = tk.Label (TextFrame, text = Text, font = (Theme.Font, Theme.TextSize), bg = Theme.BGColor, fg = Theme.SmallText)
		Label_Credits.grid (row = 2, column = 0, padx = 25, sticky = "EW")
		if Command != None:
			Label_Credits.bind ("<Button-1>", lambda e: Command ())
