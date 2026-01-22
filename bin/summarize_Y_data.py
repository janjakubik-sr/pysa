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
    summary.write("Idx File Y_median Y_min Y_max min_index max_index \n")
    for file in sorted(glob.glob(str(ptrn))):
        base=os.path.splitext(file)[0]
        data = np.loadtxt(file)
        y_data = data[:,1]
        y_med = np.median(y_data)
        y_min = np.amin(y_data)
        y_max = np.amax(y_data)
        min_index = int(np.where((y_data == y_min))[0])
        max_index = int(np.where((y_data == y_max))[0])
        summary.write(str(i)+" "+str(base)+" "+str(y_med)+" "+str(y_min)+" "+str(y_max)+" "+str(min_index)+" "+str(max_index)+"\n")
        i = i + 1
            
summary.close()

log = open("temp.log","w")
log.write(err)
log.write('Done\n')
log.close()