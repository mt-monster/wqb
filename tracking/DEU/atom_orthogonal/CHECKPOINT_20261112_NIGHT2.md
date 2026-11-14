# 会话检查点（2026-11-12 凌晨二）：BE46/BE46b + 换防审计

## 一、BE46（聚类分组直用）—— 6/6 ERROR

group_* 第二参数要求 GROUP 类型（Unit[Group:1]），pv29 聚类标签是 MATRIX ⇒ 类型不匹配。
preflight 不校验类型/单位（第三次验证此坑）。修复：bucket(rank(x), range=...) 桥接（bl6AvMkN ACTIVE 先例）。

## 二、BE46b（bucket 桥接 5 臂）—— sim 4jSD1u6Wb4Vk9Ih11Cz4eFeT ✅ 已收割

| 臂 | 外层/分组 | alpha | S | F | TO | sub | 2Y | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | neut|bucket10簇 | omamvpbJ | undefined | undefined | undefined | undefined | undefined | undefined |
| 2 | neut|bucket20簇 | rK7KL3x1 | undefined | undefined | undefined | undefined | undefined | undefined |
| 3 | neut|市值桶 | 6XMX18kO | undefined | undefined | undefined | undefined | undefined | undefined |
| 4 | zscore|bucket10簇 | Jj8jmw9m | undefined | undefined | undefined | undefined | undefined | undefined |
| 5 | zscore(market)|内层bucket10 | npapoJE8 | undefined | undefined | undefined | undefined | undefined | undefined |

## 三、★换防审计（独立于挖矿的交付质量升级）

**88NmN37X 全部验证干净，可替换 qM7KxkQV：**
- IS：S1.79 / F1.53 / TO0.091 / sub0.95 / 2Y2.37，fail=0（全维优于 qM7KxkQV）
- self 0.5538 PASS（top xArzm3Mn）
- prod 0.5541 PASS（平台实测）
- 与篮子其余 10 件互相关全对 <0.7（最大对 zq3eb7No~RREPm361 0.6879 不变）
- 约束：与 qM7KxkQV 同族（0.86-0.98）互斥，取一；是否换防属用户提交授权范围。

## 四、池状态

self pool 17 / full OS 20 / excluded PPAC 3 —— 与存量清单一致（get_user_alphas count=10 为分页假象）。


### BE46b 结果

| 臂 | 外层/分组 | alpha | S | F | TO | sub | 2Y | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | neut·bucket10簇 | omamvpbJ | 0.25 | 0.06 | 0.34 | 0.16 | 1.03 | 3 |
| 2 | neut·bucket20簇 | rK7KL3x1 | 0.18 | 0.04 | 0.34 | 0.11 | 1.17 | 3 |
| 3 | neut·市值五分位桶 | 6XMX18kO | **1.50** | 0.79 | 0.24 | 0.63 | **1.57** | 4 |
| 4 | zscore·bucket10簇 | Jj8jmw9m | 0.17 | 0.04 | 0.34 | 0.10 | 0.79 | 3 |
| 5 | zscore(market)·内层bucket10 | npapoJE8 | -0.20 | -0.06 | 0.34 | -0.23 | 0.62 | 5 |

### 终审

- **聚类桶分组全灭**（0.17-0.25）：news×I7 信号价值存在于标准行业中性化框架内，数据驱动聚类摧毁它；
- **市值桶中性化 1.50**：基线 1.46 的 +0.04，2Y 1.57 优于基线——仍差 0.08；
- **天花板三角验证**：三个独立构造同顶 1.50-1.52（QP010j5W 外层 rank / YPaPX3JJ relevance / 6XMX18kO 市值桶）；
- **三档无改善成立**（BE14 1.52 → BE43b 1.52 → BE46b 1.50）——按用户「连续 ≥3 档无改善才算方向死」纪律，NEWS×I7 线正式方向死；
- D4 分组轴穷尽（标准轴 sector/industry/market + 聚类桶 10/20 + 市值桶 + 内层混合几何），判死档案升级为**七维穷尽**。

### 交付池状态（本轮结束时）

- 交付 11 颗不变（6 ACTIVE + 5 待授权）；
- **换防选项已备齐**：88NmN37X 全闸+全相关性干净（S1.79/F1.53/TO0.091/sub0.95/self0.5538/prod0.5541），可 1:1 替换 qM7KxkQV（属用户提交授权裁定范围）；
- 缺口 9 颗在用户约束集内维持结构性闭合判定。


## 五、BE47 补记（数据集空间 100% 闭合）

- PV 塔残余三数据集（continuation_score / intraday_pv_feats / pv109）探针全灭（S -0.53~0.42，sim JYxASTF50KcqR1eiHK5a2Y）；
- IS 池近失扫描（128 件）：exhausted 线外最高 S=0.79，无遗漏候选；
- **DEU D1 在用户约束集内可探明空间 = 0 剩余**——阻塞条件第三次确认（01:28 立案 / 02:21 / 02:37），唯一解锁路径仍是用户裁定（提交授权 / leading-gap 豁免 / 解冻 D0 或已点亮塔 / 修目标）。
