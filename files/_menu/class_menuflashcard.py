# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:04:23 2019

@author: Anton
"""

import _GUI.gui_flashbook as gui
import wx
import Flashcard.fc_functions as f2
import Flashcard.fc_modules   as m2
import _shared_operations.latexoperations as ltx

class flashcardmenu(gui.MyFrame):
    def __init__(self):
        pass
    def m_menuAddCardOnMenuSelection( self, event ):  
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
                    cards = self.Latexfile.file_to_rawcards() #cards contains q,a,t,s
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
