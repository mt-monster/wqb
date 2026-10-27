# EUR × analyst7 修订族 ATOM 手册（2026-10-20 定稿）

> 本文件是 EUR 首个 **单数据集 10+ 颗全闸通过** 的完整配方与纪律。
> 证据主档：[`docs/reference/EUR/eur_analyst_field_profile_20261018.md`](../../../../docs/reference/EUR/eur_analyst_field_profile_20261018.md) §52–§56。
> 战绩：**14 颗 RA 全过 / 6 个 metric 族 / 全部 ATOM（analyst7 单数据集）**；一次最多同时提交 7 颗。

## 1. 适用范围

- 数据集：`analyst7`（1111 个 `est_12m_*` 字段；32 个指标具备 `mean + mean_3mth_ago + mean_4wks_ago + std` 四件套）。
- 类别：Analyst；金字塔 EUR/D1/ANALYST（×1.3）。
- 本手册只服务「四件套」形态。`analyst7` 的其余字段族（快照差分 / 单字段）在 60 条实测里 S 上限 0.88、2Y 全灭，不属本配方。

## 2. 设置（与区域缺省不同，必须显式传）

| 设置 | 本族值 | 区域 settings.json 缺省 |
|---|---|---|
| universe | **TOP2500** | TOPCS1600 |
| neutralization | **FAST** | SUBINDUSTRY |
| decay | **40（幅度）/ 80（广度、门控、gps）** | 4 |
| nanHandling / maxTrade | **ON / ON** | 同 |
| truncation / language | 0.08 / FASTEXPR | 同 |
| 其余 | EQUITY / D1 / 2014-01-01→2023-12-31 / FULL / pasteurization ON / unitHandling VERIFY | 同 |

⚠ `$WQ_PY -m wqb.profiles explain --region EUR` 返回的是**区域缺省**，不是本族设置。直接发 MCP 时逐项传上面这张表，否则会以 TOPCS1600/SUBINDUSTRY/decay4 跑出另一条信号。
⚠ 不要拿旧台账里的 "TOP2500 ⇒ S 崩 1.34–1.40" 否定本表：那条结论来自 `analyst_factor_signals`（不同数据集、不同结构），不适用于 `analyst7` 四件套。

## 3. 骨架（两种，同一原语）

记 `Δ(x) = subtract(x, x_4wks_ago)`，`tn(·) = group_neutralize(·, market)`。

**A. 修订幅度（主力，9 颗）**

```
tn(signed_power(group_zscore(divide(subtract(<metric>_mean, <metric>_mean_4wks_ago), <metric>_std), subindustry), p), market)
```

经济含义：4 周内共识预期的**变化量 ÷ 分歧度** = 经不确定性标准化的修正 surprise；`tn(·, market)` 去掉市场 beta 暴露。

**B. 修订广度（2 颗：4 周 `P0MOK7wx` / 1 周 `MP0L2Ogo`）**

```
tn(signed_power(group_zscore(divide(subtract(<m>_raisednum_4wks, <m>_lowerednum_4wks),
                                     add(<m>_raisednum_4wks, <m>_lowerednum_4wks)), subindustry), p), market)
```

经济含义：净上调占比 = 修正方向的一致性；与幅度形态的互相关只有 0.62–0.68，**是独立席位**。

**C. 广度 2Y 修复（`wp9EvMmv`）**：B 外包一层 `ts_mean(·, 5)` + decay 80。见 §5。

## 4. metric 族种子表（14 颗库存，全部 RA 全过）

