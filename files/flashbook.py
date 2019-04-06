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
from pathlib import Path
import PIL
import shutil
import subprocess 
import sys
import time
import threading
import wx
import wx.adv as adv
import wx.richtext
import wx.html as html
import wx._html
import platform
_platform = platform.system()
if _platform == 'Windows':
    import ctypes # pop up messages
    import wmi            # for IPaddress: WindowsManagementInstrumentation
    import win32clipboard #
    from win32api import GetSystemMetrics    
    
#------------------------------------------------------------------- modules
import gui_flashbook as gui
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
import timingmodule  as m6
import accelerators_module as m7
import historygraph
import log_module    as log
import fb_functions    as f
import fc_functions    as f2
import print_functions as f3

import random
import itertools

import math
import pylab
pylab.ioff() # make sure it is inactive, otherwise possible qwindows error    .... https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

sys.setrecursionlimit(5000)
PIL.Image.MAX_IMAGE_PIXELS = 1000000000  
#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100
"""when using Pyinstaller to create the .exe file: it will standardly give an error that it is missing the module 'qwindows.dll'
since the .exe created by --onefile takes ages to start, i won't be using that option and then module can be found in the folder below
it is resolved by simply copying the qwindows.dll module next to the .exe file"""

try:
    cwd = Path.cwd()
    dllfile= Path(cwd,"\PyQt5\Qt\plugins\platforms\qwindows.dll")
    
    if dllfile.exists():
        shutil.copy2(dllfile,cwd+r'\\') 
    else:
        print("qwindows.dll module missing")    
except:
    print("no qwindows.dll module found  (#2)")
            
def SaveTime(self):
    if hasattr(self,'TC') and hasattr(self,'bookname') and self.bookname != '':
        self.TC.update()       
def BoxesChecked(self,n):
    CHECKED1 = self.m_checkBox_col1.IsChecked()
    CHECKED2 = self.m_checkBox_col2.IsChecked()
    CHECKED3 = self.m_checkBox_col3.IsChecked()
    if n == 1:
        return CHECKED1
    elif n == 2:
        return CHECKED2
    elif n == 3:
        return CHECKED3
    else:
        log.ERRORMESSAGE("Error: invalid entry in BoxesChecked")
        return False
def CombineBookTitles(booknames):
    """To combine multiple book titles, since this would otherwise end up in a very long
    name, it will instead only take the first full name and then abbreviate the following
    books to only the first letters of the books."""
    C = '_MULTI_'
    for i,string in enumerate(booknames):
        if i==0:
            C += string
        else:
            C += '_'+ ''.join([c for c in string.title() if c.isupper()])
    return C
    
#% path to resources: 
def setup_sources(self):
    if _platform == 'Windows':
        bdir = Path(os.getenv("LOCALAPPDATA"),"Flashbook")
    elif _platform == 'Linux':
        pass
    rdir = Path(bdir,"resources")
    self.appdir         = bdir
    self.path_add     = Path(rdir,"add.png")
    self.path_min     = Path(rdir,"min.png")
    self.path_icon    = Path(rdir,"open-book1.png")
    self.path_fb      = Path(rdir,"flashbook.png")
    self.path_fc      = Path(rdir,"flashcard.png")
    self.path_wifi    = Path(rdir,"wifi.png")
    self.path_pr      = Path(rdir,"print.png")
    self.path_arrow   = Path(rdir,"arrow.png")
    self.path_arrow2  = Path(rdir,"arrow2.png")
    self.path_convert = Path(rdir,"convert.png")
    self.path_folder  = Path(rdir,"folder.png")
    self.path_repeat  = Path(rdir,"repeat.png")
    self.path_repeat_na = Path(rdir,"repeat_na.png")
#%% settings   
def settings_get(self):
    try:
        with open(Path(self.dirsettings,"settings.txt"), 'r') as file:
            settings = json.load(file)
            self.debugmode          = settings['debugmode']
            self.pdfmultiplier      = settings['pdfmultiplier'] 
            self.QAline_thickness   = settings['QAline_thickness']
            self.pdfline_thickness  = settings['pdfline_thickness']
            self.vertline_thickness = settings['vertline_thickness']
            self.QAline_color       = tuple(settings['QAline_color'])
            self.pdfline_color      = tuple(settings['pdfline_color']) 
            self.vertline_color     = tuple(settings['vertline_color'])
            self.QAline_bool        = settings['QAline_bool']
            self.pdfline_bool       = settings['pdfline_bool']
            self.vertline_bool      = settings['vertline_bool']
            self.samecolor_bool     = settings['samecolor_bool']
            self.pdfPageColsPos     = settings['pdfPageColsPos']
            self.pdfPageColsChecks  = settings['pdfPageColsChecks']
            self.LaTeXfontsize      = settings['LaTeXfontsize']
            self.bordercolors       = settings['bordercolors']
            self.drawborders        = settings['drawborders']
            self.cursor             = settings['cursor']
            self.GraphNdays         = settings['GraphNdays']
            self.Graph_bool         = settings['Graph_bool']
            self.NrCardsPreview     = settings['NrCardsPreview']
        file.close()
    except:
        # Just in case when the settings.txt has been tempered with        
        settingsfile = Path(self.dirsettings,"settings.txt")
        if settingsfile.exists():
            settingsfile.unlink()
        settings_create(self)
        settings_get(self)
           
