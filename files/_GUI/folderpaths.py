# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 18:37:50 2019

@author: aammd
"""
from pathlib import Path
import os
class paths():
    def __init__(self):
        datadir = os.getenv("LOCALAPPDATA")
        app = Path(datadir,"Flashbook")
        self.appdir = app
        self.notesdir = Path(app,"files")
        self.picsdir  = Path(app,"pics")
        self.booksdir = Path(app,"books")
        self.tempdir  = Path(app,"temporary")
        self.bordersdir  = Path(app,"borders")
        self.resourcedir = Path(app,"resources")
        self.dirIP  = Path(app,"IPadresses")
        self.dirpdf = Path(app,"PDF folder")
        self.dirpdfbook  = Path(app,"PDF books")
        self.dirsettings = Path(app,"settings")
        self.dir_topicbook_file = Path(self.dirsettings, 'data_topicbook.json')
        self.statsdir = Path(self.dirsettings, 'data_sessions.json')
        
        dirs = [self.appdir, self.notesdir, self.picsdir, self.booksdir, self.tempdir, self.bordersdir, self.resourcedir, self.dirpdf, self.dirsettings, self.dirIP, self.dirpdfbook]
        
        for item in dirs:
            if not item.exists():
                item.mkdir()
    def notes(self):
        return self.notesdir
    def pics(self):
        return self.picsdir
