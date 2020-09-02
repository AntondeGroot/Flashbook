# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 18:43:04 2017
@author: Anton
"""

try:
    del app
except:
    pass
#------------------------------------------------------------------- general
import os
from pathlib import Path
import PIL
import shutil
import sys

flashbookfolder = os.path.join(os.getcwd(),'Flashbook')
flashbookfolder = os.path.join(os.getcwd(),'Flashcard')

import sys, os

def addmodule(foldername):
    sys.path.append(os.path.abspath(os.path.join('..', foldername)))

addmodule('Flashbook')
addmodule('_settings')
addmodule('_GUI')
addmodule('_logging')
addmodule('_shared_operations')
addmodule('Print')
addmodule('Synchronize')

# Now do your import
from Flashbook.fb_modules import *
import Flashbook.page as page
from Flashbook.fb_functions import *
import _GUI.active_panel as panel
import Books.library as Books

import Flashbook.events_mouse as evt_m
from _shared_operations import *
from _logging import *

#%%
sys.path.insert(1,flashbookfolder)

import threading
import wx
import wx.adv as adv
import wx.richtext
import wx.html as html
import wx._html
import platform
_platform = platform.system() 
import Books.events_buttons as Bookbuttons
#------------------------------------------------------------------- modules
import _GUI.gui_flashbook as gui
import program as p
from _settings.settingsfile import settings
from _shared_operations.latexoperations import Latexfile
import _resources.resources as resources
import Flashbook.fb_modules    as m
import _GUI.accelerators_module as acc
import fc_functions    as f2

import math
import pylab
pylab.ioff() # make sure it is inactive, otherwise possible qwindows error    .... https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window

from Print.class_print import printer
from Flashbook.class_flashbook import flashbook
from Flashcard.class_flashcard import flashcard
from Synchronize.class_filetransfer import filetransfer
from _menu.class_menusettings import menusettings
from _menu.class_helpmenu import helpmenu
from _menu.class_menuopen import menuopen
from _menu.class_menuflashcard import flashcardmenu
from _menu.class_menubooks import booksmenu

import _logging.log_module as log

sys.setrecursionlimit(5000)
PIL.Image.MAX_IMAGE_PIXELS = 1000000000  

"""when using Pyinstaller to create the .exe file: it will standardly give an error that it is missing the module 'qwindows.dll'
since the .exe created by --onefile takes ages to start, i won't be using that option and then module can be found in the folder below
it is resolved by simply copying the qwindows.dll module next to the .exe file"""

try:
    cwd = Path.cwd()
    dllfile= Path(cwd,"\PyQt5\Qt\plugins\platforms\qwindows.dll")
    
    if dllfile.exists():
        shutil.copy2(dllfile,cwd+r'\\') 
    else:
        print("qwindows.dll module missing")    
except:
    print("no qwindows.dll module found  (#2)")
            
def SaveTime(self):
    if hasattr(self,'TC') and hasattr(self,'bookname') and self.bookname != '':
        self.TC.update()       

#% path to resources: 
def setup_sources(self):
    if _platform == 'Windows':
        bdir = Path(os.getenv("LOCALAPPDATA"),"Flashbook")
    elif _platform == 'Linux':
        pass
    rdir = Path(bdir,"resources")
    print(f"rdir = {rdir}\n"*10)
    self.appdir         = bdir
    self.path_add     = Path(rdir,"add.png")
    self.path_min     = Path(rdir,"min.png")
    self.path_icon    = Path(rdir,"flashbook_icon.png")
    self.path_fb      = Path(rdir,"flashbook.png")
    self.path_fc      = Path(rdir,"flashcard.png")
    self.path_wifi    = Path(rdir,"wifi.png")
    self.path_pr      = Path(rdir,"print.png")
    self.path_arrow   = os.path.join(rdir,"arrow.png")
    self.path_arrow2  = os.path.join(rdir,"arrow2.png")
    self.path_convert = Path(rdir,"convert.png")
    self.path_folder  = Path(rdir,"folder.png")
    self.path_repeat  = Path(rdir,"repeat.png")
    self.path_repeat_na = Path(rdir,"repeat_na.png") 

"""
###############################################################################
#####              MAINFRAME                                              #####
###############################################################################
"""

class MainFrame(settings,flashbook,flashcard,printer,filetransfer,menusettings,helpmenu,menuopen,flashcardmenu,booksmenu,Bookbuttons.libbuttons):
    
    """ INITIALIZE """
    def __init__(self,parent): 
        setup_sources(self)
        #initialize parent class
        icons = [wx.Bitmap(str(self.path_folder)) , wx.Bitmap(str(self.path_convert)) ]
        gui.MyFrame.__init__(self,parent,icons) #added extra argument, so that WXpython.py can easily add the Dialog Windows (which require an extra argument), which is now used to add extra icons to the menubar             
        settings.__init__(self)
        
        resources.resourceimages(self.resourcedir,self.notesdir) 
        
        PanelWidth, PanelHeight = self.m_panel32.GetSize()
        PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
        self.m_panel32.SetSize(PanelWidth,PanelHeight)
        #settings class
        self.settings_create()
        self.settings_get()
        self.settings_set()
        
        log.INITIALIZE(debugmode=self.debugmode)
        self.Latexfile = Latexfile()
        self.Flashcard = Flashcard(self.LaTeXfontsize)
        self.CardsDeck = CardsDeck()
        self.FlashbookLibrary = Books.Library(self)
        
        self.library   = [None]
        
        self.m_menubar1.EnableTop(2, False) # disable Flashcard menu
        self.Maximize(True) # open the app window maximized
        t_books = lambda self,delay : threading.Thread(target = p.checkBooks , args=(self, delay)).start()
        t_books(self, 0.1) 
        
        self.stitchmode_v = True
        self.FilePickEvent = True 
        p.set_bitmapbuttons(self)
        p.set_richtext(self)
        # icon
        iconimage = wx.Icon(str(self.path_icon), type=wx.BITMAP_TYPE_ANY, desiredWidth=40, desiredHeight=40)
        self.SetIcon(iconimage)
        panel.SwitchPanel(self,0)
        self.printpreview = True
        
        self.m_checkBoxSelections.Check(self.drawborders)
        self.m_checkBoxDebug.Check(self.debugmode)
        
        evt_m.setcursor(self)
        acc.AcceleratorTableSetup(self,"general","set")    
    def m_buttonTopicOnButtonClick( self, event ):
        print(f"testing")
        self.FlashbookLibrary.addtopic(event)
    def m_buttonBookOnButtonClick(self,event):
        self.FlashbookLibrary.addbook(event)
    def m_buttonReTopicOnButtonClick(self,event):
        self.FlashbookLibrary.renametopic(event)
    
    def m_buttonDelTopicOnButtonClick(self,event):
        self.FlashbookLibrary.deletetopic(event)
    def m_listTopicsOnListItemSelected(self,event):
        
        pass
    def m_listTopicsOnListItemDeselected(self,event):    
        pass
    def m_buttonStartBookOnButtonClick(self,event):
        index = self.m_listTopics.GetFocusedItem()  
        print(f"index = {index}")
        if index >= 0: #error code is -1
            
            
            
            oldtopic = self.m_listTopics.GetItemText(index)
            self.booktopic = oldtopic
            print(f"topic {oldtopic}")
            self.booknames = self.FlashbookLibrary.getbooknames(oldtopic)
            page.savetopic(self)
    #%% timecount
    def m_scrolledWindow1OnMouseEvents( self, event ):
        SaveTime(self)
        event.Skip()
    def m_scrolledWindow1OnKeyDown( self, event ):
        SaveTime(self)
        event.Skip()        
    def m_bitmapScrollOnMouseEvents( self, event ):
        SaveTime(self)
        event.Skip()
    def m_bitmapScrollOnKeyDown( self, event ):
        SaveTime(self)
        event.Skip()
    def m_bitmapScrollFCOnKeyDown( self, event ):
        SaveTime(self)
        event.Skip()
    def m_bitmapScrollFCOnMouseEvents( self, event ):
        SaveTime(self)
        event.Skip()
    def m_scrolledWindow11OnMouseEvents( self, event ):
        SaveTime(self)
        event.Skip()
    def m_scrolledWindow11OnKeyDown( self, event ):
        SaveTime(self)
        event.Skip()
    

"""
###############################################################################
#####              FLASHCARD                                              #####
###############################################################################
"""
class CardsDeck(settings):
    def __init__(self):#,flashcard):
        
        
        """ - cards are dicts because then you can easily delete a card from the deck
            - you can then use cardorder to switch cards and just omit a cardnumber from that list"""
        self.cards = {}
        self.cards_raw = {}
        self.nrcards = 0
        self.cardorder = []
        self.index = 0
        self.mode = 'Question'
        self.textdictionary = {}
        self.picdictionary  = {}
        self.rawkey = "card"
        self.key = "card_"
        self.bookname = ''
        
        settings.__init__(self)
        self.settings_get()
        
        #self.flashcard = flashcard
        #self.zoom = 1.0
    
    def reset(self):
        self.cards = {}
        self.cards_raw = {}
        self.nrcards = 0
        self.cardorder = []
        self.index = 0
        self.mode = 'Question'
        self.textdictionary = {}
        self.picdictionary  = {}
        self.bookname = ''
    
    def set_bookname(self,name):
        self.bookname = name
        
    def get_rawkey(self,index):
        return self.rawkey + index
    def get_key(self,mode,index):
        return self.key+str(mode[0]).lower()+str(index)
    
    def __len__(self):
        """nr of cards, without counting topics as separate cards"""
        return len([x for x in self.cards.keys() if 't' not in x])
        #return len(self.cards)
    
    def len_uniquecards(self):
        """You need to separate topic cards from Q/A cards"""
        return len(self.cards)
    def len_totalcards(self):
        """You need to separate topic cards from Q/A cards"""
        return len(self.cards.keys())
        
    def getcards(self):
        return self.cards #cards are ti/qi:{text: ... size: ...}
        
    def set_cards(self, cards=None, notesdir=None):
        #assert type(cards) == dict #cards contains q,a,t,s
        #assert type(self.cards_raw) == dict
        def addtodict(self, _key_, card):
            if _key_ in self.cards.keys():
                self.cards[_key_].update(card)
            else:
                self.cards[_key_] = card
        
        if notesdir and cards:
            """The cardindex does not change between a Topic Card and a Question Card
            They are considered to be the same card. Therefore it does not take the index of the enumerate()
            in 'Cards' the question and topic card are still seperated because they will be printed seperately"""
            self.nrcards = len(cards)
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS CARDSDECK: nr cards = {self.nrcards}')
            cardindex = 0
            for _, card in enumerate(cards):                
                # card i : {qi,si} or {ti,si}
                sizelist = card['size']                
                
                if 't' in card:
                    mode = 't'
                    key = self.key + f"{mode}{cardindex}"
                    if cardindex == 0:
                        line = self.bookname
                    else:
                        line = card[mode]                    
                    if line.strip() != '': #if the line is not empty, spaces are considered to be empty 
                        _card_ = {'text': line, 'size' : sizelist}
                        addtodict(self, key, _card_)           
                if 'q' in card:
                    sizecard  = sizelist[:4]
                    mode = 'q'
                    key = self.key + f"{mode}{cardindex}"
                    
                    line = card[mode]
                    _card_ = {'text': line, 'size' : sizecard}
                    addtodict(self, key, _card_)
                    cardindex += 1               
    def get_nrcards(self):
        return self.nrcards
    def get_cardorder(self):
        return self.cardorder
    def set_cardorder(self,cardorder):
        self.cardorder = cardorder
    def get_card_i(self,i):
        return self.cards[i]
    def get_rawcard_i(self,index):
        return self.cards[self.key + str(index)]


    
class Flashcard():
    def __init__(self,fontsize):
        self.a4page_w = 1240
        self.question = ''
        self.questionpic = ''
        self.answer    = ''
        self.answerpic = ''
        self.mode      = 'Question'
        self.questionmode = True
        self.topic    = ''
        self.pic_question     = []
        self.pic_answer       = []
        self.pic_question_dir = []
        self.pic_answer_dir   = []
        self.usertext         = ''
        self.size_q_txt = (0,0)
        self.size_q_pic = (0,0)
        self.size_a_txt = (0,0)
        self.size_a_pic = (0,0)
        self.size_topic = (0,0)
        self.sizelist = '[(0,0),(0,0),(0,0),(0,0),(0,0)]'
        self.LaTeXfontsize = fontsize
        
    def reset(self):
        self.question = ''
        self.questionpic = ''
        self.answer   = ''
        self.answerpic = ''
        self.mode     = 'Question'
        self.questionmode = True
        self.topic    = ''
        self.pic_question     = []
        self.pic_answer       = []
        self.pic_question_dir = []
        self.pic_answer_dir   = []
        self.usertext         = ''
        self.size_q_txt = (0,0)
        self.size_q_pic = (0,0)
        self.size_a_txt = (0,0)
        self.size_a_pic = (0,0)
        self.size_topic = (0,0)
        self.sizelist = '[(0,0),(0,0),(0,0),(0,0),(0,0)]'
    
    def setpiclist(self,mode,text):
        if mode.lower() == 'question':
            self.pic_question_dir = text
        else:
            self.pic_question_dir = text
            
    def getpicdir(self,mode):
        if mode.lower() == 'question':
            return self.pic_question_dir
        else:
            return self.pic_question_dir
            
    def removepics(self):
        def unlinkpics(dir_):    
            print(f"dir = {dir_}")
            if len(dir_) > 1:
                if isinstance(dir_,str):
                    try:
                        if Path(dir_).exists():
                            Path(dir_).unlink()
                    except:
                        pass
                elif isinstance(dir_,list):
                    for pic in dir_:
                        try:
                            if type(pic) == str and Path(pic).exists():
                                Path(pic).unlink()
                        except:
                            pass
            elif len(dir_) == 1:
                try:
                    #just one image
                    pic = dir_[0]
                    if type(pic) == str and Path(pic).exists():
                            Path(pic).unlink()
                except:
                    print("could not remove single image")
                    pass
                
        if len(self.pic_question_dir) > 0:
            dir_ = self.pic_question_dir
            unlinkpics(dir_)
        if len(self.pic_answer_dir) > 0:
            dir_ = self.pic_answer_dir    
            unlinkpics(dir_)
    
    def addpic(self,mode,orientation,name,path):        
        if mode == 'Question':
            if orientation == 'vertical':
                self.pic_question.append(name)  
                self.pic_question_dir.append(path)  
            elif orientation == 'horizontal':
                try:
                    self.pic_question[-1].append(name)  
                    self.pic_question_dir[-1].append(path)  
                except:
                    self.pic_question.append([name])  
                    self.pic_question_dir.append([path])  
            else:
                raise ValueError('Flashcard has been given a wrong orientation')
        elif mode == 'Answer':  
            if orientation == 'vertical':
                self.pic_answer.append(name)  
                self.pic_answer_dir.append(path)  
            elif orientation == 'horizontal':
                try:
                    self.pic_answer[-1].append(name)  
                    self.pic_answer_dir[-1].append(path)  
                except:
                    self.pic_answer.append([name])  
                    self.pic_answer_dir.append([path])  
            else:
                raise ValueError('Flashcard has been given a wrong orientation')
        else: 
            raise ValueError('Flashcard has been given a wrong mode')
            
    def StitchCards(self,vertical_stitch):
        if vertical_stitch:
            #question mode
            if self.questionmode and (len(self.pic_question) > 0) and (type(self.pic_question[-1]) is list) and (len(self.pic_question[-1])==1):
                self.pic_question[-1] = self.pic_question[-1][0]
                self.pic_question_dir[-1] = self.pic_question_dir[-1][0]
            #answer mode
            if (not self.questionmode) and (len(self.pic_answer) > 0) and (type(self.pic_answer[-1]) is list) and (len(self.pic_answer[-1])==1):
                self.pic_answer[-1] = self.pic_answer[-1][0]
                self.pic_answer_dir[-1] = self.pic_answer_dir[-1][0]    
        #stitch it horizontally
        else:
            #question mode
            if self.questionmode and (len(self.pic_question) > 0) and (type(self.pic_question[-1]) is not list):
                self.pic_question[-1] = [self.pic_question[-1]]
                self.pic_question_dir[-1] = [self.pic_question_dir[-1]]
            #answer mode
            if (not self.questionmode) and (len(self.pic_answer) > 0) and (type(self.pic_answer[-1]) is not list):
                self.pic_answer[-1] = [self.pic_answer[-1]]
                self.pic_answer_dir[-1] = [self.pic_answer_dir[-1]]
    def QuestionExists(self):
        if self.question.strip() != '' or self.questionpic.strip() != '':
            return True
        
    def getpiclist(self,mode):
        if mode.lower() == 'question':
            return self.pic_question_dir
        elif mode.lower() == 'answer':
            return self.pic_answer_dir
    def nrpics(self,mode):
        if mode.lower() == 'question':
            return len(self.pic_question)
        elif mode.lower() == 'answer':
            return len(self.pic_answer)
    def setSizes(self):
        if len(self.pic_question_dir) == 1:
            path = self.pic_question_dir[0]
            try:
                w,h = PIL.Image.open(path).size
            except:
                w,h = 'Error','Error'
            self.size_q_pic = (w,h)
        if len(self.pic_answer_dir) == 1:
            path = self.pic_answer_dir[0]
            try:
                w,h = PIL.Image.open(path).size
            except:
                w,h = 'Error','Error'
            self.size_a_pic = (w,h)
        self.sizelist = str([self.size_q_txt, self.size_q_pic, 
                             self.size_a_txt, self.size_a_pic, 
                             self.size_topic])
    #store user data and save sizes of images/text
    def setT(self,text):
        self.topic = text
        width_card = self.a4page_w
        height_card = int(math.ceil(len(text)/40))*0.75*100
        print(f"! topic = {text}, size = {width_card},{height_card}")
        if height_card != 0:
            print("topic size",width_card,height_card)
            self.size_topic = (width_card,height_card)                
    def setQ(self,usertext):
        if usertext.strip() != '':
            self.question = r"\text{" + usertext + r"}"
            imbool, im = f2.CreateTextCard(self,'manual',usertext)
            print(f"text size is {imbool} {usertext}")
            if imbool:
                self.size_q_txt = im.size
    def setQpic(self,partialpath):
        self.questionpic = r"\pic{" + partialpath + r"}"        
    def setA(self,usertext):
        if usertext.strip() != '':
            self.answer = r"\text{" + usertext + r"}"
            image_exists, image = f2.CreateTextCard(self,'manual',usertext)
            if image_exists:
                self.size_a_txt = image.size 
                
    def getmode(self):
        return str(self.mode)
    def setApic(self,partialpath):
        self.answerpic = r"\pic{" + partialpath + r"}"
    #save the final card  
    def saveCard(self,path):
        self.setSizes()        
        with open(path, 'a') as output:
            output.write(r"\quiz{"  + self.question + self.questionpic + "}")
            output.write(r"\ans{"   + self.answer   + self.answerpic   + "}")
            output.write(r"\topic{" + self.topic    + "}")
            output.write(r"\size{"  + self.sizelist + "}")
            output.write("\n")
    def switchmode(self):
        if self.mode == 'Question':
            self.mode = 'Answer'
            self.questionmode = False
        else:
            self.mode = 'Question'
            self.questionmode = True
    def getquestionmode(self):
        return self.questionmode


    
if __name__ == "__main__":
    # start the application
    app = wx.App(False) 
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
    del app


