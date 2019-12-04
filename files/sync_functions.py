# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:21:37 2019

@author: Anton
"""

# sources: https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
from termcolor import colored
import os  
#%% The server
import socket
import struct
import time
import threading
import json
import base64
import log_module as log

def CheckServerStatus(HOST,PORT):
    BOOL = False
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((HOST,PORT))
            message = json.dumps({'establish connection': ''}).encode('utf-8')            
            send_msg(s, message)
            data_in = recv_msg(s)
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
        return data

def GetDataList(basedir,appendDir,excludeDir,mode,PICKLE):
    X = os.listdir(basedir)
    TransferDir = [x for x in X if x not in excludeDir]
    dirs_to_overwrite = [os.path.join(basedir,dirx) for dirx in TransferDir if dirx not in appendDir]
    dirs_to_append    = [os.path.join(basedir,dirx) for dirx in TransferDir if dirx in appendDir]
    
    
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
    
    #pickle it so you can send it over Sockets
    msg = {'overwritefiles': fileslist_w, 'appendfiles': fileslist_a} 
    return msg


def SEND(key,dict_data,HOST,PORT,_debugmode):
    
    # send mode:
    # it keeps sending information that includes the name of the file, the server processes this
    # the server then sends back the name of the file. If the name matches the name of the file that was sent: we know the transfer was successful.
    #%%
    TRYSEND = True
    i = 0
    while TRYSEND:
        # send file name, mode , creation time
        message = json.dumps({key: dict_data}).encode('utf-8')
        data = Socket_send(HOST,PORT,message)
        if data != None and data != []:
            if data.decode('utf-8')!= None and data.decode('utf-8')!= '':
                TRYSEND = False
                return data
        i += 1
        if i >= 20:
            log.DEBUGLOG(debugmode=_debugmode, msg=f'SYNC FUNC: error could not connect and send data')
            TRYSEND = False
            return None
def SendGroupOfFiles(self,filelist,N,HOST,PORT):
    #filelist has absolutepaths
    sublist = {}
    for i,file in enumerate(filelist):
        filepath_rel = os.path.relpath(file, self.basedir)
        
        #load data
        bytesfile = open(file, 'rb').read()
        bytesfile = bytes2string(bytesfile)
        #  update the time this file has been last 'modified' or in this case looked at. 
        #  This makes sure you on both server and client the synchronized files are *really synchronized*
        os.utime(file, None) 
        #put in dict
        sublist[filepath_rel] = bytesfile
        key = 'sendtoServer'
        dict_data = sublist
        
        if len(sublist) == N:
            #send    
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNC FUNC: client sends {len(sublist)} files')
            SEND(self,key,dict_data,HOST,PORT)#send because you have N items
            sublist = {}
        elif i == len(filelist)-1:
            #send
            SEND(self,key,dict_data,HOST,PORT)#send because you have last items
    log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNC FUNC: client has send last file')
    
def compare_server_with_client(self,datadict,key):
    if 'compare' in datadict.keys(): 
        RUNCON    = True
        RUNSERVER = True
        SWITCH_BOOL = True
        
        sendtoServer = []
        self.sendtoClient = []
        overwrite_list_rel = datadict['compare']['overwritefiles']
        append_list_rel = datadict['compare']['appendfiles']
        
        append_list_abs = [os.path.join(self.basedir,x) for x in append_list_rel]
        overwrite_list_abs = [tuple((os.path.join(self.basedir,x[0]),x[1])) for x in overwrite_list_rel]
        overwrite_list_pathonly = [x[0] for x in overwrite_list_abs]
               
        #get the list of data from the Server side:
        serverfiles_abs = GetDataList(self.basedir,self.appendDir,self.excludeDir,'absolute',False)        
        #check if Server Side needs to be overwritten
        for item in overwrite_list_abs:
            path  = item[0]
            mtime_client = item[1]
            if os.path.exists(path):
                mtime_server = int(os.path.getmtime(path))
                if mtime_server - mtime_client > 600: #if the client is out of date by at least 10 minutes: update it
                    self.sendtoClient.append(os.path.relpath(path, self.basedir))
                if mtime_server - mtime_client < -600: #if the server is out of date by at least 10 minutes: update it
                    sendtoServer.append(os.path.relpath(path, self.basedir))
                    
            else:
                sendtoServer.append(os.path.relpath(path, self.basedir))
        #check that files that need to be overwritten exist in serverside but not client side:
        for x in serverfiles_abs['overwritefiles']:
            if x not in overwrite_list_pathonly:
                self.sendtoClient.append(os.path.relpath(x, self.basedir))
        
        
        #check if items that need to be appended are not present in server side:
        for x in append_list_abs:
            if x not in serverfiles_abs['appendfiles']:
                sendtoServer.append(os.path.relpath(x, self.basedir))
                
        #check if items that need to be appended: are present in server side but not client side:
        for x in serverfiles_abs['appendfiles']:
            if x not in append_list_abs:
                self.sendtoClient.append(os.path.relpath(x, self.basedir))
                
        self.sendtoClient
        if len(sendtoServer) > 0: # client -> server is not yet done
            data_out = json.dumps({'sendtoServer':True,'data' : sendtoServer }).encode('utf-8')
        else:
            #because there is nothing to do
            log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNC FUNC: Client -> Server is done')
            data_out = json.dumps({'finished':''}).encode('utf-8')
            if len(self.sendtoClient) != 0:
                data_out = json.dumps({'switch mode':''}).encode('utf-8')
                RUNCON = False
                RUNSERVER = False                          
                SWITCH_BOOL = True
        self.data_out = data_out
        self.RUNCON = RUNCON
        self.RUNSERVER = RUNSERVER
        self.SWITCH_BOOL = SWITCH_BOOL

def request_files_from_client(self,datadict,key):
    if 'sendtoServer' in datadict.keys():
        
        data = datadict['sendtoServer']
        filenames = data.keys()
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNC FUNC: Server received file-data from client\n\t {len(data.keys())} files received')
        for filename_key in filenames:
            filename_abs = os.path.join(self.basedir,filename_key)
            os.makedirs(os.path.dirname(filename_abs),exist_ok=True)            
            with open(filename_abs,'wb') as f:
                filedata = data[filename_key]
                filedata = string2bytes(filedata)
                f.write(filedata)
                f.close()
            
        self.data_out = json.dumps({'continue':''}).encode('utf-8')

def establish_connection_server_client(self,datadict,key):
    if 'establish connection' in datadict.keys(): 
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNC FUNC: connection established')
        self.data_out = json.dumps({'establish connection': True}).encode('utf-8')
        
def finish_server(self,datadict,key):
    if 'reallyfinished' in datadict.keys():
        pass
    if 'finished' in datadict.keys():
        log.DEBUGLOG(debugmode=self.debugmode, msg=f'SYNC FUNC: client -> server has finished')
        if datadict['finished'] == '':
            #check if server -> Client has also finished
            if hasattr(self,'sendtoClient'): 
                if self.sendtoClient == []:
                    self.RUNCON = False
                    self.RUNSERVER = False
                    self.m_txtStatus.SetValue("finished")
                    self.data_out = json.dumps({'finished':''}).encode('utf-8')                                    
                    self.SWITCH_BOOL = False
                    
                else:#if you need to send files to the client
                    self.RUNCON = False
                    self.RUNSERVER = False
                    self.data_out = json.dumps({'switch mode':''}).encode('utf-8')
                    self.SWITCH_BOOL = True
            else:
                self.RUNCON = False
                self.RUNSERVER = False
                self.m_txtStatus.SetValue("finished")
                self.data_out = json.dumps({'finished':''}).encode('utf-8')                                    
                self.SWITCH_BOOL = False
        elif datadict['finished'] == 'clientprocedure_sendlastfiles':   
            self.RUNCON = False
            self.RUNSERVER = False
            self.m_txtStatus.SetValue("finished")
            self.data_out = json.dumps({'finished':''}).encode('utf-8')                                    
            self.SWITCH_BOOL = False


# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 11:28:31 2019

@author: Anton
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 19:23:41 2019
@author: Anton
"""

