# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018
@author: Anton
"""
from random import randint
import numpy as np
import PIL
import wx
import os
import fb_functions as f
import timingmodule as m6
import log_module as log
import json
import ctypes
from pathlib import Path
#ctypes:
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW

def list2path(templist):
    output = None
    if type(templist) == list:
        if len(templist) > 1:
            if type(templist[0]) == str:
                print(f"mode1 {templist}")
                output = templist[0]
            elif type(templist[0]) == list:
                output = templist[0][0]
        elif len(templist) == 1:
            if type(templist[0]) == str:
                print(f"mode2 {templist}")
                output = templist[0]
            elif type(templist[0]) == list:
                print(f"mode2 {templist}")
                output = templist[0][0]
    return output

#%%
def dirchanged(self,path):
    
    """For scrolling: only remember last few positions, append and pop 
    if the numbers repeat [0,...,0] or [X,...,X] then you know you've reached either 
    the beginning or the end of the window: then flip page"""
    
    self.scrollpos_reset = [5, 4, 3, 2, 1]     
    self.scrollpos = self.scrollpos_reset
    
    #Keep track of "nrlist" which is a 4 digit nr 18-> "0018" so that it is easily sorted in other programs
    eventpath = Path(path)#Path(event.GetPath())
    nrlist = []
    picnames = [str(pic) for pic in eventpath.iterdir() if pic.suffix == '.jpg']
    self.totalpages = len(picnames)
    
    if self.totalpages == 0:
        MessageBox(0, " The selected folder does not contain any images!", "Error", MB_ICONINFORMATION)
    
    for _, picname in enumerate(picnames):
        
        SEARCH    = True
        name_len  = len(picname)
        indexlist = []
        while SEARCH:
            for j in range(name_len):
                k = name_len - j - 1      
                if (f.is_number(picname[k]) == True) and SEARCH:
                    indexlist.append(k)  
                elif (f.is_number(picname[k]) == False):
                    if j > 0:
                        if (f.is_number(picname[k+1])) == True:
                            SEARCH = False
                            break
                elif j == name_len - 1: #EOS
                    SEARCH = False
                    break
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
    self.bookname = eventpath.name
    if hasattr(self,'TC'):
        delattr(self,'TC')
    self.TC = m6.TimeCount(self.bookname,"flashbook")
    self.booknamepath = eventpath.relative_to(self.booksdir)
    self.currentpage = 1
    self.PathBorders = Path(self.bordersdir, self.bookname + '_borders.txt')
    f.LoadPageNr(self)
    
    #Create empty dictionary if it doesn't exist
    if not self.PathBorders.exists():
        with open(str(self.PathBorders), 'w') as file:
            file.write(json.dumps({})) 
    
    book_dir = Path(self.picsdir,self.bookname)
    if not book_dir.exists():
        book_dir.mkdir()
        
    
    self.m_CurrentPageFB.SetValue(str(self.currentpage))
    self.m_TotalPagesFB.SetValue(str(self.totalpages))
    nrlist.sort()
    
    #Open dictionary if it exists
    try:
        with open(self.PathBorders, 'r') as file:
            self.dictionary = json.load(file)
    except:
        self.dictionary = {}
        print("No drawn rects found for this file, continue")
    try: 
        self.jpgdir    = str(Path(self.booksdir, self.booknamepath, self.picnames[self.currentpage-1]))
        print(self.booknamepath,self.booksdir)
        self.pageimage = PIL.Image.open(self.jpgdir)
        self.pageimagecopy = self.pageimage
        self.width, self.height = self.pageimage.size
    except:
        log.ERRORMESSAGE("Error : could not load scrolled window 1")
        
    #Draw borders if they exist
    try:
        if self.drawborders:                    
            pageimage = self.pageimage
            self.pageimage = f.drawCoordinates(self,pageimage)
    except:
        log.ERRORMESSAGE("Error: could not draw borders")
                  
    try:
        image2 = wx.Image( self.width, self.height )
        image2.SetData( self.pageimage.tobytes() )
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))
        f.SetScrollbars(self)
    except:
        log.ERRORMESSAGE("Error: could not load scrolled window 2")
    self.Layout()
    
def bitmapleftup(self,event):
    if not self.cursor:
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    self.panel_pos2 = self.m_bitmapScroll.ScreenToClient(wx.GetMousePosition())
    
    x0, y0 = self.panel_pos
    x1, y1 = self.panel_pos2
    #rescale
    x0 = int(x0/self.zoom)
    y0 = int(y0/self.zoom)
    x1 = int(x1/self.zoom)
    y1 = int(y1/self.zoom)
    
    VALID_RECTANGLE = abs(x1-x0)>2 and abs(y1-y0)>2 #should be at least of a certain width and height
    if VALID_RECTANGLE:            
        self.BorderCoords = [x0,y0,x1,y1]
        #save all borders in dict
        
        try:#dict key exists, so you should append its value
            val = self.tempdictionary[f'page {self.currentpage}']
            val.append(self.BorderCoords)
            self.tempdictionary[f'page {self.currentpage}'] = val
            
        except:#dict key does not exist, just add the value to the new key
            self.tempdictionary.update({f'page {self.currentpage}' : [self.BorderCoords]})
            
        #crop image
        if not self.stayonpage:
            img = PIL.Image.open(self.jpgdir)
        else:
            img = self.pageimage
        img = np.array(img)            
        img = img[y0:y1,x0:x1]
        img = PIL.Image.fromarray(img)
        FIND = True
        while FIND:
            rand_nr = str(randint(0, 9999)).rjust(4, "0") #The number must be of length 4: '0006' must be a possible result.
            if not self.stayonpage:
                picname =  f"{self.bookname}_{self.currentpage}_{rand_nr}.jpg" 
            else:
                picname =  f"{self.bookname}_prtscr_{rand_nr}.jpg"
            filename = Path(self.picsdir, self.bookname, picname)    
            if not filename.exists():
                FIND = False
        img.save(filename)
        
        """The list will look like the following:
        [vert1 [hor1,hor2,hor3],vert2,vert3,[hor4,hor5]]
        So that first the horizontal [] within the list will be combined first, 
        then everythying will be combined vertically."""
        
        dir_ = str(Path(self.picsdir,self.bookname,picname))
        if self.Flashcard.getmode() == 'Question':
            if self.stitchmode_v:
                self.Flashcard.addpic('Question','vertical',picname,dir_)
            else:
                self.Flashcard.addpic('Question','horizontal',picname,dir_)
                #restore stitchmode to default
                self.stitchmode_v =  True   
                f.SetToolStitchArrow(self,orientation="vertical")
        else:
            if self.stitchmode_v:
                self.Flashcard.addpic('Answer','vertical',picname,dir_)
            else:
                self.Flashcard.addpic('Answer','horizontal',picname,dir_)
                #restore stitchmode to default
                self.stitchmode_v =  True     
                f.SetToolStitchArrow(self,orientation="vertical")
        f.ShowPage_fb(self)     
        
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
        img = PIL.Image.open(str(Path(self.tempdir,"screenshot.png")))
        img = np.array(img)            
        img = img[y0:y1,x0:x1]
        img = PIL.Image.fromarray(img)
        self.pageimagecopy = img
        self.pageimage = img
        # show current page
        f.ShowPrintScreen(self)     
    
def selectionentered(self,event):
    
    if hasattr(self,'bookname') and self.bookname != '':
        USER_textinput = self.m_userInput.GetValue()       
        PICS_DRAWN = self.Flashcard.nrpics("Question")
        QUESTION_MODE = self.Flashcard.getquestionmode()
        if  USER_textinput != '' or PICS_DRAWN > 0:
            print("selection")
            usertext = USER_textinput
            if QUESTION_MODE:
                print("selection + questionmode") 
                # change mode to answer
                self.usertext = f.text_to_latex(self,usertext)
                self.Flashcard.switchmode()
                self.m_modeDisplay.SetValue(self.Flashcard.getmode()+":")
                self.Flashcard.setT(self.m_TopicInput.GetValue())
                self.m_userInput.SetValue("")
                self.Refresh()
                # check for [[1,2,3]]
                if PICS_DRAWN > 1:
                    print("PICS DRAWN > 1")                    
                    list_ = self.Flashcard.getpiclist("Question")
                    f.CombinePics(self,list_)
                    list_ = list2path(list_)
                    #if type(list_[0]) is list:
                    self.Flashcard.setpiclist('Question',list_)   
                    self.Flashcard.setQ(usertext)                
                    self.Flashcard.setQpic(os.path.basename(list_))
                elif PICS_DRAWN == 1:
                    
                    list_ = self.Flashcard.getpiclist("Question")
                    print(f"PICS DRAWN = 1 {list_}")    
                    print(f"mode is {self.Flashcard.getmode()}")
                    if len(list_)>1 and type(list_[0]) is list:#list in list    
                        f.CombinePics(self,list_)
                        list_ = list2path(list_)
                        
                    else:
                        list_ = list2path(list_)
                        
                        print("is not a list")
                    self.Flashcard.setQ(usertext)
                    self.Flashcard.setQpic(os.path.basename(list_))
                elif PICS_DRAWN == 0:
                    print("PICS DRAWN = 0")                    
                    self.Flashcard.setQ(usertext)
                f.ShowInPopup(self,event,"Question")
                
            else:#ANSWER mode
                print("selection + answer")
                self.usertext = f.text_to_latex(self,usertext)
                self.questionmode = True
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
                f.ShowPage_fb(self)
                if not self.stayonpage: # if screenshot mode
                    with open(self.PathBorders, 'w') as file:
                        file.write(json.dumps(self.dictionary))
                        
                list_A = self.Flashcard.getpiclist("Answer")
                if list_A == None:
                    list_A = ''
                if len(list_A) > 1:
                    f.CombinePics(self,list_A)
                    if type(list_A[0]) is list:
                        list_A[0] = list_A[0][0]
                    self.Flashcard.setA(usertext)
                    self.Flashcard.setApic(os.path.basename(list_A[0]))
                elif len(list_A) == 1:
                    if type(list_A[0]) is list:        
                        f.CombinePics(self,list_A)
                        self.Flashcard.setA(usertext)
                        self.Flashcard.setApic(os.path.basename(list_A[0]))
                    else:
                        self.Flashcard.setA(usertext)
                        self.Flashcard.setApic(r" \pic{" + os.path.basename(list_A[0])+r"}")
                        print("is not a list")                
                else:
                    self.Flashcard.setA(usertext)
                

                f.ShowInPopup(self,event,"Answer")                    
                # save the user inputs in .tex file
                
                self.Flashcard.setT(self.m_TopicInput.GetValue())
                if self.Flashcard.QuestionExists():
                    path = str(Path(self.notesdir, self.bookname +'.tex'))
                    self.Flashcard.saveCard(path)
                #reset all
                self.Flashcard.reset()
                self.m_modeDisplay.SetValue(self.Flashcard.getmode()+":")
                self.m_TopicInput.SetValue('')
                self.m_userInput.SetValue("")
                
                
        elif not QUESTION_MODE:
            print("selection Answer without any input")
            # if in question mode the user only typed in some text and want to save that 
            self.Flashcard.setT(self.m_TopicInput.GetValue())
            self.tempdictionary = {}
            # remove temporary borders
            self.pageimage = self.pageimagecopy
            f.ShowPage_fb(self)
            list_A = self.Flashcard.getpiclist("Answer")
            if not self.stayonpage: # if screenshot mode
                with open(self.PathBorders, 'w') as file:
                        file.write(json.dumps(self.dictionary)) 
            if len(list_A) > 1:
                f.CombinePics(self,list_A)
                if type(list_A[0]) is list:
                    list_A[0] = list_A[0][0]
                self.Flashcard.setA(usertext)
                self.Flashcard.setApic(str(list_A[0]))
            elif len(list_A) == 1:
                if type(list_A[0]) is list:        
                    f.CombinePics(self,list_A)
                else:
                    print("is not a list")
                self.Flashcard.setA(usertext)
                self.Flashcard.setApic(str(list_A[0]))               
            

            f.ShowInPopup(self,event,"Answer")                    
            # save the user inputs in .tex file
            if self.Flashcard.QuestionExists():
                path = str(Path(self.notesdir, self.bookname +'.tex'))
                self.Flashcard.saveCard(path)
            #reset all
            self.Flashcard.reset()
            self.m_modeDisplay.SetValue(self.Flashcard.getmode()+":")
            self.m_TopicInput.SetValue('')
            self.m_userInput.SetValue("")
            
def arrowscroll(self,event,direction):
    
    scrollWin = self.m_scrolledWindow1
    if direction == 'down':    
        newpos = scrollWin.GetScrollPos(1)+1
    elif direction == 'up':     
        newpos = scrollWin.GetScrollPos(1)-1
    
    # check if you should go to the next/previous page   
    self.scrollpos.append(scrollWin.GetScrollPos(0))
    self.scrollpos.pop(0)
    
    if len(set(self.scrollpos)) == 1: # you've reached either the beginning or end of the document
        if self.scrollpos[0] == 0:             # beginning
            if direction == 'up':
                self.scrollpos = self.scrollpos_reset     # make it a little more difficult to scroll back once you scrolled a page
                self.m_pageBackFBOnToolClicked(self)
                
                if self.currentpage != 1:
                    scrollWin.SetScrollPos(wx.VERTICAL,scrollWin.GetScrollPos(1)+150,False) #orientation, value, refresh?  # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
                    scrollWin.Scroll(scrollWin.GetScrollPos(1)+150,scrollWin.GetScrollPos(1))
                else:
                    scrollWin.SetScrollPos(wx.VERTICAL,0,False) #orientation, value, refresh?  # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
                    scrollWin.Scroll(0,scrollWin.GetScrollPos(1))
        else:                                  # end of page
            if direction == 'down':
                self.scrollpos = self.scrollpos_reset 
                self.m_pageNextFBOnToolClicked(self)
    else:
        # change scrollbar    
        scrollWin.Scroll(wx.VERTICAL,newpos)
    event.Skip() # necessary to use another function after this one                               
        
def mousewheel(self,event):
    scrollWin = self.m_scrolledWindow1
    
    def scroll_end_of_page(scrollWin):
        scrollWin.SetScrollPos(wx.VERTICAL, scrollWin.GetScrollPos(1) + 150, False) #orientation, value, refresh? # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
        scrollWin.Scroll(scrollWin.GetScrollPos(1) + 150, scrollWin.GetScrollPos(1))
    def scroll_begin_of_page(scrollWin):
        scrollWin.SetScrollPos(wx.VERTICAL, 0, False) #orientation, value, refresh? # 150 is overkill, but it means the new page starts definitely at the bottom of the scroll bar
        scrollWin.Scroll(0, scrollWin.GetScrollPos(1))
    def reset_scrollpos(self):
        #make it a little more difficult to scroll once you switched a page
        self.scrollpos = self.scrollpos_reset 
        
    self.scrollpos.append(scrollWin.GetScrollPos(0))
    self.scrollpos.pop(0)
    #set booleans
    wheel_rotation  = event.GetWheelRotation()   # get rotation from mouse wheel
    wheel_scrollsup = wheel_rotation > 0 
    wheel_scrollsdown = wheel_rotation < 0
    virtualsize = scrollWin.GetVirtualSize()[1]
    realsize    = scrollWin.GetClientSize()[1]
    scrollbar_exists = realsize < virtualsize
    topofpage = (len(set(self.scrollpos)) == 1 and self.scrollpos[0] == 0)
    bottomofpage = (len(set(self.scrollpos)) == 1 and self.scrollpos[0] != 0)
    
    if scrollbar_exists:
        if topofpage and wheel_scrollsup:
            reset_scrollpos(self)
            if self.currentpage != 1:
                self.m_pageBackFBOnToolClicked(self)
                scroll_end_of_page(scrollWin)
            else:
                scroll_begin_of_page(scrollWin)
                
        elif bottomofpage and wheel_scrollsdown:
            reset_scrollpos(self)
            if self.currentpage < self.totalpages:
                self.m_pageNextFBOnToolClicked(self)
                scroll_begin_of_page(scrollWin)
            else:
                pass    
    else:# there is no scrollbar
        if wheel_scrollsup:
            reset_scrollpos(self)
            if self.currentpage != 1:
                self.m_pageBackFBOnToolClicked(self)
                scroll_end_of_page(scrollWin)
            else:
                scroll_begin_of_page(scrollWin)
        elif wheel_scrollsdown:
            reset_scrollpos(self)
            self.m_pageNextFBOnToolClicked(self)
    event.Skip() # necessary to use other functions after this one is used
    
def resetselection(self,event):    
    #  remove all temporary pictures taken
    self.Flashcard.removepics()
    #reset all values:
    self.tempdictionary = {}
    self.Flashcard.reset()
    self.m_modeDisplay.SetValue(self.Flashcard.getmode()+":")
    # update drawn borders
    self.pageimage = self.pageimagecopy
    f.LoadPage(self)
    f.ShowPage_fb(self)
    
    
    
def switchpage(self,event):
    try:
        pagenumber = self.currentpage
        if pagenumber < 1:
            pagenumber = 1
        if pagenumber > self.totalpages:
            pagenumber = self.totalpages
        self.currentpage = pagenumber
        f.LoadPage(self)
        f.ShowPage_fb(self)
    except:
        log.ERRORMESSAGE("Error: invalid page number")
    self.Layout()
    
def nextpage(self,event):
    try:
        if self.currentpage == 'prtscr':
            self.currentpage = self.currentpage_backup
            print(f" page is now{self.currentpage}")
        else:
            if self.currentpage < self.totalpages:
                self.currentpage += 1
        f.LoadPage(self)
        f.ShowPage_fb(self)
        f.SetScrollbars(self)
    except:
        log.ERRORMESSAGE("Error: can't click on next")
    self.Layout()
    
def previouspage(self,event):    
    try:
        if self.currentpage == 'prtscr':
            self.currentpage = self.currentpage_backup
        else:
            if self.currentpage > 1:
                self.currentpage -= 1    
        f.LoadPage(self)
        f.ShowPage_fb(self)
        f.SetScrollbars(self)            
    except:
        log.ERRORMESSAGE("Error: can't click on back")
    self.Layout()

def setcursor(self):
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

def zoomin(self,event):
    try:
        self.zoom += 0.1
        f.LoadPage(self)
        f.ShowPage_fb(self)
        f.SetScrollbars(self)
        percentage = int(self.zoom*100)
        self.m_ZoomFB.SetValue(f"{percentage}%")
        self.Layout()
    except:
        log.ERRORMESSAGE("Error: cannot zoom out")
        
def zoomout(self,event):    
    try:
        if round(self.zoom,1) == 0.1:
            self.zoom = self.zoom
        else:
            self.zoom += -0.1
        f.LoadPage(self)
        f.ShowPage_fb(self)
        f.SetScrollbars(self)
        percentage = int(self.zoom*100)
        self.m_ZoomFB.SetValue(f"{percentage}%")
        self.panel1.Refresh() # to remove the remnants of a larger bitmap when the page shrinks
        self.Layout()
    except:
        log.ERRORMESSAGE("Error: cannot zoom in")

