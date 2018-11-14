# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018

@author: Anton
"""
from random import randint
from termcolor import colored
import numpy as np
import PIL
import wx
import os
import matplotlib
import math
import PIL
import re
import textwrap
import pylab
import matplotlib.backends.backend_agg as agg
#matplotlib.use('TKAgg')
import fc_functions as f2
import json
import ctypes

import gui_flashbook as gui



def set_richtext2(self):
    self.txt2 = self.m_richText22
    self.txt2.BeginBold()
    self.txt2.EndBold()
    self.txt2.WriteText("                                                                                                                                                                  (left click to close window)\n")

    self.txt2.EndFontSize()
    self.txt2.BeginBold()
    self.txt2.BeginFontSize(16)
    self.txt2.WriteText("  Using FlashCard:\n")
    self.txt2.EndFontSize()
    self.txt2.EndBold()
    imagepath = os.path.join(self.dir7,"mouseicon2.png")
    image = PIL.Image.open(imagepath, mode='r').convert('RGB')
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.txt2.WriteImage(wx.Bitmap(image2))
    imagepath = os.path.join(self.dir7,"arrowkeys.png")
    image = PIL.Image.open(imagepath, mode='r').convert('RGB')
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.txt2.WriteImage(wx.Bitmap(image2))        
    self.txt2.BeginFontSize(12)
    self.txt2.WriteText('\n        1) open with "browse" a file with the bookname you want to study\n' 
                       "        2) a pop-up window will appear with settings, the settings will be implemented if you close the window.\n"
                       "        3) the total number of questions = 'multiplier' x 'nr questions', in case you want test a subject multiple times \n"
                       "        4) your progress is saved so that you can stop any time you want and continue later on.\n" 
                       "        5) be sure to hold your cursor over the image when you use the mouse short cuts")
    self.txt2.EndFontSize()
    self.Layout()   



def buttonCorrect(self):
    # score
    f2.clearbitmap(self)
    self.index += 1
    
    if self.runprogram == True:
        self.score +=1
    self.mode = 'Question'
    self.m_textCtrlMode.SetValue(self.mode)  
    if self.score > self.nr_questions + 1:
        self.score = self.nr_questions
    if self.index > (self.nr_questions-1): 
        self.index = (self.nr_questions-1)
        f2.RemoveStats(self)
        ctypes.windll.user32.MessageBoxW(0, "Your score is: {}%".format(round(float(self.score)/self.nr_questions*100,1)), "Result", 1)     
        self.runprogram = False 
    self.m_Score21.SetValue("{} %".format(round(float(self.score)/self.nr_questions*100,1)))     
    self.m_CurrentPage21.SetValue("{}".format(self.index+1))
    # update stats
    if self.runprogram == True:
        f2.SetStats(self)
        f2.SaveStats(self)   
    # display cards
    if self.runprogram == True: 
        f2.displaycard(self)
        f2.SwitchBitmap(self)
    if self.runprogram == False:
        self.m_Score21.SetValue("")     
        self.m_CurrentPage21.SetValue("")
        self.m_TotalPages21.SetValue("")
        
def buttonWrong(self):
    matplotlib.pyplot.close('all') # otherwise too many pyplot figures will be opened -> memory
    f2.clearbitmap(self)
    self.index += 1
    self.mode = 'Question'
    self.m_textCtrlMode.SetValue(self.mode)  
    if self.index > (self.nr_questions-1):
        self.index = (self.nr_questions-1)
        f2.RemoveStats(self)
        ctypes.windll.user32.MessageBoxW(0, "Your score {}%".format(round(float(self.score)/self.nr_questions*100,1)), "Result", 1)
        self.runprogram = False
    if self.score > self.nr_questions+1:
        self.score = self.nr_questions
    self.m_Score21.SetValue("{} %".format(round(float(self.score)/self.nr_questions*100,1)))      
    self.m_CurrentPage21.SetValue(str(self.index+1))
    
    ## update stats
    if self.runprogram == True:
        f2.SetStats(self)
        f2.SaveStats(self)
    
    if self.runprogram == True: # don't let it extend beyond nr of cards
        f2.displaycard(self)
        f2.SwitchBitmap(self)
    f2.SetScrollbars(self)
    if self.runprogram == False:
        self.m_Score21.SetValue("")     
        self.m_CurrentPage21.SetValue("")
        self.m_TotalPages21.SetValue("")
        
def switchCard(self):
    #matplotlib.pyplot.close('all') # otherwise too many pyplot figures will be opened -> memory
    f2.clearbitmap(self)
    if self.runprogram == True:
        #try:
        # change mode Q-> A
        if self.mode == 'Question': 
            self.mode = 'Answer'
            self.m_textCtrlMode.SetValue(self.mode)            
            
        else:
            self.mode = 'Question'
            self.m_textCtrlMode.SetValue(self.mode)
        
        # check if there is an answer: if not SwitchBitmap sets the mode back to 'question'
        f2.SwitchBitmap(self) 
        self.TextCard = False
        
        self.key = '{}{}'.format(self.mode[0],self.cardorder[self.index])
        if self.debugmode:
            print("current key = {}".format(self.key))
        # if there are no answer cards, then don't switch card: the self.key makes sure this happens
        if 'A{}'.format(self.cardorder[self.index]) not in self.textdictionary:
            self.m_textCtrlMode.SetValue(self.mode)
            self.key = '{}{}'.format(self.mode[0],self.cardorder[self.index])
        # if there are answerd cards, switch
        if self.key in self.textdictionary:#antonanton
            try:
                f2.CreateTextCard(self)
            except:
                print("Error: failed to create TextCard")
        
        # there is text, determine if there is a picture:
        if self.TextCard == True:
            if self.debugmode:
                print("\n\nwe have key {} for picdictionary {}\n\n".format(self.key,self.picdictionary))
            if self.key in self.picdictionary:
                try: # to combine text with picture
                    f2.CombinePicText(self)
                    f2.ShowPage(self)     
                except:
                    print("Error: cannot combine pic with text")
            else: #only display text
                self.image = self.imagetext
                f2.ShowPage(self)
        # there is no text: but is there a picture?
        else: #only display picture
            if self.key in self.picdictionary: # there is a picture
                try:
                    self.jpgdir = self.dir2+"\\"+self.bookname+"\\"+self.picdictionary[self.key]
                    self.image = PIL.Image.open(self.jpgdir) 
                    f2.ShowPage(self)
                except:
                    pass
            # you don't need to check for: "no Text & no picture" because SwitchBitmap already takes care of that.
        f2.SetScrollbars(self)

# main program that does all the preprocessing
def startprogram(self,event): 
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
    
    f2.SetScrollbars(self)
    
    # open file
    try:
        self.path = event.GetPath()
        print("path = {}".format(self.path))
        self.bookname = self.path.replace("{}".format(self.dir1),"")[1:-4]#to remove '\' and '.tex'
        self.filename = self.path.replace("{}".format(self.dir1),"")[1:]#to remove '\' but not '.tex'
        print("book = {} ".format(self.bookname))
    except:
        print(colored("Error: Couldn't open path",'red'))
    self.resumedata = {self.bookname : {'score': self.score, 'index': self.index, 'nr_questions':self.nr_questions}}
    try:
        if os.path.exists(self.path):
            file = open(self.path, 'r')
            texfile = file.read()
        
        self.letterfile = str(texfile)
        # positions of Questions and Answers
        q_pos   = [m.start() for m in re.finditer(self.question_command, self.letterfile)]
        a_pos   = [m.start() for m in re.finditer(self.answer_command, self.letterfile)]
        self.q_hookpos = list(np.array(q_pos)+len(self.question_command)-2)              #position of argument \command{} q_pos indicates where it starts: "\", added the length of the command -2, because it counts 2 extra '\'
        self.a_hookpos = list(np.array(a_pos)+len(self.answer_command)-2)
        
        self.nr_cards = len(q_pos)
        
    except:
        print(colored("Error: finding questions/answers",'red'))
    #try:
    ## dialog display              
    
    #open My dialog, don't forget to add two parameters to "def __init__( self, parent,MaxValue,Value )" within MyDialog 
    #and use these values to set the slider as you wish. Don't forget to add "self.Destroy" when you press the button
    data = self.nr_cards
    #open dialog window
    
    try:
        with open(self.statsdir, 'r') as file:    
            dictionary = json.load(file)
    except:
        dictionary = {}
    if self.bookname in dictionary:
        try:
            with gui.MyDialog2(self,data) as dlg: #use this to set the max range of the slider
                dlg.ShowModal()
                self.nr_questions = dlg.m_slider1.GetValue()   #nr_cards = total unique questions , nr_questions how many you want to ask #anton this might cause problems further down the line
                self.chrono = dlg.m_radioChrono.GetValue()                    
                self.continueSession = dlg.m_radioYes.GetValue()
                self.multiplier = dlg.m_textCtrl11.GetValue()
                
                # you cannot continue when the questions are randomly chosen
                if self.chrono == False:
                    self.continueSession = False
                
            if self.continueSession == True:
                print("continue session")
                f2.LoadStats(self)
            else:
                print("don't continue session")
                f2.RemoveStats(self)
                #f2.SetStats(self)
            
        except:
            print(colored("Error: Couldn't open Dialog window nr 1",'red'))
    else:
        try:
            with gui.MyDialog(self,data) as dlg: #use this to set the max range of the slider , add ",data" in the initialization of the dialog window
                dlg.ShowModal()
                self.nr_questions = dlg.m_slider1.GetValue()                        
                self.chrono = dlg.m_radioChrono.GetValue()
                self.continueSession = False
                self.multiplier = dlg.m_textCtrl11.GetValue()
        except:
            print(colored("Error: Couldn't open Dialog window nr 2",'red'))
        

    
    # if you want to use all cards twice or 1.5 times for the quiz: then exclude invalid selections of this multiplier
    
    try:
        self.multiplier = float(self.multiplier)
    except:
        print(colored("Error: entered multiplier was not a number, continue as if multiplier = 1","red"))
        self.multiplier = 1
    if self.multiplier < 0:
        self.multiplier = 1
    if self.multiplier == 0 :
        self.multiplier = 1
    if self.multiplier != 1:
        self.nr_questions = math.ceil(float(self.multiplier)*self.nr_questions)
        
    # display nr of questions and current index of questions            
    self.m_CurrentPage21.SetValue("{}".format(self.index+1))
    self.m_TotalPages21.SetValue("{}".format(self.nr_questions))
        
    f2.LoadFlashCards(self)
    f2.displaycard(self)        
    f2.SwitchBitmap(self)