import threading
import time
#import flashbook as fb
"""
class StoppableDisplayThread(threading.Thread):
    ""Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition.""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.message = ''
        self.status  = ''
        self.delay   = 0.5
        self.nrdots  = 4
    #getters and setters
    def set_delay(self,var):
        self.delay = var
    def set_nrdots(self,var):
        self.delay = var
    def get_nrdots(self):
        return self.nrdots
    def set_msg(self,var):
        self.message = var
    def set_status(self,var):
        self.status = var
    def get_msg(self):
        return self.message  
    def get_status(self):
        return self.status
    def get_delay(self):
        return 0.5
    #to stop it
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()


def Display(text,self):
    self.m_txtStatus.SetValue(text)
class DisplayStatus(fb.MainFrame,StoppableDisplayThread):
    def __init__(self):
        super(DisplayStatus, self).__init__()
    ""To Use:
    t = DisplayStatus()
    t.set_status("some text") #after status dots will be printed
    t.start()
    ...
    t.stop()
    ""
    def run(self):
        mod = self.get_nrdots()+1
        i = 0 
        while not self.stopped():
            time.sleep(self.get_delay())
            message = self.get_status()+" "+"."*int(i%mod)+" "*int(mod-i%mod)+self.get_msg()
            Display(message,self)
            i += 1
""" 



