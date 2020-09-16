# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 08:40:20 2020

@author: Anton
"""
import _GUI.active_panel as panel
import _GUI.gui_flashbook as gui
import _logging.log_module as log
from pathlib import Path
import json
import shutil
import os
import wx

import ctypes
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW

class Library(gui.MyFrame):
    def __init__(self,mainframe):
        """self. is the selfvariable of this class
        self.mainframe is the 'self' variable of the main gui 
        This way you can still access all panels etc from the original GUI"""       
        self.bookwidth = 250
        self.topicwidth = 150
        self.listctrl = mainframe.m_listTopics
        self.mainframe = mainframe
        self.datafilepath_topicbook = mainframe.dir_topicbook_file # save topic: [bookindex , [book1, ... bookN ] ]
        
        self.topic = ''
        self.bookindex = 0
        self.topic_books = {}
        
        self.newuser = False
    #======================== cosmetic    
    def cleargrid(self):
        self.listctrl.ClearAll()
    
    def setcolumns(self):
        
        """Determine how many columns you need"""
        columnnr = 1
        try:
            for entry in self.data_topicbook.values():
                _,booklist = entry
                if len(booklist) > columnnr:
                    columnnr = len(booklist)
            """Set nr of columns """
            self.listctrl.InsertColumn(0, "Topic")
            self.listctrl.SetColumnWidth(0,self.topicwidth)
            for i in range(columnnr):
                self.listctrl.InsertColumn(i+1, f"Book title {i+1}")
                self.listctrl.SetColumnWidth(i+1,self.bookwidth)
        except:pass
        """resize ListCtrl"""
        panelwidth = self.topicwidth + self.bookwidth*columnnr
        self.listctrl.SetSize(panelwidth,-1)
        
    #======================== display data in grid 
    def setdata(self):
        topicbook = self.data_topicbook
        print(f"setdata topicbook = {len(self.data_topicbook.values())}")
        
        
        for topic in topicbook:
            
            row = []
            row.append(topic)
            
            print(f"topic is {topic}")
            bookindex,books = topicbook[topic]            
            row += books
            print(f"books = {books}")
            print(f"topic + books = {row}")
            self.listctrl.Append(row)
            
        
    def showdata(self):
        self.cleargrid()
        self.loaddata()
        panel.SwitchPanel(self.mainframe,7)
        print(f"data topicbook = {self.data_topicbook}")
        if not self.data_topicbook:
            self.showcasefunctionality()
        else:
            self.setcolumns()
            self.setdata()

    #======================== show how to use it to new users    
    
    def openmessagebox(self):
        MessageBox(0, "Welcome new user!\n\n"+
                   "First fill in the name of a topic in the textbox and click 'Add Topic'. For example Physics/Biology or something more specific\n\n"+
                   "Then you can add PDFs that belong to that topic, for example a textbook & your homework assignments\n\n"+
                   "Once you've finished reading 1 PDF the program will then continue with the next PDF belonging to the same topic", "Welcome new user!", MB_ICONINFORMATION)
    def showcasefunctionality(self):
        """Ïf there are no books, showcase how it is used""" 
        self.newuser = True
        
        self.cleargrid()        
        Topic = ["Example: Physics"]
        Booktitles = ["Classical Mechanics for dummies.pdf", "Classical Mechanics for noobs.pdf","Homework assignments.pdf"]
        
        self.listctrl.InsertColumn(0, "Topic")
        for i in range(len(Booktitles)):
            print(f"i {i}")
            self.listctrl.InsertColumn(i+1, f"Book title {i+1}")
            
                
        self.listctrl.SetColumnWidth(0,self.topicwidth)
        for i in range(len(Booktitles)):
            self.listctrl.SetColumnWidth(i+1,self.bookwidth)
        self.listctrl.Append(Topic + Booktitles)        
        #resize panel
        panelwidth = self.topicwidth + self.bookwidth*len(Booktitles)
        self.listctrl.SetSize(panelwidth,-1)
        self.openmessagebox()
        

    #======================== save data

    
    def getbooknames(self,topic):
        self.topic = topic
        try:
            with open(self.datafilepath_topicbook, 'r') as file:
                userdata = json.load(file)
            file.close()
            bookindex,booknames = userdata[topic]
            self.bookindex = bookindex
            return booknames
        except:
            return None
    #======================== save data
    def switchbooks_next(self):
        
        print(f"switchbook topic = {self.topic}")
        _, booknames = self.data_topicbook[self.topic]
        nr_book_indices = len(booknames)-1
        if self.bookindex < nr_book_indices:
            self.bookindex += 1
            self.bookname = booknames[self.bookindex]
            print(f"index = {self.bookname}")
        self.savedata()    
        
    def switchbooks_previous(self):
        if self.bookindex > 0:
            self.bookindex -= 1
        self.savedata()
    
    def getcurrentbook(self,topic):
        self.topic = topic
        try:
            with open(self.datafilepath_topicbook, 'r') as file:
                userdata = json.load(file)
            file.close()
            
            _,booknames = userdata[topic]
            
            
            return booknames[self.bookindex]
        except:
            return None
    
    
    def loaddata(self):
        self.data_topicbook = {}
        try:
            with open(self.datafilepath_topicbook, 'r') as file:
                self.data_topicbook = json.load(file)
            file.close()
            return self.data_topicbook
        except:
            return None
            pass
    
        
    def savedata(self):
        try:
            with open(self.datafilepath_topicbook, 'w') as file:
                file.write(json.dumps(self.data_topicbook))
            file.close()
            self.newuser = False
        except:
            pass        
    
    
    
    
    def deletetopic(self):
        index = self.listctrl.GetFocusedItem()  
        print(f"index = {index}")
        if index >= 0: #error code is -1
            print(f"found entry")
            
            
            oldtopic = self.listctrl.GetItemText(index)
            
            
            if oldtopic in self.data_topicbook:                
                self.data_topicbook.pop(oldtopic,None)
            
            self.mainframe.m_textTopic.SetValue('') 
            self.savedata()
            self.showdata()
            self.listctrl.Focus(index)   
            self.listctrl.Select(index)
        
    def renametopic(self):
        index = self.listctrl.GetFocusedItem()  
        print(f"index = {index}")
        if index >= 0: #error code is -1
            print(f"found entry")
            
            
            oldtopic = self.listctrl.GetItemText(index)
            newtopic = self.mainframe.m_textTopic.GetValue()
            
            if newtopic.strip():
                if oldtopic in self.data_topicbook and newtopic not in self.data_topicbook:
                    self.bookindex,books = self.data_topicbook[oldtopic] 
                    self.data_topicbook.pop(oldtopic,None)
                    self.data_topicbook[newtopic] = [self.bookindex,books]
                
                self.mainframe.m_textTopic.SetValue('') 
                self.savedata()
                self.showdata()
                self.listctrl.Focus(index)   
                self.listctrl.Select(index)
        
    def addbook(self):
        index = self.listctrl.GetFocusedItem()        
        if index >= 0: #error code is -1
            topic = self.listctrl.GetItemText(index)
            
            
            #%%
            
            with wx.FileDialog(self.mainframe, "Choose a PDF",defaultDir=str(self.mainframe.dirpdfbook), wildcard="*.pdf",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                #fileDialog.SetPath(str(self.mainframe.dirpdfbook)+'\.') 
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return None    # the user changed their mind
                else:
                    filepath = fileDialog.GetPath()
                    if str(self.mainframe.dirpdfbook) not  in str(filepath):
                        #pdf is not yet imported into correct folder and is selected from elsewhere
                        src = filepath
                        dst = self.mainframe.dirpdfbook
                        shutil.copy2(src, dst, follow_symlinks=True)
                        
                    filename = os.path.basename(filepath)
                    
                    if topic in self.data_topicbook:
                        self.bookindex, booknames = self.data_topicbook[topic]                        
                        booknames += [filename]
                        self.data_topicbook[topic] = [self.bookindex,booknames]
                        #self.data_topicbook[topic] += [filename]
                    else:
                        self.data_topicbook[topic] = [self.bookindex,[filename]]
                    self.savedata()
                    self.showdata()
                    
            self.listctrl.Focus(index)   
            self.listctrl.Select(index)
        else:
            if len(self.data_topicbook) == 1:
                topic = list(self.data_topicbook.keys())[0]
                #if only one topic exists choose that one,
                with wx.FileDialog(self.mainframe, "Choose a PDF",defaultDir=str(self.mainframe.dirpdfbook), wildcard="*.pdf",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                    #with wx.DirDialog(self.mainframe, "Choose which book to open",style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST,defaultPath=str(self.mainframe.booksdir)) as DirDialog:
                    #fileDialog.SetPath(str(self.notesdir)+'\.')
                    if fileDialog.ShowModal() == wx.ID_CANCEL:
                        return None    # the user changed their mind
                    else:
                        filepath = fileDialog.GetPath()
                        filename = os.path.basename(filepath)
                        print(f"found entry")
                        
                        
                        print(f"topic = {topic}")
                        if topic in self.data_topicbook:
                            self.bookindex, booknames = self.data_topicbook[topic]
                            booknames += [filename]
                            self.data_topicbook[topic] = [self.bookindex,booknames]
                            
                        else:
                            self.data_topicbook[topic] = [self.bookindex,[filename]]
                        self.savedata()
                        self.showdata()
                self.listctrl.Focus(index)   
                self.listctrl.Select(index)    
            elif len(self.data_topicbook) > 1:
                MessageBox(0, "Select the topic to which you want to add the book!", "Error", MB_ICONINFORMATION)
                pass
                #if multiple topics exist but none were chosen, it is not clear to which it should be added, inform user
                
    def addtopic(self):
        topic = self.mainframe.m_textTopic.GetValue()
        if topic.rstrip():#entry should not be empty
            if topic not in self.data_topicbook:
                self.data_topicbook[topic] = [self.bookindex,[]]
                self.savedata()
                self.showdata()
            
            self.mainframe.m_textTopic.SetValue('')
        else:
            MessageBox(0, "You must fill in a name of the topic in the textbox!", "Error", MB_ICONINFORMATION)
        pass
    
    def User_is_New(self):
        """A user uses this program for the first time and no books/topics have been added"""
        return self.newuser