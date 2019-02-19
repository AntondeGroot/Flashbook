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
joinpath = os.path.join
import json
import shutil
import subprocess 
import PIL
import time
#-------------------------------------------------------------------- gui
import threading
import wx
import wx.adv as adv
import wx.richtext
import wx.html as html
import wx._html
import gui_flashbook as gui
import ctypes # pop up messages
import logging
#------------------------------------------------------------------- modules
import program as p
import fb_initialization as ini 
import fc_initialization as ini2 
import print_initialization as ini3
import resources
import fb_modules    as m
import fc_modules    as m2
import print_modules as m3
import sync_modules  as m4
import pdf_modules   as m5
import fb_functions    as f
import fc_functions    as f2
import print_functions as f3
#from print_modules import notes2paper
#--- for colored error messages ------------------------------------- debugging
from termcolor import colored
import win32clipboard
from win32api import GetSystemMetrics
from PIL import Image
import wmi # for IPaddress
import sys
sys.setrecursionlimit(5000)

path = os.path.join(os.getenv("LOCALAPPDATA"),'FlashBook','temporary')
LOG_FILENAME = os.path.join(path,'logging_traceback.out')
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logging.info('New session has started')


#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW

"""when using Pyinstaller to create the .exe file: it will standardly give an error that it is missing the module 'qwindows.dll'
since the .exe created by --onefile takes ages to start, i won't be using that option and then module can be found in the folder below
it is resolved by simply copying the qwindows.dll module next to the .exe file"""

try:
    cwd = os.getcwd()
    if os.path.exists(cwd+"\PyQt5\Qt\plugins\platforms\qwindows.dll"):
        shutil.copy2(cwd+"\PyQt5\Qt\plugins\platforms\qwindows.dll",cwd+r'\\') 
        #print("copied qwindows.dll module")
    else:
        print("qwindows.dll module missing")    
except:
    print("no qwindows.dll module found  (#2)")
            
#% path to resources: 
def setup_sources(self):
    self.datadir      = os.getenv("LOCALAPPDATA")
    self.dir0         = joinpath(self.datadir,"FlashBook")
    self.dir7         = joinpath(self.dir0,"resources")
    self.path_add     = joinpath(self.dir7,"add.png")
    self.path_min     = joinpath(self.dir7,"min.png")
    self.path_icon    = joinpath(self.dir7,"open-book1.png")
    self.path_fb      = joinpath(self.dir7,"flashbook.png")
    self.path_fc      = joinpath(self.dir7,"flashcard.png")
    self.path_wifi    = joinpath(self.dir7,"wifi.png")
    self.path_pr      = joinpath(self.dir7,"print.png")
    self.path_arrow   = joinpath(self.dir7,"arrow.png")
    self.path_arrow2  = joinpath(self.dir7,"arrow2.png")
    self.path_convert = joinpath(self.dir7,"convert.png")
    self.path_folder  = joinpath(self.dir7,"folder.png")
    self.path_repeat  = joinpath(self.dir7,"repeat.png")
    self.path_repeat_na = joinpath(self.dir7,"repeat_na.png")
#%% settings   
def settings_get(self):

    with open(joinpath(self.dirsettings,"settings.txt"), 'r') as file:
        settings   = json.load(file)
        debug_var  = settings['debugmode']
        self.pdfmultiplier     = settings['pdfmultiplier'] 
        self.QAline_thickness  = settings['QAline_thickness']
        self.pdfline_thickness = settings['pdfline_thickness']
        self.QAline_color      = tuple(settings['QAline_color'])
        self.pdfline_color     = tuple(settings['pdfline_color'])        
        self.QAline_bool       = settings['QAline_bool']
        self.pdfline_bool      = settings['pdfline_bool']
        
        if debug_var == 0:
            self.debugmode = False
        else:
            self.debugmode = True
            print("debugging is enabled")
            
def settings_create(self):
    if not os.path.exists(self.dirsettings+r"\settings.txt"):   
        with open(self.dirsettings+r"\settings.txt", 'w') as file:
            file.write(json.dumps({'debugmode' : 0,'pdfmultiplier': 1.0, 'QAline_thickness' : 1, 'pdfline_thickness' : 5, 
                                   'QAline_color' : (0,0,0), 'pdfline_color' : (18,5,250), 'QAline_bool': True,'pdfline_bool': True }))       
            file.close()
            
