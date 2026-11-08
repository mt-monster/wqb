# waves · KOR × INSIDERS × ATOM

> 设置档基线：KOR / TOP600 / D1 / **REVERSION_AND_MOMENTUM** / decay 4 / trunc 0.08 / unit VERIFY / nanH OFF / maxTrade OFF
> 并发纪律：`create_multi_simulation` 同时最多 **2 批在飞**（用户约束 5）
> 反过拟合纪律：**无归因不得发下一波**；每波候选数 ≤ 上一波 1/3；已死轴禁入

## 已死轴清单（命中即禁入配额）

| 死轴 | 证据 |
|---|---|
| 库藏股族（D 族全部） | wave290 8 模板 max\|S\|=0.88、max\|2Y\|=0.70 |
| `tnc` 水平作主信号 | S 1.51 但 2Y 0.08（2Y 结构不可达） |
| `real_ratio` Δ55 | S −0.07（wave290） |
| `truncation` 扫描 | KOR 多档 returns 逐位相同（区级锁定项） |
| `universe` 扫描 | KOR 唯一合法档 TOP600 |
| 同族第 4 颗 | 论坛实证：同族 2–3 颗后同步闸拦截（自相关 0.27→0.9987） |

## Wave 1（分歧度跨字段 + 新机制族，14 条 / 2 批）

**波次三问**
1. **继承**：wave290 实证「`ts_mean(vec_stddev(F),55)` 的负向臂在 `ghc_tr`/`vol_chg` 上出 1.62/1.76 全闸」⇒ 本波把它扩到其余 6 个交易/持仓字段（同机制、换腿）。
2. **准入**：禁碰库藏股族、禁用 `tnc` 水平、禁 `real_ratio` Δ 轴、禁第 4 颗同构变体。
3. **收窄**：wave290 的 8 条模板扫 → 本波 14 条但**只在一个已证机制上换字段**（8 条）+ **6 个未触碰的新几何**（B 批），无重复轴。

### 批 A · 分歧度族跨字段（8 条）— multisim `3WLLNk6aI4ri9PGq79CNLm7`
统一形态（对应 ②.b「zero_inflated / 事件稀疏 ⇒ 先聚合后排序」，且方向取 Miller 分歧-高估的负向臂）：

```text
subtract(0.5, group_rank(ts_mean(vec_stddev(<F>), 55), sector))
```

| # | F（字段） | 机制面 | 备注 |
|---|---|---|---|
| A1 | `insd5_trd_amt` | 交易**金额**分歧 | 金额腿未测过 |
| A2 | `insd5_fa_tr` | 交易后持股比例分歧 | 结构+流量交叉 |
| A3 | `insd5_fb_tr` | 交易前持股比例分歧 | 与 A2 同族不同时点 |
| A4 | `insd5_vol_bf` | 交易前持股规模分歧 | 规模轴 |
| A5 | `insd5_vol_af` | 交易后持股规模分歧 | 与 A4 同族 |
| A6 | `insd5_ratio` | 去重持股比例分歧 | 存量结构分散度 |
| A7 | `insd5_source_ratio` | 源持股比例分歧 | 与 A6 不同口径 |
| A8 | `insd5_unt_val` | **成交价**分歧 | aC 45，全场最白 |

### 批 B · 新机制族（6 条）— multisim `3ZmCujcRM5h097A155KMq1Nb`

| # | 模板 | 表达式 | 机制 / 来源 |
|---|---|---|---|
| B1 | 净增持流量比 | `group_rank(ts_mean(divide(vec_sum(insd5_vol_chg), add(vec_sum(insd5_vol_bf), 1)), 66), sector)` | M2；论坛帖「比值 > 计数」 |
| B2 | 单位持股交易额 | `subtract(0.5, group_rank(ts_mean(divide(vec_sum(insd5_trd_amt), add(vec_sum(insd5_source_data), 1)), 66), sector))` | M2 强度标准化（去规模） |
| B3 | 增持加速度 | `subtract(0.5, group_rank(ts_delta(ts_sum(vec_avg(insd5_ghc_tr), 22), 66), sector))` | M2 二阶（修正加速度） |
| B4 | 最大单笔变动 | `subtract(0.5, group_rank(ts_mean(vec_max(insd5_ghc_tr), 66), sector))` | M1 极值聚合（vs 均值/方差） |
| B5 | 自身常态偏离 | `subtract(0.5, group_rank(ts_zscore(vec_sum(insd5_ghc_tr), 252), sector))` | M2 异常增持（vs 自身一年常态）※ 原「方向一致度」因 `abs(VECTOR)` 有整批连坐风险而替换 |
| B6 | 变异系数 | `subtract(0.5, group_rank(ts_mean(divide(vec_stddev(insd5_ghc_tr), add(abs(vec_avg(insd5_ghc_tr)), 0.01)), 55), sector))` | M1 归一化分歧（分歧/方向） |


## Wave 2（预置设计，待 Wave1 读数确定具体字段）

> 铁律 G：本波候选数 ≤ Wave1 的 1/3（Wave1 14 条 ⇒ 本波 ≤5 条），且只在 Wave1 优胜集合内变动。

**待填的优先级队列（按 Wave1 读数取前 2 名字段 X / 机制 Y）**

| 序 | 模板 | 表达式（占位） | 目的 |
|---|---|---|---|
| C1 | T11 P-ATOM-1 壳 | `ts_target_tvr_decay(signed_power(group_rank(winsorize(rank(ts_backfill(<X>, 40)), std=0.24), sector), 3.5), target_tvr=0.22)` | 给裸式加壳，冲 S 1.58 |
| C2 | T10 倒数 + 壳 | `ts_target_tvr_decay(signed_power(group_rank(winsorize(rank(ts_backfill(divide(1, add(vec_avg(insd5_source_ratio), 0.01)), 5)), std=0.24), sector), 3.5), target_tvr=0.22)` | 集中度族从 1.43 冲 1.58 |
| C3 | T12 高管门控 | `trade_when(greater(vec_avg(insd5_officer), 0.5), <T01 最优>, -1)` | 高管子集是否更强（M4） |
| C4 | 中性化档 | 对最优结构扫 `STATISTICAL / CROWDING / SLOW` | 中性化是 KOR 第一杠杆（论坛实证差 3 倍） |
| C5 | 内层平滑 | 对 2Y 不足者加 `ts_mean(信号, 5)` | 2Y 闸专用杠杆（实证 0.34→1.68） |

**禁止**：库藏股族、`tnc` 水平、`real_ratio` Δ、同一模板第 4 个变体。

---

## Wave 1 归因（2026-11-06 收割，14/14）

### 读数

| 批 | # | F / 模板 | S | F | TO | 判定 |
|---|---|---|---:|---:|---:|---|
| A | A1 | trd_amt 分歧 | 0.84 | 0.51 | .096 | 弱 |
| A | A2 | fa_tr 分歧 | 1.54 | 1.31 | .097 | 近线 |
| A | A3 | fb_tr 分歧 | 1.26 | 0.96 | .097 | 可用 |
| A | A4 | vol_bf 分歧 | 1.38 | 1.06 | .094 | 可用 |
| A | A5 | vol_af 分歧 | **1.57** | 1.30 | .094 | 单闸差 0.01 |
| A | A6 | ratio 分歧 | −0.32 | −0.12 | .051 | **死** |
| A | A7 | source_ratio 分歧 | 0.36 | 0.14 | .051 | **死** |
| A | A8 | unt_val 分歧 | −0.51 | −0.25 | .098 | **死** |
| B | B1 | 净增持流量比 | 0.21 | 0.06 | .077 | 死 |
| B | B2 | 单位持股交易额 | 0.13 | 0.03 | .080 | 死 |
| B | B3 | 增持加速度 | 0.37 | 0.13 | .242 | 死 |
| B | B4 | 极值聚合 vec_max | 0.69 | 0.37 | .079 | 死 |
| B | B5 | ts_zscore 252 | −0.15 | −0.02 | **1.54** | 死 + 换手爆炸 |
| B | B6 | 变异系数 | 0.88 | 0.56 | .095 | 死 |

