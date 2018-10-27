# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

# solving errors: 
# - path_min /  path_add / path_switch are given a full path string, replace those by their respective variables: path_min,path_add,path_switch
# - Spacers have changed resulting in an error: replace AddSpacer() with simply Add()

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
## Class MyFrame
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class MyFrame
###########################################################################

class MyFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FlashBook", pos = wx.DefaultPosition, size = wx.Size( 1155,646 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menuOpen = wx.Menu()
		self.m_menuItemFlashbook = wx.MenuItem( self.m_menuOpen, wx.ID_ANY, u"Open Flashbook Folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuOpen.AppendItem( self.m_menuItemFlashbook )
		
		self.m_menuItemBackToMain = wx.MenuItem( self.m_menuOpen, wx.ID_ANY, u"Open Flashbook / Flashcard", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuOpen.AppendItem( self.m_menuItemBackToMain )
		
		self.m_menubar1.Append( self.m_menuOpen, u"Open" ) 
		
		self.m_menu2 = wx.Menu()
		self.m_menuHelp = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"How to use ...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.AppendItem( self.m_menuHelp )
		
		self.m_menubar1.Append( self.m_menu2, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel0 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel0.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer71.Add( ( 100, 0), 0, 0, 5 )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		
		gSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		gSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText9 = wx.StaticText( self.panel0, wx.ID_ANY, u"Read a book", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		gSizer1.Add( self.m_staticText9, 0, wx.ALL, 5 )
		
		self.m_btnOpenFlashbook = wx.Button( self.panel0, wx.ID_ANY, u"Open Flashbook", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_btnOpenFlashbook.SetMinSize( wx.Size( 110,-1 ) )
		self.m_btnOpenFlashbook.SetMaxSize( wx.Size( 110,-1 ) )
		
		gSizer1.Add( self.m_btnOpenFlashbook, 0, wx.ALL, 5 )
		
		self.m_staticText10 = wx.StaticText( self.panel0, wx.ID_ANY, u"Study the notes you took", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		gSizer1.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		self.m_btnOpenFlashcard = wx.Button( self.panel0, wx.ID_ANY, u"Open Flashcard", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_btnOpenFlashcard.SetMinSize( wx.Size( 110,-1 ) )
		self.m_btnOpenFlashcard.SetMaxSize( wx.Size( 110,-1 ) )
		
		gSizer1.Add( self.m_btnOpenFlashcard, 0, wx.ALL, 5 )
		
		self.m_staticText11 = wx.StaticText( self.panel0, wx.ID_ANY, u"Save the notes you took \n in a pdf", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		gSizer1.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.m_btnPrintNotes = wx.Button( self.panel0, wx.ID_ANY, u"Print", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_btnPrintNotes.SetMinSize( wx.Size( 110,-1 ) )
		self.m_btnPrintNotes.SetMaxSize( wx.Size( 110,-1 ) )
		
		gSizer1.Add( self.m_btnPrintNotes, 0, wx.ALL, 5 )
		
		
		bSizer71.Add( gSizer1, 0, 0, 5 )
		
		
		self.panel0.SetSizer( bSizer71 )
		self.panel0.Layout()
		bSizer71.Fit( self.panel0 )
		bSizer7.Add( self.panel0, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel11 = wx.Panel( self.panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel11.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_toolBar1 = wx.ToolBar( self.panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_dirPicker1 = wx.DirPickerCtrl( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		self.m_toolBar1.AddControl( self.m_dirPicker1 )
		self.m_toolPlus = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"plus", wx.Bitmap( path_add, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolMin = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"min", wx.Bitmap( path_min, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_Zoom = wx.TextCtrl( self.m_toolBar1, wx.ID_ANY, u"100%", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_toolBar1.AddControl( self.m_Zoom )
		self.m_toolBack = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_BACK,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolNext = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_staticText3 = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u"Page: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		self.m_toolBar1.AddControl( self.m_staticText3 )
		self.m_CurrentPage = wx.TextCtrl( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_CENTRE )
		self.m_CurrentPage.SetMinSize( wx.Size( 10,-1 ) )
		self.m_CurrentPage.SetMaxSize( wx.Size( 10,-1 ) )
		
		self.m_toolBar1.AddControl( self.m_CurrentPage )
		self.m_staticText6 = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u" of ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_toolBar1.AddControl( self.m_staticText6 )
		self.m_TotalPages = wx.TextCtrl( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_TotalPages.SetMinSize( wx.Size( 20,-1 ) )
		self.m_TotalPages.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar1.AddControl( self.m_TotalPages )
		self.m_TotalPage = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u"      Show Selections  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_TotalPage.Wrap( -1 )
		self.m_toolBar1.AddControl( self.m_TotalPage )
		self.m_checkBox1 = wx.CheckBox( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox1.SetValue(True) 
		self.m_toolBar1.AddControl( self.m_checkBox1 )
		self.m_staticText5 = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u"      Cross-hair cursor   ", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_toolBar1.AddControl( self.m_staticText5 )
		self.m_checkBoxCursor = wx.CheckBox( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_toolBar1.AddControl( self.m_checkBoxCursor )
		self.m_toolBar1.Realize() 
		
		bSizer2.Add( self.m_toolBar1, 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		
		self.m_staticline2 = wx.StaticLine( self.panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline2, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.m_scrolledWindow1 = wx.ScrolledWindow( self.panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmapScroll = wx.StaticBitmap( self.m_scrolledWindow1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_bitmapScroll, 0, wx.ALL, 5 )
		
		
		self.m_scrolledWindow1.SetSizer( bSizer5 )
		self.m_scrolledWindow1.Layout()
		bSizer5.Fit( self.m_scrolledWindow1 )
		bSizer2.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_textCtrl1 = wx.TextCtrl( self.panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer3.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self.panel11, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl2.SetMinSize( wx.Size( 400,-1 ) )
		
		bSizer3.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
		
		self.m_enterselection = wx.Button( self.panel11, wx.ID_ANY, u"Enter Selection", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_enterselection, 0, wx.ALL, 5 )
		
		self.m_staticline3 = wx.StaticLine( self.panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer3.Add( self.m_staticline3, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 2000 )
		
		self.m_resetselection = wx.Button( self.panel11, wx.ID_ANY, u"Reset Selection", wx.DefaultPosition, wx.DefaultSize, 0 )
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
		self.m_dirPicker1 = wx.DirPickerCtrl( self.m_toolBar2, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		self.m_toolBar2.AddControl( self.m_dirPicker1 )
		self.m_toolPlus = self.m_toolBar2.AddLabelTool( wx.ID_ANY, u"plus", wx.Bitmap( path_add, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolMin = self.m_toolBar2.AddLabelTool( wx.ID_ANY, u"min", wx.Bitmap( path_min, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_Zoom = wx.TextCtrl( self.m_toolBar2, wx.ID_ANY, u"100%", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_toolBar2.AddControl( self.m_Zoom )
		self.m_toolBack = self.m_toolBar2.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_BACK,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolNext = self.m_toolBar2.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_staticText31 = wx.StaticText( self.m_toolBar2, wx.ID_ANY, u"Page: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		self.m_toolBar2.AddControl( self.m_staticText31 )
		self.m_CurrentPage = wx.TextCtrl( self.m_toolBar2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_CENTRE )
		self.m_CurrentPage.SetMinSize( wx.Size( 10,-1 ) )
		self.m_CurrentPage.SetMaxSize( wx.Size( 10,-1 ) )
		
		self.m_toolBar2.AddControl( self.m_CurrentPage )
		self.m_staticText61 = wx.StaticText( self.m_toolBar2, wx.ID_ANY, u" of ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		self.m_toolBar2.AddControl( self.m_staticText61 )
		self.m_TotalPages = wx.TextCtrl( self.m_toolBar2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_TotalPages.SetMinSize( wx.Size( 20,-1 ) )
		self.m_TotalPages.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar2.AddControl( self.m_TotalPages )
		self.m_staticText41 = wx.StaticText( self.m_toolBar2, wx.ID_ANY, u"      Show Selections  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		self.m_toolBar2.AddControl( self.m_staticText41 )
		self.m_checkBox1 = wx.CheckBox( self.m_toolBar2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox1.SetValue(True) 
		self.m_toolBar2.AddControl( self.m_checkBox1 )
		self.m_staticText51 = wx.StaticText( self.m_toolBar2, wx.ID_ANY, u"      Cross-hair cursor   ", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText51.Wrap( -1 )
		self.m_toolBar2.AddControl( self.m_staticText51 )
		self.m_checkBoxCursor = wx.CheckBox( self.m_toolBar2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_toolBar2.AddControl( self.m_checkBoxCursor )
		self.m_toolBar2.Realize() 
		
		bSizer21.Add( self.m_toolBar2, 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		
		self.m_staticline21 = wx.StaticLine( self.panel12, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer21.Add( self.m_staticline21, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.m_richText1 = wx.richtext.RichTextCtrl( self.panel12, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer21.Add( self.m_richText1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
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
		self.m_filePicker = wx.FilePickerCtrl( self.m_toolBar3, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.tex*", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar3.AddControl( self.m_filePicker )
		self.m_toolSwitch = self.m_toolBar3.AddLabelTool( wx.ID_ANY, u"Switch", wx.Bitmap( path_switch, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_textCtrlMode = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, u"Question:", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.NO_BORDER )
		self.m_toolBar3.AddControl( self.m_textCtrlMode )
		self.m_CurrentPage = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_CENTRE|wx.TE_READONLY )
		self.m_CurrentPage.SetMinSize( wx.Size( 10,-1 ) )
		self.m_CurrentPage.SetMaxSize( wx.Size( 10,-1 ) )
		
		self.m_toolBar3.AddControl( self.m_CurrentPage )
		self.m_staticText611 = wx.StaticText( self.m_toolBar3, wx.ID_ANY, u" of ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText611.Wrap( -1 )
		self.m_toolBar3.AddControl( self.m_staticText611 )
		self.m_TotalPages = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY )
		self.m_TotalPages.SetMinSize( wx.Size( 20,-1 ) )
		self.m_TotalPages.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar3.AddControl( self.m_TotalPages )
		self.m_staticText311 = wx.StaticText( self.m_toolBar3, wx.ID_ANY, u"    Score: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText311.Wrap( -1 )
		self.m_toolBar3.AddControl( self.m_staticText311 )
		self.m_Score = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.NO_BORDER )
		self.m_Score.SetMaxSize( wx.Size( 20,-1 ) )
		
		self.m_toolBar3.AddControl( self.m_Score )
		self.m_toolPlus = self.m_toolBar3.AddLabelTool( wx.ID_ANY, u"plus", wx.Bitmap( path_add, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolMin = self.m_toolBar3.AddLabelTool( wx.ID_ANY, u"min", wx.Bitmap( path_min, wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_Zoom = wx.TextCtrl( self.m_toolBar3, wx.ID_ANY, u"100%", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		self.m_toolBar3.AddControl( self.m_Zoom )
		self.m_toolBar3.Realize() 
		
		bSizer211.Add( self.m_toolBar3, 0, wx.ALIGN_CENTER|wx.EXPAND, 0 )
		
		self.m_staticline22 = wx.StaticLine( self.panel21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer211.Add( self.m_staticline22, 0, wx.EXPAND |wx.ALL, 5 )
		
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
		bSizer31.Add( self.m_buttonCorrect, 1, wx.ALL|wx.EXPAND|wx.RIGHT, 5 )
		
		self.m_buttonWrong = wx.Button( self.panel21, wx.ID_ANY, u"Wrong", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_buttonWrong, 1, wx.ALL|wx.EXPAND|wx.LEFT, 5 )
		
		
		bSizer211.Add( bSizer31, 0, wx.EXPAND, 5 )
		
		
		self.panel21.SetSizer( bSizer211 )
		self.panel21.Layout()
		bSizer211.Fit( self.panel21 )
		bSizer81.Add( self.panel21, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.panel22 = wx.Panel( self.panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel22.SetBackgroundColour( wx.Colour( 254, 240, 231 ) )
		
		bSizer22 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_richText11 = wx.richtext.RichTextCtrl( self.panel22, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer22.Add( self.m_richText11, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.panel22.SetSizer( bSizer22 )
		self.panel22.Layout()
		bSizer22.Fit( self.panel22 )
		bSizer81.Add( self.panel22, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.panel2.SetSizer( bSizer81 )
		self.panel2.Layout()
		bSizer81.Fit( self.panel2 )
		bSizer7.Add( self.panel2, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer7 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.m_menuItemFlashbookOnMenuSelection, id = self.m_menuItemFlashbook.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuItemBackToMainOnMenuSelection, id = self.m_menuItemBackToMain.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuHelpOnMenuSelection, id = self.m_menuHelp.GetId() )
		self.m_btnOpenFlashbook.Bind( wx.EVT_BUTTON, self.m_btnOpenFlashbookOnButtonClick )
		self.m_btnOpenFlashcard.Bind( wx.EVT_BUTTON, self.m_btnOpenFlashcardOnButtonClick )
		self.m_btnPrintNotes.Bind( wx.EVT_BUTTON, self.m_btnPrintNotesOnButtonClick )
		self.m_dirPicker1.Bind( wx.EVT_DIRPICKER_CHANGED, self.m_dirPicker1OnDirChanged )
		self.Bind( wx.EVT_TOOL, self.m_toolPlusOnToolClicked, id = self.m_toolPlus.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolMinOnToolClicked, id = self.m_toolMin.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolBackOnToolClicked, id = self.m_toolBack.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolNextOnToolClicked, id = self.m_toolNext.GetId() )
		self.m_CurrentPage.Bind( wx.EVT_KEY_DOWN, self.m_PageCtrlOnKeyDown )
		self.m_CurrentPage.Bind( wx.EVT_KEY_UP, self.m_PageCtrlOnKeyUp )
		self.m_CurrentPage.Bind( wx.EVT_TEXT, self.m_CurrentPageOnText )
		self.m_checkBox1.Bind( wx.EVT_CHECKBOX, self.m_checkBox1OnCheckBox )
		self.m_checkBoxCursor.Bind( wx.EVT_CHECKBOX, self.m_checkBoxCursorOnCheckBox )
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
		self.m_enterselection.Bind( wx.EVT_BUTTON, self.m_enterselectionOnButtonClick )
		self.m_resetselection.Bind( wx.EVT_BUTTON, self.m_resetselectionOnButtonClick )
		self.m_dirPicker1.Bind( wx.EVT_DIRPICKER_CHANGED, self.m_dirPicker1OnDirChanged )
		self.Bind( wx.EVT_TOOL, self.m_toolPlusOnToolClicked, id = self.m_toolPlus.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolMinOnToolClicked, id = self.m_toolMin.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolBackOnToolClicked, id = self.m_toolBack.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolNextOnToolClicked, id = self.m_toolNext.GetId() )
		self.m_CurrentPage.Bind( wx.EVT_KEY_DOWN, self.m_PageCtrlOnKeyDown )
		self.m_CurrentPage.Bind( wx.EVT_KEY_UP, self.m_PageCtrlOnKeyUp )
		self.m_CurrentPage.Bind( wx.EVT_TEXT, self.m_CurrentPageOnText )
		self.m_checkBox1.Bind( wx.EVT_CHECKBOX, self.m_checkBox1OnCheckBox )
		self.m_checkBoxCursor.Bind( wx.EVT_CHECKBOX, self.m_checkBoxCursorOnCheckBox )
		self.m_richText1.Bind( wx.EVT_LEFT_DOWN, self.m_richText1OnLeftDown )
		self.m_filePicker.Bind( wx.EVT_FILEPICKER_CHANGED, self.m_filePickerOnFileChanged )
		self.Bind( wx.EVT_TOOL, self.m_toolSwitchOnToolClicked, id = self.m_toolSwitch.GetId() )
		self.m_CurrentPage.Bind( wx.EVT_KEY_DOWN, self.m_PageCtrlOnKeyDown )
		self.m_CurrentPage.Bind( wx.EVT_KEY_UP, self.m_PageCtrlOnKeyUp )
		self.m_CurrentPage.Bind( wx.EVT_TEXT, self.m_CurrentPageOnText )
		self.Bind( wx.EVT_TOOL, self.m_toolPlusOnToolClicked, id = self.m_toolPlus.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolMinOnToolClicked, id = self.m_toolMin.GetId() )
		self.m_bitmapScroll1.Bind( wx.EVT_LEFT_DOWN, self.m_bitmapScrollOnLeftDown )
		self.m_bitmapScroll1.Bind( wx.EVT_LEFT_UP, self.m_bitmapScrollOnLeftUp )
		self.m_bitmapScroll1.Bind( wx.EVT_MOTION, self.m_bitmapScrollOnMotion )
		self.m_bitmapScroll1.Bind( wx.EVT_LEFT_DOWN, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_LEFT_UP, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MIDDLE_DOWN, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MIDDLE_UP, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_RIGHT_DOWN, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_RIGHT_UP, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MOTION, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_LEFT_DCLICK, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MIDDLE_DCLICK, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_RIGHT_DCLICK, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_LEAVE_WINDOW, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_ENTER_WINDOW, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MOUSEWHEEL, self.m_bitmapScrollOnMouseEvents )
		self.m_bitmapScroll1.Bind( wx.EVT_MOUSEWHEEL, self.m_bitmapScrollOnMouseWheel )
		self.m_bitmapScroll1.Bind( wx.EVT_RIGHT_DOWN, self.m_bitmapScrollOnRightDown )
		self.m_buttonCorrect.Bind( wx.EVT_BUTTON, self.m_buttonCorrectOnButtonClick )
		self.m_buttonWrong.Bind( wx.EVT_BUTTON, self.m_buttonWrongOnButtonClick )
		self.m_richText11.Bind( wx.EVT_LEFT_DOWN, self.m_richText1OnLeftDown )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_menuItemFlashbookOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuItemBackToMainOnMenuSelection( self, event ):
		event.Skip()
	
	def m_menuHelpOnMenuSelection( self, event ):
		event.Skip()
	
	def m_btnOpenFlashbookOnButtonClick( self, event ):
		event.Skip()
	
	def m_btnOpenFlashcardOnButtonClick( self, event ):
		event.Skip()
	
	def m_btnPrintNotesOnButtonClick( self, event ):
		event.Skip()
	
	def m_dirPicker1OnDirChanged( self, event ):
		event.Skip()
	
	def m_toolPlusOnToolClicked( self, event ):
		event.Skip()
	
	def m_toolMinOnToolClicked( self, event ):
		event.Skip()
	
	def m_toolBackOnToolClicked( self, event ):
		event.Skip()
	
	def m_toolNextOnToolClicked( self, event ):
		event.Skip()
	
	def m_PageCtrlOnKeyDown( self, event ):
		event.Skip()
	
	def m_PageCtrlOnKeyUp( self, event ):
		event.Skip()
	
	def m_CurrentPageOnText( self, event ):
		event.Skip()
	
	def m_checkBox1OnCheckBox( self, event ):
		event.Skip()
	
	def m_checkBoxCursorOnCheckBox( self, event ):
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
	
	def m_enterselectionOnButtonClick( self, event ):
		event.Skip()
	
	def m_resetselectionOnButtonClick( self, event ):
		event.Skip()
	
	
	
	
	
	
	
	
	
	
	
	def m_richText1OnLeftDown( self, event ):
		event.Skip()
	
	def m_filePickerOnFileChanged( self, event ):
		event.Skip()
	
	def m_toolSwitchOnToolClicked( self, event ):
		event.Skip()
	
	
	
	
	
	
	
	
	
	
	
	
	def m_buttonCorrectOnButtonClick( self, event ):
		event.Skip()
	
	def m_buttonWrongOnButtonClick( self, event ):
		event.Skip()
	