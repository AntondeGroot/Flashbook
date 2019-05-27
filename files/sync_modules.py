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
import struct
import time
import datetime as dt
import sync_functions  as f4
import threading
import ctypes
import json
import wx
import wx.richtext
import base64

def Display(text,self):
    self.m_txtStatus.SetValue(text)
MB_ICONINFORMATION = 0x00000040

def clientprocedure_sendlastfiles(HOST,PORT,self):    
    N = 1
    sendtoClient_abs = [os.path.join(self.basedir,x) for x in self.sendtoClient]
    f4.SendGroupOfFiles(self,sendtoClient_abs,N,HOST,PORT)
    print("otherway finished also")
    message = json.dumps({'finished': 'clientprocedure_sendlastfiles'}).encode('utf-8')
    ___ = f4.Socket_send(HOST,PORT,message)
    print("Client -> Server is done")
    print("really stopped")        

def clientprocedure(HOST,PORT,self):  
    #send all filenames from Client to server
    msg = f4.GetDataList(self.basedir, self.appendDir, self.excludeDir, mode='relative', PICKLE=True)
    data_in = f4.SEND('compare',msg,HOST,PORT)
    
    if data_in != None and data_in != b'':
        datadict = json.loads(data_in.decode('utf-8'))
        if 'sendtoServer' in datadict.keys():
            print("CLIENT: received sendtoserver")
            paths_rel = datadict['data']
            paths_abs = [os.path.join(self.basedir,x) for x in paths_rel]
            N = 1
            f4.SendGroupOfFiles(self,paths_abs,N,HOST,PORT)
            data_in = f4.SEND('finished','',HOST,PORT)
            
        elif 'finished' in datadict.keys():
            print("CLIENT: received server is finished")
            print("Client -> Server is done")
            self.SWITCH_BOOL = False
        
        elif 'switch mode' in datadict.keys():
            print("CLIENT: received switchmode to SERVER")
            self.SWITCH_BOOL = True
    
    for i in range(2):
        #should actually loop only twice
        if data_in != None and data_in != b'':
            datadict = json.loads(data_in.decode('utf-8'))
            if 'sendtoServer' in datadict.keys():
                print("CLIENT: received sendtoserver")
                paths_rel = datadict['data']
                
                paths_abs = [os.path.join(self.basedir,x) for x in paths_rel]
                N = 1
                f4.SendGroupOfFiles(self,paths_abs,N,HOST,PORT)
                data_in = f4.SEND('finished','',HOST,PORT)
                
            elif 'finished' in datadict.keys():
                print("CLIENT: received server is finished")
                print("Client -> Server is done")
                
                self.SWITCH_BOOL = False
            
            elif 'switch mode' in datadict.keys():
                print("CLIENT: received switchmode to SERVER")
                self.SWITCH_BOOL = True
    
    
    
    
def serverprocedure(HOST, PORT, self):
    self.RUNSERVER = True
    self.m_txtStatus.SetValue("server is now listening")
    try:
        while self.RUNSERVER == True:
            #setup socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.setblocking(0)
                s.bind((HOST, PORT))
                print(f"is now listening")            
                s.listen()
                s.settimeout(60)
                conn, addr = s.accept()                
                
                self.m_txtStatus.SetValue("server is now receiving data ...")
                print("is now connected")
                self.RUNCON = True
                #if connection established
                with conn:
                    #print(colored(f"connected by: {addr}",'red'))
                    while self.RUNCON == True:
                        # listen for data from the client:
                        data_in = f4.recv_msg(conn)                            
                        # termination
                        if not data_in:    
                            self.RUNCON = False                        
                        if data_in == None:
                            self.RUNCON = False       
                        # manipulation of data
                        if data_in != None and data_in != b'':
                            #decode data: in 
                            datadict = json.loads(data_in.decode('utf-8'))
                            self.data_out = json.dumps({'Error': ''}).encode('utf-8')
                            #all 'commands' are found in the keys of the dict that has been send
                            print(f"datadict = {datadict.keys()}")
                            
                            ### if applicable: based on what server receives -- what the keydict is
                            #only one of the following will be applicable at a time
                            f4.establish_connection_server_client(self,datadict,'establish connection')  
                            f4.compare_server_with_client(self,datadict,'compare')
                            f4.request_files_from_client(self,datadict,'sendtoServer') 
                            f4.finish_server(self,datadict,'finished')
                            ###
                            
                            #send message back
                            f4.send_msg(conn, self.data_out)
                            if self.RUNSERVER == False:
                                return self.SWITCH_BOOL
        Display("Sync complete",self) 
    except socket.timeout:
        Display("",self) 
        ctypes.windll.user32.MessageBoxW(0, "Server timed out and is now shutting down.", "Warning", MB_ICONINFORMATION)   
        
