# EUR × sentiment21 字段画像（2026-11-09）

> 210/210 全量（complete=true）；AI Sentiment Score Data（AI 情绪分统计族）
> 塔位：SENTIMENT(×1.4，2/3)；拥挤度：aC 705 / uC 325；os_is 0.5223

## 一、字段结构
全部为 **pos/neg/neutral 三类情绪分 × {mean/median/min/max/std/conf_low/conf_up} × 时间窗（2d/3d/4d/5d/6d…）** 的统计量矩阵（MATRIX，cov 0.9317-1.0）。字段高度规整：snt21_{窗}{类}{统计量}[_{版本号}]。

## 二、判定
1. **极性统计族 = 家族判死**（news46 极性 77 条 S<0.6 + sentiment21 自身历史 14 条 × 两轴 0.36 + 极性机制已在 EUR 多集证伪）
2. 唯一非极性读数 = **std 类**（情绪分歧度：2neg_std uC 49/aC 64 最热）——分歧度≠极性方向，学术先验（意见分歧→高估→反转）存在但 sentiment 塔已判死过两次
3. **判定：极性族禁做；std 分歧度留档为唯一未试读数（低先验）**——若投仅 1 臂探针：multiply(-1, group_rank(ts_zscore(snt21_2neg_std,22),subindustry))
