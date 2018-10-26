# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext
import os


datadir = os.getenv("LOCALAPPDATA")
dir0 = datadir+r"\FlashBook"
dir7 = dir0 + r"\resources"
path_add = os.path.join(dir7,"add.png")
path_min = os.path.join(dir7,"min.png")
path_repeat = os.path.join(dir7,"repeat.png")
path_repeat_na = os.path.join(dir7,"repeat_na.png")

###########################################################################
## Class MyFrame
###########################################################################

class MyFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FlashCard", pos = wx.DefaultPosition, size = wx.Size( 1155,646 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menuOpen = wx.Menu()
		self.m_menuItemFlashbook = wx.MenuItem( self.m_menuOpen, wx.ID_ANY, u"Open FlashBook Folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuOpen.Append( self.m_menuItemFlashbook )
		
		self.m_menubar1.Append( self.m_menuOpen, u"Open" ) 
		
		self.m_menu2 = wx.Menu()
		self.m_menuHelp = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"How to use ...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuHelp )
		
		self.m_menubar1.Append( self.m_menu2, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel0 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel1 = wx.Panel( self.panel0, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel1.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_toolBar11 = wx.ToolBar( self.panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_filePicker = wx.FilePickerCtrl( self.m_toolBar11, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.tex*", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar11.AddControl( self.m_filePicker )
		self.m_toolSwitch = self.m_toolBar11.AddTool( wx.ID_ANY, u"Switch", wx.Bitmap( path_repeat, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_textCtrlMode = wx.TextCtrl( self.m_toolBar11, wx.ID_ANY, u"Question:", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.NO_BORDER )
		self.m_toolBar11.AddControl( self.m_textCtrlMode )
		self.m_CurrentPage = wx.TextCtrl( self.m_toolBar11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_CENTRE|wx.TE_READONLY )
		self.m_CurrentPage.SetMinSize( wx.Size( 10,-1 ) )
		self.m_CurrentPage.SetMaxSize( wx.Size( 10,-1 ) )
		
		self.m_toolBar11.AddControl( self.m_CurrentPage )
		self.m_staticText61 = wx.StaticText( self.m_toolBar11, wx.ID_ANY, u" of ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		self.m_toolBar11.AddControl( self.m_staticText61 )
		self.m_TotalPages = wx.TextCtrl( self.m_toolBar11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY )
		self.m_TotalPages.SetMinSize( wx.Size( 20,-1 ) )
		self.m_TotalPages.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar11.AddControl( self.m_TotalPages )
		self.m_staticText31 = wx.StaticText( self.m_toolBar11, wx.ID_ANY, u"    Score: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		self.m_toolBar11.AddControl( self.m_staticText31 )
		self.m_Score = wx.TextCtrl( self.m_toolBar11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.NO_BORDER )
		self.m_Score.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar11.AddControl( self.m_Score )
		self.m_toolPlus1 = self.m_toolBar11.AddTool( wx.ID_ANY, u"plus", wx.Bitmap( path_add, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolMin1 = self.m_toolBar11.AddTool( wx.ID_ANY, u"min", wx.Bitmap( path_min, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_Zoom1 = wx.TextCtrl( self.m_toolBar11, wx.ID_ANY, u"100%", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_toolBar11.AddControl( self.m_Zoom1 )
		self.m_toolBar11.Realize() 
		
		bSizer21.Add( self.m_toolBar11, 0, wx.ALIGN_CENTER|wx.EXPAND, 0 )
		
		self.m_staticline2 = wx.StaticLine( self.panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer21.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_scrolledWindow1 = wx.ScrolledWindow( self.panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmapScroll = wx.StaticBitmap( self.m_scrolledWindow1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_bitmapScroll, 0, wx.ALL, 5 )
		
		
		self.m_scrolledWindow1.SetSizer( bSizer5 )
		self.m_scrolledWindow1.Layout()
		bSizer5.Fit( self.m_scrolledWindow1 )
		bSizer21.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 0 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_buttonCorrect = wx.Button( self.panel1, wx.ID_ANY, u"Correct", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_buttonCorrect, 1, wx.ALL|wx.EXPAND|wx.RIGHT, 5 )
		
		self.m_buttonWrong = wx.Button( self.panel1, wx.ID_ANY, u"Wrong", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_buttonWrong, 1, wx.ALL|wx.EXPAND|wx.LEFT, 5 )
		
		
		bSizer21.Add( bSizer3, 0, wx.EXPAND, 5 )
		
		
		self.panel1.SetSizer( bSizer21 )
		self.panel1.Layout()
		bSizer21.Fit( self.panel1 )
		bSizer8.Add( self.panel1, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel2 = wx.Panel( self.panel0, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel2.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_richText1 = wx.richtext.RichTextCtrl( self.panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer2.Add( self.m_richText1, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.panel2.SetSizer( bSizer2 )
		self.panel2.Layout()
		bSizer2.Fit( self.panel2 )
		bSizer8.Add( self.panel2, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.panel0.SetSizer( bSizer8 )
		self.panel0.Layout()
		bSizer8.Fit( self.panel0 )
		bSizer7.Add( self.panel0, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer7 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.m_menuItemFlashbookOnMenuSelection, id = self.m_menuItemFlashbook.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuHelpOnMenuSelection, id = self.m_menuHelp.GetId() )
		self.m_filePicker.Bind( wx.EVT_FILEPICKER_CHANGED, self.m_filePickerOnFileChanged )
		self.Bind( wx.EVT_TOOL, self.m_toolSwitchOnToolClicked, id = self.m_toolSwitch.GetId() )
		self.m_CurrentPage.Bind( wx.EVT_KEY_DOWN, self.m_PageCtrlOnKeyDown )
		self.m_CurrentPage.Bind( wx.EVT_KEY_UP, self.m_PageCtrlOnKeyUp )
		self.m_CurrentPage.Bind( wx.EVT_TEXT, self.m_PageCtrlOnText )
		self.Bind( wx.EVT_TOOL, self.m_toolPlusOnToolClicked, id = self.m_toolPlus1.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolMinOnToolClicked, id = self.m_toolMin1.GetId() )
		self.m_bitmapScroll.Bind( wx.EVT_LEFT_DOWN, self.m_bitmapScrollOnLeftDown )
		self.m_bitmapScroll.Bind( wx.EVT_LEFT_UP, self.m_bitmapScrollOnLeftUp )
		self.m_bitmapScroll.Bind( wx.EVT_MOTION, self.m_bitmapScrollOnMotion )
		self.m_bitmapScroll.Bind( wx.EVT_LEFT_DOWN, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_LEFT_UP, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_MIDDLE_DOWN, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_MIDDLE_UP, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_RIGHT_DOWN, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_RIGHT_UP, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_MOTION, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_LEFT_DCLICK, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_MIDDLE_DCLICK, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_RIGHT_DCLICK, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_LEAVE_WINDOW, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_ENTER_WINDOW, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_MOUSEWHEEL, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_MOUSEWHEEL, self.m_bitmapScrollOnMouseWheel )
		self.m_bitmapScroll.Bind( wx.EVT_RIGHT_DOWN, self.m_bitmapScrollOnRightDown )
		self.m_buttonCorrect.Bind( wx.EVT_BUTTON, self.m_buttonCorrectOnButtonClick )
		self.m_buttonWrong.Bind( wx.EVT_BUTTON, self.m_buttonWrongOnButtonClick )
		self.m_richText1.Bind( wx.EVT_LEFT_DOWN, self.m_richText1OnLeftDown )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_menuItemFlashbookOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuHelpOnMenuSelection( self, event ):
		event.Skip()
	
	def m_filePickerOnFileChanged( self, event ):
		event.Skip()
	
	def m_toolSwitchOnToolClicked( self, event ):
		event.Skip()
	
	def m_PageCtrlOnKeyDown( self, event ):
		event.Skip()
	
	def m_PageCtrlOnKeyUp( self, event ):
		event.Skip()
	
	def m_PageCtrlOnText( self, event ):
		event.Skip()
	
	def m_toolPlusOnToolClicked( self, event ):
		event.Skip()
	
	def m_toolMinOnToolClicked( self, event ):
		event.Skip()
	
	def m_bitmapScrollOnLeftDown( self, event ):
		event.Skip()
	
	def m_bitmapScrollOnLeftUp( self, event ):
		event.Skip()
	
	def m_bitmapScrollOnMotion( self, event ):
		event.Skip()
	
	def m_bitmapScrollOnMouseEvents( self, event ):
		event.Skip()
	
	def m_bitmapScrollOnMouseWheel( self, event ):
		event.Skip()
	
	def m_bitmapScrollOnRightDown( self, event ):
		event.Skip()
	
	def m_buttonCorrectOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonWrongOnButtonClick( self, event ):
		event.Skip()
	
	def m_richText1OnLeftDown( self, event ):
		event.Skip()
	

###########################################################################
## Class MyDialog
###########################################################################

class MyDialog ( wx.Dialog ):
	
	def __init__( self, parent,data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 349,250 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.Size( 350,250 ) )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel4.SetBackgroundColour( wx.Colour( 254, 239, 231 ) )
		
		bSizer91 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText5 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Number of questions  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		gSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.m_slider1 = wx.Slider( self.m_panel4, wx.ID_ANY, data, 1, data, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
		gSizer1.Add( self.m_slider1, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Multiplier  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		gSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.m_textCtrl11 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_textCtrl11, 0, wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Order of cards  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_radioChrono = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"Chronological", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioChrono.SetValue( True ) 
		bSizer9.Add( self.m_radioChrono, 0, wx.ALL, 5 )
		
		self.m_radioRandom = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"Random", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.m_radioRandom, 0, wx.ALL, 5 )
		
		
		gSizer1.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		
		bSizer91.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer91 )
		self.m_panel4.Layout()
		bSizer91.Fit( self.m_panel4 )
		bSizer8.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer8 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_radioChrono.Bind( wx.EVT_RADIOBUTTON, self.m_radioChronoOnRadioButton )
		self.m_radioRandom.Bind( wx.EVT_RADIOBUTTON, self.m_radioRandomOnRadioButton )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_radioChronoOnRadioButton( self, event ):
		event.Skip()
	
	def m_radioRandomOnRadioButton( self, event ):
		event.Skip()
	

###########################################################################
## Class MyDialog2
###########################################################################

class MyDialog2 ( wx.Dialog ):
	
	def __init__( self, parent,data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 349,300 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.Size( 350,300 ) )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel4.SetBackgroundColour( wx.Colour( 254, 239, 231 ) )
		
		bSizer91 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText5 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Number of questions  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		gSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.m_slider1 = wx.Slider( self.m_panel4, wx.ID_ANY, data, 1, data, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
		gSizer1.Add( self.m_slider1, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Multiplier  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		gSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.m_textCtrl11 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_textCtrl11, 0, wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Order of cards  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_radioChrono = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"Chronological", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.m_radioChrono.SetValue( True ) 
		bSizer9.Add( self.m_radioChrono, 0, wx.ALL, 5 )
		
		self.m_radioRandom = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"Random", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.m_radioRandom, 0, wx.ALL, 5 )
		
		
		gSizer1.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		self.m_staticText17 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Continue last session?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		gSizer1.Add( self.m_staticText17, 0, wx.ALL, 5 )
		
		bSizer23 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_radioYes = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"Yes", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.m_radioYes.SetValue( True ) 
		bSizer23.Add( self.m_radioYes, 0, wx.ALL, 5 )
		
		self.m_radioNo = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"No", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer23.Add( self.m_radioNo, 0, wx.ALL, 5 )
		
		
		gSizer1.Add( bSizer23, 1, wx.EXPAND, 5 )
		
		
		bSizer91.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer91 )
		self.m_panel4.Layout()
		bSizer91.Fit( self.m_panel4 )
		bSizer8.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer8 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_radioChrono.Bind( wx.EVT_RADIOBUTTON, self.m_radioChronoOnRadioButton )
		self.m_radioRandom.Bind( wx.EVT_RADIOBUTTON, self.m_radioRandomOnRadioButton )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_radioChronoOnRadioButton( self, event ):
		event.Skip()
	
	def m_radioRandomOnRadioButton( self, event ):
		event.Skip()
	

