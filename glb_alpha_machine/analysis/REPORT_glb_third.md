# GLB_THIRD Stage 因子归因分析报告 (Markdown)

> **生成时间**: 2026-08-09 19:04
> **文件来源**: `cache/results_glb_third.jsonl`
> **报告路径**: `analysis/REPORT_glb_third.md`

---

## 1. 数据概览

| 指标 | 值 |
|------|-----|
| 有效候选 | **132** |
| Mean\|S\| | 0.482 |
| Max\|S\| | **0.620** |
| P50\|S\| | 0.480 |
| Min\|S\| | 0.360 |
| Mean Turnover | 0.0461 (4.6%) |
| 三区同号 | 27/132 (20.5%) |

### Sharpe 分布直方图

```
|S| 范围          数量
[+0.360, +0.386) █████ (5)
[+0.386, +0.412) ██████████ (10)
[+0.412, +0.438) ███████████ (11)
[+0.438, +0.464) ██████████████████ (18)
[+0.464, +0.490) ████████████████████████ (24)
[+0.490, +0.516) █████████████████████████████ (29)
[+0.516, +0.542) ███████████████████ (19)
[+0.542, +0.568) ████ (4)
[+0.568, +0.594) ███████████ (11)
[+0.594, +0.620) █ (1)
```

---

## 2. 累计 Top 5 候选

| # | \|S\| | 算子 | 分组 | Fit | Margin | Field |
|---|------|------|------|-----|--------|-------|
| 1 | 0.620 | group_zscore | market | +0.37 | +17.2bp | `anl15_s_cal_fy2_6m_chg` |
| 2 | 0.590 | group_neutralize | market | +0.34 | +16.0bp | `anl15_s_cal_fy2_6m_chg` |
| 3 | 0.590 | group_neutralize | industry | +0.35 | +17.4bp | `anl15_s_cal_fy2_6m_chg` |
| 4 | 0.580 | group_neutralize | sector | +0.34 | +16.9bp | `anl15_s_cal_fy2_6m_chg` |
| 5 | 0.580 | group_zscore | market | +0.34 | +15.1bp | `anl15_s_cal_fy2_6m_chg` |

**区域分布 (Top 5):**

| # | Amer | Apac | Emea | 一致? |
|---|------|------|------|-------|
| 1 | +0.58 | +0.10 | +0.33 | ✅ |
| 2 | +0.53 | +0.09 | +0.33 | ✅ |
| 3 | +0.54 | +0.07 | +0.35 | ✅ |
| 4 | +0.51 | +0.07 | +0.37 | ✅ |
| 5 | +0.53 | -0.05 | +0.49 | ❌ |

---

## 3. 持续 Top 追踪 (9 份报告)

### 字段出现率

| 字段 | 出现率 | 趋势 |
|------|--------|------|
| `anl15_s_cal_fy2_6m_chg` | **9/9 (100%)** | ████████████ |

### 算子出现率

| 算子 | 出现率 |
|------|--------|
| `trade_when+neutralize+winsorize+abs` | 9/9 (100%) |
| `trade_when+ts_arg_max+neutralize+winsorize+abs` | 7/9 (78%) |
| `trade_when+ts_arg_min+neutralize+winsorize+abs` | 4/9 (44%) |
| `trade_when+ts_mean+neutralize+winsorize+abs` | 3/9 (33%) |
| `trade_when+ts_std_dev+neutralize+winsorize` | 1/9 (11%) |
| `trade_when+ts_arg_min+neutralize+winsorize` | 1/9 (11%) |
| `trade_when+ts_std_dev+neutralize+winsorize+abs` | 1/9 (11%) |
| `trade_when+ts_arg_max+neutralize+winsorize` | 1/9 (11%) |
| `trade_when+ts_mean+neutralize+winsorize` | 1/9 (11%) |
| `trade_when+neutralize+winsorize` | 1/9 (11%) |
| `trade_when+group_zscore+winsorize+abs` | 1/9 (11%) |

### 组合 (field+op) 出现率

| 组合 | 出现率 |
|------|--------|
| `trade_when+neutralize+winsorize+abs(anl15_s_cal_fy2_6m_chg)` | 9/9 (100%) |
| `trade_when+ts_arg_max+neutralize+winsorize+abs(anl15_s_cal_fy2_6m_chg)` | 7/9 (78%) |

---

## 4. 区域归因分析

| 区域 | MeanSharpe | 评价 |
|------|-----------|------|
| **Amer** | +0.476 | 🟢 最强 |
| **Apac** | -0.039 | 🔴 反向 |
| **Emea** | +0.366 | 🟢 最强 |

---

## 5. 稳健性检查

| 检查项 | 结果 | 阈值 |
|--------|------|------|
| \|Sharpe\| ≥ 1.58 | 0/132 (0%) | ❌ |
| Fitness ≥ 1.0 | 0/132 (0%) | ❌ |
| Turnover ∈ [1%, 70%] | 132/132 (100%) | ✅ |
| Margin ≥ 5bp | 132/132 (100%) | ✅ |
| 三区域同号 | 27/132 (20%) | ⚠️ |

---

## 6. 关键发现与建议

### 🔑 核心发现

1. **`anl15_s_cal_fy2_6m_chg` 持续霸榜** — 9/9 报告 Top10
2. **Apac 区域**: MeanSharpe=-0.039, 系统性反向 — 信号在亚太不成立
3. **三区一致候选**: 27/132 (20.5%) — 需更多区域分散的信号

### 🏆 最佳三区一致候选

```
表达式: trade_when(ts_corr(close, volume, 20) > 0.3, group_zscore(winsorize(ts_backfill(anl15_s_cal_fy2_6m_chg, 120), std=4), densify(market)), abs(returns) > 0.1)
|S\| = 0.620
Fit  = +0.37
Marg = +17.2bp
Turn = 5.1%
Amer = +0.58
Apac = +0.10
Emea = +0.33
```

### 📋 建议

| 优先级 | 行动 |
|--------|------|
| P0 | 深挖三区一致候选，进入 stage3 尝试 basic_ops 增强 |
| P1 | 如果仍不达 1.58，考虑切换 dataset 或区域 |
| P2 | 等待更多批次完成后重新评估 |
