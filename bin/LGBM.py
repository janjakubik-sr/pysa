#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 14:27:26 2024

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import glob,os
import time
import wx
import pandas as pd
import numpy as np
import lightgbm as lgb
import matplotlib.pyplot as plt
from sklearn import linear_model
import scipy
from scipy import stats

#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

dialog = wx.FileDialog(None, "Choose a csv file to perform Multiple Linear Regression, First column = ids, last column = y", os.getcwd(), "","*.csv", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    df = pd.read_csv(selected)
    if df.shape[0]>6:
        msg = ('Perform PCA '+str(selected)+' ?')
        dlg = wx.MessageDialog(None, msg, 'Sort', wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            base=os.path.splitext(selected)[0]
            #Read data
            df = pd.read_csv(selected)
            X = df.iloc[:, 1:-1]
            y = df.iloc[:, -1]
            df['predicted']=''
            clf = lgb.LGBMClassifier()
            clf.fit(X, y)
            for i in range(0,X.shape[0]):
                to_predict = df.iloc[i,1:-2]
                predicted = clf.predict([to_predict])
                df.loc[i,'predicted'] = predicted 
            out=(str(base)+'_LGBM_out.csv')
            df.to_csv(out)
            #Correlation
            x_data=df.iloc[:, -2]
            y_data=df.iloc[:, -1]
            results=scipy.stats.spearmanr(x_data,y_data)
            rho=str("{0:.4f}".format(results[0]))
            p=str("{:.2e}".format(results[1]))
            #Save results
            res_file=(str(base)+'_LGBM_out.res')
            res=open(res_file,'w')
            res.write("\n\nSpearmans correlation statistics on "+str(selected)+"\n\n")
            res.write("Rho = "+str(rho)+"\n")
            res.write("p-value = "+str(p)+"\n")
            now = time.strftime("%d.%m.%Y %H:%M:%S")
            res.write("\n\n"+str(now)+"\n")
            res.close()
            #Plot
            x_col = df.columns[-2]
            y_col = df.columns[-1]
            title=("Rho = "+str(rho)+"\np-value = "+str(p))
            plt.scatter(df[x_col], df[y_col])
            plt.title(title)
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.show()
            #Log
            res=open(res_file,'r')
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

