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
from scipy.stats import ttest_rel
from scipy.special import stdtr

dialog = wx.FileDialog(None, "Paired T-test: Choose a data file to test", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected)    
    columns = np.size((data)[0,:])
    rows = np.size((data)[:,0])
    if columns == 2:
        a_data = data[:,0]
        b_data = data[:,1]
        a_mean = a_data.mean()
        b_mean = b_data.mean()
        a_sd = np.std(a_data)
        b_sd = np.std(b_data)
        a_n = a_data.size
        b_n = b_data.size
        t, p = ttest_rel(a_data, b_data)
        base=os.path.splitext(selected)[0]
        res=(str(base)+'_T_test_paired.res')
        res=open(res,'w')
        res.write("\nPaired T-test of "+str(selected)+"\n\n")
        res.write("mean = "+str(a_mean)+", SD = "+str(a_sd)+", n = "+str(a_n)+"\n")
        res.write("mean = "+str(b_mean)+", SD = "+str(b_sd)+", n = "+str(b_n)+"\n")
        res.write("\nT = "+str(t)+"\n")
        res.write("p = "+str(p)+"\n")
        now = time.strftime("%d.%m.%Y %H:%M:%S")
        res.write("\n"+str(now)+"\n")
        res.close()
        res=(str(base)+'_T_test_paired.res')
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
