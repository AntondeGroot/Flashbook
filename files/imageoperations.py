# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 21:57:43 2019

@author: Anton
"""
import wx
import math
import PIL
from pathlib import Path
import ctypes
import pylab
import os
pylab.ioff() # make sure it is inactive, otherwise possible qwindows error    .... https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100


def PILimage_to_Bitmap(image): 
    """ PIL image to wxBitmap """
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    image2 = wx.Bitmap(image2)
    return image2


def findpicture_path(self,picname,errorbox = False):
    """Instead of just opening the path of a picture
    Try to find out if the path exists
    if it does not exist, try to look in all other folders.
    This problem may occur if you have combined several books.
    If the picture really doesn't exist, then the user gets notified with a messagebox."""
    FOUNDPIC = False
    imagepic = None
    #if key in self.picdictionary:
    
    path = Path(self.picsdir, self.bookname, picname)
    if path.exists():
        try:
            imagepic = PIL.Image.open(str(path))
            FOUNDPIC = True
        except PermissionError:
            #invalid path given, not just a pic that does not exist
            FOUNDPIC = False
            imagepic = None
    else:
        folders = os.listdir(self.picsdir)
        for i,item in enumerate(folders):
            path = Path(self.picsdir, item, picname)
            if path.exists():
                try:
                    imagepic = PIL.Image.open(str(path))
                    FOUNDPIC = True
                except PermissionError:
                    #invalid path given, not just a pic that does not exist
                    FOUNDPIC = False
                    imagepic = None
    if FOUNDPIC == False:
        """Notify User and create a fake picture with the error message 
        as replacement for the missing picture."""
        if errorbox:
            MessageBox(0, f"Error in line : {picname}\nPicture could not be found in any folder.", "Message", ICON_STOP)
            LaTeXcode =  "This image does not exist"
            height_card = math.ceil(len(LaTeXcode)/40)/2
            fig = Figure(figsize=[8, height_card],dpi=100)
            ax = fig.gca()
            ax.plot([0, 0,0, height_card],color = (1,1,1,1))
            ax.axis('off')
            ax.text(-0.5, height_card/2,LaTeXcode, fontsize = self.LaTeXfontsize, horizontalalignment='left', verticalalignment='center',wrap = True,color = 'r')    
            canvas = FigureCanvas(fig)
            canvas.draw()        
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()
            size = canvas.get_width_height()
            # output
            imagepic = PIL.Image.frombytes("RGB", size, raw_data, decoder_name = 'raw', )
            FOUNDPIC = True #the user should be informed and shown that the picture does not exist, because it should exist!

    return FOUNDPIC, imagepic


def CombinePics(image1,image2):
    def isPILimage(img):
        return 'PIL' in str(type(img))
    def isnotPILimage(img):
        return 'PIL' not in str(type(img))    
    if isPILimage(image1) and isPILimage(image2):
        images = [image1,image2]
        widths, heights = zip(*(i.size for i in images))
        total_height = sum(heights)
        max_width = max(widths)
        new_im = PIL.Image.new('RGB', (max_width, total_height), "white")
        #combine images to 1
        y_offset = 0
        for im in images:
            new_im.paste(im, (0,y_offset))
            y_offset += im.size[1]
        return new_im
    elif isPILimage(image1) and isnotPILimage(image2):
        return image1
    elif isnotPILimage(image1) and isPILimage(image2):
        return image2