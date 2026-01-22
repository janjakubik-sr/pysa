"""
Standalone utility functions for AICc calculation.

These lightweight functions can be imported independently for quick model comparisons
without using the full BindingModelComparison class.

Usage:
    aicc = calculate_aicc(y, y_predicted, k_params=3)
"""
import os
import time
import wx
import numpy as np

#temp log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
log = open("temp.log","w")

#init

def calculate_aicc(y_obs, y_pred, k_params):
    """
    Calculate AICc (corrected Akaike Information Criterion).
    
    AICc = AIC + 2*k*(k+1)/(n-k-1)
    where AIC = -2*ln(L) + 2*k
    
    Parameters:
        y_obs (array): Observed values
        y_pred (array): Predicted/fitted values
        k_params (int): Number of fitted parameters
        verbose (bool): Print intermediate calculations
        
    Returns:
        aicc (float): AICc value
        aic (float): AIC value (for reference)
        ll (float): Log-likelihood
        
    Notes:
        - Lower AICc = better fit (accounting for complexity)
        - Use for comparing both nested and non-nested models
        - Preferred over AIC when n/k < 40 (common in pharmacology)
    """
    y_obs = np.asarray(y_obs)
    y_pred = np.asarray(y_pred)
    
    if len(y_obs) != len(y_pred):
        raise ValueError("y_obs and y_pred must have same length")
    
    n = len(y_obs)
    
    # Calculate residual sum of squares
    residuals = y_obs - y_pred
    ss_res = np.sum(residuals ** 2)
    
    # Mean squared error
    mse = ss_res / n
    
    # Log-likelihood (assuming normal errors)
    ll = -0.5 * (n * np.log(2 * np.pi * mse) + ss_res / mse)
    
    # AIC = -2*ln(L) + 2*k
    aic = -2 * ll + 2 * k_params
    
    # AICc = AIC + 2*k*(k+1)/(n-k-1)
    if n - k_params - 1 > 0:
        aicc = aic + 2 * k_params * (k_params + 1) / (n - k_params - 1)
    else:
        aicc = np.inf
    
    return aicc, aic, ll, n, ss_res, mse

#select files
dialog = wx.FileDialog(None, "Choose the data file\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_0=dialog.GetPath()
    data = np.loadtxt(selected_0)    
else:
    msg = ("AICc calculation was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: AICc calculation was canceled")
    tolog = log.read()
    None.__log(tolog)

dialog = wx.FileDialog(None, "Choose the model fit file\n", os.getcwd(), "","*.data", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_1=dialog.GetPath()
    fit = np.loadtxt(selected_1)    
else:
    msg = ("AICc calculation was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: AICc calculation was canceled")
    tolog = log.read()
    None.__log(tolog)

#Get number of parameters
ask = ('Enter number of model parameters\n')
dlg = wx.TextEntryDialog(None, ask,"Input","2")
if dlg.ShowModal() == wx.ID_OK:
    k = float(dlg.GetValue())
else:
    msg = ("Test was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: Test was canceled")
    tolog = log.read()
    None.__log(tolog)


# Calculate AICc for a single fit  
data = np.loadtxt(selected_0)
fit = np.loadtxt(selected_1)
y_data  = data[:,1]
y_fit = fit[:,1]
aicc, aic, ll, n, ss_res, mse = calculate_aicc(y_data, y_fit, k)

base=os.path.splitext(selected_1)[0]
out=(str(base)+'_AICc.res')
res=open(out,'w')
res.write("\n--- Model AICc ---\n")
res.write("  n = "+str(n)+"\n")
res.write("  k = "+str(k)+"\n")
res.write("  SS_res = "+str("{0:.6e}".format(ss_res))+"\n")
res.write("  MSE = "+str("{0:.6e}".format(mse))+"\n")
res.write("  log-likelihood = "+str("{0:.4f}".format(ll))+"\n")
res.write("  AIC = "+str("{0:.2f}".format(aic))+"\n")
res.write("  AICc = "+str("{0:.2f}".format(aicc))+"\n")
res.write("\n")
now = time.strftime("%d.%m.%Y %H:%M:%S")
res.write("\n\n"+str(now)+"\n")
res.close()

res=open(out,'r')
tolog=res.read()
log.write(tolog)
log.close()