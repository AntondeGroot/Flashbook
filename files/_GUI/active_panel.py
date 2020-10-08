# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 19:24:05 2020

@author: Anton
"""
import wx
import Flashbook.events_mouse as evt_m
import _GUI.historygraph as historygraph
def SwitchPanel(self,n):
    self.m_menubar1.EnableTop(1, False)#disable Flashcard menu
    self.m_menuHelp.Enable(True)
    self.panel0.Hide()
    self.panel1.Hide()
    self.panel2.Hide()
    self.panel3.Hide()
    self.panel4.Hide()
    self.panel5.Hide()
    self.panelHelp.Hide()
    self.panel6.Hide()
    if n == 0:
        self.panel0.Show() 
        if self.m_menuItemGraph.IsChecked(): 
            show_image, imGraph = historygraph.CreateGraph(self)
            if show_image:
                self.m_panelGraph.Show()
                image = imGraph
                image2 = wx.Image( imGraph.size)
                image2.SetData( image.tobytes() )
                self.m_bitmapGraph.SetBitmap(wx.Bitmap(image2))
            else:
                self.m_panelGraph.Hide()
        else:
            self.m_panelGraph.Hide()            
    elif n == 1:
        self.panel1.Show()
    elif n == 2:
        self.panel2.Show()
    elif n ==3:
        self.panel3.Show()
    elif n == 4:
        self.panel4.Show()
    elif n == 5:
        self.panel5.Show()
    elif n == 6:
        self.panelHelp.Show()       
    elif n == 7:
        self.panel6.Show()
        
    #reset mouse arrow
    evt_m.setcursor(self)    
    self.Layout() # force refresh of windows