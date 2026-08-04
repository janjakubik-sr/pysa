# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 12:12:20 2016

@author: roshi
"""

import os
import time
import wx
import numpy as np
import matplotlib.pyplot as plt
import scipy

dialog = wx.FileDialog(None, "Choose a data file to calculate Spearman's correlation coefficient", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected, dtype='str')    
    columns = np.size((data)[0,:])
    rows = np.size((data)[:,0])
    base=os.path.basename(selected)
    if columns == 2 and rows > 4:
        msg = ('Calculate Spearman\'s coefficient for '+str(base)+' ?')
        dlg = wx.MessageDialog(None, msg, 'Calculate', wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            #load data
            x_data=data[:,0].astype(np.float32)
            y_data=data[:,1].astype(np.float32)
            #regression
            results=scipy.stats.spearmanr(x_data,y_data)
            rho=results[0]
            p=results[1]
            #save results
            res_file=(str(base)+'_spearmans.res')
            res=open(res_file,'w')
            res.write("\n\nSpearmans correlation statistics on "+str(base)+"\n\n")
            res.write("Rho = "+str(rho)+"\n")
            res.write("p-value = "+str(p)+"\n")
            now = time.strftime("%d.%m.%Y %H:%M:%S")
            res.write("\n\n"+str(now)+"\n")
            res.close()
            #plot
            rho_value=str("{0:.4f}".format(rho))
            p_value=str("{:.2e}".format(p))
            title=("Spearman's rho="+str(rho_value)+"\n P="+str(p_value))
            plt.title(title)
            plt.plot(x_data, y_data, "o", color='skyblue')
            plt.show()
            #log
            res=(str(base)+'_spearmans.res')
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
