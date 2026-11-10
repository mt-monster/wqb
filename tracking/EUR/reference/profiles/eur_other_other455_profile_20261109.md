# EUR × other455 字段画像（2026-11-09）

> 150+/未完（complete=false，total 150 首批）；Relationship enhanced with AI/ML（Node2Vec 竞争关系图嵌入）
> 塔位：OTHER(×1.5)；拥挤度：aC 302 / uC 145

## 一、字段结构
三类：①KMeans 聚类标签（GROUP，5/10/20 簇，cov 0.9705）②PCA 因子分（MATRIX fact1-3_value，cov 0.9705）③PCA 聚类标签（GROUP）。全部基于 D1-lagged Node2Vec 竞争关系图嵌入（W1/W2 两种窗口）。

## 二、判定
1. **已判死**（普查表）：other455 node2vec-PCA **近静态 0.010-0.012**（TO 近零，PCA 分数日间不变）
2. PCA 分数=图嵌入坐标，日间几乎不变 → 无日频信息
3. **判定：近静态结构性排除**（存量结论沿用）；唯一用途=聚类标签作分组轴（同 pv29 换轴已证无效）
