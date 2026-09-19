# -*- coding: utf-8 -*-
"""structural_variants.py - 结构重构变体生成器.

针对「修订信号 vs 短期反转」等结构性权衡问题，提供四种合规重构方案：
  1. 几何重构：subtract/divide 替代 add，消除权重调参
  2. 中性化轴切换：group_neut 剥离 beta/行业暴露
  3. 时间尺度解耦：ts_delay/ts_mean 错峰
  4. 正交化：ts_regression_residual 数学剥离相关性

合规约束（记忆 7c2651ad）：
  - 禁止 add(A,B) 混信号调参
  - 禁止同信号加权调参（权重网格扫描）
  - 允许：换字段组合、换信号概念、换算子几何、换分组轴、单信号结构化

用法:
    from wqb.workflow.structural_variants import StructuralVariantGenerator

    gen = StructuralVariantGenerator()
    variants = gen.generate(
        base_signal="rank(anl45_est_revision)",
        conflict_signal="rank(ts_delta(close, 5))",
        strategy="geometric",  # geometric | neutralization | temporal | orthogonal
    )
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class ReconstructionStrategy(Enum):
    """结构重构策略枚举."""
    GEOMETRIC = "geometric"           # 几何重构：subtract/divide
    NEUTRALIZATION = "neutralization" # 中性化轴切换
    TEMPORAL = "temporal"             # 时间尺度解耦
    ORTHOGONAL = "orthogonal"         # 正交化（残差法）
    CONDITIONAL = "conditional"       # 条件触发（过滤器+触发器）


@dataclass
class StructuralVariant:
    """结构重构变体."""
    strategy: ReconstructionStrategy
    expression: str
    description: str
    expected_effect: str
    risk_note: str
    priority: int = 1  # 1=P0, 2=P1, 3=P2, 4=P3
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VariantGenerationResult:
    """变体生成结果."""
    base_expression: str
    variants: List[StructuralVariant]
    recommended: Optional[StructuralVariant]
    rationale: str


class StructuralVariantGenerator:
    """结构重构变体生成器.

    针对 sharpe 与 fitness/2Y 结构性权衡问题，生成合规的表达式变体。
    所有变体均遵守「禁止 add(A,B) 混信号」纪律。
    """

    # 几何重构模板（价差/比率结构）
    GEOMETRIC_TEMPLATES = {
        "spread": {
            "template": "subtract({base}, {conflict})",
            "description": "价差结构：捕捉相对强弱",
            "expected": "消除权重调参，降低 turnover",
            "risk": "可能损失部分多头收益",
            "priority": 1,
        },
        "ratio": {
            "template": "divide({base}, add({conflict}, 0.001))",
            "description": "比率结构：捕捉相对弹性",
            "expected": "非线性增强，对极端值敏感",
            "risk": "分母接近零时不稳定",
            "priority": 1,
        },
        "spread_rank": {
            "template": "subtract(rank({base}), rank({conflict}))",
            "description": "双 rank 价差：标准化后价差",
            "expected": "消除量纲影响，更稳定",
            "risk": "rank 后信息损失",
            "priority": 1,
        },
        "ratio_rank": {
            "template": "divide(rank({base}), add(rank({conflict}), 0.001))",
            "description": "双 rank 比率：标准化后比率",
            "expected": "结合 rank 稳定性与比率敏感性",
            "risk": "双重变换可能过度平滑",
            "priority": 2,
        },
    }

    # 中性化轴模板
    NEUTRALIZATION_AXES = {
        "country": {
            "template": "group_neut({signal}, country)",
            "description": "国家中性化：剥离主权/国家风险",
            "expected": "消除国家层面 beta 冲突",
            "risk": "可能过度中性化，损失国家层面信号",
            "priority": 2,
        },
        "sector": {
            "template": "group_neut({signal}, sector)",
            "description": "行业中性化：剥离行业风险",
            "expected": "消除行业聚集效应",
            "risk": "行业分类过粗可能残留暴露",
            "priority": 2,
        },
        "market": {
            "template": "group_neut({signal}, market)",
            "description": "市场中性化：剥离市场整体风险",
            "expected": "消除市场 beta 冲突",
            "risk": "可能剥离过多 alpha",
            "priority": 3,
        },
        "subindustry": {
            "template": "group_neut({signal}, subindustry)",
            "description": "子行业中性化：更细粒度行业剥离",
            "expected": "精准剥离行业风险",
            "risk": "子行业样本量可能不足",
            "priority": 2,
        },
    }

    # 时间尺度模板
    TEMPORAL_TEMPLATES = {
        "delay_base": {
            "template": "ts_delay({base}, {days})",
            "description": "基础信号滞后：避开短期反转期",
            "expected": "错峰进场，降低 turnover",
            "risk": "可能错过即时漂移",
            "priority": 2,
            "params": {"days": [3, 5, 10]},
        },
        "smooth_base": {
            "template": "ts_mean({base}, {window})",
            "description": "基础信号平滑：慢变量化",
            "expected": "降低噪声，与快反转解耦",
            "risk": "过度平滑损失信息",
            "priority": 2,
            "params": {"window": [10, 20, 60]},
        },
        "delay_conflict": {
            "template": "ts_delay({conflict}, {days})",
            "description": "冲突信号滞后：让反转信号错峰",
            "expected": "反转信号滞后，减少对冲",
            "risk": "反转信号失效",
            "priority": 3,
            "params": {"days": [1, 3]},
        },
        "delta_conflict": {
            "template": "ts_delta({conflict}, {window})",
            "description": "冲突信号差分：捕捉变化而非水平",
            "expected": "将水平对冲转为变化对冲",
            "risk": "差分后信号可能更噪声",
            "priority": 3,
            "params": {"window": [5, 10]},
        },
    }

    # 条件触发模板
    CONDITIONAL_TEMPLATES = {
        "quantile_filter": {
            "template": "multiply(ts_quantile({base}, {window}, {q}), {conflict})",
            "description": "分位数过滤：只在基础信号极端时启用冲突信号",
            "expected": "条件激活，减少无效对冲",
            "risk": "可能过度过滤，样本减少",
            "priority": 2,
            "params": {"window": [60], "q": [0.7, 0.8, 0.9]},
        },
        "threshold_filter": {
            "template": "multiply(ts_step({base}, {threshold}), {conflict})",
            "description": "阈值过滤：基础信号超过阈值才启用冲突信号",
            "expected": "硬条件触发，更精准",
            "risk": "阈值选择敏感",
            "priority": 3,
            "params": {"threshold": [0.5, 0.7]},
        },
    }

    # 正交化模板
    ORTHOGONAL_TEMPLATES = {
        "residual": {
            "template": "ts_regression_residual({conflict}, {base}, {window})",
            "description": "回归残差：剥离冲突信号对基础信号的暴露",
            "expected": "数学正交，保留双信号",
            "risk": "计算复杂，可能过拟合",
            "priority": 3,
            "params": {"window": [20, 60]},
        },
    }

    def __init__(self):
        """初始化生成器."""
        pass

    def generate(
        self,
        base_signal: str,
        conflict_signal: str,
        strategy: Optional[ReconstructionStrategy] = None,
        region: Optional[str] = None,
        dataset_type: Optional[str] = None,
    ) -> VariantGenerationResult:
        """生成结构重构变体.

        Args:
            base_signal: 基础信号表达式（如修订信号）
            conflict_signal: 冲突信号表达式（如反转信号）
            strategy: 指定策略，None 则生成所有策略的变体
            region: 区域代码（用于区域特定优化）
            dataset_type: 数据集类型（MATRIX/VECTOR，影响可用算子）

        Returns:
            VariantGenerationResult: 包含所有变体及推荐
        """
        variants: List[StructuralVariant] = []

        strategies = [strategy] if strategy else list(ReconstructionStrategy)

        for strat in strategies:
            if strat == ReconstructionStrategy.GEOMETRIC:
                variants.extend(self._generate_geometric(base_signal, conflict_signal))
            elif strat == ReconstructionStrategy.NEUTRALIZATION:
                variants.extend(self._generate_neutralization(base_signal, conflict_signal, region))
            elif strat == ReconstructionStrategy.TEMPORAL:
                variants.extend(self._generate_temporal(base_signal, conflict_signal))
            elif strat == ReconstructionStrategy.ORTHOGONAL:
                variants.extend(self._generate_orthogonal(base_signal, conflict_signal))
            elif strat == ReconstructionStrategy.CONDITIONAL:
                variants.extend(self._generate_conditional(base_signal, conflict_signal))

        # 按优先级排序
        variants.sort(key=lambda v: v.priority)

        # 推荐逻辑：P0 优先，其次根据区域/数据集特性
        recommended = self._select_recommended(variants, region, dataset_type)

        rationale = self._build_rationale(base_signal, conflict_signal, variants, recommended)

        return VariantGenerationResult(
            base_expression=f"add({base_signal}, {conflict_signal})",  # 原始问题表达式
            variants=variants,
            recommended=recommended,
            rationale=rationale,
        )

    def _generate_geometric(self, base: str, conflict: str) -> List[StructuralVariant]:
        """生成几何重构变体."""
        variants = []
        for key, cfg in self.GEOMETRIC_TEMPLATES.items():
            expr = cfg["template"].format(base=base, conflict=conflict)
            variants.append(StructuralVariant(
                strategy=ReconstructionStrategy.GEOMETRIC,
                expression=expr,
                description=cfg["description"],
                expected_effect=cfg["expected"],
                risk_note=cfg["risk"],
                priority=cfg["priority"],
                metadata={"subtype": key},
            ))
        return variants

    def _generate_neutralization(self, base: str, conflict: str, region: Optional[str]) -> List[StructuralVariant]:
        """生成中性化轴切换变体."""
        variants = []
        for axis, cfg in self.NEUTRALIZATION_AXES.items():
            # 对两个信号分别中性化
            base_neut = cfg["template"].format(signal=base)
            conflict_neut = cfg["template"].format(signal=conflict)
            # 然后用价差结构组合
            expr = f"subtract({base_neut}, {conflict_neut})"
            variants.append(StructuralVariant(
                strategy=ReconstructionStrategy.NEUTRALIZATION,
                expression=expr,
                description=f"{cfg['description']} + 价差结构",
                expected_effect=cfg["expected"],
                risk_note=cfg["risk"],
                priority=cfg["priority"],
                metadata={"axis": axis, "region": region},
            ))
        return variants

    def _generate_temporal(self, base: str, conflict: str) -> List[StructuralVariant]:
        """生成时间尺度解耦变体."""
        variants = []
        for key, cfg in self.TEMPORAL_TEMPLATES.items():
            for param_name, param_values in cfg.get("params", {}).items():
                for val in param_values:
                    if "{base}" in cfg["template"] and "{conflict}" in cfg["template"]:
                        # 双信号模板
                        expr = cfg["template"].format(base=base, conflict=conflict, **{param_name: val})
                    elif "{base}" in cfg["template"]:
                        # 基础信号变换，然后与冲突信号价差
                        transformed = cfg["template"].format(base=base, **{param_name: val})
                        expr = f"subtract({transformed}, {conflict})"
                    else:
                        # 冲突信号变换
                        transformed = cfg["template"].format(conflict=conflict, **{param_name: val})
                        expr = f"subtract({base}, {transformed})"

                    variants.append(StructuralVariant(
                        strategy=ReconstructionStrategy.TEMPORAL,
                        expression=expr,
                        description=f"{cfg['description']} ({param_name}={val})",
                        expected_effect=cfg["expected"],
                        risk_note=cfg["risk"],
                        priority=cfg["priority"],
                        metadata={"subtype": key, param_name: val},
                    ))
        return variants

    def _generate_orthogonal(self, base: str, conflict: str) -> List[StructuralVariant]:
        """生成正交化变体."""
        variants = []
        for key, cfg in self.ORTHOGONAL_TEMPLATES.items():
            for param_name, param_values in cfg.get("params", {}).items():
                for val in param_values:
                    expr = cfg["template"].format(base=base, conflict=conflict, **{param_name: val})
                    variants.append(StructuralVariant(
                        strategy=ReconstructionStrategy.ORTHOGONAL,
                        expression=expr,
                        description=f"{cfg['description']} ({param_name}={val})",
                        expected_effect=cfg["expected"],
                        risk_note=cfg["risk"],
                        priority=cfg["priority"],
                        metadata={"subtype": key, param_name: val},
                    ))
        return variants

    def _generate_conditional(self, base: str, conflict: str) -> List[StructuralVariant]:
        """生成条件触发变体."""
        variants = []
        for key, cfg in self.CONDITIONAL_TEMPLATES.items():
            params = cfg.get("params", {})
            # 生成参数组合
            if "window" in params and "q" in params:
                for w in params["window"]:
                    for q in params["q"]:
                        expr = cfg["template"].format(base=base, conflict=conflict, window=w, q=q)
                        variants.append(StructuralVariant(
                            strategy=ReconstructionStrategy.CONDITIONAL,
                            expression=expr,
                            description=f"{cfg['description']} (window={w}, q={q})",
                            expected_effect=cfg["expected"],
                            risk_note=cfg["risk"],
                            priority=cfg["priority"],
                            metadata={"subtype": key, "window": w, "q": q},
                        ))
            elif "threshold" in params:
                for t in params["threshold"]:
                    expr = cfg["template"].format(base=base, conflict=conflict, threshold=t)
                    variants.append(StructuralVariant(
                        strategy=ReconstructionStrategy.CONDITIONAL,
                        expression=expr,
                        description=f"{cfg['description']} (threshold={t})",
                        expected_effect=cfg["expected"],
                        risk_note=cfg["risk"],
                        priority=cfg["priority"],
                        metadata={"subtype": key, "threshold": t},
                    ))
        return variants

    def _select_recommended(
        self,
        variants: List[StructuralVariant],
        region: Optional[str],
        dataset_type: Optional[str],
    ) -> Optional[StructuralVariant]:
        """选择推荐变体.

        推荐逻辑：
        1. P0 优先（几何重构-价差）
        2. EUR/DEU 区域优先考虑 country 中性化
        3. VECTOR 数据集避免复杂时序算子
        """
        if not variants:
            return None

        # P0 优先
        p0_variants = [v for v in variants if v.priority == 1]
        if p0_variants:
            # 优先选择 spread_rank（双 rank 价差，最稳定）
            for v in p0_variants:
                if v.metadata.get("subtype") == "spread_rank":
                    return v
            return p0_variants[0]

        # 区域特定推荐
        if region in ("EUR", "DEU", "GBR"):
            country_neut = [v for v in variants
                          if v.strategy == ReconstructionStrategy.NEUTRALIZATION
                          and v.metadata.get("axis") == "country"]
            if country_neut:
                return country_neut[0]

        return variants[0]

    def _build_rationale(
        self,
        base: str,
        conflict: str,
        variants: List[StructuralVariant],
        recommended: Optional[StructuralVariant],
    ) -> str:
        """构建推荐理由."""
        lines = [
            f"基础信号: {base[:50]}{'...' if len(base) > 50 else ''}",
            f"冲突信号: {conflict[:50]}{'...' if len(conflict) > 50 else ''}",
            f"生成 {len(variants)} 个结构重构变体",
            "",
            "策略分布:",
        ]

        strategy_count = {}
        for v in variants:
            strategy_count[v.strategy.value] = strategy_count.get(v.strategy.value, 0) + 1
        for strat, count in sorted(strategy_count.items()):
            lines.append(f"  - {strat}: {count} 个")

        if recommended:
            lines.extend([
                "",
                f"推荐: {recommended.expression[:60]}{'...' if len(recommended.expression) > 60 else ''}",
                f"理由: {recommended.description}",
                f"预期: {recommended.expected_effect}",
            ])

        return "\n".join(lines)


def detect_structural_conflict(expression: str) -> Optional[Dict[str, Any]]:
    """检测表达式是否存在结构性冲突（add(A,B) 模式）.

    用于 wave_gate 预检阶段识别需要结构重构的表达式。

    Returns:
        如果检测到冲突，返回 {"base": ..., "conflict": ..., "pattern": ...}；
        否则返回 None
    """
    # 检测 add(A, B) 或加权 add 模式（按优先级排序，先检测复杂模式）
    patterns = [
        # add(multiply(w1, A), multiply(w2, B)) 函数式加权（优先检测）
        # 使用非贪婪匹配和更精确的括号匹配
        (r"add\s*\(\s*multiply\s*\(\s*[\d.]+\s*,\s*(.+?)\)\s*,\s*multiply\s*\(\s*[\d.]+\s*,\s*(.+?)\)\s*\)",
         "weighted_add_func"),
        # w1*A + w2*B 中缀式加权（简化检测）
        (r"[\d.]+\s*\*\s*([^+]+)\+\s*[\d.]+\s*\*\s*(.+)",
         "weighted_add_infix"),
        # add(A, B) 简单相加（最后检测，避免误匹配复杂模式）
        (r"add\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)",
         "simple_add"),
    ]

    for pattern, pattern_name in patterns:
        m = re.search(pattern, expression)
        if m:
            return {
                "base": m.group(1).strip(),
                "conflict": m.group(2).strip(),
                "pattern": pattern_name,
                "full_match": m.group(0),
            }

    return None


def generate_reconstruction_report(result: VariantGenerationResult) -> str:
    """生成结构重构报告（Markdown 格式）."""
    lines = [
        "# 结构重构变体报告",
        "",
        f"**原始表达式**: `{result.base_expression}`",
        "",
        "## 推荐理由",
        "",
        result.rationale,
        "",
        "## 全部变体",
        "",
        "| 优先级 | 策略 | 表达式 | 描述 | 预期效果 | 风险 |",
        "|--------|------|--------|------|----------|------|",
    ]

    for v in result.variants:
        expr_short = v.expression[:40] + "..." if len(v.expression) > 40 else v.expression
        lines.append(
            f"| P{v.priority} | {v.strategy.value} | `{expr_short}` | "
            f"{v.description} | {v.expected_effect} | {v.risk_note} |"
        )

    if result.recommended:
        lines.extend([
            "",
            "## 推荐变体详情",
            "",
            f"```python",
            f"{result.recommended.expression}",
            f"```",
            "",
            f"- **策略**: {result.recommended.strategy.value}",
            f"- **描述**: {result.recommended.description}",
            f"- **预期效果**: {result.recommended.expected_effect}",
            f"- **风险**: {result.recommended.risk_note}",
        ])

    return "\n".join(lines)
