# Collaborative-Filtering-recommendation

整个项目大体分为3个阶段。

Phase1阶段：
包含文件Phase1a、Phase1b；
该阶段未采用协同过滤算法，而是用随机值、平均值等作为结果

Phase2阶段：
包含文件Phase2a、Phase2b、Phase2bOneRun；
该阶段采用了协同过滤算法，主要是基于用户的协同过滤算法

Phase2EC阶段：
包含文件Phase2EC；
该阶段采用了协同过滤算法，取基于用户或项目的协同过滤算法的均值；
改进了相似度的计算方法

Rewrite：
用numpy等库重写了一遍Phase2EC的算法；
算法思想一致，稍微提高了一些性能
