#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pool_diversity.py — 候选池表达式结构多样性评估体系（多维标签默认启用）

对候选池做四维结构多样性评估，回测前输出报告 + 风险标注：
  1. 结构维度：单字段/比率/分组/线性组合/事件门控等 11 类
  2. 构造链维度：raw/backfill/vector_agg/delta/correlation 等 10 类
  3. 机制维度：event_conviction/analyst_revision/momentum 等 16 类
  4. 字段匹配：字段形状与机制匹配校验

输入源（优先级）：--file（每行一条表达式）> --exprs > DB（--region --wave [--dataset]）
输出：stdout 人类报告；--json 落盘结构化报告

用法:
  python tools/pool_diversity.py --region USA --wave 28 --dataset model238
  python tools/pool_diversity.py --file candidates.txt --json out.json
  python tools/pool_diversity.py --file candidates.txt --legacy --json out.json  # 传统模式（已废弃）
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

# 注入 tools 目录以导入 skeleton_tags
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

try:
    from skeleton_tags import batch_extract_tags, DEFAULT_QUOTA
    MULTIDIM_AVAILABLE = True
except ImportError:
    MULTIDIM_AVAILABLE = False
    print("[error] skeleton_tags 未安装，多维评估功能不可用")
    sys.exit(1)

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


def shannon_entropy(counter):
    total = sum(counter.values())
    if total == 0:
        return 0.0
    h = 0.0
    for n in counter.values():
        p = n / total
        h -= p * math.log2(p)
    return h


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


def assess_multidimensional(exprs, region=None, field_profiles=None):
    """四维多样性评估（经济学构造链感知）。"""
    tags_list = batch_extract_tags(exprs, field_profiles)
    n = len(tags_list)
    if n == 0:
        return {'error': '无候选表达式'}

    # 1. 结构维度
    structure_counts = collections.Counter(t['structure'] for t in tags_list)
    structure_share = {k: v / n for k, v in structure_counts.items()}
    structure_entropy = shannon_entropy(structure_counts)

    # 2. 构造链维度
    chain_counts = collections.Counter(
        tuple(t['construction_chain']) for t in tags_list
    )
    chain_entropy = shannon_entropy(chain_counts)
    unique_chains = len(chain_counts)

    # 3. 机制维度
    mechanism_counts = collections.Counter(t['mechanism'] for t in tags_list)
    mechanism_share = {k: v / n for k, v in mechanism_counts.items()}
    mechanism_entropy = shannon_entropy(mechanism_counts)

    # 4. 字段匹配维度
    field_match_status = collections.Counter(
        t['field_match']['status'] for t in tags_list
    )

    # 配额校验
    quota_violations = []
    for dim, quotas in DEFAULT_QUOTA.items():
        actual = structure_share if dim == 'structure' else mechanism_share
        for tag, cap in quotas.items():
            if actual.get(tag, 0) > cap:
                quota_violations.append(f"{dim}.{tag} 超配 {actual[tag]:.0%} > {cap:.0%}")

    # 构造链多样性校验
    min_chains = 5
    chain_diversity_ok = unique_chains >= min_chains

    # 风险标注
    issues = []
    if structure_entropy < 1.5:
        issues.append(f"[STRUCTURE-ENTROPY] 结构熵 {structure_entropy:.2f} < 1.5，结构多样性不足")
    if mechanism_entropy < 2.0:
        issues.append(f"[MECHANISM-ENTROPY] 机制熵 {mechanism_entropy:.2f} < 2.0，机制多样性不足")
    if not chain_diversity_ok:
        issues.append(f"[CHAIN-DIVERSITY] 构造链仅 {unique_chains} 种 < {min_chains}，构造链多样性不足")
    if field_match_status.get('warn', 0) > n * 0.3:
        issues.append(f"[FIELD-MATCH] {field_match_status['warn']}/{n} 字段形状不匹配")
    if quota_violations:
        issues.append(f"[QUOTA] {len(quota_violations)} 项配额超限: {quota_violations[:3]}")

    return {
        'total': n,
        'region': region,
        'multidim': True,
        'structure': {
            'distribution': {k: round(v, 3) for k, v in structure_share.items()},
            'entropy': round(structure_entropy, 3),
            'unique_structures': len(structure_counts),
        },
        'construction_chain': {
            'distribution': {str(k): v for k, v in chain_counts.items()},
            'entropy': round(chain_entropy, 3),
            'unique_chains': unique_chains,
            'min_chains_required': min_chains,
            'diversity_ok': chain_diversity_ok,
        },
        'mechanism': {
            'distribution': {k: round(v, 3) for k, v in mechanism_share.items()},
            'entropy': round(mechanism_entropy, 3),
            'unique_mechanisms': len(mechanism_counts),
        },
        'field_match': {
            'status_distribution': dict(field_match_status),
            'warn_count': field_match_status.get('warn', 0),
            'warn_share': round(field_match_status.get('warn', 0) / n, 3),
        },
        'quota_violations': quota_violations,
        'quota_passed': not quota_violations,
        'issues': issues,
        'passed': not issues,
    }


