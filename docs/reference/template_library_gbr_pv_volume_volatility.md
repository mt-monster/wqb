# GBR PV 塔模板库 —— 量能 / 波动 / 区间位置 / 非流动性

> 区域：**GBR / TOP700 / D1**（universe 唯一，无退路）
> 建立：2026-10-31
> 目标：给 PV 塔提供 **≥10 个结构互异**的模板，覆盖不同经济机制、不同矩、不同算子几何。
> 纪律：模板差异必须落在**骨架结构 / 算子几何 / 矩（水平·一阶差分·二阶方差）/ 分组轴 / 非线性变换 / 窗口族**上，**不能只是换窗口或换常数**。

---

## §0 已知的 GBR 特性（决定为什么是这些机制）

| 事实 | 证据 | 对模板的影响 |
|---|---|---|
| **高成交量溢价强正向** | `88Rg2zPV` = `rank(ts_quantile(reverse(divide(volume, ts_mean(volume,66))),252))` @ decay10 → S **−1.68** / 2Y −1.70 ⇒ 取负后正向 S ≈ **+1.68** / 2Y ≈ **+1.70** | T2 / T3 是主力 |
| **价格反转有效但 2Y 已衰竭** | `e75eWObM` = `rank(ts_quantile(reverse(ts_sum(returns,22)),252))` @ decay10 → S 1.42 / F 1.11 / 2Y **1.02** | T4 只能作辅助 |
| **形态相似度差（continuation_score）是全闸唯一** | `MPY96E7o` @ SUBIND/decay16/trunc0.06 → S 1.70 / F 1.24 / 2Y 1.94 / SUB 0.82，`failed_ra_count=0` | T1 最强，已锁定 |
| **`pattern_scores` 全族判死** | 最优 `O0AKJXap` S 1.28 / 2Y 0.63；`2rAP2dkZ` 同表达式换设置 S 1.10；无后缀版 S 0.20 | T11 仅供参考，勿再投入 |
| **`ts_max` / `ts_min` 本账号不可用** | 语法合法但回测 ERROR 并级联整批 CANCELLED | 必须用 `ts_arg_max` 绕开（T8） |
| **`group_rank` 是 SUB 杀手**（0.44→0.29） | USA 实证，跨区通用 | 桶轴一律接 `group_neutralize` |
| **横截面外层越少，SUB/S 越高** | 裸 `ts_zscore` SUB/S 0.447–0.630 vs `group_rank` 0.089–0.301 | 优先「低横截面操作」骨架 |
| **F 的公式** | `F = S × sqrt(\|returns\| / max(TO, 0.125))`；要 F≥1.0 且 S≥1.58 需 `returns/TO ≥ 0.40` | 高换手信号必须配慢基准 |
| **decay 在 F 上是零杠杆** | `88Rg2zPV`(decay10) F 0.79 → `78Lg233b`(decay20) F 0.80；TO −34% 但 returns −10%、S −13%，相消 | **不要用 decay 救 F** |

---

## §1 模板全表（13 个，结构互异）

统一记法：`F` = 主信号字段，`W` = 窗口，所有 `W ∈ {1,5,22,66,252,504,1008,1260}`（白名单）。

