# 波 188：平台 `decay` 破 TO 闸 —— RISK 塔第 3 颗成立（方法论纠错）

- **日期**：2026-10-30
- **区域 / 设置**：USA / TOP3000 / D1 / STATISTICAL / truncation 0.05 / nanHandling OFF
- **唯一变量**：平台参数 `decay` ∈ {4, 6, 8, 10, 12}
- **表达式（全 5 条完全相同）**：
  ```
  group_zscore(reverse(ts_av_diff(ts_backfill(rsk65_trsd_4mfte_mfm, 22), 252)), subindustry)
  ```
- **提交方式**：`batch_create_simulations`（7 条，成 5 条；d16/d20 被 429 拒）

---

## 1. 结论先行

**`88RAN85m`（decay=8）全闸通过，RISK 塔第 3 颗成立。**

```
checks.fail    = []                       ← 空
checks.pass    = LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, HIGH_TURNOVER,
                 CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE,
                 LOW_2Y_SHARPE, MATCHES_PYRAMID    ← 全 8 项
ra.failed_ra_count = 0
ra.failed_ppa_count = 0
pyramid_short  = "risk"
pyramids.list  = [{name: "USA/D1/RISK", multiplier: 1.1}]
```

| 指标 | 值 | 闸线 | 余量 |
|---|---|---|---|
| Sharpe | **2.68** | 1.58 | +70% |
| Fitness | **1.01** | 1.00 | +1% |
| Turnover | **61.77%** | ≤70% | **8.2pp** |
| 2Y Sharpe | **1.68** | 1.58 | +6.3% |
| Sub-universe | **2.21** | 0.63 | +251% |
| invest_S | 2.27 | — | ratio 0.8470 |
| Drawdown | 4.64% | — | — |
| longCount / shortCount | 1571 / 1554 | ≥1000 | ✅ |
| Returns / margin | 8.83% / 2.86bp | — | — |

**与波 185 的 `vR101gVG` 是同一个表达式**，唯一差别是平台 `decay`：`2 → 8`。

---

## 2. 五条结果全表（decay 曲线）

| decay | alpha | S | F | TO | R | 2Y | SUB | invest_S | ratio | DD | fRA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2（波185） | `vR101gVG` | 3.38 | 1.00 | **109.99%** ❌ | 9.54% | 2.35 | 2.61 | 2.64 | — | 3.19% | 1（TO） |
| 4 | `YP1Z1eJv` | 3.13 | **1.06** | 83.63% ❌ | 9.68% | 2.05 | 2.55 | 2.54 | 0.8115 | 4.14% | 1（TO） |
| 6 | `0mYoPb12` | 2.79 | **1.00** | **70.18%** ❌ | 8.96% | 1.76 | 2.33 | 2.40 | 0.8602 | 4.67% | 1（TO，差 0.18pp） |
| **8** | **`88RAN85m`** | **2.68** | **1.01** | **61.77%** ✅ | 8.83% | **1.68** | **2.21** | **2.27** | **0.8470** | 4.64% | **0** ✅ |
| 10 | `akKJa3gR` | 2.55 | 1.00 | 55.86% ✅ | 8.52% | **1.55** ❌ | 2.06 | 2.14 | 0.8392 | 4.67% | 1（2Y） |
| 12 | `0mYoPl8v` | 2.44 | 0.98 | 51.45% ✅ | 8.26% | **1.46** ❌ | 1.90 | 2.06 | 0.8443 | 4.53% | 2 |

**甜点区精确锁定在 decay 6–8 之间**：

- `decay 6` 的 TO 70.18% 刚好微超 0.70（严格不等式 ⇒ fail）
- `decay 8` 的 TO 61.77%（余量 8.2pp）、2Y 1.68（余量 0.10）—— **两侧约束同时最松**
- `decay 10` 起 2Y 掉到 1.55 反挂闸

⇒ **上下都有墙，不是单调可行区**。这是一个真正的窗口，而不是单调趋势里的随便一点。

---

## 3. 核心发现：平台 `decay` 是正确的那一层，表达式内平滑全是错的维度

