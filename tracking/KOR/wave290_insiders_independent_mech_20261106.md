# KOR × insiders wave290（2026-11-06）— 独立机制族

> 目标：KOR / TOP600 / D1，ATOM（单数据集）REGULAR alpha。
> 已在 insiders5 交付 2 颗全闸（kqNv1xRk / RRE9NkVj），**同属 stddev 分歧度机制**（ghc_tr / vol_chg × W55）。
> 第 3 颗必须换**独立机制**，否则撞 self-corr 0.70 线。

## 1. 本轮筛查结论（全部有硬证据，不再重探）

| 数据集 / 类 | 结论 | 证据 |
|---|---|---|
| news 全塔（24 数据集） | ⛔ **塔关闭** | reference/datasets/news20.md §7：五条轴（方向/计数/强度/结构/幅度）全落 .25–.67，十年覆盖全 PASS ⇒ 新闻信息在 D1 已定价 |
| news21 | ⛔ 无信号 | reference/datasets/news21.md L1：唯一数值字段 nws21_event_freq 落在已判死的计数轴，其余全是日期/标签 |
| news7 | ⛔ 注意力计数轴全灭 | wave187b 8/8 全灭，max|S|=0.55 |
| sentiment 塔 | ⛔ **三连死** | 189 sentiment27 覆盖死（2014–2018 五年空）/ 190 other106 机制死 / 192 other553 机制死 |
| other553 | ⛔ 判死 | KOR-OTH553-REV-SPARSE：有效标的仅 22–110 只，8/11 触发 CW，wave192 实测 S +0.13 / −0.28 |
| sentiment26 | ⚠ 塔内唯一残余 | cov .356（<0.40 换集线）、19 全 VECTOR、aC ≤7 最不拥挤；但 KOR-SENTIMENT26-NO-CROSS-SECTION-AND-7Y-COVERAGE 已判双重死因 |
| earnings3 | ⛔ 判死 | KOR 实测 S 0.83 天花板（_kor-operator-matrix.md L135）；IND/MEA/GLB 三区判「日历/计时作主信号」死；aC 2624 极拥挤 |
| institutions 全类 | ⛔ 无路 | 仅 2 数据集：fund_holdings_panel（KOR-FUND-HOLDINGS-PANEL-DEAD）+ institutions6（跨区判死，仅作门控腿，ATOM 不行） |
| imbalance5 | ⛔ 判死 | 2Y 结构性不可达（三种机制 2Y 均 ≈0.17）；aC 1109 极拥挤 |

## 2. ★ 关键铁律（本轮挖出，重塑战略判断）

> **F-4：KOR 里 S ≥ 1.58 只出现在 analyst 与 shortinterest 两个塔**
> （_field-profile-and-templates.md L25，13 个数据集实测：analyst 1.66 / shortinterest 2.09，其余 11 个最高仅 0.05–1.46）

**本轮已打破该铁律**：insiders5 产出 S 1.62 / 1.76 两颗全闸件。
⇒ KOR 的可行面 = **analyst + shortinterest + insiders5（新突破）**，其余塔全灭或已点亮。
⇒ insiders 塔 0/3 未点亮，是当前唯一既有实证成功又仍有席位的方向。

## 3. wave290 设计：两个未触碰的独立机制族

insiders5 字段族盘点（53 字段全 VECTOR）：

| 族 | 代表字段 | cov | 本轮状态 |
|---|---|---:|---|
| A 交易流量 | ghc_tr / vol_chg / fa_tr / trd_amt | .7318 | ✅ 已榨（stddev 分歧度 2 颗） |
| B 交易时点 | td_ctn / td_ghc / history_td_drt | .7318 | 未触碰（日期型，相减需验证） |
| C 持仓快照 | tnc / source_ratio / real_ratio | .9996 | ⭐ **本轮批 B** |
| D 库藏股 | trsy_ratio / trsy_data / trsy_real_ratio | .8728 | ⭐ **本轮批 A**（完全未触碰） |
| E 标识 | officer / c_company_pyt_tkm | .7318 | 留作门控轴 |

### 批 A：库藏股族（8 条）— 1EVOpgcSV4wO8D7kldBktIz
机制：库藏股比例 = 回购/注销代理，韩国资本回报特色动作，**独立于内部人交易分歧度**。

| # | 表达式 | 机制面 |
|---|---|---|
| A1 | group_rank(ts_delta(vec_avg(insd5_trsy_ratio), 55), sector) | 季度回购动作 |
| A2 | group_rank(ts_delta(vec_avg(insd5_trsy_ratio), 250), sector) | 年度回购动作 |
| A3 | group_rank(vec_avg(insd5_trsy_ratio), sector) | 库藏水平（存量） |
| A4 | group_rank(ts_rank(vec_avg(insd5_trsy_ratio), 250), sector) | 年内分位 |
| A5 | group_rank(divide(vec_avg(trsy_ratio), subtract(1, vec_avg(trsy_ratio))), sector) | 库藏/流通对数比变换 |
| A6 | group_rank(ts_delta(vec_max(insd5_trsy_ratio), 55), sector) | 最大单笔变动（降维算子换 vec_max） |
| A7 | group_rank(ts_av_diff(vec_avg(insd5_trsy_data), 250), sector) | 股数口径均值偏离 |
| A8 | group_rank(ts_delta(vec_sum(insd5_trsy_real_ratio), 55), industry) | 未去重口径 + industry 分组轴 |

### 批 B：控制权集中度族（8 条）— 1gWiweg6z4js9BdyEikMcTd
机制：关联方网络规模与内部人持股集中度 = 治理结构，**cov 0.9996 全覆盖**。

| # | 表达式 | 机制面 |
|---|---|---|
| B1 | group_rank(vec_avg(insd5_tnc), sector) | 特别关系方数量水平 |
| B2 | group_rank(ts_delta(vec_avg(insd5_tnc), 250), sector) | 关联方网络扩张 |
| B3 | group_rank(ts_rank(vec_avg(insd5_tnc), 250), sector) | 年内分位 |
| B4 | group_rank(vec_avg(insd5_source_ratio), sector) | 去重持股比例水平 |
| B5 | group_rank(ts_delta(vec_avg(insd5_source_ratio), 250), sector) | 持股集中度变动 |
| B6 | group_rank(ts_std_dev(vec_avg(insd5_source_ratio), 250), sector) | 持股稳定性（时序方差） |
| B7 | group_rank(ts_delta(vec_avg(insd5_real_ratio), 55), sector) | 未去重口径变动 |
| B8 | group_rank(ts_std_dev(vec_sum(insd5_tnc), 66), industry) | 关联方数量波动 × industry |

## 4. 设置

KOR / TOP600 / D1 / **R&M** / decay 4 / trunc 0.08 / **nanH OFF** / maxTrade OFF / pasteurization ON / unitHandling VERIFY / 2014-01-01–2023-12-31

## 5. 预置判据（照 189/190/191/192）

- 批落地后若 **max|S| < 0.8 且 max|2Y| < 1.0** ⇒ 该族机制判死，不扫参数、不换窗口。
- 任一族 S ≥ 1.3 ⇒ 转 S4 改进（窗口谱 22/44/55/66/88、分组轴、等价算子替换）。
- 存活腿必须查 check_self_correlation：与 kqNv1xRk / RRE9NkVj 的 self 必须 < 0.70（同数据集，风险高）。

## 6. 待办

- [ ] harvest 两批 → 归因
- [ ] 存活族查覆盖（get_alpha_yearly_stats，2014 起）
- [ ] 存活族查 self-corr（与已交付 2 颗）