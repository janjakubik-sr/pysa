#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 14:26:33 2025

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import glob, os
import time
import wx
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from lazypredict.Supervised import LazyClassifier

#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

dialog = wx.FileDialog(None, "Choose a csv file to look fro best ML model", os.getcwd(), "","*.csv", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    df = pd.read_csv(selected)
    if df.shape[0]>6:
        msg = ('Looking for best ML model of '+str(selected)+' ?\n Please Wait.')
        dlg = wx.MessageDialog(None, msg, 'Sort', wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            base=os.path.splitext(selected)[0]
            #Read data
            df = pd.read_csv(selected)
            X = df.iloc[:, 1:-1]
            y = df.iloc[:, -1]
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            # LazyClassifier
            clf = LazyClassifier(verbose=0, ignore_warnings=False, custom_metric = None)
            ### fitting data in LazyClassifier
            models,predictions = clf.fit(X_train, X_test, y_train, y_test)
            top_models = models.sort_values("Accuracy", ascending=False).head(10)
            #Plot results
            plt.figure(figsize=(10, 6))
            top_models["Accuracy"].plot(kind="barh", color="skyblue")
            plt.xlabel("Accuracy")
            plt.title("Top 10 Models by Accuracy (LazyPredict)")
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.show()
            #Save results
            res_file=(str(base)+'_best_MLM.res')
            res=open(res_file,'w')
            res.write("\n\nTop models for "+str(selected)+"\n\n")
            res.write(str(top_models))
            now = time.strftime("%d.%m.%Y %H:%M:%S")
            res.write("\n\n"+str(now)+"\n")
            res.close()
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

