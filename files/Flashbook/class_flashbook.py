# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:27:03 2019

@author: Anton
"""
import _GUI.gui_flashbook as gui
import wx
import Flashbook.page as page
import Flashbook.zoom as zoom
import PIL
import program as p
import Flashbook.fb_modules    as m
import Flashbook.events_mouse as mouse
import Flashbook.scrolling as scroll
import _GUI.active_panel as panel
import Books.library as Books
import Flashbook.fb_functions as f
import Print.print_modules as m3
from pathlib import Path
ICON_EXCLAIM=0x30
import _GUI.accelerators_module as acc
import _logging.log_module as log
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
        log.DEBUGLOG(debugmode=self.debugmode,msg=f'STARTUP FLASHBOOK')
        ## initialize
        self.zoom = 1.0
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(wx.Image( 1,1 ))) # always empty bitmap, in case someone reruns the program
        self.m_CurrentPageFB.SetValue('')
        self.m_TotalPagesFB.SetValue('')                      
        self.screenshotmode = False
        self.resetselection = False
        #short cuts
        
        self.m_bitmapScroll.Bind( wx.EVT_RIGHT_DOWN, self.m_resetselectionOnButtonClick )
        self.m_bitmapScroll.Bind( wx.EVT_MIDDLE_DOWN, self.m_enterselectionOnButtonClick )
        # for scrolling: only remember current and last position, append and pop, if the numbers repeat [0,0] or [X,X] then you know you've reached either the beginning or the end of the window: then flip page 
        # initialize variables:
        self.bookname       = ''
        self.booktopic      = ''
        self.booknames      = []
        self.bookindex      = 0
        self.BorderCoords   = []         
        self.colorlist      = self.bordercolors
        self.currentpage    = 1
        self.image          = []
        self.imagecopy      = []
        self.tempdictionary = {}
        self.panel_pos      = (0,0)        
        self.questionmode   = True
        #self.zoom           = 1.0
        self.m_modeDisplay.SetValue("Question:")
        self.m_ZoomFB.SetValue(f"{int(self.zoom*100)}%")  
        #f.ResetQuestions(self)
        page.SetScrollbars(self)
            
        
        self.stitchmode_v = True # stich vertical or horizontal
        self.m_bitmapScroll.SetWindowStyleFlag(False)  # first disable the border of the bitmap, otherwise you get a bordered empty bitmap. Enable the border only when there is a bitmap
        #setup_sources(self)
        panel.SwitchPanel(self,1)      
        acc.AcceleratorTableSetup(self,"flashbook","set")
        ## open window asking user what topic he wants to study
        
        
         
        self.FlashbookLibrary.showdata()
        
        
                  
                
                
    def m_btnScreenshotOnButtonClick( self, event ):
        self.BoolCropped = False # is image cropped
        self.screenshotmode = True
        if isinstance(self.currentpage,int):
            # If you keep pressing 'import screenshot' it should not override 
            # the backup with the string 'prtscr' 
            self.currentpage_backup = self.currentpage
        self.currentpage = 'prtscr'
        f.import_screenshot(self,event)
        
    def m_userInputOnEnterWindow( self, event ):
        log.DEBUGLOG(debugmode=self.debugmode,msg=f'CLASS FLASHBOOK: user entered window')
        acc.AcceleratorTableSetup(self,"flashbook","textwindow")
	
    def m_userInputOnLeaveWindow( self, event ):
        acc.AcceleratorTableSetup(self,"flashbook","set")
    
    def m_btnUndoChangesOnButtonClick( self, event ):
        if hasattr(self,"backupimage"):
            image3 = self.backupimage
            self.m_bitmap4.SetBitmap(image3)
        self.Layout()
    
    def m_btnImportScreenshotOnButtonClick( self, event ):
        self.screenshotmode = True
        #load screenshot
        
        img = PIL.Image.open(str(Path(self.tempdir,"screenshot.png")))
        self.pageimagecopy = img
        self.pageimage = img        
        image2 = wx.Image( self.width, self.height )
        image2.SetData( self.pageimage.tobytes() )
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        panel.SwitchPanel(self,1)
        f.ShowPrintScreen(self)
        
        
    def m_bitmap4OnLeftDown( self, event ):
        self.panel4_pos = self.m_bitmap4.ScreenToClient(wx.GetMousePosition())
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        
    def m_bitmap4OnLeftUp( self, event ):
        m.panel4_bitmapleftup(self,event)   
        self.panel4.Layout()
        self.Update()
        self.Refresh()       
    
	# zoom in 
    def m_toolPlusFBOnToolClicked( self, event ):
        zoom.zoomin(self,event)
	
    def m_toolMinFBOnToolClicked( self, event ):
        zoom.zoomout(self,event)
	
    # change page 
    def m_pageBackFBOnToolClicked( self, event ):
        self.screenshotmode = False
        page.previouspage(self,event)
	
    def m_pageNextFBOnToolClicked( self, event ):
        self.screenshotmode = False
        page.nextpage(self,event)
    def m_pageUPOnToolClicked( self, event ):
        m.arrowscroll(self,event,'up')
            
    def m_pageDOWNOnToolClicked( self, event ):
        m.arrowscroll(self,event,'down')        
    
    def m_CurrentPageFBOnEnterWindow( self, event ):
        acc.AcceleratorTableSetup(self,"flashbook","pagewindow")
        
    def m_CurrentPageFBOnLeaveWindow( self, event ):
        acc.AcceleratorTableSetup(self,"flashbook","set")
        try:
            self.currentpage = int(self.m_CurrentPageFB.GetValue())
        except:
            self.currentpage = 1
        page.switchpage(self,event)
    
    
    def m_bitmapScrollOnMouseWheel( self, event ):
        scroll.mousewheel(self,event)
        event.Skip()
        
	# draw borders 
    def m_bitmapScrollOnLeftDown( self, event ):
        self.panel_pos = self.m_bitmapScroll.ScreenToClient(wx.GetMousePosition())
        self.mousepos = wx.GetMousePosition() # absolute position
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        event.Skip()
        
    def m_bitmapScrollOnLeftUp( self, event ):
        mouse.bitmapleftup(self,event)   
        event.Skip()
        
    def m_toolStitchOnButtonClick( self, event ):
        self.stitchmode_v =  not self.stitchmode_v
        if self.stitchmode_v:
            f.SetToolStitchArrow(self,orientation="vertical")
        else:
            f.SetToolStitchArrow(self,orientation="horizontal")
        
        """The following is used to create a mozaic of ictures. There is a question mode and an answer mode
        The pics are stored in a list, and when the element of a list is another list it means that particular list is ment to be stitched horizontally
        while all the other elements are stitched vertically
        all it does is switch [a,...,[x]] for [a,...,x] and back to [a,...,[x]] depending on whether the user has pushed a button to change the direction in which the notes should be stitched together.  """
        
        if hasattr(self,'bookname') and self.bookname: # a book has been chosen
            self.Flashcard.StitchCards(self.stitchmode_v)
