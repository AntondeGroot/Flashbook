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
import json


datadir = os.getenv("LOCALAPPDATA")
dir0 = datadir + r"\FlashBook"
# create settings folder for debugging



def dirchanged(self,event):
    # for scrolling: only remember current and last position, append and pop, if the numbers repeat [0,0] or [X,X] then you know you've reached either the beginning or the end of the window: then flip page
    self.scrollpos = [42,1337] 
    #   INITIALIZE: ACQUIRE ALL INFO NECESSARY
    print("\nThe chosen path is {}\n".format(event.GetPath()))
    
    #try:
    path = event.GetPath() 
    # - keep track of "nrlist" which is a 4 digit nr 18-> "0018" so that it is easily sorted in other programs
    nrlist = []
    arr = os.listdir(path) #
    picnames = []
    for pic in arr:
        if '.jpg' in pic:
           picnames.append(pic)
           
    
    nr_pics = len(picnames)
    print(f"hallo {nr_pics}") 
    for i in range(nr_pics):
        indexlist = []
        TF = True
        #count = 0
        
        picname = picnames[i]
        while TF == True:
            for j in range(len(picname)):
                k=len(picname)-j-1
                
                if (f.is_number(picname[k])==True) and TF==True:
                    indexlist.append(k)  
                elif (f.is_number(picname[k])==False):
                    if j>0:
                        if (f.is_number(picname[k+1]))==True:
                            TF = False
                elif j== len(picname)-1:
                    TF = False
        indexlist.sort()
        len_nr = len(indexlist)
        # I only expect in the order of 1000 pages
        # make sure you can use the nrlist for later use so you can save the output as 
        # "Bookname + ****" a sorted 4 digit number
        if len_nr == 1:
            nrlist.append("000{}".format(picname[indexlist[0]]))
        elif len_nr ==0:
            print("found no number for {}".format(picname))
        else:
            I = indexlist[0]
            F = indexlist[-1]+1
            nrlist.append("0"*(4-len_nr)+"{}".format(picname[I:F]))
    print("hallo")                       
    picnames = [x for _,x in sorted(zip(nrlist,picnames))]
    self.picnames = picnames
    self.bookname = path.replace("{}".format(self.dir3),"")[1:]#to remove '\'
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

    if not os.path.exists(self.dir2+r"\{}".format(self.bookname)):
        os.makedirs(self.dir2+r"\{}".format(self.bookname))
    
    self.m_CurrentPage11.SetValue(str(self.currentpage))
    self.m_TotalPages11.SetValue(str(self.nr_pics))
    nrlist.sort()
    
    ## open dictionary if it exists
    try:
        with open(self.PathBorders, 'r') as file:
            self.dictionary = json.load(file)
    except:
        self.dictionary = {}
        print("no drawn rects found for this file, continue")
    try:
        self.jpgdir = self.dir3+fr'\{self.bookname}\{self.picnames[self.currentpage-1]}'
        self.pageimage = PIL.Image.open(self.jpgdir)
        self.pageimagecopy = self.pageimage
        self.width, self.height = self.pageimage.size
    except:
        print(colored("Error: could not load scrolled window",'red'))
    
    #print(self.drawborders)
    try:#try to draw borders, but if there are no borders, do nothing
        if self.drawborders == True:                    
            f.drawCoordinates(self)
    except:
        print(colored("Error: could not draw borders",'red'))
        pass            
    try:
        image2 = wx.Image( self.width, self.height )
        image2.SetData( self.pageimage.tobytes() )
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        f.SetScrollbars(self)
        

    except:
        print(colored("Error: could not load scrolled window",'red'))
    #except:
    #    print(colored("Error: could not load image",'red'))
        
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
        ## save all borders in dict
        try:
            #dict key exists, so you should append its value
            val = self.tempdictionary['page {}'.format(self.currentpage)]
            val.append(self.BorderCoords)
            self.tempdictionary['page {}'.format(self.currentpage)] = val
            #print("val = {}".format(val))
            #print("dict = {}".format(self.tempdictionary))
        except:
            #dict key does not exist, just add the value to the new key
            self.tempdictionary.update({'page {}'.format(self.currentpage): [self.BorderCoords]})
            #print("temp dictionary is: {}".format(self.tempdictionary))            
        
        # cut down image
        img = PIL.Image.open(self.jpgdir)
        img = np.array(img)            
        img = img[y0:y1,x0:x1]
        img = PIL.Image.fromarray(img)
                        
        picname =  "{}_{}_{}{}{}{}.jpg".format(self.bookname,self.currentpage,randint(0,9),randint(0,9),randint(0,9),randint(0,9))
        img.save(self.dir2+r"\{}\{}".format(self.bookname,picname))
        # the list will look like the following:
        # [vert1 [hor1,hor2,hor3],vert2,vert3,[hor4,hor5]]
        # within so that first the hor [] will be combined first horizontally, then all will be combined vertically.
        if self.questionmode == True:
            if self.stitchmode_v == True:
                self.pic_question.append(picname)  
                self.pic_question_dir.append(self.dir2+r"\{}\{}".format(self.bookname,picname))  
            else:
                try:
                    self.pic_question[-1].append(picname)  
                    self.pic_question_dir[-1].append(self.dir2+r"\{}\{}".format(self.bookname,picname))  
                except:
                    self.pic_question.append([picname])  
                    self.pic_question_dir.append([self.dir2+r"\{}\{}".format(self.bookname,picname)])  
        else:
            if self.stitchmode_v == True:
                self.pic_answer.append(picname)  
                self.pic_answer_dir.append(self.dir2+r"\{}\{}".format(self.bookname,picname))    
            else:
                try:
                    self.pic_answer[-1].append(picname)  
                    self.pic_answer_dir[-1].append(self.dir2+r"\{}\{}".format(self.bookname,picname)) 
                except:
                    self.pic_answer.append([picname])  
                    self.pic_answer_dir.append([self.dir2+r"\{}\{}".format(self.bookname,picname)])  
        # show current page
        f.ShowPage(self)     
        
