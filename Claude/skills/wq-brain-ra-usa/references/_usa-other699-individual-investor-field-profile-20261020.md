# other699 · Individual Investor Transactions（TipRanks 散户交易级）字段画像与战役记录

> 命名：单集档案 `_usa-<dataset>-field-profile-<asOf>.md`
> **as_of**：2026-10-20 ｜ 战役：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08
> 塔位：**未点亮**（USA/D1 OTHER，`get_datasets` 实测 0 回测、pyramids multiplier 1.4）
> ATOM 合规：本档全部非豁免字段均来自 `other699`；`industry` 属六个豁免分组字段之一。

---

## 0. 坐标与一句话结论

| 项 | 值 |
|---|---|
| 全名 | Individual Investor Transactions（TipRanks 个体投资者交易记录） |
| 类别 | Other（`pyramids.effective = 1`，`USA/D1/OTHER` ×1.4） |
| 字段 | **16 个，全 VECTOR**（`vec_*` 必须先聚合再进标量算子） |
| 覆盖率 | 0.9574–1.0（具名主字段均在 0.96 以上） |
| 字段 alphaCount | 2–34（**极低**，属冷门集） |
| 更新频率 | **日频事件级**：只有发生交易的 (股票, 投资者) 才产生一行 |
| 已有平台 α | 0（本档开批前实测） |
| 已用批次 | 批 1（8 条，`2RAAaq6cA4i49Qou528l5Te`）＋批 2（8 条，`3mAv4b3ZX5dDafoNUeJWHfd`） |

**一句话**：这是本战役里唯一的**散户逐笔交易级**数据（不是持仓快照、不是情绪分数），
机制对应 Kaniel-Saar-Titman 的「个体投资者买卖不平衡」，但它是**事件稀疏**的 VECTOR 字段，
裸聚合会在非事件日产生 NaN，导致截面权重塌缩到少数股票 —— 批 1 的 8 条全部踩同一个
`CONCENTRATED_WEIGHT = 0.499998`，这不是信号结论，是构造缺陷。

---

## 1. 字段画像（16 字段 / 七族）

### 1.1 字段清单（`get_datafields` 2026-10-20 实测）

| 字段 | cov | aC | 类型 | 语义（按字面与供应商文档） | 族 |
|---|---:|---:|---|---|---|
| `oth699_sharestraded` | 0.9612 | **26** | VECTOR | 该投资者本次成交股数，**带符号：+买入 / −卖出**，已做拆股调整 | 方向流 |
| `oth699_newnumofshares` | 0.9574 | 8 | VECTOR | 交易后该投资者持有股数 | 仓位规模 |
| `oth699_prevnumofshares` | 0.9612 | 10 | VECTOR | 交易前该投资者持有股数 | 仓位规模 |
| `oth699_priortransactionnumber` | 0.9612 | 12 | VECTOR | 该投资者在此股票上的**历史交易次数** | 交易者经验 |
| `oth699_priordistincttradingdays` | 0.9612 | 22 | VECTOR | 该投资者在此股票上的历史交易天数 | 交易者经验 |
| `oth699_action_14` | 1.0 | 17 | VECTOR | **事件类型**（Watchlist-Add / Opened Position …），分类值 | 事件类型 |
| `oth699_usertype_24` | 1.0 | 14 | VECTOR | **用户档位**（Basic / Premium / Ultimate），分类值 | 用户类型 |
| `oth699_executiontimestamp` | 0.9612 | 34 | VECTOR | 成交时间戳（**全字段最高 aC**） | 时间 |
| `oth699_country_15` | 1.0 | 19 | VECTOR | 投资者所属国别，分类值 | 国别 |
| `oth699_aggsplitfactor` | 0.9612 | 9 | VECTOR | 拆股因子（辅助量，非信号） | 复权 |
| `_13` / `_17` / `_18` / `_20` / `_21` / `_23` | 1.0 | 2–9 | VECTOR | 未具名变体（供应商提供的 rank / 编码派生列） | 派生 |

> 六个别名列（`_13` 等）**刻意未进批 1/批 2**：语义未知且更像同一字段的 rank 变体，
> 直接使用等于凭空引入一个未定义口径。若后续需要，先做 `vec_avg` 与主字段的秩相关，
> 确认它为独立信息再投入。

