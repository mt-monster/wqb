# MEA / Delay1 / TOP300 — S1 特征工程 ideas（战役：10 颗 REGULAR，2026-08-28）


> S0 白名单：fundamental72 / fundamental6 / earnings3（用户指定重点+豁免判死）、analyst7（辅线）。
> 已证设置模板：region=MEA, universe=TOP300, delay=1, decay=4, neutralization=COUNTRY, truncation=0.08, nanHandling=OFF。
> 约束：每条表达式 1-2 字段；LEVEL 盈利水平场禁入（PROD 饱和）；est_q_*_1mth 升降差族禁入（自家池蚕食）。

---

## 1. fundamental72（Comprehensive Fundamental，Bloomberg PIT 季报/年报）

**数据集理解**：pit_or 前缀 = point-in-time，含 BS/CF/IS 三表季度(_q)与年度(_a)字段 + announcement_dt（财报公告日）。季度族在 MEA/TOP300 覆盖率 0.8-0.88，远高于该集整体 0.545——**只用季度族与高覆盖年度族**。

**字段白名单**（cov≥0.65，平台有真实使用量）：
- `fnd72_pit_or_bs_q_bs_tot_asset` (0.876, 14 users)
- `fnd72_pit_or_bs_q_bs_retain_earn` (0.875)
- `fnd72_pit_or_bs_q_bs_cash_near_cash_item` (0.876)
- `fnd72_pit_or_bs_q_bs_net_fix_asset` (0.855)
- `fnd72_pit_or_cf_q_cf_cash_from_oper` (0.841, 10 users)
- `fnd72_pit_or_cf_q_cf_net_inc` (0.864)
- `fnd72_pit_or_cf_q_cf_cap_expend_prpty_add` (0.833)
- `fnd72_pit_or_is_q_is_oper_inc` (0.876, 11 users)
- `fnd72_pit_or_is_q_inc_bef_xo_less_min_int_pref_dvd` (0.875, 9 users)
- `fnd72_pit_or_is_q_ebitda` (0.681)
- `fnd72_pit_or_is_q_is_eps` (0.876)
- `fnd72_pit_or_bs_a_announcement_dt` (0.755)

**预处理决策**：
- VECTOR 慢变量：先 `ts_backfill(120)` 防断点，再进时序算子；若报 "does not support event inputs" 则降级 `vec_avg` 包裹。
- 金额类跨公司不可比 → 一律两字段 divide 做比率，或 ts 变化率。
- 方向类统一 `rank(...)`；反向写 `-rank(...)`（不用 reverse）。

**特征概念（正交于 LEVEL 饱和族）**：
1. **盈余动量（SUE 族变体）**：`rank(ts_av_diff(fnd72_pit_or_is_q_inc_bef_xo_less_min_int_pref_dvd,252)/ts_std_dev(...,252))` — 盈利意外的持续性，论坛模板同构但换字段换窗口。
2. **现金转化质量变化**：`divide(ts_delta(cf_cash_from_oper,252), ts_delta(is_net_inc 近义字段,252))` 或两者 zscore 差 — 应计质量的反向代理，正交于盈利水平。
3. **留存加速度**：`rank(ts_delta(ts_delta(bs_retain_earn,63),63))` — 二阶变化捕捉内生增长加速。
4. **资本开支强度反转**：`-rank(ts_delta(cf_cap_expend_prpty_add,252))` 相对变化 — 过度投资折价（MEA 小盘产能过剩）。
5. **财报陈旧度**：`-rank(ts_days_elapsed 类结构于 bs_a_announcement_dt)` — 新财报披露的漂移。

---

## 2. fundamental6（Worldscope 公司基本面）

**数据集理解**：混合频度（annual/quarterly/YTD/semiannual）VECTOR 为主 + 少量 MATRIX 季度截面字段。wave69 "全字段 EVENT" 判死**不成立**：以下字段返回正常 VECTOR/MATRIX 元数据。

**字段白名单**：
- MATRIX 季度截面（可直接横截面运算，平台高使用量实证）：
  - `fundamental_revenue_quarterly` (cov 0.692, 33 users)
  - `fundamental_income_before_extraordinary_items_q` (0.437, 74 users)
  - `fundamental_net_sales_quarterly` (0.427, 41 users)
  - `fundamental_operating_net_cash_flow` (0.442, 14 users)
  - `fundamental_current_assets_total_q` / `current_liabilities_total_quarterly`
- VECTOR 高覆盖年度：
  - `fundamental_pretax_income` (0.921), `fundamental_ebitda` (0.914)
  - `annual_depreciation_and_amortization` (0.915)
  - `fundamental_retained_earnings` (0.900), `fundamental_common_equity_total` (0.915)
  - `fundamental_inventory_total_annual` (0.853), `debt_current_liabilities_total` (0.825)
  - `fundamental_net_revenue` (0.559)

