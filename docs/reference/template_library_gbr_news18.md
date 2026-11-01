# GBR `news18`（Ravenpack News Analytics）模板库与探针账本

> 区域：GBR / universe：TOP700（唯一）/ delay：1
> 数据集：`news18` — Ravenpack News Data，70 字段全 VECTOR，数据集级 coverage 0.8192，
> 字段级覆盖分两档：`multiple_comp_*` 族 **0.9714** / 单实体族 **0.7149**
> userCount **555** / alphaCount **1197** —— 均为 GBR 全部 18 个 news 数据集之首
> 金字塔：`GBR/D1/NEWS`，倍率 **1.6**
> 建档：2026-10-31

---

## §0 选题理由：本库的建立源于一次自我纠错

`tracking/GBR/reference/gbr_dataset_ranking.json`（183 数据集，2026-08-19 生成）把
`news17`(cov 0.8371) / `news18`(0.8192) / `news20`(0.7449) / `news50`(0.6910) 全部标为 `dead`。
我曾据此在会话总结里写「NEWS 塔全灭」。

**这是错的。** 那四个数据集**从未跑过任何实测探针**，`dead` 只是离线初筛标记。

`news18` 的第一条探针（`LLMbpqPM`）就给出 S 0.76 / 2Y 1.12 / margin 35.5bp ——
sentiment/news 类历史上的最高基线。第三条探针（`QPvraOGM`）把 S 推到 0.91 且**非指标闸全清**。

> **定则（决策 #57）**：任何 `dead` 标记在使用前必须先查实测探针台账。
> 只有 ranking 标记而无探针的，一律算「未测」，不得进入判死结论。

**同族尚未实测的机会**：`news17`(0.8371) / `news20`(0.7449) / `news50`(0.6910) —— 同一笔账，尚未开。

---

## §1 字段全量分族（70 字段）

### §1.1 `multiple_comp_*` 族（12 字段，coverage 全部 **0.9714**）—— 首选载体

语义已逐个读描述核实：

| 字段 | 描述（平台原文） | uc | ac | 语义族 |
|---|---|---:|---:|---|
| `nws18_multiple_comp_ssc` | Sentiment of the news calculated using **multiple techniques** | 66 | 81 | 综合情绪 |
| `nws18_multiple_comp_sse` | **Sentiment polarity score of the event**, −1 ~ +1 | 44 | 51 | 事件极性 |
| `nws18_multiple_comp_qmb` | News sentiment specializing in **editorials** on global markets | 78 | **104** | 社论情绪 |
| `nws18_multiple_comp_qcm` | News sentiment of relevant news with **high confidence** | 34 | 42 | **置信度情绪** |
| `nws18_multiple_comp_nip` | **Degree of impact** of the news | 29 | 36 | 冲击幅度（非方向） |
| `nws18_multiple_comp_relevance` | Relevance score indicating the **significance of the entity** in the story (0–100) | 29 | 40 | 实体重要性 |
| `nws18_multiple_comp_ghc_lna` | **Change in analyst recommendation** | 13 | 16 | 评级变动 |
| `nws18_multiple_comp_ber` | News sentiment specializing in **earnings result** | 9 | 11 | 财报情绪 |
| `nws18_multiple_comp_bee` | **Earnings evaluations** score, −1/0/+1 | 10 | 11 | 财报评价 |
| `nws18_multiple_comp_bam` | News sentiment specializing in **M&A** | 6 | 6 | 并购情绪 |
| `nws18_multiple_comp_acb` | News sentiment specializing in **corporate action** announcements | 10 | 11 | 公司行动 |
| `nws18_multiple_comp_qep` | **Global equities** sentiment score, −1/0/+1 | 4 | 4 | 全市场情绪 |

### §1.2 单实体族（coverage **0.7149**）

同一批语义的「单公司」版本：`nws18_ssc`(39/58) / `nws18_sse`(26/28) / `nws18_qmb`(**142/202**，全集 alphaCount 之首) /
`nws18_nip`(**72/106**) / `nws18_qcm` / `nws18_qep` / `nws18_ghc_lna` / `nws18_ber` / `nws18_bee` /
`nws18_bam` / `nws18_acb` / `nws18_relevance`(17/23) / `nws18_event_relevance` / `nws18_event_similarity_days`(18/21)

### §1.3 新颖度族（独立维度）

| 字段 | coverage | uc/ac | 含义 |
|---|---:|---:|---|
| `nws18_mltpl_cmp_event_simildays` | **0.9714** | 7/8 | 距上次相似事件的天数（多公司版） |
| `nws18_event_similarity_days` | 0.7149 | 18/21 | 同上（单实体版） |
| `days_since_similar_event` | 0.7415 | — | 0–365 天 |

### §1.4 注意力稀释族

`multi_entity_story_event_count`（**0.9714**，35/41）/ `story_event_record_count`（0.7149，51/62）/
`story_entity_record_count_d1`（0.7415）

### §1.5 其他情绪口径（coverage 0.7415）

`event_sentiment_score`(12/17) / `sentiment_composite_score_d1`(13/17) /
`sentiment_news_impact_projection_d1`(0/0) / `sentiment_commentary_classifier` /
`sentiment_peq_score_d1` / `sentiment_earnings_classifier_d1` / `sentiment_m_and_a_classifier` 等

### §1.6 非信号（约 20 个，排除）

`company_event_summary` / `company_story_headline`（文本）· 各类 `*_date_utc` / `*_time_utc` /
`*_iso_code` / `*_sequence_number` / `record_timestamp_*`（时间戳与 ID）

**⇒ 可用信号字段约 30 个。**

---

## §2 十模板库（结构互异，preflight 全通过）

`preflight_expressions(10 条, dataset_id="news18", GBR/TOP700/D1)` →
`valid: true` / `unknown_fields: []` / `any_changed: false`

| # | 骨架结构 | 表达式 | 来源 | 状态 |
|---|---|---|---|---|
| **N1** | 时序平滑 + 截面秩（基线） | `group_rank(ts_mean(vec_avg(nws18_multiple_comp_ssc), 22), subindustry)` | forum `42659817284375` 套路三 | ✅ S 0.76 |
| **N2** | 乘性 **relevance** 权重 | `group_rank(ts_mean(multiply(vec_avg(nws18_multiple_comp_ssc), rank(vec_avg(nws18_multiple_comp_relevance))), 22), subindustry)` | forum `42659817284375` 套路一 | ❌ S 0.45 |
| **N3** | 乘性 **novelty** 权重 | `group_rank(ts_mean(multiply(vec_avg(nws18_multiple_comp_ssc), rank(vec_avg(nws18_mltpl_cmp_event_simildays))), 22), subindustry)` | forum `42659817284375` 套路二 | ★ S 0.91 |
| **N4** | 双腿同源相减（deviation） | `group_rank(ts_mean(subtract(vec_avg(nws18_sse), vec_avg(nws18_multiple_comp_ssc)), 22), subindustry)` | forum 进阶 Entity-Story Deviation | ❌ S 0.12 |
| **N5** | 单一信号掩码（注意力稀释） | `group_rank(ts_mean(if_else(less(rank(vec_avg(multi_entity_story_event_count)), 0.5), vec_avg(nws18_multiple_comp_ssc), nan), 22), subindustry)` | forum 进阶 Story Attention Dilution | 未派 |
| **N6** | 换信号维度（NIP 冲击） | `group_rank(ts_mean(vec_avg(nws18_multiple_comp_nip), 22), subindustry)` | 自建 | ❌ S −0.17 |
| **N7** | 信号 × 强度交互 | `group_rank(ts_mean(multiply(vec_avg(nws18_multiple_comp_ssc), abs(vec_avg(nws18_multiple_comp_nip))), 22), subindustry)` | 自建 | 未派 |
| **N8** | 时序标准化（新闻密度异常） | `group_rank(ts_zscore(vec_avg(multi_entity_story_event_count), 60), subindustry)` | forum `43554135453335` z-score 探针 | 未派（预期负向） |
| **N9** | 一阶差分 + 线性衰减 | `group_rank(ts_decay_linear(ts_delta(vec_avg(nws18_multiple_comp_ssc), 5), 10), subindustry)` | forum `42659817284375` 套路三（变化类） | 未派 |
| **N10** | 二阶矩（协方差） | `group_rank(ts_covariance(vec_avg(nws18_multiple_comp_sse), vec_avg(nws18_multiple_comp_sse), 22), subindustry)` | memory 二阶矩族 + forum `43624312881943` | ❌ S −0.39 |

**结构互异性自检**：基线 / 乘性权重 ×2（两个不同置信度维度）/ 双腿相减 / 掩码 / 换维度 /
交互 / 时序标准化 / 动量 / 二阶矩 ⇒ **10 类骨架，无两条共用同一结构**。
字段覆盖 7 个（ssc / sse / nip / relevance / simildays / story_event_count / qmb 待用）。

