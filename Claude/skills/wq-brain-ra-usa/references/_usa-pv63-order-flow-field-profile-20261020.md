# pv63「Order Book」字段画像（USA / TOP3000 / D1）

> as_of 2026-10-20　数据集：`pv63`（category = pv，Order Book）
> 元数据：16 字段 / MATRIX 全量 / coverage 0.9851 / userCount 5–23 / alphaCount 6–27 / valueScore 2 / pyramidMultiplier 1
> 状态：**未点亮塔（PV）新候选，本库无 dead_end 记录；批 1（8 探针）预注册已发。**
> 定位：PV 塔第 5 个候选数据集。前四个的结局：`chart_return_model` 2Y 2.42 但全期 S 0.59（regime 依赖）、
> `pattern_scores` S≤0.63（相似度无方向）、`continuation_score` fitness 天花板 0.42、`dl_volume_pred` max|S| 0.65（已封存）。
> **本集的差异点：它是逐笔事件流的日频聚合，不是模型输出。** OFI / OBI 可以用教科书形式直接构造。

---

## 1. 字段清单（全 16，无子集）

覆盖率除 `ptsl` 为 0.9825 外，其余 15 个均为 **0.9853**。

| 组 | # | 字段 | 含义 | aC | user | 归一化形态 |
|---|---|---|---:|---:|---|
| **Taker（成交侧）** | T1 | `pv63_d1_vbai` | 激进买成交股数（吃 ask） | 19 | 17 | 绝对股数 |
| | T2 | `pv63_d1_vsai` | 激进卖成交股数（砸 bid） | 27 | 23 | 绝对股数 |
| | T3 | `pv63_d1_bain` | 激进买成交笔数 | 19 | 16 | 绝对笔数 |
| | T4 | `pv63_d1_nias` | 激进卖成交笔数 | 24 | 21 | 绝对笔数 |
| | T5 | `pv63_d1_iaba` | 激进买成交金额（USD） | 20 | 18 | 绝对金额 |
| | T6 | `pv63_d1_iasa` | 激进卖成交金额（USD） | 16 | 12 | 绝对金额 |
| | T7 | `pv63_d1_vtni` | 当日总成交股数 | 16 | 16 | 绝对股数 |
| **Maker（挂单侧）** | M1 | `pv63_d1_vpbi` | 最佳买价新增挂单股数 | 6 | 6 | 绝对股数 |
| | M2 | `pv63_d1_vpai` | 最佳卖价新增挂单股数 | 8 | 7 | 绝对股数 |
| | M3 | `pv63_d1_nibp` | 最佳买价挂单事件数 | 20 | 11 | 绝对笔数 |
| | M4 | `pv63_d1_pain` | 最佳卖价挂单事件数 | 12 | 10 | 绝对笔数 |
| **Withdrawal（撤单侧）** | W1 | `pv63_d1_vwbi` | 最佳买价撤回股数 | 10 | 7 | 绝对股数 |
| | W2 | `pv63_d1_vwai` | 最佳卖价撤回股数 | 14 | 10 | 绝对股数 |
| | W3 | `pv63_d1_nibw` | 最佳买价撤单事件数 | 6 | 6 | 绝对笔数 |
| | W4 | `pv63_d1_wain` | 最佳卖价撤单事件数 | 6 | 5 | 绝对笔数 |
| **价格** | X1 | `pv63_d1_ptsl` | 当日最后成交价（USD） | 12 | 10 | 价格水平 |

**★ 结构特征（决定构造纪律）**：

1. **三组 × 双口径**：Taker / Maker / Withdrawal 各成一组，每组都有「股数」与「笔数」两个口径。
   双口径不是冗余——股数口径衡量**大单**，笔数口径衡量**单数密度**（小单/散户）。两者方向若背离，
   说明大单与小单在反向操作，这本身就是信息（见 H5）。
