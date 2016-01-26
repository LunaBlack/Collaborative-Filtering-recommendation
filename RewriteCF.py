#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, math
import pandas as pd
import numpy as np
from numpy import linalg as la


userNum = 943
itemNum = 1682


#读文件
def readFile(filename):
    dataList = []
    with open(filename, 'r') as f:
        records = f.readlines()
    for r in records:
        r = r.strip().split('\t')
        dataList.append([int(r[0]), int(r[1]), int(r[2])])
    return dataList


#划分训练集与测试集
def partitionData(dataList, testPercent):
    random.shuffle(dataList)
    testSize = int(len(dataList) * testPercent)
    trainSet = dataList[:testSize]
    testSet = dataList[testSize:]
    return [trainSet, testSet]


#list转化为array, user*item
def list2Array(dataSet):
    arr = np.zeros(shape=(userNum,itemNum), dtype=int)
    for data in dataSet:
        arr[data[0]-1][data[1]-1] = data[2]
    return arr


# 皮尔逊相关系数
def pearsSim(inA, inB):
    if len(inA) <= 1:   sim = 0.0
    else:   sim = np.corrcoef(inA, inB)[0][1]
    if np.isnan(sim):   sim = 0.0
    return sim


#计算用户相似度矩阵
def userSim(dataSet):
    n = np.shape(dataSet)[0]  #即userNum
    userSimArr = np.zeros(shape=(n,n))
    for i in range(n):
        for j in range(i+1, n):
            sim = 0
            overLap = np.nonzero(np.logical_and(dataSet[i,:]>0, dataSet[j,:]>0))[0]
            if len(overLap) > 0:
                sim = pearsSim(dataSet[i,overLap], dataSet[j,overLap])
            userSimArr[i][j] = sim
            userSimArr[j][i] = sim
    return userSimArr
    

#计算项目相似度矩阵
def itemSim(dataSet):
    n = np.shape(dataSet)[1]  #即itemNum
    itemSimArr = np.zeros(shape=(n,n))
    for i in range(n):
        for j in range(i+1, n):
            sim = 0
            overLap = np.nonzero(np.logical_and(dataSet[:,i]>0, dataSet[:,j]>0))[0]
            if len(overLap) > 0:
                sim = pearsSim(dataSet[overLap,i], dataSet[overLap,j])
            itemSimArr[i][j] = sim
            itemSimArr[j][i] = sim
    return itemSimArr


#计算改进的用户相似度矩阵
def newUserSim(dataSet):
    n = np.shape(dataSet)[0]  #即userNum
    userSimArr = np.zeros(shape=(n,n))  #基于皮尔逊相关系数的相似度矩阵,对称的
    userCommon = np.zeros(shape=(n,n))  #共同评价项目数
    newUserSim = np.zeros(shape=(n,n))  #改进的相似度矩阵,非对称的
    for i in range(n):
        for j in range(i+1, n):
            sim = 0
            overLap = np.nonzero(np.logical_and(dataSet[i,:]>0, dataSet[j,:]>0))[0]
            if len(overLap) > 0:
                sim = pearsSim(dataSet[i,overLap], dataSet[j,overLap])
            userSimArr[i][j] = sim
            userSimArr[j][i] = sim
            userCommon[i][j] = len(overLap)
            userCommon[j][i] = len(overLap)

    coef = np.exp((userCommon*1.0/userCommon.max(axis=0))-1)
    newUserSim = coef * userSimArr  #以列来读,某列代表某用户与其它用户的相似度
    newUserSim = np.nan_to_num(newUserSim)
    return newUserSim
    

#计算改进的项目相似度矩阵
def newItemSim(dataSet):
    n = np.shape(dataSet)[1]  #即itemNum
    itemSimArr = np.zeros(shape=(n,n))  #基于皮尔逊相关系数的相似度矩阵,对称的
    itemCommon = np.zeros(shape=(n,n))  #被共同评价用户数
    newItemSim = np.zeros(shape=(n,n))  #改进的相似度矩阵,非对称的
    for i in range(n):
        for j in range(i+1, n):
            sim = 0
            overLap = np.nonzero(np.logical_and(dataSet[:,i]>0, dataSet[:,j]>0))[0]
            if len(overLap) > 0:
                sim = pearsSim(dataSet[overLap,i], dataSet[overLap,j])
            itemSimArr[i][j] = sim
            itemSimArr[j][i] = sim
            itemCommon[i][j] = len(overLap)
            itemCommon[j][i] = len(overLap)

    coef = np.exp((itemCommon*1.0/itemCommon.max(axis=0))-1)
    newItemSim = coef * itemSimArr  #以列来读,某列代表某项目与其它项目的相似度
    newItemSim = np.nan_to_num(newItemSim)
    return newItemSim


