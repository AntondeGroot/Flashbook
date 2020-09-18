# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 12:39:47 2018

@author: Anton
"""
import json
import math
import os
import _shared_operations.imageoperations as imop
import PIL
import PIL.Image
import _logging.log_module as log
import re
from pathlib import Path
import wx
## figures: the following makes sure there are no figures popping up
#  make sure it is inactive, otherwise possible qwindows error might occur: https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window
import pylab
pylab.ioff() 
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

"""DEFINED FUNCTIONS -- short overview
#   contains(1)               - to find if a string is contained in a list of strings
#   find_hook(2)              - to find a "}" which closes a command
#   findchar(3)               - find a character in a string
#   find_arguments(5)         - finds all the arguments for a certain command
#   replace_allcommands(4)    - replaces user defined commands into LaTeX commands that are known.
"""

def findpicture_path(self,picname):
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
        imagepic = PIL.Image.open(str(path))
        FOUNDPIC = True
    else:
        folders = os.listdir(self.picsdir)
        for i,item in enumerate(folders):
            path = Path(self.picsdir, item, picname)
            if path.exists():
                imagepic = PIL.Image.open(str(path))
                FOUNDPIC = True
    if not FOUNDPIC:
        """Notify User and create a fake picture with the error message 
        as replacement for the missing picture."""
        
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


def findpicture(self,key):
    """Instead of just opening the path of a picture
    Try to find out if the path exists
    if it does not exist, try to look in all other folders.
    This problem may occur if you have combined several books.
    If the picture really doesn't exist, then the user gets notified with a messagebox."""
    FOUNDPIC = False
    imagepic = None
    #if key in self.picdictionary:
    if 'pic' in self.CardsDeck.getcards()[key].keys():
        picname = self.CardsDeck.getcards()[key]['pic']
        path = Path(self.picsdir, self.bookname, picname)
        if path.exists():
            imagepic = PIL.Image.open(str(path))
            FOUNDPIC = True
        else:
            folders = os.listdir(self.picsdir)
            for i,item in enumerate(folders):
                path = Path(self.picsdir, item, picname)
                if path.exists():
                    imagepic = PIL.Image.open(str(path))
                    FOUNDPIC = True
        if not FOUNDPIC:
            """Notify User and create a fake picture with the error message 
            as replacement for the missing picture."""
            
            MessageBox(0, f"Error in line {str(int(key[6:])+1)} mode {key[0]}\nline: {picname}\nPicture could not be found in any folder.", "Message", ICON_STOP)
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
    else:
        #picture does not exist and should not exist, so this is fine
        pass
    return FOUNDPIC, imagepic





def contains(iterable):
    """check if a string is contained in a list of strings
    returns Boolean, index of location"""
    i = 0
    ans = []
    con = False
    for element in iterable:
        if element:
             ans.append(i)
             con = True
        i += 1
    return con, ans 


        
def find_hook(hookpos, string):    
    """Method:
    Count
        { == +1 
        } == -1
    When the count == 0 you are done.
    """
    k = 0
    hookcount = 0
    SEARCH = True
    for i in range(hookpos, len(string)):#make sure it starts with {
        if SEARCH:
            k += 1
            char = string[i]
            if char == '{':
                hookcount += 1
            if char == '}':
                hookcount -= 1
                if hookcount == 0:
                    SEARCH = False
                    end_index = k + hookpos-1
                    return end_index  


def findchar(char,string,nr):
    """find a character in a string 
    arguments: 
        nr = "" : finds all values
        nr = N  : finds the N-th instance
    """
    ans = [m.start() for m in re.finditer(r'{}'.format(char), string )]
    if isinstance(nr,int):
        return ans[nr] 
    else:
        return ans 