2. **除 `ptsl` 外全部是绝对量** ⇒ 裸截面 rank 是 **size 代理**。所有构造必须先除以 `vtni`（同日内归一）
   或做自身时序位置（`ts_rank` / `ts_zscore`）。**这是本集第一铁律，违反即得到市值 alpha。**
3. **日频、cov 0.9853**：无需 `ts_backfill` 承载缺测，壳层保留它只为与历史批次可比。
4. **aC 6–27，user 5–23**：平台几乎无人挖过。`sharpe_filter_removed=0` ⇒ 领域内的字段没有被
   sharpe 过滤器隐藏，16 个字段全部可用。
5. **全部 MATRIX**：不需要 `vec_*` 聚合。

---

## 2. 机制假设（可证伪）

### H1 Taker 攻击性不平衡（OFI 的成交侧）
`(vbai − vsai) / vtni` —— 激进买占当日成交的比例减去激进卖。
信息交易者用市价单表达方向；买盘攻击占优 ⇒ 短期正收益。
- 文献：Cont, Kukanov & Stoikov (2014)；Chordia & Subrahmanyam (2004)。
- **反号必须成对测**：USA 是最有效率的市场，正号可能已被套利，负号（过度反应反转）同样可能。

### H2 Maker 挂单不平衡（OBI）
`(vpbi − vpai) / vtni` —— 买侧新增挂单相对卖侧。
买侧深度增加 ⇒ 价格上行压力（教科书 OBI）。
- 文献：Cont, Stoikov & Talreja (2010)；Gould et al. (2013)。

### H3 撤单不对称（流动性撤离）
`(vwbi − vwai) / vtni` —— 买侧撤单相对卖侧。
买方撤单多 ⇒ 买侧支撑消失，做市商不愿承接 ⇒ 价格下行。**预期方向为负号用法 `−(vwbi−vwai)/vtni`。**
- 文献：Easley, López de Prado & O'Hara (2012) 流动性毒性；Hasbrouck (1991)。

### H4 净订单簿压力（三腿同数据集合成）
`((vpbi − vwbi) − (vpai − vwai)) / vtni` —— 买侧净挂单减卖侧净挂单。
把「挂单」与「撤单」合成一个净供给量，比单看挂单更接近订单簿的真实变化。
- **合规说明**：这是**同一数据集、同一机制**的三个观测面合成，不是跨数据集混信号；
  H1/H2/H3 各自作为单源对照同批发测（禁用"混信号"规则的是不同信号源相加，不是同一机制的面板合成）。

### H5 笔数口径（小单密度）
`(bain − nias) / (bain + nias)` —— 与 H1 的股数口径对照。
若 H1 与 H5 同向且幅度接近 ⇒ 大小单同源；若背离 ⇒ 大单与小单逆向，信息在大单侧。
- 这是本集独有的**双口径检验**，其他订单流数据集通常只有单一口径。

### H6 激进买执行价格成本（即时价格冲击）
`(iaba / vbai) / ptsl − 1` —— 激进买成交均价相对当日收盘价的偏离。
买方越急切，成交价越高于收盘价（若之后价格回落）或越低于收盘价（若买盘推动价格上行）。
- 这个构造用 `ptsl` 做**价格归一**（美元金额 → 无量纲），不是用价格水平做信号。

### H7 撤单率时序异常（做市商供给意愿）
`ts_zscore((nibw + wain) / (nibp + pain + 1), 66)` —— 撤单事件占挂单事件比例的 66 日 z 分。 <!-- lint:counterexample: 买卖队列合计口径（分子/分母） -->
高撤单率 = 做市商集体撤离流动性 = 后续波动放大 / 反转。
- 分母 `+1` 是防零保护；分子分母均为无量纲计数比。

### 已排除的假设
- **不做跨数据集混合**（ATOM 约束）。
- **不用 `ptsl` 单独做信号**（价格水平 = size 代理）。
- **不做「成交量预测」**：`vtni` 是同期实际成交量，不是预测值；预测方向已在 `dl_volume_pred` 判弱。

