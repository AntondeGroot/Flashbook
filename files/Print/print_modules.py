# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018
@author: Anton
"""
from _settings.settingsfile import settings
import bisect
import ctypes
import img2pdf
import numpy as np
from pathlib import Path
import os
from PIL import Image
import PIL
import program as p
import _logging.log_module as log
from termcolor import colored
import win32clipboard
from win32api import GetSystemMetrics
import wx
import threading
from _logging.timingmodule import Timing
import _shared_operations.latexoperations as ltx
import _shared_operations.imageoperations as imop
from _GUI.class_progressdialog import ProgressDialog

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
    if not FOUNDPIC:
        """Notify User and create a fake picture with the error message 
        as replacement for the missing picture."""        
        MessageBox(0, f"Error: Picture '{picname}' could not be found in any folder.", "Message", ICON_STOP)
            

def createimage(self,card_i):
    
    w,h = card_i['size']
    w,h = int(w),int(h)
    
    im = PIL.Image.new("RGB", (w,h), 'white')
    height = 0
    width  = 0
    
    if 'question' in card_i:
        qtext = card_i['questiontext']
        qpic = card_i['questionpic']
    if 'answer' in card_i:
        atext = card_i['answertext']
        apic = card_i['answerpic']
    
    #if 'answer' not in card_i:
    #    atext = ''
    #    apic = ''
    if 'topic' in card_i:
        
        topic = card_i['topic']
        #im = PIL.Image.new("RGB", (card_i['size']), 'white')
        #im = PIL.Image.new("RGB", (int(self.total_width*self.scale)+self.bordersize[0]*2 ,int(self.total_height*self.scale)+self.bordersize[1]*2+self.QAline_thickness), 'white')
        if topic != '':
            _, imagetext = imop.CreateTopicCard(self,topic)
            im = imagetext
            
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'PRINTMODULE: createimage: topic card is created')
        return im
    else:
        d0 = card_i['pos'][0]+card_i['border'][0]
        d1 = card_i['pos'][1]+card_i['border'][1]
        
        scale = card_i['scale']
        if qtext:
            _, imagetext = imop.CreateTextCard(self,qtext)
            w,h = int(imagetext.size[0]*scale),int(imagetext.size[1]*scale)
            im0 = imagetext.resize((w,h), PIL.Image.ANTIALIAS)
            im.paste(im0,(d0,d1))
            
            height += h
            width  += w
            d1 += h
        if qpic:
            picname = qpic
            fullpath = findfullpicpath(self,picname)
            im0 = PIL.Image.open(fullpath)
            w,h = int(im0.size[0]*scale),int(im0.size[1]*scale)
            im0 = im0.resize((w,h), PIL.Image.ANTIALIAS)
            im.paste(im0,(d0,d1))
            height += h
            width  += w
            d1  += h
            
        if (atext or apic) and self.QAline_bool:
            pos_QAline = d1
            d1 += self.QAline_thickness
            height += self.QAline_thickness
            
        if atext:
            #self.usertext = text
            #w,h = self.sizelist[2]
            #w,h = int(w*scale),int(h*scale)
            _, imagetext = imop.CreateTextCard(self,atext)
            
            w,h = int(imagetext.size[0]*scale),int(imagetext.size[1]*scale)
            im0 = imagetext.resize((w,h), PIL.Image.ANTIALIAS)
            #im0 = PIL.Image.open(path).resize((w,h), PIL.Image.ANTIALIAS)
            im.paste(im0,(d0,d1))
            height += h
            width  += w
            d1 += h
            
        if apic:
            picname = apic
            fullpath = findfullpicpath(self,picname)
            try:
                im0 = PIL.Image.open(fullpath)
                w,h = int(im0.size[0]*scale),int(im0.size[1]*scale)
                im0 = im0.resize((w,h), PIL.Image.ANTIALIAS)
                im.paste(im0,(d0,d1))
                height += h
                width  += w
                d1 += h
            except AttributeError:
                apic = ''
        #create qa line
        if (atext or apic) and self.QAline_bool:
            imline = PIL.Image.new("RGB", (width, self.QAline_thickness), self.QAline_color)
            im.paste(imline,(0,pos_QAline))
            
        
        return im

class SortImages():
    import numpy as np
    import bisect
    def __init__(self, library = None, page_width = 1240, page_height = 1754,debug = False):
        sizelist = []
        
        for i,card_i in enumerate(library):
            size = card_i['size']
            sizelist.append(size)
        self.library = library    
        self.images_w = [x[0] for x in sizelist]
        self.images_s = sizelist
        
        self.a4page_w = page_width
        self.a4page_h = page_height
        self.page_x  = 0
        self.page_y  = 0
        self.page_nr = 0
        self.line_nr = 0
        self.datadict = {}      # {pdfpagenr " {'q1': rect , ...}}
        self.datadict2 = {}     # 
        self.datadict3 = {}
        self.datadict_path = {} # {"q1" : c://.../name}
        self.rowindex = 0
        self.debugmode = debug
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
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'PRINTMODULE: sortimages: error in path = {path}')
            
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
        
        if pagekey not in  self.datadict.keys():
            self.datadict[pagekey] = dict_
        else:
            self.datadict[pagekey].update(dict_)
            
        dictdictlist(self,pagekey,self.line_nr,cardname)    
        
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
        while self.images_w: #continue until all pictures have been processed     
            """Method:
            Cumsum the widths of images.
            Use bisect to look first instance where the cumsum is too large to fit on a page.
            Store those pages in a list separately, eliminate those from the search.
            Recalculate cumsum and repeat."""            
            #combine horizontally until it doesn't fit on the page
            self.rowindex = bisect.bisect_left(CUMSUMLEN, self.a4page_w) 
            
            k += 1
            self.page_x = 0
            self.picindex = 0
            if self.rowindex == 0: # image is too wide
                log.DEBUGLOG(debugmode=self.debugmode, msg=f'PRINTMODULE: sortpages: too wide {CUMSUMLEN[0]}')
                # rescale
                w,h = self.images_s[0]    
                w_resized,h_resized = (int(self.a4page_w),int(self.a4page_w/w*h))
                # does it fit on the page?
                if self.page_y + h_resized > self.a4page_h: 
                    self.newpage()
                
                self.savedata(w_resized,h_resized)
                self.removedata()                   # remove data from searchlist 
                self.page_x = 0
                self.page_y += h_resized
                self.line_nr += 1
                
                CUMSUMLEN = np.cumsum(self.images_w)  
            else:   # image(s) are combined not too wide
                log.DEBUGLOG(debugmode=self.debugmode, msg=f'PRINTMODULE: sortpages: images are not too wide')
                h_max = max([x[1] for x in self.images_s[:self.rowindex]])
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
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'PRINTMODULE: sortpages: finished sorting')
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

def getcardmode(path):    
    if 'card_' in path:
        index = path.find('card_')
        index += len('card_')
        path = path[index:]
        if "_" in path:
            index = path.find('_')
        else:
            index = path.find('.png')
        path = path[:index]
        return path
    else:
        log.ERRORMESSAGE(f'PRINTMODULE: error in path {path}')

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


    

def print_preview(self): 
    log.DEBUGLOG(debugmode=self.debugmode, msg=f'PRINTMODULE: preview refreshed')
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROWWAIT))
    notes2paper(self)
    self.Layout()
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    
    
class pdfpage(settings):
    def __init__(self,pagenr,DICT_page_card_rect, DICT_page_line_card,dict3,a4page_w,a4page_h,tempdir = None,bookname = '', TT = '',debug = False):
        settings.__init__(self)
        self.LaTeXfontsize = 20
        self.bookname = bookname
        self.DICT_page_card_rect = DICT_page_card_rect #{pdfpage_nr: {cardname : Rect}}
        self.DICT_page_line_card = DICT_page_line_card #{pdfpage_nr: {self.line_nr:cardname}} 
        self.dict3 = dict3 #{pdfpage_nr: {cardname: ]}}
        
        self.a4page_w = a4page_w
        self.a4page_h = a4page_h
        self.page_nr  = pagenr
        self.page_max = len(DICT_page_card_rect.keys())
        self.vertline_bool = False
        self.horiline_bool = False
        self.vertline_thickness = 0
        self.horiline_thickness = 0
        self.qaline_color   = (0,0,0)
        self.vertline_color = (0,0,0)
        self.horiline_color = (0,0,0)
        self.tempdir = tempdir
        self.TT = TT
        self.debugmode = debug
        
    def get_cardrect(self):
        key = self.pagekey()
        return self.DICT_page_card_rect[key]
    
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
            #scale = 0.5 #this determines the resolution / dpi of the final pdf page
            scale = 1
            im = im.resize((int(w*scale), int(h*scale)), PIL.Image.ANTIALIAS)
            im.save(path)
            pdflist[i] = path
            
            
        self.backuppage = self.page_nr
        pdflist = [] #contains all images
        if self.tempdir:
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
        try:
            linenumbers = self.DICT_page_line_card[key].keys()
        except KeyError:
            self.page_nr -= 1
            key = f"pdfpage{self.page_nr}" #the current page no longer exists, look a page before it
            linenumbers = self.DICT_page_line_card[key].keys()
            
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
                cards = self.DICT_page_line_card[key][line]
                for cardname in cards:
                    card_i = self.dict3[key][cardname]
                    im = createimage(self,card_i)
                    
                    x,y,w,h = self.DICT_page_card_rect[key][cardname]
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
                    ##   error message
                    """
                    if self.QAline_bool:
                        #both the program should have the QAline enabled AND the card should contain both Question and Answer
                        
                        imline = PIL.Image.new("RGB", (w, self.QAline_thickness), self.QAline_color)
                        im_pos.append({'im':im,'pos':(x,y)})
                        #pos = (x,y+...)
                        #im_pos.append({'im':im,'pos':pos})
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
        if self.page_nr:
            self.page_nr -= 1
        else: #Go back to the last page
            self.page_nr = self.page_max - 1 
        
    def nextpage(self):
        if self.page_nr != self.page_max-1:
            self.page_nr += 1
        else:
            self.page_nr = 0
        
    def getmode(self):
        pass

