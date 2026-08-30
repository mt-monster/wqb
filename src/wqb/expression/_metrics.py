# -*- coding: utf-8 -*-
"""OperatorQuotaManager and DiversityMonitor: diversity metric computation.

Extracted from diversity_enhancer.py (2026-08-29 refactor).
"""
from __future__ import annotations

import logging
import math
import random
import re
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

from ._op_signatures import DiversityMetrics


class OperatorQuotaManager:
    """算子配额管理器 - 强制算子轮换机制

    2026-08-18 修复（EUR+GBR 836 表达式实证：真实算子覆盖率仅 22%）：
      原 OPERATOR_CATEGORIES 是手写 50 算子小池，漏掉 55 个真实可用算子、
      混入 exp/range/vec_norm 3 个幽灵算子，导致 coverage_rate 分母失真、
      配额被幽灵算子污染、欠用建议永远照不见池外盲区。
      现改为以平台权威全集 VERIFIED_SAFE_OPERATORS（102）为唯一分母动态构建，
      剔除幽灵、补全漏网；新增 reduce_*/special 两类，配额键同步。
    """

    # 算子类别定义：由 VERIFIED_SAFE_OPERATORS 动态构建（见下方 _build_categories），
    # 保证与平台真实可用算子严格对齐，不再手写维护。
    OPERATOR_CATEGORIES = {}

    # 默认配额比例（按 8 类；special 为 combo/self_corr 等元算子，默认低配额）
    DEFAULT_QUOTAS = {
        'ts_*': 0.22,
        'group_*': 0.18,
        'vec_*': 0.08,
        'rank_*': 0.10,
        'arithmetic': 0.18,
        'conditional': 0.06,
        'transform': 0.05,
        'reduce_*': 0.08,
        'special': 0.05,
    }

    # 语义分类规则（仅对 VERIFIED 真实算子生效；顺序即优先级）
    _CATEGORY_RULES = (
        ('ts_*', lambda o: o.startswith('ts_')),
        ('group_*', lambda o: o.startswith('group_')),
        ('vec_*', lambda o: o.startswith('vec_')),
        ('reduce_*', lambda o: o.startswith('reduce_')),
        ('rank_*', lambda o: o in ('rank', 'quantile', 'normalize', 'scale', 'zscore')),
        ('arithmetic', lambda o: o in ('add', 'subtract', 'multiply', 'divide', 'signed_power',
                                       'sqrt', 'abs', 'log', 'sign', 'power', 'max', 'min',
                                       'inverse', 'bucket')),
        ('conditional', lambda o: o in ('if_else', 'trade_when', 'greater', 'less', 'greater_equal',
                                        'less_equal', 'equal', 'not_equal', 'and', 'or', 'not',
                                        'in', 'is_nan')),
        ('transform', lambda o: o in ('winsorize', 'pasteurize', 'densify', 'hump', 'reverse', 'tail')),
        # 兜底：combo_a/self_corr/generate_stats/universe_size/days_from_last_change/
        #       last_diff_value/kth_element 等元/特殊算子
        ('special', lambda o: True),
    )

    @classmethod
    def _verified_operators(cls):
        """平台权威真实算子全集（102）。优先取 config.VERIFIED_SAFE_OPERATORS。"""
        try:
            from wqb.config import VERIFIED_SAFE_OPERATORS
            ops = set(VERIFIED_SAFE_OPERATORS)
            if ops:
                return ops
        except Exception:
            logging.getLogger(__name__).debug("swallowed exception", exc_info=True)
        return set()

    @classmethod
    def _build_categories(cls):
        """按 _CATEGORY_RULES 把 VERIFIED 真实算子分入各类别（并集 == VERIFIED 全集）。"""
        cats = {name: [] for name, _ in cls._CATEGORY_RULES}
        for op in sorted(cls._verified_operators()):
            for name, pred in cls._CATEGORY_RULES:
                if pred(op):
                    cats[name].append(op)
                    break
        # 只保留非空类别，且每个类别内排序稳定
        return {k: v for k, v in cats.items() if v}

    @classmethod
    def all_verified_operators(cls):
        """coverage_rate 的权威分母：平台真实可用算子全集（102）。"""
        return cls._verified_operators()

    def __init__(self, quotas: Optional[Dict[str, float]] = None):
        # 动态构建 categories（首次实例化时），并同步配额键
        if not OperatorQuotaManager.OPERATOR_CATEGORIES:
            OperatorQuotaManager.OPERATOR_CATEGORIES = OperatorQuotaManager._build_categories()
        base = self.DEFAULT_QUOTAS.copy()
        # 只保留实际存在类别的配额，缺失类别补 0
        base = {k: v for k, v in base.items() if k in self.OPERATOR_CATEGORIES}
        self.quotas = quotas or base
        self.usage_history = defaultdict(int)
        self.category_usage = defaultdict(int)

    def get_operator_category(self, operator: str) -> str:
        """获取算子所属类别"""
        for category, ops in self.OPERATOR_CATEGORIES.items():
            if operator in ops:
                return category
        return 'other'

    def extract_operators(self, expression: str) -> List[str]:
        """从表达式中提取所有算子"""
        pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        return re.findall(pattern, expression)

    def analyze_expression(self, expression: str) -> Dict[str, int]:
        """分析表达式中的算子使用"""
        operators = self.extract_operators(expression)
        category_count = defaultdict(int)

        for op in operators:
            category = self.get_operator_category(op)
            category_count[category] += 1
            self.usage_history[op] += 1
            self.category_usage[category] += 1

        return dict(category_count)

    def get_underused_operators(self, threshold: float = 0.5) -> List[str]:
        """获取使用不足的算子"""
        if not self.usage_history:
            return []

        avg_usage = sum(self.usage_history.values()) / len(self.usage_history)
        underused = []

        for category, ops in self.OPERATOR_CATEGORIES.items():
            for op in ops:
                usage = self.usage_history.get(op, 0)
                if usage < avg_usage * threshold:
                    underused.append(op)

        return underused

    def suggest_next_operators(self, count: int = 5) -> List[str]:
        """建议下一批应使用的算子"""
        underused = self.get_underused_operators()

        # 按类别平衡选择
        suggestions = []
        category_needs = {}

        for category, quota in self.quotas.items():
            current = self.category_usage.get(category, 0)
            target = sum(self.category_usage.values()) * quota
            need = max(0, target - current)
            category_needs[category] = need

        # 优先从需求最大的类别中选择
        sorted_categories = sorted(category_needs.items(), key=lambda x: -x[1])

        for category, need in sorted_categories:
            if len(suggestions) >= count:
                break
            if need > 0:
                category_ops = self.OPERATOR_CATEGORIES.get(category, [])
                # 选择该类别中使用最少的算子
                category_usage = [(op, self.usage_history.get(op, 0)) for op in category_ops]
                category_usage.sort(key=lambda x: x[1])

                for op, _ in category_usage:
                    if len(suggestions) < count and op not in suggestions:
                        suggestions.append(op)

        return suggestions[:count]


