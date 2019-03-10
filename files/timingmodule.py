# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 14:13:09 2019

@author: Anton
"""
bookname = "book1"

timedict = {}
count = 120
#%%
bookname = "book2"

#date = time.strftime("%d%m%y")

class C: 

    counter = 0
    
    def __init__(self): 
        type(self).counter += 1

    def do(self):
        type(self).counter -= 1

x = C()

#%%






#%%

from termcolor import colored
import time
import os
import json

class TimeCount: 
    #class attributes
    count = 0
    timelastchecked = time.time()
    timelastsaved = time.time()
    threshold1 = 1
    threshold2 = 5
    upperbound = 180
    
    def __init__(self, bookname):
        self.path     = os.path.join(os.getenv("LOCALAPPDATA"),"Flashbook","temporary","timecount.json")
        self.timedict = {}
        self.book     = bookname
        self.date     = time.strftime("%d%m%y")
        
        #self.timelastsave = self.timelast
        print(colored(f"selfcount is {self.count}","green"))
        if os.path.isfile(self.path):
            try:
                with open(self.path, 'r') as file:
                    self.timedict = json.load(file)
                    print(type(self.timedict))
                    if self.date in self.timedict.keys():
                        if self.book in self.timedict[self.date].keys():
                            type(self).count = self.timedict[self.date][self.book]
                        else:
                            self.timedict[self.date][self.book] = count
                    else:
                        self.timedict[self.date][self.book] =  count
                file.close()
                print(f"count is {type(self).count}")
            except: #file is corrupted
                print(colored("file is corrupted","red"))
                os.remove(self.path)
                type(self).count = 0 
                self.timedict[self.date][self.book] = type(self).count
                # save
                with open(self.path, 'w') as file:
                    file.write(json.dumps(self.timedict))
                file.close()
                type(self).timelastchecked = time.time()
                type(self).timelastsaved = time.time()
            print(colored("FOUND THE FILE",'green'))
        else:
            self.timedict[self.date] = {self.book : type(self).count}
            print(False)
            
    def set_threshold1(self,var):
        if type(var) == int and var > 0:
            type(self).threshold1 = var
            
    def set_threshold2(self,var):
        if type(var) == int and var > 0:
            type(self).threshold2 = var
            
    def set_upperbound(self,var):
        if type(var) == int and var > 0:
            type(self).upperbound = var
    
    def update(self):
        v = type(self)
        
        timenow  = time.time()
        timedelta = timenow-v.timelastchecked
        
        if timedelta < v.upperbound: # in seconds
        
            if timedelta > v.threshold1: #in seconds
                
                print(colored("in time","green"))
                #print(timedelta)
                #update
                print(f"typecount = {type(self).count}")
                v.count +=  timedelta
                #print(f"timecount is now {type(self).count}\n")
                v.timelastchecked = time.time()
                
                self.timedict[self.date][self.book] = type(self).count
            
                if (timenow - v.timelastsaved) > v.threshold2:
                    print(f"saved {self.book, type(self).count, self.path}")
                    with open(self.path, 'w') as file:
                        file.write(json.dumps(self.timedict))
                    file.close()
                    v.timelastsaved = time.time()
                
                
                    #TimeCount(self.book).save()
        else:
            #user has been idle for too long, reload count from saved file
            with open(self.path, 'r') as file:
                self.timedict = json.load(file)
                if self.date in self.timedict.keys():
                    if self.book in self.timedict[self.date].keys():
                        v.count = self.timedict[self.date][self.book]
            v.timelastchecked = time.time()
            v.timelastsaved = time.time()
            file.close()
            #print("too soon")


TC = TimeCount("book2")
for i in range(11):
    time.sleep(1)
    TC.update()

time.sleep(20)

for i in range(11):
    time.sleep(1)
    TC.update()
