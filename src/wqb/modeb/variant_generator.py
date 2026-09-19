# -*- coding: utf-8 -*-
"""Mode B 全算子覆盖变体生成器.

基于问题诊断、字段类型、历史胜率、全算子轮换机制生成自适应变体.
"""

from typing import Dict, List, Optional

from .operator_catalog import (
    OPERATOR_CATALOG,
    OperatorInfo,
    TransformType,
    get_all_operator_names,
    get_operators_by_problem,
    get_operators_by_field_type,
)
from .transform_engine import TransformEngine
from .usage_tracker import OperatorUsageTracker


class FullCoverageVariantGenerator:
    """全算子覆盖的 Mode B 变体生成器."""

    def __init__(
        self,
        tracker: Optional[OperatorUsageTracker] = None,
        max_variants: int = 24,
    ):
        """初始化生成器.

        Args:
            tracker: 算子使用追踪器
            max_variants: 最大变体数
        """
        self.tracker = tracker or OperatorUsageTracker()
        self.engine = TransformEngine()
        self.max_variants = max_variants
        self.catalog = OPERATOR_CATALOG

    def generate(
        self,
        best: Dict,
        problem_type: str,
        field_type: str = "MATRIX",
        wave_number: int = 1,
        region: Optional[str] = None,
    ) -> List[Dict]:
        """生成全算子覆盖的 Mode B 变体.

        变体分配：
        - 40% 基于问题诊断的算子（8-10 条）
        - 30% 基于字段类型的算子（6-8 条）
        - 20% 基于历史胜率的算子（4-6 条）
        - 10% 全算子轮换的新算子（2-3 条）

        Args:
            best: 最强候选 {"expression": ..., "sharpe": ..., ...}
            problem_type: 问题类型（sharpe_low, fitness_low, etc.）
            field_type: 字段类型（MATRIX, VECTOR, EVENT）
            wave_number: 当前波次
            region: 区域

        Returns:
            变体列表
        """
        base_expr = best.get("expression", "")
        if not base_expr:
            return []

        # 1. 获取候选算子池
        candidates = self._get_operator_candidates(
            problem_type, field_type, wave_number
        )

        # 2. 分配变体配额
        quotas = self._allocate_quotas(candidates)

        # 3. 生成变体
        variants = []
        variant_id = 0

        for op_name, quota in quotas.items():
            op_info = self.catalog.get(op_name)
            if not op_info:
                continue

            # 为每个算子生成变体
            op_variants = self.engine.generate_variants(
                base_expr, op_info, max_variants=quota
            )

            for v in op_variants:
                if len(variants) >= self.max_variants:
                    break
                variants.append({
                    "id": f"V{variant_id}",
                    "expression": v["expression"],
                    "operator": v["operator"],
                    "transform": v["transform"],
                    "param": v.get("param"),
                    "note": f"{v['operator']} {v['transform']}",
                })
                variant_id += 1

        # 4. 记录使用
        for v in variants:
            self.tracker.record_usage(
                operator=v["operator"],
                wave=wave_number,
                region=region,
            )

        return variants

    def _get_operator_candidates(
        self,
        problem_type: str,
        field_type: str,
        wave_number: int,
    ) -> List[str]:
        """获取候选算子列表.

        优先级：
        1. 基于问题诊断的算子
        2. 基于字段类型的算子
        3. 基于历史胜率的算子
        4. 全算子轮换的算子（保底）
        """
        candidates = []

        # 1. 基于问题诊断
        problem_ops = get_operators_by_problem(problem_type)
        candidates.extend(problem_ops)

        # 2. 基于字段类型
        field_ops = get_operators_by_field_type(field_type)
        candidates.extend(field_ops)

        # 3. 基于历史胜率
        high_winrate_ops = self.tracker.get_high_winrate_operators(
            min_usage=3, top_k=5
        )
        candidates.extend(high_winrate_ops)

        # 4. 全算子轮换（保底）
        all_ops = get_all_operator_names()
        rotation_ops = self.tracker.get_rotation_candidates(
            all_operators=all_ops,
            current_wave=wave_number,
            count=3,
        )
        candidates.extend(rotation_ops)

        # 去重并保持顺序
        seen = set()
        result = []
        for op in candidates:
            if op not in seen and op in self.catalog:
                seen.add(op)
                result.append(op)

        return result

    def _allocate_quotas(self, candidates: List[str]) -> Dict[str, int]:
        """分配变体配额.

        按优先级分配：
        - 前 5 个算子：各 3 条
        - 6-10 个算子：各 2 条
        - 其余算子：各 1 条
        """
        quotas = {}

        # 按优先级排序
        sorted_candidates = sorted(
            candidates,
            key=lambda x: (
                self.catalog[x].priority,
                -self.tracker.get_success_rate(x),
            )
        )

        for i, op_name in enumerate(sorted_candidates):
            if i < 5:
                quotas[op_name] = 3
            elif i < 10:
                quotas[op_name] = 2
            else:
                quotas[op_name] = 1

        return quotas

    def record_result(
        self,
        variant: Dict,
        success: bool,
        sharpe_delta: float = 0.0,
        fitness_delta: float = 0.0,
        turnover_delta: float = 0.0,
        wave_number: int = 1,
        region: Optional[str] = None,
    ) -> None:
        """记录变体回测结果.

        Args:
            variant: 变体信息
            success: 是否成功
            sharpe_delta: Sharpe 变化
            fitness_delta: Fitness 变化
            turnover_delta: Turnover 变化
            wave_number: 当前波次
            region: 区域
        """
        self.tracker.record_usage(
            operator=variant["operator"],
            wave=wave_number,
            success=success,
            sharpe_delta=sharpe_delta,
            fitness_delta=fitness_delta,
            turnover_delta=turnover_delta,
            region=region,
        )

    def get_coverage_report(self) -> Dict:
        """获取算子覆盖度报告."""
        all_ops = get_all_operator_names()
        return self.tracker.get_coverage_report(all_ops)


