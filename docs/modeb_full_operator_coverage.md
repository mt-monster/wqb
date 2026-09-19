# Mode B 全算子覆盖框架：103 个算子的完整变体生成方案

> 目标：确保 103 个算子在 Mode B 阶段都能被合理尝试
> 原则：每个算子都有其适用场景，通过智能路由实现全覆盖
> 生成时间：2026-09-11

---

## 一、全算子覆盖的核心设计

### 1.1 覆盖策略：三层路由机制

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: 全算子轮换层（保底机制）                           │
│  - 确保 103 个算子在 N 波内至少被尝试 1 次                   │
│  - 基于算子使用频率的加权随机选择                             │
│  - 低使用率算子优先提升                                      │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: 场景适配层（智能路由）                             │
│  - 根据字段类型/问题诊断/历史胜率选择算子池                   │
│  - 每个算子都有明确的适用场景标签                             │
│  - 支持多场景组合路由                                        │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: 基础变体层（结构化生成）                           │
│  - 算子替换/插入/包裹/删除/参数调整                           │
│  - 保持表达式结构完整性                                       │
│  - 防过拟合约束校验                                          │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 算子覆盖度目标

| 算子类别 | 数量 | 当前覆盖率 | 目标覆盖率 | 覆盖策略 |
|---------|------|-----------|-----------|---------|
| Arithmetic | 17 | 24% | 100% | 场景路由 + 轮换 |
| Logical | 11 | 18% | 100% | 场景路由 + 轮换 |
| Time Series | 28 | 25% | 100% | 场景路由 + 轮换 |
| Cross Sectional | 7 | 71% | 100% | 场景路由 |
| Vector | 8 | 25% | 100% | 字段类型路由 |
| Transformational | 4 | 50% | 100% | 场景路由 |
| Group | 12 | 42% | 100% | 场景路由 |
| Reduce | 14 | 0% | 100% | COMBO 专用路由 |
| Special | 2 | 0% | 100% | SELECTION 专用路由 |
| **总计** | **103** | **~25%** | **100%** | - |

---

## 二、103 个算子的完整场景映射

### 2.1 Arithmetic 算术算子（17 个）

| 算子 | 适用场景 | 字段类型 | 问题诊断 | 变体操作 | 优先级 |
|-----|---------|---------|---------|---------|-------|
| **add** | 多腿组合增强 | 任意 | sharpe_low / 2y_low | 插入/替换 | P1 |
| **subtract** | 价差信号构建 | 价格/基本面 | sharpe_low / margin_low | 替换核心 | P1 |
| **multiply** | 信号交互确认 | 任意 | sharpe_low / 共振确认 | 插入/替换 | P2 |
| **divide** | 比率信号构建 | 基本面 | sharpe_low / margin_low | 替换核心 | P1 |
| **signed_power** | 非线性调整 | 任意 | sharpe_low / 分布优化 | 包裹/替换 | P2 |
| **power** | 指数调整 | 任意 | sharpe_low / 分布优化 | 包裹/替换 | P3 |
| **sqrt** | 降长尾 | 波动率 | fitness_low / 分布优化 | 包裹 | P3 |
| **log** | 对数变换 | 正偏态 | sharpe_low / 分布优化 | 包裹 | P3 |
| **abs** | 绝对值处理 | 波动率 | 特殊场景 | 包裹 | P4 |
| **sign** | 方向提取 | 任意 | 特殊场景 | 包裹 | P4 |
| **reverse** | 反向信号 | 任意 | 方向反转 | 包裹 | P2 |
| **inverse** | 倒数关系 | 比率 | sharpe_low | 包裹 | P3 |
| **max** | 多信号择优 | 任意 | sharpe_low | 替换组合 | P3 |
| **min** | 风险下限 | 任意 | 特殊场景 | 替换组合 | P4 |
| **pasteurize** | 异常值处理 | 任意 | fitness_low / coverage | 插入 | P2 |
| **densify** | 分组压缩 | 分组字段 | 计算优化 | 插入 | P4 |
| **bucket** | 分桶处理 | 任意 | 分组构建 | 替换/插入 | P3 |

### 2.2 Logical 逻辑算子（11 个）

