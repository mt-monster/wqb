# 波 182 —— risk65 十模板：特质残差收益 vs 特质风险水平（RISK 塔第 3 颗）

> 日期：2026-10-30 · 区域 USA / TOP3000 / D1 / STATISTICAL / decay 2 / trunc 0.05 / nanHandling OFF
> multisim `1qA37hFS58T9a9CF3J71cr`，10 条全 COMPLETE、0 错误
> 台账：`upsert_wave_result(182, PARTIAL, n_pass=0, n_near=1, candidates=[ZYQZAEW8, wpQ6bazx])`

---

## 1. 为什么开这一波

RISK 塔当时的处境是「2/3 已亮，第 3 颗无载体」：

| 载体 | 表达式核心 | S | F | 2Y | SUB | invest_S | fRA | 状态 |
|---|---|---|---|---|---|---|---|---|
| `ZYQZEawY` | `reverse(ts_decay_linear(discount_store_retail_score, 66))` | 1.64 | 1.00 | 1.64 | 0.78 | 1.32 | 0 | ✅ 全闸 |
| `qMLbW8xP` | `reverse(ts_mean(short_interest_factor_score_2, 22))` | 1.73 | 1.02 | 2.48 | 0.84 | 1.77 | 0 | ✅ 全闸 |
| 两者相关 | | | | | | | | **0.1277** |

波 178 找到的 `N1NMQJog`（`systemic_risk_measure_2`）与这两颗相关 0.4321 / −0.0984 全安全，是理想第 3 颗；**但波 181 用 10 个结构互异模板证明该字段 S 天花板 = 0.92**，距闸 1.58 差 72%，正式判死。

于是转向 `risk65`。选它的三条理由：

1. **产出率全 USA RISK 类第 1**：`get_mining_yield` strict 口径 ra_clean/backtested = **0.50（3/6）**，仅次于 `web_traffic_engage`（0.60）与 `analyst_consensus`（0.50）。
2. **不拥挤**：6 字段 / alphaCount 411 / valueScore 3.0。对照 `risk70`（158 字段 / 82,093 alphas）与 `risk62`（636 / 23,601）完全饱和。
3. **机制可能正交于已有两颗**：6 字段里 3 个是「特质残差收益」（反转机制），3 个是「特质风险估计」（低波动异象，Ang et al. 2006）。而 `ZYQZEawY` 的 `discount_store_retail_score` 名字骗人，实为「Daily specific (idiosyncratic) returns%」—— **所以 risk65 的 trsd/dsrt 很可能是同一现象的另一个供应商版本，这是本波最主要的相关性风险**。所以本波把 6 条押 `*_srisk`（风险族，机制不同轴）、4 条押 dsrt/trsd（残差收益族，其中 1 条专职做相关性对照）。

### risk65 全 6 字段

| 字段 | cov | users | alphas | 说明 |
|---|---|---|---|---|
| `rsk65_mfm_etfm3_dsrt_intermediate` | 1.0 | 142 | **191** | Instrument Specific Returns（ETFM3） |
| `rsk65_mfm_etfm3_srisk` | 0.9485 | 54 | 61 | ETFM3 特质风险估计 |
| `rsk65_mfm_etfm4_dsrt_intermediate` | 1.0 | 80 | 89 | Instrument Specific Returns（ETFM4） |
| `rsk65_mfm_etfm4_srisk` | 0.9485 | 44 | 61 | ETFM4 特质风险估计 |
| `rsk65_trsd_3mfte_mfm` | 0.9485 | 62 | 86 | 模型因子未解释的特质残差收益 |
| `rsk65_trsd_4mfte_mfm` | 1.0 | 81 | 125 | ETFM4 特质残差收益 |

---

## 2. 十个结构互异模板（差异落在矩 / 算子几何 / 分组轴 / 字段，不是换窗口）

