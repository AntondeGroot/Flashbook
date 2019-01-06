# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 12:41:59 2019

@author: Anton
"""

import os
from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
import ctypes

def ConvertPDF_to_JPG(self):
    
    #First checks all of the books have been converted# 
    #datadir = os.getenv("LOCALAPPDATA")
    #dir0 = datadir+r"\FlashBook"
    #dir3 = dir0 + r"\books"
    #dirpdfbook = dir0 + r"\PDF books"
    
    arr_pdf = [f for f in os.listdir(self.dirpdfbook) if '.pdf' in f]
    
    for i, item in enumerate(arr_pdf):
        pdfname = item[:-4]
        
        origin_dir = os.path.join(self.dirpdfbook, item)
        target_dir = os.path.join(self.dir3, pdfname)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)        
        
        try:
            os.listdir(target_dir)
        except:
            ctypes.windll.user32.MessageBoxW(0, f'The file "{pdfname}.pdf" probably has a space in its name between the name and the ".pdf" extension.\nPlease remove this space.\nOtherwise it is a different error in os.Listdir', "Error", 1)            
        try:
            if os.listdir(target_dir) == []:
                #The method convert_from_path will work for a lot of pdfs                 #
                #Yet when this method fails convert_from_bytes might convert pdfs that    #
                #couldn't be converted with from_path, if both methods don't work the user#
                #is informed to use an online-converter instead.                          #
                pages = convert_from_path(item, 170)
                if pages == []:
                    pages = convert_from_bytes(open(origin_dir, 'rb').read())
                    
                if pages != []:
                    ctypes.windll.user32.MessageBoxW(0, f'The file "{pdfname}.pdf" could not be converted to jpg.\nPlease use an online pdf converter instead.\nThen place the jpg files in a map folder named after the book in {self.dir3}', "Warning", 1)            
                    
                if pages != []:
                    i = 1
                    for page in pages:
                        filename = os.path.join(target_dir, pdfname)
                        nr = "0"*(4-len(f"{i}"))+f"{i}"
                        page.save(f'{filename}{nr}.jpg', 'JPEG')
                        i += 1
        except:
            pass
