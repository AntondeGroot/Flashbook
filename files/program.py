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
import Flashbook.fb_modules    as m
import Flashbook.events_mouse as evt_m
import Flashbook.fb_functions    as f
import _logging.log_module as log
#for colored error messages

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
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'PROGRAM: the following books were found: {categories}')
    return pdfs2send, library, pathlib, categories 
    
      
def get_IP(self,event):
    with open(os.path.join(self.dirIP,'IPadresses.txt'),'r') as file:
        data = json.load(file)
        self.IP1 = data['IP1']
        self.IP2 = data['IP2']
    self.m_txtMyIP.SetValue(self.IP1)
    self.m_txtTargetIP.SetValue(self.IP2)
    

def set_richtext(self):
    
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
                      "\t1) Click in the menubar 'Folders/Book PDF folder' to open the correct Windows folder.\n"
                        "\t2) Place the PDFs you would like to read there.\n"
                        '\t3) Convert the PDFs to JPG files using the in-program PDF converter by clicking on "Books/Convert Books" in the menubar.\n\n'
                      '\tYou can now use Flashbook!\n\n\n\n' )
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
    self.txt.WriteText( "        1) You can type a Question and an Answer in the textbox at the bottom, this is LaTeX compatible if you include '$$'.\n"
                        "        2) You can take multiple selections across pages by drawing rectangles with the mouse, all the rectangles you draw will be combined into 1 Question and 1 Answer card\n"
                        "        3) You switch modes when you confirm your selection.\n"
                        "        4) Only when you confirm your selection during the Answer mode will everything be saved. The Answer card can be left blank if you want.\n"
                        "        5) 'Reset selection' resets both Question and Answer cards.\n"
                        "        6) 'Topic' : you can add a topic that will be displayed in a horizontal black bar. E.g. the title of the chapter.\n"
                        "        7) 'Import Screenshot' : you can add extra images. After having imported a screenshot you can draw a rectangle to make a selection.\n")
    
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
    self.txt2.WriteText("\n\t1) A pop-up window will appear with settings, the settings will be implemented if you close the window and the Flashcard program will start.\n"
                        "\t2) If you want to continue a previous session it will supersede all other settings and only use the settings you used last time.\n"
                       "\t3) The total number of questions = 'multiplier' x 'nr questions', in case you want to test a subject multiple times.\n"
                       "\t4) Your progress is saved so that you can stop at any time and continue later.\n")
    self.txt2.EndFontSize()
    self.Layout()   
    
    #richtext for synchronize
    self.txt = self.m_richText4
    self.txt.BeginFontSize(16)
    self.txt.BeginBold()
    self.txt.WriteText("  How to synchronize devices")
    
    self.txt.EndBold()
    self.txt.EndFontSize()
    self.txt.BeginFontSize(12)
    self.txt.WriteText("\t"*29+"(left click to close window)\n")
    self.txt.WriteText("\t 1) The IP address of your device will be displayed as 'My IP', this will be automatically filled in.\n"
                      "\t 2) You will need to manually fill in the IP address of the other device, you must do this on both devices.\n"
                      "\t 3) First click on 'synchronize' on one device.\n"
                       "\t 4) Then do the same on the other device within 60 seconds.\n" 
                       "\t 3) It will only synchronize the PDF versions of the books, not the JPG version.\n"
                       "\t    So After synching you will need to convert newly added books.\n"
                       "\t 4) After completion you can safely continue using Flashbook.")
    self.txt.EndFontSize()
    self.Layout()

    
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
    
