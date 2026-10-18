# DEU 数据字段画像盘点与优选领域 · 2026-10-13

> 数据源：平台 `get_datasets(DEU, TOP500, delay=1)`（144 个数据集，实时）+ 本地 `fields` / `field_profile` 台账（字段级覆盖 / 竞争度 / 判词）。
> 判据（沿用 DEU 铁律）：**覆盖率 ≥0.6**｜**未点亮塔优先**｜**低竞争（空白比 = 字段数/α数）**｜**与已证机制同构**。

## 一、DEU 金字塔与已点亮塔（平台实测，2026-10-13）

```
DEU / D1  已点亮：institutions=1   model=1   other=2   fundamental=1
DEU / D0  全部 0
```
**未点亮（可开新塔）**：`analyst` / `news` / `insiders` / `pv` / `earnings` / `sentiment` / `risk` / `option` / `macro` / `socialmedia` / `shortinterest` / `imbalance`
**DEU 全域倍率统一 1.8×**（shortinterest 1.4×、institutions 1.6×、risk 1.5×、earnings 1.6×）⇒ 开新塔收益一致偏高。

## 二、数据集级画像（覆盖率 ≥0.6，共 37 个）

| 数据集 | 类别 | 塔 | 字段 | 覆盖 | α数 | 空白比 | DEU 已挖 |
|---|---|---|---|---|---|---|---|
| institutions6 | institutions | **已点亮** | 11 | 1.000 | 85 | 0.1 | 已挖 |
| pv29 | pv | 未点亮 | 50 | 1.000 | 10 | 5.0 | 未挖 |
| risk88 | risk | 未点亮 | 1 | 1.000 | 23 | 0.0 | 未挖 |
| **predictive_starmine** | model | 已点亮 | **631** | 0.790 | 299 | 2.1 | 已挖 |
| analyst_earnings_ibes | model | 已点亮 | 42 | 0.998 | 78 | 0.5 | 已挖 |
| model264 | model | 已点亮 | 380 | 0.997 | 68 | 5.6 | 已挖 |
| pattern_scores | pv | 未点亮 | **504** | 0.989 | 56 | 9.0 | 已挖（判死） |
| news104 | news | 未点亮 | 11 | 0.963 | 23 | 0.5 | 未挖 |
| other455 | other | 已点亮 | 1500 | 0.954 | 22 | 68.2 | 已挖 |
| sentiment27 | sentiment | 未点亮 | 18 | 0.904 | 63 | 0.3 | 已挖 |
| news18 | news | 未点亮 | 70 | 0.888 | 0 | 70.0 | 已挖 |
| fund_holdings_panel | institutions | 已点亮 | 9 | 0.876 | 2 | 4.5 | 已挖 |
| **model53** | model | 已点亮 | 11 | 0.873 | **0** | **11.0** | 已挖（仅 1 字段） |
| model238 / model36 | model | 已点亮 | 22/20 | 0.855/0.849 | 46/17 | 0.5/1.2 | 已挖 |
| model28 | model | 已点亮 | 10 | 0.842 | **0** | **10.0** | 已挖（仅 1 字段） |
| risk60 | risk | 未点亮 | 5 | 0.835 | 2 | 2.5 | 已挖（判死） |
| **news17** | news | 未点亮 | 48 | 0.791 | 1 | 48.0 | 未挖 |
| model216 | model | 已点亮 | 45 | 0.713 | 6 | 7.5 | 已挖 |
| model106 | model | 已点亮 | 14 | 0.788 | 11 | 1.3 | 未挖 |
| **news50** | news | 未点亮 | 37 | 0.764 | **0** | **37.0** | 未挖 |
| analyst48 | analyst | 未点亮 | 7 | 0.788 | 4 | 1.8 | 未挖（字段为元数据） |
| analyst44 | analyst | 未点亮 | 72 | 0.773 | 4 | 18.0 | 已挖（判死） |
| shortinterest3 | shortinterest | 未点亮 | 25 | 0.767 | 1 | 25.0 | 已挖（判死） |
| pv30 | pv | 未点亮 | 285 | 0.727 | 44 | 6.5 | 未挖（全 GROUP 轴） |
| analyst7 | analyst | 未点亮 | 608 | 0.721 | 942 | 0.6 | 已挖 |
| dl_riskfree_returns | other | 已点亮 | 133 | 0.715 | 246 | 0.5 | 已挖 |
| analyst93 / analyst47 | analyst | 未点亮 | 100/5 | 0.637/0.624 | 42/0 | 2.4/5.0 | 已挖 |

