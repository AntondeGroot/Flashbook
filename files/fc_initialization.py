# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 14:09:07 2018

@author: Anton
"""
import fc_functions as f2
import wx

def initializeparameters(self):
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
    
    
