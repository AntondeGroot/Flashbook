# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:44:11 2019

@author: Anton
"""
import gui_flashbook as gui
import threading
import wx
import PIL
import program as p
import fc_functions    as f2
import fc_modules as m2
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

def SaveTime(self):
    if hasattr(self,'TC') and hasattr(self,'bookname') and self.bookname != '':
        self.TC.update() 

class flashcard(gui.MyFrame):
    def __init__(self):
        pass
    def m_OpenFlashcardOnButtonClick( self, event ):
        """START MAIN PROGRAM : FLASCARD"""
        self.NEWCARD = True
        m7.AcceleratorTableSetup(self,"flashcard","set")
        p.SwitchPanel(self,2)
        p.run_flashcard(self)
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
