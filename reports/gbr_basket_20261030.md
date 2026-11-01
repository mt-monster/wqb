# GBR/TOP700/D1 候选篮子结算报告（2026-10-30）

范围：真实 GBR（`alphas.region_id = 7`）· REGULAR 提交线 · 延迟 1

> **口径铁律**：`backtest_results.region` 列不可信（例：`zqrKEPXo` 本地记 GBR，平台实读 `EUR/TOPCS1600`）。
> 全部统计一律 `JOIN alphas a ON a.alpha_id = b.alpha_id WHERE a.region_id = 7`。
> 塔位一律取 `get_alpha_details.pyramids` / `ra.pyramid_short`，**不从数据集名猜**。

---

## 1. 本轮新增的三条判死（含两条重复历史）

| 线 | 证据 | 结论 |
|---|---|---|
| **sentiment7** | 6 个结构互异骨架，最好 `78LOlldQ` S 1.25 / F 0.77 / 2Y 1.12，**SUB 0.12**（limit = 0.4743×1.25 = 0.593） | 判死。coverage 0.58 ⇒ TOP700 小半区无 Wikipedia 数据，SUB 结构性失败，换几何不可救 |
| **dl_riskfree** | `omE2k7Gn` S 1.00 但逐年 2022 **−1.63** / 2023 **0.07**，近三年 pnl 合计 **−134342**；命中已有 `GBR-DLRISKFREE-LABEL-DEAD`(2026-08-26) | 判死（**本轮 2 探针属重复历史**）。原始方向概率水平值本质是动量代理 |
| **other455** | 真实 GBR 59 行，当信号 best S 1.02 / 当分组轴 best S 1.02；命中已有 `GBR-O455-N2V-PROBE-DEAD` + `GBR-GROUPRANK-DECORREL-SHARPE-CONSERVATION` | 判死（**重复历史**） |

### 1b. 本轮新判死：earnings6 全族（8 条）

`failed_ra_count` 8 条全部 ≥1，根因一律是 `LOW_SUB_UNIVERSE_SHARPE`：

| alpha | S | F | 2Y | SUB | SUB 要求(0.4743×S) | 缺口 |
|---|---|---|---|---|---|---|
| `P0gbMLz7` | 1.77 | 1.53 | 2.06 | 0.43 | 0.84 | −49% |
| `A1v5QXmg` | 1.72 | 1.45 | 1.67 | 0.37 | 0.82 | −55% |
| `JjQkxJgl` | 1.69 | 1.41 | 1.84 | 0.34 | 0.80 | −58% |
| `ZYAzdx1n` / `qM0GQElE` | 1.68 | 1.42 | 1.64 | 0.41 | 0.80 | −49% |
| `QPKzNjAW` | 1.69 | 1.40 | 1.41 | 0.22 | 0.80 | −73% |
| `A1vzrb5d` / `omWGJvXl` | 1.59/1.58 | 1.29/1.28 | 1.47 | 0.34/0.33 | 0.75 | −55% |

**机理**：`vec_avg(ern6_actual_eps / |ern6_estimated_eps|)` 的覆盖率不足，与 sentiment7 同构——是**数据覆盖问题**，不是骨架问题。不要再对该族堆模板。

### 1c. 本轮新判死：`pv47_spret`

全库 13 条有 prod 值的 `pv47_spret` 表达式：**13/13 ≥ 0.7**（0.7710–0.8675，最高 `58jxXXb5` 0.8675）。
⇒ `KPrmWlwN`（S 1.62 / F 1.03 / 2Y 1.89 / failed_ra 0）**prod = 0.8024 直接 BLOCKED**，族层面封盘。

---

## 2. ★ 本轮最重要的结构性发现：prod 墙是**族级别**的，且 GBR 能过的族聚在 0.68–0.70

`alphas` 表按 `region_id=7 AND prod_correlation < 0.7` 统计：**ACTIVE 9 / COMPLETE 14 / UNSUBMITTED 21**。
把这 21 条按族展开后，能过 prod 的族高度集中：

