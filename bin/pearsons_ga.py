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
import scipy


#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

dialog = wx.FileDialog(None, "Choose a data file to perform Pearson's correlation test", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected, dtype='str')    
    columns = np.size((data)[0,:])
    rows = np.size((data)[:,0])
    base=os.path.basename(selected)
    if columns == 4 and rows > 8:
        msg = ('Calculate Pearson\'s coefficient for '+str(base)+' ?')
        dlg = wx.MessageDialog(None, msg, 'Calculate', wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            #load data
            x_data=data[:,0].astype(np.float32)
            y_data=data[:,1].astype(np.float32)
            groups=data[:,2].astype(np.int16)
            annotations=data[:,3]
            #regression
            results=scipy.stats.pearsonr(x_data,y_data)
            rho=results[0]
            p=results[1]
            #save data
            res_file=(str(base)+'_pearsons.res')
            res=open(res_file,'w')
            res.write("\n\nPearsons correlation statistics on "+str(selected)+"\n\n")
            res.write("Rho = "+str(rho)+"\n")
            res.write("p-value = "+str(p)+"\n")
            now = time.strftime("%d.%m.%Y %H:%M:%S")
            res.write("\n\n"+str(now)+"\n")
            res.close()
            #plot
            rho_value=str("{0:.4f}".format(rho))
            p_value=str("{:.2e}".format(p))
            title=("Pearsons's rho="+str(rho_value)+"\n P="+str(p_value))
            plt.title(title)
            colormap = np.array(['r','g','b','c','m','y','k'])
            plt.scatter(x_data, y_data, s=100, c=colormap[groups])
            for i, annotation in enumerate(annotations):
                plt.annotate(annotation, (x_data[i], y_data[i]))
            plt.show()          
            #log
            res=(str(base)+'_pearsons.res')
            res=open(res,'r')
            tolog=res.read()
            log=open("temp.log",'w')
            log.write(tolog)
            log.close()
            dlg.Destroy()
        else:
            log = open("temp.log","w")
            log.write("Testing of "+str(selected)+" interupted.")
            log.close()        
    else:
        msg = ('Wrong column count or too few datapoints.\nQuiting')
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log = open("temp.log","w")
        log.write("Error: "+str(selected)+" has wrong number of columns.")
        log.close()

dialog.Destroy()