---

## 3. 适用模板

- **比值型**（H1/H2/H3/H5）：`divide(subtract(A, B), C)`，C 取 `vtni` 或 `add(A, B)`。
- **净额型**（H4）：`divide(subtract(subtract(A, B), subtract(C, D)), vtni)`。
- **价格成本型**（H6）：`subtract(divide(divide(iaba, vbai), ptsl), 1)`。
- **时序异常型**（H7）：`ts_zscore(<ratio>, 66)`；备选 `ts_rank(<ratio>, 252)`（dl_volume_pred 教训：
  归一化可能抹掉信号，也可能救 SUB，必须实测对照）。
- **通用壳**：`quantile(group_rank(hump(ts_backfill(winsorize(<SIG>, std=4), 252), hump=0.01), industry))`。
  `winsorize` 必须具名 `std=4`；`quantile` 只接 1 参数。

---

## 4. 批 1 预注册（8 探针，写死）

> 设置：EQUITY / USA / TOP3000 / D1 / **SUBINDUSTRY** / decay 5 / truncation 0.08 /
> nanHandling ON / unitHandling VERIFY / pasteurization ON / maxTrade OFF / FASTEXPR。
> 区间为平台缺省（与历史批次可比）。

| 探针 | 假设 | 壳内 SIG | 形状 |
|---|---|---|---|
| P1 | H1 正向 | `divide(subtract(vbai, vsai), vtni)` | 股数比值 |
| P2 | H1 反向 | `multiply(-1, divide(subtract(vbai, vsai), vtni))` | 股数比值（镜像） |
| P3 | H2 正向 | `divide(subtract(vpbi, vpai), vtni)` | 挂单比值 |
| P4 | H3 负向 | `multiply(-1, divide(subtract(vwbi, vwai), vtni))` | 撤单比值 |
| P5 | H4 净压力 | `divide(subtract(subtract(vpbi, vwbi), subtract(vpai, vwai)), vtni)` | 净额 |
| P6 | H5 笔数 | `divide(subtract(bain, nias), add(bain, nias))` | 笔数比值 |
| P7 | H6 价格成本 | `subtract(divide(divide(iaba, vbai), ptsl), 1)` | 无量纲价格 |
| P8 | H7 撤单率 | `ts_zscore(divide(add(nibw, wain), add(add(nibp, pain), 1)), 66)` | 时序 z |

**预注册判据**：

- 任一 `S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB PASS` 且 `fail=0` ⇒ 立即 `check_correlation(refresh=True)`
  （prod/self < 0.7；**提交必须等用户明确确认**）。 <!-- from config.prod_corr_max -->
- **P1 vs P2 同弱**（|S| 均 <0.8）⇒ taker 方向信息不足，本集只剩 maker 侧（H2/H3/H4/H7）。
- **P3/P4/P5 显著强于 P1** ⇒ maker 行为是主机制，批 2 沿「挂单×撤单」二维穷举（窗 / 分组 / 中性化）。
- **P6 与 P1 差 <0.1** ⇒ 笔数与股数同源，后续只取一个口径。
- **P7 单独 |S|<0.8** ⇒ 即时价格冲击不是独立信息，H6 降级为对照项。
- **全部 |S|<0.8** ⇒ 判本集为弱。补批前先看 TO：若 TO 健康（1–70%）才允许补一批
  `ts_rank`/`ts_mean` 归一化对照；若 TO 已贴地或爆表，直接封存（dl_volume_pred 的教训：
  「只在 TO 健康时补事件门控」的前提要先成立）。
- **TO >70% 成片** ⇒ 批 2 统一加 `ts_mean(.,5)` 或提高 decay，**不得同时改符号与平滑**（一次一变量）。
- **TO <1% 成片** ⇒ 先查比值是否近似静态（事件计数日频变化不应低），再决定是否补批。
- **risk-neut <0.3 成片** ⇒ 判本批为 size/流动性代理，不进入组合腿登记。
- **prod ≥0.75 或踩线失败** ⇒ 按决策表 D0-P 处置，不做同族磨参数。

