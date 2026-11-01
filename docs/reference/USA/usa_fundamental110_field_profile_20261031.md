# fundamental110 字段画像（USA / TOP3000 / D1）

> 数据集：`fundamental110` — XBRL 财报**重述（restatement）**强度
> 画像日期：2026-10-31 ｜ 数据源：`get_datafields` 实时拉取（26 / 26 字段，`complete=true`）
> 平台指标：`field_count 26` / `alphaCount 141` / `multiplier 1.5` / `coverage 0.8214` / `category = FUNDAMENTAL`
> 关联波次：**wave304**（10 模板，批次 `2Lgz1o1u75hsbMQSHrFVfc8`）

---

## 1. 为什么选它：与既有 FUNDAMENTAL 机制正交

`fundamental3`（wave296–303 已挖尽）的机制是**财报水平 / 变化 / 加速度**；`fundamental110` 记录的是**同一会计科目被申报 → 再修订 → 再修订**的过程，即**会计信息质量**。

| 维度 | fundamental3 | fundamental110 |
|---|---|---|
| 信号对象 | 数值本身（营收、成本、EPS…） | **数值的修订历史**（初报值 vs 现报值、修订代次） |
| 经济学 | 盈利能力 / 成长 | **会计可信度 / 信息不对称 / 审计质量** |
| 文献先验 | — | Richardson et al. (2005) 应计可靠性；Palmer & Scholz (2013) 重述后漂移；Hennes & Leone (2008) 重述与 CEO 更替 |
| 类型 | MATRIX | **全 VECTOR（26/26）** |
| 拥挤度 | ac 75（主流字段 ac≤90，最热营收 ac 47 但 prod 0.84） | **ac 17–103，最冷 `revision_number` ac 17** |

⇒ 机制类别完全独立 ⇒ 理论上不与「加速度族」共享 prod 邻居。

---

## 2. 字段全清单（26）

### 2.1 五个信号字段（本波实际使用）

| 字段 | cov | ac | userCount | 语义 | 备注 |
|---|---|---|---|---|---|
| `fnd110_value` | 0.7676 | **52** | 32 | 该科目的**当前（含修订后）**美元值 | 与 original 配对使用 |
| `fnd110_original_value` | 0.7674 | **21** | 20 | **任何修订前**的原始申报值 | 冷门；作分母 |
| `fnd110_revision_number` | 0.7676 | **17** | 17 | 修订序列号：0=初报，>0=第 n 次修订 | **全库最冷**；修订强度直接代理 |
| `fnd110_preliminary` | 0.8883 | 24 | 21 | 是否为初步（未审计）版本 | 与 value 不同 cov（0.888 vs 0.768）|
| `fnd110_filing_type` | 0.8883 | 81 | 64 | 申报类型（10-K/10-Q/8-K…） | **本数据集最热**（ac 81），慎用 |

**重述幅度核心构造**：`subtract(vec_avg(fnd110_value), vec_avg(fnd110_original_value))`
- VECTOR 字段的数组维度 = 该股票当日**全部已申报科目/期间**的堆叠
- `vec_avg` 后相减 = **平均每科目修订额**（美元，带量纲）
- 逐项配对不可行（VECTOR 无法按 metric 对齐）⇒ **只能用聚合口径差**，这是本数据集的硬约束

### 2.2 七个元数据字段（非信号，勿当主信号）

| 字段 | cov | ac | 语义 |
|---|---|---|---|
| `fnd110_calendar_period` | 0.7676 | **103** | 日历季度（0=年度） |
| `fnd110_calendar_year` | 0.7676 | 40 | 日历年份 |
| `fnd110_fiscal_period` | 0.8883 | 45 | 财年季度（0=年度） |
| `fnd110_period_start` | 0.7676 | 37 | 财季起始日 |
| `fnd110_period_end` | 0.7676 | 40 | 财季结束日 |
| `fnd110_kic` | 0.8883 | 18 | 公司唯一识别码 |
| `fnd110_lrbx` | 0.8883 | 68 | XBRL 标签 |
| `fnd110_metric` | 0.8883 | 47 | 科目名 |

⚠ `calendar_period` ac=103 是本集**最热**字段 ⇒ 别用它当信号（已被做透）。`kic` 是 ID，`vec_avg` 无意义。

### 2.3 `_fast_d1` 双版本（13 个）

每个字段都有 `_fast_d1` 版（cov 高 0.1pp、ac 更低 22–51）。
**勿做 `_fast_d1` 与主版的差分** —— 同一数据的快速更新版，不是「预期 vs 实际」（本项目已踩过教训）。

---

## 3. 三条数据脾气（实测 / 结构推断）

### 3.1 覆盖呈「双档」而非连续
- 0.7676 档：`value` / `original_value` / `revision_number` / 期间与年份类（**8 个**）
- 0.8883 档：`preliminary` / `filing_type` / `metric` / `kic` / `lrbx`（**5 个**）

⇒ 两档相差 12pp。0.7676 档对应「有具体科目数值」的股票；0.8883 档只要申报过就有。做**除法**时（value / original_value）交集 = 0.767 档，**长仓数会被压在 ~1500 量级**。

### 3.2 稀疏字段 ⇒ `ts_backfill` 是必需项，不是可选项
本集所有信号字段 cov < 0.79 ⇒ 按本项目铁律（cov < 0.9 必须 `ts_backfill(x, 120~250)`）。wave304 全 10 条模板均带 `ts_backfill(..., 120)`。
**缺 backfill 的症状**：换手虚高（18%+）、margin 低、S 被 NaN 稀释。