class DiversityMonitor:
    """多样性监控器 - 实时计算多样性指标"""

    def __init__(self):
        self.history = []

    def calculate_metrics(self, expressions: List[str]) -> DiversityMetrics:
        """计算多样性指标"""
        if not expressions:
            return DiversityMetrics(0, 0, 0, 0, {}, {}, 0, 0)

        # 算子分布
        operator_dist = defaultdict(int)
        skeleton_dist = defaultdict(int)
        structures = []

        mutation_engine = StructuralMutationEngine()

        for expr in expressions:
            # 提取算子
            ops = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', expr)
            for op in ops:
                operator_dist[op] += 1

            # 分析骨架
            structure = mutation_engine.parse_expression_structure(expr)
            skeleton_dist[structure['skeleton_type']] += 1
            structures.append(structure)

        # 计算算子熵
        operator_entropy = self._calculate_entropy(list(operator_dist.values()))

        # 计算结构相似度（真实 pairwise 算子集 Jaccard，非"最大骨架占比"）
        structural_similarity = self._calculate_structural_similarity(structures)

        # 计算新颖度（结构签名唯一率：骨架 x 算子集 x 字段簇，非字符串唯一率）
        signatures = [self._structure_signature(s) for s in structures]
        novelty_score = self._calculate_novelty(signatures)

        # 字符串唯一率（旧 novelty 语义，兼容保留）
        expr_uniqueness = len(set(expressions)) / len(expressions) if expressions else 0

        # 计算覆盖率：分母用平台权威真实算子全集（102），而非 categories 小池。
        all_possible_ops = OperatorQuotaManager.all_verified_operators()
        if not all_possible_ops:  # config 不可用兜底：退回 categories 并集
            for ops in OperatorQuotaManager.OPERATOR_CATEGORIES.values():
                all_possible_ops.update(ops)
        # 分子只统计真实算子（剔除字段名误匹配/幽灵算子）
        used_ops = set(operator_dist.keys()) & all_possible_ops
        coverage_rate = len(used_ops) / len(all_possible_ops) if all_possible_ops else 0

        # top 算子占比与信号单点检测（GBR 复盘：rank 占 90% 的"伪多样性"必须暴露）
        top_operator_share = 0.0
        signal_single_point = False
        if operator_dist:
            top_op, _ = max(operator_dist.items(), key=lambda kv: kv[1])
            expr_with_top_op = sum(1 for s in structures if top_op in s.get('operators', []))
            top_operator_share = expr_with_top_op / len(expressions) if expressions else 0.0
            signal_single_point = top_operator_share > 0.6

        metrics = DiversityMetrics(
            operator_entropy=operator_entropy,
            structural_similarity=structural_similarity,
            novelty_score=novelty_score,
            coverage_rate=coverage_rate,
            operator_distribution=dict(operator_dist),
            skeleton_distribution=dict(skeleton_dist),
            unique_structures=len(set(str(s) for s in structures)),
            total_expressions=len(expressions),
            top_operator_share=top_operator_share,
            signal_single_point=signal_single_point,
            expr_uniqueness=expr_uniqueness
        )

        self.history.append(metrics)
        return metrics

    @staticmethod
    def _field_cluster(field: str) -> str:
        """字段归簇：去掉期限/后缀变体，识别同源信号。"""
        f = re.sub(r'_\d+_(month|year)_', '_', field)
        f = re.sub(r'_(1month|3month|6month|1year|2year|3year|4year|5year|7year|10year)$', '', f)
        f = re.sub(r'_(1|2|3|5|6|7|10|20|30|60|120|250)d?$', '', f)
        return f

    @staticmethod
    def _structure_signature(structure: Dict[str, Any]) -> Tuple[str, frozenset, frozenset]:
        """结构签名：(骨架类型, 算子集合, 字段簇集合)。可哈希，用于新颖度/有效性判定。"""
        skeleton_type = structure.get('skeleton_type', 'simple')
        ops = frozenset(structure.get('operators', []))
        fields = frozenset(DiversityMonitor._field_cluster(t)
                           for t in structure.get('fields', []))
        return (skeleton_type, ops, fields)

    def _calculate_entropy(self, counts: List[int]) -> float:
        """计算香农熵"""
        if not counts:
            return 0
        total = sum(counts)
        if total == 0:
            return 0

        entropy = 0
        for count in counts:
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        return entropy

    def _calculate_structural_similarity(self, structures: List[Dict]) -> float:
        """计算结构相似度（0-1，越高越相似）。"""
        if len(structures) < 2:
            return 0

        sample = structures
        if len(sample) > 150:
            sample = random.sample(sample, 150)

        ops_sets = [set(s.get('operators', [])) for s in sample]
        n = len(sample)
        total_sim, pairs = 0.0, 0
        for i in range(n):
            si = ops_sets[i]
            for j in range(i + 1, n):
                sj = ops_sets[j]
                if not si and not sj:
                    total_sim += 1.0
                elif not si or not sj:
                    total_sim += 0.0
                else:
                    total_sim += len(si & sj) / len(si | sj)
                pairs += 1
        return total_sim / pairs if pairs else 0.0

    def _calculate_novelty(self, signatures: List[Tuple]) -> float:
        """计算新颖度分数（结构签名唯一率）。"""
        if not signatures:
            return 0
        return len(set(signatures)) / len(signatures)

    def get_diversity_report(self) -> Dict[str, Any]:
        """获取多样性报告"""
        if not self.history:
            return {"status": "no_data"}

        latest = self.history[-1]

        # 计算趋势
        if len(self.history) > 1:
            prev = self.history[-2]
            entropy_trend = latest.operator_entropy - prev.operator_entropy
            coverage_trend = latest.coverage_rate - prev.coverage_rate
        else:
            entropy_trend = 0
            coverage_trend = 0

        return {
            "current_metrics": {
                "operator_entropy": round(latest.operator_entropy, 3),
                "structural_similarity": round(latest.structural_similarity, 3),
                "novelty_score": round(latest.novelty_score, 3),
                "coverage_rate": round(latest.coverage_rate, 3),
                "unique_structures": latest.unique_structures,
                "total_expressions": latest.total_expressions,
                "top_operator_share": round(latest.top_operator_share, 3),
                "signal_single_point": latest.signal_single_point,
                "expr_uniqueness": round(latest.expr_uniqueness, 3)
            },
            "trends": {
                "entropy_change": round(entropy_trend, 3),
                "coverage_change": round(coverage_trend, 3)
            },
            "effective": getattr(self, '_last_effective', True),
            "recommendations": self._generate_recommendations(latest)
        }

    def _generate_recommendations(self, metrics: DiversityMetrics) -> List[str]:
        """基于指标生成建议"""
        recommendations = []

        if metrics.operator_entropy < 2.0:
            recommendations.append("算子多样性不足，建议引入更多不同类别的算子")

        if metrics.structural_similarity > 0.7:
            recommendations.append("模板骨架过于相似，建议进行结构变异")

        if metrics.coverage_rate < 0.5:
            recommendations.append("算子覆盖率不足50%，建议探索未使用的算子类别")

        if metrics.novelty_score < 0.8:
            recommendations.append("表达式重复度过高，建议增加随机变异")

        # 信号单点警告
        if metrics.signal_single_point:
            recommendations.append(
                f"信号单点：top 算子占比 {metrics.top_operator_share:.0%}，表达式同源伪多样性，"
                f"应换字段/数据集信号源而非继续换算子")

        # 找出使用最少的算子类别
        if metrics.operator_distribution:
            quota_manager = OperatorQuotaManager()
            underused = quota_manager.get_underused_operators(threshold=0.3)
            if underused:
                recommendations.append(f"建议增加使用这些算子: {', '.join(underused[:5])}")

        return recommendations


# Import at end to avoid circular dependency: DiversityMonitor.calculate_metrics
# references StructuralMutationEngine which is defined in _enhancer.py.
from ._enhancer import StructuralMutationEngine  # noqa: E402
