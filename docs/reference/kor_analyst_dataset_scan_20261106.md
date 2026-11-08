# KOR · Analyst 全数据集扫描（2026-11-06，平台实拉 17/17）

> 数据源：`get_datasets(KOR, TOP600, D1)` 全表 + 逐集 `get_datafields(filter_sharpe=false)` 实拉，17 个 analyst 数据集全部翻页取全（`complete:true`）。
> 派生 JSON：`tracking/KOR/reference/field_profile/kor_<dataset>_fields_current.json`（本轮重拉，覆盖 2026-10 旧快照）。
> 区域固定 KOR / TOP600 / delay 1；IS 窗平台硬定 2014-01-01 → 2023-12-31。

## 一、扫描结论（按可挖性排序）

| 数据集 | 字段(平台) | 类型 | 平均 cov | aC=0 字段 | 单字段最高 aC | 历史回测 | 判定 |
|---|---:|---|---:|---:|---:|---:|---|
| `analyst_consensus` | 2343 | VECTOR 2325 / MATRIX 18 | 0.690 | 2147 | 17 | 0–3 | ★ 白空间王：把 consensus 与 actual 全对齐的 1929 字段大池；先验只测过覆盖广度（已判弱），revision/surprise 面几乎空白 |
| `analyst10` | 640 | MATRIX 475 / VECTOR 165 | 0.731 | 339 | 89 | 105 | ★ StarMine smartest predicted surprise（cov 0.96）；有 105 次回测史，best S 1.62 |
| `analyst44` | 540 | VECTOR 374 / MATRIX 166 | 0.773 | 167 | 104 | 42 | ★ 4 周修正族（eps/dps/bps 4wk change）；历史 best S 1.78 / 2Y 2.23 |
| `analyst_base_ref` | 14 | VECTOR 10 / MATRIX 4 | 0.732 | 3 | 27 | 0 | ★ 唯一「惊喜」专集：consensus_surprise_percentage / vs_actual_diff / stddev / num_estimates |
| `analyst_factor_signals` | 59 | MATRIX 59 | 0.577 | 21 | 54 | 2 | ★ 预计算修正因子库：eps_y1_change_3mo / revision_magnitude / trend_slope / skew / coeff_var |
| `analyst16` | 109 | VECTOR 109 | 0.653 | 37 | 28 | 15 | ○ 事件型：actsurprise / actsuescore / aftercons_difference（105 次回测里 15 次在此集） |
| `analyst11` | 210 | MATRIX 210 | 0.583 | 157 | 5 | 0 | ○ ESG/治理 KPI（不是盈利预期），慢变量；极低拥挤但机制与盈利无关 |
| `analyst9` | 48 | VECTOR 47 / MATRIX 1 | 0.567 | 9 | 20 | 0 | ○ 修正广度原语：numup / numdn / numanaylst；日频刷新 |
| `analyst48` | 70 | VECTOR 70 | 0.441 | 29 | 42 | 0 | ○ 股息/总回报预测族（bdhad / bdvd_curr_dvd_health / bnepd） |
| `analyst45` | 241 | VECTOR 241 | 0.253 | 197 | 11 | 0 | △ 极稀疏 VECTOR（分析师组合持仓/构想），cov 0.25，需 nan OFF |
| `analyst46` | 6 | MATRIX 6 | 0.421 | 0 | 10 | 0 | △ 文本情绪复合分，字段太少且已被占满 |
| `analyst81` | 5 | MATRIX 5 | 0.265 | 0 | 8 | 0 | △ 违约概率（PD），cov 0.26，机制离价格远 |
| `analyst14` | 461 | MATRIX 452 / VECTOR 9 | 0.500 | 96 | 530 | 8 | ✗ 拥挤（aC 最多 530）+ cov 恒 0.5（元数据不可信） |
| `analyst15` | 304 | MATRIX 304 | 0.525 | 1 | 3268 | 0 | ✗ 极饱和（aC 3268），零拥挤字段仅 1 个 |
| `analyst25` | 207 | VECTOR 207 | 0.500 | 1 | 470 | 0 | ✗ 极饱和（aC 470），cov 恒 0.5 |
| `analyst4` | 308 | MATRIX 260 / VECTOR 48 | 0.633 | 111 | 1095 | 0 | ✗ 极饱和（aC 1095，anl4_afv4_eps_mean） |
| `analyst39` | 43 | MATRIX 43 | 0.895 | 0 | 442 | 0 | ✗ 覆盖最高但零白空间（aC 442） |

## 二、选集决策

**第一梯队（wave272 开波）**：`analyst_factor_signals` + `analyst_base_ref`
- 两者是唯一「修正/惊喜语义直接落在字段上」的数据集，且拥挤度低（最高 aC 54 / 27）。
- 全是 MATRIX 或稠密 VECTOR（cov 0.58–0.73），不需要 nan OFF，工程风险最低。

**第二梯队（wave273 候选）**：`analyst_consensus`（2147 个零拥挤字段，红海中的白空间）、`analyst10`（pred_surps cov 0.96）、`analyst16`（事件型 surprise）。

**排除**：`analyst15/25/4/39/14` —— 单字段 aC 440–3268，已被平台玩家打满；`analyst45` 待第一梯队验证后按稀疏 VECTOR 规程（nan OFF）单独处理。

## 三、与 2026-10 判死结论的关系

旧结论（`_wave11-13_analyst_findings.md`）判死的是**「覆盖广度」与「分歧度水平」两种机制**，不是整个 analyst 面。
本轮不复刻这两条，只走 **修正动量 / 盈余惊喜 / 修正二阶结构** 三类新机制。

## 四、命中率约束（写进设计）

KOR 全战役 `prod_wall_ratio ≈ 0.52`：过 RA 闸的候选有一半死在 prod。⇒ 每族开波必须同时准备「降 prod」的壳层（`winsorize` / `ts_backfill` 改可交易集 / `signed_power`），不能等 S 达标后再补。
