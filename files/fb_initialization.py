# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 14:09:07 2018

@author: Anton
"""
import fb_functions as f
import wx

def initializeparameters(self):
    self.m_bitmapScroll.Bind( wx.EVT_RIGHT_DOWN, self.m_resetselectionOnButtonClick )
    self.m_bitmapScroll.Bind( wx.EVT_MIDDLE_DOWN, self.m_enterselectionOnButtonClick )
    # for scrolling: only remember current and last position, append and pop, if the numbers repeat [0,0] or [X,X] then you know you've reached either the beginning or the end of the window: then flip page 
    self.m_dirPicker11.SetInitialDirectory(str(self.booksdir)) #set initial directory
    # initialize variables:
    self.bookname       = ''
    self.BorderCoords   = []         
    self.colorlist      = self.bordercolors
    self.currentpage    = 1
    self.image          = []
    self.imagecopy      = []
    self.tempdictionary = {}
    self.panel_pos      = (0,0)        
    self.questionmode   = True
    self.zoom           = 1.0
    self.m_textCtrl1.SetValue("Question:")
    self.m_Zoom11.SetValue(f"{int(self.zoom*100)}%")  
    f.ResetQuestions(self)
    f.SetScrollbars(self)
