# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:21:37 2019

@author: Anton
"""

# sources: https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
from termcolor import colored

import wmi # Get IP address
import os  # Directory settings
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



def CheckServerStatus(HOST,PORT):
    BOOL = False
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((HOST,PORT))
            message = json.dumps({'establish connection': ''}).encode('utf-8')            
            f4.send_msg(s, message)
            data_in = f4.recv_msg(s)
        if data_in != None and data_in != b'':
            datadict = json.loads(data_in.decode('utf-8'))
            if 'establish connection' in datadict.keys():
                BOOL = True
    except:
        pass
    return BOOL
    
    

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


def Socket_send(HOST, PORT, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((HOST,PORT))
        send_msg(s, message)
        data = recv_msg(s)
        #print(' received' ,repr(data))
        return data

import os
import time
import base64
import struct
import pickle
import json



def GetDataList(basedir,appendDir,excludeDir,mode,PICKLE):
    X = os.listdir(basedir)
    TransferDir = [x for x in X if x not in excludeDir]
    dirs_to_overwrite = [os.path.join(basedir,dirx) for dirx in TransferDir if dirx not in appendDir]
    dirs_to_append    = [os.path.join(basedir,dirx) for dirx in TransferDir if dirx in appendDir]
    
    
    
    def string2bytes(string):
        return base64.b64decode(string)
    
    def to_lists(path,files,ctimes):
        ctimes.append(int(os.path.getmtime(path)))    
        path = os.path.relpath(path,basedir)
        files.append(path)
        
    fileslist_w  = []    
    for dir_ in dirs_to_overwrite:
        for root, dirs, files in os.walk(dir_, topdown=True):
            for name in files:       
                #variables
                path = os.path.join(root, name)
                relpath = os.path.relpath(path,basedir)
                mtime = int(os.path.getmtime(path))
                #store
                if mode == "relative":
                    relpath = os.path.relpath(path,basedir)
                    fileslist_w.append(tuple((relpath,mtime)))    
                elif mode == "absolute":
                    fileslist_w.append(path)    
                
    fileslist_a  = []
    for dir_ in dirs_to_append:
        for root, dirs, files in os.walk(dir_, topdown=True):
            for name in files:       
                #variables
                path = os.path.join(root, name)
                if mode == "relative":
                    relpath = os.path.relpath(path,basedir)
                    fileslist_a.append(relpath)    
                elif mode == "absolute":
                    fileslist_a.append(path)    
                #store    
                
           
    #pickle it so you an send it over Sockets
    msg = {'overwritefiles': fileslist_w, 'appendfiles': fileslist_a}
    
    return msg


def SEND(key,dict_data,HOST,PORT):
    
    # send mode:
    # it keeps sending information that includes the name of the file, the server processes this
    # the server then sends back the name of the file. If the name matches the name of the file that was sent: we know the transfer was successful.
    #%%
    TRYSEND = True
    while TRYSEND == True:
        print("loop1")
        # send file name, mode , creation time
        message = json.dumps({key: dict_data}).encode('utf-8')
        data = Socket_send(HOST,PORT,message)
        #print(f"data = {data}")
        if data != None and data != []:
            if data.decode('utf-8')!= None and data.decode('utf-8')!= '':
                TRYSEND = False
                return data

            #else:
            #    TRYSEND = False
            #    return None
def SendGroupOfFiles(self,filelist,N,HOST,PORT):
    #filelist has absolutepaths
    sublist = {}
    for i,file in enumerate(filelist):
        filepath_rel = os.path.relpath(file, self.basedir)
        
        #load data
        bytesfile = open(file, 'rb').read()
        bytesfile = f4.bytes2string(bytesfile)
        #  update the time this file has been last 'modified' or in this case looked at. 
        #  This makes sure you on both server and client the synchronized files are *really synchronized*
        os.utime(file, None) 
        #put in dict
        sublist[filepath_rel] = bytesfile
        key = 'sendtoServer'
        dict_data = sublist
        
        if len(sublist) == N:
            #send    
            print('dict =',len(sublist))
            data = SEND(key,dict_data,HOST,PORT)#send because you have N items
            sublist = {}
        elif i == len(filelist)-1:
            #send
            print("last file")
            data = SEND(key,dict_data,HOST,PORT)#send because you have last items
    #at end of sending files return instructions from Server
    return data
