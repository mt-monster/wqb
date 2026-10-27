# pv115「做空量 + Nasdaq 开收盘集合竞价」字段画像（USA / TOP3000 / D1）

> 采集：2026-10-20 `get_datasets(category="pv", region="USA", delay=1, universe="TOP3000")` +
> `get_datafields(dataset_id="pv115", region="USA", delay=1, universe="TOP3000")`（平台实时返回）。
> **状态：备选，未开挖**（当前主线 = pv63 批 1）。开挖前必须按 S0 三查再核一次判死 / 跨区弱 / 塔位。
> 本文件按「字段画像 → 适用模板 → 预注册回测 → 风险」组织，回测结果回填 §4。

## 0. 数据集坐标

| 项 | 值 |
|---|---|
| dataset id | `pv115`（Trading Data） |
| category / 塔 | pv（Price Volume，USA/D1 **未点亮**） |
| coverage | 0.9315（集合竞价字段 0.8973，量能字段 1.0） |
| fieldCount | 12（平台可见 11，`sharpe_filter_applied=true` 隐藏 1 个） |
| userCount / alphaCount | 106 / 374（低拥挤，远低于 1 万饱和线） |
| valueScore / pyramidMultiplier | 2 / 1.1 |
| 平台描述 | “full order book depth … net order imbalance indicators for opening, closing…” —— **实测字段与描述不符**：可见字段只有做空量 + Nasdaq 开收盘集合竞价，无量价深度 / 无 OI 指标。本画像以实测字段为准。 |

## 1. 字段清单（11 个可见 / 全 MATRIX / 无 VECTOR）

| 组 | 字段 | 描述 | cov | uC | aC |
|---|---|---|---:|---:|---:|
| 量能 | `pv115_all_tv` | Total_Volume（全市场） | 1.0 | 55 | 140 |
| 量能 | `pv115_all_sv` | Short_Volume（全市场） | 1.0 | 42 | 57 |
| 量能 | `pv115_nasdaq_tv` | Total_Volume（Nasdaq） | 1.0 | 20 | 39 |
| 量能 | `pv115_nasdaq_sv` | Short_Volume（Nasdaq） | 1.0 | 17 | 25 |
| 竞价事件 | `pv115_cc` | 当日是否有 Nasdaq Closing Cross（整数指示） | 0.8973 | 10 | 15 |
| 竞价事件 | `pv115_oc` | 当日是否有 Nasdaq Opening Cross（整数指示） | 0.8973 | 10 | 18 |
| 竞价价格 | `pv115_cc_qdsn` | Closing Cross 成交价（Nasdaq Official Closing Price, USD） | 0.8973 | 7 | 16 |
| 竞价价格 | `pv115_co_qdsn` | Opening Cross 成交价（Nasdaq Official Opening Price, USD） | 0.8973 | 10 | 19 |
| 竞价量 | `pv115_scc_qdsn` | Closing Cross 成交股数 | 0.8973 | 11 | 17 |
| 竞价金额 | `pv115_vcc_qdsn` | Closing Cross 成交金额（USD） | 0.8973 | 30 | 86 |
| 竞价金额 | `pv115_vco_qdsn` | Opening Cross 成交金额（USD） | 0.8973 | 8 | 11 |

### 1.1 结构特征（决定构造方式）

1. **绝对量必须先归一**：`all_tv` / `all_sv` / `scc_qdsn` / `vcc_qdsn` 都是绝对量，裸 rank = 市值/流动性代理（与 pv63 同患）。
   唯一允许的用法是**比值**（分子分母同量纲）或**自身时序归一**（`ts_zscore` / `ts_rank`）。
2. **做空量是「日频做空成交占比」不是空头持仓**：`all_sv/all_tv` 混入做市商对冲（Boehmer–Jones–Zhang 2008
   强调需用标记做空单区分信息交易者），预计信噪比低于双周 short interest；先按弱先验设计。
3. **竞价字段只在约 89.7% 的股票日存在**：缺失不是 0，`cc=0` 表示「未发生」、NaN 表示「无数据」。
   构造竞价占比时必须 `ts_backfill(...,252)` 并避免把「无竞价」当「零参与」——用 `cc>0` 条件门控或 `trade_when`。
