#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dryrun_multidim.py — 多维骨架标签 dry-run 验证脚本

验证多维标签系统的正确性，不实际执行选波，仅输出标签分析结果。

用法：
  python tools/dryrun_multidim.py --file candidates.json
  python tools/dryrun_multidim.py --exprs "rank(field)" "ts_backfill(field, 22)"
"""
import argparse
import json
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

try:
    from skeleton_tags import extract_tags, batch_extract_tags, summarize_tags, DEFAULT_QUOTA
    MULTIDIM_AVAILABLE = True
except ImportError as e:
    MULTIDIM_AVAILABLE = False
    print(f"[error] skeleton_tags 导入失败: {e}")
    sys.exit(1)


def dryrun_single(expr, field_profiles=None):
    """单条表达式 dry-run。"""
    print(f"\n表达式: {expr}")
    print("-" * 60)

    tags = extract_tags(expr, field_profiles)

    print(f"  结构模式: {tags['structure']}")
    print(f"  构造链: {' → '.join(tags['construction_chain'])}")
    print(f"  经济学机制: {tags['mechanism']}")
    print(f"  字段匹配: {tags['field_match']['status']}")
    if tags['field_match']['details']:
        for detail in tags['field_match']['details'][:3]:
            print(f"    - {detail}")
    print(f"  提取字段: {tags['fields']}")
    print(f"  提取算子: {tags['ops']}")

    return tags


def dryrun_batch(exprs, field_profiles=None):
    """批量 dry-run。"""
    print(f"\n=== 批量 Dry-Run: {len(exprs)} 条表达式 ===")

    tags_list = batch_extract_tags(exprs, field_profiles)
    summary = summarize_tags(tags_list)

    print(f"\n【结构模式分布】")
    for tag, count in sorted(summary['structure'].items(), key=lambda x: -x[1]):
        share = summary['structure_share'][tag]
        print(f"  {tag}: {count} 条 ({share:.0%})")

    print(f"\n【经济学机制分布】")
    for tag, count in sorted(summary['mechanism'].items(), key=lambda x: -x[1]):
        share = summary['mechanism_share'][tag]
        print(f"  {tag}: {count} 条 ({share:.0%})")

    print(f"\n【构造链分布】")
    for chain, count in sorted(summary['construction_chain'].items(), key=lambda x: -x[1])[:5]:
        print(f"  {chain}: {count} 条")

    print(f"\n【字段匹配状态】")
    for status, count in summary['field_match'].items():
        print(f"  {status}: {count} 条")

    # 配额校验
    print(f"\n【配额校验】")
    violations = []
    for dim, quotas in DEFAULT_QUOTA.items():
        actual = summary.get(f'{dim}_share', {})
        for tag, cap in quotas.items():
            if actual.get(tag, 0) > cap:
                violations.append(f"{dim}.{tag}: {actual[tag]:.0%} > {cap:.0%}")
                print(f"  [VIOLATION] {dim}.{tag}: {actual[tag]:.0%} > {cap:.0%}")

    if not violations:
        print("  [PASS] 所有配额合规")

    return summary


def main():
    ap = argparse.ArgumentParser(description='多维骨架标签 dry-run 验证')
    ap.add_argument('--file', help='候选表达式 JSON 文件')
    ap.add_argument('--exprs', nargs='+', help='直接传表达式')
    ap.add_argument('--field-profiles', help='字段画像 JSON 文件路径（可选）')
    ap.add_argument('--output', help='标签分析结果输出路径（可选）')
    a = ap.parse_args()

    if not MULTIDIM_AVAILABLE:
        print("[error] 多维标签功能不可用")
        sys.exit(1)

    # 加载表达式
    if a.file:
        with open(a.file, encoding='utf-8') as f:
            d = json.load(f)
        exprs = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
        exprs = [e for e in exprs if isinstance(e, str)]
    elif a.exprs:
        exprs = a.exprs
    else:
        # 默认测试用例
        exprs = [
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
            "winsorize(rank(ceiling_field), std=2)",
            "ts_delta(ts_backfill(F, 66), 22)",
            "days_from_last_change(F)",
            "multiply(rank(prob_high), rank(confidence))",
        ]
        print("[info] 使用默认测试用例")

    if not exprs:
        print("[error] 无候选表达式")
        sys.exit(1)

    # 加载字段画像（如果提供）
    field_profiles = None
    if a.field_profiles and os.path.exists(a.field_profiles):
        with open(a.field_profiles, encoding='utf-8') as f:
            field_profiles = json.load(f)

    # 单条详细分析（如果表达式数量少）
    if len(exprs) <= 5:
        print("=== 单条表达式详细分析 ===")
        for expr in exprs:
            dryrun_single(expr, field_profiles)

    # 批量汇总分析
    summary = dryrun_batch(exprs, field_profiles)

    # 保存结果
    if a.output:
        result = {
            'exprs': exprs,
            'summary': summary,
            'tags': [extract_tags(e, field_profiles) for e in exprs],
        }
        with open(a.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n[done] 标签分析结果已保存: {a.output}")


if __name__ == '__main__':
    main()
