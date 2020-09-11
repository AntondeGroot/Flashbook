# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018
@author: Anton
"""
from random import randint
import numpy as np
import PIL
import _GUI.active_panel as panel
import wx
import os
#import fb_functions as f
import Flashbook.fb_functions as f
import Flashbook.page as page
import _logging.timingmodule as timing
import _logging.log_module as log
import json
import ctypes
from pathlib import Path
#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW

def list2path(templist):
    output = None
    if type(templist) == list:
        if len(templist) > 1:
            if type(templist[0]) == str:
                output = templist[0]
            elif type(templist[0]) == list:
                output = templist[0][0]
        elif len(templist) == 1:
            if type(templist[0]) == str:
                output = templist[0]
            elif type(templist[0]) == list:
                output = templist[0][0]
    return output

#%%
def openbook(self,path):
    
    """For scrolling: only remember last few positions, append and pop 
    if the numbers repeat [0,...,0] or [X,...,X] then you know you've reached either 
    the beginning or the end of the window: then flip page"""
    
    self.scrollpos_reset = [5, 4, 3, 2, 1]     
    self.scrollpos = self.scrollpos_reset
    
    #Keep track of "nrlist" which is a 4 digit nr 18-> "0018" so that it is easily sorted in other programs
    path = os.path.splitext(path)[0] #always remove suffixes as they should refer to a folder not file.
    eventpath = Path(path)
    nrlist = []
    picnames = [str(pic) for pic in eventpath.iterdir() if pic.suffix == '.jpg']
    self.totalpages = len(picnames)
    
    if self.totalpages == 0:
        MessageBox(0, " The selected folder does not contain any images!", "Error", MB_ICONINFORMATION)
    
    for number, picname in enumerate(picnames):        
        im_number = number+1 #images are 1 indexed numbers        
        # I only expect in the order of 1000 pages
        # make sure you can use the nrlist for later use so you can save the output as 
        # "Bookname + ****" a sorted 4 digit number
        nrlist.append( str(im_number).zfill(4) )
        
            
    print(f"nr_list = {nrlist}")
    picnames = [x for _,x in sorted(zip(nrlist,picnames))]
    
    self.picnames = picnames
    self.bookname = eventpath.name
    print(f"booktitle is {self.bookname}\n"*100)
    print(f"bookname = {self.bookname}")
    if hasattr(self,'TC'):
        delattr(self,'TC')
    self.TC = timing.TimeCount(self.bookname,"flashbook")
    self.booknamepath = eventpath.relative_to(self.booksdir)
    self.currentpage = 1
    self.PathBorders = Path(self.bordersdir, self.bookname + '_borders.txt')
    page.LoadPageNr(self)
    
    #Create empty dictionary if it doesn't exist
    if not self.PathBorders.exists():
        with open(str(self.PathBorders), 'w') as file:
            file.write(json.dumps({})) 
    
    book_dir = Path(self.picsdir,self.bookname)
    if not book_dir.exists():
        book_dir.mkdir()
        
    
    self.m_CurrentPageFB.SetValue(str(self.currentpage))
    self.m_TotalPagesFB.SetValue(str(self.totalpages))
    nrlist.sort()
    
    #Open dictionary if it exists
    try:
        with open(self.PathBorders, 'r') as file:
            self.dictionary = json.load(file)
    except:
        self.dictionary = {}
        log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: no drawn rects found for this file {self.bookname}, continue")
    try: 
        self.jpgdir    = str(Path(self.booksdir, self.booknamepath, self.picnames[self.currentpage-1]))
        log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE:\n\t booknamepath {self.booknamepath},\n\t booksdir {self.booksdir}")
        self.pageimage = PIL.Image.open(self.jpgdir)
        self.pageimagecopy = self.pageimage
        self.width, self.height = self.pageimage.size
    except:
        log.ERRORMESSAGE("Error : could not load scrolled window 1")
        
    #Draw borders if they exist
    try:
        if self.drawborders:                    
            pageimage = self.pageimage
            self.pageimage = f.drawCoordinates(self,pageimage)
    except:
        log.ERRORMESSAGE("Error: could not draw borders")
                  
    try:
        image2 = wx.Image( self.width, self.height )
        image2.SetData( self.pageimage.tobytes() )
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        page.SetScrollbars(self)
    except:
        log.ERRORMESSAGE("Error: could not load scrolled window 2")
    panel.SwitchPanel(self,1)
    self.Layout()
    




