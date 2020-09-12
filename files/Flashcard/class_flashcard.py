# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:44:11 2019

@author: Anton
"""
import _GUI.gui_flashbook as gui
import wx
import Flashcard.fc_functions    as f2
import Flashcard.card as card
import _GUI.active_panel as panel
import Flashcard.fc_modules as m2
import Flashcard.buttons as button
ICON_EXCLAIM=0x30
import _GUI.accelerators_module as acc
import os
import ctypes
import _logging.log_module as log

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
        log.DEBUGLOG(debugmode=self.debugmode,msg=f"STARTUP FLASHCARD")
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
        acc.AcceleratorTableSetup(self,"flashcard","set")
        panel.SwitchPanel(self,2)
        
        #%%
        # When Flashbook is run in the Spyder IDE it may not open the correct folder, this however is no problem when it is run
        #       as an executable. In that case the whole 'defaultFile' isn't even necessary.
        #       when the defaultdir and the defaultfile match: it will open the dir one above the one you actually want to open
        #       if the defaultfile is a file within the defaultdir it works as it should be. In this case it is not a problem
        #       because there's always 1 file present.
        if os.listdir(self.notesdir) != []:
            defaultfile = os.path.join(self.notesdir,os.listdir(self.notesdir)[0])
        else:
            defaultfile = self.notesdir
        #%%
        
        with wx.FileDialog(self, "Choose a subject to study",defaultDir=str(self.notesdir),defaultFile = defaultfile, wildcard="*.bok",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                #the user changed their mind
                panel.SwitchPanel(self,0) 
                return None    
            else:
                self.m_menubar1.EnableTop(2,True)
                filepath = fileDialog.GetPaths()
                m2.startprogram(self,filepath)
    # button events
    def m_buttonCorrectOnButtonClick( self, event ):  
        button.buttonCorrect(self)
        SaveTime(self)
        event.Skip()
        
    def m_bitmapScrollFCOnLeftUp( self, event ):
        button.buttonCorrect(self)
        event.Skip()
    
    # flip flashcard
    def m_toolSwitchOnToolClicked( self, event ):
        card.switchCard(self)
        SaveTime(self)
        event.Skip()
    
    def m_scrolledWindow11OnLeftUp( self, event ):
        button.buttonCorrect(self)
        event.Skip()
        
    def m_scrolledWindow11OnRightUp( self, event ):
        button.buttonWrong(self)
        event.Skip()
        
    def m_scrolledWindow11OnMouseWheel( self, event ):
        card.switchCard(self)
        event.Skip()
    
    def m_buttonWrongOnButtonClick( self, event ):
        button.buttonWrong(self)
        SaveTime(self)
        event.Skip()
        
    def m_bitmapScrollFCOnRightUp( self, event ):
        button.buttonWrong(self)   
        event.Skip()
	
    def m_toolSwitchFCOnToolClicked( self, event ):
        card.switchCard(self)
	
    def m_bitmapScrollFCOnMouseWheel( self, event ):
        card.switchCard(self)
