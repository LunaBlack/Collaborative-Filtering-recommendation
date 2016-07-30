#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys
import time
import cmath as math

import numpy as np
import pandas as pd
from numpy import linalg as la
from sklearn.cross_validation import train_test_split
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import mean_squared_error


userNum = 943
itemNum = 1682


# 读文件
def readFile(filename):
    header = ['user_id', 'item_id', 'rating', 'timestamp']
    df = pd.read_csv('ml-100k/u.data', sep='\t', names=header)
    return df


# 划分训练集与测试集
def partitionData(data, testPercent):
    train_data, test_data = train_test_split(data, test_size=testPercent)
    return [train_data, test_data]


# 创建用户-项目矩阵, user*item
def createMatrix(data, n_users, n_items):
    data_matrix = np.zeros((n_users, n_items))
    for line in data.itertuples():
        data_matrix[line[1]-1, line[2]-1] = line[3]
    return data_matrix


# # 余弦相似度
# def computeSim(inA,inB):
#     sim = np.dot(inA, inB.reshape(-1, 1))/(la.norm(inA) * la.norm(inB))
#     return sim[0]


# 皮尔逊相关系数
def computeSim(inA, inB):
    sim = np.corrcoef(inA, inB)[0][1] * 0.5 + 0.5
    return sim


# 计算用户相似度矩阵
def userSim(data_matrix):
    n = np.shape(data_matrix)[0]  # 即userNum
    userSimArr = np.zeros(shape=(n, n))  # 基于皮尔逊相关系数的相似度矩阵,对称的

    for i in range(n):
        for j in range(i+1, n):
            overLap = np.nonzero(np.logical_and(data_matrix[i, :]>0, data_matrix[j, :]>0))[0]
            if len(overLap) > 1:
                sim = computeSim(data_matrix[i, overLap], data_matrix[j, overLap])
            else:
                sim = 0
            userSimArr[i][j] = sim
            userSimArr[j][i] = sim

    userSimArr = np.nan_to_num(userSimArr)
    return userSimArr


# 计算项目相似度矩阵
def itemSim(data_matrix):
    n = np.shape(data_matrix)[1]  # 即itemNum
    itemSimArr = np.zeros(shape=(n, n))  # 基于皮尔逊相关系数的相似度矩阵,对称的

    for i in range(n):
        for j in range(i+1, n):
            overLap = np.nonzero(np.logical_and(data_matrix[:, i]>0, data_matrix[:, j]>0))[0]
            if len(overLap) > 1:
                sim = computeSim(data_matrix[overLap, i], data_matrix[overLap, j])
            else:
                sim = 0
            itemSimArr[i][j] = sim
            itemSimArr[j][i] = sim

    itemSimArr = np.nan_to_num(itemSimArr)
    return itemSimArr


# 计算改进的用户相似度矩阵
def newUserSim(data_matrix):
    n = np.shape(data_matrix)[0]  # 即userNum
    userSimArr = np.zeros(shape=(n, n))  # 基于皮尔逊相关系数的相似度矩阵,对称的
    userCommon = np.zeros(shape=(n, n))  # 共同评价项目数

    for i in range(n):
        for j in range(i+1, n):
            overLap = np.nonzero(np.logical_and(data_matrix[i, :]>0, data_matrix[j, :]>0))[0]
            if len(overLap) > 1:
                sim = computeSim(data_matrix[i, overLap], data_matrix[j, overLap])
            else:
                sim = 0
            userSimArr[i][j] = sim
            userSimArr[j][i] = sim
            userCommon[i][j] = len(overLap)
            userCommon[j][i] = len(overLap)

    coef = np.exp((userCommon * 1.0 / userCommon.max(axis=0)) - 1)
    newUserSim = coef * userSimArr  # 以列来读,某列代表某用户与其它用户的相似度
    newUserSim = np.nan_to_num(newUserSim)  # 改进的相似度矩阵,非对称的
    return newUserSim, userCommon


