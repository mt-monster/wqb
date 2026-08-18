# 已提交 Alpha 经验总结

> 生成时间: 2026-08-13 | 总计: **143 Regular + 2 Super = 145 个 Alpha**

---

## 一、总览

| 维度 | 统计 |
|------|------|
| Regular Alpha | 143 |
| Super Alpha | 2（1 个已提交 ACTIVE + 1 个 IS 未完成）|
| 覆盖区域 | USA / IND / MEA / GBR / GLB / KOR / ASI（7 个区域）|
| 提交时间跨度 | 2025-03-24 → 2026-08-12 |

### 区域分布

| 配置 | 数量 | 占比 | 平均 Sharpe | 最高 Sharpe |
|------|------|------|-------------|-------------|
| USA/TOP3000/D1 | 127 | 89% | 1.56 | 4.51 |
| IND/TOP500/D1 | 4 | 2.8% | 2.50 | 3.67 |
| MEA/TOP400/D1 | 3 | 2.1% | 1.78 | 1.92 |
| GBR/TOP700/D1 | 3 | 2.1% | 1.68 | 1.80 |
| USA/ILLIQUID_MINVOL1M/D1 | 3 | 2.1% | 2.17 | 2.66 |
| GLB/TOPDIV3000/D1 | 1 | 0.7% | 2.68 | 2.68 |
| KOR/TOP600/D1 | 1 | 0.7% | 1.62 | 1.62 |
| ASI/MINVOL1M/D1 | 1 | 0.7% | 1.72 | 1.72 |

### 全局指标分布

| 指标 | Min | Max | 中位数 | 均值 |
|------|-----|-----|--------|------|
| Sharpe | 1.12 | 4.51 | 1.50 | 1.56 |
| Fitness | 0.46 | 4.13 | 1.28 | 1.37 |
| Turnover | 1.0% | 55.9% | 5.9% | 8.0% |
| Returns | 4.5% | 24.9% | — | 10.7% |
| Margin | 0.34bp | 1.94bp | 3.56bp | 5.49bp |

---

## 二、区域经验

### 2.1 USA/TOP3000/D1（127 个，核心阵地）

**数据源构成**

| 数据源 | 数量 | 平均 Sharpe | 特征 |
|--------|------|-------------|------|
| mdl177 (factor model) | 102 | 1.51 | 主力，覆盖 80% |
| fnd6 (fundamental) | 13 | 1.62 | 稳定中上 |
| anl4 (analyst) | 2 | 1.71 | 少量但有效 |
| inst18 (institutional) | 1 | 2.23 | 基金持仓变动 |
| fnd93 | 1 | 1.67 | 费用极差 |
| 其他混合 | 8 | 1.98 | 包含最高 sharpe |

**最佳 Alpha**

| ID | Sharpe | Fitness | 数据源 | 表达式 |
|----|--------|---------|--------|--------|
| xAdL5vmN | 4.51 | 4.13 | earnings_surprise | `ts_decay_linear(signed_power(subtract(group_rank(vec_avg(historic_earnings_surprise_score), subindustry), 0.5), 5), 90)` |
| vRVNZqrz | 2.26 | 1.46 | fundamental | `trade_when(ts_arg_max(volume, 5) == 0, group_zscore(group_rank(...)))` |
| MPQVZRnk | 2.23 | 1.44 | inst18 | `scale(rank(ts_zscore(subtract(ts_mean(...pre_holding,22), ts_mean(...cur_holding,22)), 189), 250))` |
| ELblWbL | 2.20 | 2.86 | mdl177 | `a = -FIELD * ts_std_dev(FIELD, 60); vector_neut(a, b)` |
| VdKw8Jw | 2.08 | 1.28 | fnd6 | `group_rank(ts_rank(fnd6_newqv1300_altoq, 10), market)` |

**OS 表现最佳**

| ID | IS Sharpe | OS Sharpe | 衰减率 | 表达式 |
|----|-----------|-----------|--------|--------|
| WL5qXEG | 1.51 | 1.72 | +14% | `-rank(ts_sum((close-low)/(high-close), 3))` |
| xGwV5Jq | 1.78 | 1.54 | -13% | `ts_sum(mdl177_fa_chgis, 252) + group_neutralize` |
| YJkjgww | 1.37 | 1.44 | +5% | `-FIELD * ts_std_dev(FIELD)` |
| GzA0rOx | 1.38 | 1.44 | +4% | `-FIELD * ts_std_dev(FIELD)` |
| KzE3N2k | 1.39 | 1.39 | 0% | `ts_std_dev(FIELD, 252) + group_neutralize` |

