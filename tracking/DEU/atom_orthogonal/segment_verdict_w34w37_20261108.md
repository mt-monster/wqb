# DEU 战役台账：Wave 34–37（2026-11-08 收割）

承接 segment_verdict_w31w33_20261112.md（论坛骨架 1YN0dw7R S2.03/2Y2.00/prod 0.704 浅钉）。

---

## Wave 34（1rFDF8gnD4tKa6Y1gk3NebCi）：S×2Y 慢/快配对 — 10/10 REJECT

设置 DEU/TOP500/D1/FAST/decay0/sector。骨架：慢腿=广度不对称比（W32-7 的 S 提供者，240 窗），快腿=各种广度计数 ts_delta 44。

| # | 慢腿（不对称比） | 快腿 | alpha | S | F | 2Y | TO | sub | dd | fail |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| W34-1 | ebi | ebt_raisednum | rKR8PK71 | 0.63 | 0.19 | 0.52 | 0.2981 | 0.34 | 0.0932 | 3 |
| W34-2 | ebt | gps_raisednum | GrW9ermG | 0.75 | 0.25 | 0.69 | 0.2939 | 0.30 | 0.0796 | 4 |
| W34-3 | gps | sal_raisednum | 88RXe8Go | 0.38 | 0.09 | 0.18 | 0.2919 | 0.04 | 0.1466 | 4 |
| W34-4 | pre | net_raisednum | j2YOr2Vj | 0.98 | 0.37 | 1.42 | 0.2971 | 0.65 | 0.0821 | 3 |
| W34-5 | ebi | rec_raisednum | 1YN0zYGM | 0.82 | 0.29 | 0.88 | 0.3048 | 0.69 | 0.0740 | 3 |
| W34-6 | ebi | ebi_num | Vkxe3kZY | 0.79 | 0.27 | 1.34 | 0.2968 | 0.77 | 0.0772 | 3 |
| W34-7 | ebi | dps_raisednum | Xg9M8gVa | 0.86 | 0.30 | 0.36 | 0.3000 | 0.77 | 0.1132 | 3 |
| W34-8 | ebi | ebt_lowerednum | zq3eRqgV | 0.33 | 0.07 | 0.09 | 0.2904 | 0.03 | 0.1219 | 4 |
| W34-9 | gps | rec_raisednum | P0oKO0Yp | 0.84 | 0.30 | 0.92 | 0.3002 | 0.62 | 0.1069 | 3 |
| W34-10 | ebi | ebi_lowerednum（同族自参照对照） | npvr8peq | 0.32 | 0.07 | -0.33 | 0.2761 | 0.12 | 0.0837 | 4 |

**判据 P：骨架的慢腿必须是「水平量」（ts_zscore 水平），不能是流量比率。**
W32-7 的不对称比单独有 S 1.13（8 算子短骨架），但放进论坛骨架的 240 窗慢腿后 S 只剩 0.98（最高），全族 0.32–0.98 ⇒ 广度比不含水平信息，撑不起慢腿。
对照：W33-1（ebi 水平慢腿）S 2.03。归因：ts_zscore(…,240) 的慢腿本质是「1 年期水平分」，广度比是快速均值回复流量，长窗 z 后无截面区分度。
⇒ 论坛骨架的适用域收窄：慢腿=水平快照，快腿=同指标或跨指标 4 周修正。

## Wave 35（2vZTys77k4EF9FJ8Y8pYJmN）：窗口网格 + ts_rank 替换 — ★★★ 10/10 failed_ra=0

设置同 Wave 34。骨架：group_rank(add(ts_zscore(ebi_mean, SLOW), ts_zscore(subtract(ebt_mean, ebt_mean_4wks_ago), FAST)), sector)

| # | (SLOW,FAST) | alpha | S | F | 2Y | TO | sub | dd | fail |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| W35-1 | (240,36) | xAr5d8Nq | 2.00 | 1.20 | 1.82 | 0.2686 | 1.16 | 0.0414 | 0 |
| W35-2 | (240,40) | WjOJVQAN | 2.02 | 1.23 | 1.87 | 0.2592 | 1.17 | 0.0463 | 0 |
| W35-3 | (240,48) | pwd3KrNv | 2.02 | 1.27 | 1.95 | 0.2446 | 1.12 | 0.0472 | 0 |
| W35-4 | (240,52) | LLM3da7L | 2.07 | 1.33 | 1.96 | 0.2392 | 1.17 | 0.0466 | 0 |
| **W35-5** | **(240,60)** | **xAr5d8jm** | **2.18** | **1.46** | **2.12** | 0.2310 | 1.27 | 0.0442 | 0 |
| **W35-6** | **(240,66)** | **YP1YgK7J** | **2.19** | **1.49** | **2.22** | 0.2260 | 1.27 | 0.0463 | 0 |
| W35-7 | (220,44) | A1VE7Z0d | 1.99 | 1.22 | 1.91 | 0.2520 | 1.14 | 0.0470 | 0 |
| W35-8 | (264,44) | KPJZEdON | 2.06 | 1.29 | 2.03 | 0.2503 | 1.16 | 0.0462 | 0 |
| W35-9 | (252,40) | akKGEZb6 | 2.03 | 1.24 | 1.85 | 0.2588 | 1.19 | 0.0478 | 0 |
| **W35-10** | **ts_rank 替换 (240,44)** | **1YN0zbXJ** | **2.17** | **1.41** | **2.00** | 0.2328 | 1.17 | **0.0400** | 0 |

