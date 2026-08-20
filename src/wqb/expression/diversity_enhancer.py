# -*- coding: utf-8 -*-
"""
diversity_enhancer.py - Alpha表达式多样性增强系统

提供操作符探索率提升、模板骨架多样性增强、实时多样性监控等功能。
"""

import json
import random
import re
import math
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path


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
            pass
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
        # 简化的结构解析
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
        # 移除算子和数字，剩下的主要是字段
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
        # 查找add/subtract/multiply/divide的两个参数并交换
        pattern = r'(add|subtract|multiply|divide)\s*\(([^,]+),\s*([^)]+)\)'
        match = re.search(pattern, expression)
        if match:
            op, arg1, arg2 = match.groups()
            return expression.replace(match.group(0), f"{op}({arg2.strip()}, {arg1.strip()})")
        return expression
    
    def _insert_layer(self, expression: str, structure: Dict) -> str:
        """插入层"""
        if not structure['has_ts'] and random.random() < 0.5:
            # 添加时间序列层
            window = random.choice([20, 60, 120, 250])
            return f"ts_mean({expression}, {window})"
        elif not structure['has_group'] and random.random() < 0.5:
            # 添加分组层
            group = random.choice(['sector', 'industry', 'subindustry'])
            return f"group_rank({expression}, {group})"
        elif not structure['has_vec'] and 'vec_' not in expression:
            # 添加向量聚合层
            vec_op = random.choice(['vec_avg', 'vec_max', 'vec_min'])
            return f"{vec_op}({expression})"
        return expression
    
    def _delete_layer(self, expression: str, structure: Dict) -> str:
        """删除层"""
        # 尝试移除外层算子
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
        # 交换嵌套算子的顺序
        if 'ts_' in expression and 'group_' in expression:
            # 尝试交换ts和group的顺序
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
            # 选择一个不同的窗口
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
        # 2026-08-18 修复：原 categories 并集仅 50 算子，coverage_rate 虚高，
        # 实战 102 全集覆盖率仅 22% 的盲区被掩盖。切到 VERIFIED 全集后口径真实。
        all_possible_ops = OperatorQuotaManager.all_verified_operators()
        if not all_possible_ops:  # config 不可用兜底：退回 categories 并集
            for ops in OperatorQuotaManager.OPERATOR_CATEGORIES.values():
                all_possible_ops.update(ops)
        # 分子只统计真实算子（剔除字段名误匹配/幽灵算子）
        used_ops = set(operator_dist.keys()) & all_possible_ops
        coverage_rate = len(used_ops) / len(all_possible_ops) if all_possible_ops else 0
        
        # top 算子占比与信号单点检测（GBR 复盘：rank 占 90% 的"伪多样性"必须暴露）
        # 占比按表达式级计（使用 top 算子的表达式数/总表达式数）：token 级频次会被
        # 嵌套表达式稀释（GBR rank token 占比仅 ~39%），漏报信号单点。
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
        """字段归簇：去掉期限/后缀变体，识别同源信号（如 annualized_pd_1_month_jc7 -> annualized_pd_jc7）。

        覆盖两种期限格式：annualized_pd_1_month_jc7（数字_单词_）与 mdl53_ms5_1month（无下划线）。
        """
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
        """计算结构相似度（0-1，越高越相似）。
        
        2026-08-18 重写（GBR 复盘）：旧实现 = 最大骨架类占比，把
        single 占 80% 误报为"结构高度相似"。新实现 = 采样两两表达式的
        算子集 Jaccard 平均，真正度量算子组合层面的相似度。
        """
        if len(structures) < 2:
            return 0
        
        # 大池采样上限，防 O(n²) 性能退化（739 表达式全量 27 万对仍可，>150 采样）
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
        """计算新颖度分数（结构签名唯一率）。
        
        2026-08-18 重写（GBR 复盘）：旧实现 = 字符串唯一率，`rank(ts_delta(x,5))`
        与 `rank(ts_delta(x,10))` 被当成两个"新颖"表达式，掩盖同源伪多样性。
        新实现 = 骨架 x 算子集 x 字段簇的签名唯一率。
        """
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
        
        # 信号单点警告（GBR 复盘：rank 占 90% 但 entropy/coverage 指标正常，必须显式暴露）
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

        field_pool: 战役数据集字段池（如 model53 的 annualized_pd_*_jc7）。
        2026-08-18 起必须与数据集绑定：旧实现硬编码 close/volume/returns 通用字段，
        生成的"增强表达式"在 5 闸字段白名单外被刷掉，增强等于白烧配额。
        None 时回退通用字段（向后兼容）。
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
            # 分析表达式
            self.quota_manager.analyze_expression(expr)
            
            # 决定是否需要变异
            if random.random() < mutation_rate:
                mutated = self.mutation_engine.mutate_expression(expr)
                enhanced.append(mutated)
            else:
                enhanced.append(expr)
        
        # 4. 生成包含未充分使用算子的新表达式（字段池注入战役数据集字段）
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
            # 优先保留多样性高的表达式
            enhanced = self._select_diverse_subset(enhanced, target_count)
        
        # 7. 有效性校验（GBR 复盘：8 表达式批次增强后 entropy/coverage 零变化却标 enhanced:true，
        #    属假增强。签名集合无新增即视为无效，返回原列表）
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
        
        # 如果多样性低，增加变异率
        if metrics.operator_entropy < 2.0:
            base_rate += 0.2
        if metrics.structural_similarity > 0.7:
            base_rate += 0.2
        if metrics.coverage_rate < 0.5:
            base_rate += 0.1
        
        return min(base_rate, 0.8)  # 最高80%变异率
    
    def _generate_with_operators(self, operators: List[str], count: int,
                                 field_pool: Optional[List[str]] = None) -> List[str]:
        """生成包含指定算子的表达式（按平台算子签名构造，单参算子绝不套窗口）。

        field_pool: 战役数据集字段池（2026-08-18 起优先传入）；None 回退通用字段。
        """
        expressions = []
        fields = field_pool or ["close", "volume", "returns", "volatility", "turnover"]

        for _ in range(count):
            op = random.choice(operators)
            field = random.choice(fields)
            style = op_arity_style(op)

            if style == "unary":
                # 单参算子：禁止带窗口/分组参数（quantile/rank 等平台仅 1 参）
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
                # vec_* 聚合无窗口
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
        """生成完全随机的表达式（按平台算子签名构造）。

        field_pool: 战役数据集字段池（2026-08-18 起优先传入）；None 回退通用字段。
        """
        expressions = []

        all_ops = []
        for ops in OperatorQuotaManager.OPERATOR_CATEGORIES.values():
            all_ops.extend(ops)

        fields = field_pool or ["close", "volume", "open", "high", "low", "returns", "vwap"]

        for _ in range(count):
            # 随机选择1-3个算子
            num_ops = random.randint(1, 3)
            selected_ops = random.sample(all_ops, num_ops)
            field = random.choice(fields)

            # 构建嵌套表达式
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
                    # unary / vec：单参，不带窗口
                    expr = f"{op}({expr})"

            expressions.append(expr)

        return expressions
    
    def _select_diverse_subset(self, expressions: List[str], target_count: int) -> List[str]:
        """选择多样性高的子集"""
        if len(expressions) <= target_count:
            return expressions
        
        # 计算每个表达式的独特性分数
        scores = []
        for i, expr in enumerate(expressions):
            # 与其他表达式的平均差异
            differences = []
            for j, other in enumerate(expressions):
                if i != j:
                    # 简化的差异计算
                    diff = len(set(expr.split()) - set(other.split()))
                    differences.append(diff)
            
            avg_diff = sum(differences) / len(differences) if differences else 0
            scores.append((expr, avg_diff))
        
        # 按独特性排序并选择前N个
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
    """
    增强表达式多样性的便捷函数
    
    Args:
        expressions: 原始表达式列表
        target_count: 目标表达式数量
        field_pool: 战役数据集字段池（None 回退通用字段）
    
    Returns:
        (增强后的表达式列表, 多样性报告)
    """
    enhancer = DiversityEnhancer()
    enhanced = enhancer.enhance_diversity(expressions, target_count, field_pool=field_pool)
    report = enhancer.get_diversity_report()
    return enhanced, report


