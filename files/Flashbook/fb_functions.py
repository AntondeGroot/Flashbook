# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 12:39:47 2018
@author: Anton
"""
import numpy as np
import PIL
import wx
import math
#matplotlib.use('Agg')
import pylab
from pathlib import Path
import re
import json
from PIL import ImageOps
import _shared_operations.imageoperations as imop

import Flashcard.fc_functions as fc
import _logging.log_module as log

import ctypes
#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MessageBox = ctypes.windll.user32.MessageBoxW
from PIL import Image
import win32clipboard
from win32api import GetSystemMetrics
#import matplotlib.backends.backend_agg as agg

pylab.ioff() # make sure it is inactive, otherwise possible qwindows error    .... https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas



    
        


def SetToolStitchArrow(self,orientation="vertical"):
    if orientation == "vertical":
        BMP = self.path_arrow2
    elif orientation == "horizontal":
        BMP = self.path_arrow
    else:
        BMP = self.path_arrow
        log.ERRORMESSAGE(f'FB FUNC: Wrong mode entered in SetToolStitchArrow')
    try:
        assert type(self.path_arrow) == str
        assert type(self.path_arrow2) == str
    except AssertionError:
        log.ERRORMESSAGE(f'FB FUNC: self.path_arrow and self.path_arrow2 should be of type STR')
    self.m_toolStitch.SetBitmap(wx.Bitmap(BMP))

def drawrect(self,layer,linecolor): 
    x0 , y0 = self.cord1
    x1 , y1 = self.cord2
    #rename coordinates if square isn't drawn from top left to bottom right.
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    #rescale
    x0 = int(x0*self.zoom)
    y0 = int(y0*self.zoom)
    x1 = int(x1*self.zoom)
    y1 = int(y1*self.zoom)  
        
    width = abs(x0 - x1)
    height = abs(y0 - y1)
    #  Vertical lines   #
    layer[y0:y1,x0] = np.tile(linecolor,[height,1])
    layer[y0:y1,x1] = np.tile(linecolor,[height,1])
    #  horizontal       #
    layer[y0,x0:x1] = np.tile(linecolor,[width,1])
    layer[y1,x0:x1] = np.tile(linecolor,[width,1])
    #  transform layer  #
    layer = np.array(layer)
    layer = np.uint8(layer)
    return layer        

def drawCoordinates(self,pageimage):
    log.DEBUGLOG(debugmode=self.debugmode, msg=f'FB FUNC: draw coordinates')
    img = np.array(pageimage)
    img = np.uint8(img)
    key = f'page {self.currentpage}'
    try:
        #try to look if there already exists borders that need to be drawn
        coordinatelist = self.dictionary[key]
        for coordinates in coordinatelist:    
            self.cord1 = coordinates[0:2]
            self.cord2 = coordinates[2:]
            img = drawrect(self,img,self.colorlist[0])
    except:
        pass
    try:    
        #there won't always be tempdict borders, so try and otherwise go further
        coordinatelist = self.tempdictionary[key]
        for coordinates in coordinatelist:    
            self.cord1 = coordinates[0:2]
            self.cord2 = coordinates[2:]
            img = drawrect(self,img,self.colorlist[1])
    except:
        pass
    #export image
    pageimage = PIL.Image.fromarray(img)
    return pageimage
    

        

def CombinePics(self,directorylist):
    i = 0
    # combine horizontal pictures horizontally. They can be recognized as [] within a [] such that [vert,[hor,hor],vert,[hor,hor,hor]]
    for imagelist in directorylist:
        if type(imagelist) is list:
            images = list(map(PIL.Image.open, imagelist))   
            widths, heights = zip(*(i.size for i in images))
            max_height = max(heights)
            total_width = sum(widths)
            new_im = PIL.Image.new('RGB', (total_width, max_height), "white")
            x_offset = 0
            for img in images:
                new_im.paste(img, (x_offset,0))
                x_offset += img.size[0]
            new_im.save(imagelist[0])
            
            for j, image in enumerate(imagelist):
                if j!= 0 and Path(image).exists():#remove superfluous images                    
                    Path(image).unlink()
            directorylist[i] = imagelist[0]  
        i += 1
    
    #combine pictures vertically    
    images = list(map(PIL.Image.open, directorylist))   
    widths, heights = zip(*(i.size for i in images))
    total_height = sum(heights)
    max_width    = max(widths)
    new_im = PIL.Image.new('RGB', (max_width, total_height), "white")
    # combine images to 1
    x_offset = 0
    for im in images:
        new_im.paste(im, (0,x_offset))
        x_offset += im.size[1]
    new_im.save(directorylist[0])
    #only save first picture (combined pic) the rest will be removed.
    for k, image in enumerate(directorylist):
        if k != 0 and Path(image).exists():
            Path(image).unlink()
           
def CreateTextCard(self):
    #try:
    self.TextCard = True    
    LaTeXcode = self.usertext
    height_card = math.ceil(len(LaTeXcode)/40)/2
    fig = Figure(figsize=[8, height_card], dpi=100)
    ax = fig.gca()
    ax.plot([0, 0,0, height_card],color = (1,1,1,1))
    ax.axis('off')
    ax.text(-0.5, height_card/2, LaTeXcode, fontsize=self.LaTeXfontsize, 
            horizontalalignment='left', verticalalignment='center', wrap=True)    
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    imagetext = PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )
    # crop the LaTeX image further
    border = 30
    SEARCH = True
    img = imagetext
    imginv = ImageOps.invert(img)
    
    img_array = np.sum(np.sum(np.array(imginv),2),0) # look where something is not "white" in the x-axis
    while SEARCH:
        for i in range(len(img_array)):
            j = len(img_array) - i-1            
            if SEARCH == True:
                if img_array[j]!= 0:
                    SEARCH = False
                    var = j
                if j == 0:
                    SEARCH = False
                    var = j
    if var + border >  img.size[0]:
        var = img.size[0]
    else:
        var = var + border
    self.imagetext = img.crop((0, 0, var, img.size[1]))



