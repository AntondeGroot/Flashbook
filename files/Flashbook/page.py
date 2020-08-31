# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 20:23:08 2020

@author: Anton
"""
import _logging.log_module as log
from pathlib import Path
import PIL
import json
import wx

def SetScrollbars(self): 
    scrollWin = self.m_scrolledWindow1
    scrollWin.SetScrollbars(int(20*self.zoom),int(20*self.zoom),int(100*self.zoom),int(100*self.zoom) )

def LoadPage(self): 
    try:
        self.jpgdir = str(Path(self.booksdir, self.booknamepath, self.picnames[self.currentpage-1]))
        
        if not self.screenshotmode:
            self.pageimage = PIL.Image.open(self.jpgdir)
            self.pageimagecopy = self.pageimage
        width, height = self.pageimage.size
        #rescale
        width, height = self.pageimagecopy.size #so that it doesn't rescale it everytime ShowPage() is used
        width , height = int(width*self.zoom) , int(height*self.zoom)
        self.pageimage = self.pageimage.resize((width, height), PIL.Image.ANTIALIAS)
    except:
        log.ERRORMESSAGE("Error: cannot load page")
    

    
def LoadPageNr(self):
    """When a book is opened either start where you left off, or start at page 1"""
    path_file = Path(self.dirsettings, 'userdata_bookpages.txt')
    if path_file.exists():
        with open(path_file,'r') as file:
            dictionary = json.load(file)
            if self.bookname in dictionary.keys():
                self.currentpage = dictionary[self.bookname]
            else:
                self.currentpage = 1
            file.close()
    else:
        self.currentpage = 1
    
def SavePageNr(self):
    path_file = Path(self.dirsettings, 'userdata_bookpages.txt')
    
    if self.currentpage == 'prtscr' and hasattr(self,'currentpage_backup'):
        self.currentpage = self.currentpage_backup
    
    if path_file.exists():
        with open(path_file,'r') as file:
            dictionary = json.load(file)        
            dictionary[self.bookname] = self.currentpage
            file.close()
    else:
        dictionary = {self.bookname:self.currentpage}
    log.DEBUGLOG(debugmode=self.debugmode, msg=f'FB FUNC: save page number, dictionary = {dictionary}')
    with open(path_file,'w') as file:
        file.write(json.dumps(dictionary))
        file.close()

def ShowPage_fb(self): 
    try:
        # update
        self.m_CurrentPageFB.SetValue(str(self.currentpage))
        #rescale image
        width, height = self.pageimagecopy.size #so that it doesn't rescale it everytime ShowPage() is used
        width, height = int(width*self.zoom) , int(height*self.zoom)
        self.pageimage = self.pageimage.resize((width, height), PIL.Image.ANTIALIAS)
        try:   #draw borders if they exist
            if self.drawborders:
                pageimage = self.pageimage
                self.pageimage = drawCoordinates(self,pageimage)
        except:
            pass        
        image2 = wx.Image( width, height )
        image2.SetData( self.pageimage.tobytes() )
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        if not self.screenshotmode:
            SavePageNr(self)
    except:
        log.ERRORMESSAGE("Error: cannot show page")