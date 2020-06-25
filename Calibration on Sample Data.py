# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 14:46:43 2020

@author: Francois le Roux
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

class Ligrani():
    '''Use this to generate the calibration data at each 'unique' pitch and yaw'''
    def __init__(self, Pt, Ps, P1, P2, P3, P4, P5):
        self.P_t = Pt
        self.P_1 = P1
        self.P_2 = P2
        self.P_3 = P3
        self.P_4 = P4
        self.P_5 = P5
        self.P_s = Ps
        
    def P_average(self):
        '''Currently Ligrani Method'''
        ans = (self.P_2+self.P_3+self.P_4+self.P_5)/4
        return ans
    
    def C_py(self):
        # ans = (self.P_2-self.P_3)/(self.P_1-self.P_average())
        #Because of definition by Ligrani this has to change
        ans = (self.P_3-self.P_2)/(self.P_1-self.P_average())
        return ans
    
    def C_pp(self):
        # ans = (self.P_4-self.P_5)/(self.P_1-self.P_average())
        #Because of definition by Ligrani this has to change
        ans = (self.P_5-self.P_4)/(self.P_1-self.P_average())
        return ans
    
    def C_pt(self):
        ans = (self.P_t-self.P_average())/(self.P_1-self.P_average())
        return ans
    
    def C_ps(self):
        ans =(self.P_1-self.P_s)/(self.P_1-self.P_average())
        return ans
    
    def C_pts(self):
        # ans = (self.P_t-self.P_s)/(self.P_1-self.P_average())
        ans = (self.P_1-self.P_s)/(self.P_1-self.P_average())
        return ans

df = pd.read_excel(r'D:\Tuks\2020\MRN\Samples\JONO\Probe Calibration\Calibration Data and Plots.xlsx')
data = np.array(df)
PS = data[0,14]
# Pt = 25.23/813309 # Due to errors in the data from Wing, this Pt is assumed from other data
Pt = 15 #From Wing
coeffs = np.zeros((len(data),6))
for j in range(len(data)):
    usage = Ligrani(Pt,PS,data[j,0],data[j,1],data[j,2],data[j,3],data[j,4])
    coeffs[j,0] = data[j,5]
    coeffs[j,1] = data[j,6]
    coeffs[j,2] = usage.C_py()
    coeffs[j,3] = usage.C_pp()
    coeffs[j,4] = usage.C_pt()
    coeffs[j,5] = usage.C_pts()
    
#Cpy vs Yaw angle
index = np.lexsort((coeffs[:,0],coeffs[:,1])) #sorted pitch, then yaw
yaw_vals = []
pitch_vals =[]
for x in range(len(coeffs)):
    yaw = coeffs[index[x],0]
    pitch = coeffs[index[x],1]
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
    plt.figure('C_py')
    pitch = pitch_vals[j]
    plot = np.zeros((len(yaw_vals),5))
    for x in range(len(yaw_vals)):
        Cpy = coeffs[index[counter],2]
        Cpp = coeffs[index[counter],3] #Actually Cpp, but this is what Wing did - his stuff was wrong
        Cpts = coeffs[index[counter],5]
        # Cpy = data[index[counter],9]
        plot[x,0] = yaw_vals[x]
        plot[x,1] = Cpy
        plot[x,2] = Cpp
        plot[x,3] = Cpts
        plot[x,4] = pitch
        counter += 1
    # plt.scatter(plot[:,0],plot[:,3],label=r'Pitch = '+str(pitch)+r'$\degree$')
    # plt.plot(plot[:,0],plot[:,3])
    plt.scatter(plot[:,1],plot[:,2])
    plt.plot(plot[:,1],plot[:,2], label=r'Pitch = '+str(pitch)+r'$\degree$')

first_legend = plt.legend(loc='upper left', bbox_to_anchor=(1.001,1), borderaxespad =0)   # Right Hand Side

index2 = np.lexsort((coeffs[:,1],coeffs[:,0])) #sorted yaw then pitch
counter2 = 0
yaw_label = []
for k in range(len(yaw_vals)):
    plt.figure('C_py')
    yaw = yaw_vals[k]
    plot2 =np.zeros((len(pitch_vals),5))
    for z in range(len(pitch_vals)):
        Cpy = coeffs[index2[counter2],2]
        Cpp = coeffs[index2[counter2],3]
        Cpts = coeffs[index2[counter2],4]
        counter2 += 1
        plot2[z,0] = yaw
        plot2[z,1] = Cpy
        plot2[z,2] = Cpp
        plot2[z,3] = Cpts
        plot2[z,4] = pitch_vals[z]
    yaw_label.append(r'Yaw = '+str(yaw)+r'$\degree$')
    # plt.scatter(plot2[:,1],plot2[:,2])
    plt.plot(plot2[:,1],plot2[:,2]) #, label=r'Yaw = '+str(yaw)+r'$\degree$')
    # plt.scatter(plot2[:,4],plot2[:,1],label=r'Pitch = '+str(pitch)+r'$\degree$')
    # plt.plot(plot2[:,4],plot2[:,1])
        
# first_legend = plt.legend(loc='upper left', bbox_to_anchor=(1.001,1), borderaxespad =0)   # Right Hand Side
# ax = plt.gca().add_artist(first_legend)
plt.legend(labels = yaw_label, loc='upper left', bbox_to_anchor=(1.001,0.35), borderaxespad=0)
ax = plt.gca().add_artist(first_legend)
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.xlabel(r"$C_{py}$",fontsize=16)
plt.ylabel(r"$C_{pp}$",fontsize=16)
plt.title(r'$C_{py}$ vs $C_{pp}$ ')
plt.show()    
    
# plt.title(r"$C_{pts}$ vs Yaw ($\beta$)",fontsize=16)
# plt.xlabel(r"Yaw Angle [$\degree$]",fontsize=16)
# plt.ylabel(r"$C_{pts}$",fontsize=16)
# plt.legend(loc='center left', bbox_to_anchor=(1,0.5), fancybox = True, shadow = True)   # Right Hand Side
# plt.legend(loc='upper center', bbox_to_anchor=(0.5,-0.05), fancybox=True, shadow = True, ncol = 6) #Bottom
# plt.show()