# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 14:13:09 2019

@author: Anton
"""


from termcolor import colored
import time
import os
import json

class Timing():
    "Class that displays how long certain parts of code takes to execute."
    time_0 = time.time()
    message = ""
    index = 1
    def __init__(self, message):
        v = type(self)
        v.time_0 = time.time()
        v.message = message
    def update(self,message):
        v = type(self)
        print(colored(f"{v.index}) {v.message} took {round(time.time()-v.time_0,2)} seconds","red"))        
        v.time_0 = time.time()
        v.message = message
        v.index += 1
    def reset(self,message):
        v = type(self)
        v.time_0 = time.time()
        v.message = message
        v.index = 1
    def stop(self):
        v = type(self)
        print(colored(f"{v.index}) {v.message} took {round(time.time()-v.time_0,2)} seconds","red"))        
        


class TimeCount: 
    """ A Class that is used to register how long a user has been working. 
    Thiss class will be called whenever mouse events or key events are registered.
    To limit the use of this class, there are some bounds: since it doesn't need to be called every second
    nor does it need to open and save a file every second.
    The goal: register the #minutes a user is using the program, variance in #seconds is insignificant
    """
    
    #class attributes
    count = 0
    timelastchecked = time.time()
    timelastsaved   = time.time()
    # bounds in seconds
    lowerbound = 1      # when to update the count
    savethreshold = 5      # when to save the current count
    upperbound = 60    # when to consider the user to be idle
    
    def __init__(self, bookname, filename):
        self.path     = os.path.join(os.getenv("LOCALAPPDATA"),"Flashbook","temporary",f"timecount_{filename}.json")
        self.timedict = {}
        self.book     = bookname
        self.date     = time.strftime("%d%m%y")
        v = type(self)
        v.count = 0
        if os.path.isfile(self.path):
            try:
                with open(self.path, 'r') as file:
                    self.timedict = json.load(file)
                file.close()
                if self.date in self.timedict.keys():
                    if self.book in self.timedict[self.date].keys():
                        v.count = self.timedict[self.date][self.book]
                    else:
                        self.timedict[self.date][self.book] = v.count
                else:
                    self.timedict[self.date] =  {self.book : v.count}
                
                
            except: #file is corrupted: restore the file
                print(colored("Error: TimeCount file is corrupted","red"))
                os.remove(self.path)
                v.count = 0 
                self.timedict[self.date][self.book] = v.count
                # save
                with open(self.path, 'w') as file:
                    file.write(json.dumps(self.timedict))
                file.close()
                v.timelastchecked = time.time()
                v.timelastsaved = time.time()
        else: #the file will be saved eventually, even if it does not exist yet
            self.timedict[self.date] = {self.book : v.count}
            
    
    def set_bounds(self,var):
        if (type(var) == list or type(var) == tuple) and len(var) == 3:
            var1, var2, var3 = var
            if type(var1) == int and var1 > 0:
                type(self).lowerbound = var1
            if type(var2) == int and var2 > 0:
                type(self).savethreshold = var2
            if type(var3) == int and var3 > 0:
                type(self).upperbound = var3
        else:
            print(colored("Error: input to Class Method should be a list/tuple of length 3","red"))
            
    
    def update(self):
        v = type(self)
        
        timenow  = time.time()
        timedelta = timenow-v.timelastchecked
        
        if timedelta < v.upperbound:     # user has not been idle    
            if timedelta > v.lowerbound:                  
                #update
                v.count +=  timedelta
                v.timelastchecked = time.time()                
                self.timedict[self.date][self.book] = round(v.count,2)            
                if (timenow - v.timelastsaved) > v.savethreshold:
                    with open(self.path, 'w') as file:
                        file.write(json.dumps(self.timedict))
                    file.close()
                    v.timelastsaved = time.time()
                    
        else: # user has been idle for too long, reload count from saved file
            with open(self.path, 'r') as file:
                self.timedict = json.load(file)
                if self.date in self.timedict.keys():
                    if self.book in self.timedict[self.date].keys():
                        v.count = self.timedict[self.date][self.book]
            file.close()
            v.timelastchecked = time.time()
            v.timelastsaved = time.time()
