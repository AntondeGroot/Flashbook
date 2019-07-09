# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:47:03 2019

@author: aammd
"""
import wx
class ProgressDialog():
    def __init__(self,max_=100,title='',msg=''):
        self.dialog = wx.ProgressDialog(title,
                                        msg,
                                        maximum=max_,
                                        parent=None,
                                        style = wx.PD_CAN_ABORT
                                        #| wx.PD_APP_MODAL
                                        | wx.PD_AUTO_HIDE
                                        #| wx.PD_ELAPSED_TIME
                                        #| wx.PD_ESTIMATED_TIME
                                        #| wx.PD_REMAINING_TIME
                                        )
    def SetRange(self,integer):
        self.dialog.SetRange(integer)
        
    def Pulse(self, msg=''):
        self.dialog.Pulse(newmsg=msg)
        
    def Update(self,index, msg):
        (keepGoing, skip) = self.dialog.Update(index, msg)
        return (keepGoing, skip)
        
    def Destroy(self):
        """ The progress dialog cannot be destroyed by dlg.Destroy() as some sources on the internet
        may suggest. Instead this will make sure it will reach it maximum value which will make sure
        it closes anyway."""
        try:
            maxrange = self.dialog.GetRange()
            self.dialog.Update(maxrange)
        except:
            pass
    