| metric | 形态 | p | decay | alpha | S | F | 2Y | sub |
|---|---|---:|---:|---|---:|---:|---:|---:|
| dps | 幅度 | 1.4 / 1.2 / 1.0 | 40 | `LL5dmv9a` / `xA1d5YMW` / `JjPvrxll` | 1.71–1.78 | 1.02–1.03 | 2.32–2.41 | 0.95–1.00 |
| ebt | 幅度 | 1.4 / 1.2 / 1.0 | 40 | `e76xGOQO` / `E5Vexv39` / `pwvK3P0V` | 2.11–2.15 | 1.43–1.59 | 1.71–1.93 | 1.11–1.13 |
| ebi | 幅度 | 1.0 | 40 | `qME6VWbj` | 1.76 | 1.07 | 1.65 | 1.01 |
| gps | 幅度 | 1.4 | **80** | `3qjeJGle`（→ 修复版 `Grge2lN3`） | 1.72 | 1.08 | 1.80 | 0.95 |
| pre | 幅度 + 门控 | 1.4 | 80 | `6XAe27eL` | 1.74 | 1.10 | 1.62 | 0.96 |
| cps | 4 周广度 + `ts_mean5` | 1.4 | 80 | `wp9EvMmv` | 1.80 | 1.01 | 2.00 | 1.27 |
| ebt | 4 周广度 | 1.4 | 40 | `P0MOK7wx` | 2.13 | 1.38 | 1.65 | 1.36 |
| ebt | 1 周广度 | 1.2 | 40 | `MP0L2Ogo` | 2.03 | 1.24 | 1.76 | 1.20 |
| ebt | median 修订 | 1.2 | 40 | `A1Q729Ll` | 2.23 | 1.60 | 1.82 | 1.27 |
| ebt | high 修订 | 1.2 | 40 | `O0Jx2O6R` | 1.94 | 1.26 | 1.86 | 1.05 |

可迁移的 metric 族：`dps / ebt / ebi / gps / pre / cps / prr`。同一 metric 的 p 变体只产 1 席（互相关 0.97–0.99）。
`median / high` 是「共识统计量的位置」，有效；`std / num`（离散度变化、分析师家数变化）S ≤0.11，**已判死**。

## 5. 2Y / CV 修复：制度门控（本区最通用的一条）

**症状**：S/F 够，2Y 差 0.1–0.4（近两年低波动，绝对计数型信号自然萎缩）。

**配方**（`Grge2lN3` 由 `3qjeJGle` 修复而来；`6XAe27eL` 同构）：

```
trade_when(abs(ts_zscore(<单字段水平值或原信号>, 66)) > 1.0, CORE, 0)
```

| 门控 | 2Y | 说明 |
|---|---:|---|
| 无门控 | 1.39–1.80 | 视族而定 |
| 计数门控（`raisednum > 2 / > 4`） | 0.51–0.66 | **反向杠杆**：绝对计数随波动率萎缩 |
| `abs(ts_zscore(SIG,66)) > 1.5` | 1.20 | 过严，样本不足 |
| **`abs(ts_zscore(SIG,66)) > 1.0`** | **1.62** | pre 族全过 |
| **`abs(ts_zscore(<gps 水平字段>,66)) > 1.0`** | **2.02**（`Grge2lN3`） | 2022 Sharpe 1.39→2.09，CV .436→.366 |

**纪律**：
1. 门控对象是「**这次修正有多异常**」（时序 zscore），不是「**有多少家改**」（计数）。门控放宽只补样本量，不改强度（1.5→1.0：S/F 1.73/1.07→1.74/1.10）。
2. **算子数 ≤9**：把 CORE 完整写两遍会到 10 个算子，触发闸 1b-2。门控单字段水平值（如 gps 的 `<m>_mean`）可把全式压到 8 个算子。
3. 门控后必重跑稳健性：CV 用最近 3 年样本口径（见 `brain-alpha-robustness`），不要只看全期。

## 6. 参数轴与甜点

| 轴 | 甜点 | 边界 / 否证 |
|---|---|---|
| 修订窗 | **4 周**（`_4wks_ago`） | 1 周 = 独立快形态（TO 7.32%）；3 个月双重失败（sub + 2Y） |
| `signed_power` p | **1.0–1.4**（幅度 1.4；广度/median 1.2） | p1.6 起 sub 比率线抬升，`Grge7PG0` sub 0.97 < 线 1.01 |
| decay | 幅度 **40**；广度/门控/gps **80** | 广度 40→80 = 2Y +0.60（主导杠杆），S +0.24 / F +0.08 |
| 平滑 | 广度 `ts_mean(·,5)` = 临门一脚（F +0.03、2Y +0.06、TVR −0.28pt） | 幅度族 `ts_mean(ratio,5)` **摧毁信号**（S 1.72→1.42） |
| 中性化/分组 | 组内 `subindustry` + 外层 `tn(·, market)` | industry/sector/country 全部封闭（2Y 1.39 / sub 0.95） |
| universe | TOP2500 | TOP1200/TOP800 S 0.57–0.82（analyst 覆盖集中在大市值） |

## 7. 已否证杠杆（不要重试）

