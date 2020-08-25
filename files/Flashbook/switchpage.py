# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 21:37:48 2020

@author: Anton
"""
import fb_functions as f
def switchpage(self,event):
    try:
        pagenumber = self.currentpage
        if pagenumber < 1:
            pagenumber = 1
        if pagenumber > self.totalpages:
            pagenumber = self.totalpages
        self.currentpage = pagenumber
        f.LoadPage(self)
        f.ShowPage_fb(self)
    except:
        log.ERRORMESSAGE("Error: invalid page number")
    self.Layout()
    
def nextpage(self,event):
    try:
        if self.currentpage == 'prtscr':
            self.currentpage = self.currentpage_backup
            log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: page is now {self.currentpage}")
        else:
            if self.currentpage < self.totalpages:
                self.currentpage += 1
        f.LoadPage(self)
        f.ShowPage_fb(self)
        f.SetScrollbars(self)
    except:
        log.ERRORMESSAGE("Error: can't click on next")
    self.Layout()
    
def previouspage(self,event):    
    try:
        if self.currentpage == 'prtscr':
            self.currentpage = self.currentpage_backup
        else:
            if self.currentpage > 1:
                self.currentpage -= 1    
        f.LoadPage(self)
        f.ShowPage_fb(self)
        f.SetScrollbars(self)            
    except:
        log.ERRORMESSAGE("Error: can't click on back")
    self.Layout()