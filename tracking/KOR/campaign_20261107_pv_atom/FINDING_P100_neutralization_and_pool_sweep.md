# FINDING · 中性化扫描 + 存量池全扫（2026-11-08 深夜）

## 一、存量 IS 池全扫：200 条里只有 10 条过线，且全部是同一族

`get_user_alphas(stage=IS, region=KOR, type=REGULAR, limit=100)` 分页拉 200 条，本地全量筛选。

- Sharpe 分布：p50 = **0.76**，p75 = 1.34，p90 = 1.40，p95 = 1.62，p99 = 2.23，max 9.13（伪像）。
- 满足 S≥1.58 ∧ 2Y≥1.58 ∧ F≥1.0 的共 **10 条，全部是 `intraday_pv_feats` 的 corr-with-volume 族**，且全部 prod 撞墙。
- ⇒ **历史池已经挖干**，不存在「旧件现在过线」的遗漏。

近线（S、2Y 均 ≥1.35）共 43 条，其中 40 条属于两个族：`dividend_policy_analysis_3`（40+ 变体）与 `corr_*_with_volume`。

## 二、dividend_policy_analysis_3 近线族：中性化扫描也救不了

基线：`subtract(group_rank(ts_mean(vec_avg(dividend_policy_analysis_3),44),industry),0.5)` @ REVERSION_AND_MOMENTUM / decay 4 / trunc 0.03
→ **S 1.42 / F 1.05 / 2Y 1.98 / raF 1（仅 LOW_SHARPE）**。

本轮扫掉最后 4 种未试中性化（decay 4，同一组 4 条表达式）：

| neutralization | 最优 S | 2Y | TO |
|---|---:|---:|---:|
| **REVERSION_AND_MOMENTUM**（基线） | **1.42** | 1.97 | 0.1052 |
| SLOW_AND_FAST | 1.28 | 1.56 | 0.1281 |
| MARKET | 1.01 | 1.98 | 0.0648 |
| SUBINDUSTRY | 0.88 | 1.80 | 0.0665 |
| STATISTICAL | 0.78 | 1.67 | 0.0831 |

⇒ **REVERSION_AND_MOMENTUM 已是该族最优中性化**，S 上限 1.42 确认结构性。
不足的 0.16 Sharpe 无法用「设置层」补，只能换信息内容。**该候选 park，不再投入。**

## 三、新铁律 F：概率桶字段名在同一数据集内不成套，派发前必须逐 id 校验

`global_seasonal_model` 的 `*_return_quantile5_prob{K}` 并非每个源都齐 5 个桶：
- `analyst_120d_return_quantile5` 只有 prob0 / prob1 / prob2（无 prob3、prob4）；
- `analyst_60d_return_quantile5` 有 prob1/2/3/4；
- `analyst_calendar_60d_return_quantile5` 只有 prob1 / prob3。

P99 首轮因用了不存在的 `analyst_120d_return_quantile5_prob4`，平台返回 `Attempted to use unknown variable`
⇒ **整批 10 条全部 CANCELLED**（父批 status=ERROR）。

**正确姿势**：把候选表达式里所有标识符抽出来，与 `get_datafields` 返回的 id 集合做集合差，差集非空就不派发。
⚠ `validate_fields: true` **不挡这个坑**——它只验字段前缀合法性，不验桶号是否成套。

## 四、工具坑补充
- `lookINTO_SimError_message` 可查子仿真：父批 ERROR 时逐 child 查能拿到真实报错（其余 CANCELLED 只是连坐）。
- `harvest_multisim_alphas` 在父批 status≠COMPLETE 时只返回 `No children found`，无法部分收割 ⇒ 必须先 lookINTO 定位。