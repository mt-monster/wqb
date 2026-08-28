#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pool_diversity.py — 候选池表达式结构多样性评估体系（建议2落地，2026-08-27）

对候选池做六维结构多样性评估，回测前输出报告 + 风险标注：
  1. 算子熵/覆盖率：算子家族分布是否单一
  2. 骨架配额：单字段 / 2腿线性组合 / 3腿+ / 事件门控 / 分组结构 的占比
  3. 字段集中度：字段使用分布 + 字段族集中度（HHI）
  4. 预处理多样性：rank/ts_zscore/ts_backfill/group_zscore/ts_decay_linear 等分布
  5. 结构相似度：池内成对 op-multiset Jaccard，报同质对占比
  6. 风险标注：同字段族同骨架批 >60% 标红（回测必高相关）

输入源（优先级）：--file（每行一条表达式）> --exprs > DB（--region --wave [--dataset]）
输出：stdout 人类报告；--json 落盘结构化报告

用法:
  python tools/pool_diversity.py --region USA --wave 28 --dataset model238
  python tools/pool_diversity.py --file candidates.txt --json out.json
退出码: 0=多样性合格, 1=存在同质化风险（可串入 pipeline）
"""
import argparse
import collections
import json
import math
import os
import re
import sqlite3
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- 算子分类（用于算子家族统计与骨架识别）----
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
# 预处理（信号整形）算子：出现在字段外层即为"预处理选择"
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
PLATFORM_FIELDS = {
    'open', 'high', 'low', 'close', 'vwap', 'returns', 'adv20', 'adv60',
    'adv120', 'cap', 'cap3', 'sharesout', 'volume', 'sector', 'industry',
    'subindustry', 'country', 'exchange', 'sector_country',
    'industry_country', 'sector_exchange', 'date', 'bucket',
}
ALL_OPS = TS_OPS | GROUP_OPS | VEC_OPS | CONDITIONAL_OPS | PREPROCESS_OPS | MATH_OPS | {'pasteurize'}


def extract_ops(expr):
    """提取表达式中出现的所有算子（按出现次数计）。"""
    idents = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', expr)
    return [t for t in idents if t in ALL_OPS]


def extract_fields(expr):
    """提取数据字段（排除算子与平台内置字段）。"""
    idents = set(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', expr))
    callables = set(re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', expr))
    named_params = {'filter', 'true', 'false', 'hump', 'k'}
    return sorted(idents - callables - ALL_OPS - PLATFORM_FIELDS - named_params)


def classify_skeleton(expr):
    """骨架分类：数 add 下的 multiply 腿数。"""
    ops = extract_ops(expr)
    if 'trade_when' in ops or 'if_else' in ops:
        return 'event_gated'
    has_group = any(o in GROUP_OPS for o in ops)
    n_mult = ops.count('multiply')
    n_add = ops.count('add')
    if n_add >= 1:
        legs = n_mult if n_mult >= 2 else 2
        if legs >= 3:
            return 'linear_mix_3plus'
        return 'linear_mix_2leg'
    if has_group and len(extract_fields(expr)) >= 1:
        return 'single_field_group'
    return 'single_field'


def op_family(op):
    if op in TS_OPS:
        return 'ts'
    if op in GROUP_OPS:
        return 'group'
    if op in VEC_OPS:
        return 'vec'
    if op in CONDITIONAL_OPS:
        return 'cond'
    if op in PREPROCESS_OPS:
        return 'preprocess'
    return 'math'


def field_family(field):
    """字段族：下划线首段；短字段取前 6 字符。"""
    if '_' in field:
        return field.split('_')[0]
    return field[:6]


def shannon_entropy(counter):
    total = sum(counter.values())
    if total == 0:
        return 0.0
    h = 0.0
    for n in counter.values():
        p = n / total
        h -= p * math.log2(p)
    return h


def hhi(counter):
    """Herfindahl 集中度：0=均匀，1=全集中。"""
    total = sum(counter.values())
    if total == 0:
        return 0.0
    return sum((n / total) ** 2 for n in counter.values())


def jaccard_multiset(a, b):
    ca, cb = collections.Counter(a), collections.Counter(b)
    inter = sum((ca & cb).values())
    union = sum((ca | cb).values())
    return inter / union if union else 1.0


def load_from_db(region, wave, dataset=None):
    db_path = os.path.join(PROJECT_ROOT, 'data', 'wqb.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = "SELECT expression FROM expressions WHERE region=? AND wave=?"
    params = [region, str(wave)]
    if dataset:
        sql += " AND dataset=?"
        params.append(dataset)
    cur.execute(sql, params)
    rows = [r[0] for r in cur.fetchall() if r[0]]
    conn.close()
    return rows


def assess(exprs, region=None):
    """六维多样性评估主函数，返回结构化报告。"""
    n = len(exprs)
    parsed = []
    for e in exprs:
        ops = extract_ops(e)
        fields = extract_fields(e)
        parsed.append({
            'expr': e,
            'ops': ops,
            'fields': fields,
            'skeleton': classify_skeleton(e),
            'preprocess': sorted({o for o in ops if o in PREPROCESS_OPS}),
        })

    # 1. 算子熵/覆盖率
    op_counter = collections.Counter(op for p in parsed for op in p['ops'])
    fam_counter = collections.Counter(op_family(op) for op in op_counter.elements())
    op_entropy = shannon_entropy(op_counter)
    op_coverage = len(op_counter) / max(len(ALL_OPS), 1)

    # 2. 骨架配额
    skel_counter = collections.Counter(p['skeleton'] for p in parsed)
    skel_share = {k: v / n for k, v in skel_counter.items()}
    linear_mix_share = skel_share.get('linear_mix_2leg', 0) + skel_share.get('linear_mix_3plus', 0)

    # 3. 字段集中度
    field_counter = collections.Counter(f for p in parsed for f in p['fields'])
    fam_counter_f = collections.Counter(field_family(f) for f in field_counter.elements())
    field_hhi = hhi(field_counter)
    fam_hhi = hhi(fam_counter_f)

    # 4. 预处理多样性
    prep_counter = collections.Counter(pr for p in parsed for pr in p['preprocess'])
    prep_entropy = shannon_entropy(prep_counter)

    # 5. 结构相似度（池内成对，op 多重集 Jaccard）
    n_pairs, n_similar, similar_pairs = 0, 0, []
    for i in range(n):
        for j in range(i + 1, n):
            n_pairs += 1
            sim = jaccard_multiset(parsed[i]['ops'], parsed[j]['ops'])
            if sim > 0.8:
                n_similar += 1
                similar_pairs.append((i, j, round(sim, 3)))
    homog_ratio = n_similar / n_pairs if n_pairs else 0.0

    # 6. 风险标注：同字段族 + 同骨架 批占比
    group_counter = collections.Counter(
        (field_family(p['fields'][0]) if p['fields'] else 'nofield', p['skeleton'])
        for p in parsed
    )
    top_group, top_count = group_counter.most_common(1)[0] if group_counter else (('none', 'none'), 0)
    top_share = top_count / n if n else 0.0

    issues = []
    if op_entropy < 2.0:
        issues.append(f"[OP-ENTROPY] 算子熵 {op_entropy:.2f} < 2.0，算子使用过于集中")
    if homog_ratio > 0.7:
        issues.append(f"[HOMOG] 池内 {homog_ratio:.0%} 表达式对结构相似度 >0.8，同质化严重")
    if top_share > 0.6 and n >= 3:
        issues.append(
            f"[GROUP-DOMINANCE] {top_count}/{n} ({top_share:.0%}) 表达式共享 "
            f"字段族={top_group[0]} + 骨架={top_group[1]}，回测必高相关"
        )
    if linear_mix_share > 0.8 and skel_counter.get('event_gated', 0) == 0:
        issues.append(
            f"[SKELETON] 线性组合骨架占 {linear_mix_share:.0%} 且无事件门控骨架，"
            "CW（CONCENTRATED_WEIGHT）墙风险高"
        )

    return {
        'total': n,
        'region': region,
        'operator_stats': {
            'unique_ops': len(op_counter),
            'entropy': round(op_entropy, 3),
            'family_distribution': dict(fam_counter),
            'top_ops': op_counter.most_common(8),
        },
        'skeleton_quota': {k: round(v, 3) for k, v in skel_share.items()},
        'field_stats': {
            'unique_fields': len(field_counter),
            'field_hhi': round(field_hhi, 3),
            'family_hhi': round(fam_hhi, 3),
            'family_distribution': dict(fam_counter_f),
            'top_fields': field_counter.most_common(8),
        },
        'preprocess_stats': {
            'entropy': round(prep_entropy, 3),
            'distribution': dict(prep_counter),
        },
        'structural_similarity': {
            'pairs': n_pairs,
            'similar_pairs': n_similar,
            'homog_ratio': round(homog_ratio, 3),
            'examples': similar_pairs[:5],
        },
        'dominant_group': {
            'field_family': top_group[0],
            'skeleton': top_group[1],
            'count': top_count,
            'share': round(top_share, 3),
        },
        'issues': issues,
        'passed': not issues,
    }


def print_report(r):
    print(f"[多样性评估] 候选池 {r['total']} 条" + (f"（region={r['region']}）" if r['region'] else ''))
    o = r['operator_stats']
    print(f"  算子: {o['unique_ops']} 种, 熵={o['entropy']}, 家族分布={o['family_distribution']}")
    print(f"  骨架配额: {r['skeleton_quota']}")
    f = r['field_stats']
    print(f"  字段: {f['unique_fields']} 个, HHI={f['field_hhi']}, 字段族HHI={f['family_hhi']}, 族分布={f['family_distribution']}")
    p = r['preprocess_stats']
    print(f"  预处理: 熵={p['entropy']}, 分布={p['distribution']}")
    s = r['structural_similarity']
    print(f"  结构相似度: {s['pairs']} 对中 {s['similar_pairs']} 对 >0.8（同质占比 {s['homog_ratio']:.0%}）")
    d = r['dominant_group']
    print(f"  主导组: 字段族={d['field_family']} 骨架={d['skeleton']} 占 {d['count']}/{r['total']}")
    if r['issues']:
        print(f"  [FAIL] {len(r['issues'])} 项风险:")
        for it in r['issues']:
            print(f"    - {it}")
    else:
        print("  [PASS] 未发现同质化风险")


def main():
    ap = argparse.ArgumentParser(description='候选池表达式结构多样性评估')
    ap.add_argument('--region', help='区域（DB 模式必填）')
    ap.add_argument('--wave', help='波次（DB 模式必填）')
    ap.add_argument('--dataset', help='数据集（DB 模式可选）')
    ap.add_argument('--file', help='候选表达式文件（每行一条）')
    ap.add_argument('--exprs', nargs='+', help='直接传表达式')
    ap.add_argument('--json', help='结构化报告落盘路径')
    a = ap.parse_args()

    if a.file:
        with open(a.file, encoding='utf-8') as fh:
            exprs = [ln.strip() for ln in fh if ln.strip() and not ln.startswith('#')]
    elif a.exprs:
        exprs = a.exprs
    elif a.region and a.wave:
        exprs = load_from_db(a.region, a.wave, a.dataset)
    else:
        ap.error('需要 --file / --exprs / (--region --wave)')

    if not exprs:
        print('[error] 无候选表达式')
        sys.exit(1)

    report = assess(exprs, region=a.region)
    print_report(report)
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
        print(f"[done] 报告已落盘: {a.json}")
    sys.exit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
