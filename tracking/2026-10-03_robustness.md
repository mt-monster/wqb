# 2026-10-03 稳健性审计报告

## gJZ7AvZO — KOR / other466 / FUNDAMENTAL 塔

**表达式**
```
quantile(group_rank(ts_rank(group_rank(divide(oth466_is_ptx_inc_norm_q, oth466_bs_eq_tot_q), industry), 1008), market))
```

**设置** KOR / TOP600 / delay1 / STATISTICAL / decay4 / truncation 0.08
**提交判定链** Failed RA 0 · prod 0.6413 · self 0.4880 · checks.fail=[] → **稳健性 PASS**

---

## Phase B 归因

### B.0 WebDataScope failed-count 门
`is.checks.fail = []`（空）、`failed_ra_count = 0`、`failed_ppa_count = 0`、名单内无 PENDING → **通过**。
体检硬门已在 RA 步 5（`tools/wave_gate.py`，`--inspect-mode warn` + 显式 waiver）过闸。

### B.2 逐年 Sharpe（近窗制度：最近 3 个 IS 年为主判定）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 3.57 | 2.27 | 2.88 | 1.70 | 1.13 | 2.01 | 2.00 | 1.84 | 1.96 | 1.37 |
| Fitness | 3.92 | 2.12 | 2.79 | 1.19 | 0.69 | 1.71 | 1.76 | 1.48 | 1.53 | 1.00 |
| Drawdown | 1.6% | 4.8% | 2.1% | 2.4% | 2.9% | 4.1% | 2.9% | 4.9% | 2.1% | 6.4% |

**10 年全部为正，无一年亏损。** 最低年 2018 = 1.13（仍高于 1.0 平台线）。

**Recent-3yr（2021/2022/2023）= 1.84 / 1.96 / 1.37**
- 三年均值 **1.72 ≥ 1.58**（用户 2Y 线）✅
- 每年均 > 0.3（无平年）✅
- CV_Sharpe = 0.245 / 1.72 = **0.142** < 0.40 ✅
- max/min = 1.96 / 1.37 = **1.43** ≤ 3 ✅
- 衰减比 = 1.37 / 2.06 = **0.665** ≥ 0.50 ✅（无衰减告警）

### B.3 PnL 归因
- 曲线形态：单调上升，**无深度回撤、无横盘期**，季度 drawdown 全部 ≤ 6.4%
- `investability-constrained-pnl` 与主 PnL **全程同向** ⇒ 无投资容量瓶颈
- 换手 12.52% / margin 14.51bp ⇒ **margin @ turnover 远优于**「≥5bp」线（且 TVR 远低于 40% 阈值）
- Top-5 个股集中度：**未判**（逐股 PnL 端点不返回分解；持仓 319/319 分散度良好，无个股集中迹象）

### B.4 相关性
- prod **0.6413** < 0.70 ✅
- self **0.4880** < 0.70 ✅（最高相关 `zq87zzqO` 0.488，余量充足）
- 交互式双闸 `all_passed: true`

### B.5 相对池贡献（`EQUITY:KOR:1:POWER_POOL`）

| 指标 | before（池） | after（池+本） | Δ |
|---|---|---|---|
| Sharpe | 4.41 | **4.44** | **+0.03** |
| Fitness | 3.22 | **3.28** | **+0.06** |
| Turnover | 0.189 | 0.182 | −0.007 |
| Drawdown | 0.0156 | 0.0164 | +0.0008 |

**边际贡献为正**（Sharpe 与 fitness 双升），非稀释性加入。

---

## Phase C 反过拟合闸

| 检查项 | 值 | 阈值 | 判定 |
|---|---|---|---|
| WebDataScope failed count | 0 | = 0 | **PASS** |
| Recent-3yr Sharpe（主判定） | 1.72 均值 | ≥1.58 且每年>0.3 | **PASS** |
| Recent-3yr CV_Sharpe | 0.142 | < 0.40 | **PASS** |
| 衰减比 | 0.665 | ≥ 0.50 | **PASS** |
| 平年（最近 3 年） | 0 | = 0 | **PASS** |
| Recent-3yr max/min 比 | 1.43 | ≤ 3 | **PASS** |
| Sub-universe | PASS (1.41) | PASS | **PASS** |
| Margin @ turnover | 14.51bp @ 12.5% | ≥ 5bp | **PASS** |
| 经济可解释性 | 一句话可写 | — | **PASS** |
| 全历史早年疲软 | 2018 最低 1.13 | 绝不据此 REJECT | 软标记 |
| 算子数 | 4 | 软标记（REGULAR 不据此 REJECT） | 软标记 |
| Top-5 集中度 | 逐股 PnL 不可得 | — | 未判 |

### 判定：**PASS**（无 CONDITIONAL 软标记需带入提交描述）

---

## 方法论备注（本次审计最值得记录的一点）

本候选的突破**不是靠几何调整，而是靠等价算子替换**：

```
signed_power(group_rank(..., sector), 0.5)      2Y 1.51  prod 0.6544   ✗
  ↓ 换实现算子（数学含义不变）
quantile(group_rank(..., sector))                2Y 1.56  prod 0.6397   ✗ 差 0.02
  ↓ 换外层轴（quantile 包装下的最优轴与 signed_power 包装下相反）
quantile(group_rank(..., market))                2Y 1.62  prod 0.6413   ✓ 全闸通过
```

d7 曾判定该族「2Y 与 prod 在分组轴上反向搬运、不可能三角、已到天花板」。
**该结论被 d8/d10 推翻** —— 那个「三角」是 `signed_power` 实现路径造成的**假性约束**。

⇒ **纪律：任何「不可能 / 天花板 / 已到顶」的结论，必须附带「已扫等价算子替换」才成立。**