def find_arguments(hookpos, sentence, defined_command, nr_arguments):
    """ find all the hooks for N arguments
    Example:
    defined command = " \secpar{a}{b}   "
    nr_arguments = 2
    sentence = "if we take the second partial derivative \secpar{X+Y}{t}"
    returns: position where (X+Y), (t)  begin and end and in the string and the arguments (x+y), (t)"""
    
    k = 0
    hookcount = 0      
    SEARCH = True
    argcount = 0
    argclose_index = [] 
    argopen_index  = []

    cstr_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), sentence )][0]
    
    for i in range(cstr_start,len(sentence)):            # make sure it starts with {
        if SEARCH:
            k += 1
            char = sentence[i]
            
            if char == '{':
                hookcount += 1
                if hookcount == 1:
                    argopen_index.append(k+cstr_start-1)  #save opening indices
                
            if char == '}':
                hookcount -= 1
                if hookcount == 0:
                    argcount += 1
                    if argcount == nr_arguments:
                        SEARCH = False
                    argclose_index.append(k+cstr_start-1) #save closing indices
    arguments = []
    for i in range(nr_arguments):
        arguments.append(sentence[argopen_index[i]+1:argclose_index[i]])
    return arguments, argopen_index, argclose_index



def replace_allcommands(defined_command, LaTeX_command, STRING, nr_arg):    
    """replace all defined commands in a string"""
   
    SEARCH = (defined_command in STRING)
    while SEARCH: 
        # if a command has arguments: you need to find their positions
        if nr_arg != 0:
            cmd_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), STRING )][0]
            arguments = find_arguments(cmd_start, STRING, defined_command, nr_arg)[0]
            # check if it gives empty [], otherwise index1 = [] will give errors
            ARG, _, _ = find_arguments(cmd_start, STRING, defined_command, nr_arg)
    
            if ARG == []: # quits if no arguments have been found
                SEARCH = False
                break
            else:
                index1 = find_arguments(cmd_start, STRING ,defined_command, nr_arg)[1][0] - len(defined_command) 
                index2 = find_arguments(cmd_start, STRING ,defined_command, nr_arg)[2][1] + 1
                
                #replace the command by a LaTeX command
                STRING = STRING.replace(STRING[index1:index2],LaTeX_command )
                #replace the temporary arguments #1,#2... by the real arguments
                for i in range(nr_arg):
                    STRING = STRING.replace(f"#{i+1}", arguments[i])
                # check if another command is in the Q&A
                SEARCH = (defined_command in STRING)
        else:
            """ if there are no arguments you can directly replace the defined_cmd for the latex_cmd
                only needs to do this once for the entire string"""
            STRING = STRING.replace(defined_command,LaTeX_command)
            SEARCH = False
            break
    
    return STRING


def switch_bitmap(self):
    path_repeat_na = Path(self.resourcedir,"repeat_na.png")
    path_repeat = Path(self.resourcedir,"repeat.png")
    """Display a bitmap indicating whether or not you can flip over the flashcard
    Check if there is an answer card, if not changes mode back to question.
    source:   https://stackoverflow.com/questions/27957257/how-to-change-bitmap1-for-toolbartoolbase-object-in-wxpython"""
    
    try:
        # you always start with a question, check if there is an answer:
        _key_ = f'card_a{self.cardorder[self.index]}' # do not use self.key: only check if there is an answer, don't change the key
        log.DEBUGLOG(debugmode=self.debugmode,msg=f"FC FUNCTIONS:\n\t switch key = {_key_}, \n\t all card keys = {self.CardsDeck.getcards().keys()}")
        try:
            
            #if _key_ not in self.CardsDeck.getcards().keys(): # there is no answer card!
            if not self.ANSWER_CARD: # there is no answer card!
                log.DEBUGLOG(debugmode=self.debugmode,msg=f"FC FUNCTIONS: there is no answer card")
                self.mode = 'Question'
                self.SwitchCard = False        
                id_ = self.m_toolSwitchFC.GetId()
                self.m_toolBar3.SetToolNormalBitmap(id_, wx.Bitmap( str(path_repeat_na), wx.BITMAP_TYPE_ANY ))  
                self.m_modeDisplayFC.SetValue(self.mode) 
                displaycard(self) 
            else:
                self.SwitchCard = True
                id_ = self.m_toolSwitchFC.GetId()
                self.m_toolBar3.SetToolNormalBitmap(id_, wx.Bitmap( str(path_repeat), wx.BITMAP_TYPE_ANY ))
                self.m_modeDisplayFC.SetValue(self.mode) 
                displaycard(self) 
        except:
            log.ERRORMESSAGE("Error: could not switch bitmap #2")
    except:
        
        log.ERRORMESSAGE("Error: could not switch bitmap #1")
    


