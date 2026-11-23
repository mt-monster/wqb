# Robustness 审计 · 78YrVgwb（2026-11-22）

> 候选：EUR / TOP2500 / D1 / decay 4 / CROWDING / trunc 0.0 / nan ON / maxTrade OFF
> 表达式：`multiply(group_rank(subtract(probability_fifth_quantile_ten_day_bucket_four_15, probability_fifth_quantile_ten_day_bucket_zero_15), industry), group_rank(ts_rank(ts_backfill(subtract(count_institutional_buyers_security, count_institutional_sellers_security), 120), 35), industry))`

## 1 逐年稳定性（`get_alpha_yearly_stats`，2014–2023 十年全 IS）

| 年 | S | F | TO | DD | long | short | margin |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2014 | 4.76 | 2.83 | 29.0% | 0.75% | 1087 | 1530 | 7.09bp |
| 2015 | 4.25 | 2.77 | 29.2% | 0.84% | 1139 | 1584 | 8.46bp |
| 2016 | 3.99 | 2.29 | 30.4% | 0.91% | 1134 | 1586 | 6.58bp |
| 2017 | 4.55 | 2.38 | 29.4% | 1.03% | 1228 | 1723 | 5.45bp |
| 2018 | **5.46** | 3.33 | 29.8% | 0.74% | 1212 | 1714 | 7.45bp |
| 2019 | 4.23 | 2.17 | 29.8% | 0.61% | 1166 | 1663 | 5.29bp |
| 2020 | 3.74 | 2.42 | 31.3% | 0.91% | 1154 | 1607 | 8.37bp |
| 2021 | 3.75 | 1.97 | 30.8% | 1.27% | 1243 | 1718 | 5.50bp |
| 2022 | **2.99** | 1.77 | 29.7% | 1.65% | 1212 | 1691 | 6.99bp |
| 2023 | 3.58 | 1.85 | 29.8% | 0.89% | 1148 | 1608 | 5.31bp |

**判定**：
- **10/10 年正收益**，最差年 S 2.99（2022），无平年、无负年 ⇒ 不触发「近3年 cv>0.5 / 有平年」拖累。
- 多空两侧**逐年均 >1000 只** ⇒ 非单边暴露、非小样本。
- TO 稳定在 **29.0–31.3%**（极差 2.3pp）⇒ 无换手突变。
- 生命周期：S/2Y = 3.93/3.14 = **1.25** ≪ 2.0 判死线。
- 衰减形态：S 由前段 4.2–5.5 缓降到后段 3.0–3.8，属**正常 alpha 衰减**，非崩塌（2023 已回升至 3.58）。

## 2 参数 / 结构敏感性（本轮 12 批 32 臂实测）

| 维 | 已扫取值 | S 区间 | prod 区间 | 结论 |
|---|---|---|---|---|
| decay | 4 / 8 / 16 | 2.87–3.93 | 0.661–0.687 | decay↑ 只换 prod −0.018，S 掉 1.06 ⇒ 取 4 |
| 机构腿时序窗 | 20 / 35 / 60 | 3.80–4.04 | — | 35 与 60 同档，20 明显差 |
| B 腿算子 | `ts_zscore` / `ts_rank` | 3.93–4.04 | 0.6794–0.6800 | 二者等价，取 `ts_rank`（有界、抗异常） |
| 合并层 | 含/不含外层 `group_rank`、含/不含 `divide` | 3.89–3.93 | 0.6794–0.6872 | 去 `divide` + 去外层 rank 更优 |
| 结构（合规四式） | bucket×2 / group_neutralize / trade_when×3 / **multiply** | 3.00–4.96 | **0.6787**（multiply）～0.8175（bucket） | **只有 multiply 同时满足合规 ∧ prod<0.70** |

**判定**：本件不是参数网格里「挑最好看」的那点，而是**合规前沿上的唯一可行点**（唯一 prod<0.70 的合规结构）。同族 bucket 形 S 更高（4.61）但 prod 0.8175 必拒 ⇒ 不存在「再调参数既能升 S 又能降 prod」的空间。

## 3 相关性与结构合规

| 项 | 值 | 判定 |
|---|---|---|
| prod（平台 `check_correlation`） | **0.6787**（histogram 0.6–0.7 仅 13 个，无 0.7+ 邻居） | PASS，余量 0.021 |
| self（本地 OS 池 21 只） | **0.4183**（top=Wjl6JJQO） | PASS，余量 0.28 |
| 闸5 `equal_weight_leg_add` | **False**（hits 0） | 合规 |
| `mix_review` | kind=**none**、blocked=False | 合规（连混腿都不算） |
| 数据源 | techindi_model × institutions6（双源，非单数据集） | 非 ATOM 单集 |
| 塔归属 | EUR/D1/INSTITUTIONS(1.1) + EUR/D1/OTHER(1.5) | 混塔取短板 1.1 |

## 4 结论

`verdict: PASS` — 可用于提交。唯一薄点：**sub/S = 0.534**（门槛 0.5303×3.93 = 2.084，实际 2.10，余量 0.016）。提交前**不得再调参数**（任何抬 S 不抬 sub 的改动都会顶穿 `LOW_SUB_UNIVERSE_SHARPE`）。