---

## 5. 回测结果及指标

### 5.1 批 1（multisim `4zRh6LftZ4tF8GH7ulyup1F`，8/8 COMPLETE，2026-10-20）

设置同上 §4；区间 2014-01-01 → 2023-12-31。**全部 UNSUBMITTED，无提交动作。**

| 探针 | alpha | S | F | 2Y | SUB（limit） | TO | returns | risk-neut | fail |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 taker 股数 | `KPmELNEE` | 0.78 | 0.32 | **2.54** | −0.08（0.34） | 1.15% | 2.17% | 0.57 | 3 |
| P2 P1 镜像 | `zqrRW8NK` | 0.27 | 0.06 | 0.50 | 0.30 | 1.17% | 0.61% | −0.09 | 3 |
| P3 maker 挂单 | `9qE7RjpK` | 0.63 | 0.22 | 1.50 | 0.27 | 1.73% | 1.56% | 0.37 | 3 |
| P4 撤单（负号） | `xA1dn3NN` | 0.50 | 0.15 | 1.80 | 0.07 | 1.77% | 1.12% | 0.06 | 3 |
| P5 净簿压力 | `6XAeEjpJ` | 0.25 | 0.05 | 1.43 | 0.14 | 1.58% | 0.60% | −0.10 | 3 |
| P6 taker 笔数 | `XgR8Kb7m` | **0.79** | 0.33 | 2.51 | **0.36 PASS** | 1.14% | 2.20% | 0.54 | 2 |
| P7 执行价成本 | `qME6Xxjv` | 0.20 | 0.04 | 1.46 | −0.15 | 1.24% | 0.53% | 0.16 | 4 |
| P8 撤单率 z66 | `LL5dRN71` | 0.69 | 0.25 | 1.44 | −0.09 | 1.15% | 1.64% | 0.28 | 4 |

**靶心结论：0 颗全闸通过，全 |S| < 0.8 ⇒ 按预注册判「弱」。** 但 TO 全部在 1.14–1.77%（健康、不贴地也不爆表），
故按预注册允许补**一批**归因对照，而不是直接封存。

### 5.2 批 1 归因（先归因后补批）

1. **不是数据起始假象**：`get_alpha_yearly_stats` 显示 P1/P6 在 2014–2023 **每年都有成交与收益**
   （P1：2016 S1.49 / 2021 S1.10 / **2022 S3.16** / **2023 S1.61**，但 2017 −0.60 / 2020 −1.06）。
   ⇒ 全期 S 被稀释是**真实 regime 依赖**，不是「数据从 2022 才开始」。
2. **P1 ≈ P6（差 0.01）**：股数口径与笔数口径是同一信息；但 **P6 的 SUB 通过（0.36）、P1 不通过（−0.08）**
   ⇒ 笔数口径在高低流动性两段更平衡，后续若留一条口径应留 **P6**，不是 P1。
3. **P2 不是 P1 的严格镜像**（0.27 vs 0.78；若严格镜像应 ≈ −0.78）：`group_rank/quantile` 是非线性的，
   但方向结论清楚 —— **正向 taker 攻击性** 才是信号，反号不成立。
4. **maker 侧（P3 0.63）弱于 taker（0.78）**，撤单（P4 0.50）更弱；**净簿压力（P5 0.25）把两腿相减后反而消失**
   ⇒ 挂单/撤单 / 净额不是主机制，**PnL 主要由 taker 攻击性承担**（与论坛「攻击性与半衰期分引擎」的先验一致）。
5. **P7 执行价成本 0.20 / P8 撤单率 0.69**：两者都不是独立 alpha；P8 的 2Y 1.44 也低于闸。
6. **risk-neut**：P1 0.57 / P6 0.54（**不是纯 size 代理**），其余 ≤0.37。P4 0.06、P5 −0.10 ⇒ 撤单/净额族的
   收益几乎全来自风格暴露，按预注册不进组合腿登记。
