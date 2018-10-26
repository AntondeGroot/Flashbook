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
import flashbook_gui as gui
#------------------------------------------------------------------- modules
import fb_functions as f
import fb_modules as m
import fb_initialization as ini 
import resources


# when using Pyinstaller to get the .exe file: it will standard give an error that it is missing the module 'qwindows.dll'
# since the .exe created by --onefile takes ages to start, i won't be using that option and then module can be found in the folder below
# it is resolved by simply copying the qwindows.dll module next to the .exe file
cwd = os.getcwd()
#print("current cwd {}".format(cwd))
try:
    if os.path.exists(cwd+"\PyQt5\Qt\plugins\platforms\qwindows.dll"):
        shutil.copy2(cwd+"\PyQt5\Qt\plugins\platforms\qwindows.dll",cwd+r'\\') 
        #print("copied qwindows.dll module")
    else:
        print("qwindows.dll module missing")    
except:
    print("no qwindows.dll module found  (#2)")
            
#% path to resources: to circumvent needing a spec. file when you use Pyinstaller 
datadir = os.getenv("LOCALAPPDATA")
dir0 = datadir+r"\FlashBook"
dir7 = dir0 + r"\resources"
path_add = os.path.join(dir7,"add.png")
path_min = os.path.join(dir7,"min.png")
path_repeat = os.path.join(dir7,"repeat.png")
path_repeat_na = os.path.join(dir7,"repeat_na.png")
path_icon = os.path.join(dir7,"open-book1.png")
#  use this to convert images to a string of bytes ... store those bytes in a script, 
#  then use this script to save those images in %appdata%, and then load those images from there
"""  
import base64
with open("add.png", "rb") as imageFile:
    string = base64.b64encode(imageFile.read())
    print(string )
fh = open("imageToSave.png", "wb")
fh.write(base64.b64decode(string))
fh.close()
"""

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
    
    # create settings folder for debugging
    if not os.path.exists(dir0+r"\settings.txt"): 
        with open(dir0+r"\settings.txt", 'w') as file:
            file.write(json.dumps({'debugmode' : 0})) 
    with open(dir0+r"\settings.txt", 'r') as file:
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


"""
###############################################################################
#####              MAINFRAME                                              #####
###############################################################################
"""
class info():
    def __init__(self):
        self.info1 = []



def set_richtext(self):
    self.txt = self.m_richText1
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

    

class MainFrame(gui.MyFrame):
    #constructor    
    def __init__(self,parent):
        initialize(self)
        #initialize parent class
        gui.MyFrame.__init__(self,parent)
        # icon
        iconimage = wx.Icon(path_icon, type=wx.BITMAP_TYPE_ANY, desiredWidth=-1, desiredHeight=-1)
        self.SetIcon(iconimage)
        ## short cuts
        ini.initializeparameters(self)
        self.panel2.Hide()
        set_richtext(self)
        
        m.SetKeyboardShortcuts(self)
    
        
    # zoom in #=======================================================
    def m_toolPlusOnToolClicked( self, event ):
        m.zoomout(self,event)
        
    # zoom out #=======================================================
    def m_toolMinOnToolClicked( self, event ):
        m.zoomin(self,event)
        
    # show drawn borders #=====================================================
    def m_checkBox1OnCheckBox( self, event ):
        lf = event.GetEventObject()
        self.drawborders = lf.GetValue()        
        self.pageimage = self.pageimagecopy # reset image
        f.ShowPage(self)

    #pop up window
    def onShowPopup(self, event):
        win = f.Window2(self.GetTopLevelParent(), wx.SIMPLE_BORDER)
        btn = event.GetEventObject()
        pos = self.panel_pos
        sz =  btn.GetSize()
        win.Position(pos, (0, sz[1]))
        win.Show(True)  
    
    # scrolling through pdf #===================================================
    def m_bitmapScrollOnMouseWheel(self,event):
        m.mousewheel(self,event)
    
    # page backwards #=======================================================
    def m_toolBackOnToolClicked( self, event ):
        m.previouspage(self,event)
        
    # page forwards #========================================================
    def m_toolNextOnToolClicked( self, event ):  
        m.nextpage(self,event)
            
    # open Appdata folder in Windows #=========================================
    def m_menuItemFlashbookOnMenuSelection( self, event ):
        os.system("explorer {}".format(self.dir3)) 

    # reset selections #=======================================================
    def m_resetselectionOnButtonClick( self, event ):               
        m.resetselection(self,event)
    
    # confirm user selections #================================================
    def m_enterselectionOnButtonClick( self, event ):
        m.selectionentered(self,event)
        
    # switch page by button ===================================================
    def m_PageCtrlOnKeyUp( self, event ):
        m.switchpage(self,event)
        
    def m_checkBoxCursorOnCheckBox( self, event ):  
        m.setcursor(self,event)
            
    # DRAW RECTANGLE WITH MOUSE, GET COORDINATES        
    def m_bitmapScrollOnLeftDown( self, event ):
        self.panel_pos = self.m_bitmapScroll.ScreenToClient(wx.GetMousePosition())
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        
    def m_bitmapScrollOnLeftUp( self,event):
        m.bitmapleftup(self,event)       
    
    # switch between the two panels
    def m_menuHelpOnMenuSelection( self, event ):        
        self.panel2.Show()
        self.panel1.Hide()
        self.Layout()
    def m_richText1OnLeftDown( self, event ):
        self.panel1.Show()
        self.panel2.Hide()
        self.Layout()
        
    ## LOAD ALL DATA ==========================================================
    def m_dirPicker1OnDirChanged(self,event):
        m.dirchanged(self,event)
        
# start the application
app = wx.App(False) 
frame = MainFrame(None)
frame.Show(True)
app.MainLoop()
del app
