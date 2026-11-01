# GBR 字段级机制地图（2026-10-31）

> **目的**（objective 第 1 条后半句）：「对 category 下的数据集字段做好充足的画像分析，**为后面使用不同机制奠定基础**」。
> **用法**：先看 §2 的「已验证通道」选字段 → 再看 §3 的「已证伪边界」排除 → 最后按 §4 的闸门顺序执行。
> **骨架底稿**：`results/field_cluster_map_gbr_20261031.md`（6465 个字段前缀簇 / 71 个 GBR 数据集；簇名 = 字段名去尾部序号取前三段 = 语义族代理）。

---

## §1 三层读法

| 层 | 内容 | 权威来源 |
|---|---|---|
| **L1 骨架** | 数据集 × 字段语义簇 × coverage × 拥挤度(alphaCount) | `results/field_cluster_map_gbr_20261031.md` |
| **L2 通道** | **已实测能出货的「字段 × 几何」组合**（含最优窗口与设置） | 本文件 §2 + 各数据集台账 |
| **L3 边界** | 已证伪的字段 / 几何 / 设置，及**为什么** | 本文件 §3 + 各数据集台账 |

★ **本地 `alphas`/`fields` 表没有字段级有效性判定**（`fields.verified` 只是「收录标记」1/0/−1，
`verified_context` 是区域标识，`field_group` 全库为空）⇒ **L2/L3 只能靠实测台账，不能查库得到。**

---

## §2 L2 · GBR 已验证通道（选字段就选这些）

### 2.1 NEWS（塔位 0→5，本轮新点亮）

| 字段 | 几何 | 强度 | 备注 |
|---|---|---|---|
| `nws17_multiple_comp_event_relevance` | `vec_sum` → `ts_mean(·,60)` → `ts_rank(·,252)` → `group_neutralize(·,densify(market))` → `ts_target_tvr_decay(target_tvr=0.05,lambda_max=5)` | **S 2.18 / F 1.45 / 2Y 2.86** | 全族最强 |
| `nws17_multiple_comp_relevance` | 同上，但 `vec_count` | S 2.10 / F 1.38 / 2Y 2.33 | 到达率轴 |
| `nws18_multiple_comp_sse` | 同上，`vec_count` | S 1.97 / F 1.27 / 2Y 2.20 | news18 唯一有意义的计数字段 |
| `nws17_multiple_comp_event_sentiment_score` | 同上，`vec_count` | S 1.86 / F 1.14 / 2Y 2.00 | 情绪到达率轴 |
| `nws17_multiple_comp_ssc` | `vec_count` × `rank(vec_avg(event_similarity_days))` | S 1.85 / F 1.14 / 2Y 1.91 | 合成置信轴（新颖度只可进乘子位） |

**统一设置档**：`GBR / TOP700 / D1 / FAST / decay 15 / trunc 0.05 / nanHandling ON / maxTrade OFF / VERIFY`。
**独立轴只有 5 条**（到达率 / sse / 事件强度 / 情绪到达率 / 合成置信），`max_mutually_below_subset = 5`。

### 2.2 FUNDAMENTAL（本轮新点亮 0→4）

| 字段 | 几何 | 强度 | 备注 |
|---|---|---|---|
| `fundamental17` 的 EBITDA / EBIT / 净利润 ÷ **`current_enterprise_value`** | `rank(ts_quantile(ts_av_diff(divide(F, EV), 252), 22, gaussian))` | S **2.48** / F 2.22 / 2Y 2.69 | ★ **纯 FUNDAMENTAL 单塔**（EV 是 fundamental17 集内市场量，不碰 PV 的 `cap`） |
| 同族 `ts_zscore` 版（EBIT/EV, 504） | `rank(ts_quantile(ts_zscore(divide(F, EV), 504), 22, gaussian))` | S 2.00 / F 1.64 / 2Y 1.92 | 与上一条互相关 0.9573 ⇒ 二选一 |
| 同族 净利润/EV 504 | 同构 | S 1.99 / F 1.57 / 2Y 2.10 | 与上一条 0.6868 |
| `fnd6_capxy` ÷ `cap` | `rank(ts_quantile(ts_av_diff(·,252),84,gaussian))` | S 2.21 / F 2.05 / 2Y 2.51 | **PV+FUND 双塔**（含 `cap`） |
| `fnd6_newq_cheq` ÷ `cap` | 同构 + `group_rank(·,subindustry)` | S 1.72 / F 1.26 / 2Y 2.09 | PV+FUND 双塔 |

