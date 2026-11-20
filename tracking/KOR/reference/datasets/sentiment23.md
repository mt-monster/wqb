# sentiment23 — Textual Sentiment Analysis Data（KOR / TOP600 / D1）

> 画像：2026-11-17 · `get_datafields(dataset_id=sentiment23, region=KOR, universe=TOP600, delay=1, filter_sharpe=false, sort_by=dateCreated)`，
> 全 156 字段（无抽样，本轮分页返回至 50KB 截断但 count=156；Fields 家族结构完整）。
> 归属：平台 `category=sentiment`（KOR D1 **未点亮塔 0/3**、倍率 1.6）。
> 命名规则：`tracking/KOR/reference/datasets/<platform dataset_id>.md`（每集一份，手工维护）。

## 1. 数据集体征

| 项 | 值 |
|---|---|
| 字段数 / 类型 | **156 / 156 全 MATRIX** |
| coverage | 0.255（2/3/4/5 变体与 neg/neut/pos 族）/ 0.285（dts 时序 + 无前缀数字后缀族）——**极稀疏** |
| dateCreated | 主体 2024-07-01、无后缀统计族 2025-11-01 |
| aC | **多数字段 0–5，最高 ≤5** ⇒ 极冷门（prod 白空间必要条件，非充分）|
| 经济轴 | 新闻标题 transformer 情绪 **分布**：pos/neg/neut 三态 × 统计量（conf_up/conf_low 置信区间、mean/median/std/max/min 离散、dts 时序）× 5 变体（variant 2/3/4/5 + 无前缀）|

## 2. 字段家族（按 description，非字段名）

### 族 A — 置信区间宽度（分歧度代理，机制核心）
`snt23_{2,3,4,5}?{neg,neut,pos}_conf_up` / `_conf_low` = 95% CI 上下界（may fall outside 0–1）。
**conf_up − conf_low = 情绪评判分歧度**，与 Diether (2002) 预测 dispersion 同源。
⚠ variant 3（USA next-day）、4/5（AMR D0）是**跨区变体**——KOR 优先用无前缀的数字后缀族与 variant 2（D1 同日），但需 preflight 验存在性。

### 族 B — 分布二阶矩（离散度）
`_std`（story 间情绪标准差）、`_max`/`_min`（极值跨度）⇒ 同一信息源的不同分歧度量。

### 族 C — 一阶矩（水平/中心）
`_mean` / `_median` / dts_gen（general sentiment score）/ dts_sop / dts_tuen（时序情绪值）⇒ 情绪方向水平。

### 族 D — 编码字段
无（全为数值统计）。

⚠ **名 vs description 差异**：带数字后缀的族（`snt23neg_conf_up_83` 等）description 只有 "Confidence level of sentiment"，
而 `snt23_2neg_conf_up` 明写 "Upper bound of 95% CI..." ⇒ **必须读 description 才还原 CI 语义**，按名前缀会误判。

## 3. 头部字段质量先验（铁律 0.1）

无前缀族 aC 最高仅 1–5（`snt23_max` aC1、`snt23_neut_min` aC1、`snt23_5pos_conf_up` aC3、`snt23_5dts_gen` aC4），
`nws` 系情绪族在 KOR 历史 aC 也低 ⇒ 头部轴 = **整体情绪水平/分歧，无单字段强轴**。方向：以机制（分歧度）而非头部字段定形态。

## 4. 机制与论文锚（铁律 H 双通道）

- **通道 B（成功）Diether, Malloy & Scherbina (2002, JF)** + Miller (1977)：
  预测分歧度高的股票未来收益低（Q1−Q5 = 9.48%/yr, t>3）；卖空约束下悲观观点被压制→价格由乐观者定→高估→信息事件后回归。
  **KOR 适用性**：KOR 有真实卖空禁令史（2020-03→2021-05、2023-11→2025-03）；文献样本 USA ⇒ 只作假说、本区实测。
  补充：Asquith/Pathak/Ritter 2005 + Boehme 2006（分歧效应集中在卖空约束强的股票）；Stambaugh/Yu/Yuan 2012（高情绪期更强）。
- **通道 A（论坛）**：`search_forum_posts("text sentiment confidence interval disagreement stock returns reversal")` 30s 超时
  ⇒ 工具故障 ≠ 论坛无解（[[forum-paper-evidence-gate]]：不落 forum_recon_negative_*），已记录、不阻塞组装。

**可证伪方向句**：情绪分歧度（conf_up − conf_low / std 高）⇒ 后续收益低（做空高分歧），持有 22–66 交易日；
卖空约束下高估需信息事件修正 ⇒ 门控事件（dts 变化）可能增强。

## 5. 预处理决策（五问 → 算子）

