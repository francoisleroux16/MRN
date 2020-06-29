# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 22:35:44 2020

@author: Francois le Roux
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import os

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

def gen_details_y(num):
    '''Number is 2 = Cpy, 3= Cpp. 5 = Cps, 4= Cpt, 6 = Cpts
    Returns name, description'''
    if num == 3:
        name = 'Cpp'
        description = r'$C_{pp}$'
        indexval = 3
    elif num == 5:
        name = 'Cps'
        description = r'$C_{ps}$'
        indexval = 5
    elif num == 4:
        name = 'Cpt'
        description = r'$C_{pt}$'
        indexval = 4
    elif num == 6:
        name = 'Cpts'
        description = r'$C_{pts}$'
        indexval = 6
    elif num == 0:
        name = 'Pitch'
        description = r'Pitch ($\alpha$)'
        indexval = 0
    elif num == 1:
        name = 'Yaw'
        description = r'Yaw ($\beta$)'
        indexval = 1
    else:
        name = 'Cpy'
        description = r'$C_{py}$'
        indexval = 2
    return name, description, indexval

def gen_details_x(num):
    name, description , indexval= gen_details_y(num)
    return name, description, indexval

def get_data(dataname,sheetname=''):
    ''' dataname is full path name (with r) - sheet name only if applicable
    returns data as numpy array'''
    print('I was here')
    if sheetname == '':
        ds = pd.read_excel(dataname)
    else:
        ds = pd.read_excel(dataname, sheet_name=sheetname)
    return np.array(ds)

def get_pitchyaw(data,index):
    yaw_v = []
    pitch_v = []
    for x in range(len(data)):
        yaw = data[index[x],1]
        pitch = data[index[x],0]
        if yaw not in yaw_v:
            yaw_v.append(yaw)
        if pitch not in pitch_v:
            pitch_v.append(pitch)
    return yaw_v, pitch_v

def plotdata(data,numx, numy):
    '''data is imported data -has coefficients already: 0 = Pitch, 1 = yaw, 2= Cpy, 3=Cpp,4=Cpt,5=Cps,6=Cpts
    num is what to plot'''

    name, description, indexval = gen_details_y(numy) #y_axis
    xname, xdescription, xindexval = gen_details_x(numx) #x-axis
    if numx == 0:
        labelname, foo, bar = gen_details_x(1)
    else:
        labelname, foo, bar = gen_details_x(0)
    plt.figure(name+' vs '+xname)
    ################
    index = np.lexsort((data[:,xindexval],data[:,bar])) 
    yaw_vals, pitch_vals = get_pitchyaw(data,index)
    ################
    for x in range(len(data)):
        yaw = data[index[x],1]
        pitch = data[index[x],0]
        if yaw not in yaw_vals:
            yaw_vals.append(yaw)
        if pitch not in pitch_vals:
            pitch_vals.append(pitch)
        
    counter = 0
    for j in range(len(pitch_vals)):
        # plt.figure('C_pp')
        if bar == 0:
            val = pitch_vals[j]
            iterate = yaw_vals
        if bar == 1:
            val = yaw_vals[j]
            iterate = pitch_vals
        plot = np.zeros((len(iterate),2))
        for x in range(len(iterate)):
            plot[x,0] = data[index[counter],xindexval] #yaw
            plot[x,1] = data[index[counter],indexval] #Cpy
            counter += 1

        plt.scatter(plot[:,0],plot[:,1],label=foo+'= '+str(val)+r'$\degree$') 
        plt.plot(plot[:,0],plot[:,1])
    ######
    plt.title(description+' vs '+xdescription, fontsize=16)
    plt.legend()
    plt.ylabel(description,fontsize=16)
    plt.xlabel(xdescription,fontsize=16)
    plt.show()

