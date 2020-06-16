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
from mpl_toolkits.mplot3d import Axes3D

kesai =2#可以调整的可变参数，用于改变力的表达式，分别取2，3，5进行模拟
Temp = 1.0#控温参数
sigma = 0.1#粘滞力系数
def checkAround(R,locationNew,squareSize,location_all_x,location_all_y,location_all_z,addedCount):#函数用于检验每一步游走后是否落在凝聚体上
    foundFriend=False
    nearEdge=False
    locationNew1=np.zeros((2))
    for i in range(3):#先检验是否在边缘
        p=locationNew[i]
        if abs(p)>0.5*squareSize:
            nearEdge=True
    if not nearEdge:
        x=locationNew[0]
        y=locationNew[1]
        z=locationNew[2]
        rr=np.sqrt(x*x+y*y+z*z)
        if rr>R+1.00001:#判断是否临近已形成的集团，以1为临界距离，小于该距离则结合
            foundFriend=False
        else:
            for i in range(addedCount):
                if np.sqrt((location_all_x[i]-x)**2+(location_all_y[i]-y)**2+(location_all_z[i]-z)**2)<=1:
                    foundFriend=True
    if not nearEdge and not foundFriend:#若既不在边缘又未结合，计算粒子此刻受力并按照verlet算法进行动力学模拟
        h = 0.1/np.sqrt(R*addedCount)#每一步时间步长反比于当前最大半径R与已结合粒子数的乘积的平方根，防止每步位移过大跳过已结合粒子
        location_all_x1=np.array(location_all_x)
        location_all_y1=np.array(location_all_y)
        location_all_z1=np.array(location_all_z)
        dx = -(x - location_all_x1)
        dy = -(y - location_all_y1)
        dz = -(z - location_all_z1)
        r2 = 1/np.sqrt(dx**2 + dy**2 + dz**2)**(1+kesai)#kesai参数已给定，用于调整幂次相互作用的形式
        fx = dx.dot(r2)#x方向受力
        fy = dy.dot(r2)#y方向受力
        fz = dz.dot(r2)#z方向受力
        locationNew1=[locationNew[0]+fx*h+10**(-4)*np.sqrt(2*Temp/sigma/h)*h*random.gauss(0,1),\
                      locationNew[1]+fy*h+10**(-4)*np.sqrt(2*Temp/sigma/h)*h*random.gauss(0,1),\
                      locationNew[2]+fz*h+10**(-4)*np.sqrt(2*Temp/sigma/h)*h*random.gauss(0,1)]#verlet算法，并引入与时间步长相关随机游走
    return (locationNew1,foundFriend, nearEdge)

def randomAtRadius(R,addedCount):
    theta = 2*np.pi*random.random()
    fai=np.pi*random.random()
    z=R*np.sin(theta)*np.cos(fai)
    x=R*np.sin(theta)*np.sin(fai)
    y=R*np.cos(theta)
    location1=[x,y,z]
    return location1#在R处产生随机分布的位置，并具有一定初速度

def DLAcluster(radius):
    if not os.path.isdir("images"):#如果没有对应路径就创建
        os.mkdir("images")
    random.seed(None)
    needGif=True

    squareSize = radius*5
    location_all_x=np.array([0],dtype=np.float32)
    location_all_y=np.array([0],dtype=np.float32)
    location_all_z=np.array([0],dtype=np.float32)
    randomWalkersCount = 0
    completeCluster = False
    addedCount=1
    usedInterval=[]
    R=0.5
    while not completeCluster:
        
        random.seed()
        locationNew=randomAtRadius(R*1.5,addedCount)
        foundFriend = False 
        nearEdge=False 
        while not foundFriend and not nearEdge:
            locationNew_temp,foundFriend, nearEdge = checkAround(R,locationNew,squareSize,location_all_x,location_all_y,location_all_z,addedCount)
            randomWalkersCount += 1
            if foundFriend:
                location_all_x=np.hstack((location_all_x,locationNew[0]))
                location_all_y=np.hstack((location_all_y,locationNew[1]))
                location_all_z=np.hstack((location_all_z,locationNew[2]))
                addedCount+=1
                R=np.max([np.sqrt((locationNew[0])**2+(locationNew[1])**2+(locationNew[2])**2),R])
            else:
                locationNew = locationNew_temp

        
            intervalSavePic=range(2,40000000,50)
            if needGif:
                if randomWalkersCount in intervalSavePic:
                    print("save picture")
                    usedInterval.append(randomWalkersCount) 
                    label=str(randomWalkersCount)
                    fig = plt.figure()
                    ax = Axes3D(fig)
                    colors1 = '#00CED1'
                    colors2 = '#FF0000'#画图使用颜色
                    horiAngle=45+randomWalkersCount/250*2#调节视角
                    vertAngle=50+randomWalkersCount/250*2
                    ax.view_init(vertAngle,horiAngle)
                    ax.set_xticks([])#消除坐标的tick
                    ax.set_yticks([])
                    ax.set_zticks([])
                    ax.scatter(locationNew[0],locationNew[1],locationNew[2],c=colors2,s=100)#绘制运动的点
                    ax.scatter(location_all_x, location_all_y, location_all_z,c=colors1,s=100)#绘制粒子团簇的点
                    
                    ax.set_ylim(-1.5*radius-1,1.5*radius+1)
                    ax.set_xlim(-1.5*radius-1,1.5*radius+1)
                    ax.set_zlim(-1.5*radius-1,1.5*radius+1)
                    plt.savefig("images/cluster{}.png".format(label), dpi=200)
                    plt.close()
       
        if randomWalkersCount==40000000:
            print("CAUTION: had to break the cycle, taking too many iterations")
            completeCluster = True

        if foundFriend and R>radius:
            print("Random walkers in the cluster: ",addedCount)
            completeCluster = True

    fig = plt.figure()
    ax = Axes3D(fig)

    horiAngle=45+randomWalkersCount/250*2
    vertAngle=50+randomWalkersCount/250*2
    ax.view_init(vertAngle,horiAngle)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.scatter(location_all_x, location_all_y, location_all_z,c=colors1,s=100)#最终图像绘制所以团簇的点
    ax.set_ylim(-1.5*radius-1,1.5*radius+1)
    ax.set_xlim(-1.5*radius-1,1.5*radius+1)
    ax.set_zlim(-1.5*radius-1,1.5*radius+1)
    plt.savefig("images/cluster.png", dpi=200)
    plt.close()
    if needGif:
        with imageio.get_writer('images/movie.gif', mode='I') as writer:
            for i in usedInterval:
                filename="images/cluster"+str(i)+".png"#保存图片的名称
                image = imageio.imread(filename)#将图片制作动画
                writer.append_data(image)
                os.remove(filename)#删除该图片
            filename="images/cluster.png"
            image = imageio.imread(filename)
            writer.append_data(image)
    return addedCount, location_all_x,location_all_y
DLAcluster(5)


 