def CombinePicText_fc(bool_text,imagetext,bool_pic,imagepic):
    if bool_text and bool_pic:
        #imagepic = findpicture(self,key)
        images = [imagetext,imagepic]
        
        widths, heights = zip(*(i.size for i in images))
        total_height = sum(heights)
        max_width = max(widths)
        new_im = PIL.Image.new('RGB', (max_width, total_height), "white")
        #combine images to 1
        y_offset = 0
        for im in images:
            new_im.paste(im, (0,y_offset))
            y_offset += im.size[1]
    elif bool_text and not bool_pic:
        new_im = imagetext
    elif not bool_text and bool_pic:
        new_im = imagepic
    elif not bool_text and not bool_pic:
        new_im = PIL.Image.new('RGB', (1, 1), "white")
        MessageBox(0, f"Error: no Text or Picture exists to combine", "Message", ICON_STOP)
    return new_im
    

    
    
def clearbitmap(self):
    """to clear it: just display a 1x1 empty bitmap"""
    self.m_bitmapScrollFC.SetBitmap(wx.Bitmap(wx.Image( 1,1 )))
        
        
def displaycard(self):
    #try:
    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FC FUNCTIONS: display card")
    print(f"displaycard : index = {self.index} , cards = {len(self.cardorder)} cardorder = {self.cardorder}")
    trueindex = self.cardorder[self.index]
    rawcard = self.Latexfile.getline_i_card(trueindex)
    
    qtext = rawcard['qtext']
    qpic  = rawcard['qpic'] 
    atext = rawcard['atext']
    apic  = rawcard['apic']
    topic = rawcard['t']
    
    bool_textcard, img_text = CreateTextCard(self,'manual',qtext)
    bool_piccard,  img_pic  = imop.findpicture_path(self,qpic)
    bool_textcard2, img_text2 = CreateTextCard(self,'manual',atext)
    bool_piccard2,  img_pic2  = imop.findpicture_path(self,apic)
    image = imop.CombinePics(img_text,img_pic)
    image2 = imop.CombinePics(img_text2,img_pic2)
    
    #%% resize images
    BMP_q = imop.PILimage_to_Bitmap(image)
    self.ANSWER_CARD = False
    try:
        BMP_a = imop.PILimage_to_Bitmap(image2)
        self.ANSWER_CARD = True
    except:
        BMP_a = wx.NullBitmap
    
    
    if self.mode[0].lower() == 'q' :
        if self.NEWCARD == False and  not self.ANSWER_CARD:
            pass
        ShowPageBMP(self,BMP_q)
        self.NEWCARD = False
    else:
        ShowPageBMP(self,BMP_a)
        self.NEWCARD = True

def CreateSingularCard(self,mode):
    self.mode = mode
    try:
        key = f'card_{self.mode[0].lower()}{self.cardorder[self.index]}'
        # try to create a TextCard
        
        bool_textcard, img_text = CreateTextCard(self,'flashcard',key)
        bool_piccard,  img_pic  = findpicture(self,key)
        image = CombinePicText_fc(bool_textcard,img_text,bool_piccard,img_pic)
        #ShowPage_fc(self,image)
        image = imop.cropimage(image,0)
        image = imop.cropimage(image,1)
        if bool_textcard == False and bool_piccard == True:
            """Make sure you don't need to save it, you can just load it"""
            return image, False
        else:
            return image, True
        
    except IndexError:
        log.ERRORMESSAGE(f"FC FUNCTIONS: Error: index error {self.index},\n cardorder = {self.cardorder},\n len cardorder = {len(self.cardorder)}")
    except:
        log.ERRORMESSAGE("FC FUNCTIONS: Error: could not display card")

