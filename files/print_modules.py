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

def CreateTopicCard(self,key):
    bool_textcard, img_text = f2.TopicCard(self,key)
    if bool_textcard:
        return img_text
    else:
        return None

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


class SortImages():
    import numpy as np
    import bisect
    def __init__(self, library = None, page_width = 1240, page_height = 1754):
        sizelist = []
        
        for i,entry in enumerate(library):
            basiscard_i = entry['card']
            size = basiscard_i.getsize()
            sizelist.append(size)
        self.library = library    
        self.images_w = [x[0] for x in sizelist]
        self.images_s = sizelist
        print(colored(f"sizelist = {sizelist}","red"))
        
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
        
        cardname = self.library[0]['mode']+self.library[0]['line'] #t0/q0 
        basecard = self.library[0]['card']
        w,h = basecard.getsize()
        Rect = (self.page_x, self.page_y, w, h)
        dict_ = {cardname : Rect}
        dict_2 = {self.line_nr: [cardname]}
        dict_3 = {cardname: basecard}
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
        #print(colored(f"CUMSUMLEN {CUMSUMLEN}","green"))
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
        print(f"anton index = {index}")
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
    startprogram(self,event)
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
    """
    
    image = PIL.Image.open(self.allimages_v[0])
    image = image.resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS)
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    
    bitmapimage = wx.Bitmap(image2)
    self.m_bitmap3.SetBitmap(bitmapimage)
    self.Layout()
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    """
def preview_refresh(self):
    
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROWWAIT))
    notes2paper(self)
    #startprogram(self,event)
    _, PanelHeight = self.m_panel32.GetSize()
    PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
    #only select first page and display it on the bitmap
    #image = self.allimages_v[0]
    #image = PIL.Image.open(self.allimages_v[0])
    #image = image.resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS) 
    #image2 = wx.Image( image.size)
    #image2.SetData( image.tobytes() )
    #bitmapimage = wx.Bitmap(image2)
    #self.m_bitmap3.SetBitmap(bitmapimage)
    self.Layout()
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    
class pdfpage():
    def __init__(self,dict1,dict2,dict3,a4page_w,a4page_h):
        self.dict1 = dict1 #{pdfpage: {cardname : Rect}}
        self.dict2 = dict2 #{pdfpage: {self.line_nr:cardname}}
        self.dict3 = dict3 #{pdfpage: {cardname: basecard}}
        self.a4page_w = a4page_w
        self.a4page_h = a4page_h
        self.page_nr  = 0
        self.page_max = len(dict1.keys())-1
        self.vertline_bool = False
        self.horiline_bool = False
        self.vertline_thickness = 0
        self.horiline_thickness = 0
        self.vertline_color = (0,0,0)
        self.horiline_color = (0,0,0)
    def setvertline(self,color = (0,0,0), thickness = 0, visible = False):
        self.vertline_bool = visible
        self.vertline_thickness = thickness
        self.vertline_color = color
    def sethoriline(self,color = (0,0,0), thickness = 0, visible = False):
        self.horiline_bool = visible
        self.horiline_thickness = thickness
        self.horiline_color = color    
    def pagekey(self):
        return f"pdfpage{self.page_nr}"
    
    def loadpage(self,page_nr):
        #key = self.pagekey()
        key = f"pdfpage{page_nr}"
        linenumbers = self.dict2[key].keys()
        imcanvas = im = PIL.Image.new("RGB", (self.a4page_w ,self.a4page_h), 'white')
        
        
        for line in linenumbers:
            xpos = [0]
            linerect = (0,0,0,0)
            cards = self.dict2[key][line]
            for cardname in cards:
                print(f"anton : key {key}, cardname {cardname} line {line} , cards {cards}")
                
                basecard = self.dict3[key][cardname]
                im = basecard.createimage()
                
                x,y,w,h = self.dict1[key][cardname]
                xpos += [x]
                xpos += [x+w]
                linerect = (min(linerect[0],x),max(linerect[1],y),linerect[2]+w,max(linerect[3],h))
                imcanvas.paste(im,(x,y))
        
            if self.vertline_bool:
                #imcanvas.paste(PIL.Image.new("RGB", (self.vertline_thickness, linerect[3]), self.vertline_color), (linerect[0],linerect[1]))
                for x_i in xpos:
                    imcanvas.paste(PIL.Image.new("RGB", (self.vertline_thickness, linerect[3]), self.vertline_color), (x_i,linerect[1]))
                
            if self.horiline_bool:
                imcanvas.paste(PIL.Image.new("RGB", (linerect[2] ,self.horiline_thickness), self.horiline_color), (linerect[0],linerect[1]))
                imcanvas.paste(PIL.Image.new("RGB", (linerect[2] ,self.horiline_thickness), self.horiline_color), (linerect[0],linerect[1]+linerect[3]))
                #imcanvas.paste(PIL.Image.new("RGB", (linerect[3] ,self.horiline_thickness), self.horiline_color), (linerect[0]+linerect[2],linerect[1]))
        #imcanvas.show()
        return imcanvas
        
    def prevpage(self):
        if self.page_nr != 0:
            self.page_nr -= 1
    def nextpage(self):
        if self.page_nr != self.page_max:
            self.page_nr += 1
            
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
    
