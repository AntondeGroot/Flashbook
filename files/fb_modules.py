# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018
@author: Anton
"""
from random import randint
from termcolor import colored
import numpy as np
import PIL
import wx
import os
import fb_functions as f
import program as p
import json
import ctypes

#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW


def dirchanged(self,event):
    
    """For scrolling: only remember last few positions, append and pop 
    if the numbers repeat [0,...,0] or [X,...,X] then you know you've reached either 
    the beginning or the end of the window: then flip page"""
    
    self.scrollpos_reset = [5, 4, 3, 2, 1]     
    self.scrollpos = self.scrollpos_reset
    
    #Keep track of "nrlist" which is a 4 digit nr 18-> "0018" so that it is easily sorted in other programs
    path = event.GetPath()
    print(f"path is {path}")
    nrlist = []
    picnames = [pic for pic in os.listdir(path) if os.path.splitext(pic)[1] == '.jpg']
    self.nr_pics = len(picnames)
    print(f"nr pics is {self.nr_pics} ")
    if self.nr_pics == 0:
        MessageBox(0, " The selected folder does not contain any images!", "Error", MB_ICONINFORMATION)
    
    for _, picname in enumerate(picnames):
        
        SEARCH    = True
        name_len  = len(picname)
        indexlist = []
        while SEARCH == True:
            for j in range(name_len):
                k = name_len - j - 1                
                if (f.is_number(picname[k]) == True) and SEARCH == True:
                    indexlist.append(k)  
                elif (f.is_number(picname[k]) == False):
                    if j > 0:
                        if (f.is_number(picname[k+1])) == True:
                            SEARCH = False
                elif j == name_len - 1: #EOS
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
            nrlist.append("0"*(4-len_nr) + f"{picname[I:F]}")
    picnames = [x for _,x in sorted(zip(nrlist,picnames))]
    self.picnames = picnames
    self.bookname = os.path.basename(path)
    self.booknamepath = path.replace(self.dir3,"")[1:]
    print(f"path = {path}   bookpath = {self.booknamepath}   bookname {self.bookname}")
    self.currentpage = 1
    self.PathBorders = os.path.join(self.dir5, self.bookname + '_borders.txt')
    if os.path.exists(os.path.join(self.temp_dir, self.bookname + '.txt')):
        file = open(os.path.join(self.temp_dir, self.bookname + '.txt'), 'r')
        self.currentpage = int(float(file.read()))    
    
    #Create empty dictionary if it doesn't exist
    if not os.path.exists(self.PathBorders):
        with open(self.PathBorders, 'w') as file:
            file.write(json.dumps({})) 
    
    book_dir = os.path.join(self.dir2,self.bookname)
    if not os.path.exists(book_dir):
        os.makedirs(book_dir)
    
    self.m_CurrentPage11.SetValue(str(self.currentpage))
    self.m_TotalPages11.SetValue(str(self.nr_pics))
    nrlist.sort()
    
    #Open dictionary if it exists
    try:
        with open(self.PathBorders, 'r') as file:
            self.dictionary = json.load(file)
    except:
        self.dictionary = {}
        print("No drawn rects found for this file, continue")
    try: 
        self.jpgdir    = os.path.join(self.dir3, self.booknamepath, self.picnames[self.currentpage-1])
        print(self.booknamepath,self.dir3)
        self.pageimage = PIL.Image.open(self.jpgdir)
        self.pageimagecopy = self.pageimage
        self.width, self.height = self.pageimage.size
    except:
        p.ERRORMESSAGE("Error : could not load scrolled window 1")
        
    #Draw borders if they exist
    try:
        if self.drawborders == True:                    
            f.drawCoordinates(self)
    except:
        p.ERRORMESSAGE("Error: could not draw borders")
                  
    try:
        image2 = wx.Image( self.width, self.height )
        image2.SetData( self.pageimage.tobytes() )
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        f.SetScrollbars(self)
    except:
        p.ERRORMESSAGE("Error: could not load scrolled window 2")
    self.Layout()
    
def bitmapleftup(self,event):
    if self.cursor == False:
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    self.panel_pos2 = self.m_bitmapScroll.ScreenToClient(wx.GetMousePosition())
    
    x0, y0 = self.panel_pos
    x1, y1 = self.panel_pos2
    #rescale
    x0 = int(x0/self.zoom)
    y0 = int(y0/self.zoom)
    x1 = int(x1/self.zoom)
    y1 = int(y1/self.zoom)
    
    if abs(x1-x0)>2 and abs(y1-y0)>2:            
        self.BorderCoords = [x0,y0,x1,y1]
        #save all borders in dict
        try:
            #dict key exists, so you should append its value
            val = self.tempdictionary[f'page {self.currentpage}']
            val.append(self.BorderCoords)
            self.tempdictionary[f'page {self.currentpage}'] = val
        except:
            #dict key does not exist, just add the value to the new key
            self.tempdictionary.update({f'page {self.currentpage}' : [self.BorderCoords]})
            
        #crop image
        if self.stayonpage == False:
            img = PIL.Image.open(self.jpgdir)
        else:
            img = self.pageimage
        img = np.array(img)            
        img = img[y0:y1,x0:x1]
        img = PIL.Image.fromarray(img)
        find = True
        while find == True:
            rand_nr = str(randint(0, 9999)).rjust(4, "0") #The number must be of length 4: '0006' must be a possible result.
            if self.stayonpage == False:
                picname =  f"{self.bookname}_{self.currentpage}_{rand_nr}.jpg" 
            else:
                picname =  f"{self.bookname}_prtscr_{rand_nr}.jpg"
            filename = os.path.join(self.dir2, self.bookname, picname)    
            if not os.path.exists(filename):
                find = False
        img.save(filename)
        
        """The list will look like the following:
        [vert1 [hor1,hor2,hor3],vert2,vert3,[hor4,hor5]]
        So that first the horizontal [] within the list will be combined first, 
        then everythying will be combined vertically."""
        
        dir_ = os.path.join(self.dir2,self.bookname,picname)
        if self.questionmode == True:
            if self.stitchmode_v == True:
                self.pic_question.append(picname)  
                self.pic_question_dir.append(dir_)  
            else:
                try:
                    self.pic_question[-1].append(picname)  
                    self.pic_question_dir[-1].append(dir_)  
                except:
                    self.pic_question.append([picname])  
                    self.pic_question_dir.append([dir_])  
                #restore stitchmode to default
                self.stitchmode_v =  True            
                self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow2))
        else:
            if self.stitchmode_v == True:
                self.pic_answer.append(picname)  
                self.pic_answer_dir.append(dir_)    
            else:
                try:
                    self.pic_answer[-1].append(picname)  
                    self.pic_answer_dir[-1].append(dir_) 
                except:
                    self.pic_answer.append([picname])  
                    self.pic_answer_dir.append([dir_])  
                #restore stitchmode to default
                self.stitchmode_v =  True            
                self.m_toolStitch.SetBitmap(wx.Bitmap(self.path_arrow2))
        f.ShowPage(self)     
        
def panel4_bitmapleftup(self,event):
    self.BoolCropped = True
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    self.panel4_pos2 = self.m_bitmap4.ScreenToClient(wx.GetMousePosition())
    
    x0, y0 = self.panel4_pos
    x1, y1 = self.panel4_pos2
    #rescale
    x0, y0 = int(x0), int(y0)
    x1, y1 = int(x1), int(y1)
    
    if abs(x1-x0)>2 and abs(y1-y0)>2:            
        # cut down image
        img = PIL.Image.open(os.path.join(self.dir4,"screenshot.png"))
        img = np.array(img)            
        img = img[y0:y1,x0:x1]
        img = PIL.Image.fromarray(img)
        self.pageimagecopy = img
        self.pageimage = img
        # show current page
        f.ShowPrintScreen(self)     
    

   
def selectionentered(self,event):
    
    if hasattr(self,'bookname') and self.bookname != '':
        if self.m_textCtrl2.GetValue() != '' or len(self.pic_question)>0:
            if self.questionmode == True:
                # change mode to answer
                self.usertext = self.m_textCtrl2.GetValue()
                self.pdf_question = self.usertext
                self.usertext = f.Text2Latex(self)
                self.questionmode = False
                self.m_textCtrl1.SetValue("Answer:")
                self.m_textCtrl2.SetValue("")
                
                # check for [[1,2,3]]
                if len(self.pic_question)>1:
                    f.CombinePics(self,self.pic_question_dir)
                    if type(self.pic_question[0]) is list:
                        self.pic_question[0] = self.pic_question[0][0]
                    self.pdf_question = str(self.pdf_question) + r" \pic{" + "{}".format(self.pic_question[0])+r"}"
                else:       
                    print("only horizontal questions")
                    print(len(self.pic_question))
                    if len(self.pic_question) == 1:
                        if type(self.pic_question[0]) is list:
                            
                            f.CombinePics(self,self.pic_question_dir)
                        else:
                            print("is not a list")
                        self.pdf_question = str(self.pdf_question) + r" \pic{" + "{}".format(self.pic_question[0])+r"}"
                f.ShowInPopup(self,event,"Question")
                 
            else:
                self.usertext = self.m_textCtrl2.GetValue()
                self.pdf_answer = self.usertext
                self.usertext = f.Text2Latex(self)
                self.questionmode = True
                self.m_textCtrl1.SetValue("Question:")
                self.m_textCtrl2.SetValue("")
                
                # save everything
                findic = self.dictionary
                tempdic = self.tempdictionary
                for key in list(tempdic):      # go over all keys
                    for value in tempdic[key]: # go over all values
                        if key in findic:      # if already exists: just add value
                            findic[key].append(value)
                        else:                  # if not, add key and value, where key = pagenr and value is rectangle coordinates
                            findic.update({key : [value]})
                self.dictionary = findic
                self.tempdictionary = {}
                
                # remove temporary borders
                self.pageimage = self.pageimagecopy
                f.ShowPage(self)
                if self.stayonpage == False: # if screenshot mode
                    with open(self.PathBorders, 'w') as file:
                            file.write(json.dumps(self.dictionary)) 
                if len(self.pic_answer) > 1:
                    f.CombinePics(self,self.pic_answer_dir)
                    if type(self.pic_answer[0]) is list:
                        self.pic_answer[0] = self.pic_answer[0][0]
                    self.pdf_answer = str(self.pdf_answer) + r" \pic{" + "{}".format(self.pic_answer[0])+r"}"                        
                elif len(self.pic_answer) == 1:
                    if type(self.pic_answer[0]) is list:        
                        f.CombinePics(self,self.pic_answer_dir)
                    else:
                        print("is not a list")                
                    self.pdf_answer = str(self.pdf_answer) + r" \pic{" + "{}".format(self.pic_answer[0])+r"}"                        
                

                f.ShowInPopup(self,event,"Answer")                    
                # save the user inputs in .tex file
                if len(self.pdf_question) != 0:
                    with open(os.path.join(self.dir1, self.bookname +'.tex'), 'a') as output: # the mode "a" appends to the file    
                        output.write(r"\quiz{" + str(self.pdf_question) + "}")
                        output.write(r"\ans{"  + str(self.pdf_answer)   + "}"+"\n")
                #reset all
                f.ResetQuestions(self)

def arrowscroll(self,event,direction):
    
    scrollWin = self.m_scrolledWindow1
    if direction == 'down':    
        newpos = scrollWin.GetScrollPos(1)+1
        print(f"scrollpos = {scrollWin.GetScrollPageSize(1),newpos,scrollWin.GetScrollPixelsPerUnit()}" )
    elif direction == 'up':     
        newpos = scrollWin.GetScrollPos(1)-1
        print(f"scrollpos = {scrollWin.GetScrollPageSize(1),newpos,scrollWin.GetScrollPixelsPerUnit()}" )
    
    # check if you should go to the next/previous page
    
    self.scrollpos.append(scrollWin.GetScrollPos(0))
    self.scrollpos.pop(0)
    
    print(f"currentpage = {self.currentpage}")
    print(f"direction is {direction}")
    if len(set(self.scrollpos)) == 1: # you've reached either the beginning or end of the document
        if self.scrollpos[0] == 0:             # beginning
            if direction == 'up':
                self.scrollpos = self.scrollpos_reset     # make it a little more difficult to scroll back once you scrolled a page
                self.m_toolBack11OnToolClicked(self)
                
                if self.currentpage != 1:
                    scrollWin.SetScrollPos(wx.VERTICAL,scrollWin.GetScrollPos(1)+150,False) #orientation, value, refresh?  # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
                    scrollWin.Scroll(scrollWin.GetScrollPos(1)+150,scrollWin.GetScrollPos(1))
                else:
                    scrollWin.SetScrollPos(wx.VERTICAL,0,False) #orientation, value, refresh?  # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
                    scrollWin.Scroll(0,scrollWin.GetScrollPos(1))
        else:                                  # end of page
            if direction == 'down':
                self.scrollpos = self.scrollpos_reset 
                self.m_toolNext11OnToolClicked(self)
    else:
        # change scrollbar    
        #scrollWin.SetScrollPos(wx.VERTICAL,newpos,True) #orientation, value, refresh?
        scrollWin.Scroll(wx.VERTICAL,newpos)
        #scrollWin.Scroll(wx.VERTICAL,newpos,scrollWin.GetScrollPos(1))    
    event.Skip()                               # necessary to use other functions after this one is used
        
def mousewheel(self,event):
    scrollWin = self.m_scrolledWindow1
    self.scrollpos.append(scrollWin.GetScrollPos(0))
    self.scrollpos.pop(0)
    if self.debugmode:
        print(f"scroll pos = {self.scrollpos}")
    self.WheelRot = event.GetWheelRotation()   # get rotation from mouse wheel
    Hvirt= self.m_scrolledWindow1.GetVirtualSize()[1]
    Hclnt = self.m_scrolledWindow1.GetClientSize()[1]
    if Hclnt < Hvirt: # there is a scrollbar
        if len(set(self.scrollpos)) == 1: # you've reached either the beginning or end of the document: all elements are the same
            if self.scrollpos[0] == 0:             # beginning
                if self.WheelRot > 0:
                    self.scrollpos = self.scrollpos_reset     # make it a little more difficult to scroll back once you scrolled a page
                    self.m_toolBack11OnToolClicked(self)
                    if self.currentpage != 1:
                        scrollWin.SetScrollPos(wx.VERTICAL, scrollWin.GetScrollPos(1) + 150, False) #orientation, value, refresh? # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
                        scrollWin.Scroll(scrollWin.GetScrollPos(1) + 150, scrollWin.GetScrollPos(1))
                    else:
                        scrollWin.SetScrollPos(wx.VERTICAL, 0, False) #orientation, value, refresh? # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
                        scrollWin.Scroll(0, scrollWin.GetScrollPos(1))
                    
            elif self.WheelRot < 0:              # end of page
                self.scrollpos = self.scrollpos_reset 
                self.m_toolNext11OnToolClicked(self)
    else:# there is no scrollbar
        if self.WheelRot > 0:
            self.m_toolBack11OnToolClicked(self)
            if self.currentpage != 1:
                scrollWin.SetScrollPos(wx.VERTICAL, scrollWin.GetScrollPos(1) + 150, False) #orientation, value, refresh? # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
                scrollWin.Scroll(scrollWin.GetScrollPos(1) + 150, scrollWin.GetScrollPos(1))
            else:
                scrollWin.SetScrollPos(wx.VERTICAL, 0, False) #orientation, value, refresh? # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
                scrollWin.Scroll(0, scrollWin.GetScrollPos(1))
        elif self.WheelRot < 0:
            self.scrollpos = self.scrollpos_reset 
            self.m_toolNext11OnToolClicked(self)
    event.Skip()                               # necessary to use other functions after this one is used
    
def resetselection(self,event):
    self.resetselection = True
    #  remove all temporary pictures taken
    if len(self.pic_answer_dir) > 0:
        for pic in self.pic_answer_dir:
            try:
                os.remove(pic)
            except:
                pass
    if len(self.pic_question_dir) > 0:
        for pic in self.pic_question_dir:
            try:
                os.remove(pic)
            except:
                pass
    #reset all values:
    self.tempdictionary = {}
    f.ResetQuestions(self)        
    self.questionmode = True
    self.m_textCtrl1.SetValue("Question:")
    self.m_textCtrl2.SetValue("")
    # update drawn borders
    f.LoadPage(self)
    f.ShowPage(self)
    self.resetselection = False
    
def switchpage(self,event):
    try:
        pagenumber = self.currentpage
        if pagenumber < 1:
            pagenumber = 1
        if pagenumber > self.nr_pics:
            pagenumber = self.nr_pics
        self.currentpage = pagenumber
        print(self.currentpage)
        f.LoadPage(self)
        f.ShowPage(self)
    except:
        p.ERRORMESSAGE("Error: invalid page number")
    self.Layout()
    
def nextpage(self,event):
    try:
        if self.currentpage == 'prtscr':
            self.currentpage = self.currentpage_backup
            print(f" page is now{self.currentpage}")
        else:
            if not self.currentpage > self.nr_pics-1:
                self.currentpage = self.currentpage+1
        f.LoadPage(self)
        f.ShowPage(self)
        f.SetScrollbars(self)
    except:
        p.ERRORMESSAGE("Error: can't click on next")
    self.Layout()
    
def previouspage(self,event):    
    try:
        if self.currentpage == 'prtscr':
            self.currentpage = self.currentpage_backup
        else:
            if not self.currentpage == 1:
                self.currentpage = self.currentpage-1    
        f.LoadPage(self)
        f.ShowPage(self)
        f.SetScrollbars(self)            
    except:
        p.ERRORMESSAGE("Error: can't click on back")
    self.Layout()
    
def setcursor(self,event):
    #lf = event.GetEventObject()
    cursor = self.m_checkBoxCursor11.IsChecked()
    self.cursor = cursor
    if cursor == True:
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
    else:
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
def zoomin(self,event):
    
    try:
        self.zoom += 0.1
        f.LoadPage(self)
        f.ShowPage(self)
        f.SetScrollbars(self)
        percentage = int(self.zoom*100)
        self.m_Zoom11.SetValue(f"{percentage}%")
        self.Layout()
    except:
        p.ERRORMESSAGE("Error: cannot zoom out")
def zoomout(self,event):
    
    try:
        if round(self.zoom,1) == 0.1:
            self.zoom = self.zoom
        else:
            self.zoom += -0.1
        f.LoadPage(self)
        f.ShowPage(self)
        f.SetScrollbars(self)
        percentage = int(self.zoom*100)
        self.m_Zoom11.SetValue(f"{percentage}%")
        self.panel1.Refresh() # to remove the remnants of a larger bitmap when the page shrinks
        self.Layout()
    except:
        p.ERRORMESSAGE("Error: cannot zoom in")

def switch_stitchmode(self): # switch the boolean to opposite
    print("you pressed switch")
    print(str(self.stitchmode_v))
    


def SetKeyboardShortcuts(self):
    
    # set keyboard short cuts: accelerator table        
    self.Id_leftkey   = wx.NewIdRef() 
    self.Id_rightkey  = wx.NewIdRef() 
    self.Id_upkey     = wx.NewIdRef() 
    self.Id_downkey   = wx.NewIdRef() 
    self.Id_enterkey  = wx.NewIdRef()
    self.Id_stitch    = wx.NewIdRef()
    
    # combine functions with the id
    self.Bind( wx.EVT_MENU, self.m_toolBack11OnToolClicked,     id = self.Id_leftkey  )
    self.Bind( wx.EVT_MENU, self.m_toolNext11OnToolClicked,     id = self.Id_rightkey )
    self.Bind( wx.EVT_MENU, self.m_enterselectionOnButtonClick, id = self.Id_enterkey )
    self.Bind( wx.EVT_MENU, self.m_toolStitchOnButtonClick,     id = self.Id_stitch )
    self.Bind(wx.EVT_MENU,  self.m_toolUPOnToolClicked,         id = self.Id_upkey)
    self.Bind(wx.EVT_MENU,  self.m_toolDOWNOnToolClicked,       id = self.Id_downkey)
    
    # combine id with keyboard = now keyboard is connected to functions
    entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_LEFT,    self.Id_leftkey),
                                  (wx.ACCEL_NORMAL,  wx.WXK_RIGHT,   self.Id_rightkey ),
                                  (wx.ACCEL_NORMAL,  wx.WXK_RETURN,  self.Id_enterkey ),
                                  (wx.ACCEL_NORMAL,  wx.WXK_UP,      self.Id_upkey),
                                  (wx.ACCEL_NORMAL,  wx.WXK_DOWN,    self.Id_downkey),
                                  (wx.ACCEL_NORMAL,  wx.WXK_HOME,    self.Id_stitch ),
                                  (wx.ACCEL_NORMAL,  wx.WXK_NUMPAD0, self.Id_stitch )])
    self.SetAcceleratorTable(entries)
        

def RemoveKeyboardShortcuts(self,index): 
    try:
        # remove the arrow keys as shortcut by setting the AcceleratorTable again, but without these keys. This overwrites all previous short cuts
        # combine functions with the id 
        self.Id_enterkey  = wx.NewIdRef()
        self.Id_stitch    = wx.NewIdRef()
        if index == 0:
            self.Bind( wx.EVT_MENU, self.m_enterselectionOnButtonClick, id = self.Id_enterkey )
            self.Bind( wx.EVT_MENU, self.m_toolStitchOnButtonClick,     id = self.Id_stitch )
            # combine id with keyboard = now keyboard is connected to functions
            entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_RETURN,  self.Id_enterkey),
                                          (wx.ACCEL_NORMAL,  wx.WXK_HOME,    self.Id_stitch ),
                                          (wx.ACCEL_NORMAL,  wx.WXK_NUMPAD0, self.Id_stitch )])
        if index == 1:
            self.Bind( wx.EVT_MENU, self.m_toolStitchOnButtonClick, id = self.Id_stitch )
            # combine id with keyboard = now keyboard is connected to functions
            entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_HOME,    self.Id_stitch ),
                                          (wx.ACCEL_NORMAL,  wx.WXK_NUMPAD0, self.Id_stitch )])
        self.SetAcceleratorTable(entries)
    except:
        p.ERRORMESSAGE("Error: cannot unset Accelerator Table")