★ **塔位杠杆**：分母用 `current_enterprise_value`（fundamental17 集内）⇒ 纯单塔不吃 trio 配额；
分母用 `cap`（PV 集内）⇒ 变双塔、吃「单组合 ≤3 / trio×非trio ≤5」配额。

### 2.3 MODEL / ANALYST（已点亮，可加固）

| 字段 | 几何 | 强度 |
|---|---|---|
| `ep_yield_pct_smest_fy1_3`（`predictive_starmine`） | `ts_delta(ts_backfill(·,500),20)` + `ts_target_tvr_decay` + `group_rank(·,industry)` | S 1.72 / F 1.03 / 2Y 1.84（**MODEL 单塔**） |
| `mdl28_sm_structural_credit_structural_asset_drift_pct` | `ts_delta(ts_backfill(·,250),8)` + `ts_target_tvr_decay` + `group_zscore` | S 1.67 / F 1.09 / 2Y 2.21 |
| `expected_dividend_yield`（`model109`） | `ts_delta(ts_backfill(·,500),11)` + `ts_target_tvr_decay` + `group_zscore` | S 1.62 / F 1.04 / 2Y 2.19 |
| `expected_dividend_yield`（ANALYST 塔变体） | 同上 | 同上 |
| `eps_revision_magnitude` ÷ `ts_mean(eps_y1_estimate_coeff_var,55)` | `group_rank` + `signed_power` + `ts_target_tvr_decay` | S 1.67 / F 1.04 / 2Y 1.81（EUR，ANALYST 单塔） |
| `mean_flash_estimate_ebt_annual12`（`analyst_consensus`） | 相对自身 252 日均值偏离 + `group_rank(·,sector)` | S 1.66 / F 1.24 / 2Y 2.09（IND） |

### 2.4 SHORTINTEREST / INSTITUTIONS

| 数据集 | 字段 | 几何 | 强度 | 状态 |
|---|---|---|---|---|
| `shortinterest3` | `transaction_count_main` | `group_rank(·,subindustry)` × −1 + 极端笔数区掩码 | S 1.95 / F 1.33 / 2Y 1.96 | ✅ **1 条**（SHORTINTEREST 塔 0→1，需 3 条才点亮） |
| `institutions6` | `quantity_institutional_shares_disposed ÷ (acquired+disposed)` | `rank(-ts_regression(ts_zscore(returns,252), ts_zscore(ts_delay(·,21),252), 252, rettype=0))` | **S 3.20 / F 2.52 / 2Y 3.00** | ★ IND 侧最强（**INSTITUTIONS+PV 双塔**） |
| `institutions6` | 卖压/买压家数、机构持股市值等 30 个字段 | 同骨架换分子 | S 2.5–3.35 | 同族 ⇒ 互相关高，最多取 1–2 条 |
| `institutions1` | 全部 7 字段 | — | — | ❌ 4 探针全灭（见 §3.4） |

### 2.5 跨区可搬运的通道（同一机制换区）

| 机制 | GBR | EUR | IND | USA |
|---|---|---|---|---|
| 机构持股卖压回归 | — | — | `E5VNe67L` S 3.20 | — |
| 内部人/大股东笔数计数 | — | — | — | `d5KPPrxx` S 3.13 / `88vJ1YKa` S 2.94 / `O0Jgd7Y7` S 2.27 |
| 信用质量比位移 | — | `omWVZ7lm`（⚠ 十年不满） | — | — |
| 现金质量比门控 | — | `mL617YPx` S 1.82 | — | — |
| 盈利质量估值偏离 | `rKRQbPPE` S 2.48 | — | — | — |