def SyncDevices(self, mode, HOST):  

    self.dirlist    = os.listdir(self.basedir)
    self.appendDir  = ["pics"]   # dont overwrite files in these directories
    self.excludeDir = ["IPadresses","books","resources","temporary"] # exclude this directory from synchronizing  
    
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    # listen to port:    
    if mode == "SERVER": # first start server, then client
        HOST = self.IP1
        Display("starting server",self)        
        #check if server is online:
        serverprocedure(HOST,PORT,self) #returns switch_bool
        if self.SWITCH_BOOL == True: #switch Server -> Client
            print(colored("server is now client","red"))
            Display("finished server, starting client",self)
            time.sleep(2)
            Display("starting client",self)
            testthread = f4.DisplayStatus()
            testthread.set_status("HELLO WORLD!")
            testthread.start()
            HOST = self.IP2
            clientprocedure_sendlastfiles(HOST,PORT,self)
            testthread.stop()
        else:
            Display("Sync completed",self)
    elif mode == "CLIENT":# first start client, then afterwards server but make sure it starts before a new client is stqarted
        HOST = self.IP2
        #start client
        Display("starting client",self)
        
        clientprocedure(HOST,PORT,self) #DETERMINES SELF.SWITCH_BOOL
        
        if self.SWITCH_BOOL == True:
            print("client is now server")
            Display("finished client",self)
            time.sleep(0.1)
            Display("starting server",self)
            HOST = self.IP1            
            serverprocedure(HOST,PORT,self)
        else:
            print("CLIENT: has stopped")        
    Display("Sync completed",self)
    #except:
    #    ctypes.windll.user32.MessageBoxW(0, "Cannot start server: no internet connection detected", "Warning", 1)   
    #self.m_txtStatus.SetValue("Synching complete!")


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
            
            print(f"my ip is {myIP}")
            with open(os.path.join(self.dirIP,'IPadresses.txt'),'w') as f:
                f.write(json.dumps({'IP1' : myIP,'IP2': "",'client': True})) 
                f.close()      
    except:
        ctypes.windll.user32.MessageBoxW(0, "Cannot start server: no internet connection detected2", "Warning", 1)
        
    with open(os.path.join(self.dirIP,'IPadresses.txt'),'r') as file:
        data = json.load(file)
        print(data)
        self.IP1 = data['IP1']
        self.IP2 = data['IP2']
        self.client = data['client']
    print(f"IP1 = {self.IP1}")
    print(f"IP2 = {self.IP2}")
    if self.IP1 != myIP:
        ctypes.windll.user32.MessageBoxW(0, "Your IP address has changed!\nThis device has updated the IP in the settings.\nMake sure the device connecting to your device changes the IP address accordingly!", "Warning", 1)
        with open(os.path.join(self.dirIP,'IPadresses.txt'),'w') as f:
                f.write(json.dumps({'IP1' : myIP,'IP2': self.IP2, 'client':self.client})) 
                f.close()
        self.IP1 = myIP
    self.m_txtMyIP.SetValue(self.IP1)
    self.m_txtTargetIP.SetValue(self.IP2) 
    self.m_radioClient.SetValue(self.client)
    self.m_radioServer.SetValue(not self.client)