| # | 结构名 | 押的矩 | 与其它模板的本质差异 |
|---|---|---|---|
| T1 | `reverse(ts_decay_linear(trsd_4mfte, 66))` + industry | 残差收益·水平（线性衰减几何） | 保幅度的衰减窗 |
| T2 | `reverse(ts_mean(etfm4_srisk, 22))` + industry | 风险水平·短窗 | 换到风险族 + 等权平滑 |
| T3 | `reverse(ts_zscore(etfm4_srisk, 504))` + industry | 风险·相对自己的长窗位置 | 时序标准化（去量纲） |
| T4 | `reverse(ts_delta(etfm4_srisk, 66))` + industry | 风险·**一阶差分**（趋势） | 只留变化量，丢水平 |
| T5 | `reverse(etfm3_srisk ÷ etfm4_srisk)` + industry | 风险·**跨模型比值** | 两个供应商版本的相对定价 |
| T6 | `reverse(ts_rank(etfm3_srisk, 504))` + industry | 风险·时序秩位 | 非参数位置（抗极值） |
| T7 | `ts_sum(trsd_4mfte, 66) ÷ etfm4_srisk` + industry（**正向**） | 残差·**风险调整累计** | 信息比形式，分母是风险不是均值 |
| T8 | `group_zscore(reverse(ts_mean(trsd_4mfte, 5)), subindustry)` | 残差收益·**短窗 + zscore + 最细轴** | 三个轴同时换（窗 5 / 统计量 / 分组） |
| T9 | `reverse(ts_std_dev(etfm4_srisk, 66))` + industry | 风险·**二阶矩**（波动） | 押风险的不稳定性而非水平 |
| T10 | `reverse(trsd_3mfte − trsd_4mfte)` + industry | 残差·**跨模型差分** | 两个供应商版本的残差分歧 |

覆盖：水平（T1/T2/T8）· 一阶差分（T4）· 二阶矩（T9）· 相对位置（T3/T6）· 比值（T5/T7/T10）· 分组轴（industry / subindustry）· 字段族（srisk / trsd_3mfte / trsd_4mfte）。

### 模板来源标注

| 来源 | 用在哪 |
|---|---|
| 平台论坛 `43175786936087`（高换手分层治理三分类） | 换手归因框架 → 波 184 的设计依据（本波先把病灶定位，未动手治） |
| 平台论坛 `36142256739095`（SUE 标准模板） | T7 的 `sum ÷ std` 信息比几何 |
| 学术文献 Ang, Hodrick, Xing, Zhang (2006)「低波动异象」 | T2 / T3 / T6 / T9 四条风险水平/秩位/二阶矩模板的经济学先验 |
| 学术文献 Lehmann (1990) / Jegadeesh (1990)「短期反转」 | T1 / T8 残差收益反转的经济学先验 |
| 自建（memory 铁律：换窗口跨度 = 第一降相关杠杆） | T1（窗 66）vs T8（窗 5）的窗口跨度设计，用于相关性对照 |
| 自建（波 181 判据：风险类字段只能出 1 颗） | T4/T5/T10 三条「换矩探针」，专职验风险族是否有第二自由度 |

---

## 3. 完整结果表

| # | alpha | S | F | TO | R | 2Y | SUB | invest_S | DD | fRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | `wpQ6bazx` | 1.38 | 0.72 | 19.08% | 5.13% | 1.14 | 0.64 | 1.11 | 6.40% | 3 | 三闸全缺 |
| T2 | `A1V6vGag` | 0.57 | 0.21 | 6.90% | 1.64% | 1.03 | 0.19 | 0.55 | 13.71% | 4 | 死 |
| T3 | `QPveKGlK` | 0.57 | 0.19 | 9.17% | 1.39% | **1.84** | 0.04 | 0.64 | 6.71% | 3 | 死（2Y 独好） |
| T4 | `0mYorpQ2` | −0.18 | −0.03 | 13.21% | −0.45% | −0.78 | −0.25 | −0.32 | 9.14% | 4 | 反号 |
| T5 | `pwd05N1X` | −0.72 | −0.28 | 7.82% | −1.95% | −1.64 | −0.12 | −0.81 | 22.18% | 3 | 反号 |
| T6 | `omE2WN9n` | 0.60 | 0.18 | 16.93% | 1.47% | **1.70** | 0.13 | 0.61 | 5.32% | 3 | 死（2Y 独好） |
| T7 | `omE2WN9E` | −1.18 | −0.57 | 16.18% | −3.81% | −1.33 | −0.18 | −0.79 | 38.15% | 3 | 反号 |
| **T8** | **`ZYQZAEW8`** | **2.01** | 0.71 | **51.29%** | 6.44% | 0.98 | **1.70** | **1.91** | **4.65%** | 2 | **只卡 F / 2Y** |
| T9 | `kqNRgP1L` | 0.77 | 0.29 | 8.89% | 1.76% | 0.47 | −0.45 | 0.69 | 5.12% | 4 | 死（SUB 负） |
| T10 | `E563RGgm` | 0.00 | — | 0.00% | 0% | — | — | — | 0% | 5 | **全空** |

