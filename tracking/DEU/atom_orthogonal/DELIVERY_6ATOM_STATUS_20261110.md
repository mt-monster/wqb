# DEU 交付清单（2026-11-10 20:3x 更新）—— 2 ACTIVE + 3 待授权 + 1 新候选

> 原 5 颗版见 `DELIVERY_FINAL_5ATOM_20261110.md`（历史记录）；本文件为最新状态。

| # | alpha | 数据集 | 塔 | S | F | 2Y | TO | self | 状态 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | zq3eb7No | analyst7 | ANALYST | 2.01 | 1.28 | 1.64 | 0.226 | 0.364 | ✅ ACTIVE |
| 2 | bl6AvMkN | analyst_factor_signals + predictive_starmine | ANALYST | 1.61 | 1.36 | 2.15 | 0.110 | 0.514 | ✅ ACTIVE |
| 3 | RREPm361 | analyst7 | ANALYST | **2.02** | 1.25 | 1.82 | 0.250 | 0.328 | 🟡 待授权 |
| 4 | 1YNMAA8M | analyst7 + analyst15 | ANALYST | 1.58 | 1.36 | 2.13 | 0.134 | 0.695 | 🟡 待授权 |
| 5 | E569ZE7L | shortinterest3 | SHORTINTEREST | 1.68 | 1.21 | 2.27 | 0.113 | 0.544 | 🟡 待授权 |
| **6** | **1YWqzPGQ** | **shrt3_bar + oth47_traffic** | **SHORT × OTHER** | **1.59** | **1.10** | **2.81** | **0.156** | **0.588** | 🟢 prod 待出 |

## 第 6 颗表达式（11 算子）
```
group_rank(add(
  -group_rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 264), subindustry),
  group_rank(ts_quantile(ts_delta(ts_backfill(vec_avg(oth47_organic_traffic), 132), 66), 252), sector)
), sector)
```

## 逐年（1YWqzPGQ，十年零空窗）
2014 3.04 / 2015 1.64 / 2016 **-1.00** / 2017 0.44 / 2018 1.19 / 2019 1.91 / 2020 0.86 / 2021 1.50 / 2022 2.50 / **2023 3.42**

## 待用户裁定
1. 是否授权提交 3 颗全清件（RREPm361 / 1YNMAA8M / E569ZE7L）
2. 是否接受 1YWqzPGQ 点亮 OTHER 塔
3. 目标口径（10 颗 vs 域内现实）