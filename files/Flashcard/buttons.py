# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 23:38:01 2020

@author: Anton
"""
import _GUI.active_panel as panel
import Flashcard.userdata as data
import Flashcard.card as card
import _logging.log_module as log
import _GUI.gui_flashbook as gui
import wx
import matplotlib
import Flashcard.fc_functions as f2
from pathlib import Path

def buttonCorrect(self):
    self.NEWCARD = True
    f2.clearbitmap(self)
    if hasattr(self,'nr_questions') and self.nr_questions != 0 and hasattr(self,'bookname') and self.bookname != '':
        #import
        runprogram = self.runprogram
        self.index += 1    
        if runprogram:
            self.score +=1
        self.mode = 'Question'
        self.m_modeDisplayFC.SetValue(self.mode)
        
        if self.score > self.nr_questions + 1:
            self.score = self.nr_questions
        if self.index > (self.nr_questions-1): 
            self.index = (self.nr_questions-1)
            data.remove_stats(self)
            _score_ = round(float(self.score)/self.nr_questions*100,1)
            #MessageBox(0, f"Your score is: {_score_}%", "Result", 1 )    
            message = f"Your score is: {_score_}%"
            with gui.MyDialogScore(self,message) as dlg:
                if dlg.ShowModal() == wx.ID_OK:  
                    panel.SwitchPanel(self,0)
                    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FC MODULE: flashcard program finished")
                    
            self.m_menubar1.EnableTop(1,False)
            runprogram = False
            if hasattr(self,'bookname'): # to stop from pop-up windows from appearing after the test is done
                delattr(self,'bookname')
            
        _score_ = round(float(self.score)/self.nr_questions*100,1)
        self.m_Score.SetValue(f"{_score_} %")     
        self.m_CurrentCard.SetValue(f"{self.index+1}")
        
        # update stats
        if runprogram:
            data.set_stats(self)
            data.save_stats(self)   
            # display cards
            f2.displaycard(self)
            f2.switch_bitmap(self)
        else:
            self.m_Score.SetValue("")     
            self.m_CurrentCard.SetValue("")
            self.m_TotalCards.SetValue("")
            #reset pictogram
            path_repeat    = Path(self.resourcedir,"repeat.png")
            id_ = self.m_toolSwitchFC.GetId()
            self.m_toolBar3.SetToolNormalBitmap(id_, wx.Bitmap( str(path_repeat), wx.BITMAP_TYPE_ANY ))
        #update self.vars accordingly
        self.runprogram = runprogram
    
def buttonWrong(self):
    self.NEWCARD = True
    matplotlib.pyplot.close('all') # otherwise too many pyplot figures will be opened -> memory
    f2.clearbitmap(self)
    if hasattr(self,'nr_questions') and self.nr_questions != 0 and hasattr(self,'bookname') and self.bookname != '':
        runprogram = self.runprogram
        self.index += 1
        self.mode = 'Question'
        self.m_modeDisplayFC.SetValue(self.mode)  
        if self.index > (self.nr_questions-1):
            self.index = (self.nr_questions-1)
            f2.remove_stats(self)
            _score_ = round(float(self.score)/self.nr_questions*100,1)
            #MessageBox(0, f"Your score is: {_score_}%", "Result", 1) 
            message = f"Your score is: {_score_}%"
            with gui.MyDialogScore(self,message) as dlg:
                if dlg.ShowModal() == wx.ID_OK: 
                    panel.SwitchPanel(self,0)
                    log.DEBUGLOG(debugmode=self.debugmode,msg=f"FC MODULE: flashcard program finished")
            self.m_menubar1.EnableTop(1,False)
            runprogram = False
            if hasattr(self,'bookname'): # to stop from pop-up windows from appearing after the test is done
                delattr(self,'bookname')
            
        if self.score > self.nr_questions+1:
            self.score = self.nr_questions
            _score_ = round(float(self.score)/self.nr_questions*100,1)
        _score_ = round(float(self.score)/self.nr_questions*100,1)
        self.m_Score.SetValue(f"{_score_} %")      
        self.m_CurrentCard.SetValue(str(self.index+1))
        
        ## update stats
        if runprogram:
            data.set_stats(self)
            data.save_stats(self)    
            f2.displaycard(self)
            f2.switch_bitmap(self)
        f2.SetScrollbars_fc(self)
        if not runprogram:
            self.m_Score.SetValue("")     
            self.m_CurrentCard.SetValue("")
            self.m_TotalCards.SetValue("")
            #reset pictogram
            path_repeat    = Path(self.resourcedir,"repeat.png")
            id_ = self.m_toolSwitchFC.GetId()
            self.m_toolBar3.SetToolNormalBitmap(id_, wx.Bitmap( str(path_repeat), wx.BITMAP_TYPE_ANY ))
        self.runprogram = runprogram