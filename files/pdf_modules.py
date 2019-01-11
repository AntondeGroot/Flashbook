# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 12:41:59 2019

@author: Anton
"""

import os
from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
import ctypes
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040

def ConvertPDF_to_JPG(self):
    
    """Convert a PDF to JPG files.
    
    Arguments: 
        self.dirpdfbook -- where the PDF is located
        self.dir3       -- where the JPG should be exported to
    
    Method:
        Use module pdf2image.
        Try functions 'convert_from_path' and 'convert_from_bytes' for conversion.
        If both methods fail user gets instructed to use online-converter instead."""
    
    MessageBox = ctypes.windll.user32.MessageBoxW   
    MessageBox(0, f'The PDF -> JPG conversion has started.\nIt may take a few minutes per book and it is RAM heavy.\nYou may need an online converter if this causes trouble.', "Message", MB_ICONINFORMATION)            
    arr_pdf = [f for f in os.listdir(self.dirpdfbook) if '.pdf' in f]
    i = 1
    for _, item in enumerate(arr_pdf):
        
        pdfname = item[:-4]
        origin_dir = os.path.join(self.dirpdfbook, item)
        target_dir = os.path.join(self.dir3, pdfname)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)                
        try:
            os.listdir(target_dir)
        except:
            MessageBox(0, f'The file "{pdfname}.pdf" probably has a space in its name between the name and the ".pdf" extension.\nPlease remove this space.\nOtherwise it is a different error in os.Listdir', "Error", ICON_STOP)            
        try:
            if os.listdir(target_dir) == []:                
                pages = convert_from_path(origin_dir, 170)
                if pages == []:
                    pages = convert_from_bytes(open(origin_dir, 'rb').read())         
                if pages == []:
                    MessageBox(0, f'The file "{pdfname}.pdf" could not be converted to jpg.\nPlease use an online pdf converter instead.\nThen place the jpg files in a map folder named after the book in {self.dir3}', "Warning", ICON_STOP)            
                    
                if pages != []:
                    i = 1
                    MessageBox(0, f'{item} has been converted and is being saved', "Message",  MB_ICONINFORMATION)    
                    for page in pages:
                        filename = os.path.join(target_dir, pdfname)
                        nr = "0"*(4-len(f"{i}"))+f"{i}"
                        page.save(f'{filename}-{nr}.jpg', 'JPEG')
                        i += 1
               
        except:
            pass
    if i != 1:
        MessageBox(0, f'Finished converting all books.', "Message", MB_ICONINFORMATION)
    else:
        MessageBox(0, f'Finished, no books needed to be converted.', "Message", MB_ICONINFORMATION)