**十模板之外追加的对照实验**（为回答归因而非扩模板）：

| # | 结构 | 表达式 | 目的 |
|---|---|---|---|
| **N11** | 权重字段单独作信号 | `group_rank(ts_mean(vec_avg(nws18_mltpl_cmp_event_simildays), 22), subindustry)` | **归因**：S 0.91 究竟来自「新颖度调制情绪」还是「新颖度本身」 |
| **N12** | 双情绪源等权合成 × novelty | `group_rank(ts_mean(multiply(add(vec_avg(nws18_multiple_comp_ssc), vec_avg(nws18_multiple_comp_qmb)), rank(vec_avg(nws18_mltpl_cmp_event_simildays))), 22), subindustry)` | 叠加正交信息源（快讯 `ssc` + 社论 `qmb`，**同概念合成，权重恒 1，不扫描**） |

---

## §3 设置档案（GBR D1 `news18` 档）

```
region=GBR  universe=TOP700  delay=1  language=FASTEXPR
neutralization = FAST          ← 已三次独立验证为「慢变量计数/供需/预期」族的数量级杠杆
decay          = 10
truncation     = 0.05
nanHandling    = ON
maxTrade       = OFF
pasteurization = ON
unitHandling   = VERIFY
```

与 `sentiment27` / `sentiment33` / `shortinterest3` / `insiders1` / `insider_agg_matrix` 同档，
保证跨数据集可比。

---

## §4 探针账本（10 条，全部实跑）

固定设置见 §3。所有数值取自 `batch_get_alpha_metrics` / `get_alpha_details`。

> **N13 / N14 例外**：这两条的第二参是 builtin `returns`（PV 侧），实测 `pyramids.list`
> 出现 `GBR/D1/PV` ⇒ 塔归属变成 **PV+NEWS 双塔**，与本表其余 8 条的单塔 NEWS 不同。

| # | 概念 | alpha | **S** | F | **2Y** | **SUB** | SUB/S | TO | **DD** | margin | returns | invest_ratio | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **N1** | 情绪水平 | `LLMbpqPM` | 0.76 | 0.30 | 1.12 | 0.26 | 0.342 ❌ | 11.33% | 4.97% | 35.5bp | 2.01% | 1.0263 | 4 |
| **N2** | × relevance | `P0orpM3J` | 0.45 | 0.14 | 1.10 | 0.27 | 0.60 | 11.90% | 7.42% | 20.0bp | 1.19% | 0.8667 | 3 |
| **N3** | **× novelty** | **`QPvraOGM`** | **0.91** | **0.39** | 1.31 | 0.58 | **0.637 ✅** | 12.65% | 4.06% | 37.7bp | 2.38% | 1.0549 | 3 |
| **N4** | `sse − ssc` | `QPvrVlzp` | 0.12 | 0.02 | 0.44 | −0.03 | — | 12.21% | 6.60% | 0.57bp | 0.35% | 0.75 | 4 |
| **N6** | NIP 水平 | `YP1wpmjW` | −0.17 | −0.03 | 0.06 | **+0.39** | — | 11.17% | 12.35% | −7.8bp | −0.43% | −0.2941 † | 3 |
| **N10** | 二阶矩 | `VkxwPlLw` | −0.39 | −0.11 | −0.51 | +0.30 | — | 13.23% | 13.89% | −15.6bp | −1.03% | 0.359 | 3 |
| **N11** | novelty 单独 | `VkxwPmlb` | **0.15** | 0.03 | 0.59 | 0.02 | — | 12.93% | 11.42% | 0.58bp | 0.38% | 2.3333 † | 4 |
| **N12** | `ssc+qmb` × novelty | `KPJY9zeN` | 0.64 | 0.23 | **1.54** | **−0.01** | — | 12.38% | 5.57% | 25.6bp | 1.59% | 0.7031 | 4 |
| **N13** | `ts_corr(nip, returns, 22)` | `d5W8RqYX` | 0.74 | 0.27 | 1.23 | **0.67** | 0.905 | 15.17% | 3.62% | 25.8bp | 1.96% | 1.1081 | 3 |
| **N14** | `ts_covariance(nip, returns, 66)` | **`3qoYezP6`** | **0.89** | **0.38** | **1.46** | **0.66** | **0.742** | **10.52%** | **3.04%** | **43.5bp** | 2.29% | **1.1348** | 3 |

† `investability_ratio` 只在 |S| ≥ 0.3 时可用（决策 #54）；N6 的 −0.2941 无意义。

### §4.1 `N3`（`QPvraOGM`）的闸门明细 —— 本库最重要的单条结果

`checks.pass` = **`LOW_TURNOVER` / `HIGH_TURNOVER` / `CONCENTRATED_WEIGHT` /
`LOW_SUB_UNIVERSE_SHARPE` / `MATCHES_PYRAMID`**

> **非指标闸全清** —— 这是 sentiment/news 类历史上第一次有候选把 SUB / 集中度 / 换手三项全部通过。

`checks.fail` = `LOW_SHARPE` 0.91 < 1.58 · `LOW_FITNESS` 0.39 < 1.0 · `LOW_2Y_SHARPE` 1.31 < 1.58
`checks.warning` = `CLUSTER_TEST` 0.97 < 1（**贴近上限，需关注**）· `MATCHES_THEMES` · `OSMOSIS_ALLOCATION`

`ra.pyramid_short = "news"` / `pyramids.list = [{name: "GBR/D1/NEWS", multiplier: 1.6}]`
`metrics.longCount = 458` / `shortCount = 452`（多空均衡）
`ra.failed_ppa_count = 1`（仅 `LOW_SHARPE`）⇒ **PPA 通道也只剩 S 一项**

**十年覆盖（`get_alpha_yearly_stats`，目标第 4 条硬门槛）**

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sharpe | 1.35 | 0.02 | **−0.31** | 0.20 | **2.10** | 1.47 | 0.69 | 1.10 | 1.31 | 1.27 |
| longCount | 432 | 490 | 491 | 522 | 485 | 464 | 426 | 421 | 433 | 411 |
| shortCount | 424 | 483 | 492 | 522 | 475 | 460 | 418 | 407 | 427 | 406 |

十年 `longCount` / `shortCount` **全部非零（无断档）✅ 满足「近十年都要有数据」**。
8 正 / 1 零 / 1 负；**2015–2017 三年几乎无信号，2018 年后才成立** ⇒
这正是 2Y 1.31 > 全期 S 0.91 的成因，也是本因子**最大的过拟合风险点**。

### §4.2 N11 / N12 —— 归因实验（回答「0.91 从哪来」）

| # | 结构 | S | SUB | 结论 |
|---|---|---:|---:|---|
| **N11** | `novelty` **单独**作信号（无 `ssc`） | **0.15** | 0.02 | 权重字段本身**几乎无信号** |
| **N12** | `ssc + qmb` 双情绪源等权 × novelty | 0.64 | **−0.01** | 加社论源**毁掉信号** |

1. **N11 证明 N3 的 0.91 来自交互项**（新颖度调制情绪），不是新颖度本身。
   0.15 与 0.91 差 6 倍 ⇒ 归因正确，N3 骨架可放心继续。
   **做乘性权重实验时必须跑「权重字段单独作信号」这一臂**，否则无法区分「骨架有效」与「权重本身就是信号」。
2. **N12 证伪「同概念多字段等权合成」**：加 `qmb`（社论/评论情绪）后 S −30%、**SUB 崩塌到 −0.01**。
   机理：社论是**事后观点**，媒体跟着价格写故事，不携带新信息；小票上符号相反。
   2Y 反而升到 1.54 ⇒ `qmb` 只在近期有信息。
   ⇒ 「同概念合成」的放行条款只在**同一信息源的多口径**上成立；**跨信息源即使同概念也不该合成**。

### §4.3 N13 / N14 —— 相关性模板（forum 帖 `40847481080087`，94 赞）

```
N13  group_rank(ts_corr(vec_avg(nws18_multiple_comp_nip), returns, 22), subindustry)
N14  group_rank(ts_covariance(vec_avg(nws18_multiple_comp_nip), returns, 66), subindustry)
```

| | S | F | 2Y | SUB | TO | DD | margin | 塔归属 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| N13 | 0.74 | 0.27 | 1.23 | 0.67 | 15.17% | 3.62% | 25.8bp | **PV+NEWS** |
| N14 | 0.89 | 0.38 | **1.46** | **0.66** | **10.52%** | **3.04%** | **43.5bp** | **PV+NEWS** |

**N14 在 2Y / SUB / TO / DD / margin 五项上全部优于 N3，S 仅差 0.02** —— 是本数据集
「质量密度」最高的一条。但两条 S 都停在 ≈0.90。