4. **开收盘价可构造隔夜收益**：`co_qdsn` 当日开盘竞价价 vs 上一日 `cc_qdsn` 收盘竞价价。
   注意拆股/复权风险：优先用**比值再 winsorize**，或直接用平台 `pv1` 的 return 字段——但 **ATOM 不允许跨数据集**
   ⇒ 只能用本集价格比，且必须限制在 `cc>0 & oc>0` 的样本。
5. **无 VECTOR**：不存在 `vec_*` 聚合问题；形状多样性靠时序算子（z/rank/delta）与分组轴提供。
6. **aC 极低（11–140）**：塔未点亮且几乎无人挖，符合「未点亮塔 × 低 alphaCount」白名单筛选原则。

## 2. 机制假设（经济含义优先；每条标明预期符号与文献）

| # | 机制 | 构造（核心字段） | 预期 | 文献 / 依据 |
|---|---|---|---|---|
| H1 | **做空成交压力** | `all_sv / all_tv`（正向做空占比） | 负 | Boehmer, Jones, Zhang (2008) 做空者知情；Asquith, Pathak, Ritter (2005) 空头持仓预测负收益 |
| H2 | **Nasdaq 局部做空异常** | `nasdaq_sv/nasdaq_tv − all_sv/all_tv` | 负 | 场内做空偏离（venue-specific short pressure），与 H1 双口径对照 |
| H3 | **做空压力时序异常** | `ts_zscore(all_sv/all_tv, 66)` | 负 | 短期做空激增 = 知情交易者入场（相对自身基线，去掉股票固定差异） |
| H4 | **收盘竞价参与度** | `vcc_qdsn / (all_tv * cc_qdsn)`（竞价金额占全日成交额） | 正/负待测 | Bogousslavsky (2021) 收盘竞价不平衡含信息；机构 MOC 需求常延续 |
| H5 | **收盘竞价参与度时序异常** | `ts_zscore(H4, 66)` | 正/负待测 | 参与度突变 = 指数调整 / 机构调仓，常伴短期动量或反转 |
| H6 | **隔夜收益** | `co_qdsn / ts_delay(cc_qdsn, 1) − 1` | 正 | Berkman et al. (2012)、Lou–Polk–Skouras (2019) 隔夜收益溢价 |
| H7 | **开盘竞价占比** | `vco_qdsn / (all_tv * co_qdsn)` | 正/负待测 | 开盘竞价信息含量低于收盘（Barclay–Hendershott 2003） |
| H8 | **做空 × 竞价条件门控** | `trade_when(H4 上穿自身 80 分位, −H1, -1)` | 负 | 只在机构大额 MOC 日放大做空信号（事件条件化） |

**已排除**：`cc`/`oc` 指示符单独当信号（0/1 事件，无截面区分力）；绝对成交金额/股数裸用（size 代理）；
`vcc_qdsn/scc_qdsn`（≈ 价格，恒等式，无信息）；跨数据集拼接（ATOM 违规）。

## 3. 适用模板（不是公式，按机制选壳）

| 模板 | 用途 | 壳 |
|---|---|---|
| T1 通用分位壳（主壳） | 所有 H1–H7 首选 | `quantile(group_rank(hump(ts_backfill(winsorize(<SIG>, std=4), 252), hump=0.01), industry))` |
| T2 自归一壳 | 绝对量/占比的时序异常（H3/H5） | `quantile(group_rank(ts_zscore(<RATIO>, 66), industry))` |
| T3 事件门控壳 | H8 | `trade_when(<COND>, <SIG>, -1)` 外层再套 T1 |
| T4 双口径对照 | H1 vs H2、H4 vs H7 | 同壳同设置，仅换字段，差异即口径效应 |
| T5 反号对 | 每条主候选 | `-1 *` 变体（方向未知者必须成对发） |

**窗口纪律**：只用标准窗 1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260；做空量与竞价参与度先短窗（5/22/66），
隔夜收益只看 1。参数一次一变量。

