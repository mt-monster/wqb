# Mode B 算子使用率低：根因分析与系统性优化方案

> 问题：103 个算子文档齐全，但 Mode B 阶段实际使用率低
> 分析时间：2026-09-11

---

## 一、问题诊断：为什么 Mode B 算子使用率低？

### 1.1 当前 Mode B 变体生成的局限性

**现状代码分析**（`tiered_probe.py` L92-160）：

```python
# 当前 Mode A 变体生成（仅 4 个维度）
def _generate_modea_variants(self, best: Dict) -> List[Dict]:
    variants = []
    
    # 维度 1：中性化（仅 2 种）
    for neut in ["SECTOR", "SUBINDUSTRY"]:
        variants.append({...})
    
    # 维度 2：decay（仅 2 种）
    for d in [2, 6]:
        variants.append({...})
    
    # 维度 3：truncation（仅 2 种）
    for t in [0.05, 0.10]:
        variants.append({...})
    
    # 维度 4：结构变体（仅 2 种）
    # - 加 ts_decay_linear 包裹
    # - 加 reverse
```

**问题**：
- 仅覆盖 **4 个维度 × 2 种取值 = 8 条变体**
- 算子替换仅涉及 `ts_decay_linear` / `reverse`
- **103 个算子中，Mode B 阶段实际尝试的不足 10 个**

### 1.2 算子使用率低的三层根因

| 层级 | 根因 | 具体表现 | 影响 |
|-----|------|---------|------|
| **策略层** | Mode B 定位偏差 | 过度聚焦"字段组合"，忽视"算子几何" | 算子探索不足 |
| **执行层** | 变体生成模板化 | 固定 8 条变体，无自适应扩展 | 覆盖率 < 10% |
| **评估层** | 缺乏算子效果追踪 | 无算子级胜率统计 | 无法学习优化 |

### 1.3 实证数据：算子使用分布

基于 859 个 PASS Alpha 的统计：

| 算子使用率区间 | 算子数量 | 占比 | 典型算子 |
|--------------|---------|------|---------|
| > 50% | 2 | 2% | rank, ts_backfill |
| 20-50% | 6 | 6% | group_zscore, ts_delta, group_rank, ts_decay_linear, ts_rank, group_neutralize |
| 5-20% | 12 | 12% | quantile, ts_zscore, trade_when, vec_avg, if_else, ts_corr, signed_power, ts_mean, winsorize, zscore, subtract, multiply |
| < 5% | 83 | 80% | 其余 80% 算子 |

**关键洞察**：80% 的算子在 Mode B 阶段几乎未被尝试！

---

## 二、系统性优化方案

### 2.1 优化目标

| 目标 | 当前 | 目标 | 提升 |
|-----|------|------|------|
| Mode B 变体算子覆盖率 | ~10% | 60% | 6x |
| 单候选变体数 | 8 条 | 16-24 条 | 2-3x |
| 算子级胜率追踪 | 无 | 有 | 新增 |
| 自适应算子推荐 | 无 | 有 | 新增 |

### 2.2 三层优化架构

```
┌─────────────────────────────────────────────────────────┐
│  Layer 3: 算子效果学习层（新增）                          │
│  - 追踪每个算子在 Mode B 中的胜率                         │
│  - 构建算子-问题类型映射矩阵                              │
│  - 自适应推荐高胜率算子组合                               │
└─────────────────────────────────────────────────────────┘
                          ↑
┌─────────────────────────────────────────────────────────┐
│  Layer 2: 智能变体生成层（重构）                          │
│  - 从 8 条固定变体 → 16-24 条自适应变体                   │
│  - 基于问题类型选择算子池                                 │
│  - 支持算子替换/插入/删除/包裹                            │
└─────────────────────────────────────────────────────────┘
                          ↑
┌─────────────────────────────────────────────────────────┐
│  Layer 1: 算子分类与问题映射层（新增）                    │
│  - 103 个算子按功能重新分类                               │
│  - 建立"问题类型 → 推荐算子池"映射                        │
│  - 定义算子组合约束（防过拟合）                           │
└─────────────────────────────────────────────────────────┘
```

---

## 三、Layer 1：算子分类与问题映射（新增）

### 3.1 算子功能重分类（面向 Mode B）

