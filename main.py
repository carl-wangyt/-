import numpy as np
import matplotlib.pyplot as plt
from deap import base, tools, creator, algorithms
import random
from copy import deepcopy

f_read = open("C101.txt")
i = 0
returnMat = np.zeros((101,7),dtype = int)

for line in  f_read.readlines():
    i = i + 1
    demo = line.split()
    if i == 5:
        car_number = int(demo[0])
        car_Q = int(demo[1])
    if i == 11:
        servetime = int(demo[6])
    if i > 9 and i < 111:        
        for j in range(7):
            returnMat[i-10][j] = int(demo[j])       

#字典保存参数信息
dataDict = {}
#坐标信息
dataDict['NodeCoor'] = []
#需求信息
dataDict['Demand'] = []
#时间窗口
dataDict['Timewindow'] = []
#装载量
dataDict['MaxLoad'] = car_Q
#服务时间
dataDict['ServiceTime'] = servetime

for i in range(101):
    dataDict['NodeCoor'].append((returnMat[i][1],returnMat[i][2])) 
    dataDict['Timewindow'].append((returnMat[i][4],returnMat[i][5]))
    dataDict['Demand'].append(returnMat[i][3])
    
#print(dataDict)


def genInd(dataDict = dataDict):
    '''生成个体'''
    nCustomer = len(dataDict['NodeCoor']) - 1 # 顾客数量
    perm = np.random.permutation(nCustomer) + 1 # 生成顾客的随机排列,注意顾客编号为1--n
    pointer = 0 # 迭代指针
    lowPointer = 0 # 指针指向下界
    permSlice = []
    # 当指针不指向序列末尾时
    while pointer < nCustomer -1:
        vehicleLoad = 0
        # 当不超载时，继续装载

        while (vehicleLoad < dataDict['MaxLoad']) and (pointer < nCustomer -1):
            vehicleLoad += dataDict['Demand'][perm[pointer]]
            pointer += 1
        if lowPointer+1 < pointer:
            tempPointer = np.random.randint(lowPointer+1, pointer)
            permSlice.append(perm[lowPointer:tempPointer].tolist())
            lowPointer = tempPointer
            pointer = tempPointer
        else:
            permSlice.append(perm[lowPointer::].tolist())
            break
    # 将路线片段合并为染色体
    ind = [0]
    for eachRoute in permSlice:
        ind = ind + eachRoute + [0]
    return ind

#-----------------------------------
## 评价函数
# 染色体解码
def decodeInd(ind):
    '''从染色体解码回路线片段，每条路径都是以0为开头与结尾'''
    indCopy = np.array(deepcopy(ind)) # 复制ind，防止直接对染色体进行改动
    idxList = list(range(len(indCopy)))
    zeroIdx = np.asarray(idxList)[indCopy == 0]
    routes = []
    for i,j in zip(zeroIdx[0::], zeroIdx[1::]):
        routes.append(ind[i:j]+[0])
    return routes

def calDist(pos1, pos2):
    '''计算距离的辅助函数，根据给出的坐标pos1和pos2，返回两点之间的距离
    输入： pos1, pos2 -- (x,y)元组
    输出： 欧几里得距离'''
    return np.sqrt((pos1[0] - pos2[0])*(pos1[0] - pos2[0]) + (pos1[1] - pos2[1])*(pos1[1] - pos2[1]))

ind = genInd(dataDict)
print(decodeInd(ind))
