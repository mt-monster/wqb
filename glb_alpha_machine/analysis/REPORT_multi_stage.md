# GLB Alpha Machine — 全阶段对比归因报告

> **生成时间**: 2026-08-09 19:04
> **数据来源**: `cache/results_*.jsonl`

---

## 1. 阶段演进总览 (Cross-Stage Progression)

| 指标 | Stage1 (一阶) | Stage2 (二阶) | Stage3 (三阶) | 演进趋势 |
|------|:---:|:---:|:---:|:---:|
| 有效候选数 | 88 | 248 | 132 | — |
| Mean\|S\| | 0.211 | 0.346 | 0.482 | 📈 持续提升 |
| Max\|S\| | 0.520 | 0.520 | 0.620 | 📈 最终上升 |
| P50\|S\| | 0.220 | 0.340 | 0.480 | 📈 持续提升 |
| Mean Turnover | 3.8% | 6.3% | 4.6% | 📈 最终上升 |
| 三区一致率 | 5% | 26% | 20% | 📈 最终上升 |

**Sharpe 演进路径:**

```
Max|S|:  0.520 ──Stage2──▶ 0.520 (+0%) ──Stage3──▶ 0.620 (+19%)
Mean|S|: 0.211 ──Stage2──▶ 0.346 (+64%) ──Stage3──▶ 0.482 (+39%)
P50|S|:  0.220 ──Stage2──▶ 0.340 (+55%) ──Stage3──▶ 0.480 (+41%)
```

**分布对比 (IQR/P50/Max):**

| 阶段 | P25 | P50 | P75 | 分布特征 |
|------|:---:|:---:|:---:|----------|
| Stage1 — 一阶原始 | 0.120 | 0.220 | 0.280 | IQR=0.160 (适中) |
| Stage2 — 二阶 group_ops | 0.310 | 0.340 | 0.370 | IQR=0.060 (集中) |
| Stage3 — 三阶 trade_when | 0.450 | 0.480 | 0.520 | IQR=0.070 (集中) |


## 2. 区域归因演进 (Regional Evolution)

| 阶段 | Amer | Apac | Emea | 最强区域 | 最弱区域 |
|------|:----:|:----:|:----:|:--------:|:--------:|
| Stage1 — 一阶原始 | +0.092 | -0.146 | -0.136 | **Amer** | ⚠️ Apac |
| Stage2 — 二阶 group_ops | +0.474 | -0.195 | -0.071 | **Amer** | ⚠️ Apac |
| Stage3 — 三阶 trade_when | +0.476 | -0.039 | +0.366 | **Amer** | ⚠️ Apac |

**区域一致性分析:**

- **Stage1 — 一阶原始**: Apac 系统性反向 (-0.146), 信号主要由 Amer 驱动
- **Stage2 — 二阶 group_ops**: Apac 系统性反向 (-0.195), 信号主要由 Amer 驱动
- **Stage3 — 三阶 trade_when**: Apac 中性 (-0.039), 需进一步验证

## 3. 各阶段 Top 候选对比

### Stage1 — 一阶原始 (Top 5)

| # | \|S\| | 核心操作 | 字段 | Fit | Margin | Turnover |
|---|:---:|:--------:|:----:|:---:|:------:|:--------:|
| 1 | 0.520 | `winsorize` | `anl15_s_cal_fy2_6m_chg` | +0.30 | +21.9bp | 3.7% |
| 2 | 0.450 | `winsorize` | `anl15_gr_12_m_pe` | -0.24 | -22.9bp | 3.2% |
| 3 | 0.410 | `winsorize` | `anl15_s_cal_fy1_1m_chg` | +0.24 | +7.9bp | 10.6% |
| 4 | 0.400 | `winsorize` | `anl15_gr_12_m_6m_chg` | +0.19 | +15.7bp | 3.6% |
| 5 | 0.390 | `winsorize` | `anl15_gr_12_m_ests_up` | +0.26 | +16.6bp | 6.9% |

### Stage2 — 二阶 group_ops (Top 5)

| # | \|S\| | 核心操作 | 字段 | Fit | Margin | Turnover |
|---|:---:|:--------:|:----:|:---:|:------:|:--------:|
| 1 | 0.520 | `group_neutralize` | `anl15_s_cal_fy2_6m_chg` | +0.30 | +21.9bp | 3.7% |
| 2 | 0.520 | `group_neutralize` | `anl15_s_cal_fy2_6m_chg` | +0.30 | +21.9bp | 3.7% |
| 3 | 0.520 | `group_neutralize` | `anl15_s_cal_fy2_6m_chg` | +0.30 | +21.8bp | 3.7% |
| 4 | 0.510 | `group_zscore` | `anl15_s_cal_fy2_6m_chg` | +0.29 | +21.6bp | 3.8% |
| 5 | 0.500 | `group_rank` | `anl15_gr_12_m_6m_chg` | +0.24 | +15.4bp | 3.9% |

