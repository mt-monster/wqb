# IND / sentiment21 全字段静态画像 · 2026-11-14

> 人工撰写审计 → `reports/dataset_experience/`。**100% 字段覆盖，不抽样**：MCP `get_datafields` 实读 `count=105 / platform_count=105 / complete=True`。事实源（机器读）= `tracking/IND/reference/ind_sentiment21_fields.json`。

- category=SENTIMENT｜当季塔=1（未亮）｜覆盖率=0.9681｜字段=105｜类型分布={'MATRIX': 105, 'V_UNTESTED': 90, 'V_DEAD_TURNOVER': 9, 'V_DEAD': 2, 'V_ALIVE': 4}

## 0. 取数口径与三条须知

1. **工具坑（本轮实测）**：`get_datafields(max_fields=null)` 显式传参会触发 `max_fields_cap`，每集只返 1 条且 `complete=false`。正确用法 = **不传 `max_fields`**（dataset-scoped 缺省不限量）或传 ≥ `platform_count` 的整数；同时必须 `filter_sharpe=False`，否则按 OS/IS Sharpe<0 过滤字段 = 隐性抽样。
2. `coverage` 不可信：GBR 2026-11-09 实测与探针 `longCount+shortCount` 有偏差；VECTOR 字段的 coverage 是**历史累计覆盖**，非任意时点覆盖（IND `news29` 判死即因 8/8 空持仓）。本表对 VECTOR 一律在「分布特征」列标稀疏风险。
3. MCP 返回**不含** `updateCount` / 更新频率 / 分布形态；IND 不在离线体检包七区（ASI/CHN/EUR/GLB/JPN/KOR/USA）且本机 `tracking/mining/field_inspect_ind_*.json` 零命中。故「更新频率」「分布特征」列由字段语义 + DB `field_profile_full.freq_hint` 静态推定，逐条标 `[inferred]`；**在线六法最小仿真集只对入选主信号字段做**，不对 185 字段逐字段跑（Q2 口径）。

## 1. 机制风险（选集证据修订）

未亮塔 1/3；⚠ 白名单写入触发 `dead_intersection` high 告警：跨 4 区（EUR/GLB/KOR/USA）判死；IND 本地 news/sentiment 族亦多证枯竭 → 标 VALIDATE_FIRST，首探只做验证性 2 条探针，无信号即换 `analyst11`。

## 2. 全字段画像（8 列，105 字段无空行）

