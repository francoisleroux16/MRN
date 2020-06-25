# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:55:23 2020

@author: Francois le Roux
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from mpl_toolkits import mplot3d
import xlsxwriter
import seaborn as sns

def cubic(x,vals1,vals2):
    tck = interpolate.splrep(vals1,vals2)
    return interpolate.splev(x,tck)

def get_coordinates(x):
    unique = set(x)
    return list(unique)

d = 1.6 #probe diameter/2

df = pd.read_excel(r'D:\Tuks\2020\MRN\Samples\Sample Data.xlsx', sheet_name='ready')
data = np.array(df)

zvals = []
yvals = []

# each row of the 2D array is a row of the excel data
for j in range(len(data)):
    z = data[j,0]
    y = data[j,1]
    zvals.append(z)
    yvals.append(y)
    
z_coords = get_coordinates(zvals)
y_coords = get_coordinates(yvals)
##
data2 = data.copy()
#Now P4 and P5
counter2 = 0
z_coords.sort()
z_coords = z_coords[::-1]
for bar in z_coords:
    P4P5 = np.zeros((len(y_coords),4))
    counter = 0
    for k in range(len(data)):
        if data[k,0] == bar:
            P4P5[counter,0] = data[k,1]
            P4P5[counter,1] = data[k,5]
            P4P5[counter,2] = data[k,6]
            P4P5[counter,3] = data[k,0]
            counter += 1
    sortb = P4P5
    # sortb = P4P5[P4P5[:,0].argsort()] #sorts according to Y
    x5 = cubic(list(np.array(sortb[:,0])+d),sortb[:,0],sortb[:,2])
    x4 = cubic(list(np.array(sortb[:,0])-d),sortb[:,0],sortb[:,1])
    for p in range(len(x5)): #Replace the values
        sortb[p,1] = x4[p]
        sortb[p,2] = x5[p]
    #sort according to previous criteria
    for k in range(len(sortb)):
        data2[counter2,5] = sortb[k,1]
        data2[counter2,6] = sortb[k,2]
        counter2 += 1

#P2 first & P3
Final_Data = np.zeros((len(zvals),11))
counter2 = 0
for foo in y_coords:
    #foo is our current y-coord, and we want to cycle over z
    P2P3 = np.zeros((len(z_coords),10))
    counter = 0
    for j in range(len(data)): #j=rows
        if data[j,1] == foo:
            P2P3[counter,0] = data[j,0] #z
            P2P3[counter,1] = data[j,3] #2
            P2P3[counter,2] = data[j,4] #3
            P2P3[counter,3] = data[j,2] #1
            P2P3[counter,4] = data2[j,5] #4
            P2P3[counter,5] = data2[j,6] #5
            P2P3[counter,7] = data[j,8] #t
            P2P3[counter,8] = data[j,9] #s
            P2P3[counter,9] = data[j,10]    #Tc
            counter += 1
    sorte = P2P3[P2P3[:,0].argsort()] #Sorts according to Z
    x2 = cubic(list(np.array(sorte[:,0])+d),sorte[:,0],sorte[:,1])
    x3 = cubic(list(np.array(sorte[:,0])-d),sorte[:,0],sorte[:,2])
    counter3 = 0
    for j in range(len(x2)):
        Final_Data[counter2,0] = sorte[counter3,0]#z
        Final_Data[counter2,1] = foo#y
        Final_Data[counter2,2] = sorte[counter3,3] #1
        Final_Data[counter2,3] = x2[j]#2
        Final_Data[counter2,4] = x3[j]#3
        Final_Data[counter2,5] = sorte[counter3,4]#4
        Final_Data[counter2,6] = sorte[counter3,5]#5
        Final_Data[counter2,8] = sorte[counter3,7] 
        Final_Data[counter2,9] = sorte[counter3,8] 
        Final_Data[counter2,10] = sorte[counter3,9] 
        Final_Data[counter2,7] = (Final_Data[counter2,3]+Final_Data[counter2,4]+Final_Data[counter2,5]+Final_Data[counter2,6])/4
        counter2 += 1
        counter3 += 1
    
def Scatterplot(zvals,yvals,size):
    plt.scatter(zvals,yvals,s=size,c='black') #shows where the pressure measurements were made
    plt.title("Coordinates at which Pressure Values were recorded")
    plt.xlabel("$Z$ [mm]")
    plt.ylabel("$Y$ [mm]").set_rotation(0)
    plt.show()
    
def Plot_3D(Data1,Data2,Data3,title):
    fig = plt.figure(title)
    ax = plt.axes(projection='3d')
    ax.scatter3D(Data1,Data2,Data3)
    plt.show()
    
