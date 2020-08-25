# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 22:44:27 2019

@author: aammd
"""

import os
import re
import numpy as np
"""Between version 1.4.x and 1.5.0 changes have been made in the way the userdata is stored and retrieved
Before: \quiz{some text\pic{picname.jpg}}
Now:    \quiz{\text{some text}\pic{picname.jpg}\size{size of text, size of pic}
This way it will be a lot faster to create the PDFs of the notes because it no longer needs to determine the size of each card.
It will only determine the size if either no size is not yet known (for example after this program is run).
Or when a card is changed."""


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
    
def separatetext(command,line):
    startpos   = [m.start() for m in re.finditer(command, line)]
    if startpos != []:
        return line[0:startpos[0]]
    else:#no \pic command so it is only text
        return line
#%%
basedir = os.path.join(os.getenv("LOCALAPPDATA"),"Flashbook","files")
paths = [os.path.join(basedir,x) for x in os.listdir(basedir) if x != 'usercommands.txt']

for filepath in paths:
    print("succes!!")
    file = open(filepath, 'r',newline='\r')
    linefile = file.readlines()
    linefile = [x for x in linefile if x.strip() != ''] #exclude empty lines
    for i,line in enumerate(linefile):
        #initialize
        qtext = ''
        qpic = ''
        atext = ''
        apic = ''
        topic = ''
        #
        quiz = argument(r"\\quiz{",line)
        qpic = argument(r"\\pic{",quiz)
        
        if r"\text{" not in quiz:#needs 1\
            qtext = separatetext(r"\\pic",quiz)
        else:
            print(f"text is in Q {quiz}")
            qtext = argument(r"\\text{",quiz)#needs 2\\
            print(f"qtext = {qtext}")
            
        answer = argument(r"\\ans{",line)
        apic = argument(r"\\pic{",answer)
        if r"\text{" not in answer:#needs 1\
            atext = separatetext(r"\\pic",answer)
        else:
            atext = argument(r"\\text{",answer)             
            
        topic = argument(r"\\topic{",line)
        #new layout
        if qtext.strip() != '':
            qtext = r"\text{" + qtext + "}"
        else:
            qtext = ''
        if qpic.strip() != '':
            qpic = r"\pic{" + qpic + "}"
        if atext.strip() != '':
            atext = r"\text{" + atext + "}"
        else:
            atext = ''
        if apic.strip() != '':
            apic = r"\pic{" + apic + "}"
        newline = r"\quiz{"+qtext +qpic+"}"+r"\ans{"+atext+apic+"}"+r"\topic{"+topic+"}"
        linefile[i] = newline
        
    with open(filepath, 'w') as output: 
        outputfile = ''
        for i,line in enumerate(linefile):
            outputfile += line
            if i != len(linefile)-1:
                outputfile += "\n"        
        output.write(outputfile)
    