| 算子 | 适用场景 | 字段类型 | 问题诊断 | 变体操作 | 优先级 |
|-----|---------|---------|---------|---------|-------|
| **if_else** | 条件门控 | 任意 | sharpe_low / 事件驱动 | 包裹/插入 | P1 |
| **trade_when** | 条件交易 | 事件型 | sharpe_low / turnover_high | 包裹/插入 | P1 |
| **greater** | 阈值判断 | 任意 | 条件构建 | 插入条件 | P2 |
| **less** | 阈值判断 | 任意 | 条件构建 | 插入条件 | P2 |
| **greater_equal** | 阈值判断 | 任意 | 条件构建 | 插入条件 | P3 |
| **less_equal** | 阈值判断 | 任意 | 条件构建 | 插入条件 | P3 |
| **equal** | 相等判断 | 分类型 | 状态匹配 | 插入条件 | P3 |
| **not_equal** | 不等判断 | 分类型 | 状态过滤 | 插入条件 | P3 |
| **and** | 逻辑与 | 任意 | 多条件组合 | 插入条件 | P2 |
| **or** | 逻辑或 | 任意 | 多条件组合 | 插入条件 | P2 |
| **not** | 逻辑非 | 任意 | 条件取反 | 插入条件 | P3 |
| **is_nan** | 缺失判断 | 任意 | coverage_low | 插入条件 | P2 |

### 2.3 Time Series 时序算子（28 个）

| 算子 | 适用场景 | 字段类型 | 问题诊断 | 变体操作 | 窗口建议 | 优先级 |
|-----|---------|---------|---------|---------|---------|-------|
| **ts_rank** | 时序动量 | 任意 | sharpe_low / 2y_low | 替换核心 | 20/60/250 | P1 |
| **ts_zscore** | 时序标准化 | 任意 | sharpe_low / 2y_low | 替换核心 | 60/120 | P1 |
| **ts_delta** | 时序差分 | 任意 | sharpe_low | 替换核心 | 5/21/63 | P1 |
| **ts_returns** | 收益率 | 价格 | sharpe_low | 替换核心 | 5/21 | P2 |
| **ts_av_diff** | 偏离均值 | 任意 | sharpe_low | 替换核心 | 20/60 | P2 |
| **ts_max_diff** | 距最大值 | 任意 | sharpe_low | 替换核心 | 20/60 | P3 |
| **ts_scale** | 时序缩放 | 任意 | sharpe_low / fitness | 替换核心 | 60/120 | P2 |
| **ts_quantile** | 时序分位 | 任意 | sharpe_low / 2y_low | 替换核心 | 60/120 | P2 |
| **ts_mean** | 时序平均 | 任意 | fitness_low / turnover | 替换核心 | 20/60 | P1 |
| **ts_std_dev** | 时序波动 | 任意 | sharpe_low | 插入/包裹 | 20/60 | P2 |
| **ts_sum** | 时序求和 | 任意 | sharpe_low | 替换核心 | 5/20 | P3 |
| **ts_product** | 时序乘积 | 任意 | sharpe_low | 替换核心 | 5/20 | P3 |
| **ts_kurtosis** | 峰度 | 任意 | sharpe_low | 插入/包裹 | 60/120 | P4 |
| **ts_ir** | 信息比率 | 任意 | sharpe_low | 替换核心 | 60/120 | P3 |
| **ts_decay_linear** | 线性衰减 | 任意 | fitness_low / turnover | 包裹/插入 | 10/21 | P1 |
| **ts_backfill** | 缺失填充 | 低覆盖 | coverage_low | 插入 | 22/66 | P1 |
| **ts_delay** | 时滞 | 任意 | sharpe_low | 插入 | 1/5 | P2 |
| **ts_corr** | 时序相关 | 任意 | sharpe_low / 共振 | 插入/包裹 | 20/60 | P2 |
| **ts_covariance** | 协方差 | 任意 | sharpe_low | 插入/包裹 | 20/60 | P3 |
| **ts_regression** | 回归 | 任意 | sharpe_low | 插入/包裹 | 60/120 | P3 |
| **ts_arg_max** | 最大值位置 | 任意 | sharpe_low | 插入/包裹 | 20/60 | P4 |
| **ts_arg_min** | 最小值位置 | 任意 | sharpe_low | 插入/包裹 | 20/60 | P4 |
| **days_from_last_change** | 距变化天数 | 事件型 | sharpe_low | 插入/包裹 | - | P3 |
| **last_diff_value** | 最近不同值 | 任意 | sharpe_low | 插入/包裹 | 20/60 | P4 |
| **ts_step** | 日计数器 | 任意 | 特殊场景 | 插入 | - | P4 |
| **ts_count_nans** | 缺失计数 | 任意 | coverage_low | 插入条件 | 20/60 | P3 |
| **kth_element** | 第k元素 | 任意 | sharpe_low | 插入/包裹 | 20/60 | P4 |
| **hump** | 变化限制 | 任意 | turnover_high | 包裹 | 0.01/0.05 | P2 |
| **ts_target_tvr_decay** | 目标换手 | 任意 | turnover_high | 包裹 | target=0.1 | P2 |
| **ts_target_tvr_hump** | 目标换手 | 任意 | turnover_high | 包裹 | target=0.1 | P2 |