## 4. 预注册回测（批次 0，**修订：只投集合竞价轴**，2026-10-20 发批）

8 条探针（EQUITY / USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / 其余同 pv63）。
按 §7.1 裁定：H1–H3 已被 `USA-SHORTINTEREST29-RANK-WEAK` 证伪 ⇒ 只留 2 条对照，其余 6 条全给 H4–H8。

| # | 机制 | 表达式信号部分 | 角色 |
|---|---|---|---|
| Q1 | H1 | `divide(pv115_all_sv, pv115_all_tv)` | 对照（已知弱族） |
| Q2 | H3 | `ts_zscore(divide(pv115_all_sv, pv115_all_tv), 66)` | 对照（测时序归一是否救得回） |
| Q3 | H4 | `divide(pv115_vcc_qdsn, multiply(pv115_all_tv, pv115_cc_qdsn))` | 收盘竞价**金额占比** |
| Q4 | H4 反号 | `multiply(-1, divide(pv115_vcc_qdsn, multiply(pv115_all_tv, pv115_cc_qdsn)))` | 方向成对 |
| Q5 | H5 | `ts_zscore(divide(pv115_vcc_qdsn, multiply(pv115_all_tv, pv115_cc_qdsn)), 66)` | 收盘竞价占比的异常 |
| Q6 | H6 | `subtract(divide(pv115_co_qdsn, ts_delay(pv115_cc_qdsn, 1)), 1)` | 隔夜收益（同日非同源价） |
| Q7 | H7 | `divide(pv115_vco_qdsn, multiply(pv115_all_tv, pv115_co_qdsn))` | 开盘竞价金额占比 |
| Q8 | H8 | `divide(pv115_scc_qdsn, pv115_all_tv)` | 收盘竞价**股数占比**（无价格口径） |

**判据（先归因再扩批）**：
1. 任一 RA 全闸 ⇒ 立即 `check_correlation(refresh=True)`（prod 墙第一优先）；**提交必须用户明确确认**。
2. Q1/Q2 仍全弱（|S|<0.8）⇒ 做空量族在本集复证死，**本集只保留竞价轴，不再给做空量任何探针**。
3. Q3 与 Q8 差 <0.1 ⇒ 金额口径与股数口径等价，后续只留 Q8（无价格、无拆股风险）。
4. Q4 与 Q3 严格镜像（和 = 0）⇒ 方向由截面决定，按强的一侧继续，**不取绝对值再造**。
5. Q3/Q5 同弱且 Q6/Q7 也弱 ⇒ 竞价轴无截面 alpha ⇒ **pv115 判弱封存**，不再补批。
6. Q5 显著强于 Q3 ⇒ 参与度「异常」而非「水平」有信息，批 2 只沿 `ts_zscore` 深挖（22/66/252 三窗）。
7. Q6 强但 TO <1% ⇒ 隔夜收益太慢，登记为组合腿，不作单腿交付；Q6 弱 ⇒ 优先排查拆股（Q6 本质是原始价比值）。
8. 全 |S| < 0.8 ⇒ 判弱封存（同 pv63 止损口径）。
9. `cc>0` 缺失不补 0：拍卖字段 cov 0.8973，`ts_backfill(...,252)` 会前向填充；
   **若 Q3/Q5/Q7/Q8 的 longCount/shortCount 明显少于 3000** ⇒ 说明退化成「有竞价的 Nasdaq 股」代理，按风险 §6.2 处置。
10. risk-neut < 0.3 成片 ⇒ size/流动性代理，判死。

## 5. 回测结果及指标

### 5.1 批 0（multisim `3s1zeRcXD4gkcxh10eXzCFsv`，8/8 COMPLETE，2026-10-20 收）

设置：EQUITY / USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / VERIFY / nan ON / maxTrade OFF。

