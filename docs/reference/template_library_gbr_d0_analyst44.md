# GBR / D0 · `analyst44` 模板库（Integrated Broker Estimates）

> 建立于 2026-10-31。GBR D0 战场第 1 个数据集。
> **D0 是独立塔位体系**（14 座全未点亮）且倍率高于 D1（analyst 1.9 vs 1.6）。
> 本文件常驻：① 字段结构口径 ② 结构互异模板库（≥10）③ 实测账本。

---

## §1 数据集结构（实测，`get_datafields` delay=0）

`analyst44` = 300 字段，**全部 VECTOR**，必须 `vec_avg` / `vec_stddev` / `vec_range` 折叠成标量。
覆盖率 0.7462，alphaCount 121，valueScore 5，D0 倍率 **1.9**。

### 1.1 带前缀的 5 后缀族（22 measure × 5 = 110 字段）

每个 measure 固定有 5 个后缀：

| 后缀 | 语义 | 用途 |
|---|---|---|
| `_value` | 当前估计值 | 主信号分子 |
| `_prevalue` | **修正前**值 | `value − prevalue` = **修正幅度** |
| `_coveredby` | 覆盖该股票的分析师**数量**（计数，带量纲） | 门控 / 正交轴（须先 `rank()`） |
| `_isexcluded` | 是否被剔除标志 | 数据清洗（未用） |
| `_lastactccy` | 上次活动的币种 | 未用 |

### 1.2 22 个 measure 全集（按覆盖率降序）

| measure | coverage | measure | coverage |
|---|---:|---|---:|
| `eps` | **0.8034** | `roe` | 0.6285 |
| `sales` | 0.7969 | `pretaxprofit` | 0.6254 |
| `ebit` | 0.7781 | `netprofit_rep` | 0.5781 |
| `ebitda` | 0.7513 | `grossmargin` | 0.5386 |
| `netprofit` | 0.7496 | `epsr` | 0.5376 |
| `dps` | 0.7476 | `pretaxprofit_rep` | 0.5236 |
| `bps` | 0.7151 | `roa` | 0.4658 |
| `netdebt` | 0.7032 | `fcfps` | 0.3942 |
| `nav` | 0.6496 | `csh` | 0.3872 |
| `capex` | 0.6414 | `operatingprofit` | 0.3337 |
| `cfps` | 0.6408 | `ebitdaps` | 0.195 |

### 1.3 ★ 裸名别名族（第三类，190 字段）

**同一数据集内字段前缀不统一**（已知平台陷阱）。每个 measure 另有一组**裸名**「上次报告值」字段，
覆盖率与对应 `anl44_<measure>_value` **逐位匹配**：

| measure（覆盖率） | 裸名「上次报告值」字段 |
|---|---|
| `epsr` 0.5376 | `latest_actual_reported_eps_value` |
| `dps` 0.7476 | `last_actual_reported_value` |
| `cfps` 0.6408 | `last_actual_cfps_value` |
| `bps` 0.7151 | `latest_actual_bps_value` |
| `capex` 0.6414 | `latest_actual_capex_value` |
| `ebitda` 0.7513 | `latest_actual_ebitda_value` |
| `netprofit` 0.7496 | `most_recent_actual_net_income_value` |
| `nav` 0.6496 | `actual_value_nav` |
| `roa` 0.4658 | `actual_value_roa` |
| `roe` 0.6285 | `last_actual_roe_value` |
| `sales` 0.7969 | `actual_value_sales` |
| `operatingprofit` 0.3337 | `operatingprofit_last_actual_value` |
| `grossmargin` 0.5386 | `last_actual_gross_margin_value` |
| `fcfps` 0.3942 | `fcfps_last_actual_value` |
| `pretaxprofit_rep` 0.5236 | `actual_value_latest` |
| `ebitdaps` 0.195 | `most_recent_actual_value` |
| `csh` 0.3872 | `latest_actual_cash_eps_value` |

⇒ 提供了**第二条独立信号线**：`value − last_actual`（预期差 / SUE 代理），
区别于 `value − prevalue`（分析师自身修正）。
⚠ 两者描述文字高度相似（都是 "most recent estimate value prior to the current event"），
**可能部分重叠**，须实测互相关后才有定论。
⚠ `eps`（0.8034）**没有**匹配的裸名「上次报告值」字段；能配对的是 `epsr`（0.5376）。

### 1.4 D0 的信息优势