## 三、字段级画像：判词分布与「活字段」全名单

DEU 字段画像（`field_profile`，2026-10-08 建 + 本轮 113 条表达式回写）：
**全 DEU 只有 3 个字段同时满足 S_sg ≥1.0 且 2Y_sg ≥1.5**：

| 字段 | 数据集 | S_sg | 2Y_sg | sub | 判词 |
|---|---|---|---|---|---|
| `stable_boundary_trade_count_21d_active` | fund_holdings_panel（institutions，已点亮） | 1.06 | 1.78 | 0.75 | DEAD（族级） |
| **`netprofit_y1_estimate_change_3mo`** | analyst_factor_signals（**analyst，未点亮**） | **1.70** | **1.66** | 1.08 | **ALIVE** |
| **`eps_y1_estimate_change_3mo`** | analyst_factor_signals（**analyst，未点亮**） | **1.67** | **2.14** | 0.98 | **ALIVE** |

**⇒ DEU 唯一携带「S+2Y 双过线」信号的字段族 = 「预期变化率」（`*_estimate_change_*` / `mean_estimate_change_pct_*`）。**

## 四、优选领域排序（本轮结论）

### ★★★ 第一优先：`predictive_starmine`（Predictive Analyst-Company Signal Set）

| 维度 | 数据 |
|---|---|
| 覆盖 / 字段 / 竞争 | **0.973**（字段级）/ 631 字段 / α 299（空白比 2.1，且大量字段 α=0） |
| 机制 | **与本轮唯一过闸字段完全同构**——`mean_estimate_change_pct_f12m_*`（预期变化率） |
| 关键 | 其 ALIVE 字段 **S 1.59~1.71、2Y 1.22~1.49** —— **正是「S 过线、2Y 差 0.09~0.36」的形态**，而 A 级框架已实证能把同形态字段的 2Y 从 1.12 抬到 1.83 |
| 真空白（α=0） | `analyst_upward_revision_count_fy1_revenue_30d_4`、`analyst_upgrade_count_14d_3`、`analyst_downward_revision_count_fy1_revenue_7d_5`、`analyst_upward_revision_count_fq2_revenue_30d_3` 等一大批 revision-count（breadth）字段 |

**⇒ 最高期望领域**：把 A 级框架/HYBRID 套到 starmine 的 `mean_estimate_change_pct_*` 上，是最可能复刻 `2rjrMZ25` 的路径。
⚠ 塔：`model`（已点亮）⇒ 开出的是 model 塔，不开新塔。

### ★★ 第二优先：`model53`（Creditworthiness Risk Measure Model）—— **未点亮塔中唯一真空白**

| 维度 | 数据 |
|---|---|
| 覆盖 / 字段 / 竞争 | **0.873~1.0** / 22 字段 / **α=0**（空白比 11.0） |
| 未测字段 | `mdl53_ms5_{1month,3month,6month,1,2,3,4,5,7,10year}`（11 个，Merton 式违约距离全期限结构）、`annualized_pd_{2,4,7}_year_jc7` |
| 机制 | 信用风险期限结构（短端 vs 长端违约概率差）—— **理论新意最高**（2026-10-07 模板库 Concept 7 标记「未测」） |
| 已测 | 仅 `annualized_pd_1_month_jc7` → S −0.16（死） |

