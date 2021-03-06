# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:13:17 2019

@author: Anton
"""
import math
import _GUI.gui_flashbook as gui
import wx
import PIL
from pathlib import Path
import _shared_operations.imageoperations as imop
import threading
import _pdf.pdf_modules as m5
import os
import random
import itertools
import pylab
pylab.ioff() # make sure it is inactive, otherwise possible qwindows error    .... https://stackoverflow.com/questions/26970002/matplotlib-cant-suppress-figure-window
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import ctypes
import _logging.log_module as log
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100

def CombineBookTitles(booknames):
    """To combine multiple book titles, since this would otherwise end up in a very long
    name, it will instead only take the first full name and then the acronyms of the subsequent books."""
    
    Name = 'MULTI_'
    for i,bookname in enumerate(booknames):
        if i == 0:
            Name += bookname
        else:
            acronym = ''.join([c for c in bookname.title() if c.isupper()])
            Name += '_'+ acronym
    return Name

def save2latexfile(self,files,title):
    assert 0 == 1
    """
    LISTOFLIST = (type(files[0])==list)
    filepath = Path(self.notesdir,title+'.pkl')
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
        with open(filepath,'a') as f:
            if type(data) == list:
                for line in data:
                    log.DEBUGLOG(debugmode=self.debugmode, info=f'CLASS MENUBOOKS line = {line}')
                    f.write(line)
            f.close()  
      """     
class booksmenu(gui.MyFrame):
    def __init__(self):
        pass
    def m_menuItemConvertOnMenuSelection( self, event ):
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS MENUBOOKS: pressed Convert Books')
        m5.AddPathvar() #needed to make PDF2jpg work, it sets "Poppler for Windows" as pathvariable
        from_    = str(self.dirpdfbook)
        tempdir_ = str(self.tempdir)
        to_      = str(self.booksdir)
        m5.ConvertPDF_to_JPG(self,from_,tempdir_,to_)
        #t_pdf = lambda self, from_, tempdir_, to_ : threading.Thread(target = m5.ConvertPDF_to_JPG , args=(self,from_, tempdir_, to_ )).start()
        #t_pdf(self, from_, tempdir_, to_) 
    
    def m_menuCombineBooksOnMenuSelection( self, event ):
        assert 0 == 1 #it should read as pickle file and combine pickle files!!!
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS MENUBOOKS: pressed Combine Books')
        with wx.FileDialog(self, "Select multiples files to combine", wildcard="*.pkl",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST|wx.FD_MULTIPLE) as fileDialog:
            fileDialog.SetPath(str(self.notesdir)+'\.')    
            if fileDialog.ShowModal() == wx.ID_OK:
                filepath = fileDialog.GetPaths()
                if len(filepath) == 1:
                    MessageBox(0, "You only selected 1 file, try again and select multiple files instead.", "Message", MB_ICONINFORMATION)
                else:
                    log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS MENUBOOKS: filepath = {filepath}')
                    filenames_str = '\n'.join([Path(x).stem for x in filepath])
                    filenames_stem = [Path(x).stem for x in filepath]
                    title = CombineBookTitles(filenames_stem)
                    title_backup = title
                    with gui.MyDialog5(self,[filenames_str,title]) as dlg:
                        if dlg.ShowModal() == wx.ID_OK:     
                            button1 = dlg.m_radioDLG5_1.GetValue()
                            button2 = dlg.m_radioDLG5_2.GetValue()
                            button3 = dlg.m_radioDLG5_3.GetValue()
                            button4 = dlg.m_radioDLG5_4.GetValue()
                            
                            title = dlg.m_textCtrlCombinedFileName.GetValue()
                            if title == '':#in case the user tries to sabotage the program
                                title = title_backup
                            nr_lines = []
                            files = []
                            for name in filepath:
                                filename = Path(Path(name).stem).with_suffix('.box')
                                file = open(str(Path(self.notesdir, filename)), 'r')
                                lines = file.readlines()
                                files.append(lines)
                                nr_lines.append(len(file.readlines()))
                                file.close()
                            
                            if button1: #alphabetically, it's standard alphabetically sorted
                                save2latexfile(self,files,title)
                            elif button2:#sort small to largest
                                nr_lines, files = (list(t) for t in zip(*sorted(zip(nr_lines, files))))#sort based on first list numbers, small to large
                                save2latexfile(self,files,title)
                            elif button3:#sort largest to smallest
                                nr_lines, files = (list(t) for t in zip(*sorted(zip(nr_lines, files))))#sort based on first list numbers, small to garge
                                nr_lines.reverse()
                                files.reverse()
                                save2latexfile(self,files,title)
                            elif button4:#sort randomly
                                temp = list(itertools.chain.from_iterable(files))
                                random.shuffle(temp)
                                random.shuffle(temp)
                                files = temp
                                save2latexfile(self,files,title)
                            
                            log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS MENUBOOKS:\n\t nr lines = {nr_lines},\n\t files = {files},\n\t title = {title}')
                            if title+'.pkl' in os.listdir(self.notesdir):
                                statinfo = os.stat(Path(self.notesdir,title+'.pkl'))
                                if statinfo.st_size > 0 :
                                    MessageBox(0, f"The books have been succesfully combined!\nAnd it has the filename: {title}", "Info", MB_ICONINFORMATION)
                                else:
                                    log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS MENUBOOKS: Error: booknotes could not be merged and resulted in an empty file')
                            else:
                                log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS MENUBOOKS: Error: merged booknotes could not be created or saved!')
                                
                                
    

                            
    def m_menuItemDelBookOnMenuSelection( self, event ):
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS MENUBOOKS: pressed Delete Book')
        with wx.FileDialog(self, "Choose which file to delete", wildcard="*.pkl",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            fileDialog.SetPath(str(self.notesdir)+'\.')    
            if fileDialog.ShowModal() == wx.ID_OK:
                log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS MENUBOOKS: delete book, clicked on OK ')
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
                        log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS MENUBOOKS:\n\t pathlib = {pathlib},\n\t library = {library}')
                        EXISTS = False
                        if pathlib == [] and library != []:
                            #if it is not in a subfolder:
                            assert len(library) == 1
                            path2del = library[0]
                            EXISTS = True
                        elif pathlib:
                            assert len(pathlib) == 1
                            path2del = pathlib[0]
                            EXISTS = True
                            
                        if EXISTS:
                            # try to remove books jpg pages
                            folder = Path(self.booksdir,path2del)
                            [file.unlink() for file in folder.iterdir() if (filename in file.name and file.suffix =='.jpg' )]
                        # try to remove pics
                        try:
                            folder = Path(self.picsdir,filename)
                            [file.unlink() for file in folder.iterdir() if (filename in file.name and file.suffix =='.jpg' )]
                        except:
                            pass
                        # try to remove tempfiles
                        try:
                            folder = Path(self.tempdir)
                            [file.unlink() for file in folder.iterdir() if (filename in file.name and file.suffix =='.txt' )]
                        except:
                            pass
                        # try to remove LaTeX notes
                        try:
                            folder = Path(self.notesdir)
                            [file.unlink() for file in folder.iterdir() if (filename in file.name and file.suffix =='.pkl' )]
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
                log.DEBUGLOG(debugmode=self.debugmode, msg=f'CLASS MENUBOOKS: operation aborted')
                return None    
        
    def m_menuNewBookOnMenuSelection( self, event ):   
        with gui.MyDialog3(self,None) as dlg: #use this to set the max range of the slider
            if dlg.ShowModal() == wx.ID_OK:
                bookname = dlg.m_textCtrl23.GetValue()
                if bookname != '':
                    
                    assert 0 == 1
                    """
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
                    path = Path(self.booksdir,bookname,bookname+"-0001.jpg")
                    N = 1.3
                    a4page_w  = round(1240*N) # in pixels
                    a4page_h  = round(1754*N)
                    if not path.parent.exists():
                        path.parent.mkdir()                        
                    IMG = PIL.Image.new('RGB', (a4page_w, a4page_h),"white")
                    IMG.paste(imagetext,(int(a4page_w/2-imagetext.width/2),100))
                    if not path.exists:
                        IMG.save(path)
                    path = Path(self.notesdir,bookname+".pkl") 
                    open(path, 'a').close()
                    """
            else:
                log.DEBUGLOG(debugmode=self.debugmode, msg=f"CLASS MENUBOOKS: closed dialog NewBook, pressed 'cancel'")
                
                