### 归因三条

1. **M1 分歧度只吃「绝对量字段」**。绝对量：vol_chg 1.76 / ghc_tr 1.62 / vol_af 1.57 / fa_tr 1.54 / vol_bf 1.38 / fb_tr 1.26 全部 >1.2；比率类：ratio −0.32 / source_ratio 0.36 / unt_val −0.51 **全灭**。
   **机理**：比率字段已被归一化，其截面离散度混入分母噪声（分母小的股票 stddev 被放大）；只有绝对量字段的 `vec_stddev` 才是「内部人观点分歧」的干净代理。
2. **批 B 六个替代机制全部失败（0.13–0.88）** ⇒ 「在 `ghc_tr` 上换聚合算子」不是新机制；M2 单字段族的表达空间已基本穷尽，**禁再刷 ghc_tr 的均值/极值/zscore 变体**。
3. **互相关墙**：6 颗 M1 候选（含存量 2 颗）两两 0.64–0.90；`max_mutually_below_subset_size = 2`（WjO32EPG × kqNv1xRk = **0.6536**）。
   ⇒ 换字段 ≠ 换机制；整条 M1 轴最多贡献 **2 颗**可提交件。

### 单闸读数（WjO32EPG）

`failed_ra_count=1`，唯一失败 **LOW_SHARPE 1.57 / 1.58**；其余全过（2Y **2.59**、fitness 1.30、subU 1.17、TO .0941）。
且与 kqNv1xRk 互相关 .6536 < .7 ⇒ **一旦过线即得第 2 颗可提交件**，是当前最便宜的推进点。

## Wave 2（2026-11-06 派发，5 条 / 2 批）

**准入**：Wave1 已死轴（比率类分歧、批 B 六机制）禁入；库藏股族 / `tnc` 水平 / `real_ratio` Δ 继续禁用。

| 批 | multisim | # | 模板 | 表达式 | 机制 |
|---|---|---|---|---|---|
| 1 | `13pIsZVf55Ga0DXi5NnctP` | N1 | 交易**广度** | `group_rank(ts_mean(vec_count(insd5_ghc_tr), 55), sector)` | 多少内部人在动（vs 动多大） |
| 1 | 同上 | N2 | 买卖**不对称** | `group_rank(ts_mean(divide(vec_max(insd5_ghc_tr), add(abs(vec_min(insd5_ghc_tr)), 0.01)), 55), sector)` | 最大增持 / 最大减持（Lakonishok-Lee 买入腿更强；论坛 43467688159511 不对称性） |
| 1 | 同上 | P1 | 优胜腿换分组轴 | `subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_vol_af), 55), industry))` | vol_af 1.57 → 更细分组轴冲 1.58 |
| 2 | `4CLk76cl94WObEm11NYEYiAZ` | N3 | 单笔**主导度** | `group_rank(ts_mean(divide(vec_max(insd5_trd_amt), add(vec_sum(insd5_trd_amt), 1)), 55), sector)` | 交易被单一内部人主导 = 伪分歧（M1 失效条件①） |
| 2 | 同上 | P3 | **高管门控** | `trade_when(greater(vec_avg(insd5_officer), 0.5), <vol_af 原式>, -1)` | M4：高管子集信息含量更高（Cohen-Malloy-Pomorski 2012） |

### Wave 2 部分读数（2026-11-06）

| # | 模板 | id | S | F | TO | 判定 |
|---|---|---|---:|---:|---:|---|
| N3 | 单笔主导度（max/sum） | `2rA9YE3Z` | **0.14** | 0.03 | .095 | ⛔ **死** |
| P3 | 高管门控（officer>0.5） | `zq3gValO` | **1.09** | 0.71 | .064 | ⛔ **比裸式 1.57 更差** |

**归因**：
1. **「单笔主导 = 伪分歧」假设被证伪**（S 0.14）。交易被单一内部人主导这个结构**与后续收益无关** ⇒ 分歧度信号不是被单笔大额交易污染的；M1 失效条件①在本区不成立。
2. **M4「高管门控」假说被否**（1.57 → 1.09）。门控后信号反而掉 0.48 S。
   **机理**：`officer>0.5` 把 cov .7318 的交易样本再切掉一大块（高管交易占比有限），样本稀疏 → 截面读数噪声化；同时 `trade_when` 的 -1 分支引入空仓，持仓数从 321 掉到更低，收益基础被削弱。
   ⇒ **禁止再用 officer 做门控轴**；E 族分类字段在本区对 M1 无增益。

## Wave 3（2026-11-06 派发，3 条 / 1 批）— 中性化档 A/B

**依据**：risk70 战役实证「中性化档是本塔第一杠杆」，且同一结构在 `CROWDING` 下比 `INDUSTRY` 高 +0.17 S；KOR 合法 11 档已核。本批**只动设置、不动表达式**，与 Wave1/2 的 R&M 基线做同结构对照。

**multisim**：`2FH7Ng61t4ZqaOY15M4j4JK8`（CROWDING / decay 4 / trunc 0.08）

**读数（CROWDING，3/3 COMPLETE）**：

| 结构 | R&M 基线 | CROWDING | Δ S |
|---|---:|---:|---:|
| M1 vol_af（`YP18RNmq`） | 1.57 | **1.39** | **−0.18** |
| M1 fa_tr（`d5WYNnmK`） | 1.54 | **1.24** | **−0.30** |
| M3 source_ratio/tnc（`MPYdJb8o`） | 1.50 | **1.30** | **−0.20** |

**归因（重要，与 risk70 相反）**：`CROWDING` 对 insiders5 **全面减分**，不是加分。
risk70 战役里 CROWDING 相对 INDUSTRY 是 +0.17，但那是「载荷类信号被统计因子剥离」的场景；
内部人交易分歧度带的是**特质信息**，CROWDING 剥离拥挤暴露时把信号本身也削掉了。
⇒ **中性化档效应是数据集/机制相关的，不可跨数据集外推**。insiders5 的最优档仍是 `REVERSION_AND_MOMENTUM`。
⇒ CROWDING / STATISTICAL 档在本数据集判死。

| # | 结构 | 表达式 | R&M 基线 |
|---|---|---|---|
| C1 | M1 vol_af 分歧 | `subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_vol_af), 55), sector))` | 1.57（差 0.01 过线） |
| C2 | M1 fa_tr 分歧 | `subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_fa_tr), 55), sector))` | 1.54 |
| C3 | M3 集中度/关系方数 | `subtract(0.5, group_rank(divide(vec_avg(insd5_source_ratio), add(vec_avg(insd5_tnc), 1)), sector))` | 1.50 |

### Wave 2 全部读数（5/5，2026-11-06）

| # | 模板 | id | S | F | TO | vs 基线 | 判定 |
|---|---|---|---:|---:|---:|---|---|
| N1 | 交易广度 vec_count | `d5WYNgVX` | **−0.27** | −0.09 | .089 | — | ⛔ 死 |
| N2 | 买卖不对称 max/\|min\| | `vR1ZWxMz` | **−0.50** | −0.23 | .091 | — | ⛔ 死（反向 +0.50 也不够） |
| N3 | 单笔主导度 max/sum | `2rA9YE3Z` | **0.14** | 0.03 | .095 | — | ⛔ 死 |
| P1 | 分组轴 industry | `88RVM79v` | **1.47** | 1.16 | .105 | 1.57（sector） | ⛔ **更差** |
| P3 | 高管门控 officer | `zq3gValO` | **1.09** | 0.71 | .064 | 1.57 | ⛔ **更差** |

