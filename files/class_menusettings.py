# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:33:22 2019

@author: Anton
"""
import print_modules as m3
import gui_flashbook as gui
import threading
import wx
import PIL
import program as p
import fb_functions    as f
import fb_modules as m
from pathlib import Path
from latexoperations import Commands as cmd
import log_module    as log
ICON_EXCLAIM=0x30
import historygraph
import ctypes
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100

def settings_reset(self):
    settingsfile = Path(self.dirsettings,"settings.txt")
    if settingsfile.exists():
        settingsfile.unlink()
        
    self.settings_create()
    self.settings_get()
    self.m_checkBoxSelections.Check(self.drawborders)
    if self.panel3.IsShown():
        self.m_colorQAline.SetColour(self.QAline_color)
        self.m_colorPDFline.SetColour(self.horiline_color)
        self.m_colorVERTline.SetColour(self.vertline_color)
        
        self.m_lineWpdf.SetValue(str(self.horiline_thickness))
        self.m_lineWqa.SetValue(str(self.QAline_thickness))
        self.m_lineWvert.SetValue(str(self.vertline_thickness))
        
        self.m_lineQA.SetValue(self.QAline_bool)
        self.m_linePDF.SetValue(self.horiline_bool)            
        self.m_lineVERT.SetValue(self.vertline_bool)
        self.m_checkBoxSameColor.SetValue(self.samecolor_bool)
        
        self.m_sliderPDFsize.SetValue(int(200-self.pdfmultiplier*100))
        self.m_slider_col1.SetValue(self.pdfPageColsPos[0])
        self.m_slider_col2.SetValue(self.pdfPageColsPos[1])
        self.m_slider_col3.SetValue(self.pdfPageColsPos[2])
        self.m_checkBox_col1.SetValue(self.pdfPageColsChecks[0])
        self.m_checkBox_col2.SetValue(self.pdfPageColsChecks[1])
        self.m_checkBox_col3.SetValue(self.pdfPageColsChecks[2])



class menusettings(gui.MyFrame):
    def __init__(self):
        pass
    def m_menuResetGraphOnMenuSelection( self, event ):
        
        path = Path(self.dirsettings,'timecount_flashbook.json')
        if path.exists():
            path.unlink()
        path = Path(self.dirsettings,'timecount_flashcard.json')
        if path.exists():
            path.unlink()
        historygraph.DisplayGraph(self)
        
    
    def m_resetselectionOnButtonClick( self, event ):           
        m.resetselection(self,event)
    
    def m_enterselectionOnButtonClick( self, event ):
        m.selectionentered(self,event)
        
    def m_checkBoxCursorOnCheckBox( self, event ):
        self.cursor = not self.cursor
        m.setcursor(self)
        self.settings_set()
    
    # show drawn borders 
    def m_checkBoxSelectionsOnCheckBox( self, event ):
        self.drawborders = self.m_checkBoxSelections.IsChecked()   
        self.settings_set()
        try:
            print(f"checkbox is {self.drawborders}")
            self.pageimage = self.pageimagecopy # reset image
            f.ShowPage_fb(self)
            self.Layout()
        except:# a book hasn't been opened
            pass    
    def m_menuResetSettingsOnMenuSelection( self, event ):
        settings_reset(self)   
        self.m_checkBoxSelections.Check(self.drawborders)
        self.m_checkBoxCursor.Check(self.cursor)
        self.m_checkBoxDebug.Check(self.debugmode)
        m.setcursor(self)   
        try:
            m3.print_preview(self)
        except:
            pass
    def m_checkBoxDebugOnMenuSelection( self, event ):
        self.debugmode = not self.debugmode
        self.settings_set()
    def m_menuResetLogOnMenuSelection( self, event ):
        folder = self.tempdir
        [file.unlink() for file in folder.iterdir() if ("logging" in file.name and file.suffix =='.out' )]
    def m_menuItemGraphOnMenuSelection( self, event ):
        self.Graph_bool = not self.Graph_bool
        self.settings_set()
        historygraph.DisplayGraph(self)