# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 12:39:47 2018
@author: Anton
"""
from termcolor import colored
import numpy as np
import PIL
import wx
import os
import math
from PIL import ImageOps
#matplotlib.use('Agg')
import pylab
from pathlib import Path
import fb_functions    as f
import fc_functions    as f2
import log_module      as log
import program as p
import json
import re
#import matplotlib.backends.backend_agg as agg
pylab.ioff() # make sure it is inactive, otherwise possible qwindows error    .... https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class Window2(wx.PopupWindow):
    """"""
    #if debugmode:
    #    print("fb=Window2")
    #----------------------------------------------------------------------
    def __init__(self, parent, style, information):
        self.info = information
        self.border = 10
        """Constructor"""
        wx.PopupWindow.__init__(self, parent, style)
        
        panel = wx.Panel(self)
        self.panel = panel
        #panel.SetBackgroundColour("CADET BLUE")
        
        panel.SetBackgroundColour(wx.Colour(179, 236, 255) )
        
        #self.m_bitmap4 = wx.StaticBitmap( panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_bitmap4 = wx.StaticBitmap( panel, wx.ID_ANY, wx.NullBitmap,[self.border,self.border], wx.DefaultSize, 0 ) #displace image by width of border
        
        
        st = wx.StaticBitmap( panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        image = self.info
        width, height = image.size
        
        image2 = wx.Image( width, height )
        image2.SetData( image.tobytes() )
        self.m_bitmap4.SetBitmap(wx.Bitmap(image2))   
        
        self.SetSize( (width+2*self.border ,height+2*self.border) )
        panel.SetSize( (width+2*self.border, height+2*self.border) )

        panel.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        panel.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        panel.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        panel.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        
        st.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        st.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        st.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        st.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        
        wx.CallAfter(self.Refresh)
    
    def OnMouseLeftDown(self, evt):
        self.Refresh()
        self.ldPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        self.wPos = self.ClientToScreen((0,0))
        self.panel.CaptureMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            dPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
            nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
                    self.wPos.y + (dPos.y - self.ldPos.y))
            self.Move(nPos)
        #added myself dont move just destroy
        self.Show(False)
        self.Destroy()
    def OnMouseLeftUp(self, evt):
        if self.panel.HasCapture():
            self.panel.ReleaseMouse()
        #added myself dont move just destroy
        self.Show(False)
        self.Destroy()
    def OnRightUp(self, evt):#orininal
        self.Show(False)
        self.Destroy()


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def drawRec(self,layer,color): # no errors
    x0 , y0 = self.cord1
    x1 , y1 = self.cord2
    #rename coordinates if square isn't drawn from top left to bottom right.
    if x0 > x1:
        x0 , x1 = x1, x0
    if y0 > y1:
        y0 , y1 = y1, y0
    #rescale
    x0 = int(x0*self.zoom)
    y0 = int(y0*self.zoom)
    x1 = int(x1*self.zoom)
    y1 = int(y1*self.zoom)
    #            
    width, height  = abs(x0 - x1), abs(y0 - y1)
    #  Vertical lines   #
    layer[y0:y1,x0] = np.tile(color,[height,1])
    layer[y0:y1,x1] = np.tile(color,[height,1])
    #  horizontal       #
    layer[y0,x0:x1] = np.tile(color,[width,1])
    layer[y1,x0:x1] = np.tile(color,[width,1])
    #  transform layer  #
    layer = np.array(layer)
    layer = np.uint8(layer)
    return layer        

def drawCoordinates(self): # no errors
    img = np.array(self.pageimage)
    img = np.uint8(img)
    try:#try to look if there already exists borders that need to be drawn
        coordinatelist = self.dictionary[f'page {self.currentpage}']
        for coord in coordinatelist:    
            self.cord1 = coord[0:2]
            self.cord2 = coord[2:]
            img = drawRec(self,img,self.colorlist[0])
    except:
        log.ERRORMESSAGE("Error: could not draw borders")
    
    try:    #there won't always be tempdict borders, so try and otherwise go further
        coordinatelist = self.tempdictionary[f'page {self.currentpage}']
        for coord in coordinatelist:    
            self.cord1 = coord[0:2]
            self.cord2 = coord[2:]
            img = drawRec(self,img,self.colorlist[1])
    except:
        log.ERRORMESSAGE("Error: could not draw temporary borders")
    #export image
    self.pageimage = PIL.Image.fromarray(img)
    
def SetScrollbars(self): 
    scrollWin = self.m_scrolledWindow1
    scrollWin.SetScrollbars(0,int(20*self.zoom),0,int(100*self.zoom) )

def LoadPage(self): 
    
    try:
        self.jpgdir = str(Path(self.booksdir, self.bookname, self.picnames[self.currentpage-1]))
        self.pageimage = PIL.Image.open(str(self.jpgdir))
        self.pageimagecopy = self.pageimage
        self.width, self.height = self.pageimage.size
        #rescale
        self.width, self.height = self.pageimagecopy.size #so that it doesn't rescale it everytime ShowPage() is used
        self.width , self.height = int(self.width*self.zoom) , int(self.height*self.zoom)
        self.pageimage = self.pageimage.resize((self.width, self.height), PIL.Image.ANTIALIAS)
    except:
        log.ERRORMESSAGE("Error: cannot load page")    
    
    
def ShowPage(self): # no error
    try:
        # update
        self.m_PageCtrl.SetValue(str(self.currentpage))
        #rescale image
        self.width, self.height = self.pageimagecopy.size #so that it doesn't rescale it everytime ShowPage() is used
        self.width , self.height = int(self.width*self.zoom) , int(self.height*self.zoom)
        self.pageimage = self.pageimage.resize((self.width, self.height), PIL.Image.ANTIALIAS)
         
        try:   #try to draw borders, but if there are no borders, do nothing
            if self.drawborders == True:
                drawCoordinates(self)
        except:
            pass
        
        image2 = wx.Image( self.width, self.height )
        image2.SetData( self.pageimage.tobytes() )
        
        ##
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        with open(str(Path(self.tempdir, self.bookname +'.txt')), 'w') as output:   
            output.write(f"{self.currentpage}")
    except:
        log.ERRORMESSAGE("Error: cannot show page")

def ResetQuestions(self): # no errors
    #if debugmode:
    #    print("fb=ResetQuestions")
    self.pdf_question     = ''
    self.pdf_answer       = ''
    self.pic_question     = []
    self.pic_answer       = []
    self.pic_question_dir = []
    self.pic_answer_dir   = []
    self.usertext         = ''

def CreateTextCardPrint(self):
    
    #if debugmode:
    #    print("fb=CreateTextCard")
    self.TextCard = True    
    #LaTeXcode = Text2Latex(self)
    self.usertext = self.textdictionary[self.key]
    LaTeXcode = self.usertext
    height_card = math.ceil(len(LaTeXcode)/40)/2
    fig = Figure(figsize=[8, height_card],dpi=100)
    ax = fig.gca()
    ax.plot([0, 0,0, height_card],color = (1,1,1,1))
    ax.axis('off')
    ax.text(-0.5, height_card/2,LaTeXcode, fontsize = self.LaTeXfontsize, horizontalalignment='left', verticalalignment='center',wrap = True)
    
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    self.imagetext = PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )
    
    # crop the LaTeX image further
    border = 30
    SEARCH = True
    img = self.imagetext
    imginv = ImageOps.invert(img)
    
    img_array = np.sum(np.sum(np.array(imginv),2),0) # look where something is not "white" in the x-axis
    while SEARCH == True:
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

def CreateTextCardPrint2(self,key):
    
    #if debugmode:
    #    print("fb=CreateTextCard")
    TextCard = True    
    #LaTeXcode = Text2Latex(self)
    LaTeXcode =  self.textdictionary[key]
    height_card = math.ceil(len(LaTeXcode)/40)/2
    fig = Figure(figsize=[8, height_card],dpi=100)
    ax = fig.gca()
    ax.plot([0, 0,0, height_card],color = (1,1,1,1))
    ax.axis('off')
    ax.text(-0.5, height_card/2,LaTeXcode, fontsize = self.LaTeXfontsize, horizontalalignment='left', verticalalignment='center',wrap = True)
    
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
    while SEARCH == True:
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
    imagetext = img.crop((0, 0, var, img.size[1]))
    return TextCard, imagetext 


    

#%% turn user LaTeX macro into useable LaTeX code


def Text2Latex(self):
    """# EXAMPLE:
    defined command = " \secpar{a}{b}   " for the second partial derivative of a wrt b
    nr = #arguments = 2 which are (a,b)
    sentence = "if we take the second partial derivative \secpar{X+Y}{t}"
    returns: position where (X+Y), (t)  begin and end and in the string and that they are the arguments"""
    
    usertext = self.usertext
    # find all user defined commands in a separate file
    # start reading after "###" because I defined that as the end of the notes    
    file1 = Path(self.notesdir,"usercommands.txt").open(mode = 'r')
    newcommand_line_lst = file1.readlines()
    
    index = []
    for i,commandline in enumerate(newcommand_line_lst):
        if "###" in commandline:
            index = i+1
    # remove the lines that precede the ###     
    newcommand_line_lst[:index]=[]
    # only look at lines containing "newcommand"
    newcommand_line_lst = [x for x in newcommand_line_lst if ("newcommand"  in x)]
    nr_commands = len(newcommand_line_lst)
    
    ###  how to replace a user defined command with a command that is known in latex ###
    
    # check for all commands
    for i in range(nr_commands):
        newcommand_line = newcommand_line_lst[i]
        # extract all the data from a commandline
        definition_start = f2.findchar('{',newcommand_line,0)
        definition_end   = f2.findchar('}',newcommand_line,0)
        
        num_start = f2.findchar('\[',newcommand_line,"")
        num_end   = f2.findchar('\]',newcommand_line,"")
        
        latex_start = f2.findchar('{',newcommand_line,1)   
        latex_end = f2.findchar('}',newcommand_line,-1)
        # find the commands explicitly
        defined_command = newcommand_line[definition_start+1:definition_end]     ## finds \secpar        
        LaTeX_command = newcommand_line[latex_start+1:latex_end] ## finds \frac{\partial^2 #1}{\partial #2^2}
        nr_arg = int(newcommand_line[int(num_start[0]+1):int(num_end[0])])            
        
        while defined_command in usertext:
            Q = usertext
            #replace all the commands
            usertext = replacecommands(defined_command,LaTeX_command,Q,nr_arg)              
    return usertext


def replacecommands(defined_command,LaTeX_command,inputstring,nr_arg):        
    length_c = len(defined_command) 
    #Check if the command can be found in Q&A
    while defined_command in inputstring:
        # if a command has arguments: you need to find their positions
        if nr_arg != 0:
            cmd_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), inputstring )][0]
            arguments = f2.find_arguments(cmd_start,inputstring,defined_command,nr_arg)[0]
            
            index1 = f2.find_arguments(cmd_start,inputstring ,defined_command,nr_arg)[1][0]-length_c
            index2 = f2.find_arguments(cmd_start,inputstring,defined_command,nr_arg)[2][1]+1
            
            #replace the command by a LaTeX command
            inputstring = inputstring.replace(inputstring[index1:index2],LaTeX_command )
            #replace the temporary arguments #1,#2... by the real arguments
            for i in range(nr_arg):
                inputstring = inputstring.replace("#{}".format(i+1), arguments[i])
        else:
            # if there are no arguments you can directly replace the defined_cmd for the latex_cmd
            inputstring = inputstring.replace(defined_command,LaTeX_command)
    
    return inputstring
