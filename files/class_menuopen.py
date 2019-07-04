# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:48:13 2019

@author: Anton
"""
import gui_flashbook as gui
import subprocess
import program as p
import threading
import pdf_modules as m5

ICON_EXCLAIM=0x30

import ctypes
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_OKCANCEL = 0x00000001
MB_YESNOCANCEL = 0x00000003
MB_DEFBUTTON2 = 0x00000100
IDOK = 1

class menuopen(gui.MyFrame):
    def __init__(self):
        pass
    
    def m_menuItemFlashbookOnMenuSelection( self, event ):        
        subprocess.Popen(f"explorer {self.dirpdfbook}")
        
    def m_menuItemJPGOnMenuSelection( self, event ):
        subprocess.Popen(f"explorer {self.booksdir}")
        
    def m_menuPDFfolderOnMenuSelection( self, event ):
        subprocess.Popen(f"explorer {self.dirpdf}")
        
    def m_menuItemBackToMainOnMenuSelection( self, event ):
        if self.panel0.IsShown():
            value = MessageBox(0, "Are you sure you want to exit?", "Exit",  MB_OKCANCEL | MB_DEFBUTTON2 | MB_ICONINFORMATION)
            # Answer was yes, user wants to exit the app
            if value == IDOK: 
                self.Close()
        else:
            p.SwitchPanel(self,0)  
        
    def m_menuItemConvertOnMenuSelection( self, event ):
        m5.AddPathvar() #needed to make PDF2jpg work, it sets "Poppler for Windows" as pathvariable
        from_    = str(self.dirpdfbook)
        tempdir_ = str(self.tempdir)
        to_      = str(self.booksdir)
        
        t_pdf = lambda self, from_, tempdir_, to_ : threading.Thread(target = m5.ConvertPDF_to_JPG , args=(self,from_, tempdir_, to_ )).start()
        t_pdf(self, from_, tempdir_, to_) 