#以基于用户的协同过滤算法进行评分预测
def userCFPrediction(u, m, dataSet, userSim, k):
    uRated = np.nonzero(dataSet[u,:])[0]
    if len(uRated) == 0:
        rating = 0.0
    else:
        rating = np.mean(dataSet[u, uRated])
    uSim = userSim[:,u].copy()
    
    simTotal = 0.0
    rateSim = 0.0
    while(k):
        index = uSim.argmax()
        m = uSim[index]
        if uSim[index] == 0:
            break  #不再有相似用户
        if dataSet[index][m] == 0:
            uSim[index] = 0  #在之后不再考虑该用户
            continue
        rateSim += m * (dataSet[index][m] - np.mean(dataSet[index, np.nonzero(dataSet[index,:])[0]]))
        simTotal += m
        uSim[index] = 0  #在之后不再考虑该用户
        k -= 1

    if simTotal != 0:
        rating += rateSim/simTotal
    return rating


#以基于项目的协同过滤算法进行评分预测
def itemCFPrediction(u, m, dataSet, itemSim, k):
    mRated = np.nonzero(dataSet[:,m])[0]
    if len(mRated) == 0:
        rating = 0.0
    else:
        rating = np.mean(dataSet[mRated, m])
    mSim = itemSim[:,m].copy()
    
    simTotal = 0.0
    rateSim = 0.0
    while(k):
        index = mSim.argmax()
        m = mSim[index]
        if mSim[index] == 0:
            break  #不再有相似项目
        if dataSet[u][index] == 0:
            mSim[index] = 0  #在之后不再考虑该项目
            continue
        rateSim += m * (dataSet[u][index] - np.mean(dataSet[np.nonzero(dataSet[:,index])[0], index]))
        simTotal += m
        mSim[index] = 0  #在之后不再考虑该项目
        k -= 1

    if simTotal != 0:
        rating += rateSim/simTotal
    return rating

        
#取基于用户和基于项目评分的均值作为最终的预测评分
def meanCFPrediction(u, m, dataSet, userSim, itemSim, k1, k2):
    rating1 = userCFPrediction(u, m, dataSet, userSim, k1)
    rating2 = itemCFPrediction(u, m, dataSet, itemSim, k2)
    return (rating1+rating2)/2.0


#计算均方根误差
def calculateRmse(actual, predicted):
    summation = 0.0
    length = len(actual)
    for i in range(length):
        summation += (actual[i] - predicted[i]) ** 2
    rmse = math.sqrt(summation/length)
    return rmse