**判据 R：窗口网格是 IS 侧单调改进，不是 prod 杠杆的证据待测。**
快窗 36→66：S 2.00→2.19 单调升、2Y 1.82→2.22 单调升、TO 0.269→0.226 单调降——**快窗 66 全面优于论坛原帖的 44**（原帖在其市场是甜点，DEU 的甜点右移）。
慢窗 220/240/252/264 平坦（1.99–2.06）⇒ 慢窗不敏感（240 恰好=年窗即可）。
ts_rank 替换（W35-10）：S 2.17 / 2Y 2.00 / dd 0.0400 全战役最低 ⇒ 标准化器替换不伤 IS，是「同结构不同截面权重」，prod 测试候选之二。

## Wave 36（4wpEzPcZn59H8xrw4KFUaUI）：冷门字段替换 — ★★★ 2 颗 failed_ra=0

设置同 Wave 34。目的：论坛第 7 条降 PC 手段（换 userCount 低的冷门字段），并用单腿替换做归因对照。

| # | 变体 | alpha | S | F | 2Y | TO | sub | dd | fail | 归因 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| W36-1 | median×median | gJeL8Abg | 1.70 | 0.96 | 0.97 | 0.2483 | 0.72 | 0.0649 | 3 | 快腿 median 杀 2Y |
| W36-2 | median×low | npvrNJPM | 1.54 | 0.85 | 1.21 | 0.2474 | 1.06 | 0.0688 | 3 | 双腿弱化 |
| **W36-3** | **median×mean（只换慢腿）** | **RREPm361** | **2.02** | **1.25** | **1.82** | 0.2508 | 1.24 | 0.0474 | **0** | ★ 冷门替换不伤信号 |
| W36-4 | mean×median（只换快腿） | 9qxkpvW2 | 1.84 | 1.08 | 1.08 | 0.2488 | 0.75 | 0.0632 | 2 | 快腿必须 mean |
| W36-5 | median_4wks_ago×median | WjOJAqLQ | 1.72 | 0.99 | 0.98 | 0.2472 | 0.70 | 0.0647 | 3 | 慢腿不能取历史快照 |
| W36-6 | mean_3mth_ago×median | kqN9P7JL | 1.42 | 0.71 | 0.30 | 0.2502 | 0.71 | 0.0605 | 3 | 同上 |
| W36-7 | median×median Δ3mth | qMLVN1Ej | 1.79 | 1.07 | 1.41 | 0.2426 | 1.03 | 0.0648 | 1 | 3 月修正弱于 4 周 |
| **W36-10** | **median×mean Δ3mth** | **e75E3p5J** | **1.84** | **1.11** | **1.62** | 0.2447 | 1.15 | 0.0492 | **0** | ★ 3 月修正版双过 |
| W36-8 | high×high | RREPm3Az | 1.43 | 0.75 | 1.28 | 0.2477 | 0.84 | 0.0711 | 3 | 极值快照无料 |
| W36-9 | low×low | VkxeG9dA | 1.46 | 0.78 | 1.37 | 0.2479 | 0.95 | 0.0664 | 3 | 极值快照无料 |

**判据 Q（骨架字段几何的三条铁律）**：
1. **慢腿可用 median（uc 69→14）**：RREPm361 S 2.02 / 2Y 1.82 与 mean 版完全同水平 ⇒ 冷门字段替换是**无损**降 PC 杠杆（不是降 IS 换降 PC）。
2. **快腿必须 mean**：median/low 快腿 2Y 掉到 0.97–1.37（9qxkpvW2 1.84/1.08）⇒ 2Y 来自「共识均值（mean）的 4 周变化」，median 共识不含此信息。
3. **历史快照（_4wks_ago/_3mth_ago）不能作慢腿水平**（1.42–1.72）⇒ 慢腿必须是「当前时点的水平分布」。

**族内互相关（12 颗 failed_ra=0 候选，compute_mutual_correlation）**：
- 66 对超 0.7；最大对 akKGEZb6↔WjOJVQAN **0.997**
- **max_mutually_below_subset_size = 1** ⇒ 整个 ebi×ebt 骨架族只占篮子 1 个位置。

**prod 破墙测试队列（账号级单并发，一次一颗，找到 <0.70 即停）**：
1. RREPm361（冷门字段，结构差异最大）
2. 1YN0zbXJ（ts_rank 标准化替换）
3. YP1YgK7J（W66 快窗，IS 最优 2.19/2.22）
1YN0dw7R 已知 0.704。测试中（首测 120s 超时，等 300s TTL 后回读）。

## Wave 37（2KBZ7c7B15b5cxA16GEph1yn）：model36 SmartRatios 信用风险 — 在飞

数据集：model36（SmartRatios Credit Risk Model，20 字段全 MATRIX，cov 0.69–1.0，uc 1–9 极冷）。
机制：KMV-Merton 结构违约模型的公司信用质量百分位（star_sr_*）+ 违约概率国家/行业/全球分位（default_risk_*）。
与既有已挖机制（分析师修正/情绪/空头/预期）完全正交，MODEL 塔内 strict-ATOM 合法（不混塔）。

模板来源：
- 论坛帖 29155767547543《Forecasting Default with the KMV-Merton Model》（JL11546，2025-01-12，28 赞）：骨架 = ts_rank(winsorize(ts_backfill(<data>,120),std=4),60) + bucket 中性化 + ts_weighted_decay；1 万次回测产 6 颗可提交（USA/GLB/KOR），作者称跨区域强泛化。
- Campbell-Hilscher-Szilagyi 2008（distress puzzle：高质量=正溢价）、QMJ（Asness-Frazzini-Pedersen 2019）。
- **论坛算子 ts_weighted_decay 在平台不存在（幽灵算子）⇒ 已改 ts_decay_linear(…,10) 等价**。