| 族 | prod 区间 | 样本 |
|---|---|---|
| `est_12m_pre_raisednum − lowerednum`（分析师修正广度） | **0.6793** | `d51O1kOX` / `akxLxjVv` / `O08r8QNp` / `blORMJwm` |
| `ep_yield_pct_smest_fy1_3` 位移 | 0.6861–0.6975 | `d51ddaWX` / `P0gvv5gE` / `RR6NOlma` / `58gMMJEk` |
| `mdl28_sm_structural_*` 位移 | 0.6608–0.6890 | `9qWwZ3go` / `mL68wNOK` / `pw58o7Nb` |
| `expected_dividend_yield` 位移 | **0.5956** | `6XKwmQgE` |
| `annualized_pd_2_year_jc7` 位移 | 0.5254–0.5338 | `zqbPGkpO` / `j289Gj1e` |
| `star_val` + `five_day_total_return_dlr2` 门控 | 0.6830–0.6986 | `rKO0GOVj`(ACTIVE) 等 |
| `forward_pe_mean_f12m_4` | 0.6900 | `GrOMbGO5` |

而撞墙侧同样成族：`annualized_pd_2_year_jc7` 的另一批几何 → **0.9985–1.0000**；`expected_dividend_yield` 的另一批 → **1.0000**。

**⇒ 可复用规则**：GBR 上「某个字段位移族」的 prod 命中率是**族属性**而非单条属性；选族优先，选几何次要。
上表 0.52–0.70 这 7 个族是 GBR 已验证可提交的通道，新候选应优先落在这几个族里换几何。

---

## 3. 候选篮子（11 条，两两互相关全 < 0.7）

`compute_mutual_correlation(threshold=0.7, years=4)` 实读：`num_points 1021`、`missing_pnl []`、
`max_mutually_below_subset_size = 11`、`max_subset_exact = true`。

| # | alpha | 塔位 | prod | S | F | 2Y | TO | margin | SUB | inv_ratio | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **`d51O1kOX`** | ANALYST | **0.6793** ✅ | 1.97 | 1.29 | 1.71 | 8.14% | 13.27bp | 1.06 | **1.000** | **0** |
| 2 | **`P0gvv5gE`** | ANALYST | **0.6905** ✅ | 1.72 | 1.03 | 1.84 | 12.23% | 7.36bp | 1.00 | 0.727 | **0** |
| 3 | **`9qWwZ3go`** | MODEL | **0.6890** ✅ | 1.67 | 1.09 | 2.21 | 13.40% | 8.48bp | 0.93 | 0.569 | **0** |
| 4 | **`6XKwmQgE`** | ANALYST | **0.5956** ✅ | 1.62 | 1.04 | 2.19 | 13.54% | 8.19bp | 1.31 | 0.661 | **0** |
| 5 | **`rKRkL9QE`** | PV+FUND | 0.6783（本轮） | 2.21 | 2.05 | 2.51 | 8.33% | 25.94bp | 1.77 | — | **0** |
| 6 | `0mYoANkv` | PV+FUND | **未测** | 1.89 | 1.54 | 2.08 | 11.66% | 14.22bp | 1.12 | — | 0 |
| 7 | `WjOkLGWx` | PV+FUND | **未测** | 1.72 | 1.26 | 2.09 | 9.31% | 14.53bp | 0.94 | — | **0** |
| 8 | `88v5aEE7` | PV | **未测** | 3.49 | 1.53 | 1.90 | 54.22% | 3.85bp | 1.88 | 0.258 | **0** |
| 9 | `d5KkorEj` | PV | **未测** | 2.68 | 1.31 | 2.22 | 37.13% | 4.81bp | 1.74 | 0.384 | **0** |
| 10 | `KPmlLE3E` | PV | **未测** | 3.17 | 1.30 | 2.56 | 53.82% | 3.34bp | 1.76 | 0.300 | **0** |
| 11 | `omWKpjgJ` | MODEL | **未测** | 1.78 | 1.02 | 2.11 | 12.58% | 6.56bp | 1.19 | 0.742 | **0** |

**家族内互相关（只能取 1 条）**：`P0gvv5gE × RR6NOlma` **0.9961**、`P0gvv5gE × 58gMMJEk` 0.9905、
`P0gvv5gE × d51ddaWX` 0.9772、`d51ddaWX × RR6NOlma` 0.9767、`d51ddaWX × 58gMMJEk` 0.9751
⇒ `ep_yield` 四兄弟取 `P0gvv5gE`（F 1.03 最高）。

**pv1 族内互相关（只能取 3 条）**：`88v5aEE7 × d5KkorEj` **0.6965**（贴线）、`88v5aEE7 × KPmlLE3E` 0.3954、
`d5KkorEj × KPmlLE3E` 0.3397；同 exponent 连扫 2.5/2.6/2.7 彼此 **0.99+**；`58jnaAAM` 与 `88v5aEE7` 指标逐位相同（重复，不提交）。

