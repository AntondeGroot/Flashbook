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
            s.settimeout(1)
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

import os
import time
import base64
import struct
import pickle
import json

def GetDataList(basedir,appenDir,excludeDir):
    X = os.listdir(basedir)
    TransferDir = [x for x in X if x not in excludeDir]
    dirs_to_overwrite = [os.path.join(basedir,dirx) for dirx in TransferDir if dirx not in appendDir]
    dirs_to_append    = [os.path.join(basedir,dirx) for dirx in TransferDir if dirx not in appendDir]
    
    
    
    def string2bytes(string):
        return base64.b64decode(string)
    
    def to_lists(path,files,ctimes):
        ctimes.append(int(os.path.getmtime(path)))    
        path = os.path.relpath(path,basedir)
        files.append(path)
        
    fileslist_w  = []
    mtimes_w = []    
    for dir_ in dirs_to_overwrite:
        for root, dirs, files in os.walk(dir_, topdown=True):
            for name in files:       
                #variables
                path = os.path.join(root, name)
                relpath = os.path.relpath(path,basedir)
                #store
                mtimes_w.append(int(os.path.getmtime(path)))    
                fileslist_w.append(relpath)
                
    fileslist_a  = []
    for dir_ in dirs_to_overwrite:
        for root, dirs, files in os.walk(dir_, topdown=True):
            for name in files:       
                #variables
                path = os.path.join(root, name)
                relpath = os.path.relpath(path,basedir)
                #store    
                fileslist_a.append(relpath)    
           
    #pickle it so you can send it over Sockets
    msg = pickle.dumps([[fileslist_w,mtimes_w],fileslist_a])
    return msg