7. **TO 反常低（≈1.1–1.8%）的解释**：日频事件计数比值经过 decay 5 后仍只有 1% 换手 ⇒ 信号是**慢变量**
   （股票级结构性攻击性），不是「今日订单流」的即时信号。这正好解释「2022–2023 强、全期弱」：
   它更像一个**近两年才被定价的慢因子**，而不是微观结构 alpha。
   ⇒ 批 2 的唯一科学问题是：**改成「相对自身基线的偏离」后是否变成全期有效**（而不是继续调 decay/窗）。

### 5.3 批 2（multisim `15pm1YgDX4RtbCJ5BzyX2U3`，8 条，2026-10-20 发出）

**只改一条轴：水平 → 自身偏离**（设置与批 1 完全相同，一次一变量）：

| # | 构造 | 对应批 1 |
|---|---|---|
| B2-1 | `ts_av_diff(taker, 22)` | P1 |
| B2-2 | `ts_zscore(taker, 66)` | P1 |
| B2-3 | `ts_zscore(taker, 252)` | P1 |
| B2-4 | `ts_av_diff(count, 22)` | P6 |
| B2-5 | `ts_zscore(count, 66)` | P6 |
| B2-6 | `ts_av_diff(maker, 22)` | P3 |
| B2-7 | `ts_av_diff(netbook, 22)` | P5 |
| B2-8 | `ts_zscore(taker − maker, 66)` | 新增：攻击性−被动性价差 |

**批 2 的反向先验（解读前必须先认这条）**：台账 `USA-MFRP-LEVEL-BLEND-PROD-STRUCTURAL-DEAD`
记录「**时间维度解拥挤**（`ts_rank` / `ts_zscore` / `ts_av_diff` 相对自身历史）**会摧毁横截面信号**
（sharpe 1.45 → 0.20–0.29）」。即「水平 → 自身偏离」这条路在本塔已有一次**明确失败**的同类证据
（解的是 prod 拥挤，代价是 alpha 本身）。批 2 正是踩这条轴，所以：
① 若 B2 组普遍低于批 1（S 降 >0.2）⇒ **不是壳的问题，是这条轴在本塔不可用**，直接按封存判据处置，
**不要**再换窗抢救；
② 只有当 B2 ≥ 批 1 才说明 pv63 的偏离确实携带新信息（与 MFRP 的差异：pv63 是事件计数比值，
MFRP 是预混合的水平因子），此时才允许往设置档推进。

**批 2 判据（写死）**：任一全闸 ⇒ 立即 `check_correlation(refresh=True)`；
**若 8 条仍全 |S|<1.0 ⇒ 封存 pv63**（两批、16 条、覆盖三面×双口径×水平/偏离，已穷尽本集主轴），
登记 `USA-PV63-ORDER-FLOW-WEAK`，不再补第三批；若 B2 显著高于批 1（≥1.2）但未全闸 ⇒ 才允许
沿「偏离」轴做一次设置档（decay / 中性化）对照。

**批 2 实测（8/8 COMPLETE，2026-10-20）**：

