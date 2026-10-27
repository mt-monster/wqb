# fundamental1（USA）字段画像与挖掘档案 · 2026-10-22

> 数据集：`fundamental1`（USA / D1 / TOP3000 / EQUITY / delay 1）
> 平台分类：`Fundamental` → pyramid `USA/D1/FUNDAMENTAL`（multiplier 1.1）
> 字段总数 **205**，类型 **全部 VECTOR**（无一 MATRIX），必须在标量算子前先 `vec_*` 聚合。
> 本档口径：字段清单取自 `wqb-db.get_field_catalog(region="USA", dataset="fundamental1")` 的 typed catalog
> （205 字段，与 `get_datafields` 经 sharpe 过滤后返回的 179 条不同——差集是本档的**平台不可回测字段**，
> 不是不存在）。census 复算脚本：`logs/_tmp_fnd1_census.py`（只读）。

---

## 0. 数据集元信息与一句话定性

| 项 | 值 |
|---|---|
| 数据集 id | `fundamental1` |
| 内容 | 董事会 / 高管**组成与激励**数据（BoardEx 风格）：董事任期、退休时钟、离职率、学历、年龄分布、性别与国籍构成、连锁董事网络、薪酬与期权计划 |
| 数据类型 | 100% VECTOR |
| 更新频率 | **年度**（以 annual report date 为锚）。批次 27 实测换手率 1.69%–2.58% 是这一点的直接证据 |
| 典型覆盖率 | 董事会/高管组成族 0.754–0.7999；薪酬与期权计划族 0.0003–0.32 |
| 拥挤度 | 平台已提交 alpha 引用总数 **335**（205 字段平均 1.6 条/字段）；aC=0 的 108 个字段中 91 个属薪酬族 |
| 与已交付族的关系 | 已交付 5 颗全部来自 analyst 族（EPS 修正 / 共识背离 / 目标价）。治理维度与分析师修正**机制正交**，prod 风险低 |

**一句话定性**：这是一份**低频、慢变量、截面离散度小**的公司治理特征集。它能提供真实但**弱**的截面倾斜
（批次 27 实测 |S| 上界 0.94），不像分析师修正那样有可交易的信息流。它更像**风险特征**而不像**alpha 源**。

---

## 1. 字段分家族（205 → 7 族）

聚类规则 = 字段 id 前缀；`filtered_` 表示已剔除关联方/非执行董事等噪声行的版本。

| 族 | 前缀 | 字段数 | cov min | cov 中位 | cov max | aC=0 | aC 1–5 | aC>5 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **A 个人董事（board 表，filtered）** | `fnd1_board_characteristics_filtered_` | 10 | 0.7893 | 0.7984 | 0.7984 | 2 | 4 | 4 |
| **B 董事会均值（board 表，raw）** | `fnd1_board_characteristics_` | 13 | 0.1712 | 0.7997 | 0.7999 | 2 | 10 | 1 |
| **C 个人董事（director 表，filtered）** | `fnd1_director_characteristics_filtered_` | 10 | 0.7891 | 0.7984 | 0.7984 | 3 | 7 | 0 |
| **D 个人董事（director 表，raw）** | `fnd1_director_characteristics_` | 14 | 0.1712 | 0.7998 | 0.7999 | 3 | 10 | 1 |
| **E 董事会聚合（filtered）** | `fnd1_filtered_` | 10 | 0.6715 | 0.7984 | 0.7984 | 3 | 2 | 5 |
| **F 董事会聚合（raw）** | `fnd1_`（其余） | 12 | 0.1220 | 0.7998 | 0.7999 | 4 | 6 | 2 |
| **G 薪酬 / 期权计划（无前缀）** | 无 `fnd1_` 前缀 | **136** | 0.0003 | 0.1991 | 0.8010 | **91** | 43 | 2 |

**读法**：

- **A/C/E/F 四族是同一批治理量在四个聚合层级上的镜像**（个人-过滤 / 个人-原始 / 董事会-过滤 / 董事会-原始）。
  选字段时不要跨族重复取同义字段（`fnd1_board_characteristics_timebrd` 与
  `fnd1_director_characteristics_timebrd` 是同一经济量的董事会均值/个人值），否则是伪多样本。