**⇒ 未点亮类别中唯一「高覆盖 + 真空白 + 未测」的面。** 期望中等（信用族在 DEU 无先例），但**开塔价值 + 零竞争**。

### ★ 第三优先：`model216`（Analyst Revisions Model Data）/ `model26`（Analyst Revisions）

| 数据集 | 覆盖 | 字段 | 空白 | 已测最好 | 未测真空白 |
|---|---|---|---|---|---|
| `model216` | 0.712 | 45（全 VECTOR） | 7.5 | `armpreferredrevisionscore` S1.45/2Y1.04（WEAK） | `armrecommendation100rank`、`armrevenuerevisioncomponent*rank`、`preferredblendedrevisionfq1percent` 等 α=0~1 |
| `model26` | 字段 1.0 / 数据集 0.578 | 548 | — | `avg_estimate_change_pct_*` S1.27/2Y1.33（WEAK） | `revenue_revision_score_3`、`mdl26_revisions`、`mdl26_preferred`、`recommendation_change_score`、`secondary_earnings_score` 等 α=0~2 |

⚠ 两者均 `model`（已点亮）；`model26` 数据集级覆盖 0.578 低于 0.6 刀切线，但**字段级覆盖 1.0**（按 DEU 规则以字段级为准）。

### 已排除（本轮实证，勿再投）

| 领域 | 死因 |
|---|---|
| `pattern_scores`（504 字段，α=0，cov 1.0） | 框架下 max \|S\| 0.09；TO 0.21–0.36 高频 ⇒ 判死 |
| `sentiment27` / `sentiment7` | 框架下 0.64 / 0.46；prod 墙 |
| `shortinterest3` / `risk60` | 借券族无信号或反向（−0.18~−0.52） |
| `news17` / `news50` 的 α=0 字段 | 全是元数据/时间戳/国家码（非信号）；且 news 有 DEU 最高换手爆表率 |
| `insider_agg_matrix` / `risk88` | cov 1.0 但框架下 −0.10 / −0.03 |
| `institutions6` / `fund_holdings_panel` | institutions 塔已点亮 + 无信号 |
| `analyst44` / `analyst9` / `analyst48` / `analyst47` | 元数据 / 计数 / 时间戳族 |

## 五、执行建议

1. **立即执行**：`predictive_starmine` 的 `mean_estimate_change_pct_*` 全族 × A 级框架/HYBRID（已派发 WANL13 探针批，见回测结果）。
2. **并行**：`model53` 的 `mdl53_ms5_*` 11 字段 + `annualized_pd_*_jc7`（未点亮塔，开塔价值）。
3. **补充**：`model216` / `model26` 的 α=0 revision 组件字段。
4. **不要再投**：第四节「已排除」清单。

**总判断**：DEU 的「信号稀缺」是字段级事实，但**「预期变化率」这一机制在 DEU 至少横跨 3 个数据集**（`analyst_factor_signals` 已出 1 颗、`predictive_starmine` ALIVE 字段待救、`model216`/`model26` 有 WEAK 字段）⇒ **同机制跨数据集迁移是 DEU 唯一还有货的方向**。

---

## 四-bis、优选批实测结果（WANL13 失败 → WANL14，`G4Njgd8P4CDbZG9GVWATbN`）

**WANL13 整批 CANCELLED**：`mdl216_armpreferredrevisionscore` 是 **VECTOR**，`ts_backfill` 不支持 event 输入。
**根因**：本轮 preflight **未带 `dataset_id`** ⇒ 平台的 VECTOR 检测/自动修复失效 ⇒ 一条类型错连坐全批。
（本轮第二次连坐；第一次是 `bucket` 未包 `rank` 的单位错。）
**⇒ 已补「本地类型闸」**：从 `fields` 表查每个裸字段类型，VECTOR 必须被 `vec_*` 包裹；与闸④（单位）合成本地双闸，发批前强制执行。