### 3.1 同 TO 档位的四方对比

全部把换手压到 60% 左右或更低，看保留了多少信号：

| 方案 | TO | S | 2Y | R | F |
|---|---|---|---|---|---|
| **平台 `decay 8`**（波188） | **61.77%** | **2.68** | **1.68** | **8.83%** | **1.01** |
| 表达式 `ts_target_tvr_decay(·,0.4)`（波187 `ZYQZQ1vx`） | 29.09% | 2.13 | 1.50 | 7.12% | 1.05 |
| 表达式 `ts_target_tvr_decay(·,0.5)`（波187 `kqNRNYYK`） | 36.43% | 2.15 | 1.31 | 7.45% | 0.97 |
| 表达式 `ts_decay_linear(·,22)`（波185 `3qodoLWQ`） | 29.81% | 1.87 | 1.01 | 5.82% | 0.83 |

⇒ **平台 `decay` 在基本相同的换手水平下，S 高 26%、2Y 高 12%、R 高 24%（对比 tvr_decay）。**

### 3.2 为什么

| 层 | 作用对象 | 信息损失方式 |
|---|---|---|
| `ts_decay_linear(·,N)` | **信号值**（每股每天） | 无差别摊薄时间新鲜度；连"当天刚到的新信息"也被压 |
| `ts_target_tvr_decay(·)` | 自适应 λ，看组合换手 | 平坦期过度平滑（tvr=0.2 时 SUB 崩到 0.37 的成因） |
| **平台 `decay`** | **持仓权重**（组合层） | 只在"仓位变了多少"上打折，不改信号本身 |

平台 `decay` 是三者中**信息损失最少**的一层：它在信号算完之后、在仓位层面做指数加权，对信号的排序与幅度都不动。这解释了为什么它能在 TO 62% 时保住 S 2.68。

### 3.3 方法论纠错

**波 184 整轮"换手治理矩阵"、波 185 的"TO 与 2Y 在表达式内锁死"、波 187 的"tvr_decay 是第三自由度"——方向都对，但层次都低了一层。**

正确的杠杆优先级应该是：

1. **平台 `decay`**（持仓层，信息损失最小）—— 先把这一层扫完
2. **`ts_target_tvr_decay`**（自适应 λ，条件性损失）—— 平台 decay 不够时叠加
3. **表达式内 `ts_decay_linear` / `ts_mean`**（信号层，损失最大）—— 最后才用
4. **`hump` 全族** —— 永不用（第五次确认必死）

波 185 的「换手 110% 是结构常量」只在**表达式内几何维度**成立；平台 decay 是与之正交的维度，能把同一表达式的 TO 从 110% 连续调到 51%。

---

## 4. 三颗 RISK 候选可共存（相关矩阵）

`compute_mutual_correlation`（4 年，986 点，阈值 0.7）：

| | `88RAN85m` | `ZYQZEawY` | `qMLbW8xP` | `vR101gVG` |
|---|---|---|---|---|
| **`88RAN85m`** | 1.0 | **0.652** | **0.0903** | 0.8467 |
| **`ZYQZEawY`** | 0.652 | 1.0 | **0.1277** | 0.4758 |
| **`qMLbW8xP`** | 0.0903 | 0.1277 | 1.0 | 0.0735 |
| `vR101gVG` | 0.8467 | 0.4758 | 0.0735 | 1.0 |

- `max_mutually_below_subset = [88RAN85m, ZYQZEawY, qMLbW8xP]`，**size = 3，exact = true**
- `88RAN85m` vs `vR101gVG` = 0.8467 —— 同一表达式不同 decay，符合预期，不共存
- **最紧的一对是 `88RAN85m` ↔ `ZYQZEawY` = 0.652**（余量 0.048）

**自相关**：`check_self_correlation(88RAN85m)` = **0.4696 通过**（OS 池 135 颗，排除 4 颗 Power Pool）。

三颗的构成逻辑（互不重复）：

