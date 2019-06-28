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
import ast
import json
from pathlib import Path
import PIL
import shutil
import sys
import threading
import wx
import wx.adv as adv
import wx.richtext
import wx.html as html
import wx._html
import platform
_platform = platform.system()
if _platform == 'Windows':
    import ctypes # pop up messages
    import wmi            # for IPaddress: WindowsManagementInstrumentation
    import win32clipboard #
    from win32api import GetSystemMetrics    
    
#------------------------------------------------------------------- modules
import gui_flashbook as gui
import program as p
import fb_initialization as ini 
import fc_initialization as ini2 
import print_initialization as ini3
from settingsfile import settings
from latexoperations import Latexfile
from latexoperations import Commands as cmd
import resources
import fb_modules    as m
import fc_modules    as m2
import print_modules as m3
import sync_modules  as m4
import pdf_modules   as m5
import timingmodule  as m6
import accelerators_module as m7
import historygraph
import log_module    as log
import fb_functions    as f
import fc_functions    as f2
import print_functions as f3
import sync_functions  as f4
import random
import itertools


import math
import pylab
pylab.ioff() # make sure it is inactive, otherwise possible qwindows error    .... https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

sys.setrecursionlimit(5000)
PIL.Image.MAX_IMAGE_PIXELS = 1000000000  
#ctypes:
ICON_EXCLAIM=0x30

ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100
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
#%% settings   

def settings_reset(self):
    settingsfile = Path(self.dirsettings,"settings.txt")
    if settingsfile.exists():
        settingsfile.unlink()
        
    self.settings_create()
    self.settings_get()
    self.m_checkBoxSelections.Check(self.drawborders)
    if self.panel3.IsShown():
        self.m_colorQAline.SetColour(self.QAline_color)
        self.m_colorPDFline.SetColour(self.horiline_color)
        self.m_colorVERTline.SetColour(self.vertline_color)
        
        self.m_lineWpdf.SetValue(str(self.horiline_thickness))
        self.m_lineWqa.SetValue(str(self.QAline_thickness))
        self.m_lineWvert.SetValue(str(self.vertline_thickness))
        
        self.m_lineQA.SetValue(self.QAline_bool)
        self.m_linePDF.SetValue(self.horiline_bool)            
        self.m_lineVERT.SetValue(self.vertline_bool)
        self.m_checkBoxSameColor.SetValue(self.samecolor_bool)
        
        self.m_sliderPDFsize.SetValue(int(200-self.pdfmultiplier*100))
        self.m_slider_col1.SetValue(self.pdfPageColsPos[0])
        self.m_slider_col2.SetValue(self.pdfPageColsPos[1])
        self.m_slider_col3.SetValue(self.pdfPageColsPos[2])
        self.m_checkBox_col1.SetValue(self.pdfPageColsChecks[0])
        self.m_checkBox_col2.SetValue(self.pdfPageColsChecks[1])
        self.m_checkBox_col3.SetValue(self.pdfPageColsChecks[2])



   
#%%
    
    

        

from class_print import printer
from class_flashbook import flashbook
from class_filetransfer import transfer
from class_menusettings import menusettings
from class_helpmenu import helpmenu
from class_menuopen import menuopen
from class_menuflashcard import flashcardmenu
from class_menubooks import booksmenu
"""
###############################################################################
#####              MAINFRAME                                              #####
###############################################################################
"""




class MainFrame(settings,flashbook,printer,transfer,menusettings,helpmenu,menuopen,flashcardmenu,booksmenu):
    
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
        
        self.Latexfile = Latexfile()
        self.Flashcard = Flashcard(self.LaTeXfontsize)
        self.CardsDeck = CardsDeck()#Flashcard(self.LaTeXfontsize))
        
        self.library   = [None]
        
        self.m_menubar1.EnableTop(2, False)#disable Flashcard menu
        self.Maximize(True) # open the app window maximized
        t_books = lambda self,delay : threading.Thread(target = p.checkBooks , args=(self,delay )).start()
        t_books(self, 0.1) 
        
        self.stitchmode_v = True
        self.FilePickEvent = True 
        p.set_bitmapbuttons(self)
        p.set_richtext(self)
        # icon
        iconimage = wx.Icon(str(self.path_icon), type=wx.BITMAP_TYPE_ANY, desiredWidth=40, desiredHeight=40)
        self.SetIcon(iconimage)
        p.SwitchPanel(self,0)
        self.printpreview = True
        
        self.m_checkBoxSelections.Check(self.drawborders)
        self.m_checkBoxCursor.Check(self.cursor)
        self.m_checkBoxDebug.Check(self.debugmode)
        
        m.setcursor(self)
        m7.AcceleratorTableSetup(self,"general","set")    
    #%% menu item events
    " menu item events "
    
        

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
class CardsDeck():
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
        #self.flashcard = flashcard
    
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
        """nr of cards"""
        return len(self.cards)
    
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
        
        if notesdir != None and cards != None:
            self.nrcards = len(cards)
            print(f"NR CARDS = {self.nrcards}\n"*10)
            cardindex = 0
            for _,item in enumerate(cards):
                i = cardindex
                card = cards[i] # cards i : {qi,ti,si}
                card = item
                sizelist = card['size']                
                
                if 't' in card:
                    mode = 't'
                    #for mode in ['t']:
                    key = self.key + f"{mode}{i}"
                    if i == 0:
                        line = self.bookname
                    else:
                        line = card[mode]                    
                    if line.strip() != '':
                        _card_ = {'text': line, 'size' : sizelist}
                        addtodict(self, key, _card_)           
                if 'q' in card:
                    sizecard  = sizelist[:4]
                    mode = 'q'
                    #for mode in ['q']:
                    key = self.key + f"{mode}{i}"
                    
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
        print(f"CARDS\n"*10)
        print(self.cards)
        return self.cards[self.key + str(index)]
        #return self.cards[self.rawkey + str(index)]


    
