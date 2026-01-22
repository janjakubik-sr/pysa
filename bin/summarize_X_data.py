#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 13:05:45 2020

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import glob,os
import wx
import numpy as np

summary="summary.dat"
summary=open(summary,"w")
i = 0

#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

#Input pattern
ask = ('Input file name pattern for data to be summarized\n')
dlg = wx.TextEntryDialog(None, ask,"Input","CHL_???.dat")
if dlg.ShowModal() == wx.ID_OK:
    ptrn = dlg.GetValue()
dlg.Destroy()

count = len(glob.glob(str(ptrn)))
if count == 0:
    msg = ('No '+str(ptrn)+' files found!\n')
    err = msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    summary.write("No "+str(ptrn)+" files found!\n")
else:
    summary.write("Idx File X_median X_min X_max \n")
    for file in sorted(glob.glob(str(ptrn))):
        base=os.path.splitext(file)[0]
        data = np.loadtxt(file)
        x_data = data[:,0]
        x_med = np.median(x_data)
        x_min = np.amin(x_data)
        x_max = np.amax(x_data)
        summary.write(str(i)+" "+str(base)+" "+str(x_med)+" "+str(x_min)+" "+str(x_max)+"\n")
        i = i + 1
            
summary.close()

log = open("temp.log","w")
log.write(err)
log.write('Done\n')
log.close()