- **G 族占 2/3 的字段数但只贡献 1/3 的可用性**：136 个薪酬字段里 91 个从未被任何平台 alpha 引用，
  且覆盖率中位仅 0.199——这是典型的「报表披露深度不均」字段块，覆盖率 <0.4 时任何裸用都会产生
  集中持仓（`CONCENTRATED_WEIGHT`）。
- **A/C 两族的 `filtered` 版本覆盖率更高**（0.7984 vs B/D 的 0.7999 但含关联方行），优先用 filtered。

---

## 2. 覆盖率 / 可用性分档

### 2.1 覆盖率分布（全 205 字段）

| 覆盖率档 | 字段数 | 占比 |
|---|---:|---:|
| < 0.40（不可裸用） | 122 | 59.5% |
| 0.40–0.60 | 6 | 2.9% |
| 0.60–0.75 | 4 | 2.0% |
| ≥ 0.75 | **73** | 35.6% |

**双峰**：治理组成字段挤在 0.75–0.80（可用），薪酬/期权字段挤在 0.00–0.32（不可用），中间几乎没有过渡。
这说明它不是「覆盖度连续衰减」的噪声集，而是**两张表拼接**：一张全量董事会表 + 一张稀疏薪酬明细表。

### 2.2 aC 分布（平台已提交 alpha 的字段引用数）

| aC | 字段数 |
|---|---:|
| 0 | **108** |
| 1–5 | 82 |
| 6–15 | 11 |
| > 15 | 4 |

- 引用总数 335。最拥挤的四个：`average_other_board_tenure` (20)、`fnd1_filtered_attrition3yr` (18)、
  `fnd1_director_characteristics_totcurrnounlstdbrd` (16)、`fnd1_board_characteristics_filtered_totnounlstdbrd` (15)。
- **aC=0 ≠ 未被挖过**：论坛帖不计入 alphaCount。本数据集的治理机制在中文论坛有定性帖（§6），
  但**无一条表达式**——所以 aC=0 的字段是可用的，但「治理」这个**概念**已被公开点题。

### 2.3 可用字段集（cov ≥ 0.40 且非标识/汇率/价格码）

**81 个**（205 的 39.5%）。按 aC 降序的头部（完整表见 `logs/_tmp_fnd1_census.py` 输出）：

| 字段 | 族 | cov | user | aC | 经济含义 |
|---|---|---:|---:|---:|---|
| `average_other_board_tenure` | G | 0.7683 | 11 | 20 | 在其他上市公司任职的平均年限（外部经验存量） |
| `fnd1_filtered_attrition3yr` | E | 0.6715 | 8 | 18 | 近 3 年执行董事离职率 |
| `fnd1_director_characteristics_totcurrnounlstdbrd` | D | 0.7957 | 8 | 16 | 当前兼任的私营(非上市)董事席位数 |
| `fnd1_board_characteristics_filtered_totnounlstdbrd` | A | 0.7980 | 7 | 15 | 历史累计私营董事席位数 |
| `fnd1_filtered_genderratio` | E | 0.7984 | 6 | 12 | 男性执行董事占比 |
| `fnd1_filtered_numberdirectors` | E | 0.7984 | 3 | 12 | 执行董事人数（董事会规模） |
| `fnd1_board_characteristics_filtered_timeretirement` | A | 0.7981 | 4 | 12 | 距退休时间 |
| `fnd1_board_characteristics_timebrd` | B | 0.7999 | 4 | 11 | 董事会平均任职年限 |
| `fnd1_board_characteristics_filtered_avgtimeothco` | A | 0.7984 | 5 | 10 | 在其他上市公司董事会的平均年限 |
| `fnd1_filtered_stdevage` | E | 0.7981 | 6 | 10 | 董事年龄标准差（代际分散度） |
| `fnd1_board_characteristics_filtered_timebrd` | A | 0.7984 | 6 | 8 | 个人董事会任职年限 |
| `fnd1_filtered_succession` | E | 0.7984 | 5 | 7 | 临近退休年龄的董事聚集度（继任风险） |
| `fnd1_filtered_stdevnoquals` | E | 0.7984 | 1 | 3 | 学历数标准差（人力资本异质性） |
| `fnd1_stdevage` / `fnd1_succession` / `fnd1_numberdirectors` | F | 0.799 | 3/3/0 | 3/4/0 | 同上，raw 版本 |
| `fnd1_board_characteristics_filtered_totcurrnolstdbrd` | A | 0.7984 | 0 | 0 | 当前上市公司董事席位（忙碌董事） |
| `fnd1_board_characteristics_timeinco` | B | 0.7999 | 0 | 0 | 董事会平均公司任期（**水平量，未挖**） |
| `fnd1_stdevtimebrd` / `fnd1_filtered_stdevtimebrd` | F/E | 0.7984–0.7999 | 0 | 0 | 任职年限标准差（**水平量，未挖**） |
| `board_nationality_diversity_ratio` | G | 0.7621 | 0 | 0 | 外籍董事占比（**未挖**） |

