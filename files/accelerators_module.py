# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 16:32:13 2019

@author: Anton
"""
import wx

class AccIDs:
    """
    A class used to store all the IDreferences 
    The function AcceleratorTableSetup makes sure this class is only instantiated once, 
    then stored as self.Acc such that it is potentially accessible anywhere else in the program.
    """
    # flashcard
    Id_correct   = 10001
    Id_wrong     = 10002
    Id_card      = 10003    
    # flashbook
    Id_leftkey   = 10004
    Id_rightkey  = 10005
    Id_upkey     = 10006
    Id_downkey   = 10007
    Id_enterkey  = 10008
    Id_stitch    = 10009
    # general
    Id_esc       = 10010
    
    def __init__(self):
        type(self).Id_correct  = wx.NewIdRef()
        type(self).Id_wrong    = wx.NewIdRef()
        type(self).Id_card     = wx.NewIdRef()
        type(self).Id_leftkey  = wx.NewIdRef()
        type(self).Id_rightkey = wx.NewIdRef()
        type(self).Id_upkey    = wx.NewIdRef()
        type(self).Id_downkey  = wx.NewIdRef()
        type(self).Id_enterkey = wx.NewIdRef()
        type(self).Id_stitch   = wx.NewIdRef()
        type(self).Id_esc      = wx.NewIdRef()
    def IDcor(self):
        return type(self).Id_correct
    def IDwrong(self):
        return type(self).Id_wrong
    def IDcard(self):
        return type(self).Id_card
    def IDleft(self):
        return type(self).Id_leftkey
    def IDright(self):
        return type(self).Id_rightkey
    def IDup(self):
        return type(self).Id_upkey
    def IDdown(self):
        return type(self).Id_downkey
    def IDenter(self):
        return type(self).Id_enterkey
    def IDstitch(self):
        return type(self).Id_stitch
    def IDesc(self):
        return type(self).Id_esc
#%%    
def AcceleratorTableSetup(self,mode,submode):
    if not hasattr(self,'Acc'):
        self.Acc = AccIDs()
    if mode == "general" and submode == "set":
        self.Bind(wx.EVT_MENU,  self.m_menuItemBackToMainOnMenuSelection ,          id = self.Acc.IDesc())
        # combine id with keyboard = now keyboard is connected to functions
        entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL,  wx.WXK_ESCAPE,  self.Acc.IDesc() )])
        self.SetAcceleratorTable(entries)   
    if mode == "flashcard" and submode == "set":            
        # combine functions with the id
        self.Bind( wx.EVT_MENU, self.m_buttonCorrectOnButtonClick,         id = self.Acc.IDcor()    )
        self.Bind( wx.EVT_MENU, self.m_buttonWrongOnButtonClick,           id = self.Acc.IDwrong()  )
        self.Bind( wx.EVT_MENU, self.m_toolSwitch21OnToolClicked,          id = self.Acc.IDcard()   )
        self.Bind( wx.EVT_MENU, self.m_menuItemBackToMainOnMenuSelection , id = self.Acc.IDesc()    )
        # combine id with keyboard = now keyboard is connected to functions
        entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_LEFT,   self.Acc.IDcor()),
                                      (wx.ACCEL_NORMAL,  wx.WXK_RIGHT,  self.Acc.IDwrong() ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_UP,     self.Acc.IDcard()),
                                      (wx.ACCEL_NORMAL,  wx.WXK_DOWN,   self.Acc.IDcard()),
                                      (wx.ACCEL_NORMAL,  wx.WXK_ESCAPE, self.Acc.IDesc() )])
        self.SetAcceleratorTable(entries)       
        
    if mode == "flashcard" and submode == "unset":
        pass
    if mode == "flashbook" and submode == "set":
        self.SetAcceleratorTable(wx.AcceleratorTable())
        # combine functions with the id
        self.Bind( wx.EVT_MENU, self.m_toolBack11OnToolClicked,     id = self.Acc.IDleft()  )
        self.Bind( wx.EVT_MENU, self.m_toolNext11OnToolClicked,     id = self.Acc.IDright() )
        self.Bind( wx.EVT_MENU, self.m_enterselectionOnButtonClick, id = self.Acc.IDenter() )
        self.Bind( wx.EVT_MENU, self.m_toolStitchOnButtonClick,     id = self.Acc.IDstitch() )
        self.Bind( wx.EVT_MENU, self.m_toolUPOnToolClicked,         id = self.Acc.IDup())
        self.Bind( wx.EVT_MENU, self.m_toolDOWNOnToolClicked,       id = self.Acc.IDdown())
        self.Bind( wx.EVT_MENU, self.m_menuItemBackToMainOnMenuSelection, id = self.Acc.IDesc())
        
        # combine id with keyboard = now keyboard is connected to functions
        entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_LEFT,    self.Acc.IDleft()),
                                      (wx.ACCEL_NORMAL,  wx.WXK_RIGHT,   self.Acc.IDright() ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_RETURN,  self.Acc.IDenter() ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_UP,      self.Acc.IDup()),
                                      (wx.ACCEL_NORMAL,  wx.WXK_DOWN,    self.Acc.IDdown()),
                                      (wx.ACCEL_NORMAL,  wx.WXK_HOME,    self.Acc.IDstitch() ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_NUMPAD0, self.Acc.IDstitch() ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_ESCAPE,  self.Acc.IDesc() )])
        self.SetAcceleratorTable(entries)
        
    if mode == "flashbook" and submode == "pagewindow":
        print("ENTERED PAGEWINDOW")
        
        entries = [wx.AcceleratorEntry() for i in range(40)]
        accel = wx.AcceleratorTable(entries)
        #self.SetAcceleratorTable(wx.AcceleratorTable()) 
        self.SetAcceleratorTable(accel)
        #self.Bind( wx.EVT_MENU, self.m_toolStitchOnButtonClick, id = self.Acc.IDstitch() )
        # combine id with keyboard = now keyboard is connected to functions
        #entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_HOME,    self.Acc.IDstitch() ),
        #                              (wx.ACCEL_NORMAL,  wx.WXK_NUMPAD0, self.Acc.IDstitch() ),
        #(wx.ACCEL_NORMAL,  wx.WXK_ESCAPE,  self.Acc.IDesc() )])
        #self.SetAcceleratorTable(entries)
        
    if mode == "flashbook" and submode == "textwindow":
        #bind id to frunction
        self.Bind( wx.EVT_MENU, self.m_enterselectionOnButtonClick, id = self.Acc.IDenter() )
        self.Bind( wx.EVT_MENU, self.m_toolStitchOnButtonClick,     id = self.Acc.IDstitch() )
        self.Bind(wx.EVT_MENU,  self.m_menuItemBackToMainOnMenuSelection ,          id = self.Acc.IDesc())
        # combine id with keyboard = now keyboard is connected to functions
        entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_RETURN,  self.Acc.IDenter()),
                                      (wx.ACCEL_NORMAL,  wx.WXK_HOME,    self.Acc.IDstitch() ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_NUMPAD0, self.Acc.IDstitch() ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_ESCAPE,  self.Acc.IDesc() )])
        self.SetAcceleratorTable(entries)
    
    
