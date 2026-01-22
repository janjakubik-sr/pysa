#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 14:27:26 2024

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import glob, os
import wx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
pio.renderers.default='browser'
from sklearn.preprocessing import StandardScaler
std_scaler = StandardScaler()
from sklearn.decomposition import PCA

#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

dialog = wx.FileDialog(None, "Choose a csv file to perform Principal component analysis, First column = ids, last column = y", os.getcwd(), "","*.csv", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    df = pd.read_csv(selected)
    if df.shape[0]>6:
        msg = ('Perform PCA '+str(selected)+' ?')
        dlg = wx.MessageDialog(None, msg, 'Sort', wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            base=os.path.splitext(selected)[0]
            #prepare file for writing results
            results=(str(base)+'_PCA.res')
            if os.path.isfile(results):
                os.remove(results)
            res = open(results,"w")
            res.write("PCA\n")
            #read data
            df = pd.read_csv(selected)
            X = df.iloc[:, 1:-1]
            y = df.iloc[:, -1]
            X_scaled = std_scaler.fit_transform(X)
            pca = PCA(n_components = 0.95)
            X_reduced = pca.fit_transform(X_scaled)
            #Save PCA results
            res.write('95% variance '+str(X_reduced.shape[1])+' parameters\n')
            res.write(str(pca.explained_variance_))
            res.close()
            #Plot PCA results
            labels = {
                str(i): f"PC {i+1} ({var:.1f}%)"
                for i, var in enumerate(pca.explained_variance_ratio_ * 100)
            }
            fig = px.scatter_matrix(
                X_reduced,
                labels=labels,
                dimensions=range(X_reduced.shape[1]),
                #color=(y)
            )
            fig.update_traces(diagonal_visible=False)
            fig.show()
            #Plot n_components vs. EVR
            nums = np.arange(X.shape[1])
            if X.shape[0]<X.shape[1]:
                nums = np.arange(X.shape[0])
            var_ratio = []
            for num in nums:
                pca = PCA(n_components=num)
                pca.fit(X_scaled)
                var_ratio.append(np.sum(pca.explained_variance_ratio_))
            plot_df = pd.DataFrame({'n_components':nums, 'Explained variance ratio':var_ratio})
            fig = px.line(plot_df, x='n_components', y='Explained variance ratio')
            fig.show()
            res=open(results,'r')
            tolog=res.read()
            log=open("temp.log",'w')
            log.write(tolog)
            log.close()    
            dlg.Destroy()
        else:
            log = open("temp.log","w")
            log.write("Testing of "+str(selected)+" interupted.")
            log.close()
            dlg.Destroy()
    else:
        msg = ('Wrong column count or too few datapoints.\nQuiting')
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log = open("temp.log","w")
        log.write("Error: "+str(selected)+" has wrong number of columns.")
        log.close()
        dialog.Destroy()

