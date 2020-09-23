# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 18:30:40 2020

@author: Francois le Roux
This Python script is to be used in conjunction with the main program for all importing purposes of raw data (as output by LabView)
"""
import pandas as pd
import numpy as np

class ImportData():
    '''This class is the one to be used for the importing of data - outputs it as a numpy array'''
    def __init__(self,filename):
        self.filename = filename
        df = pd.read_excel(f'{filename}',header=None)
        self.data = np.array(df)
    
    def get_data(self):
        return self.data
    

def prompt_data(info):
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter.messagebox import showerror
    root = tk.Tk()
    messagebox.showinfo("Take Note:",f"Please select {info} data")
    # Button(root,text="Close",command=root.destroy).pack()
    file_path = filedialog.askopenfilename()
    if not file_path:
        showerror("Error","You did not select a file, or the file you selected is corrupted")
    root.destroy()
    root.mainloop()
    return file_path

def calibration_data():
    data = ImportData(prompt_data("Calibration")).get_data()
    v = input("Please enter the velocity (assumed constant) at which the test was conducted in m/s")
    P = input("Please enter the static pressure value at which the test was conducted in Pa")
    return data, v, P

def windtunnel_data():
    data = ImportData(prompt_data("WindTunnel")).get_data()
    v = input("Please enter the velocity (assumed constant) at which the test was conducted in m/s")
    P = input("Please enter the static pressure value at which the test was conducted in Pa")
    return data, v, P

def position_data():
    data = ImportData(prompt_data("Positioning")).get_data()
    return data