### 2.4 可用性硬伤剔除

| 类别 | 数量 | 字段 | 剔除理由 |
|---|---:|---|---|
| 标识符 | 3 | `fnd1_board_characteristics_boardid`、`fnd1_director_characteristics_boardid`、`..._directorid` | 纯 id，无经济含义；作分组会把股票分到近唯一组 |
| 汇率码 | 7 | `compensation_currency_code{,_2}`、`currency_iso_code_8`、`incentive_currency_code`、`monetary_unit_code`、`option_currency_code`、`option_plan_currency_code` | 分类变量，不可当信号 |
| 价格水平 | 10 | `option_plan_stock_price`、`option_exercise_price{,_2,_5}`、`option_strike_price`、`incentive_plan_stock_price`、`ltip_wealth_stock_price`、`option_award_stock_price`、`reference_stock_price`、`incentive_option_exercise_price` | 非平稳价位，跨年跨度大，裸用等于做多/做空高价股 |

### 2.5 同名变体（29 组 / 62 字段）

去 `_2` / `_3` / `_5` 后缀后同名的有 29 组，典型如
`exercisable_option_intrinsic_value{,_2,_3}`、`option_exercise_price{,_2,_5}`、`share_award_value{,_2,_3}`。
**这些是同一经济量的不同报表口径/不同公司批次，不是独立信号**——同一波内不得同时取两条，否则是伪样本。

### 2.6 分布特征

- **比率量**（genderratio、各 diversity ratio、attrition、succession）：界在 [0,1]，右偏，大量 0；
  `winsorize(std=4)` 后仍需 `group_rank` 化，否则少数极高值主导。
- **年限量**（timebrd、timeinco、timeretirement、avgtimeothco）：右偏、单位年，跨公司尺度差异大
  ⇒ 必须 `ts_zscore` 或 `group_rank`，禁止裸用水平值做线性比较。
- **计数量**（numberdirectors、tot*brd、noquals）：离散、小整数、右偏 ⇒ `ts_backfill` + `rank` 最稳。
- **金额量**（compensation / option 族）：重尾 + 覆盖率极低 ⇒ **本档判定不可用**，不进任何候选。

---

## 3. 机制候选（经济机制，不是算子模板）

| # | 机制 | 经济陈述 | 首选字段 | 预登记方向 |
|---|---|---|---|---|
| G1 | **治理不稳定** | 高管大规模离职 → 战略断档与执行风险 | `fnd1_filtered_attrition3yr` | 高离职 → 空 |
| G2 | **继任风险** | 董事年龄聚集在退休窗口 → 权力交接不确定性 | `fnd1_filtered_succession` | 高聚集 → 空 |
| G3 | **董事会任期（壁垒 vs 经验）** | 任期长 = 知识/稳定（正面）或堑壕/监督失效（负面），待实测定向 | `fnd1_board_characteristics_timebrd`、`fnd1_director_characteristics_timeinco` | 双向 |
| G4 | **董事会异质性** | 年龄/学历/任期分散 → 监督视角多元 → 决策质量 | `fnd1_filtered_stdevage`、`fnd1_filtered_stdevnoquals`、`fnd1_stdevtimebrd` | 高离散 → 多 |
| G5 | **退休时钟** | 距退休越近 → 短期主义与继任折价；反向则是"稳态团队"溢价 | `fnd1_board_characteristics_filtered_timeretirement` | 双向 |
| G6 | **连锁董事网络** | 兼任席位数 = 信息渠道（正面）或过度承诺（负面） | `fnd1_board_characteristics_filtered_totnounlstdbrd`、`fnd1_director_characteristics_totcurrnounlstdbrd` | 待实测 |
| G7 | **董事会规模** | Gompers-Ishii-Metrick (2003)：大董事会 → 沟通成本 → 估值折价 | `fnd1_filtered_numberdirectors` | 大 → 空 |
| G8 | **多元性** | 性别/国籍多元 → 监督质量与人才池 | `fnd1_filtered_genderratio`、`board_nationality_diversity_ratio` | 多元 → 多 |

