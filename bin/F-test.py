"""
Standalone utility for F-test.

Usage:
    # Compare models
    f_stat, p_val = f_test_nested(ss_simple, ss_complex, k_simple, k_complex, n)
"""
import os
import time
import wx
import numpy as np
from scipy.stats import f as f_dist

#temp log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
log = open("temp.log","w")

#results log
if os.path.isfile("F-test.res"):
    os.remove("F-test.res")
res = open("F-test.res","w")

def f_test_nested(ss_simple, ss_complex, k_simple, k_complex, n_obs):
    """
    Extra sum-of-squares F-test for nested model comparison.
    
    Use when: model_complex is a constrained/extended version of model_simple
    (e.g., comparing one-site vs. two-site, or Hill with n=1 vs. Hill with free n)
    
    Parameters:
        ss_simple (float): Sum of squared residuals for simpler model
        ss_complex (float): Sum of squared residuals for complex model
        k_simple (int): Number of parameters in simpler model
        k_complex (int): Number of parameters in complex model
        n_obs (int): Number of observations
        
    Returns:
        f_stat (float): F-statistic
        p_value (float): Two-tailed p-value (1 - CDF)
        df_num (int): Numerator degrees of freedom
        df_denom (int): Denominator degrees of freedom
        interpretation (str): Text interpretation of result
        
    Raises:
        ValueError: If models not properly nested or insufficient df
        
    Notes:
        Null hypothesis: Simple model is adequate (complex parameters = 0)
        
        Interpretation:
        - p < 0.05: Complex model significantly better (α = 0.05)
        - p < 0.157: Evidence for complex model (equivalent to AIC threshold)
        - p ≥ 0.157: Simple model adequate (Occam's razor)
        
    References:
        Hall, D. A. (2010). Matching models to data: a receptor pharmacologist's guide.
        British Journal of Pharmacology, 161(8), 1737-1746.
    """
    
    # Validate inputs
    if k_complex <= k_simple:
        raise ValueError(
            f"Complex model must have more parameters ({k_complex}) "
            f"than simple model ({k_simple})"
        )
    
    if ss_complex > ss_simple:
        import warnings
        warnings.warn(
            "SS_complex > SS_simple. Check that models are nested correctly. "
            "(Complex model should fit at least as well as simple model.)"
        )
    
    # Calculate degrees of freedom
    df_num = k_complex - k_simple
    df_denom = n_obs - k_complex
    
    if df_denom <= 0:
        raise ValueError(
            f"Insufficient degrees of freedom: df_denom = {df_denom}. "
            f"Need n ({n_obs}) > k_complex ({k_complex})."
        )
    
    # F-statistic: F = [(SS_simple - SS_complex) / Δdf] / (SS_complex / df_denom)
    ss_diff = ss_simple - ss_complex
    f_stat = (ss_diff / df_num) / (ss_complex / df_denom)
    
    # p-value from F-distribution CDF
    p_value = 1 - f_dist.cdf(f_stat, df_num, df_denom)
    
    # Interpretation
    if p_value < 0.05:
        interpretation = (
            f"Complex model significantly better (P = {p_value:.4f}, α = 0.05)"
        )
    elif p_value < 0.157:
        interpretation = (
            f"Weak evidence for complex model (P = {p_value:.4f}, "
            f"α_AIC = 0.157)"
        )
    else:
        interpretation = (
            f"Simple model adequate (P = {p_value:.4f}); "
            f"prefer simpler model (Occam's razor)"
        )
    
    return f_stat, p_value, df_num, df_denom, interpretation

if __name__ == '__main__':
    
    #select files
    dialog = wx.FileDialog(None, "Choose the data file\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
    if dialog.ShowModal() == wx.ID_OK:
        selected_0=dialog.GetPath()
        data = np.loadtxt(selected_0)    
    else:
        msg = ("Test was canceled.")
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log.write("Error: Test was canceled")
        tolog = log.read()
        None.__log(tolog)

    dialog = wx.FileDialog(None, "Choose the simple model fit file\n", os.getcwd(), "","*.data", wx.FD_OPEN)
    if dialog.ShowModal() == wx.ID_OK:
        selected_1=dialog.GetPath()
        fit_simple = np.loadtxt(selected_1)    
    else:
        msg = ("Test was canceled.")
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log.write("Error: Test was canceled")
        tolog = log.read()
        None.__log(tolog)

    dialog = wx.FileDialog(None, "Choose the complex model file\n", os.getcwd(), "","*.data", wx.FD_OPEN)
    if dialog.ShowModal() == wx.ID_OK:
        selected_2=dialog.GetPath()
        fit_complex = np.loadtxt(selected_2)    
    else:
        msg = ("Test was canceled.")
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log.write("Error: Test was canceled")
        tolog = log.read()
        None.__log(tolog)
    # Load data
    y_data = data[:,1]
    y_fit_simple = fit_simple[:,1]
    y_fit_complex = fit_complex[:,1]

    #Get number of parameters
    ask = ('Enter number of parameters of simple model\n')
    dlg = wx.TextEntryDialog(None, ask,"Input","2")
    if dlg.ShowModal() == wx.ID_OK:
        k_simple = float(dlg.GetValue())
    else:
        msg = ("Test was canceled.")
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log.write("Error: Test was canceled")
        tolog = log.read()
        None.__log(tolog)
    ask = ('Enter number of parameters of complex model\n')
    dlg = wx.TextEntryDialog(None, ask,"Input","3")
    if dlg.ShowModal() == wx.ID_OK:
        k_complex = float(dlg.GetValue())
    else:
        msg = ("Test was canceled.")
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log.write("Error: Test was canceled")
        tolog = log.read()
        None.__log(tolog)
    
    #Compute sum of squares
    residuals_simple = y_data - y_fit_simple
    ss_simple = np.sum(residuals_simple ** 2)
    residuals_complex = y_data - y_fit_complex
    ss_complex = np.sum(residuals_complex ** 2)
    
    #Get number of observations
    n = np.size(y_data)
    
    # F-test for nested models
    f_stat, p_val, df_num, df_denom, interp = f_test_nested(
        ss_simple, ss_complex, k_simple, k_complex, n
    )
    
    #Write results
    res.write("\n--- Nested Model F-test ---\n")
    res.write("Model comparison:\n")
    res.write("  F-statistic:     "+str("{0:.4f}".format(f_stat))+"\n")
    res.write("  Degrees of freedom: "+str(df_num)+" / "+str(df_denom)+"\n")
    res.write("  p-value:         "+str("{0:.4f}".format(p_val))+"\n")
    res.write("  Interpretation:  "+str(interp)+"\n")
    res.write("\n")
    now = time.strftime("%d.%m.%Y %H:%M:%S")
    res.write("\n\n"+str(now)+"\n")
    res.close()

res=open('F-test.res','r')
tolog=res.read()
log.write(tolog)
log.close()