**Wave 2 总结论（关键）**：**M1 分歧度是窄口径的「量级分歧」效应**，最优形态锁定 =
`subtract(0.5, group_rank(ts_mean(vec_stddev(<绝对量字段>), ~55), sector))`。
所有结构性变体全部无效：
- 换**矩**（广度=0 阶计数、不对称=极值比、集中=极值占和）→ 全灭 ⇒ 被定价的不是"多少人动/谁主导"，而是**变动幅度的截面离散度**本身。
- 换**分组轴**（industry 更细）→ 1.57→1.47 ⇒ sector 已是最优粒度（更细切分让组内样本不足）。
- 加**门控**（高管子集）→ 1.09 ⇒ 子集稀疏即噪声化，M4 假说否。

⇒ **剩余唯一可动杠杆 = 设置档（中性化 / decay）**，已在 Wave 3 验证中。
⇒ 禁再刷：vec_count / vec_max / vec_min / trade_when 门控 / industry 分组轴 用于 M1。




## Wave 5 · W=5（周窗）4/4 全灭（2026-11-06 收割）

multisim 4dkNAEf0s4YC9eDtcQXmvW

| # | 字段@5 | id | S | F | TO | 2Y | subU | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | vol_af | A1Vr1OvY | 1.00 | 0.45 | .5578 | 0.95 | 0.93 | LOW_SHARPE / LOW_FITNESS / CONCENTRATED_WEIGHT / LOW_2Y |
| 2 | vol_chg | 3qokqnVX | 0.79 | 0.32 | .5573 | 0.89 | 0.70 | 同上 4 闸 |
| 3 | ghc_tr | leA5eRKn | 0.54 | 0.18 | .5534 | 0.20 | 0.39 | 同上 4 闸 |
| 4 | vol_bf | O0AM05Jp | 0.75 | 0.29 | .5588 | 0.23 | 0.72 | 同上 4 闸 |

**归因（窗口下界被锁死）**：
1. **事件密度决定 W 下界**。insiders5 交易组 cov .7318，且是申报日频稀疏事件 —— 覆盖股票平均约每 5 个交易日 1 笔申报。W=5 时窗内事件数 <2，vec_stddev 落在单点或空集上 ⇒ 读数退化为噪声。
2. **换手同步爆炸**：S 从 1.75 掉到 1.00 的同时 TO 从 .1723 涨到 .5578（3.2 倍）。机理：短窗使 ts_mean 失去平滑作用，信号每天跟着最新一笔申报翻转 ⇒ 噪声交易。TO > .5 直接触发 CONCENTRATED_WEIGHT。
3. ⇒ **W=5 在本数据集判死**（不只弱，是结构性不可用）。有效窗口下界 = 22（月度），与 ts_mean 需覆盖 ≥4 周申报事件的机制要求一致。
4. 副产物：ghc_tr@5 的 S 0.54 是六字段里最差，与 @55 的 1.62 反差最大 ⇒ ghc_tr 的信号完全依赖长窗摊平（它本身是比例变动，单笔方差极大）。

## Wave 6 · 新机制批（2026-11-06 派发，5 条）

**背景**：窗口矩阵被证明只能产出有限颗（W=5 死、W=66 衰减、W=55 与 W=22 各有所长），要凑 10 颗必须开结构互异的新机制轴。本批全部预检通过（preflight_expressions valid=true，含日期算术与 group_std_dev）。

| # | 机制 | 表达式 | 算子数 | 经济依据 |
|---|---|---|---:|---|
| V1 | M6 交易新鲜度 | subtract(0.5, group_rank(vec_avg(insd5_recent_dt), sector)) | 3 | 距最近一次内部人变动的时长 = 信息陈旧度；陈旧 = 老信号已定价完 ⇒ 后续弱 |
| V2 | M6b 持仓更新新鲜度 | subtract(0.5, group_rank(vec_avg(insd5_source_recent_dt), sector)) | 3 | 同上，用源持仓口径（aC 272 vs 127，不同披露链条） |
| V3 | M7 分歧度时序分位 | subtract(0.5, group_rank(ts_rank(ts_mean(vec_stddev(insd5_vol_chg), 22), 252), sector)) | 5 | 分歧度相对自身一年历史的分位 ⇒ 剔掉公司规模/行业基数，纯「异常分歧」 |
| V4 | M8 分歧度变化 | subtract(0.5, group_rank(ts_delta(ts_mean(vec_stddev(insd5_vol_chg), 22), 22), sector)) | 5 | Miller 讲水平，但分歧冲击（半衰期约 1 年）可能才是被定价的部分 |
| V5 | M5 披露滞后 | group_rank(ts_mean(subtract(vec_avg(insd5_td_ctn), vec_avg(insd5_history_td_drt)), 22), sector) | 5 | 公告日 − 成交日 = DART 披露延迟；滞后长 ⇒ 治理弱/信息不对称高 |

> 日历注记：YYYYMMDD 数值与真实日期同序，故 group_rank/ts_rank 上的横截面比较有效；但差值跨月不线性（如 20231203−20231128=75 而非 5），故 V5 只作探针，不作机制定论依据。

multisim：m4streS44sJbT6LD99Boe7

## 存量盘点修正（2026-11-06）

- **RRE9nkVj（vol_chg@55，S 1.76）已 404 —— 该 alpha 在平台上不存在了**，不得计入交付数。
- KOR 最新 100 条扫描：**insiders5 仅 A1VrRe7W 一颗 failed_ra_count=0**；kqNv1xRk（ghc_tr@55，S 1.62）翻到 100 条之外，仍有效。
- 近闸三颗（ra=1，全部只差 LOW_SHARPE）：

| id | 结构 | S | 2Y | F | 差多少 |
|---|---|---:|---:|---:|---|
| WjO32EPG | vol_af@55 | 1.57 | 2.59 | 1.30 | −0.01 |
| 9qx8OzXe | fa_tr@55 | 1.54 | 2.17 | 1.31 | −0.04 |
| e75VlNx6 | fa_tr@22 | 1.50 | 1.95 | 1.20 | −0.08 |

- **KOR/INSIDERS 数据集全集只有 2 个**：insiders5（53 字段 / cov .8918 / aC 5027）与 insiders1（9 字段 / cov .3526 / aC 549 / valueScore 3）。
  insiders1 全 VECTOR，且无方向字段（sign 不可得）；可用轴：insd1_tradesignificance（1–3 显著性评分，aC 40，极白）、insd1_shares / insd1_value / insd1_valueeur / insd1_holdings（绝对量，可套 M1 分歧度）、max_trade_price（aC 5，最白）。⇒ 备用数据集确实存在，M1 几何可迁移。

## Wave 4b · W=22 四字段（2026-11-06 收割，2/4 全闸）

multisim 1Me8heeZQ5hSauB1fXvfrOHM

| # | 结构 | id | S | F | TO | 2Y | ra | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | vol_chg@22 | 3qokqkZQ | **1.90** | 1.72 | .1731 | **2.59** | **0** | ✅ **全闸，本战役最高** |
| 2 | ghc_tr@22 | P0oY0YdE | **1.67** | 1.48 | .1735 | 2.10 | **0** | ✅ 全闸 |
| 3 | vol_bf@22 | kqNWqW2K | 1.34 | 0.98 | .1729 | 1.48 | 3 | ⛔ SHARPE/FITNESS/2Y |
| 4 | fb_tr@22 | zq32q21d | 1.09 | 0.74 | .1740 | 1.16 | 3 | ⛔ 同上 |

### 归因（W=22 的收益是「分字段」的，不是普遍升窗）

