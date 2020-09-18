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
import numpy as np
from pathlib import Path
import PIL
import shutil
import sys
import random
import ast
from _GUI.folderpaths import paths
flashbookfolder = os.path.join(os.getcwd(),'Flashbook')
flashbookfolder = os.path.join(os.getcwd(),'Flashcard')
"""
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
"""
# Now do your import
from Flashbook.fb_modules import *
import Flashbook.page as page
from Flashbook.fb_functions import *
import _pdf.pdf_modules as pdf
import _GUI.active_panel as panel
import Books.library as Books

import Flashbook.events_mouse as evt_m
from _shared_operations import imageoperations as imop
from _logging import *
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
#%%
#sys.path.insert(1,flashbookfolder)

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
import _resources.resources as resources
import Flashbook.fb_modules    as m
import _GUI.accelerators_module as acc
import Flashcard.fc_functions    as f2

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
from Books.library import Library

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

class MainFrame(settings,flashbook,flashcard,printer,filetransfer,menusettings,helpmenu,menuopen,flashcardmenu,booksmenu,Bookbuttons.libbuttons,Library):
    
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
        
        self.Flashcard = Flashcard(fontsize = self.LaTeXfontsize)
        
        self.Cardsdeck = Cardsdeck()
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
        self.FlashbookLibrary.addtopic()
        
    def m_buttonBookOnButtonClick(self,event):
        self.FlashbookLibrary.addbook()
        
    def m_buttonReTopicOnButtonClick(self,event):
        self.FlashbookLibrary.renametopic()
        
    
    def m_buttonDelTopicOnButtonClick(self,event):
        self.FlashbookLibrary.deletetopic()
    def m_listTopicsOnListItemSelected(self,event):
        
        pass
    def m_listTopicsOnListItemDeselected(self,event):    
        pass
    def m_buttonStartBookOnButtonClick(self,event):
        index = self.m_listTopics.GetFocusedItem()  
        print(f"index = {index}")
        if index >= 0: #error code is -1
            topic = self.m_listTopics.GetItemText(index)
            self.booktopic = topic
            print(f"topic {topic}")
            
            if not self.FlashbookLibrary.User_is_New():
                self.booknames = self.FlashbookLibrary.getbooknames(topic)
                print(f"booknames = {self.booknames}")
                ## check if books need to be converted to jpg, so that users no longer need to do this manually
                pdf.AddPathvar() #needed to make PDF2jpg work, it sets "Poppler for Windows" as pathvariable
                from_    = str(self.dirpdfbook)
                tempdir_ = str(self.tempdir)
                to_      = str(self.booksdir)
                pdf.ConvertPDF_to_JPG(self,from_,tempdir_,to_,SHOWMESSAGE = False)
                ###
                self.bookname = self.FlashbookLibrary.getcurrentbook(topic)
                
                path = os.path.join(self.booksdir,self.bookname)
                m.openbook(self,path)
            else:
                self.FlashbookLibrary.openmessagebox()
        else:
            MessageBox(0, "You must select a topic before you can start reading", "Error", MB_ICONINFORMATION)
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





class CardsDeck2(settings):
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
                
                if 'topic' in card:
                    mode = 't'
                    key = self.key + f"{mode}{cardindex}"
                    if cardindex == 0:
                        line = self.bookname
                    else:
                        line = card[mode]                    
                    if line.strip() != '': #if the line is not empty, spaces are considered to be empty 
                        _card_ = {'text': line, 'size' : sizelist}
                        addtodict(self, key, _card_)           
                if 'question' in card:
                    sizecard  = sizelist[:4]
                    mode = 'question'
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


import os
import pandas as pd

