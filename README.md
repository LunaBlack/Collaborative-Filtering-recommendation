# Collaborative-Filtering-recommendation

整个项目分为若干个阶段。

### Phase1阶段：  
包含文件Phase1a、Phase1b；  
该阶段未采用协同过滤算法，而是用随机值、平均值等作为结果

### Phase2阶段：  
包含文件Phase2a、Phase2b、Phase2bOneRun；  
该阶段采用了协同过滤算法，主要是基于用户的协同过滤算法

### Phase2EC阶段：
包含文件Phase2EC；  
该阶段采用了协同过滤算法，取基于用户或项目的协同过滤算法的均值；  
改进了相似度的计算方法

### Rewrite：
包含文件RewriteCF.py；  
用numpy等库重写了一遍Phase2EC的算法；  
算法思想一致，稍微提高了一些性能

### Phase3阶段：
包含文件Phase3.py；  
在Rewrite的基础上进一步延伸；  
不是取基于用户或项目的协同过滤算法的算术平均值，而是加权求和，给它们赋予不同权重

### Phase4阶段：
包含Phase4.py；  
重写了Phase3，加入了余弦相似度;  
算法思想基本一直，提供对比
