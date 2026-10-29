# DEU · shortinterest3 因子挖掘经验

<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照

- 范围：DEU / shortinterest3；波次 s2_shortinterest3_d1, s2_si3_cwfix2_r70_d1, s2_si3_cwfix_r36_d1, s2_si3_decay2_d1, s2_si3_gate_d1, s2_si3_insider_starmine_hybrid_r33_d1, s2_si3_nan_d1, s2_si3_stat2_d1, s2_si3_subfam_r74_d1, s2_si3_var22_d1, s2_si3_var22_stat_d1, s2_si3_w15_d1, s2_tower_sprint_r94_d1, s2_tower_sprint_r95_d1, s2_unlit_tower_20261029；去重后 146 条已完成回测，20 个实用字段。
- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。
- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。
- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。
- 筛选：delay=全部（分设置展示）；waves=该数据集全部已回测波次。

| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |
|---|---|---|---|---|---|---|
| 1 | TOP500 | STATISTICAL | 4 | 0.08 | 2013-01-01 | 2023-12-31 |
| 1 | TOP500 | SUBINDUSTRY | 2 | 0.08 | 2013-01-01 | 2023-12-31 |
| 1 | TOP500 | SUBINDUSTRY | 4 | 0.08 | 2013-01-01 | 2023-12-31 |
| 1 | TOP500 | SUBINDUSTRY | 未核实 | 未核实 | 未核实 | 未核实 |
| 未核实 | 未核实 | 未核实 | 未核实 | 未核实 | 未核实 | 未核实 |

最高 Sharpe 候选：`blRnKEk6`，Sharpe=2.02，同条 Fitness=1.7，Prod=0.5766。

## 字段证据与使用经验

| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |
|---|---|---|---:|---|---|
| `average_loan_duration_days_main` | VECTOR / 0.6872 / 9 | The weighted average age of loans in this primary key group, measured in days | 2 | -0.4 / -0.15 (`2rOWavRx`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `directional_indicator` | 未核实 / 未核实 / 未核实 | 未核实 | 4 | 1.7 / 1.35 (`kqVOo8jd`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |
| `loan_rate_volatility_main` | VECTOR / 0.6872 / 29 | Standard deviation of loan rates across transactions in this primary key group | 1 | -0.82 / -0.47 (`883YaOra`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `loaned_market_value_usd_main` | VECTOR / 0.6872 / 8 | USD market value of the units lent in transactions in this primary key group | 1 | 0.16 / 0.06 (`vRk6e59w`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `loaned_market_value_usd_p5_d1` | VECTOR / 0.7833 / 23 | Market value in US dollars of units lent in transactions in this group | 2 | 0.25 / 0.1 (`3qoLemgZ`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `loaned_share_count_main` | VECTOR / 0.6872 / 9 | Number of units (shares or par value) lent in transactions in this primary key group | 2 | 0.09 / 0.01 (`N1Q3gn6e`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `loaned_share_count_p5_d1` | VECTOR / 0.7833 / 24 | Number of units (shares or par value) lent in transactions in this group | 6 | 0.3 / 0.07 (`KPJaGP21`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `max_loan_rate_main` | VECTOR / 0.6872 / 29 | Maximum loan rate among transactions in this group | 6 | 1.01 / 0.81 (`VkxJa1Z0`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mean_estimate_change_pct_f12m_earnings_14d_4` | 未核实 / 未核实 / 未核实 | 未核实 | 20 | 2.02 / 1.7 (`blRnKEk6`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |
| `mean_estimate_change_pct_f12m_ebitda_14d_4` | 未核实 / 未核实 / 未核实 | 未核实 | 18 | 2.01 / 1.81 (`ZY0M1G53`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |
| `mean_estimate_change_pct_f12m_ebitda_90d_3` | 未核实 / 未核实 / 未核实 | 未核实 | 3 | 2.02 / 1.7 (`blRnKEk6`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |
| `mean_loan_rate_main` | VECTOR / 0.6872 / 37 | Weighted average loan rate for transactions in this group | 52 | 2.02 / 1.7 (`blRnKEk6`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `mean_loan_rate_p5_d1` | VECTOR / 0.7833 / 69 | Weighted average loan rate for all transactions in this group | 7 | 1.02 / 0.79 (`O0AaNQRp`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `min_loan_rate_main` | VECTOR / 0.6872 / 11 | Minimum loan rate among transactions in this group | 32 | 1.28 / 1.19 (`QPvXYZ6G`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `predicted_surprise_f12m_ebitda_4` | 未核实 / 未核实 / 未核实 | 未核实 | 23 | 2.02 / 1.7 (`blRnKEk6`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |
| `predicted_surprise_pct_fy2_earnings_4` | 未核实 / 未核实 / 未核实 | 未核实 | 10 | 2.01 / 1.81 (`ZY0M1G53`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |
| `r94` | 未核实 / 未核实 / 未核实 | 未核实 | 8 | 1.78 / 1.37 (`Jjxrl0dx`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |
| `r95` | 未核实 / 未核实 / 未核实 | 未核实 | 12 | 1.83 / 1.49 (`E5vx03Q0`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |
| `shrt3_bar` | VECTOR / 0.6528 / 173 | Borrow demand rating on a 1–10 scale for a stock (1 = relatively low demand, 10 = relatively high) | 8 | 0.89 / 0.62 (`JjeKNqEW`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `transaction_count_p5_d1` | VECTOR / 0.7833 / 34 | Number of transactions that fit this primary key group | 6 | 0.25 / 0.1 (`3qoLemgZ`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |

## 已完成候选逐条记录

| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| s2_shortinterest3_d1 | `akLwANM9` | 0.73 | 0.36 | 1.28 | 22.78 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `vRk6e59w` | 0.16 | 0.06 | 0.01 | 6.63 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `N1Q3gn6e` | 0.09 | 0.01 | -0.26 | 25.51 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `RRVK2NYn` | -0.05 | -0.01 | 0.09 | 6.48 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `2rOWavRx` | -0.4 | -0.15 | 0.22 | 17.94 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `58QeaL9k` | -0.68 | -0.44 | -1.11 | 5.63 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `wpYPn5O2` | -0.73 | -0.36 | -1.28 | 22.78 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `883YaOra` | -0.82 | -0.47 | -1.33 | 18.89 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_insider_starmine_hybrid_r33_d1 | `O0rVN6xq` | 1.54 | 1.11 | 1.56 | 22.06 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_insider_starmine_hybrid_r33_d1 | `GrdxbQGJ` | 1.66 | 1.25 | 1.53 | 22.2 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_insider_starmine_hybrid_r33_d1 | `mLg1mK5x` | 1.51 | 1.16 | 1.49 | 19.56 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_insider_starmine_hybrid_r33_d1 | `xAYW3lNN` | 1.39 | 0.98 | 1.49 | 21.11 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_insider_starmine_hybrid_r33_d1 | `3q95XGp0` | 1.2 | 0.83 | 1.57 | 14.6 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_insider_starmine_hybrid_r33_d1 | `e79vb13M` | 1.39 | 0.97 | 1.26 | 17.03 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_insider_starmine_hybrid_r33_d1 | `kqVOo8jd` | 1.7 | 1.35 | 1.4 | 16.49 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_insider_starmine_hybrid_r33_d1 | `2rOWwGlP` | 0.98 | 0.67 | 1.09 | 16.45 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_cwfix_r36_d1 | `1YxPZN5J` | 1.71 | 1.2 | 2.04 | 24.79 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_cwfix_r36_d1 | `RRVK6ELb` | 1.73 | 1.28 | 2.13 | 22.85 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_cwfix_r36_d1 | `rK5VeRm9` | 1.66 | 1.18 | 1.44 | 23.73 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_cwfix_r36_d1 | `KPOQrJRp` | 1.72 | 1.36 | 1.5 | 19.08 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_cwfix_r36_d1 | `Jjx1Qelj` | 1.59 | 1.12 | 2.12 | 22.93 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_cwfix_r36_d1 | `kqVOgNRl` | 1.65 | 1.25 | 1.42 | 21.56 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_cwfix_r36_d1 | `j23x8YLW` | 1.71 | 1.2 | 2.04 | 24.79 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_cwfix_r36_d1 | `qMW30LbP` | 1.4 | 0.93 | 1.56 | 22.87 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_cwfix2_r70_d1 | `rK5VnXY3` | 1.91 | 1.39 | 2.78 | 19.64 | 未核实 | 未核实 | 0.8859 | 未核实 |
| s2_si3_cwfix2_r70_d1 | `WjP0x8Md` | 1.92 | 1.48 | 2.55 | 18.26 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_cwfix2_r70_d1 | `wpYPvgqY` | 1.82 | 1.41 | 2.23 | 20.96 | 未核实 | 未核实 | 0.9251 | 未核实 |
| s2_si3_cwfix2_r70_d1 | `vRk6og8b` | 1.8 | 1.47 | 2.1 | 19.03 | 未核实 | 未核实 | 0.6877 | 0.6877 |
| s2_si3_cwfix2_r70_d1 | `ZY0M1G53` | 2.01 | 1.81 | 2.77 | 14.36 | 未核实 | 未核实 | 0.8982 | 未核实 |
| s2_si3_cwfix2_r70_d1 | `MP1Z2mWk` | 1.82 | 1.7 | 2.11 | 15.02 | 未核实 | 未核实 | 0.8829 | 未核实 |
| s2_si3_cwfix2_r70_d1 | `blRnKEk6` | 2.02 | 1.7 | 2.74 | 16.15 | 未核实 | 未核实 | 0.5766 | 0 |
| s2_si3_cwfix2_r70_d1 | `d5OoPLXJ` | 1.17 | 0.91 | 0.78 | 20.06 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_si3_subfam_r74_d1 | `A10m8LjW` | 1.96 | 1.79 | 2.67 | 13.55 | 未核实 | 未核实 | 0.8473 | 未核实 |
| s2_si3_subfam_r74_d1 | `78ZMRGW8` | 1.84 | 1.35 | 2.6 | 18.65 | 未核实 | 未核实 | 0.8114 | 未核实 |
| s2_si3_subfam_r74_d1 | `gJQdVr6M` | 1.68 | 1.44 | 2.36 | 11.41 | 未核实 | 未核实 | 0.7859 | 未核实 |
| s2_si3_subfam_r74_d1 | `mLg1WK3p` | 1.88 | 1.71 | 2.11 | 13.32 | 未核实 | 未核实 | 0.8104 | 未核实 |
| s2_si3_subfam_r74_d1 | `O0rVX6Y7` | 1.71 | 1.47 | 2.74 | 11.1 | 未核实 | 未核实 | 0.776 | 未核实 |
| s2_si3_subfam_r74_d1 | `6XrJLG8J` | 1.99 | 1.83 | 2.6 | 13.64 | 未核实 | 未核实 | 0.8963 | 0.8962289970696277 |
| s2_si3_subfam_r74_d1 | `Grdx5QAJ` | 1.89 | 1.6 | 2.2 | 14.82 | 未核实 | 未核实 | 0.9051 | 未核实 |
| s2_tower_sprint_r94_d1 | `qMWVeeME` | 1.64 | 1.42 | 1.67 | 12.42 | 未核实 | 未核实 | 0.9529 | 未核实 |
| s2_tower_sprint_r94_d1 | `d5OveekX` | 1.41 | 1.19 | 1.36 | 12.22 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r94_d1 | `P0ZKjjQp` | 1.42 | 1.21 | 1.36 | 12.23 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r94_d1 | `pwP3QQYx` | 1.64 | 1.43 | 1.48 | 12.64 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r94_d1 | `58QYR7MN` | 1.66 | 1.25 | 1.52 | 20.37 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r94_d1 | `xAY5Mwng` | 1.68 | 1.3 | 1.46 | 19.76 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r94_d1 | `Jjxrl0dx` | 1.78 | 1.37 | 2.04 | 19.76 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r94_d1 | `78ZlOqd5` | 1.63 | 1.22 | 1.56 | 20.29 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r95_d1 | `E5vx03Q0` | 1.83 | 1.49 | 2.1 | 19.6 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r95_d1 | `pwP3J0db` | 1.47 | 1.14 | 1.39 | 17.63 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r95_d1 | `3q9JYdoe` | 1.38 | 1.02 | 1.13 | 18.11 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r95_d1 | `blRA2p6l` | 1.37 | 1.06 | 1.32 | 17.66 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r95_d1 | `npKrYpQl` | 1.76 | 1.66 | 1.64 | 12.15 | 未核实 | 未核实 | 0.9562 | 未核实 |
| s2_tower_sprint_r95_d1 | `JjxrYjre` | 1.68 | 1.47 | 1.69 | 12.31 | 未核实 | 未核实 | 0.6453 | 0.6453 |
| s2_tower_sprint_r95_d1 | `le81keYe` | 1.68 | 1.48 | 1.75 | 12.39 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r95_d1 | `QP36qPoK` | 1.66 | 1.47 | 1.42 | 12.58 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r95_d1 | `E5vxY52J` | 1.57 | 1.35 | 1.35 | 12.66 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r95_d1 | `O0rgq0j7` | 1.53 | 1.3 | 1.28 | 12.6 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r95_d1 | `pwP3oweX` | 0.67 | 0.45 | 1.29 | 11.08 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_tower_sprint_r95_d1 | `9qVkbqOV` | 1.42 | 0.98 | 2.03 | 17.05 | 未核实 | 未核实 | 未核实 | 未核实 |
| s2_unlit_tower_20261029 | `78L9aY2O` | 0.67 | 0.69 | 0.25 | 10.8 | 0.35 | 未核实 | 未核实 | 未核实 |
| s2_unlit_tower_20261029 | `3qoLa02O` | 0.88 | 0.81 | 0.64 | 8.57 | 0.59 | 未核实 | 未核实 | 未核实 |
| s2_unlit_tower_20261029 | `wpQg5xZp` | 0.95 | 0.75 | 1.1 | 8.9 | 0.62 | 未核实 | 未核实 | 未核实 |
| s2_unlit_tower_20261029 | `akKvNZbv` | 0.81 | 0.89 | 0.37 | 5.54 | 0.51 | 未核实 | 未核实 | 未核实 |
| s2_unlit_tower_20261029 | `1YNEopE6` | 0.68 | 0.31 | 1.26 | 22.18 | 0.5 | 未核实 | 未核实 | 未核实 |
| s2_unlit_tower_20261029 | `9qx09por` | 0.76 | 0.39 | 1.25 | 21.56 | 0.74 | 未核实 | 未核实 | 未核实 |
| s2_unlit_tower_20261029 | `gJepxE2m` | 0.98 | 0.76 | 1.3 | 8.36 | 0.54 | 未核实 | 未核实 | 未核实 |
| s2_unlit_tower_20261029 | `wpQgLMr2` | 0.93 | 0.69 | 1.3 | 8.82 | 0.63 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `WjO8VlNG` | 0.87 | 0.37 | 1.03 | 32.24 | 0.69 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `KPJaGP21` | 0.3 | 0.07 | 0.51 | 29.71 | 0.28 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `3qoLemgZ` | 0.25 | 0.1 | 0.65 | 6.88 | -0.17 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `78L9z8r1` | 0.22 | 0.06 | -0.27 | 18.22 | 0.76 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `leAX3wxl` | 0.16 | 0.03 | 0.29 | 26.85 | 0.68 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `d5WLRalv` | 0.12 | 0.03 | 0.29 | 5.18 | -0.34 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `j2YmrkLe` | 0.03 | 0 | -0.29 | 20.34 | 0.29 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `npvV8G0d` | -0.02 | 0 | 0.18 | 1.58 | -0.38 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `zq3pR7aG` | -0.02 | 0 | 0.37 | 1.59 | -0.31 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `RREW1xXg` | -0.05 | -0.01 | 0.21 | 1.74 | -0.4 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `j2YmrPZk` | -0.1 | -0.03 | -0.09 | 1.64 | -0.96 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `88R1eWAq` | -0.15 | -0.05 | -0.16 | 1.94 | -0.8 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `P0o9OYp7` | -0.17 | -0.05 | -0.26 | 2.57 | -0.65 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `O0AaG02R` | -0.17 | -0.03 | -0.55 | 42.71 | 0.01 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `d5WLR30w` | -0.2 | -0.05 | -0.48 | 20.75 | 0.32 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `RREW1l81` | -0.3 | -0.12 | -0.29 | 1.71 | -0.83 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `E56JeQgL` | -0.37 | -0.17 | -0.86 | 2.16 | -0.42 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `78L9nvw8` | -0.41 | -0.2 | -1.15 | 2.62 | -0.42 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `O0AaxWnv` | -0.44 | -0.23 | -0.93 | 2.46 | -0.5 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `d5WLR3dJ` | -0.44 | -0.23 | -1.26 | 2.26 | -0.36 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `JjeKvWde` | -0.44 | -0.21 | -0.99 | 2.22 | -0.49 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `58EWkJaN` | -0.51 | -0.3 | -1.24 | 2.1 | -0.32 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `1YNEzlgm` | -0.61 | -0.24 | -0.25 | 32.06 | -0.87 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `MPYmGPno` | -0.66 | -0.37 | -2.22 | 10.94 | -0.93 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `vR1gvAdw` | -0.67 | -0.4 | -1.14 | 3.73 | -0.63 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `58EWkKN6` | -0.75 | -0.47 | -1.58 | 3.43 | -0.6 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `wpQgEonl` | -0.89 | -0.39 | -0.95 | 36.86 | -0.75 | 未核实 | 未核实 | 未核实 |
| s2_shortinterest3_d1 | `npvV8anq` | -0.9 | -0.57 | -1.2 | 15.56 | -0.88 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `2rAdl8XJ` | 1.15 | 0.71 | 2.17 | 24.69 | 1.09 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `N1N97xJo` | 1.12 | 0.98 | 1.68 | 8.77 | 0.81 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `MPYm7Mdo` | 0.99 | 0.97 | 0.73 | 10.56 | 0.73 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `A1VKljLl` | 0.95 | 0.75 | 1.1 | 8.9 | 0.62 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `LLMJ7VEM` | 0.93 | 0.69 | 1.3 | 8.82 | 0.63 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `j2Ym6xqe` | 0.92 | 0.69 | 1.13 | 8.27 | 0.57 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `58EWpeP6` | 0.89 | 0.68 | 0.89 | 4.79 | 0.68 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `VkxJ71Zb` | 0.86 | 0.65 | 1.28 | 9.62 | 0.35 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `3qoLlQGO` | 0.83 | 0.55 | 1.31 | 7.76 | 0.34 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `npvVNr1d` | 0.69 | 0.47 | 1.05 | 9.28 | 0.25 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `78L9j731` | 0.67 | 0.69 | 0.25 | 10.73 | 0.34 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_d1 | `xArgNWJJ` | -0.06 | -0.01 | -0.57 | 10.89 | -0.46 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_stat_d1 | `omEOqlvl` | 0.89 | 0.55 | 0.4 | 15.54 | 0.48 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_stat_d1 | `j2Ymj38Q` | 0.89 | 0.53 | -0.08 | 15.54 | 0.39 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_stat_d1 | `LLMJ7951` | 0.76 | 0.4 | 0.17 | 13.09 | 0.44 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_stat_d1 | `pwdOjPvX` | 0.75 | 0.4 | -0.18 | 9.9 | 0.37 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_stat_d1 | `E56JlvpK` | 0.74 | 0.39 | 0.99 | 13.28 | 0.3 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_stat_d1 | `P0o97Z2K` | 0.63 | 0.3 | 0.01 | 13.19 | 0.27 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_stat_d1 | `akKv7LV2` | 0.61 | 0.28 | 0.5 | 13.67 | -0.01 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_stat_d1 | `6XdOlrKJ` | 0.6 | 0.2 | 1.06 | 26.88 | 0.54 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_stat_d1 | `vR1gjk2d` | 0.33 | 0.11 | 0.41 | 12.94 | -0.27 | 未核实 | 未核实 | 未核实 |
| s2_si3_var22_stat_d1 | `LLMJ7162` | 0.16 | 0.04 | 0.88 | 13.06 | -0.23 | 未核实 | 未核实 | 未核实 |
| s2_si3_gate_d1 | `kqNlVngl` | 1.21 | 1.09 | 1.78 | 11.2 | 0.95 | 未核实 | 未核实 | 未核实 |
| s2_si3_gate_d1 | `gJepQmb0` | 0.96 | 0.97 | 1.13 | 10.48 | 0.69 | 未核实 | 未核实 | 未核实 |
| s2_si3_gate_d1 | `zq3pY5bO` | 0.92 | 0.72 | 1.21 | 5.8 | 0.58 | 未核实 | 未核实 | 未核实 |
| s2_si3_gate_d1 | `RREWVNbb` | 0.87 | 0.67 | 1.46 | 5.14 | 0.47 | 未核实 | 未核实 | 未核实 |
| s2_si3_gate_d1 | `LLMJ9nN6` | 0.49 | 0.24 | 0.75 | 12.47 | 0.37 | 未核实 | 未核实 | 未核实 |
| s2_si3_w15_d1 | `wpQgZKN2` | 1.22 | 1.08 | 1.91 | 13.06 | 1.04 | 未核实 | 未核实 | 未核实 |
| s2_si3_w15_d1 | `78L9N7G5` | 1.22 | 1.11 | 1.7 | 9.96 | 0.83 | 未核实 | 未核实 | 未核实 |
| s2_si3_w15_d1 | `KPJaNlVk` | 1.1 | 0.87 | 1.9 | 14.87 | 1.02 | 未核实 | 未核实 | 未核实 |
| s2_si3_w15_d1 | `QPvXbZOr` | 1.04 | 0.86 | 1.32 | 11.34 | 0.86 | 未核实 | 未核实 | 未核实 |
| s2_si3_w15_d1 | `E56JpON1` | 1.03 | 1.04 | 1.41 | 13.08 | 0.81 | 未核实 | 未核实 | 未核实 |
| s2_si3_w15_d1 | `O0AaNQRp` | 1.02 | 0.79 | 1.55 | 11.36 | 0.84 | 未核实 | 未核实 | 未核实 |
| s2_si3_w15_d1 | `VkxJa1Z0` | 1.01 | 0.81 | 1.5 | 12.2 | 0.63 | 未核实 | 未核实 | 未核实 |
| s2_si3_w15_d1 | `JjeKNqEW` | 0.89 | 0.62 | 1.13 | 8.47 | 0.46 | 未核实 | 未核实 | 未核实 |
| s2_si3_w15_d1 | `88R1jb9l` | 0.79 | 0.51 | 1.5 | 10.21 | 0.64 | 未核实 | 未核实 | 未核实 |
| s2_si3_w15_d1 | `xArg3OVg` | 0.44 | 0.23 | 0.7 | 3.36 | 0.05 | 未核实 | 未核实 | 未核实 |
| s2_si3_nan_d1 | `6XdOjAgO` | 1.22 | 1.08 | 1.91 | 13.06 | 1.04 | 未核实 | 未核实 | 未核实 |
| s2_si3_nan_d1 | `JjeKNPRm` | 1.22 | 1.11 | 1.7 | 9.96 | 0.83 | 未核实 | 未核实 | 未核实 |
| s2_si3_nan_d1 | `GrWJbgEG` | 1.21 | 1.09 | 1.78 | 11.2 | 0.95 | 未核实 | 未核实 | 未核实 |
| s2_si3_nan_d1 | `A1VKNQqe` | 1.03 | 1.04 | 1.41 | 13.08 | 0.81 | 未核实 | 未核实 | 未核实 |
| s2_si3_stat2_d1 | `9qx0WR0V` | 1.26 | 1.17 | 1.76 | 8.95 | 0.92 | 未核实 | 未核实 | 未核实 |
| s2_si3_stat2_d1 | `6XdOKEOJ` | 1.17 | 1 | 1.88 | 10.78 | 0.83 | 未核实 | 未核实 | 未核实 |
| s2_si3_stat2_d1 | `leAXK0b5` | 1.07 | 0.82 | 1.07 | 15.07 | 0.95 | 未核实 | 未核实 | 未核实 |
| s2_si3_stat2_d1 | `VkxJ08g8` | 1 | 0.81 | 0.91 | 12.88 | 0.83 | 未核实 | 未核实 | 未核实 |
| s2_si3_stat2_d1 | `O0Aa89aq` | 0.73 | 0.41 | 0.76 | 18.52 | 0.42 | 未核实 | 未核实 | 未核实 |
| s2_si3_stat2_d1 | `pwdO57gX` | 0.45 | 0.24 | 0.1 | 14.42 | 0.64 | 未核实 | 未核实 | 未核实 |
| s2_si3_stat2_d1 | `78L96d98` | 0.26 | 0.09 | -1.06 | 11.93 | -0.12 | 未核实 | 未核实 | 未核实 |
| s2_si3_decay2_d1 | `QPvXYZ6G` | 1.28 | 1.19 | 1.76 | 9.54 | 0.93 | 未核实 | 未核实 | 未核实 |
| s2_si3_decay2_d1 | `npvVAxXx` | 1.26 | 1.16 | 1.69 | 11.2 | 0.86 | 未核实 | 未核实 | 未核实 |
| s2_si3_decay2_d1 | `e75R6kEE` | 1.21 | 0.99 | 1.88 | 15.12 | 1.09 | 未核实 | 未核实 | 未核实 |

### 原式与局部失败证据

**akLwANM9（wave s2_shortinterest3_d1）**

```text
-rank(vec_avg(mean_loan_rate_main))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE。

**vRk6e59w（wave s2_shortinterest3_d1）**

```text
rank(vec_sum(loaned_market_value_usd_main))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**N1Q3gn6e（wave s2_shortinterest3_d1）**

```text
rank(ts_delta(vec_sum(loaned_share_count_main), 21))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE。

**RRVK2NYn（wave s2_shortinterest3_d1）**

```text
-rank(vec_sum(loaned_share_count_main))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE。

**2rOWavRx（wave s2_shortinterest3_d1）**

```text
rank(vec_avg(average_loan_duration_days_main))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**58QeaL9k（wave s2_shortinterest3_d1）**

```text
rank(ts_mean(vec_avg(mean_loan_rate_main), 22))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**wpYPn5O2（wave s2_shortinterest3_d1）**

```text
rank(vec_avg(mean_loan_rate_main))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**883YaOra（wave s2_shortinterest3_d1）**

```text
rank(vec_avg(loan_rate_volatility_main))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**O0rVN6xq（wave s2_si3_insider_starmine_hybrid_r33_d1）**

```text
add(add(-rank(vec_avg(mean_loan_rate_main)), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5)))
```

已存检查失败：LOW_SHARPE, CONCENTRATED_WEIGHT, IS_LADDER_SHARPE。

**GrdxbQGJ（wave s2_si3_insider_starmine_hybrid_r33_d1）**

```text
add(add(add(-rank(vec_avg(mean_loan_rate_main)), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)))
```

已存检查失败：CONCENTRATED_WEIGHT, IS_LADDER_SHARPE。

**mLg1mK5x（wave s2_si3_insider_starmine_hybrid_r33_d1）**

```text
add(add(add(-rank(vec_avg(mean_loan_rate_main)), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 5)))
```

已存检查失败：LOW_SHARPE, CONCENTRATED_WEIGHT, IS_LADDER_SHARPE。

**xAYW3lNN（wave s2_si3_insider_starmine_hybrid_r33_d1）**

```text
add(add(-rank(vec_avg(mean_loan_rate_main)), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))), rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 5)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, IS_LADDER_SHARPE。

**3q95XGp0（wave s2_si3_insider_starmine_hybrid_r33_d1）**

```text
add(add(rank(ts_sum(ts_backfill(directional_indicator, 66), 252)), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, IS_LADDER_SHARPE。

**e79vb13M（wave s2_si3_insider_starmine_hybrid_r33_d1）**

```text
add(add(add(rank(ts_sum(ts_backfill(directional_indicator, 66), 252)), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, IS_LADDER_SHARPE。

**kqVOo8jd（wave s2_si3_insider_starmine_hybrid_r33_d1）**

```text
add(add(add(add(rank(ts_sum(ts_backfill(directional_indicator, 66), 252)), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)))
```

已存检查失败：IS_LADDER_SHARPE。

**2rOWwGlP（wave s2_si3_insider_starmine_hybrid_r33_d1）**

```text
add(add(rank(ts_sum(ts_backfill(directional_indicator, 66), 252)), -rank(vec_avg(mean_loan_rate_main))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, IS_LADDER_SHARPE。

**1YxPZN5J（wave s2_si3_cwfix_r36_d1）**

```text
add(add(add(-group_rank(vec_avg(mean_loan_rate_main), subindustry), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)))
```

已存检查失败：CONCENTRATED_WEIGHT。

**RRVK6ELb（wave s2_si3_cwfix_r36_d1）**

```text
add(add(add(add(-group_rank(vec_avg(mean_loan_rate_main), subindustry), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))), rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 5)))
```

已存检查失败：CONCENTRATED_WEIGHT。

**rK5VeRm9（wave s2_si3_cwfix_r36_d1）**

```text
add(add(add(-group_rank(vec_avg(mean_loan_rate_main), industry), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)))
```

已存检查失败：CONCENTRATED_WEIGHT, IS_LADDER_SHARPE。

**KPOQrJRp（wave s2_si3_cwfix_r36_d1）**

```text
add(add(add(-group_rank(ts_mean(vec_avg(mean_loan_rate_main), 5), subindustry), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)))
```

已存检查失败：CONCENTRATED_WEIGHT, IS_LADDER_SHARPE。

**Jjx1Qelj（wave s2_si3_cwfix_r36_d1）**

```text
add(add(add(-group_rank(vec_avg(mean_loan_rate_main), subindustry), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5)))
```

已存检查失败：CONCENTRATED_WEIGHT。

**kqVOgNRl（wave s2_si3_cwfix_r36_d1）**

```text
add(add(add(add(-group_rank(vec_avg(mean_loan_rate_main), industry), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))), rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 5)))
```

已存检查失败：CONCENTRATED_WEIGHT, IS_LADDER_SHARPE。

**j23x8YLW（wave s2_si3_cwfix_r36_d1）**

```text
add(add(add(winsorize(-group_rank(vec_avg(mean_loan_rate_main), subindustry), std=4), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)))
```

已存检查失败：CONCENTRATED_WEIGHT。

**qMW30LbP（wave s2_si3_cwfix_r36_d1）**

```text
add(add(add(-group_rank(vec_avg(mean_loan_rate_main), subindustry), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 22)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, IS_LADDER_SHARPE。

**rK5VnXY3（wave s2_si3_cwfix2_r70_d1）**

```text
add(add(add(if_else(is_nan(-rank(vec_avg(mean_loan_rate_main))), 0, -rank(vec_avg(mean_loan_rate_main))), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**WjP0x8Md（wave s2_si3_cwfix2_r70_d1）**

```text
add(add(add(add(if_else(is_nan(-rank(vec_avg(mean_loan_rate_main))), 0, -rank(vec_avg(mean_loan_rate_main))), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))), rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 5)))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**wpYPvgqY（wave s2_si3_cwfix2_r70_d1）**

```text
add(add(add(-rank(ts_backfill(vec_avg(mean_loan_rate_main), 252)), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**vRk6og8b（wave s2_si3_cwfix2_r70_d1）**

```text
add(add(add(add(-rank(ts_backfill(vec_avg(mean_loan_rate_main), 252)), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))), rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 5)))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**ZY0M1G53（wave s2_si3_cwfix2_r70_d1）**

```text
add(add(add(add(if_else(is_nan(-rank(vec_avg(mean_loan_rate_main))), 0, -rank(vec_avg(mean_loan_rate_main))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 22))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22)))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**MP1Z2mWk（wave s2_si3_cwfix2_r70_d1）**

```text
add(add(add(add(-rank(ts_backfill(vec_avg(mean_loan_rate_main), 252)), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 22))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22)))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**blRnKEk6（wave s2_si3_cwfix2_r70_d1）**

```text
add(add(add(if_else(is_nan(-rank(vec_avg(mean_loan_rate_main))), 0, -rank(vec_avg(mean_loan_rate_main))), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22)))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**d5OoPLXJ（wave s2_si3_cwfix2_r70_d1）**

```text
add(add(add(-group_backfill(vec_avg(mean_loan_rate_main), subindustry, 252), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, IS_LADDER_SHARPE。

**A10m8LjW（wave s2_si3_subfam_r74_d1）**

```text
RV+Vk65变体
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**78ZMRGW8（wave s2_si3_subfam_r74_d1）**

```text
RV+经典3腿
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**gJQdVr6M（wave s2_si3_subfam_r74_d1）**

```text
LV+Vk65式
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**mLg1WK3p（wave s2_si3_subfam_r74_d1）**

```text
DV+Vk65式
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**O0rVX6Y7（wave s2_si3_subfam_r74_d1）**

```text
RV+LV双腿
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**6XrJLG8J（wave s2_si3_subfam_r74_d1）**

```text
RV+Vk65式
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**Grdx5QAJ（wave s2_si3_subfam_r74_d1）**

```text
DV+le89式
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**qMWVeeME（wave s2_tower_sprint_r94_d1）**

```text
R94
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**d5OveekX（wave s2_tower_sprint_r94_d1）**

```text
R94
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**P0ZKjjQp（wave s2_tower_sprint_r94_d1）**

```text
R94
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**pwP3QQYx（wave s2_tower_sprint_r94_d1）**

```text
R94
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**58QYR7MN（wave s2_tower_sprint_r94_d1）**

```text
R94
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**xAY5Mwng（wave s2_tower_sprint_r94_d1）**

```text
R94
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**Jjxrl0dx（wave s2_tower_sprint_r94_d1）**

```text
R94
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**78ZlOqd5（wave s2_tower_sprint_r94_d1）**

```text
R94
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**E5vx03Q0（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**pwP3J0db（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**3q9JYdoe（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**blRA2p6l（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**npKrYpQl（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**JjxrYjre（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**le81keYe（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**QP36qPoK（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**E5vxY52J（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**O0rgq0j7（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**pwP3oweX（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**9qVkbqOV（wave s2_tower_sprint_r95_d1）**

```text
R95
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**78L9aY2O（wave s2_unlit_tower_20261029）**

```text
reverse(group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22), exchange))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE。

**3qoLa02O（wave s2_unlit_tower_20261029）**

```text
reverse(group_zscore(ts_std_dev(vec_avg(mean_loan_rate_main), 22), exchange))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE。

**wpQg5xZp（wave s2_unlit_tower_20261029）**

```text
reverse(group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22), industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**akKvNZbv（wave s2_unlit_tower_20261029）**

```text
reverse(group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 66), exchange))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE。

**1YNEopE6（wave s2_unlit_tower_20261029）**

```text
-rank(ts_backfill(vec_avg(mean_loan_rate_p5_d1), 22))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**9qx09por（wave s2_unlit_tower_20261029）**

```text
-rank(ts_backfill(vec_avg(mean_loan_rate_main), 22))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**gJepxE2m（wave s2_unlit_tower_20261029）**

```text
reverse(group_zscore(ts_std_dev(vec_avg(mean_loan_rate_main), 22), industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**wpQgLMr2（wave s2_unlit_tower_20261029）**

```text
reverse(group_zscore(ts_covariance(vec_avg(mean_loan_rate_p5_d1), vec_avg(mean_loan_rate_p5_d1), 22), industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**WjO8VlNG（wave s2_shortinterest3_d1）**

```text
-rank(ts_zscore(ts_backfill(vec_avg(shrt3_bar), 66), 252))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**KPJaGP21（wave s2_shortinterest3_d1）**

```text
rank(ts_delta(ts_zscore(ts_backfill(vec_avg(loaned_share_count_p5_d1), 252), 252), 22))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**3qoLemgZ（wave s2_shortinterest3_d1）**

```text
rank(divide(vec_avg(loaned_market_value_usd_p5_d1), add(vec_avg(transaction_count_p5_d1), 1)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**78L9z8r1（wave s2_shortinterest3_d1）**

```text
rank(ts_rank(ts_backfill(vec_avg(loaned_market_value_usd_p5_d1), 252), 252))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**leAX3wxl（wave s2_shortinterest3_d1）**

```text
group_rank(winsorize(ts_zscore(ts_backfill(vec_avg(loaned_share_count_p5_d1), 252), 66), std=4), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**d5WLRalv（wave s2_shortinterest3_d1）**

```text
-rank(ts_std_dev(ts_backfill(vec_avg(shrt3_bar), 66), 66))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**j2YmrkLe（wave s2_shortinterest3_d1）**

```text
ts_zscore(vec_avg(loaned_share_count_p5_d1), 252)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE。

**npvV8G0d（wave s2_shortinterest3_d1）**

```text
rank(ts_mean(vec_avg(loaned_share_count_p5_d1), 252))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**zq3pR7aG（wave s2_shortinterest3_d1）**

```text
group_rank(ts_mean(vec_avg(loaned_share_count_p5_d1), 252), subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**RREW1xXg（wave s2_shortinterest3_d1）**

```text
group_rank(ts_mean(vec_avg(loaned_share_count_p5_d1), 252), industry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**j2YmrPZk（wave s2_shortinterest3_d1）**

```text
rank(ts_mean(vec_avg(transaction_count_p5_d1), 252))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**88R1eWAq（wave s2_shortinterest3_d1）**

```text
group_rank(ts_mean(vec_avg(transaction_count_p5_d1), 252), industry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**P0o9OYp7（wave s2_shortinterest3_d1）**

```text
group_rank(ts_mean(ts_backfill(vec_avg(transaction_count_p5_d1), 252), 66), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**O0AaG02R（wave s2_shortinterest3_d1）**

```text
rank(ts_delta(ts_backfill(vec_avg(mean_loan_rate_p5_d1), 252), 22))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**d5WLR30w（wave s2_shortinterest3_d1）**

```text
ts_zscore(vec_avg(transaction_count_p5_d1), 252)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE。

**RREW1l81（wave s2_shortinterest3_d1）**

```text
group_rank(ts_mean(vec_avg(transaction_count_p5_d1), 252), subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**E56JeQgL（wave s2_shortinterest3_d1）**

```text
group_rank(ts_mean(vec_avg(shrt3_bar), 252), subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**78L9nvw8（wave s2_shortinterest3_d1）**

```text
group_rank(ts_mean(vec_avg(mean_loan_rate_main), 252), industry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**O0AaxWnv（wave s2_shortinterest3_d1）**

```text
group_rank(ts_mean(vec_avg(shrt3_bar), 252), industry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**d5WLR3dJ（wave s2_shortinterest3_d1）**

```text
rank(ts_mean(vec_avg(mean_loan_rate_main), 252))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**JjeKvWde（wave s2_shortinterest3_d1）**

```text
group_rank(ts_mean(vec_avg(mean_loan_rate_main), 252), subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**58EWkJaN（wave s2_shortinterest3_d1）**

```text
rank(ts_mean(vec_avg(shrt3_bar), 252))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**1YNEzlgm（wave s2_shortinterest3_d1）**

```text
ts_zscore(vec_avg(mean_loan_rate_main), 252)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**MPYmGPno（wave s2_shortinterest3_d1）**

```text
trade_when(rank(ts_backfill(vec_avg(average_loan_duration_days_main), 252)) > 0.5, rank(ts_backfill(vec_avg(mean_loan_rate_main), 252)), 0)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**vR1gvAdw（wave s2_shortinterest3_d1）**

```text
group_rank(ts_mean(ts_backfill(vec_avg(mean_loan_rate_main), 252), 66), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**58EWkKN6（wave s2_shortinterest3_d1）**

```text
rank(ts_decay_linear(ts_backfill(vec_avg(mean_loan_rate_p5_d1), 252), 66))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**wpQgEonl（wave s2_shortinterest3_d1）**

```text
ts_zscore(vec_avg(shrt3_bar), 252)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**npvV8anq（wave s2_shortinterest3_d1）**

```text
group_rank(ts_backfill(subtract(vec_avg(max_loan_rate_main), vec_avg(min_loan_rate_main)), 252), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**2rAdl8XJ（wave s2_si3_var22_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 5), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT。

**N1N97xJo（wave s2_si3_var22_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS。

**MPYm7Mdo（wave s2_si3_var22_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22), densify(sector))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**A1VKljLl（wave s2_si3_var22_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**LLMJ7VEM（wave s2_si3_var22_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_p5_d1), vec_avg(mean_loan_rate_p5_d1), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**j2Ym6xqe（wave s2_si3_var22_d1）**

```text
-group_zscore(ts_std_dev(ts_backfill(vec_avg(mean_loan_rate_main), 22), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**58EWpeP6（wave s2_si3_var22_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 66), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**VkxJ71Zb（wave s2_si3_var22_d1）**

```text
-group_zscore(ts_covariance(vec_avg(max_loan_rate_main), vec_avg(max_loan_rate_main), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**3qoLlQGO（wave s2_si3_var22_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22), densify(subindustry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**npvVNr1d（wave s2_si3_var22_d1）**

```text
-group_zscore(ts_covariance(subtract(vec_avg(max_loan_rate_main), vec_avg(min_loan_rate_main)), subtract(vec_avg(max_loan_rate_main), vec_avg(min_loan_rate_main)), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**78L9j731（wave s2_si3_var22_d1）**

```text
-zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE。

**xArgNWJJ（wave s2_si3_var22_d1）**

```text
-group_zscore(ts_covariance(vec_avg(shrt3_bar), vec_avg(shrt3_bar), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**omEOqlvl（wave s2_si3_var22_stat_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 22), densify(sector))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**j2Ymj38Q（wave s2_si3_var22_stat_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22), densify(sector))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**LLMJ7951（wave s2_si3_var22_stat_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_p5_d1), vec_avg(mean_loan_rate_p5_d1), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**pwdOjPvX（wave s2_si3_var22_stat_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 66), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**E56JlvpK（wave s2_si3_var22_stat_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**P0o97Z2K（wave s2_si3_var22_stat_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**akKv7LV2（wave s2_si3_var22_stat_d1）**

```text
-group_zscore(ts_covariance(vec_avg(max_loan_rate_main), vec_avg(max_loan_rate_main), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**6XdOlrKJ（wave s2_si3_var22_stat_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 5), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE。

**vR1gjk2d（wave s2_si3_var22_stat_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22), densify(subindustry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**LLMJ7162（wave s2_si3_var22_stat_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 22), densify(subindustry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**kqNlVngl（wave s2_si3_gate_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 15), densify(industry))
```

已存检查失败：LOW_SHARPE。

**gJepQmb0（wave s2_si3_gate_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 22), densify(sector))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**zq3pY5bO（wave s2_si3_gate_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 44), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**RREWVNbb（wave s2_si3_gate_d1）**

```text
hump(-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 22), densify(industry)), hump=0.01)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**LLMJ9nN6（wave s2_si3_gate_d1）**

```text
-group_zscore(ts_rank(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 22), 252), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**wpQgZKN2（wave s2_si3_w15_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 12), densify(industry))
```

已存检查失败：LOW_SHARPE。

**78L9N7G5（wave s2_si3_w15_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 18), densify(industry))
```

已存检查失败：LOW_SHARPE。

**KPJaNlVk（wave s2_si3_w15_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 10), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS。

**QPvXbZOr（wave s2_si3_w15_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 15), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**E56JpON1（wave s2_si3_w15_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 15), densify(sector))
```

已存检查失败：LOW_SHARPE, LOW_2Y_SHARPE。

**O0AaNQRp（wave s2_si3_w15_d1）**

```text
-group_zscore(ts_covariance(vec_avg(mean_loan_rate_p5_d1), vec_avg(mean_loan_rate_p5_d1), 15), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**VkxJa1Z0（wave s2_si3_w15_d1）**

```text
-group_zscore(ts_covariance(vec_avg(max_loan_rate_main), vec_avg(max_loan_rate_main), 15), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**JjeKNqEW（wave s2_si3_w15_d1）**

```text
trade_when(rank(ts_zscore(vec_avg(shrt3_bar), 252)) > 0.5, -group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 15), densify(industry)), -1)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**88R1jb9l（wave s2_si3_w15_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 15), densify(subindustry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**xArg3OVg（wave s2_si3_w15_d1）**

```text
hump(-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 15), densify(industry)), hump=0.02)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**6XdOjAgO（wave s2_si3_nan_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 12), densify(industry))
```

已存检查失败：LOW_SHARPE。

**JjeKNPRm（wave s2_si3_nan_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 18), densify(industry))
```