把六个绝对量字段在两个窗口上的读数排开，规律非常干净：

| 字段 | 语义 | aC | @5 | @22 | @55 | @66 | 22−55 |
|---|---|---:|---:|---:|---:|---:|---:|
| vol_chg | 股数变动（有符号） | 126 | 0.79 | **1.90** | 1.76 | — | **+0.14** |
| ghc_tr | 持股比例变动（有符号） | 220 | 0.54 | **1.67** | 1.62 | — | **+0.05** |
| vol_af | 交易后持股数 | 75 | 1.00 | **1.75** | 1.57 | 1.32 | **+0.18** |
| fa_tr | 交易后持股比例 | 132 | — | 1.50 | 1.54 | 1.37 | −0.04 |
| vol_bf | 交易前持股数 | 95 | 0.75 | 1.34 | 1.38 | — | −0.04 |
| fb_tr | 交易前持股比例 | 76 | — | 1.09 | 1.26 | — | −0.17 |

1. **收 22 窗红利的三种字段 = 变动量(vol_chg, ghc_tr) + 交易后量(vol_af)。** 三者共性是「**包含当期交易造成的位移**」——22 窗保留最新一笔申报的权重更高，正是 M1 想捕捉的边际分歧。
2. **交易前存量(vol_bf, fb_tr)与比例存量(fa_tr)收不到红利，甚至倒退。** 机理：交易前持股与当期交易无关（是历史存量），短窗只是减少样本量 ⇒ 噪声上升。fb_tr 22−55 = −0.17 是最直接的证据。
3. **@55 的非规范窗口可以退役**：vol_chg/ghc_tr/vol_af 在 22 上都比 55 高，且 22 属用户规范窗（月度）。此前保留 55 只是因为它是 wave290 的继承值。
4. ⇒ **M1 的有效定义域锁定为**：字段 ∈ {vol_chg, ghc_tr, vol_af}（+ 边界 fa_tr 1.50–1.54），窗口 = **22**，分组轴 sector，中性化 R&M，不回填。
5. TO 同步从 .098（@55）升到 .173（@22），仍远低于 .7 上限，未触发任何换手闸。

## Wave 7 · 几何救援批（2026-11-06 派发，5 条）

**目的**：把近闸三颗（1.57 / 1.54 / 1.50）抬过 1.58，同时产出与 M1 水平式低相关的新几何。全部在 W=22 / decay 4 / R&M 下（设置不变，只换几何）。

| # | 几何 | 表达式 | 算子数 |
|---|---|---|---:|
| G1 | 内层 rank（先截面分位再时序平均） | subtract(0.5, group_rank(ts_mean(rank(vec_stddev(insd5_vol_af)), 22), sector)) | 5 |
| G2 | 同上 · fa_tr | subtract(0.5, group_rank(ts_mean(rank(vec_stddev(insd5_fa_tr)), 22), sector)) | 5 |
| G3 | 内层倒数（压高端、拉低端） | subtract(0.5, group_rank(ts_mean(divide(1, add(vec_stddev(insd5_vol_af), 1000)), 22), sector)) | 7 |
| G4 | 同上 · fa_tr | subtract(0.5, group_rank(ts_mean(divide(1, add(vec_stddev(insd5_fa_tr), 0.1)), 22), sector)) | 7 |
| G5 | 双尺度偏离（短分歧 − 长分歧） | subtract(0.5, group_rank(subtract(ts_mean(vec_stddev(insd5_vol_chg), 22), ts_mean(vec_stddev(insd5_vol_chg), 66)), sector)) | 6 |

> 机制依据：G1/G2 把「平均分歧」换成「分歧的平均分位」，剔掉公司规模基数；G3/G4 用单调非线性改变 rank 后的截面间距（历史实证：同向臂 +0.19 S 且换窗变体的相关性明显更低）；G5 抓 Miller 理论里真正被定价的「分歧冲击」而非分歧水平。

multisim：XZswv7Yg4Lg8QaP17LU0jq

### Wave 6 全部读数（5/5，2026-11-06 收割）

| # | 机制 | id | S | F | TO | 2Y | ra | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| V1 | M6 交易新鲜度 recent_dt | j2YPzzXE | 0.29 | 0.09 | .1396 | −0.03 | 4 | ⛔ 死 |
| V2 | M6b 持仓更新新鲜度 source_recent_dt | A1VrjjbY | 0.93 | 0.56 | .1333 | 0.22 | 4 | ⛔ 死 |
| V3 | M7 分歧度时序分位 ts_rank252 | O0AMQQkp | 0.89 | 0.50 | .1909 | **2.06** | 2 | ⛔ 死（2Y 却 2.06） |
| V4 | M8 分歧度变化 ts_delta | Vkxm11E0 | **0.09** | 0.02 | **.2700** | 0.10 | 5 | ⛔ 最差 |
| V5 | M5 披露滞后 td_ctn − history_td_drt | JjeWMMm2 | 0.52 | 0.22 | .1805 | 1.25 | 3 | ⛔ 死 |

### 归因（五条合成一条：M1 到底在被定价什么）

这五条每条都只改了一个「信息加工维度」，全灭因此可以精确定位 M1 的定义域：

1. **V3 时序分位（S 0.89 / 2Y 2.06）是最有信息量的一条失败。** `ts_rank(·, 252)` 把分歧度换成「相对自身一年历史的分位」⇒ 剥掉了公司规模/行业基数。S 掉 1.01，但 **2Y 反而升到 2.06**。
   ⇒ **结论：分歧度的定价来自横截面上的绝对水平，不是它相对自身历史的异常程度。** 剥掉截面基数就剥掉了信号本身。这也解释了为什么 V4（ts_delta 22）只有 0.09 —— 一阶差分把水平信息全部消掉。
2. **V4 分歧度变化 0.09（全战役最差）证伪了一个流行的理论延伸。** Miller (1977) 讲的是分歧的**水平**；把「分歧冲击」（Hong & Stein 2003 的分歧变化领先价格）搬到本数据集完全不成立。且 TO 从 .173 涨到 **.27**（变化量天然高换手）。
3. **V1/V2 新鲜度（0.29 / 0.93）死。** 日期水平在 sector 内排序后不含收益信息。但 V2（源持仓口径）0.93 显著高于 V1（0.29）⇒ 披露链条越靠近真实持仓，残余信息越多；只是远不够当独立信号。
4. **V5 披露滞后 0.52 死，尽管文献支持明确。** 外部取证：KOR DART 申报的**中位滞后仅 5 天**（insiders-trades.com 实测 170,720 条 D002 申报），且被动型机构可延至季末次月第 10 日。
   ⇒ 滞后在横截面上**方差太小**（绝大多数 5 天上下），没有可交易的截面区分度。文献结论（Cheng, *Insider Trades and Private Information: The Special Case of Delayed-Disclosure Trades*, RFS）成立的前提是存在**长滞后异常样本**，KOR TOP600 不是这种池子。另外 YYYYMMDD 差值跨月非线性也削弱了该探针。
5. ⇒ **M1 的最终定义（写死，后续不得再改）**：**「时间平均的、同一公司内部人之间交易量级（绝对值/股数/股比）的截面离散度」的横截面水平**。任何剥离横截面基数（时序归一/差分）、更换矩（计数/极值/CV）、更换构造（新鲜度/滞后）的变换都会杀死它。

## 数据集切换决定（2026-11-06，触发「无计可施」条款）

**insiders5 的搜索空间已穷尽**，证据：

