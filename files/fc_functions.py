# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 12:39:47 2018

@author: Anton
"""
import json
import math
import os
import PIL
import PIL.Image
import program as p
import log_module as log
import random
import re
from pathlib import Path
from termcolor import colored
import numpy as np
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
        if FOUNDPIC == False:
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

def cropimage(img, x, backgroundcolor=(255,255,255), border=20):
    # standard RGB color:
    # white = (255,255,255)
    # black = (0,0,0)
    SEARCH1 = True
    SEARCH2 = True
    var1 = 0
    var2 = 0
    var3 = 0
    var4 = 0
    array = np.array(img)- backgroundcolor
    img_array = np.sum(np.sum(array,2),x) #summed over x-axis
    #print(f"length is {len(img_array)}")
    while (SEARCH1 or SEARCH2):
        for i,pixel in enumerate(img_array):
            j = len(img_array) - i - 1
            pixel1 = img_array[i]
            pixel2 = img_array[j]
            if pixel1 != 0:
                if SEARCH1:
                    var1 = i
                    SEARCH1 = False
                var3 = i
            if pixel2 != 0:
                if SEARCH2:
                    var2 = j
                    SEARCH2 = False
                var4 = j
            # if from both directions the border is found
            if var1 != 0 and var2 != 0:
                SEARCH1 = False
                SEARCH2 = False
                break
            # if they both meat in the middle, the whole image has been scanned
            # and can be stopped
            if j <= i: 
                if var4 == 0:
                    var2 = var3
                if var3 == 0:
                    var1 = var4
                SEARCH1 = False
                SEARCH2 = False
                break
    if var2 + border >  img.size[x]:
        var2 = img.size[x]
    else:
        var2 = var2 + border
        
    if var1-border < 0:
        var1 = 0
    else:
        var1 = var1 - border
    #crop
    if x == 1:
        img = img.crop((0, var1, img.size[0], var2))
    if x == 0:
        img = img.crop((var1, 0, var2, img.size[1]))
        
    #print(var1,var2,var3,var4)
    return img    


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


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

def save_stats(self):
    """keep track of user progress data in a dict
    key: bookname
    value: data such as score, which question, ..."""
    
    key   = self.bookname
    value = self.resumedata[self.bookname]
    try:
        value = self.resumedata[self.bookname]
        with open(self.statsdir, 'r') as file:
            try:
                dictionary = json.load(file)
            except:
                dictionary = {}
        with open(self.statsdir, 'w') as file:
            dictionary[self.bookname] = value            
            file.write(json.dumps(dictionary) )
    except: #key was not in the dictionary
        try:
            with open(self.statsdir, 'r') as file:
                try:
                    dictionary = json.load(file)
                except:
                    dictionary = {}
                dictionary.update({key: value})
        except: #the file does not exist
            dictionary = {}
            dictionary.update({key: value})
        with open(self.statsdir, 'w') as file:
            file.write(json.dumps(dictionary) )
            
def load_stats(self):    
    try:
        with open(self.statsdir, 'r') as file:
            
            self.resumedata = json.load(file)
            self.score = self.resumedata[self.bookname]['score']
            self.index = self.resumedata[self.bookname]['index']
            self.nr_questions = self.resumedata[self.bookname]['nr_questions']
            self.cardorder = self.resumedata[self.bookname]['cardorder']
            score = round(float(self.score)/self.nr_questions*100,1)
            self.m_Score.SetValue(f"{score} %")    
    except:
        print("no stats found for this book, continue")
        
def remove_stats(self):
    try:
        with open(self.statsdir, 'r') as file:
            dictionary = json.load(file)
        with open(self.statsdir, 'w') as file:
            del dictionary[self.bookname]
            file.write(json.dumps(dictionary))
    except: # no update, just overwrite with popped dictionary
        log.ERRORMESSAGE("Error could not load saved stats from RemoveStats()")
    
    
def set_stats(self):
    self.resumedata[self.bookname]= {'score': self.score, 'index': self.index, 'nr_questions':self.nr_questions, 'cardorder': self.cardorder[:self.nr_questions] }
        
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
        if (SEARCH == True):
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
    if is_number(nr):
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
        if (SEARCH == True):
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
    while SEARCH == True: 
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






def remove_pics(string, pic_command):
    
    """by design, there is only 1 picture per Q/A, in the form: 
    'some text \pic{name.jpg} some text'   """
    
    if pic_command in string: # if \pic is found in text
        # start and endpoints of brackets
        pic_start = [m.start() for m in re.finditer(r'\{}'.format(pic_command), string )][0]        
        pic_end   = find_hook(pic_start,string)
        # output
        BOOLEAN = True
        picname = find_arguments(pic_start,string,pic_command,1)[0][0] # returns string instead of list
        string  = string[:pic_start] + string[pic_end+1:]                 # Question without picture
    else:
        BOOLEAN = False
        picname = None
    return BOOLEAN, string, picname


def switch_bitmap(self):
    path_repeat_na = Path(self.resourcedir,"repeat_na.png")
    path_repeat = Path(self.resourcedir,"repeat.png")
    """Display a bitmap indicating whether or not you can flip over the flashcard
    Check if there is an answer card, if not changes mode back to question.
    source:   https://stackoverflow.com/questions/27957257/how-to-change-bitmap1-for-toolbartoolbase-object-in-wxpython"""
    
    try:
        # you always start with a question, check if there is an answer:
        _key_ = f'card_a{self.cardorder[self.index]}' # do not use self.key: only check if there is an answer, don't change the key
        print(f"switch key is {_key_}")
        try:
            if _key_ not in self.CardsDeck.getcards().keys(): # there is no answer card!
                print("there is no answer card")
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