---

## §3 L3 · 已证伪边界（选字段时直接跳过）

### 3.1 几何级

| 写法 | 结果 | 出处 |
|---|---|---|
| 弱几何 `group_rank(ts_mean(x,22), subindustry)` | NEWS 族上限 S 0.91 ⇒ **弱几何全灭 ≠ 机制不可行** | 本轮 |
| `winsorize` / `tail` / `rank` / `signed_power` 接在 `ts_rank` 之前 | **数学恒等**（单调变换不改序） | memory |
| `ts_rank` 二次包装（`-ts_rank(ts_corr(·),252)`） | S −0.01（重复排序） | memory |
| `ts_quantile(·,252,gaussian)` 作 SUB 杠杆 | 在 S4 比值信号上 SUB 0.79→**−0.13** | 本轮十模板波 |
| `if_else` 掩码（置 nan） | TO 推高 + 广度砍半 ⇒ 双杀 F（S2 F 0.78） | 本轮十模板波 |
| `ts_corr(x, delay(x,5),66)` 二阶矩 | S 0.11（新闻到达率上全灭） | 本轮十模板波 |
| `ts_zscore` 作位移锚 | 在 fundamental6 族 2.28 vs 均值锚 2.71（弱 8%） | 台账 |
| 协方差比 `-divide(ts_covariance(A,B,d), ts_std_dev(B,d))` | S 0.53（归一化把信息量除了） | memory |

### 3.2 字段级

| 字段 / 族 | 结果 |
|---|---|
| `nws18_multiple_comp_qmb` / `ssc`（单实体族 `nws18_*`） | `vec_count` **恒等变换**（同事件集全填充）⇒ 换字段 = 换名字 |
| `nws17_multiple_comp_nip` | 与 `relevance` 相关 **1.0000**（逐位相同） |
| `event_similarity_days` 作信号本体 | S **−0.33**（元变量只能进乘子位/门控位） |
| `nws17_multiple_comp_rp_story_event_count` | S 1.47 / 2Y 0.78 |
| `fnd6_gpy ÷ fnd6_revty`（水平毛利率） | **已证伪**（台账 §6:339）⇒ 本轮补量波 10/10 全灭的直接原因 |
| `inst1_*` 流量/存量比 | GBR 4 探针全灭（DEU S 1.53 不可复现） |
| `fnd86_earnings_score`（GBR） | `fundamental86` 已判死 |
| `expected_dividend_yield` 的另一批几何 | prod **1.0000**（同族撞墙） |
| `annualized_pd_2_year_jc7` 的另一批几何 | prod **0.9985–1.0000** |

### 3.3 数据集级（结构性不可达）

`institutions4`（标识符映射非信号）· `institutions25`（cov 0）· `earnings6` / `earnings_sent_matrix`（cov 0）·
`sentiment7`（覆盖不足致 SUB 结构性失败）· `sentiment33` / `sentiment27` / `sentiment21` · `insiders1` / `insider_agg_matrix`（TO 0.016–0.06 近静态）· `news104` / `news50` · `other455` · `dl_riskfree` · `pv29`（50 字段全是簇标签）· `pv47_spret`（**prod 13/13 ≥ 0.7，族级封盘**）· `predictive_starmine` 的部分几何。

### 3.4 ★ 跨区不可搬运的三个实例

| 机制 | 原区 | 移植区 | 结果 |
|---|---|---|---|
| 稀疏事件「流量/存量比」 | DEU `institutions1` S 1.53–1.59 | GBR `institutions1` | 4 探针全灭（**DEU 成功载体本身在 GBR 也不可复现**） |
| 信用质量比位移 | EUR `quant_factor_lib` | GBR | 无该数据集 |
| `expected_dividend_yield` 位移 | GBR S 1.62 | — | USA/EUR 需各自重测（跨区 ≠ 通用） |

