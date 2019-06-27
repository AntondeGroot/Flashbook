# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018
@author: Anton
"""
from settingsfile import settings
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
import latexoperations as ltx

def CreateTopicCard(self,key):
    bool_textcard, img_text = f2.TopicCard(self,key)
    if bool_textcard:
        return img_text
    else:
        return None

def findfullpicpath(self,picname):
    """Instead of just opening the path of a picture
    Try to find out if the path exists
    if it does not exist, try to look in all other folders.
    This problem may occur if you have combined several books.
    If the picture really doesn't exist, then the user gets notified with a messagebox."""
    FOUNDPIC = False    
    path = os.path.join(self.picsdir, self.bookname, picname)
    if os.path.exists(path):
        FOUNDPIC = True
        return path        
    else:
        folders = os.listdir(self.picsdir)
        for i,item in enumerate(folders):
            path = os.path.join(self.picsdir, item, picname)
            if os.path.exists(path):
                FOUNDPIC = True
                return path
    if FOUNDPIC == False:
        """Notify User and create a fake picture with the error message 
        as replacement for the missing picture."""        
        MessageBox(0, f"Error: Picture '{picname}' could not be found in any folder.", "Message", ICON_STOP)
            

def findpicturesize(self,key):
    """Instead of just opening the path of a picture
    Try to find out if the path exists
    if it does not exist, try to look in all other folders.
    This problem may occur if you have combined several books.
    If the picture really doesn't exist, then the user gets notified with a messagebox."""
    FOUNDPIC = False
    imagesize = None
    path = None
    #if key in self.picdictionary:
    if 'pic' in self.CardsDeck.getcards()[key].keys():
        picname = self.CardsDeck.getcards()[key]['pic']
        path = os.path.join(self.picsdir, self.bookname, picname)
        if os.path.exists(path):
            imagesize = PIL.Image.open(str(path)).size
            FOUNDPIC = True
        else:
            folders = os.listdir(self.picsdir)
            for i,item in enumerate(folders):
                path = os.path.join(self.picsdir, item, picname)
                if os.path.exists(path):
                    imagesize = PIL.Image.open(str(path)).size
                    FOUNDPIC = True
        if FOUNDPIC == False:
            """Notify User and create a fake picture with the error message 
            as replacement for the missing picture."""
            
            MessageBox(0, f"Error in line {str(int(key[6:])+1)} mode {key[0]}\nline: {picname}\nPicture could not be found in any folder.", "Message", ICON_STOP)
            
    else:
        #picture does not exist and should not exist, so this is fine
        pass
    return FOUNDPIC, imagesize, path

def createimage(self,card_i):
        
    print(f"card_i = {card_i} ,has t {'t' in card_i}")
    w,h = card_i['size']
    w,h = int(w),int(h)
    
    im = PIL.Image.new("RGB", (w,h), 'white')
    height = 0
    width  = 0
    
    if 'q' in card_i:
        quiz = card_i['q']
        qtext = ltx.argument(r"\\text{",quiz)
        qpic  = ltx.argument(r"\\pic{",quiz)    
    if 'a' in card_i:
        answer = card_i['a']
        atext = ltx.argument(r"\\text{",answer)
        apic  = ltx.argument(r"\\pic{",answer)  
    if 'a' not in card_i:
        atext = ''
        apic = ''
    if 't' in card_i:
        print("topic card created\n"*10)
        topic = card_i['t']
        #im = PIL.Image.new("RGB", (card_i['size']), 'white')
        #im = PIL.Image.new("RGB", (int(self.total_width*self.scale)+self.bordersize[0]*2 ,int(self.total_height*self.scale)+self.bordersize[1]*2+self.QAline_thickness), 'white')
        if topic != '':
            _, imagetext = f2.TopicCardFromText(self,topic)
            im = imagetext
        return im
    else:
        #d0 = self.displacement[0]+card_i['border'][0]
        #d1 = self.displacement[1]+card_i['border'][1]
        d0 = card_i['pos'][0]+card_i['border'][0]
        d1 = card_i['pos'][1]+card_i['border'][1]
        
        scale = card_i['scale']
        if qtext.strip() != '':
            
            #self.usertext = text
            #w,h = self.sizelist[0]
            #w,h = int(w*scale),int(h*scale)
            _, imagetext = f2.CreateTextCard(self,'manual',qtext)
            w,h = int(imagetext.size[0]*scale),int(imagetext.size[1]*scale)
            #_, imagetext = f2.CreateTextCard(self,'manual',qtext)
            im0 = imagetext.resize((w,h), PIL.Image.ANTIALIAS)
            #im0 = PIL.Image.open(path).resize((w,h), PIL.Image.ANTIALIAS)
            im.paste(im0,(d0,d1))
            
            height += h
            width  += w
            d1 += h
        if qpic.strip() != '':
            picname = qpic
            fullpath = findfullpicpath(self,picname)
            #w,h = card_i['size']#self.sizelist[1]
            #w,h = int(w*scale),int(h*scale)
            im0 = PIL.Image.open(fullpath)
            w,h = int(im0.size[0]*scale),int(im0.size[1]*scale)
            im0 = im0.resize((w,h), PIL.Image.ANTIALIAS)
            im.paste(im0,(d0,d1))
            height += h
            width  += w
            d1  += h
        """
        if self.QAbool == True and self.QAvisible:
            self.pos_QAline = d1
            d1 += self.QAline_thickness
            height += self.QAline_thickness
        """
        #print(f"texta = {self.pica}")
        if atext != '':
            #self.usertext = text
            #w,h = self.sizelist[2]
            #w,h = int(w*scale),int(h*scale)
            _, imagetext = f2.CreateTextCard(self,'manual',atext)
            
            w,h = int(imagetext.size[0]*scale),int(imagetext.size[1]*scale)
            im0 = imagetext.resize((w,h), PIL.Image.ANTIALIAS)
            #im0 = PIL.Image.open(path).resize((w,h), PIL.Image.ANTIALIAS)
            im.paste(im0,(d0,d1))
            height += h
            width  += w
            d1 += h
            
        if apic != '':
            picname = apic
            fullpath = findfullpicpath(self,picname)
            
            im0 = PIL.Image.open(fullpath)
            w,h = int(im0.size[0]*scale),int(im0.size[1]*scale)
            im0 = im0.resize((w,h), PIL.Image.ANTIALIAS)
            im.paste(im0,(d0,d1))
            height += h
            width  += w
            d1 += h
                
        return im