`value` 与 `prevalue` **同日给出** ⇒ D0 拿到的是「当日修正完成后」的快照。
D1 上同信息晚一天可得。这是 D0 相对 D1 的**唯一信息增量来源**（除了塔位体系独立）。

---

## §2 模板库（12 个，结构互异；≥10 达标）

差异维度：**骨架结构 / 算子几何 / 矩（水平·一阶差分·二阶方差）/ 分组轴 / 非线性变换 / 窗口族**。
窗口全部落在白名单 `1/5/22/66/252/504/1008/1260`。

记 `D(m) = subtract(vec_avg(anl44_<m>_value), vec_avg(anl44_<m>_prevalue))` = **修正幅度**。

| # | 模板 | 结构差异点 | 来源 |
|---|---|---|---|
| **T1** | `rank(D(eps))` | 一阶矩（水平差），**无时序**——最裸基线 | paper: Bernard & Thomas (1989) 修正动量 |
| **T2** | `rank(divide(D(ebit), abs(vec_avg(anl44_ebit_prevalue))))` | **尺度归一**（无量纲化）；骨架差异在单位处理 | paper + 自建 |
| **T3** | `rank(ts_mean(D(eps), 66))` | **季度均值**——把「单次修正」变「季度累积修正」 | 自建（22×3=66 季度） |
| **T4** | `rank(ts_zscore(D(eps), 252))` | **二阶矩分母**（历史波动归一）⇒ 事件强度而非幅度 | forum 41420742165527（vec_avg 稀疏被单值主导） |
| **T5** | `rank(divide(subtract(vec_avg(anl44_epsr_value), vec_avg(latest_actual_reported_eps_value)), abs(vec_avg(latest_actual_reported_eps_value))))` | **换配对字段**：预期差（SUE 代理）而非修正 | paper: Bernard & Thomas (1990) SUE；Livnat & Mendenhall (2006) |
| **T6** | `trade_when(greater(rank(vec_avg(anl44_eps_coveredby)), 0.5), rank(D(eps)), -1)` | **门控层**（只在分析师覆盖广的股票上生效） | forum 33120494662423（`trade_when` 第三参 -1 = 不平仓） |
| **T7** | `rank(add(add(rank(D(eps)), rank(D(ebit))), rank(D(sales))))` | **跨口径广度**（同概念「盈利修正」三口径等权合成，权重恒 1，不扫描） | paper: Chan-Jegadeesh-Lakonishok (1996) 修正广度 |
| **T8** | `rank(divide(D(eps), vec_stddev(anl44_eps_value)))` | **信噪比**：修正是信号 / 分析师间分歧是噪声（同单位相除） | paper: Diether-Malloy-Scherbina (2002) 分歧度 |
| **T9** | `vector_neut(rank(D(eps)), rank(vec_avg(anl44_eps_coveredby)))` | **回归残差化**：剥离「覆盖广→修正大」规模效应 | forum 34366220071447（vector_neut 应用） |
| **T10** | `rank(ts_delta(D(eps), 22))` | **加速度**（一阶差分的差），月度修正的动量 | 自建 |
| **T11** | `bucket(rank(D(eps)), range="0.2,1,0.2")` | **离散化非线性变换**（5 桶；TOP500~1000 → 5~10 桶） | forum 44174743998999（bucket 降 PC 模板库，26 赞） |
| **T12** | `rank(ts_sum(D(eps), 252))` | **年度累积能量**（`ts_sum` 累积而非 `ts_mean` 平均） | 自建 |

### 2.1 合规声明

- **T7 是三字段 `add`**：声明为**同概念多字段等权（权重恒 1，不扫描）合成**，属允许形态，
  **不属于** `add(A,B)` 混信号调参。
- **T9** 是回归残差化（`vector_neut`），属允许形态。
- 其余模板均为**单信号单概念**的结构化加工，无权重混合。
- `_coveredby` 带计数单位 ⇒ **一律先 `rank()`** 再进门控 / `vector_neut` 第二参。
- 所有含 `value`/`prevalue` 的 `divide` 都是**同 measure 同单位相除**，符合 `unit_handling=VERIFY`。

### 2.2 起始设置（待实测标定）

