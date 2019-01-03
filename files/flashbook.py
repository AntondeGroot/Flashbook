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
import ctypes # pop up messages
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
# when using Pyinstaller to get the .exe file: it will standard give an error that it is missing the module 'qwindows.dll'
# since the .exe created by --onefile takes ages to start, i won't be using that option and then module can be found in the folder below
# it is resolved by simply copying the qwindows.dll module next to the .exe file
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
    self.datadir = os.getenv("LOCALAPPDATA")
    self.dir0 = self.datadir+r"\FlashBook"
    self.dir7 = self.dir0 + r"\resources"
    self.path_add = os.path.join(self.dir7,"add.png")
    self.path_min = os.path.join(self.dir7,"min.png")
    self.path_repeat = os.path.join(self.dir7,"repeat.png")
    self.path_repeat_na = os.path.join(self.dir7,"repeat_na.png")
    self.path_icon = os.path.join(self.dir7,"open-book1.png")
    self.path_fb = os.path.join(self.dir7,"flashbook.png")
    self.path_fc = os.path.join(self.dir7,"flashcard.png")
    self.path_wifi = os.path.join(self.dir7,"wifi.png")
    self.path_pr = os.path.join(self.dir7,"print.png")
    self.path_arrow = os.path.join(self.dir7,"arrow.png")
    self.path_arrow2 = os.path.join(self.dir7,"arrow2.png")
#%% settings   
def settings_get(self):

    with open(os.path.join(self.dirsettings,"settings.txt"), 'r') as file:
        settings   = json.load(file)
        debug_var  = settings['debugmode']
        self.pdfmultiplier     = settings['pdfmultiplier'] 
        #print(f"settings = {settings}")
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
            
def settings_set(self):
    with open(self.dirsettings+r"\settings.txt", 'w') as file:
        file.write(json.dumps({'debugmode' : 0, 'pdfmultiplier': self.pdfmultiplier,'QAline_thickness' : self.QAline_thickness, 'pdfline_thickness': self.pdfline_thickness, 
                               'QAline_color' : self.QAline_color, 'pdfline_color' : self.pdfline_color, 'QAline_bool': self.QAline_bool,'pdfline_bool': self.pdfline_bool}))           

#%%
def initialize(self):
    datadir = os.getenv("LOCALAPPDATA")
    dir0 = datadir+r"\FlashBook"
    self.dir0 = dir0
    self.dir1 = dir0 + r"\files"
    self.dir2 = dir0 + r"\pics"
    self.dir3 = dir0 + r"\books"
    self.dir4 = dir0 + r"\temporary"
    self.dir5 = dir0 + r"\borders"
    self.dir6 = dir0 + r"\resources"
    self.dirIP = dir0 + r"\IPadresses"
    self.dirpdf = dir0 + r"\PDF folder"
    self.dirsettings = dir0 + r"\settings"
    self.temp_dir = self.dir4
    self.statsdir = os.path.join(self.dirsettings, 'data_sessions.json')
    
    folders = []
    dirs = [dir0,self.dir1,self.dir2,self.dir3,self.dir4,self.dir5,self.dir6,self.dirpdf,self.dirsettings,self.dirIP]
    try:
        if not os.path.exists(os.path.join(self.dirIP,'IPadresses.txt')):
            
            
    
            wmi_obj = wmi.WMI()
            wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled = True"
            wmi_out = wmi_obj.query(wmi_sql)[0] #only 1 query
            
            
            myIP = wmi_out.IPAddress[0]
            
           
            with open(os.path.join(self.dirIP,'IPadresses.txt'),'w') as f:
                f.write(json.dumps({'IP1' : myIP,'IP2': ""})) 
                f.close()
    except:
        print("Error: could not access internet?")
    print("=========================================================================================")
    print("\nThe files will be saved to the following directory: {}\n".format(dir0))
    for item in dirs:
        if not os.path.exists(item):
            os.makedirs(item)
    # create settings folder for debugging
    settings_create(self)
    settings_get(self)
     
    # unpacks png images used in the gui
    resources.resourceimages(self.dir6,self.dir1) 
    #%%
    
    arr = os.listdir(self.dir3)
    for filename in arr:
        if ('.jpg' not in filename) and ('.png' not in filename):
           folders.append(filename)
    self.nr_books = len(folders)
    folders.sort() 
    
    if len(folders) == 0:
        ctypes.windll.user32.MessageBoxW(0, f"Welcome new user \n\nNo books were found in directory {self.dir3} \nGo to the menubar of the app:  `Open/Flashbook folder`\nPLace a new folder there named after a book containing jpg files", "Welcome to Flashbook", 1)
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