def settings_set(self):
    with open(self.dirsettings+r"\settings.txt", 'w') as file:
        file.write(json.dumps({'debugmode' : 0, 'pdfmultiplier': self.pdfmultiplier,'QAline_thickness' : self.QAline_thickness, 'pdfline_thickness': self.pdfline_thickness, 
                               'QAline_color' : self.QAline_color, 'pdfline_color' : self.pdfline_color, 'QAline_bool': self.QAline_bool,'pdfline_bool': self.pdfline_bool}))           
        file.close()
        
#%%
def initialize(self):
    datadir = os.getenv("LOCALAPPDATA")
    dir0 = joinpath(datadir,"FlashBook")
    self.dir0 = dir0
    self.dir1 = joinpath(dir0,"files")
    self.dir2 = joinpath(dir0,"pics")
    self.dir3 = joinpath(dir0,"books")
    self.dir4 = joinpath(dir0,"temporary")
    self.dir5 = joinpath(dir0,"borders")
    self.dir6 = joinpath(dir0,"resources")
    self.dirIP = joinpath(dir0,"IPadresses")
    self.dirpdf = joinpath(dir0,"PDF folder")
    self.dirpdfbook = joinpath(dir0,"PDF books")
    self.dirsettings = joinpath(dir0,"settings")
    self.temp_dir = self.dir4
    self.statsdir = joinpath(self.dirsettings, 'data_sessions.json')
    
    dirs = [self.dir0, self.dir1, self.dir2, self.dir3, self.dir4, self.dir5, self.dir6, self.dirpdf, self.dirsettings, self.dirIP, self.dirpdfbook]
    try:
        if not os.path.exists(joinpath(self.dirIP,'IPadresses.txt')):
            
            wmi_obj = wmi.WMI()
            wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled = True"
            wmi_out = wmi_obj.query(wmi_sql)[0] #only 1 query
            
            myIP = wmi_out.IPAddress[0]          
           
            with open(joinpath(self.dirIP,'IPadresses.txt'),'w') as f:
                f.write(json.dumps({'IP1' : myIP,'IP2': ""})) 
                f.close()
    except:
        print("Error: could not access internet")
        
    print("="*90)
    print(f"\nThe files will be saved to the following directory: {dir0}\n")
    for item in dirs:
        if not os.path.exists(item):
            os.makedirs(item)
    # create settings folder for debugging
    settings_create(self)
    settings_get(self)
    #unpack png images used in the gui
    resources.resourceimages(self.dir6,self.dir1) 
    


    
"""
###############################################################################
#####              MAINFRAME                                              #####
###############################################################################
"""