### 2.2 IND/TOP500/D1（4 个，高质量区域）

| ID | Sharpe | Fitness | 数据源 | 表达式模式 |
|----|--------|---------|--------|-----------|
| QPGbAOn5 | **3.67** | 2.96 | mdl177 | `add(rank(ts_rank(ts_backfill(FIELD,66),250))*-0.6, ...)` 多因子加权 |
| QPGvgO2G | 2.69 | 2.61 | mdl177 | 同上，4 因子组合 |
| A1GN2mWX | 1.84 | 1.63 | mdl177 | 同上，3 因子组合 |
| 1YzLbZzQ | 1.81 | 1.24 | anl39 | `scale(rank(group_zscore(ts_zscore(subtract(ts_mean(A,22),ts_mean(B,22)),189),industry)))` |

**关键经验**: mdl177 在 IND 表现远优于 USA。多因子 `rank(ts_rank(ts_backfill,66),250)` 加权组合是主力模式，负号取反向。

### 2.3 MEA/TOP400/D1（3 个）

全部使用 `mdl31` 因子模型：
- `rank(ts_rank(ts_backfill(star_eq_ope_rank,66),126))*0.6 + rank(ts_backfill(mdl31_dy_pct_current,66))*0.4`
- 平均 Sharpe 1.78，margin 3.3bp（高于 USA 均值）

**关键经验**: MEA 适合 star_eq + mdl31 组合，使用 0.6+0.4 加权。

### 2.4 GBR/TOP700/D1（3 个）

| 数据源 | 模式 |
|--------|------|
| ep_yield_pct_smest | `rank(ts_delta(ts_backfill(FIELD,66),66))*0.5 + rank(ts_delta(ts_backfill(FIELD,66),22))*0.5` |
| oth455 (relation) | `scale(-rank(group_neut(ts_mean(returns,22), oth455_cluster))) + scale(-group_rank(ts_delta(close,5), ...))` |
| 形态因子 | `0.4*rank(breakaway_gap) + 0.3*rank(rising_wedge) + 0.3*rank(v_shape)` |

**关键经验**: GBR 数据源多样，`ep_yield_pct_smest` 的 delta 双窗口组合有效。

### 2.5 GLB/TOPDIV3000/D1（1 个）

`9qpQ0VQ2`: `group_rank(ts_rank(ts_backfill(winsorize(predicted_first_quantile_ten_day_return_41, std=5), 60), 250), country)`

**关键经验**: GLB 必须用 `country` 分组做中性化，`group_rank` 是核心算子。

### 2.6 KOR/TOP600/D1（1 个）

`e73Rw8qg`: `add(ts_rank(vec_avg(anl44_second_en_eps_value), 50), -ts_rank(vec_avg(pretaxprofit_estimates_down_4w), 22))`

**关键经验**: KOR 使用 `anl44` 分析师数据 + `pretaxprofit_estimates_down` 做正向/反向组合。

> **2026-08-14 补充（重要）**：KOR 其余 value/quality 种子（price_volume_quantile1_* / short_term_regime* 变体族）PROD_CORRELATION **全败**（0.7668/0.7824/0.759/0.7654，均 >0.7，区域隔离不解码风格因子）；SUBINDUSTRY 单 alpha 无效；KOR SuperAlpha 不可构造（组件池 ~0.9 相关）。现有信号族两条路全封死，解锁须挖 **novel 非 value/quality 风格信号族**（prod-corr<0.7 且 IS 过闸）。详见 `kor_factor_mining_workflow.md` §8.5。

### 2.7 ASI/MINVOL1M/D1（1 个）

`qMNMbeGj`: `rank(ts_rank(ts_delta(ts_backfill(vec_avg(oth36_short_pos_in_shares), 200), 66), 250))`

---

## 三、数据源经验

### 3.1 mdl177（factor model，102 个，核心数据源）

mdl177 是 WorldQuant 因子模型库，包含大量预计算因子。

**Top 子字段**（使用频次）

