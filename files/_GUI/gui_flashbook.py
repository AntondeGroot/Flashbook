# -*- coding: utf-8 -*- 


# solving errors: 
# - path_min /  path_add / path_switch are given a full path string, replace those by their respective variables: path_min,path_add,path_switch
# - Spacers have changed resulting in an error: replace..Add() with simply Add()

import wx
import wx.xrc
import wx.richtext
import os
from pathlib import Path

VersionNumber = 'Version 2.0.0'

basedir     = Path(os.getenv("LOCALAPPDATA"),"Flashbook")
resourcedir = str(Path(basedir ,"resources"))
path_add    = str(Path(resourcedir,"add.png"))
path_min    = str(Path(resourcedir,"min.png"))
path_switch = str(Path(resourcedir,"repeat.png"))


###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################


###########################################################################
## Class MyFrame
###########################################################################


class MyFrame ( wx.Frame ):
	
	def __init__( self, parent, data ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Flashbook", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 9, 74, 90, 92, False, "Verdana" ) )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menuOpen = wx.Menu()
		self.m_menuItemFlashbook = wx.MenuItem( self.m_menuOpen, wx.ID_ANY, u"Book PDF folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemFlashbook.SetBitmap( data[0] )
		self.m_menuOpen.Append( self.m_menuItemFlashbook )
		
		self.m_menuItemJPG = wx.MenuItem( self.m_menuOpen, wx.ID_ANY, u"Book JPG folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemJPG.SetBitmap( data[0] )
		self.m_menuOpen.Append( self.m_menuItemJPG )
		
		self.m_menuOpen.AppendSeparator()
		
		self.m_menuPDFfolder = wx.MenuItem( self.m_menuOpen, wx.ID_ANY, u"Notes PDF folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuPDFfolder.SetBitmap( data[0] )
		self.m_menuOpen.Append( self.m_menuPDFfolder )
		
		self.m_menuOpen.AppendSeparator()
		
		self.m_menuItemBackToMain = wx.MenuItem( self.m_menuOpen, wx.ID_ANY, u"Return to main menu", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemBackToMain.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_HOME,  ) )
		self.m_menuOpen.Append( self.m_menuItemBackToMain )
		
		self.m_menubar1.Append( self.m_menuOpen, u"Folders" ) 
		
		self.m_menuBooks = wx.Menu()
		self.m_menuItemConvert = wx.MenuItem( self.m_menuBooks, wx.ID_ANY, u"Convert Books", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemConvert.SetBitmap( data[1] )
		self.m_menuBooks.Append( self.m_menuItemConvert )
		
		self.m_menuBooks.AppendSeparator()
		
		self.m_menuCombineBooks = wx.MenuItem( self.m_menuBooks, wx.ID_ANY, u"Combine booknotes", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuBooks.Append( self.m_menuCombineBooks )
		
		self.m_menuNewBook = wx.MenuItem( self.m_menuBooks, wx.ID_ANY, u"Create new topic", u"Only use this to create 'books'\nwhere you only use screenshots\nas the source material.", wx.ITEM_NORMAL )
		self.m_menuBooks.Append( self.m_menuNewBook )
		
		self.m_menuAddPDF = wx.MenuItem( self.m_menuBooks, wx.ID_ANY, u"Add an extra PDF to a book", u"Only use this to create 'books'\nwhere you only use screenshots\nas the source material.", wx.ITEM_NORMAL )
		self.m_menuBooks.Append( self.m_menuAddPDF )
		
		self.m_menuBooks.AppendSeparator()
		
		self.m_menuItemDelBook = wx.MenuItem( self.m_menuBooks, wx.ID_ANY, u"Delete book", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuBooks.Append( self.m_menuItemDelBook )
		
		self.m_menubar1.Append( self.m_menuBooks, u"Books" ) 
		
		self.m_menuCards = wx.Menu()
		self.m_menuAddCard = wx.MenuItem( self.m_menuCards, wx.ID_ANY, u"Add card", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuCards.Append( self.m_menuAddCard )
		
		self.m_menuEditCard = wx.MenuItem( self.m_menuCards, wx.ID_ANY, u"Edit card", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuCards.Append( self.m_menuEditCard )
		
		self.m_menuCards.AppendSeparator()
		
		self.m_menuPreviousCard = wx.MenuItem( self.m_menuCards, wx.ID_ANY, u"See previous card", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuCards.Append( self.m_menuPreviousCard )
		
		self.m_menubar1.Append( self.m_menuCards, u"Flashcard" ) 
		
		self.m_menuHelpbar = wx.Menu()
		self.m_menuHelp = wx.MenuItem( self.m_menuHelpbar, wx.ID_ANY, u"How to use ...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuHelpbar.Append( self.m_menuHelp )
		
		self.m_menuHelpbar.AppendSeparator()
		
		self.m_menuItemAbout = wx.MenuItem( self.m_menuHelpbar, wx.ID_ANY, u"About ...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuHelpbar.Append( self.m_menuItemAbout )
		
		self.m_menubar1.Append( self.m_menuHelpbar, u"Help" ) 
		
		self.m_menuSettings = wx.Menu()
		self.m_checkBoxSelections = wx.MenuItem( self.m_menuSettings, wx.ID_ANY, u"Show selections", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menuSettings.Append( self.m_checkBoxSelections )
		self.m_checkBoxSelections.Check( True )
		
		self.m_checkBoxDebug = wx.MenuItem( self.m_menuSettings, wx.ID_ANY, u"Debug mode", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menuSettings.Append( self.m_checkBoxDebug )
		
		self.m_menuItemGraph = wx.MenuItem( self.m_menuSettings, wx.ID_ANY, u"Show stats graph", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menuSettings.Append( self.m_menuItemGraph )
		self.m_menuItemGraph.Check( True )
		
		self.m_menuSettings.AppendSeparator()
		
		self.m_menuResetSettings = wx.MenuItem( self.m_menuSettings, wx.ID_ANY, u"Reset settings", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuSettings.Append( self.m_menuResetSettings )
		
		self.m_menuResetGraph = wx.MenuItem( self.m_menuSettings, wx.ID_ANY, u"Reset graph", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuSettings.Append( self.m_menuResetGraph )
		
		self.m_menuResetLog = wx.MenuItem( self.m_menuSettings, wx.ID_ANY, u"Reset log file", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuSettings.Append( self.m_menuResetLog )
		
		self.m_menubar1.Append( self.m_menuSettings, u"Settings" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel0 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel0.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer84 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer37 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer37.Add( ( 100, 100), 0, wx.EXPAND, 5 )
		
		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer481 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer481.Add( ( 100, 100), 0, 0, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )
		
		bSizer332 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText92 = wx.StaticText( self.panel0, wx.ID_ANY, u"Flashbook", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText92.Wrap( -1 )
		self.m_staticText92.SetFont( wx.Font( 20, 74, 90, 92, False, "Verdana" ) )
		
		bSizer332.Add( self.m_staticText92, 0, wx.ALL, 0 )
		
		self.m_staticText911 = wx.StaticText( self.panel0, wx.ID_ANY, u"Read a PDF that has been converted to jpg\nand make flashcards / notes while you read", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText911.Wrap( -1 )
		self.m_staticText911.SetFont( wx.Font( 10, 74, 90, 90, False, "Verdana" ) )
		
		bSizer332.Add( self.m_staticText911, 0, wx.ALL, 0 )
		
		
		fgSizer3.Add( bSizer332, 1, wx.EXPAND, 5 )
		
		self.m_OpenFlashbook = wx.BitmapButton( self.panel0, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK,  ), wx.DefaultPosition, wx.Size( 110,110 ), wx.BU_AUTODRAW )
		fgSizer3.Add( self.m_OpenFlashbook, 0, wx.ALL, 0 )
		
		bSizer343 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText102 = wx.StaticText( self.panel0, wx.ID_ANY, u"Flashcard", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText102.Wrap( -1 )
		self.m_staticText102.SetFont( wx.Font( 20, 74, 90, 92, False, "Verdana" ) )
		
		bSizer343.Add( self.m_staticText102, 0, wx.ALL, 0 )
		
		self.m_staticText1011 = wx.StaticText( self.panel0, wx.ID_ANY, u"Study the notes you took, either as flashcards\nor just read through your notes.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1011.Wrap( -1 )
		self.m_staticText1011.SetFont( wx.Font( 10, 74, 90, 90, False, "Verdana" ) )
		
		bSizer343.Add( self.m_staticText1011, 0, wx.ALL, 0 )
		
		
		fgSizer3.Add( bSizer343, 1, wx.EXPAND, 5 )
		
		self.m_OpenFlashcard = wx.BitmapButton( self.panel0, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 110,110 ), wx.BU_AUTODRAW )
		self.m_OpenFlashcard.SetDefault() 
		fgSizer3.Add( self.m_OpenFlashcard, 0, wx.ALL, 0 )
		
		bSizer353 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText113 = wx.StaticText( self.panel0, wx.ID_ANY, u"Print", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText113.Wrap( -1 )
		self.m_staticText113.SetFont( wx.Font( 20, 74, 90, 92, False, "Verdana" ) )
		
		bSizer353.Add( self.m_staticText113, 0, wx.ALL, 0 )
		
		self.m_staticText1112 = wx.StaticText( self.panel0, wx.ID_ANY, u"Combine all the flashcards and save them\nas a PDF. You can customize the file\nand edit / delete cards by clicking on them.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1112.Wrap( -1 )
		self.m_staticText1112.SetFont( wx.Font( 10, 74, 90, 90, False, "Verdana" ) )
		
		bSizer353.Add( self.m_staticText1112, 0, wx.ALL, 0 )
		
		
		fgSizer3.Add( bSizer353, 1, wx.EXPAND, 5 )
		
		self.m_OpenPrint = wx.BitmapButton( self.panel0, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 110,110 ), wx.BU_AUTODRAW )
		self.m_OpenPrint.SetDefault() 
		fgSizer3.Add( self.m_OpenPrint, 0, wx.ALL, 0 )
		
		bSizer3521 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1121 = wx.StaticText( self.panel0, wx.ID_ANY, u"Synchronize", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1121.Wrap( -1 )
		self.m_staticText1121.SetFont( wx.Font( 20, 74, 90, 92, False, "Verdana" ) )
		
		bSizer3521.Add( self.m_staticText1121, 0, wx.ALL, 0 )
		
		self.m_staticText11111 = wx.StaticText( self.panel0, wx.ID_ANY, u"Connect two devices: e.g. your Desktop and Laptop     \nand synchronize the files on both devices.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11111.Wrap( -1 )
		self.m_staticText11111.SetFont( wx.Font( 10, 74, 90, 90, False, "Verdana" ) )
		
		bSizer3521.Add( self.m_staticText11111, 0, wx.ALL, 0 )
		
		
		fgSizer3.Add( bSizer3521, 1, wx.EXPAND, 5 )
		
		self.m_OpenTransfer = wx.BitmapButton( self.panel0, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 110,110 ), wx.BU_AUTODRAW )
		self.m_OpenTransfer.SetDefault() 
		fgSizer3.Add( self.m_OpenTransfer, 0, wx.ALL, 0 )
		
		
		bSizer481.Add( fgSizer3, 0, wx.EXPAND, 5 )
		
		
		bSizer71.Add( bSizer481, 0, wx.EXPAND, 5 )
		
		
		bSizer71.Add( ( 50, 0), 0, wx.EXPAND, 5 )
		
		bSizer471 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer471.Add( ( 100, 100), 0, wx.EXPAND, 5 )
		
		self.m_panelGraph = wx.Panel( self.panel0, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.m_panelGraph.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer49 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmapGraph = wx.StaticBitmap( self.m_panelGraph, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer49.Add( self.m_bitmapGraph, 0, wx.ALL, 0 )
		
		
		self.m_panelGraph.SetSizer( bSizer49 )
		self.m_panelGraph.Layout()
		bSizer49.Fit( self.m_panelGraph )
		bSizer471.Add( self.m_panelGraph, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		bSizer71.Add( bSizer471, 1, wx.EXPAND, 5 )
		
		
		bSizer37.Add( bSizer71, 1, wx.EXPAND, 5 )
		
		
		bSizer84.Add( bSizer37, 1, wx.EXPAND, 5 )
		
		bSizer87 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer87.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText63 = wx.StaticText( self.panel0, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText63.Wrap( -1 )
		bSizer87.Add( self.m_staticText63, 0, wx.ALL, 5 )
		
		
		bSizer84.Add( bSizer87, 0, wx.EXPAND, 5 )
		
		
		self.panel0.SetSizer( bSizer84 )
		self.panel0.Layout()
		bSizer84.Fit( self.panel0 )
		bSizer7.Add( self.panel0, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel11 = wx.Panel( self.panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel11.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_toolBar1 = wx.ToolBar( self.panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_toolPlusFB = self.m_toolBar1.AddTool( wx.ID_ANY, u"plus", wx.Bitmap( path_add, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolMinFB = self.m_toolBar1.AddTool( wx.ID_ANY, u"min", wx.Bitmap( path_min, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_ZoomFB = wx.TextCtrl( self.m_toolBar1, wx.ID_ANY, u"100%", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_ZoomFB.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		self.m_toolBar1.AddControl( self.m_ZoomFB )
		self.m_pageBackFB = self.m_toolBar1.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_BACK,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_pageNextFB = self.m_toolBar1.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_staticText3 = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u"Page: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		self.m_staticText3.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		self.m_toolBar1.AddControl( self.m_staticText3 )
		self.m_CurrentPageFB = wx.TextCtrl( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_CENTRE )
		self.m_CurrentPageFB.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_CurrentPageFB.SetMinSize( wx.Size( 10,-1 ) )
		self.m_CurrentPageFB.SetMaxSize( wx.Size( 10,-1 ) )
		
		self.m_toolBar1.AddControl( self.m_CurrentPageFB )
		self.m_staticText6 = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u" of ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		self.m_toolBar1.AddControl( self.m_staticText6 )
		self.m_TotalPagesFB = wx.TextCtrl( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_TotalPagesFB.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_TotalPagesFB.SetMinSize( wx.Size( 20,-1 ) )
		self.m_TotalPagesFB.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar1.AddControl( self.m_TotalPagesFB )
		self.m_pageUP = self.m_toolBar1.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_UP,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_pageDOWN = self.m_toolBar1.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
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
		
		self.m_modeDisplay = wx.TextCtrl( self.panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		self.m_modeDisplay.SetFont( wx.Font( 10, 74, 90, 92, False, "Verdana" ) )
		
		bSizer3.Add( self.m_modeDisplay, 0, wx.ALL, 5 )
		
		self.m_userInput = wx.TextCtrl( self.panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_userInput.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_userInput.SetMinSize( wx.Size( 400,-1 ) )
		
		bSizer3.Add( self.m_userInput, 0, wx.ALL, 5 )
		
		self.m_enterselection = wx.Button( self.panel11, wx.ID_ANY, u"Enter Selection", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_enterselection.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
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
		
		self.m_staticText64 = wx.StaticText( self.panel11, wx.ID_ANY, u"Topic", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText64.Wrap( -1 )
		self.m_staticText64.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer3.Add( self.m_staticText64, 0, wx.ALL, 9 )
		
		self.m_TopicInput = wx.TextCtrl( self.panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_TopicInput, 0, wx.ALL, 7 )
		
		self.m_btnScreenshot = wx.Button( self.panel11, wx.ID_ANY, u"Import Screenshot", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_btnScreenshot.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer3.Add( self.m_btnScreenshot, 0, wx.ALL, 5 )
		
		self.m_resetselection = wx.Button( self.panel11, wx.ID_ANY, u"Reset Selection", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_resetselection.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_resetselection.SetToolTip( u"shortcut: right mouse button" )
		
		bSizer3.Add( self.m_resetselection, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer3, 0, wx.EXPAND, 5 )
		
		
		self.panel11.SetSizer( bSizer2 )
		self.panel11.Layout()
		bSizer2.Fit( self.panel11 )
		bSizer8.Add( self.panel11, 1, wx.EXPAND |wx.ALL, 0 )
		
		
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
		self.m_toolSwitchFC = self.m_toolBar3.AddTool( wx.ID_ANY, u"Switch", wx.Bitmap( path_switch, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_modeDisplayFC = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, u"Question:", wx.DefaultPosition, wx.Size( -1,18 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_modeDisplayFC.SetFont( wx.Font( 11, 74, 90, 92, False, "Verdana" ) )
		
		self.m_toolBar3.AddControl( self.m_modeDisplayFC )
		self.m_CurrentCard = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_CENTRE|wx.TE_READONLY )
		self.m_CurrentCard.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_CurrentCard.SetMinSize( wx.Size( 10,-1 ) )
		self.m_CurrentCard.SetMaxSize( wx.Size( 10,-1 ) )
		
		self.m_toolBar3.AddControl( self.m_CurrentCard )
		self.m_staticText611 = wx.StaticText( self.m_toolBar3, wx.ID_ANY, u" of ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText611.Wrap( -1 )
		self.m_staticText611.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		self.m_toolBar3.AddControl( self.m_staticText611 )
		self.m_TotalCards = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY )
		self.m_TotalCards.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_TotalCards.SetMinSize( wx.Size( 20,-1 ) )
		self.m_TotalCards.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar3.AddControl( self.m_TotalCards )
		self.m_staticText311 = wx.StaticText( self.m_toolBar3, wx.ID_ANY, u"    score: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText311.Wrap( -1 )
		self.m_staticText311.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		self.m_toolBar3.AddControl( self.m_staticText311 )
		self.m_Score = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.NO_BORDER )
		self.m_Score.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_Score.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar3.AddControl( self.m_Score )
		self.m_toolPlusFC = self.m_toolBar3.AddTool( wx.ID_ANY, u"plus", wx.Bitmap( path_add, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolMinFC = self.m_toolBar3.AddTool( wx.ID_ANY, u"min", wx.Bitmap( path_min, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_ZoomFC = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, u"100%", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_ZoomFC.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		self.m_toolBar3.AddControl( self.m_ZoomFC )
		self.m_toolBar3.Realize() 
		
		bSizer211.Add( self.m_toolBar3, 0, wx.ALIGN_CENTER|wx.EXPAND, 0 )
		
		self.m_staticline22 = wx.StaticLine( self.panel21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer211.Add( self.m_staticline22, 0, wx.EXPAND |wx.ALL, 3 )
		
		self.m_scrolledWindow11 = wx.ScrolledWindow( self.panel21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_scrolledWindow11.SetScrollRate( 5, 5 )
		bSizer51 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer51.Add( ( 0, 50), 0, wx.EXPAND, 5 )
		
		bSizer82 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer82.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_bitmapScrollFC = wx.StaticBitmap( self.m_scrolledWindow11, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer82.Add( self.m_bitmapScrollFC, 0, wx.ALL, 5 )
		
		
		bSizer82.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer51.Add( bSizer82, 1, wx.EXPAND, 5 )
		
		
		self.m_scrolledWindow11.SetSizer( bSizer51 )
		self.m_scrolledWindow11.Layout()
		bSizer51.Fit( self.m_scrolledWindow11 )
		bSizer211.Add( self.m_scrolledWindow11, 1, wx.EXPAND |wx.ALL, 0 )
		
		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_buttonCorrect = wx.Button( self.panel21, wx.ID_ANY, u"Correct", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonCorrect.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_buttonCorrect.SetToolTip( u"shortcut: left mouse button / left arrow key" )
		
		bSizer31.Add( self.m_buttonCorrect, 1, wx.ALL|wx.EXPAND|wx.RIGHT, 5 )
		
		self.m_buttonWrong = wx.Button( self.panel21, wx.ID_ANY, u"Wrong", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonWrong.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_buttonWrong.SetToolTip( u"shortcut: right mouse click / right arrow key" )
		
		bSizer31.Add( self.m_buttonWrong, 1, wx.ALL|wx.EXPAND|wx.LEFT, 5 )
		
		
		bSizer211.Add( bSizer31, 0, wx.EXPAND, 5 )
		
		
		self.panel21.SetSizer( bSizer211 )
		self.panel21.Layout()
		bSizer211.Fit( self.panel21 )
		bSizer81.Add( self.panel21, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.panel2.SetSizer( bSizer81 )
		self.panel2.Layout()
		bSizer81.Fit( self.panel2 )
		bSizer7.Add( self.panel2, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel3.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel31 = wx.Panel( self.panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel31.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_panel31.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		self.m_panel31.SetMaxSize( wx.Size( 400,-1 ) )
		
		bSizer30 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer30.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer23 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer23.Add( ( 0, 5), 0, wx.EXPAND, 5 )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel31, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		
		sbSizer1.SetMinSize( wx.Size( 310,-1 ) ) 
		gSizer12 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText52 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Boundary line \nbetween Q and A", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.m_staticText52.Wrap( -1 )
		self.m_staticText52.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer12.Add( self.m_staticText52, 0, wx.ALL, 5 )
		
		self.m_lineQA = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lineQA.SetValue(True) 
		self.m_lineQA.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer12.Add( self.m_lineQA, 0, wx.ALL, 5 )
		
		self.m_staticText62 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Line Thickness", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )
		self.m_staticText62.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer12.Add( self.m_staticText62, 0, wx.ALL, 5 )
		
		bSizer222 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_lineWqa = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lineWqa.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_lineWqa.SetMaxSize( wx.Size( 30,-1 ) )
		
		bSizer222.Add( self.m_lineWqa, 0, wx.ALL, 5 )
		
		self.m_staticText24 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"pixels", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		self.m_staticText24.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer222.Add( self.m_staticText24, 0, wx.ALL, 5 )
		
		
		gSizer12.Add( bSizer222, 1, 0, 5 )
		
		self.m_staticText7 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Line Color", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gSizer12.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.m_colorQAline = wx.ColourPickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.Colour( 0, 0, 0 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		gSizer12.Add( self.m_colorQAline, 0, wx.ALL, 5 )
		
		
		sbSizer1.Add( gSizer12, 1, 0, 5 )
		
		self.m_staticText34 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Settings may not be applicable if there are \nno Answer cards made by the user.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText34.Wrap( -1 )
		self.m_staticText34.SetFont( wx.Font( 7, 74, 93, 90, False, "Verdana" ) )
		
		sbSizer1.Add( self.m_staticText34, 0, wx.ALL, 5 )
		
		
		bSizer23.Add( sbSizer1, 0, 0, 5 )
		
		
		bSizer23.Add( ( 0, 10), 0, wx.EXPAND, 5 )
		
		sbSizer11 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel31, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		
		sbSizer11.SetMinSize( wx.Size( 310,-1 ) ) 
		gSizer11 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText511 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Boundary line in each \nrow of the pdf", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.m_staticText511.Wrap( -1 )
		self.m_staticText511.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer11.Add( self.m_staticText511, 0, wx.ALL, 5 )
		
		self.m_linePDF = wx.CheckBox( sbSizer11.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_linePDF.SetValue(True) 
		gSizer11.Add( self.m_linePDF, 0, wx.ALL, 5 )
		
		self.m_staticText612 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Line Thickness", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText612.Wrap( -1 )
		self.m_staticText612.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer11.Add( self.m_staticText612, 0, wx.ALL, 5 )
		
		bSizer221 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_lineWpdf = wx.TextCtrl( sbSizer11.GetStaticBox(), wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lineWpdf.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_lineWpdf.SetMaxSize( wx.Size( 30,-1 ) )
		
		bSizer221.Add( self.m_lineWpdf, 0, wx.ALL, 5 )
		
		self.m_staticText241 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"pixels", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText241.Wrap( -1 )
		self.m_staticText241.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer221.Add( self.m_staticText241, 0, wx.ALL, 5 )
		
		
		gSizer11.Add( bSizer221, 1, 0, 5 )
		
		self.m_staticText71 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Line Color", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )
		self.m_staticText71.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer11.Add( self.m_staticText71, 0, wx.ALL, 5 )
		
		self.m_colorPDFline = wx.ColourPickerCtrl( sbSizer11.GetStaticBox(), wx.ID_ANY, wx.Colour( 18, 5, 250 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		self.m_colorPDFline.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer11.Add( self.m_colorPDFline, 0, wx.ALL, 5 )
		
		
		sbSizer11.Add( gSizer11, 0, 0, 0 )
		
		
		bSizer23.Add( sbSizer11, 0, 0, 5 )
		
		
		bSizer23.Add( ( 0, 10), 0, wx.EXPAND, 5 )
		
		sbSizer111 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel31, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		
		sbSizer111.SetMinSize( wx.Size( 310,-1 ) ) 
		gSizer111 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText5111 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Vertical lines", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.m_staticText5111.Wrap( -1 )
		self.m_staticText5111.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer111.Add( self.m_staticText5111, 0, wx.ALL, 5 )
		
		self.m_lineVERT = wx.CheckBox( sbSizer111.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer111.Add( self.m_lineVERT, 0, wx.ALL, 5 )
		
		self.m_staticText6121 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Line Thickness", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6121.Wrap( -1 )
		self.m_staticText6121.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer111.Add( self.m_staticText6121, 0, wx.ALL, 5 )
		
		bSizer2211 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_lineWvert = wx.TextCtrl( sbSizer111.GetStaticBox(), wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lineWvert.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_lineWvert.SetMaxSize( wx.Size( 30,-1 ) )
		
		bSizer2211.Add( self.m_lineWvert, 0, wx.ALL, 5 )
		
		self.m_staticText2411 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"pixels", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2411.Wrap( -1 )
		self.m_staticText2411.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer2211.Add( self.m_staticText2411, 0, wx.ALL, 5 )
		
		
		gSizer111.Add( bSizer2211, 1, 0, 5 )
		
		self.m_staticText711 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Line Color", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText711.Wrap( -1 )
		self.m_staticText711.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer111.Add( self.m_staticText711, 0, wx.ALL, 5 )
		
		self.m_colorVERTline = wx.ColourPickerCtrl( sbSizer111.GetStaticBox(), wx.ID_ANY, wx.Colour( 18, 5, 250 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		self.m_colorVERTline.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer111.Add( self.m_colorVERTline, 0, wx.ALL, 5 )
		
		self.m_staticText55 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Same color as \nhorizontal lines", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText55.Wrap( -1 )
		gSizer111.Add( self.m_staticText55, 0, wx.ALL, 5 )
		
		self.m_checkBoxSameColor = wx.CheckBox( sbSizer111.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer111.Add( self.m_checkBoxSameColor, 0, wx.ALL, 5 )
		
		
		sbSizer111.Add( gSizer111, 0, 0, 0 )
		
		
		bSizer23.Add( sbSizer111, 0, wx.EXPAND, 5 )
		
		
		bSizer23.Add( ( 0, 10), 0, wx.EXPAND, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel31, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		
		sbSizer3.SetMinSize( wx.Size( 310,-1 ) ) 
		self.m_staticText33 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Fine tune image size by page width %", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )
		self.m_staticText33.SetFont( wx.Font( 8, 74, 93, 90, False, "Verdana" ) )
		
		sbSizer3.Add( self.m_staticText33, 0, wx.ALL, 5 )
		
		self.m_sliderPDFsize = wx.Slider( sbSizer3.GetStaticBox(), wx.ID_ANY, 100, 70, 130, wx.DefaultPosition, wx.Size( 275,-1 ), wx.SL_BOTH|wx.SL_HORIZONTAL|wx.SL_LABELS )
		self.m_sliderPDFsize.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		sbSizer3.Add( self.m_sliderPDFsize, 0, wx.ALL, 0 )
		
		self.m_staticText332 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Fine tune pdf quality", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText332.Wrap( -1 )
		self.m_staticText332.SetFont( wx.Font( 8, 74, 93, 90, False, "Verdana" ) )
		
		sbSizer3.Add( self.m_staticText332, 0, wx.ALL, 5 )
		
		self.m_sliderPDFquality = wx.Slider( sbSizer3.GetStaticBox(), wx.ID_ANY, 100, 10, 100, wx.DefaultPosition, wx.Size( 275,-1 ), wx.SL_HORIZONTAL|wx.SL_LABELS )
		sbSizer3.Add( self.m_sliderPDFquality, 0, wx.ALL, 0 )
		
		self.m_staticText401 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"You can select multiple widths.\nIf an image is wider than any given width,\nthen it will be resized to the nearest value.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText401.Wrap( -1 )
		self.m_staticText401.SetFont( wx.Font( 8, 74, 90, 90, False, "Verdana" ) )
		
		sbSizer3.Add( self.m_staticText401, 0, wx.ALL, 5 )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_slider_col1 = wx.Slider( sbSizer3.GetStaticBox(), wx.ID_ANY, 100, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_LABELS )
		fgSizer2.Add( self.m_slider_col1, 0, wx.ALL, 0 )
		
		self.m_checkBox_col1 = wx.CheckBox( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_checkBox_col1, 0, wx.ALL, 5 )
		
		self.m_slider_col2 = wx.Slider( sbSizer3.GetStaticBox(), wx.ID_ANY, 100, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_LABELS )
		fgSizer2.Add( self.m_slider_col2, 0, wx.ALL, 0 )
		
		self.m_checkBox_col2 = wx.CheckBox( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_checkBox_col2, 0, wx.ALL, 5 )
		
		self.m_slider_col3 = wx.Slider( sbSizer3.GetStaticBox(), wx.ID_ANY, 100, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_LABELS )
		fgSizer2.Add( self.m_slider_col3, 0, wx.ALL, 0 )
		
		self.m_checkBox_col3 = wx.CheckBox( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_checkBox_col3, 0, wx.ALL, 5 )
		
		
		sbSizer3.Add( fgSizer2, 0, wx.EXPAND, 5 )
		
		
		bSizer23.Add( sbSizer3, 0, wx.EXPAND, 5 )
		
		
		bSizer23.Add( ( 0, 30), 0, wx.EXPAND, 5 )
		
		bSizer351 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer110 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer110.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_pdfButtonPrev = wx.BitmapButton( self.m_panel31, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_GO_BACK,  ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer110.Add( self.m_pdfButtonPrev, 0, wx.ALL, 5 )
		
		self.m_pdfButtonNext = wx.BitmapButton( self.m_panel31, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD,  ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer110.Add( self.m_pdfButtonNext, 0, wx.ALL, 5 )
		
		
		bSizer110.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.txtnrcards = wx.StaticText( self.m_panel31, wx.ID_ANY, u"Page", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtnrcards.Wrap( -1 )
		self.txtnrcards.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Verdana" ) )
		
		bSizer110.Add( self.txtnrcards, 0, wx.ALL, 9 )
		
		self.m_pdfCurrentPage = wx.TextCtrl( self.m_panel31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), wx.TE_READONLY )
		bSizer110.Add( self.m_pdfCurrentPage, 0, wx.ALL, 7 )
		
		
		bSizer110.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer351.Add( bSizer110, 1, wx.EXPAND, 5 )
		
		
		bSizer23.Add( bSizer351, 0, wx.EXPAND, 5 )
		
		self.m_PrintFinal = wx.Button( self.m_panel31, wx.ID_ANY, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_PrintFinal.SetFont( wx.Font( 10, 74, 90, 90, False, "Verdana" ) )
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
		
		self.m_staticText35 = wx.StaticText( self.m_panel18, wx.ID_ANY, u"Select with left mouse button what area to select.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )
		self.m_staticText35.SetFont( wx.Font( 9, 74, 93, 90, False, "Verdana" ) )
		
		bSizer331.Add( self.m_staticText35, 0, wx.ALL, 5 )
		
		bSizer341 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_btnUndoChanges = wx.Button( self.m_panel18, wx.ID_ANY, u"Undo Changes", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_btnUndoChanges.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer341.Add( self.m_btnUndoChanges, 0, wx.ALL, 5 )
		
		self.m_btnImportScreenshot = wx.Button( self.m_panel18, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_btnImportScreenshot.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
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
		
		self.panel5 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel5.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer44 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel51 = wx.Panel( self.panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer441 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer441.Add( ( 100, 0), 0, wx.EXPAND, 5 )
		
		bSizer321 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer321.Add( ( 100, 100), 0, wx.EXPAND, 5 )
		
		self.m_panel181 = wx.Panel( self.panel51, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer48 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText39 = wx.StaticText( self.m_panel181, wx.ID_ANY, u"My IP ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText39.Wrap( -1 )
		self.m_staticText39.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		fgSizer1.Add( self.m_staticText39, 0, wx.ALL, 5 )
		
		self.m_txtMyIP = wx.TextCtrl( self.m_panel181, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtMyIP.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		fgSizer1.Add( self.m_txtMyIP, 0, wx.ALL, 5 )
		
		self.m_staticText40 = wx.StaticText( self.m_panel181, wx.ID_ANY, u"Target IP", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )
		self.m_staticText40.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		fgSizer1.Add( self.m_staticText40, 0, wx.ALL, 5 )
		
		self.m_txtTargetIP = wx.TextCtrl( self.m_panel181, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtTargetIP.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		fgSizer1.Add( self.m_txtTargetIP, 0, wx.ALL, 5 )
		
		
		bSizer48.Add( fgSizer1, 0, wx.EXPAND, 5 )
		
		
		bSizer48.Add( ( 0, 0), 0, wx.EXPAND, 5 )
		
		self.m_staticline7 = wx.StaticLine( self.m_panel181, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,1 ), wx.LI_HORIZONTAL )
		self.m_staticline7.SetMaxSize( wx.Size( 500,-1 ) )
		
		bSizer48.Add( self.m_staticline7, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer47 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_buttonTransfer = wx.Button( self.m_panel181, wx.ID_ANY, u"Synchronize", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonTransfer.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer47.Add( self.m_buttonTransfer, 0, wx.ALL, 5 )
		
		self.m_txtStatus = wx.TextCtrl( self.m_panel181, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.TE_READONLY )
		self.m_txtStatus.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer47.Add( self.m_txtStatus, 0, wx.ALL, 5 )
		
		
		bSizer48.Add( bSizer47, 1, wx.EXPAND, 0 )
		
		
		self.m_panel181.SetSizer( bSizer48 )
		self.m_panel181.Layout()
		bSizer48.Fit( self.m_panel181 )
		bSizer321.Add( self.m_panel181, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		bSizer321.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer441.Add( bSizer321, 1, wx.EXPAND, 5 )
		
		
		self.panel51.SetSizer( bSizer441 )
		self.panel51.Layout()
		bSizer441.Fit( self.panel51 )
		bSizer44.Add( self.panel51, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.panel5.SetSizer( bSizer44 )
		self.panel5.Layout()
		bSizer44.Fit( self.panel5 )
		bSizer7.Add( self.panel5, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel6.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer443 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel511 = wx.Panel( self.panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4411 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer4411.Add( ( 100, 0), 0, wx.EXPAND, 5 )
		
		bSizer3211 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer3211.Add( ( 100, 100), 0, wx.EXPAND, 5 )
		
		self.m_panel1811 = wx.Panel( self.panel511, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer482 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer11 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer11.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_listTopics = wx.ListCtrl( self.m_panel1811, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES )
		self.m_listTopics.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.m_listTopics.SetMinSize( wx.Size( 400,-1 ) )
		
		fgSizer11.Add( self.m_listTopics, 1, wx.ALL, 5 )
		
		
		bSizer482.Add( fgSizer11, 0, wx.EXPAND, 5 )
		
		
		bSizer482.Add( ( 0, 0), 0, wx.EXPAND, 5 )
		
		bSizer472 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer104 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_buttonTopic = wx.Button( self.m_panel1811, wx.ID_ANY, u"Add Topic", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonTopic.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer104.Add( self.m_buttonTopic, 0, wx.ALL, 5 )
		
		self.m_textTopic = wx.TextCtrl( self.m_panel1811, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textTopic.SetMinSize( wx.Size( 300,-1 ) )
		
		bSizer104.Add( self.m_textTopic, 0, wx.ALL, 5 )
		
		self.m_buttonReTopic = wx.Button( self.m_panel1811, wx.ID_ANY, u"Rename Topic", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonReTopic.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer104.Add( self.m_buttonReTopic, 0, wx.ALL, 5 )
		
		self.m_buttonDelTopic = wx.Button( self.m_panel1811, wx.ID_ANY, u"Delete Topic", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonDelTopic.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer104.Add( self.m_buttonDelTopic, 0, wx.ALL, 5 )
		
		
		bSizer472.Add( bSizer104, 0, wx.EXPAND, 5 )
		
		self.m_buttonBook = wx.Button( self.m_panel1811, wx.ID_ANY, u"Add Book", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonBook.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer472.Add( self.m_buttonBook, 0, wx.ALL, 5 )
		
		
		bSizer482.Add( bSizer472, 0, wx.EXPAND, 0 )
		
		self.m_staticline71 = wx.StaticLine( self.m_panel1811, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,1 ), wx.LI_HORIZONTAL )
		self.m_staticline71.SetMaxSize( wx.Size( 500,-1 ) )
		
		bSizer482.Add( self.m_staticline71, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_buttonStartBook = wx.Button( self.m_panel1811, wx.ID_ANY, u"Read", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonStartBook.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		self.m_buttonStartBook.SetMinSize( wx.Size( 200,50 ) )
		
		bSizer482.Add( self.m_buttonStartBook, 0, wx.ALL, 5 )
		
		
		self.m_panel1811.SetSizer( bSizer482 )
		self.m_panel1811.Layout()
		bSizer482.Fit( self.m_panel1811 )
		bSizer3211.Add( self.m_panel1811, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		bSizer3211.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer4411.Add( bSizer3211, 1, wx.EXPAND, 5 )
		
		
		self.panel511.SetSizer( bSizer4411 )
		self.panel511.Layout()
		bSizer4411.Fit( self.panel511 )
		bSizer443.Add( self.panel511, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.panel6.SetSizer( bSizer443 )
		self.panel6.Layout()
		bSizer443.Fit( self.panel6 )
		bSizer7.Add( self.panel6, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panelHelp = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panelHelp.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer442 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook = wx.Notebook( self.panelHelp, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_notebook.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		self.m_panel41 = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer63 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_richText2 = wx.richtext.RichTextCtrl( self.m_panel41, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		self.m_richText2.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer63.Add( self.m_richText2, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_panel41.SetSizer( bSizer63 )
		self.m_panel41.Layout()
		bSizer63.Fit( self.m_panel41 )
		self.m_notebook.AddPage( self.m_panel41, u"Flashbook", False )
		self.m_panel42 = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer64 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_richText3 = wx.richtext.RichTextCtrl( self.m_panel42, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		self.m_richText3.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer64.Add( self.m_richText3, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_panel42.SetSizer( bSizer64 )
		self.m_panel42.Layout()
		bSizer64.Fit( self.m_panel42 )
		self.m_notebook.AddPage( self.m_panel42, u"Flashcard", False )
		self.m_panel43 = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer65 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_richText4 = wx.richtext.RichTextCtrl( self.m_panel43, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		self.m_richText4.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer65.Add( self.m_richText4, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_panel43.SetSizer( bSizer65 )
		self.m_panel43.Layout()
		bSizer65.Fit( self.m_panel43 )
		self.m_notebook.AddPage( self.m_panel43, u"Synchronize", False )
		
		bSizer442.Add( self.m_notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.panelHelp.SetSizer( bSizer442 )
		self.panelHelp.Layout()
		bSizer442.Fit( self.panelHelp )
		bSizer7.Add( self.panelHelp, 1, wx.EXPAND |wx.ALL, 0 )
		
		bSizer41 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer7.Add( bSizer41, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer7 )
		self.Layout()
		bSizer7.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.m_menuItemFlashbookOnMenuSelection, id = self.m_menuItemFlashbook.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuItemJPGOnMenuSelection, id = self.m_menuItemJPG.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuPDFfolderOnMenuSelection, id = self.m_menuPDFfolder.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuItemBackToMainOnMenuSelection, id = self.m_menuItemBackToMain.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuItemConvertOnMenuSelection, id = self.m_menuItemConvert.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuCombineBooksOnMenuSelection, id = self.m_menuCombineBooks.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuNewBookOnMenuSelection, id = self.m_menuNewBook.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuAddPDFOnMenuSelection, id = self.m_menuAddPDF.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuItemDelBookOnMenuSelection, id = self.m_menuItemDelBook.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuAddCardOnMenuSelection, id = self.m_menuAddCard.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuEditCardOnMenuSelection, id = self.m_menuEditCard.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuPreviousCardOnMenuSelection, id = self.m_menuPreviousCard.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuHelpOnMenuSelection, id = self.m_menuHelp.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuItemAboutOnMenuSelection, id = self.m_menuItemAbout.GetId() )
		self.Bind( wx.EVT_MENU, self.m_checkBoxSelectionsOnMenuSelection, id = self.m_checkBoxSelections.GetId() )
		self.Bind( wx.EVT_MENU, self.m_checkBoxDebugOnMenuSelection, id = self.m_checkBoxDebug.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuItemGraphOnMenuSelection, id = self.m_menuItemGraph.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuResetSettingsOnMenuSelection, id = self.m_menuResetSettings.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuResetGraphOnMenuSelection, id = self.m_menuResetGraph.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuResetLogOnMenuSelection, id = self.m_menuResetLog.GetId() )
		self.m_OpenFlashbook.Bind( wx.EVT_BUTTON, self.m_OpenFlashbookOnButtonClick )
		self.m_OpenFlashcard.Bind( wx.EVT_BUTTON, self.m_OpenFlashcardOnButtonClick )
		self.m_OpenPrint.Bind( wx.EVT_BUTTON, self.m_OpenPrintOnButtonClick )
		self.m_OpenTransfer.Bind( wx.EVT_BUTTON, self.m_OpenTransferOnButtonClick )
		self.Bind( wx.EVT_TOOL, self.m_toolPlusFBOnToolClicked, id = self.m_toolPlusFB.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolMinFBOnToolClicked, id = self.m_toolMinFB.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_pageBackFBOnToolClicked, id = self.m_pageBackFB.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_pageNextFBOnToolClicked, id = self.m_pageNextFB.GetId() )
		self.m_CurrentPageFB.Bind( wx.EVT_ENTER_WINDOW, self.m_CurrentPageFBOnEnterWindow )
		self.m_CurrentPageFB.Bind( wx.EVT_KEY_UP, self.m_CurrentPageFBOnKeyUp )
		self.m_CurrentPageFB.Bind( wx.EVT_LEAVE_WINDOW, self.m_CurrentPageFBOnLeaveWindow )
		self.Bind( wx.EVT_TOOL, self.m_pageUPOnToolClicked, id = self.m_pageUP.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_pageDOWNOnToolClicked, id = self.m_pageDOWN.GetId() )
		self.m_scrolledWindow1.Bind( wx.EVT_KEY_DOWN, self.m_scrolledWindow1OnKeyDown )
		self.m_scrolledWindow1.Bind( wx.EVT_LEFT_DOWN, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_LEFT_UP, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_MIDDLE_DOWN, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_MIDDLE_UP, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_RIGHT_DOWN, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_RIGHT_UP, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_MOTION, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_LEFT_DCLICK, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_MIDDLE_DCLICK, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_RIGHT_DCLICK, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_LEAVE_WINDOW, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_ENTER_WINDOW, self.m_scrolledWindow1OnMouseEvents )
		self.m_scrolledWindow1.Bind( wx.EVT_MOUSEWHEEL, self.m_scrolledWindow1OnMouseEvents )
		self.m_bitmapScroll.Bind( wx.EVT_KEY_DOWN, self.m_bitmapScrollOnKeyDown )
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
		self.m_userInput.Bind( wx.EVT_ENTER_WINDOW, self.m_userInputOnEnterWindow )
		self.m_userInput.Bind( wx.EVT_LEAVE_WINDOW, self.m_userInputOnLeaveWindow )
		self.m_enterselection.Bind( wx.EVT_BUTTON, self.m_enterselectionOnButtonClick )
		self.m_toolStitch.Bind( wx.EVT_BUTTON, self.m_toolStitchOnButtonClick )
		self.m_btnScreenshot.Bind( wx.EVT_BUTTON, self.m_btnScreenshotOnButtonClick )
		self.m_resetselection.Bind( wx.EVT_BUTTON, self.m_resetselectionOnButtonClick )
		self.Bind( wx.EVT_TOOL, self.m_toolSwitchFCOnToolClicked, id = self.m_toolSwitchFC.GetId() )
		self.m_CurrentCard.Bind( wx.EVT_KEY_DOWN, self.m_CurrentCardOnKeyDown )
		self.m_CurrentCard.Bind( wx.EVT_KEY_UP, self.m_CurrentCardOnKeyUp )
		self.m_CurrentCard.Bind( wx.EVT_TEXT, self.m_CurrentCardOnText )
		self.Bind( wx.EVT_TOOL, self.m_toolPlusFCOnToolClicked, id = self.m_toolPlusFC.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolMinFCOnToolClicked, id = self.m_toolMinFC.GetId() )
		self.m_scrolledWindow11.Bind( wx.EVT_KEY_DOWN, self.m_scrolledWindow11OnKeyDown )
		self.m_scrolledWindow11.Bind( wx.EVT_LEFT_UP, self.m_scrolledWindow11OnLeftUp )
		self.m_scrolledWindow11.Bind( wx.EVT_LEFT_DOWN, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_LEFT_UP, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_MIDDLE_DOWN, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_MIDDLE_UP, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_RIGHT_DOWN, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_RIGHT_UP, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_MOTION, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_LEFT_DCLICK, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_MIDDLE_DCLICK, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_RIGHT_DCLICK, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_LEAVE_WINDOW, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_ENTER_WINDOW, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_MOUSEWHEEL, self.m_scrolledWindow11OnMouseEvents )
		self.m_scrolledWindow11.Bind( wx.EVT_MOUSEWHEEL, self.m_scrolledWindow11OnMouseWheel )
		self.m_scrolledWindow11.Bind( wx.EVT_RIGHT_UP, self.m_scrolledWindow11OnRightUp )
		self.m_bitmapScrollFC.Bind( wx.EVT_KEY_DOWN, self.m_bitmapScrollFCOnKeyDown )
		self.m_bitmapScrollFC.Bind( wx.EVT_LEFT_DOWN, self.m_bitmapScrollFCOnLeftDown )
		self.m_bitmapScrollFC.Bind( wx.EVT_LEFT_UP, self.m_bitmapScrollFCOnLeftUp )
		self.m_bitmapScrollFC.Bind( wx.EVT_MOTION, self.m_bitmapScrollFCOnMotion )
		self.m_bitmapScrollFC.Bind( wx.EVT_LEFT_DOWN, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_LEFT_UP, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_MIDDLE_DOWN, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_MIDDLE_UP, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_RIGHT_DOWN, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_RIGHT_UP, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_MOTION, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_LEFT_DCLICK, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_MIDDLE_DCLICK, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_RIGHT_DCLICK, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_LEAVE_WINDOW, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_ENTER_WINDOW, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_MOUSEWHEEL, self.m_bitmapScrollFCOnMouseEvents )
		self.m_bitmapScrollFC.Bind( wx.EVT_MOUSEWHEEL, self.m_bitmapScrollFCOnMouseWheel )
		self.m_bitmapScrollFC.Bind( wx.EVT_RIGHT_DOWN, self.m_bitmapScrollFCOnRightDown )
		self.m_bitmapScrollFC.Bind( wx.EVT_RIGHT_UP, self.m_bitmapScrollFCOnRightUp )
		self.m_buttonCorrect.Bind( wx.EVT_BUTTON, self.m_buttonCorrectOnButtonClick )
		self.m_buttonWrong.Bind( wx.EVT_BUTTON, self.m_buttonWrongOnButtonClick )
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
		self.m_lineVERT.Bind( wx.EVT_CHECKBOX, self.m_lineVERTOnCheckBox )
		self.m_lineVERT.Bind( wx.EVT_LEFT_UP, self.m_linePDFOnLeftUp )
		self.m_lineWvert.Bind( wx.EVT_TEXT, self.m_lineWvertOnText )
		self.m_lineWvert.Bind( wx.EVT_TEXT_ENTER, self.m_lineWvertOnTextEnter )
		self.m_colorVERTline.Bind( wx.EVT_COLOURPICKER_CHANGED, self.m_colorVERTlineOnColourChanged )
		self.m_checkBoxSameColor.Bind( wx.EVT_CHECKBOX, self.m_checkBoxSameColorOnCheckBox )
		self.m_sliderPDFsize.Bind( wx.EVT_KEY_UP, self.m_sliderPDFsizeOnKeyUp )
		self.m_sliderPDFsize.Bind( wx.EVT_SCROLL_CHANGED, self.m_sliderPDFsizeOnScrollChanged )
		self.m_sliderPDFquality.Bind( wx.EVT_SCROLL_CHANGED, self.m_sliderPDFqualityOnScrollChanged )
		self.m_slider_col1.Bind( wx.EVT_SCROLL_CHANGED, self.m_slider_col1OnScrollChanged )
		self.m_checkBox_col1.Bind( wx.EVT_CHECKBOX, self.m_checkBox_col1OnCheckBox )
		self.m_slider_col2.Bind( wx.EVT_SCROLL_CHANGED, self.m_slider_col2OnScrollChanged )
		self.m_checkBox_col2.Bind( wx.EVT_CHECKBOX, self.m_checkBox_col2OnCheckBox )
		self.m_slider_col3.Bind( wx.EVT_SCROLL_CHANGED, self.m_slider_col3OnScrollChanged )
		self.m_checkBox_col3.Bind( wx.EVT_CHECKBOX, self.m_checkBox_col3OnCheckBox )
		self.m_pdfButtonPrev.Bind( wx.EVT_BUTTON, self.m_pdfButtonPrevOnButtonClick )
		self.m_pdfButtonNext.Bind( wx.EVT_BUTTON, self.m_pdfButtonNextOnButtonClick )
		self.m_pdfCurrentPage.Bind( wx.EVT_TEXT_ENTER, self.m_pdfCurrentPageOnTextEnter )
		self.m_PrintFinal.Bind( wx.EVT_BUTTON, self.m_PrintFinalOnButtonClick )
		self.m_panel32.Bind( wx.EVT_MOUSEWHEEL, self.m_panel32OnMouseWheel )
		self.m_bitmap3.Bind( wx.EVT_LEFT_DOWN, self.m_bitmap3OnLeftDown )
		self.m_bitmap3.Bind( wx.EVT_MOUSEWHEEL, self.m_bitmap3OnMouseWheel )
		self.m_bitmap4.Bind( wx.EVT_LEFT_DOWN, self.m_bitmap4OnLeftDown )
		self.m_bitmap4.Bind( wx.EVT_LEFT_UP, self.m_bitmap4OnLeftUp )
		self.m_btnUndoChanges.Bind( wx.EVT_BUTTON, self.m_btnUndoChangesOnButtonClick )
		self.m_btnImportScreenshot.Bind( wx.EVT_BUTTON, self.m_btnImportScreenshotOnButtonClick )
		self.m_txtMyIP.Bind( wx.EVT_KEY_UP, self.m_txtMyIPOnKeyUp )
		self.m_txtTargetIP.Bind( wx.EVT_KEY_UP, self.m_txtTargetIPOnKeyUp )
		self.m_buttonTransfer.Bind( wx.EVT_BUTTON, self.m_buttonTransferOnButtonClick )
		self.m_listTopics.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.m_listTopicsOnListItemDeselected )
		self.m_listTopics.Bind( wx.EVT_LIST_ITEM_SELECTED, self.m_listTopicsOnListItemSelected )
		self.m_buttonTopic.Bind( wx.EVT_BUTTON, self.m_buttonTopicOnButtonClick )
		self.m_buttonReTopic.Bind( wx.EVT_BUTTON, self.m_buttonReTopicOnButtonClick )
		self.m_buttonDelTopic.Bind( wx.EVT_BUTTON, self.m_buttonDelTopicOnButtonClick )
		self.m_buttonBook.Bind( wx.EVT_BUTTON, self.m_buttonBookOnButtonClick )
		self.m_buttonStartBook.Bind( wx.EVT_BUTTON, self.m_buttonStartBookOnButtonClick )
		self.m_richText2.Bind( wx.EVT_LEFT_DOWN, self.m_richText2OnLeftDown )
		self.m_richText3.Bind( wx.EVT_LEFT_DOWN, self.m_richText3OnLeftDown )
		self.m_richText4.Bind( wx.EVT_LEFT_DOWN, self.m_richText4OnLeftDown )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_menuItemFlashbookOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuItemJPGOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuPDFfolderOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuItemBackToMainOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuItemConvertOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuCombineBooksOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuNewBookOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuAddPDFOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuItemDelBookOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuAddCardOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuEditCardOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuPreviousCardOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuHelpOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuItemAboutOnMenuSelection( self, event ):
		event.Skip()
	
	def m_checkBoxSelectionsOnMenuSelection( self, event ):
		event.Skip()
	
	def m_checkBoxDebugOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuItemGraphOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuResetSettingsOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuResetGraphOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuResetLogOnMenuSelection( self, event ):
		event.Skip()
	
	def m_OpenFlashbookOnButtonClick( self, event ):
		event.Skip()
	
	def m_OpenFlashcardOnButtonClick( self, event ):
		event.Skip()
	
	def m_OpenPrintOnButtonClick( self, event ):
		event.Skip()
	
	def m_OpenTransferOnButtonClick( self, event ):
		event.Skip()
	
	def m_toolPlusFBOnToolClicked( self, event ):
		event.Skip()
	
	def m_toolMinFBOnToolClicked( self, event ):
		event.Skip()
	
	def m_pageBackFBOnToolClicked( self, event ):
		event.Skip()
	
	def m_pageNextFBOnToolClicked( self, event ):
		event.Skip()
	
	def m_CurrentPageFBOnEnterWindow( self, event ):
		event.Skip()
	
	def m_CurrentPageFBOnKeyUp( self, event ):
		event.Skip()
	
	def m_CurrentPageFBOnLeaveWindow( self, event ):
		event.Skip()
	
	def m_pageUPOnToolClicked( self, event ):
		event.Skip()
	
	def m_pageDOWNOnToolClicked( self, event ):
		event.Skip()
	
	def m_scrolledWindow1OnKeyDown( self, event ):
		event.Skip()
	
	def m_scrolledWindow1OnMouseEvents( self, event ):
		event.Skip()
	
	def m_bitmapScrollOnKeyDown( self, event ):
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
	
	def m_userInputOnEnterWindow( self, event ):
		event.Skip()
	
	def m_userInputOnLeaveWindow( self, event ):
		event.Skip()
	
	def m_enterselectionOnButtonClick( self, event ):
		event.Skip()
	
	def m_toolStitchOnButtonClick( self, event ):
		event.Skip()
	
	def m_btnScreenshotOnButtonClick( self, event ):
		event.Skip()
	
	def m_resetselectionOnButtonClick( self, event ):
		event.Skip()
	
	def m_toolSwitchFCOnToolClicked( self, event ):
		event.Skip()
	
	def m_CurrentCardOnKeyDown( self, event ):
		event.Skip()
	
	def m_CurrentCardOnKeyUp( self, event ):
		event.Skip()
	
	def m_CurrentCardOnText( self, event ):
		event.Skip()
	
	def m_toolPlusFCOnToolClicked( self, event ):
		event.Skip()
	
	def m_toolMinFCOnToolClicked( self, event ):
		event.Skip()
	
	def m_scrolledWindow11OnKeyDown( self, event ):
		event.Skip()
	
	def m_scrolledWindow11OnLeftUp( self, event ):
		event.Skip()
	
	def m_scrolledWindow11OnMouseEvents( self, event ):
		event.Skip()
	
	def m_scrolledWindow11OnMouseWheel( self, event ):
		event.Skip()
	
	def m_scrolledWindow11OnRightUp( self, event ):
		event.Skip()
	
	def m_bitmapScrollFCOnKeyDown( self, event ):
		event.Skip()
	
	def m_bitmapScrollFCOnLeftDown( self, event ):
		event.Skip()
	
	def m_bitmapScrollFCOnLeftUp( self, event ):
		event.Skip()
	
	def m_bitmapScrollFCOnMotion( self, event ):
		event.Skip()
	
	def m_bitmapScrollFCOnMouseEvents( self, event ):
		event.Skip()
	
	def m_bitmapScrollFCOnMouseWheel( self, event ):
		event.Skip()
	
	def m_bitmapScrollFCOnRightDown( self, event ):
		event.Skip()
	
	def m_bitmapScrollFCOnRightUp( self, event ):
		event.Skip()
	
	def m_buttonCorrectOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonWrongOnButtonClick( self, event ):
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
	
	def m_lineVERTOnCheckBox( self, event ):
		event.Skip()
	
	
	def m_lineWvertOnText( self, event ):
		event.Skip()
	
	def m_lineWvertOnTextEnter( self, event ):
		event.Skip()
	
	def m_colorVERTlineOnColourChanged( self, event ):
		event.Skip()
	
	def m_checkBoxSameColorOnCheckBox( self, event ):
		event.Skip()
	
	def m_sliderPDFsizeOnKeyUp( self, event ):
		event.Skip()
	
	def m_sliderPDFsizeOnScrollChanged( self, event ):
		event.Skip()
	
	def m_sliderPDFqualityOnScrollChanged( self, event ):
		event.Skip()
	
	def m_slider_col1OnScrollChanged( self, event ):
		event.Skip()
	
	def m_checkBox_col1OnCheckBox( self, event ):
		event.Skip()
	
	def m_slider_col2OnScrollChanged( self, event ):
		event.Skip()
	
	def m_checkBox_col2OnCheckBox( self, event ):
		event.Skip()
	
	def m_slider_col3OnScrollChanged( self, event ):
		event.Skip()
	
	def m_checkBox_col3OnCheckBox( self, event ):
		event.Skip()
	
	def m_pdfButtonPrevOnButtonClick( self, event ):
		event.Skip()
	
	def m_pdfButtonNextOnButtonClick( self, event ):
		event.Skip()
	
	def m_pdfCurrentPageOnTextEnter( self, event ):
		event.Skip()
	
	def m_PrintFinalOnButtonClick( self, event ):
		event.Skip()
	
	def m_panel32OnMouseWheel( self, event ):
		event.Skip()
	
	def m_bitmap3OnLeftDown( self, event ):
		event.Skip()
	
	def m_bitmap3OnMouseWheel( self, event ):
		event.Skip()
	
	def m_bitmap4OnLeftDown( self, event ):
		event.Skip()
	
	def m_bitmap4OnLeftUp( self, event ):
		event.Skip()
	
	def m_btnUndoChangesOnButtonClick( self, event ):
		event.Skip()
	
	def m_btnImportScreenshotOnButtonClick( self, event ):
		event.Skip()
	
	def m_txtMyIPOnKeyUp( self, event ):
		event.Skip()
	
	def m_txtTargetIPOnKeyUp( self, event ):
		event.Skip()
	
	def m_buttonTransferOnButtonClick( self, event ):
		event.Skip()
	
	def m_listTopicsOnListItemDeselected( self, event ):
		event.Skip()
	
	def m_listTopicsOnListItemSelected( self, event ):
		event.Skip()
	
	def m_buttonTopicOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonReTopicOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonDelTopicOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonBookOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonStartBookOnButtonClick( self, event ):
		event.Skip()
	
	def m_richText2OnLeftDown( self, event ):
		event.Skip()
	
	def m_richText3OnLeftDown( self, event ):
		event.Skip()
	
	def m_richText4OnLeftDown( self, event ):
		event.Skip()
	

###########################################################################
## Class MyDialog
###########################################################################

class MyDialog ( wx.Dialog ):
	
	def __init__( self, parent, data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Settings", pos = wx.DefaultPosition, size = wx.Size( 349,250 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.Size( 350,250 ) )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel4.SetBackgroundColour( wx.Colour( 254, 239, 231 ) )
		
		bSizer91 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText5 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Number of questions  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.m_slider1 = wx.Slider( self.m_panel4, wx.ID_ANY, data, 1, data, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
		self.m_slider1.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer1.Add( self.m_slider1, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Multiplier  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.m_textCtrl11 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl11.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_textCtrl11.SetMaxSize( wx.Size( 30,-1 ) )
		
		gSizer1.Add( self.m_textCtrl11, 0, wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Order of cards  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_radioChrono = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"Chronological", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioChrono.SetValue( True ) 
		self.m_radioChrono.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer9.Add( self.m_radioChrono, 0, wx.ALL, 5 )
		
		self.m_radioRandom = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"Random", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioRandom.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
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
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Settings", pos = wx.DefaultPosition, size = wx.Size( 349,300 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.Size( 350,300 ) )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel4.SetBackgroundColour( wx.Colour( 254, 239, 231 ) )
		
		bSizer91 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText5 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Number of questions  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.m_slider1 = wx.Slider( self.m_panel4, wx.ID_ANY, data, 1, data, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
		self.m_slider1.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer1.Add( self.m_slider1, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Multiplier  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.m_textCtrl11 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl11.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_textCtrl11.SetMaxSize( wx.Size( 30,-1 ) )
		
		gSizer1.Add( self.m_textCtrl11, 0, wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Order of cards  :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_radioChrono = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"Chronological", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.m_radioChrono.SetValue( True ) 
		self.m_radioChrono.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer9.Add( self.m_radioChrono, 0, wx.ALL, 5 )
		
		self.m_radioRandom = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"Random", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioRandom.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer9.Add( self.m_radioRandom, 0, wx.ALL, 5 )
		
		
		gSizer1.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		self.m_staticText17 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Continue last session?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		self.m_staticText17.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		gSizer1.Add( self.m_staticText17, 0, wx.ALL, 5 )
		
		bSizer23 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_radioYes = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"Yes", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.m_radioYes.SetValue( True ) 
		self.m_radioYes.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer23.Add( self.m_radioYes, 0, wx.ALL, 5 )
		
		self.m_radioNo = wx.RadioButton( self.m_panel4, wx.ID_ANY, u"No", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioNo.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
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
	

###########################################################################
## Class MyDialog3
###########################################################################

class MyDialog3 ( wx.Dialog ):
	
	def __init__( self, parent, data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Create a new book", pos = wx.DefaultPosition, size = wx.Size( 230,100 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer50 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel26 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer53 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer57 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText49 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Bookname", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText49.Wrap( -1 )
		self.m_staticText49.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer57.Add( self.m_staticText49, 0, wx.ALL, 5 )
		
		self.m_textCtrl23 = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl23.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer57.Add( self.m_textCtrl23, 0, wx.ALL, 5 )
		
		
		bSizer53.Add( bSizer57, 1, wx.EXPAND, 5 )
		
		bSizer58 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer58.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_buttonDLG3OK = wx.Button( self.m_panel26, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonDLG3OK.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer58.Add( self.m_buttonDLG3OK, 0, wx.ALL, 0 )
		
		
		bSizer58.Add( ( 10, 0), 0, wx.EXPAND, 5 )
		
		self.m_buttonDLG3Cancel = wx.Button( self.m_panel26, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonDLG3Cancel.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer58.Add( self.m_buttonDLG3Cancel, 0, wx.ALL, 0 )
		
		
		bSizer58.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer53.Add( bSizer58, 1, wx.EXPAND, 5 )
		
		
		self.m_panel26.SetSizer( bSizer53 )
		self.m_panel26.Layout()
		bSizer53.Fit( self.m_panel26 )
		bSizer50.Add( self.m_panel26, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer50 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_buttonDLG3OK.Bind( wx.EVT_BUTTON, self.m_buttonDLG3OKOnButtonClick )
		self.m_buttonDLG3Cancel.Bind( wx.EVT_BUTTON, self.m_buttonDLG3CancelOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_buttonDLG3OKOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonDLG3CancelOnButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class MyDialog4
###########################################################################

class MyDialog4 ( wx.Dialog ):
	
	def __init__( self, parent, data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Warning", pos = wx.DefaultPosition, size = wx.Size( 422,153 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer50 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel26 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer53 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer57 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText49 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Are you sure you want to delete: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText49.Wrap( -1 )
		self.m_staticText49.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer57.Add( self.m_staticText49, 0, wx.ALL, 5 )
		
		self.m_textCtrlDelBook = wx.TextCtrl( self.m_panel26, wx.ID_ANY, data, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlDelBook.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_textCtrlDelBook.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		self.m_textCtrlDelBook.SetMinSize( wx.Size( 390,-1 ) )
		
		bSizer57.Add( self.m_textCtrlDelBook, 1, wx.ALL, 5 )
		
		
		bSizer53.Add( bSizer57, 1, wx.EXPAND, 5 )
		
		bSizer68 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText52 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"and all related files?        (Except for PDFs)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText52.Wrap( -1 )
		self.m_staticText52.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer68.Add( self.m_staticText52, 0, wx.ALL, 5 )
		
		
		bSizer53.Add( bSizer68, 1, wx.EXPAND, 5 )
		
		bSizer58 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer58.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_buttonDLG4YES = wx.Button( self.m_panel26, wx.ID_OK, u"Yes", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonDLG4YES.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer58.Add( self.m_buttonDLG4YES, 0, wx.ALL, 0 )
		
		
		bSizer58.Add( ( 10, 0), 0, wx.EXPAND, 5 )
		
		self.m_buttonDLG4NO = wx.Button( self.m_panel26, wx.ID_CANCEL, u"No", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonDLG4NO.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer58.Add( self.m_buttonDLG4NO, 0, wx.ALL, 0 )
		
		
		bSizer58.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer53.Add( bSizer58, 1, wx.EXPAND, 5 )
		
		
		self.m_panel26.SetSizer( bSizer53 )
		self.m_panel26.Layout()
		bSizer53.Fit( self.m_panel26 )
		bSizer50.Add( self.m_panel26, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer50 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_buttonDLG4YES.Bind( wx.EVT_BUTTON, self.m_buttonDLG4YESOnButtonClick )
		self.m_buttonDLG4NO.Bind( wx.EVT_BUTTON, self.m_buttonDLG4NOOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_buttonDLG4YESOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonDLG4NOOnButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class MyDialog5
###########################################################################

class MyDialog5 ( wx.Dialog ):
	
	def __init__( self, parent, data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Info", pos = wx.DefaultPosition, size = wx.Size( 468,303 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer50 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel26 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer53 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer57 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText49 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Do you want to combine the following books:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText49.Wrap( -1 )
		self.m_staticText49.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer57.Add( self.m_staticText49, 0, wx.ALL, 5 )
		
		self.m_textCtrlComBooks = wx.TextCtrl( self.m_panel26, wx.ID_ANY, data[0], wx.DefaultPosition, wx.Size( -1,70 ), wx.TE_MULTILINE )
		self.m_textCtrlComBooks.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_textCtrlComBooks.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		self.m_textCtrlComBooks.SetMinSize( wx.Size( 430,70 ) )
		self.m_textCtrlComBooks.SetMaxSize( wx.Size( -1,70 ) )
		
		bSizer57.Add( self.m_textCtrlComBooks, 1, wx.ALL, 5 )
		
		
		bSizer53.Add( bSizer57, 1, wx.EXPAND, 5 )
		
		bSizer68 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText52 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"into a new notes file, which can only be used for \nprinting and flashcards.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText52.Wrap( -1 )
		self.m_staticText52.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer68.Add( self.m_staticText52, 0, wx.ALL, 5 )
		
		
		bSizer53.Add( bSizer68, 1, wx.EXPAND, 5 )
		
		bSizer79 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioDLG5_1 = wx.RadioButton( self.m_panel26, wx.ID_ANY, u"Alphabetically", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioDLG5_1.SetValue( True ) 
		self.m_radioDLG5_1.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer79.Add( self.m_radioDLG5_1, 0, wx.ALL, 5 )
		
		self.m_radioDLG5_2 = wx.RadioButton( self.m_panel26, wx.ID_ANY, u"Small to large", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioDLG5_2.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer79.Add( self.m_radioDLG5_2, 0, wx.ALL, 5 )
		
		self.m_radioDLG5_3 = wx.RadioButton( self.m_panel26, wx.ID_ANY, u"Large to small", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioDLG5_3.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer79.Add( self.m_radioDLG5_3, 0, wx.ALL, 5 )
		
		self.m_radioDLG5_4 = wx.RadioButton( self.m_panel26, wx.ID_ANY, u"Random", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioDLG5_4.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer79.Add( self.m_radioDLG5_4, 0, wx.ALL, 5 )
		
		
		bSizer53.Add( bSizer79, 1, wx.EXPAND, 5 )
		
		bSizer185 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText125 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Combined filename :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText125.Wrap( -1 )
		self.m_staticText125.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer185.Add( self.m_staticText125, 0, wx.ALL, 5 )
		
		self.m_textCtrlCombinedFileName = wx.TextCtrl( self.m_panel26, wx.ID_ANY, data[1], wx.DefaultPosition, wx.Size( 430,-1 ), 0 )
		bSizer185.Add( self.m_textCtrlCombinedFileName, 0, wx.ALL, 5 )
		
		
		bSizer53.Add( bSizer185, 1, wx.EXPAND, 5 )
		
		bSizer58 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer58.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_buttonDLG4YES = wx.Button( self.m_panel26, wx.ID_OK, u"Yes", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonDLG4YES.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer58.Add( self.m_buttonDLG4YES, 0, wx.ALL, 0 )
		
		
		bSizer58.Add( ( 10, 0), 0, wx.EXPAND, 5 )
		
		self.m_buttonDLG4NO = wx.Button( self.m_panel26, wx.ID_CANCEL, u"No", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonDLG4NO.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer58.Add( self.m_buttonDLG4NO, 0, wx.ALL, 0 )
		
		
		bSizer58.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer53.Add( bSizer58, 1, wx.EXPAND, 5 )
		
		
		self.m_panel26.SetSizer( bSizer53 )
		self.m_panel26.Layout()
		bSizer53.Fit( self.m_panel26 )
		bSizer50.Add( self.m_panel26, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer50 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_buttonDLG4YES.Bind( wx.EVT_BUTTON, self.m_buttonDLG4YESOnButtonClick )
		self.m_buttonDLG4NO.Bind( wx.EVT_BUTTON, self.m_buttonDLG4NOOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_buttonDLG4YESOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonDLG4NOOnButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class MyDialog8
###########################################################################

class MyDialog8 ( wx.Dialog ):
	
	def __init__( self, parent, data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_CLOSE, title = u"Edit the cards", pos = wx.DefaultPosition, size = wx.Size( 527,188 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer78 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel32 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer79 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText55 = wx.StaticText( self.m_panel32, wx.ID_ANY, u"Question", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText55.Wrap( -1 )
		self.m_staticText55.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		fgSizer5.Add( self.m_staticText55, 0, wx.ALL, 5 )
		
		self.m_textCtrl24 = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[1], wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl24.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_textCtrl24.SetMinSize( wx.Size( 400,-1 ) )
		
		fgSizer5.Add( self.m_textCtrl24, 1, wx.ALL, 5 )
		
		self.m_staticText56 = wx.StaticText( self.m_panel32, wx.ID_ANY, u"Answer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText56.Wrap( -1 )
		self.m_staticText56.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		fgSizer5.Add( self.m_staticText56, 0, wx.ALL, 5 )
		
		self.m_textCtrl25 = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[2], wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl25.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_textCtrl25.SetMinSize( wx.Size( 400,-1 ) )
		
		fgSizer5.Add( self.m_textCtrl25, 0, wx.ALL, 5 )
		
		self.m_staticText68 = wx.StaticText( self.m_panel32, wx.ID_ANY, u"Topic", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText68.Wrap( -1 )
		self.m_staticText68.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		fgSizer5.Add( self.m_staticText68, 0, wx.ALL, 5 )
		
		self.m_textCtrl30 = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[3], wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl30.SetMinSize( wx.Size( 400,-1 ) )
		
		fgSizer5.Add( self.m_textCtrl30, 0, wx.ALL, 5 )
		
		
		bSizer79.Add( fgSizer5, 0, wx.EXPAND, 5 )
		
		self.m_staticline11 = wx.StaticLine( self.m_panel32, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer79.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer80 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer80.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button22 = wx.Button( self.m_panel32, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button22.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer80.Add( self.m_button22, 0, wx.ALL, 5 )
		
		
		bSizer80.Add( ( 10, 0), 0, wx.EXPAND, 5 )
		
		self.m_button23 = wx.Button( self.m_panel32, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button23.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer80.Add( self.m_button23, 0, wx.ALL, 5 )
		
		
		bSizer80.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer79.Add( bSizer80, 0, wx.EXPAND, 5 )
		
		
		self.m_panel32.SetSizer( bSizer79 )
		self.m_panel32.Layout()
		bSizer79.Fit( self.m_panel32 )
		bSizer78.Add( self.m_panel32, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer78 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class MyDialog9
###########################################################################

class MyDialog9 ( wx.Dialog ):
	
	def __init__( self, parent, data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_CLOSE, title = u"Edit the pdf card", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.Size( 650,268 ), wx.DefaultSize )
		
		bSizer78 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel32 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer79 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer111.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_bitmap13 = wx.StaticBitmap( self.m_panel32, wx.ID_ANY, data[0], wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.m_bitmap13, 0, wx.ALL, 5 )
		
		self.m_bitmap14 = wx.StaticBitmap( self.m_panel32, wx.ID_ANY, data[1], wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.m_bitmap14, 0, wx.ALL, 5 )
		
		
		bSizer111.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer79.Add( bSizer111, 1, wx.EXPAND, 5 )
		
		bSizer1111 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer1111.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		fgSizer5 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText71 = wx.StaticText( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )
		fgSizer5.Add( self.m_staticText71, 0, wx.ALL, 5 )
		
		bSizer1112 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer1112.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText72 = wx.StaticText( self.m_panel32, wx.ID_ANY, u"Text", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText72.Wrap( -1 )
		self.m_staticText72.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer1112.Add( self.m_staticText72, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		bSizer1112.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		fgSizer5.Add( bSizer1112, 1, wx.EXPAND, 5 )
		
		bSizer112 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer112.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText73 = wx.StaticText( self.m_panel32, wx.ID_ANY, u"Picture name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText73.Wrap( -1 )
		self.m_staticText73.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer112.Add( self.m_staticText73, 0, wx.ALL, 5 )
		
		
		bSizer112.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		fgSizer5.Add( bSizer112, 1, wx.EXPAND, 5 )
		
		self.m_staticText55 = wx.StaticText( self.m_panel32, wx.ID_ANY, u"Question", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText55.Wrap( -1 )
		self.m_staticText55.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		fgSizer5.Add( self.m_staticText55, 0, wx.ALL, 5 )
		
		self.m_textCtrlQtext = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[2], wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_textCtrlQtext.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_textCtrlQtext.SetMinSize( wx.Size( 200,-1 ) )
		
		fgSizer5.Add( self.m_textCtrlQtext, 1, wx.ALL, 5 )
		
		self.m_textCtrlQpic = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[3], wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_textCtrlQpic.SetMinSize( wx.Size( 200,-1 ) )
		
		fgSizer5.Add( self.m_textCtrlQpic, 0, wx.ALL, 5 )
		
		self.m_staticText56 = wx.StaticText( self.m_panel32, wx.ID_ANY, u"Answer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText56.Wrap( -1 )
		self.m_staticText56.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		fgSizer5.Add( self.m_staticText56, 0, wx.ALL, 5 )
		
		self.m_textCtrlAtext = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[4], wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlAtext.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_textCtrlAtext.SetMinSize( wx.Size( 200,-1 ) )
		
		fgSizer5.Add( self.m_textCtrlAtext, 0, wx.ALL, 5 )
		
		self.m_textCtrlApic = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[5], wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlApic.SetMinSize( wx.Size( 200,-1 ) )
		
		fgSizer5.Add( self.m_textCtrlApic, 0, wx.ALL, 5 )
		
		self.m_staticText68 = wx.StaticText( self.m_panel32, wx.ID_ANY, u"Topic", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText68.Wrap( -1 )
		self.m_staticText68.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		fgSizer5.Add( self.m_staticText68, 0, wx.ALL, 5 )
		
		self.m_textCtrlTopic = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[6], wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlTopic.SetMinSize( wx.Size( 200,-1 ) )
		
		fgSizer5.Add( self.m_textCtrlTopic, 0, wx.ALL, 5 )
		
		bSizer113 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText74 = wx.StaticText( self.m_panel32, wx.ID_ANY, u"Delete card: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText74.Wrap( -1 )
		self.m_staticText74.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer113.Add( self.m_staticText74, 0, wx.ALL, 5 )
		
		self.m_checkBoxDel = wx.CheckBox( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer113.Add( self.m_checkBoxDel, 0, wx.ALL, 5 )
		
		
		fgSizer5.Add( bSizer113, 1, wx.EXPAND, 5 )
		
		
		bSizer1111.Add( fgSizer5, 0, wx.EXPAND, 5 )
		
		
		bSizer1111.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer79.Add( bSizer1111, 0, wx.EXPAND, 5 )
		
		self.m_staticline11 = wx.StaticLine( self.m_panel32, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer79.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer80 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer80.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button22 = wx.Button( self.m_panel32, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button22.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer80.Add( self.m_button22, 0, wx.ALL, 5 )
		
		
		bSizer80.Add( ( 10, 0), 0, wx.EXPAND, 5 )
		
		self.m_button23 = wx.Button( self.m_panel32, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button23.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer80.Add( self.m_button23, 0, wx.ALL, 5 )
		
		
		bSizer80.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer79.Add( bSizer80, 0, wx.EXPAND, 5 )
		
		
		self.m_panel32.SetSizer( bSizer79 )
		self.m_panel32.Layout()
		bSizer79.Fit( self.m_panel32 )
		bSizer78.Add( self.m_panel32, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer78 )
		self.Layout()
		bSizer78.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class MyDialogScore
###########################################################################

class MyDialogScore ( wx.Dialog ):
	
	def __init__( self, parent, data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Result", pos = wx.DefaultPosition, size = wx.Size( 290,117 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer159 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel64 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer160 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer162 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_textCtrl51Score = wx.TextCtrl( self.m_panel64, wx.ID_ANY, data, wx.DefaultPosition, wx.Size( 200,-1 ), 0|wx.NO_BORDER )
		self.m_textCtrl51Score.SetFont( wx.Font( 14, 74, 90, 90, False, "Verdana" ) )
		self.m_textCtrl51Score.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		
		bSizer162.Add( self.m_textCtrl51Score, 1, wx.ALL, 5 )
		
		
		bSizer160.Add( bSizer162, 0, wx.EXPAND, 5 )
		
		bSizer163 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer163.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button45 = wx.Button( self.m_panel64, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button45.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer163.Add( self.m_button45, 0, wx.ALL, 5 )
		
		
		bSizer163.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer160.Add( bSizer163, 0, wx.EXPAND, 5 )
		
		
		self.m_panel64.SetSizer( bSizer160 )
		self.m_panel64.Layout()
		bSizer160.Fit( self.m_panel64 )
		bSizer159.Add( self.m_panel64, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer159 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class MyDialogAbout
###########################################################################

class MyDialogAbout ( wx.Dialog ):
	
	def __init__( self, parent, data ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"About", pos = wx.DefaultPosition, size = wx.Size( 391,148 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer89 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel33 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer6 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer90 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bitmapAbout = wx.StaticBitmap( self.m_panel33, wx.ID_ANY, data, wx.DefaultPosition, wx.Size( 100,100 ), 0 )
		bSizer90.Add( self.m_bitmapAbout, 0, wx.ALL, 5 )
		
		bSizer91 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText58 = wx.StaticText( self.m_panel33, wx.ID_ANY, u"Flashbook", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText58.Wrap( -1 )
		self.m_staticText58.SetFont( wx.Font( 9, 74, 93, 92, False, "Verdana" ) )
		
		bSizer91.Add( self.m_staticText58, 0, wx.ALL, 0 )
		
		self.m_staticText59 = wx.StaticText( self.m_panel33, wx.ID_ANY, VersionNumber, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText59.Wrap( -1 )
		self.m_staticText59.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer91.Add( self.m_staticText59, 0, wx.ALL, 0 )
		
		self.m_staticText60 = wx.StaticText( self.m_panel33, wx.ID_ANY, u"Author: Anton de Groot", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText60.Wrap( -1 )
		self.m_staticText60.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer91.Add( self.m_staticText60, 0, wx.ALL, 0 )
		
		bSizer92 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText61 = wx.StaticText( self.m_panel33, wx.ID_ANY, u"Github: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		self.m_staticText61.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer92.Add( self.m_staticText61, 0, wx.ALL, 0 )
		
		self.m_hyperlink3 = wx.adv.HyperlinkCtrl( self.m_panel33, wx.ID_ANY, u"Flashbook", u"https://github.com/AntondeGroot/Flashbook", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		self.m_hyperlink3.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer92.Add( self.m_hyperlink3, 0, wx.ALL, 0 )
		
		
		bSizer91.Add( bSizer92, 0, wx.EXPAND, 0 )
		
		bSizer93 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText62 = wx.StaticText( self.m_panel33, wx.ID_ANY, u"Icons:  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )
		self.m_staticText62.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer93.Add( self.m_staticText62, 0, wx.ALL, 0 )
		
		bSizer94 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_hyperlink1 = wx.adv.HyperlinkCtrl( self.m_panel33, wx.ID_ANY, u"doublejdesign", u"http://www.doublejdesign.co.uk", wx.DefaultPosition, wx.DefaultSize, 0 )
		
		self.m_hyperlink1.SetHoverColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		self.m_hyperlink1.SetNormalColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		self.m_hyperlink1.SetVisitedColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		self.m_hyperlink1.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		self.m_hyperlink1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer94.Add( self.m_hyperlink1, 0, wx.ALL, 0 )
		
		self.m_hyperlink2 = wx.adv.HyperlinkCtrl( self.m_panel33, wx.ID_ANY, u"visualpharm", u"https://www.visualpharm.com/free-icons", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		self.m_hyperlink2.SetFont( wx.Font( 9, 74, 90, 90, False, "Verdana" ) )
		
		bSizer94.Add( self.m_hyperlink2, 0, wx.ALL, 0 )
		
		
		bSizer93.Add( bSizer94, 0, wx.EXPAND, 0 )
		
		
		bSizer91.Add( bSizer93, 0, wx.EXPAND, 0 )
		
		self.m_staticText63 = wx.StaticText( self.m_panel33, wx.ID_ANY, u"© 2018 A. de Groot", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText63.Wrap( -1 )
		self.m_staticText63.SetFont( wx.Font( 9, 74, 93, 90, False, "Verdana" ) )
		
		bSizer91.Add( self.m_staticText63, 0, wx.ALL, 0 )
		
		
		bSizer90.Add( bSizer91, 1, wx.EXPAND, 5 )
		
		
		fgSizer6.Add( bSizer90, 1, wx.EXPAND, 5 )
		
		
		self.m_panel33.SetSizer( fgSizer6 )
		self.m_panel33.Layout()
		fgSizer6.Fit( self.m_panel33 )
		bSizer89.Add( self.m_panel33, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer89 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