# 计算改进的项目相似度矩阵
def newItemSim(data_matrix):
    n = np.shape(data_matrix)[1]  # 即itemNum
    itemSimArr = np.zeros(shape=(n, n))  # 基于皮尔逊相关系数的相似度矩阵,对称的
    itemCommon = np.zeros(shape=(n, n))  # 被共同评价用户数

    for i in range(n):
        for j in range(i+1, n):
            overLap = np.nonzero(np.logical_and(data_matrix[:, i]>0, data_matrix[:, j]>0))[0]
            if len(overLap) > 1:
                sim = computeSim(data_matrix[overLap, i], data_matrix[overLap, j])
            else:
                sim = 0
            itemSimArr[i][j] = sim
            itemSimArr[j][i] = sim
            itemCommon[i][j] = len(overLap)
            itemCommon[j][i] = len(overLap)

    coef = np.exp((itemCommon * 1.0 / itemCommon.max(axis=0)) - 1)
    newItemSim = coef * itemSimArr  # 以列来读,某列代表某项目与其它项目的相似度
    newItemSim = np.nan_to_num(newItemSim)  # 改进的相似度矩阵,非对称的
    return newItemSim, itemCommon


# 以基于用户的协同过滤算法进行评分预测
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
        maxSim = uSim[index]
        if maxSim == 0:
            break  #不再有相似用户
        if dataSet[index][m] == 0:
            uSim[index] = 0  #在之后不再考虑该用户
            continue
        rateSim += maxSim * (dataSet[index][m] - np.mean(dataSet[index, np.nonzero(dataSet[index,:])[0]]))
        simTotal += maxSim
        uSim[index] = 0  #在之后不再考虑该用户
        k -= 1

    if simTotal != 0:
        rating += rateSim/simTotal
    return rating


# 以基于项目的协同过滤算法进行评分预测
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
        maxSim = mSim[index]
        if maxSim == 0:
            break  #不再有相似项目
        if dataSet[u][index] == 0:
            mSim[index] = 0  #在之后不再考虑该项目
            continue
        rateSim += maxSim * (dataSet[u][index] - np.mean(dataSet[np.nonzero(dataSet[:,index])[0], index]))
        simTotal += maxSim
        mSim[index] = 0  #在之后不再考虑该项目
        k -= 1

    if simTotal != 0:
        rating += rateSim/simTotal
    return rating


# 以基于用户的、加权重的协同过滤算法进行评分预测
def userNewCFPrediction(u, m, dataSet, userSim, userCommon, k):
    uRated = np.nonzero(dataSet[u,:])[0]
    if len(uRated) == 0:
        rating = 0.0
    else:
        rating = np.mean(dataSet[u, uRated])
    uSim = userSim[:,u].copy()

    simTotal = 0.0
    rateSim = 0.0
    sumCommon = 0
    while(k):
        index = uSim.argmax()
        maxSim = uSim[index]
        if maxSim == 0:
            break  #不再有相似用户
        if dataSet[index][m] == 0:
            uSim[index] = 0  #在之后不再考虑该用户
            continue
        rateSim += maxSim * (dataSet[index][m] - np.mean(dataSet[index, np.nonzero(dataSet[index,:])[0]]))
        simTotal += maxSim
        sumCommon += userCommon[u][index]
        uSim[index] = 0  #在之后不再考虑该用户
        k -= 1

    if simTotal != 0:
        rating += rateSim/simTotal
    return rating, sumCommon


# 以基于项目的、加权重的协同过滤算法进行评分预测
def itemNewCFPrediction(u, m, dataSet, itemSim, itemCommon, k):
    mRated = np.nonzero(dataSet[:,m])[0]
    if len(mRated) == 0:
        rating = 0.0
    else:
        rating = np.mean(dataSet[mRated, m])
    mSim = itemSim[:,m].copy()

    simTotal = 0.0
    rateSim = 0.0
    sumCommon = 0
    while(k):
        index = mSim.argmax()
        maxSim = mSim[index]
        if maxSim == 0:
            break  #不再有相似项目
        if dataSet[u][index] == 0:
            mSim[index] = 0  #在之后不再考虑该项目
            continue
        rateSim += maxSim * (dataSet[u][index] - np.mean(dataSet[np.nonzero(dataSet[:,index])[0], index]))
        simTotal += maxSim
        sumCommon += itemCommon[m][index]
        mSim[index] = 0  #在之后不再考虑该项目
        k -= 1

    if simTotal != 0:
        rating += rateSim/simTotal
    return rating, sumCommon