| # | field | type | coverage | userCount | alphaCount | 更新频率 | 分布特征 | 可用性 | 潜在 alpha 适用性 |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | `snt21_2neg_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 2 | `snt21_2neg_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（未登记 verdict） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 3 | `snt21_2neg_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 4 | `snt21_2neg_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 5 | `snt21_2neg_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 6 | `snt21_2neg_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 7 | `snt21_2neg_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 8 | `snt21_2neut_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 9 | `snt21_2neut_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 10 | `snt21_2neut_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 11 | `snt21_2neut_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 12 | `snt21_2neut_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 13 | `snt21_2neut_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 14 | `snt21_2neut_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 15 | `snt21_2pos_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 16 | `snt21_2pos_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（未登记 verdict） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 17 | `snt21_2pos_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 不可用（实测判死）；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） → 排除 |
| 18 | `snt21_2pos_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 19 | `snt21_2pos_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（未登记 verdict） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 20 | `snt21_2pos_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 21 | `snt21_2pos_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 22 | `snt21_3neg_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 23 | `snt21_3neg_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（未登记 verdict） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 24 | `snt21_3neg_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 25 | `snt21_3neg_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 26 | `snt21_3neg_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 27 | `snt21_3neg_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 28 | `snt21_3neg_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 29 | `snt21_3neut_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 30 | `snt21_3neut_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 31 | `snt21_3neut_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 32 | `snt21_3neut_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 33 | `snt21_3neut_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 34 | `snt21_3neut_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 35 | `snt21_3neut_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 36 | `snt21_3pos_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 37 | `snt21_3pos_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 38 | `snt21_3pos_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（未登记 verdict） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 39 | `snt21_3pos_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（未登记 verdict） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 40 | `snt21_3pos_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 41 | `snt21_3pos_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 42 | `snt21_3pos_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 不可用（实测判死）；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） → 排除 |
| 43 | `snt21_4neg_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 44 | `snt21_4neg_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 45 | `snt21_4neg_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 46 | `snt21_4neg_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（未登记 verdict） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 47 | `snt21_4neg_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 48 | `snt21_4neg_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 49 | `snt21_4neg_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 50 | `snt21_4neut_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 51 | `snt21_4neut_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 52 | `snt21_4neut_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（未登记 verdict） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 53 | `snt21_4neut_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 54 | `snt21_4neut_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 55 | `snt21_4neut_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 56 | `snt21_4neut_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 57 | `snt21_4pos_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 58 | `snt21_4pos_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 59 | `snt21_4pos_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（未登记 verdict） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 60 | `snt21_4pos_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 61 | `snt21_4pos_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 62 | `snt21_4pos_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 63 | `snt21_4pos_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 64 | `snt21_5neg_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 65 | `snt21_5neg_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 66 | `snt21_5neg_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 67 | `snt21_5neg_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 68 | `snt21_5neg_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 69 | `snt21_5neg_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 70 | `snt21_5neg_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 71 | `snt21_5neut_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 72 | `snt21_5neut_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 73 | `snt21_5neut_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 74 | `snt21_5neut_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 75 | `snt21_5neut_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 76 | `snt21_5neut_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 77 | `snt21_5neut_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 78 | `snt21_5pos_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 79 | `snt21_5pos_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日内（分钟/逐笔） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 80 | `snt21_5pos_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 81 | `snt21_5pos_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 82 | `snt21_5pos_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 83 | `snt21_5pos_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 84 | `snt21_5pos_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 85 | `snt21_neg_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 86 | `snt21_neg_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 87 | `snt21_neg_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 88 | `snt21_neg_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 89 | `snt21_neg_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 90 | `snt21_neg_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 91 | `snt21_neg_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 92 | `snt21_neut_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 93 | `snt21_neut_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 94 | `snt21_neut_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 95 | `snt21_neut_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 96 | `snt21_neut_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 97 | `snt21_neut_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 98 | `snt21_neut_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 99 | `snt21_pos_conf_low` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 100 | `snt21_pos_conf_up` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 101 | `snt21_pos_max` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 102 | `snt21_pos_mean` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 103 | `snt21_pos_median` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |
| 104 | `snt21_pos_min` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | spread / 需 winsorize 复核 [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 105 | `snt21_pos_std` | MATRIX | 0.9681 | n/a [inferred] | n/a [inferred] | 日频 (DB field_profile_full) | 右偏、零膨胀（离散度/置信区间量） [inferred] | 待测（无历史回测，首探判定） | FE 步2：ts_mean(22) 长窗平滑 + trade_when 门控；机制=注意力/分歧度（禁情感水平族） |

## 3. 判死字段通道（不生成表达式）

共 2 / 105 字段进黑名单：`snt21_2pos_max`, `snt21_3pos_std`


## 4. 主信号候选（交 FE 步 2）

共 4 字段：`snt21_2pos_mean` (bestS=1.69, 2Y=1.78), `snt21_4pos_mean` (bestS=1.74, 2Y=2.07), `snt21_5pos_mean` (bestS=1.7, 2Y=1.8), `snt21_pos_mean` (bestS=3.01, 2Y=1.93)


## 5. 在线六法补测清单（仅主信号字段）

一批 6 条：`x`｜`x!=0`｜`ts_std_dev(x,N)!=0` N=5/22/66｜`abs(x)>1`；扩展 ≤8 条：`abs>X` X=10/100、`ts_mean(x,252)>X`、`zscore>k`。
设置 `Neutralization=None / Decay=0 / Test Period=P0Y0M0D`，读 `longCount/shortCount`；VECTOR 先 `vec_avg`。
工具 = `mcp__wq-brain-http__create_multi_simulation`（2–10 条，连坐语义），发批前 `preflight_expressions`。
