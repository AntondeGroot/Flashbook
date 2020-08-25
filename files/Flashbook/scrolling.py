# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 21:36:24 2020

@author: Anton
"""

import wx

def arrowscroll(self,event,direction):
    
    scrollWin = self.m_scrolledWindow1
    if direction == 'down':    
        newpos = scrollWin.GetScrollPos(1)+1
    elif direction == 'up':     
        newpos = scrollWin.GetScrollPos(1)-1
    
    # check if you should go to the next/previous page   
    self.scrollpos.append(scrollWin.GetScrollPos(0))
    self.scrollpos.pop(0)
    
    if len(set(self.scrollpos)) == 1: # you've reached either the beginning or end of the document
        if self.scrollpos[0] == 0:             # beginning
            if direction == 'up':
                self.scrollpos = self.scrollpos_reset     # make it a little more difficult to scroll back once you scrolled a page
                self.m_pageBackFBOnToolClicked(self)
                
                if self.currentpage != 1:
                    scrollWin.SetScrollPos(wx.VERTICAL,scrollWin.GetScrollPos(1)+150,False) #orientation, value, refresh?  # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
                    scrollWin.Scroll(scrollWin.GetScrollPos(1)+150,scrollWin.GetScrollPos(1))
                else:
                    scrollWin.SetScrollPos(wx.VERTICAL,0,False) #orientation, value, refresh?  # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
                    scrollWin.Scroll(0,scrollWin.GetScrollPos(1))
        else:                                  # end of page
            if direction == 'down':
                self.scrollpos = self.scrollpos_reset 
                self.m_pageNextFBOnToolClicked(self)
    else:
        # change scrollbar    
        scrollWin.Scroll(wx.VERTICAL,newpos)
    event.Skip() # necessary to use another function after this one                               
        
def mousewheel(self,event):
    scrollWin = self.m_scrolledWindow1
    
    def scroll_end_of_page(scrollWin):
        scrollWin.SetScrollPos(wx.VERTICAL, scrollWin.GetScrollPos(1) + 150, False) #orientation, value, refresh? # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
        scrollWin.Scroll(scrollWin.GetScrollPos(1) + 150, scrollWin.GetScrollPos(1))
    def scroll_begin_of_page(scrollWin):
        scrollWin.SetScrollPos(wx.VERTICAL, 0, False) #orientation, value, refresh? # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
        scrollWin.Scroll(0, scrollWin.GetScrollPos(1))
    def reset_scrollpos(self):
        #make it a little more difficult to scroll once you switched a page
        self.scrollpos = self.scrollpos_reset 
        
    self.scrollpos.append(scrollWin.GetScrollPos(0))
    self.scrollpos.pop(0)
    #set booleans
    wheel_rotation  = event.GetWheelRotation()   # get rotation from mouse wheel
    wheel_scrollsup = wheel_rotation > 0 
    wheel_scrollsdown = wheel_rotation < 0
    virtualsize = scrollWin.GetVirtualSize()[1]
    realsize    = scrollWin.GetClientSize()[1]
    scrollbar_exists = realsize < virtualsize
    topofpage = (len(set(self.scrollpos)) == 1 and self.scrollpos[0] == 0)
    bottomofpage = (len(set(self.scrollpos)) == 1 and self.scrollpos[0] != 0)
    
    if scrollbar_exists:
        if topofpage and wheel_scrollsup:
            reset_scrollpos(self)
            if not self.screenshotmode:
                if self.currentpage != 1:
                    self.m_pageBackFBOnToolClicked(self)
                    scroll_end_of_page(scrollWin)
                else:
                    scroll_begin_of_page(scrollWin)
            else:
                #to stay effectively on the same page as before you imported a screenshot
                self.currentpage = self.currentpage_backup + 1 
                self.m_pageBackFBOnToolClicked(self)
                
                
        elif bottomofpage and wheel_scrollsdown:
            reset_scrollpos(self)
            if not self.screenshotmode:
                if self.currentpage < self.totalpages:
                    self.m_pageNextFBOnToolClicked(self)
                    scroll_begin_of_page(scrollWin)
                else:
                    pass    
            else:
                #to stay effectively on the same page as before you imported a screenshot
                self.currentpage = self.currentpage_backup - 1
                self.m_pageNextFBOnToolClicked(self)
                
                
    else:# there is no scrollbar
        if wheel_scrollsup:
            reset_scrollpos(self)
            if self.currentpage != 1:
                self.m_pageBackFBOnToolClicked(self)
                scroll_end_of_page(scrollWin)
            else:
                scroll_begin_of_page(scrollWin)
        elif wheel_scrollsdown:
            reset_scrollpos(self)
            self.m_pageNextFBOnToolClicked(self)
    event.Skip() # necessary to use other functions after this one is used