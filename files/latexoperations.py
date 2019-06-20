# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 18:18:50 2019

@author: aammd
"""
from settingsfile import settings
import PIL
import os
import fc_functions    as f2
from pathlib import Path
import numpy as np
from folderpaths import paths
import re
import math
#%% functions

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
class Commands():
    def __init__(self):
            # some commands used to create the flashcards and seperate elements: question/answer/picture
            # this way it will remain clear for the user so that he could manually change an entry.
            self.pic_command      = r"\\pic{"
            self.question_command = r"\\quiz{"
            self.answer_command   = r"\\ans{"
            self.topic_command    = r"\\topic{"
            self.size_command     = r"\\size{"
    def pic(self):
        return self.pic_command
    def question(self):
        return self.question_command
    def answer(self):
        return self.answer_command
    def topic(self):
        return self.topic_command
    def size(self):
        return self.size_command    
    
class Latexfile(Commands,settings):
    def __init__(self):
        Commands.__init__(self)
        
        settings.__init__(self)
        settings.settings_get(self)
        self.linefile = []
        self.filepath = ''
        self.cards = {}
        self.filename = ''
    def loadfile(self,path):
        if path != None:
            self.filepath = path
            self.bookname = Path(path).stem
        if Path(self.filepath).exists():
            file = open(self.filepath, 'r',newline='\r')
            linefile = file.readlines()

        linefile = [x for x in linefile if x.strip() != ''] #exclude empty lines
        ## check if file is up-to-date and has \sizes{[0,0,0,0,0]}
        count = 0
        for i, line in enumerate(linefile):
            if '\size{' not in line and line.strip() != '':
                print(self.size_command, line)
                print("size not in line")
                count += 1
                q,a,t,_ = self.line_to_components(line)     
                newline = self.insert_line(question = q, answer = a, topic = t)
                linefile[i] = newline
        if count != 0:
            self.save_file(linefile)
        ##  
        self.linefile_raw = linefile
        self.linefile_plt = linefile
        return linefile
    
    def save_file(self,linefile):
        with open(self.filepath, 'w') as output: 
            file = ''
            for i,line in enumerate(linefile):
                file += line
                if i != len(linefile)-1:
                    file += "\n"
            
            output.write(file)
    def line_to_components(self,line):
        q = argument(self.question_command,line)
        a = argument(self.answer_command,line)
        t = argument(self.topic_command,line)
        s = argument(self.size_command,line)
        return q,a,t,s
    
    def file_to_rawcards(self):
        assert self.linefile_raw != []
        cards = {}
        
        for index, line in enumerate(self.linefile_raw):
            q = argument(self.question_command,line)
            a = argument(self.answer_command,line)
            t = argument(self.topic_command,line)
            s = argument(self.size_command,line)
            
            cards[index] = {'q': r"\quiz{"+q+"}"+r"\ans{"+a+"}", 't': t,'size':s} #cards contains q,t,s
        self.cards = cards
        
        return cards
    def textsize(self,text):
        #remove user defined macro's
        file = open(str(Path(self.notesdir, "usercommands.txt")), 'r')
        commandsfile = file.readlines()
        #print(f"text is of type {type(text)}: {text}")
        if text.strip() != '':
            text = f2.ReplaceUserCommands(commandsfile,text)
            # get image size
            imbool, im = f2.CreateTextCard(self,'manual',text)
            if imbool:
                return im.size
            else:
                return (0,0)
        else:
            return (0,0)
    def picsize(self,picname):
        try:
            w,h = PIL.Image.open(os.path.join(self.pics(), self.bookname, picname)).size
            return (w,h)
        except:
            return (0,0)
    def topicsize(self,text):
        self.a4page_w = 1240 
        width_card = self.a4page_w
        height_card = int(math.ceil(len(text)/40))*0.75*100
        print(f"! topic = {text}, size = {width_card},{height_card}")
        if height_card != 0:
            return (width_card,height_card)
        else:
            return (0,0)
    
    

    
    def insert_line(self, question = '', answer = '', topic = '', size = [(0,0),(0,0),(0,0),(0,0),(0,0)]):
        cmd   = self.pic_command
        qpic  = argument(cmd,question)
        qtext = argument(r"\\text{",question)
        apic  = argument(self.pic_command,answer)
        atext = argument(r"\\text{",answer)
        # convert qtext/atext to text without user defined LaTeX : is done in textsize
        
        size = str([self.textsize(qtext),self.picsize(qpic), self.textsize(atext),self.picsize(apic),self.topicsize(topic)])
        return r"\quiz{" + question + "}" + r"\ans{" + answer + "}" + r"\topic{" + topic + "}" + r"\size{" + size + "}"

