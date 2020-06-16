# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:20:00 2020

@author: Lenovo
"""
import numpy as np
import random
def randomAtRadius(radius, seedX, seedY):
    theta = 2*np.pi*random.random() #generate random theta
    x=int(radius*np.cos(theta))+seedX #use trig to transfer into X
    y=int(radius*np.sin(theta))+seedY #find Y coordinate
    location=[x, y] #save locaction
    return location