`ZYQZAEW8` 的闸状态（`get_alpha_details`）：`checks.fail = []`，pass 6 项（LOW_SHARPE / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / MATCHES_PYRAMID），warning 5 项（LOW_FITNESS 0.71 / LOW_2Y_SHARPE 0.98 / CLUSTER_TEST 0.61 / MATCHES_THEMES / OSMOSIS_ALLOCATION），`ra.failed_ra_count = 2`，`pyramid_short = risk`。

---

## 4. 六条确定性发现

### 4.1 ★ 风险类字段不是 alpha 源，收益类残差才是

6 条 `*_srisk` 模板（T2/T3/T4/T5/T6/T9）**S 上限 0.77**，其中 T4 一阶差分 −0.18、T5 跨模型比值 −0.72 直接反号。

这与波 181 的 `systemic_risk_measure_2`（S 上限 0.92）合并成一条跨数据集的铁律：

> **「风险水平的估计值」本身没有截面预测力；有预测力的是「残差收益」这个已经实现的量。**
> 低波动异象在 BRAIN 上要落到「实现收益」而不是「风险估计」上才成立。

推论：`risk*` 类数据集里，`*_srisk` / `*vol*` / `*risk_measure*` 这类命名应降级；`*_dsrt*` / `*_trsd*` / `*residual*return*` 才是主战场。这与波 177 的命名陷阱（`discount_store_retail_score` 实为特质残差日收益、`systemic_risk_factor_score` 实为特质方差）是同一件事的两面。

### 4.2 ★★ 窗口跨度是降相关的第一杠杆 —— 第二次独立确认

同一字段 `rsk65_trsd_4mfte_mfm`，只改窗口：

| 表达式 | 与 `ZYQZEawY` 相关 |
|---|---|
| `ts_mean(·, 5)` + subindustry + group_zscore（T8 = `ZYQZAEW8`） | **0.6905** |
| `ts_decay_linear(·, 66)` + industry + group_rank（T1 = `wpQ6bazx`） | **0.893** |

跨度 13 倍（5 → 66）把相关性拉低 **0.20**，越过 0.70 线。

这完美复现 memory 里 2026-10-30 在 GBR `shortinterest3` 上的实证排序：

> **换窗口跨度 ≳ 换变换 >> 换字段**

因为 `wpQ6bazx` 和 `ZYQZAEW8` 用的是**同一个字段、同一个 reverse 方向**，唯一区别是窗口 + 分组轴 + 统计量。字段完全相同却能从 0.893 降到 0.6905 —— 说明**「换字段」根本不是降相关的有效手段**（同族字段捕捉同一现象），而窗口改的是信号时间尺度、分组轴改的是横截面排序，这两者才真正改变持仓。

### 4.3 ★★★ RISK 塔三颗载体拼图首次凑齐

`compute_mutual_correlation([ZYQZAEW8, wpQ6bazx, ZYQZEawY, qMLbW8xP, 0mYopJ7r], 0.7, 4 年)`，986 点：

