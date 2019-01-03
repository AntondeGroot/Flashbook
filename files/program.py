# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 18:43:04 2017
@author: Anton
"""

import os
import json
import shutil
import PIL
#-------------------------------------------------------------------- gui
import threading
import wx
import wx.adv as adv
import wx.richtext
import wx.html as html
import wx._html
import gui_flashbook as gui
#------------------------------------------------------------------- modules
import fb_initialization as ini 
import fc_initialization as ini2 
import print_initialization as ini3
import resources
import fb_modules    as m
import fc_modules    as m2
import print_modules as m3
import sync_modules  as m4
import server_modules  as server
import fb_functions    as f
import fc_functions    as f2
import print_functions as f3




#--- for colored error messages -----------------------------------------------
from termcolor import colored


def run_flashbook(self):
    print("Welcome to Flashbook , one moment ...")     
    self.m_bitmapScroll.SetBitmap(wx.Bitmap(wx.Image( 1,1 ))) # always empty bitmap, in case someone reruns the program
    self.m_CurrentPage11.SetValue('')
    self.m_CurrentPage12.SetValue('')
    self.m_TotalPages11.SetValue('')
    self.m_TotalPages12.SetValue('')
    
    def initialize(self):
        os.chdir(self.dir0)
        datadir = os.getenv("LOCALAPPDATA")
        dir0 = datadir+r"\FlashBook"
        self.dir0 = dir0
        self.dir1 = dir0 + r"\files"
        self.dir2 = dir0 + r"\pics"
        self.dir3 = dir0 + r"\books"
        self.dir4 = dir0 + r"\temporary"
        self.dir5 = dir0 + r"\borders"
        self.dir6 = dir0 + r"\resources"
        self.temp_dir = self.dir4
        
        # create settings folder for debugging
        if not os.path.exists(self.dirsettings+r"\settings.txt"): 
            with open(dir0+r"\settings.txt", 'w') as file:
                file.write(json.dumps({'debugmode' : 0})) 
        with open(self.dirsettings+r"\settings.txt", 'r') as file:
            debug_var = json.load(file)['debugmode']
            print(debug_var)
            print(type(debug_var))
            if debug_var == 0:
                self.debugmode = False
            else:
                self.debugmode = True
                print("debugging is enabled")
                    
        folders = []
        dirs = [dir0,self.dir1,self.dir2,self.dir3,self.dir4,self.dir5,self.dir6]
        
        print("=========================================================================================")
        print("\nThe files will be saved to the following directory: {}\n".format(dir0))
        for item in dirs:
            if not os.path.exists(item):
                os.makedirs(item)
        
         
        # unpacks png images used in the gui
        resources.resourceimages(self.dir6,self.dir1) 
        #%%
        
        arr = os.listdir(self.dir3)
        for i in range(len(arr)):
            if ('.jpg' not in arr[i]) and ('.png' not in arr[i]):
               #print(arr[i])
               folders.append(arr[i])
        self.nr_books = len(folders)
        folders.sort() 
        
        if len(folders) == 0:
            print("No books were found in directory: {}\n 1) please type '%localappdata%' in windows explorer\n 2) find Flashbook and place a folder containing jpg files of the pdf in the".format(self.dir3)+ r"'\books' directory"+"\n")
        else:
            print("the following books were found:")
            for name in folders:
                print("- {}".format(name))
            print("")
        print("=========================================================================================")
    
    
    
    
    
    
    
    ########################################################################
    self.stayonpage = False
    self.resetselection = False
    self.m_dirPicker11.SetInitialDirectory(self.dir3)
    ## short cuts
    ini.initializeparameters(self)
    m.SetKeyboardShortcuts(self)
    initialize(self)
    def m_CurrentPage11OnText( self, event ):
        print("hallo")

def run_flashcard(self):    
    print("Welcome to Flashcard , one moment ...")
    
    #%%
    def initialize2(self):
        # set all directories
        datadir = os.getenv("LOCALAPPDATA")
        dir0 = datadir+r"\FlashBook"
        self.dir1 = dir0 + r"\files"
        self.dir2 = dir0 + r"\pics"
        self.dir3 = dir0 + r"\books"
        self.dir4 = dir0 + r"\temporary"
        self.dir5 = dir0 + r"\borders"
        self.dir6 = dir0 + r"\resources"
        self.temp_dir = self.dir4

                
        self.m_filePicker21.SetInitialDirectory(self.dir1+'\.') #for filepicker you can't just set a directory like dirPicker, in this case it should end in "\." so that it has to look for files, otherwise it will see a folder as a file...
        os.chdir(self.dir1)
        
        
        dirs = [dir0,self.dir1,self.dir2,self.dir3,self.dir4,self.dir5,self.dir6]        
        print("=========================================================================================")
        print("\nThe files will be saved to the following directory: {}\n".format(dir0))
        
        for item in dirs:
            if not os.path.exists(item):
                os.makedirs(item)
                
        self.csv_dir = dir0+'/date.csv'
        self.file_exists = os.path.isfile(self.csv_dir)
        
        self.dir_LaTeX          = self.dir1
        self.dir_LaTeX_commands = self.dir1
        self.dir_pics           = self.dir2
        # some commands used to create the flashcards and seperate elements: question/answer/picture
        # this way it will remain clear for the user so that he could manually change an entry.
        self.pic_command      = "\pic{"
        self.question_command = r'\\quiz{'
        self.answer_command   = r"\\ans{"
        
        
        for item in dirs:
            if not os.path.exists(item):
                os.makedirs(item)
        # unpack png images used in the gui
        resources.resourceimages(self.dir6,self.dir1) 
        # give info to user about what books he has
        arr = os.listdir(self.dir3) 
        booklist = []
        
        for i in range(len(arr)): # make sure the user didn't accidentally put pictures in the 'booksfolder' but in a folder in 'booksfolder'
            if ('.jpg' not in arr[i]) and ('.png' not in arr[i]):
               booklist.append(arr[i])
        booklist.sort() 
        if len(booklist) == 0:
            print(colored("No books were found in directory: {}\n 1) please type '%localappdata%' in windows explorer \n 2) find Flashbook and place a folder containing jpg files of the pdf in the".format(self.dir3)+ r"'\books' directory"+"\n","red"))
        else:
            print("the following books were found:")
            for name in booklist:
                print("- {}".format(name))
            print("")
        print("=========================================================================================")
        
    
    #%%
        
        



    

    def onShowPopup(self, event):
        win = gui.MyFrame2(self.GetTopLevelParent(), wx.SIMPLE_BORDER)
        btn = event.GetEventObject()
        
        pos = self.panel_pos
        sz =  btn.GetSize()
        win.Position(pos, (0, sz[1]))
        win.Show(True)    
    
    def SettingsPopUp( self, event ):
        win = gui.MyFrame2(self.GetTopLevelParent(), wx.SIMPLE_BORDER)
        #print("panel pos = {}".format(wx.GetMousePosition()))
        pos = wx.GetMousePosition()
        win.Position(pos,(0,0))
        win.Show(True)      


    # initialize
    initialize2(self)
    ini2.initializeparameters(self) 
    
    
    
    # set mouse short cuts: 
    self.m_bitmapScroll.Bind( wx.EVT_MOUSEWHEEL, self.m_toolSwitch21OnToolClicked )
    self.m_bitmapScroll.Bind( wx.EVT_LEFT_DOWN, self.m_buttonCorrectOnButtonClick)
    self.m_bitmapScroll.Bind( wx.EVT_RIGHT_DOWN, self.m_buttonWrongOnButtonClick )        
    
    # set keyboard short cuts: accelerator table        
    Id_Correct = wx.NewIdRef()
    Id_Wrong   = wx.NewIdRef() 
    Id_card    = wx.NewIdRef() 
    # combine functions with the id
    self.Bind( wx.EVT_MENU, self.m_buttonCorrectOnButtonClick, id = Id_Correct )
    self.Bind( wx.EVT_MENU, self.m_buttonWrongOnButtonClick,   id = Id_Wrong   )
    self.Bind( wx.EVT_MENU, self.m_toolSwitch21OnToolClicked,    id = Id_card    )
    # combine id with keyboard = now keyboard is connected to functions
    entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL,  wx.WXK_LEFT, Id_card),
                                  (wx.ACCEL_NORMAL,  wx.WXK_RIGHT, Id_card ),
                                  (wx.ACCEL_NORMAL,  wx.WXK_UP, Id_Correct),
                                  (wx.ACCEL_NORMAL,  wx.WXK_DOWN, Id_Wrong)])
    self.SetAcceleratorTable(entries)
    f2.SetScrollbars(self)
        

        
    # answers given 
    def m_buttonCorrectOnButtonClick( self, event ):
        m2.buttonCorrect(self)
        
    def m_buttonWrongOnButtonClick( self, event ):
        m2.buttonWrong(self)
        
    # flip flashcard
    def m_toolSwitchOnToolClicked( self, event ):
        m2.switchCard(self)
        
    def m_menuItemFlashbookOnMenuSelection( self, event ):
        os.system("explorer {}".format(self.dir3)) 
        
    def m_filePickerOnFileChanged( self, event ): 
        # main program, does all of the preprocessing
        m2.startprogram(self,event)

def get_IP(self,event):
    with open(os.path.join(self.dirIP,'IPadresses.txt'),'r') as file:
        data = json.load(file)
        self.IP1 = data['IP1']
        self.IP2 = data['IP2']
    self.m_txtMyIP.SetValue(self.IP1)
    self.m_txtTargetIP.SetValue(self.IP2)

    

    
def run_print(self,event):                
    
    
    def initialize(self):
        
        
                    
        folders = []
        dirs = [self.dir0,self.dir1,self.dir2,self.dir3,self.dir4,self.dir5,self.dir6]
        
        print("=========================================================================================")
        print("\nThe files will be saved to the following directory: {}\n".format(self.dir0))
        for item in dirs:
            if not os.path.exists(item):
                os.makedirs(item)
        
         
        # unpacks png images used in the gui
        resources.resourceimages(self.dir6,self.dir1) 
        #%%
        
        arr = os.listdir(self.dir3)
        for i in range(len(arr)):
            if ('.jpg' not in arr[i]) and ('.png' not in arr[i]):
               #print(arr[i])
               folders.append(arr[i])
        self.nr_books = len(folders)
        folders.sort() 
        
        if len(folders) == 0:
            print("No books were found in directory: {}\n 1) please type '%localappdata%' in windows explorer\n 2) find Flashbook and place a folder containing jpg files of the pdf in the".format(self.dir3)+ r"'\books' directory"+"\n")
        else:
            print("the following books were found:")
            for name in folders:
                print("- {}".format(name))
            print("")
        print("=========================================================================================")
    
    
    """
    ###############################################################################
    #####              MAINFRAME                                              #####
    ###############################################################################
    """    
    initialize(self)
    #initialize parent class    
    
    self.dir_LaTeX          = self.dir1
    self.dir_LaTeX_commands = self.dir1
    self.dir_pics           = self.dir2
    # some commands used to create the flashcards and seperate elements: question/answer/picture
    # this way it will remain clear for the user so that he could manually change an entry.
    self.pic_command      = "\pic{"
    self.question_command = r'\\quiz{'
    self.answer_command   = r"\\ans{"
        
    
    #
    ini3.initializeparameters(self)                  
    ## LOAD ALL DATA ==========================================================
    m3.startprogram(self,event)
      
    
def SwitchPanel(self,n,m):
    if n == 0:
        self.m_menuHelp.Enable(False)
        self.panel0.Show()
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel5.Hide()
        self.Layout() # force refresh of windows
    elif n == 1:
        self.m_menuHelp.Enable(True)
        self.panel0.Hide()
        self.panel1.Show()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel5.Hide()
        if m == 0:
            self.panel11.Show()
            self.panel12.Hide()
        else:
            self.panel11.Hide()
            self.panel12.Show()
        self.Layout() # force refresh of windows
    elif n == 2:
        self.m_menuHelp.Enable(True)
        self.panel0.Hide()
        self.panel1.Hide()
        self.panel2.Show()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel5.Hide()
        if m == 0:
            self.panel21.Show()
            self.panel22.Hide()
        else:
            self.panel21.Hide()
            self.panel22.Show()
        self.Layout() # force refresh of windows
    elif n ==3:
        self.m_menuHelp.Enable(False)
        self.panel0.Hide()
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Show()
        self.panel4.Hide()
        self.panel5.Hide()
        self.Layout()
    elif n == 4:
        self.m_menuHelp.Enable(True)
        self.panel0.Hide()
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Show()
        self.panel5.Hide()
        self.Layout()
    elif n == 5:
        self.m_menuHelp.Enable(True)
        self.panel0.Hide()
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel5.Show()
        if m == 0:
            self.panel51.Show()
            self.panel52.Hide()
        else:
            self.panel51.Hide()
            self.panel52.Show()
            
        self.Layout()

def set_bitmapbuttons(self):
    image = PIL.Image.open(self.path_fb, mode='r')
    image = image.resize((105, 105), PIL.Image.ANTIALIAS) 
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.m_OpenFlashbook.SetBitmap(wx.Bitmap(image2))
    
    image = PIL.Image.open(self.path_fc, mode='r')
    image = image.resize((105, 105), PIL.Image.ANTIALIAS) 
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.m_OpenFlashcard.SetBitmap(wx.Bitmap(image2))
    
    image = PIL.Image.open(self.path_pr, mode='r')
    image = image.resize((105, 105), PIL.Image.ANTIALIAS) 
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.m_OpenPrint.SetBitmap(wx.Bitmap(image2))
    
    image = PIL.Image.open(self.path_wifi, mode='r')
    image = image.resize((105, 105), PIL.Image.ANTIALIAS) 
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.m_OpenTransfer.SetBitmap(wx.Bitmap(image2))
    # stich
    
    image = PIL.Image.open(self.path_arrow, mode='r')
    image = image.resize((32, 32))     
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow2))
    #