| # | alpha | 构造 | S | F | 2Y | SUB(limit) | TO | returns | risk-neut | fail |
|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| B2-1 | `P0MO18OJ` | Δ22 taker | 0.71 | 0.28 | 2.07 | −0.20(0.31) | 1.18% | 1.88% | 0.28 | 3 |
| B2-2 | `O0Jx9VxR` | z66 taker | 0.68 | 0.24 | 1.52 | −0.02(0.29) | 1.12% | 1.62% | 0.24 | 4 |
| B2-3 | `gJW93d8v` | z252 taker | 0.64 | 0.22 | 1.60 | −0.13(0.28) | 1.11% | 1.54% | 0.23 | 3 |
| B2-4 | `qME6X3NO` | Δ22 count | 0.25 | 0.06 | 2.04 | 0.12 | 1.17% | 0.64% | −0.27 | 2 |
| B2-5 | `6XAeEJlP` | z66 count | 0.51 | 0.16 | 1.94 | 0.08(0.22) | 1.13% | 1.26% | 0.09 | 3 |
| B2-6 | `qME6X3jO` | Δ22 maker | 0.61 | 0.21 | 1.60 | 0.22(0.26) | 1.77% | 1.45% | 0.21 | 3 |
| B2-7 | `QPY9Qg3M` | Δ22 netbook | 0.42 | 0.12 | 1.90 | 0.00 | 1.63% | 0.97% | −0.01 | 3 |
| B2-8 | `gJW93dQM` | z66 taker−maker | 0.57 | 0.18 | 1.60 | 0.23(0.25) | 1.11% | 1.29% | 0.29 | 3 |

**结论：命中封存判据（8 条全 |S|<1.0，最高 0.71）⇒ pv63 判弱封存**，
登记 `USA-PV63-ORDER-FLOW-WEAK`，不再发第三批。三条归因（写进 §5.2 的第 8–10 条）：

8. **「水平 → 自身偏离」在本塔确实摧毁信号**（与 `USA-MFRP-LEVEL-BLEND-PROD-STRUCTURAL-DEAD` 的先验一致）：
   taker 三窗全部低于批 1（0.78 → 0.71/0.68/0.64），count 从 0.79 掉到 0.51/0.25，
   netbook 从 0.25 只微升到 0.42（仍 <0.5）。即批 1 的 S 主要来自**股票级水平差异**，不是「今天比平时异常」。
   ⇒ 这条轴在 PV 塔第二次复证失败，后续任何 PV 集都不再把「时序归一」当破 prod / 提 S 的默认杠杆。
9. **2Y 反而被偏离轴抬起来**（taker Δ22 2.07 vs 水平 2.54 不算抬；count Δ22 2.04 vs 2.51；netbook 1.90 vs 1.43）：
   全期 S 降、2Y 升 ⇒ 是「近两年 sharper、全期更 noisy」的典型反向选择，不能作为救 S 的手段。
10. **SUB 的绝对值全面缩小**：批 1 P6 的 SUB 0.36（PASS，limit 0.36）在偏离版降到 0.12（B2-4）、
   0.08（B2-5）；P1 的 −0.08 降到 −0.20。偏离轴把「低流动性段相对更强」的结构一起抹掉了，
   SUB 与 S 同向下降 ⇒ 本塔的核心矛盾（水平才有截面信息、但水平版本 SUB 只有 P6 一条贴线过）无法用窗解决。

**封存状态**：已按本文档与交付日志登记判弱结论；`seal_dead_end` 的论坛取证闸为 fail-closed，
本轮**无对应 `forum_recon_negative_*` 记录**，故未强行封存（`force_seal` / `require_forum_recon=False`
均需人工确认，见 AGENTS.md §8.11）。待下一轮补一次论坛取证后再沉降，**在此之前 pv63 视为已判弱、不得重发**。

---

## 6. 风险与预判

- **prod 墙是第一优先假设**：同塔 `USA-OBI-LEVEL-FAMILIES-PROD-WALL` 记录 order_book_imbalance
  的水平/慢窗族 prod 0.76–0.81，`USA-ORDER-FLOW-IMB-RANK-WEAK` 记录 order_flow_imb 纯截面 rank
  S≤0.87。**pv63 是这两个族的原始上游数据**，但它们的失败模式必须当作先验：IS 一旦达标，
  立刻 `check_correlation`，不要先做 Mode A 调参。
- **2Y 墙**：order_book_imbalance 全族卡 LOW_2Y_SHARPE 1.37–1.43。若 pv63 出现 S 高但 2Y <1.58，
  先查是否为 2022 前后 regime 依赖（`chart_return_model` 2Y 2.42 / 全期 0.59 是同塔同型教训），
  再决定是否换窗，不要直接判死。
