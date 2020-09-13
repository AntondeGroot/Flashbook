# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 21:57:02 2020

@author: Anton
"""
import os
import json
import Flashbook.page as page
import _logging.log_module as log
import _shared_operations.latexoperations as latex
import _shared_operations.imageoperations as imop
from Flashbook.fb_modules import list2path
import Flashbook.popupwindow as popup
from pathlib import Path

def selectionentered(self,event):
    print(f"{hasattr(self,'bookname')}\n"*10)
    if hasattr(self,'bookname') and self.bookname:
        USER_textinput = self.m_userInput.GetValue()      
        self.usertext = latex.text_to_latex(self,USER_textinput)
        QUESTION = self.Flashcard.is_question()
        ANSWER = not QUESTION
        
        if QUESTION:
            PICS_DRAWN = self.Flashcard.nrpics("Question")
        else:
            PICS_DRAWN = self.Flashcard.nrpics("Answer")
        
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
                # check for [[1,2,3]]
                if PICS_DRAWN > 1:
                    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: multiple pics are drawn")
                    list_ = self.Flashcard.getpiclist("Question")
                    imop.CombinePics(self,list_)
                    list_ = list2path(list_)
                    self.Flashcard.setQ(text = self.usertext,pic = os.path.basename(list_))                
                elif PICS_DRAWN == 1:                                        
                    list_ = self.Flashcard.getpiclist("Question")
                    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: 1 pic is drawn,\n\t pic drawn is {list_},\n\t mode is question: {self.Flashcard.is_question()}")
                    if len(list_)>1 and type(list_[0]) is list:#list in list  
                        print(f"anton watch it\n"*20)
                        imop.CombinePics(self,list_)
                        list_ = list2path(list_)
                    else:
                        list_ = list2path(list_)
                    print(os.path.basename(list_))                    
                    self.Flashcard.setQ(text = self.usertext, pic = os.path.basename(list_))                    
                elif PICS_DRAWN == 0:
                    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: only user text input, 0 pics were drawn")
                    self.Flashcard.setQ(self.usertext)
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
  
            list_A = self.Flashcard.getpiclist("Answer")
            if not list_A:
                list_A = ''
            if len(list_A) > 1:
                """"multiple pictures were taken"""
                imop.CombinePics(self,list_A)
                if type(list_A[0]) is list:
                    list_A[0] = list_A[0][0]
                self.Flashcard.setA(text=self.usertext,pic = os.path.basename(list_A[0]))
            elif len(list_A) == 1:
                """"only 1 picture was taken"""
                if type(list_A[0]) is list:        
                    imop.CombinePics(self,list_A)
                self.Flashcard.setA(text = self.usertext, pic = os.path.basename(list_A[0]))
            else:
                """"no pictures were taken"""
                self.Flashcard.setA(text=self.usertext)             
            

        
        if ANSWER: #if answer card is completed
            popup.ShowInPopup(self,event,"Answer")                    
            # save the user inputs in file                
            self.Flashcard.setT(self.m_TopicInput.GetValue())           
            #save user inputs
            if self.Flashcard.QuestionExists():
                self.Flashcard.saveCard()
            #reset all
            self.Flashcard.reset()
            self.m_modeDisplay.SetValue("Question:")
            self.m_TopicInput.SetValue('')
            self.m_userInput.SetValue("")
        

    
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