# SA_BASE —— SA 提交 × Base 到账 追踪台账

> 方法论：`docs/experience/09_sa_base_tracking.md`（记账）+ `docs/experience/10_base_multiplier_and_theme.md`（算账）
> 建表：2026-11-20 ｜ 所有值来自 MCP 直读，禁止手填估算

## 文件

| 文件 | 粒度 | 写模式 |
|---|---|---|
| `sa_daily.jsonl` | 一天一行（当日最好一颗 SA） | **append-only** |
| `base_daily.jsonl` | 一天一行（base 到账额） | **按 date_et 覆盖（可回补）** |
| `account_daily.jsonl` | 一天一行（VF / OS / 在册数 / 结构面） | **append-only** |

### `sa_daily.jsonl` 必采字段（2026-11-20 扩充，前 6 个是乘数公式的输入）

| 字段 | 取法 | 为什么必采 |
|---|---|---|
| `date_et` / `n` / `ids` / `region` | `get_user_alphas(stage=OS,type=SUPER)` | 基础 |
| `S` / `F` / `pc` / `self` / `TO` | `metrics.sharpe/fitness/prodCorrelation/selfCorrelation/turnover` | **`pc` 决定档位（<0.30 = 553）** |
| **`pc_tier`** | 由 `pc` 派生：`<0.25` 台阶｜`0.25–0.30` 553｜`0.30–0.50` 中间｜`0.50–0.65` 双5｜`>0.65` 低档 | **量级开关** |
| **`theme_hit`** | `get_alpha_details(id).checks` 是否含 `MATCHES_THEMES` | **乘数来源之一** |
| **`theme_mult`** | 该 SA 命中的 Theme 倍率（GLB ARC / 3X / 2.5X / 2X / 1X） | 进公式 |
| **`pyramid_mult`** | `get_alpha_details(id).pyramids.list[].multiplier` | 进公式 |
| **`multiplier`** | `(theme_mult + pyramid_mult − 1) × (1 + os_rank)` | **该颗的理论乘数** |

## 每日五步（全 MCP，不要脚本）

1. `get_daily_and_quarterly_payment` → 取 `base_payments.records.records`
   **回读最近 14 天**，按 `date_et` 覆盖写 `base_daily.jsonl`（base 有到账延迟，必须回补）
2. `get_user_alphas(stage="OS", type="SUPER", limit=80, order="-dateSubmitted")`
   → 凡 `date_et` 不在 `sa_daily.jsonl` 的，追加上表全部字段
   （`theme_hit` / `theme_mult` / `pyramid_mult` 逐颗补 `get_alpha_details`）
3. `get_leaderboard(user_id="MT38799")`
   → `valueFactor` / `dailyOsmosisRank` / `meanProdCorrelation` / `superAlphaMeanProdCorrelation` / `superAlphaMeanSelfCorrelation` / `submissionsCount` / `dataFieldsUsed`
4. `value_factor_trendScore(start=今日−92d, end=今日)`
   → `diversity_score` / `S_A` / `S_P` / `S_H` / `P` / `P_max` / `N`
5. `get_user_alphas(stage="OS", status="ACTIVE", limit=1)` → 读 `server_count`
   ＋ 同参再带 `type="SUPER"` → SA 在册数；差值即 RA 在册数
   → 合并 3/4/5 的结果追加一行到 `account_daily.jsonl`

## 每期必算

**月度（L1）**
```
覆盖率 = 有付天数 / 自然天数
有付日均 = 合计 base / 有付天数
```

**环比分解（L2）**
```
Δbase = (n_curr − n_prev) × p_prev  +  n_curr × (p_curr − p_prev)
         └── 天数效应 ──┘              └──── 日均效应 ────┘
```

**统计功效**（`sd(日均) ≈ 0.180`）
| 位移 | 需要天数 |
|---|---|
| +$0.30 | 3 |
| +$0.20 | 6 |
| +$0.10 | 25 |
| +$0.05 | 102 |

⇒ **小于 $0.1 的差异写「不可分辨」，不许当结论。**

## 当前基线（2026-11-20）

| 项 | 值 |
|---|---|
| 8/9/10/11 月有付日均 | $1.600 / $1.729 / $1.689 / $1.645 |
| 11 月覆盖率 | 18/18 = 100%（到 11-18） |
| VF / OS Rank | 0.73 / **0.53** ⇒ 乘数 **1.53**（11-20 当日实测；午间曾读 0.27 为旧值） |
| 在册 ACTIVE | 447（RA 389 + SA 58） |
| Q4 base / 上季 / YTD | $29.61 / $85.32 / $161.80 |

## 正在跑的实验

**E1（2026-11-20 起）**：VF 0.43 → 0.73 的杠杆测试。
对照组 = 11-01~11-18 日均 $1.645（n=18）。
- 日均 ≥ **$1.85** 且持续 **6 天** ⇒ VF 有杠杆
- 日均仍在 **$1.55–1.75** ⇒ VF 在 0.4–0.7 区间对日均无杠杆

## 禁止

- 不要把「SA 的 S/F」当作 base 的预测变量写进结论——H2 已测 41 天 corr = −0.115，需累计 60 天复检。
- 不要用最近 1–2 天的 base 值算均值（未到账）。
- 本台账不改任何提交权限。
