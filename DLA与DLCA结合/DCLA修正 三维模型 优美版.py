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

h=[0,1,0,-1,0,0,-1,1,-1,1,0,0,0,0,1,1,-1,-1,1,1,1,1,-1,-1,-1,-1]
m=[1,0,-1,0,0,0,-1,1,1,-1,1,1,-1,-1,0,0,0,0,1,1,-1,-1,1,1,-1,-1]
g=[0,0,0,0,1,-1,0,0,0,0,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1]
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
        if locationss.size==3:#单粒子
            for k in range(26):#在26个方向上判断粒子是否可能相邻或达到边界
                neighbors=matrix[locationss[2]+g[k],locationss[1]+h[k],locationss[0]+m[k]]            
                if neighbors==1 :#此时代表有粒子相邻
                    foundFriend=True
                if neighbors==2:#此时代表可能生长大小达到要求
                    exitCircle=True
        else:
            for j in range(locationss.shape[0]):#多粒子
                location0=locationss[j,:]
                for k in range(26):
                    neighbors=matrix[location0[2]+g[k],location0[1]+h[k],location0[0]+m[k]]           
                    if neighbors==1 :
                        foundFriend=True#此时代表有粒子相邻
                    if neighbors==2:
                        exitCircle=True
    if not nearEdge and not foundFriend:
        for i in range(100000):
            c=random.randint(0,25)#向26个方向游走
            dx=h[c]
            dy=m[c]
            dz=g[c]
            if locationss.size==3:
                location1=np.array([locationss[0]+dx,locationss[1]+dy,locationss[2]+dz])
                if not 0<=location1[0]<squareSize or not 0<=location1[1]<squareSize or not 0<=location1[2]<squareSize :
                    continue#游走在一定区域进行
                if matrix[location1[2]][location1[1]][location1[0]]== 1:
                    continue#游走不能出现粒子重复
                locationss=np.array([locationss[0]+dx,locationss[1]+dy,locationss[2]+dz])
                break
            else:
                y=0
                for j in range(locationss.shape[0]):
                    location0=[locationss[j,0]+dx,locationss[j,1]+dy,locationss[j,2]+dz]
                    if not 0<=location0[0]<squareSize or not 0<=location0[1]<squareSize or not 0<=location0[2]<squareSize :
                        continue#游走在一定区域进行
                    if matrix[location0[2]][location0[1]][location0[0]]!= 1:
                        y+=1#游走不能出现粒子重复
                if y==locationss.shape[0]:
                    locationss[:,0]+=dx
                    locationss[:,1]+=dy
                    locationss[:,2]+=dz
                    break
    all_location[int(rans)]=locationss
    pd=[]
    k=False
    if not nearEdge and not foundFriend and locationss.size==3:#团簇聚集计算#单粒子情况
        for i in range(NN):
            if i ==rans:
                continue
            else:
                c=all_location[i]
                if c.size==3:#如果被聚集粒子为单粒子
                    if np.abs(locationss[0]-c[0])<=1 and np.abs(locationss[1]-c[1])<=1 and np.abs(locationss[2]-c[2])<=1:
                        k=True#针对26个位置，如果出现附近有粒子则判断为聚集
                else:#如果被聚集粒子为多粒子
                    for j in range(c.shape[0]):
                        if np.abs(locationss[0]-c[j,0])<=1 and np.abs(locationss[1]-c[j,1])<=1 and np.abs(locationss[2]-c[j,2])<=1:
                            k=True#针对26个位置，如果出现附近有粒子则判断为聚集
                if k:
                    pd.append(i)
                    k=False
    if not nearEdge and not foundFriend and locationss.size!=3:#团簇聚集计算#多粒子情况
        for w in range(locationss.shape[0]):
            locationss1=locationss[w,:]
            for i in range(NN):
                if i ==rans:
                    continue
                else:
                    c=all_location[i]
                    if c.size==3:#如果被聚集粒子为单粒子
                        if np.abs(locationss1[0]-c[0])<=1 and np.abs(locationss1[1]-c[1])<=1 and np.abs(locationss1[2]-c[2])<=1:
                            k=True#针对26个位置，如果出现附近有粒子则判断为聚集
                    else:#如果被聚集粒子为多粒子
                        for j in range(c.shape[0]):
                            if np.abs(locationss1[0]-c[j,0])<=1 and np.abs(locationss1[1]-c[j,1])<=1 and np.abs(locationss1[2]-c[j,2])<=1:
                                k=True#针对26个位置，如果出现附近有粒子则判断为聚集
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