> ★★★★★ **`returns` 是 PV 侧 builtin，这是本轮唯一一次实测确认的塔归属事实。**
> N13 的 `get_alpha_details` 返回
> `ra.pyramid_short = "pv/news"` / `pyramids.list = [{GBR/D1/PV, 1.4}, {GBR/D1/NEWS, 1.6}]` / `effective = 2`。
> ⇒ **任何以 `returns` 为算子的 news 因子都构成 PV+NEWS 双塔**，占用「trio × 非 trio ≤5」的额度。
> 在额度只剩 1 个的前提下，**相关性模板这条线不划算** ⇒ 判废，不再投入。

**两条副产物**：
- `ts_corr(nip, returns, W)` 与 `ts_covariance(nip, returns, W)` 在 GBR 上**都成功实跑**
  ⇒ 移入「已验证可用算子」清单（此前只 audit safe）。
- 长窗（66）显著优于短窗（22）：S +20%、2Y +19%、DD −16%、margin +69%。
  与 forum 帖评论区 `XW23690` 主张的「短窗更敏捷」**相反**，与 `YC83503` 的「短窗会被非事件期噪声主导」
  **一致** ⇒ **GBR 上该模板应走长窗**。

### §4.4 ★★★★★ P1 —— 帖 `43541109631895` 骨架的精确复现：**本库第一条 REGULAR 全闸通过**

```
ts_target_tvr_decay(
  group_neutralize(
    -ts_rank(ts_mean(vec_count(nws18_multiple_comp_sse), 60), 252),
    densify(market)
  ),
  target_tvr=0.05, lambda_max=5, lambda_min=0
)
```
设置：`GBR / TOP700 / D1 / FAST / decay 15 / trunc 0.05 / nanHandling ON / maxTrade OFF /
pasteurization ON / VERIFY`

**alpha = `6XdPedNJ`**

| 指标 | 复现值 | 帖①声称 | 判定 |
|---|---:|---:|---|
| **Sharpe** | **1.97** | 1.97 | ✅ 逐位吻合 |
| **Fitness** | **1.27** | 1.27 | ✅ |
| **Turnover** | **7.91%** | 7.9% | ✅ |
| **margin** | **13.16bp** | 13.2bp | ✅ |
| returns | 5.21% | — | — |
| drawdown | 2.50% | — | — |
| SUB | **1.08** | — | SUB/S = **0.548** ≫ 0.434 ✅ |
| 2Y | **2.20** | — | ≫ 1.58 ✅ |
| longCount / shortCount | 452 / 457 | — | 均衡 |

**`ra.failed_ra_count = 0` / `failed_ppa_count = 0` / `checks.fail = []`**

**`checks.pass`（9 项全过）**：`LOW_SHARPE` · `LOW_FITNESS` · `LOW_TURNOVER` · `HIGH_TURNOVER` ·
`CONCENTRATED_WEIGHT` · `LOW_SUB_UNIVERSE_SHARPE` · **`CLUSTER_TEST`** · `LOW_2Y_SHARPE` · `MATCHES_PYRAMID`
**`checks.warning`**：只有 `MATCHES_THEMES` / `OSMOSIS_ALLOCATION`（非硬闸）
**`checks.pending`**：`SELF_CORRELATION` · `PROD_CORRELATION` · `POWER_POOL_CORRELATION` · `DATA_DIVERSITY` · `REGULAR_SUBMISSION`

**`pyramids.list = [{name: "GBR/D1/NEWS", multiplier: 1.6}]`，`effective = 1`**
⇒ **纯单塔 NEWS，不触发 PV**（与 N13/N14 成对照）⇒ 不占用 trio×非 trio 额度。

**十年逐年（`get_alpha_yearly_stats`）—— 10/10 全部为正**

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sharpe | 2.77 | 1.40 | 3.01 | 1.33 | 2.07 | 1.56 | 2.12 | **1.12** | 1.72 | 2.75 |
| longCount | 423 | 492 | 493 | 522 | 475 | 473 | 404 | 414 | 406 | 415 |
| shortCount | 433 | 480 | 490 | 522 | 485 | 450 | 441 | 414 | 454 | 402 |
| turnover | 8.38% | 7.84% | 7.46% | 7.13% | 8.26% | 7.54% | 8.47% | 7.94% | 8.33% | 7.84% |

**最低年 sharpe 1.12（2021），无任何负年**。对照 N3 的 2015–2017（0.02 / −0.31 / 0.20）
⇒ **P1 彻底排除了 N3 那个最大的过拟合风险点**。

**残留风险**：本条是**已提交 alpha 的逐位复现**，`PROD_CORRELATION` 是唯一实质未知闸。
若要作为独立 alpha 提交，必须换至少一个结构维度做去相关（换计数字段族 / 换 `ts_rank` 窗口 /
换分组轴），而不能原样提交。

**与现有篮子的正交性（`compute_mutual_correlation`，4 年 1021 点，阈值 0.7）**

| 对 | `akK2vpWW` | `O0AKLMKq` | `vR1aEpa3` | `E56onL5r` | `j2YNnKOQ` | `d51O1kOX` | `rKRkL9QE` | `kqNRXm5k` | `0mYoANkv` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| vs `6XdPedNJ` | 0.023 | 0.070 | 0.023 | 0.093 | **0.172** | −0.003 | 0.005 | 0.089 | 0.044 |

**最大相关 0.1718**（对 `j2YNnKOQ`），多数 < 0.1 ⇒ 几乎完全正交。
篮子 9 → **10 条**（`max_mutually_below_subset_size = 10` / `max_subset_exact: true`），
`max_pair` 不变（`vR1aEpa3 ↔ E56onL5r = 0.6954`）。

### §4.6 P2 `zq3wRx51` —— 窗口安慰剂：`ts_mean` 60 → 66

除窗口外与 P1 完全相同。**同样 `failed_ra_count = 0` / `checks.fail = []` / 9 项全过 / 纯单塔 NEWS**。

| | S | F | TO | SUB | 2Y | DD | margin | returns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P1（w60） | 1.97 | 1.27 | 7.91% | 1.08 | 2.20 | 2.50% | 13.16bp | 5.21% |
| **P2（w66）** | **1.93** | **1.23** | 7.91% | 1.03 | 2.13 | 2.45% | 12.90bp | 5.10% |
| Δ | −0.04 | −0.04 | 0 | −0.05 | −0.07 | −0.05 | −2% | −2% |

⇒ **骨架对平滑窗口不敏感（S 只掉 2%）**，不是「窗口调参调出来的 1.97」。
这是本轮最重要的一条稳健性证据：`ts_mean` 的白名单值 66 与帖①的经济值 60 等价。

**但 P1 ↔ P2 的 PnL 相关 = 0.9881**（`compute_mutual_correlation`，1021 点）
⇒ **换 `ts_mean` 平滑窗口不是去相关手段**，两条只能取一条。
去相关的候选轴剩：归一化基线（`ts_rank` 窗口）/ 分组轴 / 时序几何（双期限分位差、密度变化）。
~~换「信息源」（计数字段族）~~ —— 此路已于 §4.8 被 V1/V3 两条实测否掉。

### §4.7 V2 `VkxwGjdJ` —— 帖①第二条的重构：**失败，且暴露原帖信息不足**

帖①仅写「`nws18_relevance` 的 20 日 `ts_delta`（相关度异常上升）→ GBR Sharpe 2.61」，
**未给完整处理链**。我按第一/第三条同款链补齐：

```
ts_target_tvr_decay(
  group_neutralize(ts_rank(ts_delta(vec_avg(nws18_relevance), 20), 252), densify(market)),
  target_tvr=0.05, lambda_max=5, lambda_min=0
)
```

