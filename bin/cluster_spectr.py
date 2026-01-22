#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 10:28:07 2020

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import os
import sys
import wx
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import SpectralClustering

#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

#import data
dialog = wx.FileDialog(None, "Choose a 2D data file for clustering by K-means", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected)    
    columns = np.size((data)[0,:])
    if columns > 1:
        #guess number of clusters
        ask = ('Enter the number of clusters to be calculated\n')
        dlg = wx.TextEntryDialog(None,ask,"Input","4")
        if dlg.ShowModal() == wx.ID_OK:
            n_clusters = int(dlg.GetValue())
        dlg.Destroy()
        #find clusters
        model = SpectralClustering(n_clusters, affinity='nearest_neighbors',
                                   assign_labels='kmeans')
        labels = model.fit_predict(data)
        
        #export results
        clusters = np.column_stack((data[:,0], data[:,1], labels))
        base=os.path.splitext(selected)[0]
        results=(str(base)+'_spectrum.data')
        np.savetxt(results,clusters,fmt='%.4e')
        
        #plot results
        plt.scatter(data[:, 0], data[:, 1], c=labels, s=50, cmap='viridis')
        plt.show()
        
        #Plot with Grace
        # Works also when GraceGTK is not installed in /usr/local
        
        x_min = np.amin(data[:,0])*0.9
        x_max = np.amax(data[:,0])*1.1
        y_min = np.amin(data[:,1])*0.9
        y_max = np.amax(data[:,1])*1.1
        agr_out = (str(base)+"_cluster_spectr.draw")

        #prepare file for Grace plot
        if os.path.isfile(agr_out):
            os.remove(agr_out)
        draw = open(agr_out,"w")

        draw.write("page size 595, 842 \n")
        draw.write("view xmin 0.2 \n")
        draw.write("view xmax 0.8 \n")
        draw.write("view ymin 0.85 \n")
        draw.write("view ymax 1.25 \n")
        draw.write("world xmin "+str(x_min)+" \n")
        draw.write("world xmax "+str(x_max)+" \n")
        draw.write("world ymin "+str(y_min)+" \n")
        draw.write("world ymax "+str(y_max)+" \n")

        draw.write(" G0  type xy \n")
        draw.write("  xaxis  label font \"Helvetica\" \n")
        draw.write("  xaxis  label char size 1.0 \n")
        draw.write("  xaxis  ticklabel font \"Helvetica\" \n")
        draw.write("  xaxis  ticklabel char size 1.0 \n")
        draw.write("  yaxis  label font \"Helvetica\" \n")
        draw.write("  yaxis  label char size 1.0 \n")
        draw.write("  yaxis  ticklabel font \"Helvetica\" \n")
        draw.write("  yaxis  ticklabel char size 1.0 \n")
        draw.write("  title  \"Spectrum clustering\" \n")
        draw.write("  title  font \"Helvetica\" \n")
        draw.write("  title  size 1.0 \n")
        draw.write("  subtitle  \"number of clusters ="+str(n_clusters)+" \"\n")
        draw.write("  subtitle  font \"Helvetica\" \n")
        draw.write("  subtitle  size 1.0 \n")
        
        draw.write("read xycolor \""+str(results)+"\" \n")
        draw.write("    S0 type xycolor \n")
        draw.write("    S0 symbol 1 \n")
        draw.write("    S0 symbol fill pattern 1 \n")
        draw.write("    S0 symbol size 0.600000 \n")
        draw.write("    S0 line type 0 \n")
        draw.write("    S0 line color 1 \n")
        draw.write("    S0 legend off \n")
        
        tolog=(str(selected)+' was divided to '+str(n_clusters)+' clusters by K-means')
        log=open("temp.log",'w')
        log.write(tolog)
        log.close()
        
    else:
        msg = ('Wrong column count\nQuiting')
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        err = msg
dialog.Destroy()

log = open("temp.log","w")
log.write(err)
log.write('Done\n')
log.close()
