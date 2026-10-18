# USA 字段画像总册：字段画像 × 适用模板 × 回测指标

> **定位**：把 2026-10 两轮战役（Analyst 14 波 + 换类别 6 波）**挖过的每个字段族**沉淀为可复用的三段式档案。
> 与 `_usa-mining-playbook-20261018.md` 的分工：**那本是"怎么想"（机制/铁律），本册是"每个字段长什么样、跑出什么数"**。
> **as_of**：2026-10-18 ｜ **口径**：全部数值来自平台 `get_alpha_details` / `get_alpha_yearly_stats` / `check_correlation(refresh=True)`。
> **怎么读**：先看 §1 的「判定口径」（含本轮最有用的 `risk_neutralized_sharpe` 诊断）→ §2 按数据集查字段 → §3 选模板 → §4 对照指标预期。

---

## 1. 判定口径（读本册前必看）

| 指标 | 含义 | 阈值 / 用法 |
|---|---|---|
| `coverage` | 字段覆盖率 | <0.5 视为毒字段；0.5–0.65 换手低是优势 |
| `alphaCount` | 该字段已被多少 alpha 用过 | **<200 视为低拥挤**（prod 有戏）；>1000 慎重 |
| `type` | MATRIX / VECTOR | VECTOR 必须 `vec_avg` 归约 |
| **`risk_neutralized_sharpe`** | **剥离风险因子后的 Sharpe** | **本轮最强诊断**：<0.3 ⇒ 纯风格 beta，假 alpha，直接判死；>1.0 ⇒ 真 alpha，prod 风险低 |
| `TO` | 换手 | 平台闸 0.01–0.4；<0.01 撞 LOW_TURNOVER |
| `prod` | 与生产池最大日收益相关 | **≥0.7 不可提交（红线）** |

> ★★ **新铁律（本轮实测）**：IS 指标 S/F/2Y 全过 ≠ 能交付。**必先看 `risk_neutralized_sharpe`**——
> NEMO 网络动量 S 0.75–0.90 但 risk-neut 仅 0.07–0.23（纯 beta），Wikipedia 注意力 S 1.35 但 risk-neut 1.40（真 alpha）。

---

## 2. 字段画像（按数据集）

### 2.1 Analyst 类别（24 个数据集，仅列挖过的）

#### analyst44（300 字段，全 VECTOR，ANALYST 塔 1.2）★已交付 2 颗

| 族 | 代表字段 | cov | αC | 更新 | 判定 |
|---|---|---:|---:|---|---|
| 事件级修正配对 | `anl44_2_eps_value` / `_prevalue` | 0.958 / 0.953 | 0 | 事件级 | ★唯一强腿（S 1.77→背离 1.81） |
| 同族其他 16 个配对 | sales/netprofit/ebit/ebitda/pretax… | 0.21–0.957 | 0 | 事件级 | 判死（同财报口径共线） |
| BEst 共识 | `anl44_best_eps_4wk_up/dn` | 0.877 | 22–27 | 日更 | 判死（广度族 S ≤0.30） |
| 分歧 | `anl44_best_eps_stddev` | 0.857 | 39 | 日更 | 弱（单独 S 1.05） |
| 极拥挤 | `anl44_best_pe_ratio` | — | **399** | 日更 | 判死（prod 0.93） |

**模板**：T1 修正率 → T2 背离（eps−sales）→ T3 加速度 → T4 秩背离。详见 `_usa-mining-playbook-20261018.md` §2。

#### analyst_consensus（3424 字段，VECTOR，ANALYST 塔 1.2）★本轮主战场

| 族 | 代表字段 | cov | 机制 | 判定 |
|---|---|---:|---|---|
| 当前均值 | `mean_estimate_eps_annual12_3` | 0.9779 | 水平 | 单独弱（S 0.86） |
| **4 周前均值** | `mean_estimate_four_weeks_prior_eps_annual12_3` | 0.9699 | **修正/惊喜配对** | ★核心 |
| 3 月前均值 | `mean_estimate_three_months_prior_eps_annual12_3` | 0.9607 | 长窗修正 | 同上 |
| **实际值** | `actual_value_eps_annual12` | 0.9521 | **惊喜 = actual − 4wk 前预期** | ★★最强（S 1.86） |
| 极值 | `max_estimate_eps_annual12_3` / `min_…` | 0.9779 | 高低分歧 | 判死（S 0.63） |
| 分歧度 | `stddev_estimate_eps_annual12_3` | 0.9565 | 分歧水平 | 判死（S 0.69） |
| 其他指标配对 | revenue / pretax_reported / roe / capex / netdebt / nav / fcf / dps / bvps | 0.45–0.97 | 同结构换指标 | 弱（S 0.85–1.24） |