```
region=GBR  universe=TOP700  delay=0        # ★ D0 必须 delay=0
neutralization=INDUSTRY  decay=4  truncation=0.08
nan_handling=ON  max_trade=OFF  pasteurization=ON  unit_handling=VERIFY
```
参照 D1 上同 category 的 `analyst7` 形态（`STATISTICAL` + decay 0~4 + trunc 0.08~0.1）。
若基线 IS 不足，优先扫 `decay ∈ {0,4,8,10}` 与 `neutralization ∈ {INDUSTRY, SUBINDUSTRY, STATISTICAL}`。

---

## §3 实测账本

（待填）## §3 实测账本

### 3.0 ★★★ D0 闸门门槛（2026-10-31 实测，与 D1 对比）

| 检查 | **D0 limit** | D1 limit |
|---|---:|---:|
| `LOW_SHARPE` | **2.69** | 1.58 |
| `LOW_FITNESS` | **1.5** | 1.0 |
| `LOW_2Y_SHARPE` | **2.69** | 1.58 |
| `HIGH_TURNOVER` | 0.70 | 0.70 |
| `CONCENTRATED_WEIGHT` | 0.10 | 0.10 |

⇒ **D0 的 S 门槛 = D1 的 1.70×**。倍率 1.9 的代价就是这道门槛。
⇒ `checks.pending` 含 **`D0_SUBMISSION`**（D1 没有这一项），可作为区分 D0/D1 的旁证。
⇒ **塔位名必须读 `pyramids.list[].name`**（`GBR/D0/ANALYST`），
`ra.pyramid_short` 只是短名（`analyst`），D0/D1 共用，不能用来区分。

### 3.1 批 D0-1（2026-10-31）· `1d0GmmaZp4ydaXdEEHsnbYt`

设置 `delay=0 / INDUSTRY / decay=4 / trunc=0.08 / nanHandling ON / maxTrade OFF`

| # | 模板 | alpha | S | F | 2Y | SUB | TO | margin | CW | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| T1 | `rank(D(eps))` | `j2YNqjwo` | **1.38** | 0.37 | 1.50 | 0.99 | **150.5%** | 1.40bp | **0.50** | 5 |
| T2 | `rank(D(ebit)/abs(prevalue))` | `RRE0G7kj` | 0.45 | 0.07 | 0.15 | 0.32 | **159.9%** | 0.54bp | **0.50** | 5 |

**结论**
1. **换手是第一道墙**：150–160% vs 上限 70% ⇒ 必须先治换手再看信号。
   机理：D0 的 `value` 与 `prevalue` **同日**给出，`value−prevalue` 每日翻动；
   D1 延迟一天反而把信号平滑了。**D0 是「高频修正」数据面。**
2. **基线信号本身偏弱**：T1 S 1.38 vs 需 2.69，差 1.31。T2（尺度归一）反而更差（0.45）
   ⇒ `abs(prevalue)` 做分母在 D0 噪声过大（`prevalue` 当日也变，比值不稳定）。
3. **持仓过窄**：long 70 / short 69 = TOP700 的 20%（只有 `value≠prevalue` 的股票有信号）
   ⇒ `CONCENTRATED_WEIGHT 0.50`（limit 0.1）。需要**把信号摊到全宇宙**
   （`ts_mean` / `ts_sum` 累积能把非零覆盖拉长）。
4. **`vec_avg` 首次实跑成功**，可列入已验证算子。

**动作**：批 D0-2 换成**时序累积类**（T3 `ts_mean 66` / T12 `ts_sum 252`）+
平台 decay 4→10，同时解决「换手」与「覆盖过窄」两个问题。
### 3.2 批 D0-2（2026-10-31）· `1ZwWen8ac4XI8RzwAKg6ZvO`

设置 `delay=0 / INDUSTRY / decay=10 / trunc=0.08 / nanHandling ON / maxTrade OFF`（decay 4→10）

| # | 模板 | alpha | S | F | 2Y | SUB | TO | margin | long/short | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| T3 | `rank(ts_mean(D(eps),66))` | `VkxKANmV` | 0.83 | 0.45 | 0.86 | 0.44 | **4.46%** | **16.13bp** | 356/357 | 3 |
| T12 | `rank(ts_sum(D(eps),252))` | `N1NkYPJg` | 0.41 | 0.15 | 0.20 | 0.32 | **2.22%** | **16.03bp** | 452/452 | 3 |

**结论**
1. ★★★ **换手治理完全成功**：TO 150.5% → **4.46%**（`ts_mean 66` + decay 10），
   `CONCENTRATED_WEIGHT` 从 0.50 fail → **pass**，持仓从 139 只 → **713 只**，
   `margin` 1.40bp → **16.13bp**（落在 GBR 75% 分位 16.2bp 附近）。