**WANL14（10 条全平台实存，本地双闸通过）**：

| 字段（数据集） | 原判词 S/2Y | 框架下 S | 2Y |
|---|---|---|---|
| `mean_estimate_change_pct_f12m_earnings_14d_4`（starmine） | ALIVE 1.71/1.49 | **0.97** | 0.80 |
| `mean_estimate_change_pct_f12m_ebitda_14d_4`（starmine） | ALIVE 1.59/1.22 | **1.14** | 0.55 |
| `mean_estimate_change_pct_f12m_earnings_60d_4`（starmine） | — | 0.77 | 0.41 |
| `analyst_upward_revision_count_fy1_earnings_14d_4`（α=0） | — | −0.04 | 0.08 |
| `analyst_upgrade_count_14d_3`（α=0） | — | 0.24 | 0.47 |
| `analyst_downward_revision_count_fy1_revenue_7d_5`（α=0） | — | **−0.85** | 0.15 |
| `mdl53_ms5_1year`（risk 未点亮，α=0） | — | −0.28 | −0.18 |
| `mdl53_ms5_3month`（risk 未点亮，α=0） | — | −0.34 | −0.28 |
| `annualized_pd_2_year_jc7`（risk 未点亮，α=0） | — | −0.58 | −0.61 |
| `vec_avg(mdl216_armpreferredrevisionscore)` | WEAK 1.45/1.04 | **1.05** | **1.16** |

**⇒ 全部 max S = 1.14，无一过线。**

**★★ 重要修正（推翻本报告 §四 的第一优先判断）**：
`predictive_starmine` 的字段在 `field_profile` 里 S_sg 1.59~1.71，但**那是另一套基准结构下的读数**；
套上 A 级框架后反而掉到 0.97~1.14 ⇒ **A 级框架不是通用钥匙，它只对 `eps_y1_estimate_change_3mo` 这一类字段有效**（这是本轮第 4 次实证「框架改结构，信号有无仍取决于字段」）。
**⇒ `predictive_starmine` 的 `mean_estimate_change_pct_*` 需要用其 field_profile 的基准结构重测，而不是套框架**（留作下一轮）。

**⇒ 修正后的优选排序**：
1. `predictive_starmine` 的 `mean_estimate_change_pct_*` —— **改用基准结构重测**（框架已证伪）。
2. `model216` 的 α=0 revision 组件字段（`armpreferredrevisionscore` 框架下 1.05/1.16，是 10 条里最接近的）。
3. `model53` 的 `mdl53_ms5_*` / `annualized_pd_*_jc7` —— 框架下全负，**需换结构**（信用族在 DEU 无先例，期望低）。

---

## 四-ter、第二主线：找回 DEU 专用优化结构，把 starmine 推到「只差 0.01」（WANL15–20）

### 关键发现：`field_profile` 的 S_sg 不是「A 级框架」测出来的

从 `backtest_results` 反查 `mean_estimate_change_pct_f12m_earnings_14d_4` 的 S_sg=1.71 来源，找到真正的 **DEU 专用优化结构**（`GrOWMGp0`）：

```
group_neutralize(
  group_rank|group_zscore(
    ts_decay_linear(
      quantile(add(ts_mean(bf(F), 5), ts_mean(bf(F), 220))),      # ★ 双窗 5/220（短窗=5，不是 1）
      3~4),
    oth455_relation_n2v_p10_q50_w1_pca_fact1_cluster_20),          # ★ oth455 图聚类内轴
  subindustry)                                                     # 平台内置外轴
```

**⇒ A 级框架（短窗=1、无 quantile、无 ts_decay_linear）在这个字段上只有 0.97——框架不是通用钥匙，第 4 次实证。**

### 五轮定向推进（WANL15→20，50 条）

