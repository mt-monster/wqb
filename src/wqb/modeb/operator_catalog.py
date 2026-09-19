# -*- coding: utf-8 -*-
"""Mode B 算子目录：103 个算子的完整定义.

每个算子包含：分类、适用场景、字段类型、问题诊断、变换操作、优先级、约束.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class OperatorCategory(Enum):
    """算子分类."""
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
    """变换操作类型."""
    REPLACE = "replace"      # 替换核心算子
    WRAP = "wrap"            # 外层包裹
    INSERT = "insert"        # 插入新层
    CONDITION = "condition"  # 条件门控
    PARAM = "param"          # 参数调整
    GROUP_AXIS = "group_axis"  # 分组轴变换


@dataclass
class OperatorInfo:
    """算子信息."""
    name: str
    category: OperatorCategory
    scope: List[str]  # REGULAR, COMBO, SELECTION
    applicable_fields: List[str]  # MATRIX, VECTOR, EVENT, GROUP
    problem_types: List[str]  # sharpe_low, fitness_low, turnover_high, etc.
    transform_types: List[TransformType]
    default_params: Dict = field(default_factory=dict)
    priority: int = 2  # 0=highest, 4=lowest
    constraint: Optional[str] = None
    description: str = ""


# ============================================================================
# Phase 0: 核心算子（30 个）- 最高频使用
# ============================================================================

_CORE_OPERATORS = {
    # Cross Sectional (7)
    "rank": OperatorInfo(
        name="rank",
        category=OperatorCategory.CROSS_SECTIONAL,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "fitness_low", "base_processing"],
        transform_types=[TransformType.REPLACE, TransformType.WRAP],
        default_params={"rate": 2},
        priority=0,
        description="截面排名，最基础的标准化算子",
    ),
    "quantile": OperatorInfo(
        name="quantile",
        category=OperatorCategory.CROSS_SECTIONAL,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "2y_low", "distribution"],
        transform_types=[TransformType.WRAP],
        default_params={"driver": "gaussian", "sigma": 1.0},
        priority=1,
        description="分位变换，减少极值影响",
    ),
    "zscore": OperatorInfo(
        name="zscore",
        category=OperatorCategory.CROSS_SECTIONAL,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.REPLACE, TransformType.WRAP],
        priority=2,
        description="截面标准化",
    ),
    "winsorize": OperatorInfo(
        name="winsorize",
        category=OperatorCategory.CROSS_SECTIONAL,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["fitness_low", "outlier"],
        transform_types=[TransformType.INSERT],
        default_params={"std": 4},
        priority=2,
        constraint="EVENT 字段禁用",
        description="缩尾处理，去极值",
    ),
    "normalize": OperatorInfo(
        name="normalize",
        category=OperatorCategory.CROSS_SECTIONAL,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.REPLACE, TransformType.WRAP],
        priority=3,
        description="中心化",
    ),
    "scale": OperatorInfo(
        name="scale",
        category=OperatorCategory.CROSS_SECTIONAL,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["setting_adjust"],
        transform_types=[TransformType.PARAM],
        priority=3,
        description="缩放",
    ),
    "vector_neut": OperatorInfo(
        name="vector_neut",
        category=OperatorCategory.CROSS_SECTIONAL,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.INSERT],
        priority=4,
        description="向量正交",
    ),

    # Time Series - 核心 (10)
    "ts_rank": OperatorInfo(
        name="ts_rank",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "2y_low", "momentum"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 60, "constant": 0},
        priority=1,
        description="时序排名，动量/反转",
    ),
    "ts_zscore": OperatorInfo(
        name="ts_zscore",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "2y_low"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 60},
        priority=1,
        description="时序标准化",
    ),
    "ts_delta": OperatorInfo(
        name="ts_delta",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "momentum"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 21},
        priority=1,
        description="时序差分，捕捉变化",
    ),
    "ts_mean": OperatorInfo(
        name="ts_mean",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["fitness_low", "turnover_high", "smoothing"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 20},
        priority=1,
        description="时序平均，降噪",
    ),
    "ts_decay_linear": OperatorInfo(
        name="ts_decay_linear",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["fitness_low", "turnover_high"],
        transform_types=[TransformType.WRAP, TransformType.INSERT, TransformType.PARAM],
        default_params={"d": 21, "dense": False},
        priority=1,
        description="线性衰减平滑，降换手",
    ),
    "ts_backfill": OperatorInfo(
        name="ts_backfill",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["coverage_low", "fitness_low"],
        transform_types=[TransformType.INSERT],
        default_params={"lookback": 22, "k": 1},
        priority=0,
        description="缺失填充，提升覆盖",
    ),
    "ts_scale": OperatorInfo(
        name="ts_scale",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "fitness_low"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 60, "constant": 0},
        priority=2,
        description="时序缩放",
    ),
    "ts_quantile": OperatorInfo(
        name="ts_quantile",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "2y_low"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 60, "driver": "gaussian"},
        priority=2,
        description="时序分位",
    ),
    "ts_returns": OperatorInfo(
        name="ts_returns",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 21, "mode": 1},
        priority=2,
        description="收益率",
    ),
    "ts_av_diff": OperatorInfo(
        name="ts_av_diff",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 20},
        priority=2,
        description="偏离均值",
    ),
    "ts_min": OperatorInfo(
        name="ts_min",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "support"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 20},
        priority=3,
        description="时序最小值",
    ),
    "ts_max": OperatorInfo(
        name="ts_max",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "resistance"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 20},
        priority=3,
        description="时序最大值",
    ),

    # Group - 核心 (8)
    "group_neutralize": OperatorInfo(
        name="group_neutralize",
        category=OperatorCategory.GROUP,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["prod_corr_high", "2y_low"],
        transform_types=[TransformType.WRAP, TransformType.GROUP_AXIS],
        default_params={"group": "sector"},
        priority=1,
        constraint="最多 1 次",
        description="组内中性化，剥离行业暴露",
    ),
    "group_rank": OperatorInfo(
        name="group_rank",
        category=OperatorCategory.GROUP,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "2y_low", "sub_universe"],
        transform_types=[TransformType.REPLACE, TransformType.WRAP, TransformType.GROUP_AXIS],
        default_params={"group": "industry"},
        priority=1,
        description="组内排名",
    ),
    "group_zscore": OperatorInfo(
        name="group_zscore",
        category=OperatorCategory.GROUP,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "2y_low", "sub_universe"],
        transform_types=[TransformType.REPLACE, TransformType.WRAP, TransformType.GROUP_AXIS],
        default_params={"group": "industry"},
        priority=1,
        description="组内标准化",
    ),
    "group_scale": OperatorInfo(
        name="group_scale",
        category=OperatorCategory.GROUP,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.REPLACE, TransformType.WRAP, TransformType.GROUP_AXIS],
        default_params={"group": "sector"},
        priority=2,
        description="组内缩放",
    ),
    "group_mean": OperatorInfo(
        name="group_mean",
        category=OperatorCategory.GROUP,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.INSERT, TransformType.WRAP, TransformType.GROUP_AXIS],
        default_params={"group": "sector"},
        priority=2,
        description="组内均值",
    ),
    "group_backfill": OperatorInfo(
        name="group_backfill",
        category=OperatorCategory.GROUP,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["coverage_low"],
        transform_types=[TransformType.INSERT],
        default_params={"group": "sector", "d": 22, "std": 4.0},
        priority=2,
        description="组内填充",
    ),
    "group_sum": OperatorInfo(
        name="group_sum",
        category=OperatorCategory.GROUP,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.INSERT, TransformType.WRAP],
        default_params={"group": "sector"},
        priority=3,
        description="组内求和",
    ),
    "group_count": OperatorInfo(
        name="group_count",
        category=OperatorCategory.GROUP,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["coverage"],
        transform_types=[TransformType.INSERT, TransformType.CONDITION],
        default_params={"group": "sector"},
        priority=3,
        description="组内计数",
    ),

    # Arithmetic - 核心 (5)
    "add": OperatorInfo(
        name="add",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "2y_low", "combination"],
        transform_types=[TransformType.INSERT, TransformType.REPLACE],
        priority=1,
        constraint="禁止 add(0.4*A, 0.6*B) 调权重",
        description="信号叠加",
    ),
    "subtract": OperatorInfo(
        name="subtract",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "margin_low", "spread"],
        transform_types=[TransformType.REPLACE],
        priority=1,
        description="价差信号",
    ),
    "multiply": OperatorInfo(
        name="multiply",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "interaction"],
        transform_types=[TransformType.INSERT, TransformType.REPLACE],
        priority=2,
        description="信号交互",
    ),
    "divide": OperatorInfo(
        name="divide",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "margin_low", "ratio"],
        transform_types=[TransformType.REPLACE],
        priority=1,
        description="比率信号",
    ),
    "signed_power": OperatorInfo(
        name="signed_power",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "distribution"],
        transform_types=[TransformType.WRAP, TransformType.REPLACE],
        default_params={"y": 0.5},
        priority=2,
        description="非线性变换，保号",
    ),
}


# ============================================================================
# Phase 1: 高频算子扩展（20 个）- 累计 50 个
# ============================================================================

_HIGH_FREQ_OPERATORS = {
    # Vector (8)
    "vec_avg": OperatorInfo(
        name="vec_avg",
        category=OperatorCategory.VECTOR,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["VECTOR"],
        problem_types=["base_processing", "vector_convert"],
        transform_types=[TransformType.REPLACE],
        priority=0,
        description="向量均值，VECTOR→MATRIX",
    ),
    "vec_sum": OperatorInfo(
        name="vec_sum",
        category=OperatorCategory.VECTOR,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["VECTOR"],
        problem_types=["sharpe_low", "vector_convert"],
        transform_types=[TransformType.REPLACE],
        priority=2,
        description="向量求和",
    ),
    "vec_count": OperatorInfo(
        name="vec_count",
        category=OperatorCategory.VECTOR,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["VECTOR"],
        problem_types=["sharpe_low", "event_driven", "vector_convert"],
        transform_types=[TransformType.REPLACE, TransformType.CONDITION],
        priority=1,
        description="元素计数，事件频率",
    ),
    "vec_min": OperatorInfo(
        name="vec_min",
        category=OperatorCategory.VECTOR,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["VECTOR"],
        problem_types=["sharpe_low", "vector_convert"],
        transform_types=[TransformType.REPLACE],
        priority=3,
        description="向量最小值",
    ),
    "vec_max": OperatorInfo(
        name="vec_max",
        category=OperatorCategory.VECTOR,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["VECTOR"],
        problem_types=["sharpe_low", "vector_convert"],
        transform_types=[TransformType.REPLACE],
        priority=3,
        description="向量最大值",
    ),
    "vec_stddev": OperatorInfo(
        name="vec_stddev",
        category=OperatorCategory.VECTOR,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["VECTOR"],
        problem_types=["sharpe_low", "vector_convert"],
        transform_types=[TransformType.REPLACE],
        priority=3,
        description="向量标准差",
    ),
    "vec_range": OperatorInfo(
        name="vec_range",
        category=OperatorCategory.VECTOR,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["VECTOR"],
        problem_types=["sharpe_low", "vector_convert"],
        transform_types=[TransformType.REPLACE],
        priority=3,
        description="向量极差",
    ),

    # Logical (7)
    "if_else": OperatorInfo(
        name="if_else",
        category=OperatorCategory.LOGICAL,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "event_driven", "condition"],
        transform_types=[TransformType.WRAP, TransformType.INSERT, TransformType.CONDITION],
        priority=1,
        description="条件门控",
    ),
    "trade_when": OperatorInfo(
        name="trade_when",
        category=OperatorCategory.TRANSFORMATIONAL,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX", "EVENT"],
        problem_types=["sharpe_low", "turnover_high", "event_driven"],
        transform_types=[TransformType.WRAP, TransformType.INSERT, TransformType.CONDITION],
        priority=1,
        description="条件交易",
    ),
    "greater": OperatorInfo(
        name="greater",
        category=OperatorCategory.LOGICAL,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["condition"],
        transform_types=[TransformType.CONDITION],
        priority=2,
        description="大于判断",
    ),
    "less": OperatorInfo(
        name="less",
        category=OperatorCategory.LOGICAL,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["condition"],
        transform_types=[TransformType.CONDITION],
        priority=2,
        description="小于判断",
    ),
    "and": OperatorInfo(
        name="and",
        category=OperatorCategory.LOGICAL,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["condition"],
        transform_types=[TransformType.CONDITION],
        priority=2,
        description="逻辑与",
    ),
    "or": OperatorInfo(
        name="or",
        category=OperatorCategory.LOGICAL,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["condition"],
        transform_types=[TransformType.CONDITION],
        priority=2,
        description="逻辑或",
    ),
    "is_nan": OperatorInfo(
        name="is_nan",
        category=OperatorCategory.LOGICAL,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["coverage_low", "condition"],
        transform_types=[TransformType.CONDITION],
        priority=2,
        description="缺失判断",
    ),

    # Time Series - 扩展 (5)
    "ts_corr": OperatorInfo(
        name="ts_corr",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "correlation", "resonance"],
        transform_types=[TransformType.INSERT, TransformType.WRAP, TransformType.PARAM],
        default_params={"d": 20},
        priority=2,
        description="时序相关，共振确认",
    ),
    "ts_std_dev": OperatorInfo(
        name="ts_std_dev",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "volatility"],
        transform_types=[TransformType.INSERT, TransformType.WRAP, TransformType.PARAM],
        default_params={"d": 20},
        priority=2,
        description="时序波动",
    ),
    "ts_delay": OperatorInfo(
        name="ts_delay",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "lag"],
        transform_types=[TransformType.INSERT, TransformType.PARAM],
        default_params={"d": 1},
        priority=2,
        description="时滞",
    ),
    "hump": OperatorInfo(
        name="hump",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["turnover_high"],
        transform_types=[TransformType.WRAP, TransformType.PARAM],
        default_params={"hump": 0.01},
        priority=2,
        description="变化限制，硬降换手",
    ),
    "pasteurize": OperatorInfo(
        name="pasteurize",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["fitness_low", "coverage"],
        transform_types=[TransformType.INSERT],
        priority=2,
        description="异常值处理",
    ),
}


# ============================================================================
# Phase 2: 中频算子扩展（25 个）- 累计 75 个
# ============================================================================

_MID_FREQ_OPERATORS = {
    # Arithmetic - 扩展 (10)
    "reverse": OperatorInfo(
        name="reverse",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["direction"],
        transform_types=[TransformType.WRAP],
        priority=2,
        description="反向信号",
    ),
    "power": OperatorInfo(
        name="power",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "distribution"],
        transform_types=[TransformType.WRAP, TransformType.REPLACE],
        default_params={"y": 2},
        priority=3,
        description="幂变换",
    ),
    "sqrt": OperatorInfo(
        name="sqrt",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["fitness_low", "distribution"],
        transform_types=[TransformType.WRAP],
        priority=3,
        description="平方根",
    ),
    "log": OperatorInfo(
        name="log",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "distribution"],
        transform_types=[TransformType.WRAP],
        priority=3,
        description="对数变换",
    ),
    "abs": OperatorInfo(
        name="abs",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["volatility"],
        transform_types=[TransformType.WRAP],
        priority=4,
        description="绝对值",
    ),
    "sign": OperatorInfo(
        name="sign",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["direction"],
        transform_types=[TransformType.WRAP],
        priority=4,
        description="方向提取",
    ),
    "inverse": OperatorInfo(
        name="inverse",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.WRAP],
        priority=3,
        description="倒数",
    ),
    "max": OperatorInfo(
        name="max",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.REPLACE],
        priority=3,
        description="取大",
    ),
    "min": OperatorInfo(
        name="min",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["risk_control"],
        transform_types=[TransformType.REPLACE],
        priority=4,
        description="取小",
    ),
    "densify": OperatorInfo(
        name="densify",
        category=OperatorCategory.ARITHMETIC,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["GROUP"],
        problem_types=["computation"],
        transform_types=[TransformType.INSERT],
        priority=4,
        description="分组压缩",
    ),

    # Logical - 扩展 (5)
    "greater_equal": OperatorInfo(
        name="greater_equal",
        category=OperatorCategory.LOGICAL,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["condition"],
        transform_types=[TransformType.CONDITION],
        priority=3,
        description="大于等于",
    ),
    "less_equal": OperatorInfo(
        name="less_equal",
        category=OperatorCategory.LOGICAL,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["condition"],
        transform_types=[TransformType.CONDITION],
        priority=3,
        description="小于等于",
    ),
    "equal": OperatorInfo(
        name="equal",
        category=OperatorCategory.LOGICAL,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["condition"],
        transform_types=[TransformType.CONDITION],
        priority=3,
        description="相等",
    ),
    "not_equal": OperatorInfo(
        name="not_equal",
        category=OperatorCategory.LOGICAL,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["condition"],
        transform_types=[TransformType.CONDITION],
        priority=3,
        description="不等",
    ),
    "not": OperatorInfo(
        name="not",
        category=OperatorCategory.LOGICAL,
        scope=["REGULAR", "COMBO", "SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["condition"],
        transform_types=[TransformType.CONDITION],
        priority=3,
        description="逻辑非",
    ),

    # Time Series - 扩展 (10)
    "ts_sum": OperatorInfo(
        name="ts_sum",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "cumulative"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 5},
        priority=3,
        description="时序求和",
    ),
    "ts_product": OperatorInfo(
        name="ts_product",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "cumulative"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 5},
        priority=3,
        description="时序乘积",
    ),
    "ts_kurtosis": OperatorInfo(
        name="ts_kurtosis",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low", "tail"],
        transform_types=[TransformType.INSERT, TransformType.WRAP, TransformType.PARAM],
        default_params={"d": 60},
        priority=4,
        description="峰度",
    ),
    "ts_ir": OperatorInfo(
        name="ts_ir",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.REPLACE, TransformType.PARAM],
        default_params={"d": 60},
        priority=3,
        description="信息比率",
    ),
    "ts_covariance": OperatorInfo(
        name="ts_covariance",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.INSERT, TransformType.WRAP, TransformType.PARAM],
        default_params={"d": 20},
        priority=3,
        description="协方差",
    ),
    "ts_regression": OperatorInfo(
        name="ts_regression",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.INSERT, TransformType.WRAP, TransformType.PARAM],
        default_params={"d": 60, "lag": 0, "rettype": 0},
        priority=3,
        description="回归",
    ),
    "ts_arg_max": OperatorInfo(
        name="ts_arg_max",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.INSERT, TransformType.WRAP, TransformType.PARAM],
        default_params={"d": 20},
        priority=4,
        description="最大值位置",
    ),
    "ts_arg_min": OperatorInfo(
        name="ts_arg_min",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.INSERT, TransformType.WRAP, TransformType.PARAM],
        default_params={"d": 20},
        priority=4,
        description="最小值位置",
    ),
    "days_from_last_change": OperatorInfo(
        name="days_from_last_change",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX", "EVENT"],
        problem_types=["sharpe_low", "event"],
        transform_types=[TransformType.INSERT, TransformType.WRAP],
        priority=3,
        description="距上次变化天数",
    ),
    "last_diff_value": OperatorInfo(
        name="last_diff_value",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.INSERT, TransformType.WRAP, TransformType.PARAM],
        default_params={"d": 20},
        priority=4,
        description="最近不同值",
    ),
}


# ============================================================================
# Phase 3: 全算子覆盖（28 个）- 累计 103 个
# ============================================================================

_FULL_COVERAGE_OPERATORS = {
    # Transformational (3)
    "bucket": OperatorInfo(
        name="bucket",
        category=OperatorCategory.TRANSFORMATIONAL,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["group_construction"],
        transform_types=[TransformType.REPLACE, TransformType.INSERT],
        priority=3,
        description="分桶",
    ),
    "tail": OperatorInfo(
        name="tail",
        category=OperatorCategory.TRANSFORMATIONAL,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["fitness_low"],
        transform_types=[TransformType.INSERT],
        priority=4,
        description="尾部处理",
    ),
    "generate_stats": OperatorInfo(
        name="generate_stats",
        category=OperatorCategory.TRANSFORMATIONAL,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo_stats"],
        transform_types=[TransformType.REPLACE],
        priority=4,
        description="统计生成",
    ),

    # Group - 扩展 (4)
    "group_std_dev": OperatorInfo(
        name="group_std_dev",
        category=OperatorCategory.GROUP,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.INSERT, TransformType.WRAP],
        default_params={"group": "sector"},
        priority=3,
        description="组内标准差",
    ),
    "group_cartesian_product": OperatorInfo(
        name="group_cartesian_product",
        category=OperatorCategory.GROUP,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["GROUP"],
        problem_types=["advanced_group"],
        transform_types=[TransformType.INSERT],
        priority=4,
        description="分组笛卡尔积",
    ),
    "combo_a": OperatorInfo(
        name="combo_a",
        category=OperatorCategory.GROUP,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        default_params={"nlength": 250, "mode": "algo1"},
        priority=4,
        description="Alpha 组合",
    ),

    # Time Series - 扩展 (7)
    "ts_step": OperatorInfo(
        name="ts_step",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["time_mark"],
        transform_types=[TransformType.INSERT],
        priority=4,
        description="日计数器",
    ),
    "ts_count_nans": OperatorInfo(
        name="ts_count_nans",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["coverage_low"],
        transform_types=[TransformType.INSERT, TransformType.CONDITION, TransformType.PARAM],
        default_params={"d": 20},
        priority=3,
        description="缺失计数",
    ),
    "kth_element": OperatorInfo(
        name="kth_element",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["sharpe_low"],
        transform_types=[TransformType.INSERT, TransformType.WRAP, TransformType.PARAM],
        default_params={"d": 20, "k": 1},
        priority=4,
        description="第 k 元素",
    ),
    "ts_target_tvr_decay": OperatorInfo(
        name="ts_target_tvr_decay",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["turnover_high"],
        transform_types=[TransformType.WRAP, TransformType.PARAM],
        default_params={"lambda_min": 0, "lambda_max": 1, "target_tvr": 0.1},
        priority=2,
        description="目标换手衰减",
    ),
    "ts_target_tvr_hump": OperatorInfo(
        name="ts_target_tvr_hump",
        category=OperatorCategory.TIME_SERIES,
        scope=["REGULAR", "COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["turnover_high"],
        transform_types=[TransformType.WRAP, TransformType.PARAM],
        default_params={"lambda_min": 0, "lambda_max": 1, "target_tvr": 0.1},
        priority=2,
        description="目标换手 hump",
    ),

    # Reduce (14, COMBO 专用)
    "reduce_avg": OperatorInfo(
        name="reduce_avg",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        priority=2,
        description="平均",
    ),
    "reduce_stddev": OperatorInfo(
        name="reduce_stddev",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        priority=3,
        description="标准差",
    ),
    "reduce_ir": OperatorInfo(
        name="reduce_ir",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        priority=2,
        description="信息比率",
    ),
    "reduce_max": OperatorInfo(
        name="reduce_max",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        priority=3,
        description="最大值",
    ),
    "reduce_min": OperatorInfo(
        name="reduce_min",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        priority=3,
        description="最小值",
    ),
    "reduce_sum": OperatorInfo(
        name="reduce_sum",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        priority=3,
        description="求和",
    ),
    "reduce_norm": OperatorInfo(
        name="reduce_norm",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        priority=4,
        description="绝对和",
    ),
    "reduce_range": OperatorInfo(
        name="reduce_range",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        priority=4,
        description="极差",
    ),
    "reduce_percentage": OperatorInfo(
        name="reduce_percentage",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        default_params={"percentage": 0.5},
        priority=3,
        description="分位数",
    ),
    "reduce_skewness": OperatorInfo(
        name="reduce_skewness",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        priority=4,
        description="偏度",
    ),
    "reduce_kurtosis": OperatorInfo(
        name="reduce_kurtosis",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        priority=4,
        description="峰度",
    ),
    "reduce_count": OperatorInfo(
        name="reduce_count",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        default_params={"threshold": 0},
        priority=4,
        description="计数",
    ),
    "reduce_choose": OperatorInfo(
        name="reduce_choose",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        default_params={"nth": 1, "ignoreNan": True},
        priority=4,
        description="选择",
    ),
    "reduce_powersum": OperatorInfo(
        name="reduce_powersum",
        category=OperatorCategory.REDUCE,
        scope=["COMBO"],
        applicable_fields=["MATRIX"],
        problem_types=["combo"],
        transform_types=[TransformType.REPLACE],
        default_params={"constant": 2, "precise": False},
        priority=4,
        description="幂和",
    ),

    # Special (2, SELECTION 专用)
    "in": OperatorInfo(
        name="in",
        category=OperatorCategory.SPECIAL,
        scope=["SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["selection"],
        transform_types=[TransformType.REPLACE],
        priority=3,
        description="集合成员",
    ),
    "universe_size": OperatorInfo(
        name="universe_size",
        category=OperatorCategory.SPECIAL,
        scope=["SELECTION"],
        applicable_fields=["MATRIX"],
        problem_types=["selection"],
        transform_types=[TransformType.INSERT, TransformType.CONDITION],
        priority=3,
        description="宇宙大小",
    ),
}


# ============================================================================
# 合并所有算子
# ============================================================================

OPERATOR_CATALOG: Dict[str, OperatorInfo] = {
    **_CORE_OPERATORS,
    **_HIGH_FREQ_OPERATORS,
    **_MID_FREQ_OPERATORS,
    **_FULL_COVERAGE_OPERATORS,
}


# ============================================================================
# 查询函数
# ============================================================================

def get_all_operator_names() -> List[str]:
    """获取所有算子名称."""
    return list(OPERATOR_CATALOG.keys())


def get_operators_by_category(category: OperatorCategory) -> List[str]:
    """按分类获取算子."""
    return [
        name for name, info in OPERATOR_CATALOG.items()
        if info.category == category
    ]


def get_operators_by_problem(problem_type: str) -> List[str]:
    """按问题类型获取算子."""
    return [
        name for name, info in OPERATOR_CATALOG.items()
        if problem_type in info.problem_types
    ]


def get_operators_by_field_type(field_type: str) -> List[str]:
    """按字段类型获取算子."""
    return [
        name for name, info in OPERATOR_CATALOG.items()
        if field_type in info.applicable_fields
    ]


def get_operators_by_scope(scope: str) -> List[str]:
    """按作用域获取算子."""
    return [
        name for name, info in OPERATOR_CATALOG.items()
        if scope in info.scope
    ]


def get_operators_by_priority(max_priority: int = 2) -> List[str]:
    """按优先级获取算子."""
    return [
        name for name, info in OPERATOR_CATALOG.items()
        if info.priority <= max_priority
    ]


def get_operator_info(name: str) -> Optional[OperatorInfo]:
    """获取算子信息."""
    return OPERATOR_CATALOG.get(name)


# ============================================================================
# 统计信息
# ============================================================================

def get_catalog_stats() -> Dict:
    """获取目录统计信息."""
    stats = {
        "total": len(OPERATOR_CATALOG),
        "by_category": {},
        "by_priority": {},
        "by_scope": {},
    }

    for info in OPERATOR_CATALOG.values():
        # 按分类
        cat = info.category.value
        stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1

        # 按优先级
        pri = info.priority
        stats["by_priority"][pri] = stats["by_priority"].get(pri, 0) + 1

        # 按作用域
        for scope in info.scope:
            stats["by_scope"][scope] = stats["by_scope"].get(scope, 0) + 1

    return stats
