# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:26:29 2020

@author: Lenovo
"""

import numpy as np
import random
h=[0,1,0,-1,-1,1,-1,1,0]
m=[1,0,-1,0,-1,1,1,-1,0]
def checkAround(radius,location,squareSize,matrix):
    foundFriend=False
    exitCircle=False
    nearEdge=False
    wander=False
    rr=False
    global location1
    location1=np.zeros((2),dtype=int)
    for i in range(2):
        p=location[i]
        if p < 2 or p > squareSize-2:
            nearEdge=True
    if not nearEdge:
        x=location[0]-radius-2
        y=location[1]-radius-2
        for k in range(8):
            neighbors=matrix[location[1]+h[k],location[0]+m[k]]            
            if neighbors==1 :
                q=1*random.random()
                if q<1:
                    foundFriend=True
                else:
                    wander=True
            if x**2+y**2>=radius**2:
                exitCircle=True
    if not nearEdge and not foundFriend and not wander:

            ran=random.randint(0,7)
            location1[0]=location[0]+h[int(ran)]
            location1[1]=location[1]+m[int(ran)]
            
    if not nearEdge and not foundFriend and wander:
        for i in range(100000):
            ran=random.randint(0,8)
            location1[0]=location[0]+h[int(ran)]
            location1[1]=location[1]+m[int(ran)]
            if not 0<=location1[0]<squareSize or not 0<=location1[1]<squareSize :
                continue
            if matrix[location1[1]][location1[0]] != 1:

                for k in range(8):#该部分描述wander过程，因此也存在原地荡步
                    neighbors=matrix[location[1]+h[k],location[0]+m[k]]
                    if neighbors==1 :
                        rr=True
                        break
            if rr:
                break
    return (location1,foundFriend, nearEdge, exitCircle)