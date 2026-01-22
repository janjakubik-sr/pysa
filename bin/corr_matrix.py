"""
Plotting a diagonal correlation matrix
======================================
"""
import os
import wx
from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(context="paper", font="monospace")

# Get data
dialog = wx.FileDialog(None, "Correlation matrix heat-plot: Choose a data file to test", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected)
    nc = np.size((data)[0,:])
    rows = np.size((data)[:,0])
    if nc > 4:
        d = pd.DataFrame(data, columns=list(ascii_letters[:nc]))
        # Compute the correlation matrix
        corr = d.corr()
        # Generate a mask for the upper triangle
        # mask = np.zeros_like(corr, dtype=np.bool)
        # mask[np.triu_indices_from(mask)] = True
        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(11, 9))
        # Generate a custom diverging colormap
        #cmap = sns.diverging_palette(220, 10, as_cmap=True)
        # Draw the heatmap with the mask and correct aspect ratio
        sns.heatmap(corr, vmax=1.0, square=True, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
        #Show plot
        plt.show()
        log = open("temp.log","w")
        log.write("Correlation matrix heat plot for "+str(selected)+" has has been genarated.")
        log.close()
    else:
        msg = ('Wrong column count\nQuiting')
        dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log = open("temp.log","w")
        log.write("Error: "+str(selected)+" has wrong number of columns.")
        log.close()

dialog.Destroy()