---

## 4. 批次 27（2026-10-22）：5 机制 × 2 变换 = 10 臂

### 4.1 预登记

- 壳：`±quantile(group_rank(winsorize(ts_backfill(<transform>, 252), std=4), subindustry))`
- 设置：USA / TOP3000 / D1 / decay 20 / SUBINDUSTRY / trunc 0.08 / nan ON / VERIFY / FASTEXPR
- 变换：`ts_delta(F, 252)`（年度变化）与 `ts_zscore(F, 504)`（自身 5 年历史位置）
- multisim `2inxa1dIW531a7jNMHin1M8`，10 臂
- **判死线（预登记）**：若 10 臂全无 |S| ≥ 1.20，则本变换族（governance change）判定不可达 USA 1.58 门槛。

### 4.2 实测结果

| 臂 | 核心字段 | 变换 | alpha | S | F | 2Y | SUB | TO | 判定 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| M1a − | `fnd1_filtered_attrition3yr` | Δ252 | `1YjN0QJ6` | −0.42 | −0.15 | −1.07 | −0.09 | 1.69% | 反号后 S +0.42 |
| M1b − | 同上 | z504 | `YPx1YGQM` | −0.69 | −0.29 | −0.93 | −0.53 | 2.00% | 反号后 S +0.69 |
| M2a − | `fnd1_filtered_succession` | Δ252 | `A1QVEM3R` | −0.67 | −0.30 | −1.39 | −0.04 | 1.86% | 反号后 S +0.67 |
| M2b − | 同上 | z504 | `xA1r50ng` | −0.64 | −0.22 | −1.06 | −0.06 | 2.31% | 反号后 S +0.64 |
| M3a − | `fnd1_director_characteristics_timeinco` | Δ252 | `vRO1P3mz` | **−0.94** | −0.45 | **−2.17** | −0.17 | 1.85% | 反号后 S +0.94 / 2Y +2.17（SUB 0.17 < 0.40 挂） |
| M3b − | 同上 | z504 | `1YjN0Qgz` | −0.84 | −0.35 | −0.29 | −0.20 | 2.54% | 反号后 S +0.84 |
| M4a + | `vec_stddev(fnd1_director_characteristics_timeinco)` | Δ252 | `88vRXdLv` | 0.81 | 0.36 | **1.93** | −0.01 | 1.86% | SUB 挂（−0.01 vs 0.35） |
| M4b + | 同上 | z504 | `P0MoKd1x` | 0.62 | 0.22 | 0.39 | 0.12 | 2.48% | S/2Y/SUB 三闸掉 |
| M5a + | `fnd1_board_characteristics_filtered_timeretirement` | Δ252 | `0mjY5086` | 0.82 | 0.41 | 1.45 | **0.28** | 1.84% | SUB 差 0.08（需 0.36） |
| M5b + | 同上 | z504 | `N1eN8vOE` | 0.65 | 0.23 | 1.19 | 0.29 | 2.58% | SUB 过 / S+2Y 掉 |

### 4.3 归因（先归因再推进）

**① 方向：预登记 6/6 全错，且错误方向一致。**
M1–M3 全部预登记「高离职/高继任/长任期 → 做空」，10 臂里这 6 臂**全部为负**——即**未取反的方向 6/6 为正**
（+0.42 / +0.69 / +0.67 / +0.64 / +0.94 / +0.84）。这不是噪声，是系统性符号反转：

> 在 USA 截面里，**任期长、离职率高的董事会对应的是"稳定复利型"与"高周转成长型"两类赢家**，
> 而"治理风险溢价"（买入治理差的公司）在本样本期是**负收益**。治理变量在此表现为**质量/稳定性代理**，
> 不是风险代理。这条结论与「value/quality 在 USA 必死」的区域先验一致，但方向相反地说明：
> 治理分高的公司被市场继续给溢价，属于**动量型质量**。

