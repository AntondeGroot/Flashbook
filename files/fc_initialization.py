# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 14:09:07 2018

@author: Anton
"""
import fc_functions as f2
import wx

def initializeparameters(self):
    # some commands used to create the flashcards and seperate elements: question/answer/picture
    # this way it will remain clear for the user so that he could manually change an entry.
    self.pic_command      = "\pic{"
    self.question_command = r'\\quiz{'
    self.answer_command   = r"\\ans{"
    
    # initialize variables:
    self.bookname       = ''
    self.image          = []
    self.panel_pos      = (0,0)        
    self.zoom           = 1.0
    self.m_Zoom21.SetValue(f"{int(self.zoom*100)}%")  
    #
    self.runprogram = True
    self.SwitchCard = True
    self.index = 0
    self.score = 0
    self.nr_questions = 0
    self.mode = 'Question'
    self.m_textCtrlMode.SetValue(self.mode)
    self.cardorder   = []        
    self.questions   = []
    self.answers     = []
    self.questions2  = []
    f2.SetScrollbars_fc(self)
    
    
