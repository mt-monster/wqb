# news18 · Ravenpack News Data（KOR / TOP600 / Delay=1）

> 画像日期 2026-10-30 | 数据源：`get_datasets` + `get_datafields(filter_sharpe=false)` 实测
> 状态：**十年覆盖合格（2014–2023 全期有仓）**，机制层面出现符号翻转，见 §4

## 1. 数据集级读数

| 指标 | 值 |
|---|---|
| category | news |
| coverage | 0.5709 |
| fieldCount | 29（平台实取 29/29，complete=true） |
| userCount | 293 |
| alphaCount | 1012 |
| valueScore | 2 |
| pyramidMultiplier | 1.6 |

## 2. 字段全表（29）

### 2.1 ★ 三主题 × 三尺度矩阵（全 MATRIX，coverage 恒 0.5）

| 概念 | business | earnings | revenue |
|---|---|---|---|
| `rp_nip_*` 新闻影响投射 | aC 124 / uC 43 | aC 19 / uC 13 | aC 19 / uC 11 |
| `rp_ess_*` 事件情绪 | aC 111 / uC 43 | **aC 237 / uC 105** | aC 37 / uC 29 |
| `rp_css_*` 复合情绪 | aC 170 / uC 70 | aC 51 / uC 37 | aC 69 / uC 27 |

**画像结论**：这是本区唯一「同数据集 × 同主题 × 多尺度」的完整面板，天然适配 KOR 冠军配方
（`divide` 比值 / `subtract` 价差 → `group_rank` → `hump`），无需跨数据集组腿即可成 ATOM。

### 2.2 VECTOR 族（需 `vec_avg` / `vec_sum` 降维）

| 字段 | coverage | aC | 含义 |
|---|---|---|---|
| `nws18_nip` | .6339 | 22 | 叙事冲击分 [-1,1]，估新闻未来两小时的市场影响 |
| `nws18_qep` | .6339 | **59** | 股票情绪极性（正/负词，-1/0/+1） |
| `nws18_qcm` | .6339 | 40 | 高置信相关新闻情绪 |
| `nws18_acb` | .6339 | 31 | 公司行动公告情绪 |
| `nws18_ssc` | .7006 | 20 | 复合情绪分 -1~+1 |
| `nws18_sse` | .4845 | 18 | 实体-事件连续情绪 -1~+1 |
| `nws18_bee` | .7006 | 15 | 财报评估 -1/0/+1 |
| `nws18_bam` | .7006 | 13 | 并购情绪 |
| `nws18_qmb` | .7006 | 12 | 社论/评论立场 |
| `nws18_ghc_lna` | .6339 | 3 | 分析师推荐变化 |
| `nws18_ber` | .7006 | 4 | 财报发布标记 |

元数据类（低价值）：`nws18_relevance`、`nws18_event_relevance`、`nws18_event_similarity_days`、
`story_event_record_count`、`entity_country_iso_code_4`、`reporting_period_*`（4 个时间戳）。

## 3. 机制映射（双通道取证）

### 3.1 已测：事件情绪 vs 复合情绪背离

- **表述**：`rp_ess_X − rp_css_X`（同一主题的事件层情绪减去全量复合情绪）
- **机制**：事件层情绪比整体新闻基调更正面 ⇒ 该事件尚未被整体基调吸收 ⇒ 后续修复上涨
- **方向句**：背离为正 ⇒ 未来数周正漂移
- **形态**：`hump(group_rank(ts_mean(subtract(...), 22), sector), hump=0.003)`
- **合规**：同数据集、单一经济含义的 `subtract`（非混信号）

### 3.2 论坛实证（通道 A，post `40847481080087`，94 赞 / 22 评论）

> "相关性算子 + FAST neutralization 的组合比较适合处理 sentiment 的数据"
> "nip(news impact projection) 字段在相关性模版下面经常有不错的表现"
> "相关性算子 + FAST neutralization + nip 字段，在 EUR 地区的 D0/D1 出 PPA 还是非常容易的"
> 评论建议对比短窗（10/20d）与长窗（120d），并用 alpha_count / user_count 查拥挤度

模板：`ts_corr(fld, returns, ndays)` / `ts_covariance` / `ts_regression(returns, fld, ndays, lag=0, rettype=2)`

### 3.3 极性配对（通道 A，post `39845230299927`，73 赞）

> 同一底层概念但**相反效价**的字段对（positive vs negative sentiment、bullish vs bearish、
> increase vs decrease counts）配合低 PC 目标使用。

本集可落地的极性对：`nws18_qep`（极性）配 `nws18_nip`（有符号冲击）→ `multiply(qep, nip)` 带符号冲击。

## 4. 实测记录

### wave 197（2026-10-30，STATISTICAL / decay 4 / trunc 0.08 / TOP600）

