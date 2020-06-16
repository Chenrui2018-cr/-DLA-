# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:21:30 2020

@author: Lenovo
"""
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
import matplotlib.pyplot as plt
import os
import imageio
from number_wander import checkAround
from randomAtRadius import randomAtRadius
def DLAcluster(radius,height):
    if not os.path.isdir("images"):#如果没有对应路径就创建
        os.mkdir("images")
    random.seed()
    needGif=True
    seedX = radius+2 
    seedY = radius+2 
    squareSize = radius*2+7
    H = int(height*2+7)
    xx=np.zeros((H))
    yy=np.zeros((H))
    zzz=np.arange(-height-3,height+4,1)
    matrix=np.zeros((squareSize, squareSize,H))
    for i in range(H):
        matrix[seedX][seedY][i]=1#设置种子为一串粒子
    randomWalkersCount = 0
    completeCluster = False
    addedCount=0
    usedInterval=[]
    R=0.5
    while not completeCluster:
        random.seed()
        location=randomAtRadius(R+2,height)#产生一个粒子，粒子是在圆柱面上
        foundFriend = False #not near other particle
        nearEdge=False #not near the edge of the field
        while not foundFriend and not nearEdge:
            randomWalkersCount += 1
            locationNew,foundFriend, nearEdge, exitCircle = checkAround(radius,height,location,squareSize,matrix)
            if foundFriend:
                matrix[radius+2+location[0],radius+2+location[1],height+2+location[2]] = 1
                xx=np.hstack((xx,location[0]))
                yy=np.hstack((yy,location[1]))
                zzz=np.hstack((zzz,location[2]))
                R=np.max([R,0.5+np.sqrt((location[0])**2+(location[1])**2+(location[1])**2)])
                addedCount+=1

            else:
                location = locationNew
        

            intervalSavePic=range(2,400000,50)
            if needGif:
                if randomWalkersCount in intervalSavePic:
                    print("save picture")
                    usedInterval.append(randomWalkersCount)
                    label=str(randomWalkersCount)
                    colors1 = '#3399FF'
                    colors2 = '#FF00FF'
                    fig = plt.figure()
                    ax = Axes3D(fig)
                    ax.scatter(locationNew[0],locationNew[1],locationNew[2],c=colors1,s=100)#绘制运动的点，通过透明度调节图像的三维效果
                    ax.scatter(xx, yy, zzz,c=colors2,s=100,alpha=0.5)#绘制所有聚集体中的点
                    horiAngle=45+randomWalkersCount/100
                    vertAngle=45
                    ax.view_init(vertAngle,horiAngle)#调节视角体现三维
                    ax.set_xticks([])
                    ax.set_yticks([])
                    ax.set_zticks([])
                    ax.set_xlim(-1.5*radius-1,1.5*radius+1)
                    ax.set_ylim(-1.5*radius-1,1.5*radius+1)
                    ax.set_zlim(-1.5*radius-1,1.5*radius+1)
                    plt.savefig("images/cluster{}.png".format(label), dpi=100)#保存图像制作动画
                    plt.close()
       
        if randomWalkersCount==400000:
            print("CAUTION: had to break the cycle, taking too many iterations")
            completeCluster = True

       
        if foundFriend and exitCircle:
            print("Random walkers in the cluster: ",addedCount)
            completeCluster = True
    
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(xx, yy, zzz,c=colors1,s=100)#绘制最终的聚集体图像
    ax.set_title("DLA Cluster", fontsize=20)
    ax.set_xlabel("direction, $x$", fontsize=15)
    ax.set_ylabel("direction, $y$", fontsize=15)
    ax.set_zlabel("direction, $z$", fontsize=15)
    ax.set_ylim(-1.5*radius-1,1.5*radius+1)
    ax.set_xlim(-1.5*radius-1,1.5*radius+1)
    ax.set_zlim(-1.5*radius-1,1.5*radius+1)
    plt.savefig("images/cluster.png", dpi=100)#保存图像
    plt.close()


    if needGif:
        with imageio.get_writer('images/movie.gif', mode='I') as writer:
            for i in usedInterval:
                filename="images/cluster"+str(i)+".png"
                image = imageio.imread(filename)#将图像制作动画
                writer.append_data(image)
                os.remove(filename)#删除图像减少内存
            
    return addedCount, matrix
mass,matrix=DLAcluster(15,1)#绘图代码