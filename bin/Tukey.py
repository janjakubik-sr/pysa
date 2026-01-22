# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 12:12:20 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""

import os
import wx
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

dialog = wx.FileDialog(None, "Choose a data file for Multiple comparisons\nData must be in two columns.\nGroups in the first.", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data=np.loadtxt(selected, delimiter=',', dtype=[('Group','|U8'),('Score', 'float')])   
    columns = np.size(data[0])
    if columns == 1:
        #Select uncertainty level
        ask = ('Select P value \n')
        dlg = wx.SingleChoiceDialog(None, ask,'P value',['0.05','0.01','0.001'],wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            Pval = float(dlg.GetStringSelection())
        dlg.Destroy()
        mc = MultiComparison(data['Score'], data['Group'])
        result = mc.tukeyhsd(alpha=Pval)
        base=os.path.splitext(selected)[0]
        res=(str(base)+'_Tukey_HSD.res')
        res=open(res,'w')
        res.write("\nMultiple comparisons of "+str(selected)+"\n\n")
        res.write(str(result))
        now = time.strftime("%d.%m.%Y %H:%M:%S")
        res.write("\n"+str(now)+"\n")
        res.close()
        res=(str(base)+'_Tukey_HSD.res')
        res=open(res,'r')
        tolog=res.read()
        log=open("temp.log",'w')
        log.write(tolog)
        log.close()
#        plt.figure()
#        plt.boxplot(data)
#        plt.show()
    else:
        msg = ('Wrong data format\nQuiting')
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log = open("temp.log","w")
        log.write("Error: "+str(selected)+" Wrong data format.")
        log.close()

dialog.Destroy()
