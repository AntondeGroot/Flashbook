# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 21:39:06 2020

@author: Anton
"""
import Flashbook.page as page
import _logging.log_module as log

def zoomin(self,event):
    try:
        self.zoom += 0.1
        page.LoadPage(self)
        page.ShowPage_fb(self)
        page.SetScrollbars(self)
        percentage = int(self.zoom*100)
        self.m_ZoomFB.SetValue(f"{percentage}%")
        self.Layout()
    except:
        log.ERRORMESSAGE("Error: cannot zoom out")
        
def zoomout(self,event):    
    try:
        if round(self.zoom,1) == 0.1:
            self.zoom = self.zoom
        else:
            self.zoom += -0.1
        page.LoadPage(self)
        page.ShowPage_fb(self)
        page.SetScrollbars(self)
        percentage = int(self.zoom*100)
        self.m_ZoomFB.SetValue(f"{percentage}%")
        self.panel1.Refresh() # to remove the remnants of a larger bitmap when the page shrinks
        self.Layout()
    except:
        log.ERRORMESSAGE("Error: cannot zoom in")