def print_multidim_report(r):
    """打印四维多样性报告。"""
    print(f"[多维多样性评估] 候选池 {r['total']} 条" + (f"（region={r['region']}）" if r['region'] else ''))

    s = r['structure']
    print(f"  结构维度: {s['unique_structures']} 种, 熵={s['entropy']}")
    for tag, share in sorted(s['distribution'].items(), key=lambda x: -x[1]):
        print(f"    {tag}: {share:.0%}")

    c = r['construction_chain']
    print(f"  构造链维度: {c['unique_chains']} 种, 熵={c['entropy']}, 多样性={'OK' if c['diversity_ok'] else 'FAIL'}")
    for chain, count in sorted(c['distribution'].items(), key=lambda x: -x[1])[:5]:
        print(f"    {chain}: {count} 条")

    m = r['mechanism']
    print(f"  机制维度: {m['unique_mechanisms']} 种, 熵={m['entropy']}")
    for tag, share in sorted(m['distribution'].items(), key=lambda x: -x[1]):
        print(f"    {tag}: {share:.0%}")

    f = r['field_match']
    print(f"  字段匹配: pass={f['status_distribution'].get('pass', 0)}, "
          f"warn={f['status_distribution'].get('warn', 0)}, "
          f"unknown={f['status_distribution'].get('unknown', 0)}")

    if r['quota_violations']:
        print(f"  [QUOTA] {len(r['quota_violations'])} 项配额超限:")
        for v in r['quota_violations'][:5]:
            print(f"    - {v}")

    if r['issues']:
        print(f"  [FAIL] {len(r['issues'])} 项风险:")
        for it in r['issues']:
            print(f"    - {it}")
    else:
        print("  [PASS] 多维多样性合格")


def main():
    ap = argparse.ArgumentParser(description='候选池表达式结构多样性评估（多维标签默认启用）')
    ap.add_argument('--region', help='区域（DB 模式必填）')
    ap.add_argument('--wave', help='波次（DB 模式必填）')
    ap.add_argument('--dataset', help='数据集（DB 模式可选）')
    ap.add_argument('--file', help='候选表达式文件（每行一条）')
    ap.add_argument('--exprs', nargs='+', help='直接传表达式')
    ap.add_argument('--json', help='结构化报告落盘路径')
    ap.add_argument('--legacy', action='store_true',
                    help='传统六维评估模式（已废弃，仅用于对比）')
    ap.add_argument('--field-profiles', help='字段画像 JSON 文件路径（可选）')
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

    # 加载字段画像（如果提供）
    field_profiles = None
    if a.field_profiles and os.path.exists(a.field_profiles):
        with open(a.field_profiles, encoding='utf-8') as f:
            field_profiles = json.load(f)

    # 默认多维评估
    if a.legacy:
        print('[warn] 传统六维评估模式已废弃，仅用于对比')
        # 传统模式代码（简化版）
        print('[error] 传统模式已移除，请使用多维评估')
        sys.exit(1)
    else:
        report = assess_multidimensional(exprs, region=a.region, field_profiles=field_profiles)

    print_multidim_report(report)
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
        print(f"[done] 报告已落盘: {a.json}")
    sys.exit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