---

## §4 执行闸门顺序（每条候选必过的 5 道，本轮实证顺序）

| # | 闸 | 工具 | 成本 | 本轮拦下的 |
|---|---|---|---|---|
| 1 | **台账排除** | `grep -r "<dataset>" docs reports` 读「已证伪 / 判死」章节 | 零 | 补量波直接踩已证伪的水平毛利率 |
| 2 | **RA 闸 + 塔位** | `batch_get_alpha_metrics`（平台权威）+ `get_alpha_details`（`checks.fail` / `pyramids.list`） | 零配额 | `zqbvOmOR` S 4.30 挂 3 闸；本地库的 `failed_ra_count` 是**旧快照**（记 0、实读 3） |
| 3 | **近十年** | `get_alpha_yearly_stats` 逐年核 `longCount>0 / shortCount>0 / pnl>0` | 只读 | `omWVZ7lm` 前六年 0、`9qxP0JbV` 前五年 0、`pwv9eM76` 2015 负 |
| 4 | **self-corr** | `check_self_correlation`（本区 OS 池） | 本地计算 | 5 条（S 4.73 / 4.64 / 2.90 / 2.00 / 1.92） |
| 5 | **篮内互相关 + 配额** | `compute_mutual_correlation` + 塔位组合计数 | 本地计算 | 同族只能取 1–2 条；PV+FUND 恰好 3 条卡线 |

★ **顺序不能换**：② 先于 ③（否则把数据不满十年的当优质候选），④ 先于 ⑤（重跑项会污染最大团）。
★ **self-corr 判据分两层**：**0.7 = 提交红线**（超了不可提交）；**0.99 = 「重跑 vs 同族变体」的分类阈值**。
★ **OS 池按区隔离**（GBR 21 / EUR 12–15 / IND 52–60 / USA 140）⇒ 池小的区 self 门槛天然更松。

---

## §5 「为后面使用不同机制」的操作指引

1. **选字段**：从 §2 的通道表出发，而不是从「哪个数据集没挖过」出发 —— 后者会撞 §3 的证伪边界。
2. **选几何**：NEWS 用强几何基底（`ts_target_tvr_decay` + `group_neutralize(·,densify(market))` + `ts_mean(·,60)` + `ts_rank(·,252)`）；
   FUNDAMENTAL 用「位移 + 自历史分位」（`ts_av_diff` + `ts_quantile`），**且分母优先选集内市场量**（`current_enterprise_value`）以保单塔。
3. **换轴的唯一有效手段是换语义或换数据集**（§6.9 / §11.14）—— 同族换字段、换窗口、换算子**不产生新轴**，只会把相关推高。
4. **收割优先于重挖**：先查本地 `alphas` 的 prod-clean 池（`prod_correlation < 0.7` 且 `stage='IS'` 且未提交），
   再跑五道闸 —— 本轮用这条路径零仿真配额拿到 21 条。
5. **新机制先查论坛 + 论文**（用户纪律），并把模板族标注来源；不足 10 个互异模板不派发。

---

## §6 本轮（2026-10-31）五条新增通用结论

1. **「prod 未知」多半是检索盲区，不是平台阻塞** —— 本地 `alphas.prod_correlation` 早存着平台实测值。
2. **prod 墙是族属性**：同一字段族的 prod 命中率一致，选族优先、选几何次要。
3. **塔位杠杆**：`current_enterprise_value` 让 `divide(科目, EV)` 成为纯 FUNDAMENTAL 单塔。
4. **弱几何全灭 ≠ 机制不可行** —— 换几何能救；但**强几何也救不回不存在的信号**。
5. **跨区提交几乎不产生相关性冲突**（跨区互相关 0.00–0.22），且 OS 池按区隔离 ⇒ 跨区是凑条数与点塔的最短路径。