**② 硬闸顺序：S 是唯一真瓶颈，SUB 是并发的第二瓶颈。**
10 臂 S 落在 −0.94 ~ +0.82（反号后 +0.42 ~ +0.94），距 1.58 差 0.64–1.16；
SUB 只有 M5b 一枚过（0.29 vs 0.28），M4a 的 SUB 仅 −0.01，M5a 差 0.08。
按 `LOW_SUB_UNIVERSE_SHARPE = 0.43 × S` 的比例闸：反号后的 M3a（S 0.94）需要 SUB ≥ 0.40，实测 0.17
⇒ **即使把方向改对，SUB 也按比例挂**。这是"截面信号在高覆盖股上不成立、只在边缘股上成立"的典型指纹。

**③ 换手率 1.69%–2.58%：信号在时间上几乎不动。**
年度字段 + `ts_delta(252)` / `ts_zscore(504)` + decay 20 ⇒ 组合一年只重排一次。
平台 `LOW_TURNOVER` 闸**通过**（限值约 1%），所以这本身不违规；但它意味着
**alpha 的全部收益来自一个静态截面排序的漂移**，信息率天然受限。这一条是 S 上不去的第一性原因。

**④ F 与 2Y 的分裂：M4a / M5a 的 2Y 1.93 / 1.45 远高于全期 S。**
说明「董事会异质性」与「退休时钟」两个机制**只在近两年有效**，2014–2021 无效。
按 USA 区域纪律（`2Y ≥ 1.58` 且需要全期 S ≥ 1.58），这不足以构成可提交 alpha，且是典型的**近端过拟合风险**。

**⑤ `risk_neutralized_sharpe` 0.24–0.46（正方向臂）**：排除"纯风格 beta"——信号里有真实的特质成分，
只是**弱**。这支持"不是字段选错，是字段的信息量本身到顶"。

**结论**：批次 27 的预登记判死线（全无 |S| ≥ 1.20）**触发**。governance-change 变换族判不可达。

---

## 5. 批次 28（预登记）：静态水平量 × 2 形状 = 10 臂

**为什么要再打一波**（而不是立刻弃集）：批次 27 只测了**变化量**（Δ252 / z504）。文献里治理因子用的是
**水平量**（board tenure level、board size、diversity ratio），且批次 27 最强的两个机制（G4 异质性、G5 退休时钟）
是**水平量在近端有效**。同时 `group_zscore` 形状（肥尾）在 fnd1 上从未测过，是用户要求的"算子全面替换"里
唯一还没覆盖的壳层。这一波是**结构性尝试**，不是参数扫。

| 臂 | 机制 | 字段 | 方向 | 形状 |
|---|---|---|---|---|
| L1 | G3 任期（经验） | `fnd1_board_characteristics_timebrd` | + | `quantile(group_rank(...))` |
| L2 | G3 任期（经验） | 同上 | + | `group_zscore(...)` |
| L3 | G4 异质性 | `fnd1_filtered_stdevage` | + | `quantile(group_rank(...))` |
| L4 | G4 异质性 | 同上 | + | `group_zscore(...)` |
| L5 | G7 规模 | `fnd1_filtered_numberdirectors` | − | `quantile(group_rank(...))` |
| L6 | G7 规模 | 同上 | − | `group_zscore(...)` |
| L7 | G8 多元性 | `fnd1_filtered_genderratio` | − | `quantile(group_rank(...))` |
| L8 | G8 多元性 | 同上 | − | `group_zscore(...)` |
| L9 | G6 连锁网络 | `fnd1_board_characteristics_filtered_totnounlstdbrd` | − | `quantile(group_rank(...))` |
| L10 | G6 连锁网络 | 同上 | − | `group_zscore(...)` |

- 壳：`±quantile(group_rank(winsorize(ts_backfill(F, 252), std=4), subindustry))` 与
  `±group_zscore(winsorize(ts_backfill(F, 252), std=4), subindustry)`
- 设置同批次 27（decay 20 / SUBINDUSTRY / trunc 0.08）。
- multisim `1pCYdVaGw4IMa9SP6uP3xLZ`，10 臂。
- **判死线（预登记）**：若 10 臂仍全无 |S| ≥ 1.20，则 `fundamental1` 判**结构性不可达**，
  不再在该数据集上开波（理由：水平量与变化量、两种形状、15 个字段全部封顶在 0.94）。

### 5.1 实测结果（10/10 收批）

