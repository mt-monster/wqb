#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""corr_precheck.py — 相关性墙预判前置 (2026-08-18 wave33 教训)

背景: wave33 3个候选全硬闸过(sh1.76-1.79 2Y2.1)但 self_corr 0.78 撞 1YzLbZzQ, 浪费3条配额
核心: 设计阶段预判与 ACTIVE alpha 的核心字段重叠, 高风险候选先跑 compute_mutual_correlation

用法:
  python tools/corr_precheck.py --region KOR --exprs "expr1" "expr2" ...
  python tools/corr_precheck.py --region KOR --file exprs.txt --threshold 0.5
退出码: 0=全部低风险, 1=存在高风险
"""
import argparse
import json
import os
import re
import sys

# 添加项目根目录到路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def extract_core_fields(expr):
    """提取表达式中的核心字段 (非算子/非平台字段/非分组字段/非命名参数)"""
    # 平台内置字段
    platform = {'open', 'high', 'low', 'close', 'vwap', 'returns', 'adv20', 'adv60',
                'cap', 'sharesout', 'volume', 'cap3', 'rank', 'sector', 'industry',
                'subindustry', 'country', 'exchange', 'sector_country',
                'industry_country', 'sector_exchange', 'date', 'bucket'}
    # 命名参数关键字 (filter=true 等)
    named_params = {'filter', 'true', 'false', 'hump', 'k'}
    # 算子列表 (简化版, 从 expr_lint 导入)
    ops = {'add', 'multiply', 'subtract', 'max', 'min', 'sign', 'log', 'abs', 'sqrt',
           'inverse', 'reverse', 'pasteurize', 'densify', 'divide', 'power',
           'signed_power', 'or', 'and', 'not', 'is_nan', 'if_else', 'equal',
           'not_equal', 'greater', 'greater_equal', 'less', 'less_equal',
           'ts_corr', 'ts_zscore', 'ts_returns', 'ts_product', 'ts_std_dev',
           'ts_backfill', 'days_from_last_change', 'last_diff_value',
           'ts_scale', 'ts_sum', 'ts_av_diff', 'ts_kurtosis', 'ts_mean',
           'ts_arg_max', 'ts_rank', 'ts_ir', 'ts_delay', 'ts_quantile',
           'ts_count_nans', 'ts_covariance', 'ts_decay_linear', 'ts_arg_min',
           'ts_regression', 'ts_max_diff', 'kth_element', 'hump', 'ts_delta',
           'ts_step', 'ts_target_tvr_decay', 'ts_target_tvr_hump',
           'winsorize', 'rank', 'zscore', 'scale', 'normalize', 'quantile',
           'vec_min', 'vec_max', 'vec_avg', 'vec_sum', 'vec_count',
           'vec_stddev', 'vec_range', 'bucket', 'tail', 'trade_when',
           'group_mean', 'group_rank', 'group_backfill', 'group_scale',
           'group_count', 'group_zscore', 'group_std_dev', 'group_sum',
           'group_neutralize', 'group_cartesian_product'}
    
    idents = set(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', expr))
    fields = idents - ops - platform - named_params
    return sorted(fields)


def load_active_alphas(region):
    """加载该区域 ACTIVE alpha 列表 (从平台或本地缓存)"""
    # 优先从本地缓存读取 (避免频繁调 API)
    cache_path = os.path.join(PROJECT_ROOT, 'tracking', region, 'reference', f'{region.lower()}_active_alphas.json')
    if os.path.exists(cache_path):
        with open(cache_path, encoding='utf-8') as f:
            return json.load(f)
    
    # 本地无缓存, 返回空列表 (需先跑 fetch_active_alphas.py)
    print(f"[WARN] 无 ACTIVE alpha 缓存: {cache_path}")
    print(f"[WARN] 请先跑: python tools/fetch_active_alphas.py --region {region}")
    return []


def compute_field_overlap(expr_fields, active_fields):
    """计算字段重叠度"""
    if not active_fields:
        return 0.0, []
    overlap = set(expr_fields) & set(active_fields)
    ratio = len(overlap) / len(expr_fields) if expr_fields else 0.0
    return ratio, sorted(overlap)


def precheck(exprs, region, threshold=0.5):
    """相关性预判主函数"""
    active_alphas = load_active_alphas(region)
    if not active_alphas:
        print(f"[WARN] {region} 无 ACTIVE alpha 数据, 跳过相关性预判")
        return []
    
    # 提取所有 ACTIVE alpha 的核心字段
    active_fields_map = {}
    for alpha in active_alphas:
        alpha_id = alpha.get('id', 'unknown')
        alpha_expr = alpha.get('expr', '')
        active_fields_map[alpha_id] = extract_core_fields(alpha_expr)
    
    results = []
    for i, expr in enumerate(exprs, 1):
        expr_fields = extract_core_fields(expr)
        high_risk = []
        
        for alpha_id, active_fields in active_fields_map.items():
            ratio, overlap = compute_field_overlap(expr_fields, active_fields)
            if ratio >= threshold:
                high_risk.append({
                    'alpha_id': alpha_id,
                    'overlap_ratio': ratio,
                    'overlap_fields': overlap
                })
        
        results.append({
            'index': i,
            'expr': expr,
            'fields': expr_fields,
            'high_risk': high_risk,
            'risk_level': 'HIGH' if high_risk else 'LOW'
        })
    
    return results


def main():
    ap = argparse.ArgumentParser(description='相关性墙预判前置')
    ap.add_argument('--region', required=True, help='区域代码 (KOR/USA/EUR...)')
    ap.add_argument('--file', help='候选表达式文件')
    ap.add_argument('--exprs', nargs='+', help='直接传表达式')
    ap.add_argument('--threshold', type=float, default=0.5, help='字段重叠阈值 (默认0.5)')
    args = ap.parse_args()
    
    exprs = []
    if args.file:
        with open(args.file, encoding='utf-8') as f:
            exprs = [ln.strip() for ln in f if ln.strip() and not ln.startswith('#')]
    elif args.exprs:
        exprs = args.exprs
    else:
        ap.error('need --file or --exprs')
    
    results = precheck(exprs, args.region, args.threshold)
    
    high_count = sum(1 for r in results if r['risk_level'] == 'HIGH')
    print(f"\n[相关性预判] 共 {len(results)} 条, 高风险 {high_count} 条, 低风险 {len(results) - high_count} 条")
    
    for r in results:
        if r['risk_level'] == 'HIGH':
            print(f"\n[HIGH] #{r['index']} {r['expr'][:80]}...")
            print(f"       字段: {r['fields']}")
            for hr in r['high_risk']:
                print(f"       撞车 {hr['alpha_id']}: 重叠度 {hr['overlap_ratio']:.1%}, 字段 {hr['overlap_fields']}")
            print(f"       建议: 先跑 compute_mutual_correlation 预判, 或换字段/结构")
        else:
            print(f"[LOW]  #{r['index']} {r['expr'][:80]}...")
    
    sys.exit(1 if high_count else 0)


if __name__ == '__main__':
    main()
