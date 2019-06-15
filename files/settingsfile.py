# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 19:04:27 2019

@author: aammd
"""
from pathlib import Path
from folderpaths import paths
import json
class settings(paths):
    
    def __init__(self):
        paths.__init__(self)
    
    def settings_get(self):
        try:
            with open(Path(self.dirsettings,"settings.txt"), 'r') as file:
                settings = json.load(file)
                self.debugmode          = settings['debugmode']
                self.pdfmultiplier      = settings['pdfmultiplier'] 
                self.QAline_thickness   = settings['QAline_thickness']
                self.horiline_thickness = settings['horiline_thickness']
                self.vertline_thickness = settings['vertline_thickness']
                self.QAline_color       = tuple(settings['QAline_color'])
                self.horiline_color     = tuple(settings['horiline_color']) 
                self.vertline_color     = tuple(settings['vertline_color'])
                self.QAline_bool        = settings['QAline_bool']
                self.horiline_bool      = settings['horiline_bool']
                self.vertline_bool      = settings['vertline_bool']
                self.samecolor_bool     = settings['samecolor_bool']
                self.pdfPageColsPos     = settings['pdfPageColsPos']
                self.pdfPageColsChecks  = settings['pdfPageColsChecks']
                self.LaTeXfontsize      = settings['LaTeXfontsize']
                self.bordercolors       = settings['bordercolors']
                self.drawborders        = settings['drawborders']
                self.cursor             = settings['cursor']
                self.GraphNdays         = settings['GraphNdays']
                self.Graph_bool         = settings['Graph_bool']
                self.NrCardsPreview     = settings['NrCardsPreview']
            file.close()
        except:
            # Just in case when the settings.txt has been tempered with        
            settingsfile = Path(self.dirsettings,"settings.txt")
            if settingsfile.exists():
                settingsfile.unlink()
            self.settings_create()
            self.settings_get()
            
    def settings_create(self):
        settingsfile = Path(self.dirsettings,"settings.txt")
        if not settingsfile.exists():   
            with settingsfile.open(mode='w') as file:
                file.write(json.dumps({'debugmode'     : False,
                                       'pdfmultiplier' : 1.0, 
                                       'QAline_thickness'   : 1, 
                                       'horiline_thickness' : 5,
                                       'vertline_thickness' : 5,
                                       'QAline_color'  : (0,0,0), 
                                       'horiline_color': (18,5,250),
                                       'vertline_color': (255,128,0),
                                       'QAline_bool'   : True,
                                       'horiline_bool'  : True ,
                                       'vertline_bool' : True,
                                       'samecolor_bool': False,
                                       'pdfPageColsPos': [30 , 46 , 75],
                                       'pdfPageColsChecks' : [True, True, False],
                                       'LaTeXfontsize' : 20,
                                       'bordercolors'  : [[0,0,0],[200,0,0]],
                                       'drawborders'   : True,
                                       'cursor'        : False,
                                       'GraphNdays'    : 10,
                                       'Graph_bool'    : True,
                                       'NrCardsPreview':15}))
                file.close()
                
    def settings_set(self):
        settingsfile = Path(self.dirsettings,"settings.txt")
        with settingsfile.open(mode='w') as file:
            file.write(json.dumps({'debugmode' : self.debugmode, 
                                   'pdfmultiplier': self.pdfmultiplier,
                                   'QAline_thickness' : self.QAline_thickness, 
                                   'horiline_thickness': self.horiline_thickness, 
                                   'vertline_thickness': self.vertline_thickness,
                                   'QAline_color'   : self.QAline_color, 
                                   'horiline_color' : self.horiline_color,
                                   'vertline_color' : self.vertline_color,
                                   'QAline_bool': self.QAline_bool,
                                   'horiline_bool': self.horiline_bool,
                                   'vertline_bool': self.vertline_bool,
                                   'samecolor_bool': self.samecolor_bool,
                                   'pdfPageColsPos' : self.pdfPageColsPos,
                                   'pdfPageColsChecks': self.pdfPageColsChecks,
                                   'LaTeXfontsize' : self.LaTeXfontsize,
                                   'bordercolors' : self.bordercolors,
                                   'drawborders' : self.drawborders,
                                   'cursor' : self.cursor,
                                   'GraphNdays' :self.GraphNdays,
                                   'Graph_bool': self.Graph_bool,
                                   'NrCardsPreview': self.NrCardsPreview}))
            file.close()