★★★ **实测结论**：**「已实现惊喜」(actual vs 4wk前预期) 远强于「修正率」(current vs 4wk前预期)** —— S 1.79–1.86 vs 0.86。
且 **CROWDING 是本集的 IS 增益器**（TO 0.053→0.012、margin 20→128bp、SUB 0.90→1.14），但 **prod 不降**。

#### analyst_factor_signals（922 字段，全 MATRIX，ANALYST 塔 1.2）★★ 本轮最富矿

193 个 cov≥0.85 字段，10+ 类独立机制：

| 机制 | 代表字段 | cov | 最优读数 | 判定 |
|---|---|---:|---|---|
| **修正幅度** | `eps_revision_magnitude` | 0.9477 | **S 1.94 / F 1.26 / SUB 1.09**（subindustry 轴）★ | IS 全过、prod 0.8068 |
| 修正幅度（换指标） | netprofit / pprofit / ebit / revenue / nav / interest_expense / depr_amort / ebitda | 0.86–0.95 | S 1.10–1.58 | 弱于 eps；NAV 1.58/F 0.95 |
| **幅度背离** | `eps_revision_magnitude − netprofit_revision_magnitude` | — | S 1.79 / F 1.17 | SUB 0.49 ❌ |
| **偏度** | `eps_y1_estimate_skewness` | 0.9521 | S 1.74 / F 1.02 | 2Y 0.89 ❌ |
| **变异系数** | `eps_y1_estimate_coeff_var` | 0.9087 | S 1.71 / F 1.05 | SUB 0.36 ❌ |
| 趋势斜率 | `eps_estimate_trend_slope_1yr/2yr/3yr` | 0.878–0.930 | S 1.45 | ❌ |
| 惊喜标准差 | `eps_surprise_stddev` | 0.9098 | S 1.51 | ❌ |
| 其他未测 | 不对称度 / CAGR / QoQ·YoY 增长 / zscore / 3mo 修正率 / trailing_4q | 0.85–0.95 | — | 待测 |

#### analyst_revision_horizons（1095 字段，MATRIX，**MODEL 塔 1.3**）

| 族 | 代表字段 | cov | 最优读数 | 判定 |
|---|---|---:|---|---|
| 30/90d 修正 | `avg_estimate_change_pct_f12m_eps_30d_short_3` / `_90d_medium_3` | 0.983–0.996 | S 1.20 / 1.34（2Y 2.41/2.50 但 SUB 0.29/0.34） | ❌ |
| SmartEstimate 预测惊喜 | `predicted_surprise_pct_quarterly_eps_short_2` | 0.9676 | S 1.35（2Y 0.79） | ❌ |
| 已实现惊喜 | `pct_diff_actual_vs_predicted_quarterly_eps_short` | 0.9616 | S 0.81 | ❌ |

#### 其他 Analyst 集（挖过但判死）

| 数据集 | 字段/机制 | 读数 | 死因 |
|---|---|---|---|
| analyst_chart_cnn | `img_cnn_feature1_us_ibes_1_d1`（CNN 图像特征，cov 1.0，aC 低） | S 1.55 / F 0.92 / SUB 0.79 / TO 0.021 | S/F 差一档；**prod 0.8064**；`ts_av_diff` 会抹平（S→0.01） |
| analyst82 | `anl82_delta_epsq_q1_predict`（预测值，cov 1.0） | S 0.86 | 弱 |
| analyst16 | `anl16_sranarecstock1through5t12`（评级 1–5，cov 0.994） | S 0.82 / TO 0.271 | 弱 + ts_delta 撞 CW |
| analyst11 | `overall_sustainability_score`（ESG，cov 0.843） | S 0.62 | 弱 |
| analyst15 | `anl15_sal_ind_12_m_1m_chg`（GICS 组级广播，cov 0.994） | S 0.33 | 组内同值 ⇒ 无截面信息 |
| analyst7 | 滞后窗口配对（cov 恒 0.5） | S ≤0.95 | 过平滑 |