class Cardsdeck(settings):
    def __init__(self):#,flashcard):
        """ - cards are dicts because then you can easily delete a card from the deck
            - you can then use cardorder to switch cards and just omit a cardnumber from that list"""
        settings.__init__(self)
        settings.settings_get(self)
        
        
        #self.settings_get()
        self.cards_original = {}
        self.cards_edited = {} #to turn latex commands into useable text
        
        self.bookname = ''            
        self.columnnames = ['page','id','question','answer','topic','size']
        

        
    
    def loaddata(self,book = None):
        if book:
            self.bookname = book
            self.path = os.path.join(self.notesdir, self.bookname+'.bok')
            try:
                self.df = pd.read_csv(self.path)
                self.df = self.df.replace({np.nan: None})
                self.loaddata2card()
                
            except FileNotFoundError: 
                MessageBox(0, "Why would this file not exist?", "Error", MB_ICONINFORMATION)
    
    def loaddata2card(self):
        cards = []
        
        for index in range(len(self.df)):
            line = self.df.iloc[index]
            #
            question = ast.literal_eval(line['question'])
            if line['answer']:
                answer = ast.literal_eval(line['answer'])
            else:
                answer = None
            topic = line['topic']
            size = ast.literal_eval(line['size'])
            card_id = line['id']
            if topic:
                """If it contains a topic, then add it as an extra card """
                tsize = size[4]
                cards.append({'index':index,'topic': topic,'size':tsize,'page':999,'pos':(0,0),'scale':1,'id':card_id})
            size_qa = self.CardSizeWithoutTopic(size) #size of the whole Q/A card excluding the topic
            
            keylist = {'index':index,'question' : question, 'size':size_qa,'page':999,'pos':(0,0),'scale':1,'border' : (0,0),'id':card_id}
            
            if answer: #add the answer key
                keylist['answer'] = answer
                if 'text' in answer:
                    keylist['answertext'] = answer['text']
                if 'pic' in answer:
                    keylist['answerpic'] = answer['pic']    
            
            if 'text' in question:
                keylist['questiontext'] = question['text']
            if 'pic' in question:
                keylist['questionpic'] = question['pic']
            cards.append(keylist)
                
        self.cards = cards
        print(f"selfcards = {cards}")
    def CardSizeWithoutTopic(self,tuples_list):
        if isinstance(tuples_list,tuple):
            tuples_list = [tuples_list]
        if len(tuples_list) == 5:
            tuples_list = tuples_list[:4]
        totalwidth,totalheight = 0, 0 
        for size in tuples_list:
            w,h = size
            totalwidth = max(totalwidth,w)
            totalheight += h
        return totalwidth,totalheight
    
    def __len__(self):
        """nr of cards, without counting topics as separate cards"""
        return len([x for x in self.cards if 'topic' not in x])
        
    

