# 稳健性审计报告 — 2026-10-29（GBR / TOP700 / D1）

> 执行依据：`Claude/skills/brain-alpha-robustness/SKILL.md`（Phase C 阈值表）
> 数据源：`mcp__wq-brain-http__get_alpha_yearly_stats` 逐年 `sharpe` / `longCount` / `pnl`
> 判定脚本：`logs/_tmp_phasec.py`
> 台账写入：`mcp__wqb-db__upsert_ledger_key(region="GBR", key="robustness_<alpha_id>")`

## 阈值口径（原文照录，勿改）

| 检查项 | PASS | CONDITIONAL | REJECT |
|---|---|---|---|
| WebDataScope failed count | Failed=0 且无 PENDING | 名单内有 PENDING | Failed>0（硬 REJECT） |
| Recent-3yr Sharpe（主判定） | ≥1.58 且近 3 年每年 >0.3 | 某近年在 0–0.3 | 某近年 <0 **或** 3 年合计 < 线 |
| Recent-3yr CV_Sharpe | <0.40 | 0.40–0.60 | ≥0.60 |
| 衰减比（last_year / full） | ≥0.50 | 0.30–0.50 | <0.30 |
| 平年（仅最近 3 年，abs(s)<0.3） | 0 | 1 | ≥2 |
| Recent-3yr max/min Sharpe 比 | ≤3 | 3–5 | **>5** |
| 全历史早年疲软（CV / 厂字形 / max-min） | — | 记软标记 | **绝不** REJECT |
| Sub-universe | 平台 PASS | WARNING / 贴线 | FAIL |
| Margin @ turnover | ≥5bp | 3–5bp @ TVR≥40% | <3bp @ TVR>60% |
| Top-5 个股集中度 | <30% | 30–50% | ≥50% |

★ 本次纠正一处历史误记：`Recent-3yr max/min` 的 PASS 线是 **≤3**，REJECT 线是 **>5**；此前曾把 3 当否决线。
★ 全历史早年疲软**只作软标记**，单独不构成 REJECT。

---

## 逐条判定

### 1. `rKRkL9QE` — **PASS**

| 项 | 值 |
|---|---|
| 全期 Sharpe | 2.21 |
| 近 3 年（2021 / 2022 / 2023） | 1.66 / 2.30 / 2.88 |
| 近 3 年均值 | 2.2800 |
| CV3 | 0.2185 |
| 衰减比（2023 / 全期） | 1.303 |
| 平年数 | 0 |
| max/min 比 | 1.735 |
| 结论 | **PASS**（主判定、CV、衰减比、平年、max-min 全过） |

软标记：
- 2019 全历史 Sharpe 0.71（早年疲软，按规则仅记录）
- `IS_LADDER_SHARPE` 余量 24%
- riskNeut 后仍存 87%（信号韧性好）

### 2. `0mYoANkv` — **PASS**

| 项 | 值 |
|---|---|
| 全期 Sharpe | 1.89 |
| 近 3 年 | 2.07 / 2.02 / 2.27 |
| 近 3 年均值 | 2.1200 |
| CV3 | 0.0509（五条里最稳） |
| 衰减比 | 1.201 |
| 平年数 | 0 |
| max/min 比 | 1.124 |
| 结论 | **PASS** |

软标记（**这条风险最实**）：
- **riskNeut 后仅存 54%**（riskNeut Sharpe 1.02 / Fitness 0.51）⇒ 一半以上的收益来自风险暴露
- `IS_LADDER_SHARPE` 余量仅 3%
- 与 `9qxoa3mx` 相关 0.7227、与 `88RAnmAX` 相关 0.772 ⇒ **三条不可共存**（本次实测修正：此前误记为 0.4321）

### 3. `kqNRXm5k` — **REJECT**（不可提交）

| 项 | 值 |
|---|---|
| 全期 Sharpe | 1.70 |
| 近 3 年 | **0.32** / 2.09 / 1.92 |
| 近 3 年均值 | **1.4433**（< 线 1.58） |
| CV3 | **0.5524**（CONDITIONAL 区） |
| 衰减比 | 1.129 |
| 平年数 | 0 |
| max/min 比 | **6.531**（> 5） |
| 结论 | **REJECT** |

