# -*- coding: utf-8 -*-
"""gen_candidates_report.py — 生成 GBR 候选清单报告（战役专用，放区域 scripts/）。

输出：output_report/GBR_candidates_YYYYMMDD.md
读 data/wqb.db 的 alphas 表：已提交（date_submitted 非空）+ 储备候选（CANDS 列表）。
"""
from __future__ import annotations

import os
import sqlite3
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB = os.path.join(ROOT, "data", "wqb.db")
OUT = os.path.join(ROOT, "output_report", "GBR_candidates_20261005.md")

# 储备候选（全闸通过 + prod 为最近一次提交后实测）
CANDS = ["P0gv3AO7", "RR6NOlma", "JjQbYdGW", "omWVV6Y2"]

# 候选 → 信息维度 / self 最近邻（人工维护）
DIM = {
    "P0gv3AO7": ("**预期股息率变化**", "`model109`", "GrbQ9JWO 0.283（最低）"),
    "JjQbYdGW": ("**结构化信用：违约概率变化**", "`model28`", "3qVa2Lze 0.362"),
    "omWVV6Y2": ("**结构化信用：杠杆变化**", "`model28`", "KPNgQApj 0.501"),
    "RR6NOlma": ("**估值变化**（EP fy1）", "`predictive_starmine`", "9qWaRGEK 0.635"),
}

db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row
cur = db.cursor()

sub = [dict(r) for r in cur.execute(
    "SELECT alpha_id,sharpe,fitness,two_year_sharpe,prod_correlation,self_correlation,date_submitted"
    " FROM alphas WHERE region_id=7 AND date_submitted IS NOT NULL ORDER BY date_submitted")]

q = ",".join("?" * len(CANDS))
cand = [dict(r) for r in cur.execute(
    "SELECT alpha_id,sharpe,fitness,margin,turnover,drawdown,prod_correlation,self_correlation,"
    " expression FROM alphas WHERE alpha_id IN (%s)" % q, CANDS)]
cand.sort(key=lambda a: (a["prod_correlation"] or 1))  # prod 余量最大者在前

L = []
L.append("# GBR 战役候选清单（%s 生成）\n" % datetime.now().strftime("%Y-%m-%d %H:%M"))
L.append("## 平台已提交 ACTIVE/OS：**%d 颗 / 目标 20 颗**（还差 %d 颗；另有 %d 颗储备）\n"
         % (len(sub), 20 - len(sub), len(cand)))
L.append("| # | alpha_id | S | F | 2Y | prod | self | 提交日 |")
L.append("|---|---|---:|---:|---:|---:|---:|---|")
for i, a in enumerate(sub, 1):
    L.append("| %d | `%s` | %s | %s | %s | %s | %s | %s |" % (
        i, a["alpha_id"], a["sharpe"], a["fitness"], a["two_year_sharpe"] or "-",
        a["prod_correlation"] or "-", a["self_correlation"] or "-", str(a["date_submitted"])[:10]))

L.append("\n## ✅ 可信候选储备：**%d 颗**（全闸通过 + prod 最近一次提交后实测）\n" % len(cand))
for a in cand:
    L.append("### `%s`  —  prod %.4f / self %.4f" % (
        a["alpha_id"], a["prod_correlation"], a["self_correlation"]))
    L.append("")
    L.append("| S | F | margin | TO | DD |")
    L.append("|---:|---:|---:|---:|---:|")
    L.append("| %s | %s | %.2fbp | %.4f | %.4f |" % (
        a["sharpe"], a["fitness"], (a["margin"] or 0) * 1e4, a["turnover"] or 0,
        a["drawdown"] or 0))
    L.append("")
    L.append("```")
    L.append(a["expression"])
    L.append("```")
    L.append("")

L.append("## %d 颗候选**互不同源**（可同时提交，不会互相污染 prod）\n" % len(CANDS))
L.append("| alpha_id | 信息维度 | 数据集 | self 最近邻 |")
L.append("|---|---|---|---|")
for c in CANDS:
    d = DIM.get(c, ("", "", ""))
    L.append("| `%s` | %s | %s | %s |" % (c, d[0], d[1], d[2]))

