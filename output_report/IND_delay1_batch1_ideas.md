# IND / D1 / TOP500 — S1 字段理解与特征工程报告（批次 1）

**Dataset**: behavioral_signals
**Region**: IND
**Delay**: 1


**生成时间**: 2026-08-23 | **区域设置**: EQUITY / IND / TOP500 / delay=1
**用户约束**: 每条表达式只用 1-2 个字段；禁 `trade_when` / `add` / `multiply`；
prod_corr≥0.7 不提交；不同数据集策略间相关性 < 0.4。

---

## 0. 批次结论速览

| 数据集 | 类型 | 白名单字段数 | 优先级 | 核心故事 |
|---|---|---|---|---|
| model192 | MATRIX | 12 | P0 | CDS 信用风险变化 + 分析师修正 + 行业相对收益 |
| quant_factor_lib | VECTOR | 6 | P0 | 信用/违约因子库，极低竞争（116 alphas） |
| behavioral_signals | VECTOR | 5 | P1 | 行为金融外推偏差（曲率/显著性/连涨） |
| pv70 | VECTOR | 4 | P1 | 实体关系网络（新闻共提及/盈利联动），纯白空间 |
| news76 | VECTOR | 2 | P2 | 彭博新闻情感事件流 |

**降级**：`global_seasonal_model`（实为公司事件标志位/分类码，无连续信号）、
`analyst_earnings_ibes`（IND 实际字段为通用价格/收益数据，与 PV 同质）。

**全局预处理规则**：
- MATRIX 稀疏字段（模型填充类 `_di` 后缀）：`ts_backfill(F, 66)` 先行
- IND 胜绩结构模板（mdl177 配方迁移）：`rank(ts_rank(ts_backfill(F,66), 250))` 长窗 + 负权重方向
- VECTOR 字段：必须 `vec_*` 聚合（vec_avg/vec_count/vec_sum/vec_max）再进常规算子，否则 "rank does not support event inputs"
- EVENT 类字段禁 winsorize

---

## 1. model192（CDS Factor Data，101 字段，满覆盖，P0）

### 字段解构
亚太证券的信用违约互换（CDS）因子 + 基本面 + 分析师信号混合集。
核心叙事：**信用风险边际变化 → 股价未充分反应**（credit-equity lead-lag）。

### 字段白名单（12 个）与方向假设
| 字段 | 测什么 | 预处理 | 方向假设 |
|---|---|---|---|
| `mdl192_id_y5dpghcd5_sdc` | 5 年期 CDS 隐含违约概率 5 日变化 | ts_backfill→rank/ts_rank | 违约概率上升→负信号（做空） |
| `mdl192_id_y5dpghcm1_sdc` | 同上 1 个月变化 | 同上 | 同上，慢速版 |
| `mdl192_id_y1dpghcd1_sdc` | 1 年期违约概率日变化 | 同上 | 同上，快速版 |
| `mdl192_cds_pd5y_di` | 5 年违约概率水平 | ts_backfill→ts_rank 长窗 | 高水平→负 |
| `mdl192_id_mrspe_cf` | 分析师 EPS 修正幅度 | ts_backfill→rank | 正向修正→正信号 |
| `mdl192_fc_numrevy1_di` | FY1 分析师净修正数 | 同上 | 正修正→正 |
| `mdl192_fc_fqsurstd_di` | 季度盈利意外（标准化） | 同上 | PEAD：意外→漂移 |
| `mdl192_indrelrtn5d_di` | 5 日行业相对收益 | 同上 | 反转假设：负向 |
| `mdl192_indrelrtn4w_di` | 4 周行业相对收益 | 同上 | 动量/反转双测 |
| `mdl192_id_tni_ths` | 空头兴趣 | 同上 | 高空头→负 |
| `mdl192_id_tqe_sdc` | CDS 对股价敏感度 | 同上 | 方向待测 |
| `mdl192_altmanz_di` | Altman Z 信用分 | 同上 | 高分（安全）→正 |

### 概念（每式 1 字段）
1. **信用恶化反转**：`-rank(ts_rank(ts_backfill(mdl192_id_y5dpghcd5_sdc,66),250))` — 违约概率近期恶化最多的股票预期跑输
2. **分析师修正动量**：`rank(ts_zscore(ts_backfill(mdl192_id_mrspe_cf,66),126))` — 修正强度 z 分
3. **行业相对反转**：`-rank(ts_backfill(mdl192_indrelrtn5d_di,5))` — 短期超涨回归
4. **盈利意外漂移**：`rank(ts_decay_linear(ts_backfill(mdl192_fc_fqsurstd_di,66),63))`（若禁则退 ts_mean）

---

## 2. quant_factor_lib（信用因子库，32 字段全 VECTOR，cov 0.83，P0）

### 字段解构
CASSIE 信用风险模型套件：违约模型（Altman/CHS/Merton/Ohlson）+ 偿债压力测试 + 杠杆结构。
叙事：**资产负债表稳健性溢价的慢变体**——与 model192 的"快变信用边际"正交（同族不同频）。

