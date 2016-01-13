Phase 2 说明文件
==================


开发环境
-----------------

windows + python2


程序运行
-----------------

Phase2b.py:

从命令行运行该文件，程序自动运行，并将相应的计算结果输出到`output.txt`文件中

例如：
`Random prediction Average RMSE: 1.88647135641`
`User Mean Rating prediction Average RMSE: 1.04406887704`
`Movie Mean Rating prediction Average RMSE: 1.0293787248`
`User-Movie Mean Rating prediction Average RMSE: 0.984359868468`
`Collaborative Filtering Rating prediction Average RMSE (friends = 0): 1.04406887704`
`CollaborativeFiltering-Movie Mean Rating prediction Average RMSE (friends = 0): 0.984359868468`
`Collaborative Filtering Rating prediction Average RMSE (friends = 25): 1.1014973937`
`CollaborativeFiltering-Movie Mean Rating prediction Average RMSE (friends = 25): 0.999214991471`
`Collaborative Filtering Rating prediction Average RMSE (friends = 300): 0.952682404223`
`CollaborativeFiltering-Movie Mean Rating prediction Average RMSE (friends = 300): 0.955253191599`
`Collaborative Filtering Rating prediction Average RMSE (friends = 500): 0.94489367373`
`CollaborativeFiltering-Movie Mean Rating prediction Average RMSE (friends = 500): 0.955909458672`
`Collaborative Filtering Rating prediction Average RMSE (friends = numUsers): 0.948040576531`
`CollaborativeFiltering-Movie Mean Rating prediction Average RMSE (friends = numUsers): 0.953044612314`


Phase2bOneRun.py:

从命令行运行该文件，程序自动运行，并将相应的计算结果输出到屏幕

例如：
`Random prediction RMSE:  1.8773918078`
`User Mean Rating prediction RMSE:  1.03833881869`
`Movie Mean Rating prediction RMSE:  1.02716767744`
`User-Movie Mean Rating prediction RMSE:  0.98138251942`
`Collaborative Filtering Rating prediction RMSE (friends = 0):  1.03833881869`
`CollaborativeFiltering-Movie Mean Rating prediction RMSE (friends = 0):  0.98138251942`
`Collaborative Filtering Rating prediction RMSE (friends = 25):  1.09820474009`
`CollaborativeFiltering-Movie Mean Rating prediction RMSE (friends = 25):  0.996994564901`
`Collaborative Filtering Rating prediction RMSE (friends = 300):  0.950229964665`
`CollaborativeFiltering-Movie Mean Rating prediction RMSE (friends = 300):  0.953612248462`
`Collaborative Filtering Rating prediction RMSE (friends = 500):  0.94296614394`
`CollaborativeFiltering-Movie Mean Rating prediction RMSE (friends = 500):  0.954645617494`
`Collaborative Filtering Rating prediction RMSE (friends = numUsers):  0.945263817132`
`CollaborativeFiltering-Movie Mean Rating prediction RMSE (friends = numUsers):  0.951706226168`


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
4. 利用实际评分和某特定算法的预测评分，计算出该算法的rmse值
5. 其中，project2Phase2bOneRun.py只运行一次上述过程，并将结果输出到屏幕
   project2Phase2b.py重复十次上述过程，计算每个算法的平均rmse值(重复十次的平均值)，并将结果输出到文件


算法：

算法1：预测结果为(1, 5)中的随机任意整数
算法2：用户u曾作出的所有评分的平均值
算法3：电影m曾收到的所有评分的平均值
算法4：算法2和算法3的平均值

算法5、7、9、11、13：
(1) 根据公式计算两个用户之间的相似性，相似性介于(-1, 1)之间
(2) 根据相似性选择与指定用户最相似的k个用户
    算法5、7、9、11、13中，k的值依次为0、25、300、500、943(全部用户数)
(3) 利用这k个最相似的用户，根据公式计算用户u对电影m的预测评分

算法6、8、10、12、14：
(1) 根据公式计算两个用户之间的相似性，相似性介于(-1, 1)之间
(2) 根据相似性选择与指定用户最相似的k个用户
    算法6、8、10、12、14中，k的值依次为0、25、300、500、943(全部用户数)
(3) 利用这k个最相似的用户，根据公式计算用户u对电影m的预测评分
(4) 计算电影m曾收到的所有评分的平均值
(5) 计算步骤3和步骤4的平均值，以此作为最终结果