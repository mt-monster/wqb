# 字段-算子关系规律总结（EUR wave104-123 实证）

> 数据来源：`data/wqb.db` backtest_results 表，EUR 区域 wave104-123 共 141 条回测记录。
> 生成时间：2026-09-04

## 1. 总体算子使用分布

| 算子类别 | 使用次数 | 占比 | 平均 Sharpe | 最高 Sharpe |
|---------|---------|------|------------|------------|
| Time Series | 129 | 36.2% | 0.18 | 1.81 |
| Cross Sectional | 120 | 33.6% | 0.20 | 1.81 |
| Arithmetic | 85 | 23.8% | 0.19 | 1.81 |
| Vector | 35 | 9.8% | -0.01 | 0.84 |
| Group | 13 | 3.6% | 0.17 | 1.35 |
| Logical | 4 | 1.1% | 0.21 | 0.58 |

**关键发现**：
- `rank` 使用 119 次（84% 表达式），是绝对主导算子
- `multiply`/`add`/`subtract` 算术组合是双腿/多腿配方的基础
- `ts_mean`/`ts_delta`/`ts_backfill` 是时序处理三剑客
- **Vector 类别平均 Sharpe 为负**（-0.01），VECTOR 字段在 EUR 表现不佳
- **Logical 类别使用严重不足**（仅 4 次，1.1%），但平均 Sharpe 最高（0.21）

## 2. 高分表达式算子特征（Sharpe > 1.0，n=13）

### 2.1 核心算子组合

| 组合 | 出现次数 | 典型场景 |
|-----|---------|---------|
| `add + multiply + rank` | 8 | 双腿加权配方（0.4×慢腿 + 0.6×快腿） |
| `rank + ts_decay_linear` | 1 | 衰减加权单腿 |
| `add + group_sum + multiply` | 1 | 行业聚合 + 加权 |
| `rank + zscore` | 1 | 标准化 + 截面排序 |
| `multiply + rank + ts_mean` | 1 | 时序平滑 + 加权 |
| `rank + ts_backfill + ts_mean` | 1 | 填充 + 平滑 + 排序 |

### 2.2 高分表达式共同特征

1. **全部使用 `rank`**：13/13 高分表达式都含 `rank`
2. **双腿加权是主流**：8/13 使用 `add(multiply(w1, rank(...)), multiply(w2, rank(...)))` 结构
3. **时序算子必选**：12/13 含 Time Series 类别（`ts_mean`/`ts_delta`/`ts_backfill`）
4. **窗口选择**：慢腿 22/66，快腿 5/10（与披露周期对齐）

### 2.3 高分表达式示例（wave112，Sharpe 1.81）

```
add(
  multiply(0.4, rank(ts_mean(surprise_pct_last_year_earnings_3, 22))),
  multiply(0.6, rank(ts_delta(common_gap_up, 5)))
)
```

**结构解析**：
- 慢腿：`ts_mean(surprise_pct, 22)` — 22 日平滑，捕捉预期修正趋势
- 快腿：`ts_delta(gap_up, 5)` — 5 日变化，捕捉短期动量
- 合成：`0.4×慢 + 0.6×快` — 加权截面 rank

## 3. 低分表达式算子特征（Sharpe < 0，n=47）

### 3.1 过度使用算子

| 算子 | 低分中使用次数 | 问题 |
|-----|-------------|------|
| `rank` | 38 | 裸 rank 无信息增量 |
| `ts_mean` | 17 | 单纯平滑无方向性 |
| `vec_avg` | 16 | VECTOR 字段聚合后信号弱 |
| `ts_backfill` | 12 | 填充后时序失真 |
| `ts_zscore` | 11 | 标准化后截面区分度下降 |
| `reverse` | 7 | 反转逻辑在 EUR 不适用 |

### 3.2 低分表达式典型模式

1. **裸字段 + rank**：`rank(field)` — 无经济学机制，纯数据驱动
2. **VECTOR 字段直接聚合**：`vec_avg(sentiment_field)` — 聚合后信息损失
3. **过度平滑**：`ts_mean(ts_backfill(field, 66), 66)` — 双重平滑导致信号滞后
4. **无意义反转**：`reverse(rank(field))` — 无经济学依据的反向

## 4. 字段类型 × 算子类别适配矩阵

### 4.1 最佳组合（按平均 Sharpe 排序）

| 字段类型 | 最佳算子类别 | 平均 Sharpe | 推荐算子 |
|---------|-----------|------------|---------|
| pattern/technical | Cross Sectional | 0.90 | `rank`, `zscore` |
| pattern/technical | Time Series | 0.58 | `ts_delta`, `ts_mean` |
| other | Logical | 0.58 | `if_else`, `trade_when` |
| other | Group | 0.26 | `group_sum`, `group_zscore` |
| analyst/model | Group | 0.14 | `group_neutralize` |
| analyst/model | Cross Sectional | 0.12 | `rank`, `quantile` |