class Flashcard():
    def __init__(self,fontsize):
        self.a4page_w = 1240
        self.question = None
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
        self.question = None
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
            for pic in dir_:
                if type(pic) == str and Path(pic).exists():
                    Path(pic).unlink()
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
        if vertical_stitch == True:
            #question mode
            if (self.questionmode == True) and (len(self.pic_question) > 0) and (type(self.pic_question[-1]) is list) and (len(self.pic_question[-1])==1):
                self.pic_question[-1] = self.pic_question[-1][0]
                self.pic_question_dir[-1] = self.pic_question_dir[-1][0]
            #answer mode
            if (self.questionmode == False) and (len(self.pic_answer) > 0) and (type(self.pic_answer[-1]) is list) and (len(self.pic_answer[-1])==1):
                self.pic_answer[-1] = self.pic_answer[-1][0]
                self.pic_answer_dir[-1] = self.pic_answer_dir[-1][0]    
        #stitch it horizontally
        else:
            #question mode
            if (self.questionmode == True) and (len(self.pic_question) > 0) and (type(self.pic_question[-1]) is not list):
                self.pic_question[-1] = [self.pic_question[-1]]
                self.pic_question_dir[-1] = [self.pic_question_dir[-1]]
            #answer mode
            if (self.questionmode == False) and (len(self.pic_answer) > 0) and (type(self.pic_answer[-1]) is not list):
                self.pic_answer[-1] = [self.pic_answer[-1]]
                self.pic_answer_dir[-1] = [self.pic_answer_dir[-1]]
    def QuestionExists(self):
        if self.question != '' and self.question != None:
            return True
        else:
            return False
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
            path = self.pic_question_dir[0]
            try:
                w,h = PIL.Image.open(path).size
            except:
                w,h = 'Error','Error'
            self.size_a_pic = (w,h)
        self.sizelist = str([self.size_q_txt, self.size_q_pic, self.size_a_txt, self.size_a_pic, self.size_topic])
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
        self.question = r"\text{" + usertext + r"}"
        imbool, im = f2.CreateTextCard(self,'manual',usertext)
        print(f"text size is {imbool} {usertext}")
        if imbool:
            self.size_q_txt = im.size
    def setQpic(self,partialpath):
        self.questionpic = r"\pic{" + partialpath + r"}"        
    def setA(self,usertext):
        self.answer = r"\text{" + usertext + r"}"
        imbool, im = f2.CreateTextCard(self,'manual',usertext)
        if imbool:
            self.size_a_txt = im.size 
    def setApic(self,partialpath):
        self.answerpic = r"\pic{" + partialpath + r"}"
    #save the final card  
    def saveCard(self,path):
        self.setSizes()
        print(f"path is {self.pic_question_dir}")
        
        with open(path, 'a') as output:
            output.write(r"\quiz{"  + self.question + self.questionpic + "}")
            output.write(r"\ans{"   + self.answer   + self.answerpic   + "}")
            output.write(r"\topic{" + self.topic    + "}")
            output.write(r"\size{"  + self.sizelist + "}" + "\n")
    
    def switchmode(self):
        if self.mode == 'Question':
            self.mode = 'Answer'
            self.questionmode = False
        else:
            self.mode = 'Question'
            self.questionmode = True
    def getquestionmode(self):
        return self.questionmode
    def getQ(self):
        return self.question


    
if __name__ == "__main__":
    # start the application
    app = wx.App(False) 
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
    del app


