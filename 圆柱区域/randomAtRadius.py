# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:20:00 2020

@author: Lenovo
"""
import numpy as np
import random
def randomAtRadius(radius,height):
    theta = 2*np.pi*random.random() #generate random theta
    x=int(radius*np.cos(theta)) #use trig to transfer into X
    y=int(radius*np.sin(theta)) #find Y coordinate
    z=random.randint(-height,height)
    location=[x, y, z] #save locaction
    return location