def TryCreateTextCard(self,key):
    # try to create a TextCard]
    key = self.key
    if key in self.textdictionary:
        try:
            TextCard, imagetext = CreateTextCard(self,'flashcard',key)
        except:
            log.ERRORMESSAGE("Error: could not create textcard")
            
def TryCombinePicText(self,key):
    if key in self.picdictionary:
        try:
            imagetext = self.imagetext
            self.image = CombinePicText_fc(self,key,imagetext)
        except:
            pass
    else:
        self.image = self.imagetext
        
def TryOnlyTextPic(self):
    try:
        self.image = findpicture(self,self.key)
        ShowPage_fc(self)
    except:
        print("Error: could not load singular picture (no text available)")
        
def displaycard(self):
    #try:
    key = f'card_{self.mode[0].lower()}{self.cardorder[self.index]}'
    # try to create a TextCard
    bool_textcard, img_txt = CreateTextCard(self,'flashcard',key)
    bool_piccard, img_pic  = findpicture(self,key)
    image = CombinePicText_fc(bool_textcard,img_txt,bool_piccard,img_pic)
    ShowPage_fc(self,image) 
    
    #except:
    #    log.ERRORMESSAGE("Error: could not display card")
        
def PILimage_to_Bitmap(image): 
    """ PIL image to wxBitmap """
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    image2 = wx.Bitmap(image2)
    return image2

def CreateTopicCard(self):
    key = f'card_{self.mode[0].lower()}{self.cardorder[self.index]}'
    bool_textcard, img_text = TopicCard(self,key)
    if bool_textcard:
        return img_text
    else:
        return None

def CreateSingularCard(self,mode):
    self.mode = mode
    try:
        key = f'card_{self.mode[0].lower()}{self.cardorder[self.index]}'
        # try to create a TextCard
        bool_textcard, img_text = CreateTextCard(self,'flashcard',key)
        bool_piccard,  img_pic  = findpicture(self,key)
        image = CombinePicText_fc(bool_textcard,img_text,bool_piccard,img_pic)
        #ShowPage_fc(self,image)
        image = cropimage(image,0)
        image = cropimage(image,1)
        if bool_textcard == False and bool_piccard == True:
            """Make sure you don't need to save it, you can just load it"""
            return image, False
        else:
            return image, True
    except IndexError:
        log.ERRORMESSAGE("Error: index error")
        print(f"index = {self.index}")
        print(f"cardorder = {self.cardorder}")
        print(f"len cardorder = {len(self.cardorder)}")
    except:
        log.ERRORMESSAGE("Error: could not display card")

def TopicCard(self,key):
    width_card = 8
    INVERT = True
    if INVERT:
        fcolor, tcolor = 'black', 'white'
    else:
        fcolor, tcolor = 'white', 'black'
        
    if key in self.CardsDeck.getcards().keys():
        try:
            usertext = self.CardsDeck.getcards()[key]['text']
            width_card = self.a4page_w/100
            # display text in a plot
            height_card = int(math.ceil(len(usertext)/40))*0.75
            figure = Figure(figsize=[width_card, height_card],dpi=100,facecolor=fcolor)
            figure.add_axes([0,0,1,1])
            ax = figure.gca()
            #ax.plot([0, 0, 0, height_card],color = (1,1,1,1))
            ax.axis('off')
            #ax.text(-0.5, height_card/2,usertext, fontsize = self.LaTeXfontsize, horizontalalignment='left', verticalalignment='center',wrap = True)
            ax.text(0.5, 0.5,usertext, fontsize = self.LaTeXfontsize*2, horizontalalignment='center', verticalalignment='center',wrap = True,color=tcolor)
            # convert picture to data, if the text is illegitimate the error will occur in canvas.draw()
            canvas = FigureCanvas(figure)
            canvas.draw()
        except:
            
            #MessageBox(0, f"Error in line {str(int(key[6:])+1)} mode {modekey}\nline: {self.CardsDeck.getcards()[key]}\nFaulty text or command used.\nGo to .../Flashbook/files/... and edit it manually.\nOr edit it in Flashcard.", "Message", ICON_STOP)
            LaTeXcode =  "Error for this page: invalid code"
            height_card = math.ceil(len(LaTeXcode)/40)/2
            fig = Figure(figsize=[width_card, height_card],dpi=100)
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
        #print(colored(imagetext.size,"red"))
    else: 
        #if mode == 'flashcard' but the key is not in dict
        bool_textcard = False
        imagetext = None
    return bool_textcard, imagetext    

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
        except:
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
        
        imagetext = cropimage(imagetext,0)
        imagetext = cropimage(imagetext,1)
        
        #print(colored(imagetext.size,"red"))
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
    print("success!!")