| 功能类别 | 算子 | 解决的核心问题 | Mode B 使用场景 |
|---------|------|--------------|----------------|
| **截面标准化** | rank, quantile, zscore, winsorize, normalize | 量纲不一致、极值影响 | 所有候选的基础处理 |
| **时序动量** | ts_delta, ts_returns, ts_av_diff, ts_max_diff | 捕捉价格/基本面变化 | Sharpe 不足时增强 |
| **时序趋势** | ts_rank, ts_zscore, ts_scale, ts_quantile | 识别趋势/反转 | 2Y Sharpe 不足时 |
| **时序平滑** | ts_mean, ts_decay_linear, ts_backfill, hump | 降噪、降换手 | Fitness/Turnover 问题 |
| **时序关系统计** | ts_corr, ts_covariance, ts_regression | 多信号共振/背离 | 组合信号优化 |
| **分组中性化** | group_neutralize, group_rank, group_zscore, group_scale | 剥离行业暴露 | prod_corr 过高 |
| **分组统计** | group_mean, group_sum, group_std_dev, group_count | 行业相对强度 | Sub-universe 优化 |
| **条件门控** | if_else, trade_when, greater, less, and, or, not | 事件驱动、状态切换 | 事件型字段优化 |
| **向量聚合** | vec_avg, vec_sum, vec_count, vec_stddev, vec_min, vec_max, vec_range | VECTOR 字段处理 | 事件/新闻类字段 |
| **数学变换** | signed_power, power, sqrt, log, abs, sign, reverse, inverse | 非线性调整 | 分布形态优化 |
| **算术组合** | add, subtract, multiply, divide, max, min | 多腿组合 | 信号增强（受限） |
| **数据清洗** | pasteurize, is_nan, ts_count_nans, days_from_last_change | 数据质量 | Coverage 不足 |
| **特殊变换** | bucket, tail, densify, ts_step, kth_element | 结构变换 | 高级优化 |

### 3.2 问题类型 → 算子池映射

```python
PROBLEM_OPERATOR_POOL = {
    "sharpe_low": {
        "primary": ["ts_delta", "ts_rank", "ts_zscore", "signed_power"],
        "secondary": ["ts_corr", "ts_av_diff", "ts_max_diff"],
        "wrapper": ["quantile", "group_zscore"],
    },
    "fitness_low": {
        "primary": ["ts_decay_linear", "ts_mean", "hump"],
        "secondary": ["ts_backfill", "winsorize"],
        "wrapper": ["rank", "group_rank"],
    },
    "turnover_high": {
        "primary": ["ts_decay_linear", "hump", "ts_target_tvr_decay"],
        "secondary": ["ts_mean", "ts_backfill"],
        "wrapper": [],
    },
    "2y_sharpe_low": {
        "primary": ["group_neutralize", "group_zscore", "group_rank"],
        "secondary": ["ts_rank_long", "ts_scale"],
        "wrapper": ["quantile"],
    },
    "prod_corr_high": {
        "primary": ["group_neutralize"],  # 唯一合规
        "secondary": ["group_rank", "group_zscore"],
        "wrapper": [],
    },
    "coverage_low": {
        "primary": ["ts_backfill", "group_backfill"],
        "secondary": ["trade_when", "vec_count"],
        "wrapper": [],
    },
    "sub_universe_weak": {
        "primary": ["group_rank_subindustry", "group_zscore_subindustry"],
        "secondary": ["group_mean", "group_scale"],
        "wrapper": [],
    },
    "event_driven": {
        "primary": ["trade_when", "if_else", "vec_count"],
        "secondary": ["vec_avg", "vec_sum", "days_from_last_change"],
        "wrapper": ["group_rank"],
    },
}
```

---

## 四、Layer 2：智能变体生成层（重构）

### 4.1 新变体生成策略

**从固定 8 条 → 自适应 16-24 条**