10 模板（SUBINDUSTRY/decay4/trunc0.08，算子 2–9 个）：
| # | 模板 | 机制 | 来源 |
|---|---|---|---|
| T1 | KMV 骨架压缩版（ts_rank+W60+leverage bucket 中性化+decay_linear10） | 论坛骨架 | forum |
| T2 | 纯质量水平 group_rank(credit_risk_profitability_score_d1, sector) | QMJ | paper |
| T3 | 信用质量动量 ts_delta(66) | 评级漂移 | paper |
| T4 | 质量对自身年范 ts_zscore(252) | 自均值偏离 | self |
| T5 | 行业分位−全球分位（特异性信用风险） | 跨域失配 | self |
| T6 | QMJ 价差 profitability−leverage | QMJ 双柱 | paper |
| T7 | 增长/杠杆效率比 | 比率几何 | paper |
| T8 | 质量稳定性 -ts_std_dev(66) | 不确定性厌恶 | paper |
| T9 | 二阶差分（质量加速度） | 拐点 | self |
| T10 | 最弱链 min(coverage,liquidity,leverage) | 非线性短板 | self |

符号先验：star_sr_* 越高=信用质量越好 ⇒ 多头取正（与论坛帖 -rank(default_prob) 同经济方向）。

---

## ★★★ 破墙成功（2026-11-08）：RREPm361 prod 0.6881 < 0.70 —— 第 7 颗合格件

RREPm361  group_rank(add(ts_zscore(est_12m_ebi_median, 240), ts_zscore(subtract(est_12m_ebt_mean, est_12m_ebt_mean_4wks_ago), 44)), sector)
设置 DEU/TOP500/D1/FAST/decay0/trunc0.08，5 个算子。

| 闸 | 值 | 线 | 判 |
|---|---:|---:|---|
| Sharpe | 2.02 | >=1.58 | ✓ |
| Fitness | 1.25 | >=1.0 | ✓ |
| 2Y | 1.82 | >=1.58 | ✓ |
| TO | 0.2508 | <=0.7 | ✓ |
| sub_universe | 1.24 | >=0.957 | ✓ |
| margin | 0.000764 | >0 | ✓ |
| drawdown | 0.0474 | — | 低 |
| failed_ra | 0 | =0 | ✓ |
| self | 0.2924 | <0.7 | ✓ |
| prod | 0.6881 | <0.70 | ✓（hist [0.6,0.7) n=2） |

判据 T（prod 破墙第三杠杆）：同指标快照变体替换（mean→median，uc 69→14）把 prod 0.7040→0.6881，IS 无损（S 2.03→2.02、2Y 2.00→1.82）。1YN0dw7R 留档备选；同族其余 10 颗按互相关=1 席规则停止 prod 测试。

## Wave 37 判死：model36（SmartRatios 信用风险）

10/10 REJECT，S ∈ [-0.19, 0.62]、2Y ∈ [-0.55, 0.49]。最强 58EYlWLX（最弱链）S 0.62 但 2Y -0.43。
判据 S：KMV-Merton 论坛骨架（帖 29155767547543，作者只在 USA/GLB/KOR 验证）不泛化到 DEU；信用质量百分位水平在 DEU/TOP500 无截面收益信号。ts_weighted_decay 是幽灵算子，已用 ts_decay_linear 等价替换。

## Wave 38（264BF8bum4CibTfyQuoq7hN）：model25 探针 — 在飞

model25 = 基本面+百分位混合集（217 字段，92 个 uc<=10 冷字段）。10 模板（每条 <=6 算子，SUBINDUSTRY/decay4/trunc0.08）：
| # | 机制 | 要点 | 来源 |
|---|---|---|---|
| T1 | 收入+EBIT QoQ 双证 | add(rank(is_v6), rank(is_v15)) | 基本面动量 |
| T2 | 利润率扩张剪刀差 | subtract(rank(EBIT QoQ), rank(rev QoQ)) | 自建 |
| T3 | 现金流-应计背离 | subtract(rank(CFO QoQ), rank(NI QoQ)) | Sloan 1996 |
| T4 | FCF 产出率 | divide(rank(FCF), rank(mktcap)) | FCF yield |
| T5 | Sloan 应计（负号） | -rank(accruals_component_raw_score) | Sloan 1996 |
| T6 | 质量双柱 | add(rank(exclusions), rank(op_eff)) | Piotroski 2000 |
| T7 | 加杠杆惩罚 | -ts_zscore(leverage QoQ, 252) | 杠杆变化 |
| T8 | 增长偏离平滑 | ts_mean(rev growth deviation, 66) | 增长加速度 |
| T9 | 52 周区间宽度 | divide(rank(52wHigh), rank(52wLow)) | George-Hwang 2004 |
| T10 | 增股息+收入双证 | add(rank(DPS delta), rank(rev QoQ)) | Michaely |

---

## Wave 38 判死：model25（基本面+百分位混合集）

10/10 REJECT，S ∈ [-0.81, 0.66]、2Y ∈ [-0.67, 0.63]。
| # | 模板 | S | 2Y |
|---|---|---:|---:|
| T1 | 收入+EBIT QoQ 双证 | -0.17 | -0.46 |
| T2 | 利润率扩张剪刀差 | 0.27 | -0.62 |
| T3 | 现金流-应计背离 | 0.31 | 0.27 |
| T4 | FCF 产出率 | 0.61 | -0.67 |
| T5 | Sloan 应计（负号） | -0.81 | 0.20 |
| T6 | 质量双柱（排除+运营效率） | 0.66 | 0.28 |
| T7 | 加杠杆惩罚 | -0.14 | -0.21 |
| T8 | 增长偏离平滑 | -0.28 | 0.29 |
| T9 | 52 周区间宽度 | 0.54 | -0.04 |
| T10 | 增股息+收入双证 | 0.09 | 0.63 |

