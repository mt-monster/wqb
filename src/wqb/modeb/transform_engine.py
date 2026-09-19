# -*- coding: utf-8 -*-
"""Mode B 表达式变换引擎.

实现算子替换、包裹、插入、条件门控、参数调整、分组轴变换等操作.
"""

import re
from typing import Dict, List, Optional

from .operator_catalog import OperatorInfo, TransformType


class TransformEngine:
    """表达式变换引擎."""

    # 时序算子正则
    TS_OP_PATTERN = re.compile(
        r"\b(ts_\w+)\s*\(([^)]+)\)"
    )

    # 分组算子正则
    GROUP_OP_PATTERN = re.compile(
        r"\b(group_\w+)\s*\(([^)]+)\)"
    )

    # 截面算子正则
    CS_OP_PATTERN = re.compile(
        r"\b(rank|zscore|quantile|normalize|winsorize|scale)\s*\(([^)]+)\)"
    )

    # 向量算子正则
    VEC_OP_PATTERN = re.compile(
        r"\b(vec_\w+)\s*\(([^)]+)\)"
    )

    def __init__(self):
        """初始化变换引擎."""
        pass

    def transform(
        self,
        expr: str,
        op_info: OperatorInfo,
        transform_type: TransformType,
        **kwargs
    ) -> Optional[str]:
        """执行变换.

        Args:
            expr: 原始表达式
            op_info: 算子信息
            transform_type: 变换类型
            **kwargs: 额外参数

        Returns:
            变换后的表达式，失败返回 None
        """
        if transform_type == TransformType.REPLACE:
            return self._replace_operator(expr, op_info, **kwargs)
        elif transform_type == TransformType.WRAP:
            return self._wrap_operator(expr, op_info, **kwargs)
        elif transform_type == TransformType.INSERT:
            return self._insert_operator(expr, op_info, **kwargs)
        elif transform_type == TransformType.CONDITION:
            return self._add_condition(expr, op_info, **kwargs)
        elif transform_type == TransformType.PARAM:
            return self._adjust_param(expr, op_info, **kwargs)
        elif transform_type == TransformType.GROUP_AXIS:
            return self._change_group_axis(expr, op_info, **kwargs)
        return None

    def _replace_operator(
        self,
        expr: str,
        op_info: OperatorInfo,
        **kwargs
    ) -> Optional[str]:
        """替换核心算子.

        策略：找到表达式中的核心算子，替换为新算子（保持参数结构）.
        """
        new_op = op_info.name

        # 尝试替换时序算子
        if new_op.startswith("ts_"):
            match = self.TS_OP_PATTERN.search(expr)
            if match:
                old_op = match.group(1)
                # 保持窗口参数
                old_params = match.group(2)
                # 提取窗口参数（最后一个数字）
                window_match = re.search(r",\s*(\d+)\s*$", old_params)
                if window_match:
                    window = window_match.group(1)
                    # 构建新参数
                    field_part = old_params[:window_match.start()].strip()
                    new_expr = expr.replace(
                        match.group(0),
                        f"{new_op}({field_part}, {window})"
                    )
                    return new_expr

        # 尝试替换分组算子
        if new_op.startswith("group_"):
            match = self.GROUP_OP_PATTERN.search(expr)
            if match:
                old_op = match.group(1)
                old_params = match.group(2)
                # 保持分组轴
                new_expr = expr.replace(
                    match.group(0),
                    f"{new_op}({old_params})"
                )
                return new_expr

        # 尝试替换截面算子
        if new_op in ("rank", "zscore", "quantile", "normalize"):
            match = self.CS_OP_PATTERN.search(expr)
            if match:
                old_op = match.group(1)
                old_params = match.group(2)
                new_expr = expr.replace(
                    match.group(0),
                    f"{new_op}({old_params})"
                )
                return new_expr

        # 尝试替换向量算子
        if new_op.startswith("vec_"):
            match = self.VEC_OP_PATTERN.search(expr)
            if match:
                old_op = match.group(1)
                old_params = match.group(2)
                new_expr = expr.replace(
                    match.group(0),
                    f"{new_op}({old_params})"
                )
                return new_expr

        return None

    def _wrap_operator(
        self,
        expr: str,
        op_info: OperatorInfo,
        **kwargs
    ) -> Optional[str]:
        """外层包裹算子.

        策略：在整个表达式外层包裹新算子.
        避免不合理的嵌套（如 rank(rank(...))）.
        """
        new_op = op_info.name
        params = op_info.default_params.copy()
        params.update(kwargs)

        # 检查是否已有相同算子在最外层
        # 如果表达式已经是 new_op(...) 开头，则跳过
        if expr.strip().startswith(f"{new_op}("):
            return None

        # 对于 rank/zscore/quantile 等截面算子，避免嵌套
        if new_op in ("rank", "zscore", "quantile", "normalize"):
            # 如果表达式已经包含任何截面算子，跳过包裹
            if self.CS_OP_PATTERN.search(expr):
                return None

        # 构建包裹表达式
        if new_op == "quantile":
            driver = params.get("driver", "gaussian")
            return f"quantile({expr}, {driver})"

        elif new_op == "group_neutralize":
            group = params.get("group", "sector")
            return f"group_neutralize({expr}, {group})"

        elif new_op == "group_rank":
            group = params.get("group", "industry")
            return f"group_rank({expr}, {group})"

        elif new_op == "group_zscore":
            group = params.get("group", "industry")
            return f"group_zscore({expr}, {group})"

        elif new_op == "signed_power":
            y = params.get("y", 0.5)
            return f"signed_power({expr}, {y})"

        elif new_op == "reverse":
            return f"reverse({expr})"

        elif new_op == "ts_decay_linear":
            d = params.get("d", 21)
            return f"ts_decay_linear({expr}, {d})"

        elif new_op == "hump":
            h = params.get("hump", 0.01)
            return f"hump({expr}, {h})"

        elif new_op == "if_else":
            # 需要条件参数
            condition = kwargs.get("condition", "1")
            else_val = kwargs.get("else_val", "0")
            return f"if_else({condition}, {expr}, {else_val})"

        elif new_op == "trade_when":
            condition = kwargs.get("condition", "1")
            exit_val = kwargs.get("exit_val", "NaN")
            return f"trade_when({condition}, {expr}, {exit_val})"

        # 通用包裹（排除 rank 等截面算子）
        if new_op not in ("rank", "zscore", "normalize"):
            return f"{new_op}({expr})"

        return None

    def _insert_operator(
        self,
        expr: str,
        op_info: OperatorInfo,
        **kwargs
    ) -> Optional[str]:
        """插入新处理层.

        策略：在表达式内部插入新算子（如 ts_backfill, pasteurize）.
        避免插入到已有相同算子的字段上.
        """
        new_op = op_info.name
        params = op_info.default_params.copy()
        params.update(kwargs)

        # 找到最内层的字段引用（不在任何函数调用内的字段）
        # 使用更精确的正则：匹配字段名，但排除已有函数包裹的情况
        field_pattern = re.compile(
            r"(?<![a-zA-Z0-9_(])\b([a-zA-Z_][a-zA-Z0-9_]*)\b(?![a-zA-Z0-9_)])"
        )

        # 收集所有字段位置
        fields = []
        for match in field_pattern.finditer(expr):
            field_name = match.group(1)
            # 跳过常见非字段词
            skip_words = {
                "rank", "ts", "group", "vec", "if", "else", "and", "or", "not",
                "true", "false", "nan", "null", "sector", "industry", "subindustry",
                "country", "market", "gaussian", "cauchy", "uniform",
            }
            if field_name.lower() in skip_words:
                continue
            # 跳过数字
            if field_name.isdigit():
                continue
            fields.append((match.start(), match.end(), field_name))

        if not fields:
            return None

        # 选择第一个字段（通常是最内层的字段）
        start, end, field_name = fields[0]

        # 检查该字段是否已被目标算子包裹
        # 向前查找是否有 new_op( 在字段前
        prefix = expr[:start]
        if f"{new_op}(" in prefix:
            # 已被相同算子包裹，跳过
            return None

        # 构建插入表达式
        if new_op == "ts_backfill":
            lookback = params.get("lookback", 22)
            k = params.get("k", 1)
            new_field = f"ts_backfill({field_name}, {lookback}, {k})"
            return expr[:start] + new_field + expr[end:]

        elif new_op == "pasteurize":
            new_field = f"pasteurize({field_name})"
            return expr[:start] + new_field + expr[end:]

        elif new_op == "winsorize":
            std = params.get("std", 4)
            new_field = f"winsorize({field_name}, {std})"
            return expr[:start] + new_field + expr[end:]

        elif new_op == "group_backfill":
            group = params.get("group", "sector")
            d = params.get("d", 22)
            std = params.get("std", 4.0)
            new_field = f"group_backfill({field_name}, {group}, {d}, {std})"
            return expr[:start] + new_field + expr[end:]

        return None

    def _add_condition(
        self,
        expr: str,
        op_info: OperatorInfo,
        **kwargs
    ) -> Optional[str]:
        """添加条件门控.

        策略：在表达式外层添加 if_else 或 trade_when 条件.
        """
        new_op = op_info.name

        # 构建条件
        condition = kwargs.get("condition")
        if not condition:
            # 默认条件：基于 rank 的阈值
            condition = f"rank({expr}) > 0.5"

        if new_op == "if_else":
            else_val = kwargs.get("else_val", "0")
            return f"if_else({condition}, {expr}, {else_val})"

        elif new_op == "trade_when":
            exit_val = kwargs.get("exit_val", "NaN")
            return f"trade_when({condition}, {expr}, {exit_val})"

        elif new_op in ("greater", "less", "greater_equal", "less_equal"):
            # 这些算子用于构建条件，不是直接包裹
            threshold = kwargs.get("threshold", "0.5")
            if new_op == "greater":
                return f"if_else({expr} > {threshold}, {expr}, 0)"
            elif new_op == "less":
                return f"if_else({expr} < {threshold}, {expr}, 0)"
            elif new_op == "greater_equal":
                return f"if_else({expr} >= {threshold}, {expr}, 0)"
            elif new_op == "less_equal":
                return f"if_else({expr} <= {threshold}, {expr}, 0)"

        return None

    def _adjust_param(
        self,
        expr: str,
        op_info: OperatorInfo,
        **kwargs
    ) -> Optional[str]:
        """调整算子参数.

        策略：找到表达式中的目标算子，调整其参数.
        使用 kwargs 中的 window 参数指定新窗口值.
        """
        target_op = kwargs.get("target_op")
        new_window = kwargs.get("window")

        # 如果指定了 window 参数，直接使用
        if new_window is not None:
            match = self.TS_OP_PATTERN.search(expr)
            if match:
                old_params = match.group(2)
                # 尝试替换窗口参数
                window_match = re.search(r",\s*(\d+)\s*$", old_params)
                if window_match:
                    old_window = window_match.group(1)
                    if str(new_window) != old_window:
                        new_expr = expr.replace(
                            f", {old_window})",
                            f", {new_window})"
                        )
                        return new_expr
            return None

        # 默认：尝试不同的窗口值
        match = self.TS_OP_PATTERN.search(expr)
        if match:
            old_params = match.group(2)
            # 尝试替换窗口参数
            window_match = re.search(r",\s*(\d+)\s*$", old_params)
            if window_match:
                old_window = window_match.group(1)
                # 候选窗口（排除当前窗口）
                candidate_windows = [20, 60, 120, 250]
                for w in candidate_windows:
                    if str(w) != old_window:
                        new_expr = expr.replace(
                            f", {old_window})",
                            f", {w})"
                        )
                        return new_expr

        return None

    def _change_group_axis(
        self,
        expr: str,
        op_info: OperatorInfo,
        **kwargs
    ) -> Optional[str]:
        """变换分组轴.

        策略：找到 group_* 算子，更换其分组变量.
        """
        new_group = kwargs.get("group", "industry")

        # 候选分组轴
        candidate_groups = ["sector", "industry", "subindustry", "country", "market"]

        match = self.GROUP_OP_PATTERN.search(expr)
        if match:
            old_params = match.group(2)
            # 找到当前分组轴
            for g in candidate_groups:
                if g in old_params:
                    # 替换为新分组轴
                    new_expr = expr.replace(
                        f", {g})",
                        f", {new_group})"
                    )
                    return new_expr

        return None

    def generate_variants(
        self,
        expr: str,
        op_info: OperatorInfo,
        max_variants: int = 3,
    ) -> List[Dict]:
        """为单个算子生成多个变体.

        Args:
            expr: 原始表达式
            op_info: 算子信息
            max_variants: 最大变体数

        Returns:
            变体列表
        """
        variants = []

        for transform_type in op_info.transform_types:
            if len(variants) >= max_variants:
                break

            # 根据变换类型生成变体
            if transform_type == TransformType.GROUP_AXIS:
                # 分组轴变换：生成多个分组轴变体
                for group in ["sector", "industry", "subindustry"]:
                    if len(variants) >= max_variants:
                        break
                    new_expr = self.transform(
                        expr, op_info, transform_type, group=group
                    )
                    if new_expr and new_expr != expr:
                        variants.append({
                            "expression": new_expr,
                            "operator": op_info.name,
                            "transform": transform_type.value,
                            "param": group,
                        })

            elif transform_type == TransformType.PARAM:
                # 参数调整：生成多个参数变体
                if op_info.name.startswith("ts_"):
                    for window in [20, 60, 120]:
                        if len(variants) >= max_variants:
                            break
                        new_expr = self.transform(
                            expr, op_info, transform_type, window=window
                        )
                        if new_expr and new_expr != expr:
                            variants.append({
                                "expression": new_expr,
                                "operator": op_info.name,
                                "transform": transform_type.value,
                                "param": window,
                            })

            else:
                # 其他变换：生成单个变体
                new_expr = self.transform(expr, op_info, transform_type)
                if new_expr and new_expr != expr:
                    variants.append({
                        "expression": new_expr,
                        "operator": op_info.name,
                        "transform": transform_type.value,
                    })

        return variants
