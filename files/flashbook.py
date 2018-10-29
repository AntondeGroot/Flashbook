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
import fb_modules as m
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
def SwitchPanel(self,n,m):
    if n == 0:
        self.panel0.Show()
        self.panel1.Hide()
        self.panel2.Hide()
        self.Layout() # force refresh of windows
    elif n == 1:
        self.panel0.Hide()
        self.panel1.Show()
        self.panel2.Hide()
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
        if m == 0:
            self.panel21.Show()
            self.panel22.Hide()
        else:
            self.panel21.Hide()
            self.panel22.Show()
        self.Layout() # force refresh of windows
    
    

class MainFrame(gui.MyFrame):
    #constructor    
    def __init__(self,parent):
        setup_sources(self)
        initialize(self)
        #initialize parent class
        gui.MyFrame.__init__(self,parent)
        # icon
        iconimage = wx.Icon(self.path_icon, type=wx.BITMAP_TYPE_ANY, desiredWidth=-1, desiredHeight=-1)
        self.SetIcon(iconimage)
        self.m_dirPicker1.SetInitialDirectory(self.dir3)
        SwitchPanel(self,0,0)
        ## short cuts
        #ini.initializeparameters(self)
        
        #set_richtext(self)
        
        m.SetKeyboardShortcuts(self)
    
    #%% Panel selection
    def m_btnOpenFlashbookOnButtonClick( self, event ):
        setup_sources(self)
        set_richtext(self)
        SwitchPanel(self,1,0)        
        import program
        program.run_flashbook(self)
        
    def m_btnOpenFlashcardOnButtonClick( self, event ):
        SwitchPanel(self,2,0)
        	
    def m_btnPrintNotesOnButtonClick( self, event ):
        event.skip()
    
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
    def m_richText1OnLeftDown( self, event ):
        SwitchPanel(self,1,0) 
	
    #%% flashbook events
	
    def m_dirPicker1OnDirChanged(self,event):
        m.dirchanged(self,event)
    # open Appdata folder in Windows #=========================================
    
	# zoom in #=======================================================
    def m_toolPlusOnToolClicked( self, event ):
        m.zoomout(self,event)
	
    def m_toolMinOnToolClicked( self, event ):
        m.zoomin(self,event)
	
    # change page #=======================================================
    def m_toolBackOnToolClicked( self, event ):
        m.previouspage(self,event)
	
    def m_toolNextOnToolClicked( self, event ):
        m.nextpage(self,event)
	
    def m_PageCtrlOnKeyUp( self, event ):
        m.switchpage(self,event)
    
    def m_bitmapScrollOnMouseWheel( self, event ):
        m.mousewheel(self,event)
        
    # user selections #========================================================
    def m_resetselectionOnButtonClick( self, event ):               
        m.resetselection(self,event)
    
    def m_enterselectionOnButtonClick( self, event ):
        m.selectionentered(self,event)
        
    def m_checkBoxCursorOnCheckBox( self, event ):  
        m.setcursor(self,event)
    
    # show drawn borders 
    def m_checkBox1OnCheckBox( self, event ):
        lf = event.GetEventObject()
        self.drawborders = lf.GetValue()        
        self.pageimage = self.pageimagecopy # reset image
        f.ShowPage(self)
    
	#%%	
        
	# bitmap # DRAW RECTANGLE WITH MOUSE, GET COORDINATES  
    def m_bitmapScrollOnLeftDown( self, event ):
        self.panel_pos = self.m_bitmapScroll.ScreenToClient(wx.GetMousePosition())
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        
    def m_bitmapScrollOnLeftUp( self, event ):
        m.bitmapleftup(self,event)   
	
    
    
    
    #%% flashcard
    def m_richText11OnLeftDown( self, event ):
        SwitchPanel(self,2,0) 
    
    
    
    
    
    
    
    
    def m_bitmapScrollOnMotion( self, event ):
        event.Skip()
	
    def m_bitmapScrollOnMouseEvents( self, event ):
        event.Skip()
	

	
    def m_bitmapScrollOnRightDown( self, event ):
        event.Skip()
	
    
	
	
	
	
	
	
	
	
	
	
	
    
	
    def m_filePickerOnFileChanged( self, event ):
        event.Skip()
	
    def m_toolSwitchOnToolClicked( self, event ):
        event.Skip()
	
	
	
	
	
	
	
	
	
	
	
	
    def m_buttonCorrectOnButtonClick( self, event ):
        event.Skip()
	
    def m_buttonWrongOnButtonClick( self, event ):
        event.Skip()
    
        
# start the application
app = wx.App(False) 
frame = MainFrame(None)
frame.Show(True)
app.MainLoop()
del app