### 2.2 other / macro / news 类别（本轮换类别试挖）

| 数据集 | 字段 | cov | aC | 读数 | 判定 |
|---|---|---:|---:|---|---|
| **other545 NEMO** | `oth545_score` / `pln_omen` / `mpd`（网络动量，VECTOR） | 0.805 | 5–12 | S 0.75–0.90，**risk-neut 0.07–0.23** | ✗ 纯风格 beta |
| macro63 指数成员 | `mcr63_ldi_membership`（0/1 标志） | 1.0 | 147 | `ts_delta` S **−0.30** | ✗ 指数效应为负且弱（可 reverse 但 S 0.30） |
| **other571 Wikipedia** | `views7d/28d/84d` + 设备/时段拆分（MATRIX） | 0.54–0.60 | 2–80 | **S 上限 1.35 / F 0.95 / SUB 0.97，risk-neut 1.40** | ✗ 真 alpha 但强度不够 |
| news_sentiment_nlp | VADER/TextBlob 情绪、可读性、主观性、句间方差（VECTOR） | 0.995 | **0–9** | S 0.75–1.10，**TO 0.43–0.44** | ✗ 太快（日更头条） |
| fundamental14 董事变动 | `fnd14_*`（角色/地址编码） | 0.886 | 7574 | — | 编码型字段，FASTEXPR 不适 |
| other699 散户交易 | `oth699_sharestraded`（正买负卖）等 | 0.96–1.0 | 3–34 | — | 多为元数据，未测 |

---

## 3. 适用模板（按字段形态选）

| 模板 | 骨架 | 适用字段画像 | 实测 |
|---|---|---|---|
| **T1 修正率** | `quantile(group_rank(ts_av_diff(divide(sub(v(F),v(Fpre)),add(...)), W), AXIS))` | 事件级 value/prevalue 配对 | analyst44 eps S 1.77 |
| **T2 背离** | `subtract(T1(eps), T1(sales))` | 两个不同口径的修正率 | S 1.64–1.94 |
| **T3 加速度** | `ts_delta(T2, 252)` | 同上 | 2Y 2.19–2.21 |
| **T4 秩背离** | `subtract(rank(eps_rev), rank(sales_rev))` | 同上 | S 1.61–1.76 |
| **T5 惊喜** | `divide(sub(actual, prior_est), add(...))` | 有 actual + 4wk 前预期 | **S 1.79–1.86（最强）** |
| **T6 幅度/偏度** | `quantile(group_rank(ts_av_diff(<factor>, 252), subindustry))` | analyst_factor_signals 族 | S 1.94 |
| **T7 注意力** | `quantile(group_rank(ts_rank(<views>, 252), industry))` | 浏览量/关注度 | S 1.35（上限） |
| **T8 同集集成（❌ 不得作为主模板）** | `add(ts_rank(F1,252), ts_rank(F2,252))`（F1/F2 同数据集） | 同集两相关字段 | 实测仅边际提升（1.34→1.35）；且 **toolkit/skill_lint 的结构闸会把任何「双信号腿 add」判为 `equal_weight_leg_add`（该闸不看数据集）⇒ 派发前会被拦，不得使用** |

### 3.1 通用杠杆（本轮新增）

| 杠杆 | 效果 | 出处 |
|---|---|---|
| **neutralization 选择** | analyst44 背离：RAM/CROWDING 破 prod（0.70→0.65）；analyst_consensus 惊喜：CROWDING **抬** IS 但 prod 不降 | 逐族实测 |
| **轴选择** | `subindustry` 让 `eps_revision_magnitude` SUB 0.70→**1.09**；但对变异系数/NAV 无效（0.36–0.51）⇒ **SUB 是字段特异** | 本轮 |
| **hump 有前提** | 慢信号（views/attention）加 hump 会把 TO 压破 0.01 ⇒ **TO<0.02 的慢集禁用 hump** | 本轮 |
| **decay** | USA 越小 S 越高，但 TO 上升会伤 F：decay 3→F 0.94→0.78；**decay 5 是注意力族甜点** | 本轮 |
| `risk_neutralized_sharpe` | 选信号时先看它：<0.3 直接弃 | 本轮 |

