

import numpy as np
import random
import pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import imageio

def checkaround_all(NN,all_location,all_location_v):
    delete=[]            
    for zzz in range(NN-1):
        locationss=all_location[zzz]
        pd=[]
        if zzz not in delete:
            k=False
            if locationss.size==3:
                for i in range(0,NN):
                    if i==zzz:
                        continue
                    if i not in delete:
                        c=all_location[i]
                        if c.size==3:
                            if (locationss[0]-c[0])**2+(locationss[1]-c[1])**2+(locationss[2]-c[2])**2<=1:
                                k=True 
                        else:
                            for j in range(c.shape[0]):
                                if (locationss[0]-c[j,0])**2+(locationss[1]-c[j,1])**2+(locationss[2]-c[j,2])**2<=1 :
                                    k=True
                                    break
                        if k:
                            pd.append(i)
                            delete.append(i)
                            k=False
                       
            if locationss.size!=3:
                for w in range(locationss.shape[0]):
                    locationss1=locationss[w,:]
                    for i in range(0,NN):
                        if i in pd:
                            continue
                        if i==zzz:
                            continue
                        if i not in delete:                        
                            c=all_location[i]
                            if c.size==3:
                                if (locationss1[0]-c[0])**2+(locationss1[1]-c[1])**2+(locationss1[2]-c[2])**2<=1:
                                    k=True
                            else:
                                for j in range(c.shape[0]):
                                    if (locationss1[0]-c[j,0])**2+(locationss1[1]-c[j,1])**2+(locationss1[2]-c[j,2])**2<=1:
                                        k=True
                                        break
                            if k:
                                pd.append(i)
                                delete.append(i)
                                k=False
                            
            pd =sorted(set(pd), key = pd.index)
            if len(pd)!=0:
                for j in pd:
                    all_location[zzz]=np.vstack((all_location[zzz],all_location[j]))
                    m1=all_location[zzz].size
                    m2=all_location[j].size
                    v1=np.array(all_location_v[zzz])
                    v2=np.array(all_location_v[j])
                    all_location_v[zzz]=(m1*v1+m2*v2)/(m1+m2)
 
    t=len(all_location)
    all_location = [all_location[i] for i in range(0,t) if i not in delete]
    all_location_v = [all_location_v[i] for i in range(0,t) if i not in delete]
    return (all_location,all_location_v)

def calculate_F(num,all_location,NN):
    F=np.zeros((num,3),dtype=np.float16)
    for i in range(0,num-1):
        for j in range(i+1,num):
            if all_location[j].size>3:
                if all_location[i].size==3:
                    dx=all_location[i][0]-all_location[j][:,0]
                    dy=all_location[i][1]-all_location[j][:,1]
                    dz=all_location[i][2]-all_location[j][:,2]
                    r=1/(dx**2+dy**2+dz**2)
                    fx=dx.dot(r)#x方向受力
                    fy=dy.dot(r)#y方向受力
                    fz=dz.dot(r)
                    F[i,0]-=fx
                    F[i,1]-=fy
                    F[i,2]-=fz
                    F[j,0]+=fx
                    F[j,1]+=fy
                    F[j,2]+=fz
                else:
                    for k in range(all_location[i].shape[0]):
                        dx=all_location[i][k,0]-all_location[j][:,0]
                        dy=all_location[i][k,1]-all_location[j][:,1]
                        dz=all_location[i][k,2]-all_location[j][:,2]
                        r=1/(dx**2+dy**2+dz**2)
                        fx=dx.dot(r)#x方向受力
                        fy=dy.dot(r)#y方向受力
                        fz=dz.dot(r)
                        F[i,0]-=fx
                        F[i,1]-=fy
                        F[i,2]-=fz
                        F[j,0]+=fx
                        F[j,1]+=fy
                        F[j,2]+=fz
            else:
                if all_location[i].size==3:
                    dx=all_location[i][0]-all_location[j][0]
                    dy=all_location[i][1]-all_location[j][1]
                    dz=all_location[i][2]-all_location[j][2]
                    r=1/(dx**2+dy**2+dz**2)
                    fx=dx*r#x方向受力
                    fy=dy*r#y方向受力
                    fz=dz*r
                    F[i,0]-=fx
                    F[i,1]-=fy
                    F[i,2]-=fz
                    F[j,0]+=fx
                    F[j,1]+=fy
                    F[j,2]+=fz
                else:
                    dx=all_location[i][:,0]-all_location[j][0]
                    dy=all_location[i][:,1]-all_location[j][1]
                    dz=all_location[i][:,2]-all_location[j][2]
                    r=1/(dx**2+dy**2+dz**2)
                    fx=dx.dot(r)#x方向受力
                    fy=dy.dot(r)#y方向受力
                    fz=dz.dot(r)
                    F[i,0]-=fx
                    F[i,1]-=fy
                    F[i,2]-=fz
                    F[j,0]+=fx
                    F[j,1]+=fy
                    F[j,2]+=fz   
  #  F+=np.random.normal(size=(num,3))*0.01*(NN)**(1/4) #随机力(与1/sqrt(dt)正比)
    return F
        
