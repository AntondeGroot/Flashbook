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
#matplotlib.use('Agg')
import pylab
import json
#import matplotlib.backends.backend_agg as agg

pylab.ioff() # make sure it is inactive, otherwise possible qwindows error    .... https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


datadir = os.getenv("LOCALAPPDATA")
dir0 = datadir + r"\FlashBook"
# create settings folder for debugging



    


class Window2(wx.PopupWindow):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, parent, style,image):
        
        #print("picinfo in w2 {}".format(self.info))
        
        """Constructor"""
        wx.PopupWindow.__init__(self, parent, style)
        border = 10
        #if self.debugmode:
        print("fb=Window2")

        panel = wx.Panel(self)
        
        #panel.SetBackgroundColour("CADET BLUE")
        
        panel.SetBackgroundColour(wx.Colour(179, 236, 255) )
   
        #self.m_bitmap123 = wx.StaticBitmap( panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        self.m_bitmap123 = wx.StaticBitmap( panel, wx.ID_ANY, wx.NullBitmap,[border,border], wx.DefaultSize, 0 ) #displace image by width of border
        
        st = wx.StaticBitmap( panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        print(type(image))
        #image = self.image
        
        
        width, height = image.size
        
        image2 = wx.Image( width, height )
        image2.SetData( image.tobytes() )
        
        self.m_bitmap123.SetBitmap(wx.Bitmap(image2))   
        
        self.SetSize( (width+2*border ,height+2*border) )
        panel.SetSize( (width+2*border, height+2*border) )
        
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
    if self.debugmode:
        print("fb=drawRec")
    x0 , y0 = self.cord1
    x1 , y1 = self.cord2
    #rename coordinates if square isn't drawn from top left to bottom right.
    if x0 > x1:
        c = x0
        x0 = x1
        x1 = c
    if y0 > y1:
        c = y0
        y0 = y1
        y1 = c    
    #rescale
    x0 = int(x0*self.zoom)
    y0 = int(y0*self.zoom)
    x1 = int(x1*self.zoom)
    y1 = int(y1*self.zoom)
    #    
        
    width = abs(x0 - x1)
    height = abs(y0 - y1)
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
    if self.debugmode:
        print("fb=drawCoordinates")
    img = np.array(self.pageimage)
    img = np.uint8(img)
    try:#try to look if there already exists borders that need to be drawn
        coordinatelist = self.dictionary['page {}'.format(self.currentpage)]
        for coord in coordinatelist:    
            self.cord1 = coord[0:2]
            self.cord2 = coord[2:]
            img = drawRec(self,img,self.colorlist[0])
    except:
        pass
    
    try:    #there won't always be tempdict borders, so try and otherwise go further
        coordinatelist = self.tempdictionary['page {}'.format(self.currentpage)]
        for coord in coordinatelist:    
            self.cord1 = coord[0:2]
            self.cord2 = coord[2:]
            img = drawRec(self,img,self.colorlist[1])
    except:
        pass
    #export image
    self.pageimage = PIL.Image.fromarray(img)
    
def SetScrollbars(self): #no errors
    if self.debugmode:
        print("fb=SetScrollbars")
    scrollWin = self.m_scrolledWindow1
    scrollWin.SetScrollbars(0,int(20*self.zoom),0,int(100*self.zoom) )

def LoadPage(self): # no error
    if self.debugmode:
        print("fb=LoadPage")
    
    
    try:
        self.jpgdir = self.dir3+r'\{}\{}'.format(self.bookname,self.picnames[self.currentpage-1])
        print(self.jpgdir)
        self.pageimage = PIL.Image.open(self.jpgdir)
        self.pageimagecopy = self.pageimage
        self.width, self.height = self.pageimage.size
        #rescale
        self.width, self.height = self.pageimagecopy.size #so that it doesn't rescale it everytime ShowPage() is used
        self.width , self.height = int(self.width*self.zoom) , int(self.height*self.zoom)
        self.pageimage = self.pageimage.resize((self.width, self.height), PIL.Image.ANTIALIAS)
    except:
        print(colored("Error: cannot load page",'red'))
    
def ShowPrintScreen(self): # no error
    try:
        # update
        self.m_CurrentPage11.SetValue("PrtScr")
        #rescale image
        self.width, self.height = self.pageimagecopy.size #so that it doesn't rescale it everytime ShowPage() is used
        self.width , self.height = int(self.width*self.zoom) , int(self.height*self.zoom)
        self.pageimage = self.pageimage.resize((self.width, self.height), PIL.Image.ANTIALIAS)
        
        image2 = wx.Image( self.width, self.height )
        image2.SetData( self.pageimage.tobytes() )
        
        ##
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        self.m_bitmap4.SetBitmap(wx.Bitmap(image2))
        self.Layout()
    except:
        print(colored("Error: cannot show PrintScreen page",'red'))
    
    
    
def ShowPage(self): # no error
    if self.debugmode:
        print("fb=ShowPage")
    try:
        # update
        self.m_CurrentPage11.SetValue(str(self.currentpage))
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
        self.Layout()
        with open(os.path.join(self.temp_dir, self.bookname +'.txt'), 'w') as output:   
            output.write("{}".format(self.currentpage))
    except:
        print(colored("Error: cannot show page",'red'))

def ResetQuestions(self): # no errors
    if self.debugmode:
        print("fb=ResetQuestions")
    self.pdf_question     = ''
    self.pdf_answer       = ''
    self.pic_question     = []
    self.pic_answer       = []
    self.pic_question_dir = []
    self.pic_answer_dir   = []
    self.usertext         = ''


def CombinePics(self,directory):
    if self.debugmode:
        print("fb=CombinePics")
    i = 0
    # combine horizontal pictures horizontally. They can be recognized as [] within a [] such that [vert,[hor,hor],vert,[hor,hor,hor]]
    for im in directory:
        if type(im) is list:
            print(im)
            images = list(map(PIL.Image.open, im))   
            widths, heights = zip(*(i.size for i in images))
            max_height = max(heights)
            total_width = sum(widths)
            new_im = PIL.Image.new('RGB', (total_width, max_height), "white")
            x_offset = 0
            for img in images:
                new_im.paste(img, (x_offset,0))
                x_offset += img.size[0]
            new_im.save(im[0])
            print(len(im))
            for p in range(len(im)):
                if p!=0:
                    try:
                        os.remove(im[p])
                    except:
                        pass
            directory[i] = im[0]
            print(im[0])
        i += 1
    print(directory)
    #combine pictures vertically    
    images = list(map(PIL.Image.open, directory))   
    widths, heights = zip(*(i.size for i in images))
    total_height = sum(heights)
    max_width = max(widths)
    new_im = PIL.Image.new('RGB', (max_width, total_height), "white")
    # combine images to 1
    x_offset = 0
    for im in images:
        new_im.paste(im, (0,x_offset))
        x_offset += im.size[1]
    new_im.save(directory[0])
    #only save first picture (combined pic) the rest will be removed.
    for p in range(len(directory)):
        if p!=0:
            try:
                os.remove(directory[p])
            except:
                pass
            
def CreateTextCard(self):
    if self.debugmode:
        print("fb=CreateTextCard")
    self.TextCard = True    
    #LaTeXcode = Text2Latex(self)
    LaTeXcode = self.usertext
    height_card = math.ceil(len(LaTeXcode)/40)/2
    fig = Figure(figsize=[8, height_card],dpi=100)
    ax = fig.gca()
    ax.plot([0, 0,0, height_card],color = (1,1,1,1))
    ax.axis('off')
    ax.text(-0.5, height_card/2,LaTeXcode, fontsize = 20, horizontalalignment='left', verticalalignment='center',wrap = True)
    
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    self.imagetext = PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )
    

