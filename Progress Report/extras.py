# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 18:37:28 2020

@author: Francois le Roux
This script is for all extra stuff
"""
import numpy as np
import matplotlib.pyplot as plt

def addit(x,y,**kwargs):
    if 'cpy' in kwargs:
        cpy = kwargs['cpy']
    else:
        cpy = 0
        
    if 'cpp' in kwargs:
        cpp = kwargs['cpp']
    else:
        cpp = 0
    
    return np.sin(cpy)**(cpp)
print("Extras")