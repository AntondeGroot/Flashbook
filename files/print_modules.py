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
import os
from PIL import Image
import PIL
import fb_functions as f
import fc_functions as f2
import print_functions as f3
import program as p
import program
import re
from termcolor import colored
import win32clipboard
from win32api import GetSystemMetrics
import wx


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
                    image.save(os.path.join(self.dir4,"screenshot.png"))
                    #convert back to wxBitmap
                    data = image.tobytes()
                    image3 = wx.Bitmap().FromBuffer(ScrWidth,ScrHeight,data)
                        
                    self.backupimage = image3
                    self.m_bitmap4.SetBitmap(image3)
                    program.SwitchPanel(self,4)
                    
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
    self.allimages_v = self.allimages_v[0].resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS)
    image2 = wx.Image( self.allimages_v.size)
    image2.SetData( self.allimages_v.tobytes() )
    bitmapimage = wx.Bitmap(image2)
    self.m_bitmap3.SetBitmap(bitmapimage)
    self.Layout()
    
def preview_refresh(self):
    notes2paper(self)
    #startprogram(self,event)
    _, PanelHeight = self.m_panel32.GetSize()
    PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
    #only select first page and display it on the bitmap
    self.allimages_v = self.allimages_v[0].resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS) 
    image2 = wx.Image( self.allimages_v.size)
    image2.SetData( self.allimages_v.tobytes() )
    bitmapimage = wx.Bitmap(image2)
    self.m_bitmap3.SetBitmap(bitmapimage)
    self.Layout()
    