def visualize(zcoords,ycoords,vx,vy,vz):
    x = np.ones(len(zcoords))
    u = vx
    v = vy
    w = vz
    plt.figure()
    # fig, ax = plt.subplots()
    # fig, ax = plt.figure('Velocity Data')
    # q = ax.quiver(zcoords,ycoords,w,v, np.arctan2(v,w),angles='xy',scale_units='xy')
    plt.quiver(zcoords,ycoords,w,v,angles='xy',scale_units='xy')
    # plt.contourf((zcoords,ycoords),np.arctan2(w,v),cmap='autumn')
    # plt.colorbar()
    
    plt.xlabel(r"$Z$ [mm]")
    plt.ylabel(r'$Y$ [mm]')
    plt.title(r"Plot of the Velocity Vectors in the Z-Y Plane")
    # q = ax.quiver(ycoords,zcoords,v,w)
    # ax = fig.gca(projection='3d')
    # ax.set_xlabel("x")
    # ax.set_ylabel('y')
    # ax.set_zlabel('z')
    # ax.quiver(x,ycoords,zcoords,u,v,w,length =0.1, normalize=True)
    # ax.view_init(azim=180, elev=360)
    plt.show()
    
index = np.lexsort((Final_Data[:,1],-Final_Data[:,0]))

def generate_workbook(index, Final_Data):
    workbook = xlsxwriter.Workbook("Spatially Corrected Data.xlsx")
    worksheet = workbook.add_worksheet("Data")
    row = 0
    col = 0
    worksheet.write(row,col,"Z [mm]")
    worksheet.write(row,col+1,"Y [mm]")
    worksheet.write(row,col+2,"P1")
    worksheet.write(row,col+3,"P2")
    worksheet.write(row,col+4,"P3")
    worksheet.write(row,col+5,"P4")
    worksheet.write(row,col+6,"P5")
    worksheet.write(row,col+7,"Pavg")
    worksheet.write(row,col+8,"Pt")
    worksheet.write(row,col+9,"Ps")
    worksheet.write(row,col+10,"Tc")
    row += 1
    for x in range(len(Final_Data)):
        worksheet.write(row,col,Final_Data[index[x],0])
        worksheet.write(row,col+1,Final_Data[index[x],1])
        worksheet.write(row,col+2,Final_Data[index[x],2])
        worksheet.write(row,col+3,Final_Data[index[x],3])
        worksheet.write(row,col+4,Final_Data[index[x],4])
        worksheet.write(row,col+5,Final_Data[index[x],5])
        worksheet.write(row,col+6,Final_Data[index[x],6])
        worksheet.write(row,col+7,Final_Data[index[x],7])
        worksheet.write(row,col+8,Final_Data[index[x],8])
        worksheet.write(row,col+9,Final_Data[index[x],9])
        worksheet.write(row,col+10,Final_Data[index[x],10])
        row += 1
    workbook.close()

#Comparison of P2 vals
def plot_diffs(index,Final_Data):
    Pdiff2 = []
    Pdiff3 = []
    Pdiff4 =[]
    Pdiff5 = []
    Pavg = []
    for j in range(len(data)):
        Pold = data[j,3]
        Pnew = Final_Data[index[j],3]
        Pdiff2.append(np.abs(Pold-Pnew))
        Pdiff3.append(data[j,4]-Final_Data[index[j],4])
        Pdiff4.append(data[j,5]-Final_Data[index[j],5])
        Pdiff5.append(data[j,6]-Final_Data[index[j],6])
        Pavg.append(data[j,7]-Final_Data[index[j],7])
        
    fig = plt.figure('P2P3')
    sns.distplot(Pdiff2,  label='P2 Values')
    sns.distplot(Pdiff3,  label='P3 Values')
    plt.title("Distribution of the changes between the original and spatially corrected data")
    plt.xlabel("Value Difference")
    plt.ylabel("Frequency")
    plt.legend()
    
    fig = plt.figure('P4P5')
    sns.distplot(Pdiff4, label='P4 Values')
    sns.distplot(Pdiff5, label='P5 Values')
    plt.title("Distribution of the changes between the original and spatially corrected data")
    plt.xlabel("Value Difference")
    plt.ylabel("Frequency")
    plt.legend()
    
    fig = plt.figure('Pavg')
    sns.distplot(Pavg, label=r'$\bar P$ Values')
    plt.title("Distribution of the changes between the original and spatially corrected data")
    plt.xlabel("Value Difference")
    plt.ylabel("Frequency")
    plt.legend()
    
    fig = plt.figure('All')
    sns.distplot(Pdiff2, label='P2 Values')
    sns.distplot(Pdiff3, label='P3 Values')
    sns.distplot(Pdiff4, label='P4 Values')
    sns.distplot(Pdiff5, label='P5 Values')
    plt.title("Distribution of the changes between the original and spatially corrected data")
    plt.xlabel("Value Difference")
    plt.ylabel("Frequency")
    plt.legend()

dplot = pd.read_excel(r'D:\Tuks\2020\MRN\Samples\Sample Data.xlsx', sheet_name='v output')
velocity_components = np.array(dplot)
Zpoints = velocity_components[:,1]
# Zpoints = Zpoints.flatten()
Ypoints = velocity_components[:,2]
Vx = velocity_components[:,4]
Vy = velocity_components[:,5]
Vz = velocity_components[:,6]
# visualize(list(Zpoints), list(Ypoints), list(Vx), list(Vy), list(Vz))
