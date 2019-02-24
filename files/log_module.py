# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 22:44:48 2019

@author: Anton
"""


import logging
import traceback
import os
from termcolor import colored

def ERRORMESSAGE(msg):
    path = os.path.join(os.getenv("LOCALAPPDATA"),'FlashBook','temporary')
    LOG_FILENAME = os.path.join(path,'logging_traceback.out')
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    logging.debug('New session has started')
    print(colored(f"{msg}\n",'red',attrs=['underline']))
    ErrorMessage = traceback.format_exc()
    logging.warning(ErrorMessage)
    logging.shutdown()
    
def DEBUGLOG(*args, debugmode = False,msg = ''):
    path = os.path.join(os.getenv("LOCALAPPDATA"),'FlashBook','temporary')
    LOG_FILENAME = os.path.join(path,'logging_traceback.out')
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    logging.debug('New session has started')
    logging.info("DEBUGLOG")
    logging.debug("error anton")
    if debugmode == True:
        print("is debugged"*10)
        
        #path = os.path.join(os.getenv("LOCALAPPDATA"),'Flashbook','temporary')
        #LOG_FILENAME = os.path.join(path,'logging_traceback.out')
        #logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)    
        logging.info(msg)
        logging.debug("test")
        for arg in args:
            print("argument"*90)
            logging.info('%s before you', arg)
    logging.shutdown()
    