# -*- coding: utf-8 -*-
"""StructuralMutationEngine, DiversityEnhancer, and convenience functions.

Extracted from diversity_enhancer.py (2026-08-29 refactor).
"""
from __future__ import annotations

import json
import random
import re
from typing import Any, Dict, List, Optional, Tuple

from ._op_signatures import DiversityMetrics, op_arity_style
from ._metrics import OperatorQuotaManager, DiversityMonitor


class StructuralMutationEngine:
    """结构变异引擎 - 增强模板骨架多样性"""

    STRUCTURAL_MUTATIONS = [
        'swap_branches',
        'insert_layer',
        'delete_layer',
        'change_operator',
        'reorder_sequence',
        'add_condition',
        'change_window',
        'add_transform'
    ]

    def __init__(self):
        self.mutation_history = []

    def parse_expression_structure(self, expression: str) -> Dict[str, Any]:
        """解析表达式结构"""
        structure = {
            'operators': re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', expression),
            'fields': self._extract_fields(expression),
            'windows': re.findall(r',\s*(\d+)\s*\)', expression),
            'depth': expression.count('('),
            'has_group': 'group_' in expression,
            'has_ts': 'ts_' in expression,
            'has_vec': 'vec_' in expression,
            'has_conditional': any(op in expression for op in ['if_else', 'trade_when']),
            'skeleton_type': self._determine_skeleton(expression)
        }
        return structure

    def _extract_fields(self, expression: str) -> List[str]:
        """提取字段名"""
        cleaned = re.sub(r'[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)', '', expression)
        cleaned = re.sub(r'[\d\s,\(\)\+\-\*\/\=\<\>\'\""]', '', cleaned)
        fields = [f for f in cleaned.split() if len(f) > 3]
        return fields

    def _determine_skeleton(self, expression: str) -> str:
        """确定骨架类型"""
        if 'trade_when(' in expression or 'if_else(' in expression:
            return 'event_gated'
        if 'group_' in expression:
            if 'ts_' in expression:
                return 'group_ts_combined'
            return 'group_only'
        if 'divide(' in expression:
            return 'ratio'
        if 'add(' in expression or 'multiply(' in expression:
            return 'linear_mix'
        if 'vec_' in expression:
            return 'vector_aggregated'
        if 'ts_' in expression:
            return 'time_series'
        return 'simple'

    def mutate_expression(self, expression: str, mutation_type: Optional[str] = None) -> str:
        """对表达式进行结构变异"""
        if mutation_type is None:
            mutation_type = random.choice(self.STRUCTURAL_MUTATIONS)

        structure = self.parse_expression_structure(expression)

        if mutation_type == 'swap_branches':
            return self._swap_branches(expression)
        elif mutation_type == 'insert_layer':
            return self._insert_layer(expression, structure)
        elif mutation_type == 'delete_layer':
            return self._delete_layer(expression, structure)
        elif mutation_type == 'change_operator':
            return self._change_operator(expression, structure)
        elif mutation_type == 'reorder_sequence':
            return self._reorder_sequence(expression, structure)
        elif mutation_type == 'add_condition':
            return self._add_condition(expression)
        elif mutation_type == 'change_window':
            return self._change_window(expression)
        elif mutation_type == 'add_transform':
            return self._add_transform(expression)

        return expression

    def _swap_branches(self, expression: str) -> str:
        """交换分支"""
        pattern = r'(add|subtract|multiply|divide)\s*\(([^,]+),\s*([^)]+)\)'
        match = re.search(pattern, expression)
        if match:
            op, arg1, arg2 = match.groups()
            return expression.replace(match.group(0), f"{op}({arg2.strip()}, {arg1.strip()})")
        return expression

    def _insert_layer(self, expression: str, structure: Dict) -> str:
        """插入层"""
        if not structure['has_ts'] and random.random() < 0.5:
            window = random.choice([20, 60, 120, 250])
            return f"ts_mean({expression}, {window})"
        elif not structure['has_group'] and random.random() < 0.5:
            group = random.choice(['sector', 'industry', 'subindustry'])
            return f"group_rank({expression}, {group})"
        elif not structure['has_vec'] and 'vec_' not in expression:
            vec_op = random.choice(['vec_avg', 'vec_max', 'vec_min'])
            return f"{vec_op}({expression})"
        return expression

    def _delete_layer(self, expression: str, structure: Dict) -> str:
        """删除层"""
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\((.*)\)$'
        match = re.match(pattern, expression.strip())
        if match and structure['depth'] > 2:
            return match.group(1)
        return expression

    def _change_operator(self, expression: str, structure: Dict) -> str:
        """改变算子类型"""
        replacements = {
            'ts_mean': ['ts_median', 'ts_sum', 'ts_av_diff'],
            'ts_rank': ['ts_zscore', 'ts_scale'],
            'group_rank': ['group_zscore', 'group_mean'],
            'rank': ['quantile', 'normalize'],
            'add': ['subtract', 'multiply'],
            'multiply': ['divide', 'add']
        }

        for old_op, new_ops in replacements.items():
            if old_op in expression:
                new_op = random.choice(new_ops)
                return expression.replace(old_op, new_op, 1)
        return expression

    def _reorder_sequence(self, expression: str, structure: Dict) -> str:
        """重排序列"""
        if 'ts_' in expression and 'group_' in expression:
            pattern = r'(group_\w+)\((ts_\w+)\(([^)]+)\)(,\s*\w+)?\)'
            match = re.search(pattern, expression)
            if match:
                group_op, ts_op, inner, group_param = match.groups()
                return expression.replace(
                    match.group(0),
                    f"{ts_op}({group_op}({inner}{group_param or ''}))"
                )
        return expression

    def _add_condition(self, expression: str) -> str:
        """添加条件"""
        conditions = [
            f"trade_when(volume > ts_mean(volume, 20), {expression})",
            f"if_else(rank({expression}) > 0.5, {expression}, 0)",
            f"trade_when(ts_arg_max(close, 5) == 0, {expression})"
        ]
        return random.choice(conditions)

    def _change_window(self, expression: str) -> str:
        """改变窗口参数"""
        windows = [5, 10, 20, 40, 60, 120, 250]
        pattern = r',\s*(\d+)\s*\)'

        def replace_window(match):
            old_window = int(match.group(1))
            new_window = random.choice([w for w in windows if w != old_window])
            return f", {new_window})"

        return re.sub(pattern, replace_window, expression)

    def _add_transform(self, expression: str) -> str:
        """添加变换"""
        transforms = [
            f"winsorize({expression}, std=4)",
            f"pasteurize({expression})",
            f"ts_backfill({expression}, 66)",
            f"normalize({expression})"
        ]
        return random.choice(transforms)