class SortImages():
    import numpy as np
    import bisect
    def __init__(self, library = None, page_width = 1240, page_height = 1754):
        sizelist = []
        
        for i,card_i in enumerate(library):
            size = card_i['size']
            sizelist.append(size)
        self.library = library    
        self.images_w = [x[0] for x in sizelist]
        self.images_s = sizelist
        #print(colored(f"sizelist = {sizelist}","red"))
        
        self.a4page_w = page_width
        self.a4page_h = page_height
        self.page_x  = 0
        self.page_y  = 0
        self.page_nr = 0
        self.line_nr = 0
        self.datadict = {}      # {pdfpagenr " {'q1': rect , ...}}
        self.datadict2 = {}     # {q1: basiscard}
        self.datadict3 = {}
        self.datadict_path = {} # {"q1" : c://.../name}
        self.rowindex = 0
    def newpage(self):
        self.page_x = 0
        self.page_y = 0
        self.page_nr += 1
    def getcardmode(self,path):
        if 'card_' in path:
            _idx = path.find('card_')
            _idx += len('card_')
            path = path[_idx:]
            if "_" in path:
                _idx = path.find('_')
            else:
                _idx = path.find('.png')
            answer = path[:_idx]
            return answer
        else:
            print(f"error: path")        
    def pdfpagename(self):
        return f'pdfpage{self.page_nr}'
    
    def savedata(self,w,h):
        def dictdictlist(self,key,subkey,val):
            if key not in self.datadict2.keys():
                val_list = [val]
                base = {subkey: val_list}
                self.datadict2[key] = base
            else:
                if subkey in self.datadict2[key].keys():
                    val_list = self.datadict2[key][subkey]
                    val_list += [val]
                    self.datadict2[key][subkey] = val_list
                    
                else:
                    val_list = [val]
                    base = {subkey: val_list}
                    self.datadict2[key].update(base)
        if 't' in self.library[0]:
            cardname = 't'+str(self.library[0]['index']) #t0/q0 
        else:
            cardname = 'q'+str(self.library[0]['index']) #t0/q0 
        
        w,h = self.library[0]['size']
        Rect = (self.page_x, self.page_y, w, h)
        dict_ = {cardname : Rect}
        dict_3 = {cardname: self.library[0]}
        pagekey = self.pdfpagename()
        
        #print(f"DATA DATA = {pagekey,dict_,cardname,cardpath}")
        
        if pagekey not in  self.datadict.keys():
            self.datadict[pagekey] = dict_
        else:
            self.datadict[pagekey].update(dict_)
            
        dictdictlist(self,pagekey,self.line_nr,cardname)    
        
        #print(f"dict 2 = {self.datadict2}")
        if pagekey not in  self.datadict3.keys():
            self.datadict3[pagekey] = dict_3
        else:
            self.datadict3[pagekey].update(dict_3)
    def removedata(self):
        self.images_w = self.images_w[1:]                
        self.images_s = self.images_s[1:]
        self.library  = self.library[1:]
        
    def sortpages(self):
        CUMSUMLEN = np.cumsum(self.images_w) 
        
        k = 0
        self.line_nr = 0
        while len(self.images_w) != 0: #continue until all pictures have been processed     
             
            """Method:
            Cumsum the widths of images.
            Use bisect to look first instance where the cumsum is too large to fit on a page.
            Store those pages in a list separately, eliminate those from the search.
            Recalculate cumsum and repeat."""            
            #combine horizontally until it doesn't fit on the page
            self.rowindex = bisect.bisect_left(CUMSUMLEN, self.a4page_w) 
            
            #print(f"card{k}")
            k += 1
            self.page_x = 0
            self.picindex = 0
            if self.rowindex == 0: # image is too wide
                print(colored(f"too wide {CUMSUMLEN[0]}","red"))
                # rescale
                w,h = self.images_s[0]    
                w_resized,h_resized = (int(self.a4page_w),int(self.a4page_w/w*h))
                # does it fit on the page?
                if self.page_y + h_resized > self.a4page_h: 
                    self.newpage()
                #
                
                self.savedata(w_resized,h_resized)
                #print(f"saved pagexy = {self.page_x,self.page_y}")
                self.removedata()                   # remove data from searchlist 
                self.page_x = 0
                self.page_y += h_resized
                self.line_nr += 1
                
                CUMSUMLEN = np.cumsum(self.images_w)  
            else:   # image(s) are combined not too wide
                #print(colored("not too wide","green"))
                #print(f"size = {self.images_s[:self.rowindex]}\n")
                h_max = max([x[1] for x in self.images_s[:self.rowindex]])
                #print(f"hmax = {h_max}")                
                if self.page_y + h_max > self.a4page_h:
                    
                    self.newpage()
                # save data
                pics = self.images_s[:self.rowindex]
                for i,sizetuple in enumerate(pics):
                    self.picindex = i
                    
                    w_i,h_i = sizetuple 
                    self.savedata(w_i,h_i)
                    self.page_x += w_i
                    self.removedata()
                    
                #self.removedata()
                self.page_x  = 0
                self.page_y += h_max
                self.line_nr += 1
                CUMSUMLEN = np.cumsum(self.images_w)  
            self.page_x = 0
            
            
        # finished
        return self.datadict, self.datadict2,self.datadict3

