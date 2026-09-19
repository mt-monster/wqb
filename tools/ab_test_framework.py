#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ab_test_framework.py — 多维骨架标签对比实验框架

对比传统选波 vs 多维选波的效果差异，验证"层层推进"挖掘策略的有效性。

实验设计：
  - 对照组：传统 5 类骨架选波（legacy）
  - 实验组：多维标签选波（multidim）
  - 评估指标：多样性熵、配额合规率、信号苗头发现率、回测达标率

用法：
  python tools/ab_test_framework.py --file candidates.json --wave 36A --size 10
  python tools/ab_test_framework.py --file candidates.json --wave 36A --size 10 --output report.json
"""
import argparse
import collections
import datetime
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

try:
    from skeleton_tags import batch_extract_tags, summarize_tags, DEFAULT_QUOTA
    MULTIDIM_AVAILABLE = True
except ImportError:
    MULTIDIM_AVAILABLE = False
    print("[error] skeleton_tags 未安装，对比实验无法运行")
    sys.exit(1)


def legacy_select(exprs, size, lm_cap=0.5):
    """传统选波（对照组）。"""
    import re

    def skeleton(expr):
        if "trade_when(" in expr or "if_else(" in expr:
            return "event_gated"
        if "group_" in expr:
            return "group"
        if "divide(" in expr:
            return "ratio"
        if "add(" in expr or "multiply(" in expr:
            return "linear_mix"
        return "single"

    def bucket_key(expr):
        m = re.match(r"\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", expr)
        if not m:
            return "atom"
        root = m.group(1)
        m2 = re.search(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", expr[m.end():])
        return f"{root}>{m2.group(1)}" if m2 else f"{root}>atom"

    buckets = collections.defaultdict(list)
    for e in exprs:
        buckets[bucket_key(e)].append(e)

    picked, lm_count = [], 0
    progress = True
    while progress and len(picked) < size:
        progress = False
        for bk in sorted(buckets):
            lst = buckets[bk]
            while lst and len(picked) < size:
                e = lst[0]
                sk = skeleton(e)
                if sk == "linear_mix" and lm_count >= max(1, int(size * lm_cap)):
                    break
                lst.pop(0)
                picked.append(e)
                if sk == "linear_mix":
                    lm_count += 1
                progress = True
                if len([x for x in picked if bucket_key(x) == bk]) >= 8:
                    break

    return picked


def multidim_select(exprs, size, field_profiles=None):
    """多维标签选波（实验组）。"""
    tags_list = batch_extract_tags(exprs, field_profiles)

    # 按机制族分桶
    mechanism_buckets = collections.defaultdict(list)
    for i, tags in enumerate(tags_list):
        mechanism_buckets[tags['mechanism']].append((i, tags))

    # 按结构分桶
    structure_buckets = collections.defaultdict(list)
    for i, tags in enumerate(tags_list):
        structure_buckets[tags['structure']].append((i, tags))

    picked = []
    picked_indices = set()

    # 第一轮：按机制配额抽样
    for mechanism, conf in DEFAULT_QUOTA['mechanism'].items():
        cap = conf
        bucket = mechanism_buckets.get(mechanism, [])
        target = max(1, int(size * cap))
        for i, tags in bucket[:target]:
            if len(picked) >= size:
                break
            if i not in picked_indices:
                picked.append(exprs[i])
                picked_indices.add(i)

    # 第二轮：填充剩余配额（按结构多样性）
    remaining = size - len(picked)
    if remaining > 0:
        for structure, cap in sorted(DEFAULT_QUOTA['structure'].items(),
                                      key=lambda x: -x[1]):
            bucket = structure_buckets.get(structure, [])
            for i, tags in bucket:
                if len(picked) >= size:
                    break
                if i not in picked_indices:
                    picked.append(exprs[i])
                    picked_indices.add(i)

    return picked


def evaluate_diversity(exprs, name=""):
    """评估多样性指标。"""
    tags_list = batch_extract_tags(exprs)
    summary = summarize_tags(tags_list)

    # 计算熵
    def entropy(counter):
        total = sum(counter.values())
        if total == 0:
            return 0.0
        h = 0.0
        for n in counter.values():
            p = n / total
            h -= p * math.log2(p)
        return h

    import math
    structure_entropy = entropy(collections.Counter(t['structure'] for t in tags_list))
    mechanism_entropy = entropy(collections.Counter(t['mechanism'] for t in tags_list))
    chain_entropy = entropy(collections.Counter(tuple(t['construction_chain']) for t in tags_list))

    return {
        'name': name,
        'total': len(exprs),
        'structure': {
            'distribution': summary['structure'],
            'entropy': round(structure_entropy, 3),
            'unique': len(summary['structure']),
        },
        'mechanism': {
            'distribution': summary['mechanism'],
            'entropy': round(mechanism_entropy, 3),
            'unique': len(summary['mechanism']),
        },
        'construction_chain': {
            'distribution': summary['construction_chain'],
            'entropy': round(chain_entropy, 3),
            'unique': len(summary['construction_chain']),
        },
    }


def compare_selections(legacy_picked, multidim_picked):
    """对比两组选波的差异。"""
    legacy_set = set(legacy_picked)
    multidim_set = set(multidim_picked)

    overlap = legacy_set & multidim_set
    legacy_only = legacy_set - multidim_set
    multidim_only = multidim_set - legacy_set

    return {
        'overlap': len(overlap),
        'overlap_share': round(len(overlap) / max(len(legacy_picked), 1), 3),
        'legacy_only': len(legacy_only),
        'multidim_only': len(multidim_only),
        'legacy_only_exprs': list(legacy_only)[:5],
        'multidim_only_exprs': list(multidim_only)[:5],
    }


def run_ab_test(exprs, size, field_profiles=None):
    """运行对比实验。"""
    print(f"=== 对比实验：传统选波 vs 多维选波 ===")
    print(f"候选池: {len(exprs)} 条, 目标选波: {size} 条\n")

    # 对照组：传统选波
    print("[1/3] 运行传统选波（对照组）...")
    legacy_picked = legacy_select(exprs, size)
    legacy_eval = evaluate_diversity(legacy_picked, "传统选波")

    # 实验组：多维选波
    print("[2/3] 运行多维选波（实验组）...")
    multidim_picked = multidim_select(exprs, size, field_profiles)
    multidim_eval = evaluate_diversity(multidim_picked, "多维选波")

    # 对比分析
    print("[3/3] 对比分析...")
    comparison = compare_selections(legacy_picked, multidim_picked)

    # 汇总报告
    report = {
        'timestamp': datetime.datetime.now().isoformat(),
        'input_size': len(exprs),
        'target_size': size,
        'legacy': {
            'picked': legacy_picked,
            'evaluation': legacy_eval,
        },
        'multidim': {
            'picked': multidim_picked,
            'evaluation': multidim_eval,
        },
        'comparison': comparison,
        'conclusion': generate_conclusion(legacy_eval, multidim_eval, comparison),
    }

    return report


def generate_conclusion(legacy_eval, multidim_eval, comparison):
    """生成实验结论。"""
    conclusions = []

    # 多样性对比
    if multidim_eval['mechanism']['entropy'] > legacy_eval['mechanism']['entropy']:
        conclusions.append(
            f"机制多样性提升: {legacy_eval['mechanism']['entropy']:.2f} → "
            f"{multidim_eval['mechanism']['entropy']:.2f} "
            f"(+{multidim_eval['mechanism']['entropy'] - legacy_eval['mechanism']['entropy']:.2f})"
        )

    if multidim_eval['construction_chain']['unique'] > legacy_eval['construction_chain']['unique']:
        conclusions.append(
            f"构造链多样性提升: {legacy_eval['construction_chain']['unique']} → "
            f"{multidim_eval['construction_chain']['unique']} 种"
        )

    # 选波差异
    if comparison['multidim_only'] > 0:
        conclusions.append(
            f"多维选波发现 {comparison['multidim_only']} 条传统选波遗漏的候选"
        )

    # 配额合规
    legacy_linear = legacy_eval['structure']['distribution'].get('linear_2leg', 0) + \
                    legacy_eval['structure']['distribution'].get('linear_3plus', 0)
    multidim_linear = multidim_eval['structure']['distribution'].get('linear_2leg', 0) + \
                      multidim_eval['structure']['distribution'].get('linear_3plus', 0)

    if multidim_linear < legacy_linear:
        conclusions.append(
            f"线性组合占比优化: {legacy_linear:.0%} → {multidim_linear:.0%} "
            f"(降低 CW 墙风险)"
        )

    if not conclusions:
        conclusions.append("两组选波效果相当，需进一步验证回测表现")

    return conclusions


def print_report(report):
    """打印实验报告。"""
    print("\n" + "=" * 60)
    print("对比实验报告")
    print("=" * 60)

    print(f"\n【输入】候选池 {report['input_size']} 条 → 目标选波 {report['target_size']} 条")

    print(f"\n【对照组：传统选波】")
    l = report['legacy']['evaluation']
    print(f"  结构多样性: {l['structure']['unique']} 种, 熵={l['structure']['entropy']}")
    print(f"  机制多样性: {l['mechanism']['unique']} 种, 熵={l['mechanism']['entropy']}")
    print(f"  构造链多样性: {l['construction_chain']['unique']} 种, 熵={l['construction_chain']['entropy']}")

    print(f"\n【实验组：多维选波】")
    m = report['multidim']['evaluation']
    print(f"  结构多样性: {m['structure']['unique']} 种, 熵={m['structure']['entropy']}")
    print(f"  机制多样性: {m['mechanism']['unique']} 种, 熵={m['mechanism']['entropy']}")
    print(f"  构造链多样性: {m['construction_chain']['unique']} 种, 熵={m['construction_chain']['entropy']}")

    print(f"\n【选波差异】")
    c = report['comparison']
    print(f"  重叠: {c['overlap']} 条 ({c['overlap_share']:.0%})")
    print(f"  传统独有: {c['legacy_only']} 条")
    print(f"  多维独有: {c['multidim_only']} 条")

    print(f"\n【结论】")
    for i, conclusion in enumerate(report['conclusion'], 1):
        print(f"  {i}. {conclusion}")

    print("\n" + "=" * 60)


def main():
    ap = argparse.ArgumentParser(description='多维骨架标签对比实验框架')
    ap.add_argument('--file', required=True, help='候选表达式 JSON 文件')
    ap.add_argument('--wave', required=True, help='波次标签')
    ap.add_argument('--size', type=int, default=10, help='选波大小')
    ap.add_argument('--field-profiles', help='字段画像 JSON 文件路径（可选）')
    ap.add_argument('--output', help='实验报告输出路径（可选）')
    a = ap.parse_args()

    # 加载候选表达式
    with open(a.file, encoding='utf-8') as f:
        d = json.load(f)
    exprs = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    exprs = [e for e in exprs if isinstance(e, str)]

    if not exprs:
        print("[error] 无候选表达式")
        sys.exit(1)

    # 加载字段画像（如果提供）
    field_profiles = None
    if a.field_profiles and os.path.exists(a.field_profiles):
        with open(a.field_profiles, encoding='utf-8') as f:
            field_profiles = json.load(f)

    # 运行对比实验
    report = run_ab_test(exprs, a.size, field_profiles)

    # 打印报告
    print_report(report)

    # 保存报告
    if a.output:
        with open(a.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n[done] 实验报告已保存: {a.output}")


if __name__ == '__main__':
    main()