class DiversityEnhancer:
    """多样性增强器 - 主类"""

    def __init__(self):
        self.quota_manager = OperatorQuotaManager()
        self.mutation_engine = StructuralMutationEngine()
        self.monitor = DiversityMonitor()
        self.expression_history = []

    def enhance_diversity(self, expressions: List[str], target_count: Optional[int] = None,
                          field_pool: Optional[List[str]] = None) -> List[str]:
        """增强表达式多样性。

        field_pool: 战役数据集字段池。None 时回退通用字段（向后兼容）。
        """
        if not expressions:
            return expressions

        # 1. 计算当前多样性
        current_metrics = self.monitor.calculate_metrics(expressions)
        before_sigs = {self.monitor._structure_signature(s)
                       for s in [self.mutation_engine.parse_expression_structure(e)
                                 for e in expressions]}

        # 2. 识别需要改进的领域
        underused_ops = self.quota_manager.get_underused_operators()

        # 3. 对现有表达式进行变异
        enhanced = []
        mutation_rate = self._calculate_mutation_rate(current_metrics)

        for expr in expressions:
            self.quota_manager.analyze_expression(expr)
            if random.random() < mutation_rate:
                mutated = self.mutation_engine.mutate_expression(expr)
                enhanced.append(mutated)
            else:
                enhanced.append(expr)

        # 4. 生成包含未充分使用算子的新表达式
        if underused_ops:
            novel_expressions = self._generate_with_operators(
                underused_ops,
                count=max(1, int(len(expressions) * 0.1)),
                field_pool=field_pool
            )
            enhanced.extend(novel_expressions)

        # 5. 添加完全随机的表达式（10%）
        random_count = int(len(expressions) * 0.1)
        random_expressions = self._generate_random_expressions(random_count, field_pool=field_pool)
        enhanced.extend(random_expressions)

        # 6. 如果指定了目标数量，进行裁剪
        if target_count and len(enhanced) > target_count:
            enhanced = self._select_diverse_subset(enhanced, target_count)

        # 7. 有效性校验
        after_sigs = {self.monitor._structure_signature(s)
                      for s in [self.mutation_engine.parse_expression_structure(e)
                                for e in enhanced]}
        effective = after_sigs != before_sigs
        self.monitor._last_effective = effective
        if not effective:
            return expressions

        return enhanced

    def _calculate_mutation_rate(self, metrics: DiversityMetrics) -> float:
        """根据当前多样性计算变异率"""
        base_rate = 0.3

        if metrics.operator_entropy < 2.0:
            base_rate += 0.2
        if metrics.structural_similarity > 0.7:
            base_rate += 0.2
        if metrics.coverage_rate < 0.5:
            base_rate += 0.1

        return min(base_rate, 0.8)

    def _generate_with_operators(self, operators: List[str], count: int,
                                 field_pool: Optional[List[str]] = None) -> List[str]:
        """生成包含指定算子的表达式（按平台算子签名构造）。"""
        expressions = []
        fields = field_pool or ["close", "volume", "returns", "volatility", "turnover"]

        for _ in range(count):
            op = random.choice(operators)
            field = random.choice(fields)
            style = op_arity_style(op)

            if style == "unary":
                template = random.choice([
                    "rank({op}({field}))",
                    "group_rank({op}({field}), sector)",
                    "ts_decay_linear({op}({field}), 5)",
                ])
                expr = template.format(op=op, field=field)
            elif style == "window":
                window = random.choice([20, 60, 120])
                template = random.choice([
                    "rank({op}({field}, {window}))",
                    "ts_mean({op}({field}, {window}), 60)",
                    "{op}({field}, {window})",
                ])
                expr = template.format(op=op, field=field, window=window)
            elif style == "group":
                group = random.choice(["sector", "industry"])
                template = random.choice([
                    "{op}({field}, {group})",
                    "rank({op}({field}, {group}))",
                ])
                expr = template.format(op=op, field=field, group=group)
            elif style == "vec":
                template = random.choice([
                    "{op}({field})",
                    "rank({op}({field}))",
                    "ts_mean({op}({field}), 60)",
                ])
                expr = template.format(op=op, field=field)
            elif style == "binary":
                field2 = random.choice(fields)
                template = random.choice([
                    "{op}({field}, {field2})",
                    "rank({op}({field}, {field2}))",
                ])
                expr = template.format(op=op, field=field, field2=field2)
            else:
                expr = f"{op}({field})"

            expressions.append(expr)

        return expressions

    def _generate_random_expressions(self, count: int,
                                     field_pool: Optional[List[str]] = None) -> List[str]:
        """生成完全随机的表达式（按平台算子签名构造）。"""
        expressions = []

        all_ops = []
        for ops in OperatorQuotaManager.OPERATOR_CATEGORIES.values():
            all_ops.extend(ops)

        fields = field_pool or ["close", "volume", "open", "high", "low", "returns", "vwap"]

        for _ in range(count):
            num_ops = random.randint(1, 3)
            selected_ops = random.sample(all_ops, num_ops)
            field = random.choice(fields)

            expr = field
            for op in reversed(selected_ops):
                style = op_arity_style(op)
                if style == "window":
                    window = random.choice([5, 20, 60, 120])
                    expr = f"{op}({expr}, {window})"
                elif style == "group":
                    group = random.choice(['sector', 'industry'])
                    expr = f"{op}({expr}, {group})"
                elif style == "binary":
                    other = random.choice(fields)
                    expr = f"{op}({expr}, {other})"
                else:
                    expr = f"{op}({expr})"

            expressions.append(expr)

        return expressions

    def _select_diverse_subset(self, expressions: List[str], target_count: int) -> List[str]:
        """选择多样性高的子集"""
        if len(expressions) <= target_count:
            return expressions

        scores = []
        for i, expr in enumerate(expressions):
            differences = []
            for j, other in enumerate(expressions):
                if i != j:
                    diff = len(set(expr.split()) - set(other.split()))
                    differences.append(diff)

            avg_diff = sum(differences) / len(differences) if differences else 0
            scores.append((expr, avg_diff))

        scores.sort(key=lambda x: -x[1])
        return [expr for expr, _ in scores[:target_count]]

    def get_diversity_report(self) -> Dict[str, Any]:
        """获取多样性报告"""
        return self.monitor.get_diversity_report()

    def save_state(self, filepath: str):
        """保存状态"""
        state = {
            "operator_usage": dict(self.quota_manager.usage_history),
            "category_usage": dict(self.quota_manager.category_usage),
            "metrics_history": [
                {
                    "operator_entropy": m.operator_entropy,
                    "coverage_rate": m.coverage_rate,
                    "novelty_score": m.novelty_score
                }
                for m in self.monitor.history
            ]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def load_state(self, filepath: str):
        """加载状态"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)

            self.quota_manager.usage_history.update(state.get("operator_usage", {}))
            self.quota_manager.category_usage.update(state.get("category_usage", {}))
        except FileNotFoundError:
            pass  # 首次运行，无状态文件


# 便捷函数
def enhance_expressions(expressions: List[str], target_count: Optional[int] = None,
                        field_pool: Optional[List[str]] = None) -> Tuple[List[str], Dict[str, Any]]:
    """增强表达式多样性的便捷函数。"""
    enhancer = DiversityEnhancer()
    enhanced = enhancer.enhance_diversity(expressions, target_count, field_pool=field_pool)
    report = enhancer.get_diversity_report()
    return enhanced, report


def analyze_diversity(expressions: List[str]) -> Dict[str, Any]:
    """分析表达式多样性的便捷函数。"""
    monitor = DiversityMonitor()
    monitor.calculate_metrics(expressions)
    return monitor.get_diversity_report()


def signal_evidence_gate(results: List[Dict[str, Any]],
                         max_sharpe_floor: float = 0.5,
                         min_batches: int = 2) -> Dict[str, Any]:
    """信号证据闸：根据已回测结果判定区域/数据集是否达到信号天花板。"""
    if not results:
        return {'passed': True, 'max_sharpe': 0.0, 'batches_observed': 0,
                'verdict': 'no_evidence', 'message': '无回测结果，无法判定'}

    shs = [abs(float(r.get('sharpe', 0) or 0)) for r in results]
    max_sh = max(shs) if shs else 0.0
    batch_ids = {r.get('batch_idx') for r in results if r.get('batch_idx') is not None}
    batches_observed = len(batch_ids) if batch_ids else 1

    ceiling = max_sh < max_sharpe_floor and batches_observed >= min_batches
    if ceiling:
        verdict, message = 'ceiling', (
            f'信号天花板：{batches_observed} 批回测 max|sharpe|={max_sh:.2f} < '
            f'{max_sharpe_floor}，建议停止生成/增强，转向区域决策'
            f'（换 universe/换区域/数据集判死）')
    else:
        verdict, message = 'ok', (
            f'max|sharpe|={max_sh:.2f}（{batches_observed} 批）未触顶，可继续')

    return {'passed': not ceiling, 'max_sharpe': round(max_sh, 3),
            'batches_observed': batches_observed, 'verdict': verdict,
            'message': message}