### 1.2 八问要点

**① 是什么** 散户（TipRanks 用户）在个股上的**逐笔成交**记录，按 (股票, 投资者, 事件) 展开成 VECTOR。
**② 类型** 全 **VECTOR**：必须先 `vec_sum` / `vec_avg` / `vec_count` / `vec_stddev` 聚合；
`vec_abs` 平台不存在（`research-data/operators_platform_20260904.json` 实测）。
**③ 覆盖** 0.9574–1.0；但**覆盖 ≠ 每日有值** —— 事件稀疏，非事件日该股票无行（见 §6 风险 1）。
**④ 更新** 日频，成交即更新；`executiontimestamp` 有 aC 34 说明时间信息本身被用过。
**⑤ 分布** `sharestraded` 带符号、重尾（单笔可为整仓）；`*numofshares` 非负、右偏；
`action_14` / `usertype_24` / `country_15` **是分类量**，`vec_avg` 对它们无经济意义（只能 `vec_count` 或分组）。
**⑥ 拥挤** aC 2–34，全场最低一档；无平台 α ⇒ 纯蓝海。
**⑦ 信号** `sharestraded`（方向流）是主字段；`priortransactionnumber`（经验）在本批意外最稳。
**⑧ 用** 见 §2 模板与 §5 读数。

---

## 2. 适用模板（M01–M12，机制不限于 8 个）

> 壳层统一 `quantile(group_rank(<SIG>, industry))`；`industry` 是豁免分组字段，满足 ATOM 单数据集约束。
> **事件稀疏字段必须先 `ts_backfill(…, 252)` 再 `group_rank`** —— 这是批 1 的核心教训（§5.1）。

| # | 机制 | 字段与构造 | 经济先验 | 状态 |
|---|---|---|---|---|
| **M01** | 散户净买入动量（短窗） | `ts_mean(vec_sum(sharestraded), 5)` **正向** | KST 2008：散户净买入在数周内正向预测收益 | 批 1 已测 |
| **M02** | 净买入反转（长窗） | 同字段 22 日，**反向** | Da-Shive 式短期价格压力后回吐 | 批 1 已测（22d 反向） |
| **M03** | 交易广度 | `ts_mean(vec_count(sharestraded), 5)` | 参与人数 = 关注度，广度比金额更抗单笔巨鲸 | 批 1 已测 |
| **M04** | 平均票面 | `ts_mean(vec_avg(sharestraded), 5)` | 单笔规模 = 信念强度（大单散户更 informed） | 批 1 已测 |
| **M05** | 换手强度 | `vec_sum(sharestraded) / (vec_sum(newnumofshares) + 1)` | 交易额相对仓位 = 调仓激烈度 | 批 1 已测（2Y 1.09） |
| **M06** | **交易者经验** | `ts_mean(vec_avg(priortransactionnumber), 5)` | Seru-Shumway-Stoffman 2010：越有经验越不犯错 | 批 1 **最强 S 0.72** |
| **M07** | 交易者黏性 | `vec_avg(priordistincttradingdays)` | 长期反复交易同一票 = 本地信息优势 | 批 2 备选 |
| **M08** | 分歧度 | `ts_mean(vec_stddev(sharestraded), 5)` **反向** | 散户意见分散 = 无共识 | 批 1 已测 |
| **M09** | **净增持**（仓位口径） | `vec_sum(newnumofshares) − vec_sum(prevnumofshares)` | 比 `sharestraded` 更干净：剔除「卖了又买」的日内噪声 | 批 2 已测 |
| **M10** | 仓位增速 | M09 / `vec_sum(prevnumofshares)` | 论文标准口径：变化率而非水平（Institutions 战役 §10 同款教训） | 批 2 已测 |
| **M11** | 事件类型门控 | `action_14` 命中「Opened Position」子集计数 | 只有真正建仓才是信息事件 | 待测（需确认分类值可取子集） |
| **M12** | 用户档位门控 | `usertype_24` 取 Premium/Ultimate 子集 | 付费用户更 informed | 待测（同 M11，分类量约束） |

---

## 3. 批 1 预注册（写死，8 条）