| # | alpha | 机制 | S | F | 2Y | SUB（limit） | TO | returns | longCount | risk-neut | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1 | `QPY9akRp` | H1 做空量占比（对照） | −0.04 | 0.00 | 0.18 | 0.34 PASS | 0.91% | −0.08% | 1536 | −0.13 | 4 |
| Q2 | `xA1dx8Lq` | H3 z66(做空量占比) | −0.36 | −0.09 | −0.81 | −0.06 | 0.80% | −0.85% | 1535 | −0.29 | 4 |
| Q3 | `88vez907` | H4 收盘竞价金额占比 | 0.06 | 0.01 | −0.17 | −0.07（0.03） | 1.52% | 0.22% | 1441 | 0.27 | 4 |
| Q4 | `58jkw0mM` | H4 反向 | 0.03 | 0.00 | −0.37 | 0.24 PASS | 1.33% | 0.10% | 1460 | −0.26 | 3 |
| Q5 | `kqJZ3rwg` | H5 z66(收盘竞价占比) | 0.00 | 0.00 | −0.46 | 0.45 PASS | 1.22% | 0.01% | 1389 | −0.37 | 3 |
| Q6 | `78onwb52` | H6 隔夜收益 | −0.23 | −0.07 | −0.93 | 0.15 PASS | 1.28% | −1.01% | 1370 | 0.03 | 3 |
| Q7 | `LL5dpaQL` | H7 开盘竞价金额占比 | −0.02 | 0.00 | 0.24 | −0.22（−0.01） | 1.43% | −0.06% | 1498 | 0.35 | 4 |
| Q8 | `88vez9w7` | H8 收盘竞价股数占比 | −0.07 | −0.01 | −0.30 | −0.10（−0.03） | 1.32% | −0.24% | 1492 | −0.18 | 4 |

> **TO 全部健康（0.80–1.52%，无一踩 LOW_TURNOVER）** —— 与 pv103 相反，本集不是慢变量问题。

### 5.2 归因

1. **做空量对照双弱**：Q1（水平）S=−0.04，Q2（z66）−0.36 ⇒ 复证 `USA-SHORTINTEREST29-RANK-WEAK`
   （日频做空成交占比在 USA/D1 无截面 alpha，68 条已测）；`ts_zscore` 只把幅度从 0.04 抬到 0.36，
   方向还翻负，**时序归一没有救回**。
2. **收盘竞价参与率严格镜像无方向**：Q3=0.06 vs Q4=0.03（|差| 0.03）⇒ 参与度高低不预测收益，纯噪声；
   且 Q3 的 SUB fail（−0.07），说明小盘段同向更差。
3. **「参与度异常」比「水平」更差**：Q5=0.00（2Y −0.46）⇒ 预注册的「Q5≫Q3 则沿 zscore 深挖」不成立，
   该分支关闭。
4. **隔夜收益不存在**：Q6=−0.23（2Y −0.93、DD 28.9%），TO 1.28% 健康 ⇒ 不是太慢，是**方向/口径**问题。
   Bogousslavsky/Lou-Polk-Skouras 的隔夜溢价在「Nasdaq 官方开/收盘竞价价」口径上不可复现。
5. **开盘竞价同为噪声**：Q7=−0.02、Q8=−0.07 ⇒ 拍卖族全部 |S|<0.1，整轴无信息。
6. **样本确认为「有竞价的 Nasdaq 股」代理**（预注册判据 9）：拍卖类 longCount 1370–1498，明显少于 3000；
   但这不是弱的原因——cov 0.8973 的样本内依然应当有截面差异，实测无差异 ⇒ **信号为零，不是覆盖问题**。
7. **risk-neut 与 S 错位**：Q3/Q5/Q7 的 rns 0.27/−0.37/0.35，而 S≈0 ⇒ 风险中性化后剩下的全是噪声，
   进一步排除「被风格掩盖的真信号」。

### 5.3 结论：判弱封存

命中预注册判据 5/8：**Q3/Q5/Q6/Q7 同弱**（全部 |S|<0.3，且方向镜像）⇒
**`pv115` 判弱封存，登记 `USA-PV115-AUCTION-WEAK`，不再补批**（1 批 / 8 条 / 覆盖做空量 + 竞价 5 机制）。

- 不再发「H4 水平 vs H8 股数」「Q5 三窗」「Q6 拆股修正」等变体：本批的失败是**机制不在本数据集**，
  不是构造/窗口/覆盖问题（TO 健康、样本已核对、方向成对测过）。
