# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 20:11:52 2020

@author: Anton
"""
from PIL import Image
from pathlib import Path
import wx
import ctypes
#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MessageBox = ctypes.windll.user32.MessageBoxW
import win32clipboard
from win32api import GetSystemMetrics
import log_module as log

def import_screenshot(self,event):
    """Import a screenshot, it takes multiple monitors into account. 
    The bytestream from win32 is from a Device Independent Bitmap, i.e.'RGBquad', meaning that it is not RGBA but BGRA coded.
    The image is also flipped and rotated."""
    #win32api: total width of all monitors
    SM_CXVIRTUALSCREEN = 78
    
    ScrWidth, ScrHeight = GetSystemMetrics(SM_CXVIRTUALSCREEN),GetSystemMetrics(1)
    win32clipboard.OpenClipboard()
    
    if hasattr(self,"bookname"):
        if self.bookname != '':
            try:
                if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):# Device Independent Bitmap
                    #PrintScreen is available
                    data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                    win32clipboard.CloseClipboard()                
                    
                    #convert bytes to PIL Image
                    img = Image.frombytes('RGBA', (ScrWidth,ScrHeight), data)
                    b,g,r,a = img.split() 
                    image = Image.merge("RGB", (r, g, b))
                    image = image.rotate(180)
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)
                    image.save(str(Path(self.tempdir,"screenshot.png")))
                    
                    #convert back to wxBitmap
                    data = image.tobytes()
                    image3 = wx.Bitmap().FromBuffer(ScrWidth,ScrHeight,data)
                    
                    #store image as backup
                    self.backupimage = image3
                    
                    
                    #self.m_bitmap4.SetBitmap(image3)
                    #p.SwitchPanel(self,4)
                    img = Image.open(str(Path(self.tempdir,"screenshot.png")))
                    self.pageimagecopy = img#img
                    self.pageimage = img  
                    self.width, self.height = self.pageimage.size     
                    image2 = wx.Image( self.width, self.height )
                    image2.SetData( self.pageimage.tobytes() )
                    #image2 = data
                    self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
                    ShowPrintScreen(self)
                    
                    
                else:
                    MessageBox(0, "There is no screenshot available\npress PrtScr again\nor press Alt+PrtScr to only copy an active window", "Error", ICON_EXCLAIM)
            except:
                MessageBox(0, "There is no screenshot available\npress PrtScr again\nor press Alt+PrtScr to only copy an active window", "Error", ICON_EXCLAIM)
        else:
            MessageBox(0, "Please open a book first", "Error", ICON_EXCLAIM)
    try:
        win32clipboard.CloseClipboard()
    except:
        pass
    
def ShowPrintScreen(self):
    try:
        # update
        self.m_CurrentPageFB.SetValue("PrtScr")
        #rescale image
        width, height = self.pageimagecopy.size #so that it doesn't rescale it everytime ShowPage() is used
        width, height = int(width*self.zoom) , int(height*self.zoom)
        self.pageimage = self.pageimage.resize((width, height), Image.ANTIALIAS)
        
        image2 = wx.Image( width, height )
        image2.SetData( self.pageimage.tobytes() )
        #display
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        self.Layout()
    except:
        log.ERRORMESSAGE("Error: cannot show PrintScreen page")  