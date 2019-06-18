# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 14:09:07 2018

@author: Anton
"""
import print_functions as f
import wx

def initializeparameters(self):    
    # initialize variables:
    self.bookname       = ''
    self.BorderCoords   = []         
    self.colorlist      = self.bordercolors
    self.currentpage    = 1
    self.cursor         = False    # normal cursor
    self.drawborders    = True
    self.image          = []
    self.imagecopy      = []
    self.tempdictionary = {}
    self.panel_pos      = (0,0)        
    self.questionmode   = True
    self.zoom           = 1.0
