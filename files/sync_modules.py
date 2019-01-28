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
import threading
import ctypes
import json
import wx
import wx.richtext


import base64

def bytes2string(byt):
    str1 = base64.b64encode(byt)
    str2 = json.dumps(str1.decode()).replace("'",'"')[1:-1]
    return str2

def string2bytes(string):
    return base64.b64decode(string)

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        try:
            packet = sock.recv(n - len(data))
        except:
            packet = []
        if not packet:
            return None
        data += packet
    return data

def sendmessage(HOST,PORT,self):
    
    dirlist    = os.listdir(self.basedir)
    appendDir  = ["books","pics","resources"] # dont overwrite
    excludeDir = ["IPadresses"]              # exclude this directory from synchronizing
    
    # Does the user want to transfer books?
    
    dirlist = [x for x in dirlist if x != "books"]
    dirlist = [x for x in dirlist if x not in excludeDir]
    def Socket_send(HOST, PORT, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((HOST,PORT))
            send_msg(s, message)
            data = recv_msg(s)
            #print(' received' ,repr(data))
            
            return data
        
    for subdir in dirlist:
        print(f"directory is {subdir}")
        filelist = []
        mode = f"mode{1*(subdir in appendDir)}" #mode is either 0 (overwrite) or 1 (append)
        print(f"mode = {mode}")
        walkdir = os.path.join(self.basedir , subdir)
        
        #% get subdirectories
        if os.path.isdir(walkdir):    
            for root,dirs,files in os.walk(walkdir,topdown = False):
                for name in files:
                    filelist.append(os.path.join(root, name))
                for name in dirs:
                    print(os.path.join(root, name))
        elif os.path.isfile(walkdir):
            filelist.append(walkdir)
        
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
                
                                """Server sends data back indicating how the file should be transfered Client <-> Server
                                the data starts with bytes: "sendClientToServer" or "sendServerToClient" + the file"""
                            
                                if command == 'sendClientToServer':  
                                    # send data
                                    bytesfile = open(filepath_abs, 'rb').read()
                                    bytesfile = bytes2string(bytesfile)
                                    
                                    message = json.dumps({'name': filepath_rel, 'data': bytesfile , 'command' : 'sendClientToServer'}).encode('utf-8')
                                    data2 = Socket_send(HOST, PORT, message)  
                                    datadict = json.loads(data2.decode('utf-8'))
                                    command = datadict['command']
                                    if command == 'finished':
                                        TRYSEND = False
                                elif command == 'sendServerToClient':
                                    datadict = json.loads(data.decode('utf-8'))
                                    data2 = datadict['data']
                                    data2 = string2bytes(data2)
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
    
    
def listen(HOST, PORT, self):
    RUNSERVER = True
    self.m_txtStatus.SetValue("server is now listening")
    i = 0
    while RUNSERVER == True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setblocking(0)
            s.bind((HOST, PORT))
            
            print(f"is now listening")            
            s.listen()
            s.settimeout(200)
            conn, addr = s.accept()
            i += 1
            if i%18 in range(6):
                self.m_txtStatus.SetValue("server is now receiving data .")
            if i%18 in range(6,12):
                self.m_txtStatus.SetValue("server is now receiving data ..")
            if i%18 in range(12,18):
                self.m_txtStatus.SetValue("server is now receiving data ...")
            print("is now connected")
            
            RUNCON = True
            with conn:
                #print(colored(f"connected by: {addr}",'red'))
                while RUNCON == True:
                    # listen for data from the client:
                    data_in = recv_msg(conn)                            
                    # termination
                    if not data_in:    
                        RUNCON = False                        
                    if data_in == None:
                        RUNCON = False       
                                 
                    # manipulation of data
                    if data_in != None and data_in != b'':
                        datadict = json.loads(data_in.decode('utf-8'))
                        data_out = json.dumps({'Error': ''}).encode('utf-8')
                        
                        #there are only two types of dicts that are being send to the server:
                        # one has 'command' as a key in it and one doesn't.
                        # the first one only contains file name/creation time/ mode depending on which files are send
                        # 'command' then says if and in what direction files should be transferred.
                        
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
                                            bytesfile = bytes2string(bytesfile)
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
                                        data = string2bytes(data)
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
                                    
                        send_msg(conn, data_out)        
    self.m_txtStatus.SetValue("server finished") 
       
def SyncDevices(self, mode, HOST):        
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    # listen to port:    
    if mode == 0: # first start server, then client
        HOST = self.IP1
        self.m_txtStatus.SetValue("starting server")
        listen(HOST,PORT,self)    
        self.m_txtStatus.SetValue("finished server, now starting client")
        time.sleep(2)
        self.m_txtStatus.SetValue("starting client")
        HOST = self.IP2
        sendmessage(HOST,PORT,self)
    elif mode == 1:# first start client, then afterwards server but make sure it starts before a new client is stqarted
        HOST = self.IP2
        self.m_txtStatus.SetValue("starting client")
        sendmessage(HOST,PORT,self)
        self.m_txtStatus.SetValue("finished client")
        time.sleep(0.1)
        self.m_txtStatus.SetValue("starting server")
        HOST = self.IP1
        listen(HOST,PORT,self)    
    #except:
    #    ctypes.windll.user32.MessageBoxW(0, "Cannot start server: no internet connection detected", "Warning", 1)   
    self.m_txtStatus.SetValue("Synching complete!")

def initialize(self,event): 
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
                f.write(json.dumps({'IP1' : myIP,'IP2': ""})) 
                f.close()      
    except:
        
        ctypes.windll.user32.MessageBoxW(0, "Cannot start server: no internet connection detected2", "Warning", 1)
        
    with open(os.path.join(self.dirIP,'IPadresses.txt'),'r') as file:
        data = json.load(file)
        print(data)
        self.IP1 = data['IP1']
        self.IP2 = data['IP2']
    print(f"IP1 = {self.IP1}")
    print(f"IP2 = {self.IP2}")
    if self.IP1 != myIP:
        ctypes.windll.user32.MessageBoxW(0, "Your IP address has changed!\nThis device has updated the IP in the settings.\nMake sure the device connecting to your device changes the IP address accordingly!", "Warning", 1)
        with open(os.path.join(self.dirIP,'IPadresses.txt'),'w') as f:
                f.write(json.dumps({'IP1' : myIP,'IP2': self.IP2})) 
                f.close()
        self.IP1 = myIP
    self.m_txtMyIP.SetValue(self.IP1)
    self.m_txtTargetIP.SetValue(self.IP2) 