class pdfrow():
    def __init__(self):
        pass
    


class RectangleDetection():
    def __init__(self,dictionary):
        assert type(dictionary) == dict
        """INPUT: a dict {'name of rect1': coords1 , ... , 'name of rectN': coords N} WHERE coord = (x0,x1,y0,y1)
            then use method 'findRect' on a 2D point (x,y)
        """
        
        self.keydictionary = dictionary
        self.list = [x for x in dictionary.values()]
    def KeyFromValue(self,value):
        try:
            key_ = list(self.keydictionary.keys())[list(self.keydictionary.values()).index(value)]
            return key_
        except ValueError:
            return None    
    def distance(self,Rect, Pt):
        """Rect = (x,y,w,h)
           Pt   = (x,y)        """
         
        """ We can't solely rely on the L2norm to calculate whether a point Pt is in a Rect 
        For example: if we click inside a very large image when there is a small neighboring Rect adjacent to it.
        In that case the total length to all corners of the Rects will be much larger for the large Rect
        Instead we can first look at 3 corners, and our point needs to be within the x and y ranges of these points
        this won't be punished such that when we take the min() function this will give us the correct answer as this is the only scenario where the cost = 0.
        We will still use the L2norm for when you click outside all Rects but want to assign that click to the closest Rectangle"""
        
        try:
            assert len(Rect) == 4 and type(Rect) == tuple
            assert len(Pt) == 2   and type(Pt) == tuple
        except AssertionError:
            Rect, Pt = Pt, Rect
        cost = 0
        x,y,w,h = Rect
        pt1 = (x  , y  )
        pt2 = (x+w, y  )
        pt3 = (x  , y+h)
        def L2norm(p1,p2):
            return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2
        
        if (pt1[0] < Pt[0] < pt2[0]) == False:
            cost += L2norm(Pt,pt1)+ L2norm(Pt,pt2)
        if (pt1[1] < Pt[1] < pt3[1]) == False:
            cost += L2norm(Pt,pt1)+ L2norm(Pt,pt3)
            
        return cost
    
    def findRect(self,point):
        assert len(point) == 2 and type(point) == tuple
        NearestCoord = min(self.list, key=lambda x: self.distance(x, point))
        return self.KeyFromValue(NearestCoord), NearestCoord





#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MessageBox = ctypes.windll.user32.MessageBoxW
#win32api: total width of all monitors
SM_CXVIRTUALSCREEN = 78 