def CreateTextCard(self,mode,arg1):
    """This function is used for 3 different purposes
    1) Flashbook: create a textcard from user input -- this requires user input: self.usertext
    2) Flashcard: create a textcard from saved data -- this requires a dict key: 'key'
    3) Manual:    
    The creation of a card can fail because the userinput was incorrect it can see something starting with '\' as LaTeX code
    when it should not, or if the user used some undefined function.
    """
    
    if (mode == 'flashbook' and self.usertext != '') or (mode == 'flashcard' and 'text' in self.CardsDeck.getcards()[arg1].keys()) or (mode == 'manual' and arg1 != ''):
        try:
            if mode == 'flashbook':
                usertext = arg1
            if mode == 'manual':
                usertext = arg1
            if mode == 'flashcard':
                # acquire text
                key = arg1     
                usertext = self.CardsDeck.getcards()[key]['text']
                    
            # display text in a plot
            height_card = math.ceil(len(usertext)/40)/2
            figure = Figure(figsize=[8, height_card],dpi=100)
            ax = figure.gca()
            ax.plot([0, 0, 0, height_card],color = (1,1,1,1))
            ax.axis('off')
            ax.text(-0.5, height_card/2,usertext, fontsize = self.LaTeXfontsize, horizontalalignment='left', verticalalignment='center',wrap = True)
            # convert picture to data, if the text is illegitimate the error will occur in canvas.draw()
            canvas = FigureCanvas(figure)
            canvas.draw()
        except KeyError:
            if mode == 'flashbook':
                MessageBox(0, f"Error in text given by user.\nFaulty text or something mistakingly seen as a command used.\nGo to .../Flashbook/files/... and edit it manually.\nOr edit it in Flashcard.", "Message", ICON_STOP)
                
            if mode == 'flashcard':
                if key[:6] == 'card_a':
                    modekey = 'ANSWER'
                elif key[:6] == 'card_q':
                    modekey = 'QUESTION'
                else:
                    modekey = "Error"
                MessageBox(0, f"Error in line {str(int(key[6:])+1)} mode {modekey}\nline: {self.CardsDeck.getcards()[key]}\nFaulty text or command used.\nGo to .../Flashbook/files/... and edit it manually.\nOr edit it in Flashcard.", "Message", ICON_STOP)
            LaTeXcode =  "Error for this page: invalid code"
            height_card = math.ceil(len(LaTeXcode)/40)/2
            fig = Figure(figsize=[8, height_card],dpi=100)
            ax = fig.gca()
            ax.plot([0, 0, 0, height_card],color = (1,1,1,1))
            ax.axis('off')
            ax.text(-0.5, height_card/2,LaTeXcode, fontsize = self.LaTeXfontsize, horizontalalignment='left', verticalalignment='center',wrap = True,color = 'r')    
            canvas = FigureCanvas(fig)
            canvas.draw()
            
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        # output
        bool_textcard = True
        imagetext = PIL.Image.frombytes("RGB", size, raw_data, decoder_name = 'raw', )
        #crop image
        
        imagetext = imop.cropimage(imagetext,0)
        imagetext = imop.cropimage(imagetext,1)
        
    else: 
        #if mode == 'flashcard' but the key is not in dict
        bool_textcard = False
        imagetext = None
    return bool_textcard, imagetext

def DeleteCurrentCard(self):
    trueindex = self.cardorder[self.index]
    #open file
    with open(Path(self.notesdir,self.filename),'r') as file:
        flines = file.readlines()
        file.close()
    #make changes                    
    flines.pop(trueindex)
    #save changes
    with open(str(Path(self.notesdir, self.filename)), 'w') as output: 
        for line in flines:
            output.write(line)    
    set_stats(self)
    save_stats(self)
    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FC FUNCTIONS: card succesfully deleted")
    


def stringcontains(string,substring):
    ans = None
    con = False
    if substring in string:
        con = True
        ans = string.find(substring)    
    return con, ans

def ReplaceUserCommands(commandsfile,line):
    assert type(commandsfile) == list
    assert type(line) == str
    # replace user defined commands, found in a separate file                      
    # only look at lines containing "newcommand" removes all empty and irrelevant lines
    
    newcommand_list = [x for x in commandsfile if ("newcommand"  in x) and ("Note:" not in x)]
    
    ##  how to replace a user defined command with a command that is known in latex
    # look for all commands if they appear anywhere in questions or answers.
    # find indices of: -defined command -original command, -number of arguments
    for i,commandline in enumerate(newcommand_list):
        
        # extract all the data from a commandline
        c_start = findchar('{',commandline,0)
        c_end   = findchar('}',commandline,0)
        
        num_start = findchar('\[',commandline,"")              # the argument "" indicates it will find all instances
        num_end   = findchar('\]',commandline,"") 
       
        newc_start = findchar('{',commandline,1)   
        newc_end   = findchar('}',commandline,-1)
        
        # find the commands explicitly
        defined_command = commandline[c_start+1:c_end]         # finds \secpar{}{}            
        LaTeX_command   = commandline[newc_start+1:newc_end]   # finds \frac{\partial^2 #1}{\partial #2^2}
        assert type(num_start[0]) == int
        assert type(num_end[0]) == int
        nr_arg          = int(commandline[int(num_start[0]+1):int(num_end[0])])
        
        # replace the commandsmacro
        line = replace_allcommands(defined_command,LaTeX_command,line,nr_arg)
    return line

