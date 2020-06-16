import numpy as np
import random
#number_wander的游走方式
h=[0,1,0,-1,0,0,-1,1,-1,1,0,0,0,0,1,1,-1,-1,1,1,1,1,-1,-1,-1,-1,0]
m=[1,0,-1,0,0,0,-1,1,1,-1,1,1,-1,-1,0,0,0,0,1,1,-1,-1,1,1,-1,-1,0]
n=[0,0,0,0,1,-1,0,0,0,0,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,0]
def checkAround(radius,height,location,squareSize,matrix):
    foundFriend=False
    exitCircle=False
    nearEdge=False
    wander=False
    rr=False
    kesai = 6#控制结合概率的参数
    global location1
    location1=np.zeros((3),dtype=int)
    for i in range(2):
        p=location[i]
        if abs(p)>(0.5*squareSize):
            nearEdge=True 
         
    if not nearEdge:
        x=location[0]
        y=location[1]
    
        rr=np.sqrt(x*x+y*y)
        for k in range(27):#检查周边位置是否已被占据，若有被占据位置，则存在两种可能：直接结合或是沿着凝聚体滑行游走
            neighbors=matrix[radius+2+location[0]+h[k],radius+2+location[1]+m[k],height+2+location[2]+n[k]]
            if neighbors==1:#若存在被占据位置，有一定概率结合，结合概率的参数为kesai，取1，3，8等，对应结合概率1/kesai
                q=kesai*random.random()
                if q<1:
                    foundFriend=True
                else:
                    wander=True#滑行
            if rr>=radius :
                exitCircle=True
        
    if not nearEdge and not foundFriend and not wander:#若在限定范围内，周边无占据位置，则继续随机游走
        for i in range(100000):
            ran=random.randint(0,25)
            location1[0]=location[0]+h[int(ran)]
            location1[1]=location[1]+m[int(ran)]
            location1[2]=location[2]+n[int(ran)]
            if not abs(location1[2])<height :
                continue
            break
    if not nearEdge and not foundFriend and wander:#描述沿凝聚体滑动过程，也可能原地不动
        for i in range(100000):
            ran=random.randint(0,26)
            location1[0]=location[0]+h[int(ran)]
            location1[1]=location[1]+m[int(ran)]
            location1[2]=location[2]+n[int(ran)]
            if not abs(location1[0])<0.5*squareSize or not abs(location1[1])<0.5*squareSize or not abs(location1[2])<height :
                continue
            if matrix[radius+2+location1[0]][radius+2+location1[1]][height+2+location1[2]] != 1:
               for k in range(27):#该部分描述wander过程，因此也存在原地荡步
                    neighbors=matrix[radius+2+location[0]+h[k],radius+2+location[1]+m[k],height+2+location[2]+n[k]]
                    if neighbors==1 :
                        rr=True
                        break
            if rr:
                break
    return (location1,foundFriend, nearEdge, exitCircle)