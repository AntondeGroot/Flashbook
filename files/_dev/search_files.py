# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 15:42:25 2019

@author: Anton
"""


""" This program finds and counts all occurances of a function or keyword in 
any file in the same directory of this file. This is for debugging purposes
in case you change a function in a certain file which would influence other files."""  
#%%
SEARCH_keyword = "self.rowindex" 
DISPLAY_LINE   = False

import os
from pathlib import Path







#%%
SEARCH_keyword = SEARCH_keyword.lower()

from termcolor import colored
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = Path(os.getcwd()).parent
pyfiles = []
for path, subdirs, files in os.walk(dir_path):
    for name in files:
        pyfiles.append(os.path.join(path, name))


pyfiles = [f for f in pyfiles if (os.path.isfile(f) and os.path.splitext(f)[1]=='.py' and os.path.basename(f) != os.path.basename( __file__))]

GLOBCOUNT = 0 
for pyfile in pyfiles:
    FOUND = False
    COUNT = 0
    try:
        with open(pyfile, 'r') as file:
            lines = file.readlines()
        file.close()
        for _, line in enumerate(lines):
            if SEARCH_keyword in line.lower():
                if DISPLAY_LINE == True:
                    print(line)
                FOUND = True
                COUNT += 1
                GLOBCOUNT += 1
    except:
        pass
    if FOUND:
        parentdir = Path(pyfile).parent
        print(colored(f"found {COUNT} times in file {os.path.basename(Path(pyfile).parent)}\{os.path.basename(pyfile)}","red"))

if GLOBCOUNT == 0:
    print("Nothing found")
