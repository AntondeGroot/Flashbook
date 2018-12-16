#!/usr/bin/env python3


# sources: https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data



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



def start_server(basedirectory,ClientIP):
    wmi_obj = wmi.WMI()
    wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled = True"
    wmi_out = wmi_obj.query(wmi_sql)
    for dev in wmi_out:
        print("IPv4Address:", dev.IPAddress[0], "DefaultIPGateway:", dev.DefaultIPGateway[0])
    print("IPv4Address:\t", dev.IPAddress[0])
    
    HOST = dev.IPAddress[0]
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    
    mode = [] 
    runserver = True
    
    
    # to make sure a message has been fully send 
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
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data    
    
    
    while runserver:
        runcon = True
        data_out = b''
        
        # establish TCP connection:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            if addr == ClientIP:
                with conn:
                    print(colored(f"connected by: {addr}",'red'))
                    while runcon == True:
                        # listen for data from the client:
                        # the client will send the following data:
                        # - mode: 0 is synchronize in both directions
                        #         1 is only synchronize in one direction: for example for books
                        #         9 is to close the server
                        # - name: just the name of the file
                        # - time: creation time of the file located at the client side. 
                        # - data: the data of the file if it needs to be transferred
                        data_in = recv_msg(conn)
                        if data_in != None and b'mode' in data_in:
                            try:
                                mode = int(data_in.decode("utf-8")[4:])
                            except:
                                pass
                            
                        if data_in != None and b'time' in data_in:
                            print(f"time is \t {data_in[4:]}")
                        print(f"mode is \t {mode}" ) 
                        print(data_in)
                        
                        # termination
                        if not data_in:    
                            break
                        if data_in == None:
                            break
                        
                        
                        # manipulation of data
                        if data_in != None and data_in != b'':
                            if mode == 9: # stop server from running
                                runserver = False
                                break
                            
                            if mode == 1: #only transfer data if it doesn't exist
                                if b'name' in data_in:
                                    print("")
                                    print(colored(f"name",'green'))
                                    name = str(data_in.decode("utf-8") )[4:]
                                    name =os.path.join(dir0,name)
                                    if not os.path.exists(name):
                                        data_out = b"sendClientToServer"
                                    
                                if  b'sendClientToServer' in data_in:
                                    print(colored(f"data from client",'green'))
                                    print("data2 is ",data_in)
                                    data_in = data_in[18:]
                                    os.makedirs(os.path.dirname(name), exist_ok=True)
                                    with open(name,'wb') as f:
                                        f.write(data_in)
                                        f.close()
                                    data_out = data_in
                                    
                            if mode == 0: # overwrite data on either client side or server side.
                                
                                if b'name' in data_in:
                                    print("")
                                    print(colored(f"name",'green'))
                                    name = str(data_in.decode("utf-8") )[4:]
                                    name =os.path.join(dir0,name)
                                    print(name)
                                if b'time' in data_in:
                                    print(colored(f"time",'green'))
                                    print(f"name is {name}" )
                                    if os.path.exists(name):
                                        stats = os.stat(name)
                                        ctime_server = time.strftime('%d-%m-%y %H:%M:%S',time.gmtime(stats.st_mtime))
                                        ctime_client = data_in[4:]
                                        ctime_client = ctime_client.decode("utf-8")
                                        ctime_client = dt.datetime.strptime(ctime_client, '%d-%m-%y %H:%M:%S')
                                        ctime_server = dt.datetime.strptime(ctime_server, '%d-%m-%y %H:%M:%S')
                                                                                
                                        delta_t = int((ctime_server-ctime_client).total_seconds()/60) # time in minutes
                                        
                                        # set a minimum 10 minute threshold
                                        if delta_t > 10:
                                            myfile = open(name,'rb')
                                            bytesfile = myfile.read()
                                            
                                            data_out =  b'sendServerToClient'+bytesfile
                                        elif delta_t < -10:
                                            data_out =  b'sendClientToServer'
                                        
                                        print(f"time client = {ctime_client} \t time server = {ctime_server} \t time diff = {delta_t}")
                                    else:
                                        data_out =  b'sendClientToServer'
                                        
                                if  b'sendClientToServer' in data_in:
                                    print(colored(f"data from client",'green'))
                                    print("data2 is ",data_in)
                                    data_in = data_in[18:]
                                    os.makedirs(os.path.dirname(name), exist_ok=True)
                                    with open(name,'wb') as f:
                                        f.write(data_in)
                                        f.close()
                                    data_out = data_in
                                    
                                    
                        print(f"connection is {conn}")
                        print(f"data_in is \t {data_in}")
                        print(f"data_out is \t {data_out}")
                        send_msg(conn,data_out)
    
        print("")       