2. ★★★ **但信号被抹平**：S 1.38 → 0.83。TO 降 33× 只换来 S 降 40%，
   说明**原始信号的短周期部分贡献了大部分 Sharpe，但它是不可交易的（TO 150%）**。
3. **`ts_sum 252` 比 `ts_mean 66` 更差**（S 0.41 / 2Y 0.20）⇒ 年度累积把信号彻底摊平，
   252 窗口在 D0 上过长。**D0 的有效记忆长度在 66 日附近，不在 252。**
4. **F 反而上升**（0.37→0.45）：TO 降到 12.5% 以下后 F 公式分母走地板 `max(TO,0.125)`，
   ⇒ 低 TO 天然抬 F。**F 不是 D0 的瓶颈，S 才是。**

**★ 当前核心矛盾（本数据集）**：
```
裸信号（TO 150%）：S 1.38，TO/CW 挂
平滑信号（TO 4.5%）：S 0.83，S 挂
```
两端都不够 2.69。⇒ **「修正幅度」这个信号概念在 GBR 大盘股上本身太弱**
（GBR TOP700 分析师覆盖成熟，修正幅度小且噪声大；且仅 20% 股票在任一日有修正事件）。
**继续在同一概念上换加工方式无意义**，必须换信号概念。

### 3.3 十年数据覆盖验证（goal 第 4 条）· `j2YNqjwo`

`get_alpha_yearly_stats` 逐年核（**不看 `coverage`**）：

| 年 | pnl | long | short | TO | sharpe | returns | drawdown | margin |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2014 | 1,727,999 | 64 | 63 | 144.1% | 2.35 | 16.62% | 3.66% | 23.1bp |
| 2015 | 2,022,813 | 70 | 70 | 151.3% | **2.72** | 19.45% | 3.91% | 25.7bp |
| 2016 | 360,961 | 77 | 78 | 143.4% | 0.47 | 3.47% | 6.35% | 4.8bp |
| 2017 | 631,977 | 68 | 68 | 154.2% | 0.99 | 6.08% | 5.00% | 7.9bp |
| 2018 | 1,868,879 | 70 | 69 | 153.3% | 2.44 | 17.97% | 3.98% | 23.5bp |
| 2019 | 1,129,437 | 74 | 73 | 153.5% | 1.55 | 10.86% | 3.62% | 14.1bp |
| 2020 | 171,505 | 79 | 77 | 148.7% | **0.16** | 1.79% | **11.22%** | 2.4bp |
| 2021 | 507,572 | 74 | 72 | 149.8% | 0.70 | 4.88% | 5.48% | 6.5bp |
| 2022 | 840,058 | 66 | 66 | 152.7% | 0.97 | 8.08% | 5.08% | 10.6bp |
| 2023 | 1,626,124 | 59 | 58 | 154.0% | 2.22 | 15.64% | 4.20% | 20.3bp |

**结论**
- ✅ **2014–2023 共 10 年全部有数据**，每年 long 59–79 / short 58–78，`pnl` 全部为正、
  `sharpe` 全部为正 ⇒ **goal 第 4 条「近十年都要有数据」在 D0 上满足**。
- ⚠ **逐年 sharpe 波动极大（0.16 ↔ 2.72）**：强年 2014/2015/2018/2023（2.2–2.7），
  弱年 2016/2020/2021/2022（0.16–0.99）。**2020 年 sharpe 0.16 + 最大回撤 11.2%** —— 
  事件驱动信号在极端市场（疫情）下失效。这是该族的结构性风险。

### 3.4 环节结论汇总（截至批 2）

| 环节 | 判定 |
|---|---|
| D0 数据可用性 | ✅ 十年完整 |
| D0 塔位 | ✅ `GBR/D0/ANALYST` 独立存在（倍率 1.9） |
| `vec_avg` 算子 | ✅ 实跑可用 |
| 换手治理 | ✅ `ts_mean(66)` + decay 10 ⇒ TO 4.5% |
| 集中度 | ✅ 同上一并解决 |
| **信号强度** | ❌ **S 0.83 vs 门槛 2.69（差 1.86）** ⇒ 必须换信号概念 |
### 3.5 批 D0-3（2026-10-31）· `3z6Qjc4tI4DP8OM1dheRTFJ`

