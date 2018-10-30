# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 14:09:07 2018

@author: Anton
"""
import print_functions as f
import wx

def initializeparameters(self):
    
    
    # for scrolling: only remember current and last position, append and pop, if the numbers repeat [0,0] or [X,X] then you know you've reached either the beginning or the end of the window: then flip page
    self.scrollpos = [42,1337] 
    #self.m_dirPicker1.SetInitialDirectory(self.dir3) #set initial directory
    # initialize variables:
    self.bookname       = ''
    self.BorderCoords   = []         
    self.colorlist      = [[0,0,0],[200,0,0]]
    self.currentpage    = 1
    self.cursor         = False    # normal cursor
    self.drawborders    = True
    self.image          = []
    self.imagecopy      = []
    self.tempdictionary = {}
    self.panel_pos      = (0,0)        
    self.questionmode   = True
    self.zoom           = 1.0
    #self.m_textCtrl1.SetValue("Question:")
    self.m_textZoom.SetValue("{}%".format(int(self.zoom*100)))  
    f.ResetQuestions(self)
    f.SetScrollbars(self)