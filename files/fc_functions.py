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
import random
import re
from termcolor import colored
import wx
## figures: the following makes sure there are no figures popping up
#  make sure it is inactive, otherwise possible qwindows error might occur: https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window
import pylab
pylab.ioff() 
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

## setting up relevant paths
datadir = os.getenv("LOCALAPPDATA")
dir0    = datadir + r"\FlashBook"
dir7    = dir0 + r"\resources"
path_add   = os.path.join(dir7,"add.png")
path_min   = os.path.join(dir7,"min.png")
path_repeat    = os.path.join(dir7,"repeat.png")
path_repeat_na = os.path.join(dir7,"repeat_na.png")

 # create settings folder for debugging



"""
##= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
###################### defined functions #######################################
##= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
"""
#   contains(1)               - to find if a string is contained in a list of strings
#   find_hook(2)              - to find a "}" which closes a command
#   findchar(3)               - find a character in a string
#   find_arguments(5)         - finds all the arguments for a certain command
#   replace_allcommands(4)    - replaces user defined commands into LaTeX commands that are known.

## to check if a string is contained in a list of strings,
#  returns (T/F, index)
def contains(iterable):
    k = 0
    ans = []
    con = []
    for element in iterable:
        if element:
             ans.append(k)
             con = True
        k=k+1
    return con,ans 

## keeping track of user progress data
def SaveStats(self):
    if self.debugmode:
        print("f=savestats")
        print(self.resumedata)
        print(type(self.resumedata))
    key = self.bookname
    value = self.resumedata[self.bookname]
    print(f"value = {value}")
    try:
        value = self.resumedata[self.bookname]
        with open(self.statsdir, 'r') as file:
            try:
                dictionary = json.load(file)
            except:
                dictionary={}
        with open(self.statsdir, 'w') as file:
            print(dictionary)
            #self.resumedata.update({key: value}) #original
            #file.write(json.dumps(self.resumedata) )
            #file.update({key: value})
            dictionary[self.bookname] =  value
            
            file.write(json.dumps(dictionary) )
    except: #a certain key was not in the dictionary

        with open(self.statsdir, 'r') as file:
            try:
                dictionary = json.load(file)
            except:
                dictionary={}
            dictionary.update({key: value})
            file.write(json.dumps(dictionary) )
        with open(self.statsdir, 'w') as file:
            file.write(json.dumps(dictionary) )
def LoadStats(self):    
    if self.debugmode:
        print("f=loadstats")
    try:
        with open(self.statsdir, 'r') as file:
            
            self.resumedata = json.load(file)
            self.score = self.resumedata[self.bookname]['score']
            self.index = self.resumedata[self.bookname]['index']
            self.nr_questions = self.resumedata[self.bookname]['nr_questions']
            self.cardorder = self.resumedata[self.bookname]['cardorder']
            self.m_Score21.SetValue("{} %".format(round(float(self.score)/self.nr_questions*100,1)))    
    except:
        print("no stats found for this book, continue")
        
def RemoveStats(self):
    if self.debugmode:
        print("f=removestats")
    try:
        with open(self.statsdir, 'r') as file:
            dictionary = json.load(file)
        with open(self.statsdir, 'w') as file:
            del dictionary[self.bookname]
            file.write(json.dumps(dictionary))
    except: # no update, just overwrite with popped dictionary
        print("Error could not load saved stats from RemoveStats()")
        #with open(self.statsdir, 'w') as file:
        #    file.write(json.dumps(self.resumedata) )
    
    
def SetStats(self):
    if self.debugmode:
        print("f=setstats")
    #try:
    #    self.resumedata.update({self.bookname: {'score': self.score, 'index': self.index, 'nr_questions':self.nr_questions, 'cardorder': self.cardorder[:self.nr_questions] }})
    #except:# if it doesn't yet exist
    self.resumedata[self.bookname]= {'score': self.score, 'index': self.index, 'nr_questions':self.nr_questions, 'cardorder': self.cardorder[:self.nr_questions] }
        


## start from a given command \cmd{ and count "{" as +1 and "}" as -1, stop when count = 0
#  returns index so that you know from where to where the argument of the command is located
def find_hook(hookpos,string):    
    k = 0
    hookcount = 0
    condition = True
    for i in range(hookpos,len(string)):#make sure it starts with {
        if (condition == True):
            k = k+1
            char = string[i]
            if char == '{':
                hookcount += 1
            if char == '}':
                hookcount -= 1
                if hookcount == 0:
                    condition = False
                    end_index = k+hookpos-1
                    return end_index

