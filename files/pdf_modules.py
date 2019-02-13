# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 12:41:59 2019

@author: Anton
"""

import os
import PIL
from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
import shutil
import threading
import ctypes
import program as p
ICON_EXCLAIM=0x30
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040

def AddPathvar():
    """
    A binary containing "Poppler for Windows", a PDF rendering library.
    It will be placed in the same directory as this file.
    It will then add "\bin" within to the path variable.
    This is necessary for the module PDF2Image to work.
    source:     https://simply-python.com/tag/pdftoimage/
    """
    PathSTR = os.environ["PATH"]
    if "poppler" not in PathSTR:
        dir_ = os.path.dirname(__file__)
        print(os.listdir(dir_))
        FileName = [x for x in os.listdir(dir_) if 'poppler' in x]
        if len(FileName) != 0:
            FileName = FileName[0]
        print(FileName)
        if FileName != []:
            DirPath = os.path.join(dir_ , FileName, "bin")        
            os.environ["PATH"] += os.pathsep + DirPath



def ConvertPDF_to_JPG(self, PDFdir, tempdir, JPGdir):
    
    """Convert a PDF to JPG files.
    
    Arguments: 
        PDFdir  -- where the PDF is located
        tempdir -- where PDF is converted to a .ppm file per page, 
                         these will be converted to JPG
        JPGdir  -- where the JPG should be exported to
    
    Method:
        Use module pdf2image.
        Try functions 'convert_from_path' and 'convert_from_bytes' for conversion.
        If both methods fail user gets instructed to use online-converter instead."""
    
    MessageBox = ctypes.windll.user32.MessageBoxW     
    t_MBox = lambda a,b,c,d :threading.Thread(target=MessageBox,args=(a,b,c,d)).start()
    
    t_MBox(0, f'The PDF -> JPG conversion has started.\nIt may take a few minutes per book.', "Message", MB_ICONINFORMATION)   
    
    pdfs2send, _, _, _ = p.checkBooks(self,0)
    
    i = 1
    for _, item in enumerate(pdfs2send):
        #Get file name and dir names
        pdfname = os.path.splitext(item)[0] #exclude file extension
        tempdir_ppm = os.path.join(tempdir, pdfname)
        os.makedirs(tempdir_ppm)
        origin_dir = os.path.join(PDFdir, item)
        target_dir = os.path.join(JPGdir, pdfname)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)                
        try:
            os.listdir(target_dir)
        except:
            t_MBox(0, f'The file "{pdfname}.pdf" probably has a space in its name between the name and the ".pdf" extension.\nPlease remove this space.\nOtherwise it is a different error in os.Listdir', "Error", ICON_STOP)
        try:
            if os.listdir(target_dir) == []:    
                
                """The original module worked if you used: 'convert_from_path(origin_dir,dpi=170)'
                if you didn't use the output_folder argument. However it then needs to store all the
                pages in ram, which makes it a very expensive operation. If for example you use it on a 
                laptop which can't handle it , it will abort the operation and only save the first X pages of a book.
                
                To counteract this, if you add the argument 'output_folder' it will save all the pages as separate .ppm files
                and then converts the .ppm files to .jpg files.
                """
                #Try to convert
                convert_from_path(origin_dir, dpi=170, output_folder = tempdir_ppm)
                if os.listdir(tempdir_ppm) == []:
                    convert_from_bytes(open(origin_dir, 'rb').read(), output_folder = tempdir_ppm)         
                if os.listdir(tempdir_ppm) == []:
                    t_MBox(0, 0, f'The file "{pdfname}.pdf" could not be converted to JPG.\nPlease use an online PDF converter instead.\nThen place the JPG files in a map folder named after the book in {JPGdir}', "Error", ICON_STOP)                    
                if os.listdir(tempdir_ppm) != []:
                    t_MBox(0, f'{item} has been converted and is being saved', "Message",  MB_ICONINFORMATION)
                    i = 1
                    #Save the JPG files
                    DirList = os.listdir(tempdir_ppm)
                    for filename in DirList:
                        pagepath = os.path.join(tempdir_ppm, filename)
                        page_i = PIL.Image.open(pagepath)
                        filename = os.path.join(target_dir, pdfname)
                        nr = "0"*(4-len(f"{i}"))+f"{i}"
                        page_i.save(f'{filename}-{nr}.jpg', 'JPEG')
                        i += 1
        except:
            pass
        #delete temp directory with contents
        shutil.rmtree(tempdir_ppm, ignore_errors=True) 
    if i != 1:
        t_MBox(0, f'Finished converting all books.', "Message", MB_ICONINFORMATION)
    else:
        t_MBox(0, f'Finished, no books needed to be converted.', "Message", MB_ICONINFORMATION)