- ⚠ 论坛取证闸未过 ⇒ **未调用 `seal_dead_end`**（需 `forum_recon` 的 `no_result` 记录，`force_seal` 需人工确认）。
  在补齐取证前，本文档的「判弱封存」是**项目内纪律约束**：不得重发 pv115 的同类构造。
- PV 塔状态：pv63（判弱）+ pv115（判弱）+ pv103（批 2 在飞）⇒ pv103 是 PV 塔最后一条未封的主线。

## 6. 风险

1. **做空量是「成交」不是「持仓」**：日频做空成交占比的噪声远大于双周 short interest；可能全族 S < 1.0。
2. **竞价字段覆盖 0.8973 且非随机缺失**（Nasdaq 上市股票更完整）⇒ 信号可能变成「交易所归属」代理。
   缓解：分组轴用 industry（不用 exchange），并用 `cc>0` 门控。
3. **隔夜收益存在拆股/复权噪声**：`cc_qdsn`/`co_qdsn` 是原始价，未复权比值会在拆股日爆点。
   缓解：`winsorize(std=4)` + 只用 `cc>0 & oc>0` 样本 + 必要时改 `ts_rank` 口径。
4. **ATOM 合规**：所有非豁免字段来自 pv115；分组轴 industry 属豁免。
5. 与既有判死族的关系：本集与 `order_flow_imb`/`order_book_imbalance` **不同族**（做空量 + 集合竞价 vs 订单流失衡），
   但同属 PV 微观结构 ⇒ 两者的 prod 墙先验（0.76–0.81）仍是第一风险，IS 一过闸就立刻查 prod。

## 7. 文献与论坛证据 / 本地判死先验

### 7.1 ⚠ 本地判死先验直接覆盖 H1–H3（2026-10-20 `get_dead_ends` 实测）

`USA-SHORTINTEREST29-RANK-WEAK`（dead_end，2026-09-30）：

- family = `short_sale_volume`，**分场所做空卖量**（与 pv115 的 `all_sv/nasdaq_sv` 同性质）；
- `best_abs_sharpe = 0.93`，68 条回测；
- 已测 **强度 / 动量 / 均单规模 / 场所集中 / 平方量离散** ×
  `group_rank` / `rank` / `ts_delta` / `ts_zscore` / `ts_mean` / `divide` / `subtract`；
- 结论：**“但仍无信号”**。

⇒ 本集 H1 / H2 / H3 属于**已被同一机制、同一算子网格证伪的族**，不得作为主线复活。
若仍要投本集，**只投集合竞价轴（H4–H8）**，做空量仅作对照（≤2 条），且必须先解释
「为什么 pv115 的日频全市场/纳斯达克口径会不同于 shortinterest29」——目前没有这个理由。

### 7.2 文献（发批前仍应用 `search_forum_posts` 补一次 closing auction / overnight 检索）

1. **Boehmer, Jones & Zhang (2008)**, "Which Shorts Are Informed?" —— 只有**标记做空单**含信息，
   做市商对冲性做空是噪声；日频 aggregate short volume 混入后者 ⇒ 与 7.1 的弱结论一致。
2. **Bogousslavsky (2021)**, "The Cross-Section of Intraday and Overnight Returns" ——
   收盘竞价与隔夜收益有独立截面结构；这是 H4–H6 的主要依据。
3. **Lou, Polk & Skouras (2019)**, "A Tug of War: Overnight versus Intraday Expected Returns" ——
   隔夜收益承载动量/情绪，日内收益承载反转；H6 的依据。
4. **Barclay & Hendershott (2003)**, "Price Discovery and Trading After Hours" ——
   收盘竞价的信息含量高于开盘；H4 强于 H7 的先验。

### 7.3 结论（优先级裁定）

- **H1–H3（做空量）降为对照**：有同族 USA 判死证据，不占探针主位。
- **H4–H8（集合竞价 / 隔夜）是本集唯一未证伪的机制面**，若开挖，8 探针中 ≥6 条应给这一面。
- 若集合竞价轴也全 |S|<0.8 ⇒ 整集判弱封存，不再补批。