## find a character in a string 
#  return either all values nr="", or first for nr=0, or last for nr=-1
def findchar(char,string,nr):
    nr1 = str(nr)
    if nr1.isdigit() == True:
        ans = [m.start() for m in re.finditer(r'{}'.format(char), string )][nr]
        return ans 
    if nr == -1:  # negative numbers arent considered digits, we will only need [0,1,-1, or no argument]
        ans = [m.start() for m in re.finditer(r'{}'.format(char), string )][nr]
        return ans 
    else:
        ans = [m.start() for m in re.finditer(r'{}'.format(char), string )]
        return ans 

## find all the hooks for N arguments
#  i.e. defined command = " \secpar{a}{b}   "
#  nr = #arguments = 2
#  sentence = "if we take the second partial derivative \secpar{X+Y}{t}"
#  returns: position where (X+Y), (t)  begin and end and in the string and that they are the arguments
def find_arguments(hookpos,sentence,defined_command,nr_arguments):
    k = 0
    hookcount = 0      
    condition = True
    argcount = 0
    # find opening and closing {} for the arguments
    argclose_index = [] 
    argopen_index  = []

    cstr_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), sentence )][0]
    
    for i in range(cstr_start,len(sentence)):            # make sure it starts with {
        if (condition == True):
            k = k+1
            char = sentence[i]
            
            if char == '{':
                hookcount += 1
                if hookcount ==1:
                    argopen_index.append(k+cstr_start-1)  # save opening indices
                
            if char == '}':
                hookcount -= 1
                if hookcount == 0:
                    argcount += 1
                    if argcount== nr_arguments:           #if the nr of closed loops == nr of arguments we are done
                        condition = False
                    argclose_index.append(k+cstr_start-1) #save closing indices
    arguments = []
    for i in range(nr_arguments):
        arguments.append(sentence[argopen_index[i]+1:argclose_index[i]])
    return arguments, argopen_index, argclose_index

## replace all defined commands in a string
def replace_allcommands(defined_command,LaTeX_command,Question,nr_arg):    
    length_c = len(defined_command) 
    # check if the command can be found in Q&A
    FindCommand = (defined_command in Question)
    while FindCommand == True: 
        # if a command has arguments: you need to find their positions
        if nr_arg != 0:
            cmd_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), Question )][0]
            arguments = find_arguments(cmd_start,Question,defined_command,nr_arg)[0]
            # check if it gives empty [], otherwise index1 = [] will give errors
            A = find_arguments(cmd_start,Question ,defined_command,nr_arg)
    
            if not A[0]: # quits if the index is empty
                FindCommand = False
            else:
                index1 = find_arguments(cmd_start,Question ,defined_command,nr_arg)[1][0]-length_c
                index2 = find_arguments(cmd_start,Question,defined_command,nr_arg)[2][1]+1
                
                #replace the command by a LaTeX command
                Question = Question.replace(Question[index1:index2],LaTeX_command )
                #replace the temporary arguments #1,#2... by the real arguments
                for i in range(nr_arg):
                    Question = Question.replace("#{}".format(i+1), arguments[i])
                # check if another command is in the Q&A
                FindCommand = (defined_command in Question)
        else:
            # if there are no arguments you can directly replace the defined_cmd for the latex_cmd
            # only needs to do this once for the entire string
            Question = Question.replace(defined_command,LaTeX_command)
            FindCommand = False
    
    return Question

def remove_pics(string,pic_command):
    
    # there is only 1 pic per Q/A, in the form of "some text \pic{name.jpg} some text"   
    boolean = []
    if pic_command in string: # if \pic is found in text
        # start and endpoints of brackets
        pic_start = [m.start() for m in re.finditer(r'\{}'.format(pic_command), string )][0]        
        pic_end = find_hook(pic_start,string)
        # output
        boolean = True
        picname = find_arguments(pic_start,string,pic_command,1)[0][0] # returns string instead of list
        string = string[:pic_start]+string[pic_end+1:]                 # Question without picture
    else:
        boolean = False
        picname = []
    return boolean, string, picname