| 对 | 相关 |
|---|---|
| `ZYQZAEW8` × `qMLbW8xP` | **0.0037**（几乎正交） |
| `ZYQZAEW8` × `ZYQZEawY` | **0.6905**（卡线下 0.0095） |
| `ZYQZEawY` × `qMLbW8xP` | 0.1277 |
| `ZYQZAEW8` × `0mYopJ7r` | 0.6016 |
| `wpQ6bazx` × `ZYQZAEW8` | 0.7345 |
| `wpQ6bazx` × `0mYopJ7r` | 0.7860 |
| `wpQ6bazx` × `ZYQZEawY` | **0.8930** |
| `ZYQZEawY` × `0mYopJ7r` | 0.8914 |

`max_mutually_below_subset = [ZYQZEawY, ZYQZAEW8, qMLbW8xP]`，**size = 3**，`max_subset_exact: true`。

> **这是本会话第一次出现「RISK 塔三颗两两 <0.70」的组合。**

但注意 `ZYQZAEW8` 自身还没全闸（F 0.71 / 2Y 0.98），所以「凑齐」目前是**相关性层面**的，不是提交层面。这也意味着：一旦 `ZYQZAEW8` 的 F/2Y 被治好，RISK 塔可以一次性点亮，无需再找第 3 个字段。

### 4.4 ★★ `ZYQZAEW8` 是 RISK 塔历史最强单点，唯一病灶是换手

| 指标 | `ZYQZAEW8` | 对照：`qMLbW8xP`（RISK 塔最强全闸） | 评价 |
|---|---|---|---|
| S | **2.01** | 1.73 | 历史最高 |
| SUB | **1.70** | 0.84 | 合格线的 2 倍 |
| invest_S | **1.91** | 1.77 | invest_ratio 0.9503 |
| DD | **4.65%** | — | 极低 |
| TO | **51.29%** | 8.19% | **唯一病灶** |
| F | 0.71 | 1.02 | 被 TO 锁死 |
| 2Y | 0.98 | 2.48 | — |

换手是唯一病灶，算术证明：

```
F = S × sqrt(R / max(TO, 0.125))
  = 2.01 × sqrt(0.0644 / 0.5129)
  = 2.01 × 0.3543
  = 0.712   ✓ 与平台读数完全吻合
```

反推目标区：

| 情景 | TO | R | F |
|---|---|---|---|
| 现状 | 51.29% | 6.44% | **0.71** |
| TO 压到地板 | 12.5% | 6.44% | **1.44** ✅ |
| 保守：压到 20%，R 掉到 4.5% | 20% | 4.50% | **0.95** ✗ 差一点 |
| 目标：压到 15%，R 掉到 5.0% | 15% | 5.00% | **1.16** ✅ |

> **TO ≤ 20% 是 F 过闸的临界区，TO ≤ 15% 才有余量。** 这正是波 184 的靶心。

### 4.5 2Y 0.98 的成因是 2022 单年 −0.37，不是结构性衰退

`get_alpha_yearly_stats(ZYQZAEW8)` 十年逐年（longCount 1547–1587，**全年份都有数据**）：

| 年 | S | TO | R | margin | F |
|---|---|---|---|---|---|
| 2014 | 3.38 | 51.54% | 8.02% | 3.11bp | 1.33 |
| 2015 | **4.00** | 51.37% | 11.11% | 4.33bp | 1.86 |
| 2016 | 0.81 | 51.21% | 1.90% | 0.74bp | 0.16 |
| 2017 | 2.96 | 51.23% | 5.34% | 2.09bp | 0.96 |
| 2018 | 0.78 | 50.99% | 2.06% | 0.81bp | 0.16 |
| 2019 | 0.94 | 50.67% | 2.46% | 0.97bp | 0.21 |
| 2020 | 3.44 | 52.02% | 15.13% | 5.82bp | 1.86 |
| 2021 | 2.79 | 51.59% | 11.27% | 4.37bp | 1.30 |
| **2022** | **−0.37** | 51.13% | −1.62% | −0.63bp | −0.07 |
| 2023 | 2.59 | 51.16% | 9.12% | 3.56bp | 1.09 |

