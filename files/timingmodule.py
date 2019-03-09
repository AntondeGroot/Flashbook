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



import time
import os
import json

class TimeCount: 
    
    def __init__(self, bookname):
        
        self.path = os.path.join(os.getenv("LOCALAPPDATA"),"Flashbook","temporary","timecount.json")
        self.timedict = {}
        self.book  = bookname
        self.date  = time.strftime("%d%m%y")
        self.count = 0
        self.timenow  = time.time()
        self.timelast = self.timenow #sync
        self.timelastsave = self.timelast
        
        if os.path.isfile(self.path):
            try:
                with open(self.path, 'r') as file:
                    self.timedict = json.load(file)
                    print(type(self.timedict))
                    
                    self.count = self.timedict[self.date][self.book]
                file.close()
                print(f"count is {self.count}")
            except: #file is corrupted
                os.remove(self.path)
                self.count = 0 
                self.timedict[self.date] = {self.book : self.count}
                # save
                #TimeCount(self.book).save()
                
            print(True)
        else:
            self.timedict[self.date] = {self.book : self.count}
            #save
            #TimeCount(self.book).save()
            print(False)
        if self.date in self.timedict.keys() and self.book in self.timedict[self.date].keys():
            self.count = self.timedict[self.date][self.book]    
        else:
            self.count = 0
            
    def save(self):
        print(f"saved {self.book, self.count, self.path}")
        with open(self.path, 'w') as file:
            file.write(json.dumps(self.timedict))
        file.close()
        
    def update(self):
        
        self.timenow  = time.time()
        timedelta = self.timenow-self.timelast
        print(timedelta)
        if timedelta > 1:
            print("in time")
            print(timedelta)
            #update
            self.timelast = time.time()
            TimeCount(self.book).save()
        else:
            print("too soon")

TC = TimeCount("book1")
TC.update()
time.sleep(0.5)
print("upd1")
TC.update()
time.sleep(1.1)
print("upd2")
TC.update()
#a = x.save("hoera")


#timecount.save('hallo')
#%%
    
"""
def timecount_save(timedict,date,bookname,count):
    if date in timedict.keys():
        print(f"is in {count}")
        subdict = timedict[date]
        print(subdict)
        timedict[date][bookname] = count   
    else:
        print("not in")
        timedict[date] = {bookname : count}
        
def timecount_update()

def timecount_get(timedict,date,bookname):
    if date in timedict.keys() and bookname in timedict[date].keys():
        count = timedict[date][bookname]    
    else:
        count = 0
    return count
#count = gettimecount(timedict,date,bookname)
savetimecount(timedict,date,bookname,count)

for i in range(10):
    bookname = f"book{i}"    
    count = gettimecount(timedict,date,bookname)
    savetimecount(timedict,date,bookname,count)

#when program starts
#self.timelast = time.time()
#self.timenow = self.timelast
#self.deltatime = 60 


"""