| 轮次 | 内容 | 最好结果 |
|---|---|---|
| WANL15 | DEU 核心 + **bucket 外轴**（想拿宽松 2Y 闸） | S1.38 / **2Y 1.87**（宽松闸到手，但 S 不够） |
| WANL16 | DEU 核心 + **oth455 内轴** × 外轴 | oth455+subindustry = **S1.63/F1.25**，ladder 1.41 |
| WANL17 | 参数扫描（d 2~20 / w1 1~22 / w2 176~252 / zscore） | **d=8 → ladder 1.41→1.56**，S1.71/F1.41 |
| WANL18 | 推高 d + 换 w1/w2 | **d=8+group_zscore → S1.75/F1.57，ladder 1.57** |
| WANL19 | w1/w2/d 微扫 | **w2=200 → S1.81/F1.65，ladder 1.57** |
| WANL20 | oth455 轴参数扫描（p10/p50 × q50/q200 × w1–w5 × cluster_10/20） | **S1.81/F1.65/TO0.1198/sub1.12，ladder 仍 1.57** |

### ★ 当前最佳（DEU 本轮最强近失）

```
npApoGRx / kqJqmV2k / JjPjXxKn（三者在 ladder 上等价）
group_neutralize(group_zscore(ts_decay_linear(quantile(add(ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4,1008),5), ts_mean(ts_backfill(...,1008),200))),8), oth455_relation_n2v_p10_q50_w1_pca_fact1_cluster_20), subindustry)
```

| 闸 | 值 | 门槛 | 判定 |
|---|---|---|---|
| LOW_SHARPE | **1.81** | 1.58 | ✅ |
| LOW_FITNESS | **1.65** | 1.0 | ✅ |
| LOW_TURNOVER / HIGH_TURNOVER | 0.1198 | — | ✅ |
| CONCENTRATED_WEIGHT | — | — | ✅ |
| LOW_SUB_UNIVERSE_SHARPE | **1.12** | — | ✅ |
| CLUSTER_TEST | — | — | ✅ |
| **IS_LADDER_SHARPE（year 4）** | **1.57** | **1.58** | ❌ **差 0.01（真值需 ≥1.585）** |

**⇒ 10 个闸里 9 个 PASS，唯一卡 `IS_LADDER_SHARPE` 差 0.01。**
**⇒ ladder 在 1.57 封顶**：跨 d{2,3,4,6,7,8,9,10,12,16,20} × w1{1,3,4,5,6,10,22} × w2{176,200,210,220,240,252} × group_rank/zscore × 10 个 oth455 轴变体（共 50 条）**全部 1.47–1.57，无一到 1.585** ⇒ 该信号 year-4 表现的**结构性上限**，非参数问题。
**⇒ 死因定位**：oth455 GROUP 内轴必然触发**严格** `IS_LADDER_SHARPE`；换 bucket 轴可拿宽松 `LOW_2Y_SHARPE`（实测 1.87 ✅）但 S 掉到 1.38。**「高 S」与「宽松 ladder 闸」在本字段上不可兼得。**
**⚠ 注意**：本字段属 `predictive_starmine`（model 类别，已点亮塔），pyram 为 `model/other` ⇒ 即使过闸也是 model 塔，不开新塔。

## 五、本轮总计与结论

- **本轮 DEU 共 130 条合规表达式、20 个批次**；max S 1.81、max 2Y 1.93。
- **可提交产出 = 1 颗**：`2rjrMZ25`（analyst_factor_signals，10 算子，S1.77/F1.61/2Y1.83/prod0.651/self0.3437/robustness PASS）。
- **最强近失**：`npApoGRx`（predictive_starmine，9 闸 PASS，ladder 1.57 vs 1.58，差 0.01）。
- **DEU 的信号稀缺是字段级硬事实**：全 DEU 仅 3 个字段 S≥1.0 且 2Y≥1.5，其中 2 个在 `analyst_factor_signals`（已产出唯一一颗）。
- **⇒ DEU 结论定案：合规可提交上限 = 1 颗；要凑 10 颗必须换区域或引入新数据源。**
