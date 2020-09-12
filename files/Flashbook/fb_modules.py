# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018
@author: Anton
"""
from random import randint
import numpy as np
import PIL
import _GUI.active_panel as panel
import wx
import os
#import fb_functions as f
import Flashbook.fb_functions as f
import Flashbook.page as page
import _logging.timingmodule as timing
import _logging.log_module as log
import json
import ctypes
from pathlib import Path
#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW

def list2path(templist):
    output = None
    if type(templist) == list:
        if len(templist) > 1:
            if type(templist[0]) == str:
                output = templist[0]
            elif type(templist[0]) == list:
                output = templist[0][0]
        elif len(templist) == 1:
            if type(templist[0]) == str:
                output = templist[0]
            elif type(templist[0]) == list:
                output = templist[0][0]
    return output


import os
import pandas as pd
class Borders():
    def __init__(self,savefolder = None,bookname = None):
        if savefolder and bookname:
            self.pathfile = os.path.join(savefolder,bookname + "_borders.bor" )
        
        self.id = 0
        self.pagenr = 0
        self.columnnames = ['page','id','rect']
        self.borders_temp = pd.DataFrame(columns=self.columnnames) #empty df
        self.borders_perm = {}
        
        self.load_data()
        
    def reset(self):
        self.id = 0
        self.borders_temp = pd.DataFrame(columns=self.columnnames)
        self.pagenr = 0
    def load_data(self):
        try:
            self.df = pd.read_csv(self.pathfile)
        except FileNotFoundError: 
            self.df = pd.DataFrame(columns=self.columnnames)
        except:
            print("failed to load")
             
    def save_data(self):
        self.load_data()
        #self.insertdata(self.borders_temp)
        
        if len(self.borders_temp):
            self.df = self.df.append(self.borders_temp,ignore_index = True)    
            self.dict = {}
        self.df.to_csv(self.pathfile,index=False)
        print(self.pathfile)
    def gettempcoordinates(self,page = 0):
        
        print(f"gettemp page is {page}")
        print(f"tempbord = {self.borders_temp}")
        print("\n"*3)
        try:
            df = self.borders_temp
            subdf = df.loc[df['page'] == page]
            print(f"anton {df} \n {subdf} ")
            return subdf['rect'].tolist()
        except KeyError:
            print("ERROR! get tempcoord\n"*10)
                
    def getcoordinates(self,page = 0):
        self.load_data()
        try:
            subdf = self.df.loc[self.df['page'] == page]
            coords = subdf['rect'].tolist()
            coords = [json.loads(x) for x in coords] #otherwise the result is ['[]','[]'] a list of string representations of lists, not a list of lists
            
            if isinstance(coords,str):
                coords = list(coords)
            return coords
        except KeyError:
            print("ERROR! getcoord\n"*10)
    def addtempborder(self,page = None, idnr= None, border = None):
        if page and border and idnr:
            print("added to tempbord\n"*10)
            print(self.borders_temp.columns)
            self.borders_temp = self.borders_temp.append({'page':page,'id': idnr,'rect':border}, ignore_index = True)  
            print(f"result\n"*10)
            print(f"result is {self.borders_temp}")
        else:
            print("ERROR!\n"*10)

#%%
def openbook(self,path):
    
    """For scrolling: only remember last few positions, append and pop 
    if the numbers repeat [0,...,0] or [X,...,X] then you know you've reached either 
    the beginning or the end of the window: then flip page"""
    
    self.scrollpos_reset = [5, 4, 3, 2, 1]     
    self.scrollpos = self.scrollpos_reset
    
    #Keep track of "nrlist" which is a 4 digit nr 18-> "0018" so that it is easily sorted in other programs
    path = os.path.splitext(path)[0] #always remove suffixes as they should refer to a folder not file.
    eventpath = Path(path)
    nrlist = []
    picnames = [str(pic) for pic in eventpath.iterdir() if pic.suffix == '.jpg']
    self.totalpages = len(picnames)
    
    if self.totalpages == 0:
        MessageBox(0, " The selected folder does not contain any images!", "Error", MB_ICONINFORMATION)
    
    for number, picname in enumerate(picnames):        
        im_number = number+1 #images are 1 indexed numbers        
        # I only expect in the order of 1000 pages
        # make sure you can use the nrlist for later use so you can save the output as 
        # "Bookname + ****" a sorted 4 digit number
        nrlist.append( str(im_number).zfill(4) )
        
            
    print(f"nr_list = {nrlist}")
    picnames = [x for _,x in sorted(zip(nrlist,picnames))]
    
    self.picnames = picnames
    self.bookname = eventpath.name
    print(f"booktitle is {self.bookname}\n"*100)
    print(f"bookname = {self.bookname}")
    if hasattr(self,'TC'):
        delattr(self,'TC')
    self.TC = timing.TimeCount(self.bookname,"flashbook")
    self.booknamepath = eventpath.relative_to(self.booksdir)
    self.currentpage = 1
    #self.PathBorders = Path(self.bordersdir, self.bookname + '_borders.txt')
    page.LoadPageNr(self)
    #to store all the drawn borders
    self.Borders = Borders(savefolder = self.bordersdir , bookname = self.bookname)
    
    
    book_dir = Path(self.picsdir,self.bookname)
    if not book_dir.exists():
        book_dir.mkdir()
        
    
    self.m_CurrentPageFB.SetValue(str(self.currentpage))
    self.m_TotalPagesFB.SetValue(str(self.totalpages))
    nrlist.sort()
    
    #Open dictionary if it exists
    """
    try:
        with open(self.PathBorders, 'r') as file:
            self.dictionary = json.load(file)
    except:
        self.dictionary = {}
        log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE: no drawn rects found for this file {self.bookname}, continue")
    """ 
        
    try: 
        self.jpgdir    = str(Path(self.booksdir, self.booknamepath, self.picnames[self.currentpage-1]))
        log.DEBUGLOG(debugmode=self.debugmode,msg=f"FB MODULE:\n\t booknamepath {self.booknamepath},\n\t booksdir {self.booksdir}")
        self.pageimage = PIL.Image.open(self.jpgdir)
        self.pageimagecopy = self.pageimage
        self.width, self.height = self.pageimage.size
    except:
        log.ERRORMESSAGE("Error : could not load scrolled window 1")
        
    #Draw borders if they exist
    try:
        if self.drawborders:                    
            pageimage = self.pageimage
            self.pageimage = f.drawCoordinates(self,pageimage)
    except:
        log.ERRORMESSAGE("Error: could not draw borders")
                  
    try:
        image2 = wx.Image( self.width, self.height )
        image2.SetData( self.pageimage.tobytes() )
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        page.SetScrollbars(self)
    except:
        log.ERRORMESSAGE("Error: could not load scrolled window 2")
    panel.SwitchPanel(self,1)
    self.Layout()
    




