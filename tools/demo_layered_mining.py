#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demo_layered_mining.py — 层层推进挖掘策略演示

展示多维骨架标签如何支持"每阶段回测一下，发现信号的苗头好层层推进"的挖掘策略。

工作流程：
  1. S2 选波：多维标签确保机制多样性
  2. S3 预检：机制-形状匹配校验
  3. S4 评审：按机制族分析表现
  4. Mode B 优化：按机制族定向优化

用法：
  python tools/demo_layered_mining.py
"""
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from skeleton_tags import batch_extract_tags, summarize_tags


def demo_layered_mining():
    """演示层层推进挖掘策略。"""
    print("=" * 70)
    print("层层推进挖掘策略演示")
    print("=" * 70)

    # 模拟候选池
    candidates = [
        # 分析师修正机制
        "group_rank(ts_delta(vec_avg(eps_up_cnt), 22), industry)",
        "group_rank(ts_delta(vec_avg(eps_down_cnt), 22), industry)",
        "group_rank(ts_delta(vec_avg(eps_new_cnt), 22), industry)",

        # 目标价机制
        "group_rank(divide(vec_avg(target_prc_med), close), industry)",
        "group_rank(divide(vec_avg(target_prc_max), close), industry)",

        # 事件门控机制
        "trade_when(eps_estimate_4wk_change > 0, rank(eps_estimate_4wk_change), 0)",
        "trade_when(volume > adv20, rank(momentum), 0)",

        # 动量机制
        "ts_delta(ts_backfill(F, 66), 22)",
        "rank(ts_delta(field, 5))",

        # 均值回归机制
        "reverse(ts_rank(field, 5))",
        "multiply(sign(ts_delta(volume, 1)), reverse(ts_delta(close, 1)))",

        # 量价背离机制
        "reverse(ts_corr(rank(close), rank(volume), 10))",
        "ts_corr(rank(price), rank(volume), 5)",

        # 波动率溢价机制
        "divide(rank(signal), add(ts_std_dev(signal, 22), 0.1))",
        "multiply(reverse(rank(ts_std_dev(close, 20))), ts_corr(high, volume, 5))",

        # 流动性溢价机制
        "rank(divide(abs(returns), volume))",
        "reverse(rank(volume/adv20))",

        # 多期限共识机制
        "add(add(multiply(rank(F_40d), 0.33), multiply(rank(F_60d), 0.34)), multiply(rank(F_100d), 0.33))",

        # 置信度加权机制
        "multiply(rank(prob_high), rank(confidence))",

        # 截尾抑制机制
        "winsorize(rank(ceiling_field), std=2)",

        # 低频回填机制
        "ts_backfill(monthly_field, 63)",
    ]

    print(f"\n【候选池】{len(candidates)} 条表达式")
    print("覆盖 10 种经济学机制")

    # 阶段 1：S2 选波（多维标签）
    print("\n" + "=" * 70)
    print("阶段 1：S2 选波（多维标签确保机制多样性）")
    print("=" * 70)

    tags_list = batch_extract_tags(candidates)
    summary = summarize_tags(tags_list)

    print(f"\n机制覆盖：{len(summary['mechanism'])} 种")
    for mech, count in sorted(summary['mechanism'].items(), key=lambda x: -x[1]):
        print(f"  {mech}: {count} 条")

    # 模拟选波：每个机制选 1-2 条
    selected = []
    mechanism_count = {}
    for i, tags in enumerate(tags_list):
        mech = tags['mechanism']
        if mechanism_count.get(mech, 0) < 2:  # 每个机制最多 2 条
            selected.append(candidates[i])
            mechanism_count[mech] = mechanism_count.get(mech, 0) + 1

    print(f"\n选波结果：{len(selected)} 条（每个机制最多 2 条）")

    # 阶段 2：S3 预检（机制-形状匹配）
    print("\n" + "=" * 70)
    print("阶段 2：S3 预检（机制-形状匹配校验）")
    print("=" * 70)

    # 模拟字段画像
    field_profiles = {
        'eps_up_cnt': {'shape': 'spread', 'data_type': 'VECTOR'},
        'eps_down_cnt': {'shape': 'spread', 'data_type': 'VECTOR'},
        'eps_new_cnt': {'shape': 'spread', 'data_type': 'VECTOR'},
        'target_prc_med': {'shape': 'zero_inflated', 'data_type': 'VECTOR'},
        'target_prc_max': {'shape': 'zero_inflated', 'data_type': 'VECTOR'},
        'eps_estimate_4wk_change': {'shape': 'spread', 'data_type': 'MATRIX'},
        'volume': {'shape': 'spread', 'data_type': 'MATRIX'},
        'momentum': {'shape': 'spread', 'data_type': 'MATRIX'},
        'F': {'shape': 'spread', 'data_type': 'MATRIX'},
        'field': {'shape': 'spread', 'data_type': 'MATRIX'},
        'close': {'shape': 'spread', 'data_type': 'MATRIX'},
        'price': {'shape': 'spread', 'data_type': 'MATRIX'},
        'signal': {'shape': 'spread', 'data_type': 'MATRIX'},
        'high': {'shape': 'spread', 'data_type': 'MATRIX'},
        'returns': {'shape': 'spread', 'data_type': 'MATRIX'},
        'adv20': {'shape': 'spread', 'data_type': 'MATRIX'},
        'F_40d': {'shape': 'spread', 'data_type': 'MATRIX'},
        'F_60d': {'shape': 'spread', 'data_type': 'MATRIX'},
        'F_100d': {'shape': 'spread', 'data_type': 'MATRIX'},
        'prob_high': {'shape': 'spread', 'data_type': 'MATRIX'},
        'confidence': {'shape': 'spread', 'data_type': 'MATRIX'},
        'ceiling_field': {'shape': 'ceiling', 'data_type': 'MATRIX'},
        'monthly_field': {'shape': 'spread', 'data_type': 'MATRIX', 'freq': 'monthly'},
    }

    selected_tags = batch_extract_tags(selected, field_profiles)

    pass_count = sum(1 for t in selected_tags if t['field_match']['status'] == 'pass')
    warn_count = sum(1 for t in selected_tags if t['field_match']['status'] == 'warn')

    print(f"\n字段匹配校验：")
    print(f"  pass: {pass_count} 条")
    print(f"  warn: {warn_count} 条")
    print(f"  unknown: {len(selected_tags) - pass_count - warn_count} 条")

    # 阶段 3：S4 评审（按机制族分析表现）
    print("\n" + "=" * 70)
    print("阶段 3：S4 评审（按机制族分析表现）")
    print("=" * 70)

    # 模拟回测结果
    backtest_results = {
        'analyst_revision': {'sharpe': 1.35, 'fitness': 0.95, 'count': 3},
        'target_price': {'sharpe': 1.42, 'fitness': 1.10, 'count': 2},
        'event_gated': {'sharpe': 0.85, 'fitness': 0.65, 'count': 2},
        'momentum': {'sharpe': 1.15, 'fitness': 0.88, 'count': 2},
        'mean_reversion': {'sharpe': 0.95, 'fitness': 0.72, 'count': 2},
        'volume_price': {'sharpe': 1.28, 'fitness': 0.92, 'count': 2},
        'volatility_premium': {'sharpe': 1.05, 'fitness': 0.78, 'count': 2},
        'liquidity_premium': {'sharpe': 1.18, 'fitness': 0.85, 'count': 2},
        'multi_horizon': {'sharpe': 1.52, 'fitness': 1.15, 'count': 1},
        'confidence_weighted': {'sharpe': 1.38, 'fitness': 1.02, 'count': 1},
        'ceiling_suppress': {'sharpe': 0.92, 'fitness': 0.68, 'count': 1},
        'low_freq_backfill': {'sharpe': 1.08, 'fitness': 0.75, 'count': 1},
    }

    print(f"\n回测结果（按机制族）：")
    print(f"{'机制':<20} {'Sharpe':>8} {'Fitness':>8} {'数量':>4} {'信号苗头':>8}")
    print("-" * 60)

    promising_mechanisms = []
    for mech, result in sorted(backtest_results.items(), key=lambda x: -x[1]['sharpe']):
        sharpe = result['sharpe']
        fitness = result['fitness']
        count = result['count']

        # 信号苗头判定：sharpe >= 1.0 且 fitness >= 0.8
        is_promising = sharpe >= 1.0 and fitness >= 0.8
        marker = "✓" if is_promising else ""

        print(f"{mech:<20} {sharpe:>8.2f} {fitness:>8.2f} {count:>4} {marker:>8}")

        if is_promising:
            promising_mechanisms.append(mech)

    # 阶段 4：Mode B 优化（按机制族定向优化）
    print("\n" + "=" * 70)
    print("阶段 4：Mode B 优化（按机制族定向优化）")
    print("=" * 70)

    print(f"\n发现 {len(promising_mechanisms)} 个信号苗头机制：")
    for mech in promising_mechanisms:
        print(f"  - {mech}")

    print(f"\n优化策略：")
    print(f"  1. 对 {len(promising_mechanisms)} 个信号苗头机制进行 Mode B 优化")
    print(f"  2. 优先优化 sharpe >= 1.25 且 fitness >= 0.8 的机制")
    print(f"  3. 避免同族调权重，换字段组合/换概念")

    # 层层推进总结
    print("\n" + "=" * 70)
    print("层层推进策略总结")
    print("=" * 70)

    print(f"""
优势：
  1. S2 选波：多维标签确保机制多样性，避免同族堆叠
  2. S3 预检：机制-形状匹配校验，前置拦截机制不匹配
  3. S4 评审：按机制族分析表现，识别哪类机制有效
  4. Mode B 优化：按机制族定向优化，避免盲目调参

信号苗头发现：
  - 候选池 {len(candidates)} 条 → 选波 {len(selected)} 条
  - 发现 {len(promising_mechanisms)} 个信号苗头机制
  - 信号苗头发现率：{len(promising_mechanisms) / len(backtest_results) * 100:.0f}%

下一步：
  1. 对信号苗头机制进行 Mode B 优化
  2. 扩大候选池，验证更多机制
  3. 回测验证，积累实证证据
""")


if __name__ == '__main__':
    demo_layered_mining()