#测试基于用户、基于项目、改进且取均值 三种方式
def runAll(filename):
    testPercent = 0.2
    dataList = readFile(filename)
    [trainSet, testSet] = partitionData(dataList, testPercent)
    trainSet = list2Array(trainSet)

    oldUserSim = userSim(trainSet)
    oldItemSim = itemSim(trainSet)
    userSimArr = newUserSim(trainSet)
    itemSimArr = newItemSim(trainSet)
    
    actual = []
    predicted = []
    for i in range(15):
        predicted.append([])
        
    for t in testSet:
        actual.append(t[2])

        #取不同的k值(近邻数)进行预测
        predicted[0].append(userCFPrediction(t[0]-1, t[1]-1, trainSet, oldUserSim, 0))
        predicted[1].append(userCFPrediction(t[0]-1, t[1]-1, trainSet, oldUserSim, 25))
        predicted[2].append(userCFPrediction(t[0]-1, t[1]-1, trainSet, oldUserSim, 300))
        predicted[3].append(userCFPrediction(t[0]-1, t[1]-1, trainSet, oldUserSim, 500))
        predicted[4].append(userCFPrediction(t[0]-1, t[1]-1, trainSet, oldUserSim, userNum))

        predicted[5].append(itemCFPrediction(t[0]-1, t[1]-1, trainSet, oldItemSim, 0))
        predicted[6].append(itemCFPrediction(t[0]-1, t[1]-1, trainSet, oldItemSim, 25))
        predicted[7].append(itemCFPrediction(t[0]-1, t[1]-1, trainSet, oldItemSim, 300))
        predicted[8].append(itemCFPrediction(t[0]-1, t[1]-1, trainSet, oldItemSim, 500))
        predicted[9].append(itemCFPrediction(t[0]-1, t[1]-1, trainSet, oldItemSim, itemNum))
        
        predicted[10].append(meanCFPrediction(t[0]-1, t[1]-1, trainSet, userSimArr, itemSimArr, 0, 0))
        predicted[11].append(meanCFPrediction(t[0]-1, t[1]-1, trainSet, userSimArr, itemSimArr, 25, 25))
        predicted[12].append(meanCFPrediction(t[0]-1, t[1]-1, trainSet, userSimArr, itemSimArr, 300, 300))
        predicted[13].append(meanCFPrediction(t[0]-1, t[1]-1, trainSet, userSimArr, itemSimArr, 500, 500))
        predicted[14].append(meanCFPrediction(t[0]-1, t[1]-1, trainSet, userSimArr, itemSimArr, userNum, itemNum))

    rmses = []
    for i in range(15):
        rmses.append(calculateRmse(actual, predicted[i]))

    with open('output_all.txt', 'w') as f:
        f.write("user RMSE(k=0): " + str(rmses[0]) + "\n")
        f.write("user RMSE(k=25): " + str(rmses[1]) + "\n")
        f.write("user RMSE(k=300): " + str(rmses[2]) + "\n")
        f.write("user RMSE(k=500): " + str(rmses[3]) + "\n")
        f.write("user RMSE(k=all): " + str(rmses[4]) + "\n")
        f.write("item RMSE(k=0): " + str(rmses[5]) + "\n")
        f.write("item RMSE(k=25): " + str(rmses[6]) + "\n")
        f.write("item RMSE(k=300): " + str(rmses[7]) + "\n")
        f.write("item RMSE(k=500): " + str(rmses[8]) + "\n")
        f.write("item RMSE(k=all): " + str(rmses[9]) + "\n")
        f.write("new RMSE(k=0): " + str(rmses[10]) + "\n")
        f.write("new RMSE(k=25): " + str(rmses[11]) + "\n")
        f.write("new RMSE(k=300): " + str(rmses[12]) + "\n")
        f.write("new RMSE(k=500): " + str(rmses[13]) + "\n")
        f.write("new RMSE(k=all): " + str(rmses[14]) + "\n")


#测试改进且取均值的方式
def runNew(filename):
    testPercent = 0.2
    dataList = readFile(filename)
    [trainSet, testSet] = partitionData(dataList, testPercent)
    trainSet = list2Array(trainSet)
    userSimArr = newUserSim(trainSet)
    itemSimArr = newItemSim(trainSet)
    
    actual = []
    predicted = []
    for i in range(5):
        predicted.append([])
        
    for t in testSet:
        actual.append(t[2])

        #取不同的k值(近邻数)进行预测
        predicted[0].append(meanCFPrediction(t[0]-1, t[1]-1, trainSet, userSimArr, itemSimArr, 0, 0))
        predicted[1].append(meanCFPrediction(t[0]-1, t[1]-1, trainSet, userSimArr, itemSimArr, 25, 25))
        predicted[2].append(meanCFPrediction(t[0]-1, t[1]-1, trainSet, userSimArr, itemSimArr, 300, 300))
        predicted[3].append(meanCFPrediction(t[0]-1, t[1]-1, trainSet, userSimArr, itemSimArr, 500, 500))
        predicted[4].append(meanCFPrediction(t[0]-1, t[1]-1, trainSet, userSimArr, itemSimArr, userNum, itemNum))

    rmses = []
    for i in range(5):
        rmses.append(calculateRmse(actual, predicted[i]))
    return rmses



if __name__ == '__main__':
    runAll('u.data')
    rmses = np.zeros(5)
    for i in range(10):
        rmse = runNew('u.data')
        print "time %d: " % i, rmse
        rmses += rmse
    rmses = rmses/10
    print "average of ten times: ", rmses
        

