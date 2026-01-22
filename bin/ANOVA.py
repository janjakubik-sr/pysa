# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 12:12:20 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import os
import time
import wx
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

dialog = wx.FileDialog(None, "Choose a data file for ANOVA", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected)    
    columns = np.size((data)[0,:])
    if columns > 2 and columns < 9:
        if columns == 3:
            f, p = stats.f_oneway(data[:,0],data[:,1],data[:,2])
        if columns == 4:
            f, p = stats.f_oneway(data[:,0],data[:,1],data[:,2],data[:,3])
        if columns == 5:
            f, p = stats.f_oneway(data[:,0],data[:,1],data[:,2],data[:,3], data[:,4])
        if columns == 6:
            f, p = stats.f_oneway(data[:,0],data[:,1],data[:,2],data[:,3], data[:,4], data[:,5])
        if columns == 7:
            f, p = stats.f_oneway(data[:,0],data[:,1],data[:,2],data[:,3], data[:,4], data[:,5], data[:,6])
        if columns == 8:
            f, p = stats.f_oneway(data[:,0],data[:,1],data[:,2],data[:,3], data[:,4], data[:,5], data[:,6], data[:,7])
        if columns == 9:
            f, p = stats.f_oneway(data[:,0],data[:,1],data[:,2],data[:,3], data[:,4], data[:,5], data[:,6], data[:,7], data[:,8])
        base=os.path.splitext(selected)[0]
        res=(str(base)+'_ANOVA_test.res')
        res=open(res,'w')
        res.write("\nANOVA of "+str(selected)+"\n\n")
        res.write("\nF = "+str(f)+"\n")
        res.write("p = "+str(p)+"\n")
        now = time.strftime("%d.%m.%Y %H:%M:%S")
        res.write("\n"+str(now)+"\n")
        res.close()
        res=(str(base)+'_ANOVA_test.res')
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
        log.write("Error: "+str(selected)+" has wrong number of columns.\n For more than 9 columns use R.")
        log.close()

dialog.Destroy()
