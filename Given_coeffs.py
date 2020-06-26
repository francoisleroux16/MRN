# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 22:35:44 2020

@author: Francois le Roux
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

ds = pd.read_excel(r'D:\Tuks\2020\MRN\Samples\Govender_Data.xlsx', sheet_name='NewProbe_coeffs')
probe_data = np.array(ds)

index = np.lexsort((probe_data[:,1],probe_data[:,0])) # Pitch then Yaw

yaw_vals = []
pitch_vals =[]
for x in range(len(probe_data)):
    yaw = probe_data[index[x],1]
    pitch = probe_data[index[x],0]
    if yaw in yaw_vals:
        k=2
    else:
        yaw_vals.append(yaw)
    if pitch in pitch_vals:
        k=3
    else:
        pitch_vals.append(pitch)

counter = 0
for j in range(len(pitch_vals)):
    # plt.figure('C_pp')
    pitch = pitch_vals[j]
    plot = np.zeros((len(yaw_vals),5))
    for x in range(len(yaw_vals)):
        Cpy = probe_data[index[counter],2]
        Cpp = probe_data[index[counter],3] #Actually Cpp, but this is what Wing did - his stuff was wrong
        Cpts = probe_data[index[counter],6]
        # Cpy = data[index[counter],9]
        plot[x,0] = yaw_vals[x]
        plot[x,1] = Cpy
        plot[x,2] = Cpp
        plot[x,3] = Cpts
        plot[x,4] = pitch
        counter += 1
    # plt.scatter(plot[:,0],plot[:,1],label=r'Pitch = '+str(pitch)+r'$\degree$') #Cpy
    # plt.plot(plot[:,0],plot[:,1])
    # plt.scatter(plot[:,0],plot[:,2],label=r'Pitch = '+str(pitch)+r'$\degree$') #Cpp w.r.t. yaw
    # plt.plot(plot[:,0],plot[:,2])
    # plt.scatter(plot[:,0],plot[:,3],label=r'Pitch = '+str(pitch)+r'$\degree$') #Cpts
    # plt.plot(plot[:,0],plot[:,3])
    # plt.scatter(plot[:,1],plot[:,2]) #Cpy vs Cpp
    # plt.plot(plot[:,1],plot[:,2], label=r'Pitch = '+str(pitch)+r'$\degree$')

## Only for carpet plot

# first_legend = plt.legend(loc='upper left', bbox_to_anchor=(1.001,1), borderaxespad =0)   # Right Hand Side

index2 = np.lexsort((probe_data[:,0],probe_data[:,1])) #sorted yaw then pitch
counter2 = 0
# yaw_label = [] #for carpet
for k in range(len(yaw_vals)):
    plt.figure('C_pts_new')
    yaw = yaw_vals[k]
    plot2 =np.zeros((len(pitch_vals),5))
    for z in range(len(pitch_vals)):
        Cpy = probe_data[index2[counter2],2]
        Cpp = probe_data[index2[counter2],3]
        Cpts = probe_data[index2[counter2],4]
        counter2 += 1
        plot2[z,0] = yaw
        plot2[z,1] = Cpy
        plot2[z,2] = Cpp
        plot2[z,3] = Cpts
        plot2[z,4] = pitch_vals[z]
#     yaw_label.append(r'Yaw = '+str(yaw)+r'$\degree$')
#     # plt.scatter(plot2[:,1],plot2[:,2])
#     plt.plot(plot2[:,1],plot2[:,2]) #, label=r'Yaw = '+str(yaw)+r'$\degree$')
#     # plt.scatter(plot2[:,4],plot2[:,1],label=r'Pitch = '+str(pitch)+r'$\degree$')
#     # plt.plot(plot2[:,4],plot2[:,1])
    # plt.scatter(plot2[:,4],plot2[:,2], label=r'Yaw = '+str(yaw)+r'$\degree$') #Cpp w.r.t. pitch
    # plt.plot(plot2[:,4],plot2[:,2]) 
    plt.scatter(plot2[:,4],plot2[:,3], label=r'Yaw = '+str(yaw)+r'$\degree$') #Cpts w.r.t. pitch
    plt.plot(plot2[:,4],plot2[:,3]) 
        
# first_legend = plt.legend(loc='upper left', bbox_to_anchor=(1.001,1), borderaxespad =0)   # Right Hand Side
# ax = plt.gca().add_artist(first_legend)
# plt.legend(labels = yaw_label, loc='upper left', bbox_to_anchor=(1.001,0.35), borderaxespad=0)
# ax = plt.gca().add_artist(first_legend)
# plt.legend(loc='upper left', bbox_to_anchor=(1.001,1), borderaxespad=0)
plt.legend()
# plt.grid(b=True, which='major', color='#666666', linestyle='-') #carpet
# plt.minorticks_on() #carpet
# plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2) #carpet
# plt.xlabel(r"$C_{py}$",fontsize=16) #carpet
plt.xlabel(r"Pitch Angle [$\degree$]",fontsize=16)
plt.ylabel(r"$C_{pts}$",fontsize=16)
plt.title(r'$C_{pts}$ vs Pitch ($\alpha$)',fontsize=16)
plt.show()