def plotcarpet(data):
    '''This plots the carpet plot, with respect to Cpy and Cpp'''
    index = np.lexsort((data[:,1],data[:,0]))
    yaw_vals, pitch_vals = get_pitchyaw(data, index)
    counter = 0
    for j in range(len(pitch_vals)):
        plt.figure('Carpet')
        pitch = pitch_vals[j]
        plot = np.zeros((len(yaw_vals),4))
        for x in range(len(yaw_vals)):
            Cpy = data[index[counter],2]
            Cpp = data[index[counter],3]
            plot[x,0] = yaw_vals[x]
            plot[x,1] = pitch
            plot[x,2] = Cpy
            plot[x,3] = Cpp
            counter += 1
        plt.scatter(plot[:,2],plot[:,3])
        plt.plot(plot[:,2],plot[:,3],label=r'Pitch = '+str(pitch)+r'$\degree$')
        
    first_legend = plt.legend(loc='upper left', bbox_to_anchor=(1.001,1), borderaxespad=0)
    
    index2 = np.lexsort((data[:,0],data[:,1]))
    counter2 = 0
    yaw_label = [None]*len(yaw_vals)
    for k in range(len(yaw_vals)):
        plt.figure('Carpet')
        yaw = yaw_vals[k]
        plot2 = np.zeros((len(pitch_vals),4))
        for z in range(len(pitch_vals)):
            Cpy = data[index2[counter2],2]
            Cpp = data[index2[counter2],3]
            counter2 += 1
            plot2[z,0] = yaw
            plot[z,1] = pitch_vals[z]
            plot2[z,2] = Cpy
            plot2[z,3] = Cpp
        yaw_label[k] = r'Yaw = '+str(yaw)+r'$\degree$'
        plt.scatter(plot2[:,2],plot2[:,3])
        plt.plot(plot2[:,2],plot2[:,3], label='Yaw')
    plt.gca().add_artist(first_legend)
    plt.grid(b=True, which='major', color='#666666', linestyle='-') 
    plt.minorticks_on() #carpet
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2) 
    plt.legend(labels = yaw_label, loc='upper left', bbox_to_anchor=(1.001,0.35), borderaxespad=0)
    plt.xlabel(r"$C_{py}$",fontsize=16)
    plt.ylabel(r'$C_{pp}$',fontsize=16)
    plt.title(r'$C_{py}$ vs $C_{pp}$ over Yaw and Pitch')
    plt.show()

# data = []
# path = r'D:\Tuks\2020\MRN\Samples\Govender_Data.xlsx'
# sheetname = 'NewProbe_coeffs'
# path = r'D:\Tuks\2020\MRN\Code\Test.xlsx'
# path = input("Please enter path to excel file")
# probe_data = get_data(path.encode('unicode-escape').decode())
# def start_program():
#     ''' Keeping it neat'''
root = Tk()
# global data
def open_file():
    global data
    filename = filedialog.askopenfilename(title='Select file')
    data = get_data(filename)
    data_imported() #Enables plotting functions
    return data

def close_window():
    global data
    root.destroy()
    
def popupmsg():
    global data, boolean
    try:
        if len(data) >= 0:
            boolean = False
    except:
        boolean = True
        data = []
        popup = Tk()
        popup.wm_title("!")
        label = Label(popup, text='No data imported \n Click "Close" again to exit', font=("Verdana",10))
        label.pack(side='top',fill="x",pady=10)
        B1 = Button(popup, text="Ok",command=popup.destroy)
        B1.pack()
        popup.mainloop()
        return data, boolean

def data_imported():
    btn.pack_forget()
    
    carpet_btn.pack()

    btnx.pack()
    varx.set("Yaw")
    optionx.pack()
    
    btny.pack()
    vary.set("Cpy")
    optiony.pack()
    
    plotbtn.pack()
    
def x_axis_value():
    global xval
    temp = varx.get()
    options = ["Pitch","Yaw","Cpy", "Cpp", "Cpt","Cps","Cpts"]
    xval = options.index(temp)
    return xval

def y_axis_value():
    global yval
    temp = vary.get()
    options = ["Pitch","Yaw","Cpy", "Cpp", "Cpt","Cps","Cpts"]
    yval = options.index(temp)
    return yval

def execute(data):
    x = x_axis_value()
    y = y_axis_value()
    plotdata(data,x,y)
    
# carpet_btn = Button(root, text="Do Carpet Plot", command=lambda:plotcarpet(data))
btn = Button(root, text='Open', command = open_file)
btn.pack(side = TOP, pady=10)
closebtn = Button(root, text='Close', command = lambda:[popupmsg(),close_window()])
closebtn.pack()

carpet_btn = Button(root, text="Carpet Plot", command=lambda:plotcarpet(data))

varx = StringVar(root)
optionx = OptionMenu(root, varx, "Select","Pitch","Yaw","Cpy", "Cpp", "Cpt","Cps","Cpts")
btnx=Button(root,text="x_axis",command = x_axis_value)

vary = StringVar(root)
optiony = OptionMenu(root,vary,"Select","Pitch","Yaw","Cpy","Cpp","Cpt","Cps","Cpts")
btny = Button(root,text="y_axis",command=y_axis_value)

plotbtn = Button(root,text="Normal Plots",command=lambda:execute(data))

mainloop()

# data = start_program()