已存检查失败：LOW_SHARPE。

**GrWJbgEG（wave s2_si3_nan_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 15), densify(industry))
```

已存检查失败：LOW_SHARPE。

**A1VKNQqe（wave s2_si3_nan_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 15), densify(sector))
```

已存检查失败：LOW_SHARPE, LOW_2Y_SHARPE。

**9qx0WR0V（wave s2_si3_stat2_d1）**

```text
-group_zscore(ts_mean(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 5), 15), densify(industry))
```

已存检查失败：LOW_SHARPE。

**6XdOKEOJ（wave s2_si3_stat2_d1）**

```text
-group_zscore(ts_std_dev(vec_avg(min_loan_rate_main), 15), densify(industry))
```

已存检查失败：LOW_SHARPE。

**leAXK0b5（wave s2_si3_stat2_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(mean_loan_rate_main), 12), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**VkxJ08g8（wave s2_si3_stat2_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(mean_loan_rate_main), 15), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**O0Aa89aq（wave s2_si3_stat2_d1）**

```text
-group_zscore(ts_delta(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 15), 22), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**pwdO57gX（wave s2_si3_stat2_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(max_loan_rate_main), 15), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**78L96d98（wave s2_si3_stat2_d1）**

```text
-group_zscore(ts_corr(vec_avg(min_loan_rate_main), vec_avg(mean_loan_rate_main), 15), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**QPvXYZ6G（wave s2_si3_decay2_d1）**

```text
-group_zscore(ts_mean(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 5), 15), densify(industry))
```

已存检查失败：LOW_SHARPE。

**npvVAxXx（wave s2_si3_decay2_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 18), densify(industry))
```

已存检查失败：LOW_SHARPE。

**e75R6kEE（wave s2_si3_decay2_d1）**

```text
-group_zscore(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 12), densify(industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS。

### 读取限制

- A10m8LjW 字段解析失败：ParseError；需人工核对原式
- 78ZMRGW8 字段解析失败：ParseError；需人工核对原式
- gJQdVr6M 字段解析失败：ParseError；需人工核对原式
- mLg1WK3p 字段解析失败：ParseError；需人工核对原式
- O0rVX6Y7 字段解析失败：ParseError；需人工核对原式
- 6XrJLG8J 字段解析失败：ParseError；需人工核对原式
- Grdx5QAJ 字段解析失败：ParseError；需人工核对原式
<!-- END WQB DATASET EVIDENCE -->

## 人工机制复盘

> 本节为人工撰写（2026-10-29），机器段只给统计，不给因果。口径：DEU / TOP500 / D1 / FASTEXPR，
> 平台闸 `LOW_SHARPE` 与 `LOW_2Y_SHARPE` 均为 **1.58**，`LOW_FITNESS` 1.0。

### 1. 这个数据集卖的是什么

`shortinterest3` 是**证券借贷市场（securities lending / stock loan）的日频快照**，不是空头持仓量。
它的主字段是**借券费率**（`mean_loan_rate_*` / `min_loan_rate_*` / `max_loan_rate_*`，VECTOR 向量），
以及 `shrt3_bar` 这类衍生量。费率不是价格，而是**稀缺性报价**：谁难借，谁的费率就贵。

因此它有**三条互不相同**的可交易信息，本战役各自都做穿了：

| 信息 | 经济含义 | 载体 | 本区单信号上限 |
|---|---|---|---|
| **横截面水平** | 卖空约束强度：高费率 = 难借 + 已被看空 | `-rank(ts_backfill(vec_avg(mean_loan_rate_main),252))` | S 0.82 / **2Y 1.65** |
| **时序方差** | 卖空供给的不确定性（short-selling risk） | `-group_zscore(ts_mean(ts_covariance(vec_avg(min_loan_rate_main),…,5),15), densify(industry))` | **S 1.36** / 2Y 2.05 |
| **横截面离散度** | 同一只票不同借款人之间的报价分歧 = 供给摩擦 | `-group_zscore(ts_mean(vec_range(min_loan_rate_main),15), densify(industry))` | S 1.30 / 2Y 1.74，但**质量最优**（TO 0.055 / margin 34.8bp / CLUSTER_TEST 干净） |

方差腿的理论依据是 Engelberg–Reed–Ringgenberg (2018, JF)：**借券费率的波动本身就是被定价的风险**，
高不确定性的股票未来收益更低 ⇒ 做空高方差。水平腿的依据是 D'Avolio (2002, JFE) 的供给曲线：
费率是借券市场的清算价格。离散度腿量的是「借款人之间谈不拢」——**供给摩擦/谈判力分散**，
与方差腿同向但不是同一个矩（一个是跨日召回风险，一个是同日横截面分歧）。
三者方向一致、载体不同，**但同族高相关，不可同时提交、也不可相加**。

### 2. 三条形态边界（都是实测，不是推断）

1. **水平式不能被自身历史归一**。`ts_rank(·,250)` / `ts_zscore(·,250)` 把 2Y 从 1.65 打到 0.24–0.30，
   且换手反升。水平式的信息在**横截面的绝对分层**里，归一化把它变成择时。
2. **方差式必须带分组轴，且轴只能是 `industry`**。DEU 是单一交易所（XETRA），`exchange` 轴退化
   （等价于全局 zscore），尾部权重吃满 truncation，CW 0.47 / DD 58%。换 `industry` 后同式 CW 过、
   DD 20.6%。同轴在**分析师修正族里正好有害**（双重去行业）⇒ 轴不是区域常量，是信号属性。
3. **方差式的向量聚合只能是 `vec_avg`**。`vec_sum` −0.11（把借款人数量当强度）、`vec_max` −0.43
   （取单个最极端借款人 = 单点噪声）、`vec_min` 同源更差；口径 `min > mean > max`（min 是真正的
   稀缺端报价，max 是一次性异常报价）。

### 3. 设置定式（本数据集专用，逐条实测）

| 设置 | 取值 | 证据 |
|---|---|---|
| `neutralization` | **NONE**（唯一正向杠杆） | 同式 SUBINDUSTRY→NONE：S +0.04~+0.07、margin +1.5~+3.3bp、TO −0.016~−0.019 |
| 同上 | STATISTICAL 是强度杀手 | 8 条配对全负，ΔS 均值 **−0.30** |
| `decay` | 4 为主，2 只加 +0.02 | 同式 1.26→1.28，2Y 持平、margin −1bp |
| `nanHandling` | ON 是 no-op（逐位相同） | 4 条重跑 S/F/2Y/TO/margin 全一致 |
| `universe` | TOP500 是本区唯一档 | DEU 无更宽档，宽度杠杆不可用 |

**为什么 NONE 反而最好**：表达式里 `group_zscore(·, densify(industry))` 已经做过一次行业去均值，
SUBINDUSTRY 中性化是**在更细粒度上再去做一次均值**，把「行业内部谁更贵/谁更抖」这层信息一起抹掉。
铁律：**中性化粒度必须与分组轴错开——要么不做，要么更粗；同粒度即 no-op，更细即负迁移。**

### 4. 天花板在哪

- 嵌套骨架（`ts_mean(ts_covariance(·,5),15)`）比单层强 +0.05；外窗 W12–W18 平台，**W22 起下跌 −0.19**。
- 等价算子全扫无一破 1.58：`ts_decay_linear` +0.03 但引入 `CONCENTRATED_WEIGHT`；
  `ts_mean(·,10)` 给出最高 2Y（1.98）但 S 只 1.28；`group_rank` / `rank()` 后置 / `group_neutralize`
  全部退化（0.91 / 1.10 / 0.74）。
- 最好的读数：`ts_decay_linear(·,15)` + NONE 得 **S 1.36 / F 1.23 / 2Y 2.00 / TO 0.089 / margin 23.1bp**，
  但它**同时挂 `CONCENTRATED_WEIGHT`**；不带 CW 的最优是嵌套 5/15 + NONE：
  **S 1.31 / F 1.17 / 2Y 1.86 / TO 0.076 / margin 26.1bp，强度类唯一 FAIL 是 `LOW_SHARPE`（差 17%），
  另带非 PASS 的 `CLUSTER_TEST` 0.94（限 1）**。
  两者都属于「该概念在 DEU 的 IS 上限」，不是几何、窗口、覆盖或算子问题
  （与仓库铁律 `multileg_strength_not_decomposable_v1` 一致：DEU 历史上 best_S>1.58 的波次全是多腿）。
- **换一个矩（横截面离散度）能换到质量，但换不到强度**：`vec_range` 腿 S 1.30 / 2Y 1.74，
  但 TO 0.055（协方差版 0.082 的 −33%）、margin 34.8bp（+33%），且是**本族唯一 `CLUSTER_TEST`
  无告警、无 CW 的形态**。⇒ 若要留一条「干净」的借券费 alpha，取离散度版；
  若要冲 S 线，协方差版更高 0.06 但必须接受 CW/CLUSTER 告警。

### 5. 要过闸只有一条合规路

用户约束禁止任何形式的两两混腿与加权。合规形态只有**单主信号 + 风险门**：
本战役已验证 `trade_when(借券费 rank<0.7, 分析师修正 rank, -1)` 把 S 0.82→1.57、TO −83%、
margin ×8.8、DD 10.1%，无权重混合。**但门控腿必须是分析师修正族，不能是借券族内部另一条腿**
（同族高相关、且属"同 category 两两组合"禁区）。

### 6. 使用本数据集时不要做的事

- 不要用 `ts_rank` / `ts_zscore` / `ts_rank` 后置做归一（毁 2Y）。
- 不要用 `hump` 平滑（0.01 → 0.87、0.02 → 0.44）。
- 不要用水平式当门控去控方差腿（`trade_when` 门控后 0.89）。
- 不要给这条族补 `ts_backfill` / 开 `nanHandling`（都是 no-op，白烧配额）。
- 不要用 `ts_corr` 替代 `ts_covariance`（尺度自由会毁掉全部信息，S 塌到 0.26）。
- 不要把离散度做成相对量：`ts_std_dev(log(vec_avg(·)),15)` −0.10、嵌套版 −0.06，
  两条都死 —— 费率信号的信息在**绝对水平差**里，除以均值会把大小票/松紧期拉平。
- 不要用 `vec_count` 当压力指标（S 0.21）：报价家数多 ≠ 紧张，只有「家数少且价差大」才是挤压。
- 6 个字段存在 ParseError（见机器段「读取限制」），用之前先核对原文。
