# 口径更正 + 锚点逐年归因（2026-11-07）

## A. checks.fail 为空 ≠ 通过（重要读表更正）
leA58QNO 收割时 checks.fail 为 []，一度误判为「全绿」。直查平台后真实结构是：
- checks.fail = **[]**（空）
- checks.warning = **LOW_SHARPE 1.24/1.58 · LOW_FITNESS 0.93/1.0 · LOW_2Y_SHARPE 1.41/1.58** + MATCHES_COMPETITION / MATCHES_THEMES
- ra.failed_ra_count = **3** · ra.ra_failed = **true**

⇒ **判定必须读 ra.failed_ra_count / ra.ra_failed_checks，不能只读 checks.fail。**
LOW_SHARPE / LOW_FITNESS 被平台从 fail 降级成 warning，但资格门仍按 WARNING 计失败。

## B. ATOM 口径的官方边界（已查 GLOSSARY，勿再猜）
- ATOM = **只用单一数据集字段**（分组字段除外）+ 无 inst_pnl() / convert()。
- ATOM **只豁免 IS Ladder Sharpe Test**（改用 Last-2Y Avg IS Sharpe 判；TO<30% 时该 PASS 阈值 ×0.85）。
- **LOW_SHARPE（全期）与 LOW_FITNESS 不豁免**，仍在 RA 名单 ⇒ **ATOM 候选仍须全期 S≥1.58 且 F≥1.0**。
- ⇒ **达标线不变：S ≥1.58 · F ≥1.0 · 2Y ≥1.58。**「ATOM 只要 2Y 过」是错的。

## C. leA58QNO 逐年 S（归因，铁律 F）
| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | **0.28** | 1.32 | **2.22** | **−0.36** | 0.93 | 1.71 | 1.51 | 1.68 | ~1.8 | ~0.9 |
| pnl(万) | +14 | +94 | +110 | **−16** | +49 | +87 | +100 | +110 | +110 | — |

- **10 年 9 正，唯一硬负年是 2017（−0.36）**；次弱是 2014（0.28）。
- 年 S 均值 ≈1.20，与全样本 S 1.24 吻合。
- 要 S 1.24→1.58 需年 S 总和 +约 3.8；只修 2017 不够（最多 +1.9），**必须 2014 与 2017 同时修**。
- 经济解释：2017 是 KOR 强 risk-on 大涨年（KOSPI +22%），
  **「风险规避型」因子在 risk-on 年结构失效** ⇒ 这是机制暴露问题，不是参数问题。
- ⇒ 修法优先级：**中性化轴**（剥离风险偏好暴露）> 窗口 > 换字段。

## D. 选集重估：risk59 是真正的白空间
| 集 | 字段数 | 覆盖 | 最高 aC | 拥挤判断 |
|---|---:|---:|---:|---|
| risk70 MFM2 | 96 | 0.980 | **8018** | 极挤（本战役主力，已反复挖） |
| risk88 | 64 | 0.973 | 1418 | 中挤 |
| risk68 | 5 | 1.000 | 525 | 中 |
| **risk59** | **16** | **0.981** | **122** | **最白（低一个量级）** |

⇒ **risk59（Securities Lending）是本区最未被开采的 risk 集**：aC 最高仅 122，机制有 D'Avolio 2002 学术支撑（M2 融券约束溢价 / M3 空头挤压），
而至今只试过 3 个形态（bid_rate×DTC 交叉、shortinterestpct、squeeze 做空高）。
