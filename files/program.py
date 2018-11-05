# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 23:49:47 2018
@author: Anton
"""

import os
import json
import shutil
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
import fb_functions    as f
import fc_functions    as f2
import print_functions as f3




#--- for colored error messages -----------------------------------------------
from termcolor import colored


def run_flashbook(self):
    print("Welcome to Flashbook , one moment ...")        
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
    
    
    
    
    
    def set_richtext(self):
        self.txt = self.m_richText12
        self.txt.BeginBold()
        self.txt.BeginFontSize(16)
        self.txt.WriteText("  Getting Started                                                       ")
        self.txt.EndFontSize()
        self.txt.EndBold()
        self.txt.WriteText("                                                                                 (left click to close window)\n")
        self.txt.BeginFontSize(12)
        self.txt.WriteText("        This will allow you to make flashcards out of the notes you take.\n")
        self.txt.WriteText("        1) You need to convert a pdf to jpg files, using a free online webpage of your choise\n"
                          "        2) Click in the menu 'open/open Flashbook folder' to open the correct Windows folder\n"
                          "        3) Place all the pictures in a map named after the book or course in said folder\n"
                          '        4) Then click on "Browse" in the menubar and open the book that you would like to read\n\n' )
        self.txt.EndFontSize()
        self.txt.BeginBold()
        self.txt.BeginFontSize(16)
        self.txt.WriteText("  Taking Notes:\n")
        self.txt.EndFontSize()
        self.txt.EndBold()
        
        
        
        self.txt.BeginFontSize(12)   
        self.txt.WriteText("        1) You can type a Question and an Answer in the textbox at the bottom, this is LaTeX compatible if you include $$\n"
                          "        2) with ")
        self.txt.BeginBold()
        self.txt.WriteText("left mouse click ")
        self.txt.EndBold()
        self.txt.WriteText("you can take multiple screenshots, all the rectangles you draw will be combined\n        3) With ")
        self.txt.BeginBold()
        self.txt.WriteText("middle mouse click ")
        self.txt.EndBold()
        self.txt.WriteText("you can confirm your selections. It switches between the modes" )
        self.txt.BeginBold()
        self.txt.WriteText(" 'question'")
        self.txt.EndBold()
        self.txt.WriteText(" and ")
        self.txt.BeginBold()
        self.txt.WriteText("'answer' ")
        self.txt.EndBold()
        self.txt.WriteText(".\n        4) With ")
        self.txt.BeginBold()
        self.txt.WriteText("right mouse click ")
        self.txt.EndBold()
        self.txt.WriteText("you can reset your selections, both Question and Answer.\n"
                          
                          "        5) Multiple screenshots across different pages will be combined into a single picture per Question / Answer\n"
                          "        6) Only when you confirm your selection during the Answer mode will everything be saved\n        7) You can use arrow keys to scroll or turn a page\n"
                            )
        self.txt.EndFontSize()
        self.txt.BeginBold()
        self.txt.BeginFontSize(16)
        self.txt.WriteText("  Known Errors:\n")
        self.txt.EndFontSize()
        self.txt.EndBold()
        self.txt.BeginFontSize(12)
        self.txt.WriteText("        - when the program isn't full screen and you try to draw a rectangle it may jump around and select the wrong area. \n"
                           "        - zooming out may result in: not being able to scroll to the next page but only previous pages. The key buttons still work to swtich between pages.\n"
                           "        - same applies to zooming in too much\n"
                           "        - when scrolling; the cursor should be placed on the bookpage itself, otherwise it doesn't have 'focus' and it won't trigger the event that switches the page \n"
                           "        - some websites that convert pdf to jpg may sometimes result in unusual numberings like (1,2a,2b,3,...) this may result in an error when trying to determine the order in which these jpgs should be placed \n"
                           )
        self.txt.EndFontSize()
        self.Layout()
    
    ########################################################################
    
    self.m_dirPicker11.SetInitialDirectory(self.dir3)
    ## short cuts
    ini.initializeparameters(self)
    set_richtext(self)    
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
        
    def set_richtext2(self):
        self.txt = self.m_richText22
        self.txt.BeginBold()
        self.txt.BeginFontSize(16)
        self.txt.WriteText("  Getting Started                                                       ")
        self.txt.EndFontSize()
        self.txt.EndBold()
        self.txt.WriteText("                                                                                 (left click to close window)\n")
        self.txt.BeginFontSize(12)
        self.txt.WriteText("        If you haven't used FlashBook yet, first use that program to create your flashcards.\n")
        self.txt.WriteText("        1) You need to convert a pdf to jpg files, using a free online webpage of your choise\n"
                           "        2) Click in the menu 'open/open Flashbook folder' to open the correct Windows folder\n"
                           "        3) Place all the pictures in a map named after the book or course in said folder\n"
                           '        4) Then open FlashBook and create the flashcards there\n\n' )
        self.txt.EndFontSize()
    
        self.txt.EndFontSize()
        self.txt.BeginBold()
        self.txt.BeginFontSize(16)
        self.txt.WriteText("  Using FlashCard:\n")
        self.txt.EndFontSize()
        self.txt.EndBold()
        self.txt.BeginFontSize(12)
        self.txt.WriteText('        1) open with "browse" a file with the bookname you want to study\n' 
                           "        2) a pop-up window will appear with settings, the settings will be implemented if you close the window.\n"
                           "        3) the total number of questions = 'multiplier' x 'nr questions', in case you want test a subject multiple times \n"
                           "        4) your progress is saved so that you can stop any time you want and continue later on.\n" 
                           "        5) ")
        self.txt.BeginBold()
        self.txt.WriteText("mouse scroll ")
        self.txt.EndBold()
        self.txt.WriteText("let's you switch between question and answer\n        6) " )                       
        self.txt.BeginBold()
        self.txt.WriteText("left mouse click")
        self.txt.EndBold()
        self.txt.WriteText(" marks your answer as correct\n        7) " )                       
        self.txt.BeginBold()
        self.txt.WriteText("right mouse click")
        self.txt.EndBold()
        self.txt.WriteText(" marks your answer as wrong\n        8) be sure to hold your cursor over the image when you do so " )
        self.txt.EndFontSize()
        
        self.Layout()
        



    

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
    set_richtext2(self) # text for help
    
    
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
        

def run_print(self,event):                
    #% path to resources: to circumvent needing a spec. file when you use Pyinstaller 
    datadir = os.getenv("LOCALAPPDATA")
    dir0 = datadir+r"\FlashBook"
    
    
    def initialize(self):
        datadir = os.getenv("LOCALAPPDATA")
        dir0 = datadir+r"\FlashBook"
        #os.chdir(dir0)
        self.dir1 = dir0 + r"\files"
        self.dir2 = dir0 + r"\pics"
        self.dir3 = dir0 + r"\books"
        self.dir4 = dir0 + r"\temporary"
        self.dir5 = dir0 + r"\borders"
        self.dir6 = dir0 + r"\resources"
        self.temp_dir = self.dir4
        
        
                    
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
        