class MainFrame(gui.MyFrame):
    #constructor    
    def __init__(self,parent): 
        initialize(self)
        setup_sources(self)
        
        #initialize parent class
        gui.MyFrame.__init__(self,parent,None) #added superfluous argument, so that WXpython.py can easily add the Dialog Windows (which require an extra argument)         
        m.set_richtext(self)  # text for help
        m2.set_richtext2(self) # text for help     
        self.Maximize(True) # open the app window maximized
        thr3 = threading.Thread(target = initialize, name = 'threadINI', args = (self, ))
        thr3.run()
        
        self.stitchmode_v = True
        self.FilePickEvent = True 
        p.set_bitmapbuttons(self)
        # icon
        iconimage = wx.Icon(self.path_icon, type=wx.BITMAP_TYPE_ANY, desiredWidth=-1, desiredHeight=-1)
        self.SetIcon(iconimage)
        p.SwitchPanel(self,0,0)
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
        p.SwitchPanel(self,1,0)      
        m.SetKeyboardShortcuts(self)
        p.run_flashbook(self)
        
    def m_OpenFlashcardOnButtonClick( self, event ):
        p.SwitchPanel(self,2,0)
        p.run_flashcard(self)
    def m_OpenTransferOnButtonClick(self,event):
        p.SwitchPanel(self,5,0)
        p.get_IP(self,event)
        #client = self.m_radioClient.GetValue() #boolean
        #p.run_transfer(self,event,client)
        m4.set_richtext(self)
        m4.initialize(self,event)
        
    def m_OpenPrintOnButtonClick(self,event):
        thr1 = threading.Thread(target = p.SwitchPanel, name = 'thread1', args = (self,3,None ))
        thr1.run()
        with wx.FileDialog(self, "Choose which file to print", wildcard="*.tex",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            fileDialog.SetPath(self.dir1+'\.')
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                p.SwitchPanel(self,0,0) 
                return     # the user changed their mind
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
                thr2 = threading.Thread(target = m3.print_preview, name = 'thread2', args = (self,event ))
                thr2.run()
                print(self.image)
                
    #%% menu item events
    " menu item events "
    def m_toolStitchOnButtonClick( self, event ):
        self.stitchmode_v =  not self.stitchmode_v
        if self.stitchmode_v == True:
            self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow2))
        else:
            self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow))
        
        # the following is used to create a mozaic of pictures. There is a question mode and an answer mode
        # the pics are stored in a list, and when the element of a list is another list it means that particular list is ment to be stitched horizontally
        # while all the other elements are stitched vertically
        # all it does is switch [a,...,[x]] for [a,...,x] and back to [a,...,[x]] depending on whether the user has pushed a button to change the direction in which the notes should be stitched together.  
        
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
        self.m_dirPicker11.SetInitialDirectory(self.dir3)
        os.system("explorer {}".format(self.dir3)) 
	
    def m_menuItemBackToMainOnMenuSelection( self, event ):
        p.SwitchPanel(self,0,0)  
        
    def m_menuPDFfolderOnMenuSelection( self, event ):
        os.system("explorer {}".format(self.dirpdf)) 
    def m_menuHelpOnMenuSelection( self, event ):
        print("panel 0 is : {}".format(self.panel0.IsShown()))
        if self.panel0.IsShown():
            pass
        if self.panel1.IsShown():
            p.SwitchPanel(self,1,1) 
        if self.panel2.IsShown():
            p.SwitchPanel(self,2,1) 
        if self.panel5.IsShown():
            p.SwitchPanel(self,5,1) 
            
    def m_richText12OnLeftDown( self, event ):
        p.SwitchPanel(self,1,0) 
    def m_txtHelpSyncOnLeftDown(self,event):
        p.SwitchPanel(self,5,0) 
    #%% flashbook
    " flashbook "
    # import screenshot #
    def m_btnScreenshotOnButtonClick( self, event ):
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
        p.SwitchPanel(self,1,0)
        
    def m_bitmap4OnLeftDown( self, event ):
        self.panel4_pos = self.m_bitmap4.ScreenToClient(wx.GetMousePosition())
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        
    def m_bitmap4OnLeftUp( self, event ):
        m.panel4_bitmapleftup(self,event)   
        self.panel4.Layout()
        self.Update()
        self.Refresh()
        
    def m_dirPicker11OnDirChanged(self,event):
        self.m_bitmapScroll.SetWindowStyleFlag(wx.SIMPLE_BORDER)
        m.dirchanged(self,event)
        self.m_dirPicker11.SetPath(self.dir3)
        
    
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
        lf = event.GetEventObject()
        self.drawborders = lf.GetValue()        
        self.pageimage = self.pageimagecopy # reset image
        f.ShowPage(self)
        
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
        p.SwitchPanel(self,2,0) 
    
    #%% transfer
    def m_txtMyIPOnKeyUp( self, event ):
        self.IP1 = self.m_txtMyIP.GetValue()
        with open(os.path.join(self.dirIP,'IPadresses.txt'),'w') as f:
            f.write(json.dumps({'IP1' : self.IP1,'IP2': self.IP2})) 
            f.close()        
    def m_txtTargetIPOnKeyUp( self, event ):
        self.IP2 = self.m_txtTargetIP.GetValue()
        with open(os.path.join(self.dirIP,'IPadresses.txt'),'w') as f:
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
    def m_bitmapScroll1OnRightUp( self, event ):# anton , dit nog over kopieren van wxformbiulder
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
        self.printpreview = False
        self.FilePickEvent = False
        m3.preview_refresh(self)
        if self.printsuccessful == True:
            self.printpreview = True
            p.SwitchPanel(self,0,0)
            ctypes.windll.user32.MessageBoxW(0, " your pdf has been created\n open in the menubar: `Open/Open PDF-notes Folder` to\n open the folder in Windows explorer ", "Message", 1)
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
        
# start the application
app = wx.App(False) 
frame = MainFrame(None)
frame.Show(True)
app.MainLoop()
del app


