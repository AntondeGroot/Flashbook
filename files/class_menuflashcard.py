# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:04:23 2019

@author: Anton
"""

import gui_flashbook as gui
import threading
import wx
import PIL
import program as p
import fc_functions    as f2
import print_modules as m3
import fc_modules as m2
from pathlib import Path
from latexoperations import Commands as cmd
import imageoperations as imop
import log_module    as log
ICON_EXCLAIM=0x30

import ctypes
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100

class flashcardmenu(gui.MyFrame):
    def __init__(self):
        pass
    def m_menuAddCardOnMenuSelection( self, event ):
        print("b cardorder")
        print(self.cardorder)   
        trueindex = self.cardorder[self.index]
        data = ['Add a card', '' , '' , '' ]
        
        with gui.MyDialog8(self,data) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                #Get user data
                question = dlg.m_textCtrl24.GetValue()
                answer   = dlg.m_textCtrl25.GetValue()
                topic    = dlg.m_textCtrl30.GetValue()
                size     = (0,0)
                #open file
                with open(Path(self.notesdir,self.filename),'r') as file:
                    file_lines = file.readlines()
                    file.close()                    
                print(question,answer,topic)
                #make changes
                if question != '':
                    self.nr_questions += 1
                    print(self.cardorder)
                    
                    self.cardorder += [max(self.cardorder)+1]
                    print("cardorder")
                    print(self.cardorder)
                    print("true index")
                    print(trueindex)
                    self.m_TotalCards.SetValue(f"{self.nr_questions}")
                    file_lines.insert(trueindex, cmd().question()+str(question)+"}"+cmd().answer()+str(answer)+"}" +cmd().topic()+str(topic)+  "}"+r"\size{"+str(size)+"}"+"\n")
                    #save changes
                    with open(str(Path(self.notesdir, self.filename)), 'w') as output: 
                        for line in file_lines:
                            output.write(line)
                    #reload cards
                    self.CardsDeck.reset()
                    self.Latexfile.loadfile(self.booknamepath)
                    cards = self.Latexfile.file_to_rawcards()#cards contains q,a,t,s
                    print(f"cards = {cards}")
                    self.CardsDeck.set_cards(cards=cards,notesdir=self.notesdir)
                    f2.switch_bitmap(self)
                    f2.displaycard(self)
                    self.Refresh()
                    
                    
                
    def m_menuDeleteCardOnMenuSelection( self, event ):
        if self.SwitchCard == True: #there is also an Answer card
            modereset = self.mode
            image,_ = f2.CreateSingularCard(self,'Question')
            BMP_q = imop.PILimage_to_Bitmap(image)
            
            image,_ = f2.CreateSingularCard(self,'Answer')
            BMP_a = imop.PILimage_to_Bitmap(image)
            
            data = [BMP_q,BMP_a]
            self.mode = modereset
            
            with gui.MyDialog6(self,data) as dlg:
                if dlg.ShowModal() == wx.ID_OK:   
                    f2.DeleteCurrentCard(self)
                    print(f"index = {self.cardorder[self.index]}")
                    print(f"cardorder = {self.cardorder}")
                    #it might occur multiple times
                    self.cardorder = [x for x in self.cardorder if x != self.cardorder[self.index]]
                    #self.nr_cards = len(self.cardorder)
                    self.nr_questions -= 1
                    self.m_TotalCards.SetValue(str(self.nr_questions))
                    f2.displaycard(self)
                    self.Refresh()
                    print("success!!")
        elif self.SwitchCard == False: #there is only a Question card
            
            image,_ = f2.CreateSingularCard(self,'Question')
            BMP_q = imop.PILimage_to_Bitmap(image)
            
            with gui.MyDialog7(self,BMP_q) as dlg:
                if dlg.ShowModal() == wx.ID_OK:  
                    f2.DeleteCurrentCard(self)
                    self.cardorder = [x for x in self.cardorder if x != self.cardorder[self.index]]
                    #self.nr_cards = len(self.cardorder)
                    self.nr_questions -= 1
                    self.m_TotalCards.SetValue(f"{self.nr_questions}")
                    f2.displaycard(self)
                    self.Refresh()
                
    def m_menuEditCardOnMenuSelection( self, event ):
        trueindex = self.cardorder[self.index]
        rawcard = self.CardsDeck.get_rawcard_i(trueindex)
        data = ['Edit the card', rawcard['q'] , rawcard['a'] , rawcard['t'] ]
        
        with gui.MyDialog8(self,data) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                #Get user data
                question = dlg.m_textCtrl24.GetValue()
                answer   = dlg.m_textCtrl25.GetValue()
                topic    = dlg.m_textCtrl30.GetValue()
                #open file
                with open(Path(self.notesdir,self.filename),'r') as file:
                    file_lines = file.readlines()
                    file.close()
                    
                print(question,answer,topic)
                
                #make changes
                if question == '':
                    """ If you remove the question then the entire card will be deleted"""
                    file_lines.pop(trueindex)
                    f2.DeleteCurrentCard(self)
                    self.cardorder = [x for x in self.cardorder if x != self.cardorder[self.index]]
                    #self.nr_cards = len(self.cardorder)
                    self.nr_questions -= 1
                    self.m_TotalCards.SetValue(f"{self.nr_questions}")
                    f2.displaycard(self)
                    self.Refresh()
                else:
                    file_lines[trueindex] = r"\quiz{"+str(question)+"}"+r"\ans{"+str(answer)+"}" +r"\topic{"+str(topic)+  "}"+"\n"
                    #save changes
                    with open(str(Path(self.notesdir, self.filename)), 'w') as output: 
                        for line in file_lines:
                            output.write(line)
                    #reload cards
                    self.CardsDeck.reset()
                    self.Latexfile.loadfile(self.booknamepath)
                    cards = self.Latexfile.file_to_rawcards()#cards contains q,a,t,s
                    self.CardsDeck.set_cards(cards=cards,notesdir=self.notesdir)
                    f2.switch_bitmap(self)
                    f2.displaycard(self)
                    self.Refresh()                
                print("success!!")
                
    def m_menuPreviousCardOnMenuSelection( self, event ):
        m2.buttonPreviousCard(self)
        print("go to previous card")
