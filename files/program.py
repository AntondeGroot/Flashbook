# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 18:43:04 2017
@author: Anton
"""

import ctypes
import time
import os
joinpath = os.path.join
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
import fb_functions    as f
import fc_functions    as f2
import print_functions as f3
#for colored error messages
from termcolor import colored

#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW


def checkBooks(self,sleeptime):

    """Check if there are PDFs
    Then Check if they have been converted to JPG, they can be placed in subfolders, grouped together by topic
    e.g. "Study / Physics / Math / ..."   """
       
    time.sleep(sleeptime)
    
    # check PDFs
    library_pdf = [os.path.splitext(x)[0] for x in os.listdir(self.dirpdfbook) if os.path.splitext(x)[1] == '.pdf']
    if len(library_pdf) == 0:
        MessageBox(0, f"Welcome new user! \n\nNo PDFs were found in directory {self.dirpdfbook} \n\nGo to the menubar of the app:  `Open/Book PDF folder`\nPlace a PDF file there and click on Convert\n\nIf the conversion fails: you need to use an online PDF converter since all image manipulations are done to jpg files.", "Welcome to Flashbook", ICON_EXCLAIM)
    
    # check JPGs
    library = []
    categories  = []
    pathlib = []
    tab  = ' '*3
    
    pdfnames = [os.path.splitext(x)[0] for x in os.listdir(self.dirpdfbook) if os.path.splitext(x)[1] == '.pdf']
    """Look for all final folders""" 
    for root, dirs, _ in os.walk(self.dir3, topdown = False):
        for name in dirs:
            if name in pdfnames:
                library.append(name)
                if os.path.basename(root) != os.path.basename(self.dir3): #If it is not the dir you start in
                    categories.append(f'{os.path.basename(root).upper()} - {name}')
                    pathlib.append(os.path.join(os.path.basename(root),name))    
                else:
                    categories.append(f"{tab+name}")
                    pathlib.append(name)
    pdfs2send = [x for x in pdfnames if x not in str(pathlib)]    
    
    library.sort()
    categories.sort()
    pathlib.sort()
    
    self.nr_books = len(library)
    
    if len(library) == 0:
        MessageBox(0, f"Welcome new user! \n\nNo converted books were found in directory {self.dir3} \n\nGo to the menubar of the app:  `Open/Book PDF folder`\nPlace a PDF file there and click on Convert\n\nIf the conversion fails: you need to use an online PDF converter since all image manipulations are done to jpg files.", "Welcome to Flashbook", ICON_EXCLAIM)
    else:
        print("the following books were found:")
        for name in categories:
            print(f"- {name}")
    print("="*90)
    
    
    return library, pathlib, pdfs2send, categories 
    


def run_flashbook(self):
    print("Welcome to Flashbook , one moment ...")     
    self.m_bitmapScroll.SetBitmap(wx.Bitmap(wx.Image( 1,1 ))) # always empty bitmap, in case someone reruns the program
    self.m_CurrentPage11.SetValue('')
    self.m_TotalPages11.SetValue('')
    
    def initialize(self):
        os.chdir(self.dir0)
        
        # create settings folder for debugging
        if not os.path.exists(self.dirsettings+r"\settings.txt"): 
            with open(self.dir0+r"\settings.txt", 'w') as file:
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
                    
        dirs = [self.dir0,self.dir1,self.dir2,self.dir3,self.dir4,self.dir5,self.dir6]
        
        print("="*90)
        print(f"\nThe files will be saved to the following directory: {self.dir0}\n")
        for item in dirs:
            if not os.path.exists(item):
                os.makedirs(item)
         
        # unpacks png images used in the gui
        resources.resourceimages(self.dir6,self.dir1) 
        
    ##
    self.stayonpage = False
    self.resetselection = False
    self.m_dirPicker11.SetInitialDirectory(self.dir3)
    #short cuts
    ini.initializeparameters(self)
    m.SetKeyboardShortcuts(self)
    initialize(self)

def run_flashcard(self):    
    def initialize2(self):
        # set all directories
                
        self.m_filePicker21.SetInitialDirectory(self.dir1+'\.') #for filepicker you can't just set a directory like dirPicker, in this case it should end in "\." so that it has to look for files, otherwise it will see a folder as a file...
        os.chdir(self.dir1)        
        
        dirs = [self.dir0,self.dir1,self.dir2,self.dir3,self.dir4,self.dir5,self.dir6]        
        print("="*90)
        print("\nThe files will be saved to the following directory: {}\n".format(self.dir0))
        
        for item in dirs:
            if not os.path.exists(item):
                os.makedirs(item)
                
        self.csv_dir = self.dir0+'/date.csv'
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
        dirs = [self.dir0,self.dir1,self.dir2,self.dir3,self.dir4,self.dir5,self.dir6]       
        print("="*90)
        print("\nThe files will be saved to the following directory: {}\n".format(self.dir0))
        for item in dirs:
            if not os.path.exists(item):
                os.makedirs(item)
        resources.resourceimages(self.dir6,self.dir1) # unpacks png images used in the gui
    
    """MAINFRAME"""
    initialize(self)    
    self.dir_LaTeX          = self.dir1
    self.dir_LaTeX_commands = self.dir1
    self.dir_pics           = self.dir2
    # some commands used to create the flashcards and seperate elements: question/answer/picture
    # this way it will remain clear for the user so that he could manually change an entry.
    self.pic_command      = "\pic{"
    self.question_command = r'\\quiz{'
    self.answer_command   = r"\\ans{"
    ini3.initializeparameters(self)                  
    #Load all data
    m3.startprogram(self,event)

def set_richtext(self):
    #richtext for General tab
    self.txt2 = self.m_richText1
    self.txt2.BeginBold()
    self.txt2.EndBold()
    self.txt2.EndFontSize()
    self.txt2.BeginBold()
    self.txt2.BeginFontSize(16)
    self.txt2.WriteText("  How to use this program:")
    self.txt2.EndFontSize()
    self.txt2.EndBold()
    self.txt2.WriteText("\t"*32+"(left click to close window)\n")
    self.txt2.BeginBold()
    self.txt2.BeginFontSize(12)
    self.txt2.WriteText("\n\tFlashbook:")
    self.txt2.EndFontSize()
    self.txt2.EndBold()
    self.txt2.WriteText("\tYou can convert a PDF to JPG and use it to take notes while you read. \n")
    self.txt2.BeginBold()
    self.txt2.BeginFontSize(12)
    self.txt2.WriteText("\tFlashcard:")
    self.txt2.EndFontSize()
    self.txt2.EndBold()
    self.txt2.WriteText("\tStudy the notes you took, you can stop anytime and continue later on.\n")
    self.txt2.BeginBold()
    self.txt2.BeginFontSize(12)
    self.txt2.WriteText("\tPrint:")
    self.txt2.EndFontSize()
    self.txt2.EndBold()
    self.txt2.WriteText("\t\tAll the notes you took are converted to a PDF. Multiple cards are placed side by side, you can then adjust a parameter while looking at the number of pages so you can fine tune the file.\n")
    self.txt2.BeginBold()
    self.txt2.BeginFontSize(12)
    self.txt2.WriteText("\tSync:")
    self.txt2.EndFontSize()
    self.txt2.EndBold()
    self.txt2.WriteText("\t\tYou can synchronize two devices as long as they are on the same network e.g. your laptop and desktop using your local wifi network.\n")
    self.txt2.EndFontSize()
    self.Layout()   
    
    # richtext for Flashbook
    self.txt = self.m_richText2
    self.txt.BeginBold()
    self.txt.BeginFontSize(16)
    self.txt.WriteText("  Using Flashbook")
    self.txt.EndFontSize()
    self.txt.EndBold()
    self.txt.WriteText("\t"*32+"(left click to close window)\n")
    self.txt.BeginFontSize(12)
    self.txt.WriteText("\tThis will allow you to make flashcards while reading a book.\n")
    self.txt.WriteText(
                      "\t1) Click in the menubar 'open/Book PDF folder' to open the correct Windows folders.\n"
                        "\t2) Place the PDFs you would like to read there.\n"
                        '\t3) Convert the PDFs to JPG files using the in-program PDF converter by clicking on "Convert Books" in the menubar.\n'
                      "\t4) All image operations are performed on JPG files, if the conversion fails:\n"
            "\t\t- Place all the pictures in a map named after the book in the folder you get from 'open/Book JPG folder'\n"
                      '\t5) Then click on "Browse" in the menubar and open the book that you would like to read\n\n' )
    self.txt.EndFontSize()
    self.txt.BeginBold()
    self.txt.BeginFontSize(16)
    self.txt.WriteText("  Taking Notes:\n")
    self.txt.EndFontSize()
    self.txt.EndBold()    
    imagepath = os.path.join(self.dir7,"mouseicon.png")
    image = PIL.Image.open(imagepath, mode='r').convert('RGB')
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.txt.WriteImage(wx.Bitmap(image2))
    self.txt.Newline()    
    self.txt.BeginFontSize(12)   
    self.txt.WriteText( "        1) You can type a Question and an Answer in the textbox at the bottom, this is LaTeX compatible if you include $$\n"
                        "        2) you can take multiple selections across pages, all the rectangles you draw will be combined into 1 Question and 1 Answer card\n"
                        "        3) Only when you confirm your selection during the Answer mode will everything be saved\n"
                        "        4) You switch modes when you confirm your selection\n"
                        "        5) 'Reset selection' resets both Question and Answer cards\n")
    
    imagepath = os.path.join(self.dir7,"arrowhelp.png")
    image = PIL.Image.open(imagepath, mode='r').convert('RGB')
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.txt.WriteText("\n              ")
    self.txt.WriteImage(wx.Bitmap(image2))
    self.txt.WriteText("  Indicates in which direction the notes are taken, you can use this to create a mozaic.\n         E.g. when a sentence ends on a differen line but you want it to appear as one line in your notes\n         When the arrow point down, you paste a selection on another 'row'. If it points to the right it just puts it behind the last selection you made.")
    self.txt.EndFontSize()
    self.txt.BeginFontSize(16) 
    self.txt.BeginBold()
    self.txt.WriteText( "\n\n        N.B.\n")
    self.txt.EndBold()
    self.txt.EndFontSize()
    self.txt.BeginFontSize(12)
    self.txt.WriteText( "        Whenever you try to type something in the textbox and want to move the 'text cursor': make sure that the mouse is placed on the textbox.\n "
                        "        Otherwise you'll switch pages when you try to move the 'text cursor' with the arrow keys. ")
    self.txt.EndFontSize()
    self.Layout()      
    
    # richtext for Flashcard
    self.txt2 = self.m_richText3
    self.txt2.BeginBold()
    self.txt2.EndBold()
    self.txt2.EndFontSize()
    self.txt2.BeginBold()
    self.txt2.BeginFontSize(16)
    self.txt2.WriteText("  Using Flashcard:")
    self.txt2.EndFontSize()
    self.txt2.EndBold()
    self.txt2.WriteText("\t"*32+"(left click to close window)\n")
    imagepath = os.path.join(self.dir7,"mouseicon2.png")
    image = PIL.Image.open(imagepath, mode='r').convert('RGB')
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.txt2.WriteImage(wx.Bitmap(image2))
    imagepath = os.path.join(self.dir7,"arrowkeys.png")
    image = PIL.Image.open(imagepath, mode='r').convert('RGB')
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.txt2.WriteImage(wx.Bitmap(image2))        
    self.txt2.BeginFontSize(12)
    self.txt2.WriteText('\n\t1) Open a subject you want to study by pressing on "browse".\n' 
                       "\t2) A pop-up window will appear with settings, the settings will be implemented if you close the window and the Flashcard program will start.\n"
                        "\t3) If you want to continue a previous session it will supersede all other settings and only use the settings you used last time.\n"
                       "\t4) The total number of questions = 'multiplier' x 'nr questions', in case you want test a subject multiple times.\n"
                       "\t5) Your progress is saved so that you can stop at any time and continue later.\n" 
                       "\t6) Be sure to hold your cursor over the image when you use the mouse short cuts.")
    self.txt2.EndFontSize()
    self.Layout()   
    
    #richtext for synchronize
    self.txt = self.m_richText4
    self.txt.BeginFontSize(16)
    self.txt.BeginBold()
    self.txt.WriteText("  How to synchronize devices")
    
    self.txt.EndBold()
    self.txt.EndFontSize()
    self.txt2.BeginFontSize(12)
    self.txt.WriteText("\t"*29+"(left click to close window)\n")
    self.txt.WriteText("\t 1) First assign one device the role as 'server' and click on 'transfer'\n"
                       "\t 2) Then select on the other device 'client' and click 'transfer'.\n" 
                       "\t 3) It is important that you start the server before the client.\n"
                       "\t 4) This will start the process where the 'client' starts sending data to the 'server'.\n"
                       "\t 5) After the transfer is complete the roles are reversed automatically.\n"
                       "\t 6) This makes sure both devices contain all the data.\n"    
                       "\t 7) When all data has been transferred you can safely continue using Flashbook.")
    self.txt.EndFontSize()
    self.Layout()
    
def SwitchPanel(self,n):
    self.m_menuHelp.Enable(True)
    self.panel0.Hide()
    self.panel1.Hide()
    self.panel2.Hide()
    self.panel3.Hide()
    self.panel4.Hide()
    self.panel5.Hide()
    self.panelHelp.Hide()
    if n == 0:
        self.panel0.Show()        
    elif n == 1:
        self.panel1.Show()
        #self.panel11.Show()
    elif n == 2:
        self.panel2.Show()
        #self.panel21.Show()
    elif n ==3:
        self.panel3.Show()
    elif n == 4:
        self.panel4.Show()
    elif n == 5:
        self.panel5.Show()
        #self.panel51.Show()
    elif n == 6:
        self.panelHelp.Show()         
    self.Layout() # force refresh of windows
    
def set_bitmapbuttons(self):
    
    def Img2Bitmap(path,size):    
        image = PIL.Image.open(path, mode='r')
        image = image.resize((size, size), PIL.Image.ANTIALIAS) 
        image2 = wx.Image( image.size)
        image2.SetData( image.tobytes() )
        return image2
    
    image2 = Img2Bitmap(self.path_fb,105)
    self.m_OpenFlashbook.SetBitmap(wx.Bitmap(image2))
    
    image2 = Img2Bitmap(self.path_fc,105)
    self.m_OpenFlashcard.SetBitmap(wx.Bitmap(image2))
    
    image2 = Img2Bitmap(self.path_pr,105)
    self.m_OpenPrint.SetBitmap(wx.Bitmap(image2))
    
    image2 = Img2Bitmap(self.path_wifi,105)
    self.m_OpenTransfer.SetBitmap(wx.Bitmap(image2))
    
    #image2 = Img2Bitmap(self.path_arrow,32)
    self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow2))
    
