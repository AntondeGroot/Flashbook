# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:44:11 2019

@author: Anton
"""
import gui_flashbook as gui
import wx
import program as p
import fc_functions    as f2
import fc_modules as m2
ICON_EXCLAIM=0x30
import accelerators_module as m7
import os
import ctypes
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100

def SaveTime(self):
    if hasattr(self,'TC') and hasattr(self,'bookname') and self.bookname != '':
        self.TC.update() 

class flashcard(gui.MyFrame):
    def __init__(self):
        pass
    def m_OpenFlashcardOnButtonClick( self, event ):
        """START MAIN PROGRAM : FLASCARD"""
        # set all directories
        os.chdir(self.notesdir)                
        dirs = [self.appdir,self.notesdir,self.picsdir,self.booksdir,self.tempdir,self.bordersdir,self.resourcedir]        
        print("="*90)
        print(f"\nThe files will be saved to the following directory: {self.appdir}\n")     
        for dir_ in dirs:
            if not dir_.exists():
                dir_.mkdir()
                    
        # initialize variables:
        self.bookname       = ''
        self.image          = []
        self.panel_pos      = (0,0)        
        self.zoom           = 1.0
        self.m_ZoomFC.SetValue(f"{int(self.zoom*100)}%")  
        #
        self.runprogram = True
        self.SwitchCard = True
        self.index = 0
        self.score = 0
        self.nr_questions = 0
        self.mode = 'Question'
        self.m_modeDisplayFC.SetValue(self.mode)
        self.cardorder   = []        
        self.questions   = []
        self.answers     = []
        self.questions2  = []
        f2.SetScrollbars_fc(self)
        
        self.NEWCARD = True
        m7.AcceleratorTableSetup(self,"flashcard","set")
        p.SwitchPanel(self,2)
        with wx.FileDialog(self, "Choose a subject to study",defaultDir=str(self.notesdir), wildcard="*.tex",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                #the user changed their mind
                p.SwitchPanel(self,0) 
                return None    
            else:
                self.m_menubar1.EnableTop(2,True)
                filepath = fileDialog.GetPaths()
                m2.startprogram(self,filepath)
    # button events
    def m_buttonCorrectOnButtonClick( self, event ): 
        
        m2.buttonCorrect(self)
        SaveTime(self)
        event.Skip()
    def m_bitmapScrollFCOnLeftUp( self, event ):
        m2.buttonCorrect(self)
        event.Skip()
    
    # flip flashcard
    def m_toolSwitchOnToolClicked( self, event ):
        m2.switchCard(self)
        SaveTime(self)
        event.Skip()
    
    def m_scrolledWindow11OnLeftUp( self, event ):
        m2.buttonCorrect(self)
        event.Skip()
        
    def m_scrolledWindow11OnRightUp( self, event ):
        m2.buttonWrong(self)
        event.Skip()
        
    def m_scrolledWindow11OnMouseWheel( self, event ):
        m2.switchCard(self)
        event.Skip()
    
    def m_buttonWrongOnButtonClick( self, event ):
        m2.buttonWrong(self)
        SaveTime(self)
        event.Skip()
        
    def m_bitmapScrollFCOnRightUp( self, event ):
        m2.buttonWrong(self)   
        event.Skip()
	
    def m_toolSwitchFCOnToolClicked( self, event ):
        m2.switchCard(self)
	
    def m_bitmapScrollFCOnMouseWheel( self, event ):
        m2.switchCard(self)
