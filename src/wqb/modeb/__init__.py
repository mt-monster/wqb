# -*- coding: utf-8 -*-
"""Mode B 全算子覆盖框架.

提供 103 个算子的完整目录、智能路由、变体生成与覆盖率追踪.
"""

from .operator_catalog import (
    OperatorCategory,
    TransformType,
    OperatorInfo,
    OPERATOR_CATALOG,
    get_operators_by_category,
    get_operators_by_problem,
    get_operators_by_field_type,
    get_all_operator_names,
    get_catalog_stats,
)
from .usage_tracker import OperatorUsageTracker
from .variant_generator import FullCoverageVariantGenerator, generate_modeb_variants, diagnose_problem
from .transform_engine import TransformEngine

__all__ = [
    "OperatorCategory",
    "TransformType",
    "OperatorInfo",
    "OPERATOR_CATALOG",
    "get_operators_by_category",
    "get_operators_by_problem",
    "get_operators_by_field_type",
    "get_all_operator_names",
    "get_catalog_stats",
    "OperatorUsageTracker",
    "FullCoverageVariantGenerator",
    "generate_modeb_variants",
    "diagnose_problem",
    "TransformEngine",
]