def notes2paper(self):
    
    N = 1.3
    self.a4page_w  = round(1240*N*self.pdfmultiplier) # in pixels
    self.a4page_h  = round(1754*N*self.pdfmultiplier)
    self.paper_h      = []
    self.paper_h_list = []
    ## create images
    self.allimages   = []
    self.allimages_w = [] #widths
    
    """
    """
    for i in range(self.nr_questions):
        self.image_q = PIL.Image.new('RGB', (0, 0),"white")
        self.image_a = []
        for mode in ['Question','Answer']: 
            self.mode = mode
            self.TextCard = False      
            self.key = f'{self.mode[0]}{i}'
            try: # try to create a TextCard
                if self.key in self.textdictionary:
                    f3.CreateTextCardPrint(self)
                # if there is a textcard either combine them with a picture or display it on its own
                if self.TextCard == True: 
                    if self.key in self.picdictionary:
                        f2.CombinePicText(self)      
                    else:
                        self.image = self.imagetext                        
                        if mode == 'Question':
                            self.image_q = self.image
                        else:
                            self.image_a = self.image
                else: #if there is no textcard only display the picture
                    if self.key in self.picdictionary:
                        path = os.path.join(self.dir2, self.bookname ,self.picdictionary[self.key])
                        if os.path.isfile(path):
                            self.image = PIL.Image.open(path)
                        if mode == 'Question':
                            self.image_q = self.image
                        else:
                            self.image_a = self.image
            except:
                p.ERRORMESSAGE("Error: could not display card")  
        
        #combine question and answer:
        if self.image_a != []:
            images = [self.image_q,self.image_a]
            widths, heights = zip(*(i.size for i in images)) 
            total_height = sum(heights)
            max_width = max(widths)
            if self.QAline_bool == True:
                new_im = PIL.Image.new('RGB', (max_width, total_height + self.QAline_thickness), "white")
                line = PIL.Image.new('RGB', (round(0.7*max_width), self.QAline_thickness), self.QAline_color)
                #combine images to 1
                new_im.paste(images[0], (0,0))
                new_im.paste(line,(0,self.image_q.size[1]))
                new_im.paste(images[1], (0,self.image_q.size[1]+self.QAline_thickness))
            else:
                new_im = PIL.Image.new('RGB', (max_width, total_height), "white")
                #combine images to 1
                new_im.paste(images[0], (0,0))
                new_im.paste(images[1], (0,self.image_q.size[1]))
            
            
            
            self.image = new_im
            
        else:
            self.image = self.image_q
        
        ##anton
        if ColumnSliders(self) != []:
            columns = ColumnSliders(self)
            ColumnWidths = [int(col/100*self.a4page_w) for col in columns if col != 0]                       

            if len(ColumnWidths) > 0:
                w,h = self.image.size
                if w > min(ColumnWidths) and w > 0:
                    NearestCol = min(ColumnWidths, key=lambda x:abs(x-w))
                    self.image = self.image.resize((NearestCol,int(NearestCol/w*h)), PIL.Image.ANTIALIAS)
                
             
        
        
        self.allimages.append(self.image)
        self.allimages_w.append(self.image.size[0])
    # sort images horizontally
    A = np.cumsum(self.allimages_w)
    C = []
    while len(self.allimages_w) != 0:        
        """Method:
        Cumsum the widths of images.
        Use bisect to look first instance where the cumsum is too large to fit on a page.
        Store those pages in a list separately, eliminate those from the search.
        Recalculate cumsum and repeat."""
        
        index = bisect.bisect_left(A, self.a4page_w) 
        if index == 0 and len(A) != 0: #image is too wide
            im = self.allimages[0]
            C.append(im)
            self.allimages = self.allimages[1:] 
            self.allimages_w = self.allimages_w[1:] 
            A = np.cumsum(self.allimages_w)  
            
        elif index != len(A): #image is not too wide
            C.append(self.allimages[:index])
            self.allimages = self.allimages[index:] 
            self.allimages_w = self.allimages_w[index:] 
            A = np.cumsum(self.allimages_w)
            
        elif index == len(A): # image is not too wide AND last in list
            C.append(self.allimages)
            self.allimages_w = []
    self.paper_h_list = C
    
    # combine pics horizontally
    for i,images in enumerate(self.paper_h_list):
        try:
            widths, heights = zip(*(i.size for i in images)) 
            
            max_height = max(heights)
            total_width = sum(widths)
            
            new_im = PIL.Image.new('RGB', (total_width, max_height), "white")
            #combine images to 1
            x_offset = 0
            for im in images:
                new_im.paste(im, (x_offset,0))
                x_offset += im.size[0]
            self.image = new_im
            new_im = add_border(self,new_im)
            self.paper_h.append(new_im)
        except: # if only one picture left
            #print(images.size)
            if images.size[0] > self.a4page_w:
                w,h = images.size
                images = images.resize((self.a4page_w,int(h*self.a4page_w/w)))
            images = add_border(self,images)
            self.paper_h.append(images)
            
    #self.paper_h[0].show()    
    # sort images vertically
    D = []
    self.img_heights = []
    for img in self.paper_h:
        self.img_heights.append(img.size[1])
    
    A = np.cumsum(self.img_heights)
    if self.printpreview == False or self.printpreview == True:
        while len(self.img_heights) != 0:        
            index = bisect.bisect_left(A, self.a4page_h) #look for index where value is too large        
            if index != len(A):        
                D.append(self.paper_h[:index] )
                self.paper_h = self.paper_h[index:] 
                self.img_heights = self.img_heights[index:] 
                A = np.cumsum(self.img_heights)
                #print(A)
                #print("\n")      
            else:
                D.append(self.paper_h)
                self.img_heights = []
    else: # only look for 1st page (currently not in use)
        index = bisect.bisect_left(A, self.a4page_h) #look for index where value is too large        
        D.append(self.paper_h[:index] )
               
    self.paper_h = D
    
    # combine vertical pictures per page
    self.allimages_v = []
    
    for i,images in enumerate(self.paper_h):
        new_im = PIL.Image.new('RGB', (self.a4page_w, self.a4page_h), "white")        
        y_offset = 0
        try:
            for im in images:
                new_im.paste(im, (0,y_offset))
                y_offset += im.size[1]
            self.image = new_im
            new_im = add_margins(self,new_im)
            self.allimages_v.append(new_im)
        except: #if images is not an iterable it gives an error, it contains only 1 image so just add
            new_im.paste(images, (0,y_offset))
            new_im = add_margins(self,new_im)
            self.allimages_v.append(new_im)
    
    
    
    # imagelist is the list with all image filenames
    imagelist = self.allimages_v
    
    i = 0
    folder = []
    if self.printpreview == False:
        for image in imagelist:
            pathname = os.path.join(self.dir4,f"temporary{i}.png")
            folder.append(pathname)
            image.save(pathname)
            #image.show()
            i += 1
        filename = os.path.join(self.dirpdf,f"{self.bookname}.pdf")
        try:
            with open(filename, "wb") as file:
                file.write(img2pdf.convert([i for i in folder if i.endswith(".png")]))
            self.printsuccessful = True
        except:
            self.printsuccessful = False
            MessageBox(0, "If you have the PDF opened in another file, close it and try it again.", "Warning", ICON_EXCLAIM)
        
        # remove all temporary files of the form "temporary(...).png"    
        [os.remove(os.path.join(self.dir4,x)) for x in os.listdir(self.dir4) if ("temporary" in x and os.path.splitext(x)[1]=='.png' )]
        
    else:
        pass
    self.m_TotalPDFPages.SetValue(str(''))
    self.m_TotalPDFPages.SetValue(str(len(self.allimages_v)))

