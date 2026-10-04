# 结构重构集成方案总结

## 已完成的工作

### 1. 核心模块

| 模块 | 路径 | 功能 |
|------|------|------|
| 变体生成器 | `src/wqb/workflow/structural_variants.py` | 生成四种策略的重构变体 |
| 效果追踪器 | `src/wqb/workflow/structural_variant_tracker.py` | 记录与对比变体效果 |
| Workflow 节点 | `src/wqb/workflow/nodes/structural_reconstruct.py` | 集成到 workflow 引擎 |
| CLI 工具 | `tools/structural_reconstruct_cli.py` | 命令行接口 |
| MCP 工具 | `world-quant-brain-mcp/tools_workflow.py` | MCP 服务接口 |

### 2. 四种重构策略

| 策略 | 优先级 | 核心思想 | 适用场景 |
|------|--------|----------|----------|
| **geometric** | P0 | subtract/divide 替代 add | 一般情况首选 |
| **neutralization** | P1 | 切换中性化轴剥离 beta | EUR/DEU 等多国家区域 |
| **temporal** | P2 | 时间尺度解耦错峰 | 高 turnover 场景 |
| **orthogonal** | P3 | 回归残差数学正交 | 需保留双信号时 |
| **conditional** | P2 | 条件触发过滤器 | 精准控制信号激活 |

### 3. 合规性保障

所有生成的变体均遵守用户挖掘纪律：
- ❌ 禁止 `add(A,B)` 混信号调参
- ❌ 禁止权重网格扫描
- ✅ 使用 `subtract`/`divide` 等结构化算子
- ✅ 换字段组合、换信号概念、换算子几何、换分组轴

## 使用流程

### 场景：DEU 区域 predictive_starmine 数据集

**问题**：修订信号与短期反转信号相加导致 sharpe 高但 fitness/2Y 低

**解决步骤**：

```bash
# 1. 检测结构性冲突
python tools/structural_reconstruct_cli.py detect \
    --expr "add(multiply(0.6, rank(revision)), multiply(0.4, rank(reversal)))"

# 输出: [WARN] 检测到结构性冲突模式 (weighted_add_func)

# 2. 生成重构变体
python tools/structural_reconstruct_cli.py generate \
    --base "rank(anl45_est_revision)" \
    --conflict "rank(ts_delta(close, 5))" \
    --region DEU \
    --output variants.md

# 输出: 25 个变体，推荐 geometric/spread_rank

# 3. 选择变体进行回测（通过现有 pipeline）
# ... 回测 subtract(rank(revision), rank(reversal)) ...

# 4. 记录回测结果
python tools/structural_reconstruct_cli.py record \
    --region DEU --wave 95 \
    --variant-id geo_spread_rank \
    --original "add(rank(revision), rank(reversal))" \
    --variant "subtract(rank(revision), rank(reversal))" \
    --strategy geometric \
    --alpha-id abc123 \
    --sharpe 1.45 --fitness 0.92 --turnover 0.15

# 5. 生成对比报告
python tools/structural_reconstruct_cli.py report \
    --region DEU --wave 95 \
    --output comparison.md
```

### MCP 工具调用

```python
# 在 Agent 中直接调用
workflow_structural_reconstruct(
    action="generate",
    base_signal="rank(anl45_est_revision)",
    conflict_signal="rank(ts_delta(close, 5))",
    region="DEU"
)
```

## 效果追踪机制

### 数据库表

```sql
CREATE TABLE structural_variant_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region VARCHAR(50) NOT NULL,
    wave_number INTEGER NOT NULL,
    variant_id VARCHAR(100) NOT NULL,
    original_expression TEXT NOT NULL,
    variant_expression TEXT NOT NULL,
    strategy VARCHAR(50) NOT NULL,
    alpha_id VARCHAR(100),
    metrics JSON,
    status VARCHAR(20) DEFAULT 'pending',
    error TEXT,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(region, wave_number, variant_id)
);
```

### 效果判定

| 判定 | 条件 | 行动 |
|------|------|------|
| IMPROVED | sharpe +0.1 或 fitness +0.05 或 turnover -10% | 采用该策略 |
| DEGRADED | sharpe -0.1 或 fitness -0.05 或 turnover +10% | 回退或换策略 |
| MIXED | 正负改进并存 | 需权衡 |
| NO_CHANGE | 改进不显著 | 观察更多样本 |

## 与现有流程集成

```
┌─────────────────────────────────────────────────────────────┐
│  S2 候选池生成 (GEM)                                         │
│     ↓                                                       │
│  S3 wave_gate 预检                                           │
│     ↓ (检测到 add(A,B) 模式)                                 │
│  ┌─────────────────────────────┐                            │
│  │ structural_reconstruct      │  ← 新增节点                 │
│  │   action="detect"           │                            │
│  └─────────────────────────────┘                            │
│     ↓                                                       │
│  ┌─────────────────────────────┐                            │
│  │ structural_reconstruct      │                            │
│  │   action="generate"         │                            │
│  └─────────────────────────────┘                            │
│     ↓                                                       │
│  生成变体并回测 (batch_track)                                 │
│     ↓                                                       │
│  ┌─────────────────────────────┐                            │
│  │ structural_reconstruct      │                            │
│  │   action="record"           │                            │
│  └─────────────────────────────┘                            │
│     ↓                                                       │
│  S4 评审 (judge)                                             │
│     ↓                                                       │
│  ┌─────────────────────────────┐                            │
│  │ structural_reconstruct      │                            │
│  │   action="report"           │                            │
│  └─────────────────────────────┘                            │
│     ↓                                                       │
│  S6 台账回写 (wave_results)                                   │
└─────────────────────────────────────────────────────────────┘
```

## 测试验证

- ✅ 13 个单元测试全部通过
- ✅ CLI 工具功能正常
- ✅ Workflow 节点注册成功
- ✅ MCP 工具接口可用

## 后续建议

1. **在 wave_gate 中集成自动检测**：当检测到 add(A,B) 模式时，自动建议结构重构
2. **建立策略效果数据库**：积累各区域/数据集的策略效果数据，优化推荐算法
3. **与 Mode B 优化联动**：结构重构作为 Mode B 的一种合规改进方向
4. **定期回顾**：每月回顾结构重构案例，提炼最佳实践

## 相关文档

- [结构重构详细文档](docs/structural_reconstruction.md)
- [用户挖掘纪律](memory/7c2651ad) - 禁止 add(A,B) 混信号
- [Mode B 资格线](memory/ff6c911a) - sharpe≥1.25 且 fitness≥0.8