### 2.4 Cross Sectional 截面算子（7 个）

| 算子 | 适用场景 | 字段类型 | 问题诊断 | 变体操作 | 优先级 |
|-----|---------|---------|---------|---------|-------|
| **rank** | 截面排名 | 任意 | 基础处理 | 替换/包裹 | P0 |
| **quantile** | 分位变换 | 任意 | sharpe_low / 2y_low | 包裹 | P1 |
| **zscore** | 截面标准化 | 任意 | sharpe_low | 替换/包裹 | P2 |
| **winsorize** | 缩尾 | 任意 | fitness_low / 极值 | 插入 | P2 |
| **normalize** | 中心化 | 任意 | sharpe_low | 替换/包裹 | P3 |
| **scale** | 缩放 | 任意 | 设置层 | 设置调整 | P3 |
| **vector_neut** | 向量正交 | 任意 | sharpe_low | 插入 | P4 |

### 2.5 Vector 向量算子（8 个）

| 算子 | 适用场景 | 字段类型 | 问题诊断 | 变体操作 | 优先级 |
|-----|---------|---------|---------|---------|-------|
| **vec_avg** | 向量均值 | VECTOR | 基础处理 | 替换核心 | P0 |
| **vec_sum** | 向量求和 | VECTOR | sharpe_low | 替换核心 | P2 |
| **vec_count** | 元素计数 | VECTOR | sharpe_low / 事件 | 替换核心/插入 | P1 |
| **vec_min** | 向量最小 | VECTOR | sharpe_low | 替换核心 | P3 |
| **vec_max** | 向量最大 | VECTOR | sharpe_low | 替换核心 | P3 |
| **vec_stddev** | 向量标准差 | VECTOR | sharpe_low | 替换核心 | P3 |
| **vec_range** | 向量极差 | VECTOR | sharpe_low | 替换核心 | P3 |

### 2.6 Transformational 变换算子（4 个）

| 算子 | 适用场景 | 字段类型 | 问题诊断 | 变体操作 | 优先级 |
|-----|---------|---------|---------|---------|-------|
| **trade_when** | 条件交易 | 事件型 | sharpe_low / turnover | 包裹/插入 | P1 |
| **bucket** | 分桶 | 任意 | 分组构建 | 替换/插入 | P3 |
| **tail** | 尾部处理 | 任意 | fitness_low | 插入 | P4 |
| **generate_stats** | 统计生成 | COMBO | 特殊场景 | 替换 | P4 |

### 2.7 Group 分组算子（12 个）

| 算子 | 适用场景 | 字段类型 | 问题诊断 | 变体操作 | 分组轴 | 优先级 |
|-----|---------|---------|---------|---------|-------|-------|
| **group_neutralize** | 组内中性化 | 任意 | prod_corr_high / 2y_low | 包裹 | sector/industry | P1 |
| **group_rank** | 组内排名 | 任意 | sharpe_low / 2y_low | 替换/包裹 | industry/subindustry | P1 |
| **group_zscore** | 组内标准化 | 任意 | sharpe_low / 2y_low | 替换/包裹 | industry/subindustry | P1 |
| **group_scale** | 组内缩放 | 任意 | sharpe_low | 替换/包裹 | sector | P2 |
| **group_mean** | 组内均值 | 任意 | sharpe_low | 插入/包裹 | sector/industry | P2 |
| **group_sum** | 组内求和 | 任意 | sharpe_low | 插入/包裹 | sector/country | P3 |
| **group_count** | 组内计数 | 任意 | coverage | 插入条件 | - | P3 |
| **group_std_dev** | 组内标准差 | 任意 | sharpe_low | 插入/包裹 | sector | P3 |
| **group_backfill** | 组内填充 | 低覆盖 | coverage_low | 插入 | sector/industry | P2 |
| **group_cartesian_product** | 分组笛卡尔积 | 分组字段 | 高级场景 | 插入 | - | P4 |
| **combo_a** | Alpha组合 | COMBO | 特殊场景 | 替换 | - | P4 |