def selectionentered(self,event):
    #try:
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
        #try:                     
        f.ShowInPopup(self,event,"Question")
        #except:
        #    pass
         
    else:
        self.usertext = self.m_textCtrl2.GetValue()
        self.pdf_answer = self.usertext
        self.usertext = f.Text2Latex(self)
        self.questionmode = True
        self.m_textCtrl1.SetValue("Question:")
        self.m_textCtrl2.SetValue("")
        
        # save everything!!------------------------------------------------------------------------------------------------------------
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

        with open(self.PathBorders, 'w') as file:
                file.write(json.dumps(self.dictionary)) 
        if len(self.pic_answer)>1:
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
        
        #try:   
        f.ShowInPopup(self,event,"Answer")                    
        #except:
        #    pass
        # save the user inputs in .tex file
        if len(self.pdf_question)!=0:
            with open(os.path.join(self.dir1, self.bookname +'.tex'), 'a') as output: # the mode "a" appends to the file    
                output.write(r"\quiz{" + str(self.pdf_question) + "}")
                output.write(r"\ans{"  + str(self.pdf_answer)   + "}"+"\n")
        #reset all
        f.ResetQuestions(self)
    #except:
    #    print(colored("Error: cannot enter selection",'red'))
        
def mousewheel(self,event):
    scrollWin = self.m_scrolledWindow1
    self.scrollpos.append(scrollWin.GetScrollPos(0))
    self.scrollpos.pop(0)
    if self.debugmode:
        print("scroll pos = {}".format(self.scrollpos))
    self.WheelRot = event.GetWheelRotation()   # get rotation from mouse wheel
    if self.scrollpos[0] == self.scrollpos[1]: # you've reached either the beginning or end of the document
        if self.scrollpos[0] == 0:             # beginning
            if self.WheelRot > 0:
                self.scrollpos = [42,1337]     # make it a little more difficult to scroll back once you scrolled a page
                self.m_toolBack11OnToolClicked(self)
        else:                                  # end of page
            if self.WheelRot < 0:
                self.scrollpos = [42,1337] 
                self.m_toolNext11OnToolClicked(self)
    event.Skip()                               # necessary to use other functions after this one is used
    
def resetselection(self,event):
    #  remove all temporary pictures taken
    if len (self.pic_answer_dir)>0:
        for pic in self.pic_answer_dir:
            try:
                os.remove(pic)
            except:
                pass
    if len (self.pic_question_dir)>0:
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
def switchpage(self,event):
    try:
        pagenumber = int(self.m_CurrentPage11.GetValue())
        if pagenumber <1:
            pagenumber = 1
        if pagenumber > self.nr_pics:
            pagenumber = self.nr_pics
        self.currentpage = pagenumber
        print(self.currentpage)
        f.LoadPage(self)
        f.ShowPage(self)
    except:
        print(colored("Error: invalid page number",'red'))
    self.Layout()
def nextpage(self,event):
    try:
        if self.currentpage > self.nr_pics-1:
            self.currentpage = self.currentpage
        else:
            self.currentpage = self.currentpage+1
        f.LoadPage(self)
        f.ShowPage(self)
        f.SetScrollbars(self)
    except:
        print(colored("Error: can't click on next",'red'))
    self.Layout()