### Stage3 — 三阶 trade_when (Top 5)

| # | \|S\| | 核心操作 | 字段 | Fit | Margin | Turnover |
|---|:---:|:--------:|:----:|:---:|:------:|:--------:|
| 1 | 0.620 | `open: ts_corr(close` | `anl15_s_cal_fy2_6m_chg` | +0.37 | +17.2bp | 5.1% |
| 2 | 0.590 | `open: ts_corr(close` | `anl15_s_cal_fy2_6m_chg` | +0.34 | +16.0bp | 5.2% |
| 3 | 0.590 | `open: ts_corr(close` | `anl15_s_cal_fy2_6m_chg` | +0.35 | +17.4bp | 4.9% |
| 4 | 0.580 | `open: ts_corr(close` | `anl15_s_cal_fy2_6m_chg` | +0.34 | +16.9bp | 5.0% |
| 5 | 0.580 | `open: ts_corr(close` | `anl15_s_cal_fy2_6m_chg` | +0.34 | +15.1bp | 5.9% |

## 4. 字段归因 (跨阶段字段稳定性)

| 字段 | Stage1 | Stage2 | Stage3 | 出现阶段数 | 评价 |
|------|:------:|:------:|:------:|:----------:|:----:|
| `anl15_gr_12_m_6m_chg` | 1 | 14 | 0 | 2 | 📊 多数阶段 |
| `anl15_gr_12_m_ests_dn` | 1 | 0 | 0 | 1 | 📄 单阶段 |
| `anl15_gr_12_m_ests_up` | 1 | 18 | 0 | 2 | 📊 多数阶段 |
| `anl15_gr_12_m_pe` | 1 | 0 | 0 | 1 | 📄 单阶段 |
| `anl15_gr_18_m_6m_chg` | 1 | 32 | 0 | 2 | 📊 多数阶段 |
| `anl15_gr_fy2_ests_dn` | 1 | 14 | 0 | 2 | 📊 多数阶段 |
| `anl15_gr_fy3_ests_dn` | 0 | 15 | 0 | 1 | 📄 单阶段 |
| `anl15_gr_fy3_ests_up` | 0 | 17 | 0 | 1 | 📄 单阶段 |
| `anl15_s_12_m_ests_up` | 1 | 0 | 0 | 1 | 📄 单阶段 |
| `anl15_s_cal_fy1_1m_chg` | 1 | 32 | 0 | 2 | 📊 多数阶段 |
| `anl15_s_cal_fy2_6m_chg` | 1 | 17 | 132 | 3 | 🔥 全阶段稳定 |
| `anl15_s_fy3_ests_dn` | 1 | 15 | 0 | 2 | 📊 多数阶段 |
| `anl15_s_ltg_cos_dn` | 0 | 18 | 0 | 1 | 📄 单阶段 |

## 5. 算子/事件归因

### Stage1 — 一阶原始

| 算子/操作 | 数量 | 占比 |
|----------|:----:|:----:|
| `winsorize` | 88 | 100% |

### Stage2 — 二阶 group_ops

| 算子/操作 | 数量 | 占比 |
|----------|:----:|:----:|
| `group_neutralize` | 86 | 35% |
| `group_zscore` | 83 | 33% |
| `group_rank` | 79 | 32% |

### Stage3 — 三阶 trade_when

| 算子/操作 | 数量 | 占比 |
|----------|:----:|:----:|
| `open: ts_corr(close` | 46 | 35% |
| `open: ts_arg_max(close` | 24 | 18% |
| `open: ts_arg_max(volume` | 12 | 9% |
| `open: ts_arg_min(volume` | 12 | 9% |
| `open: ts_std_dev(returns` | 12 | 9% |
| `open: ts_mean(volume` | 10 | 8% |
| `open: ts_zscore(returns` | 8 | 6% |
| `open: group_rank(ts_std_dev(returns` | 8 | 6% |

## 6. 持续入榜字段 (Persistent Top Tracker)

### Stage2 — 二阶 group_ops (15 份报告)

| 字段 | 出现率 | 趋势 |
|------|:------:|:----:|
| `anl15_s_cal_fy2_6m_chg` | 15/15 (100%) | ████████████ |
| `anl15_gr_12_m_6m_chg` | 11/15 (73%) | ████████░░░░ |
| `anl15_gr_12_m_pe` | 5/15 (33%) | ███░░░░░░░░░ |

### Stage3 — 三阶 trade_when (9 份报告)

| 字段 | 出现率 | 趋势 |
|------|:------:|:----:|
| `anl15_s_cal_fy2_6m_chg` | 9/9 (100%) | ████████████ |

## 7. 关键发现与未来挖掘策略

### 🔑 核心发现

