# -*- coding: utf-8 -*-
"""
Created on Thu May  7 17:04:20 2020

@author: Lenovo
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import os
import imageio

Temp = 1.0
sigma = 0.1
kesai = 1#可以调整的可变参数，用于改变力的表达式，分别取0，1，2，3进行模拟
def checkAround(R,locationNew,squareSize,location_all_x,location_all_y,addedCount):#函数用于检验每一步游走后是否落在凝聚体上
    foundFriend=False
    nearEdge=False
    locationNew1=np.zeros((2))
    for i in range(2):#先检验是否在边缘
        p=locationNew[i]
        if abs(p)>2.5*squareSize:
            nearEdge=True
    if not nearEdge:
        x=locationNew[0]
        y=locationNew[1]
        rr=np.sqrt(x*x+y*y)
        if rr>R+1.00001:#判断是否临近已形成的集团，以1为临界距离，小于该距离则结合
            foundFriend=False
        else:
            for i in range(addedCount):
                if np.sqrt((location_all_x[i]-x)**2+(location_all_y[i]-y)**2)<=1:
                    foundFriend=True
    if not nearEdge and not foundFriend:#若既不在边缘又未结合，计算粒子此刻受力并按照郎之万方程进行动力学模拟
        h = 0.01/np.sqrt(R*addedCount)#每一步时间步长反比于当前最大半径R与已结合粒子数的乘积的平方根，防止每步位移过大跳过已结合粒子
        location_all_x1=np.array(location_all_x)
        location_all_y1=np.array(location_all_y)
        dx = -(x - location_all_x1)
        dy = -(y - location_all_y1)
        r2 = 1/np.sqrt(dx**2 + dy**2)**(1+kesai)#kesai参数已给定，用于调整幂次相互作用的形式
        fx = dx.dot(r2)#x方向受力
        fy = dy.dot(r2)#y方向受力
        locationNew1=[locationNew[0]+fx*h+10**(-4)*np.sqrt(2*Temp/sigma/h)*h*random.gauss(0,1),\
                      locationNew[1]+fy*h+10**(-4)*np.sqrt(2*Temp/sigma/h)*h*random.gauss(0,1)]#小雷诺数情形郎之万方程写成有限差分形式，并引入与时间步长相关随机游走
    return (locationNew1,foundFriend, nearEdge)

def randomAtRadius(R,addedCount):
    theta = 2*np.pi*random.random() 
    x=R*np.cos(theta) 
    y=R*np.sin(theta) 
    vx=random.gauss(0,1)
    vy=random.gauss(0,1)
    h=0.01/np.sqrt(R*addedCount)
    location1=[x+vx*h,y+vy*h]
    return location1#在R处产生随机分布的位置，并具有一定初速度

def DLAcluster(radius):#radius表示模拟的半径范围
    needGif=True
    if not os.path.isdir("images"):#如果没有对应路径就创建
        os.mkdir("images")
    rradius=[0]
    random.seed(None)
    seedX = 0
    seedY = 0
    squareSize = radius*5
    location_all_x=[seedX]
    location_all_y=[seedY]
    usedInterval=[]
    randomWalkersCount = 0
    completeCluster = False
    addedCount=1
    R=0.5
    c = 0
    intervalSavePic=range(2,4000000,500)
    while not completeCluster:
        
        random.seed()
        locationNew=randomAtRadius(R*1.5,addedCount)
        foundFriend = False 
        nearEdge=False 
        while not foundFriend and not nearEdge:#如果未结合且未走出边界，按照checkAround函数给定的规则不断游走
            randomWalkersCount += 1
            locationNew_temp,foundFriend, nearEdge = checkAround(R,locationNew,squareSize,location_all_x,location_all_y,addedCount)
            if foundFriend:#结合后，保存粒子位置
                location_all_x.append(locationNew[0])
                location_all_y.append(locationNew[1])
                addedCount+=1
                c=0.5+np.sqrt((locationNew[0])**2+(locationNew[1])**2)
                R=np.max([R,c])
                if c>np.max(rradius):
                    rradius.append(c)#最大半径产生变化，记录最大半径，产生半径序列
            else:#若未结合，以当前位置为起点，继续游走
                locationNew = locationNew_temp
           
            if randomWalkersCount in intervalSavePic:
                print("save picture")
                usedInterval.append(randomWalkersCount) 
                label=str(randomWalkersCount)
                plt.title("DLA Cluster", fontsize=20)
                plt.plot(locationNew[0],locationNew[1],'ro',ms=10)#绘制运动点
                plt.plot(location_all_x,location_all_y,'bo',ms=10)#绘制已经结合的团簇点
                plt.ylim(-radius*1.5-1,radius*1.5+1)
                plt.xlim(-radius*1.5-1,radius*1.5+1)
                plt.savefig("images/cluster{}.png".format(label), dpi=100)#保存图像
                plt.close()
            
        if randomWalkersCount==400000:#若粒子数达到一定数量，终止该凝聚体的模拟（通常不会发生）
            print("CAUTION: had to break the cycle, taking too many iterations")
            completeCluster = True

        if foundFriend and R>radius:#达到给定的模拟范围，结束模拟并显示凝聚体的现有粒子数
            print("Random walkers in the cluster: ",addedCount)
            completeCluster = True
    plt.title("DLA Cluster", fontsize=20)
    plt.plot(location_all_x,location_all_y,'bo',ms=10)
    plt.ylim(-radius*1.5-1,radius*1.5+1)
    plt.xlim(-radius*1.5-1,radius*1.5+1)
    plt.savefig("images/cluster.png", dpi=100)
    plt.close()
    if needGif:
        with imageio.get_writer('images/movie.gif', mode='I') as writer:
            for i in usedInterval:
                filename="images/cluster"+str(i)+".png"
                image = imageio.imread(filename)#将之前的图像生成动画
                writer.append_data(image)
                os.remove(filename)#除去原来的图像
            filename="images/cluster.png"
            image = imageio.imread(filename)
            writer.append_data(image)
DLAcluster(10)


 