| 维度 | 覆盖情况 |
|---|---|
| 字段 × 窗口 | 6 个绝对量字段 × {5, 22, 55, 66} 全部实测 = 已闭合 |
| 矩 | 0 阶(vec_count) / 1 阶(均值·比例) / 2 阶(stddev) / 极值(max·min·range) / 商(CV·主导度·不对称) = 全部实测 |
| 分组轴 | sector（最优）/ industry（更差）/ 无 |
| 门控 | officer 高管、trade_when = 全部更差 |
| 几何 | 裸式 / 内层 rank / 内层倒数 / 双尺度 / 时序分位 / 时序差分（Wave 7 在飞）|
| 中性化 | R&M（最优）/ CROWDING / STATISTICAL = 全部更差 |
| 回填 | ts_backfill = 全面减分 |
| 非交易轴 | 新鲜度×2 / 披露滞后 / 库藏股全族 = 全灭 |

⇒ 按用户约束「仅在确实无计可施时才更换，并说明原因」，切换至 **insiders1**（KOR/INSIDERS 的另一个数据集，也是唯一剩下的一个）。

## 外部取证（2026-11-06，论坛 + 文献，可复用结论）

| 来源 | 结论 | 对本次的作用 |
|---|---|---|
| 论坛《高管买入还是买压本身？》（43 赞） | 内部人交易是低频事件，绝大多数值为 0/空 ⇒ **必须先做时间维度聚合把脉冲流变成连续强度**；且绝对强度横截面不可比（大盘股天然量大）| 直接印证 M1 = ts_mean 聚合 + 截面 rank 的正确性；也解释了 W=5 为何死 |
| 论坛《KOR地区推荐数据集》（28 赞） | KOR 整体不好出，但 **insiders 是例外，KOR 竟然能出且能出很多** | 支持继续在本 category 内挖，不必跳出 INSIDERS |
| 论坛《KOR Python Alpha 实战：exp-MA 平滑降 Prod Correlation》 | `ts_mean` 等权平滑的时间指纹与大量存量 alpha 高度相似；**指数衰减加权改变时间结构 ⇒ 天然降低 prod 相关** | ⭐ 待用：G 族几何之外，用 `ts_decay_linear`/exp 衰减替代 ts_mean 作降相关抓手 |
| 论坛《看分歧度当置信度过滤器之前先做两件事》（22 赞） | ① 极端分歧会让整体失真；② **必须行业内 rank**，否则「低分歧」一半是「低分歧行业」 | 印证 sector 分组轴；industry 更细反而更差是样本量问题，不是方向错 |
| 文献 Cheng, RFS《Delayed-Disclosure Trades》 | 长滞后内部人交易携带更强私有信息 | V5 机制依据（但 KOR 滞后方差小 ⇒ 未成立）|
| 外部数据 insiders-trades.com（KOR DART 实测） | 交易→申报**中位滞后 5 天**；170,720 条 D002 申报 / 56,930 条 | 解释 V5 失败的直接原因 |
| 论坛《内部人"动了多少仓位"比"动了多少钱"更重要》（69 赞，DEU） | 信息在「比例」里不在「金额」里 | ⚠ **KOR 相反**：本文实测 vol_chg（股数）1.90 > fa_tr（比例）1.54 ⇒ 该结论区域相关，不可跨区外推 |

## Wave 8 · insiders1 首探（2026-11-06 派发，6 条）

**数据集画像**：insiders1 = Global Insider Trading Data，**9 字段全 VECTOR**，cov **.3526**（仅 35% 股票有内部人交易记录），aC 549，valueScore 3。**无方向字段**（sign 不可得）⇒ 净买入类机制在本集不可实现。

| # | 机制 | 表达式 | 算子数 | 依据 |
|---|---|---|---:|---|
| I1 | M1 迁移 · 金额分歧 | subtract(0.5, group_rank(ts_mean(vec_stddev(insd1_value), 22), sector)) | 5 | M1 定义域迁移（绝对量）|
| I2 | M1 迁移 · 股数分歧 | subtract(0.5, group_rank(ts_mean(vec_stddev(insd1_shares), 22), sector)) | 5 | 同上，口径换成股数 |
| I3 | M1 迁移 · 成交价分歧 | subtract(0.5, group_rank(ts_mean(vec_stddev(insd1_price), 22), sector)) | 5 | 成交价分布宽度 = 交易时点/价位分散度 |
| I4 | 显著性水平 | group_rank(ts_mean(vec_avg(insd1_tradesignificance), 66), sector) | 4 | 本集独有：平台预给 1–3 显著性评分（aC 40 极白）。Cohen-Malloy-Pomorski：只有高显著性交易可预测 |
| I5 | 显著性 × 规模 | group_rank(ts_mean(multiply(vec_avg(insd1_tradesignificance), vec_sum(insd1_valueeur)), 66), sector) | 5 | 信念强度 = 显著性 × 金额（同数据集内乘积，非跨信号相加）|
| I6 | 持仓换手率 | group_rank(ts_mean(divide(vec_sum(insd1_shares), add(vec_avg(insd1_holdings), 1)), 66), sector) | 6 | 交易股数 ÷ 交易后持股 = 内部人动了自己多大仓位（DEU 帖的「比例」假设，在本集做一次区域外验证）|

multisim：3TLxde4Uk5iJ9L1FmAvZQjg

> 风险预期：cov .3526 ⇒ nanHandling OFF 下持仓数约 200/边，LOW_SUB_UNIVERSE_SHARPE 与 CONCENTRATED_WEIGHT 是首要风险闸；若本批全灭，下一批改 nanHandling ON 或换 universe 验证是否纯覆盖率问题。

### Wave 7 · 几何救援批全部读数（5/5，2026-11-06 收割）

| # | 几何 | id | S | F | TO | 2Y | ra | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| G1 | 内层 rank · vol_af | e75Vk8pJ | 1.49 | 1.13 | .1739 | 2.37 | 1 | ⚠ 差 0.09（LOW_SHARPE 唯一闸）|
| G2 | 内层 rank · fa_tr | wpQ2Kwm5 | 1.29 | 0.93 | .1744 | 1.85 | 2 | ⛔ |
| G3 | 内层倒数 · vol_af | qMLY9k1j | **−1.68** | −1.38 | .1728 | −2.19 | 5 | ⭐ **强信号，方向反** |
| G4 | 内层倒数 · fa_tr | LLMmVbjm | **−1.61** | −1.31 | .1761 | −2.08 | 5 | ⭐ **强信号，方向反** |
| G5 | 双尺度偏离 22−66 | E568O079 | 0.40 | 0.15 | .2012 | 1.24 | 4 | ⛔ 死 |

### 归因（倒数几何是本战役第二个真正有效的机制轴）

1. **G3/G4 倒数几何拿到 |S| 1.68 / 1.61，与 M1 水平式同量级。** 机理：`divide(1, stddev+eps)` 把高分歧（右尾）压缩、低分歧端拉开，rank 后的截面间距被重新分配 ⇒ 它与裸式 M1 的 PnL 不是简单取负，而是**不同的持仓分布**（记忆纪律：取负不会精确翻转指标，因 truncation 0.08 与 R&M 残差回归非线性）。
   ⇒ 这是**结构互异的第二个几何轴**，且与 M1 水平式的相关性预计显著低于窗口变体（历史实证：倒数变换的相关性低于换窗变体）。是凑够 10 颗 + 提升可同时提交数的**核心抓手**。
2. **按「取负两臂必须各自实测」纪律**，Wave 9 已派发 `subtract(group_rank(...), 0.5)` 正向臂（含 vol_af / fa_tr / vol_chg / ghc_tr 四字段 + eps 变体），验证方向翻转后的实测读数，**不得假定取负就是 +1.68**。
3. **G1 内层 rank（1.49，只差 LOW_SHARPE 0.09）**：先截面分位再时序平均 = 剔掉公司规模基数。2Y 2.37 很高，但 S 没过线 ⇒ 再次印证 Wave6 的结论「截面绝对水平才是信号」，只是 rank 版损失比 ts_rank 版小。
4. **G5 双尺度偏离 0.40 死** ⇒ 短分歧 − 长分歧（分歧冲击的另一种写法）同样无效，与 V4（ts_delta）结论一致：**被定价的是水平，不是变化**。

