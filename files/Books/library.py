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
        
    #======================== cosmetic    
    def cleargrid(self):
        self.listctrl.ClearAll()
    
    def setcolumns(self):
        """Determine how many columns you need"""
        columnnr = 1
        
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
            
            print(topic)
            bookindex,books = topicbook[topic]            
            row += books
            print(f"books = {books}")
            print(f"topic + books = {row}")
            self.listctrl.Append(row)
            
        
    def showdata(self):
        self.cleargrid()
        self.loaddata()
        panel.SwitchPanel(self.mainframe,7)
        if not self.data_topicbook:
            self.showcasefunctionality()
        else:
            self.setcolumns()
            self.setdata()

    #======================== show how to use it to new users    
    def showcasefunctionality(self):
        """Ïf there are no books, showcase how it is used""" 
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

    #======================== save data
    """
    def savewhichbook(self):
        topic = self.topic
        "topic : [bookindex,[book1.pdf, ... , bookN.pdf]]"
        path_file = Path(self.mainframe.dirsettings, 'userdata_topicbook.txt')
        if path_file.exists():
            with open(path_file,'r') as file:
                dictionary = json.load(file)        
                #dictionary[self.bookname] = self.currentpage
                if topic in dictionary:
                    self.bookindex,_ ,_ =  dictionary[topic]
                else:
                    dictionary[topic]= [self.mainframe.bookindex, self.booknames]
                file.close()
        else:
            dictionary = {topic: [self.mainframe.bookindex, self.booknames]}
        with open(path_file,'w') as file:
            file.write(json.dumps(dictionary))
            file.close()
    """    
        

    
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
            
        except:
            pass
    
    def savedata(self):
        try:
            with open(self.datafilepath_topicbook, 'w') as file:
                file.write(json.dumps(self.data_topicbook))
            file.close()
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
            
            
            with wx.DirDialog(self.mainframe, "Choose which book to open",style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST,defaultPath=str(self.mainframe.booksdir)) as DirDialog:
                #fileDialog.SetPath(str(self.notesdir)+'\.')
                if DirDialog.ShowModal() == wx.ID_CANCEL:
                    return None    # the user changed their mind
                else:
                    dirpath = DirDialog.GetPath()
                    filename = os.path.basename(dirpath)
                    print(f"found entry")
                    
                    
                    print(f"topic = {topic}")
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
                with wx.DirDialog(self.mainframe, "Choose which book to open",style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST,defaultPath=str(self.mainframe.booksdir)) as DirDialog:
                    #fileDialog.SetPath(str(self.notesdir)+'\.')
                    if DirDialog.ShowModal() == wx.ID_CANCEL:
                        return None    # the user changed their mind
                    else:
                        dirpath = DirDialog.GetPath()
                        filename = os.path.basename(dirpath)
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
        pass
