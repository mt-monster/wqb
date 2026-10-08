# ANALYST category 字段深挖 · 2026-10-07

> **锁定 category = `analyst`**，把 6 个数据集的字段全部展开分类。
> 总量：**632 个高覆盖字段**，分 **14 个字段集**。

---

## 〇 数据集构成

| 数据集 | 字段 | 高覆盖 | 类型 | 角色 |
|---|---:|---:|---|---|
| `analyst7` | 608 | **425** | MATRIX | 最大池（**41% 是计数类**，见 §2） |
| `analyst_factor_signals` | 108 | **49** | MATRIX | **主力**（含唯一有产出的字段） |
| `analyst93` | 100 | **100** | **全 VECTOR** | 分析师技能元数据 |
| `analyst9` | 51 | 20 | — | 换手爆表 |
| `analyst44` | 72 | **48** | VECTOR | 换手爆表 |
| `analyst48` | 7 | **7** | VECTOR | 索引元数据 |
| `analyst47` | 5 | **1** | MATRIX | 单指标 |

---

## 一 ★ `analyst_factor_signals`（49 个高覆盖字段，**逐字段全列**）

### 1.1 字段集 A-1「预期变化率」（**唯一有效**）✅

| 字段 | cov | 结果 |
|---|---:|---|
| **`eps_y1_estimate_change_3mo`** | 0.9234 | ✅ **S1.65 / F1.47 / 0失败 → `9qWX78vV`** |
| `eps_y2_estimate_change_3mo` | 0.9234 | ❌ S1.35 |
| `netprofit_y1_estimate_change_3mo` | 0.9207 | ❌ S1.32 |
| `netprofit_y2_estimate_change_3mo` | 0.9208 | ❌ S1.16 |
| `revenue_y1_estimate_change_3mo` | 0.9222 | ❌ S0.48 |
| `revenue_y2_estimate_change_3mo` | 0.9221 | ❌ S0.58 |
| `revenue_q1_estimate_change_1mo` | 0.6371 | ❓ 未单独测 |

**⇒ 7 个字段里只有 1 个成立。**

### 1.2 字段集 A-2「修正幅度」❌（3 个）

| 字段 | cov | 最好 S |
|---|---:|---:|
| `eps_revision_magnitude` | **0.9233** | 0.78 |
| `netprofit_revision_magnitude` | 0.9207 | — |
| `revenue_revision_magnitude` | 0.9222 | — |

### 1.3 字段集 A-3「分歧度」（**16 个，最大类**）❌

| 子类 | 字段 |
|---|---|
| **偏度 skewness**（7） | `eps_q1_estimate_skewness`(0.6462) · `eps_q2_estimate_skewness`(0.6462) · `eps_y1_estimate_skewness`(**0.9277**) · `netprofit_q1_...`(0.6277) · `netprofit_q2_...`(0.6276) · `netprofit_y1_estimate_skewness_alt`(0.9255) · `revenue_q1_...`(0.7222) · `revenue_q2_...`(0.7221) · `revenue_y1_estimate_skewness`(**0.927**) |
| **不对称 asymmetry**（3） | `eps_y1_estimate_asymmetry`(0.892) · `netprofit_y1_estimate_asymmetry`(0.8864) · `revenue_y1_estimate_asymmetry`(0.8892) |
| **变异系数 coeff_var**（4） | `eps_y1_estimate_coeff_var`(0.892) · `eps_y2_...`(0.8929) · `netprofit_y2_...`(0.887) · `revenue_y1_...`(0.8892) · `revenue_y2_...`(0.8896) |
| 波动调整 | `netprofit_y1_estimate_volatility_adj_1yr`(0.8864) |

**⇒ 全部按"收敛变化"构造（`subtract(ts_mean(22), ts_mean(252))`）后 ≈ 0。**
**★ 这是本会话最有说服力的否证**：最大字段类、有研报依据（《分析师预测分歧度：从一致预期的收敛中寻找 Alpha》）、机制匹配正确 —— **仍然全灭**。

### 1.4 字段集 A-4「共识水平」❌（6 个）