### 字段白名单（6 个）
| 字段 | 测什么 | 聚合 | 方向 |
|---|---|---|---|
| `qfl_cassie_qes_cassie_impliedalpha` | 信用模型隐含预期超额收益 | vec_avg | 高→正（直接 alpha 信号） |
| `qfl_cassie_qes_cassie_score` | CASSIE 综合信用分 | vec_avg | 待测 |
| `qfl_cassie_model_altman_zscore` | 破产距离 | vec_avg | 高→正 |
| `qfl_cassie_qes_alter_insolvency_stress_1y` | 1 年破产压力分 | vec_avg | 高→负 |
| `qfl_cassie_convention_debt_mktcapital` | 债务/市值 | vec_avg | 高→负 |
| `qfl_cassie_convention_ocf_currliab` | 经营现金流/流动负债 | vec_avg | 高→正 |

### 概念
1. **隐含 alpha 直取**：`rank(vec_avg(qfl_cassie_qes_cassie_impliedalpha))` + ts_zscore(63) 平滑
2. **破产压力反向**：`-rank(ts_rank(vec_avg(...insolvency_stress_1y), 250))`
3. **现金流稳健**：`rank(ts_zscore(vec_avg(...ocf_currliab), 252))`

---

## 3. behavioral_signals（行为金融，7 字段全 VECTOR，cov 0.83，P1）

### 字段解构
投资者外推偏差度量族：价格路径形状如何诱发系统性过度反应。
叙事：**路径形状 → 外推偏差 → 可预测反转**。

### 字段白名单（5 个）
| 字段 | 测什么 | 聚合 | 方向 |
|---|---|---|---|
| `price_path_curvature_measure` | 价格路径凸性 | vec_avg | 凸（上弯）→过度外推→反转做空 |
| `visual_price_path_shape_score` | 路径在弦上方占比 | vec_avg | 同上 |
| `salience_weighted_return_score` | 显著性加权收益偏离 | vec_avg | 高→过度关注→反转 |
| `consecutive_return_streak_length` | 连涨/连跌长度（带符号） | vec_avg | 长连涨→反转 |
| `chronological_return_sequence_correlation` | 收益时序相关性 | vec_avg | 待测 |

### 概念
1. **凸性反转**：`-rank(vec_avg(price_path_curvature_measure))`
2. **显著性反转**：`-rank(ts_zscore(vec_avg(salience_weighted_return_score),63))`
3. **连涨衰竭**：`-rank(vec_avg(consecutive_return_streak_length))`

---

## 4. pv70（实体关系网络，33 字段全 VECTOR，cov 1.0，alphaCount=7，P1）

### 字段解构
Instrument1→Instrument2 事件驱动关系图（新闻共提及/IBES 盈利联动/目标价关联）。
叙事：**关系密度 = 注意力/联动度**；白空间极大（全平台仅 7 alpha）。

### 字段白名单（4 个）
| 字段 | 聚合 | 含义 |
|---|---|---|
| `pv70_news_score` | vec_count / vec_sum | 新闻关系数量与强度 |
| `pv70_ibeseps1_score_float` | vec_avg | 盈利联动强度（归一化） |
| `pv70_bbgnews_score_float` | vec_avg | 彭博新闻关系强度 |
| `pv70_ibesptg1_score_float` | vec_avg | 目标价联动强度 |

### 概念
1. **注意力溢价**：`rank(ts_zscore(vec_count(pv70_news_score),126))` — 关系密度上升=关注度上升
2. **联动强度**：`rank(vec_avg(pv70_ibeseps1_score_float))` — 方向待测
3. **注意变化**：`rank(ts_delta(vec_count(pv70_news_score),21))`（delta 若禁则用 ts_zscore 差分替代）

---

## 5. news76（彭博新闻情感，6 字段全 VECTOR，cov 0.99，P2）

### 字段白名单（2 个）
| 字段 | 聚合 | 含义 |
|---|---|---|
| `mws76_score` | vec_avg | 情感分（-1/0/1） |
| `mws76_confidence` | vec_avg | 市场波动概率置信度 |

### 概念
1. **日情感**：`rank(vec_avg(mws76_score))`
2. **置信加权情感**：情感×置信度需要 multiply（禁）→ 改单独用 `rank(vec_avg(mws76_confidence))` 测"高关注新闻"效应

---

## 6. 实现考量

- 全部 VECTOR 字段经 `vec_*` 聚合；EVENT 类不做 winsorize
- model192 `_di` 后缀字段为填充/回溯值，`ts_backfill` 已内置连续性，再套 66 日回填冗余但无害
- 方向不确定的字段（stockrating/tqe_sdc 等）用正负双方向探针
- 与已提交 4 颗（mdl177×3 + anl39）的相关性：本轮字段全部不同源，预期满足跨集 <0.4
- 每 10 次回测做多样性评估（算子/字段/骨架/预处理/收益来源）

## 7. 待验证假设

1. IND TOP500 信用-股票 lead-lag 是否成立（model192 违约概率变化领先股价？）
2. CASSIE impliedalpha 在新兴市场（印度）是否仍有定价效率缺口
3. 行为金融信号在高散户市场（印度）是否被放大