# S2 候选池生成模板（字段数分层放开版）
# 基于 GLOBAL:field_count_strategy_layered_v1
# 生成时间: 2026-08-28

## 候选池元数据

campaign_region: IND
campaign_wave: {WAVE_NUMBER}
dataset: {DATASET_ID}
strategy_layer: L1_probe | L2_base | L3_combination | L4_composite
field_count: {N}
generation_date: 2026-08-28

---

## 层级准入检查（生成前强制）

### L1_probe 准入
- [ ] 新数据集首探（无历史 campaign 记录）
- [ ] 仅用于 S0/S1 阶段，不进 S2 候选池
- [ ] max 8 表达式，early stop: max |sharpe| < 0.7

### L2_base 准入（默认）
- [ ] 主信号明确（1 字段）
- [ ] 辅助字段仅用于降换手/控风险（非信号增强）
- [ ] 预处理简单：rank(ts_backfill(...)) 或 ts_mean(...)

### L3_combination 准入
- [ ] 单/双字段已证明有效（S>=1.0 或 2y>=1.5）
- [ ] 新增字段提供正交性（周期/逻辑/数据集/信息源）
- [ ] 通过六维多样性审查（见下表）
- [ ] 非禁止组合（同族/同周期/调权重）

### L4_composite 准入
- [ ] L3 验证成功
- [ ] 每新增字段单独论证必要性
- [ ] 新增字段边际贡献 > 0.1 Sharpe
- [ ] max 2 数据集（MEA 硬约束）

---

## 正交性论证（L3/L4 必填）

| 维度 | 本候选正交性说明 | 证据/参考 |
|------|----------------|-----------|
| 周期正交 | 慢变量（___）× 快变量（___） | KOR 评级修正×SH 短周期 |
| 逻辑正交 | 基本面 × 量价 × 事件 × 情绪 | USA long_term+short_term+event_5d |
| 数据集正交 | 跨数据集组合，预估相关性 < 0.4 | 用户强制要求 |
| 信息源正交 | 财报/分析师/新闻/交易 | 避免同信息源多字段 |

**正交性结论**: [ ] 通过 [ ] 不通过（原因：___）

---

## 六维多样性审查（L3/L4 必填）

| 维度 | 本候选覆盖 | 与已有候选差异 | 评估 |
|------|-----------|---------------|------|
| 算子多样性 | ___ | ___ | [ ] 通过 |
| 字段多样性 | ___ | ___ | [ ] 通过 |
| 骨架多样性 | ___ | ___ | [ ] 通过 |
| 预处理多样性 | ___ | ___ | [ ] 通过 |
| 收益来源多样性 | ___ | ___ | [ ] 通过 |
| 失败风险多样性 | ___ | ___ | [ ] 通过 |

**多样性结论**: [ ] 通过 [ ] 不通过（原因：___）

---

## 区域特异性检查（IND 必填）

- [ ] 非 fnd94 + fnd86 组合（信号冲突）
- [ ] 非 fnd94 + mdl28 组合（稀释 IS）
- [ ] 非 fnd94 内部多字段组合
- [ ] 若主信号为 Operating-Margin，已引入正交信号族突破 robust 墙

---

## 候选表达式清单

### 表达式 1
```python
# 层级: L{1|2|3|4}
# 字段数: {N}
# 字段列表: [{field1}, {field2}, ...]
# 正交性说明: {orthogonality_note}
expression = """
{alpha_expression}
"""
settings = {
    "region": "IND",
    "universe": "TOP500",
    "delay": 1,
    "neutralization": "STATISTICAL",
    "decay": {decay},
    "truncation": {truncation},
    "maxTrade": "ON",
    "nanHandling": "ON"
}
```

### 表达式 2
...（同上结构）

---

## 生成后检查（S2→S3 门禁前）

- [ ] 所有表达式过 tools/wave_gate.py 5 闸
- [ ] L3/L4 候选已附正交性论证 + 六维多样性自评
- [ ] 无同族字段组合
- [ ] 无同周期信号互组
- [ ] 无调权重变体（同信号族）

---

## 引用配置

- 通用策略: GLOBAL:field_count_strategy_layered_v1
- 区域调整: tracking/IND/config/thresholds.json → ind_specific_adjustments