def settings_create(self):
    settingsfile = Path(self.dirsettings,"settings.txt")
    if not settingsfile.exists():   
        with settingsfile.open(mode='w') as file:
            file.write(json.dumps({'debugmode' : False,
                                   'pdfmultiplier': 1.0, 
                                   'QAline_thickness' : 1, 
                                   'pdfline_thickness' : 5,
                                   'vertline_thickness': 5,
                                   'QAline_color' : (0,0,0), 
                                   'pdfline_color' : (18,5,250),
                                   'vertline_color' : (255,128,0),
                                   'QAline_bool': True,
                                   'pdfline_bool': True ,
                                   'vertline_bool': True,
                                   'samecolor_bool': False,
                                   'pdfPageColsPos' : [30 , 46 , 75],
                                   'pdfPageColsChecks' : [True, True, False],
                                   'LaTeXfontsize' : 20,
                                   'bordercolors' : [[0,0,0],[200,0,0]],
                                   'drawborders' : True,
                                   'cursor' : False,
                                   'GraphNdays':10,
                                   'Graph_bool': True,
                                   'NrCardsPreview':15}))
            file.close()
            
def settings_set(self):
    settingsfile = Path(self.dirsettings,"settings.txt")
    with settingsfile.open(mode='w') as file:
        file.write(json.dumps({'debugmode' : self.debugmode, 
                               'pdfmultiplier': self.pdfmultiplier,
                               'QAline_thickness' : self.QAline_thickness, 
                               'pdfline_thickness': self.pdfline_thickness, 
                               'vertline_thickness': self.vertline_thickness,
                               'QAline_color' : self.QAline_color, 
                               'pdfline_color' : self.pdfline_color,
                               'vertline_color' : self.vertline_color,
                               'QAline_bool': self.QAline_bool,
                               'pdfline_bool': self.pdfline_bool,
                               'vertline_bool': self.vertline_bool,
                               'samecolor_bool': self.samecolor_bool,
                               'pdfPageColsPos' : self.pdfPageColsPos,
                               'pdfPageColsChecks': self.pdfPageColsChecks,
                               'LaTeXfontsize' : self.LaTeXfontsize,
                               'bordercolors' : self.bordercolors,
                               'drawborders' : self.drawborders,
                               'cursor' : self.cursor,
                               'GraphNdays' :self.GraphNdays,
                               'Graph_bool': self.Graph_bool,
                               'NrCardsPreview': self.NrCardsPreview}))
        file.close()

def settings_reset(self):
    settingsfile = Path(self.dirsettings,"settings.txt")
    if settingsfile.exists():
        settingsfile.unlink()
    settings_create(self)
    settings_get(self)
    self.m_checkBox11.Check(self.drawborders)
    if self.panel3.IsShown():
        self.m_colorQAline.SetColour(self.QAline_color)
        self.m_colorPDFline.SetColour(self.pdfline_color)
        self.m_colorVERTline.SetColour(self.vertline_color)
        
        self.m_lineWpdf.SetValue(str(self.pdfline_thickness))
        self.m_lineWqa.SetValue(str(self.QAline_thickness))
        self.m_lineWvert.SetValue(str(self.vertline_thickness))
        
        self.m_lineQA.SetValue(self.QAline_bool)
        self.m_linePDF.SetValue(self.pdfline_bool)            
        self.m_lineVERT.SetValue(self.vertline_bool)
        self.m_checkBoxSameColor.SetValue(self.samecolor_bool)
        
        self.m_sliderPDFsize.SetValue(int(200-self.pdfmultiplier*100))
        self.m_slider_col1.SetValue(self.pdfPageColsPos[0])
        self.m_slider_col2.SetValue(self.pdfPageColsPos[1])
        self.m_slider_col3.SetValue(self.pdfPageColsPos[2])
        self.m_checkBox_col1.SetValue(self.pdfPageColsChecks[0])
        self.m_checkBox_col2.SetValue(self.pdfPageColsChecks[1])
        self.m_checkBox_col3.SetValue(self.pdfPageColsChecks[2])
    
#%%
def initialize(self):
    datadir = os.getenv("LOCALAPPDATA")
    app = Path(datadir,"Flashbook")
    self.appdir = app
    self.notesdir = Path(app,"files")
    self.picsdir = Path(app,"pics")
    self.booksdir = Path(app,"books")
    self.tempdir = Path(app,"temporary")
    self.bordersdir = Path(app,"borders")
    self.resourcedir = Path(app,"resources")
    self.dirIP = Path(app,"IPadresses")
    self.dirpdf = Path(app,"PDF folder")
    self.dirpdfbook = Path(app,"PDF books")
    self.dirsettings = Path(app,"settings")
    self.statsdir = Path(self.dirsettings, 'data_sessions.json')
    
    dirs = [self.appdir, self.notesdir, self.picsdir, self.booksdir, self.tempdir, self.bordersdir, self.resourcedir, self.dirpdf, self.dirsettings, self.dirIP, self.dirpdfbook]
    try:
        if not Path(self.dirIP,'IPadresses.txt').exists():          
            wmi_obj = wmi.WMI()
            wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled = True"
            wmi_out = wmi_obj.query(wmi_sql)[0] #only 1 query           
            myIP = wmi_out.IPAddress[0]          
           
            with open(Path(self.dirIP,'IPadresses.txt'),'w') as f:
                f.write(json.dumps({'IP1' : myIP,'IP2': ""})) 
                f.close()
    except:
        log.ERRORMESSAGE("Error: could not access internet")
        
    print("="*90)
    print(f"\nThe files will be saved to the following directory: {self.appdir}\n")
    for item in dirs:
        if not item.exists:
            item.mkdirs()
    # create settings folder for debugging
    settings_create(self)
    settings_get(self)
    #unpack png images used in the gui
    resources.resourceimages(self.resourcedir,self.notesdir) 
    
