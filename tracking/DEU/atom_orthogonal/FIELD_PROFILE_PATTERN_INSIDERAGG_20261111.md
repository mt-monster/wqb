# 新增数据集字段画像：pattern_scores + insider_agg_matrix（2026-11-11 补漏）

> 目标第 2 条「逐数据集字段画像」补漏。两集在此前画像（FIELD_PROFILE_INDEX / *_fields.csv）中缺失。

## pattern_scores（PV 塔 · 未点亮）

- 字段数 504（平台 listing），类型 **MATRIX**（无需 vec_），覆盖 0.9647-0.9991（DEU 全场最高档）
- 用户 165 / alphas 277 / valueScore 5
- 字段语义：当前 K 线序列与经典图表形态的相似度得分（lookback 60/120，mean/median/max/std/q95/dynamic 六种统计量）
- 形态家族：breakaway_gap up/down、common_gap up/down、asc_triangle（含 down 变体）、
  symmetrical_triangle up/down、V_reversal bottom/top、falling_wedge、rising_wedge
- 高使用字段：breakaway_gap_up_dynamic_simscore_lookback60 (u9/a18)、
  avg_similarity_downward_symmetrical_triangle (u11/a11)、avg_similarity_v_reversal_bottom (u6/a7)
- 机制先验：Lo-Mamaysky-Wang 2000；论坛 continuation_score 生产级帖（同类数据）
- 矩先验：相似度是「中速变量」——水平价差（多空形态对冲）与 Δ22 形成动量双探针

## insider_agg_matrix（INSIDERS 塔 · 未点亮）

- 字段数 34，类型 MATRIX，覆盖 0.534（事件聚合面）/ 1.0（directional_indicator/2）
- 用户 96 / alphas 182 / valueScore 4
- 字段四族：
  1. 方向指标：directional_indicator (cov 1.0, u36/a52)、directional_indicator_2 (cov 1.0, u15/a23)
  2. 流量：total/avg × buy/sell × {全部董事, 高管(top), 直接交易(secondary)}
  3. 显著性：significant_value_1-4、top/directional_significant_value_1-4
  4. 注记字段（text）若干
- 与 insiders1（事件明细 VECTOR）互补：agg 版已是日频 MATRIX，天然低换手
- 机制先验：Cohen-Malloy-Pomorski 2012（内部人购买信息含量）、Lakonishok-Lee 2001
- 矩先验：流量类用 66 日均值水平面；方向指标 cov 1.0 可裸用

## socialmedia39（SOCIALMEDIA 塔）

- 单字段 scl39_top5_people_also_watch_ticker_ii（VECTOR，cov 0.275，u87/a148）
- 语义为「共同浏览邻居 ticker 的 Atlas ID 列表」——ID 无数值含义，vec_avg 无意义、vec_count≤5 近常数
- **判定：数值聚合不可用，跳过回测**（画像级排除，非判死）

## fundamental 侧勘误（对照 atom_fundamental 终审 2026-11-07）

- fnd45 天花板 0.99 / fnd90 1.02（2Y 内禀死）/ fnd22 ESG 0.48 / fnd17·86·93·72·89 历史探针全灭
- ⇒ fundamental 塔在 DEU 可投面 = fnd6 oiadpq 单点（槽位已被 Wje5K71x 占用），无新增空间（维持旧结论）
