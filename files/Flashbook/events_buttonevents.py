# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 21:57:02 2020

@author: Anton
"""

def selectionentered(self,event):
    
    if hasattr(self,'bookname') and self.bookname:
        USER_textinput = self.m_userInput.GetValue()       
        PICS_DRAWN = self.Flashcard.nrpics("Question")
        QUESTION_MODE = self.Flashcard.getquestionmode()
        if  USER_textinput or PICS_DRAWN > 0:
            log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: a selection was entered")
            usertext = USER_textinput
            if QUESTION_MODE:
                log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: question mode")
                # change mode to answer
                self.usertext = f.text_to_latex(self,usertext)
                self.Flashcard.switchmode()
                self.m_modeDisplay.SetValue(self.Flashcard.getmode()+":")
                self.Flashcard.setT(self.m_TopicInput.GetValue())
                self.m_userInput.SetValue("")
                self.Refresh()
                # check for [[1,2,3]]
                if PICS_DRAWN > 1:
                    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: multiple pics are drawn")
                    list_ = self.Flashcard.getpiclist("Question")
                    f.CombinePics(self,list_)
                    list_ = list2path(list_)
                    #if type(list_[0]) is list:
                    self.Flashcard.setpiclist('Question',list_)   
                    self.Flashcard.setQ(usertext)                
                    self.Flashcard.setQpic(os.path.basename(list_))
                elif PICS_DRAWN == 1:
                                        
                    list_ = self.Flashcard.getpiclist("Question")
                    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: 1 pic is drawn,\n\t pic drawn is {list_},\n\t mode is {self.Flashcard.getmode()}")
                    if len(list_)>1 and type(list_[0]) is list:#list in list    
                        f.CombinePics(self,list_)
                        list_ = list2path(list_)
                        
                    else:
                        list_ = list2path(list_)
                        
                    self.Flashcard.setQ(usertext)
                    self.Flashcard.setQpic(os.path.basename(list_))
                elif PICS_DRAWN == 0:
                    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: only user text input, 0 pics were drawn")
                    self.Flashcard.setQ(usertext)
                f.ShowInPopup(self,event,"Question")
                
            else:#ANSWER mode
                log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: answer mode")
                self.usertext = f.text_to_latex(self,usertext)
                self.questionmode = True
                # save everything
                findic = self.dictionary
                tempdic = self.tempdictionary
                
                """Add temporary dictionary to permanent dictionary to add itto the border list file
                Don't do this for the PRTscr pages because they are not important
                """
                for key in list(tempdic):      # go over all keys
                    #key = page nr / page prtscr
                    if 'prtscr' not in key:
                        for value in tempdic[key]: # go over all values
                            if key in findic:      # if already exists: just add value
                                findic[key].append(value)
                            else:                  # if not, add key and value, where key = pagenr and value is rectangle coordinates
                                findic.update({key : [value]})
                self.dictionary = findic
                self.tempdictionary = {}
                
                # remove temporary borders
                self.pageimage = self.pageimagecopy
                f.ShowPage_fb(self)
                if self.dictionary:
                    with open(self.PathBorders, 'w') as file:
                        file.write(json.dumps(self.dictionary))
                        
                list_A = self.Flashcard.getpiclist("Answer")
                if list_A == None:
                    list_A = ''
                if len(list_A) > 1:
                    f.CombinePics(self,list_A)
                    if type(list_A[0]) is list:
                        list_A[0] = list_A[0][0]
                    self.Flashcard.setA(usertext)
                    self.Flashcard.setApic(os.path.basename(list_A[0]))
                elif len(list_A) == 1:
                    if type(list_A[0]) is list:        
                        f.CombinePics(self,list_A)
                        self.Flashcard.setA(usertext)
                        self.Flashcard.setApic(os.path.basename(list_A[0]))
                    else:
                        self.Flashcard.setA(usertext)
                        self.Flashcard.setApic(os.path.basename(list_A[0]))            
                else:
                    self.Flashcard.setA(usertext)
                

                f.ShowInPopup(self,event,"Answer")                    
                # save the user inputs in .tex file
                
                self.Flashcard.setT(self.m_TopicInput.GetValue())
                if self.Flashcard.QuestionExists():
                    path = str(Path(self.notesdir, self.bookname +'.tex'))
                    self.Flashcard.saveCard(path)
                #reset all
                self.Flashcard.reset()
                self.m_modeDisplay.SetValue(self.Flashcard.getmode()+":")
                self.m_TopicInput.SetValue('')
                self.m_userInput.SetValue("")
                
                
        elif not QUESTION_MODE:
            log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: answer mode without any input")
            
            # if in question mode the user only typed in some text and want to save that 
            self.Flashcard.setT(self.m_TopicInput.GetValue())
            self.tempdictionary = {}
            # remove temporary borders
            self.pageimage = self.pageimagecopy
            f.ShowPage_fb(self)
            list_A = self.Flashcard.getpiclist("Answer")
            if self.dictionary:
                with open(self.PathBorders, 'w') as file:
                        file.write(json.dumps(self.dictionary)) 
            if len(list_A) > 1:
                f.CombinePics(self,list_A)
                if type(list_A[0]) is list:
                    list_A[0] = list_A[0][0]
                self.Flashcard.setA(usertext)
                self.Flashcard.setApic(str(list_A[0]))
            elif len(list_A) == 1:
                if type(list_A[0]) is list:        
                    f.CombinePics(self,list_A)
                else:
                    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: is not a list")
                self.Flashcard.setA(usertext)
                self.Flashcard.setApic(str(list_A[0]))               
            

            f.ShowInPopup(self,event,"Answer")                    
            # save the user inputs in .tex file
            if self.Flashcard.QuestionExists():
                path = str(Path(self.notesdir, self.bookname +'.tex'))
                self.Flashcard.saveCard(path)
            #reset all
            self.Flashcard.reset()
            self.m_modeDisplay.SetValue(self.Flashcard.getmode()+":")
            self.m_TopicInput.SetValue('')
            self.m_userInput.SetValue("")
            

    
def resetselection(self,event):    
    #  remove all temporary pictures taken
    self.Flashcard.removepics()
    #reset all values:
    self.tempdictionary = {}
    self.Flashcard.reset()
    self.m_modeDisplay.SetValue(self.Flashcard.getmode()+":")
    # update drawn borders
    self.pageimage = self.pageimagecopy
    f.LoadPage(self)
    f.ShowPage_fb(self)