def save2latexfile(self,files,title):
    
    LISTOFLIST = (type(files[0])==list)
    filepath = Path(self.notesdir,title+'.tex')
    if filepath.exists():
        filepath.unlink()
    if LISTOFLIST:#list of lists of data
        for i,data in enumerate(files):
            with open(filepath,'a') as f:
                if type(data) == list:
                    for line in data:
                        f.write(line)
                f.close()  
    else:
        data = files
        print(f"data = {data[0:20]}")
        with open(filepath,'a') as f:
            if type(data) == list:
                for line in data:
                    print(f"line = {line}")
                    f.write(line)
            f.close()  
        
    
"""
###############################################################################
#####              MAINFRAME                                              #####
###############################################################################
"""

class MainFrame(gui.MyFrame):
    
    """ INITIALIZE """
    def __init__(self,parent): 
        initialize(self)
        
        
        setup_sources(self)
        
        #initialize parent class
        icons = [wx.Bitmap(str(self.path_folder)) , wx.Bitmap(str(self.path_convert)) ]
        gui.MyFrame.__init__(self,parent,icons) #added extra argument, so that WXpython.py can easily add the Dialog Windows (which require an extra argument), which is now used to add extra icons to the menubar             
        settings_get(self)
        settings_set(self)
        #settings_set(self)
        self.m_menubar1.EnableTop(2, False)#disable Flashcard menu
        self.Maximize(True) # open the app window maximized
        t_books = lambda self,delay : threading.Thread(target = p.checkBooks , args=(self,delay )).start()
        t_books(self, 2) 
        
        self.stitchmode_v = True
        self.FilePickEvent = True 
        p.set_bitmapbuttons(self)
        p.set_richtext(self)
        # icon
        iconimage = wx.Icon(str(self.path_icon), type=wx.BITMAP_TYPE_ANY, desiredWidth=-1, desiredHeight=-1)
        self.SetIcon(iconimage)
        p.SwitchPanel(self,0)
        self.printpreview = True
        
        self.m_checkBox11.Check(self.drawborders)
        self.m_checkBoxCursor11.Check(self.cursor)
        self.m_checkBoxDebug.Check(self.debugmode)
        
        m.setcursor(self)
        m7.AcceleratorTableSetup(self,"general","set")
    #%% MAIN PROGRAMS
    """ MAIN PROGRAMS """ 
    
    def m_OpenFlashbookOnButtonClick( self, event ):
        """START MAIN PROGRAM : FLASHBOOK"""
        self.stayonpage = False
        self.stitchmode_v = True # stich vertical or horizontal
        self.m_dirPicker11.SetInitialDirectory(str(self.booksdir))
        self.m_dirPicker11.SetPath(str(self.booksdir))
        self.m_bitmapScroll.SetWindowStyleFlag(False)  # first disable the border of the bitmap, otherwise you get a bordered empty bitmap. Enable the border only when there is a bitmap
        setup_sources(self)
        p.SwitchPanel(self,1)      
        m7.AcceleratorTableSetup(self,"flashbook","set")
        p.run_flashbook(self)
        
        
    def m_OpenFlashcardOnButtonClick( self, event ):
        """START MAIN PROGRAM : FLASCARD"""
        
        m7.AcceleratorTableSetup(self,"flashcard","set")
        p.SwitchPanel(self,2)
        p.run_flashcard(self)
        
        
    def m_OpenTransferOnButtonClick(self,event):
        """START MAIN PROGRAM : WIFI SYNC"""
        p.SwitchPanel(self,5)
        p.get_IP(self,event)
        m4.initialize(self,event)
        
    def m_OpenPrintOnButtonClick(self,event):
        """START MAIN PROGRAM : PRINT PDF NOTES"""
        t_panel = lambda self,page : threading.Thread(target = p.SwitchPanel , args=(self,page )).start()
        t_panel(self, 3) 
        settings_get(self)                
        self.m_CtrlNrCards.SetValue(str(self.NrCardsPreview))
        
        self.m_colorQAline.SetColour(self.QAline_color)
        self.m_colorPDFline.SetColour(self.pdfline_color)
        self.m_colorVERTline.SetColour(self.vertline_color)
        
        self.m_lineWpdf.SetValue(str(self.pdfline_thickness))
        self.m_lineWqa.SetValue(str(self.QAline_thickness))
        self.m_lineWvert.SetValue(str(self.vertline_thickness))
        
        self.m_lineQA.SetValue(self.QAline_bool)
        self.m_linePDF.SetValue(self.pdfline_bool)            
        self.m_lineVERT.SetValue(self.vertline_bool)
        self.m_checkBoxSameColor.SetValue(self.samecolor_bool)
        
        self.m_sliderPDFsize.SetValue(int(200-self.pdfmultiplier*100))
        self.m_slider_col1.SetValue(self.pdfPageColsPos[0])
        self.m_slider_col2.SetValue(self.pdfPageColsPos[1])
        self.m_slider_col3.SetValue(self.pdfPageColsPos[2])
        self.m_checkBox_col1.SetValue(self.pdfPageColsChecks[0])
        self.m_checkBox_col2.SetValue(self.pdfPageColsChecks[1])
        self.m_checkBox_col3.SetValue(self.pdfPageColsChecks[2])
        with wx.FileDialog(self, "Choose which file to print", wildcard="*.tex",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            fileDialog.SetPath(str(self.notesdir)+'\.')
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                p.SwitchPanel(self,0) 
                return None    # the user changed their mind
            else:
                self.fileDialog = fileDialog
                self.FilePickEvent = True
                
                #m3.print_preview(self,event)
                t_preview = lambda self,evt : threading.Thread(target = m3.print_preview, name = 't_preview' , args=(self,evt )).run()
                t_preview(self, event) 
                
    def m_buttonDLG3OKOnButtonClick( self, event ):
        print("pressed OK dlg3")
    def m_buttonDLG3CancelOnButtonClick( self, event ):
        self.close()
    def m_menuCombineBooksOnMenuSelection( self, event ):
        with wx.FileDialog(self, "Choose which file to delete", wildcard="*.tex",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST|wx.FD_MULTIPLE) as fileDialog:
            fileDialog.SetPath(str(self.notesdir)+'\.')    
            if fileDialog.ShowModal() == wx.ID_OK:
                filepath = fileDialog.GetPaths()
                if len(filepath) == 1:
                    MessageBox(0, "You only selected 1 file, try again and select multiple files instead.", "Message", MB_ICONINFORMATION)
                else:
                    print(filepath)
                    
                    filenames_str = '\n'.join([Path(x).stem for x in filepath])
                    filenames_stem = [Path(x).stem for x in filepath]
                    with gui.MyDialog5(self,filenames_str) as dlg:
                        if dlg.ShowModal() == wx.ID_OK:     
                            print("success!!")
                            btn1 = dlg.m_radioDLG5_1.GetValue()
                            btn2 = dlg.m_radioDLG5_2.GetValue()
                            btn3 = dlg.m_radioDLG5_3.GetValue()
                            btn4 = dlg.m_radioDLG5_4.GetValue()
                            print(btn1,btn2,btn3,btn4)
                            
                            nr_lines = []
                            files = []
                            for name in filepath:
                                filename = Path(Path(name).stem).with_suffix('.tex')
                                file = open(str(Path(self.notesdir, filename)), 'r')
                                lines = file.readlines()
                                files.append(lines)
                                nr_lines.append(len(file.readlines()))
                                file.close()
                            
                            
                            print(nr_lines)
                            print(files)
                            title = CombineBookTitles(filenames_stem)
                            if btn1 == True: #alphabetically, it's standard alphabetically sorted
                                save2latexfile(self,files,title)
                            if btn2 == True:#sort small to largest
                                nr_lines, files = (list(t) for t in zip(*sorted(zip(nr_lines, files))))#sort based on first list numbers, small to large
                                save2latexfile(self,files,title)
                            if btn3 == True:#sort largest to smallest
                                nr_lines, files = (list(t) for t in zip(*sorted(zip(nr_lines, files))))#sort based on first list numbers, small to garge
                                nr_lines.reverse()
                                files.reverse()
                                save2latexfile(self,files,title)
                            if btn4 == True:#sort randomly
                                temp = list(itertools.chain.from_iterable(files))
                                random.shuffle(temp)
                                random.shuffle(temp)
                                files = temp
                                save2latexfile(self,files,title)
                            print()
                            print(os.listdir(self.notesdir))
                            print()
                            print(title)
                            if title+'.tex' in os.listdir(self.notesdir):
                                statinfo = os.stat(Path(self.notesdir,title+'.tex'))
                                if statinfo.st_size > 0 :
                                    MessageBox(0, f"The books have been succesfully combined!\nAnd it has the filename: {title}", "Info", MB_ICONINFORMATION)
                                else:
                                    print("Error: booknotes could not be merged and resulted in an empty file")
                            else:
                                print("Error: merged booknotes could not be created or saved!")
                                
                                
    def m_menuItemDelBookOnMenuSelection( self, event ):
        #with wx.FileDialog(self, "Choose which file to delete", wildcard="*.tex",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
        with wx.FileDialog(self, "Choose which file to delete", wildcard="*.tex",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            fileDialog.SetPath(str(self.notesdir)+'\.')    
            if fileDialog.ShowModal() == wx.ID_OK:
                print("clicked on OK, filedialog")
                filepath = fileDialog.GetPath()
                #filename = fileDialog.GetFilename()
                filename = Path(filepath).stem
                with gui.MyDialog4(self,filename) as dlg:
                    if dlg.ShowModal() == wx.ID_OK:                        
                        library = []
                        pathlib = []
                        for root, dirs, _ in os.walk(str(self.booksdir), topdown = False):
                            for name in dirs:
                                if name.lower() in filename.lower():
                                    library.append(name)
                                    if os.path.basename(root) != self.booksdir.name: #If it is not the dir you start in
                                        pathlib.append(os.path.join(os.path.basename(root),name))    
                        print(pathlib)
                        print(library)
                        EXISTS = False
                        if pathlib == [] and library != []:
                            #if it is not in a subfolder:
                            assert len(library) == 1
                            path2del = library[0]
                            EXISTS = True
                        elif pathlib != []:
                            assert len(pathlib) == 1
                            path2del = pathlib[0]
                            EXISTS = True
                            
                        if EXISTS:
                            #books jpg pages
                            folder = Path(self.booksdir,path2del)
                            [file.unlink() for file in folder.iterdir() if (filename in file.name and file.suffix =='.jpg' )]
                        #pics
                        try:
                            folder = Path(self.picsdir,filename)
                            [file.unlink() for file in folder.iterdir() if (filename in file.name and file.suffix =='.jpg' )]
                        except:
                            pass
                        #tempfiles
                        try:
                            folder = Path(self.tempdir)
                            [file.unlink() for file in folder.iterdir() if (filename in file.name and file.suffix =='.txt' )]
                        except:
                            pass
                        #notes latex
                        try:
                            folder = Path(self.notesdir)
                            [file.unlink() for file in folder.iterdir() if (filename in file.name and file.suffix =='.tex' )]
                        except:
                            pass
                        #final check if it has been deleted and inform user
                        try:
                            directories = [os.listdir(x) for x in [Path(self.booksdir,path2del),self.picsdir,self.tempdir,self.notesdir]]
                        except:
                            directories = [os.listdir(x) for x in [self.picsdir,self.tempdir,self.notesdir]]
                        if not any(filename in listdir for listdir in directories):
                            MessageBox(0, f"The book has been succesfully deleted!", "Info", MB_ICONINFORMATION)
            else: 
                print("operation aborted")
                return None    
        
    def m_menuNewBookOnMenuSelection( self, event ):   
        with gui.MyDialog3(self,None) as dlg: #use this to set the max range of the slider
            if dlg.ShowModal() == wx.ID_OK:
                print("closed dlg3, pressed: OK")
                bookname = dlg.m_textCtrl23.GetValue()
                if bookname != '':
                    
                    LaTeXcode = "intentionally left blank"
                    height_card = math.ceil(len(LaTeXcode)/40)/2
                    fig = Figure(figsize=[8, height_card], dpi=100)
                    ax = fig.gca()
                    ax.plot([0, 0,0, height_card],color = (1,1,1,1))
                    ax.axis('off')
                    ax.text(-0.5, height_card/2, LaTeXcode, fontsize = self.LaTeXfontsize, horizontalalignment = 'left', verticalalignment = 'center', wrap = True)
                    
                    canvas = FigureCanvas(fig)
                    canvas.draw()
                    renderer = canvas.get_renderer()
                    raw_data = renderer.tostring_rgb()
                    size = canvas.get_width_height()
                    imagetext = PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )
                    imagetext = f2.cropimage(imagetext,0)
                    imagetext = f2.cropimage(imagetext,1)
                    print(bookname)
                    path = Path(self.booksdir,bookname,bookname+"-0001.jpg")
                    print(path)
                    N = 1.3
                    a4page_w  = round(1240*N) # in pixels
                    a4page_h  = round(1754*N)
                    if path.parent.exists() == False:
                        path.parent.mkdir()                        
                    IMG = PIL.Image.new('RGB', (a4page_w, a4page_h),"white")
                    IMG.paste(imagetext,(int(a4page_w/2-imagetext.width/2),100))
                    if not path.exists:
                        IMG.save(path)
                    path = Path(self.notesdir,bookname+".tex") 
                    open(path, 'a').close()
            else:
                print("closed dlg3, pressed: Cancel")
                
                
            
            

    def m_slider_col1OnScrollChanged(self, event):
        self.pdfPageColsPos[0] = self.m_slider_col1.GetValue()
        settings_set(self)
        if BoxesChecked(self,1):
            t_preview = lambda self : threading.Thread(target = m3.preview_refresh, name = 't_preview' , args=(self, )).run()
            t_preview(self) 
            
            
            
    def m_slider_col2OnScrollChanged(self, event):
        self.pdfPageColsPos[1] = self.m_slider_col2.GetValue()
        settings_set(self)
        if BoxesChecked(self,2):
            t_preview = lambda self : threading.Thread(target = m3.preview_refresh, name = 't_preview' , args=(self, )).run()
            t_preview(self) 
            
    def m_slider_col3OnScrollChanged(self, event):
        self.pdfPageColsPos[2] = self.m_slider_col3.GetValue()
        settings_set(self)
        if BoxesChecked(self,3):
            t_preview = lambda self : threading.Thread(target = m3.preview_refresh, name = 't_preview' , args=(self, )).run()
            t_preview(self) 
            
    def m_checkBox_col1OnCheckBox( self, event ):
        self.pdfPageColsChecks[0] = self.m_checkBox_col1.GetValue()
        settings_set(self)
        t_preview = lambda self : threading.Thread(target = m3.preview_refresh, name = 't_preview' , args=(self, )).run()
        t_preview(self) 
            
    def m_checkBox_col2OnCheckBox( self, event ):
        self.pdfPageColsChecks[1] = self.m_checkBox_col2.GetValue()
        settings_set(self)
        t_preview = lambda self : threading.Thread(target = m3.preview_refresh, name = 't_preview' , args=(self, )).run()
        t_preview(self) 
            
    def m_checkBox_col3OnCheckBox( self, event ):
        self.pdfPageColsChecks[2] = self.m_checkBox_col3.GetValue()
        settings_set(self)
        t_preview = lambda self : threading.Thread(target = m3.preview_refresh, name = 't_preview' , args=(self, )).run()
        t_preview(self) 
            
    #%% menu item events
    " menu item events "
    def m_toolStitchOnButtonClick( self, event ):
        self.stitchmode_v =  not self.stitchmode_v
        if self.stitchmode_v == True:
            self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow2))
        else:
            self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow))
        
        """The following is used to create a mozaic of ictures. There is a question mode and an answer mode
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
        subprocess.Popen(f"explorer {self.booksdir}")
        
    def m_menuItemBackToMainOnMenuSelection( self, event ):
        if self.panel0.IsShown():
            val = MessageBox(0, "Are you sure you want to exit?", "Exit",  MB_YESNO | MB_DEFBUTTON2 )
            # Answer was yes, user wants to exit the app
            if val == 6: 
                self.Close()
        else:
            p.SwitchPanel(self,0)  
        
    def m_menuItemConvertOnMenuSelection( self, event ):
        
        m5.AddPathvar() #needed to make PDF2jpg work, it sets "Poppler for Windows" as pathvariable
        from_    = str(self.dirpdfbook)
        tempdir_ = str(self.tempdir)
        to_      = str(self.booksdir)
        
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
    #%%Flashcard menu
    def m_menuDeleteCardOnMenuSelection( self, event ):
        if self.SwitchCard == True: #there is also an Answer card
            modereset = self.mode
            image = f2.CreateSingularCard(self,'Question')
            BMP_q = f2.PILimage_to_Bitmap(image)
            
            image = f2.CreateSingularCard(self,'Answer')
            BMP_a = f2.PILimage_to_Bitmap(image)
            
            data = [BMP_q,BMP_a]
            self.mode = modereset
            
            with gui.MyDialog6(self,data) as dlg:
                if dlg.ShowModal() == wx.ID_OK:   
                    f2.DeleteCurrentCard(self)
                    print(f"index = {self.cardorder[self.index]}")
                    print(f"cardorder = {self.cardorder}")
                    #it might occur multiple times
                    self.cardorder = [x for x in self.cardorder if x != self.cardorder[self.index]]
                    self.nr_cards = len(self.cardorder)
                    self.nr_questions -= 1
                    self.m_TotalPages21.SetValue(f"{self.nr_questions}")
                    f2.displaycard(self)
                    self.Refresh()
                    print("success!!")
        elif self.SwitchCard == False: #there is only a Question card
            
            image = f2.CreateSingularCard(self,'Question')
            BMP_q = f2.PILimage_to_Bitmap(image)
            
            with gui.MyDialog7(self,BMP_q) as dlg:
                if dlg.ShowModal() == wx.ID_OK:  
                    f2.DeleteCurrentCard(self)
                    self.cardorder = [x for x in self.cardorder if x != self.cardorder[self.index]]
                    self.nr_cards = len(self.cardorder)
                    self.nr_questions -= 1
                    self.m_TotalPages21.SetValue(f"{self.nr_questions}")
                    f2.displaycard(self)
                    self.Refresh()
                
    def m_menuEditCardOnMenuSelection( self, event ):
        trueindex = self.cardorder[self.index]
        
        data = [self.questions_raw[trueindex],self.answers_raw[trueindex]]
        
        with gui.MyDialog8(self,data) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                question = dlg.m_textCtrl24.GetValue()
                answer   = dlg.m_textCtrl25.GetValue()
                #open file
                with open(Path(self.notesdir,self.filename),'r') as file:
                    flines = file.readlines()
                    file.close()
                #make changes
                if question == '':
                    flines.pop(trueindex)
                    f2.DeleteCurrentCard(self)
                    self.cardorder = [x for x in self.cardorder if x != self.cardorder[self.index]]
                    self.nr_cards = len(self.cardorder)
                    self.nr_questions -= 1
                    self.m_TotalPages21.SetValue(f"{self.nr_questions}")
                    f2.displaycard(self)
                    self.Refresh()
                else:
                    flines[trueindex] = r"\quiz{"+str(question)+"}"+r"\ans{"+str(answer)+"}"+"\n"
                    #save changes
                    with open(str(Path(self.notesdir, self.filename)), 'w') as output: 
                        for line in flines:
                            output.write(line)
                print("success!!")
                
    def m_menuPreviousCardOnMenuSelection( self, event ):
        m2.buttonPreviousCard(self)
        print("go to previous card")
    
    #%% settings menu
    """ settings menu """
    def m_resetselectionOnButtonClick( self, event ):           
        m.resetselection(self,event)
    
    def m_enterselectionOnButtonClick( self, event ):
        m.selectionentered(self,event)
        
    def m_checkBoxCursor11OnCheckBox( self, event ):
        self.cursor = not self.cursor
        m.setcursor(self)
        settings_set(self)
    
    # show drawn borders 
    def m_checkBox11OnCheckBox( self, event ):
        self.drawborders = self.m_checkBox11.IsChecked()   
        settings_set(self)
        try:
            print(f"checkbox is {self.drawborders}")
            self.pageimage = self.pageimagecopy # reset image
            f.ShowPage_fb(self)
            self.Layout()
        except:# a book hasn't been opened
            pass    
    def m_menuResetSettingsOnMenuSelection( self, event ):
        settings_reset(self)   
        self.m_checkBox11.Check(self.drawborders)
        self.m_checkBoxCursor11.Check(self.cursor)
        self.m_checkBoxDebug.Check(self.debugmode)
        m.setcursor(self)   
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
        m7.AcceleratorTableSetup(self,"flashbook","textwindow")
	
    def m_textCtrl2OnLeaveWindow( self, event ):
        m7.AcceleratorTableSetup(self,"flashbook","set")
    
    def m_btnSelectOnButtonClick( self, event ):
        if hasattr(self,"backupimage"):
            image3 = self.backupimage
            self.m_bitmap4.SetBitmap(image3)
        self.Layout()
    
    def m_btnImportScreenshotOnButtonClick( self, event ):
        self.stayonpage = True
        #load screenshot
        if self.BoolCropped == False: #load original screenshot
            img = PIL.Image.open(str(Path(self.tempdir,"screenshot.png")))
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
        m7.AcceleratorTableSetup(self,"flashbook","pagewindow")
        
    def m_CurrentPage11OnLeaveWindow( self, event ):
        m7.AcceleratorTableSetup(self,"flashbook","set")
        try:
            self.currentpage = int(self.m_CurrentPage11.GetValue())
        except:
            self.currentpage = 1
        m.switchpage(self,event)
    
    
    def m_bitmapScrollOnMouseWheel( self, event ):
        m.mousewheel(self,event)
        event.Skip()
        
	# draw borders #===========================================================
    def m_bitmapScrollOnLeftDown( self, event ):
        self.panel_pos = self.m_bitmapScroll.ScreenToClient(wx.GetMousePosition())
        self.mousepos = wx.GetMousePosition() # absolute position
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        event.Skip()
        
    def m_bitmapScrollOnLeftUp( self, event ):
        m.bitmapleftup(self,event)   
        event.Skip()
        
	# help menu #==============================================================
    def m_richText22OnLeftDown( self, event ):
        p.SwitchPanel(self,2) 
    
    #%% sync files
    """ sync files """
    def m_txtMyIPOnKeyUp( self, event ):
        self.IP1 = self.m_txtMyIP.GetValue()
        with open(Path(self.dirIP,'IPadresses.txt'),'w') as f:
            f.write(json.dumps({'IP1' : self.IP1,'IP2': self.IP2})) 
            f.close()        
    def m_txtTargetIPOnKeyUp( self, event ):
        self.IP2 = self.m_txtTargetIP.GetValue()
        with open(Path(self.dirIP,'IPadresses.txt'),'w') as f:
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
    """ flashcard """
    # main program
    def m_filePicker21OnFileChanged( self, event ):
        self.m_menubar1.EnableTop(2,True)
        m2.startprogram(self,event)
    
    # button events
    def m_buttonCorrectOnButtonClick( self, event ):        
        m2.buttonCorrect(self)
        SaveTime(self)
        event.Skip()
    def m_bitmapScroll1OnLeftUp( self, event ):
        m2.buttonCorrect(self)
        event.Skip()
    
    def m_scrolledWindow11OnLeftUp( self, event ):
        m2.buttonCorrect(self)
        event.Skip()
    def m_scrolledWindow11OnRightUp( self, event ):
        m2.buttonWrong(self)
        event.Skip()
    def m_scrolledWindow11OnMouseWheel( self, event ):
        m2.switchCard(self)
        event.Skip()
    
    def m_buttonWrongOnButtonClick( self, event ):
        m2.buttonWrong(self)
        SaveTime(self)
        event.Skip()
    def m_bitmapScroll1OnRightUp( self, event ):
        m2.buttonWrong(self)   
        event.Skip()
	
    def m_toolSwitch21OnToolClicked( self, event ):
        m2.switchCard(self)
	
    def m_bitmapScroll1OnMouseWheel( self, event ):
        m2.switchCard(self)
        
    #%% print the notes
    """ print the notes """
    def m_sliderPDFsizeOnScrollChanged(self,event):
        self.pdfmultiplier = float(200-self.m_sliderPDFsize.GetValue())/100
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
        
    def m_lineVERTOnCheckBox( self, event):
        self.FilePickEvent = False
        self.vertline_bool = self.m_lineVERT.GetValue()
        settings_set(self)
        m3.preview_refresh(self)
        
    
    def m_colorQAlineOnColourChanged( self, event ):
        original_color = self.QAline_color
        self.FilePickEvent = False
        RGB = self.m_colorQAline.GetColour()
        self.QAline_color  = (RGB.Red(),RGB.Green(),RGB.Blue())   
        if original_color != self.QAline_color:
            settings_set(self)
            m3.preview_refresh(self)
        
    def m_colorPDFlineOnColourChanged( self, event ):
        original_color = self.pdfline_color
        self.FilePickEvent = False
        RGB = self.m_colorPDFline.GetColour()
        self.pdfline_color  = (RGB.Red(),RGB.Green(),RGB.Blue())    
            
        if self.m_checkBoxSameColor.GetValue() == True:
            if self.vertline_color != original_color or self.pdfline_color != original_color:
                self.vertline_color  = self.pdfline_color 
                self.m_colorVERTline.SetColour(self.pdfline_color)
                settings_set(self)
                m3.preview_refresh(self)
        else:
            if self.pdfline_color != original_color:
                settings_set(self)
                m3.preview_refresh(self)
        
    def m_colorVERTlineOnColourChanged( self, event):
        original_color = self.vertline_color
        if self.m_checkBoxSameColor.GetValue() == True:
            self.vertline_color  = self.pdfline_color 
            new_color = self.pdfline_color
            self.m_colorVERTline.SetColour(self.pdfline_color)
        else:
            self.FilePickEvent = False
            RGB = self.m_colorVERTline.GetColour()
            self.vertline_color  = (RGB.Red(),RGB.Green(),RGB.Blue())    
            new_color = self.vertline_color 
            
        if original_color != new_color:
            #In case you chose the exact same color do nothing
            settings_set(self)
            m3.preview_refresh(self)
        
        
        
    def m_PrintFinalOnButtonClick( self, event ):
        self.printsuccessful = False
        self.printpreview    = False
        self.FilePickEvent   = False
        m3.preview_refresh(self)
        if self.printsuccessful == True:
            self.printpreview = True
            p.SwitchPanel(self,0)
            # remove all temporary files of the form "temporary(...).png"    
            if self.debugmode == False:
                folder = self.tempdir
                [file.unlink() for file in folder.iterdir() if ("temporary" in file.name and file.suffix =='.png' )]
            MessageBox(0, " Your PDF has been created!\n Select in the menubar: `Open/Open PDF-notes Folder` to\n open the folder in Windows explorer. ", "Message", MB_ICONINFORMATION)
            
    def m_CtrlNrCardsOnText( self, event ):
        try:
            var = self.m_CtrlNrCards.GetValue()
            print(f"var is {var}")
            if var == "":
                
                self.NrCardsPreview = ''
            elif int(var) > 0:
                self.NrCardsPreview = int(var)
            settings_set(self)
            m3.preview_refresh(self)
        except:
            log.ERRORMESSAGE("Error: invalid entry in CtrlNrCardsOnText")
            
    def m_lineWpdfOnText( self, event ):
        
        try:            
            if int(self.m_lineWpdf.GetValue()) >= 0:
                if int(self.m_lineWpdf.GetValue()) != self.pdfline_thickness:
                    #only execute if the value has changed
                    self.pdfline_thickness = int(self.m_lineWpdf.GetValue())
                    settings_set(self)
                    m3.preview_refresh(self)
        except:
            log.ERRORMESSAGE("Error: invalid entry in lineWpdf")
            
    def m_lineWqaOnText( self, event ):
        try:            
            if int(self.m_lineWqa.GetValue()) >= 0:
                if int(self.m_lineWqa.GetValue()) != self.QAline_thickness:
                    self.QAline_thickness = int(self.m_lineWqa.GetValue())
                    settings_set(self)
                    m3.preview_refresh(self)
        except:
            log.ERRORMESSAGE("Error: invalid entry")
            
    def m_lineWvertOnText( self, event ):
        try:            
            if int(self.m_lineWvert.GetValue()) >= 0:
                if int(self.m_lineWvert.GetValue()) != self.vertline_thickness:
                    #only execute if the value has changed
                    self.vertline_thickness = int(self.m_lineWvert.GetValue())
                    settings_set(self)
                    m3.preview_refresh(self)
        except:
            log.ERRORMESSAGE("Error: invalid entry")  
    def m_checkBoxSameColorOnCheckBox(self,event):
        self.samecolor_bool = self.m_checkBoxSameColor.IsChecked()
        #check if it has been checked
        if self.samecolor_bool == True:
            if self.vertline_color != self.pdfline_color:
                self.FilePickEvent = False
                self.vertline_color = self.pdfline_color     
                self.m_colorVERTline.SetColour(self.vertline_color)     
                settings_set(self)
                m3.preview_refresh(self)
        
    #%% Help menu
    def m_richText1OnLeftDown(self,event):
        p.SwitchPanel(self,self.lastpage)
    def m_richText2OnLeftDown(self,event):
        p.SwitchPanel(self,self.lastpage)
    def m_richText3OnLeftDown(self,event):
        p.SwitchPanel(self,self.lastpage)
    def m_richText4OnLeftDown(self,event):
        p.SwitchPanel(self,self.lastpage)
    #%%
    def m_checkBoxDebugOnMenuSelection( self, event ):
        self.debugmode = not self.debugmode
        settings_set(self)
    def m_menuResetLogOnMenuSelection( self, event ):
        folder = self.tempdir
        [file.unlink() for file in folder.iterdir() if ("logging" in file.name and file.suffix =='.out' )]
    def m_menuItemGraphOnMenuSelection( self, event ):
        self.Graph_bool = not self.Graph_bool
        settings_set(self)
        if self.panel0.IsShown():
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
            self.Layout()
        
    #%% timecount
    def m_scrolledWindow1OnMouseEvents( self, event ):
        SaveTime(self)
        event.Skip()
    def m_scrolledWindow1OnKeyDown( self, event ):
        SaveTime(self)
        event.Skip()        
    def m_bitmapScrollOnMouseEvents( self, event ):
        SaveTime(self)
        event.Skip()
    def m_bitmapScrollOnKeyDown( self, event ):
        SaveTime(self)
        event.Skip()
    def m_bitmapScroll1OnKeyDown( self, event ):
        SaveTime(self)
        event.Skip()
    def m_bitmapScroll1OnMouseEvents( self, event ):
        SaveTime(self)
        event.Skip()
    def m_scrolledWindow11OnMouseEvents( self, event ):
        SaveTime(self)
        event.Skip()
    def m_scrolledWindow11OnKeyDown( self, event ):
        SaveTime(self)
        event.Skip()
        
if __name__ == "__main__":
    # start the application
    app = wx.App(False) 
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
    del app


