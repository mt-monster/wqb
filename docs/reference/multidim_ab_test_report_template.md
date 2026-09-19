# 多维骨架标签对比实验报告

> 实验日期：{{timestamp}}
> 实验目的：验证多维骨架标签（经济学构造链感知）相比传统 5 类骨架选波的有效性
> 实验假设：多维标签能提升机制多样性、降低 CW 墙风险、发现更多信号苗头

---

## 一、实验设计

| 项 | 内容 |
|---|---|
| 对照组 | 传统 5 类骨架选波（single/ratio/group/linear_mix/event_gated） |
| 实验组 | 多维标签选波（结构/构造链/机制/字段匹配） |
| 候选池 | {{input_size}} 条表达式 |
| 选波大小 | {{target_size}} 条 |
| 评估维度 | 多样性熵、配额合规率、构造链覆盖度、机制覆盖度 |

---

## 二、多样性对比

### 2.1 结构维度

| 指标 | 传统选波 | 多维选波 | 差异 |
|------|----------|----------|------|
| 结构种类 | {{legacy.structure.unique}} | {{multidim.structure.unique}} | {{diff.structure.unique}} |
| 结构熵 | {{legacy.structure.entropy}} | {{multidim.structure.entropy}} | {{diff.structure.entropy}} |

**结构分布详情**：

| 结构标签 | 传统选波 | 多维选波 |
|----------|----------|----------|
| linear_2leg | {{legacy.structure.distribution.linear_2leg}} | {{multidim.structure.distribution.linear_2leg}} |
| linear_3plus | {{legacy.structure.distribution.linear_3plus}} | {{multidim.structure.distribution.linear_3plus}} |
| group_relative | {{legacy.structure.distribution.group_relative}} | {{multidim.structure.distribution.group_relative}} |
| event_gated | {{legacy.structure.distribution.event_gated}} | {{multidim.structure.distribution.event_gated}} |
| ... | ... | ... |

### 2.2 经济学机制维度

| 指标 | 传统选波 | 多维选波 | 差异 |
|------|----------|----------|------|
| 机制种类 | {{legacy.mechanism.unique}} | {{multidim.mechanism.unique}} | {{diff.mechanism.unique}} |
| 机制熵 | {{legacy.mechanism.entropy}} | {{multidim.mechanism.entropy}} | {{diff.mechanism.entropy}} |

**机制分布详情**：

| 机制标签 | 传统选波 | 多维选波 | 经济学含义 |
|----------|----------|----------|-----------|
| analyst_revision | {{legacy.mechanism.distribution.analyst_revision}} | {{multidim.mechanism.distribution.analyst_revision}} | 分析师修正广度 |
| momentum | {{legacy.mechanism.distribution.momentum}} | {{multidim.mechanism.distribution.momentum}} | 动量/信息扩散 |
| mean_reversion | {{legacy.mechanism.distribution.mean_reversion}} | {{multidim.mechanism.distribution.mean_reversion}} | 均值回归 |
| volume_price | {{legacy.mechanism.distribution.volume_price}} | {{multidim.mechanism.distribution.volume_price}} | 量价背离 |
| ... | ... | ... | ... |

### 2.3 构造链维度

| 指标 | 传统选波 | 多维选波 | 差异 |
|------|----------|----------|------|
| 构造链种类 | {{legacy.construction_chain.unique}} | {{multidim.construction_chain.unique}} | {{diff.construction_chain.unique}} |
| 构造链熵 | {{legacy.construction_chain.entropy}} | {{multidim.construction_chain.entropy}} | {{diff.construction_chain.entropy}} |

**构造链覆盖**：

| 构造链 | 传统选波 | 多维选波 | 经济学功能 |
|--------|----------|----------|-----------|
| raw | {{legacy.construction_chain.distribution.raw}} | {{multidim.construction_chain.distribution.raw}} | 原始字段直接读取 |
| backfill | {{legacy.construction_chain.distribution.backfill}} | {{multidim.construction_chain.distribution.backfill}} | 低频字段回填 |
| vector_agg | {{legacy.construction_chain.distribution.vector_agg}} | {{multidim.construction_chain.distribution.vector_agg}} | VECTOR 事件聚合 |
| delta | {{legacy.construction_chain.distribution.delta}} | {{multidim.construction_chain.distribution.delta}} | 变化检测 |
| ... | ... | ... | ... |

---

## 三、选波差异分析

| 指标 | 数值 |
|------|------|
| 重叠表达式 | {{comparison.overlap}} 条 ({{comparison.overlap_share}}) |
| 传统选波独有 | {{comparison.legacy_only}} 条 |
| 多维选波独有 | {{comparison.multidim_only}} 条 |

**多维选波独有的候选示例**（前 5 条）：

