# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:47:11 2020

@author: Lenovo
"""
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
import matplotlib.pyplot as plt
import os
import imageio
from number_wander3D import checkAround
#from radius_wander import checkAround
from randomAtRadius import randomAtRadius

def DLAcluster(radius):
    if not os.path.isdir("images"):#如果没有对应路径就创建
        os.mkdir("images")
    seedX = radius+5 
    seedY = radius+5 
    seedZ = radius+5
    
    squareSize = radius*2+10
    
    matrix=np.zeros((squareSize, squareSize,squareSize))
    
    matrix[seedX][seedY][seedZ]=1
    for i in range(squareSize):
        for j in range(squareSize):
            for k in range(squareSize):
                if np.sqrt((i-seedX)**2+(j-seedY)**2+(k-seedZ)**2)>=radius:
                    matrix[k][j][i]=2

    R=0.5
    randomWalkersCount = 0
    xx=[]
    yy=[]
    zzz=[]
    completeCluster = False
    randomWalkersCount=0
    addedCount=0 
    usedInterval=[]
    intervalSavePic=range(2,60000000,50)
    while not completeCluster:
        random.seed()
        location=randomAtRadius(R+3, seedX, seedY,seedZ)
        foundFriend = False 
        nearEdge=False 
        while not foundFriend and not nearEdge:
            randomWalkersCount+=1
            locationNew,foundFriend, nearEdge, exitCircle = checkAround(R,radius,location,squareSize,matrix)
            
            if foundFriend:
                if matrix[location[2]][location[1]][location[0]] != 1:
                    matrix[location[2]][location[1]][location[0]] = 1
                    addedCount+=1
                    xx.append(location[2])
                    yy.append(location[1])
                    zzz.append(location[0])
                    c=np.sqrt((location[1]-seedX)**2+(location[0]-seedY)**2+(location[2]-seedY)**2)+0.5
                    if c>R:
                        R=c

            else:
                location = locationNew
    

            if randomWalkersCount in intervalSavePic:#每隔一段时间保存一次
                print("save picture")
                usedInterval.append(randomWalkersCount)
                label=str(randomWalkersCount)
                fig = plt.figure()
                ax = Axes3D(fig)
                ax.scatter(locationNew[2],locationNew[1],locationNew[0],'ro',s=120)#绘制游走中的粒子
                ax.scatter(xx, yy, zzz,'bo',s=120)
                horiAngle=45+randomWalkersCount/200*2#旋转一定角度便于三维观察
                vertAngle=50+randomWalkersCount/200*2
                ax.view_init(vertAngle,horiAngle)
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_zticks([])
                ax.set_xlim(2,squareSize-2)#设置范围便于观察图像
                ax.set_ylim(2,squareSize-2)
                ax.set_zlim(2,squareSize-2)
                plt.savefig("images/cluster{}.png".format(label), dpi=200)#图片保存以绘制动画
                plt.close()
       
        if randomWalkersCount==4000000:
            print("CAUTION: had to break the cycle, taking too many iterations")
            completeCluster = True
        if foundFriend and exitCircle:
            print("Random walkers in the cluster: ",addedCount)
            completeCluster = True
    

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(xx, yy, zzz,'bo',s=120)#绘制所有的点
    ax.set_title("DLA Cluster", fontsize=20)
    ax.set_xlabel("direction, $x$", fontsize=15)
    ax.set_ylabel("direction, $y$", fontsize=15)
    ax.set_zlabel("direction, $z$", fontsize=15)
    ax.set_xlim(2,squareSize-2)
    ax.set_ylim(2,squareSize-2)
    ax.set_zlim(2,squareSize-2)
    plt.savefig("images/cluster.png", dpi=200)
    plt.close()


    with imageio.get_writer('images/movie.gif', mode='I') as writer:
        for i in usedInterval:
            filename="images/cluster"+str(i)+".png"#选择制作动画的图像
            image = imageio.imread(filename)
            writer.append_data(image)
            os.remove(filename)#删除原图像以减少内存占用
           
    return addedCount, matrix
mass,matrix=DLAcluster(10)