def CombinePicText(self,directory):
    if self.debugmode:
        print("fb=CombinePicText")
    if os.path.exists(directory):
        imagepic = PIL.Image.open(directory)
        images = [self.imagetext,imagepic]
        
        widths, heights = zip(*(i.size for i in images))
        total_height = sum(heights)
        max_width = max(widths)
        new_im = PIL.Image.new('RGB', (max_width, total_height), "white")
        #combine images to 1
        x_offset = 0
        for im in images:
            new_im.paste(im, (0,x_offset))
            x_offset += im.size[1]
        self.image = new_im

def ShowInPopup(self,event,mode):
    if self.debugmode:
        print("fb=ShowInPopup")
    try:# a picture directory may not exist
        if mode == "Answer":
            directory = self.pic_answer_dir[0]
        if mode == "Question":
            directory = self.pic_question_dir[0]
        image = PIL.Image.open(directory)
        self.image = image
        #image.show()
    except:
        print("Error: could not open file in popup")
    try:
        CreateTextCard(self)
    except:
        pass
    try:
        CombinePicText(self,directory)
    except:
        try:
            self.image = self.imagetext
        except:
            pass
    print("test test")
    image = self.image
    print(type(image))
    #image.show()
    #except:
    ##try:#only text
    #####CreateTextCard(self)
    ######image = self.imagetext
    ##except:
    ##    pass
    try:
        a = self.mousepos # try to access mousepos, but if there wasn't any mouseclick: then just place the popupwindow in the middle of your screen.
    except:
        self.mousepos = (int(wx.GetDisplaySize()[0]/2),int(wx.GetDisplaySize()[1]/2))
        
    win = Window2(self.GetTopLevelParent(), wx.SIMPLE_BORDER,image)    
    win.Position((self.mousepos[0]-10,self.mousepos[1]-10), (0,0))
    win.Show(True)  
    try:
        delattr(self, 'imagetext')
    except AttributeError:
        pass


