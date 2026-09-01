# -*- coding: utf-8 -*-
"""operator_diversity_analyzer.py - 算子多样性分析器.

分析候选池中算子使用情况，识别未使用算子，提出优化建议.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import os
import re
import sqlite3
import sys
from typing import Any, Dict, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 平台全部可用算子（从 pool_diversity.py 复制）
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

ALL_OPS = TS_OPS | GROUP_OPS | VEC_OPS | CONDITIONAL_OPS | PREPROCESS_OPS | MATH_OPS | {'pasteurize'}

# 算子分类
OP_CATEGORIES = {
    'ts': TS_OPS,
    'group': GROUP_OPS,
    'vec': VEC_OPS,
    'cond': CONDITIONAL_OPS,
    'preprocess': PREPROCESS_OPS,
    'math': MATH_OPS,
}


def extract_ops(expr: str) -> List[str]:
    """提取表达式中的算子."""
    idents = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', expr)
    return [t for t in idents if t in ALL_OPS]


def get_op_category(op: str) -> str:
    """获取算子类别."""
    for cat, ops in OP_CATEGORIES.items():
        if op in ops:
            return cat
    return 'other'


def load_expressions_from_db(region: str, wave: int = None, dataset: str = None) -> List[str]:
    """从 DB 加载表达式."""
    db_path = os.path.join(PROJECT_ROOT, 'data', 'wqb.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    sql = "SELECT expression FROM expressions WHERE region=?"
    params = [region]
    
    if wave:
        sql += " AND wave=?"
        params.append(str(wave))
    if dataset:
        sql += " AND dataset=?"
        params.append(dataset)
    
    cur.execute(sql, params)
    rows = [r[0] for r in cur.fetchall() if r[0]]
    conn.close()
    return rows


def analyze_operator_usage(exprs: List[str]) -> Dict[str, Any]:
    """分析算子使用情况."""
    # 统计算子使用
    op_counter = collections.Counter()
    for expr in exprs:
        ops = extract_ops(expr)
        op_counter.update(ops)
    
    # 按类别统计
    cat_counter = collections.Counter()
    for op, count in op_counter.items():
        cat = get_op_category(op)
        cat_counter[cat] += count
    
    # 识别未使用算子
    used_ops = set(op_counter.keys())
    unused_ops = ALL_OPS - used_ops
    
    # 按类别分组未使用算子
    unused_by_cat = {}
    for op in unused_ops:
        cat = get_op_category(op)
        if cat not in unused_by_cat:
            unused_by_cat[cat] = []
        unused_by_cat[cat].append(op)
    
    # 计算算子熵
    total = sum(op_counter.values())
    entropy = 0.0
    if total > 0:
        for count in op_counter.values():
            p = count / total
            entropy -= p * math.log2(p)
    
    # 计算覆盖率
    coverage = len(used_ops) / len(ALL_OPS) if ALL_OPS else 0.0
    
    # 识别过度使用算子（top 10%）
    sorted_ops = sorted(op_counter.items(), key=lambda x: -x[1])
    top_ops = sorted_ops[:max(1, len(sorted_ops) // 10)]
    
    return {
        'total_expressions': len(exprs),
        'total_operators_used': len(used_ops),
        'total_operators_available': len(ALL_OPS),
        'coverage_rate': round(coverage, 3),
        'operator_entropy': round(entropy, 3),
        'operator_usage': dict(op_counter.most_common(50)),
        'category_usage': dict(cat_counter),
        'unused_operators': sorted(unused_ops),
        'unused_by_category': {k: sorted(v) for k, v in unused_by_cat.items()},
        'top_operators': dict(top_ops),
        'underused_operators': [
            op for op, count in sorted_ops
            if count < total * 0.01  # 使用少于 1%
        ][:20],
    }


def generate_recommendations(analysis: Dict[str, Any]) -> List[str]:
    """生成优化建议."""
    recommendations = []
    
    # 覆盖率建议
    coverage = analysis['coverage_rate']
    if coverage < 0.3:
        recommendations.append(
            f"算子覆盖率仅 {coverage:.0%}，建议探索未使用算子以提升多样性"
        )
    elif coverage < 0.5:
        recommendations.append(
            f"算子覆盖率 {coverage:.0%}，仍有提升空间"
        )
    
    # 熵建议
    entropy = analysis['operator_entropy']
    if entropy < 2.0:
        recommendations.append(
            f"算子熵 {entropy:.2f} 偏低，算子分布过于集中"
        )
    
    # 未使用算子建议
    unused_count = len(analysis['unused_operators'])
    if unused_count > 0:
        recommendations.append(
            f"发现 {unused_count} 个未使用算子，建议引入以提升多样性"
        )
        
        # 按类别推荐
        for cat, ops in analysis['unused_by_category'].items():
            if len(ops) >= 3:
                recommendations.append(
                    f"  - {cat} 类：{', '.join(ops[:5])} 等 {len(ops)} 个算子未使用"
                )
    
    # 过度使用建议
    top_ops = analysis['top_operators']
    if top_ops:
        top_op, top_count = next(iter(top_ops.items()))
        total = sum(analysis['operator_usage'].values())
        if top_count / total > 0.3:
            recommendations.append(
                f"算子 '{top_op}' 使用占比 {top_count/total:.0%} 过高，建议减少使用"
            )
    
    # 类别平衡建议
    cat_usage = analysis['category_usage']
    total_usage = sum(cat_usage.values())
    for cat, count in cat_usage.items():
        share = count / total_usage if total_usage > 0 else 0
        if share > 0.5:
            recommendations.append(
                f"{cat} 类算子使用占比 {share:.0%} 过高，建议增加其他类别"
            )
    
    return recommendations


def generate_expression_templates(analysis: Dict[str, Any]) -> List[Dict[str, str]]:
    """生成使用未使用算子的表达式模板."""
    templates = []
    unused = analysis['unused_by_category']
    
    # TS 类模板
    if 'ts' in unused:
        ts_ops = unused['ts'][:3]
        for op in ts_ops:
            if op == 'ts_corr':
                templates.append({
                    'category': 'ts',
                    'operator': op,
                    'template': f'rank({op}(field_a, field_b, 10))',
                    'description': '字段间时序相关性'
                })
            elif op == 'ts_regression':
                templates.append({
                    'category': 'ts',
                    'operator': op,
                    'template': f'rank({op}(field, market_return, 20, 0))',
                    'description': '字段对市场回归残差'
                })
            elif op == 'ts_kurtosis':
                templates.append({
                    'category': 'ts',
                    'operator': op,
                    'template': f'rank({op}(returns, 20))',
                    'description': '收益率峰度（尾部风险）'
                })
    
    # Group 类模板
    if 'group' in unused:
        group_ops = unused['group'][:3]
        for op in group_ops:
            if op == 'group_cartesian_product':
                templates.append({
                    'category': 'group',
                    'operator': op,
                    'template': f'rank({op}(field, industry))',
                    'description': '字段与行业笛卡尔积'
                })
            elif op == 'group_vector_neut':
                templates.append({
                    'category': 'group',
                    'operator': op,
                    'template': f'rank({op}(field, industry, market))',
                    'description': '向量中性化'
                })
    
    # Conditional 类模板
    if 'cond' in unused:
        cond_ops = unused['cond'][:2]
        for op in cond_ops:
            if op == 'trade_when':
                templates.append({
                    'category': 'cond',
                    'operator': op,
                    'template': f'{op}(rank(field) > 0.7, rank(field), 0)',
                    'description': '条件交易（高分位才持有）'
                })
    
    # Math 类模板
    if 'math' in unused:
        math_ops = unused['math'][:3]
        for op in math_ops:
            if op == 'signed_power':
                templates.append({
                    'category': 'math',
                    'operator': op,
                    'template': f'rank({op}(field, 0.5))',
                    'description': '保留符号的幂变换'
                })
            elif op == 'kth_element':
                templates.append({
                    'category': 'math',
                    'operator': op,
                    'template': f'rank({op}(field, industry, 3))',
                    'description': '行业内第 3 大值'
                })
    
    return templates


def main():
    ap = argparse.ArgumentParser(description="算子多样性分析器")
    ap.add_argument("--region", required=True, help="区域")
    ap.add_argument("--wave", type=int, help="波次")
    ap.add_argument("--dataset", help="数据集")
    ap.add_argument("--file", help="表达式文件（每行一条）")
    ap.add_argument("--exprs", nargs="+", help="直接传表达式")
    ap.add_argument("--json", help="JSON 输出路径")
    ap.add_argument("--detail", action="store_true", help="详细输出")
    args = ap.parse_args()
    
    # 加载表达式
    if args.file:
        with open(args.file, encoding='utf-8') as f:
            exprs = [line.strip() for line in f if line.strip()]
    elif args.exprs:
        exprs = args.exprs
    else:
        exprs = load_expressions_from_db(args.region, args.wave, args.dataset)
    
    if not exprs:
        print("Error: 未找到表达式")
        sys.exit(1)
    
    # 分析
    analysis = analyze_operator_usage(exprs)
    
    # 生成建议
    recommendations = generate_recommendations(analysis)
    analysis['recommendations'] = recommendations
    
    # 生成模板
    templates = generate_expression_templates(analysis)
    analysis['expression_templates'] = templates
    
    # 输出
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"JSON 报告已保存： {args.json}")
    
    # 人类可读报告
    print(f"\n{'='*70}")
    print(f"算子多样性分析 - {args.region}" + (f" Wave {args.wave}" if args.wave else ""))
    print(f"{'='*70}")
    print(f"表达式总数： {analysis['total_expressions']}")
    print(f"已使用算子： {analysis['total_operators_used']} / {analysis['total_operators_available']}")
    print(f"覆盖率： {analysis['coverage_rate']:.1%}")
    print(f"算子熵： {analysis['operator_entropy']:.2f}")
    
    print(f"\n{'='*70}")
    print("算子使用 TOP 10")
    print(f"{'='*70}")
    for i, (op, count) in enumerate(list(analysis['operator_usage'].items())[:10], 1):
        share = count / sum(analysis['operator_usage'].values())
        print(f"{i:2d}. {op:25s} {count:4d} 次 ({share:.1%})")
    
    print(f"\n{'='*70}")
    print("类别使用分布")
    print(f"{'='*70}")
    for cat, count in sorted(analysis['category_usage'].items(), key=lambda x: -x[1]):
        share = count / sum(analysis['category_usage'].values())
        print(f"{cat:15s} {count:4d} 次 ({share:.1%})")
    
    print(f"\n{'='*70}")
    print(f"未使用算子 ({len(analysis['unused_operators'])} 个)")
    print(f"{'='*70}")
    for cat, ops in analysis['unused_by_category'].items():
        print(f"\n{cat} 类 ({len(ops)} 个):")
        for op in ops[:10]:
            print(f"  - {op}")
        if len(ops) > 10:
            print(f"  ... 还有 {len(ops) - 10} 个")
    
    print(f"\n{'='*70}")
    print("优化建议")
    print(f"{'='*70}")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    
    if templates:
        print(f"\n{'='*70}")
        print("表达式模板（使用未使用算子）")
        print(f"{'='*70}")
        for i, tmpl in enumerate(templates[:10], 1):
            print(f"\n{i}. {tmpl['operator']} ({tmpl['category']})")
            print(f"   描述： {tmpl['description']}")
            print(f"   模板： {tmpl['template']}")
    
    # 退出码
    if analysis['coverage_rate'] < 0.3 or analysis['operator_entropy'] < 2.0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
