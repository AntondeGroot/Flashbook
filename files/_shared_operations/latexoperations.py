# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 18:18:50 2019

@author: aammd
"""
import ast
from _settings.settingsfile import settings
import PIL
import os
import fc_functions    as f2
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
        
        
        if path:
            self.filepath = path
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: selected file {path}')
            self.bookname = Path(path).stem
        if Path(self.filepath).exists():
            file = open(self.filepath, 'r',newline='\r')
            linefile = file.readlines()
            file.close()
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: loaded file {path}')
        else:
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: file does not exist {path}')

        linefile = [x for x in linefile if x.strip() != ''] #exclude empty lines
        ## check if file is up-to-date and has \sizes{[0,0,0,0,0]}
        uptodate = True
        for i, line in enumerate(linefile):
            if '\size{' not in line and line.strip() != '':
                log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: \size not in line: {line}')
                uptodate = False
                q,a,t,_ = self.line_to_components(line)     
                newline = self.insert_line(question = q, answer = a, topic = t)
                linefile[i] = newline
            if '\sizes{[(0,0), (0,0), (0,0), (0,0), (0,0)]}' in line:
                uptodate = False
                q,a,t,_ = self.line_to_components(line)     
                newline = self.insert_line(question = q, answer = a, topic = t)
                linefile[i] = newline
            if i == 0:
                self.bookname
                q,a,t,_ = self.line_to_components(line)
                t = self.bookname
                newline = self.insert_line(question = q, answer = a, topic = t)
                linefile[i] = newline
                
        if not uptodate:
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: linefile was not uptodate')
            self.save_file(linefile)
            
        self.linefile = linefile
        self.linefile_plt = linefile
        return linefile
    def resetlatexfile(self):
        ipath = self.filepath
        """remove all extraneous \n's in the file
        I tried to implement it in save_file but for some reason it doesn't work"""
        file = open(ipath, 'r',newline='\r\n')
        linefile = file.readlines()
        file.close()
        linefile2 = []
        for i, item in enumerate(linefile):
            if type(item) == str:
                if item.strip() != '':
                    lst = item.split("\n")
                    for it in lst:
                        it = it.lstrip("\n")
                        linefile2.append(it)    
        with open(ipath, 'w') as output: 
            for item in linefile2:
                output.write("%s" % item)
        output.close()
                
    def save_file(self,linefile):
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: saving latex file')
        #edit linefile to remove superfluos "\n"
        linefile2 = []
        for i, line in enumerate(linefile):
            if type(line) == str:
                if line.strip() != '':
                    splitline = line.split("\n")
                    for string in splitline:
                        #remove \n if the string starts with it
                        string = string.lstrip("\n")
                        string = string.rstrip("\r")
                        string = string.rstrip("\n")
                        linefile2.append(string)
        self.linefile = linefile2
        try:     
            with open(self.filepath, 'w') as output: 
                for item in linefile2:
                    output.write("%s\n" % item)
            output.close()
        except:
            pass
        
        self.resetlatexfile()
    def line_to_components(self,line):
        q = argument(self.question_command,line)
        a = argument(self.answer_command,line)
        t = argument(self.topic_command,line)
        s = argument(self.size_command,line)
        return q,a,t,s
    
    def combine_tuples(self,tuples_list):
        if type(tuples_list) == tuple:
            tuples_list = [tuples_list]
        w0,h0 = 0, 0 
        for size in tuples_list:
            w,h = size
            w0 = max(w0,w)
            h0 += h
        return w0,h0
    def file_to_rawcards(self):
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: file converted to raw cards')
        assert self.linefile != []
        cards = []
        
        for index, line in enumerate(self.linefile):
            q = argument(self.question_command,line)
            a = argument(self.answer_command,line)
            t = argument(self.topic_command,line)
            s = argument(self.size_command,line)
            s = ast.literal_eval(s)
            if s[4] != (0,0):
                size = s[4]
                cards.append({'index':index,'t': t,'size':size,'page':999,'pos':(0,0),'scale':1})
            size = self.combine_tuples(s[:4])
            if a.strip() != '':
                cards.append({'index':index,'q' : q, 'a' : a, 'size':size,'page':999,'pos':(0,0),'scale':1,'border' : (0,0)})
            else:
                cards.append({'index':index,'q' : q, 'size':size,'page':999,'pos':(0,0),'scale':1,'border' : (0,0)})
        self.cards = cards
        
        
        return cards
    def textsize(self,text):
        #remove user defined macro's
        file = open(str(Path(self.notesdir, "usercommands.txt")), 'r')
        commandsfile = file.readlines()
        file.close()
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
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: pics {picname} has size: {w,h}')
            return (w,h)
        except:
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: Error: pics with name "{picname}" could not be found and thus has no size')
            return (0,0)
    def topicsize(self,text):
        self.a4page_w = 1240 
        width_card = self.a4page_w
        height_card = int(math.ceil(len(text)/40))*0.75*100
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: topic = {text} has size: {width_card,height_card}')
        if height_card != 0:            
            return (width_card,height_card)
        else:
            return (0,0)
    
    def getline_i_card(self,index):
        
        line = self.linefile[index]
        q,a,t,_ = self.line_to_components(line)
        qtext = argument(r"\\text{",q)
        qpic  = argument(r"\\pic{",q)
        atext = argument(r"\\text{",a)
        apic  = argument(r"\\pic{",a)
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: getline card of index: {index}\n\t qpic = {qpic},\n\t apic = {apic}')
        if qpic.strip() != '' and qtext.strip() != '':
            q = qtext+r"\pic{"+qpic+"}"
        if qpic.strip() != '' and qtext.strip() == '':
            q = r"\pic{"+qpic+"}"
        if qpic.strip() == '' and qtext.strip() != '':
            q = qtext
        
        if apic.strip() != '' and atext.strip() != '':
            a = atext+r"\pic{"+apic+"}"
        if apic.strip() != '' and atext.strip() == '':
            a = r"\pic{"+apic+"}"
        if apic.strip() == '' and atext.strip() != '':
            a = atext
        
        return {'qtext':qtext,'qpic':qpic,'atext':atext,'apic':apic,'t':t,'q':q,'a':a}
    
    def popline(self,index):
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: popline with index {index}')
        index = int(index)
        self.linefile.pop(index)
        self.save_file(self.linefile)
        
    def replace_line(self,index, qtext= '', qpic = '', atext = '',apic = '', topic = '', size = [(0,0),(0,0),(0,0),(0,0),(0,0)]):
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: replace line with index {index}')
        size = str([self.textsize(qtext),self.picsize(qpic), self.textsize(atext),self.picsize(apic),self.topicsize(topic)])
        
        question = ''
        if qtext != '':
            question += r"\text{"+qtext+"}"
        if qpic != '':
            question += r"\pic{"+qpic+"}"
        answer = ''
        if atext != '':
            answer += r"\text{"+atext+"}"
        if apic != '':
            answer += r"\pic{"+apic+"}"
                        
        line =  r"\quiz{" + question + "}" + r"\ans{" + answer + "}" + r"\topic{" + topic + "}" + r"\size{" + size + "}"
        self.linefile[index] = line
        self.save_file(self.linefile)
    def addline(self,index = 0,question = '', answer = '', topic = '', size = [(0,0),(0,0),(0,0),(0,0),(0,0)]):
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: addline with index {index}')
        #when the user adds a question and answer, which by definition does not include a picture
        qpic  = ''
        qtext = question
        apic  = ''
        atext = answer
        topic = topic
        size = str([self.textsize(qtext),self.picsize(qpic), self.textsize(atext),self.picsize(apic),self.topicsize(topic)])
        line = r"\quiz{" + r"\text{"+question+ "}" + "}" + r"\ans{" +r"\text{"+ answer+ "}" + "}" + r"\topic{" + topic + "}" + r"\size{" + size + "}"
        self.linefile.insert(index,line)
        
        self.save_file(self.linefile)
    def insert_line(self, question = '', answer = '', topic = '', size = [(0,0),(0,0),(0,0),(0,0),(0,0)]):
        cmd   = self.pic_command
        qpic  = argument(cmd,question)
        qtext = argument(r"\\text{",question)
        apic  = argument(self.pic_command,answer)
        atext = argument(r"\\text{",answer)
        # convert qtext/atext to text without user defined LaTeX : is done in textsize
        size = str([self.textsize(qtext),self.picsize(qpic), self.textsize(atext),self.picsize(apic),self.topicsize(topic)])
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS LATEXFILE: insertline\n\t question: {question}\n\t answer: {answer}\n\t topic: {topic}\n\t size: {size}')
        return r"\quiz{" + question + "}" + r"\ans{" + answer + "}" + r"\topic{" + topic + "}" + r"\size{" + size + "}"


def ShowPopupCard(self,trueindex):
    # get the card
    rawcard = self.Latexfile.getline_i_card(trueindex)
    # get data from the cards
    log.DEBUGLOG(debugmode=self.debugmode, msg=f'LATEXOPERATIONS: show popupcard: rawcard = {rawcard}')
    qtext = rawcard['qtext']
    qpic  = rawcard['qpic'] 
    atext = rawcard['atext']
    apic  = rawcard['apic']
    topic = rawcard['t']
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

