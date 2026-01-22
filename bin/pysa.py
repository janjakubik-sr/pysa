# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 16:01:00 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
#!/usrenv python
import wx
import os
import sys
import subprocess
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, ttest_ind_from_stats
from scipy.special import stdtr
from uncertainties import ufloat
from uncertainties.umath import *

import preferences as pref
install_dir = (pref.install_dir)
sys.path.append(install_dir)
doc_dir = (pref.doc_dir)
sys.path.append(doc_dir)
example_dir = (pref.example_dir)
sys.path.append(example_dir)
width = (pref.width)
height = (pref.height)

#temp file
if os.path.isfile("nc.tmp"):
    os.remove("nc.tmp")

def exec_full(filepath):
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
    }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)


welcome = "\n******************************************\nHello, welcome to PySA\nPythonic Statistical Analysis\nby Jan Jakubik jan.jakubik@fgu.cas.cz\nCreative Commons Licence BY-NC\n*****************************************\n"

stamp = time.strftime("%Y%m%d%H%M%S")
class MainWindow(wx.Frame):
    def __init__(self, filename=(stamp+'.log')):
        super(MainWindow, self).__init__(None, size=(width,height))
        self.filename = filename
        self.dirname = '.'
        self.CreateInteriorWindowComponents()
        self.CreateExteriorWindowComponents()

    def CreateInteriorWindowComponents(self):
        self.logger = wx.TextCtrl(self, value=welcome, style=wx.TE_MULTILINE|wx.TE_READONLY)
        
    def CreateExteriorWindowComponents(self):
        self.CreateMenu()
        self.CreateStatusBar()
        self.SetTitle()

    def CreateMenu(self):
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_SAVE, '&Save log', 'Save the current log file', self.OnSave),
             (wx.ID_OPEN, '&Working Directory', 'Change working directory', self.OnCWD),
             (wx.ID_PREFERENCES, 'Preferences', 'Define default aplications, etc.', self.OnPrefs),
             (wx.ID_EXIT, 'E&xit', 'Terminate the program', self.OnExit)
            ]:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

        dataMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Edit in text editor', 'Edit data', self.OnEdit),
            (wx.ID_ANY, 'Error propagation', 'Error propagation', self.OnEPC), 
            (wx.ID_ANY, 'Sort data by X', 'Sort data by value of x', self.OnSortX),
            (wx.ID_ANY, 'Sort data by Y', 'Sort data by value of y', self.OnSortY),
            (wx.ID_ANY, 'Swap X and Y', 'Swap axes', self.OnTransformSwap),
            (wx.ID_ANY, 'Transform X', 'Transform X', self.OnTransformX),
            (wx.ID_ANY, 'Transform Y', 'Transform Y', self.OnTransformY),
            (wx.ID_ANY, 'Transform dX', 'Transform dX', self.OnTransformDX),
            (wx.ID_ANY, 'Transform dY', 'Transform dY', self.OnTransformDY)
	       ]:
            if id == None:
                dataMenu.AppendSeparator()
            else:
                item = dataMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

        

        resMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Plot results with Grace', 'Plot results with grace', self.OnTaskPlot),
             (wx.ID_ANY, 'View Grace graph', 'Open graph in grace', self.OnShowGraph),
             (wx.ID_ANY, 'View results plot', 'View results file in viewer', self.OnShowPlot),
             (wx.ID_ANY, 'View results table', 'View results file in viewer', self.OnShowRes),
             (wx.ID_ANY, 'XYCSym', 'Heat plot as XYCSym', self.OnTaskColorbat),
	      ]:
            if id == None:
                resMenu.AppendSeparator()
            else:
                item = resMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        
        sampleMenu = wx.Menu()
        oneMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Data distribution test', 'Skewnwss Kurtosis test', self.OnDataDist),
             (wx.ID_ANY, 'Shapiro-Wilk normality test', 'Shapiro-Wilk normality test', self.OnNTest),
             (wx.ID_ANY, 'Single sample T-test', 'Single sample T-test', self.OnTTest1S),
	      ]:
            if id == None:
                oneMenu.AppendSeparator()
            else:
                item = oneMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        sampleMenu.AppendSubMenu(oneMenu,"One sample test")

        twoMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Mean, SD, n', 'Mean, SD, n', self.OnTestSD),
             (wx.ID_ANY, 'Mean, SEM, n', 'Mean, SEM, n', self.OnTestSEM),
             (wx.ID_ANY, 'Paired T-test', 'Paired T-test', self.OnPTTest),
             (wx.ID_ANY, 'Welch\'s T-test', 'Welch\'s T-test', self.OnTTest),
	      ]:
            if id == None:
                twoMenu.AppendSeparator()
            else:
                item = twoMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        sampleMenu.AppendSubMenu(twoMenu,"Two samples test")

        multiMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'ANOVA one-way', 'ANOVA one-way', self.OnANOVA),
             (wx.ID_ANY, 'Analyse X-values', 'Analysis of X-values', self.OnSumX),
             (wx.ID_ANY, 'Analyse Y-values', 'Analysis of Y-values', self.OnSumY),
             (wx.ID_ANY, 'Merge 2D arrays to matrix', 'Data merging', self.OnMerge),
             (wx.ID_ANY, 'Tukey HSD', 'Multiple comparison of means', self.OnTukey),
             (wx.ID_ANY, 'Two-way ANOVA', 'Two-way ANOVA', self.OnTWA),
	      ]:
            if id == None:
                multiMenu.AppendSeparator()
            else:
                item = multiMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        sampleMenu.AppendSubMenu(multiMenu,"Multiple comparisons")

        modelMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'F-test', 'F-test nested models', self.OnFtest),
             (wx.ID_ANY, 'AICc', 'Akaike\'s Information Criterion corrected', self.OnAICc),
             (wx.ID_ANY, 'Residual analysis', 'Residual analysis', self.OnResA),
	      ]:
            if id == None:
                modelMenu.AppendSeparator()
            else:
                item = modelMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        
        correlMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Linear regression', 'Linear regression', self.OnLinReg),
             (wx.ID_ANY, 'Person\'s correlation', 'Pearson\'s correlation', self.OnPCor),
             (wx.ID_ANY, 'Person\'s correlation, data annotations', 'Pearson\'s correlation', self.OnPACor),
             (wx.ID_ANY, 'Person\'s correlation, groups and data annotations', 'Pearson\'s correlation', self.OnPGACor),
             (wx.ID_ANY, 'Spearman\'s correlation', 'Spearman\'s correlation', self.OnSCor),
             (wx.ID_ANY, 'Spearman\'s correlation, data annotations', 'Spearman\'s correlation', self.OnSACor),
             (wx.ID_ANY, 'Spearman\'s correlation, groups and data annotations', 'Spearman\'s correlation', self.OnSGACor),
             (wx.ID_ANY, 'Correlation Matrix Heat-Plot', 'Correlation Matrix', self.OnCorM),
	      ]:
            if id == None:
                correlMenu.AppendSeparator()
            else:
                item = correlMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
                
        clusterMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Clustering by K-means', 'Clustering by K-means', self.OnKmeans),
             (wx.ID_ANY, 'Spectral Clustering', 'Spectral Clustering', self.OnSpectralC),
             (wx.ID_ANY, 'HDBSCAN', 'HDBSCAN', self.OnHDBSCAN),
	      ]:
            if id == None:
                clusterMenu.AppendSeparator()
            else:
                item = clusterMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

        MLMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Decision Tree', 'Decision Tree', self.OnDT),
             (wx.ID_ANY, 'LGBM Classifier', 'Large Gradient Boosting Machine Classifier', self.OnLGBM),
             (wx.ID_ANY, 'LGBM test', 'LGBM test', self.OnLGBMtest),
             (wx.ID_ANY, 'MLM selection', 'Lazy Classifier MLM selection', self.OnMLMSel),
             (wx.ID_ANY, 'Multiple Linear Regression', 'Multiple Linear Regerssion', self.OnMLRM),
             (wx.ID_ANY, 'PCA', 'Principal component analysis', self.OnPCA),
             (wx.ID_ANY, 'PCA colored by y-value', 'PCA colored by y-value', self.OnPCAc),
             (wx.ID_ANY, 'PCA with subsets', 'PCA with subsets', self.OnPCAs),
	      ]:
            if id == None:
                MLMenu.AppendSeparator()
            else:
                item = MLMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
    

        appMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'IPython', 'Open IPython console', self.OnTaskIP),
            (wx.ID_ANY, 'Plotting (Grace)', 'Open Grace', self.OnTaskGG),
            (wx.ID_ANY, 'Statistics (R)', 'Open R console', self.OnTaskR),
            (wx.ID_ANY, 'Spreadsheet (pyspread)', 'Open shell console', self.OnTaskSpread),
            (wx.ID_ANY, 'Terminal (Shell)', 'Open shell console', self.OnTaskSh),
	      ]:
            if id == None:
                appMenu.AppendSeparator()
            else:
                item = appMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

        helpMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_HELP, '&Help', 'Help', self.OnHelp),
             (wx.ID_HELP_INDEX, 'Examples', 'Examples', self.OnExample),
             (wx.ID_ABOUT, '&About', 'Information about this program', self.OnAbout),]:
            if id == None:
                helpMenu.AppendSeparator()
            else:
                item = helpMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
                
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, 'File')
        menuBar.Append(dataMenu, 'Data Transformation')
        menuBar.Append(resMenu, 'Results')
        menuBar.Append(sampleMenu,"Compare samples")
        menuBar.Append(modelMenu,"Compare models")
        menuBar.Append(correlMenu,"Correlations")
        menuBar.Append(clusterMenu,"Clustering")
        menuBar.Append(MLMenu, 'Machine Learning')
        menuBar.Append(appMenu, 'Auxilary Apps')
        menuBar.Append(helpMenu, 'Help')
        self.SetMenuBar(menuBar)

    def SetTitle(self):
        # MainWindow.SetTitle overrides wx.Frame.SetTitle, so we have to
        # call it using super:
        super(MainWindow, self).SetTitle('PySA')

    # Helper method(s):

    def __log(self, message):
        ''' Private method to append a string to the logger text
            control. '''
        self.logger.AppendText('%s\n'%message)

    # Event handlers:
    def OnAbout(self, event):
        dialog = wx.MessageDialog(self, 'Pythonic Statistical Analysis by Jan Jakubik. Non-commercial use allowed under Creative commons licence (BY-NC).', 'About This App', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def OnCWD(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
                           | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            new_dir = dlg.GetPath()
            self.__log('Current dir is '+str(new_dir))
            os.chdir(new_dir)
            if os.path.isfile("nc.tmp"):
                os.remove("nc.tmp")
            dlg.Destroy()

    def OnPrefs(self, event):
        cmd = ('python '+str(install_dir)+'prefs.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        
    def OnHelp(self, event):
        cmd = ('python '+str(install_dir)+'help.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnExample(self, event):
        dlg = wx.DirDialog(self, "Choose a directory with examples:",
                           defaultPath=example_dir,
                           style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
                           | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            new_dir = dlg.GetPath()
            self.__log('Current dir is '+str(new_dir))
            os.chdir(new_dir)
            dlg.Destroy()

    def OnExit(self, event):
        self.Close()  # Close the main window.

    def OnSave(self, event):
        textfile = open(os.path.join(self.dirname, self.filename), 'w')
        textfile.write(self.logger.GetValue())
        textfile.close()

    def OnEdit(self, event):
        cmd = ('python '+str(install_dir)+'editor.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnSortX(self, event):
        self.__log('Sorting by X values')
        exec_full(str(install_dir)+'sort_by_x.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnSortY(self, event):
        self.__log('Sorting by Y values')
        exec_full(str(install_dir)+'sort_by_y.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransformSwap(self, event):
        self.__log('Swapping X and Y axes ...')
        exec_full(str(install_dir)+'swap_axes.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransformX(self, event):
        self.__log('Transforming X values')
        exec_full(str(install_dir)+'transform_x.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransformY(self, event):
        self.__log('Transforming Y values')
        exec_full(str(install_dir)+'transform_y.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransformDY(self, event):
        self.__log('Transforming dY values')
        exec_full(str(install_dir)+'transform_dy.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransformDX(self, event):
        self.__log('Transforming dX values')
        exec_full(str(install_dir)+'transform_dx.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransform(self, event):
        cmd = ('glue')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        
    def OnShowRes(self, event):
        cmd = ('python '+str(install_dir)+'viewer.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnShowPlot(self, event):
        cmd = ('python '+str(install_dir)+'graph_viewer.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnShowGraph(self, event):
        dialog = wx.FileDialog(self, "Choose Grace file to open", os.getcwd(), "","*.agr", wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            selected=dialog.GetPath()
            cmd = (str(pref.cmdGG)+" "+str(selected))
            subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        dialog.Destroy()
        
    def OnTaskPlot(self, event):
        dialog = wx.FileDialog(self, "Choose a draw file to plot with Grace", os.getcwd(), "","*.draw", wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            selected=dialog.GetPath()
            cmd = (str(pref.cmdGB)+" "+str(selected))
            subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        dialog.Destroy()

    def OnTaskColorbat(self, event):
        self.__log('Heat plot view ...')
        exec_full(str(install_dir)+'colorbat.py')

    def OnTaskIP(self, event):
        subprocess.Popen(pref.cmdIP, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnTaskGG(self, event):
        subprocess.Popen(pref.cmdGG, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnTaskR(self, event):
        subprocess.Popen(pref.cmdR, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnTaskSh(self, event):
        subprocess.Popen(pref.cmdSh, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnTaskSpread(self, event):
        subprocess.Popen(pref.cmdspread, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnTask(self, event):
        dialog = wx.MessageDialog(self, 'Not implemented yet.', 'Ehm', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
     
    def OnANOVA(self, event):
        self.__log('Statistics ...')
        exec_full(str(install_dir)+'ANOVA.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTukey(self, event):
        self.__log('Statistics ...')
        exec_full(str(install_dir)+'Tukey.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTWA(self, event):
        self.__log('Statistics ...')
        exec_full(str(install_dir)+'Two_way_ANOVA.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnDataDist(self, event):
        self.__log('Statistics ...')
        exec_full(str(install_dir)+'data_distribution.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnNTest(self, event):
        self.__log('Statistics ...')
        exec_full(str(install_dir)+'shapiro.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTTest1S(self, event):
        self.__log('Statistics ...')
        exec_full(str(install_dir)+'T_test_1_sample.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnPTTest(self, event):
        self.__log('Statistics ...')
        exec_full(str(install_dir)+'T_test_paired.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTTest(self, event):
        self.__log('Statistics ...')
        exec_full(str(install_dir)+'T_test.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnFtest(self, event):
        self.__log('F-test nested models comparison ...')
        exec_full(str(install_dir)+'F-test.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnAICc(self, event):
        self.__log('AICc calculation ...')
        exec_full(str(install_dir)+'AICc.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnResA(self, event):
        self.__log('Residual analysis ...')
        exec_full(str(install_dir)+'residual_analysis.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnLinReg(self, event):
        self.__log('Linear regression ...')
        exec_full(str(install_dir)+'lin_reg.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnPCor(self, event):
        self.__log('Pearsons correlation ...')
        exec_full(str(install_dir)+'pearsons.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnPACor(self, event):
        self.__log('Pearsons correlation ...')
        exec_full(str(install_dir)+'pearsons_a.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnPGACor(self, event):
        self.__log('Pearsons correlation ...')
        exec_full(str(install_dir)+'pearsons_ga.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnSCor(self, event):
        self.__log('Spearmans correlation ...')
        exec_full(str(install_dir)+'spearmans.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnSACor(self, event):
        self.__log('Spearmans correlation ...')
        exec_full(str(install_dir)+'spearmans_a.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnSGACor(self, event):
        self.__log('Spearmans correlation ...')
        exec_full(str(install_dir)+'spearmans_ga.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnCorM(self, event):
        self.__log('Correlation ...')
        exec_full(str(install_dir)+'corr_matrix.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnKmeans(self, event):
        self.__log('Clustering ...')
        exec_full(str(install_dir)+'cluster_K-means.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnSpectralC(self, event):
        self.__log('Clustering ...')
        exec_full(str(install_dir)+'cluster_spectr.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnDT(self, event):
        self.__log('Decision tree ...')
        exec_full(str(install_dir)+'decision_tree.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnLGBM(self, event):
        self.__log('Large Gradient Boosting Machine ...')
        exec_full(str(install_dir)+'LGBM.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnLGBMtest(self, event):
        self.__log('Testing LGBM ...')
        exec_full(str(install_dir)+'LGBM_test.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnMLMSel(self, event):
        self.__log('Selecting best ML model ...')
        exec_full(str(install_dir)+'MLM_selection.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnPCA(self, event):
        self.__log('Principal component analysis ...')
        exec_full(str(install_dir)+'PCA.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnPCAc(self, event):
        self.__log('Subset pricipal component analysis ...')
        exec_full(str(install_dir)+'PCA_color_by_y-value.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnPCAs(self, event):
        self.__log('Subset pricipal component analysis ...')
        exec_full(str(install_dir)+'PCA_subsets.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnMLRM(self, event):
        self.__log('Multiple linear regression model ...')
        exec_full(str(install_dir)+'MLRM.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnHDBSCAN(self, event):
        self.__log('Clustering ...')
        exec_full(str(install_dir)+'cluster_HDBSCAN.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnSumX(self, event):
        self.__log('Analysing X-data ...')
        exec_full(str(install_dir)+'summarize_X_data.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnSumY(self, event):
        self.__log('Analysing Y-data ...')
        exec_full(str(install_dir)+'summarize_Y_data.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnMerge(self, event):
        self.__log('Merging data ...')
        exec_full(str(install_dir)+'merge_data.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnEPC(self, event):
        self.__log('Calculating error propagation')
        dlg = EPC(self, -1, "Enter values", size=(350, 200),
                       #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                       style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                       )
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            mean1 = float(dlg.mean1.GetValue())
            mean2 = float(dlg.mean2.GetValue())
            mean3 = float(dlg.mean3.GetValue())
            SD1 = float(dlg.SD1.GetValue())
            SD2 = float(dlg.SD2.GetValue())
            SD3 = float(dlg.SD3.GetValue())
            formula = dlg.formula.GetValue()
            a = ufloat(mean1, SD1)
            b = ufloat(mean2, SD2)
            c = ufloat(mean3, SD3)
            x = eval(formula)
            res=('EPC.out')
            res=open(res,'w')
            res.write("\nError propagation\n\n")
            res.write("a = "+str(mean1)+", +/- "+str(SD1)+"\n")
            res.write("b = "+str(mean2)+", +/- "+str(SD2)+"\n")
            res.write("x = "+str(formula)+"\n")
            res.write("x = "+str(x)+"\n")
            res.close()
            res=('EPC.out')
            res=open(res,'r')
            tolog=res.read()
            self.__log(tolog)
        else:
            msg = ('Calculation was canceled.')
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            log = open("temp.log","w")
            log.write("Error: Claculation was canceled")
            log.close()
            tolog = log.read()
            self.__log(tolog)
        dlg.Destroy()
       
    def OnTestSD(self, event):
        self.__log('Statistics ...')
        dlg = TestSD(self, -1, "Enter values", size=(350, 200),
                       #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                       style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                       )
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            mean1 = float(dlg.mean1.GetValue())
            mean2 = float(dlg.mean2.GetValue())
            SD1 = float(dlg.SD1.GetValue())
            SD2 = float(dlg.SD2.GetValue())
            n1 = float(dlg.n1.GetValue())
            n2 = float(dlg.n2.GetValue())
            t, p = ttest_ind_from_stats(mean1, SD1, n1, mean2, SD2, n2, equal_var=False)
            res=('T_test.out')
            res=open(res,'w')
            res.write("\nWelch\'s t-test of two samples\n\n")
            res.write("mean = "+str(mean1)+", SD = "+str(SD1)+", n = "+str(n1)+"\n")
            res.write("mean = "+str(mean2)+", SD = "+str(SD2)+", n = "+str(n2)+"\n")
            res.write("\nT = "+str(t)+"\n")
            res.write("p = "+str(p)+"\n")
            now = time.strftime("%d.%m.%Y %H:%M:%S")
            res.write("\n"+str(now)+"\n")
            res.close()
            res=('T_test.out')
            res=open(res,'r')
            tolog=res.read()
            self.__log(tolog)
        else:
            msg = ('Test was canceled.')
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            log = open("temp.log","w")
            log.write("Error: Test was canceled")
            log.close()
            tolog = log.read()
            self.__log(tolog)
        dlg.Destroy()

    def OnTestSEM(self, event):
        self.__log('Statistics ...')
        dlg = TestSEM(self, -1, "Enter values", size=(350, 200),
                       #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                       style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                       )
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            mean1 = float(dlg.mean1.GetValue())
            mean2 = float(dlg.mean2.GetValue())
            SEM1 = float(dlg.SEM1.GetValue())
            SEM2 = float(dlg.SEM2.GetValue())
            n1 = float(dlg.n1.GetValue())
            n2 = float(dlg.n2.GetValue())
            SD1 = SEM1*np.sqrt(n1)
            SD2 = SEM2*np.sqrt(n2)
            t, p = ttest_ind_from_stats(mean1, SD1, n1, mean2, SD2, n2, equal_var=False)
            res=('T_test.out')
            res=open(res,'w')
            res.write("\nWelch\'s t-test of two samples\n\n")
            res.write("mean = "+str(mean1)+", SEM = "+str(SEM1)+", n = "+str(n1)+"\n")
            res.write("mean = "+str(mean2)+", SEM = "+str(SEM2)+", n = "+str(n2)+"\n")
            res.write("\nT = "+str(t)+"\n")
            res.write("p = "+str(p)+"\n")
            now = time.strftime("%d.%m.%Y %H:%M:%S")
            res.write("\n"+str(now)+"\n")
            res.close()
            res=('T_test.out')
            res=open(res,'r')
            tolog=res.read()
            self.__log(tolog)
        else:
            msg = ('Test was canceled.')
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            log = open("temp.log","w")
            log.write("Error: Test was canceled")
            log.close()
            tolog = log.read()
            self.__log(tolog)
        dlg.Destroy()

class DataSets(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, ID, title, pos, size, style)

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "How many data sets do you want to analyse?")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        sampleList = ['1', '2', '3', '4', '5']
        rb = wx.RadioBox(
                self, -1, "", wx.DefaultPosition, wx.DefaultSize,
                sampleList, 5, wx.RA_SPECIFY_COLS | wx.NO_BORDER
                )
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
        rb.SetToolTip(wx.ToolTip("Select the number"))
        sizer.Add(rb, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
        
        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
    def EvtRadioBox(self, event):
        choice = (event.GetSelection())
        curves = float(choice) + 1
        nc = open('nc.tmp','w')
        nc.write(str(curves))
        nc.close()

class EPC(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, ID, title, pos, size, style)

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "Error propagation")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(4, 2, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "a = ")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.mean1 = wx.TextCtrl(self, -1, "900", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.mean1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, " +/- ")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.SD1 = wx.TextCtrl(self, -1, "30", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.SD1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "b = ")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.mean2 = wx.TextCtrl(self, -1, "1500", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.mean2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, " +/- ")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.SD2 = wx.TextCtrl(self, -1, "80", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.SD2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "c = ")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.mean3 = wx.TextCtrl(self, -1, "50", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.mean3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, " +/- ")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.SD3 = wx.TextCtrl(self, -1, "5", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.SD3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "x = ")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.formula = wx.TextCtrl(self, -1, "(a-c)/(b-c)", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.formula, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(grid_sizer, 1, 0, 10)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

class TestSD(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, ID, title, pos, size, style)

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "T-test mean, SD, n")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(2, 3, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Mean #1:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.mean1 = wx.TextCtrl(self, -1, "1", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.mean1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "SD #1:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.SD1 = wx.TextCtrl(self, -1, "0.1", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.SD1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "n #1:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.n1 = wx.TextCtrl(self, -1, "3", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.n1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Mean #2:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.mean2 = wx.TextCtrl(self, -1, "2", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.mean2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "SD #2:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.SD2 = wx.TextCtrl(self, -1, "0.1", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.SD2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "n #2:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.n2 = wx.TextCtrl(self, -1, "3", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.n2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(grid_sizer, 1, 0, 10)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

class TestSEM(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, ID, title, pos, size, style)

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "T-test mean, SEM, n")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(2, 3, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Mean #1:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.mean1 = wx.TextCtrl(self, -1, "1", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.mean1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "SEM #1:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.SEM1 = wx.TextCtrl(self, -1, "0.1", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.SEM1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "n #1:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.n1 = wx.TextCtrl(self, -1, "3", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.n1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Mean #2:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.mean2 = wx.TextCtrl(self, -1, "2", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.mean2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "SEM #2:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.SEM2 = wx.TextCtrl(self, -1, "0.1", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.SEM2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "n #2:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.n2 = wx.TextCtrl(self, -1, "3", size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.n2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(grid_sizer, 1, 0, 10)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

        
app = wx.App(False)
frame = MainWindow()
frame.Show()
app.MainLoop()