### 2.8 Reduce 归约算子（14 个，COMBO 专用）

| 算子 | 适用场景 | 变体操作 | 优先级 |
|-----|---------|---------|-------|
| **reduce_avg** | Alpha 组合平均 | 替换核心 | P2 |
| **reduce_stddev** | 组合标准差 | 替换核心 | P3 |
| **reduce_ir** | 信息比率 | 替换核心 | P2 |
| **reduce_max** | 最大值 | 替换核心 | P3 |
| **reduce_min** | 最小值 | 替换核心 | P3 |
| **reduce_sum** | 求和 | 替换核心 | P3 |
| **reduce_norm** | 绝对和 | 替换核心 | P4 |
| **reduce_range** | 极差 | 替换核心 | P4 |
| **reduce_percentage** | 分位数 | 替换核心 | P3 |
| **reduce_skewness** | 偏度 | 替换核心 | P4 |
| **reduce_kurtosis** | 峰度 | 替换核心 | P4 |
| **reduce_count** | 计数 | 替换核心 | P4 |
| **reduce_choose** | 选择 | 替换核心 | P4 |
| **reduce_powersum** | 幂和 | 替换核心 | P4 |

### 2.9 Special 特殊算子（2 个，SELECTION 专用）

| 算子 | 适用场景 | 变体操作 | 优先级 |
|-----|---------|---------|-------|
| **in** | 集合成员 | 替换核心 | P3 |
| **universe_size** | 宇宙大小 | 插入条件 | P3 |

---

## 三、全算子覆盖的智能路由算法

### 3.1 路由决策树

```python
def route_operator(
    candidate: Dict,
    problem_type: str,
    field_type: str,
    wave_number: int,
    operator_stats: Dict,
) -> List[str]:
    """
    全算子覆盖的智能路由
    
    Returns:
        推荐算子列表（按优先级排序）
    """
    recommended = []
    
    # Step 1: 基于问题诊断的算子池
    problem_pool = PROBLEM_OPERATOR_POOL.get(problem_type, {})
    recommended.extend(problem_pool.get("primary", []))
    
    # Step 2: 基于字段类型的算子池
    if field_type == "VECTOR":
        recommended.extend(["vec_avg", "vec_sum", "vec_count", "vec_stddev"])
    elif field_type == "EVENT":
        recommended.extend(["trade_when", "vec_count", "days_from_last_change"])
    
    # Step 3: 基于历史胜率的算子推荐
    high_winrate_ops = get_high_winrate_operators(
        problem_type, operator_stats, top_k=5
    )
    recommended.extend(high_winrate_ops)
    
    # Step 4: 全算子轮换（保底机制）
    # 确保低使用率算子有机会被尝试
    all_ops = get_all_operators()
    used_ops = set(operator_stats.keys())
    unused_ops = [op for op in all_ops if op not in used_ops]
    
    # 按使用率排序，优先推荐低使用率算子
    sorted_unused = sorted(
        unused_ops,
        key=lambda x: operator_stats.get(x, {}).get("usage_count", 0)
    )
    
    # 每波至少尝试 2 个新算子
    recommended.extend(sorted_unused[:2])
    
    # 去重并排序
    return deduplicate_and_sort(recommended, operator_stats)
```

### 3.2 算子使用频率追踪

```python
class OperatorUsageTracker:
    """算子使用频率追踪器"""
    
    def __init__(self):
        self.usage_count = {}  # {operator: count}
        self.success_count = {}  # {operator: success_count}
        self.last_used_wave = {}  # {operator: wave_number}
    
    def get_usage_rate(self, operator: str) -> float:
        """获取算子使用率"""
        total = sum(self.usage_count.values())
        return self.usage_count.get(operator, 0) / max(total, 1)
    
    def get_success_rate(self, operator: str) -> float:
        """获取算子胜率"""
        used = self.usage_count.get(operator, 0)
        success = self.success_count.get(operator, 0)
        return success / max(used, 1)
    
    def should_boost(self, operator: str, current_wave: int) -> bool:
        """判断是否应该提升该算子的使用优先级"""
        # 条件 1：使用率低于平均值
        avg_usage = sum(self.usage_count.values()) / max(len(self.usage_count), 1)
        low_usage = self.usage_count.get(operator, 0) < avg_usage * 0.5
        
        # 条件 2：长时间未使用
        last_wave = self.last_used_wave.get(operator, 0)
        long_unused = (current_wave - last_wave) > 5
        
        return low_usage or long_unused
```

