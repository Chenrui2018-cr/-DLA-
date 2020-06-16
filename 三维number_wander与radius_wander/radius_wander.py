# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:12:01 2020

@author: Lenovo
"""

import numpy as np
import random

h=[0,1,0,-1,0,0,-1,1,-1,1,0,0,0,0,1,1,-1,-1,1,1,1,1,-1,-1,-1,-1,0]
m=[1,0,-1,0,0,0,-1,1,1,-1,1,1,-1,-1,0,0,0,0,1,1,-1,-1,1,1,-1,-1,0]
n=[0,0,0,0,1,-1,0,0,0,0,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,0]
def checkAround(R,radius,location,squareSize,matrix):#结合概率与粒子数有关且wander
    wander=False
    foundFriend=False
    exitCircle=False
    nearEdge=False
    couldfoundFriend=False
    rrr=False
    global location1
    location1=np.zeros((3),dtype=int)
    for i in range(3):
        p=location[i]
        if p < radius-R+2 or p > radius+8+R:
            nearEdge=True
    if not nearEdge:
        for k in range(26):
            neighbors=matrix[location[2]+h[k],location[1]+m[k],location[0]+n[k]]            
            if neighbors==1 :
                couldfoundFriend=True
            if neighbors==2:
                exitCircle=True    
            
            
    if couldfoundFriend:
        x=location[0]-radius-2
        y=location[1]-radius-2
        z=location[2]-radius-2
        rr=np.sqrt(x*x+y*y+z*z)
        q=1.5*random.random()
        ww=rr/radius
        if ww<q:
            foundFriend=True
        else:
            wander=True
    if not nearEdge and not foundFriend and not wander:
       
        ran=random.randint(0,25)
        location1[0]=location[0]+h[int(ran)]
        location1[1]=location[1]+m[int(ran)]
        location1[2]=location[2]+n[int(ran)]
    if not nearEdge and not foundFriend and wander:
      
       for i in range(100000):
            ran=random.randint(0,26)
            location1[0]=location[0]+h[int(ran)]
            location1[1]=location[1]+m[int(ran)]
            location1[2]=location[2]+n[int(ran)]
            if not 0<=location1[0]<squareSize or not 0<=location1[1]<squareSize or not 0<=location1[2]<squareSize :
                continue
            if matrix[location1[2]][location1[1]][location1[0]] != 1:
                for k in range(26):#该部分描述wander过程，因此也存在原地荡步
                    neighbors=matrix[location[2]+n[k],location[1]+h[k],location[0]+m[k]]
                    if neighbors==1 :
                        rrr=True
                        break
            if rrr:
                break
    return (location1,foundFriend, nearEdge, exitCircle)