def getmode(key):
    assert "card_" in key
    letter = key[5].lower()
    if letter == 'q':
        return 'Question'
    elif letter == 'a':
        return 'Answer'
    elif letter == 't':
        return 'Topic'
    
    
def notes2paper(self):
    log.DEBUGLOG(debugmode=self.debugmode, msg=f'PRINTMODULE: notes2paper: panel size = {self.m_panel32.GetSize()}')
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
    # open file
    if self.onlyatinitialize == 0:
        
        try:
            if self.FilePickEvent:
                self.path         = self.fileDialog.GetPath()      
                self.booknamepath = self.path
                self.filename     = self.fileDialog.GetFilename()
                self.bookname     = Path(self.filename).stem
        except:
            log.ERRORMESSAGE("Error: Couldn't open path")
    self.onlyatinitialize += 1
    
    
    
    
    if self.bookname == '':
        self.bookname = os.path.splitext(os.path.basename(self.booknamepath))[0]
    TT.update("load the latexfile")
    self.Cardsdeck.loaddata(book = self.bookname)
    TT.update("Latex To cards")
    cards = self.Cardsdeck.getallcards() # cards contains keys: q,a,t,s

    
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
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'PRINTMODULE: notes2paper: cardorder first 10 cards = {self.cardorder[:10]}')
        else:
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'PRINTMODULE: notes2paper: cardorder = {self.cardorder}')
    
    #%%    
    """ create all the individual images """
    TT.update("make checklist")
    # this can still be implemented to verify whether a specific card needs to be created 
    # or whether it already has been created. This might shave off 0.5 of 1.2 seconds on my laptop
    # but only shave off 0.05 of .2 seconds on my desktop

    TT.update('resize all the images')
    if ColumnSliders(self) != []:
        columns = ColumnSliders(self)
        ColumnWidths = [int(col/100*self.a4page_w) for col in columns if col != 0]                       
        if len(ColumnWidths) > 0:
            for _idx_ , card_i in enumerate(cards):
                if 't' in card_i:
                    pass #don't resize
                    w,h = card_i["size"]
                    card_i['size'] = (self.a4page_w,h)
                else:                    
                    w,h = card_i["size"]
                    if w > min(ColumnWidths) and w > 0:
                        NearestCol = min(ColumnWidths, key=lambda x:abs(x-w))
                        newsize = (int(NearestCol),int(NearestCol/w*h))
                        if newsize != (w,h):
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
                cards[_idx_] = card_i   

    #%% sort images horizontally AND vertically
    TT.update("sort images over all pdf pages") 
    
    if hasattr(self,'SortImages'):
        delattr(self,'SortImages')
    
    self.SortImages = SortImages(library = cards, page_width = self.a4page_w, page_height = self.a4page_h,debug = self.debugmode)
    DICT_page_card_rect, DICT_page_line_card, dct3 = self.SortImages.sortpages()
    
    
    #%% create test page
    TT.update("create single pdf page") 
    
    if hasattr(self,'pdfpage'):
        pagenr = self.pdfpage.getpage()
    else:
        pagenr = 0
    self.pdfpage = pdfpage(pagenr, DICT_page_card_rect, DICT_page_line_card, 
                           dct3,self.a4page_w,self.a4page_h,tempdir = self.tempdir,bookname = self.bookname, TT = TT,debug = self.debugmode)
    self.pdfpage.setqaline(  color = self.QAline_color   , thickness = self.QAline_thickness   , visible = self.QAline_bool  )
    self.pdfpage.setvertline(color = self.vertline_color , thickness = self.vertline_thickness , visible = self.vertline_bool)
    self.pdfpage.sethoriline(color = self.horiline_color , thickness = self.horiline_thickness , visible = self.horiline_bool)
    pdfimage_i = self.pdfpage.loadpage()
    
    #%% display result
    TT.update("get panel size")
    _, PanelHeight = self.m_panel32.GetSize()
    PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
    TT.update("set panel size")
    self.m_panel32.SetSize((PanelWidth,PanelHeight))
    
    #only select first page and display it on the bitmap
    TT.update("image to bitmap resize")
    image = pdfimage_i
    image = image.resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS)
    #the following makes the transition smoother when the image is displayed on the bitmap, but it makes a difference of 0.2 sec of 1-1.3 sec omitting this makes it faster and more stable in runtime
    TT.update("set bitmap to gui")
    image2 = wx.Image( image.size)
    TT.update("image set to bitmap")
    image2.SetData( image.tobytes() )
    self.m_bitmap3.SetBitmap(wx.Bitmap(image2)) #using setbitmap(wxbitmap) is either equally fast or a little faster than a = wxbitmap() and then doing setbitmap(a)
    
    #%%
    TT.update("layout")
    self.Layout()
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))   
    self.allimages_v = [pdfimage_i]
    TT.update("create pdf") 
    
    #%% export to PDF file    
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    if not self.printpreview:
        TT.update("writing files to pdf")
        dlg = ProgressDialog(title='Writing files to pdf',msg='This may take a minute')
        filename = os.path.join(self.dirpdf,f"{os.path.splitext(os.path.basename(self.booknamepath))[0]}.pdf")
        dlg.Pulse()
        try:
            imagelist = self.pdfpage.createpdf()
            with open(filename, "wb") as file:
                #file.write(img2pdf.convert([im for im in imagelist if im.endswith(".png")]))
                file.write(img2pdf.convert([im for im in imagelist]))
            file.close()
            self.printsuccessful = True
            dlg.Destroy()
        except:
            log.ERRORMESSAGE("Error: Couldn't create pdf")
            self.printsuccessful = False
            MessageBox(0, "If you have the PDF opened in another file, close it and try it again.", "Warning", ICON_EXCLAIM)
            dlg.Destroy()
        TT.stop()
    #page info
    currentpage, maxpage = self.pdfpage.getpageinfo()
    self.m_pdfCurrentPage.SetValue(f"{currentpage}/{maxpage}")
    self.Layout()
    self.Update()
    self.Refresh()
    TT.stop()

    
def add_margins(self,img):
    margin = 0.05
    margin_pxs = round(margin * self.a4page_w)
    new_im = PIL.Image.new("RGB", (self.a4page_w + 2*margin_pxs, self.a4page_h + 2*margin_pxs),"white")    
    new_im.paste(img, (margin_pxs , margin_pxs))
    
    return new_im