def getcardmode(path):
    
    if 'card_' in path:
        index = path.find('card_')
        index += len('card_')
        path = path[index:]
        if "_" in path:
            index = path.find('_')
        else:
            index = path.find('.png')
        #print(f"index = {index}")
        path = path[:index]
        return path
    else:
        print(f"error: path")






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
    notes2paper(self)
    #resize to A4 format
    _, PanelHeight = self.m_panel32.GetSize()
    PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
    #only select first page and display it on the bitmap
    
    image = self.allimages_v[0]
    image = image.resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS)
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    
    bitmapimage = wx.Bitmap(image2)
    self.m_bitmap3.SetBitmap(bitmapimage)
    self.Layout()
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    
def preview_refresh(self):
    print("preview refresh")
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROWWAIT))
    notes2paper(self)
    _, PanelHeight = self.m_panel32.GetSize()
    PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
    #only select first page and display it on the bitmap
    image = self.allimages_v[0]
    image = image.resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS) 
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    bitmapimage = wx.Bitmap(image2)
    self.m_bitmap3.SetBitmap(bitmapimage)
    
    self.Layout()
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    
class pdfpage(settings):
    def __init__(self,pagenr,dict1,dict2,dict3,a4page_w,a4page_h,tempdir = None,bookname = '', TT = ''):
        settings.__init__(self)
        self.LaTeXfontsize = 20
        self.bookname = bookname
        #print(self.LaTeXfontsize)
        self.dict1 = dict1 #{pdfpage_nr: {cardname : Rect}}
        self.dict2 = dict2 #{pdfpage_nr: {self.line_nr:cardname}}
        self.dict3 = dict3 #{pdfpage_nr: {cardname: basiscard}}
        self.a4page_w = a4page_w
        self.a4page_h = a4page_h
        self.page_nr  = pagenr
        self.page_max = len(dict1.keys())
        self.vertline_bool = False
        self.horiline_bool = False
        self.vertline_thickness = 0
        self.horiline_thickness = 0
        self.qaline_color   = (0,0,0)
        self.vertline_color = (0,0,0)
        self.horiline_color = (0,0,0)
        self.tempdir = tempdir
        self.TT = TT
        
    def get_cardrect(self):
        key = self.pagekey()
        return self.dict1[key]
    
    def add_margins(self,img):
        margin = 0.05
        margin_pxs = round(margin * self.a4page_w)
        new_im = PIL.Image.new("RGB", (self.a4page_w + 2*margin_pxs, self.a4page_h + 2*margin_pxs),"white")    
        new_im.paste(img, (margin_pxs , margin_pxs))    
        return new_im
    
    def getpage(self):
        return self.page_nr
    
    def setpage(self,nr):
        self.page_nr = nr
        
    def getpageinfo(self):
        return self.page_nr+1,self.page_max
    
    def setqaline(self,color = (0,0,0), thickness = 0 , visible = False):
        self.QAline_bool      = visible
        self.QAline_thickness = thickness
        self.QAline_color     = color
        
    def setvertline(self,color = (0,0,0), thickness = 0, visible = False):
        self.vertline_bool      = visible
        self.vertline_thickness = thickness
        self.vertline_color     = color
        
    def sethoriline(self,color = (0,0,0), thickness = 0, visible = False):
        self.horiline_bool      = visible
        self.horiline_thickness = thickness
        self.horiline_color     = color    
        
    def pagekey(self):
        return f"pdfpage{self.page_nr}"
    def createpdf(self):
        def threadfunction(self,i,pdflist):
            path = os.path.join(self.tempdir,f"temporary_pdfpage{i}.png")
            self.page_nr = i
            im = self.loadpage()
            w,h = im.size
            scale = 0.5
            im = im.resize((int(w*scale),int(h*scale)), PIL.Image.ANTIALIAS)
            im.save(path)
            pdflist[i] = path
            
        self.backuppage = self.page_nr
        pdflist = [] #contains all images
        if self.tempdir != None:
            threads = [None] * len(range(self.page_max))        
            pdflist = [None] * len(range(self.page_max))        
            for i in range(self.page_max):
                
                threads[i] = threading.Thread(target = threadfunction  , args=(self,i,pdflist))
                threads[i].start()
                                
            for i,thread in enumerate(threads):
                thread.join()
        self.page_nr = self.backuppage
        return pdflist
        
    def loadpage(self):
        key = f"pdfpage{self.page_nr}"
        linenumbers = self.dict2[key].keys()
        imcanvas = im = PIL.Image.new("RGB", (self.a4page_w ,self.a4page_h), 'white')        
        
        
        
        threads = [None]*len(linenumbers)
        
        im_pos = [] #im,pos
        self.TT.update("create images thread") 
        for i,line in enumerate(linenumbers):
            def threadfunction(self,line,key,im_pos):
                xpos = [0]
                ypos = [0]
                linerect = (0,0,0,0)
                #self.TT.update("single image created") 
                cards = self.dict2[key][line]
                for cardname in cards:
                    #print(f"cardinfo : key {key}, cardname {cardname} line {line} , cards {cards}")
                    card_i = self.dict3[key][cardname]
                    print(f"!test {line}, {cards}")
                    im = createimage(self,card_i)
                    
                    x,y,w,h = self.dict1[key][cardname]
                    im_pos.append({'im':im,'pos':(x,y)})
                    #y += self.horiline_thickness
                    xpos += [x]
                    xpos += [x+w]
                    ypos += [y]
                    ypos += [y+h]
                    linerect = (min(linerect[0],x),max(linerect[1],y),linerect[2]+w,max(linerect[3],h))
                    ##try:
                    ##    imcanvas.paste(im,(x,y))
                    ##except:
                    ##    print(f"error for {im,x}")
                    """
                    if self.QAline_bool and basiscard.hasQAline():
                        #both the program should have the QAline enabled AND the card should contain both Question and Answer
                        print("BASISCARD HAS QALINE")
                        im = PIL.Image.new("RGB", (w, self.QAline_thickness), self.QAline_color)
                        pos = (x,y+basiscard.QAlineposition())
                        im_pos.append('im':,'pos')
                    """
                    
                
                if len([x for x in cards if 't' in x]) == 0: #if it does not contain a topic card 'ti' 
                    if self.vertline_bool:
                        for x_i in xpos:
                            im = PIL.Image.new("RGB", (int(self.vertline_thickness), int(linerect[3])), self.vertline_color) 
                            pos = (x_i,linerect[1])
                            im_pos.append({'im':im,'pos':pos})
               
                    if self.horiline_bool:
                        #prints line at EVERY cards' bottom line across the whole page
                        if self.vertline_bool:
                            d = self.vertline_thickness
                        else:
                            d = 0
                        #imcanvas.paste(PIL.Image.new("RGB", (linerect[2]+d ,self.horiline_thickness), self.horiline_color), (linerect[0],linerect[1]))
                        im = PIL.Image.new("RGB", (linerect[2]+d ,self.horiline_thickness), self.horiline_color)
                        pos = (linerect[0],linerect[1])
                        im_pos.append({'im':im,'pos':pos})
                        #imcanvas.paste(PIL.Image.new("RGB", (linerect[2]+d ,self.horiline_thickness), self.horiline_color), (linerect[0],linerect[1]+linerect[3]))
                        im = PIL.Image.new("RGB", (linerect[2]+d ,self.horiline_thickness), self.horiline_color)
                        pos = (linerect[0],linerect[1]+linerect[3])
                        im_pos.append({'im':im,'pos':pos})
                
            threads[i] = threading.Thread(target = threadfunction  , args=(self,line,key,im_pos))
            threads[i].start()
            
        for i,thread in enumerate(threads):
            thread.join()
        #print(im_pos   )
        self.TT.update("pasting the images together")
        for i,item in enumerate(im_pos):
            im = item['im']
            pos = item['pos']
            imcanvas.paste(im,(int(pos[0]),int(pos[1])))
        self.TT.update("adding margins")
        imcanvas = self.add_margins(imcanvas)
        self.TT.update("adding margins2")
        return imcanvas
        
    def prevpage(self):
        if self.page_nr != 0:
            self.page_nr -= 1
        else: 
            self.page_nr = self.page_max - 1 
        return True
        
    def nextpage(self):
        if self.page_nr != self.page_max-1:
            self.page_nr += 1
        else:
            self.page_nr = 0
        return True
        
    def getmode(self):
        pass

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
    