#%% turn user LaTeX macro into useable LaTeX code
import re
import os
import fc_functions as fc


# EXAMPLE:
# defined command = " \secpar{a}{b}   " for the second partial derivative of a wrt b
# nr = #arguments = 2 which are (a,b)
# sentence = "if we take the second partial derivative \secpar{X+Y}{t}"
# returns: position where (X+Y), (t)  begin and end and in the string and that they are the arguments

def Text2Latex(self):
    usertext = self.usertext
    # find all user defined commands in a separate file
    # start reading after "###" because I defined that as the end of the notes    
    file1 = open(os.path.join(self.dir1, r"usercommands.txt"), 'r')
    newcommand_line_lst = file1.readlines()
    
    index = []
    for i in range(len(newcommand_line_lst)):
        if "###" in newcommand_line_lst[i]:
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
        definition_start = fc.findchar('{',newcommand_line,0)
        definition_end   = fc.findchar('}',newcommand_line,0)
        
        num_start = fc.findchar('\[',newcommand_line,"")
        num_end   = fc.findchar('\]',newcommand_line,"")
        
        latex_start = fc.findchar('{',newcommand_line,1)   
        latex_end = fc.findchar('}',newcommand_line,-1)
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
    # check if the command can be found in Q&A
    #while FindCommand == True: 
    while defined_command in inputstring:
        # if a command has arguments: you need to find their positions
        if nr_arg != 0:
            cmd_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), inputstring )][0]
            arguments = fc.find_arguments(cmd_start,inputstring,defined_command,nr_arg)[0]
            
            index1 = fc.find_arguments(cmd_start,inputstring ,defined_command,nr_arg)[1][0]-length_c
            index2 = fc.find_arguments(cmd_start,inputstring,defined_command,nr_arg)[2][1]+1
            
            #replace the command by a LaTeX command
            inputstring = inputstring.replace(inputstring[index1:index2],LaTeX_command )
            #replace the temporary arguments #1,#2... by the real arguments
            for i in range(nr_arg):
                inputstring = inputstring.replace("#{}".format(i+1), arguments[i])
        else:
            # if there are no arguments you can directly replace the defined_cmd for the latex_cmd
            inputstring = inputstring.replace(defined_command,LaTeX_command)
    
    return inputstring
