# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 10:36:15 2020

@author: Lenovo
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import os
import imageio
from mpl_toolkits.mplot3d import Axes3D
h=[0,1,0,-1,0,0,-1,1,-1,1,0,0,0,0,1,1,-1,-1,1,1,1,1,-1,-1,-1,-1]
m=[1,0,-1,0,0,0,-1,1,1,-1,1,1,-1,-1,0,0,0,0,1,1,-1,-1,1,1,-1,-1]
g=[0,0,0,0,1,-1,0,0,0,0,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1]
def checkaround(NN,rans,all_location):            
    locationss=all_location[rans]
    pd=[]
    k=False
    if locationss.size==3:
        for i in range(NN):
            if i ==rans:
                continue
            else:
                c=all_location[i]
                if c.size==3:
                    if abs(locationss[0]-c[0])<=1 and abs(locationss[1]-c[1])<=1 and abs(locationss[2]-c[2])<=1:
                        k=True
                   
                else:
                    for j in range(c.shape[0]):
                        if abs(locationss[0]-c[j,0])<=1 and abs(locationss[1]-c[j,1])<=1 and\
                        abs(locationss[2]-c[j,2])<=1:
                            k=True
                       
                if k:
                    pd.append(i)
                    k=False
               
    if locationss.size!=3:
        for w in range(locationss.shape[0]):
            locationss1=locationss[w,:]
            for i in range(NN):
                if i ==rans:
                    continue
                else:
                    c=all_location[i]
                    if c.size==3:
                        if abs(locationss1[0]-c[0])<=1 and abs(locationss1[1]-c[1])<=1 \
                        and abs(locationss1[2]-c[2])<=1 :
                            k=True
                    else:
                        for j in range(c.shape[0]):
                            if abs(locationss1[0]-c[j,0])<=1 and abs(locationss1[1]-c[j,1])<=1 \
                            and abs(locationss1[2]-c[j,2])<=1:
                                k=True
                if k:
                    pd.append(i)
                    k=False
    pd =sorted(set(pd), key = pd.index)
    if len(pd)!=0:
        for j in pd:
            all_location[int(rans)]=np.vstack((all_location[int(rans)],all_location[j]))
    return (all_location,pd)


def wander(k,rans,all_location,radius):
    locationss=all_location[rans]
    for i in range(50):
        c=random.randint(0,25)
        dx=h[c]
        dy=m[c]
        dz=g[c]
        if locationss.size==3:
            location1=np.array([locationss[0]+dx,locationss[1]+dy,locationss[2]+dz])
            if location1[0]**2+location1[1]**2+location1[2]**2<radius**2:
                locationss=location1
                break
            
        else:
            yyy=True
            for j in range(locationss.shape[0]):
                location0=[locationss[j,0]+dx,locationss[j,1]+dy,locationss[j,2]+dz]
                if location0[0]**2+location0[1]**2+location0[2]**2>radius**2:
                    yyy=False
                    break
                
                    
            if yyy:
                locationss[:,0]+=dx
                locationss[:,1]+=dy
                locationss[:,2]+=dz
                break
            
    all_location[rans]=locationss
    return all_location


def randomAtRadius(radius):
    x=radius*(2*random.random()-1)
    y=radius*(2*random.random()-1)
    z=radius*(2*random.random()-1)
    radius_square=radius**2
    while x**2+y**2+z**2>radius_square:
        x=radius*(2*random.random()-1)
        y=radius*(2*random.random()-1)
        z=radius*(2*random.random()-1)
    location=np.array([x, y,z]) #save locaction
    return location


def DLAcluster(NN,radius):#NN代表同时释放的粒子数，粒子数越多代表浓度越高，1为DLA
    if not os.path.isdir("images"):#如果没有对应路径就创建
        os.mkdir("images")
    random.seed(None)
    randomWalkersCount = 0
    all_location=[]
    usedInterval=[]
    location=randomAtRadius(radius)
    all_location.append(location)
    num=1
    for i in range(100000):
        location=randomAtRadius(radius)
        pp=True
        for k in range(num):
            if  (location==all_location[k]).all():
                pp=False
        if pp:
            all_location.append(location)
            num+=1
        if num==NN:
            break
    all_x=[]
    all_y=[]
    all_z=[]
    intervalSavePic=range(2,4000000,50)
    while num>1:
        randomWalkersCount += 1
        rans=random.randint(0,num-1)
        all_location,pd = checkaround(num,rans,all_location)
        all_location = wander(num,rans,all_location,radius)
        all_location = [all_location[i] for i in range(0,len(all_location)) if i not in pd]
        num=len(all_location)
    
        if randomWalkersCount in intervalSavePic:
            fig=plt.figure()
            usedInterval.append(randomWalkersCount) #append to the used count
            label=str(randomWalkersCount)
            plt.title("DLA Cluster", fontsize=20)
            all_locationx=[]
            all_locationy=[]
            all_locationz=[]
            ax = Axes3D(fig)
            for i in range(len(all_location)) :
                k=all_location[i]
                if k.size==3:
                    all_locationx.append(k[0])
                    all_locationy.append(k[1])
                    all_locationz.append(k[2])
                    
                else:
                   for j in range(k.shape[0]):
                       all_locationx.append(k[j,0])
                       all_locationy.append(k[j,1])
                       all_locationz.append(k[j,2])
                       
            ax.plot(all_locationx,all_locationy,all_locationz,'ro',ms=5)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_zticks([])
            horiAngle=45+randomWalkersCount/50*2
            vertAngle=50+randomWalkersCount/50*2
            ax.view_init(vertAngle,horiAngle)
            ax.set_xlim(-radius-1,1+radius)
            ax.set_ylim(-radius-1,1+radius)
            ax.set_zlim(-radius-1,1+radius)
            plt.savefig("images/cluster{}.png".format(label), dpi=200)
            plt.close()
    
    for ww in range(NN):
        all_x.append(all_location[0][ww,0])
        all_y.append(all_location[0][ww,1])
        all_z.append(all_location[0][ww,2])
    fig=plt.figure()
    ax = Axes3D(fig)
    ax.plot(all_x,all_y,all_z,'ro',ms=5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlim(-radius-1,1+radius)
    ax.set_ylim(-radius-1,1+radius)
    ax.set_zlim(-radius-1,1+radius)
    plt.savefig("images/cluster.png", dpi=200)
    plt.close()
    with imageio.get_writer('images/movie.gif', mode='I') as writer:
        for i in usedInterval:
            filename="images/cluster"+str(i)+".png"
            image = imageio.imread(filename)
            writer.append_data(image)
            os.remove(filename)
DLAcluster(120,15)