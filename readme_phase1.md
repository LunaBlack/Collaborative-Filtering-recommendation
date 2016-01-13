Phase 1 说明文件
==================


开发环境
-----------------

windows + python2


程序运行
-----------------

Phase1b.py:

从命令行运行该文件，程序自动运行，并输出相应的计算结果

例如：
`Random prediction RMSE:  1.88661071766`
`User Mean Rating prediction RMSE:  1.03264113429`
`Movie Mean Rating prediction RMSE:  1.02037396712`
`User-Movie Mean Rating prediction RMSE:  0.974268531385`


设计思路
-----------------

目标：指定用户ID，基于该用户和其他人的评价历史，根据某个特定算法
预测该用户对某特定电影m的评分，并对算法的预测结果进行质量评估

具体过程为：
1. 从文件中读出ratingList，list元素为tuple(user, movie, rating)
2. 将ratingList按80-20的比例划分为训练集和测试集，并根据训练集得到rLu和rLm
   list(rLu)是每个用户评价过的电影，元素是{movie1:rating1, movie2:rating2……}
   list(rLm)是每部电影收到的用户评价，元素是{user1:rating1, user2:rating2……}
3. 针对测试集中的每个tuple，预测其中的用户u在特定算法下对电影m的评分，记录实际评分和预测评分
4. 利用实际评分和某特定算法的预测评分，计算出该算法的rmse值，并输出到屏幕

算法：
算法1：预测结果为(1, 5)中的随机任意整数
算法2：用户u曾作出的所有评分的平均值
算法3：电影m曾收到的所有评分的平均值
算法4：算法2和算法3的平均值