## display a bitmap indicating whether or not you can flip over the flashcard
# source:   https://stackoverflow.com/questions/27957257/how-to-change-bitmap1-for-toolbartoolbase-object-in-wxpython
def SwitchBitmap(self): # checks if there is an answer card, if not changes mode back to question.
    if self.debugmode:
        print("f=switchbitmap")
    try:
        # you always start with a question, check if there is an answer:
        key = 'A{}'.format(self.cardorder[self.index]) # do not use self.key: only check if there is an answer, don't change the key
        try:
            if key not in self.textdictionary and key not in self.picdictionary: # there is no answer card!
                self.mode = 'Question'
                self.SwitchCard = False        
                id = self.m_toolSwitch21.GetId()
                self.m_toolBar3.SetToolNormalBitmap(id,wx.Bitmap( path_repeat_na, wx.BITMAP_TYPE_ANY ))        
            else:
                self.SwitchCard = True
                id = self.m_toolSwitch21.GetId()
                self.m_toolBar3.SetToolNormalBitmap(id,wx.Bitmap( path_repeat, wx.BITMAP_TYPE_ANY ))
        except:
            print(colored("Error: could not switch bitmap #2","red"))
    except:
        
        print(colored("Error: could not switch bitmap #1","red"))
    
def CombinePicText(self):
    if self.debugmode:
        print("f=combinepictext")
    # get images
    imagepic = PIL.Image.open(self.dir2+"\\"+self.bookname+"\\"+self.picdictionary[self.key])
    images = [self.imagetext,imagepic]
    # get info
    widths, heights = zip(*(i.size for i in images))
    total_height = sum(heights)
    max_width = max(widths)
    new_im = PIL.Image.new('RGB', (max_width, total_height), "white")
    # combine images to one image
    x_offset = 0
    for im in images:
        new_im.paste(im, (0,x_offset))
        x_offset += im.size[1]
    # output
    self.image = new_im
    
# to clear: just display a 1x1 empty bitmap
def clearbitmap(self):
    self.m_bitmapScroll1.SetBitmap(wx.Bitmap(wx.Image( 1,1 )))

def displaycard(self):
    if self.debugmode:
        print("f=displaycard")
    try:
        self.TextCard = False
        self.key = '{}{}'.format(self.mode[0],self.cardorder[self.index])
        
        # try to create a TextCard
        if self.key in self.textdictionary:
            try:
                CreateTextCard(self)
            except:
                print(colored("Error: could not create textcard","red"))
        # if there is a textcard either combine them with a picture or display it on its own
        if self.TextCard == True: 
            if self.key in self.picdictionary:
                try:
                    CombinePicText(self)
                    ShowPage(self)
                except:
                    pass
            else:
                self.image = self.imagetext
                ShowPage(self)
        else: #if there is no textcard only display the picture
            try:
                self.image = PIL.Image.open(self.dir2+"\\"+self.bookname+"\\"+self.picdictionary[self.key])
                ShowPage(self)
            except:
                pass
    except:
        print(colored("Error: could not display card","red"))

def CreateTextCard(self):
    if self.debugmode:
        print("f=createtextcard")
        print("is pylab interactive? = {}".format(pylab.isinteractive()))
        pylab.ioff()
        print("is pylab interactive? = {} (after explicitly deactivating it)".format(pylab.isinteractive()))
    # acquire text
    usertext = self.textdictionary[self.key]
    # display text in a plot
    height_card = math.ceil(len(usertext)/40)/2
    figure = Figure(figsize=[8, height_card],dpi=100)
    ax = figure.gca()
    ax.plot([0, 0,0, height_card],color = (1,1,1,1))
    ax.axis('off')
    ax.text(-0.5, height_card/2,usertext, fontsize = 20, horizontalalignment='left', verticalalignment='center',wrap = True)
    # convert picture to data
    canvas = FigureCanvas(figure)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    # output
    self.TextCard = True
    self.imagetext = PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )

def LoadFlashCards(self):
    if self.debugmode:
        print("f=loadflashcards")
    #try:
    # find the closing '}' for a command                                         
    end_q_index = 0
    end_a_index = 0    
    for N in range(self.nr_cards):   
        end_q_index = find_hook(self.q_hookpos[N],self.letterfile)
        end_a_index = find_hook(self.a_hookpos[N],self.letterfile)    
        # collect all Questions and Answers
        self.questions.append(self.letterfile[self.q_hookpos[N]+1:end_q_index])
        self.answers.append(self.letterfile[self.a_hookpos[N]+1:end_a_index])        
    # replace user defined commands, found in a separate file                  
    file1 = open(os.path.join(self.dir_LaTeX_commands, r"usercommands.txt"), 'r')
    newcommand_line_lst = file1.readlines()
    # start reading after "###" because I defined that as the end of the notes
    index = []
    for i in range(len(newcommand_line_lst)):
        cond = "###" in newcommand_line_lst[i]
        if cond == True:
            index = i+1
    # remove the lines that precede the ### for user explanation on how to use newcommand        
    if "{}".format(index).isdigit() == True:
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
        newc_end = findchar('}',newcommand_line,-1)
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
                self.answers[index2] = replace_allcommands(defined_command,LaTeX_command,A,nr_arg)
                
    ## replace all \pics out of the QnA and save the picture names.
    self.picdictionary  = {}
    self.textdictionary = {}
    self.q_pics = []
    self.a_pics = []
    # remove all \pic{} commands
    for i in range(self.nr_cards):
        findpic = True
        findpic2 = True            
        # Questions: replace pics{}
        while findpic == True:#find all pic commands
            [T_F,QnA,picname]=remove_pics(self.questions[i],self.pic_command)
            self.questions[i] = QnA # removed pic{} from Question
            if T_F == True:
                self.picdictionary.update({'Q{}'.format(i): picname})
            findpic = T_F
              
        while findpic2 == True: 
            [T_F2,QnA,picname]=remove_pics(self.answers[i],self.pic_command) 
            self.answers[i] = QnA # removed pic{} from Question
            if T_F2 == True:
                self.picdictionary.update({'A{}'.format(i): picname})
            findpic2 = T_F2      
    """
    CARD ORDER
    """
    ## determine cardorder based on user given input
    if self.continueSession == False:
        if self.nr_questions < self.nr_cards:   
            if self.chrono == True:
                self.cardorder = range(self.nr_questions)    
            elif self.chrono == False:
                self.cardorder = random.sample(range(self.nr_cards),self.nr_questions) 
        else: 
            ## If there are more questions than cards
            # we would like to get every question about the same number of times, to do this we do sampling without
            # replacement, then we remove a question if it is immediately repeated.
            if self.chrono == True:
                self.cardorder = list(range(self.nr_cards))*self.nr_questions
                self.cardorder = self.cardorder[:self.nr_questions]
            else:
                cardorder = []
                for i in range(self.nr_cards):   # possibly way larger than needed:
                    cardorder.append(random.sample(range(self.nr_cards),self.nr_cards))
                cardorder = [val for sublist in cardorder for val in sublist]
                con=True
                index = 0
                # remove duplicate numbers
                while con == True:
                    if index == len(cardorder)-2:
                        con = False
                    if cardorder[index] == cardorder[index+1]:
                        del cardorder[index+1]
                        index=index+1
                    index = index+1    
                self.cardorder = cardorder[:self.nr_questions] 
    else:
        LoadStats(self)
        
    # reformat QnA
    self.questions2 = []
    self.answers2 = []
    for i in range(len(self.questions)):
        self.questions2.append(self.questions[i].strip())
        self.answers2.append(self.answers[i].strip())
    # save questions and answers in dictionaries
    for i in range(len(self.questions)):
        if self.questions2[i] != '':
            self.textdictionary.update({'Q{}'.format(i): self.questions2[i]})
        if self.answers2[i] != '':
           self.textdictionary.update({'A{}'.format(i): self.answers2[i]})
    #except:
    #    print(colored("Error: couldn't pick file",'red'))

def ShowPage(self):
    if self.debugmode:
        print("f=showpage")
    try:
        width, height = self.image.size
        image2 = wx.Image( width, height )
        image2.SetData( self.image.tobytes() )        
        self.m_bitmapScroll1.SetBitmap(wx.Bitmap(image2))        
    except:        
        print(colored("Error: cannot show image","red"))

# reset scroll bar when switching page:
def SetScrollbars(self):
    if self.debugmode:
        print("f=setscrollbars")    
    scrollWin = self.m_scrolledWindow11
    scrollWin.SetScrollbars(0,int(20*self.zoom),0,int(100*self.zoom) )
