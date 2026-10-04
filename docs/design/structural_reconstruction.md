# 结构重构变体生成与效果追踪

## 概述

针对「修订信号 vs 短期反转」等 **sharpe 与 fitness/2Y 结构性权衡** 问题，本模块提供四种合规重构方案，并建立完整的效果追踪机制。

### 问题背景

当两个独立信号（如分析师修订信号与短期反转信号）简单相加时，会产生结构性冲突：
- **Sharpe 高**：两条信号叠加后收益增强
- **Fitness/2Y 低**：信号对冲导致 turnover 高、长期稳定性差

### 合规约束

根据用户挖掘纪律（记忆 7c2651ad）：
- ❌ 禁止 `add(A,B)` 混信号调参
- ❌ 禁止权重网格扫描（0.4/0.6 → 0.3/0.7）
- ✅ 允许：换字段组合、换信号概念、换算子几何、换分组轴、单信号结构化

## 四种重构策略

### 1. 几何重构（Geometric）- P0 推荐

用 `subtract`/`divide` 替代 `add`，消除权重调参：

| 变体 | 表达式 | 描述 | 预期效果 |
|------|--------|------|----------|
| spread | `subtract(A, B)` | 价差结构 | 消除权重，降低 turnover |
| ratio | `divide(A, add(B, 0.001))` | 比率结构 | 非线性增强 |
| spread_rank | `subtract(rank(A), rank(B))` | 双 rank 价差 | 消除量纲影响 |
| ratio_rank | `divide(rank(A), add(rank(B), 0.001))` | 双 rank 比率 | 结合稳定性与敏感性 |

### 2. 中性化轴切换（Neutralization）- P1

剥离 beta/行业暴露，让两条信号在同一风险维度上：

| 轴 | 表达式 | 适用场景 |
|----|--------|----------|
| country | `group_neut(signal, country)` | EUR/DEU 等多国家区域 |
| sector | `group_neut(signal, sector)` | 行业聚集效应明显 |
| market | `group_neut(signal, market)` | 剥离市场 beta |
| subindustry | `group_neut(signal, subindustry)` | 精准行业剥离 |

### 3. 时间尺度解耦（Temporal）- P2

让两条信号错峰，避免同一时间截面对冲：

| 变体 | 表达式 | 描述 |
|------|--------|------|
| delay_base | `ts_delay(base, 5)` | 基础信号滞后，避开反转期 |
| smooth_base | `ts_mean(base, 20)` | 基础信号平滑，慢变量化 |
| delay_conflict | `ts_delay(conflict, 3)` | 冲突信号滞后 |
| delta_conflict | `ts_delta(conflict, 5)` | 冲突信号差分 |

### 4. 条件触发（Conditional）- P2

基础信号作为过滤器，冲突信号作为触发器：

| 变体 | 表达式 | 描述 |
|------|--------|------|
| quantile_filter | `multiply(ts_quantile(base, 60, 0.8), conflict)` | 分位数过滤 |
| threshold_filter | `multiply(ts_step(base, 0.7), conflict)` | 阈值过滤 |

### 5. 正交化（Orthogonal）- P3

数学上剥离相关性：

| 变体 | 表达式 | 描述 |
|------|--------|------|
| residual | `ts_regression_residual(conflict, base, 20)` | 回归残差 |

## 使用方法

### MCP 工具调用

```python
# 1. 检测结构性冲突
workflow_structural_reconstruct(
    action="detect",
    expression="add(multiply(0.6, rank(revision)), multiply(0.4, rank(reversal)))"
)

# 2. 生成重构变体
workflow_structural_reconstruct(
    action="generate",
    base_signal="rank(anl45_est_revision)",
    conflict_signal="rank(ts_delta(close, 5))",
    region="DEU"
)

# 3. 记录回测结果
workflow_structural_reconstruct(
    action="record",
    region="DEU",
    wave=95,
    variant_id="geo_spread_rank",
    original_expr="add(rank(A), rank(B))",
    variant_expr="subtract(rank(A), rank(B))",
    strategy="geometric",
    alpha_id="abc123",
    metrics={"sharpe": 1.45, "fitness": 0.92, "turnover": 0.15}
)

# 4. 生成对比报告
workflow_structural_reconstruct(
    action="report",
    region="DEU",
    wave=95
)

# 5. 获取策略统计
workflow_structural_reconstruct(
    action="stats",
    region="DEU"
)
```

### CLI 命令