| 子字段 | 频次 | 因子类别 |
|--------|------|----------|
| managementqualityfactor_ollev | 6 | 管理质量 |
| valanalystmodel_qva_balsht | 6 | 估值 |
| liquidityriskfactor_gear_alt | 4 | 流动性风险 |
| industryrrelativevaluefactor_curindbp | 4 | 行业相对价值 |
| garpanalystmodel_qgp_vfpriceratio | 4 | 分析师模型 |
| deepvaluefactor_cashp | 4 | 深度价值 |
| fangma_rvm_usa_fangma_rvm1 | 4 | 方方马模型 |
| sensitivityfactor400_pbroeresidual | 4 | 敏感度 |
| historicalgrowthfactor_fcfequity | 4 | 历史成长 |
| garpanalystmodel_qgp_relgrowth | 4 | 分析师成长 |

**关键发现**: mdl177 在 USA 平均 Sharpe 1.51，但 OS 表现分化严重：
- 好的（OS > IS）：YJkjgww, GzA0rOx, RzMOGR0
- 衰减的（OS < IS）：6J1P0XL (2.2→1.06), 1K9bE3z (1.81→0.94), 06exgMk (2.01→0.91)
- **教训**: 高 IS sharpe 不等于好 OS，mdl177 因子在 USA 存在明显的过拟合风险

### 3.2 fnd6（fundamental，13 个）

全部使用 `group_rank(ts_rank(FIELD, 60), group)` 模板：
- 分组: market / sector / subindustry
- 窗口: 10 / 60 天

平均 Sharpe 1.62，表现稳定。

**最佳**: `VdKw8Jw` (sh=2.08) — `group_rank(ts_rank(fnd6_newqv1300_altoq, 10), market)`
**最低**: `5Glv3nn` (sh=1.29)

### 3.3 混合/其他数据源（8 个，最高均值 1.98）

包含非标准数据集：
- `historic_earnings_surprise_score`（最高 sharpe 4.51）
- `eur_top_value_2`（欧式估值）
- `annual_unearned_revenue_total / annual_sga_cost_total`（会计比率）
- `(close-low)/(high-close)`（价量关系，OS 表现最佳 1.72）

**关键经验**: 非主流数据源有更高潜力但需要精细建模。

---

## 四、表达式模板经验

### 4.1 模板一：动量/反转（vector_neut 型）

```
a = -FIELD * ts_std_dev(FIELD, N); b = abs(ts_mean(returns,252) / ts_std_dev(returns,252)); vector_neut(a, b)
```

- **数量**: 31 个（mdl177 主力）
- **平均 Sharpe**: 1.49
- **OS 衰减**: 严重（多个 IS>2.0 的 alpha OS 降至 1.0 以下）
- **适用**: mdl177 各类因子

**变体**: `-FIELD * ts_std_dev(FIELD, N)`（无 vector_neut）
- 数量: 8 个，平均 Sharpe 1.46
- 更简洁但 OS 衰减同样严重

### 4.2 模板二：累积 + 分层中性化

```
a = ts_sum(FIELD, N); a1 = group_neutralize(a, market); a2 = group_neutralize(a1, bucket(rank(cap), range='0.1,1,0.1'))
```

- **数量**: 14 + 4 + 4 = 22 个
- **平均 Sharpe**: 1.52-1.55
- **特征**: 先累积再按市值分层中性化，降低容量风险

**变体**（按 industry 中性化）: 4 个，avg_sh=1.65

### 4.3 模板三：异质波动率（idiosyncratic volatility）

```
piece = group_mean(ts_std_dev(FIELD, N), N, industry) - ts_std_dev(FIELD, N); ts_mean(piece, N)
```

- **数量**: 12 个（9+3）
- **平均 Sharpe**: 1.48
- **特征**: 用组内平均波动率减去个股波动率，捕捉异质风险

### 4.4 模板四：基本面排名

```
group_rank(ts_rank(FIELD, 60), group)
```

- **数量**: 13 个（fnd6 全部）
- **平均 Sharpe**: 1.62
- **分组**: market / sector / subindustry
- **特征**: 最简洁稳定的模板，过拟合风险低

### 4.5 模板五：相对价值（log-diff）

```
group_rank(log(ts_mean(FIELD_A, N)) - log(ts_mean(FIELD_B, N)), group)
```

- **数量**: 9 个
- **平均 Sharpe**: 1.55
- **适用**: mdl177 两个相关因子做差

### 4.6 模板六：多因子加权组合

```
add(multiply(rank(ts_rank(ts_backfill(FIELD_A, 66), 250)), W1), multiply(rank(ts_rank(ts_backfill(FIELD_B, 66), 250)), W2), ...)
```