class Flashcard(paths):
    def __init__(self,fontsize = 20):
        paths.__init__(self)
        #self.path = os.path.join(savefolder, 'userdata.txt')
        savefolder = self.notesdir
        self.path = savefolder
        self.idfile = os.path.join(savefolder, 'unique_ids.txt')
        self.columnnames = ['page','id','question','answer','topic','size']
        """                [ 0    ,1234,{text:"hello", pic:"\path\img.jpg"}, ... , "topic",[(10,200),...(0,0)]    """
        self.bookname = ''
        self.dict = {}
        self.load_data()
        
        ###
        self.a4page_w = 1240
        self.question = {}
        self.answer    = {}
        self.idnr = 0
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
        self.sizelist = [(0,0),(0,0),(0,0),(0,0),(0,0)] #qtext, qpic, atext,apic, topic
        self.LaTeXfontsize = fontsize
        self.savefolder = savefolder
        
        self.carddict = {}
        self.questiondict = {}
        self.answerdict = {}
        
        self.QuestionPicPaths = []
        self.QuestionPicOrientation = []
        self.AnswerPicPaths = []
        self.AnswerPicOrientation = []
        
        self.pagenr = 1
    def reset(self):
        self.question = {}
        self.answer    = {}
        self.idnr = 0
        
        self.questionpic = ''
        
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
        self.sizelist = [(0,0),(0,0),(0,0),(0,0),(0,0)]#qtext, qpic, atext,apic, topic
        
        
        self.QuestionPicPaths = []
        self.QuestionPicOrientation = []
        self.AnswerPicPaths = []
        self.AnswerPicOrientation = []
    def generate_id(self):        
        def loadid():
            try:
                df_id = pd.read_csv(self.idfile)
            except FileNotFoundError: 
                df_id = pd.DataFrame(columns=['id'])
            return df_id
        def saveid(df):
            df.to_csv(self.idfile,index=False)
        
        df = loadid()
        SEARCH = True
        while SEARCH:
            stringlow  = "abcdefghijklmnopqrstvwxyz"
            stringup = stringlow.upper()
            digits = '0123456789'
            id_nr = ''.join(random.choices(stringlow+stringup+digits, k=4)) 
            if id_nr not in set(df['id'].values):
                #print(id_, set(df['id']), str(df['id'].values))
                df = df.append({'id':str(id_nr)},ignore_index = True)    
                saveid(df)
                df = loadid()
                SEARCH = False
        return id_nr
        
    def setbook(self,bookname):
        if bookname.strip():
            self.bookname = bookname
            self.path = os.path.join(self.savefolder, self.bookname+'.bok')
            
    def load_data(self):
        if self.bookname:
            print(f"path = {self.path}")
            try:
                self.df = pd.read_csv(self.path)
                self.df = self.df.replace({np.nan: None})
                self.check_columns()
            except FileNotFoundError: 
                self.df = pd.DataFrame(columns=self.columnnames)
                self.save_data()
        
    def get_data(self):
        return self.df
    
    def check_columns(self):
        """To check if the saved file has enough columns, e.g. if I added more column names without adding data"""
        columnnames = self.columnnames
        nrcol = len(self.df.columns)
        if len(columnnames) > nrcol:
            for col in columnnames:
                if col not in self.df.columns:
                    pos = len(self.df.columns)
                    self.df.insert(pos, col, None, True)
    def setID(self):
        if not self.idnr:
            self.idnr = self.generate_id()
            
    def saveCard(self):
        self.load_data()
        self.insert_data(page = self.pagenr, id = self.idnr,question = self.question, answer = self.answer, topic = self.topic,size = self.sizelist )
        self.save_data()
        self.idnr = 0
             
    def save_data(self):
        if self.bookname:
            if self.dict:
                self.df = self.df.append(self.dict,ignore_index = True)    
                self.dict = {}
            self.df.to_csv(self.path,index=False)
            print(self.path)
        
    def insert_data(self,**kwargs):
        self.dict = {}
        for key, value in kwargs.items():
            if key in self.columnnames and value:
                self.dict[key] = value
            elif key not in self.columnnames:
                print(f"argument '{key}' is not a column name of : {self.columnnames}")
        
    def get_idnr(self):
        return self.idnr
            
    def get_colnames(self):
        return self.columnnames
    
    def find_row(self,col,value):
        if col in self.df.columns:
            return self.df.loc[self.df[col] == value]    
    
    
    
    def setQ(self,text = '',pic = None):
        if text.strip() != '':
            self.question['text'] = text
            imbool, im = f2.CreateTextCard(self,'manual',text)
            print(f"text size is {imbool} {text}")
            if imbool:
                self.sizelist[0] = im.size
                print(self.sizelist)
        if pic:
            #partial path to image
            self.question['pic'] = pic 
            imsize = imop.findpicturesize_relpath(self,pic)
            self.sizelist[1] =  imsize
    def setA(self,text = '',pic = None):
        if text.strip() != '':
            self.answer['text'] = text
            image_exists, image = f2.CreateTextCard(self,'manual',text)
            if image_exists:
                self.sizelist[2] = image.size
                #self.size_a_txt = image.size 
        if pic:
            #partial path to image
            self.answer['pic'] = pic 
            imsize = imop.findpicturesize_relpath(self,pic)
            self.sizelist[3] =  imsize
    def nrpics(self,mode):
        try:
            if mode.lower() == 'question':
                return len(self.question['pic'])
            else:
                return len(self.answer['pic'])
        except KeyError:
            return 0
        #def getquestionmode(self):
        #    return self.questionmode
    
    def switchmode(self):
        self.questionmode = not self.questionmode
    
    def is_question(self):
        return self.questionmode
    
    def addpic(self,VerticalBool = True,fullpath = None):        
        if self.is_question():
            self.QuestionPicPaths.append(fullpath)
            self.QuestionPicOrientation.append(VerticalBool)
            print(self.QuestionPicPaths)
            print(self.QuestionPicOrientation)
            
        else:
            self.AnswerPicPaths.append(fullpath)
            self.AnswerPicOrientation.append(VerticalBool)
        
            
            
    def fliporientation(self):
        try:
            if self.is_question():
                self.QuestionPicOrientation[-1] = not self.QuestionPicOrientation[-1]
            else:
                self.AnswerPicOrientation[-1] = not self.AnswerPicOrientation[-1]
        except IndexError:
            pass
    
    def setT(self,text):
        if text.strip():
            self.topic = text
            width_card = self.a4page_w
            height_card = int(math.ceil(len(text)/40))*0.75*100
            print(f"! topic = {text}, size = {width_card},{height_card}")
            if height_card:
                print("topic size",width_card,height_card)
                self.sizelist[4] = (width_card,height_card)
    
    
    def StitchPicsTogether(self):
        """LOOK AT LIST OF PATHS 
        IF THE ELEMENT OF THE LIST IS A PATHSTRING IT WILL JOIN THEM VERTICALLY
        IF THE ELEMENT IS ANOTHER LIST OF PATHSTRINGS THEN THOSE WILL BE JOINED HORIZONTALLY
        THE COMBINED PICTURE WILL BE SAVED AS THE FIRST PATHSTRING, THE OTHER PICTURES WILL BE DELETED"""
        
        
        print("combine pics")
        if self.is_question():
            picpaths = self.QuestionPicPaths
            orien = self.QuestionPicOrientation
        else:
            picpaths = self.AnswerPicPaths
            orien = self.AnswerPicOrientation
        
        
        originalpaths = picpaths.copy()
        images = imop.fullpath_to_imagelist(picpaths)
        index = 0
        
        if orien and picpaths:
            """"""
            orien[-1] = True
            while False in orien:    
                print("...")
                if index < len(orien)-1:#last orientation does not matter
                    if orien[index] == False:
                        #combine with next
                        combpic = imop.CombinePicturesHorizontal([images[index],images[index+1]])
                        #replace the second image with the combined image, the combined image will then just assume the second pictures orientation
                        images[index+1] = combpic            
                        #pop the first bool and pic from list
                        orien.pop(index)
                        images.pop(index)            
                    else:
                        index += 1
                else:
                    break
            """combine the images vertically"""
            combinedim = imop.CombinePicturesVertical(images)            
            combinedim.save(originalpaths[0]) #save the image as the first path, delete the other images that were merged    
            for k, imagepath in enumerate(originalpaths):
                if k != 0 and Path(imagepath).exists():
                    Path(imagepath).unlink()
                    
            #convert fullpath to relpath
            imagename = os.path.basename(originalpaths[0])
            if self.is_question():
                self.setQ(pic = imagename)
            else:
                self.setA(pic = imagename)
            return originalpaths[0]
    def getpiclist(self,mode):
        try:
            if mode.lower() == 'question':
                return self.question['pic']
            elif mode.lower() == 'answer':
                return self.answer['pic']
        except KeyError:
            return []
        
    def QuestionExists(self):
        if len(self.question):
            return True
    def setpagenr(self,pagenr):
        self.pagenr = pagenr
        
    def removepics(self):
        def unlinkpics(dir_):    
            print(f"dir = {dir_}")
            if len(dir_) > 1:
                if isinstance(dir_,str):
                    if Path(dir_).exists():
                        Path(dir_).unlink()
                elif isinstance(dir_,list):
                    for pic in dir_:
                        if type(pic) == str and Path(pic).exists():
                            Path(pic).unlink()
            elif len(dir_) == 1:
                try:
                    #just one image
                    pic = dir_[0]
                    if type(pic) == str and Path(pic).exists():
                            Path(pic).unlink()
                except:
                    print("could not remove single image")
                    pass
                
        if self.is_question():
            dir_ = self.QuestionPicPaths
            unlinkpics(dir_)
        else:
            dir_ = self.AnswerPicPaths
            unlinkpics(dir_)    
    
        


    
if __name__ == "__main__":
    # start the application
    app = wx.App(False) 
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
    del app


