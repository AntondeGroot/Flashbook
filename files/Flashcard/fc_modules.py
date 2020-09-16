# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018

@author: Anton
"""

from termcolor import colored
import wx
import matplotlib
import math
from pathlib import Path
import random
import Flashcard.fc_functions as f2
import _logging.timingmodule as timing
import _logging.log_module as log
import json
import ctypes
import _GUI.gui_flashbook as gui
import program as p
import Flashcard.userdata as userdata

MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW




import Flashcard.cardsorder as crd

def startprogram(self,filepath): 
    """main program that does all the preprocessing"""
    self.runprogram   = True
    self.nr_questions = 0
    self.zoom   = 1
    self.chrono = False
    self.index  = 0
    self.score  = 0
       
    self.mode = 'Question'
    self.m_modeDisplayFC.SetValue(self.mode)
        
    self.questions   = []
    self.answers     = []
    self.questions2  = []
    
    f2.SetScrollbars_fc(self)
    
    # open file
    try:
        
        if type(filepath) == list:
            filepath = filepath[0]
        eventpath = filepath
        self.filename = Path(eventpath).name
        self.bookname = Path(eventpath).stem
        self.booknamepath = eventpath
        
        log.DEBUGLOG(debugmode=self.debugmode,msg=f"FC MODULE: open file:\n\t path = {eventpath}\n\t book = {self.bookname}")
        
        if hasattr(self,'TC'):
            delattr(self,'TC')
        self.TC = timing.TimeCount(self.bookname,"flashcard")
    except:
        log.ERRORMESSAGE("Error: Couldn't open path {filepath}")
    self.resumedata = {self.bookname : {'score': self.score, 'index': self.index, 'nr_questions':self.nr_questions}}    
    
    self.Flashcard.setbook(self.bookname)
    self.Flashcard.load_data()
    
    self.Cardsdeck.loaddata(book = self.bookname)
    
    
    
    cards = self.FlashcardReader.file_to_cards(df) #cards contains the keys #index:  ,.... 'q' and if applicable also 'a'
    self.CardsDeck.set_cards(cards=cards,notesdir=self.notesdir)  # set_cards converts the text to somthing Matplotlib can understand
    
    #open dialog window
    """open My dialog, don't forget to add two parameters to "def __init__( self, parent,MaxValue,Value )" within MyDialog 
    and use these values to set the slider as you wish. Don't forget to add "self.Destroy" when you press the button"""
    
    data = len(self.CardsDeck)
    
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
                
            if self.continueSession:
                log.DEBUGLOG(debugmode=self.debugmode,msg=f"FC MODULE: continue last flashcard session")
                userdata.load_stats(self)
            else:
                log.DEBUGLOG(debugmode=self.debugmode,msg=f"FC MODULE: do not continue last flashcard session")
                userdata.remove_stats(self)
            
        except:
            log.ERRORMESSAGE("Error: Couldn't open Dialog window nr 1")
    else:
        #try:
        with gui.MyDialog(self,data) as dlg: #'data' sets the max range of the slider
            dlg.ShowModal()
            self.nr_questions = dlg.m_slider1.GetValue()                        
            self.chrono = dlg.m_radioChrono.GetValue()
            self.continueSession = False
            self.multiplier = dlg.m_textCtrl11.GetValue()
        #except:
        #    log.ERRORMESSAGE("Error: Couldn't open Dialog window nr 2")
    
    
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
    self.m_CurrentCard.SetValue(f"{self.index+1}")
    self.m_TotalCards.SetValue(f"{self.nr_questions}")
    
    crd.DetermineCardorder(self,True)
    
    f2.displaycard(self)     
    f2.SetScrollbars_fc(self)
    f2.switch_bitmap(self)


    
