# B 路线选集报告（缺口 2 条 · GBR 全库产出率扫描）

日期：2026-11-02。数据源：`wqb-db get_mining_yield(region=GBR, by_dataset=true, strict=true)`，全量落盘 `logs/_gbr_yield_by_dataset.json`（153 个选集 / 6092 回测行）。

## 0. 背景

A 路线（NEWS 塔第三条）已终局判死：news17 三波 36 条 + news18 一波 12 条 = 48 条全 REJECT（IS 天花板 0.91），现货五轴判死。缺口 2 条只能走 B（其它塔凑 10，NEWS 停 2/3）。

## 1. 全库口径（strict）

| 口径 | 值 |
|---|---|
| 表达式总数 | 10570 |
| 回测行 | 6092 |
| ra_clean（S/F 达标且 RA 全过） | 627（10.3%） |
| prod_clean（已测 prod 且 <0.7） | 50 |
| prod_blocked（撞 prod 墙） | 137（已测样本中 73% 撞墙！） |
| ra_unknown（ra_failed_checks 未读） | 4374 |

⚠ prod 墙占比高：已测 prod 的 187 条里 137 撞墙 —— **新候选必须把「降 prod」当一等设计目标**，不是事后补救。

## 2. B 路线候选选集（按 ra_clean 产出率 × 样本量排序）

### Tier 1（推荐主攻）

| 选集 | 回测行 | ra_clean | 产出率 | prod_clean | 塔位 | 备注 |
|---|---|---|---|---|---|---|
| **fundamental72** | 205 | 74 | **36.1%** | 4 | FUNDAMENTAL（非 trio） | 大样本高产、**prod 墙 0 撞**；单集 ATOM 不占两塔配额 |
| **predictive_starmine** | 161 | 23 | 14.3% | **8（全库最多）** | MODEL（trio） | prod_clean 产出最多，说明这个集天然出低相关 |
| **analyst7** | 455 | 99 | 21.8% | 5 | ANALYST（非 trio） | 全库最大样本，proven |

### Tier 2（补充）

| 选集 | 回测行 | ra_clean | 产出率 | prod_clean | 塔位 |
|---|---|---|---|---|---|
| model28 | 112 | 17 | 15.2% | 4 | MODEL |
| model38_star_val | 5 | 5 | 100%（n 太小） | 1 | MODEL |
| analyst_earnings_ibes | 19 | 4 | 21.0% | 1 | ANALYST |
| model53 | 58 | 8 | 13.8% | 1 | MODEL |

### Tier 3（两集组合，受塔混配额约束）

| 组合 | 回测行 | ra_clean | 产出率 | 配额约束 |
|---|---|---|---|---|
| analyst47+pv47 | 15 | 10 | 66.7% | ANALYST×PV = trio×非trio，计入 ≤5 名额 |
| quant_factor_lib+risk60 | 23 | 13 | 56.5% | 需先查 category，若 MODEL×OTHER 则**禁混** |
| pv1+pv47 | 66 | 36 | 54.5% | **PV+PV 禁混，直接排除** |
| fundamental72+pv1 | 117 | 33 | 28.2% | FUND×PV 计入 ≤5 名额 |

### 判死/低产选集（不再投入）

news 系全灭（news17/18/20/50/104 产出率 0，与 A 路线判死一致）；institutions6 / fund_holdings_panel / shortinterest3 / pattern_scores / sentiment27 / earnings6 / order_book_imbalance 等产出率 0。

## 3. 建议

1. **首选 fundamental72 单集 ATOM**：205 行大样本、36.1% 产出率、prod 墙零撞 —— 数学上最可能一次出 2 条，且单集 ATOM 不占两塔配额、FUNDAMENTAL 是非 trio 塔（与篮内 PV+FUND 组合不同轴）。
2. **次选 predictive_starmine**：prod_clean=8 全库第一，专治 prod 墙；但属 MODEL 塔，篮内已有 2 条 MODEL，点塔均匀性略亏。
3. 每个新集开波前照纪律：模板池 ≥10 互异模板 + 论坛模板检索（web_search 402 仍暂停）。

## 4. 待用户裁定

- B（其它塔凑 10，NEWS 停 2/3）vs C（先提交 8 条再定）vs 放弃凑 10。
- `O0AKLMKq` vs `leAJn9e2` 二选一（0.8493 互斥）。
- 提交授权（8 条备齐；prod 漂移剧烈，建议尽快定）。
