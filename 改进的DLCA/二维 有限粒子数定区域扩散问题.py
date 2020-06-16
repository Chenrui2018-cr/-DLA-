

import numpy as np
import random
import matplotlib.pyplot as plt
import os
import imageio

h=[0,1,0,-1,1,1,-1,-1]
m=[1,0,-1,0,-1,1,-1,1]
def checkaround(NN,rans,all_location):            
    locationss=all_location[rans]
    pd=[]
    k=False
    if locationss.size==2:
        for i in range(NN):
            if i ==rans:
                continue
            else:
                c=all_location[i]
                if c.size==2:
                    if abs(locationss[0]-c[0])<=1 and abs(locationss[1]-c[1])<=1:
                        k=True
                   
                else:
                    for j in range(c.shape[0]):
                        if abs(locationss[0]-c[j,0])<=1 and abs(locationss[1]-c[j,1])<=1:
                            k=True
                       
                if k:
                    pd.append(i)
                    k=False
               
    if locationss.size!=2:
        for w in range(locationss.shape[0]):
            locationss1=locationss[w,:]
            for i in range(NN):
                if i ==rans:
                    continue
                else:
                    c=all_location[i]
                    if c.size==2:
                        if abs(locationss1[0]-c[0])<=1 and abs(locationss1[1]-c[1])<=1:
                            k=True
                    else:
                        for j in range(c.shape[0]):
                            if abs(locationss1[0]-c[j,0])<=1 and abs(locationss1[1]-c[j,1])<=1:
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
    for i in range(50000):
        c=random.randint(0,7)
        dx=h[c]
        dy=m[c]
        
        if locationss.size==2:
            location1=np.array([locationss[0]+dx,locationss[1]+dy])
            if location1[0]**2+location1[1]**2<radius**2:
                locationss=location1
                break
            
        else:
            yyy=True
            for j in range(locationss.shape[0]):
                location0=[locationss[j,0]+dx,locationss[j,1]+dy]
                if location0[0]**2+location0[1]**2>radius**2:
                    yyy=False
                    break
                
                    
            if yyy:
                locationss[:,0]+=dx
                locationss[:,1]+=dy
                break
            
    all_location[rans]=locationss
    return all_location


def randomAtRadius(radius):
    theta=2*np.pi*random.random()
    r=random.random()*radius
    x=np.sin(theta)*r
    y=np.cos(theta)*r
    location=np.array([x, y]) #save locaction
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
    intervalSavePic=range(2,400000,100)
    while num>1:
        randomWalkersCount += 1
        rans=random.randint(0,num-1)
        all_location,pd = checkaround(num,rans,all_location)
        all_location = wander(num,rans,all_location,radius)
        all_location = [all_location[i] for i in range(0,len(all_location)) if i not in pd]
        num=len(all_location)
    
        if randomWalkersCount in intervalSavePic:#每隔一段时间保存图片
            usedInterval.append(randomWalkersCount) 
            label=str(randomWalkersCount)
            plt.title("DLA Cluster", fontsize=20)
            all_locationx=[]
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
                       
            plt.plot(all_locationx,all_locationy,'ro',ms=5)#绘制所有的点
            plt.xticks([])#消除x坐标标签
            plt.yticks([])#消除y坐标标签
            plt.xlim(-radius-1,1+radius)
            plt.ylim(-radius-1,1+radius)
            plt.savefig("images/cluster{}.png".format(label), dpi=200)#保存图片
            plt.close()
    
    for ww in range(NN):
        all_x.append(all_location[0][ww,0])
        all_y.append(all_location[0][ww,1])
    fig=plt.figure()
    plt.plot(all_x,all_y,'ro',ms=5)#绘制最终的图片
    plt.xlim(-radius-1,radius+1)
    plt.ylim(-radius-1,radius+1)
    plt.savefig("images/cluster.png", dpi=200)
    plt.close()
    with imageio.get_writer('images/movie.gif', mode='I') as writer:
        for i in usedInterval:
            filename="images/cluster"+str(i)+".png"
            image = imageio.imread(filename)#绘制最终的动画
            writer.append_data(image)
            os.remove(filename)#删去已经制作动画的图片
        image = imageio.imread("images/cluster.png")
        writer.append_data(image)#将最终的图片也写入动画
DLAcluster(1000,40)
    