| 臂 | 核心字段 | 方向 | 形状 | alpha | S | F | 2Y | SUB | TO | `risk_neu_S` |
|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| L1 | `fnd1_board_characteristics_timebrd` | + | rank | `E5V6xEe9` | **0.69** | 0.38 | **1.29** | 0.15 | 1.68% | 0.59 |
| L2 | 同上 | + | zscore | `xA1r5kNq` | 0.51 | 0.25 | 1.09 | 0.26 | 1.63% | 0.40 |
| L3 | `fnd1_filtered_stdevage` | + | rank | `ZYmQNnEZ` | 0.11 | 0.02 | 0.12 | −0.07 | 1.88% | 0.18 |
| L4 | 同上 | + | zscore | `WjLOJGAN` | −0.56 | −0.19 | −0.71 | −0.27 | 1.87% | −0.21 |
| L5 | `fnd1_filtered_numberdirectors` | − | rank | `e765E03O` | −0.72 | −0.34 | −1.22 | −0.35 | 1.98% | −0.41 |
| L6 | 同上 | − | zscore | `wp9QWlaQ` | −0.38 | −0.14 | −0.85 | −0.26 | 2.14% | 0.00 |
| L7 | `fnd1_filtered_genderratio` | − | rank | `akVKGn1w` | −0.29 | −0.07 | −1.14 | −0.17 | 1.95% | −0.53 |
| L8 | 同上 | − | zscore | `LL5M317L` | 0.19 | 0.04 | −0.57 | −0.12 | 1.99% | −0.22 |
| L9 | `fnd1_board_characteristics_filtered_totnounlstdbrd` | − | rank | `rKdR8ljm` | **−0.94** | −0.41 | −0.42 | −0.25 | 1.80% | −0.91 |
| L10 | 同上 | − | zscore | `KPmJZ978` | −0.45 | −0.15 | 0.19 | −0.01 | 1.86% | −0.70 |

### 5.2 归因

**① 判死线触发**：全波最强 |S| = **0.94**（L9 连锁董事数），次强 0.72（L5 董事会规模），
与批次 27 的最强 0.94 完全相同。**15 个字段 / 2 类变换（水平 vs 变化）/ 2 种形状（秩 vs z）全部封顶在 0.94**
⇒ 不是字段选错，是这个数据集的信息量天花板。

**② 形状有系统差异，秩变换稳定更强**：L1 0.69 vs L2 0.51、L3 0.11 vs L4 −0.56、L9 −0.94 vs L10 −0.45。
秩变换（`quantile(group_rank)`）在 3 组里 3 组更强 ⇒ 信号由**尾部**驱动，线性关系弱。
这是"信息稀疏、只在极端值上有效"的形态，与年度更新频率一致。

**③ 规模/网络两族方向为负且 `risk_neu_S` 也负**（L9 −0.91 / L7 −0.53 / L5 −0.41）：
「董事席位越多 / 董事会越大 / 性别越单一 → 未来收益越差」在风险中性化后仍然成立，
说明这不是风格 beta，而是**真实的（但是弱的）质量折价**。这是本集唯一有理论一致性的方向，
但强度只有 0.94，离 1.58 的闸差 0.64。

**④ 任期（G3）仍是唯一"近端有效"的机制**：L1 的 2Y 1.29 显著高于全期 0.69（与批次 27 的 M4a 2Y 1.93 同型）。
2014–2021 无效、2022–2023 有效 ⇒ 近端过拟合风险，不可作提交依据。

**⑤ TO 1.63%–2.14%**：15 个字段无一例外落在 2% 邻域。年度字段 + 任意变换 + decay 20
都改不了「一年只重排一次」的事实 ⇒ 信息到达频率是结构性的，`LOW_TURNOVER` 虽过（限 ~1%），
但 Sharpe 上限被限死。

### 5.3 结论

`fundamental1` **判结构性不可达**（预登记判死线触发）。后续不再在该集开波。

---

## 6. 论坛取证（2026-10-22）

| 帖 | 日期 | 内容 | 对本集的含义 |
|---|---|---|---|
| `43691541466903`「治理维度的数据化：Management and Executive Data 能做什么」 | 2026-09-23（24 赞，0 评论） | **纯定性**：点名董事会构成 / 独立董事比例 / 连锁董事网络 / 人事变动前兆 / **低频慢变量** / 覆盖范围差异；**无一条表达式、无一个字段 id** | 概念已被公开点题 ⇒ 中等拥挤；但**无配方** ⇒ 不是致命拥挤。它独立佐证了两件事：① "低频慢变量"（正是 TO 1.7% 的成因）；② 连锁董事网络与独立董事比例是自然的下一批机制 |
| 同批检索 `高管 董事 管理层 变更` | — | 50 条命中，`fundamental14`（Audit Analytics Directors Data）另有一帖 | `fundamental14` 是 USA 另一份治理集，若 fnd1 判死可作后续候选（但注意：换数据集需说明理由） |

