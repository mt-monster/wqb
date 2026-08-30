# -*- coding: utf-8 -*-
"""DiversityMetrics dataclass and platform operator signature tables.

Extracted from diversity_enhancer.py (2026-08-29 refactor) to separate
the data model + signature constants from the metric computation logic.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class DiversityMetrics:
    """多样性指标数据类"""
    operator_entropy: float
    structural_similarity: float
    novelty_score: float
    coverage_rate: float
    operator_distribution: Dict[str, int]
    skeleton_distribution: Dict[str, int]
    unique_structures: int
    total_expressions: int
    # 2026-08-18 新增（GBR 复盘）：
    # - top_operator_share: top1 算子使用占比，>0.6 即"信号单点"（如 GBR rank 占 90% 未被旧指标捕获）
    # - signal_single_point: 信号单点标记，触发时建议换字段源而非换算子
    # - expr_uniqueness: 字符串唯一率（旧 novelty 语义，保留用于兼容）
    top_operator_share: float = 0.0
    signal_single_point: bool = False
    expr_uniqueness: float = 0.0


# ---------------------------------------------------------------------------
# 平台算子签名表（2026-08-17 实证版）
#
# 与 BRAIN 平台实际签名对齐，而非 verifier 宽松签名表：
#   - quantile 平台仅 1 参（wave17Z 事故实证：2 参报 Invalid number of inputs
#     并级联 CANCEL 整批），verifier/expr_lint 旧签名 (1,3) 是陷阱
#   - rank 仅 1 参（第二参是数值 rate，不是窗口/分组）
#   - power/signed_power 是 2 参（x, p）
# 生成器按此签名构造表达式，从源头杜绝非法参数个数。
# ---------------------------------------------------------------------------
UNARY_OPS = {"quantile", "rank", "normalize", "abs", "log", "sign", "sqrt",
             "exp", "inverse", "reverse", "pasteurize", "densify", "zscore"}
BINARY_OPS = {"add", "subtract", "multiply", "divide", "power", "signed_power",
              "greater", "less"}


def op_arity_style(op: str) -> str:
    """返回算子的参数风格: unary | window | group | vec | binary。"""
    if op in UNARY_OPS:
        return "unary"
    if op in BINARY_OPS:
        return "binary"
    if op.startswith("group_"):
        return "group"
    if op.startswith("vec_"):
        return "vec"
    if op.startswith("ts_"):
        return "window"
    return "unary"  # 未知算子保守按单参，避免强加窗口
