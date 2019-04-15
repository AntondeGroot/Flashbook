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
    f4.SendGroupOfFiles(self,self.sendtoClient,N,HOST,PORT)
    f4.SEND('finished','',HOST,PORT)
    print("Client -> Server is done")
    print("really stopped")        

def clientprocedure(HOST,PORT,self):    
    msg = f4.GetDataList(self.basedir, self.appendDir, self.excludeDir, mode='relative', PICKLE=True)
    data_in = f4.SEND('compare',msg,HOST,PORT)
    if data_in != None and data_in != b'':
        datadict = json.loads(data_in.decode('utf-8'))
        if 'sendtoServer' in datadict.keys():
            paths_rel = datadict['data']
            
            paths_abs = [os.path.join(self.basedir,x) for x in paths_rel]
            N = 2
            f4.SendGroupOfFiles(self,paths_abs,N,HOST,PORT)
            
            
        elif 'finished' in datadict.keys():
            f4.SEND('finished','',HOST,PORT)
            print("Client -> Server is done")
            
    print("really stopped")        
    #print(f"data from compare from server: {data_in}")
    #send all the relpaths and mtimes
    
    
    """
    for subdir in dirlist:
        print(f"directory is {subdir}")
        filelist = []
        mode = f"mode{1*(subdir in appendDir)}" #mode is either 0 (overwrite) or 1 (append)
        print(f"mode = {mode}")
        walkdir = os.path.join(self.basedir , subdir)
        
        
        
        
        
        
        #%%
        i = 0
        for filepath_abs in filelist:
            i += 1
            fname = os.path.join(os.path.split(os.path.dirname(filepath_abs))[-1],os.path.basename(filepath_abs))
            if i%3==0:
                self.m_txtStatus.SetValue(f"Transferring . \t{fname}")
            if i%3==1:
                self.m_txtStatus.SetValue(f"Transferring .. \t{fname}")
            if i%3==2:
                self.m_txtStatus.SetValue(f"Transferring ... \t{fname}")
            stats = os.stat(filepath_abs)
            # last time file was modified
            creation_time = time.strftime('%y-%m-%d %H:%M:%S',time.gmtime(stats.st_mtime))
            filepath_rel = os.path.relpath(filepath_abs, self.basedir)           
            # send mode:
            # it keeps sending information that includes the name of the file, the server processes this
            # the server then sends back the name of the file. If the name matches the name of the file that was sent: we know the transfer was successful.
            #%%
            TRYSEND = True
            while TRYSEND == True:
                print("loop1")
                # send file name, mode , creation time
                message = json.dumps({'name': filepath_rel,'mode': mode, 'creation time' : creation_time}).encode('utf-8')
                data = Socket_send(HOST,PORT,message)
                #print(f"data = {data}")
                if data != None and data != []:
                    if data.decode('utf-8')!= None and data.decode('utf-8')!= '':
                        if "name" in data.decode('utf-8'):
                            #print(f"data is {data.decode('utf-8')} of type {type(data)}")
                            #data = data.decode('utf-8')
                            #print(f"data is {data} of type {type(json.loads(data.decode('utf-8')))}")
                            #print(f"{json.loads(data.decode('utf-8')).keys()}")
                            
                            if json.loads(data.decode('utf-8'))['name'] == filepath_rel:
                                datadict = json.loads(data.decode('utf-8'))
                                data_backup = data
                                TRYSEND = False
                        else:
                            TRYSEND = False
                            
            TRYSEND = True            
            while TRYSEND == True:
                print("loop2")
                try:
                    command = datadict['command']
                    #message = json.dumps({'name': filepath_rel,'data': mode,'command':command}).encode('utf-8')
                    #data = Socket_send(HOST,PORT,message)                    
                    if data != None and data != []:
                        datadict = json.loads(data.decode('utf-8'))
                        if all (k in datadict for k in ("name", "command")):
                            if datadict['name'] == filepath_rel:
                                command = json.loads(data.decode('utf-8'))['command']                            
                
                                ""Server sends data back indicating how the file should be transfered Client <-> Server
                                the data starts with bytes: "sendClientToServer" or "sendServerToClient" + the file""
                            
                                if command == 'sendClientToServer':  
                                    # send data
                                    bytesfile = open(filepath_abs, 'rb').read()
                                    bytesfile = f4.bytes2string(bytesfile)
                                    
                                    message = json.dumps({'name': filepath_rel, 'data': bytesfile , 'command' : 'sendClientToServer'}).encode('utf-8')
                                    data2 = Socket_send(HOST, PORT, message)  
                                    datadict = json.loads(data2.decode('utf-8'))
                                    command = datadict['command']
                                    if command == 'finished':
                                        TRYSEND = False
                                elif command == 'sendServerToClient':
                                    datadict = json.loads(data.decode('utf-8'))
                                    data2 = datadict['data']
                                    data2 = f4.string2bytes(data2)
                                    command = datadict['command']
                                    
                                    os.makedirs(os.path.dirname(filepath_abs), exist_ok = True)
                                    with open(filepath_abs, 'wb') as f:
                                        f.write(data2)
                                        f.close()
                                    #if command == 'finished':
                                    TRYSEND = False
                                elif command == 'finished':
                                    TRYSEND = False
                                
                except:
                    data = data_backup
                    print("connection failed")
    self.m_txtStatus.SetValue("Transfer has finished")
    #stop server:
    message = json.dumps({'command':'finished'}).encode('utf-8')
    data2 = Socket_send(HOST, PORT, message)  
    print("Transfer has finished")
    """
    
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
                s.settimeout(200)
                conn, addr = s.accept()
                #socket_nr
                
                
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
                            
                            #there are only two types of dicts that are being send to the server:
                            # one has 'command' as a key in it and one doesn't.
                            # the first one only contains file name/creation time/ mode depending on which files are send
                            # 'command' then says if and in what direction files should be transferred.
                            print(f"datadict = {datadict.keys()}")
                            if 'establish connection' in datadict.keys():
                                
                                print("connection established")
                                data_out = json.dumps({'establish connection': True}).encode('utf-8')
                                
                            if 'compare' in datadict.keys(): 
                                print("\n"*5)
                                sendtoServer = []
                                sendtoClient = []
                                overwrite_list_rel = datadict['compare']['overwritefiles']
                                print(colored(overwrite_list_rel,"green"))
                                append_list_rel = datadict['compare']['appendfiles']
                                print(colored(append_list_rel,"red"))
                                
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
                                    data_out = json.dumps({'sendtoServer':True,'data' : sendtoServer }).encode('utf-8')
                                else:
                                    print("Client -> Server is done")
                                    data_out = json.dumps({'finished':''}).encode('utf-8')
                                
                                        
                                
                                
                                
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
                            if 'finished' in datadict.keys():
                                print("client -> server has finished")
                                #check if server -> Client has also finished
                                if sendtoClient == []:
                                    RUNSERVER = False
                                    self.m_txtStatus.SetValue("finished")
                                    #self.switchServerClient = False
                                    return False
                                else:
                                    RUNSERVER = False
                                    #self.switchServerClient = True
                                    return True
                                
                            """
                            #%% Check if and how files should be transferred
                            if 'command' not in datadict.keys():# don't transfer files just yet, first determine in which direction they should be transferred
                                
                                if all (k in datadict for k in ("name","mode","creation time")):
                                    filepath_rel = datadict['name']
                                    name = os.path.join(self.basedir,filepath_rel)                                        
                                    mode = datadict['mode']
                                    
                                    if os.path.exists(name):
                                        if mode == 'mode1':
                                            print("don't overwrite")
                                            data_out = json.dumps({'name': filepath_rel, 'command' : 'finished' }).encode('utf-8')
                                        if mode == 'mode0' :
                                            stats = os.stat(name)
                                            ctime_server = time.strftime('%y-%m-%d %H:%M:%S',time.gmtime(stats.st_mtime))
                                            ctime_client = datadict['creation time']
                                            ctime_client = dt.datetime.strptime(ctime_client, '%y-%m-%d %H:%M:%S')
                                            ctime_server = dt.datetime.strptime(ctime_server, '%y-%m-%d %H:%M:%S')                                   
                                            delta_t = int((ctime_server-ctime_client).total_seconds()/60) # time in minutes
                                            
                                            # set a minimum 10 minute threshold
                                            if delta_t > 10:
                                                myfile = open(name,'rb')
                                                #  update the time this file has been last 'modified' or in this case looked at. 
                                                #  This makes sure you on both server and client the synchronized files are *really synchronized*
                                                os.utime(name, None) 
                                                
                                                bytesfile = myfile.read()
                                                bytesfile = f4.bytes2string(bytesfile)
                                                data_out = json.dumps({'name': filepath_rel,'mode': mode, 'command' : 'sendServerToClient','data':bytesfile }).encode('utf-8')
                                            elif delta_t < -10:
                                                data_out = json.dumps({'name': filepath_rel,'mode': mode, 'command' : 'sendClientToServer' }).encode('utf-8')
                                            else:
                                                data_out = json.dumps({'name': filepath_rel,'mode': mode, 'command' : 'finished' }).encode('utf-8')
                                        
                                    else: # file does not exist on server side: send it
                                        data_out = json.dumps({'name': filepath_rel,'mode': mode, 'command' : 'sendClientToServer' }).encode('utf-8')
                                    
                            #%% transfer files        
                            elif 'command' in datadict.keys(): 
                                print("accepted phase1")
                                print(datadict.keys())
                                if all (k in datadict for k in ("name","command","data")): #check if all keys are in dict
                                    print("accepted datadict")
                                    filepath_rel = datadict['name']
                                    name = os.path.join(self.basedir,filepath_rel)
                                    command = datadict['command']
                                    data = datadict['data']
                                    
                                    if command == 'sendClientToServer':
                                        os.makedirs(os.path.dirname(name), exist_ok=True)
                                        with open(name,'wb') as f:
                                            data = f4.string2bytes(data)
                                            f.write(data)
                                            print(f"filename \t{name} \t is saved")
                                            f.close()
                                        if os.path.exists(name):
                                            data_out = json.dumps({'name': filepath_rel, 'command' : 'finished'}).encode('utf-8')
                                        else: # file failed to create
                                            data_out = json.dumps({'name': 'failed', 'command' : 'failed'}).encode('utf-8')
                                elif "command" in datadict:
                                    command = datadict['command']
                                    if command == 'finished':
                                        RUNSERVER = False
                            """
                            if RUNSERVER:
                                f4.send_msg(conn, data_out)        
        self.m_txtStatus.SetValue("server finished") 
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
            print("server is now client")
            self.m_txtStatus.SetValue("finished server, now starting client")
            time.sleep(2)
            self.m_txtStatus.SetValue("starting client")
            HOST = self.IP2
            #clientprocedure_sendlastfiles(HOST,PORT,self)
        
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