### 4.2 最差组合（避免）

| 字段类型 | 最差算子类别 | 平均 Sharpe | 问题 |
|---------|-----------|------------|------|
| sentiment/news | Arithmetic | -0.20 | 算术运算放大噪声 |
| sentiment/news | Cross Sectional | -0.08 | 截面区分度低 |
| sentiment/news | Vector | -0.05 | 聚合后信号弱 |
| sentiment/news | Time Series | -0.05 | 时序平滑滞后 |
| analyst/model | Vector | 0.01 | 不适用 |

### 4.3 字段类型适配建议

| 字段类型 | 推荐策略 | 避免策略 |
|---------|---------|---------|
| **pattern/technical** | `rank(ts_delta(field, 5))` / `rank(zscore(field))` | 避免 Group 算子 |
| **analyst/model** | `group_zscore(field, industry)` / `rank(ts_mean(field, 22))` | 避免 Vector 聚合 |
| **sentiment/news** | 暂不建议在 EUR 使用 | 所有类别均表现不佳 |
| **flow/ownership** | `rank(ts_delta(field, 10))` / `if_else(condition, field, 0)` | 避免裸 rank |
| **price/volume** | `rank(ts_corr(price, volume, 22))` | 避免过度平滑 |

## 5. 算子类别使用不足根因分析

### 5.1 Logical 类别（使用 1.1%，平均 Sharpe 0.21）

**根因**：
1. **GEM prompt 未强制要求**：prompt 中 Logical 是"建议"而非"必须"
2. **LLM 不熟悉场景**：`if_else`/`trade_when` 需要条件构造能力，LLM 倾向简单包裹
3. **Gate 未硬闸**：Logical 类别缺失不阻断 wave

**改进**：
- Gate 硬闸：Logical/Group/Vector 至少各 1 个（已落地 `wave_gate.py`）
- Prompt 教学示例：`if_else(ts_delta(x,5)>0, rank(x), rank(reverse(x)))`

### 5.2 Group 类别（使用 3.6%，平均 Sharpe 0.17）

**根因**：
1. **行业中性化认知不足**：LLM 不知道 `group_zscore(x, industry)` 比 `rank(x)` 更稳健
2. **Group 算子参数复杂**：需要指定 group 字段（industry/sector/subindustry）
3. **EUR 行业分类数据质量**：subindustry 覆盖度低，group 算子效果打折

**改进**：
- Prompt 强制要求：至少 1 个 `group_zscore`/`group_neutralize`
- 字段适配表：analyst/model 字段优先 Group 算子

### 5.3 Vector 类别（使用 9.8%，平均 Sharpe -0.01）

**根因**：
1. **VECTOR 字段本身信号弱**：EUR 的 VECTOR 数据集（news_sentiment_dl/analyst45）alphaCount 低
2. **聚合方式单一**：只用 `vec_avg`，未尝试 `vec_stddev`（分歧度）/`vec_count`（覆盖度）
3. **VECTOR 字段预处理缺失**：未做 `ts_backfill` 填充导致时序断裂

**改进**：
- VECTOR 字段必须先 `vec_stddev` 或 `vec_count` 提取分歧/覆盖特征
- 避免 `vec_avg` 直接聚合（信息损失）

## 6. 落地改进清单

| 优化项 | 状态 | 落地位置 |
|-------|------|---------|
| Gate 算子类别覆盖硬闸 | ✅ 已落地 | `tools/wave_gate.py` 第 284-354 行 |
| 算子使用频率反馈到 GEM | ✅ 已落地 | `tools/update_operator_stats.py` |
| GEM prompt 算子场景示例 | ✅ 已落地 | `economic_priors.py` 第 207-222 行 |
| 字段-算子适配前置检查 | 🔄 待落地 | S1 字段扫描自动标注 |
| Logical/Group 算子强制注入 | 🔄 待落地 | `build_wave.py` 契约算子注入 |

## 7. 下一步行动

1. **S1 字段扫描增强**：自动标注字段类型（signal/scale/metadata/date）+ 推荐算子类别
2. **GEM prompt 强制约束**：Logical/Group/Vector 至少各 1 个 concept
3. **build_wave 契约算子注入**：自动补全缺失类别（如 `if_else`/`group_zscore`/`vec_stddev`）
4. **S6 回写算子统计**：每波回测后更新 `region_kb.operator_usage_stats`

---

*本文档由 `logs/_tmp_field_op_pattern.py` 分析生成，数据截至 wave123。*