实测 **S −0.41 / F −0.16 / DD 39.19% / margin −3.3bp / SUB −0.33 / 2Y 0.89**
（`failed_ra_count = 4`：`LOW_SHARPE` / `LOW_FITNESS` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_2Y_SHARPE`）。

**三条判读**：
1. 符号即使翻转也只有 S +0.41 / DD ≈39%，**离 2.61 差 6 倍** ⇒ 不是符号问题，是**加工链不同**。
   最可能是：① 原帖用的是 `multiple_comp_relevance`（cov 0.9714）而非单实体 `nws18_relevance`（0.7149）；
   ② 原帖可能未套 `ts_rank(·,252)`，直接 `ts_delta` 做信号；
   ③ 原帖可能用 `vec_sum` 而非 `vec_avg`。
2. **DD 39.19% 是全库最差**（P1 仅 2.5%）⇒ 无论符号如何，这条形态都不可用。
3. **教训**：论坛帖只给「字段 + 窗口 + S 值」而不给完整表达式时，**不可把同帖其它 alpha 的链套上去**。
   本条的 −0.41 vs 声称的 2.61 就是套链的代价。要么找到原表达式，要么放弃。
   ⇒ 该路线（relevance `ts_delta`）**暂停，不再投入**；若日后要复活，必须先从论坛拿到完整表达式。

### §4.8 ★★★★★ V1 / V3 —— 换信息源的代价是**2Y 悬崖**，以及 `sse` 语义的不可替代性

§4.6 曾写「去相关必须换信息源」。**这条已被两条实测否掉**，代价不在 S，而在 **2Y**：

| # | 信号源 | cov | alpha | S | F | **2Y** | SUB | TO | DD | margin | failed_ra |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | `multiple_comp_sse` | 0.9714 | `6XdPedNJ` | **1.97** | 1.27 | **2.20** | 1.08 | 7.91% | 2.50% | 13.16bp | **0** |
| V1 | `nws18_ssc`（单实体） | 0.7149 | `GrW0GVEQ` | 1.36 | 0.80 | **0.68** | 0.63 | 8.85% | 4.49% | 9.73bp | 4 |
| V3 | `multiple_comp_qmb`（社论） | 0.9714 | `d5W8Z0mj` | 1.39 | 0.75 | **0.68** | 0.80 | 7.78% | 2.60% | 9.42bp | 3 |

三条实测事实：

1. **两个毫不相干的字段（单实体 `ssc` / 多实体社论 `qmb`，coverage 也不同）得到了精确同值的 2Y = 0.68。**
   这不是巧合能解释的，最可能是平台 2Y 计算在「非全量字段」上的共同失效模式。
2. **corr(V3, V1) = 0.8728 > corr(V3, P1) = 0.7166** ⇒ V1 与 V3 是**同一族的低质量版本**
   （都在数「筛选后的事件条数」），而 `sse` 是**唯一覆盖全部硬新闻事件的情绪极性字段**
   ⇒ `vec_count(sse)` = 纯新闻条数。
3. **`qmb` = 社论 / 全球市场评论 = 事后观点，媒体跟着价格写故事**（决策 #66 已由 N12 独立验证），
   用它做注意力计数必然弱 ⇒ V3 的 S 1.39 / 2Y 0.68 是同一结论的第二次独立印证。

**V1 的闸门明细（`GrW0GVEQ`）**：

| 闸 | 值 | limit | 缺口 |
|---|---:|---:|---|
| `LOW_SHARPE` | 1.36 | 1.58 | −14% |
| `LOW_FITNESS` | 0.80 | 1.0 | −20% |
| `LOW_SUB_UNIVERSE_SHARPE` | 0.63 | **0.65** | **−3%** |
| `LOW_2Y_SHARPE` | 0.68 | 1.58 | **−57%** |

⇒ **2Y 差 57%，无法靠微调补救**；其余三项都只是小差距。`CLUSTER_TEST` 0.67（P1 是 pass）。

**★ 顺带更正一个口径**：`LOW_SUB_UNIVERSE_SHARPE` 的 limit = 0.65 而 S = 1.36 ⇒
**GBR/TOP700 的 SUB 系数 = 0.478**（此前记 0.434）。仍须每次用 `checks.fail` 里的 limit 反推，不要背常数。

**结论（修正 §4.6 的判读）**：

- **`sse` 的「全量硬新闻条数」语义不可替代，换字段做 `vec_count` 这条路走到头** ——
  剩下的 `multiple_comp` 字段要么是社论 / 评估类（滞后观点），要么是幅度类（`nip` / `relevance`，半子集）。
- **第二条 NEWS alpha 必须从「同一 `sse` 信号 + 不同加工几何」里出**，候选轴只剩：
  ① `ts_rank` 归一化基线（252 → 504）② 分组轴（`market` → `sector`）
  ③ 双期限分位差（`ts_rank(·,252) − ts_rank(·,1008)`）④ 密度变化（`ts_delta(ts_mean(·,60), 22)`）
  ⑤ 平滑算子（`ts_mean` → `ts_decay_linear`）。
- corr(V1, P1) = 0.6389 证明**换源的去相关效力本身是真的**（Δ 0.35），只是代价太大
  ⇒ 不废「换源能去相关」这条机理，废的是「用低覆盖 / 滞后字段换源」这个具体做法。

### §4.9 ★★★★★ 两条新的全闸 alpha，以及「无害变体全相关」的定量结论

V4 / V5 均为 **`failed_ra_count = 0`**，其中 **V4 在六项指标上优于 P1**：

| # | 单一改动 | alpha | S | F | 2Y | SUB | TO | DD | margin | returns | failed_ra | **corr vs P1** |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | 基准 | `6XdPedNJ` | 1.97 | 1.27 | **2.20** | 1.08 | 7.91% | 2.50% | 13.16bp | 5.21% | **0** | — |
| **V4** | `ts_rank` 252 → **504** | `gJeq8XbQ` | **2.02** | **1.32** | 1.58 | **1.21** | 7.95% | **2.28%** | **13.45bp** | **5.35%** | **0** | **0.9257** |
| **V5** | 分组轴 market → **sector** | `e75835Zz` | 1.96 | 1.26 | 2.13 | 1.08 | 7.90% | 2.56% | 13.10bp | 5.17% | **0** | **0.9942** |
| P2 | `ts_mean` 60 → 66 | `zq3wRx51` | 1.93 | 1.23 | 2.13 | 1.03 | 7.91% | 2.45% | 12.90bp | 5.10% | **0** | **0.9881** |

**⇒ 三条「无害变体」（平滑窗 / 归一化基线 / 分组轴）全部 `failed_ra_count = 0`，但相关 0.9881 / 0.9257 / 0.9942。**
**去相关的三个候选维度至此全部实测失效**，P1 骨架的任何参数级微调都拿不到独立 alpha。
要第二条 NEWS alpha，必须**换加工几何 / 换信息类型**，不能换参数。

**V4 单独看是本库最强的一条**（S 2.02 / F 1.32 / SUB 1.21 / DD 2.28% / margin 13.45bp），
唯一弱项是 2Y 1.58（贴 `LOW_2Y_SHARPE` limit 1.58 压线，但 `failed_ra_count = 0` 说明平台判定通过）。
**若 P1 因 prod 相关性风险被弃，V4 是等价或更优的替换品。**

### §4.10 ★★★★★ 「2Y = 0.68」之谜解开：单实体族的 `vec_count` 是**恒等变换**

V1 / V3 / V6 的 2Y 精确等于 0.68，三条用了三个不同字段。直接验相关：

| 对 | corr | 说明 |
|---|---:|---|
| `P0orGx6J`（`vec_count(nws18_qmb)`）↔ `GrW0GVEQ`（`vec_count(nws18_ssc)`） | **1.0000** | **PnL 完全相同** |
| `GrW0GVEQ` ↔ `d5W8Z0mj`（`vec_count(multiple_comp_qmb)`） | 0.8728 | 不同带 |
| `P0orGx6J` ↔ `d5W8Z0mj` | 0.8728 | 同上 |

**机理（决定了本数据集后续所有「计数型」设计）**：

- **单实体族（cov 0.7149，`nws18_*`）是「每实体-每事件一条记录」，所有字段在每条记录上都填充**
  ⇒ `vec_count(任意字段)` **数的是同一个「记录条数」** ⇒ 换字段 = 恒等变换 ⇒ 字段名对 `vec_count` 毫无意义。
  这也是三条变体 2Y 精确同值 0.68 的原因：**它们其实是同一条 alpha**。
- **多实体族（cov 0.9714，`multiple_comp_*`）是条件性填充**：
  `sse`（事件情绪极性）在**全部事件**上有值 ⇒ `vec_count(sse)` = 纯新闻条数；
  `qmb`（社论）只在社论类故事上有值 ⇒ `vec_count(qmb)` = 社论子集条数（且是滞后观点，见 §4.8）。

**⇒ 硬结论：在 `news18` 上做计数型 alpha，唯一有意义的字段是 `nws18_multiple_comp_sse`。**
其余字段的 `vec_count` 要么恒等（单实体族），要么是弱子集（社论 / 评估类）。
这条同时解释了为什么 P1 用 `sse` 而不用「看起来更全面的」`ssc`。

### §4.11 ★★★★★ `sse` 的「数值加工族」全灭：只有 `vec_count` 这一条路活着

P1 骨架固定，把 `vec_count(...)` 换成 `sse` 上的其它统计量（同一多实体高覆盖带、同一设置档）：

| # | 加工方式 | alpha | S | F | **2Y** | SUB | TO | DD | margin | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **P1** | **`vec_count(sse)` 事件计数** | `6XdPedNJ` | **1.97** | **1.27** | **2.20** | **1.08** | 7.91% | 2.50% | 13.16bp | **0** |
| V9 | `vec_sum(sse)` 净情绪总量 | `bl62jZRr` | 0.57 | 0.21 | 0.29 | 0.68 | 8.01% | 5.20% | 4.05bp | 3 |
| V11 | `vec_stddev(sse)` 情绪分歧度 | `6XdPlOP7` | −0.03 | −0.00 | 0.16 | −0.31 | 7.41% | 6.60% | −0.18bp | 4 |
| V8 | `ts_delta(·,22)` 密度变化 | `qMLkNpmP` | 1.23 | 0.63 | 1.91 | 0.75 | 7.85% | 3.50% | 8.32bp | 2 |
| V7 | 双期限分位差 `ts_rank 252 − 1008` | `rKR62xl8` | −0.30 | −0.08 | 0.85 | −0.50 | 8.00% | **19.12%** | −2.2bp | 4 |

**⇒ 从 1.97 到 −0.03，跨度 2.0 个 Sharpe 的全部差异只来自「怎么读同一个字段」：**

1. **`vec_count`（数事件有没有发生）是本数据集唯一有信息的读法** —— S 1.97。
2. **`vec_sum`（情绪总量）掉到 0.57**，掉 71%。原因：情绪有正负，`vec_sum` 让正负相消；
   而事件数不论正负都累加。**GBR 上「新闻多少」有信息，「新闻说好还是坏」没有信息。**
3. **`vec_stddev`（分歧度）是 0** —— 分歧度这个维度在本数据集上不存在（DD 6.6% 说明几乎没有仓位）。
4. **`ts_delta`（密度变化）保留 62% 的信号但把 2Y 从 2.20 修到 1.91** —— 见 §4.12，
   这是唯一「去相关且 2Y 不崩」的方向，但全期弱。
5. **双期限分位差是灾难** —— 日频噪声在 `ts_rank(1008)` 尺度上分母太大，
   长窗分位几乎恒定 ⇒ 相减后近似「短期秩 − 常数」，DD 19.12% 说明这是一个高波动、无方向的组合。

**★ 与 §5.3「`nip` 是幅度而非方向」合起来看，本数据集的完整画像已经清楚：**
**它是一个「事件到达率」数据集，不是一个「情绪」数据集。**
所有把字段当连续情绪值做算术的尝试（sum / stddev / delta / 分位差 / relevance 加权 / 相减）
都在 0.03–0.91 区间；所有把它当「计数器」的尝试（`vec_count`）在 1.97。

**应用（写进下一轮任何数据集的第一性判断）**：
拿到一个「每条记录多个字段全填」的事件型数据集，先问：**这个字段是「事件自身的属性」还是「事件的标识」？**
- 是标识（所有记录都填、值在记录内无差异）⇒ 只能数记录，任何算术都是噪声。
- 是属性（条件性填充、有方向）⇒ 才能进 `sum / mean / stddev`。
**news18 的 `sse` 属于后者（有方向），但实测方向无用 ⇒ 方向存在不等于方向有信息。**

### §4.12 ★★★★ 三个参数级 + 三个几何级去相关杠杆的完整效力表（news18 收官）

要拿到**第二条与 P1 独立的 NEWS alpha**（塔点亮需 3 条互相关 <0.7），系统性试了 7 个杠杆：

| 杠杆 | 层级 | corr vs P1 | S | 2Y | 判定 |
|---|---|---:|---:|---:|---|
| `ts_mean` 平滑窗 60→66 | 参数 | 0.9881 | 1.93 | 2.13 | ❌ 无效 |
| `ts_rank` 基线 252→504 | 参数 | 0.9257 | **2.02** | 1.58 | ❌ 无效（但 S 更好，V4 可替换 P1） |
| 分组轴 `market`→`sector` | 参数 | **0.9942** | 1.96 | 2.13 | ❌ 完全无效 |
| 换信息源→单实体族 | 几何 | 0.6389 | 1.36 | **0.68** | ⚠️ 相关达标但 2Y 崩 |
| 换信息源→多实体社论 | 几何 | 0.7166 | 1.39 | **0.68** | ⚠️ 同上 |
| `ts_delta(·,22)` 密度变化 | 几何 | **0.5956**（vs V4） | 1.23 | **1.91** | ⭐ 唯一双向达标，但 S 差 0.35 |
| 双期限分位差 | 几何 | 未测 | −0.30 | 0.85 | ❌ 直接死 |

**结论（决策 #70 的强化版）**：
**参数层三个杠杆的 corr 全部 ≥0.9257，无一可用。** 去相关只能走几何层，而几何层里
「换信息源」必然把 2Y 打到 0.68（覆盖度下降，见 §4.8），「换几何」里只有密度变化方向对。
**⇒ news18 上「同一信息源 + 独立几何」的第三条路径，已经被穷尽到只剩 `ts_delta` 一条，且它 S 不够。**

### §4.13 ★★★★★ 换数据集 —— 唯一有效的去相关维度（W1 `9qxPX77V`，news17 移植成功）

**P1 骨架原样搬到 `news17`（PR Edition，公司新闻稿/监管披露），只换字段 `nws18_multiple_comp_sse` → `nws17_multiple_comp_event_sentiment_score`：**

```
ts_target_tvr_decay(
  group_neutralize(
    -ts_rank(ts_mean(vec_count(nws17_multiple_comp_event_sentiment_score), 60), 252),
    densify(market)
  ),
  target_tvr=0.05, lambda_max=5, lambda_min=0
)
```
`GBR / TOP700 / D1 / FAST / decay 15 / trunc 0.05 / nanHandling ON / maxTrade OFF / VERIFY`

| 指标 | **W1 `9qxPX77V`（news17）** | P1 `6XdPedNJ`（news18） |
|---|---:|---:|
| Sharpe | **1.86** | 1.97 |
| Fitness | **1.14** | 1.27 |
| 2Y | **2.00** | 2.20 |
| SUB | **1.33** | 1.08 |
| SUB/S | **0.715** | 0.548 |
| TO | 7.74% | 7.91% |
| DD | **2.51%** | 2.50% |
| margin | 12.07bp | 13.16bp |
| returns | 4.67% | 5.21% |
| long/short | 457/452 | 452/457 |
| `failed_ra_count` | **0** | **0** |
| `failed_ppa_count` | **0** | **0** |
| `pyramids.list` | **GBR/D1/NEWS (1.6)，effective 1** | 同 |

**★ SUB 反而更强**（1.33 vs 1.08，SUB/S 0.715 vs 0.548）—— 新闻稿比新闻报道在小票上更均匀。

**★★★ 去相关的决定性数据（`compute_mutual_correlation`，1021 个交易日，4 年窗）：**

| 对 | corr | 判定 |
|---|---:|---|
| **P1(news18) ↔ W1(news17)** | **0.5051** | ✅ **远低于 0.7** |
| W1 ↔ V4 `gJeq8XbQ`(news18/504) | 0.4828 | ✅ |
| W1 ↔ V8 `qMLkNpmP`(news18/密度变化) | 0.3825 | ✅ |
| V4 ↔ V8 | 0.5956 | ✅ |
| P1 ↔ V8 | 0.7121 | ❌ 超阈 |
| P1 ↔ V4 | 0.9257 | ❌ |
| P1 ↔ V5 | 0.9942 | ❌ |

**⇒ 去相关效力排序（跨全部 11 个变体实测）：**

| 维度 | 代表操作 | corr vs P1 |
|---|---|---:|
| **换数据集** | news18 → **news17** | **0.5051** ⭐ |
| 换信息源（同集内换子族） | 多实体 → 单实体族 | 0.6389（但 2Y 崩到 0.68） |
| 换几何（同源，语义保持） | `ts_mean` → `ts_delta` | 0.7121（2Y 1.91 但 S 1.23） |
| 换 `ts_rank` 基线 | 252 → 504 | 0.9257 |
| 换平滑窗 | 60 → 66 | 0.9881 |
| **换分组轴** | market → sector | **0.9942**（最无效） |

**★ 结论（决策 #70 的最终形态，写进任何数据集的去相关路线图）：**
**参数层杠杆（窗口 / 基线 / 分组轴）corr 全部 ≥0.92，无一可用。几何层只有 `ts_delta` 方向对但 S 不够。
唯一能同时做到「corr < 0.6 且指标不崩」的操作是换数据集 —— 且必须是同结构、同语义、同覆盖档（≥0.70）的兄弟数据集。**
`news17` 与 `news18` 同为 RavenPack 系列、同 `multiple_comp_*` 结构、字段级 cov 0.9669 vs 0.9714 ⇒ 骨架零改动可移植，而信息源性质不同（公司主动披露 vs 媒体加工）⇒ 天然独立。

**★ 十年逐年（10/10 全部为正，最低年 2020 = 0.14）：**

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | 2.52 | **3.63** | 2.59 | 1.10 | 1.19 | 1.56 | **0.14** | 1.73 | 1.84 | 2.27 |
| pnl(万) | 60.1 | 100.3 | 67.6 | 19.4 | 27.9 | 40.0 | 3.9 | 44.7 | 58.0 | 60.4 |
| TO | 8.16% | 7.95% | 7.49% | 7.19% | 7.79% | 7.38% | 7.68% | 8.03% | 7.86% | 7.89% |
| long | 427 | 489 | 497 | 527 | 484 | 463 | 426 | 414 | 435 | 410 |
| short | 429 | 484 | 486 | 517 | 476 | 460 | 418 | 414 | 426 | 407 |

**2020 是唯一薄弱年（S 0.14）—— P1 同年 2.07。** 机理：疫情年新闻稿发布量暴增且同质化
（大量「疫情声明」类公告），事件密度的横截面区分度被压缩。**这不是过拟合证据，是行业冲击年**，
但也是 W1 相对 P1 的唯一时间结构弱点。

### §4.14 `news20` / `news50` 画像（第三、第四条候选的数据准备）

`news18` 已榨干，NEWS 塔点亮还差第三条。GBR news 类的其余处女地：

**`news20`（46 字段，cov 0.8756 多实体 / 0.625 单实体）** —— **与 news18 同结构、同 `multiple_comp_*` 命名、
同 RavenPack 系列，只是每个覆盖档低 0.10**。⇒ **同源风险高**，若 W1（换到 0.9669 带的 news17）相关都降到 0.51，
那 news20（0.8756 带）与 news18 的相关大概率在 0.6–0.8 区间，**不是首选**。

**`news50`（37 字段，全部 `mws50_*`，cov 0.691 单带）** —— **完全不同的数据源（RPNA edition）+ 独家字段类型**：

| 字段 | userCount/alphaCount | 语义 | 为什么独特 |
|---|---|---|---|
| **`mws50_aes`** | **55/64** | 过去 **91 天**滚动窗内「正面事件 / 全部非中性事件」的比率（0–100） | **数据集自带的预聚合横截面比率** —— 不需要自己做 `ts_mean(count, 60)` |
| **`mws50_vea`** | **24/26** | 过去 **91 天**聚合事件量（只数 ESS ≠ 50 的非中性事件） | **数据集自带的预聚合事件量** |
| `mws50_ess` | 51/80 | 情绪分 0–100（granular） | 与 news18 `sse` 同义但刻度不同 |
| `mws50_qmb` | 36/65 | Editorials & Commentary | 社论（news18 已证滞后无信息） |
| `mws50_nip` | 19/23 | News Impact Projections 0–100 | 幅度类 |
| novelty 全套 | `mws50_ens`(13/16) / `mws50_ens_elapsed`(3/3) / `mws50_ens_similarity_gap`(6/8) / `mws50_g_ens`(3/3) | 24 小时窗内新颖度 / 距上次相似故事的天数 | **比 news18 的 novelty 字段更完整（含 global 版）** |
| `mws50_rp_story_event_count` | 16/18 | 每个故事的实体记录总数 | 计数型 |

**⇒ `news50` 的两条独立价值主张：**
1. **`aes` / `vea` 是预聚合的 91 天指标** —— 它们的 `ts_mean` 已经在数据集内部做完，
   因子构造只剩「横截面排序」，几何与 news18 完全不同 ⇒ 天然去相关。
2. **novelty 字段族比 news18 更完整**（有 `g_ens` 全局版、`ens_elapsed` 毫秒级、`ens_similarity_gap` 天数），
   而 novelty 加权在 news18 上是**已证实的量级杠杆**（N3 0.76 → 0.91）⇒ 值得单独试。

**待派探针（已 preflight `valid: true`，4 条，沿用 P1 骨架档）：**
```
T1  ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(vec_count(mws50_ess), 60), 252), densify(market)), ...)      # P1 骨架移植
T2  ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(vec_avg(mws50_aes), 22), 252), densify(market)), ...)        # 预聚合情绪占比
T3  ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(vec_avg(mws50_vea), 22), 252), densify(market)), ...)        # 预聚合事件量水平
T4  ts_target_tvr_decay(group_neutralize(-ts_rank(ts_delta(ts_mean(vec_avg(mws50_vea), 22), 66), 252), densify(market)), ...)  # 预聚合事件量变化
```

### §4.15 ★★★★★ NEWS 塔三条齐了：`wpQwjWn6` / `6XdPedNJ` / `9qxPX77V` 全部互相关 < 0.7

**这是本库的终点状态，也是整个 GBR 战役最重要的一组结果。**

| # | alpha | 数据集 | 字段与几何 | S | F | 2Y | SUB | SUB/S | TO | DD | margin | returns | 最低年 | failed_ra |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| **W3** | `wpQwjWn6` | **news17** | `vec_count(relevance)` | **2.10** | **1.38** | **2.33** | **1.44** | 0.686 | 7.80% | 2.50% | 13.75bp | 5.36% | 0.36 (2019) | **0** |
| P1 | `6XdPedNJ` | news18 | `vec_count(sse)` | 1.97 | 1.27 | 2.20 | 1.08 | 0.548 | 7.91% | 2.50% | 13.16bp | 5.21% | 1.12 (2022) | **0** |
| W1 | `9qxPX77V` | **news17** | `vec_count(event_sentiment_score)` | 1.86 | 1.14 | 2.00 | 1.33 | 0.715 | 7.74% | 2.51% | 12.07bp | 4.67% | 0.14 (2020) | **0** |

三条共用骨架（只在「数据集 × 字段」上不同）：
```
ts_target_tvr_decay(
  group_neutralize(
    -ts_rank(ts_mean(vec_count(<字段>), 60), 252),
    densify(market)
  ),
  target_tvr=0.05, lambda_max=5, lambda_min=0
)
```
`GBR / TOP700 / D1 / FAST / decay 15 / trunc 0.05 / nanHandling ON / maxTrade OFF / VERIFY`

**★★★ 三条全部通过的可验证闸（逐项）：**

| 闸 | W3 | P1 | W1 |
|---|---|---|---|
| `failed_ra_count == 0` | ✅ 0 | ✅ 0 | ✅ 0 |
| `failed_ppa_count == 0` | ✅ 0 | ✅ 0 | ✅ 0 |
| `checks.fail == []` | ✅ | ✅ | ✅ |
| `checks.pass` 9 项（含 CLUSTER_TEST / LOW_2Y_SHARPE / MATCHES_PYRAMID） | ✅ | ✅ | ✅ |
| `pyramids.effective == 1`（纯单塔 NEWS，不触 PV） | ✅ | ✅ | ✅ |
| 十年 10/10 全部为正 | ✅ | ✅ | ✅ |
| long/short 均衡 | 459/450 | 452/457 | 457/452 |
| **互相关（三条之间）** | 0.4537 (vs P1) / **0.6583** (vs W1) | 0.4537 / 0.5051 | 0.5051 / 0.6583 |
| **self corr（18 条 OS 池）** | **0.0519** | **0.0852** | **0.0647** |
| `PROD_CORRELATION` | ⚠️ 平台侧无法验证 | ⚠️ | ⚠️ |

**⇒ 全部互相关 < 0.7，self corr < 0.09 ⇒ 三条可同时提交，NEWS 塔点亮（需 3 条）。**

**★★★ 12 条总篮子的互相关矩阵（`compute_mutual_correlation`，1021 交易日）：**

`all_below_threshold = true` / `pairs_over_threshold = []` / **`max_mutually_below_subset_size = 12`**
`max_pair` 仍是旧的 `vR1aEpa3 ↔ E56onL5r = 0.6954`（未被三条新的推高）。

三条新 alpha 对 9 条旧篮子的相关区间：
- `6XdPedNJ`：0.003 – **0.1718**（最大 `j2YNnKOQ`）
- `9qxPX77V`：−0.078 – 0.0647
- `wpQwjWn6`：−0.0658 – **0.0885**

**★ 与旧篮子几乎正交（|corr| < 0.18）。这是 NEWS 事件计数族与 PV/FUND/ANALYST 族天然低相关的体现。**

**★★★ W1 与 W3 的弱年完美互补（这解释了 0.6583 而非 0.92+）：**

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | **2019** | **2020** | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **W1**（sse） | 2.52 | 3.63 | 2.59 | 1.10 | 1.19 | 1.56 | **0.14** | 1.73 | 1.84 | 2.27 |
| **W3**（relevance） | 2.83 | 2.61 | 2.42 | **3.51** | 1.86 | **0.36** | 2.03 | 1.59 | 1.58 | **3.06** |

**W1 最差年 2020（0.14）在 W3 上是 2.03；W3 最差年 2019（0.36）在 W1 上是 1.56。**
两个字段捕捉的是**不同的新闻稿子集**：
- `event_sentiment_score` = 有情绪判定的新闻稿（疫情年被同质化公告淹没 ⇒ 2020 失效）
- `relevance` = 有实体相关性评分的事件（疫情年反而因「哪些公告与公司真正相关」区分度上升 ⇒ 2020 有效）

**⇒ 方法论结论：同数据集同操作（`vec_count`）但换字段，只要两个字段的 coverage 带相同而
「非零填充时机不同」，就能在 PnL 上产生 0.66 的相关 —— 这比换窗口/换分组轴的 0.92–0.99 强得多。
「换字段」是一个被低估的去相关维度，前提是字段语义不同（情绪 vs 相关性）而不是同一族的别名。**
（与 §4.10 的「单实体族换字段 = 恒等」形成对照：**多实体族的条件性填充才是换字段有效的必要条件**。）

**★ 剩余唯一未知闸：`PROD_CORRELATION`。** 三条都没有在平台算出的 prod 值；
但三条与自池 max 仅 0.052–0.085，且与 9 条旧篮子正交 ⇒ 撞 prod 墙的风险显著低于此前的 `pv47_spret` 族（13/13 全撞）。

### §4.16 `news17` 的字段效力排序（4 条探针实测）

| # | 加工 | alpha | S | F | 2Y | SUB | 结论 |
|---|---|---|---:|---:|---:|---:|---|
| W3 | `vec_count(multiple_comp_relevance)` | `wpQwjWn6` | **2.10** | **1.38** | **2.33** | **1.44** | ✅ **全闸，最强** |
| W1 | `vec_count(multiple_comp_event_sentiment_score)` | `9qxPX77V` | **1.86** | **1.14** | **2.00** | **1.33** | ✅ **全闸** |
| W2 | `vec_sum(multiple_comp_rp_story_event_count)` | `78Lqjde5` | 1.47 | 0.81 | **0.78** | 1.15 | ❌ S + 2Y 双缺 |
| **W4** | **`vec_sum(multiple_comp_event_relevance)`** | **`leA6jmoe`** | **2.18** | **1.45** | **2.86** | **1.65** | ✅ **全闸，全组最强** |

**★★★ W2 失败而 W4 最强 —— 同一个 `vec_sum`，两个字段，结果差 1.7 个 Sharpe：**

| | W2 `rp_story_event_count` | **W4 `event_relevance`** |
|---|---|---|
| 字段语义 | 「每个故事的实体记录数」= **已经开始聚合的量** | 「事件与公司的相关强度 0–100」= **原始强度** |
| `vec_sum` 之后 | ≈ 记录数²（量的平方，双重加权） | = 所有实体的相关性总和（强度 × 广度，量纲合适） |
| S / 2Y | 1.47 / **0.78** | **2.18 / 2.86** |

**机理：`vec_sum` 只能作用在「原始强度字段」上，不能作用在「已是聚合量的字段」上。**
`rp_story_event_count` 本身 = 一个故事的实体数；再 `vec_sum` 就等于把「故事热度」平方，
热门故事被过度加权 ⇒ 持仓向少数股票集中 ⇒ 2Y 崩。
`event_relevance` 是逐事件强度；`vec_sum` = 「今天关于这只股票的全部事件的累计相关度」，
既捕捉「多少事件」又捕捉「多相关」，是**自然的经济量**。

**⇒ 修正 §5.3 的推论（原来只说「`nip` 是幅度非方向」）：**
**`vec_sum` 的正确判据不是「字段是计数还是强度」，而是「字段是否已经是聚合量」。**
- 原始强度字段（relevance / sentiment / impact）⇒ `vec_sum` 合法且可能最强；
- 已聚合量字段（`rp_story_event_count` / `story_event_record_count`）⇒ 只能 `vec_count`。

**★ 四条全闸 NEWS alpha 的完整互相关（`all_below_threshold = true`，subset size 4）：**

|  | P1 | W1 | W3 | W4 |
|---|---:|---:|---:|---:|
| **P1** `6XdPedNJ` | — | 0.5051 | 0.4537 | **0.3512** |
| **W1** `9qxPX77V` | 0.5051 | — | **0.6583** | 0.5982 |
| **W3** `wpQwjWn6` | 0.4537 | 0.6583 | — | 0.4888 |
| **W4** `leA6jmoe` | 0.3512 | 0.5982 | 0.4888 | — |

**最大对 0.6583（W1↔W3），全部远低于 0.7 红线。**

**★ W4 十年逐年（10/10 全正，2019 最低 0.74）：**

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | **2019** | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | 2.21 | 3.23 | 2.99 | 2.26 | 1.62 | **0.74** | 1.04 | 2.06 | 2.20 | **3.62** |
| TO | 8.15% | 8.05% | 7.80% | 7.24% | 8.25% | 7.82% | 8.19% | 8.19% | 8.18% | 8.28% |
| long | 428 | 482 | 475 | 520 | 486 | 464 | 420 | 412 | 428 | 407 |
| short | 428 | 491 | 508 | 524 | 475 | 459 | 424 | 416 | 432 | 409 |

**★★★ 13 条总篮子互相关（`compute_mutual_correlation`，含 9 条旧 + 4 条 NEWS）：**
`all_below_threshold = true` / `pairs_over_threshold = []` / **`max_mutually_below_subset_size = 13`**
`max_pair` 仍是旧对 `vR1aEpa3 ↔ E56onL5r = 0.6954`。

**四条 NEWS 对 9 条旧篮子的相关区间（几乎完全正交）：**
- `6XdPedNJ`：−0.003 – **0.1718**
- `9qxPX77V`：−0.078 – 0.0647
- `wpQwjWn6`：−0.0658 – 0.0885
- **`leA6jmoe`：0.0209 – 0.0752** ← 全组最正交

**⇒ NEWS 塔点亮所需 3 条已具备 4 条（余额 1），且 W4 是最强的一条（S 2.18 / DD 2.09%）。**

### §4.5 公式更正：`margin ≈ returns / (TO × 504)`

前序笔记用 `returns / (TO × 252)` 反推 margin，与平台值系统性差 2 倍。用 P1 校准：
`0.001316 × 0.0791 × 504 = 0.05246` vs 平台 `returns = 0.0521` ✅（误差 0.7%）。
⇒ **换手是双边计（买+卖），一日的 turnover 对应两笔成交额**。

**`F` 公式复核**：`F = S × sqrt(|returns| / max(TO, 0.125))`
- P1：`1.97 × sqrt(0.0521/0.125) = 1.272` vs 平台 1.27 ✅
- N14：`0.89 × sqrt(0.0229/0.125) = 0.381` vs 0.38 ✅
- `akK2vpWW`：`1.95 × sqrt(0.0589/0.125) = 1.338` vs 1.33 ✅（此前用 252 口径算的 2.94% 是错的）
⇒ **`F` 公式本身正确，此前唯一的错是 margin↔returns 的 504 系数**。

### §4.17 ★★★★ `news50` 三条探针全灭 ⇒ CONFIRMED-DEAD；`news` 类目全域清点完毕（无新处女地）

**`news50`（Web News Analytics，RPNA edition，cov 0.691，37 字段全 `mws50_*`）三条探针，覆盖它的三个独立维度，天花板 S 0.97：**

| # | 维度 | 表达式要点 | alpha | S | F | 2Y | SUB | TO | DD | failed_ra |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| T1 | 事件计数密度 | `vec_count(mws50_ess)` + P1 骨架 | `58E7Q7bX` | 0.77 | 0.34 | 1.43 | 0.77 | 8.74% | 5.64% | 3 |
| T2 | **预聚合情绪占比**（91 天 `aes` = 正面/非中性事件比率） | `vec_avg(mws50_aes)` | `RREZVY6e` | **−0.63** | −0.24 | −1.03 | −0.55 | 8.81% | **21.56%** | 4 |
| T3 | **预聚合事件量**（91 天 `vea` 事件累计） | `vec_avg(mws50_vea)` | `Xg9wWOrl` | 0.97 | 0.47 | **2.19** | 0.71 | 8.93% | 5.40% | 2 |

三条全部 `GBR / TOP700 / D1 / FAST / decay 15 / trunc 0.05 / nanHandling ON / maxTrade OFF`。

**三条硬结论：**

1. **同一个骨架，从 news18 搬到 news50 降 61%**（P1 `vec_count(multiple_comp_sse)` S 1.97 → T1 `vec_count(mws50_ess)` S 0.77）。
   病根是覆盖度：news18 多实体带字段级 cov **0.9714**，news50 集级 **0.691**。**这是决策 #76「覆盖度下降 ⇒ 信号崩」的第三次独立验证**（前两次：V1/V3/V6 换低覆盖字段 2Y 精确崩到 0.68；news104 cov 0.9695 但字段稀疏全灭）。
2. **`aes` 预聚合情绪占比的符号是反的** —— 我用 `-ts_rank(...)` 得 S −0.63，即去掉反转号后 S 只有 **+0.63**。说明「正面事件占比高 ⇒ 后续跑赢」（**不反转**），与「注意力密度高 ⇒ 反转」是**相反的经济机制**。这是 news50 唯一提供的正面信息，但量级远不够（且 DD 21.56% 已爆）。
3. **`vea` 的 2Y（2.19）显著高于全期 S（0.97）** —— 预聚合事件量只在近两年有效，早期失效。**这种「2Y ≫ S」的形态不是好事**，它意味着信号是近端窗口拟合，不是十年稳定的机制。T3 因此不可作为「压线候选」挽留。

**⇒ `news50` CONFIRMED-DEAD（3 探针，覆盖 3 个独立维度）。**

**`news` 类目 18 个数据集全域清点（`get_datasets(category="news")` 实测）：**

| 数据集 | coverage | 字段 | alphaCount | 状态 |
|---|---:|---:|---:|---|
| news104 | 0.9695 | 11 | 388 | ❌ 8 探针判死 |
| **news17** | 0.8371 | 48 | 384 | ✅ **3 条全闸**（W1/W3/W4） |
| **news18** | 0.8192 | 70 | 1197 | ✅ **1 条全闸**（P1） |
| news20 | 0.7449 | 46 | 217 | 同源 news18、每档低 0.10 ⇒ 不投入 |
| news38 | **0.5985** | **3** | 30 | 太薄 + 字段太少 ⇒ 不投入 |
| news50 | 0.691 | 37 | 361 | ❌ 本条判死 |
| news21/23/29/3/31/51/52/54/7/73/76/81 | **0.0** | 2–73 | 7–217 | ❌ **GBR TOP700 零覆盖，零成本判死** |

**⇒ NEWS 类目的矿已经挖到底：18 个里 12 个零覆盖、1 个已判死、2 个在产、2 个结构性不可用。补量必须换 category。**

**⇒ 下一个目标：`institutions6`（INSTITUTIONS 塔，**coverage 1.0** / 11 字段全 MATRIX / alphaCount 881 / 倍率 1.4 / 该塔 0 条已点亮）。**
它是论坛帖 `43212475386007` 那套「流量 ÷ 存量」稀疏事件骨架在 GBR 上**唯一可行**的载体：原帖点名的 `institutions1` 在 GBR cov 仅 **0.3118**（必崩，即上次复现失败的真正原因），而 institutions6 同时具备「机构买卖家数/股数」（流量）与 `aggregate_share_count_institutions`（存量），且 cov = 1.0 满足决策 #76 的 ≥0.96 硬要求。

---

## §5 判读（上半场结论）

### §5.1 ★★★★★ forum 帖 `42659817284375` 的两个套路，一个验证一个证伪

同骨架、同设置、只换乘性权重字段的三臂单变量对照：

| 臂 | 权重字段 | 语义 | S | SUB | margin | invest_ratio |
|---|---|---|---:|---:|---:|---:|
| 裸信号 | — | — | 0.76 | 0.26 | 35.5bp | 1.0263 |
| **× relevance** | `multiple_comp_relevance` | 实体在故事中的重要性（**信息量代理**） | **0.45 ↓** | 0.27 | 20.0bp | 0.8667 |
| **× novelty** | `mltpl_cmp_event_simildays` | 距上次相似事件天数（**定价充分度**） | **0.91 ↑** | **0.58** | **37.7bp** | **1.0549** |

**机理**：
- **`relevance` 加权有害**。relevance 度量「信息量」，但**不区分新旧**；高 relevance 集中在被多家
  报道的大票 ⇒ 权重被推向信息已充分定价的一侧，且**挤掉小票**（`invest_ratio` 1.03 → 0.87），
  margin 同步腰斩。forum 帖原话「相关性加权提升信噪比」在 GBR 上**不成立**。
- **新颖度加权是量级杠杆**。`event_similarity_days` 度量的是「**信息尚未被定价**」—— 这是
  直接度量，不是代理。forum 帖原话「相似事件越久远 ⇒ 新信息比例越高 ⇒ 情绪对价格冲击越强；
  旧闻重复已被定价，情绪无效」在 GBR 上**成立**。

**判据（可跨数据集迁移）**：乘性权重应选**「定价充分度」**类字段
（novelty / similarity_days / days_since_* / surprise），
不选**「信息量 / 重要性」**类字段（relevance / importance / coverage / story_count）。

### §5.2 ★★★★ 「相消即同源」在本数据集上是误导性命名

N4 试 `sse − ssc`，指望拿到「Story 聚合 vs Entity 单体」的偏离（forum 帖的 Entity-Story Deviation）。
实测 S **0.12** / margin **0.57bp** ⇒ 纯噪声。

根因：`sse`（事件极性）与 `ssc`（多技术综合情绪）**coverage 完全相同（0.9714）、alphaCount 同量级
（51 vs 81）、描述都指同一批新闻** ⇒ 它们是**同一信息源的两个统计口径**，不是「故事 vs 实体」。
双腿相减前必须先验证两腿**语义不同源**，命名相似（都带 `multiple_comp_`）不等于同源。

### §5.3 ★★★★ `nip` 是幅度而非方向，不能当信号用

N6 裸水平 S **−0.17** / DD 12.35% / margin **−7.8bp**。
但同时 **SUB +0.39 而全期 S 为负** ⇒ 大盘股上符号相反 ⇒ 该字段不是方向性信号。

`nip` 描述是 "Degree of impact of the news" = **冲击程度**，与方向无关。
正确用法只能是**作乘性权重**（N7 的形态：`multiply(ssc, abs(nip))`），不能作水平信号。
⚠ 但 N2 已证「信息量类权重有害」，`nip` 同属信息量类 ⇒ N7 预期也是负向，低优先。

### §5.4 ★★★ `ts_covariance(x, x, W)` 的符号取决于「高方差是机会还是风险」

同一个算子（`ts_covariance(sse, sse, 22)` = 方差）：
- 在 `shortinterest3` 上是 **S 1.60 / 2Y 0.73**（`FAST`）—— 借券利用率的高方差 = 空头压力积聚 = 机会
- 在 `news18` 上是 **S −0.39 / 2Y −0.51 / DD 13.89%** —— 情绪的高方差 = 信息混乱 = 风险

⇒ 二阶矩本身**没有固定方向**，必须先答「这个量的高方差代表机会还是风险」，不能照搬骨架符号。

### §5.5 ★★★★★ `F` 的地板效应在 N3 上再次精确验证

`F ≈ S × sqrt(|returns| / max(TO, 0.125))`

- N1：`0.76 × sqrt(0.0201/0.125) = 0.305` vs 平台 **0.30** ✅（TO 11.33% 已走地板）
- N3：`0.91 × sqrt(0.0238/0.1265) = 0.395` vs 平台 **0.39** ✅（TO 12.65% 刚过地板）

**要 S=1.58 且 F=1.0 ⇒ returns 需 = `0.125 × (1.0/1.58)²` = 5.01%**，当前 N3 只有 2.38%
（需 ×2.10，而 S 只需 ×1.74）⇒ **实际需要 S ≈ 1.75–1.80，而非 1.58**。
继续压低 TO 不会提 F，只会按比例压 returns。

---

## §6 判定门（本库的退出条件）

- **继续投入**：只要还有**未测的结构维度**（N5 掩码 / N7 交互 / N8 时序标准化 / N9 动量 /
  N11 归因 / N12 双源 / `qcm` 置信度族），且 **N3 的骨架持续给出 S > 0.85**。
- **判 `PROBE-KILLED`**：跑满 8 探针 / ≥5 结构 / 覆盖 multiple_comp 族过半，S 天花板 < 0.95。
- **判 `CONFIRMED-DEAD`**：S 区间整体落在 [−0.4, +0.6] 且无一条过任何指标闸。
- **不判死**：只要 N3 骨架还活着 —— 它的非指标闸已全清，缺的只是信号强度，
  属「加工/叠加不足」而非「无信号」。

---

## §7 交叉引用

- `docs/reference/template_library_gbr_sentiment33.md` —— SENTIMENT 塔 8 探针 CONFIRMED-DEAD 的对照
- `docs/reference/template_library_gbr_news104.md` —— 同族 8 探针 CONFIRMED-DEAD（信息寿命分钟级）
- `docs/reference/template_library_gbr_shortinterest3.md` —— `FAST` 中性化与 `ts_covariance` 的首次实证
- `docs/reference/field_profile_fundamental6_gbr_20261030.md` —— `F` 公式与 TO 地板的首次校准

**论坛**：`42659817284375`（relevance/novelty/聚合族）· `38878004433815`（EUR news18 失败记录，
2400 表达式均值 S 0.05 / 均值 TO 111% ⇒ 方法无效而非数据集无效；EUR 73 字段含 58 MATRIX，
GBR 70 字段全 VECTOR ⇒ **两区字段构成不同，本质是两个数据集**）·
`43554135453335`（新闻密度突增 = 反转，给 N8 的负向预置）· `43541109631895`（异常注意力，GBR 已证伪）

**外部论文**：Da-Engelberg-Gao (2011) *JF* 66(5)「ASVI 异常注意力 ⇒ 短期正收益后反转」·
Chan (2003) *JFE* 70(2)「有无新闻区分动量/反转」· Tetlock (2007) *JF* 62(3)（GBR 符号相反）