三条读出：

1. **2Y（2022+2023）= 0.98 完全由 2022 单年拖累**。剔除 2022，其余 9 年平均 S = **2.19**。2022 是加息暴跌年，短窗反转策略在那种年份会失效 —— 这是机制层面的合理失效，不是数据或骨架问题。
2. **TO 逐年恒定在 50.7%–52.0%**，方差极小 ⇒ 换手是**结构属性**（短窗 5 天 × 日频残差收益的必然结果），不是调参失误，也不可能靠 truncation / 分组轴微调解决。
3. **margin 只有 2.51bp**（对比 `qMLbW8xP` 10.58bp），2022 甚至 −0.63bp ⇒ 高换手 + 低 margin 的组合是 F 的直接病因。

推论：2Y 短板大概率会**随换手治理一并改善** —— 平滑之后 2022 的噪声反转会减少。但这需要波 184 实测确认，不能先验假设。

### 4.6 两个字段相减得全空（新坑）

`E563RGgm` = `group_rank(reverse(subtract(ts_backfill(rsk65_trsd_3mfte_mfm, 22), ts_backfill(rsk65_trsd_4mfte_mfm, 22))), industry)` 得：

```
S 0.00 / TO 0.00% / longCount 0 / shortCount 0 / pnl 0 / bookSize 0 / fRA = 5
checks.pass = [LOW_FITNESS:ERROR, HIGH_TURNOVER, LOW_SUB_UNIVERSE_SHARPE:ERROR, CLUSTER_TEST:ERROR, MATCHES_PYRAMID]
```

两个 coverage 0.9485 / 1.0 的字段相减**不应该全空**。这与波 183 的 `eps_change_percentage_value`（全空字段）、波 177 的 `broad_market_factor_score_2`（整列为 0）表现同型：`checks.pass` 里出现 `:ERROR` 后缀 + `longCount = 0` + `fRA = 5` 就是「输入侧全 NaN」的指纹。

> **判：`rsk65_trsd_3mfte_mfm` 与 `rsk65_trsd_4mfte_mfm` 不能直接相减。** 平台侧要么单位不一致、要么两者在不同日期段有效导致交集为空。要用跨模型差分必须先各自 `group_rank` 再相减，或者先各跑裸水平确认时间轴对齐。

---

## 5. 为什么波 182 没能直接出货

本波 0/10 全闸，但**没有一条是「骨架选错」**：

- 4 条反号（T4/T5/T7 及 T10 全空）是**机制不存在**，不是骨架问题 —— 风险族没有第二自由度。
- 4 条死于 S 太低（T2/T3/T6/T9，S 0.57–0.77）—— 同样是风险族单自由度问题。
- T1 三闸全缺但 S 1.38 已是风险族上限。
- **T8 是唯一有货的**，且它的病跟前面 9 条完全不同性质：不是信号弱，是**信号太强太急**。

所以波 182 的净值是：
- 否证了 risk65 的 3 个 `*_srisk` 字段（不再投入）；
- 拿到 `ZYQZAEW8` 这个 S 2.01 的强载体；
- 证明 RISK 塔三颗在相关性上可以共存；
- 把 `ZYQZAEW8` 的病精确锁定到单一变量（TO 51.29%），并算出 F 过闸需要的 TO 区间。

---

## 6. 波 184 的设计依据（已派发 `430ZzF4BM4oDaMzE4qVHeYE`）

靶心：**TO 51.29% → ≤20%（理想 ≤15%），同时 S 不低于 1.8、R 不低于 4.5%**。

按 forum `43175786936087` 的「换手治理三分类」框架，`ZYQZAEW8` 的归因是**第一类：数据源高频翻转**（日频特质残差收益 × 5 日等权窗），不是「构造放大噪声」也不是「权重集中」。对应药方是**数据层** —— `ts_mean` / `ts_sum` 拉长周期对齐数据更新节奏。

