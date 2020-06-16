# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:47:11 2020

@author: Lenovo
"""
import numpy as np
import random
import matplotlib.pyplot as plt
import os
from matplotlib import colors
import imageio
h=[0,1,0,-1,1,1,-1,-1]
m=[1,0,-1,0,-1,1,-1,1]

def checkAround(NN,rans,all_location,squareSize,matrix):
    foundFriend=False
    exitCircle=False
    nearEdge=False
    global locationss,c
    locationss=all_location[int(rans)]
    min_loc=np.min(locationss)
    max_loc=np.max(locationss)
    if min_loc < 2 or max_loc > squareSize-2:
        nearEdge=True#判断是否会游走出去
    
    if not nearEdge:
        if locationss.size==2:#单粒子
            for k in range(8):#此时判断结合的标准为8个方向
                neighbors=matrix[locationss[1]+h[k],locationss[0]+m[k]]            
                if neighbors==1 :#此时代表有粒子相邻
                    foundFriend=True
                if neighbors==2:#此时代表可能生长大小达到要求
                    exitCircle=True
        else:
            for j in range(locationss.shape[0]):#多粒子

                location0=locationss[j,:]
                for k in range(8):#此时判断结合的标准为8个方向
                    neighbors=matrix[location0[1]+h[k],location0[0]+m[k]]            
                    if neighbors==1 :#此时代表有粒子相邻
                        foundFriend=True
                    if neighbors==2:#此时代表可能生长大小达到要求
                        exitCircle=True
    if not nearEdge and not foundFriend :#向8个方向游走，上下左右，上左，上右，下左，下右
        for i in range(100000):
            c=random.randint(0,7)
            dx=h[c]
            dy=m[c]
            if locationss.size==2:
                location1=np.array([locationss[0]+dx,locationss[1]+dy])
                if not 0<=location1[0]<squareSize or not 0<=location1[1]<squareSize :
                    continue#游走在一定区域进行
                if matrix[location1[1]][location1[0]]== 1:
                    continue#游走不能出现粒子重复
                locationss=np.array([locationss[0]+dx,locationss[1]+dy])
                break
            else:
                y=0
                for j in range(locationss.shape[0]):
                    location0=[locationss[j,0]+dx,locationss[j,1]+dy]
                    if not 0<=location0[0]<squareSize or not 0<=location0[1]<squareSize :
                        continue#游走在一定区域进行
                    if matrix[location0[1]][location0[0]]!= 1:
                        y+=1#游走不能出现粒子重复，对于多粒子团体不能出现一个粒子的重复现象
                if y==locationss.shape[0]:
                    locationss[:,0]+=dx
                    locationss[:,1]+=dy
                    break
    all_location[int(rans)]=locationss
    pd=[]
    
    k=False
  
    if not nearEdge and not foundFriend and locationss.size==2:#团簇聚集计算#单粒子情况
        for i in range(NN):
            if i ==rans:
                continue
            else:
                c=all_location[i]
                if c.size==2:
                    if np.abs(locationss[0]-c[0])<=1 and np.abs(locationss[1]-c[1])<=1:#定义部分聚集发生在8个位置
                        k=True
                else:
                    for j in range(c.shape[0]):#针对多粒子情况
                        if np.abs(locationss[0]-c[j,0])<=1 and np.abs(locationss[1]-c[j,1])<=1:
                            k=True
                            break
                if k:
                    pd.append(i)
                    k=False
               
    if not nearEdge and not foundFriend and locationss.size!=2:#多粒子情况
        for w in range(locationss.shape[0]):
            locationss1=locationss[w,:]
            for i in range(NN):
                if i ==rans:
                    continue
                else:
                    c=all_location[i]
                    if c.size==2:
                        if np.abs(locationss1[0]-c[0])<=1 and np.abs(locationss1[1]-c[1])<=1:#定义聚集为在整个团簇的8个位置
                            k=True
                    else:
                        for j in range(c.shape[0]):#针对多粒子情况判断是否聚集
                            if np.abs(locationss1[0]-c[j,0])<=1 and np.abs(locationss1[1]-c[j,1])==1:
                                k=True
                                break
                if k:
                    pd.append(i)
                    k=False
    pd =sorted(set(pd), key = pd.index)
    if len(pd)!=0:
        for j in pd:
            all_location[int(rans)]=np.vstack((all_location[int(rans)],all_location[j]))
    if nearEdge:
        pd.append(rans)

    return (all_location,foundFriend, nearEdge, exitCircle,pd)


def randomAtRadius(radius, seedX, seedY):#产生随机一个粒子
    theta = 2*np.pi*random.random() 
    x=int(radius*np.cos(theta))+seedX 
    y=int(radius*np.sin(theta))+seedY 
    location=[x, y]
    return location


def DLAcluster(NN,radius):#NN代表同时释放的粒子数，粒子数越多代表浓度越高，1为DLA
    if not os.path.isdir("images"):#如果没有对应路径就创建
        os.mkdir("images")

    needGif=True
    seedX = radius+2 
    seedY = radius+2 
    squareSize = radius*2
    matrix=np.zeros((squareSize, squareSize))
    for row in range (0,squareSize):
        for col in range (0,squareSize):
            if np.sqrt((seedX-col)**2+(seedY-row)**2)<1: 
                matrix[row][col]=1
          
            elif np.sqrt((seedX-col)**2+(seedY-row)**2)>radius:
                matrix[row][col]=2
    

 
    randomWalkersCount = 0


    completeCluster = False
    xx=[seedX]
    yy=[seedY]
   
 
    addedCount=0 
    
    usedInterval=[]
    all_location=[]
    location=np.array(randomAtRadius(radius, seedX, seedY))
    all_location.append(location)
    
    for i in range(10000):
        location=np.array(randomAtRadius(radius, seedX, seedY))
        pp=True
        for k in range(len(all_location)):
            if  (location==all_location[k]).all():
                pp=False
        if pp:
            all_location.append(location)
        if len(all_location)==NN:
            break
    colors1 = '#EE82EE'
    colors2 = '#800000'
    while not completeCluster:
        
        random.seed()
        foundFriend = False
        nearEdge=False 
        
        while not foundFriend and not nearEdge:
            randomWalkersCount += 1
            tt=len(all_location)
            if tt<NN:
                for i in range(NN-tt):
                    for j in range(10000):
                        location=np.array(randomAtRadius(radius, seedX, seedY))
                        pp=True
                        for k in range(tt):
                            if all_location[k].size==2 and (location==all_location[k]).all():
                                pp=False
                            if all_location[k].size!=2:
                                for w in range(all_location[k].shape[0]):
                                    c=all_location[k]
                                    if (location==c[w,:]).all():
                                        pp=False
                        if pp:
                            all_location.append(location)
                            break
            rans=random.randint(0,NN-1)
            all_locationNew,foundFriend, nearEdge, exitCircle,pd = checkAround(NN,rans,all_location,squareSize,matrix)
            if foundFriend:
                c=all_locationNew[rans]
                if c.size==2:
                    matrix[c[1]][c[0]] = 1
                    xx.append(c[0])
                    yy.append(c[1])
                   
                    addedCount+=1
                else:
                    for j in range(c.shape[0]):
                        matrix[c[j,1]][c[j,0]] = 1
                        xx.append(c[j,0])
                        yy.append(c[j,1])
                        
                        addedCount+=1
                location=randomAtRadius(radius, seedX, seedY)
                all_location[rans]=(np.array(location))
            else:
                all_location = [all_locationNew[i] for i in range(0,len(all_locationNew)) if i not in pd]
            
            intervalSavePic=range(2,400000,500)
            if needGif:
                if randomWalkersCount in intervalSavePic:#每隔几张图保存图像
                    print("save picture")
                    usedInterval.append(randomWalkersCount) 
                    label=str(randomWalkersCount)
                    plt.title("DLA Cluster", fontsize=20)
                    all_locationx=[]#保存所有x,y坐标
                    all_locationy=[]
                    
                    for i in range(len(all_location)) :
                        k=all_location[i]
                        if k.size==2:
                            all_locationx.append(k[0])
                            all_locationy.append(k[1])
                            
                            
                        else:
                           for j in range(k.shape[0]):
                               all_locationx.append(k[j,0])
                               all_locationy.append(k[j,1])
                               
            
                    plt.scatter(xx, yy, c=colors1,s=30)#绘制游走得粒子
                    plt.scatter(all_locationx,all_locationy,c=colors2,s=30)#绘制团簇中得粒子
                    plt.xticks([])
                    plt.yticks([])
                    plt.xlim(seedX-radius,seedX+radius)
                    plt.ylim(seedY-radius,seedY+radius)
                    plt.savefig("images/cluster{}.png".format(label), dpi=200)
                    plt.close()
       
        if randomWalkersCount==400000:
            print("CAUTION: had to break the cycle, taking too many iterations")
            completeCluster = True

        if foundFriend and exitCircle:
            print("Random walkers in the cluster: ",addedCount)
            completeCluster = True
    
    plt.scatter(xx,yy,c=colors1,s=30)
    plt.xticks([])
    plt.yticks([])
    plt.xlim(seedX-radius,seedX+radius)
    plt.ylim(seedY-radius,seedY+radius)
    plt.savefig("images/cluster.png", dpi=200)


    if needGif:
        with imageio.get_writer('images/movie.gif', mode='I') as writer:
            for i in usedInterval:
                filename="images/cluster"+str(i)+".png"
                image = imageio.imread(filename)#将图片生成动画
                writer.append_data(image)
                os.remove(filename)#删除原图片
            filename="images/cluster.png"
            image = imageio.imread(filename)
            writer.append_data(image)#将最终得到图像也生成动画
    return addedCount, matrix
mass,matrix=DLAcluster(5,30)