**跨族互相关极低**：`d51O1kOX` 对全部其余 10 条均在 **−0.12 ~ +0.04**，是篮子里最好的分散项。

### 塔位效果（提交 11 条后）

| 塔 | 现状 | 提交后 | 是否点亮 |
|---|---|---|---|
| **PV** | 1 | 1 + 6 = **7** | ✅ 点亮 |
| **FUNDAMENTAL** | 0 | 0 + 3 = **3** | ✅ 点亮 |
| ANALYST | 3 | 3 + 3 = 6 | 已点亮 |
| MODEL | 5 | 5 + 2 = 7 | 已点亮 |

### trio × 非 trio 配额（上限 5）

已占 4/5：`6XA8AGjL`(PV+ANALYST)、`rKRkL9QE`、`0mYoANkv`、`WjOkLGWx`。
纯 PV（`88v5aEE7`/`d5KkorEj`/`KPmlLE3E`）、纯 ANALYST（`d51O1kOX`/`P0gvv5gE`/`6XKwmQgE`）、
纯 MODEL（`9qWwZ3go`/`omWKpjgJ`）**均不占配额** ⇒ 11 条全提交后仍余 1 席。

---

## 4. 未验证项 / 风险（提交前必读）

1. **6 条 prod 未测**（`0mYoANkv`/`WjOkLGWx`/`88v5aEE7`/`d5KkorEj`/`KPmlLE3E`/`omWKpjgJ`）。
   账号级单并发，本轮两次触发均被兄弟会话（`ZYQZbnYx`、`omE2Xn8k`）抢占，`retry_after 240`。需独占窗口才能做。
2. **4 条 prod 值是 2026-10-08 的（21 天前）**：`d51O1kOX` 0.6793 / `P0gvv5gE` 0.6905 / `9qWwZ3go` 0.6890 / `6XKwmQgE` 0.5956。
   生产池会漂移，只有 `6XKwmQgE`（余量 0.104）安全，前三条余量仅 0.010–0.021，**提交前须 `refresh=True` 终验**。
3. **`FUNDAMENTAL` 塔点亮依赖 `0mYoANkv` + `WjOkLGWx` 双过 prod**（rKR 单颗只能贡献 1/3）。
4. **pv1 三条生产池风险未知**：同族历史 `1YjkooEW` prod 0.7562（BLOCKED）、`LL5VwgO1` 0.6926（过），**50% 命中率**，不能按族推断。
5. **pv1 三条流动性偏薄**：`investability_ratio` 仅 0.258/0.384/0.300，`88v5aEE7` 与 `KPmlLE3E` margin 3.85bp/3.34bp @ TVR 54% ⇒ Phase C **CONDITIONAL**（3–5bp @ 40%+）。`d5KkorEj` 三条里最优（2Y 2.22 / TO 37% / margin 4.81bp / inv 0.384）。
6. **`WjOkLGWx` risk_neutralized_sharpe 仅 0.65（38%）**、`0mYoANkv` 1.02（54%）⇒ 两条都有 prod 撞墙的结构性风险。
7. `ep_yield` 四兄弟 2Y 差异：`d51ddaWX` 2.05 > `P0gvv5gE` 1.84 > `58gMMJEk` 1.82 > `RR6NOlma` 1.79；
   若 prod 终验发现 `P0gvv5gE` 0.6905 已漂过 0.7，备胎按上述 2Y 顺序换，但**换腿不换族**，相关性 0.975+ 视同同一条。

---

## 5. 结论

- 已判死：`sentiment7`（6 结构）、`dl_riskfree`（2 探针 + 逐年为负）、`other455`（信号与轴两用）、
  `earnings6`（8 条全 SUB 失败）、`pv47_spret`（13/13 prod ≥ 0.77）、`KPrmWlwN`（prod 0.8024）。
- 可用篮子 **11 条**，两两 < 0.7，`failed_ra` 全 0，其中 **5 条 prod 已验证 < 0.7**。
- 提交后一次点亮 **PV + FUNDAMENTAL 两塔**，距离 20 条目标完成 11 条。
- 剩余瓶颈是 prod 单并发被兄弟会话长期占用；以及 6 条 prod 未测。