**预处理决策**：年度慢字段 `ts_backfill(365)`；MATRIX 季度字段直接 `rank`/`ts_zscore(…,252)`；比率一律两字段 divide。

**特征概念**：
1. **边际利润率变化**：`rank(ts_delta(divide(income_before_extra_q, revenue_quarterly),252))` — 盈利质量拐点（1 表达式 2 字段）。
2. **营运资本效率**：`-rank(divide(current_assets_total_q, net_sales_quarterly))` 的 ts 变化 — 资产轻量化溢价。
3. **税前利润动量**：`rank(ts_av_diff(fundamental_pretax_income,252)/ts_std_dev(fundamental_pretax_income,252))` — SUE 同构换数据源。
4. **库存周期背离**：`-rank(ts_delta(fundamental_inventory_total_annual,252))` 与收入动量背离方向 — 需求转弱预警。

---

## 3. earnings3（财报日历，4 个 MATRIX 字段）

**字段**：`ern3_pre_interval`（距上次财报交易日数，非正值，cov 0.525）、`ern3_next_interval`（距下次，cov 0.429）、`ern3_pre_reptime` / `ern3_next_reptime`（时段码）。

**预处理决策**：MATRIX 直接可用；整数字段用 `rank`/`bucket`，禁 `ts_mean` 平滑；cov≈0.5 有 CONCENTRATED_WEIGHT 风险 → 表达式必须带横截面 rank 且避免门控后样本过窄。

**特征概念**：
1. **财报临近漂移**：`-rank(ern3_next_interval)` — 财报前买入窗口效应。
2. **财报后漂移衰减**：`rank(ts_delta(ern3_pre_interval,5))` — 刚发布财报的动量。
3. **日历节奏异常**：`-rank(ern3_pre_interval - ts_mean(ern3_pre_interval,252))` 的变体 — 披露节奏变化（延迟披露=坏消息假说）。

---

## 4. analyst7（Broker Estimates，辅线）

**禁入**：`est_q_*_raisednum/lowerednum_1mth` 升降差族（自家池 14+ 高分变体，SELF 蚕食铁律）。

**字段白名单（正交家族）**：
- 一致预期水平与历史快照：`est_q_pre_mean`(0.52,61 users)、`est_q_pre_mean_4wks_ago`、`est_q_pre_mean_28d`(0.55)、`est_q_eps_mean`(0.57,96 users)、`est_q_eps_mean_3mth_ago`、`est_q_sal_mean`(0.58)、`est_q_net_mean_28d`(0.60)、`analyst_mean_revenue`
- 价格目标：`analyst_price_target_mean`(MATRIX, cov 0.665，但 alphaCount 1823 拥挤 → 只做变化率)

**特征概念**：
1. **修正动量（幅度型，区别于广度型）**：`rank(ts_av_diff(est_q_pre_mean,21)/abs(est_q_pre_mean_4wks_ago))` — 4 周修正幅度。
2. **快闪-稳定背离**：`rank(est_q_pre_mean_28d - est_q_pre_mean)` — 短期情绪 vs 稳定共识的裂口。
3. **盈利预期加速度**：`rank(ts_delta(est_q_eps_mean,63)/abs(est_q_eps_mean_3mth_ago))`。
4. **目标价修正**：`rank(ts_delta(analyst_price_target_mean,21))` — MATRIX 直接可用。

---

## 5. 多样性与配额规划（10 颗目标）

| 数据集 | 目标颗数 | 收益来源 | 骨架 |
|---|---|---|---|
| fundamental72 | 3-4 | 盈余动量/现金质量/投资效率 | ts_av_diff 标准化、二阶 delta、比率 delta |
| fundamental6 | 2-3 | 利润率拐点/营运效率 | 比率 zscore、SUE 同构 |
| earnings3 | 1-2 | 日历效应 | rank 截面、短窗 delta |
| analyst7 | 2-3 | 预期修正动量 | 幅度型修正、快闪背离 |

- 跨数据集策略相关性目标 < 0.4（S4 用 compute_mutual_correlation 验证）。
- 算子多样性：rank / ts_av_diff / ts_delta / divide / ts_zscore / group_rank 至少 6 类；禁用 hump、reverse。
- 每波 ≤10 条进回测；EXPECTED_BLOCK（CW/高 turnover）在门禁层即回 Mode B。

## 6. 已知风险与闸门
- f72/f6 VECTOR 字段若报 event 错误 → 该字段本轮剔除（不恋战）。
- cov<0.6 字段一律要求表达式带横截面 rank + COUNTRY 中性。
- LEVEL 盈利水平场（rank(zscore(net_inc,252)) 类）全禁：PROD 池饱和（死路 MEA-FND72-ISQ-LEVEL）。