def wander(num,all_location,all_location_v,radius,NN,F1,num_old):
    h=1/np.sqrt(NN)*0.1
    if num!=num_old:
        F1=calculate_F(num,all_location,NN)

    for k in range(0,num):
        m=all_location[k].size
        if m==3:
            all_location[k][:]+=all_location_v[k][:]*h+2/3*F1[k,0]/m*h*h#更新位置  
        else:
            all_location[k][:,:]+=all_location_v[k][:]*h+2/3*F1[k,:]/m*h*h#更新位置   
          
    F2=calculate_F(num,all_location,NN)
    for k in range(0,num):
        m=all_location[k].size
        if m==3:
            all_location_v[k][:]+=2/3*(F1[k,:]+F2[k,:])/m*h
        else:
            all_location_v[k][:]+=2/3*(F1[k,:]+F2[k,:])/m*h       
    
    return all_location,all_location_v,F2


def randomAtRadius(radius):
    theta=2*np.pi*random.random()
    fai=np.pi*random.random()
    r=random.random()*radius
    x=np.sin(theta)*r*np.sin(fai)
    y=np.cos(theta)*r*np.sin(fai)
    z=np.cos(fai)*r
    location=np.array([x, y,z]) #save locaction
    location_v=np.zeros((3))
    return location,location_v


def DLAcluster(NN,radius):#NN代表同时释放的粒子数，粒子数越多代表浓度越高，1为DLA
    if not os.path.isdir("images"):#如果没有对应路径就创建
        os.mkdir("images") 
    random.seed(None)
    all_location=[]
    all_location_v=[]
    usedInterval=[]
    location,location_v=randomAtRadius(radius)
    all_location.append(location)
    all_location_v.append(location_v)
    randomWalkersCount = 0
    num=1
    for i in range(100000):
        location,location_v=randomAtRadius(radius)
        pp=True
        for k in range(num):
            if  (location==all_location[k]).all():
                pp=False
        if pp:
            all_location.append(location)
            all_location_v.append(location_v)
            num+=1
        if num==NN:
            break
    all_x=[]
    all_y=[]
    all_z=[]
    num_old=NN
    intervalSavePic=range(2,4000000,10)
    F=calculate_F(num,all_location,NN) 
    while num>1:
        randomWalkersCount += 1
        all_location,all_location_v=checkaround_all(num,all_location,all_location_v)
        num=len(all_location)
        all_location,all_location_v,F=wander(num,all_location,all_location_v,radius,NN,F,num_old)
        num_old=num
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
                       
            ax.plot(all_locationx,all_locationy,all_locationz,'bo',ms=5)#绘制所有的点
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_zticks([])
            horiAngle=45+randomWalkersCount*1/10#调节图像的旋转角度以观察三维效果
            vertAngle=50+randomWalkersCount*1/10
            ax.view_init(vertAngle,horiAngle)
            ax.set_xlim(-radius-1,1+radius)
            ax.set_ylim(-radius-1,1+radius)
            ax.set_zlim(-radius-1,1+radius)
            plt.savefig("images/cluster{}.png".format(label), dpi=200)#储存图像以供绘图
            plt.close()
    for ww in range(NN):
        all_x.append(all_location[0][ww,0])
        all_y.append(all_location[0][ww,1])
        all_z.append(all_location[0][ww,2])
    fig=plt.figure()
    ax = Axes3D(fig)
    ax.plot(all_x,all_y,all_z,'bo',ms=5)#绘制最终图像
    ax.set_xticks([])#隐藏图像的x坐标轴的标签
    ax.set_yticks([])#隐藏图像的y坐标轴的标签
    ax.set_zticks([])#隐藏图像的z坐标轴的标签
    ax.set_xlim(-radius-1,1+radius)
    ax.set_ylim(-radius-1,1+radius)
    ax.set_zlim(-radius-1,1+radius)
    plt.savefig("images/cluster.png", dpi=200)
    plt.close()
    with imageio.get_writer('images/movie.gif', mode='I') as writer:
        for i in usedInterval:
            filename="images/cluster"+str(i)+".png"
            image = imageio.imread(filename)#将图像绘制成动画
            writer.append_data(image)
            os.remove(filename)#删除已经绘制的图像
DLAcluster(300,15)