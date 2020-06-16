# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 11:37:38 2020

@author: Lenovo
"""
import numpy as np
import random
def randomAtRadius(radius, seedX, seedY,seedZ):
    ##radius=radius*random.random()
    theta = 2*np.pi*random.random() #generate random theta
    csi=np.pi*random.random()
    x=int(radius*np.cos(theta)*np.sin(csi))+seedX #use trig to transfer into X
    y=int(radius*np.sin(theta)*np.sin(csi))+seedY 
    z=int(radius*np.cos(csi))+seedZ#find Y coordinate
    location=[x, y,z] #save locaction
    return location