1. **Sharpe 提升路径**: Stage1 Max=0.520 → Stage2=0.520 → Stage3=0.620 (总提升 +19%)
   - group_ops (二阶) 提升: +0%
   - trade_when (三阶) 提升: +19%
2. **最稳定字段**: `anl15_s_cal_fy2_6m_chg` — 在 15 份报告中 100% 入 Top10
3. **区域诊断**:
   - Amer: Stage3 MeanSharpe=+0.476 — ✅ 有效
   - Apac: Stage3 MeanSharpe=-0.039 — ❌ 系统性反向
   - Emea: Stage3 MeanSharpe=+0.366 — ✅ 有效
4. **提交差距**: 当前 Max|S|=0.620, 距 1.58 差 **0.96** (155%)

### 📋 未来挖掘策略 (Future Mining Strategy)

#### 策略 A: 深化当前信号链 (当前最优)

```
当前最优信号链:
  字段: anl15_s_cal_fy2_6m_chg
  一阶: winsorize(ts_backfill(field, 120), std=4)
  二阶: group_neutralize(...) / group_zscore(...)
  三阶: trade_when(ts_corr(close, volume, 20) > 0.3, ...)

可扩展方向:
  1. 测试不同 ts_backfill 窗口: 60/90/180/250 (当前=120)
  2. 测试不同 winsorize std: 2/3/5/6 (当前=4)
  3. 组合二阶+三阶: trade_when() 内嵌套 group_rank()
  4. 叠加 basic_ops: signed_power(zscore(rank(...)), 3)
```

#### 策略 B: 拓展字段池

```
当前仅使用 analyst15 (1个 dataset):
  - 已验证: anl15_s_cal_fy2_6m_chg (100%入Top)
  - 次优: anl15_gr_12_m_6m_chg (71%入Top)

推荐尝试的 dataset:
  1. analyst16 — 分析师评级 (与 anl15 互补)
  2. options — 期权隐含波动率/偏度
  3. fundamentals — 财务基本面
  4. price_volume — 量价信号
  5. short_interest — 做空数据
  6. institutional — 机构持仓变化
```

#### 策略 C: 拓展算子空间

```
当前算子:
  Stage1: zscore/rank/ts_zscore/ts_rank/...
  Stage2: group_neutralize/group_rank/group_zscore
  Stage3: trade_when (12 open events)

可拓展算子:
  - basic_ops: signed_power, quantile, normalize
  - ts_ops: ts_product, ts_quantile, ts_ir
  - 新增 trade_when open events:
    · ts_regression(volume, price, 20)
    · group_zscore(field, market) > 1.5
    · ts_delta(volume, 1) > 0 (放量)
    · ts_momentum(close, 20) > 0 (趋势)
```

#### 策略 D: 区域突破

```
当前 Apac 系统性反向 — 这是核心瓶颈:

方案1: 寻找 Apac 正向的 dataset
  - options/derivatives 在亚太可能更有效
  - fundamentals 在新兴市场有独特信号

方案2: 使用 country 级别分组代替 market
  - group_neutralize(field, country) 可能捕捉区域性信号

方案3: 分区域独立挖掘
  - 先做 Amer-only 提交 (如果允许)
  - 再独立探索 Apac/Emea 专属信号
```

#### 策略 E: 高阶组合

```
当 Max|S| 卡在 0.5~0.7 区间时, 考虑:

1. 双信号 blend:
   0.5 * trade_when(event1, field_A) + 0.5 * trade_when(event2, field_B)

2. 条件嵌套:
   trade_when(event1, trade_when(event2, field))

3. 时间窗口缩放:
   用 ts_backfill 的不同窗口做差分:
   ts_backfill(field, 60) - ts_backfill(field, 120)

4. 算子叠加:
   signed_power(zscore(rank(ts_zscore(field))), 3)
```

## 8. 提交检查清单 (Submission Readiness)

| 检查项 | 阈值 | Stage3 状态 | 通过? |
|--------|:----:|:-----------:|:-----:|
| |Sharpe| | ≥1.58 | 0.620 | ❌ |
| Fitness | ≥1.0 | 0.37 | ❌ |
| Turnover | [5%, 20%] | 5.1% | ✅ |
| Margin | >5bp | 17.2bp | ✅ |
| Return | >5% | 4.4% | ❌ |
| Drawdown | <Return | 10.1% | ⚠️ |

## 9. 运行状态

| 阶段 | 进度 | 有效结果 | Mean\|S\| | Max\|S\| |
|------|:----:|:--------:|:-------:|:------:|
| Stage1 — 一阶原始 | ✅ 完成 | 88 | 0.211 | 0.520 |
| Stage2 — 二阶 group_ops | 39/45 (87%) | 248 | 0.346 | 0.520 |
| Stage3 — 三阶 trade_when | 47/120 (39%) | 132 | 0.482 | 0.620 |
