# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 12:39:47 2018
@author: Anton
"""
import numpy as np
import PIL
import math
from PIL import ImageOps
#matplotlib.use('Agg')
import pylab
#import matplotlib.backends.backend_agg as agg
pylab.ioff() # make sure it is inactive, otherwise possible qwindows error    .... https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import ctypes
#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100

def CreateTextCardPrint(self,key):
    
    TextCard = True    
    try:
        LaTeXcode =  self.textdictionary[key]
        height_card = math.ceil(len(LaTeXcode)/40)/2
        fig = Figure(figsize=[8, height_card],dpi=100)
        ax = fig.gca()
        ax.plot([0, 0,0, height_card],color = (1,1,1,1))
        ax.axis('off')
        ax.text(-0.5, height_card/2,LaTeXcode, fontsize = self.LaTeXfontsize, horizontalalignment='left', verticalalignment='center',wrap = True)    
        canvas = FigureCanvas(fig)
        canvas.draw()
    except:
        if key[0] == 'A':
            modekey = 'ANSWER'
        elif key[0] == 'Q':
            modekey = 'QUESTION'
        MessageBox(0, f"Error in line {str(int(key[1:])+1)} mode {modekey}\nline: {self.textdictionary[key]}\nFaulty text or command used.\nGo to .../Flashbook/files/... and edit it manually.", "Message", ICON_STOP)
        LaTeXcode =  "Error for this page: invalid code"
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
    imagetext = PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )
    
    # crop the LaTeX image further
    border = 30
    search = True
    img = imagetext
    imginv = ImageOps.invert(img)
    
    img_array = np.sum(np.sum(np.array(imginv),2),0) # look where something is not "white" in the x-axis
    while search:
        for i in range(len(img_array)):
            j = len(img_array) - i-1            
            if search:
                if img_array[j]!= 0:
                    search = False
                    var = j
                    break
                if j == 0:
                    search = False
                    var = j
                    break
    if var + border >  img.size[0]:
        var = img.size[0]
    else:
        var = var + border
    imagetext = img.crop((0, 0, var, img.size[1]))
    return TextCard, imagetext 