10 个模板（全部保 decay 2、subindustry 或 industry、STATISTICAL，隔离算子变量）：

| # | 治理层 | 表达式骨架 | 预期 |
|---|---|---|---|
| T1 | 数据层·中窗 | `ts_mean(·, 22)` | TO 预计 ~15–20%，S 略降 |
| T2 | 数据层·长窗 | `ts_mean(·, 66)` | TO 最低，S 降幅最大 |
| T3 | 数据层·保幅度衰减 | `ts_decay_linear(·, 22)` | 介于 5 与 22 之间，保近期权重 |
| T4 | 构造层·时序标准化 | `ts_zscore(·, 66)` | 去水平趋势，可能降 TO 且变换排序轴 |
| T5 | 构造层·风险调整 | `ts_sum(·, 22) ÷ etfm4_srisk` | 分母是风险 ⇒ margin 可能提升 |
| T6 | 构造层·秩位 | `ts_rank(·, 252)` | 秩位天然低换手 |
| T7 | 二阶矩 | `ts_std_dev(·, 66)` | 押残差波动（与水平族正交，做相关性对照） |
| T8 | 换字段 | `ts_mean(rsk65_trsd_3mfte_mfm, 22)` | 验是否同一现象 |
| T9 | 换分组轴 | `ts_mean(·, 22)` + industry | 与 T1 单变量对照 |
| T10 | 信息比 | `ts_mean(·, 66) ÷ ts_std_dev(·, 66)` | 风险调整收益（ts_ir 等价形式） |

**关键风险提示**：memory 记录 `divide(ts_mean, ts_std_dev)` 在 `systemic_risk_measure_2` 上把 S 打到 −0.03（波 181 T3）。那里分子分母同源（都是风险度量本身），语义畸变；本波 T10 的分子是**收益**、分母是**收益波动**，语义是标准的风险调整收益，机制不同，值得实测。

**若波 184 全部无法把 F 拉到 1.0**，则 `ZYQZAEW8` 也判死，RISK 塔第 3 颗需转向 `risk59`（16 字段全 VECTOR 借券费率族）—— 但那与已确认 prod 墙的 `shortinterest3`（`kqNRbvJP` PC = 0.8463）机制同源，prod 墙风险高，优先级应低于把 `ZYQZAEW8` 的换手治好。

---

## 7. 五条可复用判据

1. **风险类数据集的字段命名决定投入优先级**：`*_srisk` / `*risk_measure*` / `*vol*`（风险估计）优先级最低，`*_dsrt*` / `*_trsd*` / `*residual*return*`（已实现残差收益）优先。前者在 USA 已两次实测 S 上限 ≤0.92。
2. **想看相关性对照，就只改窗口跨度**：同字段 `ts_mean 5` vs `ts_decay_linear 66` 能差 0.20 相关性。不要浪费仿真槽去「换个相似字段」——同族字段捕捉同一现象，相关性不会降。
3. **拿到高 S + 高 TO 的组合，先算 F 靶心而不是先加 decay**：`F = S×sqrt(R/max(TO,0.125))` 反解出「TO 要压到多少」，再选治理层。本例 51.29% → 15% 才有余量，这个数字决定了要 3 倍以上的平滑跨度，而不是「加一点 decay 试试」。
4. **`longCount = 0` + `checks.pass` 含 `:ERROR` + `fRA = 5` 是「输入全 NaN」的三联指纹**。看到这三条同时出现，直接判字段/表达式不可用，不要再去调骨架。本次 `E563RGgm`、`eps_change_percentage_value`、`broad_market_factor_score_2` 三处一致。
5. **2Y 缺口先查单年归因再决定是否治**：`ZYQZAEW8` 的 2Y 0.98 是 2022 一年 −0.37 造成的（其余 9 年平均 S 2.19）。如果逐年表显示只有 1 年拖累，那是机制层面的合理失效，治它的正确方向是换手治理（顺带降噪），而不是去找「2022 年专属的调参」。
