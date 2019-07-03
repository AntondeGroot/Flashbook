# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:04:23 2019

@author: Anton
"""

import gui_flashbook as gui
import threading
import wx
import PIL
import program as p
import fc_functions    as f2
import print_modules as m3
import fc_modules as m2
from pathlib import Path
from latexoperations import Commands as cmd
import latexoperations as ltx
import imageoperations as imop
import log_module    as log
ICON_EXCLAIM=0x30

import ctypes
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100

class flashcardmenu(gui.MyFrame):
    def __init__(self):
        pass
    def m_menuAddCardOnMenuSelection( self, event ):
        print("b cardorder")
        print(self.cardorder)   
        trueindex = self.cardorder[self.index]
        data = ['Add a card', '' , '' , '' ]
        
        with gui.MyDialog8(self,data) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                #Get user data
                qtext = dlg.m_textCtrl24.GetValue()
                atext = dlg.m_textCtrl25.GetValue()
                topic = dlg.m_textCtrl30.GetValue()
                
                if qtext.strip() != '':
                    self.Latexfile.addline(index = trueindex,question = qtext,answer = atext,topic = topic)
                    self.cardorder += [max(self.cardorder)+1]
                    self.nr_questions += 1
                    self.m_TotalCards.SetValue(f"{self.nr_questions}")
                    self.CardsDeck.reset()
                    self.Latexfile.loadfile(self.booknamepath)
                    cards = self.Latexfile.file_to_rawcards()#cards contains q,a,t,s
                    print(f"cards = {cards}")
                    self.CardsDeck.set_cards(cards=cards,notesdir=self.notesdir)
                    f2.switch_bitmap(self)
                    f2.displaycard(self)
                    self.Refresh()
                
    def m_menuEditCardOnMenuSelection( self, event ):
        trueindex = self.cardorder[self.index]
        ltx.ShowPopupCard(self,trueindex)
        f2.displaycard(self)
        self.Refresh()
           
    def m_menuPreviousCardOnMenuSelection( self, event ):
        m2.buttonPreviousCard(self)
        print("go to previous card")
