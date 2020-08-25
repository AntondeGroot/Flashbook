# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 15:42:25 2019

@author: Anton
"""

""" This program finds and counts all occurances of any function in
any file in the same directory of this file. This is for debugging purposes
in case you change a function in a certain file which would influence other files."""  


from pathlib import Path
import re
import os
from termcolor import colored

dir_path = os.path.dirname(os.path.realpath(__file__))
files    = os.listdir(dir_path)
pyfiles  = [os.path.join(dir_path,file) for file in files if (os.path.isfile(file) and os.path.splitext(file)[1]=='.py' and file != os.path.basename( __file__))]

# search all files for defined functions
funclist  = {}
forbiddenlist = {}
for _, pyfile in enumerate(pyfiles):
    with open(pyfile, 'r') as file:
        lines = file.readlines()
    file.close()
    for line_index, line in enumerate(lines):
        # a line needs to contain "def ():"
        if all([(symb in line) for symb in ['def','(',')',':']]): 
            
            beginindex = [m.start() for m in re.finditer('def', line )][0]+4        
            endindex = [m.start() for m in re.finditer('\(', line )][0]
            
            found_function = line[beginindex:endindex]
            if found_function not in funclist.keys() and found_function not in forbiddenlist.keys():                        
                funclist[found_function] = [0,Path(pyfile).name,line_index]
            else:
                try:
                    funclist.pop(found_function)
                    forbiddenlist[found_function] = 0
                except:
                    pass

# search all files for occurances when the function was used and not when it was just defined
for _, pyfile in enumerate(pyfiles):
    with open(pyfile, 'r') as file:
        lines = file.readlines()
    file.close()
    for _, line in enumerate(lines):        
        for function in funclist.keys():
            if function in line and 'def' not in line:
                #print(f"word = {word}")
                count = funclist[function][0]+1
                funclist[function] = [count]+funclist[function][1:]

# lay out:
filenamelen = 0
funcnamelen = 0
for i,item in enumerate(funclist):
    if funclist[item][0] == 0:
        filenamelen = max(filenamelen,len(funclist[item][1] ))
        funcnamelen = max(funcnamelen,len(item))
        
# print results:
COUNT = 0
for i,item in enumerate(funclist):
    if funclist[item][0] == 0:    
        COUNT += 1
        len_1 = funcnamelen - len(item)
        len_2 = filenamelen - len(funclist[item][1]) + 2
        print(colored("unused function:","red")+f"    {item}"+f"{' '*len_1}" +colored(" file    ","red") + f"{funclist[item][1]}"+f"{' '*len_2}" + colored(" line ","red") + f"{funclist[item][2]}")


if COUNT == 0 :
    print("No unused functions have been found")



