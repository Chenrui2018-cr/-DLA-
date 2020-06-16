# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:02:17 2020

@author: Lenovo
"""

import numpy as np
import random

h=[0,1,0,-1,0,0,-1,1,-1,1,0,0,0,0,1,1,-1,-1,1,1,1,1,-1,-1,-1,-1,0]
m=[1,0,-1,0,0,0,-1,1,1,-1,1,1,-1,-1,0,0,0,0,1,1,-1,-1,1,1,-1,-1,0]
n=[0,0,0,0,1,-1,0,0,0,0,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,0]
def checkAround(radius,height,location,squareSize,matrix):
    foundFriend=False
    exitCircle=False
    nearEdge=False
    couldfoundFriend=False
    wander=False
    rr=False
    global location1
    location1=np.zeros((3),dtype=int)
    for i in range(2):
        p=location[i]
        if abs(p)>(0.5*squareSize):
            nearEdge=True

    if not nearEdge:
        x=location[0]
        y=location[1]
        z=location[2]
        rr=np.sqrt(x*x+y*y)
        for k in range(27):
            neighbors=matrix[radius+2+location[0]+h[k],radius+2+location[1]+m[k],height+2+location[2]+n[k]]
            if neighbors==1 :
                couldfoundFriend=True
            if rr>=radius :
                exitCircle=True
        if couldfoundFriend:
            q=4*random.random()
            ww=np.sqrt(rr**2+z**2)/np.sqrt(radius**2+height**2)
            if ww<q:
                foundFriend=True
            else:
                wander=True
    if not nearEdge and not foundFriend and not wander:
        for i in range(100000):
            ran=random.randint(0,25)
            location1[0]=location[0]+h[int(ran)]
            location1[1]=location[1]+m[int(ran)]
            location1[2]=location[2]+n[int(ran)]
            if not abs(location1[2])<height :
                continue
            break
    if not nearEdge and not foundFriend and wander:
        for i in range(100000):
            ran=random.randint(0,26)
            location1[0]=location[0]+h[int(ran)]
            location1[1]=location[1]+m[int(ran)]
            location1[2]=location[2]+n[int(ran)]
            if not abs(location1[0])<0.5*squareSize or not abs(location1[1])<0.5*squareSize or not abs(location1[2])<height :
                continue
            if matrix[radius+2+location1[0]][radius+2+location1[1]][height+2+location1[2]] != 1:
               for k in range(27):#该部分描述wander过程，因此也存在原地荡步
                    neighbors=matrix[radius+2+location[0]+h[k],radius+2+location[1]+m[k],height+2+location[2]+n[k]]
                    if neighbors==1 :
                        rr=True
                        break
            if rr:
                break
    return (location1,foundFriend, nearEdge, exitCircle)