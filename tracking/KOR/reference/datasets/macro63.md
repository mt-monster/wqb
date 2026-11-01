# macro63 — Index Reconstitution Data（KOR / TOP600 / Delay=1）

> 画像日期：2026-10-30。数据源：MCP `get_datasets` + `get_datafields`（region=KOR, delay=1, universe=TOP600）。
> 塔归属：**macro**（KOR/D1 未点亮，塔乘数 1.4）。

## 1. 数据集事实

| 项 | 值 |
|---|---|
| id / 名称 | `macro63` / Index Reconstitution Data |
| category | macro |
| 覆盖率 | **1.0**（全 universe） |
| 字段数 | **1** |
| userCount / alphaCount | 81 / **192** |
| valueScore / 塔乘数 | 3 / 1.4 |

## 2. 字段全表（1/1）

| 字段 | 类型 | 覆盖率 | αC | description（原文） |
|---|---|---|---|---|
| `mcr63_membership` | MATRIX | 1.0 | 192 | Indicates the membership status of stocks in the WisdomTree WTIDJH Index |

**读数含义（关键）**：这是一个 **0/1 成员状态哑变量**，不是连续量。
- 「覆盖率 1.0」= 每个标的每天都有值（**含 0**），**不等于**「每只股票都在指数内」。
- 有效横截面 = 成员集合（远小于 600），非成员一侧全 0 ⇒ **裸 `rank` 只有两档，直接做多空等于做「入指组合 vs 非入指组合」的静态暴露**，不是 alpha。

## 3. 字段画像五问（0.3）

| 问 | 答 | 决策 |
|---|---|---|
| 测什么 | 某只股票**当前**是否属于 WTIDJH 指数 | 状态变量（存量、离散） |
| 怎么测 | 平台给的日频快照 | 只能取**变化率**才成信号（铁律 A） |
| 时间维度 | 存量（且离散） | `ts_delta(·, N)` 是**唯一合法主形态** |
| 为何存在 | 指数供应商的重构事件记录 | 事件在 `ts_delta` 里显现 |
| 可靠性 | 覆盖率满，但**事件极稀疏**（年度重构） | ⚠ CW（CONCENTRATED_WEIGHT）必须第一读数 |

**预处理决策**：`ts_delta(mcr63_membership, 252)` ⇒ 入指 +1 / 出指 −1 / 无事件 0。
窗口取 **252**（年度重构节奏）与 **126**（半年度）两档；短窗（≤22）**不测**——重构不是月度事件，短窗期望恒为 0。

## 4. A-2 收益来源声明

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | 被动资金（跟踪 WTIDJH 的 ETF / 指数基金）与套利者 |
| **为什么会被错** | **需求曲线向下倾斜**（Shleifer 1986）：入指 ⇒ 指数基金被迫买入 ⇒ 价格临时高于基本面；出指 ⇒ 被迫卖出 ⇒ 临时低估。摩擦来自**指数基金的授权约束**（不能持有非成分股），不是信息 |
| **错了多久修复** | 效应在**生效日前后数日**达峰，**20–60 个交易日**部分回吐（Harris-Gurel 1986 的价格压力-反转；Greenwood 2008 的过度联动在事件后持续数周） |
| **预期方向** | 入指后**短期正**、随后反转；出指后**短期负**、随后反转。★ 这两个方向在同一表达式里靠 `ts_delta` 的符号自然对冲，**不需要加权拼腿** |

## 5. 双通道取证状态

| 通道 | 状态 | 内容 |
|---|---|---|
| A｜论坛 | ✅ **已查（2026-10-30）**，见 §5.1 | `tools/forum_recon.py`，question_key `ccc7934485`，`found=true` / 4 篇；**逐条核读后只有 1 篇真正相关** |
| B｜文献 | ✅ 机制成立（下文） | Shleifer 1986 JPE「Do Demand Curves for Stocks Slope Down?」；Harris & Gurel 1986 JF「Price and Volume Effects Associated with Changes in the S&P 500 List」；Greenwood 2008 JF「Excess Comovement of Stock Returns」 |

⚠ **文献偏误登记**：三条实证全部基于 **USA / S&P 500**。KOR 的 WTIDJH 是**外资指数供应商的股息指数**，
成分调整触发的是**跨境被动资金**，规模与节奏都不同于 S&P ⇒ **只作机制假说，方向与持有期必须本区实测**。

### 5.1 A 通道实测（2026-10-30，`tools/forum_recon.py`，key `ccc7934485`）

`found=true` / 4 篇 / 1 轮收敛。**逐条核读后的诚实结论：只有 1 篇相关，且是方法论贴不是配方贴。**

