# Insider 同族冷门集探针 P55-P57（2026-11-07）

目标：补测此前从未测过的 4 个 insider 语义数据集，评估能否补足交付颗数。
设置：KOR/TOP600/D1 · REVERSION_AND_MOMENTUM · decay4 · trunc0.08 · **nanHandling OFF**（VECTOR 事件族统一用 settings_ins2）。

## 1. P55 model244（Insider Transaction Analytics，30 字段，aC 17，cov 0.459）

| # | alpha | 表达式要点 | S | F | TO | 2Y | raF |
|---|---|---|---:|---:|---:|---:|---:|
| 10 | A1VEWz1e | `-group_rank(ts_mean(vec_stddev(mdl244_transaction_value),66),sector)` | **0.86** | 0.57 | 0.096 | 1.01 | 3 |
| 4 | vR1PqGKv | `-group_rank(ts_mean(vec_avg(mdl244_insider_holdings),22),sector)` | 0.70 | 0.38 | 0.177 | 0.59 | 3 |
| 2 | YP1Yrzj6 | `-group_rank(ts_std_dev(vec_sum(mdl244_transaction_value),66),sector)` | 0.60 | 0.35 | 0.121 | 0.68 | 3 |
| - | 其余 7 条 | significance / revision / sentiment / count / mcap归一 / zscore | -0.38~0.33 | - | - | - | 4-7 |

判定：**model244 判死**（天花板 0.86）。「aC 极低」再次被证明 ≠ 有信号（与 model238/model32 同型教训）。
另注：`vec_count` 与 `divide(...,market_cap)` 两条 TO 爆到 1.16-1.40，事件计数类不可直接 ts_zscore。

## 2. P56 insiders1（Global Insider Trading，9 字段，aC 549，cov 0.3526）

| # | alpha | 表达式要点 | S | F | TO | 2Y | raF |
|---|---|---|---:|---:|---:|---:|---:|
| 2 | E56x7No0 | `-group_rank(ts_sum(vec_sum(insd1_value),66),sector)` | **1.39** | 1.20 | 0.0991 | 1.18 | 2 |
| 5 | A1VEWeJd | `-group_rank(ts_mean(vec_sum(insd1_shares),66),sector)` | **1.36** | 1.24 | 0.1003 | **1.82** | 1（仅 LOW_SHARPE） |
| 1 | e75EpNAN | `-group_rank(ts_std_dev(vec_sum(insd1_value),66),sector)` | 0.95 | 0.76 | 0.132 | 0.70 | 3 |
| 3 | 88RXoVgl | `-group_rank(vec_count(insd1_value),sector)` | -0.37 | -0.09 | **1.389** | -1.26 | 6 |
| 4 | Xg9MrVXx | `-group_rank(ts_mean(vec_avg(insd1_tradesignificance),22),sector)` | -0.71 | -0.42 | 0.187 | -1.41 | 5 |

## 3. P57 insiders1 窗口/轴阶梯（对 1.36-1.39 两条最强腿做单杠杆位移）

| # | 变体 | S | F | TO | 2Y | raF |
|---|---|---:|---:|---:|---:|---:|
| 8 | shares W66 industry | 1.25 | 1.05 | 0.108 | 1.34 | 2 |
| 2 | value W88 sector | 1.25 | 1.00 | 0.086 | 1.30 | 2 |
| 7 | shares W88 sector | 1.21 | 1.01 | 0.088 | 1.81 | 1 |
| 6 | shares W44 sector | 1.19 | 1.07 | 0.126 | 1.81 | 1 |
| 1 | value W44 sector | 1.13 | 0.94 | 0.127 | 0.94 | 3 |
| 4 | value W66 industry | 1.11 | 0.84 | 0.108 | 0.84 | 3 |
| 9 | value W250 sector | 1.10 | 0.76 | 0.058 | 1.25 | 3 |
| 3 | value W132 sector | 0.94 | 0.64 | 0.072 | 0.90 | 3 |
| 5 | value W66 subindustry | 0.69 | 0.41 | 0.115 | 0.67 | 3 |
| 10 | value ts_zscore252 | -0.36 | -0.08 | **1.395** | -0.65 | 6 |

⇒ **W66 是局部峰**（1.36-1.39），所有位移都更低；industry 轴 1.11-1.25、subindustry 0.69 均劣于 sector。
insiders1 的 S 硬顶 ≈ **1.39**，距 1.58 差 0.19 且无杠杆可用 ⇒ **判死**（2Y 虽好但 S 是硬闸）。

## 4. model68（RAM，4 字段，aC 27，cov 0.85）

| # | alpha | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| 7 | `group_rank(ts_delta(vec_avg(mdl68_score),66),sector)` | 0.87 | 0.44 | 0.192 | -0.02 |
| 6 | `group_rank(ts_mean(vec_avg(mdl68_score),22),sector)` | 0.08 | 0.02 | 0.081 | -0.10 |
| 9 | `group_rank(ts_mean(vec_avg(mdl68_ram),22),sector)` | 0.08 | 0.02 | 0.079 | -0.04 |
| 8 / 10 | raw 反向 / score÷mktcap | -0.36 / -0.20 | - | - | - |

⇒ **model68 判死**（DREAM 动量分数在 KOR 无效；字段描述写的是「China-listed equity」，与 KOR 宇宙不符）。

## 5. 结论

| dataset | 判定 | 依据 |
|---|---|---|
| model244 | 判死 | 天花板 S0.86 |
| insiders1 | 判死 | 天花板 S1.39（W66 局部峰，位移全劣） |
| model68 | 判死 | 天花板 S0.87，本体 0.08 |
| other83 | 暂不测 | 与 model244 同源同名字段族，model244 已判死，边际价值极低 |

**本轮唯一合格新增：d5Wvpmbx（risk68，S1.82/F1.25/2Y4.10/raF0/self0.2023/prod0.6906）。**
KOR 交付推进至 **4/10**（待提交确认）。