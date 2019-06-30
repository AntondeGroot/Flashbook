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
import PIL
from pathlib import Path
#-------------------------------------------------------------------- gui
import wx
import wx.adv as adv
import wx.richtext
import wx.html as html
import wx._html
#------------------------------------------------------------------- modules
import fb_modules    as m
import fb_functions    as f
#for colored error messages
from termcolor import colored

#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MB_YESNO = 0x00000004
MessageBox = ctypes.windll.user32.MessageBoxW




def checkBooks(self,sleeptime):

    """Check if there are PDFs
    Then Check if they have been converted to JPG, they can be placed in subfolders, grouped together by topic
    e.g. "Study / Physics / Math / ..."   """
       
    time.sleep(sleeptime)
    
    # check PDFs
    library_pdf = [os.path.splitext(x)[0] for x in os.listdir(self.dirpdfbook) if os.path.splitext(x)[1] == '.pdf']
    if len(library_pdf) == 0:
        MessageBox(0, f"Welcome new user! \n\nNo PDFs were found in directory {self.dirpdfbook} \n\nGo to the menubar of the app:  `Open/Book PDF folder`\nPlace a PDF file there and click on Convert\n\nIf the conversion fails: you need to use an online PDF converter since all image manipulations are done to jpg files.", "Welcome to Flashbook", MB_ICONINFORMATION )
    
    # check JPGs
    library = []
    categories  = []
    pathlib = []
    tab  = ' '*3
    
    pdfnames = [os.path.splitext(x)[0] for x in os.listdir(self.dirpdfbook) if os.path.splitext(x)[1] == '.pdf']
    """Look for all final folders""" 
    for root, dirs, _ in os.walk(str(self.booksdir), topdown = False):
        for name in dirs:
            if name in pdfnames:
                library.append(name)
                if os.path.basename(root) != self.booksdir.name: #If it is not the dir you start in
                    categories.append(f'{os.path.basename(root).upper()} - {name}')
                    pathlib.append(os.path.join(os.path.basename(root),name))    
                else:
                    categories.append(f"{tab+name}")
                    pathlib.append(name)
    pdfs2send = [x for x in os.listdir(self.dirpdfbook) if os.path.splitext(x)[0] not in str(pathlib)]    
    
    library.sort()
    categories.sort()
    pathlib.sort()
    
    self.nr_books = len(library)
    
    if len(library) == 0 and len(library_pdf)!= 0:
        MessageBox(0, f"Welcome new user! \n\nNo converted books were found in directory {self.booksdir} \n\nGo to the menubar of the app:  `Open/Book PDF folder`\nPlace a PDF file there and click on Convert\n\nIf the conversion fails: you need to use an online PDF converter since all image manipulations are done to jpg files.", "Welcome to Flashbook", MB_ICONINFORMATION )
    else:
        print("the following books were found:")
        for name in categories:
            print(f"- {name}")
    print("="*90)
    
    
    return pdfs2send, library, pathlib, categories 
    
      
def get_IP(self,event):
    with open(os.path.join(self.dirIP,'IPadresses.txt'),'r') as file:
        data = json.load(file)
        self.IP1 = data['IP1']
        self.IP2 = data['IP2']
        self.client = data['client']
    self.m_txtMyIP.SetValue(self.IP1)
    self.m_txtTargetIP.SetValue(self.IP2)
    self.m_radioClient.SetValue(self.client)
    self.m_radioServer.SetValue(not self.client)
    

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
    imagepath = str(Path(self.resourcedir,"mouseicon.png"))
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
    
    imagepath = str(Path(self.resourcedir,"arrowhelp.png"))
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
    
    imagepath = str(Path(self.resourcedir,"mouseicon2.png"))
    image = PIL.Image.open(imagepath, mode='r').convert('RGB')
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.txt2.WriteImage(wx.Bitmap(image2))
    
    imagepath = str(Path(self.resourcedir,"arrowkeys.png"))
    image = PIL.Image.open(imagepath, mode='r').convert('RGB')
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.txt2.WriteImage(wx.Bitmap(image2))        
    self.txt2.BeginFontSize(12)
    self.txt2.WriteText('\n\t1) Open a subject you want to study by pressing on "browse".\n' 
                       "\t2) A pop-up window will appear with settings, the settings will be implemented if you close the window and the Flashcard program will start.\n"
                        "\t3) If you want to continue a previous session it will supersede all other settings and only use the settings you used last time.\n"
                       "\t4) The total number of questions = 'multiplier' x 'nr questions', in case you want test a subject multiple times.\n"
                       "\t5) Your progress is saved so that you can stop at any time and continue later.\n")
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
import historygraph
def SwitchPanel(self,n):
    self.m_menubar1.EnableTop(2, False)#disable Flashcard menu
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
        if self.m_menuItemGraph.IsChecked(): 
            SHOWIMAGE, imGraph = historygraph.CreateGraph(self)
            if SHOWIMAGE == True:
                self.m_panelGraph.Show()
                image = imGraph
                image2 = wx.Image( imGraph.size)
                image2.SetData( image.tobytes() )
                self.m_bitmapGraph.SetBitmap(wx.Bitmap(image2))
            else:
                self.m_panelGraph.Hide()
        else:
            self.m_panelGraph.Hide()            
    elif n == 1:
        self.panel1.Show()
    elif n == 2:
        self.panel2.Show()
    elif n ==3:
        self.panel3.Show()
    elif n == 4:
        self.panel4.Show()
    elif n == 5:
        self.panel5.Show()
    elif n == 6:
        self.panelHelp.Show()        
    #reset mouse arrow
    m.setcursor(self)    
    self.Layout() # force refresh of windows
    
def Imgpath_to_SquareBitmap(path,size): 
    path = str(path)
    image = PIL.Image.open(path, mode='r')
    image = image.resize((size, size), PIL.Image.ANTIALIAS) 
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    image2 = wx.Bitmap(image2)
    return image2    

def set_bitmapbuttons(self):    
    BMP = Imgpath_to_SquareBitmap(str(self.path_fb),105)
    self.m_OpenFlashbook.SetBitmap(BMP)
    
    BMP = Imgpath_to_SquareBitmap(str(self.path_fc),105)
    self.m_OpenFlashcard.SetBitmap(BMP)
    
    BMP = Imgpath_to_SquareBitmap(str(self.path_pr),105)
    self.m_OpenPrint.SetBitmap(BMP)
    
    BMP = Imgpath_to_SquareBitmap(str(self.path_wifi),105)
    self.m_OpenTransfer.SetBitmap(BMP)
    
    f.SetToolStitchArrow(self,orientation="vertical")
    
