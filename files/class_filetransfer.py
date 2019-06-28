# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:11:31 2019

@author: Anton
"""
import gui_flashbook as gui
import threading
import wx
import PIL
import program as p
import fc_functions    as f2
import sync_functions  as f4
import fc_modules as m2
import sync_modules  as m4
from pathlib import Path
from latexoperations import Commands as cmd
import log_module    as log
ICON_EXCLAIM=0x30
import accelerators_module as m7
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
                f.write(json.dumps({'IP1' : myIP,'IP2': "",'client':True})) 
                f.close()
    except:
        log.ERRORMESSAGE("Error: could not access internet")


class transfer(gui.MyFrame):
    def __init__(self):
        initialize(self)
        pass
        
    
    def m_OpenTransferOnButtonClick(self,event):
        """START MAIN PROGRAM : WIFI SYNC"""
        p.SwitchPanel(self,5)
        p.get_IP(self,event)
        m4.initialize(self)
    
    def m_txtMyIPOnKeyUp( self, event ):
        self.IP1 = self.m_txtMyIP.GetValue()
        with open(Path(self.dirIP,'IPadresses.txt'),'w') as f:
            f.write(json.dumps({'IP1' : self.IP1,'IP2': self.IP2,'client': self.client})) 
            f.close()        
    def m_txtTargetIPOnKeyUp( self, event ):
        self.IP2 = self.m_txtTargetIP.GetValue()
        with open(Path(self.dirIP,'IPadresses.txt'),'w') as f:
            f.write(json.dumps({'IP1' : self.IP1,'IP2': self.IP2,'client': self.client})) 
            f.close()
    def m_radioServerOnRadioButton( self, event ):
        self.client = not self.m_radioServer.GetValue()
        with open(Path(self.dirIP,'IPadresses.txt'),'w') as f:
            f.write(json.dumps({'IP1' : self.IP1,'IP2': self.IP2,'client': self.client})) 
            f.close()
    def m_radioClientOnRadioButton( self, event ):
        self.client = self.m_radioClient.GetValue()
        with open(Path(self.dirIP,'IPadresses.txt'),'w') as f:
            f.write(json.dumps({'IP1' : self.IP1,'IP2': self.IP2,'client': self.client})) 
            f.close()
    def m_buttonTransferOnButtonClick(self,event):
        Client = self.m_radioClient.GetValue()
        if Client:
            HOST = self.IP2
            print(f"HOST IS {HOST}")
            print("start client")
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROWWAIT))
            SERVERONLINE = f4.CheckServerStatus(HOST,65432)
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
            print(f"server is online: {SERVERONLINE}")
            if SERVERONLINE:
                self.m_txtStatus.SetValue("starting client")
                t_sync = lambda self,mode,HOST :threading.Thread(target=m4.SyncDevices,args=(self,mode,HOST)).start()
                t_sync(self,"CLIENT",HOST)        
            else:
                ctypes.windll.user32.MessageBoxW(0, "Server is not online. \nMake sure you start the server before you start the client.\nTry to connect again.", "Warning", ICON_STOP)               
        else:
            HOST = self.IP1
            print(f"HOST IS {HOST}")
            print("start server")
            self.m_txtStatus.SetValue("starting server")
            t_sync = lambda self,mode,HOST :threading.Thread(target=m4.SyncDevices,args=(self,mode,HOST)).start()
            t_sync(self,"SERVER",HOST)