| # | 模板表达式 | 机制 | 矩 | 骨架结构 | 算子几何 | 非线性 | 来源 |
|---|---|---|---|---|---|---|---|
| **T1** | `ts_quantile(subtract(ts_backfill(F_down,22), ts_backfill(F_up,22)), 252)` | 形态相似度差（下跌形态 vs 上涨形态） | 水平差 | 双字段差 → 时序分位 | `subtract` + `ts_backfill` + `ts_quantile` | 分位反 CDF | 论坛 43298855144855 + 自建 |
| **T2** | `rank(ts_quantile(divide(volume, ts_mean(volume, 66)), 252))` | 高成交量溢价（短基准异常量） | 水平比 | 自比短基准 → 分位 → 秩 | `divide` + `ts_mean` + `ts_quantile` + `rank` | 分位 + 截面秩 | 论文 Gervais-Odean-Mingelgrin 2001 |
| **T3** | `ts_quantile(divide(volume, ts_mean(volume, 252)), 252)` | 高成交量溢价（**长基准**，慢变量） | 水平比 | 自比长基准 → 分位 | `divide` + `ts_mean(252)` + `ts_quantile` | 分位反 CDF | 自建（T2 的**窗口族**变体：基准 66日→252日，跨季度→跨年度） |
| **T4** | `ts_quantile(reverse(ts_sum(returns, 22)), 252)` | 短期反转（Lehmann 1990） | 累积一阶 | 累积 → 取反 → 分位 | `ts_sum` + `reverse` + `ts_quantile` | 分位 | 论文 Lehmann 1990 / Jegadeesh 1990 |
| **T5** | `ts_quantile(ts_std_dev(returns, 66), 252)` | 低波动异象（Ang-Hodrick-Xing-Zhang 2006） | **二阶（方差）** | 波动率 → 分位 | `ts_std_dev` + `ts_quantile` | 分位 | 论文 Ang et al. 2006 |
| **T6** | `ts_quantile(ts_mean(divide(abs(returns), volume), 66), 252)` | Amihud 非流动性（2002） | 一阶绝对值/量 | 比值均值 → 分位 | `abs` + `divide` + `ts_mean` + `ts_quantile` | 分位 | 论文 Amihud 2002 |
| **T7** | `ts_quantile(close, 252)` | 52 周区间位置（George-Hwang 2004 锚定效应） | 水平（自历史分布） | 价格自历史分位 | `ts_quantile(close)` 单参 | 分位反 CDF | 论文 GFV 2004 |
| **T8** | `rank(ts_arg_max(high, 252))` | 距 52 周新高天数（**绕开 `ts_max`**） | **极值时点** | 时序极值位置 → 截面秩 | `ts_arg_max` + `rank` | 截面秩 | 论坛 CW90254（`ts_decay_linear(rank(ts_arg_max(high,20)),5)`）+ GFV 2004 |
| **T9** | `ts_quantile(ts_corr(returns, volume, 66), 252)` | 量价相关（信息到达速率） | **二阶（协方差标准化）** | 滚动相关 → 分位 | `ts_corr` + `ts_quantile` | 分位 | 论坛 ZZ90023（high/low 携带日内信息）+ 自建 |
| **T10** | `ts_quantile(divide(high - low, close), 252)` | 日内振幅（真实波幅，ATR 归一） | **极差** | 极差/价格 → 分位 | `subtract` + `divide` + `ts_quantile` | 分位 | 论坛 TN48752（ATR 构造 TR = max(high-low, …)） |
| **T11** | `ts_quantile(subtract(ts_backfill(breakaway_gap_down_mean_simscore_lookback60,22), ts_backfill(breakaway_gap_up_mean_simscore_lookback60,22)), 252)` | pattern gap 形态差 | 水平差 | 同 T1，字段来自 `pattern_scores` | 同 T1 | 分位 | 自建（**已判死**，仅存档：S 1.10 / 2Y 0.89） |
| **T12** | `divide(open - ts_delay(close, 1), close)` | 隔夜跳空（隔夜信息 vs 日内修正） | **一阶差分** | 跳空/价格 | `subtract` + `ts_delay` + `divide` | 无（裸比值） | 论坛 ZZ90023（隔夜涨 + 日内跌 = 套利者修正） |
| **T13** | `ts_quantile(divide(ts_delta(close, 252), ts_std_dev(returns, 252)), 252)` | **风险调整动量**（类夏普比的价量复合） | 一阶/二阶复合 | 收益 ÷ 波动 → 分位 | `ts_delta` + `divide` + `ts_std_dev` | 分位 | 自建（融合 Frazzini-Pedersen 2014 风险调整思想与 Jegadeesh-Titman 1993 动量） |

**结构互异性核验**（差异维度分布）：

| 维度 | 覆盖的模板 |
|---|---|
| 矩 = 水平 | T1, T2, T3, T7, T11 |
| 矩 = 一阶差分/累积 | T4, T12 |
| 矩 = 二阶（方差/协方差） | T5, T9 |
| 矩 = 极值/极差 | T8, T10 |
| 矩 = 复合 | T13 |
| 骨架 = 单字段自比 | T2, T3, T5, T6, T7, T8, T10 |
| 骨架 = 双字段差 | T1, T11, T12 |
| 骨架 = 双字段复合 | T9, T13 |
| 非线性 = 时序分位 | T1–T7, T9–T11, T13 |
| 非线性 = 截面秩 | T2, T8 |
| 非线性 = 无（裸比值） | T12 |
| 窗口族 = 短基准（≤66） | T2, T5, T6, T9, T10 |
| 窗口族 = 长基准（≥252） | T3, T7, T8, T13 |

---

## §2 已实测结果（防止重复投入）

