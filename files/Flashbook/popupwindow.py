# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 20:09:56 2020

@author: Anton
"""
import wx
import _shared_operations.imageoperations as imop
class Window2(wx.PopupWindow):
    def __init__(self, parent, style,image):
        wx.PopupWindow.__init__(self, parent, style)
        border = 10
        panel = wx.Panel(self)
        
        panel.SetBackgroundColour(wx.Colour(179, 236, 255) )        
        
        self.m_bitmap123 = wx.StaticBitmap( panel, wx.ID_ANY, wx.NullBitmap,[border,border], wx.DefaultSize, 0 ) #displace image by width of border
        st = wx.StaticBitmap( panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        width, height = image.size
        image2 = wx.Image( width, height )
        image2.SetData( image.tobytes() )
        self.m_bitmap123.SetBitmap(wx.Bitmap(image2))   
        self.SetSize( (width+2*border ,height+2*border) )
        panel.SetSize( (width+2*border, height+2*border) )
      
        panel.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        panel.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        panel.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        panel.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)        
        st.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        st.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        st.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        st.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)       
        wx.CallAfter(self.Refresh)       
    
    def OnMouseLeftDown(self, evt):
        self.Refresh()
        self.ldPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        self.wPos = self.ClientToScreen((0,0))
        self.panel.CaptureMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            dPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
            nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
                    self.wPos.y + (dPos.y - self.ldPos.y))
            self.Move(nPos)
        #dont move just destroy
        self.Show(False)
        self.Destroy()
    def OnMouseLeftUp(self, evt):
        if self.panel.HasCapture():
            self.panel.ReleaseMouse()
        #dont move just destroy
        self.Show(False)
        self.Destroy()
    def OnRightUp(self, evt):#orininal
        self.Show(False)
        self.Destroy()


def ShowInPopup(self,event,mode):
    # a picture directory may not exist
    dir_ = self.Flashcard.getpiclist(mode)
    try:
        if type(dir_) == list: 
            directory = dir_[0]
        else: 
            directory = dir_
    except:
        pass
    
    usertext = self.usertext
    _, img_text  = imop.CreateTextCard(self,usertext)
    try:
        _, img_pic   = imop.findpicture_path(self,directory)
        self.image  = imop.CombinePics(img_text,img_pic)
    except:
        self.image = img_text
    try:
        image = self.image
        """Try to access mousepos, if there wasn't any mouseclick: then just place the popupwindow in the middle of your screen. 
        this is the case if you only entered text, but didn't select anything with the mouse"""
        try:
            a = self.mousepos  
        except:
            self.mousepos = (int(wx.GetDisplaySize()[0]/2),int(wx.GetDisplaySize()[1]/2))
            
        win = Window2(self.GetTopLevelParent(), wx.SIMPLE_BORDER,image)    
        win.Position((self.mousepos[0]-10,self.mousepos[1]-10), (0,0))
        win.Show(True)  
        if hasattr(self,'imagetext'):
            delattr(self, 'imagetext')
        self.image = []
    except:
        # this is a normal occurance when you switch between Q and A
        pass