| leg | alpha | S | F | 2Y | TO |
|---|---|---|---|---|---|
| ess−css earnings | `MPY9N7pn` | 0.46 | 0.16 | −0.69 | .2157 |
| 反号 | `zq3XnkmX` | −0.63 | −0.26 | +0.45 | .2155 |
| ess−css business | `A1Vq8eYw` | 0.07 | 0.01 | 0.12 | .1500 |
| ts_corr(nip, returns, 20) | `LLMOYEq2` | −0.11 | −0.02 | −0.05 | .2498 |

**十年覆盖**：`MPY9N7pn` 2014 年 long/short 各 290 / 290，2014–2023 无空年 ⇒ **通过**。

**逐年 S（正向腿）**

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|
| **2.11** | **2.20** | 1.21 | 0.48 | 0.51 | 0.02 | 0.46 | −0.81 | −0.83 | −0.56 |

**判读**：这是**机制性符号翻转**，不是强度不足——
- 2014–2016 强正（S 2.1~2.2）
- 2017–2020 衰减到 0.0~0.5
- 2021–2023 反号（−0.56~−0.83），且反号腿完全镜像（2014 −2.68 → 2022 +0.77）

⇒ 两个方向都不稳定，按 `wq-brain-ra-kor` 决策表「近年 S 断崖 ⇒ 换 regime 无关的机制」，
**禁扫 decay / 窗口 / 平滑救援**。

**换手率**：四条腿 TO .15~.25，高于 KOR 冠军甜区 .075~.136 ⇒ `hump=0.003 + ts_mean(22)`
不足以压到甜区，后续需 `ts_decay_linear` 长窗或上调 hump。

### wave 199（计划，待跑）

`ts_corr(rp_nip_business, returns, {10,60})` + `ts_corr(vec_avg(nws18_nip), returns, 20)`，
**中性化改 FAST**（论坛原文条件），补完 §3.2 模板的公平测试。
跨类 news+PV 累计用量：wave197 一条 + wave199 三条 = **4/5**。

## 5. 边界与陷阱

- `rp_*` 矩阵族 coverage 恒 0.5（仅半数 TOP600 有新闻覆盖）⇒ `nanHandling=OFF` 下
  `divide` 的缺数会传染，须 `add(denominator, 0.0001)` 且不要对分母做 `ts_backfill`（事件型）。
- VECTOR 族必须 `vec_avg` / `vec_sum` 降维后再进 `ts_*`（本集 `ts_backfill` 不支持事件型输入）。
- `nws18_nip` 与 `rp_nip_*` 是两个不同产品线（VECTOR 叙事冲击 vs MATRIX 影响投射），
  不可当作同一字段的两种表示互换。

## 6. 「≥5 模板 + 每模板完整梯度」补齐战役（2026-11-22）

> 达标标准见记忆 `imbalance-news-template-gradient-compliance-20261122`。全部 KOR/TOP600/D1/INDUSTRY/decay4/trunc0.08。
> 证据闸：论坛双帖（§3.2/3.3）已在档案；论文多样证 PASS（18 篇/15 作者，含 Pacific-Basin Finance 2025《MFA RPC news sentiment and stock returns》直接对口本集 RavenPack + JPM 2024 Four-Fold News Sentiment）。

### 6.1 五模板定义（互异经济机制）
| 模板 | 机制 | 主字段 |
|---|---|---|
| T1 事件情绪背离 | 事件层减复合层情绪（未吸收→修复） | `rp_ess_X − rp_css_X` |
| T2 复合情绪水平 | 全量新闻基调水平 | `rp_css_earnings/business` |
| T3 nip 相关性 | 新闻冲击与收益相关性（论坛冠军模板） | `ts_corr(vec_avg(nws18_nip),returns,n)` |
| T4 极性配对 | 情绪极性×有符号冲击 | `multiply(vec_avg(qep),vec_avg(nip))` |
| T5 财报评估 | 财报事件评级/事件情绪 | `nws18_bee` / `rp_ess_earnings` |

### 6.2 L1 外层截面全类别替换（逐模板推进）
| 模板 | wave | 最优 | S | 2Y | 判 |
|---|---|---|---:|---:|---|
| T1 | `s2_news18_T1_esscss_L1_d1` | `VkNeEOWb` `ts_decay_linear(rank(ess−css_earnings))` | 0.46 | −0.32 | 全臂 CW=0.5 FAIL，符号翻转复现（§4）；无近闸 |
| T2 | `s2_news18_T2_csslevel_L1_d1` | `P05KlNkq` `group_rank(css_earnings)` | 0.20 | −0.47 | 全臂 CW=1.0 FAIL，复合情绪水平无定价力 |
| T3 | `s2_news18_T3_nipcorr_L1_d1` | `e7aEqOKM` `ts_corr(nip,returns,60)` | **0.68** | 0.38 | 本集 L1 最高 S（差 0.90）；论坛冠军模板在 KOR/D1 远不及 EUR，且 eff=2（PV+NEWS 混塔） |
| T4 | `s2_news18_T4_polarity_L1_d1` | `d5avEbXX` `-rank(qep×nip)` | 0.46 | 0.26 | 正号极性配对全负（S−0.62），反号转正⇒带极性冲击是反向信号；仍 0 全闸 |
| T5 | `s2_news18_T5_earnings_L1_d1` | **`npar371d`** `rank(ts_mean(ess−css_earnings,66))` | **1.02** | 0.59 | ★全轮首个 near：F0.74/TO0.0586/subU0.78/RN0.86/checks.fail 空；长窗66把T1(窗22,S0.46)抬到S1.02，窗口轴是明确杠杆 |