### 逐年覆盖判据（用户约束「近十年都要有数据」）

4 颗全闸候选各跑 `get_alpha_yearly_stats`，判据 = 逐年 `longCount>0 && shortCount>0 && pnl≠0`：

| id | 覆盖年份 | 年数 | 连续空窗 |
|---|---|---:|---|
| 3qokqkZQ | 2014–2023 | 10 | **无** |
| A1VrRe7W | 2014–2023 | 10 | **无** |
| P0oY0YdE | 2014–2023 | 10 | **无** |
| kqNv1xRk | 2014–2023 | 10 | **无** |

⇒ insiders5 在本区间**十年逐年满覆盖**，全部满足用户约束 6。无「起始晚型 leading gap」问题（2014 起即有 pnl）。

### prod 相关性槽位（2026-11-06）

读 `logs/_dblock/correlation.lock.json`：`tag=corr:get_production_correlation(E56NbqZK)`、`pid=116024` ⇒ **别人（RISK 战役）在算 prod**，账号唯一 prod 槽被占。按记忆纪律**让路**（不杀进程、不反复 refresh、不重启服务）；inflight TTL 300s，接近交付时统一读取。

### Wave 9 · 倒数几何取负臂（5/5，2026-11-06 收割）—— 验证「取负不精确翻转」

| # | 字段 | id | S | F | 2Y | subU | ra | 唯一失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | vol_af | 2rAX8j1Y | 1.48 | 1.15 | 1.96 | 1.29 | 1 | LOW_SHARPE |
| 2 | fa_tr | 9qxdZEqK | 1.38 | 1.06 | 1.78 | 1.25 | 1 | LOW_SHARPE |
| 3 | vol_chg | 6XdomAXp | **1.57** | 1.29 | 2.06 | 1.49 | 1 | LOW_SHARPE（差 0.01）|
| 4 | ghc_tr | e75Vk676 | **1.57** | 1.34 | 2.03 | 1.57 | 1 | LOW_SHARPE（差 0.01）|
| 5 | vol_chg eps=1 | pwdMYvw3 | 1.50 | 1.21 | 1.95 | 1.42 | 1 | LOW_SHARPE |

**归因（记忆纪律的又一次实证）**：G3 反向臂 S −1.68，其精确取负臂（W9 vol_af）只有 **+1.48**，差 0.20；fa_tr −1.61 → +1.38，差 0.23。
⇒ **`subtract(0.5, group_rank(X))` 的取负不是指标镜像**（truncation 0.08 截断位置 + R&M 残差回归的非线性使极端权重落在不同股票上）。两臂必须各自实测，本条再次确认。
⇒ 但**倒数几何确实是与 M1 水平式结构互异、且强度同量级的第二轴**：vol_chg/ghc_tr 正向臂 1.57，若破 0.01 墙即得 2 颗全闸新件。按「n=1 浅钉不判死、先归因定向破墙」纪律 → Wave 10 用 `winsorize(std=2)` 压 `vec_stddev` 重尾 + eps 扫描两个单杠杆破墙。

### self 相关性实测（本地口径，2026-11-06）

| alpha | max_corr | passes | pool_size |
|---|---:|---|---:|
| 3qokqkZQ | 0.2526 | ✅ | 30 |
| A1VrRe7W | 0.2100 | ✅ | 30 |
| P0oY0YdE | 0.2780 | ✅ | 30 |
| 6XdomAXp | 0.2759 | ✅ | 30 |
| e75Vk676 | 0.2883 | ✅ | 30 |

⇒ 全部对已提交 OS 池 PASS（max 0.21–0.29，远低于 0.7）。
⚠ 但按记忆纪律：**self 只跟已提交池比，两颗未提交的同机制件会双双 PASS**，不能用 self 通过证明「可以一起提交」。族内互相关见下节 `compute_mutual_correlation` 结果。

## Wave 10 · 破墙批（2026-11-06 派发，8 条）

针对 W9 两条 1.57 浅钉（vol_chg / ghc_tr 倒数正向臂），两个单杠杆：
- `winsorize(·, std=2)` 压 `vec_stddev` 重尾（字段画像：vol_chg 量纲跨 6 数量级、重尾；risk70 先例 winsorize 是 S 主杠杆 1.49→1.63）
- eps 扫描（100 / 1000 / 10000 与 0.01 / 0.1 / 1）控制倒数变换的拉伸程度（记忆：eps 要试两档，太大会把低分歧股压平）

multisim：3sdj0Yd9c51F90y1haGZHYBJ

### 互相关实测（compute_mutual_correlation，threshold 0.7 / years 4，2026-11-06）

6 颗（4 颗 M1 全闸 + 2 颗倒数正向臂 1.57）：

| pair | corr |
|---|---:|
| P0oY0YdE × e75Vk676 | **0.9865** |
| 3qokqkZQ × 6XdomAXp | **0.9200** |
| 3qokqkZQ × P0oY0YdE | 0.8757 |
| 6XdomAXp × e75Vk676 | 0.8779 |
| 3qokqkZQ × A1VrRe7W | 0.7962 |
| A1VrRe7W × kqNv1xRk | 0.5241 |

`max_mutually_below_subset = [P0oY0YdE, A1VrRe7W]`，**size = 2**。

**归因（重要修正）**：倒数几何虽在表达式上结构互异，但 **PnL 与 M1 水平式高度同源**（0.92–0.99）。
⇒ 它**不是独立的第二条经济轴**，只是同一「截面分歧度水平」信号的单调变换。整条 M1 轴（含倒数族）最多只能同时提交 **2 颗**（与 Wave1 归因一致）。
⇒ 与 risk70 先例的结构性结论一致：**KOR 该塔只有一条可行经济轴**，10 颗将是同族参数邻域，实际可同时提交数受 self-corr 限制。交付报告必须如实标注（照抄 risk70 §5 的口径）。

### insiders1 首批读数（6/6，2026-11-06 收割）

| # | 机制 | id | S | F | 2Y | subU | lc | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| I1 | 金额分歧 | O0AMObQb | 0.60 | 0.34 | −0.11 | 0.59 | 311 | ⛔ |
| I2 | 股数分歧 | Xg9vG2mx | 0.93 | 0.66 | 0.54 | 0.99 | 313 | ⛔ |
| I3 | 成交价分歧 | RRElM2Ma | −0.03 | 0.00 | −0.67 | −0.20 | 313 | ⛔ |
| I4 | 显著性水平 | O0AMObOJ | 0.28 | 0.11 | 0.67 | 0.34 | 341 | ⛔ |
| I5 | 显著性×金额 | YP1E62r6 | **−1.71** | −1.62 | −1.63 | −1.51 | 322 | ⭐ 强反向 |
| I6 | 持仓换手率 | vR1p8eqv | **−0.99** | −0.69 | −1.53 | −0.90 | 329 | 反向 |

**归因**：
1. **M1 分歧度几何不能直接跨数据集迁移**：insiders5 上 1.90 的骨架在 insiders1 上只有 0.60/0.93/−0.03。
   机理：insiders5 的 `vec_stddev` 吃的是**同一公司多个内部人**（53 字段含高管/关联方/库藏多口径向量）；insiders1 是**全球口径逐笔交易**，向量内是不同交易而非不同持有人，且 cov .3526 使每股票向量更短 ⇒ 离散度信噪比低。