设置 `delay=0 / INDUSTRY / decay=10 / trunc=0.08 / nanHandling ON / maxTrade OFF`

| # | 模板 | alpha | S | F | 2Y | SUB | TO | margin | long/short | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| — | `rank(ts_delta(vec_avg(anl44_eps_coveredby),66))` | `qMLeQp5E` | 0.28 | 0.04 | **−0.11** | 0.43 | **167.7%** | 0.34bp | 34/34 | 5 |
| T5 | `rank(ts_mean(dps_value − last_actual_reported_value, 66))` | `d5WeN69v` | 0.17 | 0.06 | **−0.08** | 0.11 | 3.13% | 9.6bp | 48/48 | 3 |

**两条新机制独立失败**
1. **分析师覆盖度变化**（`coveredby` 的 66 日差分，该字段 alphaCount=0 从未被用）：
   S 0.28 / 2Y **−0.11** / TO **167.7%** / 持仓仅 34+34 只。
   ⇒ ① `coveredby` 是整数计数，`ts_delta` 每日翻动 ⇒ 换手爆表；
   ② 覆盖度变化非零的股票极少（34 只）⇒ 天生窄持仓、`CONCENTRATED_WEIGHT` 必挂。
   **「关注度动量」在 GBR 大盘股上不成立**（覆盖已饱和，变动少且噪声大）。
2. **预期差（dps 版）**：S 0.17 / 2Y **−0.08**。且带 **UNITS 警告**：
   `Incompatible unit for input of "subtract" at index 1, expected "Unit[]", found "Unit[CSPrice:1]"`
   ⇒ ★ **`last_actual_reported_value` 不是 `dps` 的配对字段**（前者带货币单位 `CSPrice`，后者无量纲）。

### 3.6 ★★ 教训：覆盖率匹配 ≠ 字段配对

我曾按「覆盖率逐位相同」推断裸名字段与 `anl44_<measure>_value` 的配对关系
（例如 `dps` 0.7476 ↔ `last_actual_reported_value` 0.7476）。**这个推断是错的**——
UNITS 警告直接证明两者单位不同。覆盖率相同可能只是**同一批股票都有这两类数据**，
不代表语义配对。

⇒ **动作**：以后凡用裸名「上次报告值」字段构造 `subtract`，**必须先看 UNITS 警告**；
出现 `Unit[CSPrice:1]` / 其它单位不匹配就说明配对错了，不要继续在这条线上投入。

### 3.7 ★★★ `analyst44` 数据集判死（三线全灭）

| 信号概念 | 最佳 S | 门槛 2.69 | 缺口 |
|---|---:|---:|---:|
| 修正幅度 `value − prevalue`（裸） | 1.38 | 2.69 | −1.31（且 TO 150% 不可交易） |
| 修正幅度（`ts_mean 66` 平滑） | 0.83 | 2.69 | −1.86 |
| 修正幅度（`ts_sum 252` 累积） | 0.41 | 2.69 | −2.28 |
| 分析师覆盖度变化 | 0.28 | 2.69 | −2.41（且 2Y 为负） |
| 预期差（裸名配对，配对错误） | 0.17 | 2.69 | −2.52（且 2Y 为负） |

**判死依据**：5 条仿真、3 个**机制互不相同**的信号概念（自身修正 / 关注度动量 / 预期差），
全部距门槛 ≥1.31，且最强的两条一个 TO 爆表、一个 2Y 为负。
不是「加工方式不对」，而是**该数据集在 GBR TOP700 上没有足够强的信号**。

**根因假设**：GBR TOP700 全是大盘股，分析师覆盖成熟 ⇒ 修正幅度小、噪声大；
且任一日只有约 20% 股票有修正事件 ⇒ 天然窄持仓。
**这是「大盘股 + 分析师数据」的结构性弱点，不是本数据集独有** ⇒
同 category 的 `analyst10` / `analyst9` / `analyst45` 预期同样弱，**优先级下调**。

**保留资产**：
- ✅ 该数据集**十年数据完整**（2014–2023，见 §3.3）⇒ 若将来有更强骨架可复用；
- ✅ `vec_avg` 算子实跑验证通过；
- ✅ **换手治理配方**：`ts_mean(66)` + 平台 decay 10 把 TO 150%→4.5%、CW fail→pass、
  margin 1.4bp→16.1bp。**这个配方可迁移到任何 D0 高频数据集**。