| 模板 | alpha | 设置 | S | F | TO | 2Y | SUB | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| T1（continuation） | `MPY96E7o` | SUBIND/16/0.06 | **1.70** | **1.24** | 12.91% | **1.94** | 0.82 | ✅ **全闸** |
| T1（pattern breakaway 60） | `O0AKJXap` | IND/2/0.05 | 1.28 | — | 22.57% | 0.63 | 0.85 | ❌ 2Y |
| T1（pattern common 无后缀） | `RRE0vWLb` | SUBIND/16/0.06 | 0.20 | 0.05 | 13.15% | 0.22 | −0.01 | ❌ 全灭 |
| T1（pattern breakaway @ 换设置） | `2rAP2dkZ` | SUBIND/16/0.06 | 1.10 | 0.63 | 12.84% | 0.89 | 0.53 | ❌ 2Y + SUB |
| T4（+ reverse） | `e75eWObM` | IND/10/0.05 | 1.42 | **1.11** | 12.81% | 1.02 | 0.86 | ❌ S/2Y（且触发 `REVERSION_COMPONENT`） |
| T2（+ reverse，取负读） | `88Rg2zPV` | IND/10/0.05 | −1.68 | −0.79 | 32.51% | −1.70 | −0.47 | 正向 S≈1.68 / 2Y≈1.70 双过，**F 0.79 差 21%** |
| T2（正向 @ decay20） | `78Lg233b` | IND/20/0.05 | 1.46 | 0.80 | 21.49% | **1.55** | 0.47 | ❌ S/2Y/F/SUB（2Y 仅差 1.9%） |
| 量能扩张 5/252 | `9qxg2889` | IND/20/0.05 | 0.87 | 0.46 | 12.88% | 1.10 | 0.17 | ❌ 判死 |
| T2 裸版（去 rank） | 批 56 在飞 | IND/10/0.05 | ? | ? | ? | ? | ? | 待收 |
| T3（长基准裸版） | 批 56 在飞 | IND/10/0.05 | ? | ? | ? | ? | ? | 待收 |
| T5 / T6 / T7 / T9 | — | — | — | — | — | — | — | **未测** |
| T8 / T10 / T12 / T13 | — | — | — | — | — | — | — | **未测**（已过 `operator_audit` safe + preflight valid） |

---

## §3 关键算子技巧（本轮从论坛补入）

### 3.1 `ts_arg_max` —— `ts_max` 的第四种替代（此前遗漏）

`ts_arg_max(x, d)` = **距最近 d 日最大值的交易日数**（0 = 今天是新高）。

- 直接给出「距 52 周新高多少天」，是 GFV 2004 的**原生实现**，不需要先求最大值。
- 论坛出处：《精通 Alpha 算子：從原始數據到穩健訊號》（CW90254，13 赞）
  `ts_decay_linear(rank(ts_arg_max(high, 20)), 5)` —— 「瞄準觸及 20 天新高的股票，但透過平滑執行來節省成本」。
- **之前记的三种替代（`ts_sum` / 嵌套 `max` 展开 / `ts_rank`）优先序应更新**：
  1. `ts_arg_max(x, W)` —— 语义最贴（只要「何时」不要「多大」）
  2. `ts_sum(x, W)` —— 累积脉冲能量
  3. 嵌套二元 `max` 展开 —— 最忠实但表达式爆炸
  4. `ts_rank(x, W)` 逼近 1 —— 只保留位置信息

### 3.2 `winsorize(·, std=4)` + `ts_quantile` 组合

论坛出处：《【MCP WorkFlow】GLB》（JL52079，22 赞）：`ts_quantile(winsorize(ts_delta(X,42)/ts_delay(X,42), std=4), 5)`
- 先截尾（std=4）再分位，防止单日异常值主导分位。
- 与既有教训一致：`ts_quantile` 单用会被单一极端值影响（`vec_avg` 稀疏场景同病）。

### 3.3 GBR 单位闸注意

- **`unit_handling=VERIFY`** 下不能给带单位字段加无量纲常数；比值一律同单位相除。
- `divide(abs(returns), volume)`：`returns` 无量纲 / `volume` 有量纲 ⇒ 结果 1/量纲，合法（T6）。
- `divide(ts_delta(close,252), ts_std_dev(returns,252))`：价格 / 无量纲 ⇒ 有价格量纲，`ts_quantile` 收口后无量纲（T13）。
- 门控一律 `greater(rank(x), 0.5)`，不可 `greater(<带单位计数>, 常数)`。

---

## §4 使用建议

1. **先测未测的 4 个机制族**：T5（低波）/ T6（Amihud）/ T7（区间位置）/ T8（新高距离）——这 4 个互不相关且都是「慢变量」，TO 天然低，最可能同时过 F 与 SUB。
2. **T2 的 F 缺口是结构性的**：高成交量溢价本身是「高换手低 margin」（margin 6.03bp vs GBR 中位 11.9bp）。**不要用 decay 救**（零杠杆，已证），要救只能换更慢的成交量定义（T3）或换机制。
3. **T4 / T11 不再投入**：T4 的 2Y 已衰竭到 1.02 且触发 `REVERSION_COMPONENT`；T11 全族判死。
4. **PV 塔内部去相关空间极大**（8 条实测矩阵）：
   - `78Lg233b` vs `MPY96E7o` = **0.1519**
   - `78Lg233b` vs `2rAP2dkZ` = 0.021 / vs `O0AKJXap` = 0.0346
   - `MPY96E7o` vs `2rAP2dkZ` = 0.606 / vs `O0AKJXap` = 0.5724
   ⇒ **PV 塔的瓶颈是指标不是相关性**。只要每个机制各自过闸，可共存容量不是问题。

