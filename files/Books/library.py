# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 08:40:20 2020

@author: Anton
"""
import _GUI.active_panel as panel
import _GUI.gui_flashbook as gui

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
        pass
        
        
    def clear(self):
        self.listctrl.ClearAll()
        
    def showcasefunctionality(self):
        """Ïf there are no books, showcase how it is used"""
    
        Topic = ["Example: Physics"]
        Booktitles = ["Classical Mechanics for dummies.pdf", "Classical Mechanics for noobs.pdf","Homework assignments.pdf"]
        
        self.clear()
        
        
        panel.SwitchPanel(self.mainframe,7)
        
        
        self.listctrl.InsertColumn(0, "Topic")
        self.listctrl.SetColumnWidth(0,self.topicwidth)
        for i in range(len(Booktitles)):
            self.listctrl.InsertColumn(i+1, f"Book title {i+1}")
            self.listctrl.SetColumnWidth(i+1,self.bookwidth)
        self.listctrl.Append(Topic + Booktitles)
        
        panelwidth = self.topicwidth + self.bookwidth*len(Booktitles)
        self.listctrl.SetSize(panelwidth,-1)
    
         
    def m_buttonTopicOnButtonClick(self,event):
        print("test")
            
    def get_books():
        pass
    def itemselect(self):
        pass        
    
    def addbook(self,event):
        print(self.listctrl.GetItemText(0,0))
        index = self.listctrl.GetFocusedItem()
        print(index)
        
        
        if index >= 0: #error code is -1
            topic = self.listctrl.GetItemText(index)
            self.listctrl.DeleteItem (index)
            self.listctrl.Append([topic, "label"])
        print("end")

    def addtopic(self,event):
        topic = self.mainframe.m_textTopic.GetValue()
        if topic.rstrip():
            if not self.topic_books:
                self.clear()    
                self.listctrl.InsertColumn(0, "Topic")
                self.listctrl.InsertColumn(1, "Book title 1")
                self.topic_books = {topic : None}
            self.listctrl.Append([topic])
            self.mainframe.m_textTopic.SetValue('')
        
        
        pass