---

## 四、全算子覆盖的变体生成器

### 4.1 完整变体生成流程

```python
def generate_full_coverage_variants(
    best: Dict,
    problem_type: str,
    field_type: str,
    wave_number: int,
    operator_tracker: OperatorUsageTracker,
    max_variants: int = 24,
) -> List[Dict]:
    """
    全算子覆盖的 Mode B 变体生成
    
    变体分配：
    - 40% 基于问题诊断的算子（8-10 条）
    - 30% 基于字段类型的算子（6-8 条）
    - 20% 基于历史胜率的算子（4-6 条）
    - 10% 全算子轮换的新算子（2-3 条）
    """
    base_expr = best["expression"]
    variants = []
    
    # 获取推荐算子
    recommended_ops = route_operator(
        candidate=best,
        problem_type=problem_type,
        field_type=field_type,
        wave_number=wave_number,
        operator_stats=operator_tracker.usage_count,
    )
    
    # 分配变体配额
    quotas = {
        "problem_based": int(max_variants * 0.4),
        "field_based": int(max_variants * 0.3),
        "winrate_based": int(max_variants * 0.2),
        "rotation": max_variants - int(max_variants * 0.9),
    }
    
    # 生成变体
    variant_id = 0
    
    # 1. 问题诊断算子变体
    for op in recommended_ops[:quotas["problem_based"]]:
        variant = create_variant(base_expr, op, variant_id, "problem")
        variants.append(variant)
        variant_id += 1
    
    # 2. 字段类型算子变体
    field_ops = get_field_type_operators(field_type)
    for op in field_ops[:quotas["field_based"]]:
        variant = create_variant(base_expr, op, variant_id, "field")
        variants.append(variant)
        variant_id += 1
    
    # 3. 高胜率算子变体
    high_winrate_ops = operator_tracker.get_high_winrate_operators(top_k=quotas["winrate_based"])
    for op in high_winrate_ops:
        variant = create_variant(base_expr, op, variant_id, "winrate")
        variants.append(variant)
        variant_id += 1
    
    # 4. 全算子轮换变体（保底）
    rotation_ops = operator_tracker.get_rotation_candidates(
        all_operators=get_all_operators(),
        count=quotas["rotation"],
    )
    for op in rotation_ops:
        variant = create_variant(base_expr, op, variant_id, "rotation")
        variants.append(variant)
        variant_id += 1
    
    return variants
```

### 4.2 算子变换操作全集

```python
OPERATOR_TRANSFORMS = {
    # 替换操作
    "replace": {
        "description": "替换核心算子",
        "applicable": ["ts_*", "group_*", "vec_*", "rank", "zscore", "quantile"],
        "constraint": "同功能类别内替换",
    },
    
    # 包裹操作
    "wrap": {
        "description": "外层包裹算子",
        "applicable": ["quantile", "group_*", "signed_power", "reverse", "winsorize"],
        "constraint": "最多 2 层包裹",
    },
    
    # 插入操作
    "insert": {
        "description": "插入新处理层",
        "applicable": ["ts_backfill", "ts_decay_linear", "pasteurize", "is_nan"],
        "constraint": "不破坏现有结构",
    },
    
    # 条件插入
    "condition": {
        "description": "插入条件门控",
        "applicable": ["if_else", "trade_when", "greater", "less", "and", "or"],
        "constraint": "最多 1 个条件层",
    },
    
    # 参数调整
    "param": {
        "description": "调整算子参数",
        "applicable": ["ts_*", "hump", "winsorize"],
        "constraint": "2-3 个候选参数",
    },
    
    # 分组轴变换
    "group_axis": {
        "description": "变换分组轴",
        "applicable": ["group_*"],
        "constraint": "sector/industry/subindustry/country",
    },
}
```

---

## 五、实施代码框架