class basiscard(settings):
    def __init__(self):
        settings.__init__(self)
        self.a4page_w  = round(1240*1.3)
        self.LaTeXfontsize = 20
        self.basecoordinates = (0,0)
        self.displacement = (0,0) #how much each picture should be displaced wrt basecoordinates / when you add lines to the image
        self.total_width  = 0
        self.total_height = 0
        self.linecolor    = (0,0,0)
        self.scale        = 1
        self.topiccard    = False
        self.QAbool       = False
        self.QAvisible    = False
        self.pos_QAline   = 0
        self.QAline_thickness = 0
        self.line = ''
        #self.textq = None  #[text, size]
        #self.picq  = None  #[path, size]
        #self.texta = None  #[text, size]
        #self.pica  = None  #[path, size]
        self.texttopic = None #[text, size]
        self.bordersize = (0,0)
        self.bookname = ''
    def setbookname(self, bookname):
        self.bookname = bookname
    def setQAthickness(self, thickness):
        self.QAline_thickness = thickness
        
    def combine_tuples(self,tuples_list):
        if type(tuples_list) == tuple:
            tuples_list = [tuples_list]
        w0,h0 = 0, 0 
        #print(tuples_list)
        for size in tuples_list:
            w,h = size
            w0 = max(w0,w)
            h0 += h
        return w0,h0
    def checkifanswer(self,tuples_list):
        if len(tuples_list) >= 4:
            tuples_list = tuples_list[2:4]
            w,h = self.combine_tuples(tuples_list)
            if (w,h) != (0,0):
                self.QAbool = True
            else:
                self.QAbool = False
   
    def hasQAline(self):
        return self.QAbool
    
    def QAlineposition(self):
        return self.pos_QAline
    
    def addbordersize(self,size):
        assert type(size) == tuple and len(size) == 2
        w,h = size
        self.bordersize = size
        
    def __str__(self):
        return f"textq = {self.textq} , picq = {self.picq} \n texta = {self.texta}, pica = {self.pica}\n topic = {self.topiccard} \n size = {self.total_width,self.total_height}"
    
    def setQAvisible(self,value):
        self.QAvisible = value
    
    def settopic(self,text,size):
        self.texttopic = [text,size]
        self.topiccard = True
    
    def createimage(self):
        self.TT('look for arguments')
        quiz = ltx.argument(r"\\quiz{",self.line)
        answer = ltx.argument(r"\\ans{",self.line)
        qtext = ltx.argument(r"\\text{",quiz)
        qpic  = ltx.argument(r"\\pic{",quiz)
        atext = ltx.argument(r"\\text{",answer)
        apic  = ltx.argument(r"\\pic{",answer)
        topic = ltx.argument(r"\\topic",self.line)
        height = 0
        width  = 0
        self.TT('look for ')
        #if not self.topiccard:
        #    im = PIL.Image.new("RGB", (int(self.total_width*self.scale)+self.bordersize[0]*2 ,int(self.total_height*self.scale)+self.bordersize[1]*2+self.QAline_thickness), 'white')
        #    return im
        d0 = self.displacement[0]+self.bordersize[0]
        d1 = self.displacement[1]+self.bordersize[1]
        if self.topiccard:
            self.LaTeXfontsize = 20
            if topic != '':
                _, imagetext = f2.TopicCardFromText(self,topic)
                im = imagetext
                imagetext.show()
        else:
            
            if qtext.strip() != '':
                #self.usertext = text
                w,h = self.sizelist[0]
                w,h = int(w*self.scale),int(h*self.scale)
                _, imagetext = f2.CreateTextCard(self,'manual',qtext)
                im0 = imagetext.resize((w,h), PIL.Image.ANTIALIAS)
                #im0 = PIL.Image.open(path).resize((w,h), PIL.Image.ANTIALIAS)
                im.paste(im0,(d0,d1))
                
                height += h
                width  += w
                d1 += h
            
            if qpic.strip() != '':
                picname = qpic
                fullpath = findfullpicpath(self,picname)
                w,h = self.sizelist[1]
                w,h = int(w*self.scale),int(h*self.scale)
                im0 = PIL.Image.open(fullpath).resize((w,h), PIL.Image.ANTIALIAS)
                im.paste(im0,(d0,d1))
                height += h
                width  += w
                d1  += h
                
            if self.QAbool == True and self.QAvisible:
                self.pos_QAline = d1
                d1 += self.QAline_thickness
                height += self.QAline_thickness
            
            #print(f"texta = {self.pica}")
            
            if atext != '':
                #self.usertext = text
                w,h = self.sizelist[2]
                w,h = int(w*self.scale),int(h*self.scale)
                _, imagetext = f2.CreateTextCard(self,'manual',atext)
                im0 = imagetext.resize((w,h), PIL.Image.ANTIALIAS)
                #im0 = PIL.Image.open(path).resize((w,h), PIL.Image.ANTIALIAS)
                im.paste(im0,(d0,d1))
                height += h
                width  += w
                d1 += h
             
            if apic != '':
                picname = apic
                fullpath = findfullpicpath(self,picname)
                w,h = self.sizelist[3]
                w,h = int(w*self.scale),int(h*self.scale)
                im0 = PIL.Image.open(fullpath).resize((w,h), PIL.Image.ANTIALIAS)
                im.paste(im0,(d0,d1))
                height += h
                width  += w
                d1 += h
                    
            return im
        
    def addsize(self,size):
        self.total_height += size[1]
        self.total_width = max(self.total_width,size[0])    
    
    def set_regularcard(self,line,size):
        self.sizelist = size
        self.checkifanswer(size)
        if self.QAbool and self.QAvisible:
            size.append((0,self.QAline_thickness))
        
        totalsize = self.combine_tuples(size)
        self.line = line
        self.cardsize = totalsize
        self.total_width = totalsize[0]
        self.total_height = totalsize[1]
        
    def set_topiccard(self,line,size):
        self.sizelist = size
        self.line = line
        self.texttopic = line
        self.topiccard = True
        
        totalsize = self.combine_tuples(size)
        self.cardsize = totalsize
        self.total_width = totalsize[0]
        self.total_height = totalsize[1]
        
    def resize(self,scale):
        self.scale = scale
    def getsize_withoutQA(self): #for rescaling purposes
        
        if self.QAvisible:
            extraThickness = self.QAline_thickness
        else:
            extraThickness = 0
        
        return self.total_width, self.total_height, extraThickness
        
    def getsize(self):
        if self.QAvisible:
            extraThickness = self.QAline_thickness
        else:
            extraThickness = self.QAline_thickness
        return int(self.total_width*self.scale)+self.bordersize[0]*2, int(self.total_height*self.scale)+self.bordersize[1]*2 + extraThickness
    def hasline(self):
        return self.QAbool
    def getrect(self):
        x,y = self.basecoordinates
        if self.QAvisible:
            extraThickness = self.QAline_thickness
        else:
            extraThickness = 0
        w,h = int(self.total_width*self.scale),int(self.total_height*self.scale)
        h += extraThickness
        return (x,y,w,h)
    
