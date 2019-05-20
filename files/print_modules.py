# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018
@author: Anton
"""
import bisect
import ctypes
import img2pdf
import fc_initialization as ini2
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
import fc_modules    as m2
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
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    
def preview_refresh(self):
    
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROWWAIT))
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
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    

  
def notes2paper(self):
    
     
    self.linesep = 5
    N = 1.3
    self.a4page_w  = round(1240*N*self.pdfmultiplier) # in pixels
    self.a4page_h  = round(1754*N*self.pdfmultiplier)
    self.paper_h      = []
    self.paper_h_list = []
    
    ## create images
    if self.onlyonce == 0:
        self.allimagepaths_QAbrackets = []
        self.allimagepaths_QAcombined = []
        
        self.allimagesizes_QAbrackets = []
        self.allimagesizes_QAcombined = []
        self.allimagesizes_resized_QAcombined = []
        
        if self.printpreview == True:
            if self.NrCardsPreview != '':
                nrQ = int(self.NrCardsPreview)
                if self.NrCardsPreview > self.nr_questions:
                    nrQ = self.nr_questions
            else:
                nrQ = self.nr_questions
        else:
            nrQ = self.nr_questions
        #self.nr_questions = 15
        self.cardorder = [x for x in range(self.nr_questions)]
        if len(self.cardorder) > 10:
            print(f"carorder = {self.cardorder[:10]}")
        else:
            print(f"carorder = {self.cardorder}")
        
    
    
    nrUnique = self.CardsDeck.len_uniquecards()
    
    #save individual cards
    def getmode(key):
        assert "card_" in key
        letter = key[5].lower()
        #print(f"letter = {letter}")
        if letter == 'q':
            return 'Question'
        elif letter == 'a':
            return 'Answer'
        elif letter == 't':
            return 'Topic'
        
    """ Create the cards """
    TT = Timing("Create the QA cards")
    
    if self.onlyonce == 0:
        keys = self.CardsDeck.getcards().keys()            
        threads       = [None] * len(keys)
        allimagepaths = []
        for i,key in enumerate(keys):            
            # initialize variables
            mode = getmode(key)
            self.mode = mode
            self.index = int(key[6:])
            #print(f"mode = {mode}\nnow at card: {key}\nindex = {self.index}")
            image     = None
            imagename = f"temporary_{key}.png"
            imagepathname = str(Path(self.tempdir, imagename))
            
            # create images
            if mode == 'Question' or mode == 'Answer':
                image,_ = f2.CreateSingularCard(self,mode)            
            elif mode == 'Topic':
                image = f2.CreateTopicCard(self)
            else:#invalid mode
                image = None
                MessageBox(0, f"Critical Error: invalid mode entered in line{self.index}", "Warning", ICON_EXCLAIM)    
            # Error:
            if mode == 'Question' and image == None:
                MessageBox(0, "Critical Error: question image should not be empty", "Warning", ICON_EXCLAIM)
            
            # save images    
            if image != None:
                if mode == 'Question':
                    allimagepaths.append([imagepathname])
                    self.allimagesizes_QAbrackets.append([image.size])
                if mode == 'Answer':
                    allimagepaths[-1].append(imagepathname)
                    self.allimagesizes_QAbrackets[-1].append(image.size)
                if mode == 'Topic':
                    allimagepaths.append(imagepathname)
                    self.allimagesizes_QAbrackets.append(image.size)
                threads[i] = threading.Thread(target = saveimage  , args=(image,imagepathname))
                threads[i].start()
        for i,thread in enumerate(threads):
            thread.join()
            
    
    
        """combine Q&A cards -- they will be combined as a list [path1,path2]"""
        for i,item in enumerate(allimagepaths):
            if type(item) == list and len(item) == 1:
                assert type(item[0]) == str
                allimagepaths[i] = item[0]
        #self.allimages = allimagepaths
        self.allimagepaths_QAbrackets = allimagepaths
    
           
    if len(self.allimagepaths_QAbrackets) > 10:
        print(f"allimages = {self.allimagepaths_QAbrackets[:10]}... ...")
    
    
    self.allimagepaths_QAcombined = self.allimagepaths_QAbrackets.copy()
    self.onlyonce += 1
    #%% combine question and answer cards and save them as a new card
    nrthreads = len([x for x in self.allimagepaths_QAcombined if (type(x) == list and len(x) == 2)])
    threads_save = [None] * nrthreads    
    self.allimagesizes_QAcombined = self.allimagesizes_QAbrackets.copy()
    j = 0
    for i,item in enumerate(self.allimagepaths_QAcombined):
        if type(item) == list and len(item) == 2:
            #initialize
            q_path = item[0]
            a_path = item[1]
            temp_path = q_path[:-4]+"_"+str(i)+".png"
            self.allimagepaths_QAcombined[i] = temp_path
            #get pictures
            image_a = None
            image_q = None
            try:
                #paths
                image_q = PIL.Image.open(q_path)
                image_a = PIL.Image.open(a_path)
                #images
                image_q = f2.cropimage(image_q,0)
                image_q = f2.cropimage(image_q,1)
                image_a = f2.cropimage(image_a,0)
                image_a = f2.cropimage(image_a,1)
            except:
                pass
            #combine pics
            if image_q != None and image_a != None:
                images = [image_q,image_a]
                #image sizes
                widths, heights = zip(*(im.size for im in images)) 
                max_width, total_height = max(widths), sum(heights)
                if self.QAline_bool == True:
                    new_im = PIL.Image.new('RGB', (max_width, total_height + self.QAline_thickness), "white")
                    line = PIL.Image.new('RGB', (image_q.size[0], self.QAline_thickness), self.QAline_color)
                    #combine images to 1
                    new_im.paste(images[0], (0,0))
                    new_im.paste(line,(0,image_q.size[1]))
                    new_im.paste(images[1], (0,image_q.size[1]+self.QAline_thickness))
                else:
                    #combine images to 1
                    new_im = PIL.Image.new('RGB', (max_width, total_height), "white")
                    new_im.paste(images[0], (0,0))
                    new_im.paste(images[1], (0,image_q.size[1]))
                
                IMG_QA = new_im
                self.allimagesizes_QAcombined[i] = IMG_QA.size
                threads_save[j] = threading.Thread(target = saveimage  , args=(IMG_QA,temp_path))
                threads_save[j].start()
                j+=1
                
    for _,thread in enumerate(threads_save):
        thread.join() 
    
    #remove superfluous brackets
    for _idx_ , item in enumerate(self.allimagesizes_QAcombined):
        if type(item) == list and len(item) == 1: 
            self.allimagesizes_QAcombined[_idx_] = item[0]
    
    self.allimagesizes_resized_QAcombined = self.allimagesizes_QAcombined.copy()
    #%%resize images    
    if ColumnSliders(self) != []:
        columns = ColumnSliders(self)
        ColumnWidths = [int(col/100*self.a4page_w) for col in columns if col != 0]                       
        if len(ColumnWidths) > 0:
            assert len(self.allimagesizes_resized_QAcombined) == len(self.allimagepaths_QAcombined)
            for _idx_ , imgsize in enumerate(self.allimagesizes_resized_QAcombined):
                if "card_t" not in self.allimagepaths_QAcombined[_idx_]: #topic cards should not be resized but should be page wide
                    w,h = imgsize
                    print(f"idx, imgsize ={_idx_}, {imgsize}")
                    print(f"w,col = {w},{min(ColumnWidths)}")
                    if w > min(ColumnWidths) and w > 0:
                        NearestCol = min(ColumnWidths, key=lambda x:abs(x-w))
                        self.allimagesizes_resized_QAcombined[_idx_] = (int(NearestCol),int(NearestCol/w*h))    
                else:
                    #resize topic card always to the pagewidth
                    w,h = imgsize
                    self.allimagesizes_resized_QAcombined[_idx_] = (int(self.a4page_w),int(self.a4page_w/w*h))
                    
    
    
    if len(self.allimagesizes_QAcombined) > 10:
        print("original")
        print(self.allimagesizes_QAcombined[:10])
        print("resized")
        print(self.allimagesizes_resized_QAcombined[:10])
    
    
    #add border next to the images
    if self.vertline_bool:
        for i,imgsize in enumerate(self.allimagesizes_resized_QAcombined):
            # Keep in mind the extra width needed for the vertical lines
            # Overestimate by 1 vertline_thickness to play it safe:            thickness << width of image
            imgsize = imgsize[0]+ 2*self.vertline_thickness + 2*5, imgsize[1]
            self.allimagesizes_resized_QAcombined[i] = imgsize
    
           
    #%% sort images horizontally
    TT.update("sort images horizontally")    
    
    paper_h_list = [] #list of paths
    allimages_w = [x[0] for x in self.allimagesizes_resized_QAcombined]
    allimages_h = [x[1] for x in self.allimagesizes_resized_QAcombined]
    allimages_s = self.allimagesizes_resized_QAcombined.copy()
    allimagepaths_QAcombined = self.allimagepaths_QAcombined.copy()
    
    CUMSUMLEN = np.cumsum(allimages_w)
    paper_h_list_sizes = []
    
    while len(allimages_w) != 0:        
        """Method:
        Cumsum the widths of images.
        Use bisect to look first instance where the cumsum is too large to fit on a page.
        Store those pages in a list separately, eliminate those from the search.
        Recalculate cumsum and repeat."""
        
        index = bisect.bisect_left(CUMSUMLEN, self.a4page_w) 
        #print(f"cumsumlen = {CUMSUMLEN} , {self.a4page_w}")
        if index == 0 and len(CUMSUMLEN) != 0: #image is too wide
            #rescale images that are too wide to fit on the page to the pagewidth
            w,h = allimages_s[0]      
            allimages_s[0] = (int(self.a4page_w),int(self.a4page_w/w*h))
            
            paper_h_list.append(allimagepaths_QAcombined[0])
            paper_h_list_sizes.append([allimages_s[0]])
            #
            allimagepaths_QAcombined   = allimagepaths_QAcombined[1:] 
            allimages_w = allimages_w[1:]
            allimages_h = allimages_h[1:]
            allimages_s = allimages_s[1:]
            CUMSUMLEN = np.cumsum(allimages_w)  
            
        elif index != len(CUMSUMLEN): #image is not too wide
            paper_h_list.append(allimagepaths_QAcombined[:index])
            paper_h_list_sizes.append(allimages_s[:index])
            #
            allimagepaths_QAcombined = allimagepaths_QAcombined[index:] 
            allimages_w = allimages_w[index:] 
            allimages_s = allimages_s[index:]
            CUMSUMLEN = np.cumsum(allimages_w)  
        elif index == len(CUMSUMLEN): # image is not too wide AND last in list
            paper_h_list.append(allimagepaths_QAcombined)
            paper_h_list_sizes.append(allimages_s)
            allimages_w = []
    if len(paper_h_list) >  10:
        print(f"paper_h_list = {paper_h_list[:5]} ... ...")
    
    #%% combine pics horizontally
    TT.update("combine pics horizontally")
    paper_h         = [None] * len(paper_h_list)
    paper_v_widths  = [None] * len(paper_h_list)
    paper_v_heights = [None] * len(paper_h_list)
    threads         = [None] * len(paper_h_list)
    
    def combine_h(self,paper_h_list_sizes,i,paths,paper_v_heights , paper_v_widths, paper_h):
        imagesizes = paper_h_list_sizes[i]
        cardtype = ''
        if type(paths) == list:
            # if there are multiple pics
            images = []
            for l,im in enumerate(paths):
                images.append(PIL.Image.open(im).resize(imagesizes[l], PIL.Image.ANTIALIAS))
        elif type(paths) == str:
            # if there is only 1 pic
            images = [PIL.Image.open(paths).resize(imagesizes[0], PIL.Image.ANTIALIAS)]
            if 'card_t' in paths:
                cardtype = "topiccard"                
        N = len(images)      
        widths, heights = zip(*(im.size for im in images)) 
        if self.vertline_bool:
            total_width = sum(widths) + (N+1)*self.vertline_thickness+2*N*self.linesep
            max_height  = max(heights)+2*self.linesep
            if cardtype == 'topiccard':
                total_width = sum(widths)
        else:
            total_width = sum(widths)
        if self.pdfline_bool:
            max_height = max(heights) + 2*self.pdfline_thickness+2*self.linesep
            if cardtype == 'topiccard':
                max_height = max(heights)
        else:
            max_height = max(heights)
        
        
        
        new_im = PIL.Image.new('RGB', (total_width, max_height), "white")
        #combine images to 1
        x_offset = 0
        for _,im in enumerate(images):
            if  self.vertline_bool == True:        
                if cardtype == 'topiccard':
                    linecolor = 'black'
                else:
                    linecolor = self.vertline_color
                border = PIL.Image.new("RGB", (self.vertline_thickness , max_height), linecolor)        
                new_im.paste(border, (x_offset,0))
                if cardtype == 'topiccard':#topic cards should not have white spaces
                    x_offset += self.vertline_thickness
                else:
                    x_offset += self.vertline_thickness + self.linesep
            
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0] + self.linesep           
        if self.vertline_bool:
            if cardtype == 'topiccard': #this is a bit strange and trying to fix the topic card for a problem that occurs for calculating x_offset
                if x_offset > im.size[0]:
                    x_offset = im.size[0]-self.vertline_thickness
            if cardtype == 'topiccard':
                pass
                #print(f"x_offset = {x_offset}, imsize = {im.size[0]}")
            if cardtype != 'topiccard':
                new_im.paste(border, (x_offset,0))            
                #print(f"x_offset = {x_offset}, imsize = {im.size[0]}")
        self.image = new_im
        pathname = str(Path(self.tempdir,f"temporary_p{i}.png"))
        saveimage(new_im,pathname)
        paper_h[i] = pathname
        paper_v_widths[i] = new_im.size[0]
        paper_v_heights[i] = new_im.size[1]        
        
    
    for i, paths in enumerate(paper_h_list):
        threads[i] = threading.Thread(target = combine_h  , args=(self,paper_h_list_sizes,i,paths,paper_v_heights , paper_v_widths, paper_h))
        threads[i].start()
        
    for _,thread in enumerate(threads):
        thread.join()
    
    #%% sort images vertically
    TT.update("sort images vertically")
    D = []    
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
    #print(f"widths {self.widthsperpage}")
    
    #%% combine vertical pictures per page
    TT.update("combine vertical pictures per page")
    imagelist = [None] * len(paper_h)
    threads   = [None] * len(paper_h)
    for page_i, images_on_page_i in enumerate(paper_h):        
        new_im = PIL.Image.new('RGB', (self.a4page_w, self.a4page_h), "white")        
        y_offset = 0
        x_offset = 0
        
        linelengths = calculate_pdflines(self.widthsperpage[page_i])
        for j, path in enumerate(images_on_page_i):    
            im = PIL.Image.open(path)
            
            if im.size[0] > self.a4page_w:
                """This shouldn't actually occur for some reason some row images are too wide for the page by just a few pixels
                ~20px compared to 1.500 px for the entire page width. Instead of trying to figure out where this occurs I just resize it here
                so it will appear nice and tidy on the pdf."""
                w,h = im.size
                size = (int(self.a4page_w),int(self.a4page_w/w*h))
                im = im.resize(size, PIL.Image.ANTIALIAS)
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
            if y_offset > self.a4page_h:
                """This should not occur, but for some reason it still does, this makes sure a pdfline is not cut off and invisible
                """
                y_offset = self.a4page_h-self.pdfline_thickness
            new_im.paste(line,(0,y_offset))
        
        
        
        self.combinedwidth = x_offset
        new_im = add_margins(self,new_im)
        pathname = str(Path(self.tempdir,f"temporary_h{page_i}.png"))
        imagelist[page_i] = pathname
        #save image
        threads[page_i] = threading.Thread(target = saveimage  , args=(new_im,pathname))
        threads[page_i].start()
    for _, thread in enumerate(threads):
        thread.join()
    self.allimages_v = imagelist
    
    print(f"imagelist is {imagelist}")
    #%% export to PDF file    
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
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
        
    self.m_TotalPDFPages.SetValue(str(''))
    self.m_TotalPDFPages.SetValue(str(len(self.allimages_v)))
    print("end "*3)

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
    ini2.initializeparameters(self) 
    # open file
    try:
        if self.FilePickEvent == True:
            self.path     = self.fileDialog.GetPath()            
            self.filename = self.fileDialog.GetFilename()
            self.bookname = Path(self.filename).stem
    except:
        log.ERRORMESSAGE("Error: Couldn't open path")
        
    try:
        linefile = f2.loadfile(self.path)
        cards = f2.File_to_Cards(self,linefile)                       # converts to raw cards
        self.CardsDeck.set_bookname(self.bookname)
        self.CardsDeck.set_cards(cards=cards,notesdir=self.notesdir)    
        
        self.nr_cards = len(self.CardsDeck)
        self.nr_questions = len(self.CardsDeck)
    except:
        log.ERRORMESSAGE("Error: finding questions/answers")

    ## dialog display              
    self.chrono = True
    self.multiplier = 1    
    # display nr of questions and current index of questions            
    #m2.LoadFlashCards(self, False,letterfile)
    print(self.nr_questions)
    
    notes2paper(self)