双重失败：`recent3_strength`（均值 1.4433 < 1.58）+ `max_min`（6.531 > 5）。
根因：2019–2021 连续三年弱（0.51 / 0.91 / 0.32），信号只在最近两年（2022 / 2023）有效 ⇒ 非稳定 alpha。
**后果**：`submit_verdict` 读取本条台账后会对该 alpha 返回 `BLOCKED / ROBUSTNESS_REJECT`。

### 4. `9qxoa3mx` — **PASS**

| 项 | 值 |
|---|---|
| 全期 Sharpe | 1.59 |
| 近 3 年 | 1.73 / 1.31 / 2.08 |
| 近 3 年均值 | 1.7067 |
| CV3 | 0.1844 |
| 衰减比 | 1.308 |
| 平年数 | 0 |
| max/min 比 | 1.588 |
| 结论 | **PASS** |

软标记：
- 2015 年 0.55、2017 年 0.32（早年疲软）
- **`LOW_SHARPE` 全期 1.59 vs 线 1.58，余量 0.6%** ⇒ 任何参数重跑抖动都可能翻闸
- 与 `88RAnmAX` 相关 0.9584（近重复）

### 5. `88RAnmAX` — **PASS**

| 项 | 值 |
|---|---|
| 全期 Sharpe | 1.67 |
| 近 3 年 | 1.73 / 1.39 / 2.28 |
| 近 3 年均值 | 1.8000 |
| CV3 | 0.2037 |
| 衰减比 | 1.365 |
| 平年数 | 0 |
| max/min 比 | 1.640 |
| 结论 | **PASS** |

软标记：
- 2017 年全历史 0.10（早年疲软）
- 与 `9qxoa3mx` 相关 0.9584 ⇒ 两条等价，不应同时提交

---

## 汇总

| alpha | 近3年均值 | CV3 | 衰减比 | max/min | 判定 | 主要软标记 |
|---|---|---|---|---|---|---|
| `rKRkL9QE` | 2.2800 | 0.2185 | 1.303 | 1.735 | **PASS** | ladder 余量 24% |
| `0mYoANkv` | 2.1200 | 0.0509 | 1.201 | 1.124 | **PASS** | riskNeut 仅存 54%、ladder 余量 3% |
| `kqNRXm5k` | **1.4433** | 0.5524 | 1.129 | **6.531** | **REJECT** | 2019–2021 连续三年弱 |
| `9qxoa3mx` | 1.7067 | 0.1844 | 1.308 | 1.588 | **PASS** | LOW_SHARPE 余量 0.6%、×88R 0.9584 |
| `88RAnmAX` | 1.8000 | 0.2037 | 1.365 | 1.640 | **PASS** | 2017 年 0.10、×9qx 0.9584 |

**可用腿（PASS）**：`rKRkL9QE` / `0mYoANkv` / `9qxoa3mx` / `88RAnmAX`
**不可用**：`kqNRXm5k`（REJECT）

**互相关约束（4 年日收益，`compute_mutual_correlation` 实读）**：
- `0mYoANkv × 9qxoa3mx` = **0.7227** ⇒ 超 0.7
- `0mYoANkv × 88RAnmAX` = **0.772** ⇒ 超 0.7
- `9qxoa3mx × 88RAnmAX` = **0.9584** ⇒ 近重复
⇒ 四个 PASS 里只能组成 `{rKRkL9QE, 0mYoANkv}` 这一对（相关 0.5139）。

**结合平台存量 `6XA8AGjL`（PV 塔唯一一颗，prod 0.547）**：
`6XA8AGjL × rKRkL9QE = −0.0228`、`6XA8AGjL × 0mYoANkv = −0.0313` ⇒ 三条两两 −0.023 / −0.031 / 0.514 全部 < 0.7，`max_mutually_below_subset_size = 3` 且 `max_subset_exact = true`。
⇒ **提交 `rKRkL9QE` + `0mYoANkv` 即可把 GBR/D1 PV 塔从 1 颗点到 3 颗**（详见 `ledger_key: pv_tower_clear_path_20261029`）。

---

## 待补项

- `0mYoANkv` riskNeut 保留率 54% 是全批最薄的一环，且生产相关性对 IS 候选**不可测量**（端点全局返空）⇒ 提交时存在撞 0.70 墙的现实风险，撞墙由平台直接拒绝、不消耗配额。
- `9qxoa3mx` 的 `LOW_SHARPE` 余量 0.6%，不建议作为点塔腿（任何设置微调都可能翻闸）。
