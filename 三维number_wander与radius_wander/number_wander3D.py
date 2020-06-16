# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 11:40:19 2020

@author: Lenovo
"""
import numpy as np
import random
#number_wander的游走方式
h=[0,1,0,-1,0,0,-1,1,-1,1,0,0,0,0,1,1,-1,-1,1,1,1,1,-1,-1,-1,-1,0]
m=[1,0,-1,0,0,0,-1,1,1,-1,1,1,-1,-1,0,0,0,0,1,1,-1,-1,1,1,-1,-1,0]
n=[0,0,0,0,1,-1,0,0,0,0,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,0]
def checkAround(R,radius,location,squareSize,matrix):#结合概率与粒子数有关且wander
    wander=False
    foundFriend=False
    exitCircle=False
    nearEdge=False
    rrr=False
    kesai=6#结合概率与粒子数有关且wander
    global location1
    location1=np.zeros((3),dtype=int)
    for i in range(3):
        p=location[i]
        if p < radius-R+2 or p > radius+8+R:
            nearEdge=True
    if not nearEdge:

        for k in range(26):#检查周边位置是否已被占据，若有被占据位置，则存在两种可能：直接结合或是沿着凝聚体滑行游走
            neighbors=matrix[location[2]+h[k],location[1]+m[k],location[0]+n[k]]            
            if neighbors==1 :#若存在被占据位置，有一定概率结合，结合概率的参数为kesai，取1，3，8等，对应结合概率1/kesai
                q=kesai*random.random()
                if q<1:
                    foundFriend=True
                else:
                    wander=True#滑行
            if neighbors==2:
                exitCircle=True
    
    if not nearEdge and not foundFriend and not wander:#若在限定范围内，周边无占据位置，则继续随机游走

        ran=random.randint(0,25)
        location1[0]=location[0]+h[int(ran)]
        location1[1]=location[1]+m[int(ran)]
        location1[2]=location[2]+n[int(ran)]
    if not nearEdge and not foundFriend and wander:#描述沿凝聚体滑动过程，也可能原地不动
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