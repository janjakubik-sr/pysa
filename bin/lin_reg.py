# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 12:12:20 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""

import glob,os
import time
import wx
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import stats

dialog = wx.FileDialog(None, "Choose a data file to perform linear regression", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected)    
    columns = np.size((data)[0,:])
    rows = np.size((data)[:,0])
    if columns == 2 and rows > 4:
        msg = ('Perform linear regression for '+str(selected)+' ?')
        dlg = wx.MessageDialog(None, msg, 'Sort', wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            #load data
            x_data=data[:,0]
            y_data=data[:,1]
            #regression
            slope, intercept, r, p, std_err = stats.linregress(x_data,y_data)
            r_squared=r**2
            #save daa
            base=os.path.splitext(selected)[0]
            res_file=(str(base)+'_lin_reg.res')
            res=open(res_file,'w')
            res.write("\n\nLiner regression of "+str(selected)+"\n\n")
            res.write("Slope = "+str(slope)+"\n")
            res.write("Intercept = "+str(intercept)+"\n")
            res.write("R^2 = "+str(r_squared)+"\n")
            res.write("p-value = "+str(p)+"\n")
            now = time.strftime("%d.%m.%Y %H:%M:%S")
            res.write("\n\n"+str(now)+"\n")
            res.close()
            #plot
            a=str("{:.2e}".format(slope))
            b=str("{:.2e}".format(intercept))
            r_value=str("{0:.4f}".format(r_squared))
            p_value=str("{:.2e}".format(p))
            title=("y="+str(a)+"*x+"+str(b)+"\nR^2="+str(r_value)+" P="+str(p_value))
            plt.title(title)
            plt.plot(x_data, y_data, "o", color='skyblue')
            x_sorted=np.sort(x_data)
            y_calc=np.array(x_sorted)*slope+intercept
            plt.plot(x_sorted, y_calc, color='red')
            plt.show()
            #log
            res=(str(base)+'_lin_reg.res')
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