def dirchanged(self,event):
    #   INITIALIZE: ACQUIRE ALL INFO NECESSARY
    print(f"\nThe chosen path is {event.GetPath()}\n")
    try:
        path = event.GetPath() 
        # - keep track of "nrlist" which is a 4 digit nr 18-> "0018" so that it is easily sorted in other programs
        nrlist = []
        picnames = [d for d in os.listdir(path) if '.jpg' in d]
        nr_pics = len(picnames)
        for i in range(nr_pics):
            indexlist = []
            picname = picnames[i]
            SEARCH = True
            while SEARCH == True:
                for j in range(len(picname)): # can't simply use enumerate, we need to work backwards
                    
                    k = len(picname)-j-1
                    
                    if (f3.is_number(picname[k]) == True) and SEARCH == True:
                        indexlist.append(k)  
                    elif (f3.is_number(picname[k]) == False):
                        if j > 0:
                            if (f3.is_number(picname[k+1])) == True:
                                SEARCH = False
                    elif j == len(picname) - 1:
                        SEARCH = False
            indexlist.sort()
            len_nr = len(indexlist)
            # I only expect in the order of 1000 pages
            # make sure you can use the nrlist for later use so you can save the output as 
            # "Bookname + ****" a sorted 4 digit number
            if len_nr == 1:
                nrlist.append("000{}".format(picname[indexlist[0]]))
            elif len_nr == 0:
                print(f"found no number for {picname}")
            else:
                I = indexlist[0]
                F = indexlist[-1] + 1
                nrlist.append("0"*(4-len_nr)+"{}".format(picname[I:F]))
                       
        picnames = [x for _,x in sorted(zip(nrlist,picnames))]
        self.picnames = picnames
        self.bookname = path.replace(f"{self.dir3}","")[1:]#to remove '\'
        self.currentpage = 1
        
        self.PathBorders = os.path.join(self.dir5, self.bookname +'_borders.txt')
        
        if os.path.exists(os.path.join(self.temp_dir, self.bookname +'.txt')):
            file = open(os.path.join(self.temp_dir, self.bookname+'.txt'), 'r')
            self.currentpage = int(float(file.read()))    
        
        #create empty dictionary if it doesn't exist
        if not os.path.exists(self.PathBorders): #notna
            with open(self.PathBorders, 'w') as file:
                file.write(json.dumps({})) 
                
        self.nr_pics = nr_pics
        dirpath = os.path.join(self.dir2,self.bookname)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        
        self.m_CurrentPage.SetValue(str(self.currentpage))
        self.m_textCtrl5.SetValue(str(self.nr_pics))
        nrlist.sort()

        ## open dictionary if it exists
        try:
            with open(self.PathBorders, 'r') as file:
                self.dictionary = json.load(file)
        except:
            self.dictionary = {}
            print("no drawn rects found for this file, continue")
        try:
            self.jpgdir = os.path.join(self.dir3, self.bookname, self.picnames[self.currentpage-1])
            self.pageimage = PIL.Image.open(self.jpgdir)
            self.pageimagecopy = self.pageimage
            self.width, self.height = self.pageimage.size
        except:
            p.ERRORMESSAGE("Error: could not load scrolled window")
        
        #try to draw borders, but if there are no borders, do nothing
        if self.drawborders == True:                    
            f3.drawCoordinates(self)
             
        try:
            image2 = wx.Image( self.width, self.height )
            image2.SetData( self.pageimage.tobytes() )
            self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
            f3.SetScrollbars(self)
            

        except:
            p.ERRORMESSAGE("Error: could not load scrolled window")
    except:
        p.ERRORMESSAGE("Error: could not load image")






    