2. **I5/I6 是两个新的强反向信号**，经济含义清晰：
   - I5「高显著性×大金额交易」−1.71 ⇒ 大规模、被平台标为高显著性的内部人交易后**跟随下跌**（信息已被抢跑 / 大额减持主导）。
   - I6「动了自己大比例仓位」−0.99 ⇒ 同向佐证，高换手内部人交易后偏弱。
   - 两者与 M1 是**不同数据集 + 不同机制**，若取负臂过线即得与 M1 低相关的独立件 ⇒ 这是凑 10 颗里真正有多样性的部分。
3. **按取负两臂各自实测纪律** → Wave 11 派发 I5/I6 取负臂 + 显著性单腿取负 + valueeur/holdings 分歧（M1 迁移补测两个未测字段）。

## Wave 11 · insiders1 取负臂 + M1 迁移补测（2026-11-06 派发，6 条）

multisim：3ORlGo5xd4BEcxfjmjPHy36

### Wave 10 破墙批全部读数（8/8，2026-11-06 收割）—— 3 颗全闸

| # | 几何 | id | S | F | TO | 2Y | subU | ra | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| W1 | winsorize(std=2) vol_chg 倒数 | **P0oYN1Qp** | **1.58** | 1.30 | .1735 | 2.08 | 1.49 | **0** | ✅ 全闸（差 0.01→过线）|
| W2 | winsorize(std=2) ghc_tr 倒数 | vR1p8m8w | 1.57 | 1.34 | .1756 | 2.03 | 1.57 | 1 | LOW_SHARPE |
| W3 | winsorize(std=2) vol_af 倒数 | 9qxdYRYo | 1.49 | 1.16 | .1728 | 1.97 | 1.30 | 1 | LOW_SHARPE |
| W4 | winsorize(std=2) fa_tr **水平式** | RRElMrMd | **−1.76** | −1.51 | .1738 | −2.27 | −1.48 | 5 | ⭐ 正向臂应 ≈ +1.76 |
| W5 | vol_chg 倒数 eps=100 | ZYQd6o60 | 1.52 | 1.23 | .1726 | 1.97 | 1.43 | 1 | LOW_SHARPE |
| W6 | vol_chg 倒数 eps=**10000** | **58EAxvx5** | **1.70** | 1.44 | .1753 | 2.37 | 1.61 | **0** | ✅ 全闸（本族最高）|
| W7 | ghc_tr 倒数 eps=0.01 | vR1p8mqz | 1.49 | 1.25 | .1749 | 1.85 | 1.50 | 1 | LOW_SHARPE |
| W8 | ghc_tr 倒数 eps=**1** | **ZYQd6o50** | **1.64** | 1.44 | .1745 | 2.10 | 1.62 | **0** | ✅ 全闸 |

**归因（定向破墙成功，两个杠杆都验证了先验）**：
1. **eps 是倒数几何的主杠杆，且方向单调**：vol_chg 从 eps=1(1.57) → 100(1.52) → 1000(1.57) → **10000(1.70)**；ghc_tr 从 eps=0.01(1.49) → 0.1(1.57) → **1(1.64)**。
   机理：eps 越大，倒数变换越接近线性（压缩高端、拉开低端的非线性越弱）⇒ 在 **vol_chg 这种量纲跨 6 数量级的重尾字段上，eps 必须足够大才不会把低分歧端过度放大成噪声**。这解释了为何 fa_tr（[0,100] 有界）在 eps=0.1 就到 1.38、而 vol_chg 要到 10000 才 1.70。
2. **winsorize(std=2) 对 vol_chg 倒数臂有效**（1.57→1.58 刚好过线），但对 ghc_tr/vol_af 无效 ⇒ 与 risk70 先例一致：winsorize 只在**厚尾最严重**的字段上是 S 主杠杆。
3. **W4（−1.76）是方向写法的副产物**：`subtract(rank, 0.5)` 用于 fa_tr 水平式得到强负，说明 **`subtract(0.5, winsorize(M1水平))` 的正向臂约 +1.76** —— winsorize 压 `vec_stddev` 重尾在水平式上同样有效。⇒ Wave 12 派发 M1 水平式 + winsorize 正向臂 8 条，补齐剩余 3 颗。

### 全闸候选清单（截至 Wave 10，7 颗，全部 batch_get_alpha_metrics 复核 ra=0）

| # | id | 机制族 | 字段@W/几何 | S | F | TO | 2Y | subU | 十年覆盖 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | 3qokqkZQ | M1 水平 | vol_chg@22 | **1.90** | 1.72 | .1731 | 2.59 | 1.78 | ✅ |
| 2 | A1VrRe7W | M1 水平 | vol_af@22 | 1.75 | 1.47 | .1723 | 2.52 | 1.40 | ✅ |
| 3 | P0oY0YdE | M1 水平 | ghc_tr@22 | 1.67 | 1.48 | .1735 | 2.10 | 1.63 | ✅ |
| 4 | kqNv1xRk | M1 水平 | ghc_tr@55 | 1.62 | 1.50 | .0981 | 2.23 | 1.56 | ✅ |
| 5 | P0oYN1Qp | 倒数+winsor | vol_chg eps1000 std2 | 1.58 | 1.30 | .1735 | 2.08 | 1.49 | ✅ |
| 6 | 58EAxvx5 | 倒数 | vol_chg eps10000 | **1.70** | 1.44 | .1753 | 2.37 | 1.61 | ✅ |
| 7 | ZYQd6o50 | 倒数 | ghc_tr eps1 | 1.64 | 1.44 | .1745 | 2.10 | 1.62 | ✅ |

⇒ 7/10，还需 3 颗。Wave 12（M1+winsorize 水平正向臂 8 条）在飞，Wave 11（insiders1 取负臂 6 条）在飞。

## Wave 12 · M1 水平式 + winsorize 正向臂（2026-11-06 派发，8 条）

依据 W4 的 −1.76：对 6 个绝对量字段的 M1 水平式统一加 `winsorize(ts_mean(vec_stddev(F),22), std∈{2,3})`，方向统一 `subtract(0.5, group_rank(·, sector))`。单杠杆 = 压重尾，不混信号、不加装饰算子。

multisim：4hmBjg1ML55NcAC1dU62fG1p

### Wave 12 全部读数（8/8）—— 发现 winsorize 在 group_rank 前幂等（重要）

| # | 结构 | id | S | F | 2Y | ra |
|---|---|---|---:|---:|---:|---:|
| 1 | fa_tr winsor std2 | MPYeWRY8 | 1.50 | 1.20 | 1.95 | 1 |
| 2 | vol_af winsor std2 | E5687W6L | 1.75 | 1.47 | 2.53 | 0 |
| 3 | vol_chg winsor std2 | gJegAOaO | 1.90 | 1.71 | 2.59 | 0 |
| 4 | ghc_tr winsor std2 | npveJRa8 | 1.67 | 1.48 | 2.10 | 0 |
| 5 | vol_bf winsor std2 | A1VrWZxe | 1.34 | 0.98 | 1.48 | 3 |
| 6 | fb_tr winsor std2 | E5687Wm1 | 1.10 | 0.75 | 1.17 | 3 |
| 7 | vol_chg winsor std3 | 88REo9Ga | 1.90 | 1.71 | 2.59 | 0 |
| 8 | fa_tr winsor std3 | YP1ErKlM | 1.49 | 1.19 | 1.95 | 1 |

**读数与 Wave4 的裸 M1 水平式逐位相同**（vol_chg 1.90/2.59/.1731、vol_af 1.75/2.53、ghc_tr 1.67/2.10）。
`compute_mutual_correlation(threshold=0.99)` 实测：
- `3qokqkZQ`（裸）~`gJegAOaO`（winsor std2）~`88REo9Ga`（winsor std3）= **1.000 / 1.000**
- `A1VrRe7W` ~ `E5687W6L` = **1.000**；`P0oY0YdE` ~ `npveJRa8` = **0.9999**