---

## 4. 回测结果及指标

### 4.1 已交付（ACTIVE）

| alpha | 数据集 | 机制 | S | F | 2Y | SUB | TO | prod | self |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `gJWoaJqv` | analyst44 | T3 加速度/RAM/market/504/d20 | 1.74 | 1.27 | 2.21 | 0.86 | 0.101 | 0.6978 | 0.5803 |
| `kqJLawqP` | analyst44 | T4 秩背离/CROWDING/market/756 | 1.61 | 1.11 | 1.62 | 0.84 | 0.096 | 0.6757 | 0.6445 |

### 4.2 本轮 IS 八闸全过但 prod 拦截（5 条，全部留池待 prod 回落）

| alpha | 数据集/机制 | S | F | 2Y | SUB | TO | **prod** |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `88vaY1Jq` | factor_signals/修正幅度/subindustry | **1.94** | **1.26** | 1.59 | **1.09** | 0.0121 | **0.8068** |
| `A1QgNQZY` | consensus/EPS 惊喜/CROWDING/252 | 1.86 | 1.45 | 2.48 | 1.14 | 0.0118 | 0.8476 |
| `A1Qg0XmR` | consensus/EPS 惊喜/RAM/252 | 1.79 | 1.29 | 2.56 | 0.90 | 0.0526 | 0.8484 |
| `JjPgQgqe` | consensus/惊喜背离 | 1.72 | 1.33 | 2.22 | 1.16 | 0.0121 | 0.8673 |
| `Vkd2adjb` | consensus/EPS 惊喜/CROWDING/504 | 1.72 | 1.28 | 2.21 | 0.91 | 0.0114 | 0.8532 |

### 4.3 差一闸（近失，附缺口）

| alpha | 数据集/机制 | S | F | 2Y | SUB | 缺口 |
|---|---|---|---:|---:|---:|---:|---|
| `ZYmjrJ3Z` | other571/7d+移动端集成 | 1.35 | 0.95 | 1.52 | 0.97 | S −0.23 |
| `zqr5OqvG` | other571/ts_rank 7d | 1.34 | 0.94 | 1.48 | 0.95 | S −0.24 |
| `qMEnkANj` | factor_signals/NAV 修正 | 1.58 | **0.95** | 1.88 | 0.73 | F −0.05 |
| `mLYq2qj1` | factor_signals/幅度背离/industry | 1.79 | 1.17 | 1.86 | 0.49 | SUB −0.29 |
| `akVNX83O` | factor_signals/变异系数 | 1.71 | 1.05 | 1.83 | 0.36 | SUB −0.38 |
| `JjPgPvqe` | factor_signals/偏度 | 1.74 | 1.02 | **0.89** | 0.81 | 2Y −0.69 |
| `rKdJ7rwJ` | factor_signals/修正幅度/industry | 1.74 | 1.14 | 1.99 | 0.70 | SUB −0.05 |
| `MP0bXx8k` | chart_cnn/图像特征 | 1.55 | 0.92 | 1.74 | 0.79 | S −0.03 / F −0.08 |

### 4.4 判死清单（勿重试）

**Analyst**：breadth 族、17 配对中非 eps 的 16 个、dispersion 单独、horizon gap、median−mean、lastactvalue 三级、事件流−共识差、analyst7 全族、`ts_regression`（全零）、`numest`/`4wk_chg`（TO<0.01）、analyst15 组级广播、ESG/评级/CNN 水平值。
**跨类别**：other545 NEMO（risk-neut 0.07–0.23）、macro63 指数成员、news_sentiment_nlp（TO 0.44）、fundamental14（编码字段）。
**算子**：`ts_av_diff` 会抹平 embedding/CNN 类字段（S 1.55→0.01）；`ts_delta` 用在 1–100 跳变评级会撞 CW（0.387>0.1）。

---

## 5. 三条硬结论（写进选字段的第一屏）