### 5.1 核心数据结构

```python
# src/wqb/modeb/operator_catalog.py

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class OperatorCategory(Enum):
    ARITHMETIC = "arithmetic"
    LOGICAL = "logical"
    TIME_SERIES = "time_series"
    CROSS_SECTIONAL = "cross_sectional"
    VECTOR = "vector"
    TRANSFORMATIONAL = "transformational"
    GROUP = "group"
    REDUCE = "reduce"
    SPECIAL = "special"

class TransformType(Enum):
    REPLACE = "replace"
    WRAP = "wrap"
    INSERT = "insert"
    CONDITION = "condition"
    PARAM = "param"
    GROUP_AXIS = "group_axis"

@dataclass
class OperatorInfo:
    name: str
    category: OperatorCategory
    scope: List[str]  # REGULAR, COMBO, SELECTION
    applicable_fields: List[str]  # MATRIX, VECTOR, EVENT, GROUP
    problem_types: List[str]  # sharpe_low, fitness_low, etc.
    transform_types: List[TransformType]
    default_params: Dict
    priority: int  # 0-4, 0=highest
    constraint: Optional[str] = None

# 103 个算子的完整目录
OPERATOR_CATALOG: Dict[str, OperatorInfo] = {
    # Arithmetic
    "add": OperatorInfo(
        name="add",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "2y_low"],
        transform_types=[TransformType.INSERT, TransformType.REPLACE],
        default_params={},
        priority=1,
        constraint="禁止 add(0.4*A, 0.6*B) 调权重",
    ),
    # ... 其他 102 个算子定义
}
```

### 5.2 变体生成器

```python
# src/wqb/modeb/variant_generator.py

from typing import List, Dict
from .operator_catalog import OPERATOR_CATALOG, TransformType
from .usage_tracker import OperatorUsageTracker

class FullCoverageVariantGenerator:
    """全算子覆盖的 Mode B 变体生成器"""
    
    def __init__(self, tracker: OperatorUsageTracker):
        self.tracker = tracker
        self.catalog = OPERATOR_CATALOG
    
    def generate(
        self,
        best: Dict,
        problem_type: str,
        field_type: str,
        wave_number: int,
        max_variants: int = 24,
    ) -> List[Dict]:
        """生成全算子覆盖的变体"""
        
        # 1. 获取候选算子池
        candidates = self._get_operator_candidates(
            problem_type, field_type, wave_number
        )
        
        # 2. 分配变体配额
        quotas = self._allocate_quotas(candidates, max_variants)
        
        # 3. 生成变体
        variants = []
        for op_name, quota in quotas.items():
            op_info = self.catalog[op_name]
            for i in range(quota):
                variant = self._create_variant(
                    best["expression"],
                    op_info,
                    variant_id=len(variants),
                )
                if variant:
                    variants.append(variant)
        
        return variants[:max_variants]
    
    def _get_operator_candidates(
        self,
        problem_type: str,
        field_type: str,
        wave_number: int,
    ) -> List[str]:
        """获取候选算子列表"""
        candidates = []
        
        # 基于问题类型
        for op_name, op_info in self.catalog.items():
            if problem_type in op_info.problem_types:
                candidates.append(op_name)
        
        # 基于字段类型
        for op_name, op_info in self.catalog.items():
            if field_type in op_info.applicable_fields:
                candidates.append(op_name)
        
        # 全算子轮换（保底）
        all_ops = list(self.catalog.keys())
        underused = self.tracker.get_underused_operators(all_ops)
        candidates.extend(underused[:3])  # 至少尝试 3 个低使用率算子
        
        return list(dict.fromkeys(candidates))  # 去重
    
    def _allocate_quotas(
        self,
        candidates: List[str],
        max_variants: int,
    ) -> Dict[str, int]:
        """分配变体配额"""
        quotas = {}
        
        # 按优先级分配
        sorted_candidates = sorted(
            candidates,
            key=lambda x: (
                self.catalog[x].priority,
                -self.tracker.get_success_rate(x),
            )
        )
        
        # 高优先级算子分配更多配额
        for i, op_name in enumerate(sorted_candidates):
            if i < 5:
                quotas[op_name] = 3  # 前 5 个各 3 条
            elif i < 10:
                quotas[op_name] = 2  # 6-10 各 2 条
            else:
                quotas[op_name] = 1  # 其余各 1 条
        
        return quotas
    
    def _create_variant(
        self,
        base_expr: str,
        op_info: OperatorInfo,
        variant_id: int,
    ) -> Optional[Dict]:
        """创建单个变体"""
        # 根据算子类型选择变换方式
        for transform_type in op_info.transform_types:
            if transform_type == TransformType.REPLACE:
                new_expr = self._replace_operator(base_expr, op_info)
            elif transform_type == TransformType.WRAP:
                new_expr = self._wrap_operator(base_expr, op_info)
            elif transform_type == TransformType.INSERT:
                new_expr = self._insert_operator(base_expr, op_info)
            else:
                continue
            
            if new_expr and new_expr != base_expr:
                return {
                    "id": f"V{variant_id}",
                    "expression": new_expr,
                    "operator": op_info.name,
                    "transform": transform_type.value,
                    "note": f"{op_info.name} {transform_type.value}",
                }
        
        return None
```