{{#each comparison.multidim_only_exprs}}
- {{this}}
{{/each}}

**传统选波独有的候选示例**（前 5 条）：

{{#each comparison.legacy_only_exprs}}
- {{this}}
{{/each}}

---

## 四、配额合规性

| 配额维度 | 传统选波 | 多维选波 | 状态 |
|----------|----------|----------|------|
| linear_mix ≤ 50% | {{legacy.linear_mix_share}} | {{multidim.linear_mix_share}} | {{quota_status}} |
| event_gated ≥ 10% | {{legacy.event_gated_share}} | {{multidim.event_gated_share}} | {{quota_status}} |
| group ≥ 15% | {{legacy.group_share}} | {{multidim.group_share}} | {{quota_status}} |

---

## 五、实验结论

{{#each conclusion}}
{{@index}}. {{this}}
{{/each}}

---

## 六、信号苗头发现率评估（待回测验证）

| 评估项 | 传统选波 | 多维选波 | 预期差异 |
|--------|----------|----------|----------|
| 机制覆盖度 | {{legacy.mechanism.unique}}/16 | {{multidim.mechanism.unique}}/16 | 多维覆盖更多经济学机制 |
| 构造链覆盖度 | {{legacy.construction_chain.unique}}/10 | {{multidim.construction_chain.unique}}/10 | 多维覆盖更多预处理阶段 |
| 字段匹配合规率 | - | {{multidim.field_match.pass_share}} | 多维前置拦截机制不匹配 |
| CW 墙风险 | {{legacy.cw_risk}} | {{multidim.cw_risk}} | 多维降低线性组合占比 |

---

## 七、层层推进策略验证计划

### 阶段 1：Dry-run 验证（当前）
- [x] 多维标签提取正确性
- [x] 配额配置合规性
- [x] 选波差异分析

### 阶段 2：小批量回测（下一步）
- [ ] 各选 10 条表达式回测
- [ ] 对比达标率（sharpe ≥ 1.25 且 fitness ≥ 0.8）
- [ ] 对比信号苗头发现率（sharpe ≥ 1.0）

### 阶段 3：全量对比（后续）
- [ ] 各选 48 条表达式回测
- [ ] 对比 CW 墙发生率
- [ ] 对比 PROD 相关性超标率

### 阶段 4：生产环境部署（最终）
- [ ] 多维选波设为默认
- [ ] 传统选波标记 deprecated
- [ ] 持续监控多样性指标

---

## 八、附录

### 8.1 多维标签定义

| 维度 | 标签 | 判定规则 |
|------|------|----------|
| 结构 | single_raw | 仅含 rank/ts_*，无预处理 |
| 结构 | single_preprocessed | 含 ts_backfill/ts_zscore/winsorize |
| 结构 | single_aggregated | 含 vec_avg/vec_max/vec_sum |
| 结构 | ratio_pair | divide/subtract 两字段 |
| 结构 | ratio_adjusted | divide 含 ts_std_dev/volume |
| 结构 | group_relative | group_rank/group_neutralize |
| 结构 | group_bucket | group_rank + integer 字段 |
| 结构 | linear_2leg | add + multiply ×2 |
| 结构 | linear_3plus | add + multiply ×3+ |
| 结构 | event_gated | trade_when/if_else |
| 结构 | event_freshness | days_from_last_change/last_diff_value |

### 8.2 经济学机制定义

| 机制 | 核心构造 | 适用字段形状 |
|------|----------|-------------|
| event_conviction | divide(flow, stock) → ts_sum → group_rank → winsorize → tail | zero_inflated/point_mass |
| event_gated | trade_when(event_cond, signal, neutral) | zero_inflated/point_mass |
| spread_pair | subtract(rank(A), rank(B)) | spread |
| ceiling_suppress | winsorize(rank(ceiling_field), std) | ceiling |
| discrete_score | group_rank(int_field, group) | integer/spread |
| low_freq_backfill | ts_backfill(low_freq_field, window) | monthly/quarterly |
| analyst_revision | group_rank(ts_delta(vec_avg(cnt)), group) | spread/VECTOR |
| target_price | group_rank(divide(vec_avg(target), close), group) | zero_inflated/VECTOR |
| momentum | ts_delta/ts_rank | spread |
| mean_reversion | reverse(ts_delta/ts_rank) | spread |
| volume_price | ts_corr(price, volume) | spread |
| volatility_premium | divide(signal, ts_std_dev) | spread |
| liquidity_premium | divide(abs(returns), volume) | spread |
| multi_horizon | add(multiply(rank(F_short), w), multiply(rank(F_long), w)) | spread |
| confidence_weighted | multiply(rank(prob), rank(confidence)) | spread |
| free_explore | 兜底 | 不限 |

---

*报告生成时间：{{timestamp}}*
*实验工具：ab_test_framework.py*
*标签系统：skeleton_tags.py v2.0*