1. **先看 `risk_neutralized_sharpe` 再花仿真**：<0.3 的是风格 beta，IS 再好看也不会有 prod 之外的未来。
2. **强度天花板由"信息内容"决定，不由变换决定**：Wikipedia 注意力怎么变换都停在 S 1.35；EPS 惊喜一次就把 S 做到 1.86。
3. **prod 由"是否被生产池挖过"决定**：同族换窗口/中性化/轴只能动 ±0.03；**唯一有效的是换到没人挖过的信息**（如 analyst_factor_signals 的修正幅度 → prod 0.807 vs 惊喜族 0.85）。

---

## 6. 追记（2026-10-18 19:00–20:00）：换类别第二轮 5 个数据集

| 数据集 | 字段 / 机制 | cov | aC | 读数 | 判定 |
|---|---|---:|---:|---|---|
| **pv115** Trading Data | `all_sv/all_tv`（做空占比，**反向**） | 1.0 | 57/140 | **S 1.67 / SUB 1.67**（d5）｜**F 0.60（TO 0.41）**｜**2Y 0.60**；d20：S 1.44/F 0.77/TO 0.16/**2Y 0.71** | ✗ **2Y 结构性衰减**（近年被套利），两种 decay 都 0.6–0.75 |
| pv115 | `scc_qdsn/all_tv`（收盘集合竞价占比） | 0.897 | 21 | S −0.39 | ✗ |
| **equity_kpi_forecast** | `prior_beat_count`（过去 12 季 beat 次数） | 0.367 | 7 | S **1.66** / F **1.38** / 2Y 0.97 / SUB 0.78 | ✗ **CONCENTRATED_WEIGHT 0.203 > 0.1**（与符号无关，反转救不了） |
| equity_kpi_forecast | `forecast_consensus_surprise_percent`（第三方模型 OdinUltra 预测惊喜，aC **2**） | 0.380 | 2 | S 1.40 / F 1.08 / **SUB 0.59（限 0.61）** / 2Y 1.08 | ✗ SUB 差 0.02，2Y 差 0.50 |

### 新增判据

1. **`CONCENTRATED_WEIGHT` 是"死的"，`2Y` 衰减也是"死的"**：前者与信号符号无关（反转无效）；后者若在多个 decay 档都低（0.60/0.71），说明是**信息被套利**而非参数问题。
2. **反向信号的完整检查清单**（本轮 pv115 实证）：`S`/`SUB`/`2Y` 会随符号翻转，`CONCENTRATED_WEIGHT`/`prod`/`self` **不会** ⇒ 反转前先看 CW 与 prod，否则白跑一批。
3. **TO 对 F 的杠杆被高估**：pv115 把 TO 从 0.41 压到 0.16（decay 20），F 从 0.60 只升到 0.77，同时 S 从 1.67 掉到 1.44、2Y 从 0.60 掉到 0.71 ⇒ **降 TO 与保 S 双输时，说明信号速度与闸门不匹配，放弃**。

### 今日换类别总账

| 方向 | 最好读数 | 死因 |
|---|---|---|
| other545 NEMO 网络动量 | S 0.90（risk-neut 0.23） | 纯风格 beta |
| macro63 指数成员 | S −0.30 | 弱且方向为负 |
| other571 Wikipedia 注意力 | S 1.35 / risk-neut 1.40 | 强度不足（距闸 0.23） |
| news_sentiment_nlp | S 1.10 / TO 0.44 | 太快太噪 |
| pv115 做空占比（反向） | S 1.67 / SUB 1.67 | 2Y 衰减 0.60–0.71 |
| equity_kpi_forecast | S 1.66 / F 1.38 | CW 0.203；模型惊喜 SUB/2Y 双缺 |

⇒ **结论**：USA 区当日**未产出可交付新 ATOM**。两类瓶颈清晰：
① **Analyst**：IS 强（S 1.94）但 prod 地板 0.806；② **非 Analyst**：prod 无问题但 **2Y 普遍衰减**（信息被套利）或强度不足。
⇒ 下一步优先级：**(a)** 5 条 Analyst IS 全过候选留池等 prod 回落（最省力）；**(b)** 在 analyst_factor_signals 剩余未测机制（asymmetry / CAGR / QoQ·YoY 增长 / zscore / 3mo 变化）上系统扫 SUB 轴；**(c)** 若再挖非 Analyst，先看 `2Y` 再花仿真（本轮 5 个方向里 3 个死在 2Y）。

---

## 7. ★★★★★ 角点全图：`eps_q1_estimate_qoq_growth`（今日最佳候选，2026-10-18 20:40）

**字段画像**：MATRIX / cov 0.9243 / **uc 5、ac 6（全 QoQ 增长族最冷门）** / ANALYST 塔 1.2
**机理**：Q1 预期 EPS 的**环比增长率** = 增长速率（不是修正、不是惊喜）

### 7.1 归因（0 仿真，`gate_attribution.py`）

```
cause=mechanism_crowded  levres 排名：
 #1 换同机制字段 → 查族内 uc/ac 后【否决】：本字段已是全族最冷门（uc5/ac6），换任何一个都更挤
 #2 trade_when 门控窗口 → 实测门控把 S 打到 0.34【否决】
 #4 ⚠ 禁投 hump（TO<0.15 时反升 prod）→ 实测成立：去 hump prod 0.7497→0.7033
 #5 ⚠ 无效：保序形变 / 中性化档 → 部分成立（RAM 有效 −0.04，但只此一档）
```

### 7.2 角点全图（15 条实测，全部 `check_correlation(refresh=True)`）

| # | 结构 | S | F | 2Y | SUB | TO | **prod** | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **A** | **RAM / subindustry / hump0.01 / d10** | **1.89** | **1.12** | 1.66 | **0.84** | 0.037 | **0.7094** | ★**七闸全过，prod 差 0.0094（今日最优）** |
| B | CROWDING / subindustry / hump0.01 / d10 | 1.80 | 1.10 | **1.76** | **0.87** | 0.012 | 0.7497 | 七闸全过，prod 差 0.05 |
| C | CROWDING / subindustry / **无 hump** | **2.23** | **1.56** | 2.01 | 0.41❌ | 0.038 | **0.7033** | SUB 崩（hump 是 SUB 的命门） |
| D | RAM / sector / hump0.01 | 1.78 | 1.11 | 1.95 | 0.75❌ | 0.042 | — | SUB 差 0.02 |
| E | RAM / market / hump0.01 | 1.81 | 1.14 | **2.25** | 0.75❌ | 0.043 | — | SUB 差 0.03 |
| F | RAM / subindustry / 126 窗 | 1.86 | 1.09 | 1.68 | 0.72❌ | 0.037 | — | SUB 差 0.09 |
| G | RAM / subindustry / d20 | 1.75 | 1.01 | 1.59 | 0.63❌ | 0.036 | — | d20 伤 SUB |
| H | CROWDING / hump0.02 / 0.03 / 0.05 | 1.76–1.79 | 1.06–1.08 | **1.09–1.15**❌ | 0.93–0.99 | 0.011 | — | hump>0.01 立刻杀 2Y |
| I | CROWDING / ts_mean 5·22、ts_decay_linear 5 | 2.06–2.22 | 1.39–1.55 | 1.66–1.98 | **0.35–0.41**❌ | 0.033 | — | 非 hump 平滑一律 SUB 崩 |
| J | trade_when(rank>0.4) 门控 | 0.34 | 0.08 | 0.46 | 0.41 | 0.009 | — | 门控毁信号 |
| K | CROWDING / 加速度 ts_delta(·,63) | 1.85 | 1.24 | 2.08 | 0.93 | 0.012 | 0.8334 | 八闸全过但 prod 更差 |

### 7.3 三条机理结论（可迁移）

1. **`hump` 是本族的「SUB 命门」**：只有 hump 能把 TO 压到 0.011 并让 SUB 从 0.41 → 0.87–0.99；
   `ts_mean`/`ts_decay_linear`/无平滑一律 SUB 0.35–0.41 ⇒ **不要用"更轻的平滑"替代 hump，替代品不存在**。
2. **hump 阈值是二值开关**：0.01 保 2Y（1.76），0.02 起 2Y 立刻掉到 1.09–1.15 ⇒ **只能用 0.01**。
3. **中性化对本族是 prod 杠杆而非 S 杠杆**：RAM vs CROWDING —— prod 0.7497→0.7094（−0.04）、
   S 1.80→1.89（+0.09）、但 TO 0.012→0.037、SUB 0.87→0.84。**两者都七闸全过，RAM 版 prod 最低。**

### 7.4 当前状态与建议

- **`1YjoKAz6`**（角点 A）已七闸全过、CLUSTER 1.17 干净、self 未测（同族 self 预计 <0.7，因池内无同数据集腿）。 <!-- from config -->
- **缺口仅 prod 0.0094**。prod 每日漂移实测可达 ±0.29/半天 ⇒ **建议每日重测一次，<0.7 即刻提交**（无需重跑）。
- 若要继续压：唯一未试的合法方向是**同集多字段组合**（用户 2026-10-18 确认同数据集内允许）——
  例如 `subtract(qoq_growth_eps, qoq_growth_revenue)` 做「增长质量」（EPS 增长 vs 收入增长），
  但 toolkit 的 `equal_weight_leg_add` 闸只拦 add，subtract 需自行确认；下一轮优先试这条。

---

## 8. 破 prod 的方法盘点（2026-10-18 21:00：论坛故障 + 外部研究 + 实测）

### 8.1 论坛：通道故障，非"无解"

`tools/forum_recon.py` 跑了 8 轮检索，对照探针（'alpha'）0 结果 ⇒
`status=error / reason_code=control_probe_failed`（会话过期或被拦）。
**工具自身声明：这不是"论坛无解"，不作判死证据、不入缓存**；修好后须重跑同一问题。

### 8.2 外部研究结论（5 篇一致）

| 来源 | 结论 |
|---|---|
| quantrading.space / quantmemo / inferensys | **正交化（residualization）是标准方法**：把新信号对已有信号（或已知因子）回归，只留残差 ⇒ 贡献"增量信息" |
| IQC 2026 指南 | **"Residual momentum — momentum unexplained by beta and sector"** 是被点名的有效形态 |
| 同上 | 另一条闸门公式：`SUB 阈值 = 0.75 × sqrt(子宇宙占比) × S`（解释了为何 S 越高 SUB 要求越高） |
| BRAIN 规则汇总 | **self 有 10% 夏普豁免**（S 比被相关 alpha 高 10% 即可），**prod 无同类豁免** |

### 8.3 实测：正交化在本族是「照妖镜」而非解药

用**同数据集**增长代理做 `vector_neut`（ATOM 安全，无需跨集）：

| 正交化对象 | S | F | 2Y | SUB | 判定 |
|---|---:|---:|---:|---:|---|
| `eps_y1_cagr_2yr`（2 年 CAGR） | **0.62** | 0.19 | 0.50 | 0.52 | 崩 |
| `eps_estimate_trend_slope_1yr` | 0.62 | 0.19 | 1.09 | 0.37 | 崩 |
| `eps_y1_consensus_value` | 0.63 | 0.20 | 0.26 | 0.59 | 崩 |
| 增长质量 `subtract(qoq_eps, qoq_revenue)` | 1.29 | 0.70 | 1.23 | 0.66 | 弱 |

⇒ **S 从 1.89 → 0.62（−67%）**：说明该信号 60%+ 的 PnL 就是增长因子暴露，
正交化后残差**没有 alpha**。**这同时验证了 prod 0.75 的归因**（cause=mechanism_crowded 且是"增长 beta"而非"字段拥挤"）。

### 8.4 破 prod 方法总表（本族已穷尽）

| 方法 | 实测效果 | 状态 |
|---|---|---|
| 换持仓字段（同机制） | 本字段已是全族最冷门（uc5/ac6） | ✗ 无更优字段 |
| 换中性化 | RAM 0.7497→0.7094（−0.04，唯一有效档） | ✓ 已用 |
| 去 hump | 0.7497→0.7033，但 SUB 0.87→0.41 | ✗ SUB 崩 |
| 换轴 | sector/market SUB 差 0.02–0.03 | ✗ |
| 换窗/decay | 126/504/d20 均伤 SUB 或 2Y | ✗ |
| 加速度（ts_delta） | prod 0.8334（更差） | ✗ |
| trade_when 门控 | S 0.34 | ✗ |
| **正交化（vector_neut）** | **S 1.89→0.62** | ✗ **信号本体=因子** |
| 换 universe | 纪律禁止（修复保持 TOP3000） | — |
| **等 prod 自然漂移** | 实测 ±0.29/半天 | ★ 唯一可行 |

### 8.5 结论（写死进选信号纪律）

> **正交化不是"降 prod 的杠杆"，而是"判断信号是否真有 alpha 的过滤器"**：
> 若 `vector_neut(信号, 因子代理)` 后 S 掉超过 50%，说明信号本体就是那个因子 ⇒
> **不要再对它做任何参数/中性化微调，直接换信息源**（本族从 15 个角点走到 0.7094 已是天花板）。

---

## 9. 两个工具：照妖镜预筛 + prod 巡检（2026-10-18 落地）

### 9.1 `tools/nemesis_prescreen.py` —— 照妖镜（判断信号是否为因子换皮）

```bash
# ① 生成 vector_neut 变体（零仿真）
$WQ_PY tools/nemesis_prescreen.py --gen \
    --signals tracking/USA/candidates/nemesis_input.json \
    --proxies "eps_y1_cagr_2yr,eps_estimate_trend_slope_1yr,eps_y1_consensus_value" --json
# ② 派发（MCP create_multi_simulation，settings 与原信号完全一致）
# ③ 判定（输入 harvest_multisim_alphas 的结果文件）
$WQ_PY tools/nemesis_prescreen.py --judge harvest.json
```

判定：`S 掉幅 <30% = PASS｜30–50% = WEAK｜>50% = KILL`。
**KILL ⇒ 信号本体就是该因子，停止微调，换信息源**（本族实测 67% ⇒ KILL）。

代理选择纪律（**必须同数据集**，否则变 combined）：
| 想剥离的因子 | 代理字段示例（analyst_factor_signals） |
|---|---|
| 增长 | `eps_y1_cagr_2yr`、`eps_estimate_trend_slope_1yr` |
| 规模/水平 | `eps_y1_consensus_value`、`eps_trailing_4q_estimate` |
| 分歧 | `eps_y1_estimate_coeff_var`、`eps_y1_estimate_skewness` |

### 9.2 `tools/prod_watch.py` —— 每日 prod 巡检（候选池）

```bash
$WQ_PY tools/prod_watch.py --pool tracking/USA/candidates/prod_waitlist.json
$WQ_PY tools/prod_watch.py --pool ... --json --no-write   # CI/自动化
```

- 端点 = **`/alphas/{id}/correlations/prod`**（`/correlations/production` 会 404）；
  响应顶层直接是 `max`；**空体 200 = 平台仍在算**，文档要求重试。
- 状态：`READY(<0.70)` / `NEAR(<0.75)` / `BLOCKED`；会自动把 `last_prod` / `last_checked` 原子回写池文件。
- 单并发 + 条间 sleep（平台每账号单并发，实测单条 ~94s）。

**当前池（7 条，全部 IS 八闸全过、仅差 prod）**：

| alpha | 机制 | S | prod（2026-10-18 20:43） | 状态 |
|---|---|---:|---:|---|
| `1YjoKAz6` | QoQ 增长 / RAM / subind | 1.89 | **0.7094** | NEAR（差 0.0094） |
| `vRO5Gz5v` | QoQ 增长 / CROWDING / subind | 1.80 | 0.7497 | NEAR |
| `88vaY1Jq` | 修正幅度 / subind | 1.94 | 0.8068 | BLOCKED |
| `A1QgNQZY` | EPS 惊喜 / CROWDING | 1.86 | 0.8476 | BLOCKED |
| `A1Qg0XmR` | EPS 惊喜 / RAM | 1.79 | 0.8484 | BLOCKED |
| `Vkd2adjb` | EPS 惊喜 / CROWDING / 504 | 1.72 | 0.8532 | BLOCKED |
| `JjPgQgqe` | 惊喜背离 | 1.72 | 0.8673 | BLOCKED |

### 9.3 标准工作流（新候选进入交付流程前）

```
1. 选信号（未点亮塔 × 低 alphaCount × 有经济机理）
2. 照妖镜预筛  → 掉幅 >50% 直接弃（省掉全部后续仿真）
3. 七闸仿真 + prod 实测 → 全过则进池、否则按 gate_attribution 的杠杆排名定向推
4. 进池后每日 prod_watch；<0.70 即提交（唯一零成本路径）
```
