# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 23:49:47 2018
@author: Anton
"""

""" to make a spec file
pyi-makespec flashbook 1.0.0.py --icon=book.ico
pyi-makespec flashcard 1.0.0.py --icon=book.ico

# then add at the beginning of those spec files:

import sys
sys.setrecursionlimit(5000)

# then run:

pyinstaller flashbook 1.0.0.spec -- icon=book.ico
pyinstaller flashcard 1.0.0.spec -- icon=book.ico
"""

"""
#https://github.com/wxWidgets/wxPython/blob/master/demo/PopupWindow.py
#https://wxpython.org/Phoenix/docs/html/wx.Font.html#wx.Font
"""

try:
    del app
except:
    print("Welcome to Flashcard , one moment ...")
#--- general ------------------------------------------------------------------
import json
import os
#--- gui ----------------------------------------------------------------------
import wx
import wx.adv as adv
import wx._html
import wx.richtext
import flashcard_gui as gui
#--- displaying text in matplotlib like figure --------------------------------
import shutil
#--- for colored error messages -----------------------------------------------
from termcolor import colored
#-------
import fc_functions as f2
import fc_modules as m2
import fc_initialization as ini2 
import resources

datadir = os.getenv("LOCALAPPDATA")
dir0 = datadir+r"\FlashBook"
dir7 = dir0 + r"\resources"
path_add = os.path.join(dir7,"add.png")
path_min = os.path.join(dir7,"min.png")
path_repeat = os.path.join(dir7,"repeat.png")
path_repeat_na = os.path.join(dir7,"repeat_na.png")
path_icon = os.path.join(dir7,"open-book1.png")


# when using Pyinstaller to get the .exe file: it will standard give an error that it is missing the module 'qwindows.dll'
# since the .exe created by --onefile takes ages to start, i won't be using that option and then module can be found in the folder below
# it is resolved by simply copying the qwindows.dll module next to the .exe file
cwd = os.getcwd()
#print("current cwd {}".format(cwd))
try:
    if os.path.exists(cwd+"\PyQt5\Qt\plugins\platforms\qwindows.dll"):
        shutil.copy2(cwd+"\PyQt5\Qt\plugins\platforms\qwindows.dll",cwd+r'\\') 
        print("copied qwindows.dll module")
    else:
        print("no qwindows.dll module found")    
except:
    print("no qwindows.dll module found (#2)")


#%%
def initialize(self):
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
    # create settings-folder for debugging: user can set it to debug mode if an error were to occur
    if not os.path.exists(dir0+r"\settings.txt"):
        with open(dir0+r"\settings.txt", 'w') as file:
            file.write(json.dumps({'debugmode' : 0})) 
    with open(dir0+r"\settings.txt", 'r') as file:
        debug_var = json.load(file)['debugmode']
        if debug_var == 0:
            self.debugmode = False
        else:
            self.debugmode = True
            print("debugging is enabled")
            
    self.m_filePicker.SetInitialDirectory(self.dir1+'\.') #for filepicker you can't just set a directory like dirPicker, in this case it should end in "\." so that it has to look for files, otherwise it will see a folder as a file...
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
    
def set_richtext(self):
    self.txt = self.m_richText1
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
    

 # create settings folder for debugging
if not os.path.exists(dir0+r"\settings.txt"): 
    with open(dir0+r"\settings.txt", 'w') as file:
        file.write(json.dumps({'debugmode' : 0})) 
with open(dir0+r"\settings.txt", 'r') as file:
    debug_var = json.load(file)['debugmode']
    if debug_var == 0:
        debugmode = False
    else:
        debugmode = True
        print("debugging is enabled: in fc_functions")



"""
###############################################################################
#####              MAINFRAME                                              #####
###############################################################################
"""

class MainFrame(gui.MyFrame):
    #constructor
    #pop up window
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

    # to switch between the two panels
    def m_menuHelpOnMenuSelection( self, event ):
        self.panel2.Show()
        self.panel1.Hide()
        self.Layout()
    def m_richText1OnLeftDown(self,event):
        self.panel1.Show()
        self.panel2.Hide()
        self.Layout()
        
    # initialize
    def __init__(self,parent):
        #initialize parent class
        gui.MyFrame.__init__(self,parent)     
        initialize(self)
        ini2.initializeparameters(self) 
        set_richtext(self) # text for help
        # show correct panel                
        self.panel2.Hide()
        self.panel1.Show()
        self.Layout()
        
        
        # set program icon
        image = wx.Icon(path_icon, type=wx.BITMAP_TYPE_ANY, desiredWidth=-1, desiredHeight=-1)
        self.SetIcon(image)
        
        # set mouse short cuts: 
        self.m_bitmapScroll.Bind( wx.EVT_MOUSEWHEEL, self.m_toolSwitchOnToolClicked )
        self.m_bitmapScroll.Bind( wx.EVT_LEFT_DOWN, self.m_buttonCorrectOnButtonClick)
        self.m_bitmapScroll.Bind( wx.EVT_RIGHT_DOWN, self.m_buttonWrongOnButtonClick )        
        
        # set keyboard short cuts: accelerator table        
        Id_Correct = wx.NewIdRef()
        Id_Wrong   = wx.NewIdRef() 
        Id_card    = wx.NewIdRef() 
        # combine functions with the id
        self.Bind( wx.EVT_MENU, self.m_buttonCorrectOnButtonClick, id = Id_Correct )
        self.Bind( wx.EVT_MENU, self.m_buttonWrongOnButtonClick,   id = Id_Wrong   )
        self.Bind( wx.EVT_MENU, self.m_toolSwitchOnToolClicked,    id = Id_card    )
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
        
        
# start the application
app = wx.App(False) 
frame = MainFrame(None)
frame.Show(True)
app.MainLoop()
del app