**归因**：`winsorize` = 单调截断（clamp 到 ±N·std 边界），`group_rank` 是对输入做**排序** ⇒ 单调截断**不改变相对次序**，rank 输出不变 ⇒ PnL 完全相同。
⇒ **`winsorize(·, std)` 放在 `group_rank` 之前是幂等算子**（对最终 alpha 零影响），属于「装饰算子」，与用户「禁止为凑数加装饰算子」一致。
⇒ **Wave 12 的 4 颗全闸件全部是已交付件的重复，不计入 10 颗**。（风险点：若不看互相关直接按 ra=0 计数，会误凑 4 颗废件。）
⇒ 要真正改变几何，截断必须放在 **rank 之后**（`winsorize(group_rank(...), std)` 改变权重分布），或换非线性变换（倒数已验证有效）。

## Wave 13 · 倒数几何补齐批（2026-11-06 派发，8 条）

对尚未出过全闸件的字段（fa_tr / vol_af / vol_bf）做倒数几何 + 大 eps 扫描，补结构互异的全闸件至 10 颗。
依据 Wave10 的 eps 单调律：vol_chg 需 eps=10000、ghc_tr 需 eps=1；本批给 fa_tr 试 {1,10,100}、vol_af 试 {10000,100000}、vol_bf 试 10000、ghc_tr 补 {10,100}。

multisim：4xqfgdbeq4AqblL2WJ9A7ma
### Wave 13 全部读数（8/8）—— 4 颗全闸 + 倒数大 eps 退化律

| # | 字段 | eps | id | S | F | 2Y | subU | ra |
|---|---|---:|---|---:|---:|---:|---:|---:|
| 1 | fa_tr | 1 | RREl3lv1 | 1.41 | 1.09 | 1.82 | 1.25 | 1 (LOW_SHARPE) |
| 2 | fa_tr | 10 | vR1pqpoA | 1.48 | 1.18 | 1.86 | 1.28 | 1 |
| 3 | fa_tr | 100 | 88REoEZm | 1.50 | 1.20 | 1.93 | 1.30 | 1 |
| 4 | vol_af | 10000 | YP1ErEOw | 1.62 | 1.30 | 2.16 | 1.40 | **0** |
| 5 | vol_af | 100000 | qMLY1Ypj | **1.69** | 1.38 | 2.51 | 1.41 | **0** |
| 6 | vol_bf | 10000 | ZYQd5d98 | 1.23 | 0.87 | 1.35 | 1.03 | 3 |
| 7 | ghc_tr | 10 | npveJe53 | 1.66 | 1.47 | 2.08 | 1.63 | **0** |
| 8 | ghc_tr | 100 | O0AMYMXg | 1.67 | 1.48 | 2.10 | 1.63 | **0** |

**归因（倒数大 eps 退化律）**：`divide(1, add(x, eps))` 当 eps ≫ x 时 ≈ `(1/eps)(1 − x/eps²)`，是 x 的**单调线性**函数 ⇒ `group_rank` 后排序与裸 `vec_stddev` 完全反向 ⇒ PnL 退回裸 M1。
- ghc_tr 量纲极小（±0.0x–x%），任何 eps≥1 都退化：eps1/10/100 与裸 `P0oY0YdE` 互相关 **0.9969 / 0.9997 / 1.0000**（eps100 读数 1.67/1.48/2.10 与裸件逐位相同）。
- vol_chg 量纲跨 6 数量级，eps=10000 相对不算大 ⇒ 倒数才真正改变几何（与裸 `3qokqkZQ` 0.9598，仍高但明显低于 ghc_tr）。
- ⇒ **倒数几何在本数据集不是独立于 M1 水平式的第二经济轴**，只是同一轴的单调重参数化（与 Agent memory 一致）。

## Wave 11 收尾 · insiders1 取负臂（multisim 3ORlGo5xd4BEcxfjmjPHy36）

COMPLETE，6/6 全灭（无全闸件）。首探 `3TLxde4Uk5iJ9L1FmAvZQjg` 里 `YP1E62r6` S−1.71 的「显著性×金额」强反向信号，取正向臂后实测只有 1.49–1.51 / 2Y 1.26–1.32，全卡 LOW_SHARPE + LOW_2Y_SHARPE。
再次确认「取负/反向不精确翻转指标，两臂必须各自实测」；且 insiders1 cov .3526 + 无方向码的结构性缺陷无法靠几何补救。⇒ insiders1 作为「最后手段」已用尽，不贡献交付件。

## 最终裁定（收波）

- 全战役 13 波，唯一出货轴 = **M1 分歧度截面水平**（`vec_stddev` 的时序均值 → sector 内 rank → 反向），字段限 vol_chg / vol_af / ghc_tr，窗口 W=22 最优、W=55 仅 ghc_tr 可用。
- 所有「新机制」（净流比 / 加速度 / 极值 / 自身 z / 变异系数 / 广度 / 不对称 / 主导度 / 门控 / 新鲜度 / 披露滞后 / CROWDING / STATISTICAL / ts_backfill）**全灭**；insiders5 结构空间已穷尽，insiders1 亦穷尽。
- ra=0 候选池 15 颗 → 剔除两类重复件后取 10 颗：
  - ① Wave12 的 `winsorize`（放在 group_rank 前）幂等纯重复 4 颗（corr=1.000，读数逐位同）全部排除；
  - ② Wave13 的 `O0AMYMXg`（ghc_tr eps100，corr=1.0000、读数与裸 `P0oY0YdE` 逐位同）排除；
  - ③ 余 10 颗 = 最终交付清单（见 final_report.md），全部 `failed_ra_count=0` / S≥1.58 / 2Y≥1.58 / 2014–2023 逐年 longCount>0 && shortCount>0 && pnl≠0 / self<0.7。
- **诚实披露**：10 颗仍是同一机制族的高相关参数邻域，互相关 0.90–0.9998，`compute_mutual_correlation(threshold=0.9)` 给 `max_mutually_below_subset_size=4`（threshold=0.7 时仅 2）。实际可同时提交进同一本书的数量受 SELF_CORRELATION 限制（见 final_report.md §5）。
- **prod 实测撞墙（22:40 闭合，替换原「prod 未知」）**：族代表 `3qokqkZQ` 用 MCP `check_correlation(production, refresh=False)` 零成本读回平台已算好的存储值 `prod=0.8495`（`passes_check=false`、`computed=false`，直方图深钉厚尾 `max=0.8495`），`persist_correlation` 已落库 `alphas` 表。此前 21:48 busy / 22:26 MCP 120s 超时 / 22:30 busy+空体均如实保留为「当时未取到值」，22:40 重查命中已完成值 ⇒ 未知闭合。按族代表预判三档（>0.80 整族封盘）＋深钉厚尾判死 ⇒ 其余 9 颗不再逐颗占用账号唯一 prod 槽、10 颗均不可提交、不再量产；不得把 self PASS 当 prod PASS（完整口径见 final_report.md §5.3）。
- **算子数**：交付 10 颗每条 4–7 个算子，均 ≤12，未加任何装饰算子凑数。

### 补充记录（21:48 prod 复测，收波后）

用 MCP `check_correlation(3qokqkZQ, production, refresh=False)` 对族代表做零成本 prod 复测（不占槽、不强制回源、不并发），返回 `status=correlation_busy / retry_after=240 / holder=corr:get_production_correlation(rKRRP3pa) / inflight=false`。holder 是另一工作线 alpha（非本战役 10 颗），按 prod 规范让路、不重触发、不把 busy 当读数。已排一次延时重查（self_reminder，20 分钟），待账号 prod 槽释放后再用 `refresh=False` 命中平台缓存；本 10 颗 prod 仍为「未知」。
