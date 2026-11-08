# EUR NEWS 跨区迁移战役（2026-11-03）

> 战役目标：把 GBR 的 NEWS 模板族迁移到 EUR，在 **EUR/D1/news category** 下挖 regular alpha。
> 闸线：**S≥1.58 / F≥1.58 / 2Y≥1.58** / TO 1–70% / fRA=0 / prod<0.7 / self<0.7。
> 设置档：EUR/TOP2500/D1；论坛机制用 **COUNTRY/decay6/trunc0.04**，壳版用 SUBINDUSTRY/decay4/trunc0.08。

## §1 选靶与存量

- EUR/D1 共 **20 个 news 数据集**（实拉 `get_datasets`）。
- 首选 **news36**（cov 0.7713 / 15 字段 / aC 144）——与 HKG news36 同族，字段名 `mws36_*`。
- 次选 **news73**（cov 0.813 / 22 字段 / 字段级 aC 1–20，**极不拥挤**）——与 AMR news73 同族。
- 关键发现：`earnings_sent_matrix`（**earnings category，非 news**）上有论坛实证 S 1.65 的「情绪概率差」机制。

## §2 论坛机制移植（核心）

论坛帖 `43620895448343`（EUR 财报电话会「情绪概率差」）实证表达式：

```
signed_power(subtract(ts_zscore(ts_backfill(pos, 60), 250),
                      ts_zscore(ts_backfill(neg, 60), 250)), 3)
```

设置：EUR/TOP2500/D1/**COUNTRY**/**decay6**/**trunc0.04**，**无壳**。
数据：`earnings_sent_matrix`（MATRIX，cov 0.5062，字段 `positive_sentiment_probability_3` / `negative_sentiment_probability_3`）。

### 移植到 EUR news36（VECTOR，需 vec_avg）

| tag | 变体 | alpha | S | F | TO |
|---|---|---|---:|---:|---:|
| E1_forum_exact | bf60/z250/p3 | `wpQjqkld` | **+0.49** | 0.16 | 25.0% |
| E2_bf30 | **bf30**/z250/p3 | `58ElbWQk` | **+0.54** | 0.16 | 21.0% |
| E3_bf120 | bf120/z250/p3 | `1YNw9pxK` | +0.41 | 0.13 | 30.9% |

⇒ **回填窗越短越强**（bf30 > bf60 > bf120），与财报电话会（季度稀疏事件，bf60）不同。

### 移植到 EUR news73（部分分字段）

| tag | 变体 | alpha | S | F | TO |
|---|---|---|---:|---:|---:|
| F1_forum_exact | bf60/z250/p3 | `GrWlawAP` | +0.49 | 0.14 | 33.5% |
| F2_bf30 | bf30/z250/p3 | `Jje7we3x` | **+0.53** | 0.15 | 34.9% |

⇒ **与 news36 独立同值（~0.5）** ⇒ 机制本身在 EUR NEWS 上的上限约 0.5。

## §3 关键判读

1. **论坛机制在 EUR NEWS 上真实但弱（S≈0.5）**，距闸线 1.58 差 **3.2×**。
2. **同一机制在 `earnings_sent_matrix` 上实证 1.65** ⇒ 差异来自**数据集本身**（财报电话会事件情绪 vs 日常新闻情绪），不是表达式。
3. **回填窗是 EUR NEWS 的主杠杆**：bf30 最优（0.54），bf60 次之（0.49），bf120 更弱（0.41）。
4. **带壳版（SUBINDUSTRY/decay4/trunc0.08 + zscore60）显著更差**：prob 波次 E1=+0.10 / E2=−0.28。
   ⇒ **源区（GBR）的强几何壳不可照抄**，与既有「设置档区域特异」结论一致。

## §4 在飞 / 待派

- **在飞**：EUR news36 forum 波次（12 条，bg_e23dfa61）；EUR `earnings_sent_matrix` 诊断波次（12 条，bg_4a390a3c）。
- **待派**：`_eur_news36_wave2_list.json`（回填阶梯 bf5/10/22 + winsorize + 情绪-收益错配）；`_eur_news36_wave3_list.json`（词数三类分布 pos/neg/neutral 比率）。
- **诊断目的**：确认 `earnings_sent_matrix` 的 1.65 是否可复现 ⇒ 决定「NEWS 是否有机会」还是「必须换 category」。

## §5 跨区对照（NEWS category）

| region | 集 | 最强轴 | |S| | 闸线 | 差距 |
|---|---|---|---:|---:|---:|
| CHN | news46 | 密度 | 0.18 | 2.07 | 11.5× |
| HKG | news36 | 词数归一情绪 | 0.88 | 1.58 | 1.8× |
| AMR | news73 | uncertainty | 0.92 | 1.58 | 1.7× |
| **EUR** | **news36/73** | **论坛概率差** | **0.54** | 1.58 | **2.9×** |

⇒ EUR NEWS 是目前跨区迁移里**最弱**的一站；机制真实但量级不足。
