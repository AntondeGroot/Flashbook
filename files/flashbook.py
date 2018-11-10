# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 23:49:47 2018
@author: Anton
"""

try:
    del app
except:
    pass
print("Welcome to Flashbook , one moment ...")
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
import program
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
from print_modules import notes2paper
#--- for colored error messages ------------------------------------- debugging
from termcolor import colored








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
            
#% path to resources: to circumvent needing a spec. file when you use Pyinstaller 
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
    self.path_pr = os.path.join(self.dir7,"print.png")
    self.path_arrow = os.path.join(self.dir7,"arrow.png")
    self.path_arrow2 = os.path.join(self.dir7,"arrow2.png")
#%% settings   
def settings_get(self):

    with open(os.path.join(self.dirsettings,"settings.txt"), 'r') as file:
        settings   = json.load(file)
        debug_var  = settings['debugmode']
        self.pdfmultiplier     = settings['pdfmultiplier'] 
        print(f"settins = {settings}")
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
    self.dirpdf = dir0 + r"\PDF folder"
    self.dirsettings = dir0 + r"\settings"
    self.temp_dir = self.dir4
    self.statsdir = os.path.join(self.dirsettings, 'data_sessions.json')
    
    folders = []
    dirs = [dir0,self.dir1,self.dir2,self.dir3,self.dir4,self.dir5,self.dir6,self.dirpdf,self.dirsettings]
    
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
    for i in range(len(arr)):
        if ('.jpg' not in arr[i]) and ('.png' not in arr[i]):
           #print(arr[i])
           folders.append(arr[i])
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


def settings_create(self):
    if not os.path.exists(self.dirsettings+r"\settings.txt"):   
        with open(self.dirsettings+r"\settings.txt", 'w') as file:
            file.write(json.dumps({'debugmode' : 0,'pdfmultiplier': 1.0, 'QAline_thickness' : 1, 'pdfline_thickness' : 5, 'QAline_color' : (0,0,0), 'pdfline_color' : (18,5,250), 'QAline_bool': True,'pdfline_bool': True }))       
def settings_set(self):
    with open(self.dirsettings+r"\settings.txt", 'w') as file:
        file.write(json.dumps({'debugmode' : 0, 'pdfmultiplier': self.pdfmultiplier,'QAline_thickness' : self.QAline_thickness, 'pdfline_thickness': self.pdfline_thickness, 'QAline_color' : self.QAline_color, 'pdfline_color' : self.pdfline_color, 'QAline_bool': self.QAline_bool,'pdfline_bool': self.pdfline_bool}))       

"""
###############################################################################
#####              MAINFRAME                                              #####
###############################################################################
"""

########################################################################
def SwitchPanel(self,n,m):
    if n == 0:
        self.panel0.Show()
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.Layout() # force refresh of windows
    elif n == 1:
        self.panel0.Hide()
        self.panel1.Show()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        if m == 0:
            self.panel11.Show()
            self.panel12.Hide()
        else:
            self.panel11.Hide()
            self.panel12.Show()
        self.Layout() # force refresh of windows
    elif n == 2:
        self.panel0.Hide()
        self.panel1.Hide()
        self.panel2.Show()
        self.panel3.Hide()
        self.panel4.Hide()
        if m == 0:
            self.panel21.Show()
            self.panel22.Hide()
        else:
            self.panel21.Hide()
            self.panel22.Show()
        self.Layout() # force refresh of windows
    elif n ==3:
        self.panel0.Hide()
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Show()
        self.panel4.Hide()
        self.Layout()
    elif n ==4:
        self.panel0.Hide()
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Show()
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
    
    # stich
    
    image = PIL.Image.open(self.path_arrow, mode='r')
    image = image.resize((32, 32))     
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow2))
    #
    
    
def print_preview(self,event):
    program.run_print(self,event) 
    #resize        
    panelwidth = round(float(self.m_panel32.GetSize()[1])/1754.0*1240.0)
    panelheight = self.m_panel32.GetSize()[1]
    self.allimages_v = self.allimages_v[0].resize((panelwidth, panelheight), PIL.Image.ANTIALIAS)
    
    image2 = wx.Image( self.allimages_v.size)
    image2.SetData( self.allimages_v.tobytes() )
    bitmapimage = wx.Bitmap(image2)
    self.m_bitmap3.SetBitmap(bitmapimage)
    print(self.m_panel32.GetSize())
    self.Layout()
def preview_refresh(self):
    
    notes2paper(self)
    panelwidth = round(float(self.m_panel32.GetSize()[1])/1754.0*1240.0)
    panelheight = self.m_panel32.GetSize()[1]
    self.allimages_v = self.allimages_v[0].resize((panelwidth, panelheight), PIL.Image.ANTIALIAS) 
    image2 = wx.Image( self.allimages_v.size)
    image2.SetData( self.allimages_v.tobytes() )
    bitmapimage = wx.Bitmap(image2)
    self.m_bitmap3.SetBitmap(bitmapimage)
    print(self.m_panel32.GetSize())
    self.Layout()



class MainFrame(gui.MyFrame):
    #constructor    
    def __init__(self,parent):
        
        setup_sources(self)
        
        #initialize parent class
        gui.MyFrame.__init__(self,parent)
        self.Maximize(True) #open the app window maximized
        thr3 = threading.Thread(target = initialize, name = 'threadINI', args = (self, ))
        thr3.run()
        #initialize(self)
        self.stitchmode_v = True
        self.FilePickEvent = True
        
        
        set_bitmapbuttons(self)
        # icon
        iconimage = wx.Icon(self.path_icon, type=wx.BITMAP_TYPE_ANY, desiredWidth=-1, desiredHeight=-1)
        self.SetIcon(iconimage)
        SwitchPanel(self,0,0)
        self.printpreview = True
        #self.m_OpenFlashbook.Bind( self.m_OpenFlashbookOnButtonClick, self.m_btnOpenFlashbookOnButtonClick)
        
        ## short cuts
        #ini.initializeparameters(self)
        
    #%% Panel selection
    def m_OpenFlashbookOnButtonClick( self, event ):
        self.stayonpage = False
        self.stitchmode_v = True # stich vertical or horizontal
        self.m_dirPicker11.SetInitialDirectory(self.dir3)
        self.m_bitmapScroll.SetWindowStyleFlag(False) # at first disable the border of the bitmap, otherwise you get a bordered empty bitmap. Enable the border only when there is a bitmap
        
        setup_sources(self)
        SwitchPanel(self,1,0)      
        m.SetKeyboardShortcuts(self)
        program.run_flashbook(self)
        
    def m_OpenFlashcardOnButtonClick( self, event ):
        SwitchPanel(self,2,0)
        program.run_flashcard(self)
        
    def m_filePickerPrintOnFileChanged( self, event ): 
        self.FilePickEvent = True
        SwitchPanel(self,3,None)
        settings_get(self)
        self.m_colorQAline.SetColour(self.QAline_color)
        self.m_colorPDFline.SetColour(self.pdfline_color)
        self.m_lineWpdf.SetValue(str(self.pdfline_thickness))
        self.m_lineWqa.SetValue(str(self.QAline_thickness))
        self.m_lineQA.SetValue(self.QAline_bool)
        self.m_linePDF.SetValue(self.pdfline_bool)
        print_preview(self,event)
        print(self.image)
        
    def m_OpenPrintOnButtonClick(self,event):
        thr1 = threading.Thread(target = SwitchPanel, name = 'thread1', args = (self,3,None ))
        thr1.run()
        
        with wx.FileDialog(self, "Choose which file to print", wildcard="*.tex",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            fileDialog.SetPath(self.dir1+'\.')
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                SwitchPanel(self,0,0) 
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
                
                thr2 = threading.Thread(target = print_preview, name = 'thread2', args = (self,event ))
                thr2.run()
                #print_preview(self,event)
                print(self.image)
        
        
        
        
    def m_btnPrintNotesOnButtonClick( self, event ):
        print(f"label is {self.m_menu2.GetLabel()}")
        self.printbool = False
        with gui.MyPrintDialog(self,'data') as self.dlg: #use this to set the max range of the slider , add ",data" in the initialization of the dialog window
            self.dlg.ShowModal()
        
            #if self.dlg.m_PrintFinal                
            #self.nr_questions = dlg.m_slider1.GetValue()                        
            #self.chrono = dlg.m_radioChrono.GetValue()
            #self.continueSession = False
            #self.multiplier = dlg.m_textCtrl11.GetValue()
    #%% menu item events
    def m_toolStitchOnButtonClick( self, event ):
        self.stitchmode_v =  not self.stitchmode_v
        if self.stitchmode_v == True:
            self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow2))
        else:
            self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow))
        
        
    
    def m_menuItemFlashbookOnMenuSelection( self, event ):
        self.m_dirPicker11.SetInitialDirectory(self.dir3)
        os.system("explorer {}".format(self.dir3)) 
	
    def m_menuItemBackToMainOnMenuSelection( self, event ):
        SwitchPanel(self,0,0)  
    def m_menuPDFfolderOnMenuSelection( self, event ):
        os.system("explorer {}".format(self.dirpdf)) 
    def m_menuHelpOnMenuSelection( self, event ):
        print("panel 0 is : {}".format(self.panel0.IsShown()))
        if self.panel0.IsShown():
            pass
        if self.panel1.IsShown():
            self.panel11.Hide()
            self.panel12.Show()
            self.Layout()
        if self.panel2.IsShown():
            self.panel21.Hide()
            self.panel22.Show()
            self.Layout()
    #
    def m_richText12OnLeftDown( self, event ):
        SwitchPanel(self,1,0) 
	
    #%% flashbook
    # import screenshot #======================================================
    def m_btnScreenshotOnButtonClick( self, event ):
        import wx
        import win32clipboard
        from win32api import GetSystemMetrics
        from PIL import Image
        
        
        win32clipboard.OpenClipboard()
        print(f"book = {self.bookname}")
        if hasattr(self,"bookname"):
            if self.bookname != '':
                try:
                    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):# Device Independent Bitmap
                        print("PrtScr available")
                        data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                        win32clipboard.CloseClipboard()
                        ### convert bytes to PIL Image
                        try:                            # since I regularly work with 2 monitors: check if the processing makes sense for 2 monitors, else chose 1 monitor.
                            img = Image.frombytes('RGBA', (int(GetSystemMetrics(0))*2, int(GetSystemMetrics(1))), data)
                            # the bytestream from win32 is from a Device Independent Bitmap, i.e.'RGBquad', meaning that it is not RGBA but BGRA coded:
                            b,g,r,a = img.split() 
                            image = Image.merge("RGB", (r, g, b))
                            image = image.rotate(180) # image is otherwise flipped and rotated
                            image = image.transpose(Image.FLIP_LEFT_RIGHT)
                            image.save(os.path.join(self.dir4,"screenshot.png"))
                            ### back to wxBitmap
                            data = image.tobytes()
                            image3 = wx.Bitmap().FromBuffer(GetSystemMetrics(0)*2,GetSystemMetrics(1),data)
                        except:
                            img = Image.frombytes('RGBA', (int(GetSystemMetrics(0)), int(GetSystemMetrics(1))), data)
                            # the bytestream from win32 is from a Device Independent Bitmap, i.e.'RGBquad', meaning that it is not RGBA but BGRA coded:
                            b,g,r,a = img.split() 
                            image = Image.merge("RGB", (r, g, b))
                            image = image.rotate(180) # image is otherwise flipped and rotated
                            image = image.transpose(Image.FLIP_LEFT_RIGHT)
                            image.save(os.path.join(self.dir4,"screenshot.png"))
                            ### back to wxBitmap
                            data = image.tobytes()
                            image3 = wx.Bitmap().FromBuffer(GetSystemMetrics(0),GetSystemMetrics(1),data)
                        self.backupimage = image3
                        self.m_bitmap4.SetBitmap(image3)
                        SwitchPanel(self,4,None)
                        
                    else:
                        ctypes.windll.user32.MessageBoxW(0, "There is no screenshot available\npress PrtScr again", "ErrorMessage", 1)
                except:
                    ctypes.windll.user32.MessageBoxW(0, "There is no screenshot available\npress PrtScr again", "ErrorMessage", 1)
            else:
                ctypes.windll.user32.MessageBoxW(0, "Please open a book first", "ErrorMessage", 1)
        try:
            win32clipboard.CloseClipboard()
        except:
            pass
        
    def m_btnSelectOnButtonClick( self, event ):
        print("undo")
        if hasattr(self,"backupimage"):
            image3 = self.backupimage
            self.m_bitmap4.SetBitmap(image3)
        self.Layout()
    
    def m_btnImportScreenshotOnButtonClick( self, event ):
        self.stayonpage = True
        SwitchPanel(self,1,0)
        
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
	
    def m_CurrentPage11OnKeyUp( self, event ):
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
        SwitchPanel(self,2,0) 
    
    
    
    #%% flashcard
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
        preview_refresh(self)
    
    def m_lineQAOnCheckBox( self, event ):
        self.FilePickEvent = False
        self.QAline_bool = self.m_lineQA.GetValue()
        settings_set(self)
        preview_refresh(self)
        
    def m_linePDFOnCheckBox( self, event ):
        self.FilePickEvent = False
        self.pdfline_bool = self.m_linePDF.GetValue()
        settings_set(self)
        preview_refresh(self)
    
    def m_colorQAlineOnColourChanged( self, event ):
        self.FilePickEvent = False
        RGB = self.m_colorQAline.GetColour()
        self.QAline_color  = (RGB.Red(),RGB.Green(),RGB.Blue())    
        settings_set(self)
        preview_refresh(self)
        
    def m_colorPDFlineOnColourChanged( self, event ):
        self.FilePickEvent = False
        RGB = self.m_colorPDFline.GetColour()
        self.pdfline_color  = (RGB.Red(),RGB.Green(),RGB.Blue())    
        settings_set(self)
        preview_refresh(self)
        
        
    def m_PrintFinalOnButtonClick( self, event ):
        self.printpreview = False
        self.FilePickEvent = False
        preview_refresh(self)
        self.printpreview = True
        SwitchPanel(self,0,0)
        ctypes.windll.user32.MessageBoxW(0, " your pdf has been created\n open in the menubar: `Open/Open PDF-notes Folder` to\n open the folder in Windows explorer ", "Message", 1)
    def m_lineWpdfOnText( self, event ):
        try:
            int(self.m_lineWpdf.GetValue())
            
            if int(self.m_lineWpdf.GetValue()) >= 0:
                self.pdfline_thickness = int(self.m_lineWpdf.GetValue())
                settings_set(self)
                preview_refresh(self)
        except:
            print("Error: invalid entry")
    def m_lineWqaOnText( self, event ):
        try:
            int(self.m_lineWqa.GetValue())
            
            if int(self.m_lineWqa.GetValue()) >= 0:
                self.QAline_thickness = int(self.m_lineWqa.GetValue())
                settings_set(self)
                preview_refresh(self)
        except:
            print("Error: invalid entry")
    
	
	
	
	
	
    
        
# start the application
def runapp():
    app = wx.App(False) 
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
    del app
    
# initialize a thread
thr_main = threading.Thread(target = runapp, name = 'mainthread',args = ())
thr_main.run()


