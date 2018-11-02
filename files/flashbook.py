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
#-------------------------------------------------------------------- gui
import wx
import wx.adv as adv
import wx.richtext
import wx.html as html
import gui_flashbook as gui
#------------------------------------------------------------------- modules
import fb_initialization as ini 
import resources
import fb_functions as f


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

#%% settings   
def settings_get(self):

    with open(self.dir0+r"\settings.txt", 'r') as file:
        settings   = json.load(file)
        debug_var  = settings['debugmode']
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
    if not os.path.exists(self.dir0+r"\settings.txt"):   
        with open(self.dir0+r"\settings.txt", 'w') as file:
            file.write(json.dumps({'debugmode' : 0, 'QAline_thickness' : 1, 'pdfline_thickness' : 5, 'QAline_color' : (0,0,0), 'pdfline_color' : (18,5,250), 'QAline_bool': True,'pdfline_bool': True }))       
def settings_set(self):
    with open(self.dir0+r"\settings.txt", 'w') as file:
        file.write(json.dumps({'debugmode' : 0, 'QAline_thickness' : self.QAline_thickness, 'pdfline_thickness': self.pdfline_thickness, 'QAline_color' : self.QAline_color, 'pdfline_color' : self.pdfline_color, 'QAline_bool': self.QAline_bool,'pdfline_bool': self.pdfline_bool}))       
#%%
def initialize(self):
    datadir = os.getenv("LOCALAPPDATA")
    dir0 = datadir+r"\FlashBook"
    #os.chdir(dir0)
    self.dir0 = dir0
    self.dir1 = dir0 + r"\files"
    self.dir2 = dir0 + r"\pics"
    self.dir3 = dir0 + r"\books"
    self.dir4 = dir0 + r"\temporary"
    self.dir5 = dir0 + r"\borders"
    self.dir6 = dir0 + r"\resources"
    self.dir7 = dir0 + r"\pdfs of notes"
    self.temp_dir = self.dir4
    
    # create settings folder for debugging
    settings_create(self)
    settings_get(self)
                
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


class info():
    def __init__(self):
        self.info1 = []




########################################################################
def SwitchPanel(self,n,m):
    if n == 0:
        self.panel0.Show()
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.Layout() # force refresh of windows
    elif n == 1:
        self.panel0.Hide()
        self.panel1.Show()
        self.panel2.Hide()
        self.panel3.Hide()
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
        self.Layout()

import fb_modules as m
import fc_modules as m2

#import fc_modules as m2  

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
    from print_modules import notes2paper
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

import program
import PIL

class MainFrame(gui.MyFrame):
    #constructor    
    def __init__(self,parent):
        self.FilePickEvent = True
        setup_sources(self)
        
        initialize(self)
        #initialize parent class
        gui.MyFrame.__init__(self,parent)
        set_bitmapbuttons(self)
        self.Maximize(True)
        #self.TransferDataToWindow
        # icon
        iconimage = wx.Icon(self.path_icon, type=wx.BITMAP_TYPE_ANY, desiredWidth=-1, desiredHeight=-1)
        self.SetIcon(iconimage)
        self.m_dirPicker11.SetInitialDirectory(self.dir3)
        #self.m_filePickerPrint.SetInitialDirectory(self.dir1+'\.') #for filepicker you can't just set a directory like dirPicker, in this case it should end in "\." so that it has to look for files, otherwise it will see a folder as a file...
        SwitchPanel(self,0,0)
        self.printpreview = True
        #self.m_OpenFlashbook.Bind( self.m_OpenFlashbookOnButtonClick, self.m_btnOpenFlashbookOnButtonClick)
        
        ## short cuts
        #ini.initializeparameters(self)
        #self.m_filePickerPrint.Bind( wx.EVT_FILEPICKER_CHANGED, self.m_btnPrintNotesOnButtonClick )
        #self.m_filePickerPrint.Bind(wx.EVT_BUTTON,self.m_btnPrintNotesOnButtonClick)
        #self.m_OpenPrint.Bind(wx.EVT_BUTTON,self.m_filePickerPrintOnKeyDown)
        #self.Bind(wx.EVT_BUTTON, self.m_filePickerPrintOnButtonClick, self.m_OpenPrint)
        
    #%% Panel selection
    def m_OpenFlashbookOnButtonClick( self, event ):
        self.m_bitmapScroll.SetWindowStyleFlag(False)
        self.m_dirPicker11.SetInitialDirectory(self.dir3)
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
        with wx.FileDialog(self, "Choose which file to print", wildcard="*.tex",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            fileDialog.SetPath(self.dir1+'\.')
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
            else:
                self.fileDialog = fileDialog
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
    def m_menuItemFlashbookOnMenuSelection( self, event ):
        os.system("explorer {}".format(self.dir3)) 
	
    def m_menuItemBackToMainOnMenuSelection( self, event ):
        SwitchPanel(self,0,0)  
	
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
	
    #% flashbook events
	
    def m_dirPicker11OnDirChanged(self,event):
        self.m_bitmapScroll.SetWindowStyleFlag(wx.SIMPLE_BORDER)
        m.dirchanged(self,event)
        
    # open Appdata folder in Windows #=========================================
    
	# zoom in #=======================================================
    def m_toolPlus11OnToolClicked( self, event ):
        m.zoomin(self,event)
	
    def m_toolMin11OnToolClicked( self, event ):
        m.zoomout(self,event)
	
    # change page #=======================================================
    def m_toolBack11OnToolClicked( self, event ):
        m.previouspage(self,event)
	
    def m_toolNext11OnToolClicked( self, event ):
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
    
	#%
        
	# bitmap # DRAW RECTANGLE WITH MOUSE, GET COORDINATES  
    def m_bitmapScrollOnLeftDown( self, event ):
        self.panel_pos = self.m_bitmapScroll.ScreenToClient(wx.GetMousePosition())
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        
    def m_bitmapScrollOnLeftUp( self, event ):
        m.bitmapleftup(self,event)   
	
    def m_richText22OnLeftDown( self, event ):
        SwitchPanel(self,2,0) 
    
    
    #%% flashcard
    def m_filePicker21OnFileChanged( self, event ):
        m2.startprogram(self,event)
    
    
    #buttons
    def m_buttonCorrectOnButtonClick( self, event ):
        import fc_modules as m2
        m2.buttonCorrect(self)
    def m_bitmapScroll1OnLeftUp( self, event ):
        import fc_modules as m2
        m2.buttonCorrect(self)
    
    def m_buttonWrongOnButtonClick( self, event ):
        m2.buttonWrong(self)
    def m_bitmapScroll1OnRightUp( self, event ):# anton , dit nog over kopieren van wxformbiulder
        import fc_modules as m2
        m2.buttonCorrect(self)    
	
    def m_toolSwitch21OnToolClicked( self, event ):
        m2.switchCard(self)
	
    def m_bitmapScroll1OnMouseWheel( self, event ):
        m2.switchCard(self)
    #%% print the notes
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
app = wx.App(False) 
frame = MainFrame(None)
frame.Show(True)
app.MainLoop()
del app