`eps_y1_consensus_value`(0.8932) · `eps_y2_...`(0.9277) · `netprofit_y1_...`(0.8904) · `netprofit_y2_...`(0.9255) · `revenue_y1_...`(0.8907) · `revenue_y2_...`(0.927)
构造 `ts_av_diff(bf, 252)` → **S<0**。

### 1.5 字段集 A-5「增长 CAGR」❌（9 个）

`eps_y1_cagr_{2,3,4}yr`（0.7994/0.7085/0.6266）· `netprofit_y1_cagr_2yr_alt`/`_3yr`/`_4yr`（0.7949/0.7036/0.6215）· `revenue_y1_cagr_{2,3,4}yr`（0.7954/0.704/0.621）
水平形 → **S0.31**。

### 1.6 字段集 A-6「趋势斜率」❌（3 个）

`eps_estimate_trend_slope_1yr`(0.6463) · `netprofit_estimate_trend_slope_1yr`(0.6279) · `revenue_estimate_trend_slope_1yr`(0.7222) → **S0.22**。

### 1.7 字段集 A-7「季度环比增长」❓（3 个）

`eps_q2_estimate_qoq_growth`(0.6462) · `netprofit_q2_...`(0.6277) · `revenue_q2_...`(0.7222) → **未单独测**（与 A-1 同属"变化"语义，**优先级高**）。

---

## 二 ★ `analyst7`（425 个高覆盖字段）—— **41% 是计数类**

### 2.1 交叉表：19 个指标 × 20+ 个统计

**指标维度**（19 种）：
`net`(37) · `dps`(36) · `ebt`(36) · `pre`(27) · `ebi`(27) · `sal`(27) · `gps`(26) · `bps`(26) · `cps`(23) · `ent`(23) · `nav`(23) · `roa`(22) · `opr`(14) · `grm`(14) · `tbv`(10) · `ndt`(10) · `prr`(10) · `ner`(10) · `csh`(10)

**统计维度**（20+ 种）：
| 统计 | 字段数 | 语义 | 判定 |
|---|---:|---|---|
| **`num`** | **44** | 有预估的分析师**数量** | ❌ 计数 |
| **`lowerednum`** | **44** | 下修人数 | ❌ 计数 |
| **`raisednum`** | **44** | 上修人数 | ❌ 计数 |
| **`num_4wks_ago`** | **22** | 4 周前的数量 | ❌ 计数 |
| **`num_3mth_ago`** | **22** | 3 月前的数量 | ❌ 计数 |
| `mean` | 25 | 均值（**水平**） | ❌ 水平 |
| `raised` / `lowered` | 22×2 | 上/下修（1 周内？） | ❌ 计数 |
| `high` / `median` / `low` | 14×3 | 高/中/低估值 | ❌ 水平 |
| `std` | 12 | 标准差（**分歧**） | ❌ 分歧 |
| `{mean,median,low,high,num}_{3mth,4wks}_ago` | ~12×4 | 历史快照 | ❌ |

**★★ 关键量化**：`*num*` 类共 **44+44+44+22+22 = 176 个（占 425 的 41%）** —— **全部是计数类 ⇒ 全部属于「2Y 有 S 无」的判死形态**。

### 2.2 子集分类与优先级

| 子集 | 字段数 | 状态 | 说明 |
|---|---:|---|---|
| **计数类**（`*num*` / `*raised*` / `*lowered*`） | **176** | ❌ | 41%，判死形态 |
| 水平类（`*_mean` / `*_median` / `*_high` / `*_low`） | ~67 | ❌ | 最好 S0.99（`est_12m_ebi_mean`） |
| 分歧类（`*_std`） | 12 | ❌ | 未测；但同 category 的 A-3 分歧度已全灭 |
| 历史快照（`*_3mth_ago` / `*_4wks_ago`） | ~170 | ❓ | **未测** —— 可做「预期的时间变化」（快照间差分）！ |

**★ 唯一有希望的方向**：`*_{3mth,4wks}_ago` 与当前值的**差分**（= 另一种"变化率"构造，与 A-1 同机制）。
成本低（在已有字段上取差），且 A-1 已证明该机制在本 category 有效。

---

## 三 `analyst93`（100 个，**全 VECTOR**，7 个族）