#%%
        

import ctypes
import os
import socket
import struct
import time
import wmi
# source https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data


def start_client(dirlist,dirappendlist = '',HostIP):
    
    modelist = []
    for di in dirlist:
        modelist.append(f"mode{1*(di in dirappendlist)}") #make list of 0 (overwrite) and 1 (append but don't overwrite) 
    
    if len(dirlist) == len(modelist):
        for i in range(len(dirlist)):
            directory = dirlist[i]
            mode = modelist[i]
            """ 
            # dirlist contains a list of all initial directories                               #    
            # modelist contains a list of all modes, the initial directory determines the mode #
            """
            
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
                    packet = sock.recv(n - len(data))
                    if not packet:
                        return None
                    data += packet
                return data
            #%% get subdirectories
            filelist = []
            for root,dirs,files in os.walk(directory,topdown = False):
                for name in files:
                    filelist.append(os.path.join(root,name))
                for name in dirs:
                    print(os.path.join(root,name))
            
            #%% Get IP address
            
            wmi_obj = wmi.WMI()
            wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
            wmi_out = wmi_obj.query( wmi_sql )
            
            for dev in wmi_out:
                print("IPv4Address:", dev.IPAddress[0], "DefaultIPGateway:", dev.DefaultIPGateway[0])
                
            
            #%% Start the Client
            
            HOST =  HostIP # ipaddress of host
            PORT = 65432              # port used by the server
            
            filestosend = filelist
            
            for filepath_abs in filestosend: # files that need to be overwritten
                print(filepath_abs)
                
                stats = os.stat(filepath_abs)
                creation_time = time.strftime('%d-%m-%y %H:%M:%S',time.gmtime(stats.st_mtime))
                filepath_rel = os.path.relpath(filepath_abs,dir0)
                #filename = os.path.split(filepath_rel)[1]
                print("##########\n")
                #send mode
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                    print(f"socket is {s}")
                    s.connect((HOST,PORT))
                    send_msg(s, bytes(mode,'utf-8'))
                    data = recv_msg(s)
                    print(f"mode is {data}")
                print("##########\n")
                # send file name
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                    s.connect((HOST,PORT))
                    send_msg(s, b'name'+bytes(filepath_rel,'utf-8'))
                    data = recv_msg(s)
                    print(f"data is {data}")
                
                #send creation time: server checks if it has the most up to date time
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                    s.connect((HOST,PORT))
                    send_msg(s, b'time'+bytes(creation_time,'utf-8'))
                    data = recv_msg(s)
                
                print(f"test is {data}")
                if data != None and data != []:
                    # save the file on the server side: by transferring the data 
                    if b'sendClientToServer' in data :    
                        # send data
                        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                            print("SENDING DATA TO SERVER")
                            
                            myfile = open(filepath_abs, 'rb')
                            bytesfile = myfile.read()
                            s.connect((HOST,PORT))
                            message = b'sendClientToServer'+bytesfile
                            print(f"message: {message}")
                            send_msg(s, message)
                            data  = recv_msg(s)
                    # save the file on client side
                    if b'sendServerToClient' in data:
                        data = data[18:]
                        os.makedirs(os.path.dirname(filepath_abs), exist_ok=True)
                        with open(filepath_abs,'wb') as f:
                            f.write(data)
                            f.close
                        
                        print("Data received from server")
            
            print(' received' ,repr(data))
    else:
        ctypes.windll.user32.MessageBoxW(0, "Error: mismatch of length of directory list to be transfered", "Message", 1)
    

