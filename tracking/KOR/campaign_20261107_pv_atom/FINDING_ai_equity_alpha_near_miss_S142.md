# ai_equity_alpha 开荒：dividend_policy_analysis_3 近线候选 S1.42（2026-11-07）

数据集：`ai_equity_alpha`（model · **582 VECTOR 字段** · coverage **1.0** · alphaCount 53 · userCount 21）。
字段族约 60 个（会计舞弊 / 盈余质量 / 股东回报 / 股利政策 / 回购 / 信息不透明 / 市场热度 / 内在价值 / 资金流 / 相关性风险 …）。

## 1. 三轮族扫描（共 40 条，P69/P71/P75）

统一几何 `subtract(0.5, group_rank(ts_mean(vec_avg(F),22),sector))`，读数为该几何下的 S：

| 字段族 | S | 2Y | 说明 |
|---|---:|---:|---|
| **fund_flow_prediction_metric** | **−1.48** | −1.24 | 镜像后 1.28；全场最强单族 |
| combined_technical_indicators | −1.22 | −1.16 | 镜像 1.22 |
| company_size_factor | −1.22 | −1.69 | 镜像 1.22（规模壳） |
| accruals_contribution_score | −1.17 | −0.54 | 镜像 1.17 |
| cashflow_trend_analysis | −1.20 | −1.30 | 镜像 1.20 |
| shareholder_yield_metric | −1.02 | −1.56 | 镜像 1.02 |
| dividend_policy_analysis | −1.00 | −1.85 | 镜像 1.00 |
| information_opacity_score | +0.71 | **+1.59** | 唯一正向过 2Y |
| 其余 12 族 | \|S\|≤0.93 | | 含 buzz / accounting_forensics / earnings_quality / analyst_opinion |

**结论：几乎全族落在 0.7–1.3 区间**；单族最强 fund_flow 换多种几何后最高 1.32。

## 2. 突破点：dividend_policy_analysis_3

`dividend_policy_analysis` 族 8 个变体中**只有 `_3` 有信号**（其余 7 个 0.00–0.85，P80/P81 已证）。
精修后最优（P76/P82 一致）：

```text
subtract(group_rank(ts_mean(vec_avg(dividend_policy_analysis_3), 44), industry), 0.5)
设置：KOR/TOP600/D1 · REVERSION_AND_MOMENTUM · decay 4 · trunc 0.03~0.08 · 2014-2023
```

| 指标 | 读数 | 门槛 | 状态 |
|---|---:|---:|---|
| Sharpe | **1.42** | ≥1.58 | ✗ 差 0.16 |
| Fitness | **1.05** | ≥1.0 | ✓ |
| 2Y Sharpe | **1.98** | ≥1.58 | ✓ |
| Turnover | 0.1052 | | ✓ |
| raF | **1（仅 LOW_SHARPE）** | 0 | 唯一失败项 |

## 3. 已穷尽的杠杆（S 稳定 1.42，纹丝不动）

| 杠杆 | 结果 |
|---|---|
| 窗口 28–66（步长 2–4） | S 1.19–1.42，峰值 W44 |
| 分组轴 sector / industry / subindustry / market | industry 最优；subindustry 崩到 1.13 |
| decay 4 / 8 / 12 / 16 | 4 与 12 同峰 1.42；16 降到 1.40 |
| truncation 0.03 / 0.05 / 0.06 / 0.08 | **完全无差异**（未触截断上限） |
| 中性化 REVERSION_AND_MOMENTUM / STATISTICAL | STATISTICAL 崩到 0.5–0.78（2Y 保持 1.6） |
| 字段变体 _2/_4/_5/_6/_7/_8 | 0.00–0.85（`_3` 独苗） |
| signed_power 1.2/1.3/1.5/1.8 | 1.40/1.39/1.37/1.33（越高越差） |
| winsorize std 2/2.5/3 | 与裸式逐位相同 |
| group_scale | 1.42（无增益） |
| 双层 ts_mean(5,44) | 1.37（更差） |
| 全市场 rank 替代 group_rank | 1.19（更差） |

⇒ **该字段的 Sharpe 上限约 1.42，属结构性上限，不是参数问题。**

## 4. 判定

**近线候选（park）**：S 1.42 / F 1.05 / 2Y 1.98 / raF 1（仅 LOW_SHARPE）。
除 Sharpe 外全闸通过，是 KOR 本轮除已交付 4 颗外**最接近可提交线的一条**。
要过线需要 +0.16 Sharpe，现有算子杠杆已全部耗尽 → 要么换数据集，要么接受不可提交。

## 5. 同批其他数据集的判定

- `quant_factor_lib`（Cassie 信用风险库，32 字段）：**死**，最高 |S| 0.74、TO 0.05。
- `price_signal_dl`（28 趋势/量能指标）：**降级**，字段可仿真但裸用最强仅 S 0.40；且 `ts_backfill` + 该数据集会整批失败。
- `continuation_score`（560 图表形态相似度，cov 1.0）：**弱**，10 个代表形态最高 S 0.94（cup_handle 中位相似度），多数 0.1–0.6。