class checkcard():  
    
    def __init__(self):
        self.checkcard  = {}
        
    def initialize(self,dictionary):
        #print(f"checkcard dictionary is {dictionary}")
        """Each card has a key associated with it: card_t0 , card_q0, card_a3 etc."""
        assert type(dictionary) == dict
        #print(f"dictionary keys {dictionary.keys()}")
        ##
        keys = dictionary.keys()
        for i,card_mode_nr in enumerate(keys):
            number = card_mode_nr[6:]
            self.checkcard[number] = True
        #print(f"\ncheckcard initialized= {self.checkcard}")
        
    def set_True(self,index):
        index = str(index)
        self.checkcard[index] = True
        
    def alldone(self):
        for i,item in enumerate(self.checkcard):
            self.checkcard[item] = False
    def check_allQA(self,library):
        try:
            for i,libraryentry in enumerate(library):
                basiscard = libraryentry['card']
                if basiscard.hasQAline() == True:
                    index = i#libraryentry['cardname'][1:] #cardname is t0/q0/q1...
                    self.checkcard[index] = True
        except:
            pass
        
    def check_i(self,index):
        """INPUT: can either be 'card_q15' or just '15' 
        it's only important to know which Nth card it is"""
        try:
            int(index)
        except ValueError:
            index = index[6:]
            
        if index in self.checkcard:
            return self.checkcard[index]
        else:
            return False
        
            
    