| 族 | 字段数 | 换手 | 状态 | 说明 |
|---|---:|---|---|---|
| **`recprofitabilityprev`** | **28** | **0.0795** ✅正常 | ⚠️ **活的族** | `anl93_recprofitabilityprev_{analyst,estimator}_{analyst,profitability1,profitability2,...}`，历史单信号 **S1.30（n=19）** |
| `profitabilityprev` | 28 | 0.0792 | ⚠️ | 历史单信号 S1.06 |
| `analyst` | 18 | 0.0286 | ❌ | 静态（换手 0.019~0.029） |
| `estimator` | 18 | 0.0284 | ❌ | 静态 |
| `consistency` | 4 | — | ❌ | 静态 |
| `correv` | 2 | — | ❌ | 静态 |
| `accuracy` | 2 | 0.0237 | ❌ | 静态 |

**★★ 修正**：`analyst93` **不是整体死的** —— `recprofitabilityprev` / `profitabilityprev` 两族（56 个字段）**换手 0.079~0.080（正常）**，历史单信号 S1.06~1.30。
我上一轮只测了 4 个静态族（`accuracy/consistency/correv/estimator`）就下了全局结论 —— **这是越界**。

**★ 机制含义**：`recprofitabilityprev_*` = **"上一期推荐该股的、之后被证明盈利的分析师"** —— 是**前瞻性分析师质量**（不是历史准确率）。

---

## 四 其他数据集

| 数据集 | 字段集 | 状态 |
|---|---|---|
| `analyst44`（48） | `anl44_2_{eps,roe,bps,tbvps}_value` | 🚫 **换手 1.64 爆表** |
| `analyst9`（20） | `anl9_consensusv2span_*`、`anl9_{s_numup,daily_numup}` | 🚫 **换手 0.73~1.47 爆表** |
| `analyst48`（7） | `anl48_bulk_*`、`anl48_index_bulk_*` | ❓ 索引元数据，疑似无信号 |
| `analyst47`（1） | `anl47_indicator` | ❓ |

---

## 五 analyst category 总账与下一步

| 字段集 | 字段数 | 状态 |
|---|---:|---|
| A-1 预期变化率 | 7 | ✅ **1 颗就绪** |
| A-2 修正幅度 | 3 | ❌ |
| **A-3 分歧度** | **16** | ❌（最有说服力的否证） |
| A-4 共识水平 | 6 | ❌ |
| A-5 增长 CAGR | 9 | ❌ |
| A-6 趋势斜率 | 3 | ❌ |
| A-7 季度环比增长 | 3 | ❓ **未测** |
| **A-8 analyst7 计数类** | **176** | ❌ 41% 判死形态 |
| A-8b analyst7 水平/分歧类 | ~79 | ❌ |
| **A-8c analyst7 历史快照类** | **~170** | ❓ **未测**（可做快照间差分） |
| **A-9 analyst93 技能元数据** | 40 | ❌ 静态 |
| **A-10 analyst93 recprofitability/profitabilityprev** | **56** | ⚠️ **活的族，未深挖** |
| A-11 analyst44 价值 | 48 | 🚫 换手爆表 |
| A-12 analyst9 | 20 | 🚫 换手爆表 |
| A-13 analyst48 | 7 | ❓ |
| A-14 analyst47 | 1 | ❓ |

### ⇒ analyst category 的下一步（按性价比）

| 优先 | 动作 | 成本 | 依据 |
|---|---|---|---|
| **1** | **深挖 A-10**：`recprofitabilityprev_*` / `profitabilityprev_*`（56 个 VECTOR 字段） | 先搜 `vec_*`（1 批）+ 轴深/窗长（2~3 批） | 换手正常 + 历史单信号 S1.06~1.30 ⇒ **已确认是活的族** |
| **2** | **A-8c 历史快照差分**：`est_12m_<指标>_{mean,median,high,low}_{3mth,4wks}_ago` 与当前值取差（≈170 字段可组合） | 1 批 | **与 A-1 同机制**（"变化率"），而 A-1 是本 category 唯一有效的机制 |
| **3** | **A-7 季度环比增长**（3 个，未测） | 合批 | 同属"变化"语义 |
| **4** | A-13/A-14 小池 | 合批 | 补齐 |

**★ 最值得先做的是 ① 和 ②** —— 一个走"已确认活的族"，一个走"已验证有效机制的新字段来源"。
