# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 22:00:23 2020

@author: Anton
"""

class Flashcard2():
    def __init__(self,fontsize = 20, savefolder = None):
        self.a4page_w = 1240
        self.question = ''
        self.questionpic = ''
        self.answer    = ''
        self.answerpic = ''
        self.mode      = 'Question'
        self.questionmode = True
        self.topic    = ''
        self.pic_question     = []
        self.pic_answer       = []
        self.pic_question_dir = []
        self.pic_answer_dir   = []
        self.usertext         = ''
        self.size_q_txt = (0,0)
        self.size_q_pic = (0,0)
        self.size_a_txt = (0,0)
        self.size_a_pic = (0,0)
        self.size_topic = (0,0)
        self.sizelist = '[(0,0),(0,0),(0,0),(0,0),(0,0)]'
        self.LaTeXfontsize = fontsize
        self.savefolder = savefolder
        
        
        self.carddict = {}
        self.questiondict = {}
        self.answerdict = {}
        self.bookname = ''
        self.pagenr = 1
        
        """{card_id : 12345, question : {rect_id: 54321, text: '',pic : '' }, answer : {rect_id: 12435, text: '',pic : '' }, topic : 'Topic', size: [0,0,0,0]}
        
        The idea is: each Q/A card has an unique ID
        The Q card has an sub-id if a rectangle has been drawn
        The A card has an sub-id"""
    
    
    def setpagenr(self,pagenr):
        self.pagenr = pagenr
    def addID(self):
        from random import randint
        FIND_ID = True
        
        settingsfile = Path(self.savefolder,"ID_list.txt")
        
            
        
        while FIND_ID:
            rand_nr = str(randint(0, 99999)).rjust(5, "0")
            print(rand_nr)
        
        pass
        
    def reset(self):
        self.question = ''
        self.questionpic = ''
        self.answer   = ''
        self.answerpic = ''
        self.mode     = 'Question'
        self.questionmode = True
        self.topic    = ''
        self.pic_question     = []
        self.pic_answer       = []
        self.pic_question_dir = []
        self.pic_answer_dir   = []
        self.usertext         = ''
        self.size_q_txt = (0,0)
        self.size_q_pic = (0,0)
        self.size_a_txt = (0,0)
        self.size_a_pic = (0,0)
        self.size_topic = (0,0)
        self.sizelist = '[(0,0),(0,0),(0,0),(0,0),(0,0)]'
    
    def setpiclist(self,mode,text):
        if mode.lower() == 'question':
            self.pic_question_dir = text
        else:
            self.pic_question_dir = text
            
    def getpicdir(self,mode):
        if mode.lower() == 'question':
            return self.pic_question_dir
        else:
            return self.pic_question_dir
            
    def removepics(self):
        def unlinkpics(dir_):    
            print(f"dir = {dir_}")
            if len(dir_) > 1:
                if isinstance(dir_,str):
                    try:
                        if Path(dir_).exists():
                            Path(dir_).unlink()
                    except:
                        pass
                elif isinstance(dir_,list):
                    for pic in dir_:
                        try:
                            if type(pic) == str and Path(pic).exists():
                                Path(pic).unlink()
                        except:
                            pass
            elif len(dir_) == 1:
                try:
                    #just one image
                    pic = dir_[0]
                    if type(pic) == str and Path(pic).exists():
                            Path(pic).unlink()
                except:
                    print("could not remove single image")
                    pass
                
        if len(self.pic_question_dir) > 0:
            dir_ = self.pic_question_dir
            unlinkpics(dir_)
        if len(self.pic_answer_dir) > 0:
            dir_ = self.pic_answer_dir    
            unlinkpics(dir_)
    
    def addpic(self,mode,orientation,name,path):        
        mode = mode.lower()
        orientation = orientation.lower()
        
        if mode == 'question':
            if orientation == 'vertical':
                self.pic_question.append(name)  
                self.pic_question_dir.append(path)  
            elif orientation == 'horizontal':
                try:
                    self.pic_question[-1].append(name)  
                    self.pic_question_dir[-1].append(path)  
                    print(f"horizontal existing")
                except:
                    print(f"horizontal not existing")
                    self.pic_question.append([name])  
                    self.pic_question_dir.append([path])  
        elif mode == 'answer':  
            if orientation == 'vertical':
                self.pic_answer.append(name)  
                self.pic_answer_dir.append(path)  
            elif orientation == 'horizontal':
                try:
                    self.pic_answer[-1].append(name)  
                    self.pic_answer_dir[-1].append(path)  
                except:
                    self.pic_answer.append([name])  
                    self.pic_answer_dir.append([path])  
            
    def StitchCards(self,vertical_stitch):
        """only when user presses the arrow button, this needs to change entry from/to a list within the total list"""
        
        if vertical_stitch:
            #question mode
            if self.questionmode and (len(self.pic_question) > 0) and (type(self.pic_question[-1]) is list) and (len(self.pic_question[-1])==1):
                self.pic_question[-1] = self.pic_question[-1][0]
                self.pic_question_dir[-1] = self.pic_question_dir[-1][0]
            #answer mode
            if (not self.questionmode) and (len(self.pic_answer) > 0) and (type(self.pic_answer[-1]) is list) and (len(self.pic_answer[-1])==1):
                self.pic_answer[-1] = self.pic_answer[-1][0]
                self.pic_answer_dir[-1] = self.pic_answer_dir[-1][0]    
        #stitch it horizontally
        else:
            #question mode
            if self.questionmode and (len(self.pic_question) > 0) and (type(self.pic_question[-1]) is not list):
                self.pic_question[-1] = [self.pic_question[-1]]
                self.pic_question_dir[-1] = [self.pic_question_dir[-1]]
            #answer mode
            if (not self.questionmode) and (len(self.pic_answer) > 0) and (type(self.pic_answer[-1]) is not list):
                self.pic_answer[-1] = [self.pic_answer[-1]]
                self.pic_answer_dir[-1] = [self.pic_answer_dir[-1]]
    def QuestionExists(self):
        if self.question.strip() != '' or self.questionpic.strip() != '':
            return True
        
    def getpiclist(self,mode):
        if mode.lower() == 'question':
            return self.pic_question_dir
        elif mode.lower() == 'answer':
            return self.pic_answer_dir
    def nrpics(self,mode):
        
        if mode.lower() == 'question':
            
            return len(self.question['pic'])
        elif mode.lower() == 'answer':
            return len(self.answer['pic'])
    def setSizes(self):
        if len(self.pic_question_dir) == 1:
            path = self.pic_question_dir[0]
            try:
                w,h = PIL.Image.open(path).size
            except:
                w,h = 'Error','Error'
            self.size_q_pic = (w,h)
        if len(self.pic_answer_dir) == 1:
            path = self.pic_answer_dir[0]
            try:
                w,h = PIL.Image.open(path).size
            except:
                w,h = 'Error','Error'
            self.size_a_pic = (w,h)
        self.sizelist = str([self.size_q_txt, self.size_q_pic, 
                             self.size_a_txt, self.size_a_pic, 
                             self.size_topic])
    #store user data and save sizes of images/text
    def setT(self,text):
        self.topic = text
        width_card = self.a4page_w
        height_card = int(math.ceil(len(text)/40))*0.75*100
        print(f"! topic = {text}, size = {width_card},{height_card}")
        if height_card != 0:
            print("topic size",width_card,height_card)
            self.size_topic = (width_card,height_card)                
    def setQ(self,usertext):
        if usertext.strip() != '':
            self.question = usertext
            imbool, im = f2.CreateTextCard(self,'manual',usertext)
            print(f"text size is {imbool} {usertext}")
            if imbool:
                self.size_q_txt = im.size
    def setQpic(self,partialpath):
        self.questionpic = partialpath
    def setA(self,usertext):
        if usertext.strip() != '':
            self.answer = usertext
            image_exists, image = f2.CreateTextCard(self,'manual',usertext)
            if image_exists:
                self.size_a_txt = image.size 
                
    def getmode(self):
        return str(self.mode)
    def setApic(self,partialpath):
        self.answerpic = partialpath
    #save the final card  
    def saveCard(self):
        import json
        if self.savefolder and self.bookname:
            path = os.path.join(self.savefolder, self.bookname + '.bok')
            self.setSizes()        
            
            if not os.path.exists(path):
                with open(path, 'w') as output:
                    output.write("")
                output.close
            else:
                with open(path,'a') as file:
                    dictionary = {}
                    if self.question:
                        dictionary['qtext'] = self.question
                    if self.questionpic:
                        dictionary['qpic'] = self.questionpic
                    if self.answer:
                        dictionary['atext'] = self.answer
                    if self.answerpic:
                        dictionary['apic'] = self.answerpic
                    
                    file.write(json.dumps(dictionary))
                    file.close()
            
    def switchmode(self):
        
        if self.mode == 'Question':
            self.mode = 'Answer'
            self.questionmode = False
        else:
            self.mode = 'Question'
            self.questionmode = True
        #def getquestionmode(self):
        #    return self.questionmode
    
    def is_question(self):
        return self.questionmode