---

## 六、覆盖度验证

### 6.1 覆盖度检查清单

| 检查项 | 验证方法 | 通过标准 |
|-------|---------|---------|
| 算子目录完整性 | 对比平台 get_operators | 103 个算子全收录 |
| 场景映射完整性 | 检查每个算子的 problem_types | 每个算子至少 1 个场景 |
| 变换操作完整性 | 检查每个算子的 transform_types | 每个算子至少 1 种变换 |
| 轮换机制有效性 | 模拟 10 波 Mode B | 低使用率算子被尝试 |
| 约束校验有效性 | 检查 forbidden 规则 | 违规变体被拦截 |

### 6.2 覆盖度统计报表

```python
def generate_coverage_report(
    tracker: OperatorUsageTracker,
    waves: int = 10,
) -> Dict:
    """生成算子覆盖度统计报表"""
    
    all_ops = get_all_operators()
    
    report = {
        "total_operators": len(all_ops),
        "used_operators": len(tracker.usage_count),
        "coverage_rate": len(tracker.usage_count) / len(all_ops),
        "by_category": {},
        "underused": [],
        "never_used": [],
    }
    
    for op in all_ops:
        category = get_operator_category(op)
        usage = tracker.usage_count.get(op, 0)
        
        if category not in report["by_category"]:
            report["by_category"][category] = {
                "total": 0,
                "used": 0,
                "coverage": 0,
            }
        
        report["by_category"][category]["total"] += 1
        if usage > 0:
            report["by_category"][category]["used"] += 1
        
        if usage == 0:
            report["never_used"].append(op)
        elif usage < waves * 0.5:
            report["underused"].append(op)
    
    for cat in report["by_category"]:
        cat_data = report["by_category"][cat]
        cat_data["coverage"] = cat_data["used"] / cat_data["total"]
    
    return report
```

---

## 七、总结

### 7.1 全算子覆盖的关键机制

| 机制 | 描述 | 效果 |
|-----|------|------|
| **场景路由** | 每个算子映射到具体问题场景 | 确保算子在合适场景被尝试 |
| **字段类型路由** | VECTOR/EVENT 字段触发对应算子 | 确保字段类型匹配 |
| **胜率推荐** | 基于历史胜率推荐高潜力算子 | 提高成功率 |
| **全算子轮换** | 低使用率算子优先提升 | 确保 100% 覆盖 |
| **配额分配** | 按优先级分配变体数量 | 平衡探索与利用 |

### 7.2 预期覆盖效果

| 指标 | 当前 | 目标 | 机制 |
|-----|------|------|------|
| 算子覆盖率 | ~25% | 100% | 全算子轮换 |
| 场景匹配率 | ~40% | 90% | 场景路由 |
| 变体多样性 | 8 条固定 | 24 条自适应 | 配额分配 |
| 低使用率算子提升 | 无 | 每波 2-3 个 | 轮换机制 |

### 7.3 实施优先级

| Phase | 内容 | 算子覆盖 |
|-------|------|---------|
| P0 | 核心算子（rank, ts_*, group_*） | 30 个 |
| P1 | 高频算子（quantile, vec_*, if_else） | 50 个 |
| P2 | 中频算子（signed_power, ts_corr, winsorize） | 75 个 |
| P3 | 低频算子（reduce_*, special） | 103 个 |

---

*全算子覆盖框架设计完毕，103 个算子全部纳入 Mode B 变体生成范围*