def analyze_diversity(expressions: List[str]) -> Dict[str, Any]:
    """
    分析表达式多样性的便捷函数
    
    Args:
        expressions: 表达式列表
    
    Returns:
        多样性分析报告
    """
    monitor = DiversityMonitor()
    metrics = monitor.calculate_metrics(expressions)
    return monitor.get_diversity_report()


def signal_evidence_gate(results: List[Dict[str, Any]],
                         max_sharpe_floor: float = 0.5,
                         min_batches: int = 2) -> Dict[str, Any]:
    """信号证据闸：根据已回测结果判定区域/数据集是否达到信号天花板。

    GBR 复盘（2026-08-18）：多样性指标只反映结构分布，与回测表现零相关。
    29 批 232 回测 0 候选、max|sharpe|≈0.8 仍被多样性体系判"继续增强"。
    本闸在批量回测后调用：连续 min_batches 批 max|sharpe| < floor 即判
    信号天花板，建议停止生成/增强，转向区域决策（换 universe/换区域/判死）。

    Args:
        results: 回测结果列表，每项含 sharpe（可用 batch_idx 区分批次，缺省按 1 批）
        max_sharpe_floor: 信号下限（GBR 窄截面建议 0.5）
        min_batches: 需要至少几批证据才判定（防单批噪声误杀）

    Returns:
        {passed, max_sharpe, batches_observed, verdict, message}
    """
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