| 命中帖 | 判定 |
|---|---|
| **《断点回归在 Alpha 效应识别中的巧妙应用》**（16 赞，DA98440） | ⭐ **唯一可用**。明确把「指数纳入与剔除」列为 RDD 三场景之一：纳入决策基于可投资性评分、阈值附近被纳入 vs 未纳入的差异可归因为被动资金流。**但它的「实用价值」段自我否证**：`断点效应往往是短暂的…一个只在阈值附近 1% 的股票上有效的信号，转换到整个 universe 的 Alpha 的价值有限` |
| 《市场制度对 Alpha 表现的深远影响》 | 制度变迁对**既有信号**的影响（分数报价→小数报价），与本机制无关 |
| 《从垃圾堆中翻出了一个 MAPC 的 Alpha》 | ETF 残差 return 的时序稳定度，与成分变更无关 |
| 《预防高 pc 的 alpha 以及解决方法》 | 通用降相关清单，无机制 |

**A 通道对本数据集的实际贡献**：不给表达式，只给两条**硬约束**——
① 阈值局部信号（≈ 每年十几个标的非零）**天然撞 CW**，与该贴自述的「1% 股票上有效」完全同构；
② 有效窗口短（数日到数周）⇒ 只能 `trade_when` 事件门控，**不能持久 rank 持仓**。
⇒ 与 §4 A-2 的 Harris-Gurel 20–60 日回吐窗口一致，两条通道在「短窗事件」上收敛。

**取证后的裁决（fail-closed 已满足）**：允许发 **1 条** CW 探针（M1），**不按整族发波**；
若 M1 的 CW ≥ 0.1，按 `KOR-AIEQUITY-PROBE-DEAD` 同形处理，整集不进 quota。


## 6. 候选设计（≤4，A 通道取证前不派发）

| # | 表达式 | 机制 | 风险 |
|---|---|---|---|
| M1 | `group_rank(ts_delta(mcr63_membership, 252), sector)` | 入指/出指事件（年度） | CW 破 0.1（事件日极少数标的非零） |
| M2 | `group_rank(ts_delta(mcr63_membership, 126), sector)` | 半年度重构节奏 | 同上 |
| M3 | `group_rank(ts_mean(ts_delta(mcr63_membership, 252), 63), sector)` | 事件后 63 日持有（对齐 Harris-Gurel 反转窗口前段） | 平滑后非零面略宽，CW 可能缓解 |
| M4 | `group_rank(ts_decay_linear(ts_delta(mcr63_membership, 252), 63), sector)` | 同上但线性衰减（M3 的对照） | 同 M3 |

**派发前必须满足**：① 论坛 A 通道取证完成（fail-closed）；② 先发 **1 条** 探针（M1）确认 CW 读数——
若 M1 的 CW ≥ 0.1，整族按 `KOR-AIEQUITY-PROBE-DEAD` 同形处理，**不进 quota**。

## 6.1 wave 215 实发式（3 条，按铁律 B 显式双侧 + 1 条持有形态）

| # | 表达式 | 取式理由（指回 ②.b 某行） |
|---|---|---|
| 1 | `group_rank(ts_delta(mcr63_membership, 252), sector)` | ②.b「单边恒正/离散存量 ⇒ `ts_delta`」（铁律 A）；正向臂 = 入指后做多 |
| 2 | `reverse(group_rank(ts_delta(mcr63_membership, 252), sector))` | 铁律 B：`reverse()` 不是精确反号（截断×decay×符号交互），必须实发 |
| 3 | `group_rank(ts_decay_linear(ts_delta(mcr63_membership, 252), 63), sector)` | Harris–Gurel temporary 窗口 20–60 日 ⇒ 事件后 63 日线性持有；同时是 CW 缓解形态 |

**派发前预注册证伪条件（读数前写死，铁律 F 前置）**：

1. **CW 硬判据**：M1 的 `CONCENTRATED_WEIGHT` ≥ 0.1 ⇒ 按 `KOR-AIEQUITY-PROBE-DEAD` 同形处理，
   **整集不进 quota**（事件日非零标的数 ≈ 全 universe 的 5% ⇒ 权重天然集中，这是机制自带的，不是参数问题）。
2. **机制方向**：Shleifer 需求曲线 ⇒ 入指后**短期上涨**；若 M1 的 S < 0 且 M2（反向）≈ +|S|，
   说明读到的是「入指前已涨完、入指即反转」（信息泄露/抢跑），属另一条机制，须换方向句后才续挖。
3. **无信号判据**：`max(|S|) < 0.5` 且 `max(|2Y|) < 0.8` ⇒ 判「单字段 0/1 哑变量在 TOP600 上截面信息量不足」，
   macro 塔按数据稀缺关闭（本塔只有 1 个数据集 / 1 个字段），**不补参数**。
4. **十年覆盖（约束 4）**：任一年 `longCount = 0` ⇒ 整集出局。⚠ 本字段 cov=1.0 但**事件稀疏**，
   `longCount` 在非事件年可能只剩 0 值持仓 ⇒ 必须先看 `get_alpha_yearly_stats` 再谈信号强弱。