**设置**：EQUITY / USA / TOP3000 / D1 / decay 5 / SUBINDUSTRY / trunc 0.08 /
pasteurization ON / unitHandling VERIFY / nanHandling ON / maxTrade OFF / FASTEXPR；
区间 2014-01-01 → 2023-12-31。

| # | 表达式 |
|---|---|
| P1 | `-quantile(group_rank(winsorize(ts_mean(vec_sum(oth699_sharestraded), 5), std=4), industry))` |
| P2 | `quantile(group_rank(winsorize(ts_mean(vec_sum(oth699_sharestraded), 5), std=4), industry))` |
| P3 | `-quantile(group_rank(winsorize(ts_mean(vec_count(oth699_sharestraded), 5), std=4), industry))` |
| P4 | `quantile(group_rank(winsorize(ts_mean(vec_avg(oth699_sharestraded), 5), std=4), industry))` |
| P5 | `-quantile(group_rank(winsorize(ts_mean(vec_sum(oth699_sharestraded) / (vec_sum(oth699_newnumofshares) + 1), 5), std=4), industry))` |
| P6 | `quantile(group_rank(winsorize(ts_mean(vec_avg(oth699_priortransactionnumber), 5), std=4), industry))` |
| P7 | `-quantile(group_rank(winsorize(ts_mean(vec_stddev(oth699_sharestraded), 5), std=4), industry))` |
| P8 | `-quantile(group_rank(winsorize(ts_mean(vec_sum(oth699_sharestraded), 22), std=4), industry))` |

**预注册判据**（收割前写死）：

- 任一 `S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB PASS / TO 1%–70%` 且 `fail=0` ⇒ 立即 `check_correlation(refresh=True)`。
- `P1` 与 `P2` 必须严格镜像；同号或 |S| 差 >0.2 ⇒ 只有单一方向成分。
- **全批 |S| < 0.8 且 TO 健康 ⇒ 本集判弱**，写明归因后再换集。
- **全批出现同一个 `CONCENTRATED_WEIGHT` 数值 ⇒ 归因为构造/数据稀疏，不是信号结论**，
  只允许做一个「单一变量修复」（补 `ts_backfill`）的批 2；若批 2 仍全弱则封存。
- M06（经验族）最强但 `risk_neut < 0.3` ⇒ 按风格代理处理，不做同族磨参数。

---

## 4. 外部证据（论坛 + 文献）

**论坛取证**（`search_forum_posts` 2026-10-20，`search_query="retail order flow"` / `"TipRanks individual investor"`）：

- **无 TipRanks / other699 专帖**（该集在中文论坛零覆盖，属纯蓝海）。
- 命中 KOR 帖 **JX84394「卖/买比一周峰值反转」**（S 2.43），其参考文献指向
  **Kaniel, Saar, Titman (2008)** —— 与本集 M01 同一机制，但那是**交易所会员/账户级汇总**，
  不是逐笔；本集粒度更细，**不能直接套用其窗口与符号**（该帖用 1 周峰值 + 反转）。
- 另命中一篇论文合集帖，收录 individual investor / attention 方向文献，作为机制旁证。

**文献**（机制层，四篇独立支持 + 一篇口径）：

1. **Kaniel, Saar, Titman (2008, JF 63(1)) "Individual Investor Trading and Stock Returns"**：
   个体投资者**买卖不平衡**在 1–4 周尺度上**正向**预测收益（信息含量在高关注度股票更强）。
   ⇒ 支撑 M01（短窗正向）；也说明**方向先验应为正**，反向版（P1/P8）是用来探 regime 的对偶。
2. **Barber & Odean (2001/2008)**：散户买 attention-grabbing 股票、且存在处置效应 ⇒ 短窗买入是关注度冲击，
   之后可能回吐 ⇒ 支撑 M02（长窗反转）。
3. **Boehmer, Jones, Zhang & Zhang (2021, JF) "Tracking Retail Investor Activity"**：
   用子笔订单规则识别的散户**订单不平衡**正向预测收益，效应在 2010 后样本更强。
   ⇒ 支撑 M01，并预警：**近年更强**意味着全期 S 可能被前段拖低（本批 P1 的 2Y +0.76 vs 全期 −0.51 正是此形态）。