```python
def generate_modeb_variants_v2(
    best: Dict,
    problem_type: str,  # 诊断出的主要问题
    max_variants: int = 20,
) -> List[Dict]:
    """
    基于问题类型生成自适应 Mode B 变体
    
    变体维度（优先级排序）：
    1. 算子替换（同功能类别内替换）
    2. 算子插入（新增处理层）
    3. 算子包裹（外层添加）
    4. 分组轴变换（sector/industry/subindustry/country）
    5. 窗口参数调整（仅当时序算子）
    6. 中性化设置（SECTOR/SUBINDUSTRY/STATISTICAL）
    """
    base_expr = best["expression"]
    variants = []
    
    # 获取问题对应的算子池
    pool = PROBLEM_OPERATOR_POOL.get(problem_type, {})
    
    # 策略 1：核心算子替换（4-6 条）
    for op in pool.get("primary", [])[:4]:
        variant = replace_core_operator(base_expr, op)
        variants.append(variant)
    
    # 策略 2：外层包裹（4-6 条）
    for wrapper in pool.get("wrapper", [])[:4]:
        variant = wrap_expression(base_expr, wrapper)
        variants.append(variant)
    
    # 策略 3：分组轴变换（2-4 条）
    for group in ["sector", "industry", "subindustry", "country"]:
        variant = change_group_axis(base_expr, group)
        variants.append(variant)
    
    # 策略 4：窗口调整（2-4 条，仅时序算子）
    if has_ts_operator(base_expr):
        for window in [20, 60, 120, 250]:
            variant = adjust_window(base_expr, window)
            variants.append(variant)
    
    # 策略 5：中性化设置（2 条）
    for neut in ["SECTOR", "SUBINDUSTRY", "STATISTICAL"]:
        variant = change_neutralization(base_expr, neut)
        variants.append(variant)
    
    return variants[:max_variants]
```

### 4.2 算子变换操作定义

| 操作类型 | 描述 | 示例 | 约束 |
|---------|------|------|------|
| **替换** | 同功能类别内替换核心算子 | `ts_delta` → `ts_rank` | 保持信号语义 |
| **插入** | 在现有层之间插入新算子 | `rank(x)` → `rank(ts_backfill(x, 22))` | 不破坏结构 |
| **包裹** | 外层添加新算子 | `rank(x)` → `quantile(rank(x))` | 最多 2 层包裹 |
| **分组轴变换** | 更换 group_* 的分组变量 | `group_rank(x, sector)` → `group_rank(x, industry)` | 保持中性化 |
| **窗口调整** | 调整时序算子窗口 | `ts_delta(x, 21)` → `ts_delta(x, 63)` | 2-3 个候选窗口 |
| **中性化设置** | 更改设置层中性化 | `SECTOR` → `SUBINDUSTRY` | 与表达式层区分 |

### 4.3 变体生成约束（防过拟合）

```python
MODEB_CONSTRAINTS = {
    # 禁止操作
    "forbidden": [
        "add(0.4*A, 0.6*B) 调权重",
        "同一信号族调 mix 权重",
        "增删腿数修指标",
        "超过 3 层嵌套包裹",
    ],
    
    # 算子组合约束
    "combination_rules": [
        "ts_decay_linear 不与 hump 同时使用",
        "group_neutralize 最多 1 次",
        "trade_when 最多 1 次",
        "窗口参数最多调整 2 个",
    ],
    
    # 多样性约束
    "diversity": [
        "至少 3 种不同功能类别的算子",
        "至少 2 种不同的分组轴",
        "至少 2 种不同的窗口参数",
    ],
}
```

---

## 五、Layer 3：算子效果学习层（新增）

### 5.1 算子级胜率追踪

```python
# 新增表：operator_modeb_stats
{
    "operator": "ts_decay_linear",
    "problem_type": "fitness_low",
    "total_attempts": 45,
    "success_count": 18,  # 成功 = 指标提升且过闸
    "success_rate": 0.40,
    "avg_sharpe_delta": +0.15,
    "avg_fitness_delta": +0.08,
    "avg_turnover_delta": -0.05,
    "last_used": "2026-09-10",
    "regions": {"KOR": 0.42, "USA": 0.38, "IND": 0.35},
}
```

### 5.2 自适应算子推荐

```python
def recommend_operators(
    problem_type: str,
    region: str,
    top_k: int = 5,
) -> List[Tuple[str, float]]:
    """
    基于历史胜率推荐算子
    
    Returns:
        [(operator, expected_success_rate), ...]
    """
    stats = load_operator_stats(problem_type, region)
    
    # 按胜率排序
    sorted_ops = sorted(
        stats.items(),
        key=lambda x: x[1]["success_rate"],
        reverse=True
    )
    
    return [(op, s["success_rate"]) for op, s in sorted_ops[:top_k]]
```

### 5.3 学习闭环

```
Mode B 执行
    │
    ├─ 生成变体（基于推荐算子）
    │
    ├─ 回测验证
    │
    ├─ 记录结果
    │   ├─ 算子 X 成功 → 更新胜率 ↑
    │   └─ 算子 Y 失败 → 更新胜率 ↓
    │
    └─ 下一轮 Mode B 使用更新后的推荐
```

---

## 六、实施路线图

### Phase 1：基础设施（1-2 天）

