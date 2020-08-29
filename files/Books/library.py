# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 08:40:20 2020

@author: Anton
"""
import _GUI.active_panel as panel
import _GUI.gui_flashbook as gui
import json

class Library(gui.MyFrame):
    def __init__(self,mainframe):
        """self. is the selfvariable of this class
        self.mainframe is the 'self' variable of the main gui 
        This way you can still access all panels etc from the original GUI"""
        
        self.bookwidth = 250
        self.topicwidth = 120
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
        self.listctrl.SetColumnWidth(0,self.topicwidth)
        """Determine how many columns you need"""
        columnnr = 1
        for entry in self.userdata.values():
            if len(entry) > columnnr:
                columnnr = len(entry)
        """Set nr of columns """
        self.listctrl.InsertColumn(0, "Topic")
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
            self.listctrl.Append(topic+books)
    
    
    def showdata(self):
        self.cleargrid()
        self.loaddata()
        if not self.userdata:
            self.showcasefunctionality()
        else:
            self.setcolumns()
            self.setdata()
            self.setcolumns()
        panel.SwitchPanel(self.mainframe,7)
        
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
    
    def addbook(self,event):
        index = self.listctrl.GetFocusedItem()        
        if index >= 0: #error code is -1
            print(f"found entry")
            
            topic = self.listctrl.GetItemText(index)
            print(f"topic = {topic}")
            if topic in self.userdata:
                self.userdata[topic] += ["booklabel"]
            else:
                self.userdata[topic] = ["booklabel"]
            self.savedata()
            self.showdata()
            
    def addtopic(self,event):
        topic = self.mainframe.m_textTopic.GetValue()
        if topic.rstrip():#entry should not be empty
            if topic not in self.userdata:
                self.userdata[topic] = []
                self.savedata()
                self.showdata()
                
            #self.listctrl.Append([topic])
            self.mainframe.m_textTopic.SetValue('')
        
        
        pass