判据 U：model25 判死（机制级）。副产物：DEU 应计方向与 Sloan 相反（+accruals ≈ +0.81），与 fundamental6 Sloan S1.09 判弱互证——DEU 不给应计溢价定价。T6 质量双柱 0.66 / T4 FCF 产出率 0.61 是天花板，均远低于 1.58。

## Wave 39（gZ463fWS4Cf90DrW8Ut2jR）：model250 MALTA 子信号分解 — 在飞

机制族：ML 复合分 vs 分量残差 / 季节性（日历异常）/ 对冲（下行保护）/ 短中期分量 / 复合分稳定性与加速度。冷字段优先：lmt_close_eq_score uc6、lmt_open uc4、hc_eq_short uc1。10 模板（SUBINDUSTRY/decay4/trunc0.08，<=7 算子）。

## Wave 40（KkPFTfiH4u9blzzRzDvIrZ）：other47 SEMrush 数字足迹 — 在飞

18 字段全 VECTOR（有机流量/关键词/SEMrush rank/付费预算/付费访客/PLA）。机制：网络流量=营收前瞻代理（SVI 类文献：Da-Engelberg-Gao 2011）；付费/有机结构=获客质量。全部 vec_avg 包装 + ts_backfill 22。10 模板（<=7 算子）。cov 0.50-0.65。

---

## Wave 39 判死：model250（MALTA ML 子信号）

8 REJECT + 2 REVIEW，S ∈ [-0.22, 1.14]。
| # | 模板 | alpha | S | F | 2Y | fail |
|---|---|---|---:|---:|---:|---:|
| T1 | lmt_close 水平 | JjerN0ml | 0.75 | 0.29 | 0.73 | 3 |
| T2 | lmt_open z252 | 78LlNqQZ | 1.02 | 0.47 | 0.53 | 3 |
| T3 | hc_short（最冷 uc1） | QPv6brjp | 0.85 | 0.65 | 0.00 | 3 |
| T4 | 复合-分量残差 | gJeLbqPK | 0.38 | 0.17 | -1.61 | 4 |
| T5 | 季节性水平 | MPYVal8L | 1.14 | 0.95 | 0.27 | 3 |
| T6 | 季节性动量 | bl6Ab2Pr | 0.09 | 0.02 | -0.04 | 4 |
| T7 | 对冲×弱中期 | A1VENJaX | -0.22 | -0.08 | -1.70 | 4 |
| T8 | 短+中期双证 | 1YN0XVnQ | 0.88 | 0.65 | 0.42 | 3 |
| T9 | 复合分加速度 | Xg9MbwYb | 0.44 | 0.12 | -0.99 | 4 |
| T10 | 复合分稳定性 | zq3e8wJE | 0.73 | 0.47 | 0.84 | 3 |

判据 V：model250 判死。唯一半活通道 = 季节性水平（S 1.14 但 2Y 0.27，日历溢价近两年坍塌）；与 1.58 缺口 0.44 太大，不救。

## Wave 40 判死：other47（SEMrush 数字足迹）