## 7. 实测记录

### 7.1 wave 215（2026-10-30，3 条；STATISTICAL / decay 4 / truncation 0.08 / TOP600 / D1）

批次 `4lrgL86Ff4hA9l0Fv4Sv7kq`（multisim，本波按 `--batch-type probe` 免闸 6）；DB
`harvest_multisim_results` 回写 `linked=3 / upserted=3 / wave_result=FAIL`；pipeline `candidates=0 near=0`，
checkpoint `db:ledger_kv/KOR/ckpt_w215`。

| # | alpha | 表达式 | S | TO | longCount |
|---|---|---|---|---|---|
| 1 | `xArwZvdw` | `group_rank(ts_delta(mcr63_membership, 252), sector)` | 0.00 | 0.00 | 0 |
| 2 | `LLMbQKd1` | `reverse(...)`（M1 反向臂） | 0.00 | 0.00 | 0 |
| 3 | `3qoYN0e0` | `group_rank(ts_decay_linear(ts_delta(mcr63_membership, 252), 63), sector)` | 0.00 | 0.00 | 0 |

**逐年（`get_alpha_yearly_stats(xArwZvdw)`，2014–2023 共 10 年）**：每一年 `pnl / longCount / shortCount /
turnover / sharpe / returns / fitness` **全部为 0**，`bookSize` 恒 20,000,000。
⇒ **整个 IS 期是一张空账 —— 不是「信号弱」，是「一次都没建仓」。**

平台 checks：`LOW_SHARPE` 0.00 vs limit **1.58** fail；`LOW_TURNOVER` 0.00 vs limit 0.01 fail；
`LOW_FITNESS` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_INVESTABILITY_CONSTRAINED_SHARPE` / `CLUSTER_TEST`
均 `:ERROR`（无持仓无从计算）。补证：`get_record_sets(xArwZvdw)` 返回空响应体（无 record set）——与空账一致。

### 7.2 判读（预注册条件逐条对账）

| 预注册条件 | 读数 | 结论 |
|---|---|---|
| ① CW ≥ 0.1 | CW `:ERROR`（无持仓） | **未触发** —— 不是「权重集中」，是「没有权重」 |
| ② 机制方向（S<0 且 reverse ≈ +\|S\|） | 双臂同为 0 | **未触发** —— 零对零判不出方向 |
| ③ `max\|S\| < 0.5` 且 `max\|2Y\| < 0.8` | 0.00 / 0（`:ERROR`） | **数值上触发**，但成因不是预想的「0/1 哑变量截面信息量不足」，而是**恒空仓** |
| ④ 任一年 `longCount = 0` ⇒ 整集出局 | **10/10 年全为 0** | ✅ **触发 ⇒ 判死** |

**失败机制（按 ④ 硬判，不补参数、不发 215b）**：`mcr63_membership` 的 description 是
「Indicates the membership status of stocks in the **WisdomTree WTIDJH Index**」——
一条**日本红利指数**的成分标记。它在 KOR/TOP600 的 `coverage` 元数据仍报 **1.0**
（平台 `get_datafields(KOR, macro63, TOP600, delay=1, filter_sharpe=false)` 实测
`coverage:1 / userCount:81 / alphaCount:192 / complete:true`），但那是「**字段有定义**」而不是
「**韩国有非零值**」：韩国标的恒为非成分 ⇒ 标记恒 0 ⇒ `ts_delta` 恒 0 ⇒ 截面零离散 ⇒
中性化后全 0 ⇒ 空账。侧证：同一查询换 `JPN/TOP1600` 返回 `count:0`（本季该字段连 JPN 数据集表里都没有）
⇒ **没有任何区域能给出这份 0/1 的截面差异**。

⇒ **`macro63` 判死（结构性，非参数问题）**：`KOR-MACRO63-NO-CROSS-SECTION`。
macro 塔（`KOR/D1/MACRO`，乘数 1.4）只有 `other106`（wave 190 实测 max\|S\|=0.75）与本集两个数据集，
两者皆死 ⇒ **macro 塔关闭，不再开波**。

⚠ **本波最大教训**：**平台的 `coverage` 元数据 ≠「本区有截面差异」**。`coverage=1` 只说「100% 标的行有覆盖」，
不说非零率 / 离散度。事前应加两条判据：① description 里的**标的物归属**先查（指数名 / 机构名 / 国家名）；
② 0/1 类字段**先用 1 条最小探针确认 `longCount > 0`**，再谈机制与平滑。
⚠ 另：**`ts_backfill` 修不了这一条** —— pipeline 打印的 `sparse_field_long_window_v1` 明写
「ts_backfill 不支持事件型输入」，且本集的空账源于**取值全同**而非 NaN 缺口，回填只会把 0 填成 0。