class basiscard():
    def __init__(self):
        self.basecoordinates = (0,0)
        self.displacement = (0,0) #how much each picture should be displaced wrt basecoordinates / when you add lines to the image
        self.total_width  = 0
        self.total_height = 0
        self.linecolor    = (0,0,0)
        
        self.topiccard    = False
        self.QAbool       = False
        self.pos_QAline   = 0
        self.QAline_thickness = 5
        self.textq = None#[path, size]
        self.picq  = None#[path, size]
        self.texta = None#[path, size]
        self.pica  = None#[path, size]
        self.bordersize = (0,0)
    def addbordersize(self,size):
        assert type(size) == tuple and len(size) == 2
        w,h = size
        self.bordersize = size
        #self.total_width  += w*2
        #self.total_height += h*2
        #w0,h0 = self.displacement
        #self.displacement = (w0+w,h0+h)
        #if self.QAbool:
        #    self.pos_QAline += h#what about w?
    def __str__(self):
        return f"textq = {self.textq} , picq = {self.picq} \n texta = {self.texta}, pica = {self.pica}\n topic = {self.topiccard} \n size = {self.total_width,self.total_height}"
    
    def settopic(self):
        self.topiccard = True
    
    def createimage(self):
        
        height = 0
        width  = 0
        im = PIL.Image.new("RGB", (self.total_width+self.bordersize[0]*2 ,self.total_height+self.bordersize[1]*2), 'white')
        
        d0 = self.displacement[0]+self.bordersize[0]
        d1 = self.displacement[1]+self.bordersize[1]
        if self.textq != None:
            path = self.textq[0]
            w,h = self.textq[1]
            im0 = PIL.Image.open(path).resize((w,h), PIL.Image.ANTIALIAS)
            im.paste(im0,(d0,d1))
            
            height += h
            width  += w
            d1 += h
        if self.picq != None:
            path = self.picq[0]
            w,h = self.picq[1]
            im0 = PIL.Image.open(path).resize((w,h), PIL.Image.ANTIALIAS)
            im.paste(im0,(d0,d1))
            height += h
            width  += w
            d1  += h
            
        if self.QAbool == True:
            self.pos_QAline = d1
            d1 += self.QAline_thickness
            height += self.QAline_thickness
            
        if self.texta != None:
            path = self.texta[0]
            w,h = self.texta[1]
            im0 = PIL.Image.open(path).resize((w,h), PIL.Image.ANTIALIAS)
            im.paste(im0,(d0,d1))
            
            height += h
            width  += w
            d1 += h
        if self.pica != None:
            path = self.pica[0]
            w,h = self.pica[1]
            im0 = PIL.Image.open(path).resize((w,h), PIL.Image.ANTIALIAS)
            im.paste(im0,(d0,d1))
            height += h
            width  += w
            d1 += h
        realw,realh = w,h
        if self.QAbool == True:
            im.paste(PIL.Image.new("RGB", (realw ,self.QAline_thickness), self.linecolor), (self.displacement[0],self.pos_QAline))
        
        return im
        
    def addsize(self,size):
        self.total_height += size[1] 
        self.total_width = max(self.total_width,size[0])
    
    def setq_text(self,path,size):
        self.textq = [path,size]
        self.addsize(size)
        self.pos_QAline += size[1]
    def setq_pic(self,path,size):
        self.picq = [path,size]
        self.addsize(size)
        self.pos_QAline += size[1]
    def seta_text(self,path,size):
        self.texta = [path,size]
        self.addsize(size)
        self.QAbool = True
    def seta_pic(self,path,size):
        self.pica = [path,size]
        self.addsize(size)
        self.QAbool = True
    def resize(self,size):
        Wp = size[0]/self.total_width
        Hp = size[1]/self.total_height
        self.total_width = size[0]
        #print(f"WpHp = {Wp,Hp}")
        #make sure that the dividing line between Q and A is NOT resized
        height = 0
        if self.textq != None:
            w,h = int(self.textq[1][0]*Wp) , int(self.textq[1][1]*Hp)
            self.textq = [self.textq[0],(w,h)]
            height += h
        if self.picq != None:
            w,h = int(self.picq[1][0]*Wp) , int(self.picq[1][1]*Hp)
            self.picq = [self.picq[0],(w,h)]
            height += h
        self.pos_QAline = height
        if self.texta != None:
            w,h = int(self.texta[1][0]*Wp) , int(self.texta[1][1]*Hp)
            self.texta = [self.texta[0],(w,h)]
            height += h
        if self.pica != None:
            w,h = int(self.pica[1][0]*Wp) , int(self.pica[1][1]*Hp)
            self.pica = [self.pica[0],(w,h)]    
            height += h
        self.total_height = height + self.QAline_thickness
        #print(f"totalsize = {self.total_width,self.total_height}")
        
    def getsize_ini(self):
        #when used the first time otherwise the QAline thickness is not included
        return self.total_width+self.QAline_thickness, self.total_height
    def getsize(self):
        return self.total_width+self.bordersize[0]*2, self.total_height+self.bordersize[1]*2
    def hasline(self):
        return self.QAbool
    def getrect(self):
        x,y = self.basecoordinates
        w,h = self.total_width,self.total_height
        return (x,y,w,h)