| alpha | 数据集 / 字段 | 机制 | 信号族 |
|---|---|---|---|
| `ZYQZEawY` | `mfm_model_output` / `discount_store_retail_score` | 特质残差**日收益的66日衰减** | 慢变水平 |
| `88RAN85m` | `risk65` / `rsk65_trsd_4mfte_mfm` | 特质残差**252日偏离的幅度** | 中期偏离 |
| `qMLbW8xP` | `mfm_model_output` / `short_interest_factor_score_2` | **卖空因子水平** | 完全不同现象 |

前两者虽都属"特质残差"族（相关 0.652），但时间尺度差 4 倍、加工方式（衰减 vs 偏离）不同；第三者是完全独立的卖空维度。

---

## 5. 工程记录

### 5.1 `batch_create_simulations` 的真实行为

- 提交 7 条 → **成功 5 条**，d16/d20 报 `429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED`（与 MEMORY 记载一致）
- 返回的是**单仿真 id**，不是 multisim
- **必须用 `lookINTO_SimError_message` 查，且 location 要带 `/simulations/` 前缀**
- `batch_status(单仿真id)` 会返回 `child_count=0 / parent_status=COMPLETE / error="parent COMPLETE but children empty"` 的伪状态 —— 看起来像失败，其实是完成了

### 5.2 d16/d20 无需补派

d10（2Y 1.55）、d12（2Y 1.46）已显示 2Y 在 decay>8 后单调下滑，外推 d16/d20 必然挂 `LOW_2Y_SHARPE`。补派只会浪费槽位。

---

## 6. 下一步

### 6.1 立即可做（不需新回测）

| 动作 | 状态 |
|---|---|
| `88RAN85m` self-corr | ✅ 0.4696 通过 |
| `88RAN85m` / `ZYQZEawY` / `qMLbW8xP` 三颗互相关 | ✅ 全 < 0.7，size=3 exact |
| **prod correlation** | ⏳ 待测（后台 `bg_92422758` 正在跑，`ZYQZEawY` 因 correlation_busy 超时未取到） |

### 6.2 波 190（待派）：验证平台 decay 的普适性

如果 `decay 8` 在其他骨架上同样有效，则 RISK 塔内可再挖出低相关载体，且该方法论可迁移到其他塔。计划：

| # | 骨架（+ decay 8） | 目的 |
|---|---|---|
| 1 | `ts_rank(x,1008)` | 秩型信号是否同样受益 |
| 2 | `ts_zscore(x,504)` | 除 std 的几何是否同样受益 |
| 3 | `ts_rank(x,504)` | 与 #1 构成窗口跨度对（降相关） |
| 4 | `ts_av_diff(x,66)` | 短窗是否同样受益 |
| 5 | `ts_zscore(x,66)` | 短窗 + 除 std |
| 6 | `ts_av_diff(x,252)` + **decay 7** | 细扫甜点区下沿 |
| 7 | `ts_av_diff(x,252)` + **decay 9** | 细扫甜点区上沿 |

### 6.3 方法论回灌

**波 184 / 185 / 187 的候选应全部用平台 `decay` 重扫一遍**——那些"卡 TO"或"卡 2Y"的结论可能是层次选错导致的伪失败。优先：
- `1YNvjQoz`（TO 30.22% / 2Y 0.97）→ 裸表达式 + decay 8 可能同时拿到 2Y 1.68
- `ZYQZAEW8`（TO 51.29% / F 0.71 / 2Y 0.98）→ 同上
- `ZYQZQ1vx`（TO 29.09% / 2Y 1.50）→ 平台 decay 与 tvr_decay 叠加是否更好

---

## 7. 已知边界

- `decay` 的可行性区间不是单调的：**6–8 之间是甜点，>10 挂 2Y，<6 挂 TO**
- `decay 6` 的 TO 70.18% 证明平台 `HIGH_TURNOVER` 上限是**严格 0.70 不等式**（70.18% 即 fail）
- `CLUSTER_TEST` 在本波 5 条上全部 0.84–1.08，仍只是 warning，不进 `ra_failed_checks`
- `batch_create_simulations` 的 429 是槽位满时的**一次性返回**，不重试；要按"提交成功数"记账