**纪律沉淀（可复用）**：`aC=0 ≠ 未被挖过`。选字段前应按**机制名**（不是字段 id）检索论坛；
命中 `【Alpha Idea】` / `【Alpha灵感】` 形态的帖子要当作"概念已公开"处理。

---

## 7. 待收与索引

- 批次 28 收批后回填 §5 的实测列；若判死，在本档 §8 写终判并 `seal_dead_end`（需用户 `force_seal`，
  论坛取证闸 fail-closed）。
- 字段 census 可复算：`world-quant-brain-mcp/.venv/Scripts/python.exe -X utf8 logs/_tmp_fnd1_census.py`。
- 关联档案：[`_usa-field-profile-playbook-20261018.md`](_usa-field-profile-playbook-20261018.md)（逐字段判死口径）、
  [`_usa-fundamental-dataset-scan-20261019.md`](_usa-fundamental-dataset-scan-20261019.md)（Fundamental 类别全景）。

---

## 8. 终判（2026-10-22）：`fundamental1` 判 `dead_end`（数据集级）

**结论一句话**：在 USA / TOP3000 / D1，`fundamental1`（Management & Executive，205 字段全 VECTOR、年度更新）
**不能产出一颗满足 USA 1.58 闸的 ATOM alpha**，最强读数 0.94，离闸差 0.64。

**证据面（20 臂，覆盖 15 个字段、3 类变换、2 种形状、2 组设置）**：

| 维度 | 覆盖面 | 最强 |S| |
|---|---|---:|
| 变化量（Δ252 / z504） | 批 27：5 机制 × 2 = 10 臂 | 0.94 |
| 水平量（`vec_avg` 原值） | 批 28：5 字段 × 2 形状 = 10 臂 | 0.94 |
| 变换族 | 水平 / 年度变化 / 5 年自身 z 分 / VECTOR 内离散度 | — |
| 形状族 | `quantile(group_rank)` / `group_zscore` | — |
| 机制族 | G1 离职 / G2 继任 / G3 任期 / G4 异质性 / G5 退休 / G6 连锁 / G7 规模 / G8 多元性 | — |

**四条判死依据**：

1. **信息到达频率是硬上限**：15 个字段的换手率全部落在 1.63%–2.58%（年度治理披露 + 任意变换 + decay 20），
   组合一年只重排一次；`LOW_TURNOVER` 虽过（限 ~1%），但 Sharpe 被信息率锁死。
2. **两类变换给出同一天花板**：水平量与变化量的最强臂都是 0.94 ⇒ 不是变换没试对，是字段本身信息量到顶。
3. **唯一有理论一致性的方向也太弱**：G6 连锁董事数 / G7 董事会规模为负且 `risk_neutralized_sharpe`
   仍为负（−0.91 / −0.41）⇒ 这是真实的（弱）质量折价，不是风格 beta；但 0.94 的强度不可提交。
4. **近端有效 ≠ 可提交**：G3 任期的 2Y 1.29（批 28 L1）与 G4 异质性的 2Y 1.93（批 27 M4a）都远高于全期 S，
   是 2022–2023 单窗口贡献，属典型近端过拟合形态。

**不再投入的理由**：已按用户约束「不频繁切换数据集」在该集打满 2 波 20 臂，覆盖全部 8 个机制假设与
全部可用变换/形状组合；继续在同一集上扫参属于「同族磨参数」，触发 USA 区域纪律 D0-P 的禁止项。

**换集决策（说明原因）**：转向 `analyst_factor_signals`（922 字段 / MATRIX / 季度更新 / 平台 α 覆盖广）。
依据有两条：① USA Fundamental 类别级扫描（`_usa-fundamental-dataset-scan-20261019.md` §6）已实证
**Fundamental 类在 USA/TOP3000 无法产出 ATOM**（32 条实测最高 S 1.43 且 SUB 挂）；② 已交付的 5 颗全部来自
analyst 族，是本区唯一被证明能过闸+过 prod 的族。新波次只打**未交付过的机制族**（不确定性/修正强度/实现值），
不与已交付的增长率/偏度/背离/动量族重叠。
