Phase 2 EC 说明文件
==================


开发环境
-----------------

windows + python2


程序运行
-----------------

Phase2EC.py:

从命令行运行该文件，程序自动运行
算法运行一次的相应计算结果将输出到屏幕
算法运行十次求平均值的相应计算结果将输出到`output_ec.txt`文件中

例如：
`New Collaborative Filtering Rating prediction RMSE (friends = 0): 0.922145716259`
`New Collaborative Filtering Rating prediction RMSE (friends = 25): 0.908329394481`
`New Collaborative Filtering Rating prediction RMSE (friends = 300): 0.859090681201`
`New Collaborative Filtering Rating prediction RMSE (friends = 500): 0.851466940324`
`New Collaborative Filtering Rating prediction RMSE (friends = all): 0.859026254055`



设计思路
-----------------

目标：指定用户ID，基于该用户和其他人的评价历史，根据某个特定算法
预测用户u对电影m的评分，并对算法的预测结果进行质量评估

具体过程为：
1. 从文件中读出ratingList，list元素为tuple(user, movie, rating)
2. 将ratingList按80-20的比例划分为训练集和测试集，并根据训练集得到rLu和rLm
   list(rLu)是每个用户评价过的电影，元素是{movie1:rating1, movie2:rating2……}
   list(rLm)是每部电影收到的用户评价，元素是{user1:rating1, user2:rating2……}
3. 针对测试集中的每个tuple，预测其中的用户u在特定算法下对电影m的评分，记录实际评分和预测评分
4. 利用实际评分和某特定算法的预测评分，计算出该算法的rmse值
5. 其中，函数oneRun只运行一次上述过程，并将结果输出到屏幕
   函数averageTenRuns重复十次上述过程，计算每个算法的平均rmse值(重复十次的平均值)，并将结果输出到文件


算法：
(共5个算法，均为EC部分优化的算法，不同点在于k1、k2取不同值)
(主要调整了用户相似性的计算公式，同时加入基于项目/电影的评分预测计算，最终的预测结果为两者的平均值)
(1) 根据重新调整的公式计算两个用户之间的相似性
(2) 根据公式计算两个电影之间的相似性
(3) 根据相似性选择与指定用户最相似的k1个用户
    在实验中，k1的值依次为0、25、300、500、943(全部用户数)
    利用这k1个最相似的用户，根据公式计算用户u对电影m的预测评分
(4) 根据相似性选择与指定电影最相似的k2个电影
    在实验中，k2的值依次为0、25、300、500、1682(全部电影数)
    利用这k2个最相似的电影，根据公式计算用户u对电影m的预测评分
(5) 求(3)和(4)中结果的平均值，以此作为最终的预测评分