def Cards_ReplaceUserCommands(self):
    # replace user defined commands, found in a separate file                  
    file = open(str(Path(self.notesdir, "usercommands.txt")), 'r')
    newcommand_line_lst = file.readlines()
    # start reading after "###" because I defined that as the end of the notes
    index = []
    for i,commandline in enumerate(newcommand_line_lst):
        if "###" in commandline:
            index = i+1
    # remove the lines that precede the ### for user explanation on how to use newcommand        
    if f"{index}".isdigit():
        newcommand_line_lst[:index]=[]
    # only look at lines containing "newcommand" removes all empty and irrelevant lines
    newcommand_line_lst = [x for x in newcommand_line_lst if ("newcommand"  in x)]
    nr_c = len(newcommand_line_lst)
    
    ##  how to replace a user defined command with a command that is known in latex
    # look for all commands if they appear anywhere in questions or answers.
    # find indices of: -defined command -original command, -number of arguments
    for i in range(nr_c):
        newcommand_line = newcommand_line_lst[i]
        # extract all the data from a commandline
        c_start = findchar('{',newcommand_line,0)
        c_end   = findchar('}',newcommand_line,0)
        
        num_start = findchar('\[',newcommand_line,"")              # the argument "" indicates it will find all instances
        num_end   = findchar('\]',newcommand_line,"") 
       
        newc_start = findchar('{',newcommand_line,1)   
        newc_end   = findchar('}',newcommand_line,-1)
        
        # find the commands explicitly
        defined_command = newcommand_line[c_start+1:c_end]         # finds \secpar{}{}            
        LaTeX_command   = newcommand_line[newc_start+1:newc_end]   # finds \frac{\partial^2 #1}{\partial #2^2}
        nr_arg          = int(newcommand_line[int(num_start[0]+1):int(num_end[0])])
        
        # find where they can be found in all of the questions/answers
        cond_q = contains(defined_command in x for x in self.questions) 
        cond_a = contains(defined_command in x for x in self.answers)  
        
        #check questions: does the i-th command occur in the questions
        if cond_q[0]: #first index gives T/F, 2nd index gives index where it is true
            nr = len(cond_q[1])
            for j in range(nr):
                index1 = cond_q[1]
                index2 = index1[j]                    
                # select the right question and replace all the commands
                Q = self.questions[index2]
                self.questions[index2] = replace_allcommands(defined_command,LaTeX_command,Q,nr_arg)
                                
        #check answers: does the i-th command occur in the answers
        if cond_a[0]: #first index gives T/F, 2nd index gives index where it is true
            nr = len(cond_a[1])
            for k in range(nr):
                index1 = cond_a[1]
                index2 = index1[k]
                # select the right answer and replace all the commands
                A = self.answers[index2]
                self.answers[index2] = replace_allcommands(defined_command, LaTeX_command, A, nr_arg)
            

           
def ShowPageBMP(self,bmp):
    if bmp:
        self.m_bitmapScrollFC.SetBitmap(bmp)     
        self.Refresh()
    
    
def ShowPage_fc(self,image):
    if image:
        image = imop.cropimage(image,0)
        image = imop.cropimage(image,1)
        width, height = image.size
        image2 = wx.Image( width, height )
        image2.SetData( image.tobytes() )        
        self.m_bitmapScrollFC.SetBitmap(wx.Bitmap(image2))     
        self.Refresh()


# reset scroll bar when switching page:
def SetScrollbars_fc(self):
    scrollWin = self.m_scrolledWindow11
    scrollWin.SetScrollbars(0,int(20*self.zoom),0,int(100*self.zoom) )
