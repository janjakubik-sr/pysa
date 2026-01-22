# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 12:12:20 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""

import os
import time
import wx
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy


#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

def load_2_column_data(filepath):
    """
    Loads data from a 2-column space-separated file.

    Both columns are converted to floats (x_data and y_data).

    Args:
        filepath (str): The path to the input file.

    Returns:
        tuple: A tuple containing four lists (x_data, y_data, groups, annotations).
    """
    x_data = []
    y_data = []

    try:
        with open(selected, 'r') as f:
            for line_number, line in enumerate(f, 1):
                # Strip leading/trailing whitespace and split by whitespace
                parts = line.strip().split()

                # Ensure we have exactly 3 columns
                if len(parts) != 2:
                    print(f"Warning: Skipping line {line_number} in {selected}. Expected 4 columns, found {len(parts)}: '{line.strip()}'")
                    continue

                try:
                    # Column 1: x_data (float)
                    x = float(parts[0])
                    # Column 2: y_data (float)
                    y = float(parts[1])

                    x_data.append(x)
                    y_data.append(y)

                except ValueError as e:
                    # Handle case where conversion to float fails
                    print(f"Error on line {line_number}: Could not convert columns 1 or 2 to float. Details: {e}")
                    continue

        return x_data, y_data

    except FileNotFoundError:
        print(f"Error: The file '{selected}' was not found.")
        return [], []
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return [], []

dialog = wx.FileDialog(None, "Choose a data file to perform Spearman's correlation test", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    msg = ('Calculate Spearman\'s coefficient for '+str(selected)+' ?')
    dlg = wx.MessageDialog(None, msg, 'Calculte', wx.OK|wx.CANCEL)
    if dlg.ShowModal() == wx.ID_OK:
        with open(selected) as d:
            reader = csv.reader(d, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)
            if num_cols == 2:
                #load data
                x_data, y_data = load_2_column_data(selected)
                #regression
                results=scipy.stats.spearmanr(x_data,y_data)
                rho=results[0]
                p=results[1]
                #save data
                base=os.path.splitext(selected)[0]
                res_file=(str(base)+'_spearmans.res')
                res=open(res_file,'w')
                res.write("\n\nSpearmans correlation statistics on "+str(selected)+"\n\n")
                res.write("Rho = "+str(rho)+"\n")
                res.write("p-value = "+str(p)+"\n")
                now = time.strftime("%d.%m.%Y %H:%M:%S")
                res.write("\n\n"+str(now)+"\n")
                res.close()
                #plot
                rho_value=str("{0:.4f}".format(rho))
                p_value=str("{:.2e}".format(p))
                title=("Spearman's rho="+str(rho_value)+"\n P="+str(p_value))
                plt.title(title)
                colormap = np.array(['r','g','b','c','m','y','k'])
                plt.scatter(x_data, y_data, s=100)
                plt.show()          
                #log
                res=(str(base)+'_spearmans.res')
                res=open(res,'r')
                tolog=res.read()
                log=open("temp.log",'w')
                log.write(tolog)
                log.close()
                dlg.Destroy()
            else:
                msg = ('Wrong column count!\n2 expected, '+str(num_cols)+' found')
                err = msg
                dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
                dialog.ShowModal()
                dialog.Destroy()
    else:
        log = open("temp.log","w")
        log.write("Testing of "+str(selected)+" interupted.")
        log.close()
        dlg.Destroy()
