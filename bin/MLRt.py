#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 14:27:26 2024

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import os
import time
import wx
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import scipy

#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

dialog = wx.FileDialog(None, "Choose a csv file to perform Multiple Linear Regression, First column = ids, last column = y", os.getcwd(), "","*.csv", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    df = pd.read_csv(selected)
    if df.shape[0]>6:
        msg = ('Perform MLR '+str(selected)+' ?')
        dlg = wx.MessageDialog(None, msg, 'Confirm', wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            base=os.path.splitext(selected)[0]
            #Read data
            df = pd.read_csv(selected)
            X = df.iloc[:, 1:-1]
            y = df.iloc[:, -1]
            df['predicted']='' 
            # Split the dataset into training and testing sets
            ask = ('Enter test size \n')
            dlg = wx.TextEntryDialog(None, ask,"Input","0.2")
            if dlg.ShowModal() == wx.ID_OK:
                	t_size = dlg.GetValue()
            dlg.Destroy()
            ask = ('Enter tracer seed value \nKeep same for reproducibility \n')
            dlg = wx.TextEntryDialog(None, ask,"Input","42")
            if dlg.ShowModal() == wx.ID_OK:
                	t_seed = dlg.GetValue()
            dlg.Destroy()
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=t_size, random_state=t_seed)
            # Train model
            regr = linear_model.LinearRegression()
            regr.fit(X_train, y_train)
            # Test model
            y_predict = regr.predict(X_test)
            #Correlation
            results=scipy.stats.spearmanr(y_test,y_predict)
            rho=str("{0:.4f}".format(results[0]))
            p=str("{:.2e}".format(results[1]))
            #Save results
            res_file=(str(base)+'_MLR_test_out.res')
            res=open(res_file,'w')
            res.write("\nSpearmans correlation statistics on "+str(selected)+"\n")
            res.write("Rho = "+str(rho)+"\n")
            res.write("p-value = "+str(p)+"\n")
            now = time.strftime("%d.%m.%Y %H:%M:%S")
            res.write("\n\n"+str(now)+"\n")
            res.close()
            #Plot
            title=("Rho = "+str(rho)+"\np-value = "+str(p))
            plt.plot(y_test, y_predict, "o", color='skyblue')
            plt.title(title)
            plt.xlabel("y_test")
            plt.ylabel("y_predict")
            plt.show()
            #Log
            res=open(res_file,'r')
            tolog=res.read()
            log=open("temp.log",'w')
            log.write(tolog)
            log.close()
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

