# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 16:15:34 2019

@author: Anton
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 21:18:48 2019

@author: Anton
"""
import fc_functions as f2
import PIL
import pylab
import wx
import textwrap

pylab.ioff() 
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.pyplot import cm
import numpy as np
from pathlib import Path
# Get data
import json
import time
from datetime import datetime
import random

import imageoperations as imop


#% FUNCTIONS
def GetValues(timedict,datethreshold):
    totaldict = {}
    today = time.strftime("%d%m%y")
    
    dtoday = datetime.strptime(today,"%d%m%y")
    
    for date in timedict.keys():
        dthen = datetime.strptime(date,"%d%m%y")
        if (dtoday-dthen).days < datethreshold: #if within N days
            for book in timedict[date]:
                value = timedict[date][book]
                if book in totaldict.keys():
                    totaldict[book] += value
                else:
                    totaldict[book] = value
    
    totalbooks = [book for book in totaldict.keys()]
    totalvalues = [value for value in totaldict.values()]
    if today in timedict.keys():
        todaybooks = [book for book in timedict[today].keys()]
        todayvalues = [value for value in timedict[today].values()]
    else:
        todaybooks = []
        todayvalues = []
    return (totalbooks,totalvalues,todaybooks, todayvalues)

def takeSecond(elem):
    return elem[1]

def textcard(TEXT,width,textpos):
    
    height_card = 0.5
    fig = Figure(figsize=[width, height_card],dpi=100)
    fig.patch.set_facecolor((254/255,240/255,231/255,1))
    ax = fig.gca()
    ax.plot([height_card, 0,0, height_card],color = (254/255,240/255,231/255,1))
    
    ax.axis('off')
    ax.get_xaxis().set_visible(False)
    ax.text(textpos/3+0.25, height_card/2,TEXT, fontsize = 20, horizontalalignment='center', verticalalignment='center',wrap = True)    
    
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    return PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )

def drawcard(X,Y,legend2):
    Y = Sec2Min(Y) #the Y-axis has a scale in Minutes
    legend = [legend2[x] for x in X]
    
    X_it,Y_it,legend_it = iter(X),iter(Y),iter(legend)
    #sort small to large
    X2 = [(next(X_it),next(Y_it),next(legend_it)) for _ in X]
    # sort list with key
    X2.sort(key=takeSecond)
    X = [x[0] for x in X2]
    Y = [x[1] for x in X2]
    legend = [x[2] for x in X2]
    
    height_card = 2
    width_card = 3
    fig = Figure(figsize=[width_card, height_card],dpi=100)
    fig.patch.set_facecolor( (254/255, 240/255, 231/255, 1) ) #flashbook theme color rescaled to [0,1]
    ax = fig.gca()
    for i,x in enumerate(X):
        ax.bar(X[i],Y[i],edgecolor = 'black', color=legend[i][0] ,width = 1,  align='center', fill=True,linestyle = '--', snap=False, hatch=legend2[x][1])    
    ax.axis('on')
    
    #Set limit of Y axis:
    #The maximum of the Y-axis should be 10 Minutes unless it has been surpassed
    if Y !=[] and max(Y) < 10: 
        ax.set_ylim(top=10)
    if Y == []:
        ax.set_ylim(top=10)
    ax.get_xaxis().set_visible(False)
    
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    return PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )


def TimeString(seconds): 
    """Convert nr Seconds to a string of one of the following formats: 
        if it contains Hours:   at least | '01Hours00Minutes00Seconds' |  a leading '0'
        if it contains Minutes: at least | '1Minutes00Seconds'         | no leading '0'
        if it contains Seconds: at least | '1Seconds'                  | no leading '0'
        
        The variable Seconds will get subtracted unless we can no longer subtract [HOURS] and [MINUTES] and we know that the remainder is [SECONDS]
    """
    txt = ""
    
    hours = int(seconds/3600)
    if hours > 0:
        if len(str(hours)) == 1:
            txt += f"0{hours}h"
        else:
            txt += f"{hours}h"
        seconds = seconds - hours*3600 
    
    minutes = int(seconds/60)
    if minutes > 0 or hours != 0:
        if len(str(minutes)) == 1 and hours != 0:
            txt += f"0{minutes}m"
        else:
            txt += f"{minutes}m"
        seconds = seconds - minutes*60
        
    seconds = int(seconds) #round off
    if seconds >= 0:
        if len(str(seconds)) == 1 and (minutes != 0 or hours != 0):
            txt += f"0{seconds}s"
        else:
            txt += f"{seconds}s"
    
    return txt

def drawlegend(totalbooks, totalvalues, legendbackup, hatchlist):
    
    colors = [legend_item[0] for i,legend_item in enumerate(legendbackup.values())] #legend_item = (color , hatch)
    
    hatch_it = iter(hatchlist)
    handles = [mpatches.Patch(edgecolor='black',facecolor=c,hatch=next(hatch_it),label="hallo") for c in colors]
    
    totalvalue_it  = iter(totalvalues)
    labels = totalbooks
    labels = [textwrap.fill(f"{x} ({ TimeString(next(totalvalue_it))})",40) for x in totalbooks]
    legend = plt.legend( handles, labels, loc=2, framealpha=False, frameon=True, markerscale=3.6, markerfirst=True, fontsize=12 )
    
    fig = Figure( figsize=[4, 40], dpi=100 )
    fig = legend.figure
    fig.set_size_inches( 8, 30 )
    fig.tight_layout()
    fig.canvas.draw()
    ax = fig.gca()
    ax.axis('off')
    ax.get_xaxis().set_visible(False)
    fig.patch.set_facecolor( (254/255, 240/255, 231/255, 1) )
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    img = PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )
    #cut down image
    color = ( 254, 240, 231 )
    img = imop.cropimage(img, 0, backgroundcolor = color, border = 5)
    img = imop.cropimage(img, 1, backgroundcolor = color, border = 5)
    
    return img

def sortsubdata(data):
    totalbooks = []
    totalvalues = []
    #first order FC entries, then FB then combine the two
    for book,value in zip(data[0],data[1]):
        if book not in totalbooks:
            totalbooks.append(book)
            totalvalues.append(value)
    
    books_it  = iter(totalbooks)
    values_it = iter(totalvalues)
    
    X2 = [(next(books_it),next(values_it)) for _ in totalbooks] #[('book1',t1) , ... , ('bookN',tN)]
    # sort list with 'key', this way we can sort the list by the second element: the amount of time spend
    X2.sort( key=takeSecond )
    return X2

def Sec2Min(listing):   
    return [round(item/60,1) for item in listing]

def CreateGraph(self):
    datethreshold = self.GraphNdays
    try:
        with open(str(Path(self.dirsettings,"timecount_flashbook.json")), 'r') as file:
            timedict_fb = json.load(file)
        file.close()
    except:
        timedict_fb = {}
    try:
        with open(str(Path(self.dirsettings,"timecount_flashcard.json")), 'r') as file2:
            timedict_fc = json.load(file2)
        file2.close()
    except:
        timedict_fc = {}
    
    #% COLLECT ALL DATA
    data_fb = GetValues(timedict_fb,datethreshold)
    data_fc = GetValues(timedict_fc,datethreshold)    
    # COMBINE DATA
    sortedDATA = sortsubdata(data_fc) + sortsubdata(data_fb) #prioritize Flashcard statistics over Flashbook: (10s,1s) + (2s,20s) = > (1,10,2,20) ordered from small to large
    
    totalvalues = []
    totalbooks  = []
    for i,data in enumerate(sortedDATA):
        book = data[0]
        value = data[1]
        if book not in totalbooks:
            totalbooks.append(book)
            totalvalues.append(value)
            
    if len(totalvalues) > 0:
        #Set Colormap
        lvlC = np.linspace(0.03, 0.97, len(totalbooks)) #to exclude colors like Black from appearing in the legend
        color = cm.nipy_spectral(lvlC)           
        
        #CREATE LEGEND: colors and hatches (pattern displayed on barplots)
        hatch_it = iter(["","/////","---","\\\\\\\\\\"]*len(totalbooks))  
        hatchlist = []
        for _ in enumerate(totalbooks):
            hatchlist.append(next(hatch_it))
            
        #Associate a book with: a color and a hatch pattern.
        legend = {}
        for i,book in enumerate(totalbooks):   
            legend[book] = tuple((color[i],hatchlist[i] ))
        legendbackup = legend    
        
        #CREATE TEXT IMAGES
        txt1 = textcard("Today",3.5,2)
        txt2 = textcard(f"Last {datethreshold} days", 3,2)
        txt3 = textcard("Flashbook",2,4).rotate(90, expand = 1)
        txt4 = textcard("Flashcard",2,4).rotate(90, expand = 1)
        
        #CREATE IMAGES
        im1 = drawcard(data_fb[2],data_fb[3],legend)
        im2 = drawcard(data_fb[0],data_fb[1],legend)
        im3 = drawcard(data_fc[2],data_fc[3],legend)
        im4 = drawcard(data_fc[0],data_fc[1],legend)
        im5 = drawlegend(totalbooks,totalvalues,legendbackup,hatchlist)
        
        # COMBINE ALL IMAGES TO A MOZAIC
        width = im1.width + im2.width + txt3.width+im5.width
        height = max(im1.height*2 + txt1.height, im5.height+txt2.height)
        new_im = PIL.Image.new('RGB', (width, height), (254,240,231))
        new_im.paste( txt1, (txt3.width , 0))
        new_im.paste( txt3, (0 , txt1.height))
        new_im.paste( txt4, (0 , txt1.height+txt3.height))
        new_im.paste( txt2, (txt3.width + txt1.width , 0 ))
        new_im.paste( im1,  (txt3.width , txt1.height))
        new_im.paste( im2,  (txt3.width+im1.width , txt2.height))
        new_im.paste( im3,  (txt3.width , txt1.height+im1.height))
        new_im.paste( im4,  (txt3.width+im1.width , txt2.height+im2.height))
        new_im.paste( im5,  (txt3.width+im1.width+im2.width , int(txt2.height*1.5)))
        new_im.paste
    else:
        new_im = PIL.Image.new('RGB', (1, 1), (254, 240, 231))
    
    #resize horizontally
    VirtualWidth = self.m_panelGraph.GetVirtualSize()[0]
    VirtualWidth = int(VirtualWidth * 0.95)
    if new_im.width == 0: #just to avoid /0 errors
        new_im.width = 1
    h = int(new_im.height/new_im.width*VirtualWidth)
    w = VirtualWidth
    
    #resize vertically
    if h > 440:
        w = int(w/h*440)
        h = 440
    
    #output
    new_im = new_im.resize((w, h), PIL.Image.ANTIALIAS)
    BOOL = len(totalvalues) > 0
    return BOOL, new_im

def DisplayGraph(self):
    if self.panel0.IsShown():
        if self.m_menuItemGraph.IsChecked(): 
            SHOWIMAGE, imGraph = CreateGraph(self)
            if SHOWIMAGE == True:
                self.m_panelGraph.Show()
                image = imGraph
                image2 = wx.Image( imGraph.size)
                image2.SetData( image.tobytes() )
                self.m_bitmapGraph.SetBitmap(wx.Bitmap(image2))
            else:
                self.m_panelGraph.Hide()
        else:
            self.m_panelGraph.Hide()
        self.Layout()

    
def testmodule():
    
    N = 50
    totalbooks = [f"book{i}" for i in range(N)]
    totalvalues = [i for i in range(N)]
    
    lvlC = np.linspace(0.03,0.97,len(totalbooks))
    #random.shuffle(lvlC)
    color = cm.Paired(lvlC)
    color = cm.nipy_spectral(lvlC)           
    
    #CREATE LEGEND: colors and hatches (pattern displayed on barplots)
    hatch_it = iter(["","/////","---","\\\\\\\\\\"]*len(totalbooks))  
    hatchlist = []
    for _ in enumerate(totalbooks):
        hatchlist.append(next(hatch_it))
    legend = {}
    for i,book in enumerate(totalbooks):   
        legend[book] = tuple((color[i],hatchlist[i] ))
    
    legendbackup = legend    
    im = drawlegend(totalbooks,totalvalues,legendbackup,hatchlist)
    #im.show()
    
#testmodule()