- **计数门控**（`raisednum > n`）→ 2Y 0.51–0.66。
- **`ts_mean(ratio, 5)` 于幅度形态** → S 1.72→1.42。
- **`winsorize(2.5)` / decay 120 求降 CV** → CV .520 / .444–.489（更差）。
- **`group_zscore` 替 `signed_power(group_rank)`**（旧 `analyst_factor_signals` 结构）→ S 1.75→1.12；本族已用 `signed_power`，不要反向替换。
- **下侧（low）修订** → sub 0.76（−0.18）；只做上侧 / 中位 / high。
- **3 个月窗口**、**std/num 形态**、**`mean_28d` 以外的一阶矩之外的插值**：见 §4/§6。
- **同族 p 变体当多条腿**：互相关 0.97–0.99，平台 self 闸只放 1 颗。
- **靠设置档换腿降 prod**：同族实测互相关地板 0.92–0.94（幂次 6.0 / INDUSTRY / lambda_max 0.5），prod 地板 0.9231；「强度-占用」同源，保序变换无法降相关。

## 8. 互相关与席位

- 同族 p 变体：dps 0.9704–0.9925；ebt 0.9728–0.9933 ⇒ **每族 1 席**。
- ebt 广度 vs 幅度：0.6216–0.6815（**真独立**）；ebi 幅度 vs ebt 幅度：0.6957–0.7383（边缘）。
- gps 最独立（与所有族 0.37–0.63）；cps 广度次之（0.30–0.57）。
- **最大互不相关团 = 7（精确解）**：`{LL5dmv9a, e76xGOQO, P0MOK7wx, qME6VWbj, 3qjeJGle, 6XAe27eL, wp9EvMmv}`，团内最大对 0.6957（贴线合规）。
- 因此「14 颗通过验证」≠「14 颗可同时提交」；**一次最多 7 颗**，其余进 B 席。

## 9. 测量与提交协议（顺序不可换）

1. `get_alpha_details`：读数 + 确认 `failed_ra_count = 0`。
2. `get_alpha_yearly_stats`：最近 3 年逐年 Sharpe（robustness 的 CV 口径）。
3. `get_alpha_pnl`：回撤日历与换手 × margin。
4. 本地 `check_self_correlation` 预估同族占用。
5. `check_correlation(refresh=True)`：平台 prod/self 终值（阻塞、账号级单并发、7 天缓存）。**读 `max`**。
6. `compute_mutual_correlation`：新增腿与既有池的最大相关（本地 4 年日收益即可，1021 点已够）。
7. 台账 `robustness_<id>` → `submit_verdict`（只否决）→ 用户明确确认 → `workflow_submit_alpha(confirm_submit=True)`。

`submit_verdict` 在 EUR 可能返回 `UNVERIFIABLE_404`（提交端点探针失败），**这不是拦截**；是否放行仍以平台 prod 实测 + 用户确认为准。

## 10. 派发纪律（本轮真实事故）

- `create_multi_simulation` **只认 snake_case**：`instrument_type` / `max_trade` / `nan_handling` / `unit_handling` / `test_period`。camelCase 键被**静默丢弃**，不报错。
  - 事故：AS/AT 两批以缺省 `nanHandling OFF / maxTrade OFF` 运行（换手 7.6–8.0% vs 同族 5.2%），读数只能作方向性证据、不进交付库存。
- **派发后读回一个子项的 `settings`，断言 `nanHandling` / `maxTrade` 为 ON** 再继续。
- 指标异常（换手偏高/偏低 2 个点以上）先查设置档，再归因信号。
- `validate_fields=true` 会把 `std=2.5` 这类命名参数误当字段 → 省略该开关。
- 一台 multisim 只带一个 settings 块；跨设置对比必须拆批（按表达式去重会吞掉重复式）。

## 11. 证据索引

| 内容 | 位置 |
|---|---|
| §55 收割与 14 颗库存 | `docs/reference/EUR/eur_analyst_field_profile_20261018.md` §55 |
| §56 prod 实测与座位 | 同上 §56 |
| 2Y/CV 修复全记录 | `reports/robustness_20261020.md`（`Grge2lN3` 段） |
| 边界算子合法档 | `tracking/EUR/reference/boundary_ops_eur.json` + [`_boundary-ops-eur.md`](_boundary-ops-eur.md) |
| DB 波次键 | `eur_a7_al` / `eur_a7_ap` / `eur_a7_au`（`backtest_results`） |
