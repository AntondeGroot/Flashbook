# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:44:04 2019

@author: Anton
"""
import gui_flashbook as gui
import threading
import wx
import PIL
import program as p
import fc_functions    as f2
import print_modules as m3
from pathlib import Path
from latexoperations import Commands as cmd
import log_module    as log
ICON_EXCLAIM=0x30

import ctypes
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100

class helpmenu(gui.MyFrame):
    def __init__(self):
        pass
    
    def m_menuHelpOnMenuSelection( self, event ):
        if self.panel0.IsShown():
            self.lastpage = 0
        elif self.panel1.IsShown():
            self.lastpage = 1
        elif self.panel2.IsShown():
            self.lastpage = 2
        elif self.panel3.IsShown():
            self.lastpage = 3    
        elif self.panel4.IsShown():
            self.lastpage = 4
        elif self.panel5.IsShown():
            self.lastpage = 5
        p.SwitchPanel(self,6)
        
    def m_menuItemAboutOnMenuSelection( self, event ):      
        image = PIL.Image.open(str(Path(self.resourcedir,"flashbook_logo.png")))
        image = image.resize((100, 100), PIL.Image.ANTIALIAS)
        BMP = f2.PILimage_to_Bitmap(image)
        data = BMP
        with gui.MyDialogAbout(self,data) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                pass
            
    def m_richText1OnLeftDown(self,event): #helpmenuitem
        p.SwitchPanel(self,self.lastpage)
    def m_richText2OnLeftDown(self,event): #helpmenuitem
        p.SwitchPanel(self,self.lastpage)
    def m_richText3OnLeftDown(self,event): #helpmenuitem
        p.SwitchPanel(self,self.lastpage)
    def m_richText4OnLeftDown(self,event): #helpmenuitem
        p.SwitchPanel(self,self.lastpage)