4. **Seru, Shumway & Stoffman (2010, JF) "Learning by Trading"**：交易经验提升个体投资者绩效。
   ⇒ 支撑 M06（`priortransactionnumber` = 经验的直接代理），这是本批唯一非方向流的独立机制。
5. **Institutions 战役 §10 口径教训（本仓已有实证）**：同一数据集换「测量口径」（水平 / 变化 / 变化率）
   对 SUB 与 S 的影响远大于换算子 ⇒ 本批 M09/M10 直接采用**仓位变化率**口径（批 2）。

---

## 5. 回测结果及指标

### 5.1 批 1（multisim `2RAAaq6cA4i49Qou528l5Te`，8/8 COMPLETE）

| # | alpha | 机制 | S | F | 2Y | SUB | TO | returns | DD | risk-neut | fail |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | `zqrRmYLX` | 5d 流量（反向） | −0.51 | −0.19 | **0.76** | −0.20 | 27.1% | −3.93% | 40.1% | −0.22 | 4 |
| P2 | `Vkd3P6R0` | 5d 流量（正向） | 0.51 | 0.19 | −0.76 | 0.20 **FAIL** | 27.1% | 3.93% | 17.7% | 0.22 | 5 |
| P3 | `leM3l8Nn` | 交易广度（反向） | −0.66 | −0.39 | 0.59 | −0.53 | 16.2% | −5.63% | 52.8% | −0.31 | 5 |
| P4 | `akVEnL8v` | 平均票面（正向） | 0.56 | 0.22 | −0.67 | **0.26 PASS** | 27.8% | 4.24% | 17.7% | 0.25 | 4 |
| P5 | `xA1dkYon` | 换手强度（反向） | −0.57 | −0.22 | **1.09** | −0.34 | 28.9% | −4.21% | 40.8% | −0.23 | 5 |
| P6 | `O0JxZrjR` | **交易者经验** | **0.72** | **0.35** | 0.38 | **0.51 PASS** | 23.8% | **5.50%** | 17.7% | 0.21 | 4 |
| P7 | `0mjMER2q` | 分歧度（反向） | −0.69 | −0.36 | 0.32 | −0.49 | 20.0% | −5.45% | 47.9% | −0.29 | 5 |
| P8 | `GrgeLd53` | 22d 流量（反向） | −0.18 | −0.06 | 0.70 | 0.22 | 12.3% | −1.45% | 32.4% | −0.45 | 4 |

> **全部 8 条的 `CONCENTRATED_WEIGHT` 读数是同一个值 `0.499998`**（对比日期 2016-09-22 / 2016-10-13）。
> 这一项**不是**各构造分别产生的，而是同一个构造缺陷在不同信号下的同一投影。

#### 归因（8 条）

1. **CW 同一数值 = 构造缺陷，不是信号结论**。事件级 VECTOR 在非事件日返回 NaN，
   `ts_mean` 虽有 5 日窗口但不足以覆盖稀疏事件 ⇒ 截面在事件日塌缩到少数股票，
   `truncation=0.08` 也无法把单只权重压回。判据可复用：**整批 CW 数值逐位相同 ⇒ 先修数据稀疏，不看 S**。
2. **P1 / P2 严格镜像**（S ±0.51、2Y ∓0.76，差 0），说明方向流只有**单一成分**；
   且**全期为负、近两年为正** ⇒ 与 Boehmer et al. 2021「2010 后散户订单流更有效」一致，
   但方向在样本内发生**翻转**，属 regime 依赖（同 pv63 / chart_return_model 的 yearly 形态）。
3. **P3 与 P7 同向**（−0.66 / −0.69，2Y 均为正）⇒ 「广度 + 分歧」是两个同源测度（都吃散户参与强度），
   不构成两个独立机制，后续只保留一个。
4. **P4 ≈ P2**（0.56 vs 0.51）⇒ `vec_avg` 与 `vec_sum` 差 0.05，说明**单笔平均规模不携带方向信息**，
   方向全在 `sharestraded` 的符号里。
5. **P5 是唯一 2Y > 1.0 的轴**（1.09）但全期 −0.57 ⇒ 换手强度也是近两年才有效的 regime 因子。
6. **P6（交易者经验）是唯一非方向流机制**：2Y 0.38 但全期 0.72 / SUB 0.51 PASS / investability 0.93，
   说明信号在**可投资子集上更强**（0.93 > 0.72），不是小盘垃圾；但 `risk_neut 0.21` ⇒ 仍有风格成分。
