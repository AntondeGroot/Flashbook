# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 12:09:00 2019

@author: Anton
"""

#!/usr/bin/env python3


# sources: https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
from termcolor import colored
# Get IP address
import wmi
# Directory settings
import os
#%% The server
import socket
import time
import sync_functions  as f4
import ctypes
import json
import log_module as log

def Display(text,self):
    self.m_txtStatus.SetValue(text)
MB_ICONINFORMATION = 0x00000040

def clientprocedure_sendlastfiles(HOST,PORT,self):    
    N = 1
    sendtoClient_abs = [os.path.join(self.basedir,x) for x in self.sendtoClient]
    f4.SendGroupOfFiles(self,sendtoClient_abs,N,HOST,PORT)
    message = json.dumps({'finished': 'clientprocedure_sendlastfiles'}).encode('utf-8')
    _ = f4.Socket_send(HOST,PORT,message)
    log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: sendlastfiles: Client -> Server is done')

def clientprocedure(HOST,PORT,self):  
    #send all filenames from Client to server
    msg = f4.GetDataList(self.basedir, self.appendDir, self.excludeDir, mode='relative', PICKLE=True)
    data_in = f4.SEND('compare',msg,HOST,PORT,self.debugmode)
    Display("client is receiving data ...",self)
    if data_in:
        datadict = json.loads(data_in.decode('utf-8'))
        if 'sendtoServer' in datadict.keys():
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: clientprocedure: client received sendtoserver')
            paths_rel = datadict['data']
            paths_abs = [os.path.join(self.basedir,x) for x in paths_rel]
            N = 1
            f4.SendGroupOfFiles(self,paths_abs,N,HOST,PORT)
            data_in = f4.SEND('finished','',HOST,PORT,self.debugmode)
            
        elif 'finished' in datadict.keys():
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: clientprocedure: Client -> Server is done')            
            SWITCH_BOOL = False
        
        elif 'switch mode' in datadict.keys():
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: clientprocedure: now switching from client to server')
            SWITCH_BOOL = True
        else:
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: invalid key was given to clientprocedure, keys = {datadict.keys()}')
            SWITCH_BOOL = False
            
    """
    for i in range(2):
        #should actually loop only twice
        if data_in != None and data_in != b'':
            datadict = json.loads(data_in.decode('utf-8'))
            if 'sendtoServer' in datadict.keys():
                log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: clientprocedure: CLIENT: received SendtoServer command')
                paths_rel = datadict['data']                
                paths_abs = [os.path.join(self.basedir,x) for x in paths_rel]
                N = 1
                f4.SendGroupOfFiles(self,paths_abs,N,HOST,PORT)
                data_in = f4.SEND('finished','',HOST,PORT,self.debugmode)
                
            elif 'finished' in datadict.keys():
                log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: clientprocedure: Client -> Server is done')                
                SWITCH_BOOL = False            
            elif 'switch mode' in datadict.keys():
                log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: clientprocedure: received switchmode to SERVER')
                SWITCH_BOOL = True
    """
    return SWITCH_BOOL
    
    
    
def serverprocedure(HOST, PORT, self):
    self.RUNSERVER = True
    self.m_txtStatus.SetValue("server is now listening")
    SWITCH_BOOL = False
    try:
        while self.RUNSERVER:
            #setup socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.setblocking(0)
                s.bind((HOST, PORT))
                log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: serverprocedure: server is now listening')
                s.listen()
                s.settimeout(60)
                conn, addr = s.accept()                
                
                self.m_txtStatus.SetValue("server is now receiving data ...")
                log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: serverprocedure: server is now connected and receiving data')
                self.RUNCON = True
                #if connection established
                with conn:
                    while self.RUNCON:
                        # listen for data from the client:
                        data_in = f4.recv_msg(conn)                            
                        # termination
                        if not data_in:    
                            self.RUNCON = False                        
                            return SWITCH_BOOL
                        if data_in == None:
                            self.RUNCON = False  
                            return SWITCH_BOOL
                        # manipulation of data
                        if data_in != None and data_in != b'':
                            #decode data: in 
                            datadict = json.loads(data_in.decode('utf-8'))
                            self.data_out = json.dumps({'Error': ''}).encode('utf-8')
                            #all 'commands' are found in the keys of the dict that has been send
                            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: serverprocedure: datadict = {datadict.keys()}')
                            
                            ### if applicable: based on what server receives -- what the keydict is
                            #only one of the following will be applicable at a time
                            f4.establish_connection_server_client(self,datadict,'establish connection')  
                            f4.compare_server_with_client(self,datadict,'compare')
                            f4.request_files_from_client(self,datadict,'sendtoServer') 
                            SWITCH_BOOL = f4.finish_server(self,datadict,'finished')
                            
                            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: syncdevices: SWITCH_BOOL from within serverprocedure has status {SWITCH_BOOL}')
                            ###
                            #send message back
                            f4.send_msg(conn, self.data_out)
                            if not self.RUNSERVER:
                                return SWITCH_BOOL
        Display("Sync complete",self) 
    except socket.timeout:
        Display("",self) 
        ctypes.windll.user32.MessageBoxW(0, "Server timed out and is now shutting down.", "Warning", MB_ICONINFORMATION)
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: serverprocedure: server has timed out')
        return SWITCH_BOOL
    finally:
        return SWITCH_BOOL
        
def SyncDevices(self, mode, HOST):  
    
    log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: start SyncDevices')
    self.dirlist    = os.listdir(self.basedir)
    self.appendDir  = ["pics"]   # dont overwrite files in these directories
    self.excludeDir = ["IPadresses","books","resources","temporary"] # exclude this directory from synchronizing  
    
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    # listen to port:    
    if mode == "SERVER": # first start server, then client
        HOST = self.IP1
        Display("starting server",self)        
        #check if server is online:
        SWITCH_BOOL = serverprocedure(HOST,PORT,self) #returns switch_bool
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: syncdevices: SWITCH_BOOL from Server has status {SWITCH_BOOL}')
        if SWITCH_BOOL: #switch Server -> Client
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: syncdevices: server is now client')
            Display("finished server, starting client",self)
            time.sleep(2)
            Display("starting client",self)
            Display("client is sending data",self)
            HOST = self.IP2
            clientprocedure_sendlastfiles(HOST,PORT,self)
        else:
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: syncdevices: server has stopped')
    elif mode == "CLIENT":# first start client, then afterwards server but make sure it starts before a new client is stqarted
        
        
        HOST = self.IP2
        #start client
        Display("starting client",self)
        
        SWITCH_BOOL = clientprocedure(HOST,PORT,self)
        
        if SWITCH_BOOL:
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: syncdevices: client is now server')
            Display("finished client",self)
            time.sleep(0.1)
            Display("starting server",self)
            HOST = self.IP1            
            SWITCH_BOOL = serverprocedure(HOST,PORT,self)
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: syncdevices: SWITCH_BOOL from Client has status {SWITCH_BOOL}')
        else:
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: syncdevices: client has stopped')
    Display("Sync completed",self)
    log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNCMODULE: syncdevices: sync completed')
    #except:
    #    ctypes.windll.user32.MessageBoxW(0, "Cannot start server: no internet connection detected", "Warning", 1)   
    


def initialize(self):

    self.basedir = os.path.join(os.getenv("LOCALAPPDATA") ,"FlashBook")
    self.dirIP   = os.path.join(self.basedir, "IPadresses")
    if not os.path.exists(self.dirIP):
        os.makedirs(self.dirIP)
    try:     
        wmi_obj = wmi.WMI()
        wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled = True"
        wmi_out = wmi_obj.query(wmi_sql)[0] #only 1 query
        
        myIP = wmi_out.IPAddress[0]
        
        if not os.path.exists(os.path.join(self.dirIP,'IPadresses.txt')):
            with open(os.path.join(self.dirIP,'IPadresses.txt'),'w') as f:
                f.write(json.dumps({'IP1' : myIP,'IP2': "",'client': True})) 
                f.close()      
    except:
        ctypes.windll.user32.MessageBoxW(0, "Cannot start server: no internet connection detected2", "Warning", 1)
        
    with open(os.path.join(self.dirIP,'IPadresses.txt'),'r') as file:
        data = json.load(file)
        self.IP1 = data['IP1']
        self.IP2 = data['IP2']
        
    if self.IP1 != myIP:
        ctypes.windll.user32.MessageBoxW(0, "Your IP address has changed!\nThis device has updated the IP in the settings.\nMake sure the device connecting to your device changes the IP address accordingly!", "Warning", 1)
        with open(os.path.join(self.dirIP,'IPadresses.txt'),'w') as f:
                f.write(json.dumps({'IP1' : myIP,'IP2': self.IP2})) 
                f.close()
        self.IP1 = myIP
    self.m_txtMyIP.SetValue(self.IP1)
    self.m_txtTargetIP.SetValue(self.IP2) 
