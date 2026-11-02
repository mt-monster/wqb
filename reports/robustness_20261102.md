# EUR 提交前稳健性审计 — 6 条 OFF 篮

> 日期：2026-11-02T12:20+08:00
> 范围：EUR 严格 OFF 可提交篮 6 条（`vR15O0aw` / `ZYQjm0Pd` / `78oNgz1Z` / `mL61avpx` / `6Xdw1OqG` / `qMLAdj7V`）
> 依据：`brain-alpha-robustness` Phase B / C（判定阈值 = 2026-04-22 论坛共识台账，不随当日论坛内容变动）
> 设置：EUR / TOPCS1600 / D1 / SUBINDUSTRY / decay 4 / truncation 0.08 / **maxTrade=OFF**
> IS 区间：2014-01-01 ~ 2023-12-31 ⇒ **最近 3 个 IS 年 = 2021 / 2022 / 2023**

---

## 0. 结论

| verdict | 条数 | alpha |
|---|---|---|
| **PASS** | **3** | `vR15O0aw` / `6Xdw1OqG` / `qMLAdj7V` |
| **CONDITIONAL** | **2** | `78oNgz1Z`（统计面）/ `ZYQjm0Pd`（构造纪律面） |
| **REJECT** | **1** | **`mL61avpx`** |

⇒ **提交可用篮从 6 条降到 5 条**（3 PASS + 2 CONDITIONAL 待复核），`mL61avpx` 被稳健性闸挡下。

**本轮零提交**：所有判定只写台账，未做任何不可逆动作。

---

## 1. Phase C 主表（最近 3 个 IS 年 = 2021–2023）

| alpha | 近3年 S | 2021 | 2022 | 2023 | 近3年均值 | 全期 S | CV | 衰减比 | max/min | 平年 | 算子 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `vR15O0aw` | 2.41 / 3.34 / 2.60 | 2.41 | 3.34 | 2.60 | **2.78** | 3.10 | **0.144** | 0.839 | 1.39 | 0 | 5 | **PASS** |
| `ZYQjm0Pd` | 3.37 / 1.64 / 2.56 | 3.37 | 1.64 | 2.56 | **2.52** | 2.12 | 0.280 | 1.208 | 2.06 | 0 | 11 ⚠ | **CONDITIONAL**（构造纪律） |
| `78oNgz1Z` | 2.29 / 1.14 / 3.53 | 2.29 | 1.14 | 3.53 | **2.32** | 1.91 | **0.421** ⚠ | 1.848 | **3.10** ⚠ | 0 | 5 | **CONDITIONAL** |
| `mL61avpx` | 3.38 / 2.39 / **0.56** | 3.38 | 2.39 | **0.56** | 2.11 | 1.78 | **0.554** ⚠ | **0.315** ⚠ | **6.04** ✗ | 0 | 9 ⚠ | **REJECT** |
| `6Xdw1OqG` | 2.18 / 2.58 / 2.32 | 2.18 | 2.58 | 2.32 | **2.36** | 1.68 | **0.070** | 1.381 | 1.18 | 0 | 5 | **PASS** |
| `qMLAdj7V` | 2.79 / 2.37 / 1.65 | 2.79 | 2.37 | 1.65 | **2.27** | 1.63 | **0.207** | 1.012 | 1.69 | 0 | 5 | **PASS** |

**共同达标项**（6/6 全过）：
- 近 3 年均值 **2.11–2.78**，全部 ≥ 2Y 线 1.58；
- 近 3 年**每年为正且 > 0.3**，**平年 0 个**；
- `LOW_SUB_UNIVERSE_SHARPE` 全部 PASS；
- Margin @ turnover 全部 ≥ 5bp（最低 `mL61avpx` 2023 年 4.55bp @ TVR 8.4%，未触发「<3bp @ >60%TVR」条）；
- WebDataScope `failed_ra_count == 0`（6/6，见 §4）。

---

## 2. 逐条判定依据

### 2.1 `vR15O0aw` → **PASS**

```
group_neutralize(group_scale(signed_power(
  rank(ts_backfill(tm_16_r1_r5_r10_rh_glb_d1_r10_q1, 22)), 1.5), industry), subindustry)
```
- **经济可解释性 ✓**：`tm_16_*` 是模型预测分数，排序后做多高分股；`rank` + `signed_power(1.5)` + 双层分组标准化只做截面整形，不改信号方向。一句话可写。
- 近 3 年 S 2.41/3.34/2.60，CV **0.144**、max/min **1.39**，是本篮最平稳的一条。
- 算子 5 个，无过拟合软标记。
- ⚠ 软标记：2020 年回撤 4.83%，是全期年均 1.69% 的 **2.86 倍**；`signed_power` 指数取 **1.5**（既有纪律是 0.5 / 2 附近）。