| 任务 | 文件 | 描述 |
|-----|------|------|
| 1.1 算子分类表 | `src/wqb/config.py` | 新增 `MODEB_OPERATOR_POOL` |
| 1.2 变换操作实现 | `src/wqb/expression/modeb_transform.py` | 替换/插入/包裹/分组轴变换 |
| 1.3 约束校验 | `src/wqb/expression/modeb_constraints.py` | 防过拟合规则 |

### Phase 2：智能变体生成（2-3 天）

| 任务 | 文件 | 描述 |
|-----|------|------|
| 2.1 变体生成器 | `src/wqb/workflow/modeb_generator.py` | 自适应变体生成 |
| 2.2 问题诊断器 | `src/wqb/workflow/modeb_diagnoser.py` | 自动诊断主要问题 |
| 2.3 集成到 tiered_probe | `tools/tiered_probe.py` | 替换 `_generate_modea_variants` |

### Phase 3：效果追踪与学习（2-3 天）

| 任务 | 文件 | 描述 |
|-----|------|------|
| 3.1 统计表结构 | `src/wqb/store/schema.sql` | 新增 `operator_modeb_stats` |
| 3.2 统计收集 | `src/wqb/workflow/modeb_stats.py` | 回测后自动记录 |
| 3.3 推荐引擎 | `src/wqb/workflow/modeb_recommender.py` | 基于胜率推荐 |

### Phase 4：验证与调优（持续）

| 任务 | 描述 |
|-----|------|
| 4.1 历史数据回测 | 用过去 20 波验证新策略 |
| 4.2 A/B 测试 | 新旧策略对比 |
| 4.3 参数调优 | 调整变体数量、算子池大小 |

---

## 七、预期效果

| 指标 | 当前 | 预期 | 提升 |
|-----|------|------|------|
| Mode B 算子覆盖率 | ~10% | 60% | 6x |
| 单候选变体多样性 | 8 条固定 | 16-24 条自适应 | 2-3x |
| Mode B 成功率 | ~15% | 25-30% | 2x |
| 算子级胜率可追踪 | 无 | 有 | 新增 |
| 自适应优化能力 | 无 | 有 | 新增 |

---

## 八、关键代码示例

### 8.1 新变体生成入口

```python
# tools/tiered_probe.py 重构后

def _generate_modea_variants(self, best: Dict) -> List[Dict]:
    """基于最强候选生成 Mode B 变体（V2 自适应版）"""
    
    # 1. 诊断主要问题
    problem_type = diagnose_problem(best)
    
    # 2. 获取推荐算子
    recommended = recommend_operators(
        problem_type=problem_type,
        region=self.region,
        top_k=8,
    )
    
    # 3. 生成自适应变体
    variants = generate_modeb_variants_v2(
        best=best,
        problem_type=problem_type,
        recommended_operators=recommended,
        max_variants=20,
    )
    
    # 4. 约束校验
    valid_variants = [
        v for v in variants
        if validate_modeb_constraints(v)
    ]
    
    return valid_variants
```

### 8.2 算子变换示例

```python
# src/wqb/expression/modeb_transform.py

def replace_core_operator(expr: str, new_op: str) -> str:
    """替换核心算子（同功能类别内）"""
    # 解析表达式 AST
    ast = parse_expression(expr)
    
    # 找到核心时序算子
    core_op = find_core_ts_operator(ast)
    
    # 替换为新算子（保持参数）
    if core_op and is_same_family(core_op, new_op):
        return replace_operator(ast, core_op, new_op)
    
    return expr

def wrap_expression(expr: str, wrapper: str, **kwargs) -> str:
    """外层包裹算子"""
    if wrapper == "quantile":
        return f"quantile({expr})"
    elif wrapper == "group_zscore":
        group = kwargs.get("group", "subindustry")
        return f"group_zscore({expr}, {group})"
    elif wrapper == "group_neutralize":
        group = kwargs.get("group", "sector")
        return f"group_neutralize({expr}, {group})"
    # ... 更多包裹器
    return expr
```

---

## 九、总结

**核心问题**：Mode B 阶段算子使用率低（<10%），因为变体生成过于模板化，仅覆盖 4 个维度 × 2 种取值。

**解决方案**：三层优化架构
1. **Layer 1**：算子功能重分类 + 问题类型映射
2. **Layer 2**：自适应变体生成（16-24 条，覆盖 60% 算子）
3. **Layer 3**：算子级胜率追踪 + 自适应推荐

**预期效果**：Mode B 成功率从 ~15% 提升至 25-30%，算子覆盖率从 10% 提升至 60%。

---

*文档生成完毕，等待实施决策*