7. **risk-neut 全 ≤0.25** ⇒ 八个构造没有一个能剥离 size/liquidity，这一集本质上是**参与度代理**。

#### 决策（预注册判据 vs 偏离留痕）

- 预注册：**全批 |S| < 0.8 且 TO 健康 ⇒ 判弱**。读数满足该条（max |S| 0.72、TO 12–29%）。
- **偏离**：整批 CW 同一个 `0.499998` 证明这 8 条**不是对信号的干净测试**（组合被单票扭曲），
  因此按「先归因再推进」的纪律，**只做一个单一变量修复批**（补 `ts_backfill(…,252)`，
  与 other580 已验证壳一致），不换数据集、不换设置。若批 2 仍全弱 ⇒ 封存。

### 5.2 批 2（multisim `3mAv4b3ZX5dDafoNUeJWHfd`，8 条）

**唯一改动 = 在 `winsorize` 之后加 `ts_backfill(…, 252)`**（其余设置逐项不动）。
另外把 M09/M10（仓位变化 / 变化率）纳入，检验「换测量口径」是否比换算子有效（Institutions §10 的教训）。

| # | alpha | 机制 | 表达式核心 | S | F | 2Y | SUB | TO | rns | 失败数 |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| B1 | `KPmE9Z2z` | 经验 5d + backfill | `vec_avg(priortransactionnumber)` 5d | 0.59 | 0.29 | **1.38** | 0.25 FAIL | 19.9% | 0.59 | 5 |
| B2 | `zqrRmeEo` | 经验 22d + backfill | 同上 22d | 0.54 | 0.33 | **1.47** | 0.16 FAIL | 9.3% | 0.59 | 5 |
| B3 | `QPY9V6AK` | 流量 5d + backfill | `vec_sum(sharestraded)` 5d | 0.38 | 0.13 | −0.58 | −0.02 | 25.3% | 0.61 | 5 |
| B4 | `rKdPl8wa` | 换手强度 + backfill | 比率 5d（**方向反转**） | −0.38 | −0.13 | 1.10 | −0.08 | 24.6% | −0.58 | 4 |
| B5 | `MP0LQVN9` | 广度 + backfill | `vec_count` 5d | 0.57 | 0.35 | −0.26 | **0.31 PASS** | 13.7% | 0.67 | 4 |
| B6 | `GrgeL95o` | 净增持（仓位口径） | `vec_sum(new) − vec_sum(prev)` 5d | 0.38 | 0.13 | −0.58 | −0.02 | 25.3% | 0.61 | 5 |
| B7 | `d5KR0vrY` | 仓位增速 | B6 / `vec_sum(prev)` | **0.67** | 0.27 | −0.81 | 0.38 | 34.1% | **0.77** | 4 |
| B8 | `6XAe9N67` | 分歧度（正向） | `vec_stddev` 5d | −0.49 | −0.26 | 0.41 | −0.15 | 14.5% | −0.62 | 4 |

**批 2 的读数**：

1. **CW 仍是同一个 `0.5`，但日期从批 1 的 2016-09-22 / 10-13 移到 2016-10-28**。
   `ts_backfill(…,252)` 只能填 252 个交易日内的缺口；最差日改变而数值不变（0.5 = 当日仅两只票有权重），
   说明这是**数据集级、跨年度的整段缺失**，不是单日 NaN，也不是表达式构造问题。
   ⇒ 这一集在任何壳下都会挂 `CONCENTRATED_WEIGHT`，除非再加 `trade_when` 只在自己有数据的日子交易（成本高、且 TO 会掉到 1% 以下）。
2. **backfill 确实改善了「近两年」而不是「全期」**：B1/B2 的 2Y 从批 1 的 0.38 升到 1.38/1.47，
   investability 1.53/1.39（高于全期 S），risk-neut 从 0.21 升到 0.59。
   ⇒ 同一信号在**可投资子集 + 近两年**是有效的，全期被 2014–2019 的无效段拖平。
