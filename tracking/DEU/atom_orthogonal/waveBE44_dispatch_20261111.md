# BE44 派发：pattern_scores（PV 塔未点亮）+ insider_agg_matrix（INSIDERS 塔未点亮）首批探针（2026-11-11）

## 一、为什么是这两个数据集（普查补漏）

对 DEU D1 全 172 集按 category 枚举普查 + 对照 atom_fundamental 终审（11-07）：
- fundamental 侧 fnd17/22/45/86/89/90/93/72 全部已在 11-07 战役实测判死（0.48-1.02）；
- **pattern_scores（PV 塔）：cov 0.9888 = DEU 全场最高覆盖，504 字段，165 用户 277 alphas，
  本战役从未入册、从未回测**——master 总表漏项；
- **insider_agg_matrix（INSIDERS 塔）：cov 0.534-1.0，34 字段 MATRIX，
  directional_indicator 字段 cov 1.0 / u36 / a52 平台重度使用**——同样漏项；
- socialmedia39 单字段是「共同浏览邻居 ticker ID 列表」，数值聚合无经济含义（vec_count≈常数≤5），记不可用。

塔位合规：PV 塔与 INSIDERS 塔 OS 均为 0 颗（未点亮）→ 按用户 11-11「已点亮塔不再投入」指令允许投入。
两腿均为单数据集 ATOM 探针，无禁混风险。

## 二、模板依据（论坛+论文）

- 论坛 2026-09 生产级帖【K线形态Peak统计量的做空因子化】（continuation_score，560 形态相似度字段）：
  形态相似度类数据在平台有成熟 ATOM 玩法；
- 学术：Lo-Mamaysky-Wang 2000（图表形态含增量预测信息）；实盘突破胜率 ~59.6%；
- 内部人流量：Lakonishok-Lee 2001 / Cohen-Malloy-Pomorski 2012（内部人净买入预测收益）。

## 三、派发内容（sim 2lLky1c5M4gqcIe11fUlGsGH，10 臂）

设置同 BE43a。全部 MATRIX 字段（无需 vec_），算子 3-7/臂（精简口径）。

| 臂 | 数据集 | 模板 | 机制 |
|---|---|---|---|
| 1 | pattern_scores | 向上突破缺口相似度 − 向下（sector rank 差） | 形态方向价差 |
| 2 | pattern_scores | (V反转底+下降楔) − 上升楔 | 多空形态复合 |
| 3 | pattern_scores | 上升三角形上破 − 下破 | 突破方向分解 |
| 4 | pattern_scores | 突破缺口相似度 Δ22 | 形态形成动量 |
| 5 | insider_agg | directional_indicator 平滑 rank | 内部人活动方向（cov 1.0） |
| 6 | insider_agg | 买入股数 rank − 卖出股数 rank | 内部人净流量 |
| 7 | insider_agg | 高管买入/(买+卖) 比值 | 知情者（高管）净买占比 |
| 8 | insider_agg | directional_indicator_2 裸 rank | 增强方向指标（cov 1.0） |
| 9 | pattern_scores | 下降楔相似度水平 rank | 单形态水平面 |
| 10 | insider_agg | 直接交易买−卖均值价差 | 二级市场直接交易净额 |

## 四、探针纪律

探针臂命中 S≥1.2 才升级满波（≥10 结构互异模板）；全灭则记「探针级判死」并归档。
注意 ts_target_tvr_decay/_hump 在 DEU 为负杠杆（priors 实证），本波全部不用。