- **数量**: 多区域使用
- **最佳**: IND QPGbAOn5 (sh=3.67)
- **特征**: 2-4 个因子，权重和为 1.0 或 -1.0（负号取反向）

### 4.7 特殊模板（高 sharpe 单例）

| 模板 | Sharpe | 核心思想 |
|------|--------|----------|
| `ts_decay_linear(signed_power(group_rank(...) - 0.5, 5), 90)` | 4.51 | 盈余惊喜 → signed_power → 线性衰减 |
| `trade_when(ts_arg_max(volume,5)==0, ...)` | 2.26 | 只在放量日交易 |
| `group_rank(ts_ir(winsorize(ts_backfill(...), 4), 20), industry)` | 1.66 | IR + winsorize 防极端值 |
| `rank(ts_rank(ts_delta(ts_backfill(..., 200), 66), 250))` | 1.72 | 200 天 backfill → delta |

---

## 五、参数选择经验

### 5.1 中性化

| 中性化方式 | 数量 | 适用场景 |
|-----------|------|---------|
| MARKET | 112 (78%) | 默认，通用 |
| SUBINDUSTRY | 14 (10%) | MEA/GBR 等需行业精度（IND 实际用 STATISTICAL，见 rules.json） |
| SECTOR | 5 (3%) | 基本面数据 |
| INDUSTRY | 4 (3%) | 行业因子 |
| COUNTRY | 3 (2%) | GLB 必须 |
| STATISTICAL | 3 (2%) | 特殊 |

### 5.2 衰减

| Decay | 数量 | 适用 |
|-------|------|------|
| 5 | 113 (79%) | 默认 |
| 0 | 11 (8%) | 价量类 |
| 4 | 7 (5%) | 中等频率 |
| 3 | 3 (2%) | IND |

### 5.3 截断

- **8%**: 139 个 (97%) — 标准配置
- 4%: 2 个
- 1%: 2 个

### 5.4 时间窗口经验

| 窗口 | 用途 | 出现频次 |
|------|------|---------|
| 66 | ts_backfill | 高频（22 季） |
| 22 | ts_mean / ts_zscore | 高频 |
| 250 | ts_rank / ts_sum | 年度窗口 |
| 252 | ts_std_dev / ts_mean(returns) | 年度波动率 |
| 30 | ts_std_dev / ts_rank | 短期 |
| 60 | ts_rank / ts_std_dev | 中期 |
| 189 | ts_zscore (6*21≈126 交易日的 1.5 倍) | 中期 zscore |

---

## 六、Super Alpha 经验

### 6.1 成功配方：gJ8eVmNM（已提交 ACTIVE）

```python
combo = combo_a(alpha)
selection = (prod_correlation > 0)
```

| 指标 | 值 |
|------|------|
| Sharpe (IS) | 4.11 |
| Fitness | 4.18 |
| Turnover | 9.0% |
| Returns | 12.9% |
| Drawdown | 2.8% |
| Prod Correlation Max | 0.7149 |
| Self Correlation Max | 0.6143 |

**关键机制**: `prod_correlation > 0` 从整个 OS 池（上万个 alpha）中自动筛选正相关 alpha，因子暴露被极度分散，绕过了手动指定 children 时 prod_corr 过高的问题。

### 6.2 失败的 SA（教训）

| ID | 问题 | Prod Correlation |
|----|------|-----------------|
| VkGxovMM | 手动 10 个 children，因子暴露集中 | 0.897 |
| omNEOojb | `(color == "BLUE")` 筛选，仍高度相关 | 0.907 |
| 2rpAb7lP | `selection='1'` 无筛选 | 0.946 |

**教训**: 手动选择 children 时，即使 10 个 alpha 各自合格，组合后 prod_corr 仍然高达 0.9+。必须用 selection 表达式从大范围自动筛选。

### 6.3 SA 配置要点

- **selection 必须包含 `(prod_correlation > 0)`** — 这是 USA SA 的硬性要求
- **combo_a(alpha)** 是唯一可靠的组合算子
- **至少 10 个组件** — selection 筛选结果必须 ≥ 10 个
- **componentActivation = IS** — 使用 IS 数据
- **startDate=2014-01-01, endDate=2023-12-31** — 确保完整 IS 期覆盖
- **description ≥ 100 字符** — combo 和 selection 都需要

---

## 七、OS 表现分析

### 7.1 IS-OS 衰减规律

从 124 个有 OS 数据的 alpha 中：