class MainFrame(gui.MyFrame):
    #constructor    
    def __init__(self,parent): 
        initialize(self)
        setup_sources(self)
        
        #initialize parent class
        icons = [wx.Bitmap(self.path_folder) , wx.Bitmap(self.path_convert) ]
        gui.MyFrame.__init__(self,parent,icons) #added extra argument, so that WXpython.py can easily add the Dialog Windows (which require an extra argument), which is now used to add extra icons to the menubar             
        self.Maximize(True) # open the app window maximized
        t_books = lambda self,delay : threading.Thread(target = p.checkBooks , args=(self,delay )).start()
        t_books(self, 2) 
        
        self.stitchmode_v = True
        self.FilePickEvent = True 
        p.set_bitmapbuttons(self)
        p.set_richtext(self)
        # icon
        iconimage = wx.Icon(self.path_icon, type=wx.BITMAP_TYPE_ANY, desiredWidth=-1, desiredHeight=-1)
        self.SetIcon(iconimage)
        p.SwitchPanel(self,0)
        self.printpreview = True
                        
    #%% Panel selection
    " Panel selection "
    def m_OpenFlashbookOnButtonClick( self, event ):
        self.stayonpage = False
        self.stitchmode_v = True # stich vertical or horizontal
        self.m_dirPicker11.SetInitialDirectory(self.dir3)
        self.m_dirPicker11.SetPath(self.dir3)
        # at first disable the border of the bitmap, 
        # otherwise you get a bordered empty bitmap. Enable the border only when there is a bitmap
        self.m_bitmapScroll.SetWindowStyleFlag(False) 
        setup_sources(self)
        p.SwitchPanel(self,1)      
        m.SetKeyboardShortcuts(self)
        p.run_flashbook(self)
        
    def m_OpenFlashcardOnButtonClick( self, event ):
        p.SwitchPanel(self,2)
        p.run_flashcard(self)
    def m_OpenTransferOnButtonClick(self,event):
        p.SwitchPanel(self,5)
        p.get_IP(self,event)
        #client = self.m_radioClient.GetValue() #boolean
        #p.run_transfer(self,event,client)
        m4.initialize(self,event)
        
    def m_OpenPrintOnButtonClick(self,event):
        t_panel = lambda self,page : threading.Thread(target = p.SwitchPanel , args=(self,page )).start()
        t_panel(self, 3) 
        
        with wx.FileDialog(self, "Choose which file to print", wildcard="*.tex",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            fileDialog.SetPath(self.dir1+'\.')
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                p.SwitchPanel(self,0) 
                return None    # the user changed their mind
            else:
                self.fileDialog = fileDialog
                self.FilePickEvent = True
                settings_get(self)
                self.m_colorQAline.SetColour(self.QAline_color)
                self.m_colorPDFline.SetColour(self.pdfline_color)
                self.m_lineWpdf.SetValue(str(self.pdfline_thickness))
                self.m_lineWqa.SetValue(str(self.QAline_thickness))
                self.m_lineQA.SetValue(self.QAline_bool)
                self.m_linePDF.SetValue(self.pdfline_bool)            
                
                t_preview = lambda self,evt : threading.Thread(target = m3.print_preview, name = 't_preview' , args=(self,evt )).run()
                t_preview(self, event) 
                
    #%% menu item events
    " menu item events "
    def m_toolStitchOnButtonClick( self, event ):
        self.stitchmode_v =  not self.stitchmode_v
        if self.stitchmode_v == True:
            self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow2))
        else:
            self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow))
        
        """The following is used to create a mozaic of pictures. There is a question mode and an answer mode
        The pics are stored in a list, and when the element of a list is another list it means that particular list is ment to be stitched horizontally
        while all the other elements are stitched vertically
        all it does is switch [a,...,[x]] for [a,...,x] and back to [a,...,[x]] depending on whether the user has pushed a button to change the direction in which the notes should be stitched together.  """
        
        if hasattr(self,'bookname') and self.bookname != '': # a book has been chosen
            #stitch it vertically
            if self.stitchmode_v == True:
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
                
            
    def m_menuItemFlashbookOnMenuSelection( self, event ):        
        subprocess.Popen(f"explorer {self.dirpdfbook}")
        
    def m_menuItemJPGOnMenuSelection( self, event ):
        subprocess.Popen(f"explorer {self.dir3}")
        
    def m_menuItemBackToMainOnMenuSelection( self, event ):
        p.SwitchPanel(self,0)  
        
    def m_menuItemConvertOnMenuSelection( self, event ):
        
        m5.AddPathvar() #needed to make PDF2jpg work, it sets "Poppler for Windows" as pathvariable
        from_    = self.dirpdfbook
        tempdir_ = self.dir4
        to_      = self.dir3 
        
        t_pdf = lambda self, from_, tempdir_, to_ : threading.Thread(target = m5.ConvertPDF_to_JPG , args=(self,from_, tempdir_, to_ )).start()
        t_pdf(self, from_, tempdir_, to_) 
        
    def m_menuPDFfolderOnMenuSelection( self, event ):
        subprocess.Popen(f"explorer {self.dirpdf}")
        
    def m_menuHelpOnMenuSelection( self, event ):
        if self.panel0.IsShown():
            self.lastpage = 0
        elif self.panel1.IsShown():
            self.lastpage = 1
        elif self.panel2.IsShown():
            self.lastpage = 2
        elif self.panel3.IsShown():
            self.lastpage = 3    
        elif self.panel4.IsShown():
            self.lastpage = 4
        elif self.panel5.IsShown():
            self.lastpage = 5
        p.SwitchPanel(self,6)
            
    def m_richText12OnLeftDown( self, event ):
        p.SwitchPanel(self,1) 
    def m_txtHelpSyncOnLeftDown(self,event):
        p.SwitchPanel(self,5) 
    #%% flashbook
    " flashbook "
    #Import screenshot
    def m_btnScreenshotOnButtonClick( self, event ):
        self.BoolCropped = False # is image cropped
        self.currentpage_backup = self.currentpage
        self.currentpage = 'prtscr'
        m3.import_screenshot(self,event)
        
    def m_textCtrl2OnEnterWindow( self, event ):
        print("entered window")
        m.RemoveKeyboardShortcuts(self,0)
	
    def m_textCtrl2OnLeaveWindow( self, event ):
        m.SetKeyboardShortcuts(self)
    
    def m_btnSelectOnButtonClick( self, event ):
        if hasattr(self,"backupimage"):
            image3 = self.backupimage
            self.m_bitmap4.SetBitmap(image3)
        self.Layout()
    
    def m_btnImportScreenshotOnButtonClick( self, event ):
        self.stayonpage = True
        #load screenshot
        if self.BoolCropped == False: #load original screenshot
            img = PIL.Image.open(joinpath(self.dir4,"screenshot.png"))
            self.pageimagecopy = img
            self.pageimage = img        
            image2 = wx.Image( self.width, self.height )
            image2.SetData( self.pageimage.tobytes() )
            self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        p.SwitchPanel(self,1)
        f.ShowPrintScreen(self)
        
        
    def m_bitmap4OnLeftDown( self, event ):
        self.panel4_pos = self.m_bitmap4.ScreenToClient(wx.GetMousePosition())
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        
    def m_bitmap4OnLeftUp( self, event ):
        m.panel4_bitmapleftup(self,event)   
        self.panel4.Layout()
        self.Update()
        self.Refresh()
        
    def m_dirPicker11OnDirChanged( self, event ):
        print("dir has changed")
        self.m_bitmapScroll.SetWindowStyleFlag(wx.SIMPLE_BORDER)
        m.dirchanged(self,event)        
        
    
	# zoom in #================================================================
    def m_toolPlus11OnToolClicked( self, event ):
        m.zoomin(self,event)
	
    def m_toolMin11OnToolClicked( self, event ):
        m.zoomout(self,event)
	
    # change page #============================================================
    def m_toolBack11OnToolClicked( self, event ):
        self.stayonpage = False
        m.previouspage(self,event)
	
    def m_toolNext11OnToolClicked( self, event ):
        self.stayonpage = False
        m.nextpage(self,event)
    def m_toolUPOnToolClicked( self, event ):
        m.arrowscroll(self,event,'up')
            
    def m_toolDOWNOnToolClicked( self, event ):
        m.arrowscroll(self,event,'down')        
    
    
    
    
    
    
    def m_CurrentPage11OnEnterWindow( self, event ):
        m.RemoveKeyboardShortcuts(self,1)
        
    def m_CurrentPage11OnLeaveWindow( self, event ):
        m.SetKeyboardShortcuts(self)
        try:
            self.currentpage = int(self.m_CurrentPage11.GetValue())
        except:
            self.currentpage = 1
        m.switchpage(self,event)
    
    
    def m_bitmapScrollOnMouseWheel( self, event ):
        m.mousewheel(self,event)
        
    # user selections #========================================================
    def m_resetselectionOnButtonClick( self, event ):               
        m.resetselection(self,event)
    
    def m_enterselectionOnButtonClick( self, event ):
        m.selectionentered(self,event)
        
    def m_checkBoxCursor11OnCheckBox( self, event ):  
        m.setcursor(self,event)
    
    # show drawn borders 
    def m_checkBox11OnCheckBox( self, event ):
        try:
            self.drawborders = self.m_checkBox11.IsChecked()   
            print(f"checkbox is {self.drawborders}")
            self.pageimage = self.pageimagecopy # reset image
            f.ShowPage(self)
            self.Layout()
        except:# a book hasn't been opened
            pass
        
	# draw borders #===========================================================
    def m_bitmapScrollOnLeftDown( self, event ):
        self.panel_pos = self.m_bitmapScroll.ScreenToClient(wx.GetMousePosition())
        self.mousepos = wx.GetMousePosition() # absolute position
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        event.Skip()
        
    def m_bitmapScrollOnLeftUp( self, event ):
        m.bitmapleftup(self,event)   
	# help menu #==============================================================
    def m_richText22OnLeftDown( self, event ):
        p.SwitchPanel(self,2) 
    
    #%% transfer
    def m_txtMyIPOnKeyUp( self, event ):
        self.IP1 = self.m_txtMyIP.GetValue()
        with open(joinpath(self.dirIP,'IPadresses.txt'),'w') as f:
            f.write(json.dumps({'IP1' : self.IP1,'IP2': self.IP2})) 
            f.close()        
    def m_txtTargetIPOnKeyUp( self, event ):
        self.IP2 = self.m_txtTargetIP.GetValue()
        with open(joinpath(self.dirIP,'IPadresses.txt'),'w') as f:
            f.write(json.dumps({'IP1' : self.IP1,'IP2': self.IP2})) 
            f.close()
    def m_buttonTransferOnButtonClick(self,event):
        Client = self.m_radioClient.GetValue()
        if Client:
            HOST = self.IP2
            print(f"HOST IS {HOST}")
            print("start client")
            self.m_txtStatus.SetValue("starting client")
            t_sync = lambda self,mode,HOST :threading.Thread(target=m4.SyncDevices,args=(self,mode,HOST)).start()
            t_sync(self,1,HOST)
            
            
        else:
            HOST = self.IP1
            print(f"HOST IS {HOST}")
            print("start server")
            self.m_txtStatus.SetValue("starting server")
            t_sync = lambda self,mode,HOST :threading.Thread(target=m4.SyncDevices,args=(self,mode,HOST)).start()
            t_sync(self,0,HOST)
            
            
        
    #%% flashcard
    " flashcard "
    # main program
    def m_filePicker21OnFileChanged( self, event ):
        m2.startprogram(self,event)
    
    # button events
    def m_buttonCorrectOnButtonClick( self, event ):        
        m2.buttonCorrect(self)
    def m_bitmapScroll1OnLeftUp( self, event ):
        m2.buttonCorrect(self)
    
    def m_buttonWrongOnButtonClick( self, event ):
        m2.buttonWrong(self)
    def m_bitmapScroll1OnRightUp( self, event ):
        m2.buttonCorrect(self)    
	
    def m_toolSwitch21OnToolClicked( self, event ):
        m2.switchCard(self)
	
    def m_bitmapScroll1OnMouseWheel( self, event ):
        m2.switchCard(self)
        
    #%% print the notes
    def m_sliderPDFsizeOnScrollChanged(self,event):
        self.pdfmultiplier = float(self.m_sliderPDFsize.GetValue())/100
        settings_set(self)
        m3.preview_refresh(self)
    
    def m_lineQAOnCheckBox( self, event ):
        self.FilePickEvent = False
        self.QAline_bool = self.m_lineQA.GetValue()
        settings_set(self)
        m3.preview_refresh(self)
        
    def m_linePDFOnCheckBox( self, event ):
        self.FilePickEvent = False
        self.pdfline_bool = self.m_linePDF.GetValue()
        settings_set(self)
        m3.preview_refresh(self)
    
    def m_colorQAlineOnColourChanged( self, event ):
        self.FilePickEvent = False
        RGB = self.m_colorQAline.GetColour()
        self.QAline_color  = (RGB.Red(),RGB.Green(),RGB.Blue())    
        settings_set(self)
        m3.preview_refresh(self)
        
    def m_colorPDFlineOnColourChanged( self, event ):
        self.FilePickEvent = False
        RGB = self.m_colorPDFline.GetColour()
        self.pdfline_color  = (RGB.Red(),RGB.Green(),RGB.Blue())    
        settings_set(self)
        m3.preview_refresh(self)
        
        
    def m_PrintFinalOnButtonClick( self, event ):
        self.printsuccessful = False
        self.printpreview  = False
        self.FilePickEvent = False
        m3.preview_refresh(self)
        if self.printsuccessful == True:
            self.printpreview = True
            p.SwitchPanel(self,0)
            MessageBox(0, " Your PDF has been created!\n Select in the menubar: `Open/Open PDF-notes Folder` to\n open the folder in Windows explorer. ", "Message", MB_ICONINFORMATION)
    def m_lineWpdfOnText( self, event ):
        try:
            int(self.m_lineWpdf.GetValue())
            
            if int(self.m_lineWpdf.GetValue()) >= 0:
                self.pdfline_thickness = int(self.m_lineWpdf.GetValue())
                settings_set(self)
                m3.preview_refresh(self)
        except:
            print("Error: invalid entry")
    def m_lineWqaOnText( self, event ):
        try:
            int(self.m_lineWqa.GetValue())
            
            if int(self.m_lineWqa.GetValue()) >= 0:
                self.QAline_thickness = int(self.m_lineWqa.GetValue())
                settings_set(self)
                m3.preview_refresh(self)
        except:
            print("Error: invalid entry")
    #%% Help menu
    def m_richText1OnLeftDown(self,event):
        p.SwitchPanel(self,self.lastpage)
    def m_richText2OnLeftDown(self,event):
        p.SwitchPanel(self,self.lastpage)
    def m_richText3OnLeftDown(self,event):
        p.SwitchPanel(self,self.lastpage)
    def m_richText4OnLeftDown(self,event):
        p.SwitchPanel(self,self.lastpage)
    
# start the application
app = wx.App(False) 
frame = MainFrame(None)
frame.Show(True)
app.MainLoop()
del app


