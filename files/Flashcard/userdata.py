# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 22:18:06 2020

@author: Anton
"""
import _logging.log_module as log
import json

def save_stats(self):
    """keep track of user progress data in a dict
    key: bookname
    value: data such as score, which question, ..."""
    
    key   = self.bookname
    value = self.resumedata[self.bookname]
    try:
        value = self.resumedata[self.bookname]
        with open(self.statsdir, 'r') as file:
            try:
                dictionary = json.load(file)
            except:
                dictionary = {}
        with open(self.statsdir, 'w') as file:
            dictionary[self.bookname] = value            
            file.write(json.dumps(dictionary) )
    except: #key was not in the dictionary
        try:
            with open(self.statsdir, 'r') as file:
                try:
                    dictionary = json.load(file)
                except:
                    dictionary = {}
                dictionary.update({key: value})
        except: #the file does not exist
            dictionary = {}
            dictionary.update({key: value})
        with open(self.statsdir, 'w') as file:
            file.write(json.dumps(dictionary) )
            
def load_stats(self):    
    try:
        with open(self.statsdir, 'r') as file:
            
            self.resumedata = json.load(file)
            self.score = self.resumedata[self.bookname]['score']
            self.index = self.resumedata[self.bookname]['index']
            self.nr_questions = self.resumedata[self.bookname]['nr_questions']
            self.cardorder = self.resumedata[self.bookname]['cardorder']
            score = round(float(self.score)/self.nr_questions*100,1)
            self.m_Score.SetValue(f"{score} %")    
    except:
        log.DEBUGLOG(debugmode=self.debugmode,msg=f"FC FUNCTIONS: no stats were found for the book")
        
def remove_stats(self):
    try:
        with open(self.statsdir, 'r') as file:
            dictionary = json.load(file)
        with open(self.statsdir, 'w') as file:
            del dictionary[self.bookname]
            file.write(json.dumps(dictionary))
    except: # no update, just overwrite with popped dictionary
        log.ERRORMESSAGE("Error could not load saved stats from RemoveStats()")
    
    
def set_stats(self):
    self.resumedata[self.bookname]= {'score': self.score, 'index': self.index, 'nr_questions':self.nr_questions, 'cardorder': self.cardorder[:self.nr_questions] }