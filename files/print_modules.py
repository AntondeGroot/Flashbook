# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:26:43 2018
@author: Anton
"""
import bisect
import ctypes
import img2pdf
import json
import numpy as np
import os
from PIL import Image
import PIL
import print_functions as f
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
    program.run_print(self, event)
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
    
    import print_functions as f
    N = 1.3
    self.a4page_w  = round(1240*N*self.pdfmultiplier) # in pixels
    self.a4page_h = round(1754*N*self.pdfmultiplier)
    self.paper_h      = []
    self.paper_h_list = []
    #target directory
    self.dir_t = os.path.join(os.getenv("LOCALAPPDATA"),"FlashBook","temporary")
    ## create images
    self.allimages   = []
    self.allimages_w = [] #widths
    
    for i in range(self.nr_questions):
        self.image_q = PIL.Image.new('RGB', (0, 0),"white")
        self.image_a = []
        for mode in ['Question','Answer']: 
            self.mode = mode
            self.TextCard = False      
            self.key = '{}{}'.format(self.mode[0],i)
            try:          
                # try to create a TextCard
                if self.key in self.textdictionary:
                    try:
                        f.CreateTextCard(self)
                    except:
                        print(colored("Error: could not create textcard","red"))
                # if there is a textcard either combine them with a picture or display it on its own
                if self.TextCard == True: 
                    if self.key in self.picdictionary:
                        try:
                            f.CombinePicText(self)      
                        except:
                            pass
                    else:
                        self.image = self.imagetext                        
                        if mode == 'Question':
                            self.image_q = self.image
                        else:
                            self.image_a = self.image
                else: #if there is no textcard only display the picture
                    if self.key in self.picdictionary:
                        try:
                            self.image = PIL.Image.open(self.dir2+"\\"+self.bookname+"\\"+self.picdictionary[self.key])
                        except:
                            pass
                        if mode == 'Question':
                            self.image_q = self.image
                        else:
                            self.image_a = self.image
            except:
                print(colored("Error: could not display card","red"))  
        
        #combine question and answer:
        if self.image_a != []:
            images = [self.image_q,self.image_a]
            widths, heights = zip(*(i.size for i in images)) 
            total_height = sum(heights)
            max_width = max(widths)
            if self.QAline_bool == True:
                new_im = PIL.Image.new('RGB', (max_width, total_height+self.QAline_thickness), "white")
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
            print(images.size)
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
                print(A)
                print("\n")      
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
            
            pathname = os.path.join(self.dir_t,"temporary{}.png".format(i))
            folder.append(pathname)
            image.save(pathname)
            #image.show()
            i += 1
        filename = os.path.join(self.dirpdf,"{}.pdf".format(self.bookname))
        try:
            with open(filename, "wb") as f:
                f.write(img2pdf.convert([i for i in folder if i.endswith(".png")]))
            self.printsuccessful = True
        except:
            self.printsuccessful = False
            MessageBox(0, "If you have the PDF opened in another file, close it and try it again.", "Warning", ICON_EXCLAIM)
    else:
        pass
    self.m_TotalPDFPages.SetValue(str(''))
    self.m_TotalPDFPages.SetValue(str(len(self.allimages_v)))

def dirchanged(self,event):
    # for scrolling: only remember current and last position, append and pop, if the numbers repeat [0,0] or [X,X] then you know you've reached either the beginning or the end of the window: then flip page
    self.scrollpos = [42,1337] 
    #   INITIALIZE: ACQUIRE ALL INFO NECESSARY
    print("\nThe chosen path is {}\n".format(event.GetPath()))
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
                    
                    if (f.is_number(picname[k]) == True) and SEARCH == True:
                        indexlist.append(k)  
                    elif (f.is_number(picname[k]) == False):
                        if j > 0:
                            if (f.is_number(picname[k+1])) == True:
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
            elif len_nr ==0:
                print("found no number for {}".format(picname))
            else:
                I = indexlist[0]
                F = indexlist[-1]+1
                nrlist.append("0"*(4-len_nr)+"{}".format(picname[I:F]))
                       
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
            self.jpgdir = self.dir3+r'\{}\{}'.format(self.bookname,self.picnames[self.currentpage-1])
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
    except:
        print(colored("Error: could not load image",'red'))



        


def find_hook(hookpos,string):    
    """Method:
    Count
        { == +1 
        } == -1
    When the count == 0 you are done.
    """
    k = 0
    hookcount = 0
    condition = True
    for i in range(hookpos,len(string)):#make sure it starts with {
        if (condition == True):
            k = k+1
            char = string[i]
            if char == '{':
                hookcount += 1
            if char == '}':
                hookcount -= 1
                if hookcount == 0:
                    condition = False
                    end_index = k+hookpos-1
                    return end_index  


def findchar(char,string,nr):
    nr1 = str(nr)
    if nr1.isdigit() == True:
        ans = [m.start() for m in re.finditer(r'{}'.format(char), string )][nr]
        return ans 
    if nr == -1:  # negative numbers arent considered digits, we will only need [0,1,-1, or no argument]
        ans = [m.start() for m in re.finditer(r'{}'.format(char), string )][nr]
        return ans 
    else:
        ans = [m.start() for m in re.finditer(r'{}'.format(char), string )]
        return ans 

def contains(iterable):
    k = 0
    ans = []
    con = []
    for element in iterable:
        if element:
             ans.append(k)
             con = True
        k=k+1
    return con,ans 

def find_arguments(hookpos,sentence,defined_command,nr_arguments):
    
    k = 0
    hookcount = 0      
    condition = True
    argcount = 0
    # find opening and closing {} for the arguments
    argclose_index = [] 
    argopen_index  = []

    cstr_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), sentence )][0]
    
    for i in range(cstr_start,len(sentence)):            # make sure it starts with {
        if (condition == True):
            k = k+1
            char = sentence[i]
            
            if char == '{':
                hookcount += 1
                if hookcount ==1:
                    argopen_index.append(k+cstr_start-1)  # save opening indices
                
            if char == '}':
                hookcount -= 1
                if hookcount == 0:
                    argcount += 1
                    if argcount== nr_arguments:           #if the nr of closed loops == nr of arguments we are done
                        condition = False
                    argclose_index.append(k+cstr_start-1) #save closing indices
    arguments = []
    for i in range(nr_arguments):
        arguments.append(sentence[argopen_index[i]+1:argclose_index[i]])
    return arguments, argopen_index, argclose_index


def replace_allcommands(defined_command,LaTeX_command,Question,nr_arg):    
    
    length_c = len(defined_command) 
    # check if the command can be found in Q&A
    FindCommand = (defined_command in Question)
    while FindCommand == True: 
        # if a command has arguments: you need to find their positions
        if nr_arg != 0:
            cmd_start = [m.start() for m in re.finditer(r'\{}'.format(defined_command), Question )][0]
            arguments = find_arguments(cmd_start,Question,defined_command,nr_arg)[0]
            # check if it gives empty [], otherwise index1 = [] will give errors
            A = find_arguments(cmd_start,Question ,defined_command,nr_arg)
    
            if not A[0]: # quits if the index is empty
                FindCommand = False
            else:
                index1 = find_arguments(cmd_start,Question ,defined_command,nr_arg)[1][0]-length_c
                index2 = find_arguments(cmd_start,Question,defined_command,nr_arg)[2][1]+1
                
                #replace the command by a LaTeX command
                Question = Question.replace(Question[index1:index2],LaTeX_command )
                #replace the temporary arguments #1,#2... by the real arguments
                for i in range(nr_arg):
                    Question = Question.replace("#{}".format(i+1), arguments[i])
                # check if another command is in the Q&A
                FindCommand = (defined_command in Question)
        else:
            # if there are no arguments you can directly replace the defined_cmd for the latex_cmd
            # only needs to do this once for the entire string
            Question = Question.replace(defined_command,LaTeX_command)
            FindCommand = False
    
    return Question

def remove_pics(string,pic_command):
    
    # there is only 1 pic per Q/A, in the form of "some text \pic{name.jpg} some text"   
    if pic_command in string: # if \pic is found in text
        # start and endpoints of brackets
        pic_start = [m.start() for m in re.finditer(r'\{}'.format(pic_command), string )][0]        
        pic_end = find_hook(pic_start, string)
        # output
        BOOLEAN = True
        picname = find_arguments(pic_start, string, pic_command, 1)[0][0] # returns string instead of list
        string = string[:pic_start] + string[pic_end+1:]                 # Question without picture
    else:
        BOOLEAN = False
        picname = []
    return BOOLEAN, string, picname

def LoadFlashCards(self):
    #if self.debugmode:
    #    print("f=loadflashcards")
    try:
        # find the closing '}' for a command                                         
        end_q_index = 0
        end_a_index = 0    
        for N in range(self.nr_cards):   
            end_q_index = find_hook(self.q_hookpos[N], self.letterfile)
            end_a_index = find_hook(self.a_hookpos[N], self.letterfile)    
            # collect all Questions and Answers
            self.questions.append(self.letterfile[self.q_hookpos[N]+1:end_q_index])
            self.answers.append(self.letterfile[self.a_hookpos[N]+1:end_a_index])        
        # replace user defined commands, found in a separate file                  
        file1 = open(os.path.join(self.dir_LaTeX_commands, r"usercommands.txt"), 'r')
        newcommand_line_lst = file1.readlines()
        # start reading after "###" because I defined that as the end of the notes
        index = []
        for i,commandline in enumerate(newcommand_line_lst):
            if "###" in commandline:
                index = i+1
        # remove the lines that precede the ### for user explanation on how to use newcommand        
        if "{}".format(index).isdigit() == True:
            newcommand_line_lst[:index]=[]
        # only look at lines containing "newcommand" removes all empty and irrelevant lines
        newcommand_line_lst = [x for x in newcommand_line_lst if ("newcommand"  in x)]
        nr_c = len(newcommand_line_lst)
        
        ##  how to replace a user defined command with a command that is known in latex
        # look for all commands if they appear anywhere in questions or answers.
        # find indices of: -defined command -original command, -number of arguments
        for i in range(nr_c):
            newcommand_line = newcommand_line_lst[i]
            # extract all the data from a commandline
            c_start = findchar('{',newcommand_line,0)
            c_end   = findchar('}',newcommand_line,0)
            
            num_start = findchar('\[',newcommand_line,"")              # the argument "" indicates it will find all instances
            num_end   = findchar('\]',newcommand_line,"") 
           
            newc_start = findchar('{',newcommand_line,1)   
            newc_end = findchar('}',newcommand_line,-1)
            # find the commands explicitly
            defined_command = newcommand_line[c_start+1:c_end]         # finds \secpar{}{}            
            LaTeX_command   = newcommand_line[newc_start+1:newc_end]   # finds \frac{\partial^2 #1}{\partial #2^2}
            nr_arg          = int(newcommand_line[int(num_start[0]+1):int(num_end[0])])
            
            # find where they can be found in all of the questions/answers
            cond_q = contains(defined_command in x for x in self.questions) 
            cond_a = contains(defined_command in x for x in self.answers)  
            
            #check questions: does the i-th command occur in the questions
            if cond_q[0] == True: #first index gives T/F, 2nd index gives index where it is true
                nr = len(cond_q[1])
                for j in range(nr):
                    index1 = cond_q[1]
                    index2 = index1[j]                    
                    # select the right question and replace all the commands
                    Q = self.questions[index2]
                    self.questions[index2] = replace_allcommands(defined_command,LaTeX_command,Q,nr_arg)
                                    
            #check answers: does the i-th command occur in the answers
            if cond_a[0] == True: #first index gives T/F, 2nd index gives index where it is true
                nr = len(cond_a[1])
                for k in range(nr):
                    index1 = cond_a[1]
                    index2 = index1[k]
                    # select the right answer and replace all the commands
                    A = self.answers[index2]
                    self.answers[index2] = replace_allcommands(defined_command,LaTeX_command,A,nr_arg)
                    
        ## replace all \pics out of the QnA and save the picture names.
        self.picdictionary  = {}
        self.textdictionary = {}
        self.q_pics = []
        self.a_pics = []
        # remove all \pic{} commands
        for i in range(self.nr_cards):
            findpic = True
            findpic2 = True            
            # Questions: replace pics{}
            while findpic == True:#find all pic commands
                [T_F,QnA,picname]=remove_pics(self.questions[i],self.pic_command)
                self.questions[i] = QnA # removed pic{} from Question
                if T_F == True:
                    self.picdictionary.update({'Q{}'.format(i): picname})
                findpic = T_F
                  
            while findpic2 == True: 
                [T_F2,QnA,picname]=remove_pics(self.answers[i],self.pic_command) 
                self.answers[i] = QnA # removed pic{} from Question
                if T_F2 == True:
                    self.picdictionary.update({'A{}'.format(i): picname})
                findpic2 = T_F2      
        """
        CARD ORDER
        """
        ## determine cardorder based on user given input
        self.cardorder = range(self.nr_questions)    
            
        # reformat QnA
        self.questions2 = []
        self.answers2 = []
        for i,question in enumerate(self.questions):
            answer = self.answers[i]
            self.questions2.append(question.strip())
            self.answers2.append(answer.strip())
        # save questions and answers in dictionaries
        for i,question in enumerate(self.questions):
            if self.questions2[i] != '':
                self.textdictionary.update({'Q{}'.format(i): self.questions2[i]})
            if self.answers2[i] != '':
               self.textdictionary.update({'A{}'.format(i): self.answers2[i]})
    except:
        print(colored("Error: couldn't pick file",'red'))
          
    notes2paper(self)
    
def ShowPage(self):
    if self.debugmode:
        print("f=showpage")
    try:
        width, height = self.image.size
        image2 = wx.Image( width, height )
        image2.SetData( self.image.tobytes() )        
        self.m_bitmapScroll.SetBitmap(wx.Bitmap(image2))        
    except:        
        print(colored("Error: cannot show image","red"))
        
def resetselection(self,event):
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
    
def switchpage(self,event):
    try:
        pagenumber = int(event.GetEventObject().GetValue())
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

def setcursor(self,event):
    lf = event.GetEventObject()
    cursor = lf.GetValue()
    self.cursor = cursor
    if cursor == True:
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
    else:
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        
def zoomout(self,event):
    try:
        self.zoom += 0.1
        f.LoadPage(self)
        f.ShowPage(self)
        f.SetScrollbars(self)
        self.m_textZoom.SetValue(f"{int(self.zoom*100)}%")
    except:
        print(colored("Error: cannot zoom out",'red'))
        
def zoomin(self,event):
    try:
        if self.zoom == 0.1:
            self.zoom = self.zoom
        else:
            self.zoom += -0.1
        f.LoadPage(self)
        f.ShowPage(self)
        f.SetScrollbars(self)
        self.m_textZoom.SetValue(f"{int(self.zoom*100)}%")
        self.m_panel1.Refresh() #remove the remnants of a larger bitmap when the page shrinks
    except:
        print(colored("Error: cannot zoom in",'red'))
        
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
    try:# look if Id's already exist
        # combine functions with the id        
        self.Unbind( wx.EVT_MENU, self.m_toolBackOnToolClicked,       id = self.Id_leftkey  )
        self.Unbind( wx.EVT_MENU, self.m_toolNextOnToolClicked,       id = self.Id_rightkey )
        self.Unbind( wx.EVT_MENU, self.m_enterselectionOnButtonClick, id = self.Id_enterkey )
        # empty acceleratortable?
        self.SetAcceleratorTable()
    except:
        pass

def SwitchBitmap(self): # checks if there is an answer card, if not changes mode back to question.
    if self.debugmode:
        print("f=switchbitmap")
    try:
        # you always start with a question, check if there is an answer:
        key = 'A{}'.format(self.cardorder[self.index]) # do not use self.key: only check if there is an answer, don't change the key
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
            print(colored("Error: could not switch bitmap #2","red"))
    except:
        
        print(colored("Error: could not switch bitmap #1","red"))

def add_border(self,img):
    if self.pdfline_bool == True:
        new_im = PIL.Image.new("RGB", (self.a4page_w,img.size[1]+self.pdfline_thickness),"white")    
        border = PIL.Image.new("RGB", (self.a4page_w,self.pdfline_thickness), self.pdfline_color)    
        #print(type(self.pdfline_color ))
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
    
    f.SetScrollbars(self)    
    # open file
    try:
        if self.FilePickEvent == True:
            self.path     = self.fileDialog.GetPath()            
            self.filename = self.fileDialog.GetFilename()
            self.bookname = self.filename.replace(".tex","")
    except:
        print(colored("Error: Couldn't open path",'red'))
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
    
    except:
        print(colored("Error: finding questions/answers",'red'))

    ## dialog display              
    
    #open My dialog, don't forget to add two parameters to "def __init__( self, parent,MaxValue,Value )" within MyDialog 
    #and use these values to set the slider as you wish. Don't forget to add "self.Destroy" when you press the button
    #open dialog window
    self.nr_questions = self.nr_cards
    self.chrono = True
    self.multiplier = 1
    
    # display nr of questions and current index of questions            
    LoadFlashCards(self)
    #SwitchBitmap(self)
