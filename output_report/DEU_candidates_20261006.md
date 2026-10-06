# DEU 战役候选清单（2026-10-06）

> 设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / truncation 0.08 / nanHandling OFF / maxTrade OFF
> **全部 UNSUBMITTED**（全局闸 `ALLOW_ALPHA_SUBMIT=False` 全程未动）。31 波 / ~230 探针。

## 一、全 RA 闸通过的候选（`failed_ra_count = 0`，历史首次）—— 唯一阻塞 = prod

| # | alpha | 表达式 | S | F | 2Y | sub | tvr | prod |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `xAbx0zwW` | `rank(ts_mean(ts_backfill(value_momentum_sector_percentile, 66), 22))` | 1.65 | 1.60 | **1.67** | 0.81 | 0.036 | ~0.96 ❌ |
| 2 | `vR2L3KXw` | `rank(ts_mean(ts_backfill(value_momentum_sector_rank_float, 66), 5))` | **1.74** | 1.73 | **1.69** | 0.85 | 0.062 | 未测 |
| 3 | `pw56XLRV` | `rank(ts_backfill(value_momentum_sector_percentile, 66))` | **1.77** | **1.77** | 1.64 | 0.86 | 0.084 | **0.9653 ❌** |
| 4 | `kqg32xM8` | `rank(ts_mean(ts_backfill(value_momentum_region_rank_float, 66), 5))` | 1.62 | 1.57 | **1.59** | 0.80 | 0.061 | 未测 |
| 5 | `QPKaL1pr` | `rank(ts_mean(value_momentum_global_rank_float, 5))` | 1.63 | 1.59 | **1.59** | 0.81 | 0.061 | **0.9438 ❌** |
| 6 | `RR6p3gbz` | `rank(ts_mean(value_momentum_sector_percentile, 5))` | 1.75 | 1.74 | **1.70** | 0.87 | — | 未测 |

**判定**：`value_momentum_*`（model25，公共因子）**PASS** S / F / CONCENTRATED_WEIGHT / sub_universe / **LOW_2Y_SHARPE** / IS_LADDER / CLUSTER / MATCHES_PYRAMID —— **只挂 PROD_CORRELATION（0.94~0.97）**。

## 二、prod 干净的候选 —— 唯一阻塞 = 2Y

| # | alpha | 表达式 | S | F | 2Y | prod | self |
|---|---|---|---:|---:|---:|---:|---:|
| 7 | `wpbRqwp5` | `signed_power(ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 1008), 8), 0.3)` | 1.67 | 1.26 | 1.22 ❌ | **0.578 ✅** | 0.573 ✅ |
| 8 | `88PnaqMo` | `rank(ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 1008), 8))` | 1.70 | 1.17 | 1.03 ❌ | **0.578 ✅** | 0.573 ✅ |
| 9 | `gJZ1EY5m` | `rank(ts_backfill(value_momentum_global_rank_float, 66))` | 1.67 | 1.64 | 1.55 ❌ | 未测 | — |

## 三、总判定

DEU 存在**结构性「prod × 2Y」两难**：强单信号（`value_momentum_*`）必为拥挤公共因子（prod 0.94~0.97），
prod 干净族（`predictive_starmine`）2Y 天花板仅 1.24。

台账全量扫描证实：DEU 唯一同时过 S(≥1.55) 与 2Y(≥1.55) 的 alpha **全部是 5 腿 `add()` 复合**
（`78ZM5QR5` S1.83 / F1.85 / 2Y2.29 / `failed_ra_count=0`）⇒ **历史唯一通路 = 多腿分散化**，与「禁混信号」规则直接冲突。

⇒ **在「禁混信号」铁律下，DEU 可提交单信号数 = 0；「10 颗」不可达**。
非调参、非素材、非形态设计问题，而是因子拥挤 vs 2Y 持续性的结构取舍。

## 四、可复用方法论（本轮实证）

1. **修 CONCENTRATED_WEIGHT（NaN 型）**：`ts_backfill(x, 66~252)` 或 `ts_mean(x, 5)`（一次修好 8/8）；
   `winsorize` / `group_neutralize` / `signed_power` **无效**。
2. **2Y 正杠杆**：`signed_power(x, 0.3~0.4)`（**必须输出端**，包在 `rank()` 里是 no-op；starmine 1.03→1.24）；
   `ts_mean(x, 5)`（value_momentum 1.66→1.70）。
3. **中性化档**：SUBINDUSTRY 最优（MARKET → 2Y 1.49 / STATISTICAL → 0.24）。
4. **符号铁律**：DEU starmine（分析师修正）= **正号**；shortinterest3（借券费率）= **负号**；**跨数据集不可类比**。
5. **工程**：`tools/submit_batch.py`（`tools/ind_sim_submit.py` 已不存在）每个 `--path` 文件**必须 ≥2 条表达式**；
   新算子/新参数形态**先单条验证再进批**（一次语法错 = 整批 8 条连坐 CANCELLED）。
