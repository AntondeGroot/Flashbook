# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 21:56:19 2020

@author: Anton
"""
import PIL
import numpy as np
import Flashbook.screenshot as screenshot
import Flashbook.page as page
from pathlib import Path
from random import randint
import Flashbook.fb_functions as f
import wx
def bitmapleftup(self,event):
    if not self.cursor:
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    self.panel_pos2 = self.m_bitmapScroll.ScreenToClient(wx.GetMousePosition())
    
    x0, y0 = self.panel_pos
    x1, y1 = self.panel_pos2
    #rescale
    x0 = int(x0/self.zoom)
    y0 = int(y0/self.zoom)
    x1 = int(x1/self.zoom)
    y1 = int(y1/self.zoom)
    print(f"leftup\n"*200)
    
    VALID_RECTANGLE = abs(x1-x0)>2 and abs(y1-y0)>2 #should be at least of a certain width and height
    print(f"rectangle = {VALID_RECTANGLE}\n")
    self.Flashcard.setpagenr(self.currentpage)
    if VALID_RECTANGLE:            
        self.BorderCoords = [x0,y0,x1,y1]
        #save all borders in dict
        self.Flashcard.setID() #unique id to Q/A card, only when first data is entered in Q card
        idnr = self.Flashcard.get_idnr()
        self.Borders.addtempborder(page = self.currentpage,idnr = idnr,border = self.BorderCoords)
            
        #crop image
        if not self.screenshotmode:
            img = PIL.Image.open(self.jpgdir)
        else:
            img = self.pageimage
        img = np.array(img)            
        img = img[y0:y1,x0:x1]
        img = PIL.Image.fromarray(img)
        FIND = True
        while FIND:
            rand_nr = str(randint(0, 9999)).rjust(4, "0") #The number must be of length 4: '0006' must be a possible result.
            if not self.screenshotmode:
                picname =  f"{self.bookname}_{self.currentpage}_{rand_nr}.jpg" 
            else:
                picname =  f"{self.bookname}_prtscr_{rand_nr}.jpg"
            filename = Path(self.picsdir, self.bookname, picname)    
            if not filename.exists():
                FIND = False
        img.save(filename)
        
        
        """The list will look like the following:
        [vert1 [hor1,hor2,hor3],vert2,vert3,[hor4,hor5]]
        So that first the horizontal [] within the list will be combined first, 
        then everythying will be combined vertically."""
        
        dir_ = str(Path(self.picsdir,self.bookname,picname))
        print(f"fullpath is {dir_}"*20)        
        if self.stitchmode_v:
            self.Flashcard.addpic('vertical',dir_)
        else:
            self.Flashcard.addpic('horizontal',dir_)
            #restore stitchmode to default
            self.stitchmode_v =  True   
            f.SetToolStitchArrow(self,orientation="vertical")
        page.ShowPage_fb(self)     
        
def panel4_bitmapleftup(self,event):
    self.BoolCropped = True
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    self.panel4_pos2 = self.m_bitmap4.ScreenToClient(wx.GetMousePosition())
    
    x0, y0 = self.panel4_pos
    x1, y1 = self.panel4_pos2
    #rescale
    x0, y0 = int(x0), int(y0)
    x1, y1 = int(x1), int(y1)
    
    if abs(x1-x0)>2 and abs(y1-y0)>2:            
        # cut down image
        img = PIL.Image.open(str(Path(self.tempdir,"screenshot.png")))
        img = np.array(img)            
        img = img[y0:y1,x0:x1]
        img = PIL.Image.fromarray(img)
        self.pageimagecopy = img
        self.pageimage = img
        # show current page
        screenshot.ShowPrintScreen(self)     
    


def setcursor(self):
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))