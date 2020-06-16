# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:21:30 2020

@author: Lenovo
"""
import numpy as np
import random
import matplotlib.pyplot as plt
import os
from matplotlib import colors
import imageio
from number_wander import checkAround
#from radius_wander import checkAround
from randomAtRadius import randomAtRadius
def DLAcluster(radius):
    if not os.path.isdir("images"):#如果没有对应路径就创建
        os.mkdir("images")

    needGif=True
    seedX = radius+2 
    seedY = radius+2 
    squareSize = radius*2+5
    matrix=np.zeros((squareSize, squareSize))
    matrix[seedX][seedY]=1


   
    randomWalkersCount = 0
    xx=[seedX]
    yy=[seedY]

    completeCluster = False

 
    addedCount=0

    usedInterval=[]
    R=0.5
    while not completeCluster:
        
        random.seed()


        location=randomAtRadius(R+2, seedX, seedY)

        
        foundFriend = False 
        nearEdge=False

        
        
        while not foundFriend and not nearEdge:
            randomWalkersCount += 1
          
            locationNew,foundFriend, nearEdge, exitCircle = checkAround(radius,location,squareSize,matrix)
            
          
            if foundFriend:
                
            
                matrix[location[1]][location[0]] = 1
                R=np.max([R,0.5+np.sqrt((location[1]-seedX)**2+(location[0]-seedY)**2)])
                addedCount+=1
                xx.append(location[1])
                yy.append(location[0])

            else:
                location = locationNew
        

            intervalSavePic=range(2,400000,50)
            if needGif:
                if randomWalkersCount in intervalSavePic:#每隔一定时间保存图像
                    print("save picture")
                    usedInterval.append(randomWalkersCount) 
                    label=str(randomWalkersCount)
                    plt.title("DLA Cluster", fontsize=20)
                    plt.plot(locationNew[1],locationNew[0],'ro',ms=10)#绘制游走过程中点的图像
                    plt.plot(xx,yy,'bo',ms=10)#绘制已经结合的点的图像
                    plt.xlim(0,squareSize)
                    plt.ylim(0,squareSize)
                    plt.xlabel("direction, $x$", fontsize=15)
                    plt.ylabel("direction, $y$", fontsize=15)
                    plt.savefig("images/cluster{}.png".format(label), dpi=200)#储存图像
                    plt.close()
       
        if randomWalkersCount==400000:
            print("CAUTION: had to break the cycle, taking too many iterations")
            completeCluster = True

        
        if foundFriend and exitCircle:
            print("Random walkers in the cluster: ",addedCount)
            completeCluster = True
    
    plt.title("DLA Cluster", fontsize=20)
    plt.plot(xx,yy,'bo',ms=10)#绘制所有的点的最终图像
    plt.xlim(0,squareSize)
    plt.ylim(0,squareSize)
    plt.xlabel("direction, $x$", fontsize=15)
    plt.ylabel("direction, $y$", fontsize=15)
    plt.savefig("images/cluster.png", dpi=200)#保存最终图像
    plt.close()
    print(usedInterval)
    if needGif:
        with imageio.get_writer('images/movie.gif', mode='I') as writer:
            for i in usedInterval:
                filename="images/cluster"+str(i)+".png"
                image = imageio.imread(filename)#将图像写入动画
                writer.append_data(image)
                os.remove(filename)#删除所有做成动画的图片
            

    return addedCount, matrix
mass,matrix=DLAcluster(15)