- **TO 墙**：论坛实证 order_flow_imb 被列为「天然高换手基因」数据集、被推荐做 High Turnover PPA。
  pv63 是同一类事件流，裸用比值 TO 可能 >70%。decay 5 已压一档；`hump 0.01` 在壳内。
  若仍爆表，批 2 用 `ts_mean(.,5)` 而不是砍信号。
- **分母为 0**：`vtni`、`add(bain,nias)` 理论上可为 0（停牌日）。cov 0.9853 说明停牌日无数据，
  nanHandling ON 会把它们排除，不额外加常数（加了会改变比值语义）。
- **ATOM 合规**：16 个字段全部来自 `pv63`；`industry` 分组属豁免。

---

## 7. 文献与论坛证据（可复用）

1. **Cont, Kukanov & Stoikov (2014)**, "The Price Impact of Order Book Events" —— OFI 对短期价格变动
   近似线性；这是 H1 与 H4 的理论依据。
2. **Chordia & Subrahmanyam (2004)**, "Order imbalance and individual stock returns" —— 订单不平衡
   在日频上预测短期收益。
3. **Cont, Stoikov & Talreja (2010)**, "A stochastic model for order book dynamics" —— OBI 作为队列
   失衡的简化统计量；H2 的依据。
4. **Easley, López de Prado & O'Hara (2012)**, VPIN —— 订单流毒性/流动性提供者的逆向选择；H3/H7 的依据。
5. **Hasbrouck (1991)**, "Measuring the information content of stock trades" —— 交易方向的信息含量。
6. **论坛「一个被忽视的 Alpha 来源：订单流失衡的微观结构信号」**（2025-12-04）—— 给出 OFI 的 tick 级定义
   `Σ(delta_bid | trade at ask) − Σ(delta_ask | trade at bid)`，并明确要「除以该时段总笔数或总成交量」。
   pv63 的 `nibp/nibw/pain/wain` 正是最佳买卖价的挂单/撤单事件数 ⇒ 日频版 OFI 可直接由本集构造。
7. **论坛「谁在付 Spread？—— 订单流攻击性、半衰期分层与一个双引擎架构」**（2026-09-02）—— 单数据集
   `pv103` 在 GBR/TOP700 做到 IS Sharpe 1.96、全硬检查 PASS。**结论：PV 塔的微观结构数据能过平台闸，
   失败都发生在构造层，不在数据层。** 其「攻击性 × 半衰期分层」的双引擎思路提示：taker 方向
   （攻击性）与 maker 撤单（半衰期）应当分开建模，不要一开始就合并。
8. **论坛「开发高换手率的 Alpha 因子」**（2026-04-08）—— order_flow_imb 被作为 High Turnover PPA
   的首选数据集，120 字段 / valueScore 5.0 / 仅 56 个 alpha（蓝海）。**结论：该族天然高换手，
   TO 控制要前置设计，不能事后补救。**

### 与两个判死族的区别（避免被误判为同族重复）

| 判死族 | 字段本质 | 已证伪的构造 | pv63 的差异 |
|---|---|---|---|
| `order_flow_imb`（S≤0.87） | 客户/机构**分类后**的订单流不平衡 | 纯截面 rank、`ts_mean`、`ts_delta`、`ts_zscore`、pro−customer 价差 | pv63 是**逐笔事件计数**，可做 taker/maker/withdrawal 三面分解与双口径对照 |
| `order_book_imbalance`（prod 0.76–0.81、2Y 1.37–1.43） | fill_prob / dark / auction / patience / price-pair 等**衍生概率** | 水平 / 慢窗同族变体 | pv63 是**原始事件流**，可直接构造 OFI/OBI 的教科书形式 |

⇒ pv63 是这两个族的上游原始数据，不是同族变体。但它们的失败模式（prod 墙、2Y 墙）是本集的
**第一优先假设**，已写入 §6 与预注册判据。