| 问 | 读数 | 决策 |
|---|---|---|
| 时间维度 | CI 宽度 / std = 存量分歧度（截面）；dts = 时序 | 存量 ⇒ `group_rank` 截面排序；dts 变化 ⇒ `ts_delta` |
| 相对性 | CI 上下界有量纲（0–1 外）⇒ 须做差 | `subtract(conf_up, conf_low)` 成正分歧度，再 `group_rank`/`group_zscore` |
| 中心趋势 | 情绪分 0–1 有界 | 水平可用，但主流机制是分歧（二阶矩）|
| 覆盖 | cov 0.255–0.285 < 0.4 | **必须 `ts_backfill(F, 250)` 前置**，并 trade_when 门控可选 |
| 事件性 | 新闻驱动稀疏 | 非事件期可持仓（存量分歧度持续），不强制 trade_when |

⚠ **VECTOR 不在此集**（全 MATRIX），无 vec_* 需求。
⚠ **近十年**：2024-07 / 2025-11 onboard（与 A 通道 2023 逻辑冲突——须 wave 后 `get_alpha_yearly_stats` 逐年核，若 2014–2020 空窗则数据层排除，不硬凑）。

## 6. 已试记录

### W1 · 分歧度探针（批次 `2HZsuL9Hm50m8Qyf5lX5Wjm`，2026-11-17，STATISTICAL/d2，8 条）

**三问**：继承=Diether (2002) 分歧度论（高分歧→低收益，Miller 卖空约束高估）；
准入=只用本集字段实名核对通过的 9 个字段（剔除跨平台不存在的 `snt23pos_conf_up_83`），cov 0.255 全 `ts_backfill(250)` 前置，正反双向（铁律 B），分组轴 sector/industry/subindustry 三档（D4）；
收窄=8 条探针，4 族（CI 宽度 / std / 水平 / dts）。

| # | 机制 | 字段 | 方向 |
|---|---|---|---|
| 1 | CI 宽度(pos) | conf_up−conf_low | 反向(做空高分歧) |
| 2 | CI 宽度(pos) | conf_up−conf_low | 正向(对照) |
| 3 | CI 宽度(neg) | conf_up−conf_low | 反向 |
| 4 | std(pos) | pos_std | 反向 |
| 5 | std(neg) | neg_std | 反向(industry) |
| 6 | 水平(pos) | pos_mean | 正向(subindustry) |
| 7 | std(neg无后缀) | neg_std | 反向(subindustry) |
| 8 | dts 时序 | 5dts_gen | 反向 |

**读数（2026-11-17 收批，批次 `2HZsuL9Hm50m8Qyf5lX5Wjm`，8/8 COMPLETE）— 8/8 REJECT**：

| # | 机制 | alpha | S | 2Y | TO | fRA |
|---|---|---|---:|---:|---:|---:|
| 1 | CI宽度(pos)反向 | `6XMEw7qY` | 0.03 | −0.10 | 0.099 | 3 |
| 2 | CI宽度(pos)正向 | `N1POp0j7` | −0.23 | −0.22 | 0.099 | 5 |
| 3 | CI宽度(neg)反向 | `npaWg9za` | −0.18 | 0.17 | 0.107 | 4 |
| 4 | std(pos)反向 | `A1x3w9aX` | 0.02 | −0.09 | 0.100 | 3 |
| 5 | std(neg)反向 | `1YWg7enQ` | −0.20 | −0.04 | 0.108 | 4 |
| 6 | 水平(pos)正向 | `KPgLb3w8` | −0.61 | −1.47 | 0.108 | 5 |
| 7 | std(neg)反向/subind | `YPaAp6Wv` | −0.07 | −0.45 | 0.112 | 4 |
| 8 | dts时序反向 | `GrmowP3Q` | −0.04 | −0.27 | 0.100 | 3 |

**归因（先归因再推进）**：CI 宽度分歧度正反两向都≈0（6XMEw7qY 0.03 / N1POp0j7 −0.23）
⇒ **不是方向错，是分歧度轴本身在 KOR 无截面定价力**（Diether 2002 在此集不成立）。
std 离散度族全 −0.20…0.02，水平 pos_mean 最强也 −0.61。8 条 fRA 3–5（信号层死，非 prod 墙）。
**近十年问题未触发**：无需查逐年（无正信号可谈定价力）。sentiment23 判 PROVISIONAL 信号层死，不再开波。

（imbalance5 的辅助验证读数见 `tracking/KOR/reference/datasets/imbalance5.md` §8，不在此档案重复。）

### W2 · 极值/偏度/动量新族（批次 `3zcl7gcnu4uB9qm1fYGdobNZ`，5 条）— ⚠ 平台侧未完成

5 条：pos/neg 的 max−min 极值跨度、median−mean 偏度、pos_mean/neg_mean 的 22 日情绪动量。
**状态**：派发后 `progress=0.1` 持续 >12 分钟无错误、无 child（区别于正常的 0.35 排队指纹），
重认证后仍 0.1 ⇒ 平台侧该批次未完成。**按纪律不重复派发、不用未完成的读数做判定依据**。
不影响本集结论：W1 的 8 条已正反双向证明分歧度/离散度/水平轴在 KOR 无定价力（fRA 3–5），
W2 的极值/偏度/动量是同族一阶/二阶矩变体，§7.6 D2/D3 已由 W1 覆盖其机制族。
本集维持 PROVISIONAL 信号层死，不再开波。