def randomAtRadius(radius, seedX, seedY,seedZ):#随机在球面释放单个粒子
    theta = 2*np.pi*random.random() 
    csi=np.pi*random.random()
    x=int(radius*np.cos(theta)*np.sin(csi))+seedX 
    y=int(radius*np.sin(theta)*np.sin(csi))+seedY 
    z=int(radius*np.cos(csi))+seedZ
    location=[x, y,z]
    return location


def DLAcluster(NN,radius):#NN代表同时释放的粒子数，粒子数越多代表浓度越高，1为DLA
    if not os.path.isdir("images"):#如果没有对应路径就创建
        os.mkdir("images")

    squareSize = radius*2+5
    xx=[]
    yy=[]
    zzz=[]
    matrix=np.zeros((squareSize, squareSize,squareSize))
    seedX = radius+2 
    seedY = radius+2 
    seedZ = radius+2
    squareSize = radius*2+5

    for row in range (0,squareSize):
        for col in range (0,squareSize):
            for zz in range (0,squareSize):
                if np.sqrt((seedX-col)**2+(seedY-row)**2+(seedZ-zz)**2)==0: 
                    matrix[zz][row][col]=1
                    xx.append(row)
                    yy.append(col)
                    zzz.append(zz)
                elif np.sqrt((seedX-col)**2+(seedY-row)**2+(seedZ-zz)**2)>=radius:
                    matrix[zz][row][col]=2


    randomWalkersCount = 0

    # Set the cluster to NOT be complete
    completeCluster = False

    # Start running random walkers
    addedCount=0 #keep track of number added

    # initialize array for the used interval for graphing
    usedInterval=[]
    all_location=[]
    location=np.array(randomAtRadius(radius, seedX, seedY,seedZ))
    all_location.append(location)
    
    for i in range(10000):
        location=np.array(randomAtRadius(radius, seedX, seedY,seedZ))
        pp=True
        for k in range(len(all_location)):
            if  (location==all_location[k]).all():
                pp=False
        if pp:
            all_location.append(location)
        if len(all_location)==NN:
            break
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
                        location=np.array(randomAtRadius(radius, seedX, seedY,seedZ))
                        pp=True
                        for k in range(tt):
                            if all_location[k].size==3 and (location==all_location[k]).all():
                                pp=False
                            if all_location[k].size!=3:
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
                if c.size==3:
                    matrix[c[2]][c[1]][c[0]] = 1
                    xx.append(c[0])
                    yy.append(c[1])
                    zzz.append(c[2])
                    addedCount+=1
                else:
                    for j in range(c.shape[0]):
                        matrix[c[j,2]][c[j,1]][c[j,0]] = 1
                        xx.append(c[j,0])
                        yy.append(c[j,1])
                        zzz.append(c[j,2])
                        addedCount+=1
                location=randomAtRadius(radius, seedX, seedY,seedZ)
                all_location[rans]=(np.array(location))
            else:
                all_location = [all_locationNew[i] for i in range(0,len(all_locationNew)) if i not in pd]
            intervalSavePic=range(2,60000000,50)
            if randomWalkersCount in intervalSavePic:#间隔一段保存图片
                print("save picture")
                usedInterval.append(randomWalkersCount)
                label=str(randomWalkersCount)
                colors1 = '#8A2BE2'
                colors2 = '#FFD700'#绘图颜色
                fig = plt.figure()
                ax = Axes3D(fig)
                all_locationx=[]
                all_locationy=[]
                all_locationz=[]
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
                        
                ax.scatter(xx, yy, zzz,c=colors1,s=150)#绘制运动的点
                ax.scatter(all_locationx,all_locationy,all_locationz,c=colors2,s=150)#绘制所有结合的点
                horiAngle=45+randomWalkersCount/100*2
                vertAngle=50+randomWalkersCount/100*2#调整图像视角
                ax.view_init(vertAngle,horiAngle)
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_zticks([])
                ax.set_xlim(2,squareSize-2)
                ax.set_ylim(2,squareSize-2)
                ax.set_zlim(2,squareSize-2)
                plt.savefig("images/cluster{}.png".format(label), dpi=200)#保存图片
                plt.close()
       
        if randomWalkersCount==60000000:
            print("CAUTION: had to break the cycle, taking too many iterations")
            completeCluster = True

        if foundFriend and exitCircle:
            print("Random walkers in the cluster: ",addedCount)
            completeCluster = True
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(xx, yy, zzz,c=colors1,s=150)#绘制最终图像
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
            filename="images/cluster"+str(i)+".png"
            image = imageio.imread(filename)#将已经绘制的图像生成动画
            writer.append_data(image)
            os.remove(filename)#删除已经绘制成动画的图片
        filename="images/cluster.png"
        image = imageio.imread(filename)
        writer.append_data(image)#将最终的图片加入动画
    return addedCount, matrix
mass,matrix=DLAcluster(10,13)