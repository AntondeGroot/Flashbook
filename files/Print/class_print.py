# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:33:22 2019

@author: Anton
"""
import _GUI.gui_flashbook as gui
import threading
import _shared_operations.latexoperations as ltx
import wx
import PIL
import program as p
import Print.print_modules as m3
import _logging.log_module    as log
ICON_EXCLAIM=0x30

import ctypes
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100

def BoxesChecked(self,n):
    CHECKED1 = self.m_checkBox_col1.IsChecked()
    CHECKED2 = self.m_checkBox_col2.IsChecked()
    CHECKED3 = self.m_checkBox_col3.IsChecked()
    if n == 1:
        return CHECKED1
    elif n == 2:
        return CHECKED2
    elif n == 3:
        return CHECKED3
    else:
        log.ERRORMESSAGE("Error: invalid entry in BoxesChecked")
        return False


class printer(gui.MyFrame):
    def __init__(self):
        pass
    def m_OpenPrintOnButtonClick(self,event):
        #initialize variables
        self.bookname       = ''
        self.BorderCoords   = []         
        self.colorlist      = self.bordercolors
        self.currentpage    = 1
        self.cursor         = False    # normal cursor
        self.drawborders    = True
        self.image          = []
        self.imagecopy      = []
        self.tempdictionary = {}
        self.panel_pos      = (0,0)        
        self.questionmode   = True
        self.zoom           = 1.0
        
        self.onlyinitiate = 0
        self.onlyonce = 0
        self.onlyatinitialize = 0
        """START MAIN PROGRAM : PRINT PDF NOTES"""
        t_panel = lambda self,page : threading.Thread(target = p.SwitchPanel , args=(self,page )).start()
        t_panel(self, 3) 
        self.settings_get()                
        
        
        self.m_colorQAline.SetColour(self.QAline_color)
        self.m_colorPDFline.SetColour(self.horiline_color)
        self.m_colorVERTline.SetColour(self.vertline_color)
        
        self.m_lineWpdf.SetValue(str(self.horiline_thickness))
        self.m_lineWqa.SetValue(str(self.QAline_thickness))
        self.m_lineWvert.SetValue(str(self.vertline_thickness))
        
        self.m_lineQA.SetValue(self.QAline_bool)
        self.m_linePDF.SetValue(self.horiline_bool)            
        self.m_lineVERT.SetValue(self.vertline_bool)
        self.m_checkBoxSameColor.SetValue(self.samecolor_bool)
        
        self.m_sliderPDFsize.SetValue(int(200-self.pdfmultiplier*100))
        self.m_slider_col1.SetValue(self.pdfPageColsPos[0])
        self.m_slider_col2.SetValue(self.pdfPageColsPos[1])
        self.m_slider_col3.SetValue(self.pdfPageColsPos[2])
        self.m_checkBox_col1.SetValue(self.pdfPageColsChecks[0])
        self.m_checkBox_col2.SetValue(self.pdfPageColsChecks[1])
        self.m_checkBox_col3.SetValue(self.pdfPageColsChecks[2])
        import os
        notesdir = self.notesdir
        
        #%%
        # When Flashbook is run in the Spyder IDE it may not open the correct folder, this however is no problem when it is run
        #       as an executable. In that case the whole 'defaultFile' isn't even necessary.
        #       when the defaultdir and the defaultfile match: it will open the dir one above the one you actually want to open
        #       if the defaultfile is a file within the defaultdir it works as it should be. In this case it is not a problem
        #       because there's always 1 file present.
        if os.listdir(notesdir) != []:
            defaultfile = os.path.join(notesdir,os.listdir(notesdir)[0])
        else:
            defaultfile = notesdir
        #%%
        with wx.FileDialog(self, "Choose which file to print", defaultDir = str(notesdir), defaultFile = defaultfile, 
                           wildcard="*.tex", style=wx.FD_DEFAULT_STYLE ) as fileDialog:
            
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                p.SwitchPanel(self,0) 
                return None    # the user changed their mind
            else:
                
                self.SetCursor(wx.Cursor(wx.CURSOR_ARROWWAIT))
                self.fileDialog = fileDialog
                self.FilePickEvent = True
                
                t_preview = lambda self : threading.Thread(target = m3.print_preview, name = 't_preview' , args=(self,)).run()
                t_preview(self) 
                
    def m_bitmap3OnMouseWheel( self, event ):
        wheel_rotation  = event.GetWheelRotation()   # get rotation from mouse wheel
        wheel_scrollsup = wheel_rotation > 0 
        wheel_scrollsdown = wheel_rotation < 0
        if wheel_scrollsup:
            self.m_pdfButtonPrevOnButtonClick(event)
        if wheel_scrollsdown:
            self.m_pdfButtonNextOnButtonClick(event)

    def m_sliderPDFsizeOnScrollChanged(self,event):
        self.pdfmultiplier = float(200-self.m_sliderPDFsize.GetValue())/100
        self.settings_set()
        m3.print_preview(self)
    
    def m_lineQAOnCheckBox( self, event ):
        self.onlyonce = 0
        self.FilePickEvent = False
        self.QAline_bool = self.m_lineQA.GetValue()
        self.settings_set()
        m3.print_preview(self)
        
    def m_linePDFOnCheckBox( self, event ):
        self.FilePickEvent = False
        self.horiline_bool = self.m_linePDF.GetValue()
        self.settings_set()
        m3.print_preview(self)
        
    def m_lineVERTOnCheckBox( self, event):
        self.FilePickEvent = False
        self.vertline_bool = self.m_lineVERT.GetValue()
        self.settings_set()
        m3.print_preview(self)
    
    def m_bitmap3OnLeftDown(self, event):
        
        self.pdfmousepos = self.m_bitmap3.ScreenToClient(wx.GetMousePosition())
        
        W, H = self.m_panel32.GetSize()
        Wp = self.pdfmousepos[0]/W*self.a4page_w - round(0.05 * self.a4page_w)/W
        Hp = self.pdfmousepos[1]/H*self.a4page_h - round(0.05 * self.a4page_h)/H
        
        pagerectdict = self.pdfpage.get_cardrect()
        self.RectangleDetection = m3.RectangleDetection(pagerectdict)
        key = self.RectangleDetection.findRect((Wp,Hp))
        index = key[0][1:]
        trueindex = int(index)        
        ltx.ShowPopupCard(self,trueindex)
        m3.notes2paper(self)     

    def m_colorQAlineOnColourChanged( self, event ):
        original_color = self.QAline_color
        self.FilePickEvent = False
        RGB = self.m_colorQAline.GetColour()
        self.QAline_color  = (RGB.Red(),RGB.Green(),RGB.Blue())   
        if original_color != self.QAline_color:
            self.settings_set()
            m3.print_preview(self)
        
    def m_colorPDFlineOnColourChanged( self, event ):
        original_color = self.horiline_color
        self.FilePickEvent = False
        RGB = self.m_colorPDFline.GetColour()
        self.horiline_color  = (RGB.Red(),RGB.Green(),RGB.Blue())    
        
        if self.m_checkBoxSameColor.GetValue():
            if self.vertline_color != original_color or self.horiline_color != original_color:
                self.vertline_color  = self.horiline_color 
                self.m_colorVERTline.SetColour(self.horiline_color)
                self.settings_set()
                m3.print_preview(self)
        else:
            if self.horiline_color != original_color:
                self.settings_set()
                m3.print_preview(self)
        
    def m_colorVERTlineOnColourChanged( self, event):
        original_color = self.vertline_color
        RGB = self.m_colorVERTline.GetColour()
        if self.m_checkBoxSameColor.GetValue():
            #self.vertline_color  = self.horiline_color
            self.vertline_color = (RGB.Red(),RGB.Green(),RGB.Blue()) 
            self.horiline_color  = self.vertline_color
            new_color = self.horiline_color
            self.m_colorVERTline.SetColour(self.vertline_color)
            self.m_colorPDFline.SetColour(self.horiline_color)
        else:
            self.FilePickEvent = False
            self.vertline_color  = (RGB.Red(),RGB.Green(),RGB.Blue())    
            new_color = self.vertline_color 
            
        if original_color != new_color:
            #In case you chose the exact same color do nothing
            self.settings_set()
            m3.print_preview(self)
        
        
        
    def m_PrintFinalOnButtonClick( self, event ):
        
        
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROWWAIT))
        self.printsuccessful = False
        self.printpreview    = False
        self.FilePickEvent   = False
        m3.print_preview(self)
        if self.printsuccessful:
            self.printpreview = True
            p.SwitchPanel(self,0)
            # remove all temporary files of the form "temporary(...).png"    
            if not self.debugmode:
                folder = self.tempdir
                [file.unlink() for file in folder.iterdir() if ("temporary" in file.name and file.suffix =='.png' )]
            MessageBox(0, " Your PDF has been created!\n Select in the menubar: `Open/Open PDF-notes Folder` to\n open the folder in Windows explorer. ", "Message", MB_ICONINFORMATION)
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
         
    def m_pdfCurrentPageOnTextEnter( self, event ):
        try:
            var = self.m_pdfCurrentPage.GetValue()
            if var == "":
                self.NrCardsPreview = ''
            elif int(var) > 0:
                self.NrCardsPreview = int(var)
                
            self.settings_set()
            m3.print_preview(self)
        except:
            log.ERRORMESSAGE("Error: invalid entry in CtrlNrCardsOnText")
            
    def m_lineWpdfOnText( self, event ):
        
        try:            
            if int(self.m_lineWpdf.GetValue()) >= 0:
                if int(self.m_lineWpdf.GetValue()) != self.horiline_thickness:
                    #only execute if the value has changed
                    self.horiline_thickness = int(self.m_lineWpdf.GetValue())
                    self.settings_set()
                    m3.print_preview(self)
        except:
            log.ERRORMESSAGE("Error: invalid entry in lineWpdf")
            
    def m_lineWqaOnText( self, event ):
        self.onlyonce = 0
        try:            
            if int(self.m_lineWqa.GetValue()) >= 0:
                if int(self.m_lineWqa.GetValue()) != self.QAline_thickness:
                    self.QAline_thickness = int(self.m_lineWqa.GetValue())
                    self.settings_set()
                    m3.print_preview(self)
        except:
            log.ERRORMESSAGE("Error: invalid entry QAline thickness")
            
    def m_lineWvertOnText( self, event ):
        try:            
            if int(self.m_lineWvert.GetValue()) >= 0:
                if int(self.m_lineWvert.GetValue()) != self.vertline_thickness:
                    #only execute if the value has changed
                    self.vertline_thickness = int(self.m_lineWvert.GetValue())
                    self.settings_set()
                    m3.print_preview(self)
        except:
            log.ERRORMESSAGE("Error: invalid entry")  
    def m_checkBoxSameColorOnCheckBox(self,event):
        self.samecolor_bool = self.m_checkBoxSameColor.IsChecked()
        #check if it has been checked
        if self.samecolor_bool:
            if self.vertline_color != self.horiline_color:
                self.FilePickEvent = False
                self.vertline_color = self.horiline_color     
                self.m_colorVERTline.SetColour(self.vertline_color)     
                self.settings_set()
                m3.print_preview(self)
    def m_slider_col1OnScrollChanged(self, event):
        self.pdfPageColsPos[0] = self.m_slider_col1.GetValue()
        self.settings_set()
        if BoxesChecked(self,1):
            t_preview = lambda self : threading.Thread(target = m3.print_preview, name = 't_preview' , args=(self, )).run()
            t_preview(self) 
            
            
            
    def m_slider_col2OnScrollChanged(self, event):
        self.pdfPageColsPos[1] = self.m_slider_col2.GetValue()
        self.settings_set()
        if BoxesChecked(self,2):
            t_preview = lambda self : threading.Thread(target = m3.print_preview, name = 't_preview' , args=(self, )).run()
            t_preview(self) 
            
    def m_slider_col3OnScrollChanged(self, event):
        self.pdfPageColsPos[2] = self.m_slider_col3.GetValue()
        self.settings_set()
        if BoxesChecked(self,3):
            t_preview = lambda self : threading.Thread(target = m3.print_preview, name = 't_preview' , args=(self, )).run()
            t_preview(self) 
            
    def m_checkBox_col1OnCheckBox( self, event ):
        self.pdfPageColsChecks[0] = self.m_checkBox_col1.GetValue()
        self.settings_set()
        t_preview = lambda self : threading.Thread(target = m3.print_preview, name = 't_preview' , args=(self, )).run()
        t_preview(self) 
            
    def m_checkBox_col2OnCheckBox( self, event ):
        self.pdfPageColsChecks[1] = self.m_checkBox_col2.GetValue()
        self.settings_set()
        t_preview = lambda self : threading.Thread(target = m3.print_preview, name = 't_preview' , args=(self, )).run()
        t_preview(self) 
            
    def m_checkBox_col3OnCheckBox( self, event ):
        self.pdfPageColsChecks[2] = self.m_checkBox_col3.GetValue()
        self.settings_set()
        t_preview = lambda self : threading.Thread(target = m3.print_preview, name = 't_preview' , args=(self, )).run()
        t_preview(self) 
    def m_pdfButtonPrevOnButtonClick( self, event ):
        self.pdfpage.prevpage()
        pdfimage_i = self.pdfpage.loadpage()
        # display result
        _, PanelHeight = self.m_panel32.GetSize()
        PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
        #only select first page and display it on the bitmap
        
        image = pdfimage_i
        image = image.resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS)
        image2 = wx.Image( image.size)
        image2.SetData( image.tobytes() )
        
        bitmapimage = wx.Bitmap(image2)
        self.m_bitmap3.SetBitmap(bitmapimage)
        self.Layout()
        
        #page info
        currentpage, maxpage = self.pdfpage.getpageinfo()
        self.m_pdfCurrentPage.SetValue(f"{currentpage}/{maxpage}")
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
	
    def m_pdfButtonNextOnButtonClick( self, event ):
        self.pdfpage.nextpage()
        pdfimage_i = self.pdfpage.loadpage()
        # display result
        _, PanelHeight = self.m_panel32.GetSize()
        PanelWidth = round(float(PanelHeight)/1754.0*1240.0)
        #only select first page and display it on the bitmap
        
        image = pdfimage_i
        image = image.resize((PanelWidth, PanelHeight), PIL.Image.ANTIALIAS)
        image2 = wx.Image( image.size)
        image2.SetData( image.tobytes() )
        
        bitmapimage = wx.Bitmap(image2)
        self.m_bitmap3.SetBitmap(bitmapimage)
        self.Layout()
        
        #page info
        currentpage, maxpage = self.pdfpage.getpageinfo()
        self.m_pdfCurrentPage.SetValue(f"{currentpage}/{maxpage}")
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