def createbasiscards(self,index,card_mode_nr,cardsdicts,library,CardsDeckEntries):
    #print(f"carkey_nr = {card_mode_nr}")
    #Entries may contain card_t0 / card_q0 / card_a0
    # initialize variables
    t = card_mode_nr[5:]
    line_nr = card_mode_nr[6:]
    #print(f"t = {t}")
    mode = getmode(card_mode_nr)
    currentcard = cardsdicts[card_mode_nr]
   
    basiscard_i = basiscard()    
    
    #print(f"anton mode = {mode}")
    
    if mode == 'Topic':
        
        basiscard_i.settopic()
        key = f"card_{t}"
        img_text = CreateTopicCard(self,key)
        imagename = f"temporary_{card_mode_nr}_{mode}.png"
        imagepathname = str(Path(self.tempdir, imagename))
        imgsize = img_text.size
        
        saveimage(img_text,imagepathname)
        basiscard_i.setq_text(imagepathname,imgsize)
        
    elif mode == 'Question':
        #print(f"keys = {currentcard.keys()}")
        if 'text' in currentcard.keys():
            #text = currentcard['text']
            bool_textcard, img_text = f2.CreateTextCard(self,'flashcard',card_mode_nr)
            if bool_textcard:
                img_text = f2.cropimage(img_text,0)    
                imagename = f"temporary_{card_mode_nr}_{mode}.png"
                imagepathname = str(Path(self.tempdir, imagename))
                
                imgsize = img_text.size
                saveimage(img_text,imagepathname)
                basiscard_i.setq_text(imagepathname,imgsize)
        if 'pic' in currentcard.keys():
            key = 'card_'+t
            FOUNDPIC, imagesize,path = findpicturesize(self,key)
            if FOUNDPIC:
                basiscard_i.setq_pic(path,imagesize)
        #MessageBox(0, f"{'a'+mode[1:]} , {CardsDeckEntries}", "Error", ICON_EXCLAIM)
        tempkey = 'card_a'+card_mode_nr[6:]
        if tempkey in CardsDeckEntries:
        
            print(f"currentcard.keys = {currentcard.keys()}")
            #if 'a'+mode[1:] in CardsDeckEntries:
            if 'text' in currentcard.keys():
                #text = currentcard['text']
                bool_textcard, img_text = f2.CreateTextCard(self,'flashcard',tempkey)
                if bool_textcard:
                    img_text = f2.cropimage(img_text,0)    
                    imagename = f"temporary_{tempkey}_{mode}.png"
                    imagepathname = str(Path(self.tempdir, imagename))
                    imgsize = img_text.size
                    saveimage(img_text,imagepathname)
                    basiscard_i.seta_text(imagepathname,imgsize)
            if 'pic' in currentcard.keys():
                
                FOUNDPIC, imagesize,path = findpicturesize(self,tempkey)
                if FOUNDPIC:
                    basiscard_i.seta_pic(path,imagesize)    
        
    #print(basiscard_i)
    library[index] = {'mode': mode[0].lower(), 'card': basiscard_i,'line':line_nr,'cardname': mode[0].lower()+line_nr,'size':basiscard_i.getsize()}
    #{'card0': {'textq': ['txt', (w,h)],'picq': ['path',(w,h)],'texta':['text':(w,h)],'pica':['path',(w,h)],'totalsize':(max(w),max(h)) }  }
    
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
    try:
        if self.FilePickEvent == True:
            self.path         = self.fileDialog.GetPath()      
            self.booknamepath = self.path
            self.filename     = self.fileDialog.GetFilename()
            self.bookname     = Path(self.filename).stem
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
    TT.update("Create the QA cards")
    """All text images are created and saved, and their [path,size] is stored 
    For all other pictures it only checks their sizes and stores [path,size] as well"""
    if self.onlyonce == 0:
        CardsDeckEntries = self.CardsDeck.getcards().keys()
        nrUnique   = self.CardsDeck.len_uniquecards()
        cardsdicts = self.CardsDeck.getcards()            
        checkcard  = [True] * nrUnique
        library    = [None] * nrUnique
        CardsDeckUniqueCards = [x for x in CardsDeckEntries if 'card_a' not in x]
        for index,card_mode_nr in enumerate(CardsDeckUniqueCards):
            if checkcard[index] == True:
                createbasiscards(self,index,card_mode_nr,cardsdicts,library,CardsDeckEntries)
        self.library = library
    self.onlyonce += 1
    #print(f"library = ")
    #[print(x) for x in library]
    #%% resize images    
    if hasattr(self,'library2'):
        delattr(self,'library2')
    self.library2 = self.library
    TT.update('resize all the images')
    
    if ColumnSliders(self) != []:
        columns = ColumnSliders(self)
        ColumnWidths = [int(col/100*self.a4page_w) for col in columns if col != 0]                       
        if len(ColumnWidths) > 0:
            for _idx_ , entrydict in enumerate(self.library2):
                if entrydict['mode'] == 't':
                    pass #don't resize
                    #resize topic card always to the pagewidth
                    #w,h = imgsize
                elif entrydict['mode'] == 'q':
                    basiscard_j = entrydict['card']
                    w,h = basiscard_j.getsize_ini()
                    if w > min(ColumnWidths) and w > 0:
                        NearestCol = min(ColumnWidths, key=lambda x:abs(x-w))
                        newsize = (int(NearestCol),int(NearestCol/w*h))
                        if newsize != (w,h):
                            #print(f"newsize = {newsize}")
                            basiscard_j.resize(newsize)
                            entrydict['card'] = basiscard_j
                            try:
                                assert entrydict['card'].getsize() == newsize
                            except AssertionError:
                                pass
                                #print(colored(f"Error: original{(w,h)} new: {newsize} vs {entrydict['card'].getsize()}","red"))
                            self.library2[_idx_] = entrydict
    
    #%% add border to the images:
    TT.update('add borders to all the images')
    if self.vertline_bool or self.pdfline_bool:
        for i,entrydict in enumerate(self.library2):
            if entrydict['mode'] != 't':
                basiscard_j = entrydict['card']
                width  = 0
                height = 0
                if self.vertline_bool:
                    width += self.vertline_thickness + self.linesep
                if self.pdfline_bool:
                    height += self.pdfline_thickness + self.linesep
                bordersize = (width,height)
                #print(f"bordersize = {bordersize}")
                #print(f"before = {basiscard_j.getsize()}")
                basiscard_j.addbordersize(bordersize)# anton hier zit het probleem
                #print(f"after = {basiscard_j.getsize()}\n")
                entrydict['card'] = basiscard_j
                self.library2[i] = entrydict
    
    if False:
        for i in range(5):
            print("original")
            entrydict = self.library2[i]
            print(entrydict['card'])
            #print("resized")
            
            #print(entrydict['card'])
      
    #%% sort images horizontally AND vertically
    TT.update("sort images over all pdf pages") 
    
    if hasattr(self,'SortImages'):
        delattr(self,'SortImages')
    
    self.SortImages = SortImages(library = self.library2, page_width = self.a4page_w, page_height = self.a4page_h)
    dct,dct2,dct3 = self.SortImages.sortpages()
    
    #%% create test page
    TT.update("create single pdf page") 
    if hasattr(self,'pdfpage'):
        delattr(self,'pdfpage')
    self.pdfpage = pdfpage(dct,dct2,dct3,self.a4page_w,self.a4page_h)
    self.pdfpage.setvertline(color = self.vertline_color , thickness = self.vertline_thickness,visible = self.vertline_bool)
    self.pdfpage.sethoriline(color = self.pdfline_color , thickness = self.pdfline_thickness,visible = self.pdfline_bool)
    pdfimage_i = self.pdfpage.loadpage(1)
    #print(f"dct = {dct}\ndct2 = {dct2}\ndct3 = {dct3}")
    
    #%% display result
    _, PanelHeight = self.m_panel32.GetSize()
    PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
    #only select first page and display it on the bitmap
    
    image = pdfimage_i
    image = image.resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS)
    image2 = wx.Image( image.size)
    image2.SetData( image.tobytes() )
    
    bitmapimage = wx.Bitmap(image2)
    self.m_bitmap3.SetBitmap(bitmapimage)
    self.Layout()
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
       
    self.allimages_v = [pdfimage_i]
    TT.update("create pdf") 
    #%% export to PDF file    
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    if self.printpreview == False:
        TT.update("writing files to pdf")
        filename = os.path.join(self.dirpdf,f"{self.bookname}.pdf")
        try:
            with open(filename, "wb") as file:
                #file.write(img2pdf.convert([im for im in imagelist if im.endswith(".png")]))
                file.write(img2pdf.convert([im for im in imagelist]))
            file.close()
            self.printsuccessful = True
        except:
            self.printsuccessful = False
            MessageBox(0, "If you have the PDF opened in another file, close it and try it again.", "Warning", ICON_EXCLAIM)
        TT.stop()
    
    self.m_TotalPDFPages.SetValue(str(''))
    self.m_TotalPDFPages.SetValue(str(len(self.allimages_v)))
    print("end "*3)
    TT.stop()
    
    
    
    

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
    notes2paper(self)
