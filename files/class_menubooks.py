# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:13:17 2019

@author: Anton
"""
import math
import gui_flashbook as gui
import threading
import wx
import PIL
import program as p
import print_modules as m3
import fc_modules as m2
from pathlib import Path
from latexoperations import Commands as cmd
import imageoperations as imop
import log_module    as log
import os
import random
import itertools
import pylab
pylab.ioff() # make sure it is inactive, otherwise possible qwindows error    .... https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

ICON_EXCLAIM=0x30

import ctypes
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100

def CombineBookTitles(booknames):
    """To combine multiple book titles, since this would otherwise end up in a very long
    name, it will instead only take the first full name and then abbreviate the following
    books to only the first letters of the books."""
    C = 'MULTI_'
    for i,string in enumerate(booknames):
        if i==0:
            C += string
        else:
            C += '_'+ ''.join([c for c in string.title() if c.isupper()])
    return C

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
            
class booksmenu(gui.MyFrame):
    def __init__(self):
        pass
    def m_menuCombineBooksOnMenuSelection( self, event ):
        with wx.FileDialog(self, "Select multiples files to combine", wildcard="*.tex",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST|wx.FD_MULTIPLE) as fileDialog:
            fileDialog.SetPath(str(self.notesdir)+'\.')    
            if fileDialog.ShowModal() == wx.ID_OK:
                filepath = fileDialog.GetPaths()
                if len(filepath) == 1:
                    MessageBox(0, "You only selected 1 file, try again and select multiple files instead.", "Message", MB_ICONINFORMATION)
                else:
                    print(filepath)
                    filenames_str = '\n'.join([Path(x).stem for x in filepath])
                    filenames_stem = [Path(x).stem for x in filepath]
                    title = CombineBookTitles(filenames_stem)
                    title_backup = title
                    with gui.MyDialog5(self,[filenames_str,title]) as dlg:
                        if dlg.ShowModal() == wx.ID_OK:     
                            print("success!!")
                            btn1 = dlg.m_radioDLG5_1.GetValue()
                            btn2 = dlg.m_radioDLG5_2.GetValue()
                            btn3 = dlg.m_radioDLG5_3.GetValue()
                            btn4 = dlg.m_radioDLG5_4.GetValue()
                            print(btn1,btn2,btn3,btn4)
                            title = dlg.m_textCtrlCombinedFileName.GetValue()
                            if title == '':#in case the user tries to sabotage the program
                                title = title_backup
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
                    imagetext = imop.cropimage(imagetext,0)
                    imagetext = imop.cropimage(imagetext,1)
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