### 2.2 `ZYQjm0Pd` → **CONDITIONAL**（统计面全过，构造纪律面存疑）

```
group_neutralize(group_scale(add(
  signed_power(group_zscore(divide(est_12m_dps_raisednum_4wks,
                                   est_12m_dps_num_4wks_ago), subindustry), 1.5),
  multiply(1.2, group_rank(divide(ts_backfill(vec_sum(num_jobs_active), 250),
                                  add(ts_backfill(vec_avg(mean_days_job_active), 250), 1)),
                           subindustry))), industry), market)
```
- 统计面：近 3 年均值 2.52、CV 0.280、衰减比 1.208、max/min 2.06、平年 0 —— **全部 PASS**。
- **但构造形态撞了用户硬约束**：`add(信号A, multiply(1.2, 信号B))` 正是「**禁止 `add(A,B)` 混信号调参**」点名的模式，且权重 **1.2 是手设常数**。
  - 信号 A = 分析师上调 12 个月股息预测的家数占比（ANALYST，修正广度）
  - 信号 B = 招聘岗位活跃度（`num_jobs_active` / `mean_days_job_active`，劳动市场类）
  - 两条腿经济含义无关，靠 1.2 的权重拼在一起，属于典型的多信号拼接。
- 另：算子 **11 个**（软标记线 > 5），`signed_power` 指数同为 1.5。
- **处置建议**：不要把 `multiply(1.2, …)` 当可调参数去扫（那正是过拟合的来源）。若要用，二选一——
  ① 只用 A 腿单信号重建（掉 S 但构造干净）；② 保留但如实向用户说明这是历史双腿拼接，接受其过拟合风险。

### 2.3 `78oNgz1Z` → **CONDITIONAL**

```
ts_target_tvr_decay(trade_when(greater(fnd6_newa1_ebitda, fnd6_newa1_ib),
                               group_zscore(divide(fnd6_newa2_oancf, fnd6_newa1_at), sector), -1),
                    lambda_min=0, lambda_max=1, target_tvr=0.12)
```
- **经济可解释性 ✓**：先用「EBITDA > 利息支出」筛掉付息有压力的公司，再按「经营现金流 / 总资产」做行业内截面打分 —— 赚得到钱且杠杆不压人的公司，现金流效率越高越好。一句话可写。
- 触发 **2 个 CONDITIONAL 项**：
  - `CV_Sharpe = 0.421`（0.40–0.60 带）——近 3 年 2.29 / 1.14 / 3.53 跳幅大；
  - `max/min = 3.10`（3–5 带）——2022 年 1.14 是三年最低。
- ⚠ 软标记：2020 年回撤 **8.29%**，年均 3.57% 的 **2.32 倍**，是全篮绝对回撤最大的一条。
- 未触发任何 REJECT 项。按 skill，CONDITIONAL → 先 `brain-alpha-repair` 复核（≤2 轮）再请用户确认。

### 2.4 `mL61avpx` → **REJECT**

```
ts_target_tvr_decay(quantile(signed_power(
  trade_when(greater(divide(vec_avg(fnd72_pit_or_is_a_ebitda),
                            vec_avg(fnd72_pit_or_cf_a_cf_net_inc)), 0.28),
             group_rank(multiply(divide(vec_avg(...cash_from_oper), vec_avg(...bs_tot_asset)),
                                 divide(vec_avg(...cash_from_oper), vec_avg(...net_inc))),
                        sta1_allc5), -1), 1.05),
  driver=gaussian), lambda_min=0, lambda_max=1, target_tvr=0.06)
```
- **硬 REJECT 项**：`Recent-3yr max/min Sharpe = 3.38 / 0.56 = 6.04 > 5`。
  2023 年 Sharpe 从 2022 的 2.39 **塌到 0.56**，margin 从 27.4bp 掉到 **4.55bp**（−83%），是全篮唯一一条**近端明显衰减**的。
- 伴随 CONDITIONAL：`衰减比 = 0.56 / 1.78 = 0.315`（0.30–0.50 带，**离 REJECT 线 0.30 只有 0.015**）。
- 统计上它并没有失效（近 3 年均值仍有 2.11），但**近一年几乎失去边际**，按闸规则不提交。
- 算子 9 个（软标记）；`signed_power` 指数 1.05、`quantile(driver=gaussian)` 属非标设置。