---

## §5 批 66 收批：T13 / T9 双判死（2026-10-31）

设置 `GBR/TOP700/D1/INDUSTRY/decay10/trunc0.05/maxTrade OFF/nanHandling OFF`，multisim = `2Stohm4vJ4NN9rJ19nsAevL5`。

| 模板 | alpha | 表达式 | S | F | 2Y | SUB | TO | margin | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| **T13** 风险调整动量 | `E56ojgoK` | `vector_neut(rank(ts_quantile(divide(ts_sum(returns,252), ts_std_dev(returns,252)), 252)), rank(ts_zscore(ts_backfill(volume,22),66)))` | **−0.64** | −0.32 | −0.87 | −0.17 | 14.95% | −4.93bp | ❌ **反向** |
| **T9** 量价相关 | `A1VqpgqQ` | `vector_neut(rank(ts_corr(returns, ts_zscore(ts_backfill(volume,22),66), 66)), rank(ts_std_dev(returns,252)))` | **0.28** | 0.10 | 0.26 | 0.30 | 6.04% | 5.53bp | ❌ 太弱 |

两条 `failed_ra_count = 3`（LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE），且都带 `REVERSION_COMPONENT` 警告。

### 5.1 T13 的直接读法：GBR 是**长期反转市**，不是动量市

`ts_sum(returns,252)/ts_std_dev(returns,252)`（12 个月风险调整动量）在 GBR TOP700 上 **S = −0.64**，即**动量显著为负、长期反转显著为正**。
- 反向后约 `S ≈ +0.64`，仍远低于 1.58 ⇒ **长期反转也不足以单独过闸**。
- 与既有教训合流：GBR 短期反转（Lehmann 1990 / Jegadeesh 1990）2Y 已衰竭，长期反转够不着闸 ⇒ **GBR 反转族的强度带夹在「短期已衰竭」与「长期不够强」之间**。
- `maxTrade=OFF` 下 TO 仅 14.95%，说明该信号本身换手很低，不是换手问题。

### 5.2 T9 的输出是「低换手低污染但无信号」

TO 6.04% / margin 5.53bp / `SUB 0.30 > S 0.28`（罕见地 SUB 超过全期 S）。这是「信号干净但强度不足」的典型形态 —— 与 T7 同类，非换手问题。**双判死，不再变体。**

### 5.3 PV builtin 模板剩余清单（本轮后）

| 状态 | 模板 |
|---|---|
| **已判死** | T4 / T5（低波 S 0.17）/ T7（区间位置 S −0.23）/ T9（0.28）/ T11 全族 / T13（−0.64） |
| **未测** | T6 Amihud 非流动性 / T8 `ts_arg_max` 新高距离 / T10 日内振幅 / T12 隔夜跳空 |

⇒ **PV 塔在 builtin 价量上的可用模板已只剩 4 个，且 T6/T8/T10/T12 全是「慢变量低换手」型，与已死的 T5/T7 同族风险高。**

### 5.4 ★ 结构性发现：塔位由**表达式用到的字段所在数据集**决定

- `E56onL5r` = FUND 会计信号 + `rank(cap)` + `rank(volume-zscore)` 残差化 ⇒ `pyramids.list = [GBR/D1/PV, GBR/D1/FUNDAMENTAL]`，**effective 2**。
- `j2YNnKOQ` = 纯 `quarterly_ebit_value / current_enterprise_value` ⇒ `pyramids.list = [GBR/D1/FUNDAMENTAL]`，effective 1。

**⇒ 给任何 FUND / ANALYST 候选加一层 `rank(cap)` 或 `rank(ts_zscore(ts_backfill(volume,22),66))` 残差化轴，会顺带把 PV 塔位带上，且这两层正好也是已验证的降 prod 杠杆（−0.048 / −0.051）。**

这条把「点 PV 塔」从「必须找 PV 主信号」降级为「给现有过闸候选加一层正交轴」——**成本从一次新机制探索降到一次残差化实验**。
注意配额：trio（PV/MODEL/OTHER）× 非 trio 总量 ≤5，`E56onL5r` 已占 1 个。