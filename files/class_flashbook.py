# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:27:03 2019

@author: Anton
"""
import gui_flashbook as gui
import threading
import wx
import PIL
import program as p
import fc_functions    as f2
import fb_modules    as m
import fb_functions as f
import print_modules as m3
from pathlib import Path
from latexoperations import Commands as cmd
import log_module    as log
ICON_EXCLAIM=0x30
import accelerators_module as m7
import ctypes
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100

class flashbook(gui.MyFrame):
    def __init__(self):
        pass
    
    def m_OpenFlashbookOnButtonClick( self, event ):
        """START MAIN PROGRAM : FLASHBOOK"""
        self.stayonpage = False
        self.stitchmode_v = True # stich vertical or horizontal
        self.m_bitmapScroll.SetWindowStyleFlag(False)  # first disable the border of the bitmap, otherwise you get a bordered empty bitmap. Enable the border only when there is a bitmap
        #setup_sources(self)
        p.SwitchPanel(self,1)      
        m7.AcceleratorTableSetup(self,"flashbook","set")
        p.run_flashbook(self)
        with wx.DirDialog(self, "Choose which book to open",style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST,defaultPath=str(self.booksdir)) as DirDialog:
            #fileDialog.SetPath(str(self.notesdir)+'\.')
            if DirDialog.ShowModal() == wx.ID_CANCEL:
                p.SwitchPanel(self,0) 
                return None    # the user changed their mind
            else:
                dirpath = DirDialog.GetPath()
                print(f"opened dirdialog {dirpath}")
                m.dirchanged(self,dirpath)
    def m_btnScreenshotOnButtonClick( self, event ):
        self.BoolCropped = False # is image cropped
        self.currentpage_backup = self.currentpage
        self.currentpage = 'prtscr'
        m3.import_screenshot(self,event)
        
    def m_userInputOnEnterWindow( self, event ):
        print("entered window")
        m7.AcceleratorTableSetup(self,"flashbook","textwindow")
	
    def m_userInputOnLeaveWindow( self, event ):
        m7.AcceleratorTableSetup(self,"flashbook","set")
    
    def m_btnUndoChangesOnButtonClick( self, event ):
        if hasattr(self,"backupimage"):
            image3 = self.backupimage
            self.m_bitmap4.SetBitmap(image3)
        self.Layout()
    
    def m_btnImportScreenshotOnButtonClick( self, event ):
        self.stayonpage = True
        #load screenshot
        if self.BoolCropped == False: #load original screenshot
            img = PIL.Image.open(str(Path(self.tempdir,"screenshot.png")))
            self.pageimagecopy = img
            self.pageimage = img        
            image2 = wx.Image( self.width, self.height )
            image2.SetData( self.pageimage.tobytes() )
            self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        p.SwitchPanel(self,1)
        f.ShowPrintScreen(self)
        
        
    def m_bitmap4OnLeftDown( self, event ):
        self.panel4_pos = self.m_bitmap4.ScreenToClient(wx.GetMousePosition())
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        
    def m_bitmap4OnLeftUp( self, event ):
        m.panel4_bitmapleftup(self,event)   
        self.panel4.Layout()
        self.Update()
        self.Refresh()       
    
	# zoom in #================================================================
    def m_toolPlusFBOnToolClicked( self, event ):
        m.zoomin(self,event)
	
    def m_toolMinFBOnToolClicked( self, event ):
        m.zoomout(self,event)
	
    # change page #============================================================
    def m_pageBackFBOnToolClicked( self, event ):
        self.stayonpage = False
        m.previouspage(self,event)
	
    def m_pageNextFBOnToolClicked( self, event ):
        self.stayonpage = False
        m.nextpage(self,event)
    def m_pageUPOnToolClicked( self, event ):
        m.arrowscroll(self,event,'up')
            
    def m_pageDOWNOnToolClicked( self, event ):
        m.arrowscroll(self,event,'down')        
    
    def m_CurrentPageFBOnEnterWindow( self, event ):
        m7.AcceleratorTableSetup(self,"flashbook","pagewindow")
        
    def m_CurrentPageFBOnLeaveWindow( self, event ):
        m7.AcceleratorTableSetup(self,"flashbook","set")
        try:
            self.currentpage = int(self.m_CurrentPageFB.GetValue())
        except:
            self.currentpage = 1
        m.switchpage(self,event)
    
    
    def m_bitmapScrollOnMouseWheel( self, event ):
        m.mousewheel(self,event)
        event.Skip()
        
	# draw borders #===========================================================
    def m_bitmapScrollOnLeftDown( self, event ):
        self.panel_pos = self.m_bitmapScroll.ScreenToClient(wx.GetMousePosition())
        self.mousepos = wx.GetMousePosition() # absolute position
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        event.Skip()
        
    def m_bitmapScrollOnLeftUp( self, event ):
        m.bitmapleftup(self,event)   
        event.Skip()
        
    def m_toolStitchOnButtonClick( self, event ):
        self.stitchmode_v =  not self.stitchmode_v
        if self.stitchmode_v == True:
            f.SetToolStitchArrow(self,orientation="vertical")
        else:
            f.SetToolStitchArrow(self,orientation="horizontal")
        
        """The following is used to create a mozaic of ictures. There is a question mode and an answer mode
        The pics are stored in a list, and when the element of a list is another list it means that particular list is ment to be stitched horizontally
        while all the other elements are stitched vertically
        all it does is switch [a,...,[x]] for [a,...,x] and back to [a,...,[x]] depending on whether the user has pushed a button to change the direction in which the notes should be stitched together.  """
        
        if hasattr(self,'bookname') and self.bookname != '': # a book has been chosen
            self.Flashcard.StitchCards(self.stitchmode_v)