10/10 REJECT，S ∈ [-0.22, 0.57]。
值得记录：流量动量族 2Y 达标（traffic z252 qMLVxXdV S0.57/**2Y1.82**；SEMrush rank 改善 kqN9oKm6 S0.56/2Y1.51）⇒ **数字足迹的近期信息是活的，但全史 Sharpe 被早期年拖死**（流量数据早期噪音大）。S 缺口 1.01，不救，判死。

## Wave 41（4oXemVdLZ4rw8VfqeFN42Yv）：other545 NEMO 2.0 网络动量 — 在飞

4 字段（score 复合 / pln_omen NLP 链接动量 / mpd 价格动量分量 / mktcap），全 VECTOR，uc 1-5 极冷。机制：文本挖掘网络动量（NEMO），与价格动量/分析师修正/情绪均不同源。10 模板（水平/动量/z/残差/稳定性/市值效率/双分量共振），<=7 算子。

## Wave 42（bdGfP8m15c3bbx1bjZYua2l）：institutions4 机构持仓 Δ — 在飞

6 字段全 VECTOR（current/previous × shares/market_value + percent_of_portfolio / percent_of_shares_outstanding），cov 0.3413。机制：机构增减仓（smart money 流）。10 模板（Δshares/ΔMV/组合权重信念/流通占比/背离构造），<=7 算子。

---

## Wave 41 判死：other545（NEMO 2.0 网络动量）

10/10 REJECT，S ∈ [-0.31, 0.78]。最强：双分量共振 2rAewx08 S0.78/F0.87 但 2Y 0.27、dd 0.49。复合分水平 0.59、价格分量 0.62——NEMO 的网络动量在 DEU TOP500 无独立信息。判死。

## Wave 42 判死：institutions4（机构持仓）

10/10 REJECT，S ∈ [-0.68, 0.58]。Δshares/ΔMV/组合权重/流通占比全灭；流通占比动量 j2YOAk0j TO 0.8753 换手爆炸。DEU 机构持仓数据（cov 0.34）不含 smart money 信号。判死。

## Wave 43（1p7zu84Ej5afcd91di6Ex9xf）：model109 修正扩散族 — 在飞

机制：**修正扩散比**（up/down 修正家数比，与 analyst7 广度通道同源但极冷 uc 0-2）+ 期望差（LT−FY2 增长差）+ 现金流 ROE + 毛利率年改善 + 应收应付周转差。10 模板全 <=5 算子。

## Wave 44（38KDmB7AN4YVb0zxAyG5pKo）：multifactor_return_pred ML 分位数 — 在飞

机制：多视界（20d/60d/120d）长短侧分位数信号 + 置信分 + 回归预测 + 季节性预测。全 uc=1 极冷（ac 10-57）。风险提示：与已死的 model250 同为 ML 复合预测族，但本集按 hedge/视界/分位结构化。10 模板全 <=5 算子。

---

## Wave 43 判死：model109（修正扩散族）

10/10 REJECT，S ∈ [-0.2, 0.84]。扩散比族（eps/revenue/target/ebitda/recommendation diffusion）全部 0.12-0.29 无信号——**model109 的冷字段扩散比与 analyst7 广度通道不同源，无信息**。最强 operating_cash_flow_return_on_equity S 0.84 但 2Y -0.15。判死。

## Wave 44 判死：multifactor_return_pred（ML 分位数面板）

10/10 REJECT，S ∈ [-0.93, 0.75]。与 model250 同命运——**DEU/TOP500/D1 对 ML 复合预测分（多视界/分位/置信结构）一致无信号**，跨两个数据集复证的机制级死亡。回归预测 0.75（2Y -0.1）、alt3 short hedge 置信 0.73（2Y 0.83）是天花板。判死。

## ★★★ Wave 45（1Q7SAQb8p5csbBCAiq53ni6）：analyst7 同源对 @W66 —— 判据 M 推翻 + 第 8 席

设置 FAST/decay0/sector。结论：**2Y 供给来自「同源盈利流指标对的 W66 修正」，不是 ebt 独有**（判据 M 修订：W44 时只有 ebi×ebt 过 2Y 是因为快窗不够快）。

| # | 慢×快 | alpha | S | F | 2Y | TO | sub | dd | fail | 与 RREPm361 互相关 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| W45-1 | net×pre | 78Ll6Pn8 | 1.88 | 1.17 | 1.39 | 0.2267 | 1.00 | 0.0701 | 1 | 0.6671 |
| W45-2 | pre×net | E56xRneK | 1.77 | 1.06 | 1.14 | 0.2279 | 0.73 | 0.0716 | 2 | — |
| W45-3 | net×ebt | ZYQNAVKQ | 1.99 | 1.29 | 1.87 | 0.2271 | 1.24 | 0.0473 | 0 | 0.8733 |
| W45-4 | ebt×net | MPYV3vLr | 1.80 | 1.08 | 1.22 | 0.2288 | 0.79 | 0.0583 | 2 | 0.6959 |
| **W45-5** | **pre×ebt** | **bl6AO0Qp** | **2.16** | **1.44** | **2.08** | 0.2257 | 1.27 | 0.0412 | **0** | 0.8652 |
| **W45-6** | **ebt×pre** | **zq3eb7No** | **2.01** | **1.28** | **1.64** | 0.2262 | 1.00 | 0.0515 | **0** | **0.6879** |
| W45-7 | gps×net | O0Ag8dG7 | 1.71 | 1.02 | 0.92 | 0.2252 | 0.88 | 0.0793 | 1 | — |
| W45-8 | net×gps | P0oKgLGK | 1.87 | 1.17 | 0.87 | 0.2230 | 1.05 | 0.0657 | 1 | — |
| W45-9 | sal×ebt | kqN9gpjd | 1.61 | 0.92 | 1.73 | 0.2265 | 1.09 | 0.0664 | 1 | 0.7349 |
| W45-10 | opr×ebt | 78Ll6PjQ | 0.74 | 0.27 | 1.48 | 0.2501 | 0.45 | 0.1050 | 3 | — |

**互相关矩阵（13 颗，threshold 0.7）**：max_mutually_below_subset = **8** = 老 7 颗 + zq3eb7No。
- zq3eb7No（ebt×pre）与 RREPm361 只 0.6879：共腿但角色互换（ebt 从快腿变慢腿、快腿换成 pre），实证**「共腿必 0.84」要按角色区分**——同腿同角色 0.87+，同腿异角色可低至 0.69。
- bl6AO0Qp（IS 最高 2.16/2.08）与 RREPm361 0.8652 只能换席；RREPm361 已验 prod 0.6881 留任，bl6AO0Qp 留档。
- zq3eb7No 全闸：S 2.01 ✓ F 1.28 ✓ 2Y 1.64 ✓ TO 0.2262 ✓ sub 1.00 ✓ fail 0 ✓ self **0.3321** ✓（池 14）；prod 测试中。

## Wave 46 判死：order_book_imbalance（盘口微结构）

10/10 REJECT，S ∈ [-1.2, 0.57]。买卖不平衡/撤单/拍卖错位/Amihud 冲击/价差全灭；TO 0.60-0.96 爆炸——**日频盘口对 delay-1 回测太快，信息在下一次开盘前已耗散**。判死。

---

## Wave 47 归因：analyst7 pre-快腿扩展 — 判据 AC（骨架容量=2 席）

| 慢×pre-Δ快 | alpha | S | 2Y | fail |
|---|---|---:|---:|---:|
| net W80 | GrW9WXMx | 1.86 | 1.08 | 1 |
| net W88 | d5WvWYnX | 1.80 | 0.98 | 1 |
| net_median W66 | 88RXRVOa | 1.68 | 1.25 | 2 |
| roa | qMLVLOXZ | 1.70 | 1.26 | 2 |
| sal | e75E5Nnz | 1.46 | 1.10 | 3 |
| 其余（grm/tbv/bps/csh/nav） | — | ≤1.17 | ≤0.97 | 3 |

**快窗 W66→W80/W88 反而杀 2Y**（1.39→1.08/0.98）⇒ 2Y 甜点锁定 W66，过窗毁 2Y（与 S 的单调性不同轴）。net/pre/gps 三角 2Y 天花板 1.39（W66），其余慢腿全灭 ⇒ **analyst7 水平×修正骨架容量 = 2 席**。

## Wave 48 判死：institutions1（内部人交易）

10/10 REJECT，S ∈ [-0.68, 0.40]。持仓变化/交易强度/金额活跃度全灭，dd 普遍 0.5-1.06（数据稀疏踩空）⇒ cov 0.23 + 内部人信号在 DEU 不定价。判死。

## Wave 49（3Z4KTW5rD50Dbfn16kmzyd7w）：pv109 债券信用联动 — 在飞

机制：Kwan 1996 债券领先股票——YTM 水平/Δ66/Δ22/年范 z（信用恶化⇒空）、bid-ask YTM 价差（债券流动性）、成交活跃度、赎回/面值比、在外 outstanding 变化（还债=信用改善）。全 VECTOR + ts_backfill 22，<=6 算子。

---

## Wave 49 判死：pv109（债券信用联动）

10/10 REJECT，S ∈ [-0.26, 0.44]。YTM 水平/变化/利差/活跃度/赎回比全灭 ⇒ DEU delay-1 日频下债券信息不领先股票。判死。

## Wave 50 判死：model262（Compustat 预测误差）

10/10 REJECT，S ∈ [-0.39, 0.91]。最强 dlttq_mae（长期债预测误差，负号）S 0.91/2Y 0.81，不足线。earnings_yield3 0.62。预测误差=不透明度溢价在 DEU 不定价。判死。

## Wave 51 判死：model144（StarPerformer DL 分）

10/10 REJECT，S ∈ [-0.38, 0.63]。2 字段 10 模板穷尽。判死。

## 备用池复核（2026-11-08）：6 颗全部不可加

备用池 vs 当前 8 席篮子互相关：wpQYNvZp 0.7486 / Vkx3MjW8 0.7441 / Xg9WNVvl 0.7199（全部卡 LLMzYrZe）、A1Vvqded 0.9087 / QPveY7Kg 0.9922（卡 mLox6Mg2）、npvwXA8l 0.9197（卡 MPY9VNY9）。max_mutually_below_subset 保持 **8**。其中 wpQYNvZp/Vkx3MjW8 本身是 MODEL+MODEL 违禁件，双重不可用。

## Wave 52（3HUwXhdug4yA9jZ4287cUDy）：model26 ARM 修正分 — 在飞

最后一个未开发数据集（548 字段，uc 479 拥挤）。机制：ARM 复合分族（国家排名/收入分量/二级盈利分/修正分/推荐变化分/升级降级数差）。与 analyst93 同型（后者出过 QPv6jLvX）。10 模板（6 水平 + 动量 + z + 价差 + 双确认），<=5 算子。风险：uc 拥挤 ⇒ prod 相关性风险高。

---

## ★★★ zq3eb7No prod 落地：0.6171 < 0.70 —— 第 8 席确认（2026-11-08）

直方图 [0.6,0.7) n=2。全闸：S 2.01 ✓ / F 1.28 ✓ / 2Y 1.64 ✓ / TO 0.2262 ✓ / sub 1.00 ✓ / fail 0 ✓ / self 0.3321 ✓ / 互相关 0.6879 ✓ / **prod 0.6171** ✓。
zq3eb7No = group_rank(add(ts_zscore(est_12m_ebt_mean, 240), ts_zscore(subtract(est_12m_pre_mean, est_12m_pre_mean_4wks_ago), 66)), sector)，DEU/TOP500/D1/FAST/decay0/trunc0.08，5 算子。

## Wave 52 判死：model26（ARM 修正分）—— 数据集宇宙穷尽

10/10 REJECT，S ∈ [-0.16, 0.86]。ARM 国家排名 0.85 / 修正分 0.86 / rank 0.85 / 二级盈利分 0.84（同一天花板，2Y 0-0.61）。ARM 复合分在 DEU/TOP500 不定价（与 analyst93 的 profitability 通道不同——后者是行业相对盈利分，可定价）。判死。
**至此 16 个数据集判死**：model36/25/109/250/262/144/26、other47/545、institutions1/4、multifactor_return_pred、order_book_imbalance、pv109 + 本段前的 44 个 cov=0。未开的仅剩 model182/162/140/313（3-7 字段 ac 2-4，密度不足 10 模板规则）与 other384（电话会文本，撞已死的新闻/文本族）。

## 第 9 席最后通路：analyst_factor_signals 严格 ATOM 第二席

bl6AvMkN（MODEL+ANALYST 双集）只用 eps_y1_estimate_change_3mo 一腿。该集共 6 个 estimate_change_3mo 字段，其余 5 个（revenue/ebitda/等）可做不相交新对 → Wave 53。

---

## Wave 53 判死：analyst_factor_signals 第二席 —— 判据 AI（收官）

4 REVIEW + 6 REJECT，最优 netprofit_y1_estimate_change_3mo S 1.42 但 **2Y 0.73**；netprofit_y2 1.27/0.99、eps_y2 1.25/0.84 全部 2Y<1.58；趋势斜率族（eps/revenue slope_1yr，uc 2-10 极冷）直接负号。y2−y1 剪刀差 -0.26。
结论：该集唯一可定价通道=eps_y1 修正（bl6AvMkN 已占用），netprofit/revenue 通道与 y2 远期修正在 DEU 无 2Y。**第二席不可得。**

---

# ★★★ 战役收官（2026-11-08）：最终篮子 8 席

| # | alpha | 数据集 | 类型 | S | F | 2Y | TO | self | prod | 算子 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | mLox6Mg2 | sentiment7+sentiment27 | 双集(SENTIMENT) | 2.05 | 1.71 | 2.53 | 0.147 | — | 0.6935 ⚠ | — |
| 2 | QPvzNNGG | predictive_starmine | 严格ATOM(MODEL) | 1.70 | 1.30 | 2.18 | 0.155 | — | 0.6777 | — |
| 3 | LLMzYrZe | predictive_starmine | 严格ATOM(MODEL) | 1.61 | 1.16 | 1.69 | 0.153 | — | 0.6697 | — |
| 4 | MPY9VNY9 | shortinterest3 | 严格ATOM(SHORTINT) | 1.59 | 1.26 | 2.36 | 0.036 | — | 0.5986 | — |
| 5 | QPv6jLvX | analyst93 | 严格ATOM(ANALYST) | 1.59 | 1.52 | 2.01 | 0.0411 | — | 0.6615 | — |
| 6 | bl6AvMkN | afs+starmine | 双集(MODEL+ANALYST) | 1.61 | 1.36 | 2.15 | 0.1097 | 0.514 | 0.6470 | — |
| 7 | RREPm361 | analyst7 | 严格ATOM(ANALYST) | 2.02 | 1.25 | 1.82 | 0.2508 | 0.2924 | 0.6881 | 5 |
| 8 | zq3eb7No | analyst7 | 严格ATOM(ANALYST) | 2.01 | 1.28 | 1.64 | 0.2262 | 0.3321 | 0.6171 | 5 |

互相关全对 ≤0.7（max_mutually_below_subset=8）。
未达标缺口：第 9/10 席。来源穷尽证明：16 数据集本段判死 + 44 cov=0 + 备用池 6 颗复核全阻塞 + analyst7 骨架容量 2 席（互相关）+ starmine 2 席（备用池互相关）+ afs 第二席判死 + 剩余未开集（model182/162/140/313 共 18 字段 ac 12、other384 文本族已死×5）密度不足或家族已死。
风险提示：prod 每日漂移，正式提交前须逐颗 refresh=True 终验（mLox6Mg2 0.6935 最贴线）。

## Wave 54 判死：analyst93 技能族 —— 判据 AJ（终局）

10/10 REJECT，S ∈ [-0.42, 0.96]。准确率 rule2 −0.11、修正方向正确率 0.41、预测跟随盈利 profitability2 0.96（2Y 0.41）、一致性 −0.42。anl93 唯一可定价通道=推荐跟随盈利（QPv6jLvX 已占用），技能/准确率/一致性维度在 DEU 无信息。判死。
**至此挖掘正式穷尽**：17 数据集本段判死 + 44 cov=0 + 5 密度不足（model182/162/140/313、other384 文本族）+ 备用池 6 颗互相关阻塞 + 全部家族容量映射完毕（analyst7×2、starmine×2、anl93×1、shortinterest×1、sentiment×1、afs×1）。

**最终交付 = 8 席**（6 严格 ATOM + 2 合法双集）。第 9/10 席在当前约束（region=DEU 固定、REGULAR/ATOM only、禁混集合、互相关 ≤0.7、算子 ≤12）下不存在合规来源。

---

# ★★★ 2026-11-08 深夜变阵（用户指令 + prod 漂移事件）

## 变阵 1：用户指令——交付篮子互相关标准从 ≤0.7 收紧为 **<0.5**

以 threshold=0.5 重算 14 颗全候选池：**max_mutually_below_subset = 6**
[RREPm361, QPvzNNGG, MPY9VNY9, A1Vvqded, QPv6jLvX, bl6AvMkN]
出局名单：LLMzYrZe（0.678 vs QPvzNNGG）、zq3eb7No（0.688 vs RREPm361）、bl6AO0Qp/ZYQNAVKQ/YP1YgK7J（0.87-0.94 vs RREPm361）、Xg9WNVvl（0.72 vs LLMzYrZe / 0.60 vs QPvzNNGG）、QPveY7Kg（0.916 vs A1Vvqded）、npvwXA8l（0.92 vs MPY9VNY9）。
关键新证据：QPvzNNGG↔LLMzYrZe 0.678（同集双席在 0.5 下不可共存——starmine 容量从 2 席降为 1 席）。

## 变阵 2：mLox6Mg2 prod 漂移爆表——0.9922 FAIL（refresh 终验 2026-11-08）

直方图出现 [0.9,1.0] n=1 单钉（生产池出现近同构件，疑为他人提交同骨架）。情绪席位失守。
**A1Vvqded 是 mLox6Mg2 的近孪生**（同 snt7+snl27 骨架，仅 decay 2/4 与一处 backfill 差异，互相关 0.9087；S 1.90/F 1.47/TO 0.1593 无 fail）⇒ 其 prod 大概率同命运，实测中。
QPveY7Kg（0.9922 vs mLox6Mg2）几乎必死同钉。

## 变阵后状态

- 6 席篮子 = [RREPm361, QPvzNNGG, MPY9VNY9, QPv6jLvX, bl6AvMkN] 5 颗已验 + A1Vvqded（prod 实测中）
- 若 A1Vvqded prod 死：情绪族无交付件，篮子降为 5 席
- 缺口：10 - 篮子席位（6 或 5）= 4 或 5 席，全部待新来源（当前 DEU 数据集宇宙已穷尽）

## 变阵终态（2026-11-08 02:26+）：A1Vvqded prod 0.916 FAIL ⇒ 情绪族全灭，篮子收敛 **5 席**

- A1Vvqded prod 0.916（与 mLox6Mg2 同一颗 [0.9,1.0] 生产池钉子）；QPveY7Kg 按「族代表预判」规则判死（族内两颗实测 prod 0.99/0.92，同骨架 0.99 孪生不再烧槽）。
- **最终篮子（<0.5 互相关标准）= 5 席**：
  1. RREPm361（analyst7，S 2.02/2Y 1.82/prod 0.6881 ⚠ 余量 0.012 薄）
  2. QPvzNNGG（starmine，S 1.70/2Y 2.18/prod 0.6777）
  3. MPY9VNY9（shortinterest3，S 1.59/2Y 2.36/prod 0.5986）
  4. QPv6jLvX（anl93，S 1.59/2Y 2.01/prod 0.6615）
  5. bl6AvMkN（afs+starmine，S 1.61/2Y 2.15/prod 0.6470）
- 互相关关键对：QPvzNNGG↔bl6AvMkN 0.402（最大对，其余全 <0.4）。
- 备援：zq3eb7No（prod 0.6171，与 RREPm361 互相关 0.688 超新标准不能同篮）为 RREPm361 提交时漂移过墙的**换防备选**（prod 余量 0.083）。
- 出局名单（<0.5 标准）：LLMzYrZe（0.678 vs QPvzNNGG）、zq3eb7No（0.688 vs RREPm361）、mLox6Mg2/A1Vvqded/QPveY7Kg（prod 族灭）、Xg9WNVvl（0.60/0.72）、npvwXA8l（0.92）、bl6AO0Qp/ZYQNAVKQ/YP1YgK7J（0.87-0.94）。
- 缺口：10 − 5 = **5 席**，待用户裁定路径（放宽互相关回 ≤0.7 可回 7 席 / 新区域 / 其他）。

## ⚠⚠ prod 漂移风暴第二波（2026-11-08 03:00-03:40）：MPY9VNY9 死亡 —— 篮子 5→4

**MPY9VNY9 prod = 0.9924 FAIL**（原 0.5986、余量 0.101，ts_target_tvr_decay 独特结构也被近同构件顶死）。今夜已有 mLox6Mg2(0.9922)/A1Vvqded(0.916)/MPY9VNY9(0.9924) 三颗爆表；漂移速度=小时级。
npvwXA8l（同 shortinterest 家族孪生）按族代表预判规则连坐判死。shortinterest 族清零。

**紧急终验结果（refresh 重算）**：
| alpha | prod | 漂移 | 判 |
|---|---:|---|---|
| RREPm361 | 0.6881 | 0（直方图逐位一致） | ✓ |
| zq3eb7No | 0.6171 | 0（缓存一致） | ✓（换防备选） |
| QPvzNNGG | 0.6777 | 0（重算落地） | ✓ |
| QPv6jLvX | 0.6615 | 0（重算落地） | ✓ |
| bl6AvMkN | 0.6470 | 0（重算落地） | ✓ |

**当前有效篮子 = 4 席** [RREPm361, QPvzNNGG, QPv6jLvX, bl6AvMkN]（互相关最大对 0.402）+ zq3eb7No 换防备选。
教训固化：**未提交候选的 prod 值保鲜期以小时计**——mLox6Mg2 事件（0.6935→0.9922）与 MPY9VNY9 事件（0.5986→0.9924）都发生在「测后 24-48h」内。提交动作必须「终验→立即提交」，不得隔夜。

## Wave 55/56 判死：model313（无形资产强度）/ model140（通胀利率敏感度）

- Wave 55（2U2n3sePz4QGcH55ADVKU4v）：10/10 REJECT，S ∈ [-0.19, 0.69]。无形强度/知识资本/组织资本全灭——DEU 不给无形资产溢价定价。
- Wave 56（3FuvREbWv4zvar8XyBL2vFR）：10/10 REJECT，S ∈ [-0.05, 0.46]。通胀/利率敏感度族全灭。
- Wave 57（2I3K2PMY4Ef8HLv7OLfwsU）：model182 网络动量 — 在飞。Wave 58（model162 预测价格）待派。

至此 19 数据集判死。剩余未探仅 model162 一波。

## Wave 57/58 判死：model182（网络动量）/ model162（财报会预测价格）—— 数据集宇宙 100% 穷尽

- Wave 57（2I3K2PMY4Ef8HLv7OLfwsU）：10/10 REJECT，S ∈ [-0.36, 0.37]。网络动量家族二次证伪（与 other545 同判）。
- Wave 58（9aOSS3xQ50SalU132c8Y1Pp）：10/10 REJECT，最优 vwap_126 水平 LLM30lx2 S 1.10/F 1.21/2Y 1.28（F>S 的低换手形态，但 S 缺口 0.48）。
- **DEU/TOP500/D1 有覆盖数据集 68 个全部处置完毕**（本段 20 判死 + 前段 44 cov=0 + 4 个已交付家族）。穷尽证明无死角。

---

# ★ 终局状态（2026-11-08 04:00）

**有效篮子 = 4 席（全部 prod 零漂移终验）+ zq3eb7No 换防备选**：
| # | alpha | prod | 互相关 |
|---|---|---:|---|
| 1 | RREPm361 | 0.6881 | 最大对 0.402 |
| 2 | QPvzNNGG | 0.6777 | |
| 3 | QPv6jLvX | 0.6615 | |
| 4 | bl6AvMkN | 0.6470 | |
| 备 | zq3eb7No | 0.6171 | 0.688 vs RREPm361（<0.5 下不可同篮） |

**今夜死亡名单（prod 漂移风暴）**：mLox6Mg2 0.9922、A1Vvqded 0.916、QPveY7Kg（族）、MPY9VNY9 0.9924、npvwXA8l（族）——情绪族与 shortinterest 族清零。
**结构性缺口**：10 目标 − 4 席 = 6 席。数据集宇宙 100% 穷尽 + 漂移风暴把既有候选又削 2 席。剩余路径全部需要用户级决策（换区域/放宽互相关/接受 4 席/暂停）。

**漂移风暴方法论沉淀**：未提交候选 prod 保鲜期=小时级；「终验→立即提交」是唯一纪律；家族内一颗被生产池近同构件打死 ⇒ 同族孪生全部连坐（族代表预判规则的双向适用）。