def FindArgumentsCards(self,q_hookpos,a_hookpos,letterfile):
    nr_cards = len(q_hookpos)
    self.questions_raw = []
    self.answers_raw   = []
    self.questions     = []
    self.answers       = []
    for N in range(nr_cards):   
        end_q_index = find_hook(q_hookpos[N],letterfile)
        end_a_index = find_hook(a_hookpos[N],letterfile)    
        # collect all Questions and Answers
        self.questions.append(letterfile[q_hookpos[N]+1:end_q_index])
        self.answers.append(letterfile[a_hookpos[N]+1:end_a_index]) 
        #store the unedited questions and answers. This will be used when the user wants to edit the original Q and A
        self.questions_raw.append(letterfile[self.q_hookpos[N]+1:end_q_index])
        self.answers_raw.append(letterfile[self.a_hookpos[N]+1:end_a_index])

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
    if f"{index}".isdigit() == True:
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
        if cond_q[0] == True: #first index gives T/F, 2nd index gives index where it is true
            nr = len(cond_q[1])
            for j in range(nr):
                index1 = cond_q[1]
                index2 = index1[j]                    
                # select the right question and replace all the commands
                Q = self.questions[index2]
                self.questions[index2] = replace_allcommands(defined_command,LaTeX_command,Q,nr_arg)
                                
        #check answers: does the i-th command occur in the answers
        if cond_a[0] == True: #first index gives T/F, 2nd index gives index where it is true
            nr = len(cond_a[1])
            for k in range(nr):
                index1 = cond_a[1]
                index2 = index1[k]
                # select the right answer and replace all the commands
                A = self.answers[index2]
                self.answers[index2] = replace_allcommands(defined_command, LaTeX_command, A, nr_arg)

def SeparatePicsFromText(self,line):
    T_F, QnA, picname = remove_pics(line,"\pic{")
    if QnA.strip() == '':
        QnA = None
    return QnA, picname

def SeparatePicsFromCards(self):
    ## replace all \pics out of the QnA and save the picture names.
    self.picdictionary  = {}
    self.textdictionary = {}
    self.q_pics = []
    self.a_pics = []
    # remove all \pic{} commands
    for i in range(len(self.CardsDeck)):
        SEARCH1 = True
        SEARCH2 = True            
        # Questions: replace pics{}
        while SEARCH1 == True:#find all pic commands
            [T_F, QnA, picname] = remove_pics(self.questions[i],self.pic_command)
            self.questions[i] = QnA # removed pic{} from Question
            if T_F == True:
                self.picdictionary.update({f'Q{i}': picname})
            SEARCH1 = T_F
              
        while SEARCH2 == True: 
            [T_F2,QnA,picname] = remove_pics(self.answers[i],self.pic_command) 
            self.answers[i] = QnA # removed pic{} from Answer
            if T_F2 == True:
                self.picdictionary.update({f'A{i}': picname})
            SEARCH2 = T_F2  
            
def Cards_To_TextDicts(self):
    # reformat QnA
    questions2 = []
    answers2 = []
    for i,question in enumerate(self.questions):
        answer = self.answers[i]
        questions2.append(question.strip())
        answers2.append(answer.strip())
    # save questions and answers in dictionaries
    for i,item in enumerate(self.questions):
        if questions2[i] != '':
            self.textdictionary.update({f'Q{i}' : questions2[i]})
        if answers2[i] != '':
           self.textdictionary.update({f'A{i}' : answers2[i]})
           

    
def ShowPage_fc(self,image):
    try:
        image = cropimage(image,0)
        image = cropimage(image,1)
        width, height = image.size
        image2 = wx.Image( width, height )
        image2.SetData( image.tobytes() )        
        self.m_bitmapScrollFC.SetBitmap(wx.Bitmap(image2))     
        self.Refresh()
    except:        
        log.ERRORMESSAGE("Error: cannot show image")

# reset scroll bar when switching page:
def SetScrollbars_fc(self):
    scrollWin = self.m_scrolledWindow11
    scrollWin.SetScrollbars(0,int(20*self.zoom),0,int(100*self.zoom) )
