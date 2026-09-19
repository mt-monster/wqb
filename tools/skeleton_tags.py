#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skeleton_tags.py — 多维骨架标签提取器（经济学构造链感知）

输入：单条表达式
输出：四维标签字典 {structure, construction_chain, mechanism, field_match}

用法：
  from skeleton_tags import extract_tags
  tags = extract_tags("group_rank(ts_delta(vec_avg(eps_cnt), 22), industry)")
  # → {
  #     "structure": "group_relative",
  #     "construction_chain": ["vector_agg", "delta"],
  #     "mechanism": "analyst_revision",
  #     "field_match": {"status": "pass", "details": []},
  #     "fields": ["eps_cnt"],
  #     "ops": ["group_rank", "ts_delta", "vec_avg"],
  #   }
"""
import re
import collections
from typing import Dict, List, Optional

# ---- 算子分类（复用 pool_diversity.py）----
TS_OPS = {
    'ts_corr', 'ts_zscore', 'ts_returns', 'ts_product', 'ts_std_dev',
    'ts_backfill', 'ts_scale', 'ts_sum', 'ts_av_diff', 'ts_kurtosis',
    'ts_mean', 'ts_arg_max', 'ts_rank', 'ts_ir', 'ts_delay', 'ts_quantile',
    'ts_count_nans', 'ts_covariance', 'ts_decay_linear', 'ts_arg_min',
    'ts_regression', 'ts_max_diff', 'ts_delta', 'ts_step',
    'ts_target_tvr_decay', 'ts_target_tvr_hump', 'days_from_last_change',
    'last_diff_value',
}
GROUP_OPS = {
    'group_mean', 'group_rank', 'group_backfill', 'group_scale',
    'group_count', 'group_zscore', 'group_std_dev', 'group_sum',
    'group_neutralize', 'group_cartesian_product', 'group_arg_max',
    'group_arg_min', 'group_vector_neut',
}
VEC_OPS = {'vec_min', 'vec_max', 'vec_avg', 'vec_sum', 'vec_count',
           'vec_stddev', 'vec_range'}
CONDITIONAL_OPS = {'trade_when', 'if_else', 'bucket', 'tail'}
PREPROCESS_OPS = {
    'rank', 'zscore', 'scale', 'normalize', 'quantile', 'winsorize',
    'ts_backfill', 'ts_zscore', 'ts_mean', 'ts_rank', 'ts_decay_linear',
    'ts_delta', 'ts_scale', 'group_zscore', 'group_rank', 'group_neutralize',
}
MATH_OPS = {
    'add', 'multiply', 'subtract', 'divide', 'max', 'min', 'sign', 'log',
    'abs', 'sqrt', 'inverse', 'reverse', 'pasteurize', 'densify', 'power',
    'signed_power', 'or', 'and', 'not', 'is_nan', 'equal', 'not_equal',
    'greater', 'greater_equal', 'less', 'less_equal', 'kth_element', 'hump',
}
ALL_OPS = TS_OPS | GROUP_OPS | VEC_OPS | CONDITIONAL_OPS | PREPROCESS_OPS | MATH_OPS

PLATFORM_FIELDS = {
    'open', 'high', 'low', 'close', 'vwap', 'returns', 'adv20', 'adv60',
    'adv120', 'cap', 'cap3', 'sharesout', 'volume', 'sector', 'industry',
    'subindustry', 'country', 'exchange', 'sector_country',
    'industry_country', 'sector_exchange', 'date', 'bucket',
}

# ---- 构造链阶段映射 ----
CONSTRUCTION_CHAIN_MAP = {
    'ts_backfill': 'backfill',
    'vec_avg': 'vector_agg', 'vec_max': 'vector_agg', 'vec_sum': 'vector_agg',
    'vec_min': 'vector_agg', 'vec_count': 'vector_agg',
    'ts_decay_linear': 'smooth', 'ts_mean': 'smooth',
    'winsorize': 'transform', 'zscore': 'transform', 'scale': 'transform',
    'normalize': 'transform', 'ts_zscore': 'transform',
    'ts_delta': 'delta', 'ts_av_diff': 'delta',
    'ts_corr': 'correlation', 'ts_covariance': 'correlation',
    'days_from_last_change': 'freshness', 'last_diff_value': 'freshness',
    'ts_std_dev': 'volatility', 'ts_ir': 'volatility',
    'bucket': 'bucket', 'tail': 'bucket', 'quantile': 'bucket',
}

# ---- 经济学机制模板（复用 template_families.json 逻辑）----
MECHANISM_PATTERNS = {
    'event_conviction': {
        'required_ops': ['divide', 'ts_sum', 'group_rank'],
        'optional_ops': ['winsorize', 'tail'],
        'field_shapes': ['zero_inflated', 'point_mass'],
        'description': '事件驱动-信念强度：流量相对存量的不寻常程度',
    },
    'event_gated': {
        'required_ops': ['trade_when'],
        'optional_ops': ['if_else'],
        'field_shapes': ['zero_inflated', 'point_mass'],
        'description': '稀疏事件门控：信号只在事件发生时持仓',
    },
    'spread_pair': {
        'required_ops': ['subtract', 'rank'],
        'optional_ops': [],
        'field_shapes': ['spread'],
        'description': '连续字段相对价值/双rank去相关',
    },
    'ceiling_suppress': {
        'required_ops': ['winsorize', 'rank'],
        'optional_ops': [],
        'field_shapes': ['ceiling'],
        'description': '截尾抑制：值接近上界的字段先抑制极值',
    },
    'discrete_score': {
        'required_ops': ['group_rank'],
        'optional_ops': ['bucket'],
        'field_shapes': ['spread', 'concentrated'],
        'field_integer': True,
        'description': '离散评分/计数分层：integer字段用bucket/group_rank',
    },
    'low_freq_backfill': {
        'required_ops': ['ts_backfill'],
        'optional_ops': [],
        'field_freq': ['monthly', 'quarterly', 'semi-annual'],
        'description': '低频字段回填：月度/季度字段先ts_backfill',
    },
    'analyst_revision': {
        'required_ops': ['group_rank', 'ts_delta', 'vec_avg'],
        'optional_ops': [],
        'field_shapes': ['spread'],
        'field_type': ['VECTOR'],
        'description': '分析师修正广度：下修/上调/新估计的分析师数量变化',
    },
    'target_price': {
        'required_ops': ['group_rank', 'divide', 'vec_avg'],
        'optional_ops': [],
        'field_shapes': ['zero_inflated'],
        'field_type': ['VECTOR'],
        'description': '目标价相对溢价：分析师目标价相对现价的溢价空间',
    },
    'momentum': {
        'required_ops': ['ts_delta'],
        'optional_ops': ['ts_rank', 'ts_backfill'],
        'field_shapes': ['spread'],
        'description': '动量/信息扩散：信息逐步被定价',
    },
    'mean_reversion': {
        'required_ops': ['reverse'],
        'optional_ops': ['ts_delta', 'ts_rank'],
        'field_shapes': ['spread'],
        'description': '均值回归/短期反转：价格压力是暂时的',
    },
    'volume_price': {
        'required_ops': ['ts_corr'],
        'optional_ops': ['ts_covariance', 'rank'],
        'field_shapes': ['spread'],
        'description': '量价背离：价量同向放大=散户追涨拥挤',
    },
    'volatility_premium': {
        'required_ops': ['divide', 'ts_std_dev'],
        'optional_ops': ['rank'],
        'field_shapes': ['spread'],
        'description': '波动率风险溢价/低波动异象',
    },
    'liquidity_premium': {
        'required_ops': ['divide', 'abs'],
        'optional_ops': ['rank'],
        'field_shapes': ['spread'],
        'description': '流动性溢价（Amihud非流动性）',
    },
    'multi_horizon': {
        'required_ops': ['add', 'multiply', 'rank'],
        'optional_ops': [],
        'field_shapes': ['spread'],
        'min_legs': 2,
        'description': '多期限共识：短期/中期/长期预测一致看涨',
    },
    'confidence_weighted': {
        'required_ops': ['multiply', 'rank'],
        'optional_ops': [],
        'field_shapes': ['spread'],
        'description': '置信度加权：高概率×高置信度=期望收益',
    },
}


def extract_ops(expr: str) -> List[str]:
    """提取表达式中出现的所有算子。"""
    idents = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', expr)
    return [t for t in idents if t in ALL_OPS]


def extract_fields(expr: str) -> List[str]:
    """提取数据字段（排除算子与平台内置字段）。"""
    idents = set(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', expr))
    callables = set(re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', expr))
    named_params = {'filter', 'true', 'false', 'hump', 'k'}
    return sorted(idents - callables - ALL_OPS - PLATFORM_FIELDS - named_params)


def classify_structure(expr: str, ops: List[str]) -> str:
    """维度 1：结构模式分类。"""
    # 事件门控优先
    if 'trade_when' in ops or 'if_else' in ops:
        return 'event_gated'
    if 'days_from_last_change' in ops or 'last_diff_value' in ops:
        return 'event_freshness'

    # group 结构
    has_group = any(o in GROUP_OPS for o in ops)
    if has_group:
        if 'bucket' in ops or 'tail' in ops:
            return 'group_bucket'
        return 'group_relative'

    # ratio 结构
    if 'divide' in ops:
        if 'ts_std_dev' in ops or 'ts_ir' in ops:
            return 'ratio_adjusted'
        return 'ratio_pair'
    if 'subtract' in ops:
        return 'ratio_pair'

    # linear_mix 结构
    n_mult = ops.count('multiply')
    n_add = ops.count('add')
    if n_add >= 1:
        legs = n_mult if n_mult >= 2 else 2
        if legs >= 3:
            return 'linear_3plus'
        return 'linear_2leg'

    # single 结构（细分）
    if any(o in VEC_OPS for o in ops):
        return 'single_aggregated'
    if any(o in {'ts_backfill', 'ts_zscore', 'winsorize', 'ts_decay_linear',
                 'ts_mean', 'zscore', 'scale', 'normalize'} for o in ops):
        return 'single_preprocessed'
    return 'single_raw'


def extract_construction_chain(ops: List[str]) -> List[str]:
    """维度 2：构造链阶段提取。"""
    chain = []
    seen = set()
    for op in ops:
        stage = CONSTRUCTION_CHAIN_MAP.get(op)
        if stage and stage not in seen:
            chain.append(stage)
            seen.add(stage)
    return chain if chain else ['raw']


def classify_mechanism(expr: str, ops: List[str], fields: List[str]) -> str:
    """维度 3：经济学机制分类。"""
    op_set = set(ops)

    # 按优先级匹配机制
    for mechanism, pattern in MECHANISM_PATTERNS.items():
        required = set(pattern.get('required_ops', []))
        if required.issubset(op_set):
            # 检查 min_legs（multi_horizon）
            if mechanism == 'multi_horizon':
                n_mult = ops.count('multiply')
                if n_mult < pattern.get('min_legs', 2):
                    continue
            return mechanism

    return 'free_explore'


def match_field_profile(mechanism: str, field_profiles: Dict[str, Dict]) -> Dict[str, str]:
    """维度 4：字段形状匹配校验。

    Args:
        mechanism: 经济学机制
        field_profiles: {field_id: {shape, coverage, data_type, integer, freq}}

    Returns:
        匹配结果 {status: "pass"/"warn"/"fail", details: [...]}
    """
    if mechanism == 'free_explore' or not field_profiles:
        return {'status': 'pass', 'details': []}

    pattern = MECHANISM_PATTERNS.get(mechanism, {})
    required_shapes = pattern.get('field_shapes', [])
    required_type = pattern.get('field_type', [])
    required_freq = pattern.get('field_freq', [])
    required_integer = pattern.get('field_integer')

    mismatches = []
    for field_id, profile in field_profiles.items():
        shape = profile.get('shape', 'unknown')
        dtype = profile.get('data_type', profile.get('type', '')).upper()
        freq = profile.get('freq', '')
        integer = profile.get('integer', False)

        if required_shapes and shape not in required_shapes:
            mismatches.append(f"{field_id}: shape={shape} not in {required_shapes}")
        if required_type and dtype not in [t.upper() for t in required_type]:
            mismatches.append(f"{field_id}: type={dtype} not in {required_type}")
        if required_freq and freq not in required_freq:
            mismatches.append(f"{field_id}: freq={freq} not in {required_freq}")
        if required_integer is not None and integer != required_integer:
            mismatches.append(f"{field_id}: integer={integer} != {required_integer}")

    if mismatches:
        return {'status': 'warn', 'details': mismatches}
    return {'status': 'pass', 'details': []}


def extract_tags(expr: str, field_profiles: Optional[Dict[str, Dict]] = None) -> Dict:
    """主入口：提取表达式的四维标签。

    Args:
        expr: alpha 表达式
        field_profiles: 可选，字段画像 {field_id: {shape, coverage, ...}}

    Returns:
        {
            "structure": "group_relative",
            "construction_chain": ["vector_agg", "delta"],
            "mechanism": "analyst_revision",
            "field_match": {"status": "pass", "details": []},
            "fields": ["eps_cnt"],
            "ops": ["group_rank", "ts_delta", "vec_avg"],
        }
    """
    ops = extract_ops(expr)
    fields = extract_fields(expr)

    structure = classify_structure(expr, ops)
    chain = extract_construction_chain(ops)
    mechanism = classify_mechanism(expr, ops, fields)

    # 字段形状匹配（如果有 field_profiles）
    field_match = {'status': 'unknown', 'details': ['no field_profiles provided']}
    if field_profiles:
        matched_profiles = {f: field_profiles.get(f, {}) for f in fields if f in field_profiles}
        if matched_profiles:
            field_match = match_field_profile(mechanism, matched_profiles)

    return {
        'structure': structure,
        'construction_chain': chain,
        'mechanism': mechanism,
        'field_match': field_match,
        'fields': fields,
        'ops': ops,
    }


def batch_extract_tags(exprs: List[str], field_profiles: Optional[Dict[str, Dict]] = None) -> List[Dict]:
    """批量提取标签。"""
    return [extract_tags(e, field_profiles) for e in exprs]


def summarize_tags(tags_list: List[Dict]) -> Dict:
    """汇总标签统计。"""
    n = len(tags_list)
    if n == 0:
        return {'total': 0}

    structure_counts = collections.Counter(t['structure'] for t in tags_list)
    mechanism_counts = collections.Counter(t['mechanism'] for t in tags_list)
    chain_counts = collections.Counter(
        tuple(t['construction_chain']) for t in tags_list
    )
    field_match_status = collections.Counter(
        t['field_match']['status'] for t in tags_list
    )

    return {
        'total': n,
        'structure': dict(structure_counts),
        'mechanism': dict(mechanism_counts),
        'construction_chain': {str(k): v for k, v in chain_counts.items()},
        'field_match': dict(field_match_status),
        'structure_share': {k: round(v / n, 3) for k, v in structure_counts.items()},
        'mechanism_share': {k: round(v / n, 3) for k, v in mechanism_counts.items()},
    }


# ---- 默认配额配置 ----
DEFAULT_QUOTA = {
    'structure': {
        'linear_2leg': 0.25,
        'linear_3plus': 0.15,
        'group_relative': 0.15,
        'group_bucket': 0.05,
        'ratio_pair': 0.10,
        'ratio_adjusted': 0.05,
        'event_gated': 0.10,
        'event_freshness': 0.05,
        'single_raw': 0.05,
        'single_preprocessed': 0.03,
        'single_aggregated': 0.02,
    },
    'mechanism': {
        'analyst_revision': 0.15,
        'target_price': 0.10,
        'event_conviction': 0.10,
        'event_gated': 0.10,
        'spread_pair': 0.10,
        'momentum': 0.10,
        'mean_reversion': 0.05,
        'volume_price': 0.05,
        'volatility_premium': 0.05,
        'liquidity_premium': 0.05,
        'multi_horizon': 0.05,
        'confidence_weighted': 0.05,
        'ceiling_suppress': 0.03,
        'discrete_score': 0.03,
        'low_freq_backfill': 0.02,
        'free_explore': 0.02,
    },
}


if __name__ == '__main__':
    # 简单测试
    test_exprs = [
        "rank(field)",
        "ts_backfill(field, 22)",
        "vec_avg(field)",
        "group_rank(field, industry)",
        "divide(rank(A), rank(B))",
        "add(multiply(rank(A), 0.4), multiply(rank(B), 0.6))",
        "trade_when(cond, signal, 0)",
        "group_rank(ts_delta(vec_avg(eps_cnt), 22), industry)",
        "divide(abs(returns), volume)",
        "reverse(ts_corr(rank(price), rank(volume), 10))",
    ]

    print("=== 多维骨架标签测试 ===\n")
    for expr in test_exprs:
        tags = extract_tags(expr)
        print(f"表达式: {expr}")
        print(f"  结构: {tags['structure']}")
        print(f"  构造链: {tags['construction_chain']}")
        print(f"  机制: {tags['mechanism']}")
        print(f"  字段: {tags['fields']}")
        print()

    print("=== 批量汇总 ===")
    tags_list = batch_extract_tags(test_exprs)
    summary = summarize_tags(tags_list)
    print(f"总计: {summary['total']} 条")
    print(f"结构分布: {summary['structure']}")
    print(f"机制分布: {summary['mechanism']}")