def previouspage(self,event):
    try:
        if self.currentpage == 1:
            self.currentpage = self.currentpage
        else:
            self.currentpage = self.currentpage-1    
        f.LoadPage(self)
        f.ShowPage(self)
        f.SetScrollbars(self)            
    except:
        print(colored("Error: can't click on back",'red'))
    self.Layout()
def setcursor(self,event):
    lf = event.GetEventObject()
    cursor = lf.GetValue()
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
        value = int(self.zoom*100)
        self.m_Zoom11.SetValue("{}%".format(value))
        self.Layout()
    except:
        print(colored("Error: cannot zoom out",'red'))
def zoomout(self,event):
    
    try:
        if round(self.zoom,1) == 0.1:
            self.zoom = self.zoom
        else:
            self.zoom += -0.1
        f.LoadPage(self)
        f.ShowPage(self)
        f.SetScrollbars(self)
        value = int(self.zoom*100)
        self.m_Zoom11.SetValue("{}%".format(value))
        self.panel1.Refresh() # to remove the remnants of a larger bitmap when the page shrinks
        self.Layout()
        #self.m_panel1.Update()
    except:
        print(colored("Error: cannot zoom in",'red'))

def switch_stitchmode(self): # switch the boolean to opposite
    print("you pressed switch")
    print(str(self.stitchmode_v))
    


def SetKeyboardShortcuts(self):
    
    try:# look if Id's already exist
        # combine functions with the id
        self.Bind( wx.EVT_MENU, self.m_toolBack11OnToolClicked,       id = self.Id_leftkey  )
        self.Bind( wx.EVT_MENU, self.m_toolNext11OnToolClicked,       id = self.Id_rightkey )
        self.Bind( wx.EVT_MENU, self.m_enterselectionOnButtonClick, id = self.Id_enterkey )
        self.Bind( wx.EVT_MENU, self.m_toolStitchOnButtonClick, id = self.Id_stitch )
        # combine id with keyboard = now keyboard is connected to functions
        entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL,  wx.WXK_LEFT, self.Id_leftkey),
                                      (wx.ACCEL_NORMAL,  wx.WXK_RIGHT, self.Id_rightkey),
                                      (wx.ACCEL_NORMAL,  wx.WXK_RETURN, self.Id_enterkey),
                                      (wx.ACCEL_NORMAL,  wx.WXK_HOME, self.Id_stitch ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_NUMPAD0, self.Id_stitch )])
        self.SetAcceleratorTable(entries)
    except:
        # set keyboard short cuts: accelerator table        
        self.Id_leftkey   = wx.NewIdRef() 
        self.Id_rightkey  = wx.NewIdRef() 
        self.Id_enterkey  = wx.NewIdRef()
        self.Id_stitch    = wx.NewIdRef()
        # combine functions with the id
        self.Bind( wx.EVT_MENU, self.m_toolBack11OnToolClicked,       id = self.Id_leftkey  )
        self.Bind( wx.EVT_MENU, self.m_toolNext11OnToolClicked,       id = self.Id_rightkey )
        self.Bind( wx.EVT_MENU, self.m_enterselectionOnButtonClick, id = self.Id_enterkey )
        self.Bind( wx.EVT_MENU, self.m_toolStitchOnButtonClick, id = self.Id_stitch )
        # combine id with keyboard = now keyboard is connected to functions
        entries = wx.AcceleratorTable([(wx.ACCEL_NORMAL,  wx.WXK_LEFT, self.Id_leftkey),
                                      (wx.ACCEL_NORMAL,  wx.WXK_RIGHT, self.Id_rightkey ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_RETURN, self.Id_enterkey ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_HOME, self.Id_stitch ),
                                      (wx.ACCEL_NORMAL,  wx.WXK_NUMPAD0, self.Id_stitch )])
        self.SetAcceleratorTable(entries)

def RemoveKeyboardShortcuts(self):
    try:# look if Id's already exist
        # combine functions with the id        
        self.Unbind( wx.EVT_MENU, self.m_toolBack11OnToolClicked,       id = self.Id_leftkey  )
        self.Unbind( wx.EVT_MENU, self.m_toolNext11OnToolClicked,       id = self.Id_rightkey )
        self.Unbind( wx.EVT_MENU, self.m_enterselectionOnButtonClick, id = self.Id_enterkey )
        # empty acceleratortable?
        self.SetAcceleratorTable()
    except:
        pass