def createbasiscards(self,index,card_mode_nr,cardsdicts,library,CardsDeckEntries):
    
    #Entries may contain card_t0 / card_q0 
    # initialize variables
    t = card_mode_nr[5:]
    line_nr = card_mode_nr[6:]
    
    mode = getmode(card_mode_nr)
    currentcard = cardsdicts[card_mode_nr] #cards are qi:{text: ... pic: ... size: ...}
    #print(f"cardsdicts = {cardsdicts}")
   
    basiscard_i = basiscard()
    basiscard_i.setbookname(self.bookname)    
    basiscard_i.setQAthickness(self.QAline_thickness)
    #print(f"mode = {mode}")
    ##print(f"current card is {currentcard}")
    size_of_card = currentcard['size']
    text = currentcard['text']     
    if mode == 'Topic':        
        basiscard_i.set_topiccard(text,size_of_card)                
    elif mode == 'Question':        
        basiscard_i.set_regularcard(text,size_of_card)
    
    self.library[index] = {'mode': mode[0].lower(), 'card': basiscard_i,'line':line_nr}#'cardname': mode[0].lower()+line_nr}
    
def notes2paper(self):
    #%% initialize
    """ initialize the cards """
    TT = Timing("Initialize the cards")
    ##initialize
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
    if self.onlyatinitialize == 0:
        
        try:
            if self.FilePickEvent == True:
                self.path         = self.fileDialog.GetPath()      
                self.booknamepath = self.path
                self.filename     = self.fileDialog.GetFilename()
                self.bookname     = Path(self.filename).stem
        except:
            log.ERRORMESSAGE("Error: Couldn't open path")
    self.onlyatinitialize += 1
    
    try:
        if self.bookname == '':
            self.bookname = os.path.splitext(os.path.basename(self.booknamepath))[0]
        TT.update("load the latexfile")
        self.Latexfile.loadfile(self.path)
        TT.update("Latex To cards")
        cards = self.Latexfile.file_to_rawcards() # cards contains keys: q,a,t,s
        #TT.update("Latexcards To cardsdeck")
        self.CardsDeck.set_bookname(self.bookname)
        self.CardsDeck.set_cards(cards=cards,notesdir=self.notesdir)   #cardsdeck contains ti, qi,ai
        
        #self.nr_cards = len(self.CardsDeck)
        #self.nr_questions = len(self.CardsDeck)
    except:
        log.ERRORMESSAGE("Error: finding questions/answers")
    
    
    ## dialog display              
    self.chrono = True
    self.multiplier = 1   
    #%%
    self.linesep = 5
    N = 1.3
    self.a4page_w  = round(1240*N*self.pdfmultiplier) # in pixels
    self.a4page_h  = round(1754*N*self.pdfmultiplier)
    
    if self.onlyonce == 0:
        #initialize
        self.cardorder = [x for x in range(self.nr_questions)]
        if len(self.cardorder) > 10:
            print(f"carorder = {self.cardorder[:10]}")
        else:
            print(f"carorder = {self.cardorder}")    
    nrUnique = self.CardsDeck.len_uniquecards()
    
    #%%    
    """ create all the individual images """
    TT.update("make checklist")
    # this can still be implemented to verify whether a specific card needs to be created 
    # or whether it already has been created. This might shave off 0.5 of 1.2 seconds on my laptop
    # but only shave off 0.05 of .2 seconds on my desktop

    TT.update('resize all the images')
    #print(f"\ncount is {cnt}")
    
    #assert None not in self.library2
    if ColumnSliders(self) != []:
        columns = ColumnSliders(self)
        ColumnWidths = [int(col/100*self.a4page_w) for col in columns if col != 0]                       
        if len(ColumnWidths) > 0:
            for _idx_ , card_i in enumerate(cards):
                if 't' in card_i:
                    pass #don't resize
                    #resize topic card always to the pagewidth
                    #w,h = imgsize
                else:
                    
                    w,h = card_i["size"]
                    if w > min(ColumnWidths) and w > 0:
                        NearestCol = min(ColumnWidths, key=lambda x:abs(x-w))
                        newsize = (int(NearestCol),int(NearestCol/w*h))
                        if newsize != (w,h):
                            #print(f"newsize = {newsize}")
                            scale = round(NearestCol/w,4)
                            card_i['scale'] = scale
                            card_i['size'] = (int(w*scale),int(h*scale))
                            if 'a' in card_i and self.QAline_bool:
                                card_i['size'] = (int(w*scale)+self.QAline_thickness,int(h*scale))    
                            
                            if self.vertline_bool or self.horiline_bool:
                                w,h = card_i["size"]
                                w0,h0 = 0,0
                                if self.vertline_bool:
                                    w0 = self.vertline_thickness + self.linesep
                                    #border_w += self.vertline_thickness
                                if self.horiline_bool:
                                    h0 = self.horiline_thickness + self.linesep
                                    #border_h += self.horiline_thickness
                                
                                card_i["border"] = (w0,h0)
                                card_i["size"] = (w+2*w0,h+2*h0)
                                
                                #anton resize if images is too wide for the page!!
                                
                cards[_idx_] = card_i
    

    #%% sort images horizontally AND vertically
    TT.update("sort images over all pdf pages") 
    
    if hasattr(self,'SortImages'):
        delattr(self,'SortImages')
    
    self.SortImages = SortImages(library = cards, page_width = self.a4page_w, page_height = self.a4page_h)
    dct,dct2,dct3 = self.SortImages.sortpages()
    
    #print(f"dict3 = {dct3}")
    #%% create test page
    TT.update("create single pdf page") 
    
    if hasattr(self,'pdfpage'):
        pagenr = self.pdfpage.getpage()
    else:
        pagenr = 0
    self.pdfpage = pdfpage(pagenr,dct,dct2,dct3,self.a4page_w,self.a4page_h,tempdir = self.tempdir,bookname = self.bookname, TT = TT)
    self.pdfpage.setqaline(  color = self.QAline_color   , thickness = self.QAline_thickness   , visible = self.QAline_bool  )
    self.pdfpage.setvertline(color = self.vertline_color , thickness = self.vertline_thickness , visible = self.vertline_bool)
    self.pdfpage.sethoriline(color = self.horiline_color , thickness = self.horiline_thickness , visible = self.horiline_bool)
    pdfimage_i = self.pdfpage.loadpage()
    #print(f"dct = {dct}\ndct2 = {dct2}\ndct3 = {dct3}")
    
    #%% display result
    TT.update("get panel size")
    _, PanelHeight = self.m_panel32.GetSize()
    PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
    TT.update("set panel size")
    self.m_panel32.SetSize((PanelWidth,PanelHeight))
    
    #only select first page and display it on the bitmap
    TT.update("image to bitmap resize")
    image = pdfimage_i
    
    #the following makes the transition smoother when the image is displayed on the bitmap, but it makes a difference of 0.2 sec of 1-1.3 sec omitting this makes it faster and more stable in runtime
    TT.update("set bitmap to gui")
    image2 = wx.Image( image.size)
    #TT.update("image set to bitmap")
    image2.SetData( image.tobytes() )
    self.m_bitmap3.SetBitmap(wx.Bitmap(image2)) #using setbitmap(wxbitmap) is either equally fast or a little faster than a = wxbitmap() and then doing setbitmap(a)
    
    
    
    TT.update("layout")
    self.Layout()
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
       
    self.allimages_v = [pdfimage_i]
    TT.update("create pdf") 
    #%% export to PDF file    
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    if self.printpreview == False:
        TT.update("writing files to pdf")
        filename = os.path.join(self.dirpdf,f"{os.path.splitext(os.path.basename(self.booknamepath))[0]}.pdf")
        
        try:
            imagelist = self.pdfpage.createpdf()
            with open(filename, "wb") as file:
                #file.write(img2pdf.convert([im for im in imagelist if im.endswith(".png")]))
                file.write(img2pdf.convert([im for im in imagelist]))
            file.close()
            self.printsuccessful = True
        except:
            log.ERRORMESSAGE("Error: Couldn't create pdf")
            self.printsuccessful = False
            MessageBox(0, "If you have the PDF opened in another file, close it and try it again.", "Warning", ICON_EXCLAIM)
        TT.stop()
    
    #page info
    currentpage, maxpage = self.pdfpage.getpageinfo()
    self.m_pdfCurrentPage.SetValue(f"{currentpage}/{maxpage}")
    
    TT.stop()


    
def add_margins(self,img):
    margin = 0.05
    margin_pxs = round(margin * self.a4page_w)
    new_im = PIL.Image.new("RGB", (self.a4page_w + 2*margin_pxs, self.a4page_h + 2*margin_pxs),"white")    
    new_im.paste(img, (margin_pxs , margin_pxs))
    
    return new_im
