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


MB_ICONINFORMATION = 0x00000040

def clientprocedure_sendlastfiles(HOST,PORT,self):    
    N = 5
    sendtoClient_abs = [os.path.join(self.basedir,x) for x in self.sendtoClient]
    f4.SendGroupOfFiles(self,sendtoClient_abs,N,HOST,PORT)
    print("otherway finished also")
    _ = f4.SEND('reallyfinished','',HOST,PORT)
    print("Client -> Server is done")
    print("really stopped")        

def clientprocedure(HOST,PORT,self):  
    #send all filenames from Client to server
    msg = f4.GetDataList(self.basedir, self.appendDir, self.excludeDir, mode='relative', PICKLE=True)
    data_in = f4.SEND('compare',msg,HOST,PORT)
    
    for i in range(2):
        #should actually loop only twice
        if data_in != None and data_in != b'':
            datadict = json.loads(data_in.decode('utf-8'))
            if 'sendtoServer' in datadict.keys():
                print("CLIENT: received sendtoserver")
                paths_rel = datadict['data']
                
                paths_abs = [os.path.join(self.basedir,x) for x in paths_rel]
                N = 5
                f4.SendGroupOfFiles(self,paths_abs,N,HOST,PORT)
                data_in = f4.SEND('finished','',HOST,PORT)
                
            elif 'finished' in datadict.keys():
                print("CLIENT: received server is finished")
                print("Client -> Server is done")
                
                return False
            
            elif 'switch mode' in datadict.keys():
                print("CLIENT: received switchmode to SERVER")
                
                return True
    
    
    
    
