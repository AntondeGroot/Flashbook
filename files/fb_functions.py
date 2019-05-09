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
from pathlib import Path
import re
import json
import PIL
import numpy as np
from PIL import ImageOps
import fc_functions as fc
import program as p
import log_module as log
#import matplotlib.backends.backend_agg as agg

pylab.ioff() # make sure it is inactive, otherwise possible qwindows error    .... https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class Window2(wx.PopupWindow):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, parent, style,image):
                
        """Constructor"""
        wx.PopupWindow.__init__(self, parent, style)
        border = 10
        print("FB popupwindow")
        panel = wx.Panel(self)
        
        #panel.SetBackgroundColour("CADET BLUE")        
        panel.SetBackgroundColour(wx.Colour(179, 236, 255) )        
        
        self.m_bitmap123 = wx.StaticBitmap( panel, wx.ID_ANY, wx.NullBitmap,[border,border], wx.DefaultSize, 0 ) #displace image by width of border
        st = wx.StaticBitmap( panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        
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


def SetToolStitchArrow(self,orientation="vertical"):
    if orientation == "vertical":
        BMP = self.path_arrow2
    elif orientation == "horizontal":
        BMP = self.path_arrow
    else:
        BMP = self.path_arrow
        print(colored("Wrong mode entered in SetToolStitchArrow","red"))
    try:
        assert type(self.path_arrow) == str
        assert type(self.path_arrow2) == str
    except AssertionError:
        print(colored("ERROR: self.path_arrow and self.path_arrow2 should be of the type STR","red"))
        print(colored("use os.path.join()","red"))
    self.m_toolStitch.SetBitmap(wx.Bitmap(BMP))

def drawrect(self,layer,linecolor): # no errors
    if self.debugmode:
        print("fb=drawRec")
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
    if self.debugmode:
        print("fb=drawCoordinates")
    img = np.array(pageimage)
    img = np.uint8(img)
    key = f'page {self.currentpage}'
    try:#try to look if there already exists borders that need to be drawn
        coordinatelist = self.dictionary[key]
        for coordinates in coordinatelist:    
            self.cord1 = coordinates[0:2]
            self.cord2 = coordinates[2:]
            img = drawrect(self,img,self.colorlist[0])
    except:
        pass
    try:    #there won't always be tempdict borders, so try and otherwise go further
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
    
def SetScrollbars(self): 
    scrollWin = self.m_scrolledWindow1
    scrollWin.SetScrollbars(int(20*self.zoom),int(20*self.zoom),int(100*self.zoom),int(100*self.zoom) )

def LoadPage(self): 
    try:
        self.jpgdir = str(Path(self.booksdir, self.booknamepath, self.picnames[self.currentpage-1]))
        
        if self.stayonpage == False:
            self.pageimage = PIL.Image.open(self.jpgdir)
            self.pageimagecopy = self.pageimage
        width, height = self.pageimage.size
        #rescale
        width, height = self.pageimagecopy.size #so that it doesn't rescale it everytime ShowPage() is used
        width , height = int(width*self.zoom) , int(height*self.zoom)
        self.pageimage = self.pageimage.resize((width, height), PIL.Image.ANTIALIAS)
    except:
        log.ERRORMESSAGE("Error: cannot load page")
    
def ShowPrintScreen(self): # no error
    try:
        # update
        self.m_CurrentPage11.SetValue("PrtScr")
        #rescale image
        width, height = self.pageimagecopy.size #so that it doesn't rescale it everytime ShowPage() is used
        width, height = int(width*self.zoom) , int(height*self.zoom)
        self.pageimage = self.pageimage.resize((width, height), PIL.Image.ANTIALIAS)
        
        image2 = wx.Image( width, height )
        image2.SetData( self.pageimage.tobytes() )
        
        ##
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        self.m_bitmap4.SetBitmap(wx.Bitmap(image2))
        self.Layout()
    except:
        log.ERRORMESSAGE("Error: cannot show PrintScreen page")
    
def LoadPageNr(self):
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
    print(f"dictionary = {dictionary}")
    with open(path_file,'w') as file:
        file.write(json.dumps(dictionary))
        file.close()
        
        
    

def ShowPage_fb(self): 
    try:
        # update
        self.m_CurrentPage11.SetValue(str(self.currentpage))
        #rescale image
        width, height = self.pageimagecopy.size #so that it doesn't rescale it everytime ShowPage() is used
        width, height = int(width*self.zoom) , int(height*self.zoom)
        self.pageimage = self.pageimage.resize((width, height), PIL.Image.ANTIALIAS)
        try:   #draw borders if they exist
            if self.drawborders == True:
                pageimage = self.pageimage
                self.pageimage = drawCoordinates(self,pageimage)
        except:
            pass
        
        image2 = wx.Image( width, height )
        image2.SetData( self.pageimage.tobytes() )
        
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        SavePageNr(self)
    except:
        log.ERRORMESSAGE("Error: cannot show page")
        

def CombinePics(self,directorylist):
    if self.debugmode:
        print("fb=Combine pics")
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
    self.ERROR = False
    #try:
    self.TextCard = True    
    LaTeXcode = self.usertext
    height_card = math.ceil(len(LaTeXcode)/40)/2
    fig = Figure(figsize=[8, height_card], dpi=100)
    ax = fig.gca()
    ax.plot([0, 0,0, height_card],color = (1,1,1,1))
    ax.axis('off')
    ax.text(-0.5, height_card/2, LaTeXcode, fontsize = self.LaTeXfontsize, horizontalalignment = 'left', verticalalignment = 'center', wrap = True)
    
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
    self.imagetext = img.crop((0, 0, var, img.size[1]))
    #except:
    #    self.ERROR = True
    #    log.ERRORMESSAGE("Error: could not create textcard")





def CombinePicText_fb(self,directory):
    self.ERROR = False
    try:
        if self.debugmode:
            print("fb=CombinePicText")
        if Path(directory).exists():
            imagepic = PIL.Image.open(directory)
            images   = [self.imagetext, imagepic]
            
            widths, heights = zip(*(i.size for i in images))
            total_height = sum(heights)
            max_width    = max(widths)
            NewImage     = PIL.Image.new('RGB', (max_width, total_height), "white")
            #combine images to 1
            y_offset = 0
            for im in images:
                NewImage.paste(im, (0,y_offset))
                y_offset += im.size[1]
            self.image = NewImage
    except:
        self.ERROR = True




def ShowInPopup(self,event,mode):
    #try:# a picture directory may not exist
    dir_ = self.Flashcard.getpiclist(mode)
    print(f"dir = {dir_}")
    try:
        if type(dir_) == list: 
            directory = dir_[0]
        else: 
            directory = dir_
        
        if directory != '':
            image = PIL.Image.open(directory)
            self.image = image
    except:
        pass
        #except: 
        #    log.ERRORMESSAGE("Error: could not open file in popup ")
        
    try:
        CreateTextCard(self)
    except:
        pass
    try:
        CombinePicText_fb(self,Path(directory))
    except:
        try:
            print("Only contains text not image")
            self.image = self.imagetext
        except:
            pass
    try:
        image = self.image
        """Try to access mousepos, if there wasn't any mouseclick: then just place the popupwindow in the middle of your screen. 
        this is the case if you only entered text, but didn't select anything with the mouse"""
        try:
            a = self.mousepos  
        except:
            self.mousepos = (int(wx.GetDisplaySize()[0]/2),int(wx.GetDisplaySize()[1]/2))
            
        win = Window2(self.GetTopLevelParent(), wx.SIMPLE_BORDER,image)    
        win.Position((self.mousepos[0]-10,self.mousepos[1]-10), (0,0))
        win.Show(True)  
        if hasattr(self,'imagetext'):
            delattr(self, 'imagetext')
        self.image = []
    except:
        # this is a normal occurance when you switch between Q and A
        pass
        


#%% turn user LaTeX macro into useable LaTeX code




def text_to_latex(self,usertext):
    """EXAMPLE:
    defined command = " \secpar{x}{t}}   " for the second partial derivative of a wrt b
    nr = #arguments = 2 which are (a,b)
    sentence = "if we take the second partial derivative \secpar{X+Y}{t}"
    returns: position where (X+Y), (t)  begin and end and in the string and that they are the arguments
    """
    # find all user defined commands in a separate file
    # start reading after "###" because I defined that as the end of the notes    
    with open(Path(self.notesdir,"usercommands.txt"),'r') as file1:
        commandsfile = file1.readlines()
    file1.close()
    
    index = 0
    for i,line in enumerate(commandsfile):
        if "###" in line:
            index = i+1
    # remove the lines that precede the ###     
    commandsfile[:index] = []
    # only look at lines containing "newcommand"
    commands = [line for line in commandsfile if ("newcommand"  in line)]
    
    ###  how to replace a user defined command with a command that is known in latex ###
    
    # check for all commands
    for _, command_line in enumerate(commands):
        # extract all the data from a commandline
        definition_start = fc.findchar('{',command_line,0)
        definition_end   = fc.findchar('}',command_line,0)
        
        num_start = fc.findchar('\[',command_line,"")
        num_end   = fc.findchar('\]',command_line,"")
        
        latex_start = fc.findchar('{',command_line,1)   
        latex_end   = fc.findchar('}',command_line,-1)
        # find the commands explicitly
        defined_command = command_line[definition_start+1:definition_end]     ## finds \secpar        
        LaTeX_command   = command_line[latex_start+1:latex_end] ## finds \frac{\partial^2 #1}{\partial #2^2}
        nr_arg = int(command_line[int(num_start[0]+1):int(num_end[0])])            
        
        while defined_command in usertext:
            usertext = replacecommands(defined_command, LaTeX_command, usertext, nr_arg)              
    return usertext


def replacecommands(defined_command,LaTeX_command,inputstring,nr_arg):        
    length_c = len(defined_command) 
    #check if the command can be found in Q&A card
    while defined_command in inputstring:
        # if a command has arguments: you need to find their positions
        if nr_arg != 0:
            cmd_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), inputstring )][0]
            arguments = fc.find_arguments(cmd_start, inputstring, defined_command, nr_arg)[0]
            
            index1 = fc.find_arguments(cmd_start, inputstring ,defined_command, nr_arg)[1][0]-length_c
            index2 = fc.find_arguments(cmd_start, inputstring ,defined_command, nr_arg)[2][1]+1
            
            #replace the command by a LaTeX command
            inputstring = inputstring.replace(inputstring[index1:index2], LaTeX_command )
            #replace the temporary arguments #1,#2... by the real arguments
            for i in range(nr_arg):
                inputstring = inputstring.replace(f"#{i+1}", arguments[i])
        else:
            #if there are no arguments to begin with you can directly replace the defined_cmd for the latex_cmd
            inputstring = inputstring.replace(defined_command, LaTeX_command)
    return inputstring
