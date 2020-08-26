# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 21:56:19 2020

@author: Anton
"""
import wx
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
        if not self.screenshotmode:
            img = PIL.Image.open(self.jpgdir)
        else:
            img = self.pageimage
        img = np.array(img)            
        img = img[y0:y1,x0:x1]
        img = PIL.Image.fromarray(img)
        FIND = True
        while FIND:
            rand_nr = str(randint(0, 9999)).rjust(4, "0") #The number must be of length 4: '0006' must be a possible result.
            if not self.screenshotmode:
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
    


def setcursor(self):
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))