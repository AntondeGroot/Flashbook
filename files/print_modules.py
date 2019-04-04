# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018
@author: Anton
"""
import bisect
import ctypes
import img2pdf
import print_initialization as ini3
import json
import numpy as np
from pathlib import Path
import os
from PIL import Image
import PIL
import fb_functions as f
import fc_functions as f2
import print_functions as f3
import program as p
import log_module as log
import re
from termcolor import colored
import win32clipboard
from win32api import GetSystemMetrics
import wx
import threading
from timingmodule import Timing


#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MessageBox = ctypes.windll.user32.MessageBoxW
#win32api: total width of all monitors
SM_CXVIRTUALSCREEN = 78 

def ColumnSliders(self):
    LIST = []
    if self.m_checkBox_col1.IsChecked():
        LIST.append(self.m_slider_col1.GetValue())
    if self.m_checkBox_col2.IsChecked():
        LIST.append(self.m_slider_col2.GetValue())
    if self.m_checkBox_col3.IsChecked():
        LIST.append(self.m_slider_col3.GetValue())
    return LIST

def saveimage(image,path_):
    im = image
    path = path_
    im.save(path)

def Flatlist_to_List(list1,list2):
    x = 0
    list3 = []
    """
    List1 is a list of lists
    List2 is a flatlist
    convert List2 to the same form as List1
    """
    #check first if the two lists have the same nr of elements
    flatlist = [item for sublist in list1 for item in sublist]
    assert len(flatlist) == len(list2)
    #convert list2 in the same form as list
    nrlist = [len(x) for x in list1]
    for nr in nrlist:
        y = x
        x+=nr
        list3.append(list2[y:x])
    return list3


def calculate_pdflines(_input):
    _list = _input
    B = []
    _list.insert(0,0)
    
    for i,x in enumerate(_list):
        if i != 0 and i != len(_list):
            B.append(max(x,_list[i-1]))
    assert len(B) == len(_input)-1
    return B

def import_screenshot(self,event):
    """Import a screenshot, it takes multiple monitors into account. 
    The bytestream from win32 is from a Device Independent Bitmap, i.e.'RGBquad', meaning that it is not RGBA but BGRA coded.
    The image is also flipped and rotated."""
    
    ScrWidth, ScrHeight = GetSystemMetrics(SM_CXVIRTUALSCREEN),GetSystemMetrics(1)
    win32clipboard.OpenClipboard()
    
    if hasattr(self,"bookname"):
        if self.bookname != '':
            try:
                if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):# Device Independent Bitmap
                    #PrtScr available
                    data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                    win32clipboard.CloseClipboard()                
                    
                    #convert bytes to PIL Image
                    img = Image.frombytes('RGBA', (ScrWidth,ScrHeight), data)
                    b,g,r,a = img.split() 
                    image = Image.merge("RGB", (r, g, b))
                    image = image.rotate(180)
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)
                    image.save(str(Path(self.tempdir,"screenshot.png")))
                    
                    #convert back to wxBitmap
                    data = image.tobytes()
                    image3 = wx.Bitmap().FromBuffer(ScrWidth,ScrHeight,data)
                        
                    self.backupimage = image3
                    self.m_bitmap4.SetBitmap(image3)
                    p.SwitchPanel(self,4)
                    
                else:
                    MessageBox(0, "There is no screenshot available\npress PrtScr again\nor press Alt+PrtScr to only copy an active window", "Error", ICON_EXCLAIM)
            except:
                MessageBox(0, "There is no screenshot available\npress PrtScr again\nor press Alt+PrtScr to only copy an active window", "Error", ICON_EXCLAIM)
        else:
            MessageBox(0, "Please open a book first", "Error", ICON_EXCLAIM)
    try:
        win32clipboard.CloseClipboard()
    except:
        pass




def print_preview(self,event): 
    ini3.initializeparameters(self) 
    startprogram(self,event)
    #resize to A4 format
    _, PanelHeight = self.m_panel32.GetSize()
    PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
    #only select first page and display it on the bitmap
    
    image = PIL.Image.open(self.allimages_v[0])
    image = image.resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS)
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    
    bitmapimage = wx.Bitmap(image2)
    self.m_bitmap3.SetBitmap(bitmapimage)
    self.Layout()
    
def preview_refresh(self):
    notes2paper(self)
    #startprogram(self,event)
    _, PanelHeight = self.m_panel32.GetSize()
    PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
    #only select first page and display it on the bitmap
    image = PIL.Image.open(self.allimages_v[0])
    image = image.resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS) 
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    bitmapimage = wx.Bitmap(image2)
    self.m_bitmap3.SetBitmap(bitmapimage)
    self.Layout()

  
def notes2paper(self):
    self.linesep = 5
    N = 1.3
    self.a4page_w  = round(1240*N*self.pdfmultiplier) # in pixels
    self.a4page_h  = round(1754*N*self.pdfmultiplier)
    self.paper_h      = []
    self.paper_h_list = []
    ## create images
    self.allimages   = []
    self.allimages_w = [] #widths
    if self.printpreview == True:
        if self.NrCardsPreview != '':
            nrQ = int(self.NrCardsPreview)
        else:
            nrQ = self.nr_questions
    else:
        nrQ = self.nr_questions
    allimages   = [None]*nrQ
    allimages_w = [None]*nrQ
    threads_save = [None]*nrQ
    
    """ Create the cards """
    TT = Timing("Create the QA cards")
    
    
    for i in range(nrQ):
        print(f"now at card: {i}")
        imagename = f"temporary{i}.png" 
        #print(self.textdictionary)
        imagepath = str(Path(self.tempdir, imagename))
        image_q = PIL.Image.new('RGB', (0, 0),"white")
        image_a = []
        for mode in ['Question','Answer']: 
            self.mode = mode
            TextCard = False      
            key = f'{self.mode[0]}{i}'
            #try: # try to create a TextCard
            if key in self.textdictionary:
                print(f"create textcard for {key}")
                TextCard, imagetext = f3.CreateTextCardPrint(self,key)
                #assert TextCard == self.TextCard
                #assert imagetext == self.imagetext
                self.TextCard = TextCard
                self.imagetext = imagetext
                # if there is a textcard either combine them with a picture or display it on its own
                #if TextCard == True: 
                if key in self.picdictionary:
                    print(f"create combicard for {key}")
                    image = f2.CombinePicText_fc(self,key,imagetext)
                    #assert image == self.image
                    self.image = image
                    if mode == 'Question':
                        image_q = image
                    else:
                        image_a = image
                else:
                    image = imagetext                        
                    if mode == 'Question':
                        image_q = image
                    else:
                        image_a = image
            else: #if there is no textcard only display the picture
                if key in self.picdictionary:
                    path = Path(self.picsdir, self.bookname ,self.picdictionary[key])
                    image = f2.findpicture(self,key)
                    #if path.is_file():
                    #image = PIL.Image.open(str(path))
                    if mode == 'Question':
                        image_q = image
                    else:
                        image_a = image
            #except:
            #    log.ERRORMESSAGE("Error: could not display card")  
        
        #self.image should be different
        #combine question and answer:
        if image_a != []:
            images = [image_q,image_a]
            widths, heights = zip(*(i.size for i in images)) 
            total_height = sum(heights)
            max_width = max(widths)
            if self.QAline_bool == True:
                new_im = PIL.Image.new('RGB', (max_width, total_height + self.QAline_thickness), "white")
                line = PIL.Image.new('RGB', (image_q.size[0], self.QAline_thickness), self.QAline_color)
                #combine images to 1
                new_im.paste(images[0], (0,0))
                new_im.paste(line,(0,image_q.size[1]))
                new_im.paste(images[1], (0,image_q.size[1]+self.QAline_thickness))
            else:
                new_im = PIL.Image.new('RGB', (max_width, total_height), "white")
                #combine images to 1
                new_im.paste(images[0], (0,0))
                new_im.paste(images[1], (0,image_q.size[1]))
            
            IMG_QA = new_im
            
        else:
            if image_q.size != (0,0): 
                IMG_QA = image_q
            else:
                print(colored("FATAL error"*5,'red'))
        ##anton
        if ColumnSliders(self) != []:
            columns = ColumnSliders(self)
            ColumnWidths = [int(col/100*self.a4page_w) for col in columns if col != 0]                       

            if len(ColumnWidths) > 0:
                w,h = IMG_QA.size
                if w > min(ColumnWidths) and w > 0:
                    NearestCol = min(ColumnWidths, key=lambda x:abs(x-w))
                    IMG_QA = IMG_QA.resize((int(NearestCol),int(NearestCol/w*h)), PIL.Image.ANTIALIAS)
        try:
            #IMG_QA.save(imagepath)
            threads_save[i] = threading.Thread(target = saveimage  , args=(IMG_QA,imagepath))
            threads_save[i].start()
        except:
            print(f"goes wrong for {imagename}")
            
        #self.allimages.append(imagepath)
        allimages[i] = imagepath
        if self.vertline_bool:
            # Keep in mind the extra width needed for the vertical lines
            # Overestimate by 1 vertline_thickness to play it safe:            thickness << width of image
            allimages_w[i] = IMG_QA.size[0] + 2*self.vertline_thickness + 2*5
        else:
            allimages_w[i] = IMG_QA.size[0]
            
         
    
    for i,thread in enumerate(threads_save):
        thread.join()

        
    #self.allimages_w = allimages_w
    #self.allimages = allimages            
    # sort images horizontally
    TT.update("sort images horizontally")
    A = np.cumsum(allimages_w)
    C = []
    while len(allimages_w) != 0:        
        """Method:
        Cumsum the widths of images.
        Use bisect to look first instance where the cumsum is too large to fit on a page.
        Store those pages in a list separately, eliminate those from the search.
        Recalculate cumsum and repeat."""
        
        index = bisect.bisect_left(A, self.a4page_w) 
        if index == 0 and len(A) != 0: #image is too wide
            im = allimages[0]
            C.append(im)
            allimages = allimages[1:] 
            allimages_w = allimages_w[1:] 
            A = np.cumsum(allimages_w)  
            
        elif index != len(A): #image is not too wide
            C.append(allimages[:index])
            allimages = allimages[index:] 
            allimages_w = allimages_w[index:] 
            A = np.cumsum(allimages_w)  #anton what if it is too wide
        elif index == len(A): # image is not too wide AND last in list
            C.append(allimages)
            allimages_w = []
            
    paper_h_list = C
    paper_h      = [None] * len(paper_h_list)
    paper_v_widths = [None] * len(paper_h_list)
    paper_v_heights = [None] * len(paper_h_list)
    threads = [None] * len(paper_h_list)
    # combine pics horizontally
    TT.update("combine pics horizontally")
    for i,paths in enumerate(paper_h_list):
        images = [PIL.Image.open(x) for x in paths]
        N = len(images)
        #try:
        widths, heights = zip(*(im.size for im in images)) 
        if self.vertline_bool:
            total_width = sum(widths) + (N+1)*self.vertline_thickness+2*N*5
        else:
            total_width = sum(widths)
        if self.pdfline_bool:
            max_height = max(heights) + 2*self.pdfline_thickness+2*self.linesep
        else:
            max_height = max(heights)
        
        self.maxheight = max_height
        
        new_im = PIL.Image.new('RGB', (total_width, max_height), "white")
        #combine images to 1
        x_offset = 0
        
        
        for j,im in enumerate(images):
            if  self.vertline_bool == True:        
                border = PIL.Image.new("RGB", (self.vertline_thickness , self.maxheight), self.vertline_color)        
                new_im.paste(border, (x_offset,0))
                x_offset += self.linesep + self.vertline_thickness
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0] + self.linesep
        if self.vertline_bool:
            new_im.paste(border, (x_offset,0))
            
        self.image = new_im
        #new_im = add_border(self,new_im,"single")
        pathname = str(Path(self.tempdir,f"temporary_p{i}.png"))
        #new_im.save(pathname)
        threads[i] = threading.Thread(target = saveimage  , args=(new_im,pathname))
        threads[i].start()
        paper_h[i] = pathname
        paper_v_widths[i] = new_im.size[0]
        paper_v_heights[i] = new_im.size[1]
        """    
        except: # if only one picture left
        
            #print(images.size)
            if images.size[0] > self.a4page_w:
                if i == 0 :
                    images = add_sideborder(self,images,"both")
                else:
                    images = add_sideborder(self,images,"right")
                w,h = images.size
                images = images.resize((self.a4page_w,int(h*self.a4page_w/w)))
            
            images = add_border(self,images,"single")
            pathname = str(Path(self.tempdir,f"temporary_p{i}.png"))
            images.save(pathname)
            
            paper_h[i] = pathname
            paper_v_widths[i] = new_im.size[0]
            paper_v_heights[i] = new_im.size[1]
        """ 
    for i in range(len(threads)):
        threads[i].join()
    if None in paper_h or None in paper_v_widths:
        print("NONE DETECTED"*10)
    paper_h = [x for x in paper_h if x != None]
    paper_v_widths = [x for x in paper_v_widths if x != None]
    paper_v_heights = [x for x in paper_v_heights if x != None]
    #self.paper_h[0].show()    
    # sort images vertically
    TT.update("sort images vertically")
    D = []
    #self.img_heights = []
    #for path in self.paper_h:
    #    img = PIL.Image.open(path)
    #    if self.pdfline_bool:
    #        self.img_heights.append(img.size[1]+self.pdfline_thickness)
    #    else:
    #        self.img_heights.append(img.size[1])
    ##self.img_heights = self.paper_v_heights
    
    A = np.cumsum(paper_v_heights)
    if self.printpreview == False or self.printpreview == True:
        while len(paper_v_heights) != 0:        
            index = bisect.bisect_left(A, self.a4page_h) #look for index where value is too large        
            if index != len(A):        
                D.append(paper_h[:index] )
                paper_h = paper_h[index:] 
                paper_v_heights = paper_v_heights[index:] 
                A = np.cumsum(paper_v_heights)    
            else:
                D.append(paper_h)                
                paper_v_heights = []
    else: # only look for 1st page (currently not in use)
        index = bisect.bisect_left(A, self.a4page_h) #look for index where value is too large        
        D.append(paper_h[:index] )
        
               
    paper_h = D
    
    
    self.widthsperpage = Flatlist_to_List(paper_h ,paper_v_widths)
    print(f"widths {self.widthsperpage}")
    
    # combine vertical pictures per page
    TT.update("combine vertical pictures per page")
    imagelist = [None] * len(paper_h)
    threads = [None] * len(paper_h)
    for page_i, images_on_page_i in enumerate(paper_h):
        images = images_on_page_i
        
        new_im = PIL.Image.new('RGB', (self.a4page_w, self.a4page_h), "white")        
        y_offset = 0
        x_offset = 0
        #try:
        
        linelengths = calculate_pdflines(self.widthsperpage[page_i])
        
        for j, path in enumerate(images_on_page_i):
            
            im = PIL.Image.open(path)
            line = PIL.Image.new("RGB", (linelengths[j] ,self.pdfline_thickness), self.pdfline_color)  
            if self.pdfline_bool:
                new_im.paste(line,(0,y_offset))
                y_offset += self.linesep
            
            new_im.paste(im, (0,y_offset))
            y_offset += im.size[1]
            
            x_offset += im.size[0]
            lastwidth = im.size[0]
        if self.pdfline_bool: 
            line = PIL.Image.new("RGB", (lastwidth ,self.pdfline_thickness), self.pdfline_color)  
            new_im.paste(line,(0,y_offset))
        self.combinedwidth = x_offset
    
        #self.image = new_im
        new_im = add_margins(self,new_im)
        #except: #if images is not an iterable it gives an error, it contains only 1 image so just add
        #    new_im.paste(images, (0,y_offset))
        #    new_im = add_margins(self,new_im)
        
        pathname = str(Path(self.tempdir,f"temporary_h{page_i}.png"))
        #new_im.save(pathname)
        threads[page_i] = threading.Thread(target = saveimage  , args=(new_im,pathname))
        threads[page_i].start()
        
        
        imagelist[page_i] = pathname
    for i in range(len(threads)):
        threads[i].join()
    self.allimages_v = imagelist
    # imagelist is the list with all image filenames
    
    
    i = 0
    
    print(f"imagelist is {imagelist}")
    #folder = []
    if self.printpreview == False:
        TT.update("writing files to pdf")
        filename = os.path.join(self.dirpdf,f"{self.bookname}.pdf")
        try:
        
            with open(filename, "wb") as file:
                file.write(img2pdf.convert([im for im in imagelist if im.endswith(".png")]))
            file.close()
            self.printsuccessful = True
            
        except:
            self.printsuccessful = False
            MessageBox(0, "If you have the PDF opened in another file, close it and try it again.", "Warning", ICON_EXCLAIM)
        TT.stop()
        
    else:
        pass
    self.m_TotalPDFPages.SetValue(str(''))
    self.m_TotalPDFPages.SetValue(str(len(self.allimages_v)))


def add_border(self,img,mode):
    if self.pdfline_bool == True:
        if mode == "single":
            new_im = PIL.Image.new("RGB", (self.a4page_w,img.size[1]+self.pdfline_thickness),"white")    
            border = PIL.Image.new("RGB", (img.size[0] ,self.pdfline_thickness), self.pdfline_color)    
        else:
            new_im = PIL.Image.new("RGB", (self.a4page_w,img.size[1]+self.pdfline_thickness),"white")    
            border = PIL.Image.new("RGB", (self.combinedwidth ,self.pdfline_thickness), self.pdfline_color)    
        new_im.paste(border, (0,img.size[1]))
        new_im.paste(img, (0,0))
        return new_im
    else:
        return img


def add_sideborder(self,img,mode):
    linesep = 5
    #self.maxheight = img.size[1]
    if  self.vertline_bool == True:        
        if mode == "left":
            new_size =  (img.size[0] + 2*self.vertline_thickness + 2*linesep ,self.maxheight )
            IMGPOS  = (linesep + self.vertline_thickness , 0)
            POS = (img.size[0] + self.vertline_thickness+2*linesep  ,0)
            
            new_im = PIL.Image.new("RGB", new_size,"white")
            border = PIL.Image.new("RGB", (self.vertline_thickness , self.maxheight), self.vertline_color)    
            new_im.paste(img, IMGPOS)
            new_im.paste(border, (0 ,0))
            new_im.paste(border, POS)
        else:
            new_size =  (img.size[0] + self.vertline_thickness + 3*linesep,self.maxheight )
            IMGPOS  = (0 , 0)
            #POS = (img.size[0] + 3*linesep  ,0)
            POS = (img.size[0] + int(2.8*linesep) ,0)
            new_im = PIL.Image.new("RGB", new_size,"white")
            border = PIL.Image.new("RGB", (self.vertline_thickness , self.maxheight), self.vertline_color)    
            new_im.paste(img, IMGPOS)
            new_im.paste(border, POS)
        return new_im
    else:
        return img



def add_sideborder(self,img,mode):
    linesep = 5
    #self.maxheight = img.size[1]
    if  self.vertline_bool == True:        
        if mode == "both":
            new_size =  (img.size[0] + 2*self.vertline_thickness + 2*linesep ,self.maxheight )
            IMGPOS  = (linesep + self.vertline_thickness , 0)
            POS = (img.size[0] + self.vertline_thickness+2*linesep  ,0)
            
            new_im = PIL.Image.new("RGB", new_size,"white")
            border = PIL.Image.new("RGB", (self.vertline_thickness , self.maxheight), self.vertline_color)    
            new_im.paste(img, IMGPOS)
            new_im.paste(border, (0 ,0))
            new_im.paste(border, POS)
        else:
            new_size =  (img.size[0] + self.vertline_thickness + 3*linesep,self.maxheight )
            IMGPOS  = (0 , 0)
            #POS = (img.size[0] + 3*linesep  ,0)
            POS = (img.size[0] + int(2.8*linesep) ,0)
            new_im = PIL.Image.new("RGB", new_size,"white")
            border = PIL.Image.new("RGB", (self.vertline_thickness , self.maxheight), self.vertline_color)    
            new_im.paste(img, IMGPOS)
            new_im.paste(border, POS)
        return new_im
    else:
        return img

    
def add_margins(self,img):
    margin = 0.05
    margin_pxs = round(margin * self.a4page_w)
    new_im = PIL.Image.new("RGB", (self.a4page_w + 2*margin_pxs, self.a4page_h + 2*margin_pxs),"white")    
    new_im.paste(img, (margin_pxs , margin_pxs))
    return new_im

# main program that does all the preprocessing
def startprogram(self,event): 
    self.runprogram   = True
    self.nr_questions = 0
    self.zoom     = 1
    self.chrono   = True
    self.index    = 0
    self.nr_cards = 0
    self.mode     = 'Question'    
    self.questions   = []
    self.answers     = []
    self.questions2  = []
    
    # open file
    try:
        if self.FilePickEvent == True:
            self.path     = self.fileDialog.GetPath()            
            self.filename = self.fileDialog.GetFilename()
            self.bookname = Path(self.filename).stem
    except:
        log.ERRORMESSAGE("Error: Couldn't open path")
    try:
        if os.path.exists(self.path):
            file = open(self.path, 'r')
            texfile = file.read()
        
        letterfile = str(texfile)
        # positions of Questions and Answers
        q_pos   = [m.start() for m in re.finditer(self.question_command, letterfile)]
        a_pos   = [m.start() for m in re.finditer(self.answer_command,   letterfile)]
        self.q_hookpos = list(np.array(q_pos) + len(self.question_command) - 2)              #position of argument \command{} q_pos indicates where it starts: "\", added the length of the command -2, because it counts 2 extra '\'
        self.a_hookpos = list(np.array(a_pos) + len(self.answer_command)   - 2)
        
        self.nr_cards = len(q_pos)
        self.nr_questions = len(q_pos)
    except:
        log.ERRORMESSAGE("Error: finding questions/answers")

    ## dialog display              
    self.chrono = True
    self.multiplier = 1    
    # display nr of questions and current index of questions            
    f2.LoadFlashCards(self, False,letterfile)
    notes2paper(self)
