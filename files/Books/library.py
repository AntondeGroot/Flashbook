# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 08:40:20 2020

@author: Anton
"""
import _GUI.active_panel as panel
import _GUI.gui_flashbook as gui
import json
import os
import wx

class Library(gui.MyFrame):
    def __init__(self,mainframe):
        """self. is the selfvariable of this class
        self.mainframe is the 'self' variable of the main gui 
        This way you can still access all panels etc from the original GUI"""
        
        self.bookwidth = 250
        self.topicwidth = 150
        self.listctrl = mainframe.m_listTopics
        self.mainframe = mainframe
        self.topic_books = {}
        self.itemselected = None
        self.datafilepath = mainframe.dir_topicbook_file
        pass
        
        
    def cleargrid(self):
        self.listctrl.ClearAll()
    
    
    def setcolumns(self):
        
        self.userdata
        
        """Determine how many columns you need"""
        columnnr = 1
        for entry in self.userdata.values():
            if len(entry) > columnnr:
                columnnr = len(entry)
        """Set nr of columns """
        self.listctrl.InsertColumn(0, "Topic")
        self.listctrl.SetColumnWidth(0,self.topicwidth)
        for i in range(columnnr):
            self.listctrl.InsertColumn(i+1, f"Book title {i+1}")
            self.listctrl.SetColumnWidth(i+1,self.bookwidth)
        """resize ListCtrl"""
        panelwidth = self.topicwidth + self.bookwidth*columnnr
        self.listctrl.SetSize(panelwidth,-1)
        
    def setdata(self):
        for key in self.userdata:
            topic = [key]
            books = self.userdata[key]
            print(f"tb = {topic+books}")
            self.listctrl.Append(topic+books)
        
    
    def showdata(self):
        self.cleargrid()
        self.loaddata()
        panel.SwitchPanel(self.mainframe,7)
        
        if not self.userdata:
            self.showcasefunctionality()
        else:
            self.setcolumns()
            self.setdata()
            
        
        
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
    
    def getbooknames(self,topic):
        
        try:
            with open(self.datafilepath, 'r') as file:
                userdata = json.load(file)
            file.close()
            return userdata[topic]
        except:
            return None
    
    def loaddata(self):
        self.userdata = {}
        try:
            with open(self.datafilepath, 'r') as file:
                self.userdata = json.load(file)
            file.close()
        except:
            pass
    
    def savedata(self):
        try:
            with open(self.datafilepath, 'w') as file:
                file.write(json.dumps(self.userdata))
            file.close()
        except:
            pass        
        
    def deletetopic(self,event):
        index = self.listctrl.GetFocusedItem()  
        print(f"index = {index}")
        if index >= 0: #error code is -1
            print(f"found entry")
            
            
            oldtopic = self.listctrl.GetItemText(index)
            
            
            if oldtopic in self.userdata:                
                self.userdata.pop(oldtopic,None)
            
            self.mainframe.m_textTopic.SetValue('') 
            self.savedata()
            self.showdata()
            self.listctrl.Focus(index)   
            self.listctrl.Select(index)
        
    def renametopic(self,event):
        index = self.listctrl.GetFocusedItem()  
        print(f"index = {index}")
        if index >= 0: #error code is -1
            print(f"found entry")
            
            
            oldtopic = self.listctrl.GetItemText(index)
            newtopic = self.mainframe.m_textTopic.GetValue()
            
            if oldtopic in self.userdata and newtopic not in self.userdata:
                books = self.userdata[oldtopic] 
                self.userdata.pop(oldtopic,None)
                self.userdata[newtopic] = books
            
            self.mainframe.m_textTopic.SetValue('') 
            self.savedata()
            self.showdata()
            self.listctrl.Focus(index)   
            self.listctrl.Select(index)
        
    def addbook(self,event):
        index = self.listctrl.GetFocusedItem()        
        if index >= 0: #error code is -1
            with wx.DirDialog(self.mainframe, "Choose which book to open",style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST,defaultPath=str(self.mainframe.booksdir)) as DirDialog:
                #fileDialog.SetPath(str(self.notesdir)+'\.')
                if DirDialog.ShowModal() == wx.ID_CANCEL:
                    return None    # the user changed their mind
                else:
                    dirpath = DirDialog.GetPath()
                    filename = os.path.basename(dirpath)
                    print(f"found entry")
                    
                    topic = self.listctrl.GetItemText(index)
                    print(f"topic = {topic}")
                    if topic in self.userdata:
                        self.userdata[topic] += [filename]
                    else:
                        self.userdata[topic] = [filename]
                    self.savedata()
                    self.showdata()
            self.listctrl.Focus(index)   
            self.listctrl.Select(index)
            
    def addtopic(self,event):
        topic = self.mainframe.m_textTopic.GetValue()
        if topic.rstrip():#entry should not be empty
            if topic not in self.userdata:
                self.userdata[topic] = []
                self.savedata()
                self.showdata()
            
            self.mainframe.m_textTopic.SetValue('')
        pass