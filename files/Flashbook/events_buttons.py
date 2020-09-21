# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 21:57:02 2020

@author: Anton
"""
import os
import json
import Flashbook.page as page
import Flashbook.fb_functions as func
import _logging.log_module as log
import _shared_operations.latexoperations as latex
import _shared_operations.imageoperations as imop
from Flashbook.fb_modules import list2path
import Flashbook.popupwindow as popup
from pathlib import Path
from termcolor import colored

def selectionentered(self,event):
    print("selection entered")
    if hasattr(self,'bookname') and self.bookname:
        USER_textinput = self.m_userInput.GetValue()      
        self.usertext = latex.text_to_latex(self,USER_textinput)
        QUESTION = self.Flashcard.is_question()
        ANSWER = not QUESTION
        
        self.Flashcard.StitchPicsTogether()  
        
        if QUESTION:
            PICS_DRAWN = self.Flashcard.nrpics("Question")
        else:
            PICS_DRAWN = self.Flashcard.nrpics("Answer")
        print(f"nr pics drawn is {PICS_DRAWN}")
        if  QUESTION and (USER_textinput or PICS_DRAWN > 0):
            self.Flashcard.setbook(self.bookname)
            log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: a selection was entered")
            self.usertext = USER_textinput
            
            if self.Flashcard.is_question():                
                print("mode is question/n"*10)
                log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: question mode")
                # change mode to answer
                self.Flashcard.setID() #unique id to Q/A card, only when first data is entered in Q card
                self.Flashcard.switchmode()
                self.m_modeDisplay.SetValue("Answer:")
                self.Flashcard.setT(self.m_TopicInput.GetValue())
                self.m_userInput.SetValue("")
                self.Refresh()
                
                self.Flashcard.setQ(text = self.usertext)                
                popup.ShowInPopup(self,event,"Question")
                
        if ANSWER:    
            log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: answer mode")
            self.questionmode = True
            # save everything
            
            """Add temporary dictionary to permanent dictionary to add itto the border list file
            Don't do this for the PRTscr pages because they are not important
            """
            self.Flashcard.setT(self.m_TopicInput.GetValue()) 
            self.Borders.save_data()                
            # remove temporary borders
            self.pageimage = self.pageimagecopy
            page.ShowPage_fb(self)
            self.Flashcard.setA(text = self.usertext)
            
            popup.ShowInPopup(self,event,"Answer")                    
            
            #save user inputs
            if self.Flashcard.QuestionExists():
                self.Flashcard.saveCard()
            #reset all
            self.Flashcard.reset()
            self.m_modeDisplay.SetValue("Question:")
            self.m_TopicInput.SetValue('')
            self.m_userInput.SetValue("")
            self.Borders.reset()
            page.ShowPage_fb(self)
            

    
def resetselection(self,event):    
    #  remove all temporary pictures taken
    self.Flashcard.removepics()
    #reset all values:
    
    self.Borders.reset()
    self.Flashcard.reset()
    self.m_modeDisplay.SetValue("Question:")
    # update drawn borders
    self.pageimage = self.pageimagecopy
    page.LoadPage(self)
    page.ShowPage_fb(self)