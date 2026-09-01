# 从字段角度看 wqb 数据库：字段如何处理、如何组合成 alpha

> 数据源：`data/wqb.db`（46,663 字段 / 598 数据集 / 957 alpha / 10 区域）
> 分析日期：2026-08-31
> 指标来源：`alphas` 表（唯一可靠指标源，sharpe/fitness 直接非空）

---

## 0. 一句话结论

**你的问题不是"字段不够"，而是"字段开发极度不均"：46,663 个字段里只有 389 个（1.3%）真正进过 alpha 表达式。**
真正该做的不是继续找新字段，而是 (1) 把已验证有效的字段模式吃透并横向复制；(2) 从 28,000+ 个"高覆盖但从没碰过"的字段里，按已验证的字段模式去定向开采。

---

## 1. 数据库字段现状盘点

### 1.1 规模
| 维度 | 数量 |
|---|---|
| 字段总数 | 46,663 |
| 数据集总数 | 598 |
| alpha 总数（含表达式） | 957 |
| 区域 | 10（USA/GBR/EUR/MEA/IND/KOR/ASI/GLB/HKG/DEU）|

### 1.2 字段类型
| 类型 | 数量 | 含义 |
|---|---|---|
| MATRIX | 35,606 (76%) | 横截面时序（每日每股票一个值）→ **主力信号源** |
| VECTOR | 10,768 (23%) | 时序向量 → 需 `vec_avg`/`vec_sum` 降维后才能用 |
| GROUP | 273 | 分组字段（sector/industry）→ 只用于中性化，不做信号 |
| SYMBOL/UNIVERSE | 16 | 元信息 |

> 注意：数据库里 `field_group` 列几乎全空（46,663 里只有 1 个填了 growth），**字段分组必须靠名称前缀推断**，不能依赖这个字段。

### 1.3 区域字段开发度（核心发现）
| 区域 | 总字段 | 已用字段 | 高覆盖(≥0.9)但未用 | 开发率 |
|---|---|---|---|---|
| **USA** | 38,649 | 264 | **28,081** | **0.7%** |
| **EUR** | 4,570 | 16 | **2,262** | **0.4%** |
| GBR | 765 | 83 | 331 | 10.8% |
| MEA | 2,115 | 165 | 344 | 7.8% |
| IND | 564 | 29 | 380 | 5.1% |

**解读**：USA 和 EUR 是最大矿藏，但开发率不到 1%。你的算力几乎全砸在 MEA（184 个 alpha）和 IND 上，而这两处字段总量加起来还不到 USA 的 8%。

---

## 2. 什么样的字段真正出 alpha？（从 957 个 alpha 反推）

### 2.1 高表现 alpha（sharpe≥1.5 且 fitness≥1.0）命中的字段 TOP
| 字段 | 出现次数 | 字段本质 |
|---|---|---|
| `fnd72_pit_or_bs_q_bs_tot_asset` | 47 | 基本面-总资产（分母/规模锚） |
| `fnd72_pit_or_is_q_ebitda` | 40 | 基本面-EBITDA（盈利能力） |
| `ern3_next_interval` | 40 | 财报事件-距下次财报间隔 |
| `analyst_eps_upward_revisions_4weeks` | 40 | 分析师-EPS上调计数 |
| `analyst_eps_downward_revisions_last_four_weeks_count` | 40 | 分析师-EPS下调计数 |
| `analyst_dividend_per_share_raises_1m_count` | 36 | 分析师-股息上调（avgSharpe **1.73**，最高） |
| `analyst_lowered_dividend_per_share_count_1m` | 36 | 分析师-股息下调 |
| `analyst_net_income_raised_count_one_week` | 32 | 分析师-净利上调 |
| `fnd72_pit_or_cf_q_cf_cash_from_oper` | 22 | 基本面-经营现金流 |
| `debt_current_liabilities_total` | 22 | 基本面-流动负债 |

### 2.2 反直觉发现：什么字段不出 alpha
| 字段族 | avgSharpe | avgFitness | 结论 |
|---|---|---|---|
| `analyst_dividend_*`（分析师修正） | **1.73** | 1.70 | ✅ 最强信号族 |
| `analyst_eps/price_target_*` | 1.4–1.5 | 1.3–1.5 | ✅ 稳定有效 |
| `fnd72_*`（基本面 PIT） | 1.1–1.4 | 1.2–1.5 | ✅ 作分母/锚定极稳 |
| `mdl238_global_rank` / 模型分 | 0.9 | 0.9 | ⚠️ 中等，需组合 |
| `nws104_*`（新闻情绪） | **0.09–0.35** | 0.04–0.09 | ❌ 单独用几乎无效 |
| `snl27_*`（社交情绪） | 0.43–0.59 | 0.18–0.25 | ❌ 单独用弱 |
| `average_positive_sentiment_*` | 0.27–0.55 | 0.06–0.12 | ❌ 弱 |

**核心规律**：
- **"计数差"型字段（上调数 − 下调数）是地表最强信号**——分析师修正类全部是这个结构。
- **基本面 PIT 字段单独不出彩，但当分母/规模锚（除以总资产/市值）后极稳**。
- **原始情绪分（新闻/社交/NLP）单独用全是噪音**，必须与事件或分析师修正绑定才有意义。