```bash
# 检测冲突
python tools/structural_reconstruct_cli.py detect \
    --expr "add(rank(A), rank(B))"

# 生成变体
python tools/structural_reconstruct_cli.py generate \
    --base "rank(anl45_est_revision)" \
    --conflict "rank(ts_delta(close, 5))" \
    --region DEU \
    --output report.md

# 记录结果
python tools/structural_reconstruct_cli.py record \
    --region DEU --wave 95 \
    --variant-id geo_spread_rank \
    --original "add(rank(A), rank(B))" \
    --variant "subtract(rank(A), rank(B))" \
    --strategy geometric \
    --alpha-id abc123 \
    --sharpe 1.45 --fitness 0.92

# 生成报告
python tools/structural_reconstruct_cli.py report \
    --region DEU --wave 95 \
    --output comparison.md
```

### Python API

```python
from wqb.workflow.structural_variants import StructuralVariantGenerator
from wqb.workflow.structural_variant_tracker import StructuralVariantTracker

# 生成变体
generator = StructuralVariantGenerator()
result = generator.generate(
    base_signal="rank(anl45_est_revision)",
    conflict_signal="rank(ts_delta(close, 5))",
    region="DEU",
)

print(f"推荐变体: {result.recommended.expression}")
print(f"理由: {result.recommended.description}")

# 记录结果
tracker = StructuralVariantTracker(db_path="data/wqb.db")
tracker.record_variant_result(
    region="DEU",
    wave=95,
    variant_id="geo_spread_rank",
    original_expr="add(rank(A), rank(B))",
    variant_expr="subtract(rank(A), rank(B))",
    strategy="geometric",
    alpha_id="abc123",
    metrics={"sharpe": 1.45, "fitness": 0.92},
)

# 生成对比报告
report = tracker.generate_comparison_report("DEU", 95)
print(report)
```

## 效果追踪

### 数据表结构

变体结果存储在 `structural_variant_results` 表：

| 字段 | 类型 | 描述 |
|------|------|------|
| region | VARCHAR | 区域代码 |
| wave_number | INTEGER | 波次号 |
| variant_id | VARCHAR | 变体唯一标识 |
| original_expression | TEXT | 原始表达式 |
| variant_expression | TEXT | 变体表达式 |
| strategy | VARCHAR | 重构策略 |
| alpha_id | VARCHAR | 平台 alpha id |
| metrics | JSON | 回测指标 |
| status | VARCHAR | 状态 |
| created_at | TIMESTAMP | 创建时间 |

### 效果判定标准

| 判定 | 条件 | 建议 |
|------|------|------|
| IMPROVED | sharpe +0.1 或 fitness +0.05 或 turnover -10% | 采用该策略 |
| DEGRADED | sharpe -0.1 或 fitness -0.05 或 turnover +10% | 回退或换策略 |
| MIXED | 正负改进并存 | 需权衡 |
| NO_CHANGE | 改进不显著 | 观察更多样本 |

### 与现有流程集成

```
S2 候选池生成
    ↓
S3 wave_gate 预检
    ↓ (检测到 add(A,B) 模式)
structural_reconstruct generate  ←── 新增节点
    ↓
生成变体并回测
    ↓
structural_reconstruct record  ←── 记录结果
    ↓
S4 评审
    ↓
structural_reconstruct report  ←── 效果对比
    ↓
S6 台账回写
```

## 最佳实践

### 1. 何时使用结构重构

- 当 `add(A,B)` 模式被 wave_gate 拦截时
- 当 sharpe 高但 fitness/2Y 不达标时
- 当 turnover 异常高时

### 2. 策略选择建议

| 场景 | 推荐策略 |
|------|----------|
| 一般情况 | geometric (spread_rank) |
| EUR/DEU 区域 | neutralization (country) |
| 高 turnover | temporal (delay_base) |
| 需要保留双信号 | orthogonal (residual) |

### 3. 效果验证流程

1. 生成 3-5 个变体
2. 小批量回测（每变体 1-2 条）
3. 记录结果到 tracker
4. 对比分析，选择最佳
5. 扩大验证

## 注意事项

1. **合规性**：所有变体均遵守「禁止 add(A,B) 混信号」纪律
2. **样本量**：结构重构需要足够样本验证，建议至少 3 波数据
3. **区域差异**：不同区域可能需要不同策略（EUR 重中性化，USA 重几何）
4. **过拟合风险**：避免在同一数据集上反复尝试不同策略

## 相关文件

- `src/wqb/workflow/structural_variants.py` - 变体生成器
- `src/wqb/workflow/structural_variant_tracker.py` - 效果追踪器
- `src/wqb/workflow/nodes/structural_reconstruct.py` - Workflow 节点
- `tools/structural_reconstruct_cli.py` - CLI 工具
- `tests/unit/test_structural_reconstruct.py` - 单元测试