# 取基于用户和基于项目评分的均值作为最终的预测评分
def meanCFPrediction(u, m, dataSet, userSim, itemSim, k1, k2):
    rating1 = userCFPrediction(u, m, dataSet, userSim, k1)
    rating2 = itemCFPrediction(u, m, dataSet, itemSim, k2)
    return (rating1+rating2)/2.0
    # return rating1


# 取基于用户和基于项目评分的加权和作为最终的预测评分
def avgCFPrediction(u, m, dataSet, userSim, itemSim, userCommon, itemCommon, k1, k2):
    rating1, userSumCommon = userNewCFPrediction(u, m, dataSet, userSim, userCommon, k1)
    rating2, itemSumCommon = itemNewCFPrediction(u, m, dataSet, itemSim, itemCommon, k2)
    sumCommon = userSumCommon + itemSumCommon
    if sumCommon == 0:
        return (rating1+rating2)/2.0
    else:
        return (userSumCommon*1.0/sumCommon)*rating1 + (itemSumCommon*1.0/sumCommon)*rating2
    # return rating1


# 计算均方根误差
def calculateRmse(actual, predicted):
    summation = 0.0
    length = len(actual)
    for i in range(length):
        summation += (actual[i] - predicted[i]) ** 2
    rmse = math.sqrt(summation/length).real
    return rmse


# 测试未改进的、取均值的方式
def runOld(filename, n_users, n_items, testPercent=0.2, k=[0, 25, 300, 500]):
    data = readFile(filename)
    [train_data, test_data] = partitionData(data, testPercent)
    train_matrix = createMatrix(train_data, n_users, n_items)
    print '{} finish loading data'.format(time.ctime())

    userSimArr = userSim(train_matrix)
    itemSimArr = itemSim(train_matrix)
    print '{} finish computing similary'.format(time.ctime())

    actual = []
    predicted = []
    for i in range(len(k)):
        predicted.append([])

    for t in test_data.values:
        actual.append(t[2])

        # 取不同的k值(近邻数)进行预测
        for n, i in enumerate(k):
            predicted[n].append(meanCFPrediction(t[0]-1, t[1]-1, train_matrix, userSimArr, itemSimArr, i, i))

    print '{} finish predicting rating'.format(time.ctime())

    rmses = []
    for i in range(len(k)):
        rmses.append(calculateRmse(actual, predicted[i]))
    print '{} finish computing rmse'.format(time.ctime())
    return rmses


# 测试改进的、取加权均值的方式
def runNew(filename, n_users, n_items, testPercent=0.2, k=[0, 25, 300, 500]):
    data = readFile(filename)
    [train_data, test_data] = partitionData(data, testPercent)
    train_matrix = createMatrix(train_data, n_users, n_items)
    print '{} finish loading data'.format(time.ctime())

    userSimArr, userCommon = newUserSim(train_matrix)
    itemSimArr, itemCommon = newItemSim(train_matrix)
    print '{} finish computing similary'.format(time.ctime())

    actual = []
    predicted = []
    for i in range(len(k)):
        predicted.append([])

    for t in test_data.values:
        actual.append(t[2])

        # 取不同的k值(近邻数)进行预测
        for n, i in enumerate(k):
            predicted[n].append(avgCFPrediction(t[0]-1, t[1]-1, train_matrix, userSimArr, itemSimArr, userCommon, itemCommon, i, i))

    print '{} finish predicting rating'.format(time.ctime())

    rmses = []
    for i in range(len(k)):
        rmses.append(calculateRmse(actual, predicted[i]))
    print '{} finish computing rmse'.format(time.ctime())
    return rmses



if __name__ == '__main__':
    print '{} start'.format(time.ctime())

    rmses = np.zeros(4)
    for i in range(10):
        # rmse = runOld('ml-100k/u.data', userNum, itemNum, 0.2, k=[0, 25, 300, 500])
        rmse = runNew('ml-100k/u.data', userNum, itemNum, 0.2, k=[0, 25, 300, 500])
        print "time %d: " % (i+1), rmse
        print '{} iteration {}/{} end'.format(time.ctime(), i+1, 10)
        rmses += rmse

    rmses = rmses / 10
    print "average of ten times: ", rmses
    print time.ctime()
