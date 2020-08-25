# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 22:44:48 2019

@author: Anton
"""

from pathlib import Path
import logging
import traceback
import os
from termcolor import colored

def INITIALIZE(debugmode=False):
    try:
        if debugmode:               
            basepath = Path(os.getenv("LOCALAPPDATA"),'FlashBook','temporary')
            LOG_FILENAME = Path(basepath,'logging_traceback.out')
            logging.basicConfig(filename=str(LOG_FILENAME), level=logging.DEBUG)
            logging.debug('\n\nNEW SESSION HAS STARTED')
            logging.shutdown()
            
    except:
        pass        

def ERRORMESSAGE(msg):
    try:
        basepath = Path(os.getenv("LOCALAPPDATA"),'FlashBook','temporary')
        LOG_FILENAME = Path(basepath,'logging_traceback.out')
        logging.basicConfig(filename=str(LOG_FILENAME), level=logging.DEBUG)
        ErrorMessage = traceback.format_exc()
        # critical errors are still shown in the IDE's console
        print(colored(f"{msg}\n",'red',attrs=['underline']))
        print(ErrorMessage)
        # log the error
        logging.warning(msg)          #log message: what part of the program
        logging.warning(ErrorMessage) #log traceback explicitly
        logging.shutdown()
    except:
        pass

    
def DEBUGLOG(*args, debugmode=False, msg='', info=''):
    try:
        basepath = Path(os.getenv("LOCALAPPDATA"),'FlashBook','temporary')
        LOG_FILENAME = Path(basepath,'logging_traceback.out')
        
        #logging.basicConfig(filename=str(LOG_FILENAME), level=logging.DEBUG)
        logging.basicConfig(filename=str(LOG_FILENAME), level=logging.DEBUG)
        if debugmode:  
            if msg != '':             
                logging.debug(msg)
            if info != '':
                logging.info(info)
            for arg in args:
                logging.info('%s before you', arg)
        logging.shutdown()
    except:
        pass        
