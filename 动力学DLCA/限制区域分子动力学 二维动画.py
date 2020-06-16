

import numpy as np
import random
import pylab as plt
import os
import imageio
def checkaround_all(NN,all_location,all_location_v):
    delete=[]            
    for zzz in range(NN-1):
        locationss=all_location[zzz]
        pd=[]
        if zzz not in delete:
            k=False
            if locationss.size==2:
                for i in range(0,NN):
                    if i==zzz:
                        continue
                    if i not in delete:
                        c=all_location[i]
                        if c.size==2:
                            if (locationss[0]-c[0])**2+(locationss[1]-c[1])**2<=1:
                                k=True 
                        else:
                            for j in range(c.shape[0]):
                                if (locationss[0]-c[j,0])**2+(locationss[1]-c[j,1])**2<=1 :
                                    k=True
                                    break
                        if k:
                            pd.append(i)
                            delete.append(i)
                            k=False
                       
            if locationss.size!=2:
                for w in range(locationss.shape[0]):
                    locationss1=locationss[w,:]
                    for i in range(0,NN):
                        if i in pd:
                            continue
                        if i==zzz:
                            continue
                        if i not in delete:                        
                            c=all_location[i]
                            if c.size==2:
                                if (locationss1[0]-c[0])**2+(locationss1[1]-c[1])**2<=1:
                                    k=True
                            else:
                                for j in range(c.shape[0]):
                                    if (locationss1[0]-c[j,0])**2+(locationss1[1]-c[j,1])**2<=1:
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
    F=np.zeros((num,2),dtype=np.float16)
    for i in range(0,num-1):
        for j in range(i+1,num):
            if all_location[j].size>2:
                if all_location[i].size==2:
                    dx=all_location[i][0]-all_location[j][:,0]
                    dy=all_location[i][1]-all_location[j][:,1]
                    r=1/(dx**2+dy**2)
                    fx=dx.dot(r)#x方向受力
                    fy=dy.dot(r)#y方向受力
                    F[i,0]-=fx
                    F[i,1]-=fy
                    F[j,0]+=fx
                    F[j,1]+=fy
                else:
                    for k in range(int(all_location[i].size/2)):
                        dx=all_location[i][k,0]-all_location[j][:,0]
                        dy=all_location[i][k,1]-all_location[j][:,1]
                        r=1/(dx**2+dy**2)
                        fx=dx.dot(r)#x方向受力
                        fy=dy.dot(r)#y方向受力
                        F[i,0]-=fx
                        F[i,1]-=fy
                        F[j,0]+=fx
                        F[j,1]+=fy
            else:
                if all_location[i].size==2:
                    dx=all_location[i][0]-all_location[j][0]
                    dy=all_location[i][1]-all_location[j][1]
                    r=1/(dx**2+dy**2)
                    fx=dx*r#x方向受力
                    fy=dy*r#y方向受力
                    F[i,0]-=fx
                    F[i,1]-=fy
                    F[j,0]+=fx
                    F[j,1]+=fy
                else:
                    dx=all_location[i][:,0]-all_location[j][0]
                    dy=all_location[i][:,1]-all_location[j][1]
                    r=1/(dx**2+dy**2)
                    fx=dx.dot(r)#x方向受力
                    fy=dy.dot(r)#y方向受力
                    F[i,0]-=fx
                    F[i,1]-=fy
                    F[j,0]+=fx
                    F[j,1]+=fy     
  #  F+=np.random.normal(size=(num,2))*0.01*(NN)**(1/4) #随机力(与1/sqrt(dt)正比)
    return F
        
def wander(num,all_location,all_location_v,radius,NN,F1,num_old):
    h=1/np.sqrt(NN)*0.1
    if num!=num_old:
        F1=calculate_F(num,all_location,NN)

    for k in range(0,num):
        m=all_location[k].size
        if m==2:
            all_location[k][:]+=all_location_v[k][:]*h+F1[k,0]/m*h*h#更新位置  
        else:
            all_location[k][:,:]+=all_location_v[k][:]*h+F1[k,:]/m*h*h#更新位置   
          
    F2=calculate_F(num,all_location,NN)
    for k in range(0,num):
        m=all_location[k].size
        if m==2:
            all_location_v[k][:]+=(F1[k,:]+F2[k,:])/m*h
        else:
            all_location_v[k][:]+=(F1[k,:]+F2[k,:])/m*h       
    
    return all_location,all_location_v,F2


def randomAtRadius(radius):
    theta=2*np.pi*random.random()
    r=random.random()*radius
    x=np.sin(theta)*r
    y=np.cos(theta)*r
    location=np.array([x, y]) #产生随机分布的位置
    location_v=np.zeros((2))
    return location,location_v


def DLAcluster(NN,radius):#NN代表同时释放的粒子数，粒子数越多代表浓度越高，1为DLA
    random.seed(None)
    all_location=[]
    all_location_v=[]
    location,location_v=randomAtRadius(radius)
    all_location.append(location)
    all_location_v.append(location_v)
    if not os.path.isdir("images"):#如果没有对应路径就创建
        os.mkdir("images")
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
    num_old=NN
    randomWalkersCount = 0
    intervalSavePic=range(2,400000,3)
    usedInterval=[]
    F=calculate_F(num,all_location,NN) 
    while num>1:
        randomWalkersCount += 1
        all_location,all_location_v=checkaround_all(num,all_location,all_location_v)
        num=len(all_location)
        all_location,all_location_v,F=wander(num,all_location,all_location_v,radius,NN,F,num_old)
        num_old=num
        if randomWalkersCount in intervalSavePic:#每隔几个点保存图片
            usedInterval.append(randomWalkersCount)
            label=str(randomWalkersCount)
            plt.title("DLA Cluster", fontsize=20)
            all_locationx=[]#储存所有的x,y坐标
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
            fig=plt.figure()           
            plt.plot(all_locationx,all_locationy,'bo',ms=10)#将所有的点绘制图像
            plt.xticks([])#将x坐标轴的标签除去
            plt.yticks([])#将y坐标轴的标签除去
            plt.xlim(-radius-1,1+radius)
            plt.ylim(-radius-1,1+radius)
            plt.savefig("images/cluster{}.png".format(label), dpi=200)#保存图片
            plt.close()
    for ww in range(NN):
        all_x.append(all_location[0][ww,0])
        all_y.append(all_location[0][ww,1])
    fig=plt.figure()
    plt.plot(all_x,all_y,'bo',ms=10)#绘制最终的图像
    plt.xlim(-radius-1,radius+1)
    plt.ylim(-radius-1,radius+1)
    plt.savefig("images/cluster.png", dpi=200)
    plt.close()
    with imageio.get_writer('images/movie.gif', mode='I') as writer:
        for i in usedInterval:
            filename="images/cluster"+str(i)+".png"
            image = imageio.imread(filename)#将所有图像绘制成动画
            writer.append_data(image)
            os.remove(filename)#删除已经绘制的图像
        image = imageio.imread("images/cluster.png")
        writer.append_data(image)
DLAcluster(200,20)
