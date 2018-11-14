# -*- coding: utf-8 -*- 


# solving errors: 
# - path_min /  path_add / path_switch are given a full path string, replace those by their respective variables: path_min,path_add,path_switch
# - Spacers have changed resulting in an error: replace..Add() with simply Add()

import wx
import wx.xrc
import wx.richtext
import os

datadir = os.getenv("LOCALAPPDATA")
dir0 = datadir+r"\FlashBook"
dir7 = dir0 + r"\resources"
path_add = os.path.join(dir7,"add.png")
path_min = os.path.join(dir7,"min.png")
path_switch = os.path.join(dir7,"repeat.png")


###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class MyFrame
###########################################################################

class MyFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FlashBook", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menuOpen = wx.Menu()
		self.m_menuItemFlashbook = wx.MenuItem( self.m_menuOpen, wx.ID_ANY, u"Flashbook folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuOpen.Append( self.m_menuItemFlashbook )
		
		self.m_menuPDFfolder = wx.MenuItem( self.m_menuOpen, wx.ID_ANY, u"PDF-notes folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuOpen.Append( self.m_menuPDFfolder )
		
		self.m_menuItemBackToMain = wx.MenuItem( self.m_menuOpen, wx.ID_ANY, u"Return to main menu", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuOpen.Append( self.m_menuItemBackToMain )
		
		self.m_menubar1.Append( self.m_menuOpen, u"Open" ) 
		
		self.m_menu2 = wx.Menu()
		self.m_menuHelp = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"How to use ...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuHelp )
		
		self.m_menubar1.Append( self.m_menu2, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel0 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel0.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer37 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer37.Add( ( 100, 0), 0, wx.EXPAND, 5 )
		
		bSizer71 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer71.Add( ( 100, 100), 0, 0, 5 )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		gSizer1.SetMinSize( wx.Size( 700,-1 ) ) 
		bSizer33 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText9 = wx.StaticText( self.panel0, wx.ID_ANY, u"Flashbook", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		self.m_staticText9.SetFont( wx.Font( 20, 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer33.Add( self.m_staticText9, 0, wx.ALL, 0 )
		
		self.m_staticText91 = wx.StaticText( self.panel0, wx.ID_ANY, u"Read a PDF that has been converted to jpg\nand make flashcards / notes while you read", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91.Wrap( -1 )
		self.m_staticText91.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer33.Add( self.m_staticText91, 0, wx.ALL, 0 )
		
		
		gSizer1.Add( bSizer33, 1, wx.EXPAND, 5 )
		
		self.m_OpenFlashbook = wx.BitmapButton( self.panel0, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK,  ), wx.DefaultPosition, wx.Size( 110,110 ), wx.BU_AUTODRAW )
		gSizer1.Add( self.m_OpenFlashbook, 0, wx.ALL, 0 )
		
		bSizer34 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText10 = wx.StaticText( self.panel0, wx.ID_ANY, u"Flashcard", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		self.m_staticText10.SetFont( wx.Font( 20, 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer34.Add( self.m_staticText10, 0, wx.ALL, 0 )
		
		self.m_staticText101 = wx.StaticText( self.panel0, wx.ID_ANY, u"Study the notes you took, either as flashcards\nor just as notes. ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText101.Wrap( -1 )
		self.m_staticText101.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer34.Add( self.m_staticText101, 0, wx.ALL, 0 )
		
		
		gSizer1.Add( bSizer34, 1, wx.EXPAND, 5 )
		
		self.m_OpenFlashcard = wx.BitmapButton( self.panel0, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 110,110 ), wx.BU_AUTODRAW )
		self.m_OpenFlashcard.SetDefault() 
		gSizer1.Add( self.m_OpenFlashcard, 0, wx.ALL, 0 )
		
		bSizer35 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText11 = wx.StaticText( self.panel0, wx.ID_ANY, u"Print", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		self.m_staticText11.SetFont( wx.Font( 20, 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer35.Add( self.m_staticText11, 0, wx.ALL, 0 )
		
		self.m_staticText111 = wx.StaticText( self.panel0, wx.ID_ANY, u"combines all the flashcards and saves them\nas a pdf. Includes both Question and Answer.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )
		self.m_staticText111.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer35.Add( self.m_staticText111, 0, wx.ALL, 0 )
		
		
		gSizer1.Add( bSizer35, 1, wx.EXPAND, 5 )
		
		self.m_OpenPrint = wx.BitmapButton( self.panel0, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 110,110 ), wx.BU_AUTODRAW )
		self.m_OpenPrint.SetDefault() 
		gSizer1.Add( self.m_OpenPrint, 0, wx.ALL, 0 )
		
		
		bSizer71.Add( gSizer1, 0, 0, 5 )
		
		
		bSizer37.Add( bSizer71, 1, wx.EXPAND, 5 )
		
		
		self.panel0.SetSizer( bSizer37 )
		self.panel0.Layout()
		bSizer37.Fit( self.panel0 )
		bSizer7.Add( self.panel0, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel11 = wx.Panel( self.panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel11.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_toolBar1 = wx.ToolBar( self.panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_dirPicker11 = wx.DirPickerCtrl( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar1.AddControl( self.m_dirPicker11 )
		self.m_toolPlus11 = self.m_toolBar1.AddTool( wx.ID_ANY, u"plus", wx.Bitmap( path_add, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolMin11 = self.m_toolBar1.AddTool( wx.ID_ANY, u"min", wx.Bitmap( path_min, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_Zoom11 = wx.TextCtrl( self.m_toolBar1, wx.ID_ANY, u"100%", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_toolBar1.AddControl( self.m_Zoom11 )
		self.m_toolBack11 = self.m_toolBar1.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_BACK,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolNext11 = self.m_toolBar1.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_staticText3 = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u"Page: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		self.m_toolBar1.AddControl( self.m_staticText3 )
		self.m_CurrentPage11 = wx.TextCtrl( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_CENTRE )
		self.m_CurrentPage11.SetMinSize( wx.Size( 10,-1 ) )
		self.m_CurrentPage11.SetMaxSize( wx.Size( 10,-1 ) )
		
		self.m_toolBar1.AddControl( self.m_CurrentPage11 )
		self.m_staticText6 = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u" of ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_toolBar1.AddControl( self.m_staticText6 )
		self.m_TotalPages11 = wx.TextCtrl( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_TotalPages11.SetMinSize( wx.Size( 20,-1 ) )
		self.m_TotalPages11.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar1.AddControl( self.m_TotalPages11 )
		self.m_TotalPage = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u"      Show Selections  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_TotalPage.Wrap( -1 )
		self.m_toolBar1.AddControl( self.m_TotalPage )
		self.m_checkBox11 = wx.CheckBox( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox11.SetValue(True) 
		self.m_toolBar1.AddControl( self.m_checkBox11 )
		self.m_staticText5 = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u"      Cross-hair cursor   ", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_toolBar1.AddControl( self.m_staticText5 )
		self.m_checkBoxCursor11 = wx.CheckBox( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_toolBar1.AddControl( self.m_checkBoxCursor11 )
		self.m_toolBar1.Realize() 
		
		bSizer2.Add( self.m_toolBar1, 0, wx.ALIGN_CENTER|wx.EXPAND, 0 )
		
		self.m_staticline2 = wx.StaticLine( self.panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		self.m_staticline2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer2.Add( self.m_staticline2, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.m_panel15 = wx.Panel( self.panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer46 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_scrolledWindow1 = wx.ScrolledWindow( self.m_panel15, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel16 = wx.Panel( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel16.Enable( False )
		
		bSizer5.Add( self.m_panel16, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_bitmapScroll = wx.StaticBitmap( self.m_scrolledWindow1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
		bSizer5.Add( self.m_bitmapScroll, 0, wx.ALL, 0 )
		
		self.m_panel17 = wx.Panel( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5.Add( self.m_panel17, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_scrolledWindow1.SetSizer( bSizer5 )
		self.m_scrolledWindow1.Layout()
		bSizer5.Fit( self.m_scrolledWindow1 )
		bSizer46.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_panel15.SetSizer( bSizer46 )
		self.m_panel15.Layout()
		bSizer46.Fit( self.m_panel15 )
		bSizer2.Add( self.m_panel15, 1, wx.ALL|wx.EXPAND, 0 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_textCtrl1 = wx.TextCtrl( self.panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		self.m_textCtrl1.SetFont( wx.Font( 10, 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer3.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self.panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl2.SetMinSize( wx.Size( 400,-1 ) )
		
		bSizer3.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
		
		self.m_enterselection = wx.Button( self.panel11, wx.ID_ANY, u"Enter Selection", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_enterselection.SetToolTip( u"shortcut: middle mouse button" )
		
		bSizer3.Add( self.m_enterselection, 0, wx.ALL, 5 )
		
		self.m_toolStitch = wx.BitmapButton( self.panel11, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 27,27 ), wx.BU_AUTODRAW )
		self.m_toolStitch.SetDefault() 
		self.m_toolStitch.SetToolTip( u"shortcut: numpad 0 / Home\ndirection in which notes are taken\ncan be used to create a mozaic" )
		
		bSizer3.Add( self.m_toolStitch, 0, wx.ALL, 5 )
		
		self.m_staticText32 = wx.StaticText( self.panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		self.m_staticText32.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText32.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		self.m_staticText32.SetToolTip( u"V is for vertical mode.\nH is for horizontal mode\nin case you want to select multiple sentences." )
		
		bSizer3.Add( self.m_staticText32, 0, wx.ALL, 10 )
		
		self.m_staticline3 = wx.StaticLine( self.panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer3.Add( self.m_staticline3, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 2000 )
		
		self.m_btnScreenshot = wx.Button( self.panel11, wx.ID_ANY, u"Import Screenshot", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_btnScreenshot, 0, wx.ALL, 5 )
		
		self.m_resetselection = wx.Button( self.panel11, wx.ID_ANY, u"Reset Selection", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_resetselection.SetToolTip( u"shortcut: right mouse button" )
		
		bSizer3.Add( self.m_resetselection, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer3, 0, wx.EXPAND, 5 )
		
		
		self.panel11.SetSizer( bSizer2 )
		self.panel11.Layout()
		bSizer2.Fit( self.panel11 )
		bSizer8.Add( self.panel11, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel12 = wx.Panel( self.panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel12.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_toolBar2 = wx.ToolBar( self.panel12, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_dirPicker12 = wx.DirPickerCtrl( self.m_toolBar2, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar2.AddControl( self.m_dirPicker12 )
		self.m_toolPlus12 = self.m_toolBar2.AddTool( wx.ID_ANY, u"plus", wx.Bitmap( path_add, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolMin12 = self.m_toolBar2.AddTool( wx.ID_ANY, u"min", wx.Bitmap( path_min, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_Zoom12 = wx.TextCtrl( self.m_toolBar2, wx.ID_ANY, u"100%", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_toolBar2.AddControl( self.m_Zoom12 )
		self.m_toolBack12 = self.m_toolBar2.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_BACK,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolNext12 = self.m_toolBar2.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_staticText31 = wx.StaticText( self.m_toolBar2, wx.ID_ANY, u"Page: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		self.m_toolBar2.AddControl( self.m_staticText31 )
		self.m_CurrentPage12 = wx.TextCtrl( self.m_toolBar2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_CENTRE )
		self.m_CurrentPage12.SetMinSize( wx.Size( 10,-1 ) )
		self.m_CurrentPage12.SetMaxSize( wx.Size( 10,-1 ) )
		
		self.m_toolBar2.AddControl( self.m_CurrentPage12 )
		self.m_staticText61 = wx.StaticText( self.m_toolBar2, wx.ID_ANY, u" of ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		self.m_toolBar2.AddControl( self.m_staticText61 )
		self.m_TotalPages12 = wx.TextCtrl( self.m_toolBar2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_TotalPages12.SetMinSize( wx.Size( 20,-1 ) )
		self.m_TotalPages12.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar2.AddControl( self.m_TotalPages12 )
		self.m_staticText41 = wx.StaticText( self.m_toolBar2, wx.ID_ANY, u"      Show Selections  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		self.m_toolBar2.AddControl( self.m_staticText41 )
		self.m_checkBox12 = wx.CheckBox( self.m_toolBar2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox12.SetValue(True) 
		self.m_toolBar2.AddControl( self.m_checkBox12 )
		self.m_staticText51 = wx.StaticText( self.m_toolBar2, wx.ID_ANY, u"      Cross-hair cursor   ", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText51.Wrap( -1 )
		self.m_toolBar2.AddControl( self.m_staticText51 )
		self.m_checkBoxCursor12 = wx.CheckBox( self.m_toolBar2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_toolBar2.AddControl( self.m_checkBoxCursor12 )
		self.m_toolBar2.Realize() 
		
		bSizer21.Add( self.m_toolBar2, 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		
		self.m_staticline21 = wx.StaticLine( self.panel12, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer21.Add( self.m_staticline21, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.m_richText12 = wx.richtext.RichTextCtrl( self.panel12, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer21.Add( self.m_richText12, 1, wx.EXPAND |wx.ALL, 10 )
		
		
		self.panel12.SetSizer( bSizer21 )
		self.panel12.Layout()
		bSizer21.Fit( self.panel12 )
		bSizer8.Add( self.panel12, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.panel1.SetSizer( bSizer8 )
		self.panel1.Layout()
		bSizer8.Fit( self.panel1 )
		bSizer7.Add( self.panel1, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer81 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel21 = wx.Panel( self.panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel21.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer211 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_toolBar3 = wx.ToolBar( self.panel21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_filePicker21 = wx.FilePickerCtrl( self.m_toolBar3, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.tex*", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar3.AddControl( self.m_filePicker21 )
		self.m_toolSwitch21 = self.m_toolBar3.AddTool( wx.ID_ANY, u"Switch", wx.Bitmap( path_switch, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_textCtrlMode = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, u"Question:", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.NO_BORDER )
		self.m_textCtrlMode.SetFont( wx.Font( 12, 70, 90, 92, False, wx.EmptyString ) )
		
		self.m_toolBar3.AddControl( self.m_textCtrlMode )
		self.m_CurrentPage21 = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_CENTRE|wx.TE_READONLY )
		self.m_CurrentPage21.SetMinSize( wx.Size( 10,-1 ) )
		self.m_CurrentPage21.SetMaxSize( wx.Size( 10,-1 ) )
		
		self.m_toolBar3.AddControl( self.m_CurrentPage21 )
		self.m_staticText611 = wx.StaticText( self.m_toolBar3, wx.ID_ANY, u" of ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText611.Wrap( -1 )
		self.m_toolBar3.AddControl( self.m_staticText611 )
		self.m_TotalPages21 = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY )
		self.m_TotalPages21.SetMinSize( wx.Size( 20,-1 ) )
		self.m_TotalPages21.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar3.AddControl( self.m_TotalPages21 )
		self.m_staticText311 = wx.StaticText( self.m_toolBar3, wx.ID_ANY, u"    Score: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText311.Wrap( -1 )
		self.m_toolBar3.AddControl( self.m_staticText311 )
		self.m_Score21 = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.NO_BORDER )
		self.m_Score21.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar3.AddControl( self.m_Score21 )
		self.m_toolPlus21 = self.m_toolBar3.AddTool( wx.ID_ANY, u"plus", wx.Bitmap( path_add, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolMin21 = self.m_toolBar3.AddTool( wx.ID_ANY, u"min", wx.Bitmap( path_min, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_Zoom21 = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, u"100%", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_toolBar3.AddControl( self.m_Zoom21 )
		self.m_toolBar3.Realize() 
		
		bSizer211.Add( self.m_toolBar3, 0, wx.ALIGN_CENTER|wx.EXPAND, 0 )
		
		self.m_staticline22 = wx.StaticLine( self.panel21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer211.Add( self.m_staticline22, 0, wx.EXPAND |wx.ALL, 3 )
		
		self.m_scrolledWindow11 = wx.ScrolledWindow( self.panel21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_scrolledWindow11.SetScrollRate( 5, 5 )
		bSizer51 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmapScroll1 = wx.StaticBitmap( self.m_scrolledWindow11, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer51.Add( self.m_bitmapScroll1, 0, wx.ALL, 5 )
		
		
		self.m_scrolledWindow11.SetSizer( bSizer51 )
		self.m_scrolledWindow11.Layout()
		bSizer51.Fit( self.m_scrolledWindow11 )
		bSizer211.Add( self.m_scrolledWindow11, 1, wx.EXPAND |wx.ALL, 0 )
		
		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_buttonCorrect = wx.Button( self.panel21, wx.ID_ANY, u"Correct", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonCorrect.SetToolTip( u"shortcut: left mouse button / left arrow key" )
		
		bSizer31.Add( self.m_buttonCorrect, 1, wx.ALL|wx.EXPAND|wx.RIGHT, 5 )
		
		self.m_buttonWrong = wx.Button( self.panel21, wx.ID_ANY, u"Wrong", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonWrong.SetToolTip( u"shortcut: right mouse click / right arrow key" )
		
		bSizer31.Add( self.m_buttonWrong, 1, wx.ALL|wx.EXPAND|wx.LEFT, 5 )
		
		
		bSizer211.Add( bSizer31, 0, wx.EXPAND, 5 )
		
		
		self.panel21.SetSizer( bSizer211 )
		self.panel21.Layout()
		bSizer211.Fit( self.panel21 )
		bSizer81.Add( self.panel21, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel22 = wx.Panel( self.panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel22.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer22 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_richText22 = wx.richtext.RichTextCtrl( self.panel22, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer22.Add( self.m_richText22, 1, wx.EXPAND |wx.ALL, 15 )
		
		
		self.panel22.SetSizer( bSizer22 )
		self.panel22.Layout()
		bSizer22.Fit( self.panel22 )
		bSizer81.Add( self.panel22, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.panel2.SetSizer( bSizer81 )
		self.panel2.Layout()
		bSizer81.Fit( self.panel2 )
		bSizer7.Add( self.panel2, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel3.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel31 = wx.Panel( self.panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel31.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		self.m_panel31.SetMaxSize( wx.Size( 400,-1 ) )
		
		bSizer30 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer30.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer23 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer23.Add( ( 0, 5), 0, wx.EXPAND, 5 )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel31, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		
		sbSizer1.SetMinSize( wx.Size( 275,-1 ) ) 
		gSizer12 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText52 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Boundary line in each \ncard between Q and A?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText52.Wrap( -1 )
		gSizer12.Add( self.m_staticText52, 0, wx.ALL, 5 )
		
		self.m_lineQA = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u" yes", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lineQA.SetValue(True) 
		gSizer12.Add( self.m_lineQA, 0, wx.ALL, 5 )
		
		self.m_staticText62 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Line Thickness", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )
		gSizer12.Add( self.m_staticText62, 0, wx.ALL, 5 )
		
		bSizer222 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_lineWqa = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lineWqa.SetMaxSize( wx.Size( 30,-1 ) )
		
		bSizer222.Add( self.m_lineWqa, 0, wx.ALL, 5 )
		
		self.m_staticText24 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"pixels", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		bSizer222.Add( self.m_staticText24, 0, wx.ALL, 5 )
		
		
		gSizer12.Add( bSizer222, 1, 0, 5 )
		
		self.m_staticText7 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Line Color", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gSizer12.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.m_colorQAline = wx.ColourPickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.Colour( 0, 0, 0 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		gSizer12.Add( self.m_colorQAline, 0, wx.ALL, 5 )
		
		
		sbSizer1.Add( gSizer12, 1, 0, 5 )
		
		self.m_staticText34 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Settings may not be applied if there are no \nAnswer cards made by the user.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText34.Wrap( -1 )
		self.m_staticText34.SetFont( wx.Font( 7, 70, 94, 90, False, wx.EmptyString ) )
		
		sbSizer1.Add( self.m_staticText34, 0, wx.ALL, 5 )
		
		
		bSizer23.Add( sbSizer1, 0, 0, 5 )
		
		
		bSizer23.Add( ( 0, 10), 0, wx.EXPAND, 5 )
		
		sbSizer11 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel31, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		
		sbSizer11.SetMinSize( wx.Size( 275,-1 ) ) 
		gSizer11 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText511 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Boundary line in each \nrow of the pdf?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText511.Wrap( -1 )
		gSizer11.Add( self.m_staticText511, 0, wx.ALL, 5 )
		
		self.m_linePDF = wx.CheckBox( sbSizer11.GetStaticBox(), wx.ID_ANY, u" yes", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_linePDF.SetValue(True) 
		gSizer11.Add( self.m_linePDF, 0, wx.ALL, 5 )
		
		self.m_staticText612 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Line Thickness", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText612.Wrap( -1 )
		gSizer11.Add( self.m_staticText612, 0, wx.ALL, 5 )
		
		bSizer221 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_lineWpdf = wx.TextCtrl( sbSizer11.GetStaticBox(), wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lineWpdf.SetMaxSize( wx.Size( 30,-1 ) )
		
		bSizer221.Add( self.m_lineWpdf, 0, wx.ALL, 5 )
		
		self.m_staticText241 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"pixels", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText241.Wrap( -1 )
		bSizer221.Add( self.m_staticText241, 0, wx.ALL, 5 )
		
		
		gSizer11.Add( bSizer221, 1, 0, 5 )
		
		self.m_staticText71 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Line Color", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )
		gSizer11.Add( self.m_staticText71, 0, wx.ALL, 5 )
		
		self.m_colorPDFline = wx.ColourPickerCtrl( sbSizer11.GetStaticBox(), wx.ID_ANY, wx.Colour( 18, 5, 250 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		gSizer11.Add( self.m_colorPDFline, 0, wx.ALL, 5 )
		
		
		sbSizer11.Add( gSizer11, 0, 0, 0 )
		
		
		bSizer23.Add( sbSizer11, 0, 0, 5 )
		
		
		bSizer23.Add( ( 0, 10), 0, wx.EXPAND, 5 )
		
		self.m_staticText33 = wx.StaticText( self.m_panel31, wx.ID_ANY, u"Fine tune image size", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )
		self.m_staticText33.SetFont( wx.Font( 8, 70, 94, 90, False, wx.EmptyString ) )
		
		bSizer23.Add( self.m_staticText33, 0, wx.ALL, 5 )
		
		self.m_sliderPDFsize = wx.Slider( self.m_panel31, wx.ID_ANY, 100, 70, 130, wx.DefaultPosition, wx.Size( 275,-1 ), wx.SL_BOTH|wx.SL_HORIZONTAL|wx.SL_LABELS )
		self.m_sliderPDFsize.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer23.Add( self.m_sliderPDFsize, 0, wx.ALL, 0 )
		
		self.m_PrintFinal = wx.Button( self.m_panel31, wx.ID_ANY, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_PrintFinal.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
		self.m_PrintFinal.SetMinSize( wx.Size( 275,-1 ) )
		self.m_PrintFinal.SetMaxSize( wx.Size( -1,30 ) )
		
		bSizer23.Add( self.m_PrintFinal, 1, wx.ALL, 0 )
		
		
		bSizer30.Add( bSizer23, 1, wx.EXPAND, 5 )
		
		
		bSizer30.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		self.m_panel31.SetSizer( bSizer30 )
		self.m_panel31.Layout()
		bSizer30.Fit( self.m_panel31 )
		bSizer26.Add( self.m_panel31, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panel32 = wx.Panel( self.panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.DOUBLE_BORDER|wx.TAB_TRAVERSAL )
		self.m_panel32.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.m_panel32.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )
		
		bSizer28 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmap3 = wx.StaticBitmap( self.m_panel32, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP_BOOK,  ), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer28.Add( self.m_bitmap3, 0, wx.ALIGN_CENTER, 10 )
		
		
		self.m_panel32.SetSizer( bSizer28 )
		self.m_panel32.Layout()
		bSizer28.Fit( self.m_panel32 )
		bSizer26.Add( self.m_panel32, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 0 )
		
		self.m_panel33 = wx.Panel( self.panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer26.Add( self.m_panel33, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.panel3.SetSizer( bSizer26 )
		self.panel3.Layout()
		bSizer26.Fit( self.panel3 )
		bSizer7.Add( self.panel3, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel4.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer32 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel18 = wx.Panel( self.panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer331 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_scrolledWindow3 = wx.ScrolledWindow( self.m_panel18, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow3.SetScrollRate( 5, 5 )
		bSizer342 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmap4 = wx.StaticBitmap( self.m_scrolledWindow3, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.DOUBLE_BORDER )
		bSizer342.Add( self.m_bitmap4, 1, wx.ALL, 0 )
		
		
		self.m_scrolledWindow3.SetSizer( bSizer342 )
		self.m_scrolledWindow3.Layout()
		bSizer342.Fit( self.m_scrolledWindow3 )
		bSizer331.Add( self.m_scrolledWindow3, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText35 = wx.StaticText( self.m_panel18, wx.ID_ANY, u"Select with left mouse button what area to select", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )
		self.m_staticText35.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 94, 90, False, wx.EmptyString ) )
		
		bSizer331.Add( self.m_staticText35, 0, wx.ALL, 5 )
		
		bSizer341 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_btnSelect = wx.Button( self.m_panel18, wx.ID_ANY, u"Undo Changes", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer341.Add( self.m_btnSelect, 0, wx.ALL, 5 )
		
		self.m_btnImportScreenshot = wx.Button( self.m_panel18, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer341.Add( self.m_btnImportScreenshot, 0, wx.ALL, 5 )
		
		
		bSizer331.Add( bSizer341, 0, wx.EXPAND, 5 )
		
		
		self.m_panel18.SetSizer( bSizer331 )
		self.m_panel18.Layout()
		bSizer331.Fit( self.m_panel18 )
		bSizer32.Add( self.m_panel18, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.panel4.SetSizer( bSizer32 )
		self.panel4.Layout()
		bSizer32.Fit( self.panel4 )
		bSizer7.Add( self.panel4, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer7 )
		self.Layout()
		bSizer7.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.m_menuItemFlashbookOnMenuSelection, id = self.m_menuItemFlashbook.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuPDFfolderOnMenuSelection, id = self.m_menuPDFfolder.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuItemBackToMainOnMenuSelection, id = self.m_menuItemBackToMain.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuHelpOnMenuSelection, id = self.m_menuHelp.GetId() )
		self.m_OpenFlashbook.Bind( wx.EVT_BUTTON, self.m_OpenFlashbookOnButtonClick )
		self.m_OpenFlashcard.Bind( wx.EVT_BUTTON, self.m_OpenFlashcardOnButtonClick )
		self.m_OpenPrint.Bind( wx.EVT_BUTTON, self.m_OpenPrintOnButtonClick )
		self.m_dirPicker11.Bind( wx.EVT_DIRPICKER_CHANGED, self.m_dirPicker11OnDirChanged )
		self.Bind( wx.EVT_TOOL, self.m_toolPlus11OnToolClicked, id = self.m_toolPlus11.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolMin11OnToolClicked, id = self.m_toolMin11.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolBack11OnToolClicked, id = self.m_toolBack11.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolNext11OnToolClicked, id = self.m_toolNext11.GetId() )
		self.m_CurrentPage11.Bind( wx.EVT_KEY_DOWN, self.m_CurrentPage11OnKeyDown )
		self.m_CurrentPage11.Bind( wx.EVT_KEY_UP, self.m_CurrentPage11OnKeyUp )
		self.m_CurrentPage11.Bind( wx.EVT_TEXT, self.m_CurrentPage11OnText )
		self.m_checkBox11.Bind( wx.EVT_CHECKBOX, self.m_checkBox11OnCheckBox )
		self.m_checkBoxCursor11.Bind( wx.EVT_CHECKBOX, self.m_checkBoxCursor11OnCheckBox )
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
		self.m_textCtrl2.Bind( wx.EVT_ENTER_WINDOW, self.m_textCtrl2OnEnterWindow )
		self.m_textCtrl2.Bind( wx.EVT_LEAVE_WINDOW, self.m_textCtrl2OnLeaveWindow )
		self.m_enterselection.Bind( wx.EVT_BUTTON, self.m_enterselectionOnButtonClick )
		self.m_toolStitch.Bind( wx.EVT_BUTTON, self.m_toolStitchOnButtonClick )
		self.m_btnScreenshot.Bind( wx.EVT_BUTTON, self.m_btnScreenshotOnButtonClick )
		self.m_resetselection.Bind( wx.EVT_BUTTON, self.m_resetselectionOnButtonClick )
		self.m_dirPicker12.Bind( wx.EVT_DIRPICKER_CHANGED, self.m_dirPicker12OnDirChanged )
		self.Bind( wx.EVT_TOOL, self.m_toolPlus12OnToolClicked, id = self.m_toolPlus12.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolMin12OnToolClicked, id = self.m_toolMin12.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolBack12OnToolClicked, id = self.m_toolBack12.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolNext12OnToolClicked, id = self.m_toolNext12.GetId() )
		self.m_CurrentPage12.Bind( wx.EVT_KEY_DOWN, self.m_CurrentPage2OnKeyDown )
		self.m_CurrentPage12.Bind( wx.EVT_KEY_UP, self.m_CurrentPage2OnKeyUp )
		self.m_CurrentPage12.Bind( wx.EVT_TEXT, self.m_CurrentPage12OnText )
		self.m_checkBox12.Bind( wx.EVT_CHECKBOX, self.m_checkBox12OnCheckBox )
		self.m_checkBoxCursor12.Bind( wx.EVT_CHECKBOX, self.m_checkBoxCursor12OnCheckBox )
		self.m_richText12.Bind( wx.EVT_LEFT_DOWN, self.m_richText12OnLeftDown )
		self.m_filePicker21.Bind( wx.EVT_FILEPICKER_CHANGED, self.m_filePicker21OnFileChanged )
		self.Bind( wx.EVT_TOOL, self.m_toolSwitch21OnToolClicked, id = self.m_toolSwitch21.GetId() )
		self.m_CurrentPage21.Bind( wx.EVT_KEY_DOWN, self.m_CurrentPage21OnKeyDown )
		self.m_CurrentPage21.Bind( wx.EVT_KEY_UP, self.m_CurrentPage21OnKeyUp )
		self.m_CurrentPage21.Bind( wx.EVT_TEXT, self.m_CurrentPage21OnText )
		self.Bind( wx.EVT_TOOL, self.m_toolPlus21OnToolClicked, id = self.m_toolPlus21.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolMin21OnToolClicked, id = self.m_toolMin21.GetId() )
		self.m_bitmapScroll1.Bind( wx.EVT_LEFT_DOWN, self.m_bitmapScroll1OnLeftDown )
		self.m_bitmapScroll1.Bind( wx.EVT_LEFT_UP, self.m_bitmapScroll1OnLeftUp )
		self.m_bitmapScroll1.Bind( wx.EVT_MOTION, self.m_bitmapScroll1OnMotion )
		self.m_bitmapScroll1.Bind( wx.EVT_LEFT_DOWN, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_LEFT_UP, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MIDDLE_DOWN, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MIDDLE_UP, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_RIGHT_DOWN, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_RIGHT_UP, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MOTION, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_LEFT_DCLICK, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MIDDLE_DCLICK, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_RIGHT_DCLICK, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_LEAVE_WINDOW, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_ENTER_WINDOW, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MOUSEWHEEL, self.m_bitmapScroll1OnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MOUSEWHEEL, self.m_bitmapScroll1OnMouseWheel )
		self.m_bitmapScroll1.Bind( wx.EVT_RIGHT_DOWN, self.m_bitmapScrollOnRightDown )
		self.m_bitmapScroll1.Bind( wx.EVT_RIGHT_UP, self.m_bitmapScroll1OnRightUp )
		self.m_buttonCorrect.Bind( wx.EVT_BUTTON, self.m_buttonCorrectOnButtonClick )
		self.m_buttonWrong.Bind( wx.EVT_BUTTON, self.m_buttonWrongOnButtonClick )
		self.m_richText22.Bind( wx.EVT_LEFT_DOWN, self.m_richText22OnLeftDown )
		self.m_lineQA.Bind( wx.EVT_CHECKBOX, self.m_lineQAOnCheckBox )
		self.m_lineQA.Bind( wx.EVT_LEFT_UP, self.m_lineQAOnLeftUp )
		self.m_lineWqa.Bind( wx.EVT_TEXT, self.m_lineWqaOnText )
		self.m_lineWqa.Bind( wx.EVT_TEXT_ENTER, self.m_lineWqaOnTextEnter )
		self.m_colorQAline.Bind( wx.EVT_COLOURPICKER_CHANGED, self.m_colorQAlineOnColourChanged )
		self.m_linePDF.Bind( wx.EVT_CHECKBOX, self.m_linePDFOnCheckBox )
		self.m_linePDF.Bind( wx.EVT_LEFT_UP, self.m_linePDFOnLeftUp )
		self.m_lineWpdf.Bind( wx.EVT_TEXT, self.m_lineWpdfOnText )
		self.m_lineWpdf.Bind( wx.EVT_TEXT_ENTER, self.m_lineWpdfOnTextEnter )
		self.m_colorPDFline.Bind( wx.EVT_COLOURPICKER_CHANGED, self.m_colorPDFlineOnColourChanged )
		self.m_sliderPDFsize.Bind( wx.EVT_KEY_UP, self.m_sliderPDFsizeOnKeyUp )
		self.m_sliderPDFsize.Bind( wx.EVT_SCROLL_CHANGED, self.m_sliderPDFsizeOnScrollChanged )
		self.m_PrintFinal.Bind( wx.EVT_BUTTON, self.m_PrintFinalOnButtonClick )
		self.m_bitmap4.Bind( wx.EVT_LEFT_DOWN, self.m_bitmap4OnLeftDown )
		self.m_bitmap4.Bind( wx.EVT_LEFT_UP, self.m_bitmap4OnLeftUp )
		self.m_btnSelect.Bind( wx.EVT_BUTTON, self.m_btnSelectOnButtonClick )
		self.m_btnImportScreenshot.Bind( wx.EVT_BUTTON, self.m_btnImportScreenshotOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_menuItemFlashbookOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuPDFfolderOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuItemBackToMainOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuHelpOnMenuSelection( self, event ):
		event.Skip()
	
	def m_OpenFlashbookOnButtonClick( self, event ):
		event.Skip()
	
	def m_OpenFlashcardOnButtonClick( self, event ):
		event.Skip()
	
	def m_OpenPrintOnButtonClick( self, event ):
		event.Skip()
	
	def m_dirPicker11OnDirChanged( self, event ):
		event.Skip()
	
	def m_toolPlus11OnToolClicked( self, event ):
		event.Skip()
	
	def m_toolMin11OnToolClicked( self, event ):
		event.Skip()
	
	def m_toolBack11OnToolClicked( self, event ):
		event.Skip()
	
	def m_toolNext11OnToolClicked( self, event ):
		event.Skip()
	
	def m_CurrentPage11OnKeyDown( self, event ):
		event.Skip()
	
	def m_CurrentPage11OnKeyUp( self, event ):
		event.Skip()
	
	def m_CurrentPage11OnText( self, event ):
		event.Skip()
	
	def m_checkBox11OnCheckBox( self, event ):
		event.Skip()
	
	def m_checkBoxCursor11OnCheckBox( self, event ):
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
	
	def m_textCtrl2OnEnterWindow( self, event ):
		event.Skip()
	
	def m_textCtrl2OnLeaveWindow( self, event ):
		event.Skip()
	
	def m_enterselectionOnButtonClick( self, event ):
		event.Skip()
	
	def m_toolStitchOnButtonClick( self, event ):
		event.Skip()
	
	def m_btnScreenshotOnButtonClick( self, event ):
		event.Skip()
	
	def m_resetselectionOnButtonClick( self, event ):
		event.Skip()
	
	def m_dirPicker12OnDirChanged( self, event ):
		event.Skip()
	
	def m_toolPlus12OnToolClicked( self, event ):
		event.Skip()
	
	def m_toolMin12OnToolClicked( self, event ):
		event.Skip()
	
	def m_toolBack12OnToolClicked( self, event ):
		event.Skip()
	
	def m_toolNext12OnToolClicked( self, event ):
		event.Skip()
	
	def m_CurrentPage2OnKeyDown( self, event ):
		event.Skip()
	
	def m_CurrentPage2OnKeyUp( self, event ):
		event.Skip()
	
	def m_CurrentPage12OnText( self, event ):
		event.Skip()
	
	def m_checkBox12OnCheckBox( self, event ):
		event.Skip()
	
	def m_checkBoxCursor12OnCheckBox( self, event ):
		event.Skip()
	
	def m_richText12OnLeftDown( self, event ):
		event.Skip()
	
	def m_filePicker21OnFileChanged( self, event ):
		event.Skip()
	
	def m_toolSwitch21OnToolClicked( self, event ):
		event.Skip()
	
	def m_CurrentPage21OnKeyDown( self, event ):
		event.Skip()
	
	def m_CurrentPage21OnKeyUp( self, event ):
		event.Skip()
	
	def m_CurrentPage21OnText( self, event ):
		event.Skip()
	
	def m_toolPlus21OnToolClicked( self, event ):
		event.Skip()
	
	def m_toolMin21OnToolClicked( self, event ):
		event.Skip()
	
	def m_bitmapScroll1OnLeftDown( self, event ):
		event.Skip()
	
	def m_bitmapScroll1OnLeftUp( self, event ):
		event.Skip()
	
	def m_bitmapScroll1OnMotion( self, event ):
		event.Skip()
	
	def m_bitmapScroll1OnMouseEvents( self, event ):
		event.Skip()
	
	def m_bitmapScroll1OnMouseWheel( self, event ):
		event.Skip()
	
	
	def m_bitmapScroll1OnRightUp( self, event ):
		event.Skip()
	
	def m_buttonCorrectOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonWrongOnButtonClick( self, event ):
		event.Skip()
	
	def m_richText22OnLeftDown( self, event ):
		event.Skip()
	
	def m_lineQAOnCheckBox( self, event ):
		event.Skip()
	
	def m_lineQAOnLeftUp( self, event ):
		event.Skip()
	
	def m_lineWqaOnText( self, event ):
		event.Skip()
	
	def m_lineWqaOnTextEnter( self, event ):
		event.Skip()
	
	def m_colorQAlineOnColourChanged( self, event ):
		event.Skip()
	
	def m_linePDFOnCheckBox( self, event ):
		event.Skip()
	
	def m_linePDFOnLeftUp( self, event ):
		event.Skip()
	
	def m_lineWpdfOnText( self, event ):
		event.Skip()
	
	def m_lineWpdfOnTextEnter( self, event ):
		event.Skip()
	
	def m_colorPDFlineOnColourChanged( self, event ):
		event.Skip()
	
	def m_sliderPDFsizeOnKeyUp( self, event ):
		event.Skip()
	
	def m_sliderPDFsizeOnScrollChanged( self, event ):
		event.Skip()
	
	def m_PrintFinalOnButtonClick( self, event ):
		event.Skip()
	
	def m_bitmap4OnLeftDown( self, event ):
		event.Skip()
	
	def m_bitmap4OnLeftUp( self, event ):
		event.Skip()
	
	def m_btnSelectOnButtonClick( self, event ):
		event.Skip()
	
	def m_btnImportScreenshotOnButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class MyDialog
###########################################################################

class MyDialog ( wx.Dialog ):
	
	def __init__( self, parent, data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Settings", pos = wx.DefaultPosition, size = wx.Size( 349,250 ), style = wx.DEFAULT_DIALOG_STYLE )
		
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
		self.m_textCtrl11.SetMaxSize( wx.Size( 30,-1 ) )
		
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
	
	def __init__( self, parent, data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Settings", pos = wx.DefaultPosition, size = wx.Size( 349,300 ), style = wx.DEFAULT_DIALOG_STYLE )
		
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
		self.m_textCtrl11.SetMaxSize( wx.Size( 30,-1 ) )
		
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
	

