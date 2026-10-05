# ANALYST 塔 USA 深度挖掘报告 — 2026-10-02

> 目标：在 USA 的 ANALYST 塔（25 个数据集，blank 塔）找到可提交的 REGULAR alpha。
> 方法：论坛（analyst10/15/4/14 系列帖 + 262 票模版帖）+ 外部文献（开源证券 FOM 因子、中信建投一致预期体系、分析师异常覆盖度）→ 结构设计 → 逐轮实测。

## 1. 最终结论（一句话）

**ANALYST 塔的 IS 闸可被攻破（拿下了 USA 首个「全 IS 闸通过」的非 news 候选），但 prod 相关性墙无法绕过（0.88–0.90）。**

## 2. 攻破 IS 闸的冠军候选

**`58gRVm65`**（`group_neutralize` 版，S=1.60）
```
ts_decay_linear(
  group_neutralize(
    group_rank(
      ts_zscore(ts_mean(ts_backfill(vec_avg(consensus_high_estimate_quarterly), 252), 22), 630),
      subindustry),
    subindustry),
  400)
```
设置：USA / TOP3000 / D1 / decay 66 / SUBINDUSTRY / truncation 0.08

| 平台检查 | 结果 |
|---|---|
| LOW_SHARPE | **PASS 1.60** ✅ |
| LOW_FITNESS | **PASS 1.13** ✅ |
| LOW_2Y_SHARPE | **PASS 2.20** ✅ |
| LOW_SUB_UNIVERSE_SHARPE | **PASS 0.72** ✅ |
| Turnover | 0.0151 |

> 基线版 `O08eEGPR`（无 group_neutralize）S=1.58 / F=1.16 —— 同样是全 IS 闸 PASS。

## 3. 完整旋钮链（S 1.24 → 1.60）

| 步骤 | 变化 | 效果 |
|---|---|---|
| 0 | 基线（无 backfill） | S=0.63、2Y=−0.29 |
| 1 | **+`ts_backfill(vec_avg(F), 252)`** | S→1.24、**2Y→2.08 PASS**（估算字段稀疏，必须回填）|
| 2 | **z-score 窗 60 → 630** | S **1.24 → 1.54（+0.30）** |
| 3 | **ts_decay_linear 窗 200 → 400** | F **0.84 → 1.11** |
| 4 | **`ts_mean(…, 22)` 预平滑** | S **1.54 → 1.58**（破闸）|
| 5 | **`group_neutralize(…, subindustry)`** | S **1.58 → 1.60** |

## 4. 被否定的分支（附证据）

| 分支 | 结果 |
|---|---|
| **FOM 预期修正率**（文献第一因子）| S ≤ 1.12，2Y 多 FAIL |
| 分歧度 stddev | S ≤ 1.01 |
| 盈余惊喜 surprise | S ≤ 0.53 |
| 覆盖变化 count | S ≤ 1.07 |
| 下修数（负向）| S 1.08，**2Y 1.69 PASS** 但 SUB 0.41 F |
| biasfree 系 | S ≤ 1.48（2Y 最高 2.46）|
| `analyst_consensus`(3245 字段) 目标价/long-term EPS | S 0.80–0.89 |
| TOP2000 宇宙 | S 0.90（TOP3000 正确）|
| settings decay 0 / 200 | 1.51 / 1.52（66 最优）|

## 5. prod 相关性：全部失败

| 候选 | S | prod |
|---|---|---|
| O08eEGPR（champ） | 1.58 | **0.90** ✗ |
| O08eEYMJ（w693） | 1.56 | **0.8976** ✗ |
| 58gRVm65（gn subindustry） | 1.60 | **0.8805** ✗ |
| LLZeeLwn（gn market） | 1.60 | **0.8985** ✗ |

去相关手段（subtract / `group_neutralize` / `ts_regression` 残差 / `vector_neut` / `trade_when` / delta）**全部无法把 prod 拉到 0.7 以下**（最好的只降 0.02）。

## 6. ★★ 板级结论

| 独立概念 | prod |
|---|---|
| analyst 一致预期 | 0.88–0.90 |
| news 情绪 | 0.80–0.96 |
| 财报电话会 NLP | 0.90 |
| insider 交易 | 0.82–0.93 |
| quant_factor_lib (MODEL) | 0.90 |

**五个互不相关的概念，prod 全部落在 0.82–0.96。** 机制：它们都是**慢速（T≈0.015）、低换手的横截面水平信号**，共同载荷在 size / quality / market 因子上。

⇒ **USA 的 prod 拥挤是「板级」现象，与选哪个数据集/概念无关。** 想在美国点新塔，只能：
1. **走 PPA 通道**（Power Pool：Sharpe ≥ 1.0、算子 ≤ 8、字段 ≤ 3、PPAC < 0.5，仅限主题窗口内，且需平台 web UI）
2. **换战场**（GBR / DEU / ASI / AMR 等零提交区）

## 7. 平台算子可用性（实测，供后续复用）

| 算子 | 状态 |
|---|---|
| `to_nan` | ❌ 无权限（替代 `if_else(x == 0, nan, x)`）|
| `ts_max` / `ts_min` | ❌ 不存在（只有 `ts_arg_max`/`ts_max_diff`）|
| `ts_quantile(x, d, driver=gaussian)` | ✅ |
| `group_neutralize` / `hump`(1 参) / `reverse` / `densify` | ✅ |
