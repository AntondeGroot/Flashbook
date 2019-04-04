# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018

@author: Anton
"""

import os
import numpy as np
import PIL
from termcolor import colored
import wx
import matplotlib
import math
import PIL
from pathlib import Path
import re
import textwrap
import pylab
import matplotlib.backends.backend_agg as agg
#matplotlib.use('TKAgg')
import fc_functions as f2
import timingmodule as m6
import log_module as log
import program as p
import json
import ctypes
import gui_flashbook as gui

MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW



def buttonCorrect(self):
    f2.clearbitmap(self)
    if hasattr(self,'nr_questions') and self.nr_questions != 0 and hasattr(self,'bookname') and self.bookname != '':
        #import
        log.DEBUGLOG("test1","test2",debugmode = self.debugmode, msg="hallo")
        runprogram = self.runprogram
        self.index += 1    
        if runprogram == True:
            self.score +=1
        self.mode = 'Question'
        self.m_textCtrlMode.SetValue(self.mode)
        
        if self.score > self.nr_questions + 1:
            self.score = self.nr_questions
        if self.index > (self.nr_questions-1): 
            self.index = (self.nr_questions-1)
            f2.remove_stats(self)
            _score_ = round(float(self.score)/self.nr_questions*100,1)
            MessageBox(0, f"Your score is: {_score_}%", "Result", 1 )     
            runprogram = False
            if hasattr(self,'bookname'): # to stop from pop-up windows from appearing after the test is done
                delattr(self,'bookname')
            
        _score_ = round(float(self.score)/self.nr_questions*100,1)
        self.m_Score21.SetValue(f"{_score_} %")     
        self.m_CurrentPage21.SetValue(f"{self.index+1}")
        
        # update stats
        if runprogram == True:
            f2.set_stats(self)
            f2.save_stats(self)   
            # display cards
            f2.displaycard(self)
            f2.switch_bitmap(self)
        else:
            self.m_Score21.SetValue("")     
            self.m_CurrentPage21.SetValue("")
            self.m_TotalPages21.SetValue("")
            #reset pictogram
            path_repeat    = Path(self.resourcedir,"repeat.png")
            id_ = self.m_toolSwitch21.GetId()
            self.m_toolBar3.SetToolNormalBitmap(id_, wx.Bitmap( str(path_repeat), wx.BITMAP_TYPE_ANY ))
        #update self.vars accordingly
        self.runprogram = runprogram
    
def buttonWrong(self):
    matplotlib.pyplot.close('all') # otherwise too many pyplot figures will be opened -> memory
    f2.clearbitmap(self)
    if hasattr(self,'nr_questions') and self.nr_questions != 0 and hasattr(self,'bookname') and self.bookname != '':
        runprogram = self.runprogram
        self.index += 1
        self.mode = 'Question'
        self.m_textCtrlMode.SetValue(self.mode)  
        if self.index > (self.nr_questions-1):
            self.index = (self.nr_questions-1)
            f2.remove_stats(self)
            _score_ = round(float(self.score)/self.nr_questions*100,1)
            MessageBox(0, f"Your score is: {_score_}%", "Result", 1)     
            runprogram = False
            if hasattr(self,'bookname'): # to stop from pop-up windows from appearing after the test is done
                delattr(self,'bookname')
            
        if self.score > self.nr_questions+1:
            self.score = self.nr_questions
            _score_ = round(float(self.score)/self.nr_questions*100,1)
        _score_ = round(float(self.score)/self.nr_questions*100,1)
        self.m_Score21.SetValue(f"{_score_} %")      
        self.m_CurrentPage21.SetValue(str(self.index+1))
        
        ## update stats
        if runprogram == True:
            f2.set_stats(self)
            f2.save_stats(self)    
            f2.displaycard(self)
            f2.switch_bitmap(self)
        f2.SetScrollbars_fc(self)
        if runprogram == False:
            self.m_Score21.SetValue("")     
            self.m_CurrentPage21.SetValue("")
            self.m_TotalPages21.SetValue("")
            #reset pictogram
            path_repeat    = Path(self.resourcedir,"repeat.png")
            id_ = self.m_toolSwitch21.GetId()
            self.m_toolBar3.SetToolNormalBitmap(id_, wx.Bitmap( str(path_repeat), wx.BITMAP_TYPE_ANY ))
        self.runprogram = runprogram
        
def switchCard(self):
    #matplotlib.pyplot.close('all') # otherwise too many pyplot figures will be opened -> memory
    f2.clearbitmap(self)
    if self.runprogram == True:
        # change mode Q <-> A
        if self.mode == 'Question': 
            self.mode = 'Answer'
        else:
            self.mode = 'Question'
        self.m_textCtrlMode.SetValue(self.mode)
        # check if there is an answer: if not switch_bitmap sets the mode back to 'question'
        f2.switch_bitmap(self) 
        self.TextCard = False
        AbsoluteIndex = self.cardorder[self.index] 
        self.key = f'{self.mode[0]}{AbsoluteIndex}' #e.g. Q12 is a key
        if self.debugmode:
            print(f"current key = {self.key}")
        # if there are no answer cards, then don't switch card: the self.key makes sure this happens
        if f'A{AbsoluteIndex}' not in self.textdictionary:
            self.m_textCtrlMode.SetValue(self.mode)
            self.key = f'{self.mode[0]}{AbsoluteIndex}'
        # if there are answerd cards, switch
        if self.key in self.textdictionary:
            try:
                f2.CreateTextCard(self)
            except:
                log.ERRORMESSAGE("Error: failed to create TextCard")
        #There is text, determine if there is a picture:
        if self.TextCard == True:
            if self.debugmode:
                print(f"\n\nwe have key {self.key} for picdictionary {self.picdictionary}\n\n")
            if self.key in self.picdictionary:
                try: # to combine text with picture
                    key = self.key
                    imagetext = self.imagetext
                    f2.CombinePicText_fc(self,key,imagetext)
                    f2.ShowPage_fc(self)     
                except:
                    log.ERRORMESSAGE("Error: cannot combine pic with text")
            else: #only display text
                self.image = self.imagetext
                f2.ShowPage_fc(self)
        # there is no text: but is there a picture?
        else: #only display picture
            if self.key in self.picdictionary: # there is a picture
                try:
                    self.jpgdir = str(Path(self.picsdir,self.bookname,self.picdictionary[self.key]))
                    self.image = PIL.Image.open(self.jpgdir) 
                    f2.ShowPage_fc(self)
                except:
                    pass
            # you don't need to check for: "no Text & no picture" because switch_bitmap already takes care of that.
        f2.SetScrollbars_fc(self)

def startprogram(self,event): 
    """main program that does all the preprocessing"""
    self.runprogram   = True
    self.nr_questions = 0
    self.zoom   = 1
    self.chrono = False
    self.index  = 0
    self.score  = 0
       
    self.mode = 'Question'
    self.m_textCtrlMode.SetValue(self.mode)
        
    self.questions   = []
    self.answers     = []
    self.questions2 = []
    
    f2.SetScrollbars_fc(self)
    
    # open file
    try:
        eventpath = event.GetPath()
        print(f"path = {eventpath}")
        self.filename = Path(eventpath).name
        self.bookname = Path(eventpath).stem
        print(f"book = {self.bookname} ")
        if hasattr(self,'TC'):
            delattr(self,'TC')
        self.TC = m6.TimeCount(self.bookname,"flashcard")
    except:
        log.ERRORMESSAGE("Error: Couldn't open path")
    self.resumedata = {self.bookname : {'score': self.score, 'index': self.index, 'nr_questions':self.nr_questions}}
    try:
        if Path(eventpath).exists():
            file = open(eventpath, 'r')
            letterfile = str(file.read())
        
        # positions of Questions and Answers
        q_pos   = [m.start() for m in re.finditer(self.question_command, letterfile)]
        a_pos   = [m.start() for m in re.finditer(self.answer_command, letterfile)]
        self.q_hookpos = list(np.array(q_pos)+len(self.question_command)-2)              #position of argument \command{} q_pos indicates where it starts: "\", added the length of the command -2, because it counts 2 extra '\'
        self.a_hookpos = list(np.array(a_pos)+len(self.answer_command)-2)
        
        self.nr_cards = len(q_pos)
        
    except:
        log.ERRORMESSAGE("Error: could not find questions/answers")


    #open dialog window
    """open My dialog, don't forget to add two parameters to "def __init__( self, parent,MaxValue,Value )" within MyDialog 
    and use these values to set the slider as you wish. Don't forget to add "self.Destroy" when you press the button"""
    
    data = self.nr_cards
    try:
        with open(self.statsdir, 'r') as file:    
            dictionary = json.load(file)
    except:
        dictionary = {}
    if self.bookname in dictionary:
        try:
            with gui.MyDialog2(self,data) as dlg: #use this to set the max range of the slider
                dlg.ShowModal()
                self.nr_questions = dlg.m_slider1.GetValue()   
                self.chrono = dlg.m_radioChrono.GetValue()                    
                self.continueSession = dlg.m_radioYes.GetValue()
                self.multiplier = dlg.m_textCtrl11.GetValue()
                
                # you cannot continue when the questions are randomly chosen
                if self.chrono == False:
                    self.continueSession = False
                
            if self.continueSession == True:
                print("continue session")
                f2.load_stats(self)
            else:
                print("don't continue session")
                f2.remove_stats(self)
            
        except:
            log.ERRORMESSAGE("Error: Couldn't open Dialog window nr 1")
    else:
        try:
            with gui.MyDialog(self,data) as dlg: #'data' sets the max range of the slider
                dlg.ShowModal()
                self.nr_questions = dlg.m_slider1.GetValue()                        
                self.chrono = dlg.m_radioChrono.GetValue()
                self.continueSession = False
                self.multiplier = dlg.m_textCtrl11.GetValue()
        except:
            log.ERRORMESSAGE("Error: Couldn't open Dialog window nr 2")
            
    # if you want to use all cards twice or 1.5 times for the quiz: then exclude invalid selections of this multiplier
    try:
        self.multiplier = float(self.multiplier)
    except:
        log.ERRORMESSAGE("Error: entered multiplier was not a number, continue as if multiplier = 1")
        self.multiplier = 1
    if self.multiplier <= 0:
        self.multiplier = 1
    if self.multiplier != 1:
        self.nr_questions = math.ceil(float(self.multiplier)*self.nr_questions)
        
    # display nr of questions and current index of questions            
    self.m_CurrentPage21.SetValue(f"{self.index+1}")
    self.m_TotalPages21.SetValue(f"{self.nr_questions}")
        
    f2.LoadFlashCards(self, True,letterfile)
    f2.displaycard(self)        
    f2.switch_bitmap(self)