### 2.5 `6Xdw1OqG` → **PASS**

```
vector_neut(reverse(rank(divide(ts_backfill(total_financing_cash_flow, 252),
                                ts_backfill(assets_total_2, 252)))),
            rank(divide(ts_backfill(operating_cashflow, 252),
                        ts_backfill(assets_total_2, 252))))
```
- **经济可解释性 ✓**：融资现金流占资产越高 ⇒ 公司越依赖外部融资扩张 ⇒ 后续回报越弱，故 `reverse` 做多低依赖者；再用经营现金流/资产做正交化，剔除「本来就是现金牛」的重叠。一句话可写。
- 近 3 年 2.18 / 2.58 / 2.32 —— **CV 0.070、max/min 1.18**，全篮最稳。
- 算子 5 个；margin 36.1bp @ TO 2.79%，容量比 0.994（全库存最健康）。
- ⚠ 软标记：2020 年回撤 4.95%，年均 2.24% 的 **2.21 倍**。

### 2.6 `qMLAdj7V` → **PASS**

```
reverse(rank(ts_mean(divide(ts_backfill(total_financing_cash_flow, 252),
                            ts_backfill(assets_total_2, 252)), 504)))
```
- **经济可解释性 ✓**：同 2.5，但用 2 年（504 日）均值代替正交化——只取「长期融资强度」这一个概念。一句话可写。
- 近 3 年 2.79 / 2.37 / 1.65，CV 0.207、衰减比 1.012、max/min 1.69，全部 PASS。
- 算子 5 个；margin **109.8bp** @ TO 1.08%。
- ⚠ 软标记：2020 年回撤 7.35%，年均 2.81% 的 **2.62 倍**；TO 距 `LOW_TURNOVER` 下限仅 **8bp**。

---

## 3. 一个必须说清的系统性现象：2020 年回撤告警对所有 6 条同时成立

| alpha | 2020 回撤 | 年均回撤 | 倍数 | 是否标警 |
|---|---|---|---|---|
| `vR15O0aw` | 4.83% | 1.69% | 2.86× | 是 |
| `ZYQjm0Pd` | 4.62% | 1.62% | 2.85× | 是 |
| `78oNgz1Z` | 8.29% | 3.57% | 2.32× | 是 |
| `mL61avpx` | 3.43% | 2.16% | 1.59× | 否 |
| `6Xdw1OqG` | 4.95% | 2.24% | 2.21× | 是 |
| `qMLAdj7V` | 7.35% | 2.81% | 2.62× | 是 |

**5/6 条在同一年（2020）同时越 2 倍线**，且这 6 条底层数据集互不相同（`tm_16` / ANALYST+劳动 / `fnd6` / `fnd72` / `fundamental23`×2）。
⇒ 这是 **EUR 区域的 2020 年制度性事件**，不是任何单条 alpha 的缺陷。**不应据此单独拒绝某一条**，只作组合层的统一提示。

（这与前几轮已记录的「2020 年弱是 EUR 共性」一致：`ZYQjm0Pd` −0.75、`78oNgz1Z` −0.64、`mL61avpx` 0.33 同样在 2020 塌陷，只有 `vR15O0aw` 2.64 扛住。）

---

## 4. 未测项（如实标注，不充当已通过）

| 检查 | 状态 | 原因 |
|---|---|---|
| **prod 相关性** | **未测** | 保鲜期 48h，实测 2–3 天可从 0.58 漂到 0.98；提交冻结期测了等于白测。解冻后须逐条 `check_correlation(refresh=True)` 终验 |
| **Top-5 个股市集中度** | **未测** | 当前 `get_alpha_pnl` 只返回累计 PnL，无逐股分解；skill 亦注明逐股归因在分解可得前是可选的 |
| **季度级回撤日历** | 用**年度**回撤近似 | 同上，无日频持仓分解；年度最大回撤已足以识别 2020 事件（§3） |
| **`performance_comparison`** | 未跑 | 边际贡献为负只是软标记；本轮判定未被它影响，留待用户终审前补 |

---

## 5. 台账落点

`ledger_kv[EUR]` 写入 6 个键 `robustness_<alpha_id>`，`report_path = reports/robustness_20261102.md`。
`submit_verdict` 读到 `REJECT`（`mL61avpx`）即 BLOCKED（`reason_code: ROBUSTNESS_REJECT`）；
`CONDITIONAL`（`78oNgz1Z` / `ZYQjm0Pd`）不改判，但 `next_step` 会提示先复核再请用户确认。
