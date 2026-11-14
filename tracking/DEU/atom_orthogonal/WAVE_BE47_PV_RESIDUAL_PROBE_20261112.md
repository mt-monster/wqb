# BE47 判决：PV 塔残余三数据集探针死，数据集空间 100% 闭合（2026-11-12 凌晨）

## 一、6 臂结果（sim JYxASTF50KcqR1eiHK5a2Y，complete=6）

| 臂 | 数据集 | 机制 | alpha | S | F | TO | sub | 2Y |
|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | continuation_score | 上升通道相似度水平 | 2r5rRY26 | -0.07 | -0.01 | 0.31 | 0.05 | 0.70 |
| 2 | continuation_score | 形态离散度 Δ22 | RReRYgoj | 0.42 | 0.13 | 0.20 | 0.45 | 1.08 |
| 3 | intraday_pv_feats | ask/VWAP 比值 | gJaJK25K | 0.31 | 0.12 | 0.08 | -0.13 | -0.45 |
| 4 | intraday_pv_feats | bid/ask 比值 | e7a7KjPO | -0.02 | 0.00 | 0.03 | 0.14 | 0.96 |
| 5 | pv109 | YTM 水平（信用回避） | YPaPmeOv | -0.53 | -0.28 | 0.03 | 0.28 | -1.06 |
| 6 | pv109 | 债券价格动量 | kqaqXAMg | 0.24 | 0.08 | 0.11 | -0.13 | 1.19 |

## 二、判定

- continuation_score：与 pattern_scores 同族同命（论坛 ASI 帖不迁移）；
- intraday_pv_feats：微结构比值无横截面方向信息（同 risk88「描述性无方向」判据）；
- pv109：债券报价面 DEU TOP500 不可行；
- cov=0 → lc<100 先验 4/4（f89/f72/risk72/本轮）。

## 三、空间闭合声明

172 数据集全部落格：实测 / 探针关闭（本轮 3 集）/ 画像排除（socialmedia39）/ 约束冻结（已点亮塔、D0、TOP500 外）。
**DEU D1 在用户约束集内可探明空间 = 0 剩余。**

## 四、IS 池近失扫描（同轮）

128 件全量，前 100 最新件逐一核对：已知 exhausted 线之外最高 S = 0.79（MP6POZar，news18）。无遗漏近失候选。