def serverprocedure(HOST, PORT, self):
    RUNSERVER = True
    self.m_txtStatus.SetValue("server is now listening")
    try:
        while RUNSERVER == True:
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
                RUNCON = True
                #if connection established
                with conn:
                    #print(colored(f"connected by: {addr}",'red'))
                    while RUNCON == True:
                        # listen for data from the client:
                        data_in = f4.recv_msg(conn)                            
                        # termination
                        if not data_in:    
                            RUNCON = False                        
                        if data_in == None:
                            RUNCON = False       
                        # manipulation of data
                        if data_in != None and data_in != b'':
                            #decode data: in 
                            datadict = json.loads(data_in.decode('utf-8'))
                            data_out = json.dumps({'Error': ''}).encode('utf-8')
                            #all 'commands' are found in the keys of the dict that has been send
                            print(f"datadict = {datadict.keys()}")
                            if 'establish connection' in datadict.keys(): 
                                print("connection established")
                                data_out = json.dumps({'establish connection': True}).encode('utf-8')
                                
                            if 'compare' in datadict.keys(): 
                                print("\n"*2)
                                sendtoServer = []
                                sendtoClient = []
                                overwrite_list_rel = datadict['compare']['overwritefiles']
                                print("list to overwrite: ",colored(overwrite_list_rel,"green"))
                                append_list_rel = datadict['compare']['appendfiles']
                                print("list to append: ",colored(append_list_rel,"red"))
                                
                                append_list_abs = [os.path.join(self.basedir,x) for x in append_list_rel]
                                overwrite_list_abs = [tuple((os.path.join(self.basedir,x[0]),x[1])) for x in overwrite_list_rel]
                                overwrite_list_pathonly = [x[0] for x in overwrite_list_abs]
                                
                                        
                                #get the list of data from the Server side:
                                serverfiles_abs = f4.GetDataList(self.basedir,self.appendDir,self.excludeDir,'absolute',False)
                                
                                #check if Server Side needs to be overwritten
                                for item in overwrite_list_abs:
                                    path  = item[0]
                                    mtime_client = item[1]
                                    if os.path.exists(path):
                                        mtime_server = int(os.path.getmtime(path))
                                        if mtime_server - mtime_client > 600: #if the client is out of date by at least 10 minutes: update it
                                            sendtoClient.append(os.path.relpath(path, self.basedir))
                                        if mtime_server - mtime_client < -600: #if the server is out of date by at least 10 minutes: update it
                                            sendtoServer.append(os.path.relpath(path, self.basedir))
                                            
                                    else:
                                        sendtoServer.append(os.path.relpath(path, self.basedir))
                                #check that files that need to be overwritten exist in serverside but not client side:
                                for x in serverfiles_abs['overwritefiles']:
                                    if x not in overwrite_list_pathonly:
                                        sendtoClient.append(os.path.relpath(x, self.basedir))
                                
                                
                                #check if items that need to be appended are not present in server side:
                                for x in append_list_abs:
                                    print(f"error {x}")
                                    if x not in serverfiles_abs['appendfiles']:
                                        sendtoServer.append(os.path.relpath(x, self.basedir))
                                        
                                #check if items that need to be appended: are present in server side but not client side:
                                for x in serverfiles_abs['appendfiles']:
                                    if x not in append_list_abs:
                                        sendtoClient.append(os.path.relpath(x, self.basedir))
                                        
                                self.sendtoClient = sendtoClient
                                if len(sendtoServer) > 0:
                                    print("Client -> Server is not yet done")
                                    data_out = json.dumps({'sendtoServer':True,'data' : sendtoServer }).encode('utf-8')
                                else:
                                    #because there is nothing to do
                                    print("Client -> Server is done")
                                    data_out = json.dumps({'finished':''}).encode('utf-8')
                                    if len(sendtoClient) != 0:
                                        data_out = json.dumps({'switch mode':''}).encode('utf-8')
                                        RUNCON = False
                                        RUNSERVER = False                          
                                        BOOL = True
                                        
                                
                                
                                
                                print("\n"*3)
                                print(f"sendtoServer = {sendtoServer}")
                                print("\n"*3)
                                print(f"sendtoclient = {sendtoClient}")
                                
                                
                                #append_list_rel    = datadict['compare']['appendfiles']
                                
                            if 'sendtoServer' in datadict.keys():
                                print("\nServer received file-data from client\n")
                                data = datadict['sendtoServer']
                                filenames = data.keys()
                                print(f"{len(data.keys())} files received")
                                for filename_key in filenames:
                                    filename_abs = os.path.join(self.basedir,filename_key)
                                    os.makedirs(os.path.dirname(filename_abs),exist_ok=True)
                                    
                                    
                                    with open(filename_abs,'wb') as f:
                                        filedata = data[filename_key]
                                        filedata = f4.string2bytes(filedata)
                                        f.write(filedata)
                                        print(f"filename \t{filename_key} \t is saved")
                                        f.close()
                                    
                                data_out = json.dumps({'continue':''}).encode('utf-8')
                            if 'reallyfinished' in datadict.keys():
                                break
                            if 'finished' in datadict.keys():
                                print("client -> server has finished")
                                #check if server -> Client has also finished
                                if sendtoClient == []:
                                    RUNCON = False
                                    RUNSERVER = False
                                    self.m_txtStatus.SetValue("finished")
                                    data_out = json.dumps({'finished':''}).encode('utf-8')                                    
                                    BOOL = False
                                    
                                else:#if you need to send files to the client
                                    RUNCON = False
                                    RUNSERVER = False
                                    data_out = json.dumps({'switch mode':''}).encode('utf-8')
                                    BOOL = True
                                    
                            #send message back
                            f4.send_msg(conn, data_out)
                            if RUNSERVER == False:
                                return BOOL
        self.m_txtStatus.SetValue("Sync complete") 
    except socket.timeout:
        self.m_txtStatus.SetValue("") 
        ctypes.windll.user32.MessageBoxW(0, "Server timed out and is now shutting down.", "Warning", MB_ICONINFORMATION)   
        
def SyncDevices(self, mode, HOST):  

    self.dirlist    = os.listdir(self.basedir)
    self.appendDir  = ["pics"]   # dont overwrite files in these directories
    self.excludeDir = ["IPadresses","books","resources","temporary"] # exclude this directory from synchronizing  
    
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    # listen to port:    
    if mode == "SERVER": # first start server, then client
        
        HOST = self.IP1
        self.m_txtStatus.SetValue("starting server")
        #check if server is online:
        
        switchside = serverprocedure(HOST,PORT,self)    
        
        if switchside:
            print(colored("server is now client","red"))
            self.m_txtStatus.SetValue("finished server, now starting client")
            time.sleep(2)
            self.m_txtStatus.SetValue("starting client")
            HOST = self.IP2
            clientprocedure_sendlastfiles(HOST,PORT,self)
        else:
            self.m_txtStatus.SetValue("Sync completed")
    elif mode == "CLIENT":# first start client, then afterwards server but make sure it starts before a new client is stqarted
        HOST = self.IP2
        self.m_txtStatus.SetValue("starting client")
        switchside = clientprocedure(HOST,PORT,self)
        if switchside:
            print("client is now server")
            self.m_txtStatus.SetValue("finished client")
            time.sleep(0.1)
            self.m_txtStatus.SetValue("starting server")
            HOST = self.IP1            
            switchside = serverprocedure(HOST,PORT,self) 
        else:
            print("CLIENT: has stopped")
            self.m_txtStatus.SetValue(f"Sync completed")
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
