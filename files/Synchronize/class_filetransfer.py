# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:11:31 2019

@author: Anton
"""
import _GUI.gui_flashbook as gui
import threading
import wx
import program as p
import Synchronize.sync_functions  as f4
import Synchronize.sync_modules  as m4
from pathlib import Path
import _logging.log_module    as log
ICON_EXCLAIM=0x30
import json
import ctypes
import wmi
ICON_STOP = 0x10
MB_ICONINFORMATION = 0x00000040
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YESNO = 0x00000004
MB_DEFBUTTON2 = 0x00000100

def initialize(self):
    try:
        if not Path(self.dirIP,'IPadresses.txt').exists():          
            wmi_obj = wmi.WMI()
            wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled = True"
            wmi_out = wmi_obj.query(wmi_sql)[0] #only 1 query           
            myIP = wmi_out.IPAddress[0]          
           
            with open(Path(self.dirIP,'IPadresses.txt'),'w') as f:
                f.write(json.dumps({'IP1' : myIP,'IP2': ""})) 
                f.close()
    except:
        log.ERRORMESSAGE("CLASS FILETRANSFER: Error: could not access internet")


class filetransfer(gui.MyFrame):
    def __init__(self):
        pass
    
    def m_OpenTransferOnButtonClick(self,event):
        initialize(self)
        """START MAIN PROGRAM : WIFI SYNC"""     
        p.SwitchPanel(self,5)
        p.get_IP(self,event)
        m4.initialize(self)
    
    def m_txtMyIPOnKeyUp( self, event ):
        self.IP1 = self.m_txtMyIP.GetValue()
        with open(Path(self.dirIP,'IPadresses.txt'),'w') as f:
            f.write(json.dumps({'IP1' : self.IP1,'IP2': self.IP2})) 
            f.close()        
    def m_txtTargetIPOnKeyUp( self, event ):
        self.IP2 = self.m_txtTargetIP.GetValue()
        with open(Path(self.dirIP,'IPadresses.txt'),'w') as f:
            f.write(json.dumps({'IP1' : self.IP1,'IP2': self.IP2})) 
            f.close()
    
    def m_buttonTransferOnButtonClick(self,event):
        
        """First try to run the Client, if the server is online it proceeds normally. 
        When no server is detected it will assume the role of server.
        This way the user does not have to choose which side is client/server."""
        
        log.DEBUGLOG(debugmode=self.debugmode,msg=f'CLASS FILETRANSFER: starting synchronisation')
        HOST = self.IP2
        self.PORT = 65432 # Port to listen on (non-privileged ports are > 1023)
        SERVERONLINE = f4.CheckServerStatus(HOST,self.PORT,self)
        log.DEBUGLOG(debugmode=self.debugmode,msg=f'CLASS FILETRANSFER: \n\t server is online: {SERVERONLINE}')
        if SERVERONLINE:
            self.m_txtStatus.SetValue("starting client")
            log.DEBUGLOG(debugmode=self.debugmode,msg=f'CLASS FILETRANSFER: \n\t Starting Client')
            t_sync = lambda self, :threading.Thread(target=m4.Thread_Client,args=(self,)).start()
            t_sync(self)        
        else:
            
            self.m_txtStatus.SetValue("starting server")
            log.DEBUGLOG(debugmode=self.debugmode,msg=f'CLASS FILETRANSFER: \n\t Starting Server')
            t_sync = lambda self, :threading.Thread(target=m4.Thread_Server,args=(self,)).start()
            t_sync(self)
