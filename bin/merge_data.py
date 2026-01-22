#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:06:06 2020

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""

import glob,os
import wx
import numpy as np

i = 0
idx="idx.dat"
idx=open(idx,"w")

#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

#Input pattern
ask = ('Input file name pattern for data to be merged\n')
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
else:
    count = len(glob.glob(str(ptrn)))
    if count == 0:
        print ('No files found!\n')
    else:
        for file in sorted(glob.glob(str(ptrn))):
            base=os.path.splitext(file)[0]
            idx.write(str(i)+" "+str(base)+"\n") 
            i = i + 1
            data = np.loadtxt(file)
            x_data = data[:,0]
            y_data = data[:,1]
            if i == 1:
                xy_data = np.column_stack((x_data, y_data))
            else:
                xy_data = np.column_stack((xy_data, y_data))

idx.close()
res = "merged_data.dat"
np.savetxt(res,xy_data,fmt='%.4e')

log = open("temp.log","w")
log.write(err)
log.write('Done\n')
log.close()
