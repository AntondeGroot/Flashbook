# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 18:18:50 2019

@author: aammd
"""
import ast
from _settings.settingsfile import settings
import PIL
import os
import Flashcard.fc_functions    as f2
from pathlib import Path
import numpy as np
import re
import math
import wx
import _GUI.gui_flashbook as gui
import _shared_operations.imageoperations as imop
import _logging.log_module as log
#%% functions
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False



def find_hook(hookpos, string):    
    """Method:
    Count
        { == +1 
        } == -1
    When the count == 0 you are done."""
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
                
def argument(command,line):
    startpos   = [m.start() for m in re.finditer(command, line)]
    if startpos != []:
        hookpos = list(np.array(startpos)+len(command)-2)[0]
        end_index = find_hook(hookpos,line)
        return line[hookpos+1:end_index]
    else:
        return ''

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
    search = True
    argcount = 0
    argclose_index = [] 
    argopen_index  = []

    cstr_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), sentence )][0]
    
    for i in range(cstr_start,len(sentence)):            # make sure it starts with {
        if search:
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
                        search = False
                    argclose_index.append(k+cstr_start-1) #save closing indices
    arguments = []
    for i in range(nr_arguments):
        arguments.append(sentence[argopen_index[i]+1:argclose_index[i]])
    return arguments, argopen_index, argclose_index 

def replacecommands(defined_command,LaTeX_command,inputstring,nr_arg):        
    length_c = len(defined_command) 
    #check if the command can be found in Q&A card
    while defined_command in inputstring:
        # if a command has arguments: you need to find their positions
        if nr_arg != 0:
            cmd_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), inputstring )][0]
            arguments = find_arguments(cmd_start, inputstring, defined_command, nr_arg)[0]
            
            index1 = find_arguments(cmd_start, inputstring ,defined_command, nr_arg)[1][0]-length_c
            index2 = find_arguments(cmd_start, inputstring ,defined_command, nr_arg)[2][1]+1
            
            #replace the command by a LaTeX command
            inputstring = inputstring.replace(inputstring[index1:index2], LaTeX_command )
            #replace the temporary arguments #1,#2... by the real arguments
            for i in range(nr_arg):
                inputstring = inputstring.replace(f"#{i+1}", arguments[i])
        else:
            #if there are no arguments to begin with you can directly replace the defined_cmd for the latex_cmd
            inputstring = inputstring.replace(defined_command, LaTeX_command)
    return inputstring


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
    commands = [x for x in commandsfile if ("newcommand"  in x) and ("Note:" not in x)] 
    ###  how to replace a user defined command with a command that is known in latex ### 
    # check for all commands
    for _, command_line in enumerate(commands):
        # extract all the data from a commandline
        definition_start = findchar('{',command_line,0)
        definition_end   = findchar('}',command_line,0)
        
        num_start = findchar('\[',command_line,"")
        num_end   = findchar('\]',command_line,"")
        
        latex_start = findchar('{',command_line,1)   
        latex_end   = findchar('}',command_line,-1)
        # find the commands explicitly
        defined_command = command_line[definition_start+1:definition_end]     ## finds \secpar        
        LaTeX_command   = command_line[latex_start+1:latex_end] ## finds \frac{\partial^2 #1}{\partial #2^2}
        nr_arg = int(command_line[int(num_start[0]+1):int(num_end[0])]) 
        
        
        while defined_command in usertext:
            usertext = replacecommands(defined_command, LaTeX_command, usertext, nr_arg)              
    return usertext






def replace_allcommands(defined_command, LaTeX_command, STRING, nr_arg):    
    """replace all defined commands in a string"""
   
    search = (defined_command in STRING)
    while search: 
        # if a command has arguments: you need to find their positions
        if nr_arg != 0:
            cmd_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), STRING )][0]
            arguments = find_arguments(cmd_start, STRING, defined_command, nr_arg)[0]
            # check if it gives empty [], otherwise index1 = [] will give errors
            ARG, _, _ = find_arguments(cmd_start, STRING, defined_command, nr_arg)
    
            if ARG == []: # quits if no arguments have been found
                search = False
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
                search = (defined_command in STRING)
        else:
            """ if there are no arguments you can directly replace the defined_cmd for the latex_cmd
                only needs to do this once for the entire string"""
            STRING = STRING.replace(defined_command,LaTeX_command)
            search = False
            break
    
    return STRING



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
#%% the classes

    



def ShowPopupCard(self,trueindex):
    # get the card
    rawcard = self.Cardsdeck.getoriginalcard_i(trueindex)
    print(f"rawcard = {rawcard},type {type(rawcard)}")
    # get data from the cards
    log.DEBUGLOG(debugmode=self.debugmode, msg=f'LATEXOPERATIONS: show popupcard: rawcard = {rawcard}')
    
    answer = ['','','','',''] #check all keywords if they occur in the dict / they must be empty strings and not None, because they need to be put in a textbox
    for index,key in enumerate(['questiontext','questionpic','answertext','answerpic','topic']):
        if key in rawcard:
            answer[index] = rawcard[key]
    qtext, qpic, atext ,apic,topic = answer
    
    print(f"answer = {answer}")
    
    #create the images
    
    _, img_text  = imop.CreateTextCard(self,qtext)
    _, img_pic   = imop.findpicture_path(self,qpic)
    _, img_text2 = imop.CreateTextCard(self,atext)
    _, img_pic2  = imop.findpicture_path(self,apic)
    image  = imop.CombinePics(img_text,img_pic)
    image2 = imop.CombinePics(img_text2,img_pic2)
    
    #%%    
    #self.cardorder = [index]
    #self.index = 0
    #%% resize images
    image = image.resize((int(image.size[0]/2),int(image.size[1]/2)), PIL.Image.ANTIALIAS)
    BMP_q = imop.PILimage_to_Bitmap(image)
    try:
        image2 = image2.resize((int(image2.size[0]/2),int(image2.size[1]/2)), PIL.Image.ANTIALIAS)
        BMP_a = imop.PILimage_to_Bitmap(image2)
    except:
        BMP_a = wx.NullBitmap
    #%% images to dialog window                
    data = [BMP_q, BMP_a, qtext, qpic, atext, apic, topic]        
    print(f"data = {data}")
    
    with gui.MyDialog9(self,data) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            #Get user data
            qtext = dlg.m_textCtrlQtext.GetValue()
            qpic  = dlg.m_textCtrlQpic.GetValue()
            atext = dlg.m_textCtrlAtext.GetValue()
            apic  = dlg.m_textCtrlApic.GetValue()
            topic = dlg.m_textCtrlTopic.GetValue()                  
            DelCard = dlg.m_checkBoxDel.GetValue()
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'LATEXOPERATIONS: show popupcard: pressed OK\n\t Delete card = {DelCard}')            
            #make changes
            if DelCard or (qtext.strip() == '' and qpic.strip() ==''):
                """the entire card will be deleted"""
                self.Latexfile.popline(trueindex)
                try:
                    self.nr_questions -= 1
                except:
                    pass
            else:
                self.Latexfile.replace_line(trueindex, qtext= qtext, qpic = qpic, atext = atext,apic = apic, topic = topic)
            
            self.Refresh()                                    
            
        else: #dialog closed by user
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'LATEXOPERATIONS: show popupcard: dialog closed by user: bookname = {self.booknamepath}')

