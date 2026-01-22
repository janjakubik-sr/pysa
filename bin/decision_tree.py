#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 16:11:04 2024

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import glob, os
import time
import wx
import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

dialog = wx.FileDialog(None, "Choose a csv file to perform Decision tree\nFirst column ids, last column 0/1", os.getcwd(), "","*.csv", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    df = pd.read_csv(selected)
    if df.shape[0]>6:
        msg = ('Calculate decision tree for '+str(selected)+' ?')
        dlg = wx.MessageDialog(None, msg, 'Sort', wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            base=os.path.splitext(selected)[0]
            features = df.columns[1:-1]
            X = df[features]
            y = df.iloc[:, -1]
            dtree = DecisionTreeClassifier()
            dtree = dtree.fit(X, y)
            tree.plot_tree(dtree, feature_names=features)
            fig_name=(str(base)+'_DT.png')
            plt.savefig(fig_name, dpi=300)
            plt.show()
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

log = open("temp.log","w")
log.write(err)
log.write('Done\n')
log.close()
