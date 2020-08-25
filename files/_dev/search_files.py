# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 15:42:25 2019

@author: Anton
"""


""" This program finds and counts all occurances of a function or keyword in 
any file in the same directory of this file. This is for debugging purposes
in case you change a function in a certain file which would influence other files."""  
#%%
SEARCH_keyword = "settings_set"
DISPLAY_LINE   = False

#%%
SEARCH_keyword = SEARCH_keyword.lower()
import os
from termcolor import colored
dir_path = os.path.dirname(os.path.realpath(__file__))
files = os.listdir(dir_path)
pyfiles = [os.path.join(dir_path,f) for f in files if (os.path.isfile(f) and os.path.splitext(f)[1]=='.py' and f != os.path.basename( __file__))]

GLOBCOUNT = 0 
for _, pyfile in enumerate(pyfiles):
    FOUND = False
    COUNT = 0
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
    if FOUND:
        print(colored(f"found {COUNT} times in file {os.path.basename(pyfile)}","red"))

if GLOBCOUNT == 0:
    print("Nothing found")
