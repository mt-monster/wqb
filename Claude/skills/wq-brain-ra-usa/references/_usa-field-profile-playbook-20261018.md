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
