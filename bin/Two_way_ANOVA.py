#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:44:34 2017

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import os
import wx
import time
import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.factorplots import interaction_plot
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats

#Get data
dialog = wx.FileDialog(None, "Choose a data file for Two-way ANOVA\nData must be in columns.", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = pd.read_csv(selected)
    noc = len(data.columns)
    if noc > 2:
        var_names = list(data)
        #Select factors and variable
        dlg = wx.SingleChoiceDialog(None, 'Select column with groups.\nData type must be string','Group column',var_names,wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            groups = dlg.GetStringSelection()
        dlg.Destroy()
        dlg = wx.SingleChoiceDialog(None, 'Select dependency variable.','Dependency variable',var_names,wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dv = dlg.GetStringSelection()
        dlg.Destroy()
        dlg = wx.SingleChoiceDialog(None, 'Select response variable.\nData type must be float.','Response variable',var_names,wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            rv = dlg.GetStringSelection()
        dlg.Destroy()
        #Interaction plot
        fig1 = interaction_plot(data.eval(dv), data.eval(groups), data.eval(rv), colors=['red','blue'], markers=['D','^'], ms=10)
        plt.show(fig1)
        formula = str(rv)+' ~ C('+str(groups)+' ) + C('+str(dv)+') + C('+str(groups)+'):C(' +str(dv)+')'
        model = ols(formula, data).fit()
        aov_table = anova_lm(model, typ=2)
        base=os.path.splitext(selected)[0]
        res=(str(base)+'_Two-way_ANOVA.res')
        res=open(res,'w')
        res.write("\nTwo-way ANOVA of "+str(selected)+"\n\n")
        res.write(str(aov_table))
        now = time.strftime("%d.%m.%Y %H:%M:%S")
        res.write("\n"+str(now)+"\n")
        res.close()
        res=(str(base)+'_Two-way_ANOVA.res')
        res=open(res,'r')
        tolog=res.read()
        log=open("temp.log",'w')
        log.write(tolog)
        log.close()
        resid = model.resid 
        fig2 = sm.qqplot(resid, line='s')
        plt.show(fig2)
    else:
        msg = ('Wrong data format\nQuiting')
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log = open("temp.log","w")
        log.write("Error: "+str(selected)+" Wrong data format.")
        log.close()

dialog.Destroy()

 


