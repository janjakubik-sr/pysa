#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 09:55:29 2018

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import os
import time
import wx
import numpy as np
import scipy

#temp log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
log = open("temp.log","w")

def residual_anal(y_obs, y_pred):
    """
        - Residual analysis
    """
    y_obs = np.asarray(y_obs)
    y_pred = np.asarray(y_pred)
    
    if len(y_obs) != len(y_pred):
        raise ValueError("y_obs and y_pred must have same length")
    
    n = len(y_obs)
    
    # Calculate residuals
    residuals = y_obs - y_pred
    """
    Shapiro-Wilk test for normality of residuals.
    (Simple approximation; use scipy.stats.shapiro for full version)
    """
    _, p_val = scipy.stats.shapiro(residuals)
 
    return residuals, p_val, n


#select files
dialog = wx.FileDialog(None, "Choose the data file\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_0=dialog.GetPath()
    data = np.loadtxt(selected_0)    
else:
    msg = ("Fitting was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: Fitting was canceled")
    tolog = log.read()
    None.__log(tolog)

dialog = wx.FileDialog(None, "Choose the model fit file\n", os.getcwd(), "","*.data", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_1=dialog.GetPath()
    fit_simple = np.loadtxt(selected_1)    
else:
    msg = ("Fitting was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: Fitting was canceled")
    tolog = log.read()
    None.__log(tolog)
    

    

# Run residual test analysis for a single fit  
data = np.loadtxt(selected_0)
fit = np.loadtxt(selected_1)
y_data  = data[:,1]
y_fit = fit[:,1]
residuals, p_val, n = residual_anal(y_data, y_fit)

base=os.path.splitext(selected_1)[0]
out=(str(base)+'_residuals.res')
res=open(out,'w')
res.write("\n--- Residual analysis ---\n")
res.write("  n = "+str(n)+"\n")
res.write("  Mean (should be ~0):  "+str("{:8.2e}".format(np.mean(residuals)))+"\n")
res.write("  Std Dev:              "+str("{:8.2e}".format(np.std(residuals)))+"\n")
res.write("  Min / Max:            "+str("{:8.2e}".format(np.min(residuals)))+" / "+str("{:8.2e}".format(np.max(residuals)))+"\n")
res.write("  Shapiro-Wilk p-value: "+str("{:8.4f}".format(p_val))+"\n")
res.write("\n")
now = time.strftime("%d.%m.%Y %H:%M:%S")
res.write("\n\n"+str(now)+"\n")
res.close()

res=open(out,'r')
tolog=res.read()
log.write(tolog)
log.close()