# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 12:12:20 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""

import glob,os
import sys
import subprocess
import time
import wx
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp
from scipy.special import stdtr

dialog = wx.FileDialog(None, "One sample T-test: Choose a data file to test", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected)
    if len(data) == np.size(data):
        a_mean = np.mean(data)
        a_sd = np.std(data)
        a_n = data.size
        #get basal value
        ask = ('Enter mu value for ' +str(selected)+'\n')
        dlg = wx.TextEntryDialog(None, ask,"Input","1.0")
        if dlg.ShowModal() == wx.ID_OK:
            mu = dlg.GetValue()
        dlg.Destroy()
        mu=float(mu)
        t, p = ttest_1samp(data,mu)
        base=os.path.splitext(selected)[0]
        res=(str(base)+'_T_test_1samp.res')
        res=open(res,'w')
        res.write("\nOne sample T-test of "+str(selected)+"\n\n")
        res.write("mean = "+str(a_mean)+", SD = "+str(a_sd)+", n = "+str(a_n)+"\n")
        res.write("mu="+str(mu)+"\n")
        res.write("T = "+str(t)+"\n")
        res.write("p = "+str(p)+"\n")
        now = time.strftime("%d.%m.%Y %H:%M:%S")
        res.write("\n"+str(now)+"\n")
        res.close()
        res=(str(base)+'_T_test_1samp.res')
        res=open(res,'r')
        tolog=res.read()
        log=open("temp.log",'w')
        log.write(tolog)
        log.close()
        plt.figure()
        plt.boxplot(data)
        plt.show()
    else:
        msg = ('Wrong column count\nQuiting')
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log = open("temp.log","w")
        log.write("Error: "+str(selected)+" has wrong number of columns.")
        log.close()

dialog.Destroy()