# ============================================================================
# 便捷函数
# ============================================================================

def diagnose_problem(best: Dict) -> str:
    """诊断候选的主要问题.

    Args:
        best: 候选指标 {"sharpe": ..., "fitness": ..., "turnover": ..., ...}

    Returns:
        问题类型
    """
    sharpe = best.get("sharpe", 0) or 0
    fitness = best.get("fitness", 0) or 0
    turnover = best.get("turnover", 0) or 0
    two_year = best.get("two_year_sharpe", 0) or 0
    prod_corr = best.get("prod_correlation", 0) or 0

    # 按优先级诊断
    if prod_corr >= 0.7:
        return "prod_corr_high"
    if sharpe < 1.0:
        return "sharpe_low"
    if fitness < 0.6:
        return "fitness_low"
    if turnover > 0.3:
        return "turnover_high"
    if two_year < 1.0:
        return "2y_low"
    if sharpe < 1.25:
        return "sharpe_low"
    if fitness < 0.8:
        return "fitness_low"

    return "general"


def generate_modeb_variants(
    best: Dict,
    tracker: Optional[OperatorUsageTracker] = None,
    max_variants: int = 24,
    wave_number: int = 1,
    region: Optional[str] = None,
) -> List[Dict]:
    """生成 Mode B 变体（便捷函数）.

    Args:
        best: 最强候选
        tracker: 算子使用追踪器
        max_variants: 最大变体数
        wave_number: 当前波次
        region: 区域

    Returns:
        变体列表
    """
    # 诊断问题
    problem_type = diagnose_problem(best)

    # 推断字段类型
    expr = best.get("expression", "")
    field_type = "MATRIX"
    if "vec_" in expr:
        field_type = "VECTOR"
    elif "trade_when" in expr or "event" in expr.lower():
        field_type = "EVENT"

    # 生成变体
    generator = FullCoverageVariantGenerator(
        tracker=tracker,
        max_variants=max_variants,
    )

    return generator.generate(
        best=best,
        problem_type=problem_type,
        field_type=field_type,
        wave_number=wave_number,
        region=region,
    )