**★T5 near 臂 `npar371d` 余量表**：S1.02(差0.56)/F0.74(差0.26)/2Y0.59(差0.99)/TO0.0586(远低于floor)/subU0.78/RN0.86/CW过。三缺口（S/F/2Y），2Y 最厚。L2 内层全类别替换在飞（`3Pcn5O4xZ5dA91615Ohbsn0h`），验证长窗66是否最优。

### 6.3 L2 内层时序全类别替换（逐模板推进）
| 模板 | wave | 内层替换最优 | S | L1→L2 Δ | 判 |
|---|---|---|---:|---|---|
| T1 | `s2_news18_T1_esscss_L2_d1` | `58JYOVbo` `ts_mean(44)` / `blaAq3Zr` `rank@66` | 0.69 / 0.53 | 0.46→**0.69 (Δ+0.23)** | business 主题长窗抬升（窗44 S0.69/2Y0.54；窗66 rank S0.53/2Y0.91），内层 decay/av_diff/delta/zscore/裸全崩(TO1.3-1.4) |
| T2 | `s2_news18_T2_csslevel_L2_d1` | `0mP5M99r` `group_rank@66` | 0.34 | 0.20→0.34 | 全臂 |S|≤0.34，复合情绪水平无定价力，内层收敛 |
| T3 | `s2_news18_T3_nipcorr_L2_d1` | `N1P8blkp` `group_rank@ts_corr60` | 0.69 | 0.68→0.69 | 窗轴40/60甜点，全部 eff=2（PV+NEWS 混塔）；2Y/SUB 主墙，内层收敛 |
| T4 | `s2_news18_T4_polarity_L2_d1` | `XgaMWJWb` 裸反号配对 | 0.48 | 0.46→0.48 | TO1.19 超闸；长窗 44/126 压 TO 到 0.04–0.08 但 S≤0.34；2Y 主墙（7/8），内层收敛 |
| T5 | `s2_news18_T5_earnings_L2_d1` | `rK78Wjn8` `ts_mean(44)` / `e7aErzZd` `group_rank@66` | 1.10 / 1.02 | 1.02→**1.10 (Δ+0.08)** | 内层 ts_mean 守擂（窗44 S1.10/F0.87/2Y0.22；窗66 S1.02/2Y0.37），decay/av_diff/delta/zscore/裸全崩(TO0.7-0.8)；**S↔2Y 跷跷板**，2 near |

**T5 L2 定格**：窗44 抬 S 到 1.10 但 2Y 掉到 0.22；窗66（L1 npar371d）S1.02/2Y0.59 是 S/2Y 最佳平衡。三缺口 S(0.48)/F(0.26)/2Y(0.99)，2Y 最厚；按余量表非 near-gate（三缺口），不值得继续调参。

### 6.4 收口判定（2026-11-22）
**news18 已满足「≥5 模板 + 每模板完整梯度」**：T1–T5 × (L1 外层全类别 8 臂 + L2 内层全类别 8 臂) = 10 wave / 80 臂，全部入库。
- **0 全闸**：全集最高 S1.10（T5 L2 `rK78Wjn8` 窗44，但 2Y0.22）；最佳平衡 `npar371d`/`e7aErzZd` S1.02/2Y0.37–0.59。
- **主墙 = S↔2Y 跷跷板 + CW**：T5 事件情绪背离长窗抬 S 必压 2Y（窗44 S1.10/2Y0.22 ↔ 窗66 S1.02/2Y0.59），三缺口无法同时补；其余 T1–T4 S≤0.69。
- **机制性符号翻转复现**（§4）：2014–16 强正/2021–23 反号，两方向都不稳定，按 KOR 决策表禁扫 decay/窗口救援；本轮 L2 内层全类别替换再次确认该结论。
- **T3 nip 相关性全部 eff=2（PV+NEWS 混塔）**，且 KOR/D1 表现（S≤0.69）远不及论坛 EUR 案例；论坛冠军模板不可跨区外推。
- **不判死**：记「梯度证据完整、信号层弱 + regime 断裂」，需外部新机制才可能翻案；不得外推其它 news 集。
- 证据闸：论坛双帖（§3.2/3.3）+ 论文多样证 PASS（18 篇/15 作者，含 Pacific-Basin Finance 2025 对口本集数据）。

（后续模板梯度收敛后继续追加，不覆盖）
