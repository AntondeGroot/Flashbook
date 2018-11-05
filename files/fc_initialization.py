# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 14:09:07 2018

@author: Anton
"""
import fc_functions as f2
import wx

def initializeparameters(self):
    self.scrollpos = [42,1337] 
    # initialize variables:
    self.bookname       = ''
    self.image          = []
    self.panel_pos      = (0,0)        
    self.zoom           = 1.0
    self.m_Zoom21.SetValue("{}%".format(int(self.zoom*100)))  
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
    f2.SetScrollbars(self)
    
    # set mouse short cuts: 
    self.m_bitmapScroll.Bind( wx.EVT_MOUSEWHEEL, self.m_toolSwitch21OnToolClicked )
    self.m_bitmapScroll.Bind( wx.EVT_LEFT_DOWN, self.m_buttonCorrectOnButtonClick)
    self.m_bitmapScroll.Bind( wx.EVT_RIGHT_DOWN, self.m_buttonWrongOnButtonClick )        
    
    # set keyboard short cuts: accelerator table        
    Id_Correct = wx.NewIdRef()
    Id_Wrong   = wx.NewIdRef() 
    Id_card    = wx.NewIdRef() 
    # combine functions with the id
    self.Bind( wx.EVT_MENU, self.m_buttonCorrectOnButtonClick, id = Id_Correct )
    self.Bind( wx.EVT_MENU, self.m_buttonWrongOnButtonClick,   id = Id_Wrong   )
    self.Bind( wx.EVT_MENU, self.m_toolSwitch21OnToolClicked,    id = Id_card    )
    # combine id with keyboard = now keyboard is connected to functions
    entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL,  wx.WXK_LEFT, Id_Correct),
                                  (wx.ACCEL_NORMAL,  wx.WXK_RIGHT, Id_Wrong ),
                                  (wx.ACCEL_NORMAL,  wx.WXK_UP, Id_card),
                                  (wx.ACCEL_NORMAL,  wx.WXK_DOWN, Id_card)])
    self.SetAcceleratorTable(entries)