### 3.3 带量纲 ⇒ 禁与常数相加/比较
`value` / `original_value` 是美元值。本项目已 4 次踩到 `add(x, ε)` / `max(x, 1)` 触发 UNITS 硬错。
⇒ 做除法保护须**先 zscore 化掉量纲**，或改用 `ratio-of-means`（`divide(ts_mean(diff), ts_mean(abs(original)))`，模板 R9 即此设计）。

---

## 4. 十个结构互异模板（wave304 全量）

结构差异维度：**矩**（水平 / 一阶差分 / 二阶矩 / 窗口差）× **几何**（`ts_zscore` / `ts_rank` / `ratio-of-means`）× **聚合**（`vec_avg` / `vec_sum` / `vec_range`）× **分组轴**（subindustry）× **符号先验**。

| # | 名称 | 机制 | 核心骨架 |
|---|---|---|---|
| R1 | 重述幅度水平 | 一阶矩·水平 | `ts_backfill(vec_avg(value) - vec_avg(original), 120)` → `ts_zscore(252)` |
| R2 | 相对修正幅度 | 无量纲比率 | `divide(diff, vec_avg(original))` |
| R3 | 修订代次水平 | 不同聚合口径 | `vec_avg(revision_number)` |
| R4 | 未审计占比 | 会计可信度水平 | `vec_avg(preliminary)` |
| R5 | 重述加速度 | **窗口差 252−504** | `subtract(ts_mean(diff,252), ts_mean(diff,504))` |
| R6 | 重述波动率 | **二阶矩** | `ts_std_dev(diff, 252)` |
| R7 | 修订频率变化 | **一阶差分** | `ts_delta(vec_avg(revision_number), 252)` |
| R8 | 申报口径离散度 | **vec_range** | `vec_range(filing_type)` |
| R9 | 相对严重度 | **ratio-of-means** | `divide(ts_mean(diff,252), ts_mean(abs(vec_avg(original)),252))` |
| R10 | 相对幅度 + 序数化 | **非线性 ts_rank** | R2 外层加 `ts_rank(..., 252)` |

外层统一：`multiply(-1, group_rank(<inner>, subindustry))`
- `group_rank`：财报/事件族**必须序数化**（`group_zscore` / `group_scale` / `group_neutralize` / `ts_quantile` 在本项目实测全灭）
- `multiply(-1, ...)`：文献先验 —— 重述强度高 = 会计质量差 ⇒ 未来跑输 ⇒ 取负
- `negate` 算子不可用，只能 `multiply(-1, ...)`

### 4.1 模板来源与验证
- **机制启发**：`search_forum_posts`（XBRL / restatement / revision 关键词）+ 上述三篇文献的因子定义方向。
- **结构来源**：R1/R2/R9 取自财报质量族常见「修正额 / 修正率」定义；R5/R7 源自本项目已验证的「加速度骨架」（`ts_mean(Ws) − ts_mean(Wl)`，wave297–300 最大突破）；R6 源自「二阶矩 = 不确定性」；R8/R10 为本波自建。
- **符号先验未在 USA 本数据集验证过** ⇒ 若 10 条全灭且最佳为负 S，下一步做一次性符号翻转诊断（只翻 TOP2–3，不整批翻）。

---

## 5. 闸线速查（USA / D1）

| 闸 | 线 |
|---|---|
| `LOW_SHARPE` | 1.58 |
| `LOW_FITNESS` | 1.00 |
| `LOW_2Y_SHARPE` | 1.58 |
| `LOW_SUB_UNIVERSE_SHARPE` | **0.435 × S**（随 S 浮动） |
| `HIGH_TURNOVER` | 0.70 |
| `CONCENTRATED_WEIGHT` | 0.10 |
| prod / self 相关 | < 0.70（严格不等） |

`fitness ≈ S × √(returns / max(TO, 0.125))` ⇒ 若 TO < 12.5%（事件型字段极可能），分母恒取 0.125 地板 ⇒ **提换手无法提 fitness**，只能提 S 或提 returns。

---

## 6. 未开发靶子（本波之外）

| 靶子 | 机制 | 为什么没进本波 |
|---|---|---|
| `vec_avg(metric)` 多样性 | 科目组成广度 | metric 是类别标识，`vec_avg` 语义弱，`vec_range` 已用（R8）|
| `fnd110_lrbx` | XBRL 标签一致性 | 同上，属元数据 |
| `period_end − period_start` | 报告期长度异常 | 日期型 VECTOR 相减后单位不明，UNITS 风险高 |
| `_fast_d1` 版单独建模 | 快速更新路径 | 与主版近重复（互相关会 ≈1），不产出独立候选 |
| 重述 × 申报类型交互 | 条件型（在 10-K 内看重述） | 需 `trade_when` / 条件算子，留给下一波 |

---

## 7. 平移指引（给其它区域 / 其它 XBRL 数据集）

1. **VECTOR 必须 `vec_*` 聚合才能进 `ts_*`** —— `vec_avg` / `vec_sum` / `vec_range` 可用；`vec_median` 不存在。
2. **逐项配对不可行** ⇒ 只能用聚合口径差（`vec_avg(A) − vec_avg(B)`）。想要「同科目内修订幅度」必须平台提供按 metric 分组的算子，本集没有。
3. **两档覆盖决定长仓数**：做除法/乘法时交集 = 低覆盖档 ⇒ 长仓数 ≈ 1500，`CONCENTRATED_WEIGHT` 与 `SUB` 会变脆。
4. **符号必须逐区验**：本项目已在 GBR 实测「美股文献方向 ≠ 本地实测方向」（借券费率、网站关注度均反向）。USA 本集按文献取负，其它区先按本区先验跑一组再看。