L.append("""
## 重要纪律（2026-10-05 实测得出）

1. **提交会污染整个候选池的 prod**：提交 1 颗会把同族候选 prod 从 0.65 抬到 0.90+。
   实测：`wpZ3RP96` 记录 0.6865、`VkaZYdbG` 0.6849 → `3qVa2Lze` 提交后刷新 → **0.9036 / 0.9899**。
2. **DB 里的 prod 凡在最近一次提交之前测的，一律作废**；提交前必须
   `check_correlation(alpha_id, refresh=True)`。
3. **同族铁律**：同批候选 prod 差异 <0.01 ⇒ 判同族，只提 1 颗。
   ⚠ `mdl28` leverage 的多个窗（5/8/9/11/22）**属同族**，只能提 1 颗（选 `omWVV6Y2`）。
4. **优化判据是 prod 余量，不是 S 高低**：`RR6NOlma` 族 S 1.70→1.72 只涨 0.02，
   但 prod 0.6861→0.6975（余量 0.014→0.0025）⇒ 原版才最优。

## 本轮新增活族 / 字段

### `model28` 结构化信用（Merton 类）—— 已探尽
| 字段 | 正确方向 | S | F |
|---|---|---:|---:|
| `..._credit_..._pd_pct`（窗13, tvr0.13） | 正向 | **1.62** | **1.00** |
| `..._multiple_..._leverage`（窗8, tvr0.15, bf500） | 正向 | **1.62** | **1.02** |
| `..._credit_..._asset_drift_pct`（窗8） | **取反** | 1.57 | 0.99 |
| 所有 `*_rank` 变体 | 取反 | ≤1.27 | 弱 |
⚠ `*_rank_float` 与 `*_rank` **逐位相同**（重复字段）；`distance_to_default` 甜点在窗 22。

### `model109`（542 字段）—— 只挖出 1 个有效字段
| 字段 | S | F |
|---|---:|---:|
| **`expected_dividend_yield`** | **1.69** | **1.07** |
| `yield_with_share_buybacks` | 1.04 | 0.51 |
| `trailing_dividend_yield` | 0.88 | 0.41 |
| 其余（应计/MAX/技术指标/市值的 150+ 字段） | ≤0.6 或负 | 灭 |
★ **“预期”口径 ≫ “滚动”口径**（同维度 1.69 vs 0.88）⇒ 优先 `expected/projected/forward` 前缀。

## 🚫 ANALYST category 专攻结论（2026-10-05，32 条实测 ⇒ 0 产出）

**数据集盘点**：GBR 20 个 ANALYST 数据集中，**只有 `analyst7` 可用**（502 字段、cov 0.75、
412 个 cov≥0.5 的 MATRIX 字段）；其余全是 **VECTOR 或 cov=0.00**（`analyst44`/`analyst48`/`analyst9`
全 VECTOR；`analyst10`/`analyst15`/`analyst_consensus`/`analyst69`/`analyst83` 等 cov=0）。
⚠ `analyst_earnings_ibes` 的 category 其实是 **MODEL**。

**6 类机制全部无效**（`analyst7` 共 24 条 + `model109` 分析师修订 20 条 = 52 条）：

| 机制 | 条数 | 最好 S |
|---|---:|---:|
| 净修正广度 `raised − lowered`（8 对 aCnt 全 0、cov 1.00） | 8 | 0.28 |
| 估计离散度 `std` / `high − low` | 2 | 0.40 |
| 覆盖广度/变化 `num` | 2 | 0.06 |
| 共识修订 `mean − mean_{4wks,3mth}_ago` | 4 | 0.47 |
| 意外计数 `act_q_*_surprisenum`（aCnt 全 0） | 4 | 0.16 |
| 估计值比率（派息率/利润率/增长） | 4 | 0.63 |

**★★★ 结论（第三次验证）：GBR 窄截面下“分析师预期/修订”维度无法提取横截面信号。**
- 有效维度只有两类：① **原始财务量的时间变化**（`ts_delta` + 短窗：PD / 杠杆 / 违约概率）；
  ② **前瞻收益率**（`expected_dividend_yield`）。
- **可操作推论**：预期类字段里**只有能表达成“收益率”口径的才有信号**（如预期股息率）；
  **纯“计数 / 比率 / 修订”类一律无效**。
- 本段全部 52 条 **TO 极低（0.06–0.095）且 S<1.0** —— 低 TO 在此伴随低 S，与成功案例（TO 0.136）不同。

## 🔍 GBR 全 category 系统扫描（2026-10-05，用户要求逐 category 过数据集）

**方法**：每 category 统计 `cov>=0.5` 的 MATRIX 字段 → 统一配方派 8 条代表字段探测 → 记最好 S。
配方 = `group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(F,500),11)), lm0,lm1,tvr0.15), industry)`

| category | 数据集 | 可用MATRIX | 低拥挤 | **探测最好 S** | 判定 |
|---|---:|---:|---:|---:|---|
| **MODEL** | 13 | 1071 | 921 | **1.70** | ✅ **唯一有信号**：`model28`(结构化信用) / `model109`(预期股息率) / `predictive_starmine`(估值) |
| OTHER | 12 | 499 | 425 | **0.99** | ⚠ 弱：`other455` 供应链图嵌入 fact1；`dl_riskfree_returns` 1.08 |
| PV | 6 | 544 | 537 | 0.26 | ❌ 537 里几乎全是已测死的 `pattern_scores`；`pv29/pv30` 是 GROUP 轴 |
| ANALYST | 6 | 417 | 235 | 0.63 | ❌ 32 条实测全 <1.0 |
| FUNDAMENTAL | 3 | 106 | 9 | 0.14 | ❌ `fundamental6` 原始科目无效（S −0.20~0.14）|
| INSIDERS | 1 | 34 | 18 | 0.23 | ❌ 净买入无信号 |
| INSTITUTIONS / RISK | 5 | 12 | **0** | — | 无低拥挤字段 |
| SOCIALMEDIA/SHORTINTEREST/SENTIMENT/OPTION/NEWS/MACRO/EARNINGS | 13 | **0** | 0 | — | **无任何可用 MATRIX 字段** |

### 本轮新挖的两个未测大池（探测后均判弱/死）
**① `other455` = 供应链图嵌入库**（此前完全未挖）—— 4 家族 × 75 = 300 字段
（`competitor`/`customer`/`partner`/`relation` × `pca_fact{1,2,3}`）
- 探测最好 **S 0.99**（`competitor_..._fact1`），其余 −0.42~0.45 ⇒ **弱，不达闸**
- ⚠ 已提交的 `WjAV89jG` 用 `relation` 家族 ⇒ relation 族已被占用

**② `predictive_starmine` 未测家族**
| 家族 | 字段数 | 探测最好 S |
|---|---:|---:|
| `predicted_surprise`（预测盈利意外） | 39 | 0.77 |
| `eq_vr_dlra1_*`（质量复合分：应计/现金流分量） | 33 | −0.88（取反 +0.88）|
| `mean_estimate_change_pct_*`（自带共识变化率） | 82 | 0.33 |

### ★★ 沉淀判据（第五次验证，可直接省掉大量无效仿真）
> **拿到一个新字段，先问：它是「原始量」还是「派生分」？**
> - **派生分**（PCA / 概率 / 百分位 / 评分 / 聚类 / 复合分量）⇒ **直接跳过**，GBR 上无一例外无效。
> - **原始量**（财务科目 / 信用量 / 股息 / 价格）⇒ 用 `ts_delta` + 短窗（8–13）试。
> - 例外：能表达成**收益率口径**的前瞻量也有效（`expected_dividend_yield` S1.69）。

### 覆盖统计
本次共探测 **9 个 category / 约 100 条表达式**；GBR 全 15 个 category 中，
**8 个 category 连一个可用 MATRIX 字段都没有**，**6 个探测判死**，**仅 MODEL 一类产信号**。

## ⚙ 继续推进段（2026-10-05 21:10-21:35）：路径 1/2 双双失败 + 两个结构性发现

### ❌ 路径 1：`asset_drift` 换轴提 F —— **假设被证伪**
| 轴 | S | F |
|---|---:|---:|
| **industry（原版）** | **1.57** | **0.99** |
| sector / subindustry / market | 1.40–1.45 | 0.84–0.90 |
**换轴不提 F，反而降 S。**此前"sector 把 leverage 的 F 提到 1.02"是该字段的特例，**不可外推**。
**F 公式**：`F = S × sqrt(|returns| / max(TO, 0.125))` ⇒ **TO ≤ 0.125 时降 TO 提不动 F**，只能提 S 或 margin。

### ❌ 路径 2：model109 第二批 + 收益率定向搜索 —— 无新候选
| 字段 | 机制 | S |
|---|---|---:|
| `ep_yield_pct_smest_fy2_7` / `f12m_6` | 盈利收益率（高后缀） | 1.38 / 1.17 |
| `mdl53_implied_spreads` | 隐含信用利差 | 0.52 |
| `mdl53_ms5_*`（8 期限，另一套 PD 模型） | PD | 0.15–0.34 |
| `annualized_pd_5_year_jc7` / `7_year_jc7` | PD 其他期限 | 1.15 / 0.87 |
| `iv_steady_state_dividend_payout_rate_3` / 投影股息 / 技术指标 | — | ≤0.24 |

### ★★ 两个可复用的结构性发现
**① 后缀 = 数据质量档，且差距巨大**
- `ep_yield_pct_smest_fy2_**3**` → S **1.76**（已提交 npdm0mrq）
- `ep_yield_pct_smest_fy2_**7**` → S **1.38**
- **同一信号不同后缀差 0.38** ⇒ **选字段优先低后缀**（`_2`/`_3` 优于 `_6`/`_7`）。

**② PD 族的期限与模型**
- 期限：**2 年最优**（1.70，已提交）；5 年 1.15、7 年 0.87 ⇒ **期限越长越弱**。
- `mdl53_ms5_*` 是**另一套 PD 口径，明显更弱**（0.15–0.34）——别以为同族就同强度。

### 段末判定
**已知有效配方（原始量 + `ts_delta` 短窗 8–13）在 MODEL 类的可用字段上已基本穷尽。**
剩余未试字段以**派生分**为主，按已五次验证的规律**预期全部无效**。

## 🎯 中性化档突破（2026-10-05 21:29 起）—— 今天最大发现

> **自查**：今天前 60+ 条仿真**全部**用 `neutralization=STATISTICAL`，从未变过。
> GBR delay1 实际有 **11 个合法档**（`get_platform_setting_options` 查得）：
> `NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST`
> ⚠ **中性化是「批级」参数**，一个档一个批。

### 同一信号换档，S/F 大幅变化（4 颗储备 × 7 档实测）
| 候选（基准 STATISTICAL） | SLOW | CROWDING | MARKET | SUBINDUSTRY | FAST | SLOW_AND_FAST |
|---|---|---|---|---|---|---|
| `leverage`（1.62/1.02） | **1.94/1.37** | 1.58/1.20 | 1.47/1.17 | 1.53/1.22 | 1.08/0.46 | 1.20/0.51 |
| `pd_pct`（1.62/1.00） | 1.57/1.00 | 1.21/0.83 | 1.34/1.03 | 1.39/1.07 | 1.27/0.64 | 1.11/0.50 |
| `ep_yield_pct_smest_fy1_3`（1.70/1.02） | 1.66/0.99 | **1.70/1.11** | **1.74/1.15** | 1.49/0.91 | 1.42/0.74 | 1.22/0.57 |
| `expected_dividend_yield`（1.69/1.07） | 1.39/0.82 | 1.31/0.91 | 1.29/0.94 | 1.34/0.96 | 0.79/0.30 | 0.80/0.30 |
| **`asset_drift`（1.57/0.99）** | **1.77/1.21** ⭐ | 1.29/0.91 | 1.25/0.90 | 1.31/0.94 | — | — |
- **`NONE`（不中性化）**：TO 塌到 **0.048–0.057**、margin 飙到 **80–96bp**，但 S 掉到 0.65–0.80（F 仍 0.88–1.09）。
  ⇒ NONE 是另一条支线（超低换手 + 超高 margin），S 不够。

### ⚠ prod 同步上升：换档不是免费午餐
| 换档候选 | S/F | prod | 判定 |
|---|---|---:|---|
| `N1VO1Loq` ep_yield × **CROWDING** | 1.70/1.11 | **0.6919** | ✅ **通过**（self 0.6926）|
| `KPrLRJo8` ep_yield × MARKET | 1.74/1.15 | 0.7047 | ✗ 差 0.005 |
| `E5RK5RKR` leverage × SLOW | 1.94/1.37 | 0.7243 | ✗ |
| `P0g10xEW` leverage × CROWDING | 1.58/1.20 | 0.7348 | ✗ |
| `d51Qwzmw` leverage × SUBINDUSTRY | 1.53/1.22 | 0.7884 | ✗ |
| `d51QwzgJ` pd_pct × SUBINDUSTRY | 1.39/1.07 | 0.7978 | ✗ |
| `O089k78g` **asset_drift × SLOW** | **1.77/1.21** | **0.7169** | ✗ 超 0.017 |
**规律**：换档同时抬高 F 与 prod ⇒ **只有 prod 本就有余量的候选才过得去**（ep_yield 0.6861→0.6919 涨 0.006 过关；
leverage 0.6579→0.7243 涨 0.066 就崩）。
⚠ `N1VO1Loq` 与 `RR6NOlma` **同信号 ⇒ 同族，只能提 1 颗**。

### ❌ `asset_drift` × SLOW（`O089k78g`）：prod **0.7169 FAIL**
S **1.77** / F **1.21**（原 STATISTICAL 1.57/0.99）—— 但换档把 prod 从 0.6731 抬到 **0.7169**，超线 0.017。
⇒ **中性化档是真实强杠杆（F 可达 +0.35），但与 prod 强正相关，不能凭空造出候选。**
**正确用法**：对「已在 prod 边缘、但 S/F 偏弱」的候选用它推 F；**不要用它救 prod 已很紧的候选**。

### ★★★ 方法论修正（本段最重要的沉淀）
**「中性化档」是与「字段」「窗口」「轴」并列的独立杠杆，且强度最大（S 可达 +0.32 / F +0.35）。**
- 旧记忆只写"中性化档是真 prod 杠杆但代价 2Y 塌"—— 实测**S 也会大涨**，不止 prod。
- **更新后的操作序**：① 选对字段 → ② 扫 `STATISTICAL` 定方向 → ③ **扫 `SLOW`/`CROWDING`/`MARKET` 攻 F**
  → ④ 测 prod（换档抬 prod，须逐档实测）→ ⑤ 避开 `FAST`/`SLOW_AND_FAST`/`REVERSION_AND_MOMENTUM`（一律更差）。
- **教训**：**参数空间扫描必须把「批级设置」纳入网格**，不能只扫表达式内部参数。
  我此前把最强杠杆锁死在默认档，是流程性失误。

## GBR 空间结论
- 平台 GBR TOP700 D1 **只有 50 个数据集**，多数 coverage=0 或全 VECTOR（`quant_factor_lib` 在 GBR 亦然）。
- **能提取横截面信号的只有三类维度**：① 估值水平/变化（prod 已饱和 0.69–0.72）；
  ② 信用违约（`model53` 已用）；③ **结构化信用 `model28`** + **预期股息率（`model109`）**（本轮新发现）。
- **规律**：**派生/复合字段（概率、百分位、聚类、模型分）在 GBR 窄截面普遍无区分度**；
  有效的是**原始财务/信用/股息量在时间上的变化**（`ts_delta` + **短窗 8–13**）。
- **点塔**：本季 GBR D1 全为 MODEL 塔；OTHER/NEWS/INSTITUTIONS/PV(pattern_scores)/INSIDERS 全部实测无效。
""")

open(OUT, "w", encoding="utf-8").write("\n".join(L))
print("written:", OUT)