| OS 区间 | 数量 | 典型特征 |
|---------|------|---------|
| OS > IS | ~10 | 简单价量关系、`ts_sum` 累积 |
| OS ≈ IS | ~30 | `group_rank(ts_rank(...))` 稳定模板 |
| OS 显著衰减 | ~80+ | `FIELD * ts_std_dev(FIELD)` 动量/反转型 |

### 7.2 抗衰减模式

表现最稳健（IS-OS 接近）的表达式特征：
1. **`group_rank(ts_rank(FIELD, 60), group)`** — 简单排名，过拟合风险低
2. **`ts_sum(FIELD, 252)` + 分层中性化** — 长期累积平滑
3. **`-rank(ts_sum((close-low)/(high-close), 3))`** — 极简价量
4. **`ts_std_dev(FIELD)` + `group_neutralize`** — 波动率中性化

### 7.3 高衰减模式（避免）

1. **`-FIELD * ts_std_dev(FIELD, N)`** — 虽然 IS 高但 OS 衰减严重
2. **`vector_neut(a, b)`** 类型 — 高 IS 但 OS 普遍不及预期
3. **`group_mean(ts_std_dev) - ts_std_dev`** 异质波动率 — IS 中等但 OS 衰减

---

## 八、关键经验总结

### ✅ 有效的

1. **mdl177 因子模型**是 USA 核心数据源，但需搭配稳健模板
2. **`group_rank(ts_rank(FIELD, 60), group)`** 是最稳定的表达式模板（sh 1.29-2.08，OS 衰减少）
3. **IND 区域**的 `rank(ts_rank(ts_backfill, 66), 250)` 多因子加权在 3 个 alpha 上均达标
4. **MEA 区域**的 `star_eq + mdl31` 组合稳定产出 1.7+
5. **非主流数据源**（earnings_surprise, 会计比率）有更高 sharpe 潜力
6. **SA 用 `prod_correlation > 0` 做 selection** 可绕过 prod_corr 墙

### ⚠️ 需要注意的

1. **mdl177 在 USA 存在过拟合** — 高 IS sharpe 不等于好 OS，需要谨慎选择子字段
2. **`vector_neut` 型**表达式 OS 衰减严重，不建议作为首选
3. **跨区域 sharpe 不可直接比较** — USA 竞争激烈（mean=1.56），IND 竞争少（mean=2.50）
4. **margin 普遍偏低**（median=3.56bp），>1bp 的仅 20 个

### 🚫 无效的

1. **手动指定 10 个 children 做 SA** — prod_corr 必然 > 0.89，无法通过
2. **`(color == "BLUE")` 筛选** — 仍高度相关
3. **`reduce_avg(alpha)`, `reduce_sum(alpha)`** — 不支持，报 "single expression" 错误
4. **`-1 * combo_a(alpha)`** — 报 "single expression" 错误
5. **`(sharpe > X)` 作为 selection** — sharpe 不是可用变量

### 📋 参数标准配置

```python
# USA/TOP3000 默认
neutralization = MARKET
decay = 5
truncation = 0.08
pasteurization = ON
nan_handling = ON
unit_handling = VERIFY
maxTrade = OFF
```

```python
# IND/TOP500 默认（以 rules.json 结构化提取为准）
neutralization = STATISTICAL
decay = 8
truncation = 0.08
```

---

## 九、提交节奏

| 时期 | 特征 | 日均提交 |
|------|------|---------|
| 2025-03~04 | 起步期 | 0.3/天 |
| 2025-06 | 加速期 | 2.5/天 |
| 2025-07 | 高峰期 | 4.5/天 |
| 2025-08~2026-06 | 低谷期 | 0.02/天 |
| 2026-07~08 | 复苏期 | 1.2/天 |

---

## 十、下一步方向

1. **补强 OS 表现** — 现有 127 个 USA alpha 中大量 OS 衰减，需复盘 mdl177 因子选择
2. **扩展数据源** — 非主流数据源（earnings_surprise, 会计比率）有更高潜力
3. **GLB/KOR/ASI** — 当前覆盖不足。**KOR 须先挖 novel 非 value/quality 风格信号族**（现有种子 PROD_CORRELATION 全败、SA 不可构造，见 `kor_factor_mining_workflow.md` §8.5）才能解锁；单 alpha 提交前先过 PROD 探针。
4. **SA 多样化** — 尝试 `(prod_correlation > 0) and (sharpe > X)` 等更精细筛选
5. **margin 优化** — 当前 margin 中位数仅 3.56bp，需寻找高 margin 模式