def SetKeyboardShortcuts(self):
    try:# look if Id's already exist
        # combine functions with the id
        self.Bind( wx.EVT_MENU, self.m_toolBackOnToolClicked,       id = self.Id_leftkey  )
        self.Bind( wx.EVT_MENU, self.m_toolNextOnToolClicked,       id = self.Id_rightkey )
        self.Bind( wx.EVT_MENU, self.m_enterselectionOnButtonClick, id = self.Id_enterkey )
        # combine id with keyboard = now keyboard is connected to functions
        entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL,  wx.WXK_LEFT, self.Id_leftkey),
                                      (wx.ACCEL_NORMAL,  wx.WXK_RIGHT, self.Id_rightkey),
                                      (wx.ACCEL_NORMAL,  wx.WXK_RETURN, self.Id_enterkey)])
        self.SetAcceleratorTable(entries)
    except:
        # set keyboard short cuts: accelerator table        
        self.Id_leftkey   = wx.NewIdRef() 
        self.Id_rightkey  = wx.NewIdRef() 
        self.Id_enterkey  = wx.NewIdRef()
        # combine functions with the id
        self.Bind( wx.EVT_MENU, self.m_toolBackOnToolClicked,       id = self.Id_leftkey  )
        self.Bind( wx.EVT_MENU, self.m_toolNextOnToolClicked,       id = self.Id_rightkey )
        self.Bind( wx.EVT_MENU, self.m_enterselectionOnButtonClick, id = self.Id_enterkey )
        
        # combine id with keyboard = now keyboard is connected to functions
        entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL,  wx.WXK_LEFT, self.Id_leftkey),
                                      (wx.ACCEL_NORMAL,  wx.WXK_RIGHT, self.Id_rightkey ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_RETURN, self.Id_enterkey )])
        self.SetAcceleratorTable(entries)

def RemoveKeyboardShortcuts(self):
    # combine functions with the id        
    self.Unbind( wx.EVT_MENU, self.m_toolBackOnToolClicked,       id = self.Id_leftkey  )
    self.Unbind( wx.EVT_MENU, self.m_toolNextOnToolClicked,       id = self.Id_rightkey )
    self.Unbind( wx.EVT_MENU, self.m_enterselectionOnButtonClick, id = self.Id_enterkey )
    # empty acceleratortable?
    self.SetAcceleratorTable()

"""
def SwitchBitmap(self): # checks if there is an answer card, if not changes mode back to question.
    if self.debugmode:
        print("f=switchbitmap")
    try:
        # you always start with a question, check if there is an answer:
        nr = self.cardorder[self.index]
        key = f'A{nr}' # do not use self.key: only check if there is an answer, don't change the key
        try:
            if key not in self.textdictionary and key not in self.picdictionary: # there is no answer card!
                self.mode = 'Question'
                self.SwitchCard = False        
                id = self.m_toolSwitch.GetId()
                self.m_toolBar11.SetToolNormalBitmap(id,wx.Bitmap( self.path_repeat_na, wx.BITMAP_TYPE_ANY ))        
            else:
                self.SwitchCard = True
                id = self.m_toolSwitch.GetId()
                self.m_toolBar11.SetToolNormalBitmap(id,wx.Bitmap( self.path_repeat, wx.BITMAP_TYPE_ANY ))
        except:
            p.ERRORMESSAGE("Error: could not switch bitmap #2")
    except:
        
        p.ERRORMESSAGE("Error: could not switch bitmap #1")
"""
def add_border(self,img):
    if self.pdfline_bool == True:
        new_im = PIL.Image.new("RGB", (self.a4page_w,img.size[1]+self.pdfline_thickness),"white")    
        border = PIL.Image.new("RGB", (self.a4page_w,self.pdfline_thickness), self.pdfline_color)    
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
    self.questions2  = []
    
    f3.SetScrollbars(self)    
    # open file
    try:
        if self.FilePickEvent == True:
            self.path     = self.fileDialog.GetPath()            
            self.filename = self.fileDialog.GetFilename()
            self.bookname = self.filename.replace(".tex","")
    except:
        p.ERRORMESSAGE("Error: Couldn't open path")
    try:
        if os.path.exists(self.path):
            file = open(self.path, 'r')
            texfile = file.read()
        
        self.letterfile = str(texfile)
        # positions of Questions and Answers
        q_pos   = [m.start() for m in re.finditer(self.question_command, self.letterfile)]
        a_pos   = [m.start() for m in re.finditer(self.answer_command,   self.letterfile)]
        self.q_hookpos = list(np.array(q_pos) + len(self.question_command) - 2)              #position of argument \command{} q_pos indicates where it starts: "\", added the length of the command -2, because it counts 2 extra '\'
        self.a_hookpos = list(np.array(a_pos) + len(self.answer_command)   - 2)
        
        self.nr_cards = len(q_pos)
        self.nr_questions = len(q_pos)
    except:
        p.ERRORMESSAGE("Error: finding questions/answers")

    ## dialog display              
    self.nr_questions = self.nr_cards
    self.chrono = True
    self.multiplier = 1    
    # display nr of questions and current index of questions            
    f2.LoadFlashCards(self, False)
    notes2paper(self)