### 2.3 高 sharpe alpha 的表达式结构（拆解 sharpe≥2 的样本）
```
# 模式A：分析师修正差 + 基本面锚（MEA S=2.29）
add(multiply(rank(subtract(raised_count, lowered_count)), 0.4),
    add(multiply(rank(subtract(...)), ...)))

# 模式B：时序变化 + 长期 zscore 反向（MEA S=2.38）
add(multiply(rank(ts_delta(vec_avg(est_q_pre_mean),63)),0.6),
    multiply(rank(multiply(ts_zscore(vec_avg(other_liabilities),252),-1)),0.4))

# 模式C：最简单的价值比（MEA S=2.19）
rank(quarterly_net_income/market_cap)

# 模式D：分组中性化 + quantile（IND S=2.76）
group_neutralize(quantile(subtract(backfill(score_A),backfill(score_B))), industry)
```

**表达式骨架就三种**：
1. `rank(X/Y)` —— 价值/比率型（基本面当分母）
2. `rank(subtract(up_count, down_count))` —— 计数差型（分析师修正）
3. `add(multiply(rank(A),w1), multiply(rank(B),w2))` —— 加权合成（⚠️ 违反你的纪律①，见 §4）

---

## 3. 字段处理的四条具体路径（按优先级）

### 路径一：把"计数差"模式横向复制到所有 analyst 字段族【最高优先级】
你已验证 `subtract(up_count, down_count)` 是有效结构。数据库里 analyst 类字段有 **17,215 个（USA）+ 3,993（GBR）**，但你只碰了其中十几个计数对。

**做法**：
- 在 fields 表里筛 `field_name LIKE '%raised%' OR '%lowered%' OR '%upward%' OR '%downward%'`
- 按语义配对（同指标同周期的 up/down），逐对套 `rank(subtract(up,down))`
- USA analyst 还有 **96 个高覆盖未开发字段**，GBR analyst 几乎没动——直接复制已验证模板即可。

### 路径二：基本面字段一律当"锚"，不当信号
`fnd72_*`（USA 11,230 字段）单独用 sharpe 平平，但当分母时（`X/tot_asset`、`X/market_cap`、`X/ebitda`）极稳。

**做法**：
- 任何基本面字段 → 默认套 `rank(field / fnd72_pit_or_bs_q_bs_tot_asset)` 或 `/market_cap` 再测。
- 时间窗口只用 1/5/22/66/252（你的纪律③）。

### 路径三：VECTOR 字段先降维再进表达式
23% 字段是 VECTOR，必须用 `vec_avg()`/`vec_sum()` 包一层（你的高 sharpe 样本里 `vec_avg` 出现 1,335 次）。**直接用 VECTOR 字段名会报 unknown variable**——这就是你记录里的 token-name 隐患的一部分。

### 路径四：原始情绪字段只在"事件叠加"时用
`nws104_*`/`snl27_*` 单独用全废。正确用法是乘上事件掩码（如 `ern3_next_interval<5` 财报临近）或与分析师修正同向确认，把弱信号变成条件信号。

---

## 4. 必须遵守的纪律（来自 alpha_search_principles）

1. **禁止混信号调参**：高 sharpe 样本里的 `add(multiply(rank(A),0.6),multiply(rank(B),0.4))` 加权相加，**正是你纪律里明令禁止的混信号结构**。这些老 alpha 能跑不代表新 alpha 该这么写——新信号一律拆成 atom alpha。
2. **优先单数据集 atom alpha**：先让单个字段（或同数据集内字段对）独立过闸门，再谈组合。
3. **时间窗口只用** 1/5/22/66/252/504/1008/1260。
4. **token-name 隐患**：用任何字段前，先在 fields 表里确认它真实存在（`opt6_ivetfratio`、`momentum_strength_index` 这类在表达式出现但平台报 unknown variable）。

---

## 5. 立即可执行的开采清单（按 ROI 排序）

| 优先级 | 目标 | 字段规模 | 理由 |
|---|---|---|---|
| ★★★ | USA analyst 未开发字段配对（raised/lowered 计数差） | 96 高覆盖未用 | 已验证最强模式，同区同结构直接复制 |
| ★★★ | USA fnd72 基本面当分母的比率族 | 11,230 字段 | 锚定结构稳定，prod_corr 低 |
| ★★☆ | USA recovered_ds_* 数据集（12,735 高覆盖未用字段） | 最大矿藏 | ⚠️ 先字段反查归类（recovered 是假名，同标号混多数据集），别按 ds 编号批跑 |
| ★★☆ | EUR 全区（开发率 0.4%，2,262 高覆盖未用） | 4,570 字段 | 几乎处女地，predictive_starmine/analyst_consensus 都没碰 |
| ★☆☆ | GBR analyst/model 高 value_score 数据集 | vs=9–10 | 平台已标高价值但 0 alpha |

---

## 6. 风险提示

- **PROD_CORRELATION 主战场在 USA/GLB**：USA 的 book 已高度同质（~145 ACTIVE 价值/盈利族），新 USA 字段组合前先用 `SUBINDUSTRY` 中性化把 prod_corr 压到 0.7 以下（你已验证的决定性杠杆）。
- **recovered_ds_* 不能按标号归类**：必须字段反查（唯一字段多数票），否则会把不同数据集的字段混成一锅。
- **EUR/GLB 开发率低不等于好挖**：GLB 情绪族刚被 prod_corr 团灭（0.82–0.86），去 EUR 前先确认新信号与现有 book 的相关性。