3. **B3 ≡ B6（读数逐位相同）**：`vec_sum(sharestraded)` 与 `vec_sum(new) − vec_sum(prev)` 在这个数据集里是同一个量
   （成交股数 = 持仓变化量），不是两个独立机制。B4/B7 同理（换手强度 ≡ 仓位增速，读数差仅来自分母）。
   ⇒ 16 个构造实际只覆盖 **4 个独立机制**：经验、流量、广度、分歧。
4. **B7 的 risk-neut 0.77 是全组最高**，但仍低于 1.0 且 2Y −0.81 ⇒ 方向在近两年崩塌。

#### 决策：判弱封存（`USA-OTHER699-RETAIL-FLOW-WEAK`）

- 预注册判据「批 2 仍全弱 ⇒ 封存」成立：8 条 max S 0.67、max F 0.35、**无一条 fail ≤ 1**，且 CW 结构性不可修。
- 登记 **salvage**：B1/B2（交易者经验 + 252 backfill）的 **2Y 1.38 / 1.47 + investability 1.53 / 1.39**
  是全批唯一「近端有效且不是小盘垃圾」的证据；将来若做**只覆盖 2022–2023 的近期窗口策略**或与低相关慢腿组合时可回捞，
  但作为**全期 REGULAR 单腿不可交付**（USA 闸看全期 S）。
- 不换设置重发：CW 归因已定位到数据集缺口，换 neutralization / decay 只会改变哪一天成为最差日，不会消除 0.5。
- **可复用判据（写入索引）**：`ts_backfill` 改善 2Y 但 CW 数值不变 ⇒ 缺口长度 > backfill 窗口，**数据集级问题，立即封存**，不再做第三个变量批。

---

## 6. 风险与预判

1. **事件稀疏是最主要风险，且它伪装成「信号弱」**。`sharestraded` cov 0.9612 是**行级覆盖率**，
   不等于「每日每票有值」。批 1 的 CW 同一数值就是证据。今后凡事件级 VECTOR 字段，
   **首条探针必须同时发「裸聚合」与「backfill 聚合」两条对照**，否则整批读数都不可用。
2. **分类量不可 `vec_avg`**：`action_14` / `usertype_24` / `country_15` 是分类编码，
   对它们做 `vec_avg` 得到的「平均类别号」无经济意义。M11 / M12 只能用 `vec_count` + 子集筛选，
   而 FASTEXPR 没有直接的条件向量过滤 ⇒ 需用分组算子或 `trade_when` 间接实现，成本高，列为低优先。
3. **方向在样本内翻转**（P1/P2 全期与 2Y 符号相反）⇒ 任何靠「全期 S」选出来的符号，
   在 OS 期可能反向。本集若出货，必须**同时**看 2Y 与全期，并在 robustness 阶段做逐年诊断。
4. **risk-neut ≤0.25**：这一集很可能整体是「散户参与度 = 流动性/规模」的代理。
   若批 2 的 risk-neut 仍 <0.3，则即便 S 上去也按 `USA-BOARD-GOV-*` 的先例做 prod 实测，
   **不因 IS 过闸而提交**。
5. **ATOM 合规**：M11/M12 若引入 `action_14` 之外的字段做门控，仍须全部来自 `other699`；
   `industry` 分组豁免可用，`sector`/`subindustry` 同理。
6. **`aggsplitfactor` 不是信号**：它只用来理解 `sharestraded` 的拆股调整，
   `vec_avg` 它等于「平均拆股因子」，无截面信息。
7. **`executiontimestamp` 是 aC 最高（34）的字段，但时间戳不能直接当信号** ——
   若要用，只能派生「成交集中在开盘/收盘」的比例（类似 pv103 的拍卖轴，而 pv103 已判弱）
   ⇒ 本集不投入，记录为已知未用维度。

---

## 7. 索引

- 本篇：`references/_usa-other699-individual-investor-field-profile-20261020.md`
- 交付台账：`references/_usa-atom-delivery-log-20261020.md`（other699 行）
- 同型「事件稀疏 / CW 同值」教训对照：`references/_usa-pv63-order-flow-field-profile-20261020.md`（逐笔事件流）、
  `references/_usa-other580-etf-holdings-field-profile-20261020.md`（流量族，被判弱）
- 口径教训（换测量口径 > 换算子）：`references/_usa-institutions-pv-dataset-scan-20261019.md` §10
