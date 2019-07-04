# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 14:13:09 2019
@author: Anton
"""

from pathlib import Path
from termcolor import colored
import time
import os
import json

class Timing():
    
    """Class that displays how long certain parts of code takes to execute, and the total runtime."""
    
    """Example:
    TT = Timing('loading files')
    TT.update('processing files')
    TT.update('storing data')
    TT.stop()
    """
    
    def __init__(self, message):
        self.time_started = time.time()
        self.time_lastused = self.time_started
        self.message = message
        self.index = 1

    def update(self,message):        
        output = f"{self.index}) {self.message} took {round(time.time()-self.time_lastused,2)} seconds"
        print(colored(output,"red"))                
        self.time_lastused = time.time()
        self.message = message
        self.index += 1
        
    def reset(self,message):
        self.time_lastused = time.time()
        self.index = 1
        self.message = message
        
    def stop(self):
        output = f"{self.index}) {self.message} took {round(time.time()-self.time_lastused,2)} seconds"
        print(colored(output,"red"))
        output2 = f"it took in total: {round(time.time()-self.time_started,2)} seconds"
        print(colored(output2,"red"))        
        


class TimeCount: 
    
    """ A Class that is used to register how long a user has been working. 
    Thiss class will be called whenever mouse events or key events are registered.
    To limit the use of this class, there are some bounds: since it doesn't need to be called every second
    nor does it need to open and save a file every second.
    The goal: register the #minutes a user is using the program, inaccuracy in #seconds is insignificant
    """
    
    def __init__(self, bookname, filename):
        self.path     = Path(os.getenv("LOCALAPPDATA"),"Flashbook","settings",f"timecount_{filename}.json")
        self.timedict = {}
        self.book     = bookname
        self.date     = time.strftime("%d%m%y")
        ## variables
        self.count = 0
        self.timelastchecked = time.time()
        self.timelastsaved   = time.time()
        # bounds in seconds
        self.lowerbound = 1     # when to update the count
        self.savethreshold = 5  # when to save the current count
        self.upperbound = 60    # when to consider the user to be idle    
        
        if self.path.is_file():
            try:
                with open(self.path, 'r') as file:
                    self.timedict = json.load(file)
                file.close()
                if self.date in self.timedict.keys():
                    if self.book in self.timedict[self.date].keys():
                        self.count = self.timedict[self.date][self.book]
                    else:
                        self.timedict[self.date][self.book] = self.count
                else:
                    self.timedict[self.date] =  {self.book : self.count}
                
                
            except: #file is corrupted: restore the file
                print(colored("Error: TimeCount file is corrupted","red"))
                # remove
                self.path.unlink() 
                self.count = 0 
                self.timedict[self.date][self.book] = self.count
                # save
                with open(self.path, 'w') as file:
                    file.write(json.dumps(self.timedict))
                file.close()
                self.timelastchecked = time.time()
                self.timelastsaved = time.time()
        else: #the file will be saved eventually, even if it does not exist yet
            self.timedict[self.date] = {self.book : self.count}
            with open(self.path, 'w') as file:
                file.write(json.dumps(self.timedict))
            file.close()
    
    def set_bounds(self, lower = 0, threshhold = 0, upper = 0):
        if type(lower) == int and lower > 0:
            self.lowerbound = lower
        if type(threshhold) == int and threshhold > 0:
            self.savethreshold = threshhold
        if type(upper) == int and upper > 0:
            self.upperbound = upper
            
    
    def update(self):
        
        timenow  = time.time()
        timedelta = timenow-self.timelastchecked
        
        if timedelta < self.upperbound: # user has not been idle    
            if timedelta > self.lowerbound:     
                #update
                self.count +=  timedelta
                self.timelastchecked = time.time()                
                self.timedict[self.date][self.book] = round(self.count,2)            
                if (timenow - self.timelastsaved) > self.savethreshold:
                    with open(self.path, 'w') as file:
                        file.write(json.dumps(self.timedict))
                    file.close()
                    self.timelastsaved = time.time()
                    
        else: # user has been idle for too long, reload count from saved file
            with open(self.path, 'r') as file:
                self.timedict = json.load(file)
                if self.date in self.timedict.keys():
                    if self.book in self.timedict[self.date].keys():
                        self.count = self.timedict[self.date][self.book]
            file.close()
            self.timelastchecked = time.time()
            self.timelastsaved = time.time()
