# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 23:38:49 2020

@author: Anton
"""
import Flashcard.fc_functions as f2
import Flashcard.userdata as userdata
import _logging.log_module as log
import wx
from pathlib import Path

def buttonPreviousCard(self):
    f2.clearbitmap(self)
    if hasattr(self,'nr_questions') and self.nr_questions != 0 and hasattr(self,'bookname') and self.bookname != '':
        runprogram = self.runprogram
        if self.index > 0:
            self.index -= 1
        if self.score > 0:
            self.score -= 1
        self.mode = 'Question'
        self.m_modeDisplayFC.SetValue(self.mode)  
        _score_ = round(float(self.score)/self.nr_questions*100,1)
        self.m_Score.SetValue(f"{_score_} %")      
        self.m_CurrentCard.SetValue(str(self.index+1))
        
        ## update stats
        if runprogram:
            userdata.set_stats(self)
            userdata.save_stats(self)    
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

        
def switchCard(self):
    #matplotlib.pyplot.close('all') # otherwise too many pyplot figures will be opened -> memory
    
    try:
        if self.runprogram:
            # change mode Q <-> A
            if self.mode == 'Question': 
                self.mode = 'Answer'
            else:
                self.mode = 'Question'
            self.m_modeDisplayFC.SetValue(self.mode)
            # check if there is an answer: if not switch_bitmap sets the mode back to 'question'
            f2.switch_bitmap(self)       
    except:
        log.ERRORMESSAGE("Error: Couldn't switch card")