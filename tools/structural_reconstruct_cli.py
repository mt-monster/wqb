#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""structural_reconstruct_cli.py - 结构重构命令行工具.

提供命令行接口，用于：
  1. 检测表达式结构性冲突
  2. 生成结构重构变体
  3. 记录变体回测结果
  4. 生成对比报告

用法:
    # 检测冲突
    python structural_reconstruct_cli.py detect --expr "add(rank(A), rank(B))"

    # 生成变体
    python structural_reconstruct_cli.py generate \
        --base "rank(anl45_est_revision)" \
        --conflict "rank(ts_delta(close, 5))" \
        --region DEU

    # 记录结果
    python structural_reconstruct_cli.py record \
        --region DEU --wave 95 \
        --variant-id geo_spread_rank \
        --original "add(rank(A), rank(B))" \
        --variant "subtract(rank(A), rank(B))" \
        --strategy geometric \
        --alpha-id abc123 \
        --sharpe 1.45 --fitness 0.92

    # 生成报告
    python structural_reconstruct_cli.py report --region DEU --wave 95
"""

import argparse
import json
import os
import sys

# 确保 src 在 path 中
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC_PATH = os.path.join(_REPO_ROOT, "src")
if _SRC_PATH not in sys.path:
    sys.path.insert(0, _SRC_PATH)

from wqb.workflow.structural_variants import (
    ReconstructionStrategy,
    StructuralVariantGenerator,
    detect_structural_conflict,
    generate_reconstruction_report,
)
from wqb.workflow.structural_variant_tracker import StructuralVariantTracker


def cmd_detect(args):
    """检测结构性冲突."""
    conflict = detect_structural_conflict(args.expr)

    if conflict:
        print("[WARN] 检测到结构性冲突模式")
        print(f"  模式类型: {conflict['pattern']}")
        print(f"  基础信号: {conflict['base'][:60]}...")
        print(f"  冲突信号: {conflict['conflict'][:60]}...")
        print()
        print("建议: 使用 generate 子命令生成结构重构变体")
        return 1
    else:
        print("[OK] 未检测到结构性冲突模式")
        return 0


def cmd_generate(args):
    """生成结构重构变体."""
    strategy = None
    if args.strategy:
        try:
            strategy = ReconstructionStrategy(args.strategy)
        except ValueError:
            print(f"错误: 未知策略 '{args.strategy}'")
            print(f"支持: {[s.value for s in ReconstructionStrategy]}")
            return 1

    generator = StructuralVariantGenerator()
    result = generator.generate(
        base_signal=args.base,
        conflict_signal=args.conflict,
        strategy=strategy,
        region=args.region,
    )

    # 打印摘要
    print(f"基础信号: {args.base}")
    print(f"冲突信号: {args.conflict}")
    print(f"生成 {len(result.variants)} 个变体")
    print()

    if result.recommended:
        print("=" * 60)
        print("推荐变体 (P{})".format(result.recommended.priority))
        print("=" * 60)
        print(f"策略: {result.recommended.strategy.value}")
        print(f"表达式: {result.recommended.expression}")
        print(f"描述: {result.recommended.description}")
        print(f"预期: {result.recommended.expected_effect}")
        print(f"风险: {result.recommended.risk_note}")
        print()

    # 打印全部变体
    print("=" * 60)
    print("全部变体")
    print("=" * 60)
    for i, v in enumerate(result.variants, 1):
        print(f"\n[{i}] P{v.priority} | {v.strategy.value}")
        print(f"    {v.expression}")
        print(f"    {v.description}")

    # 保存报告
    if args.output:
        report = generate_reconstruction_report(result)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n报告已保存: {args.output}")

    # 输出 JSON（用于管道）
    if args.json:
        output = {
            "base_expression": result.base_expression,
            "variants": [
                {
                    "strategy": v.strategy.value,
                    "expression": v.expression,
                    "priority": v.priority,
                }
                for v in result.variants
            ],
            "recommended": result.recommended.expression if result.recommended else None,
        }
        print(f"\nJSON: {json.dumps(output, ensure_ascii=False)}")

    return 0


def cmd_record(args):
    """记录变体回测结果."""
    db_path = args.db or os.environ.get("WQB_DB_PATH")
    if not db_path:
        # 默认路径
        db_path = os.path.join(_REPO_ROOT, "data", "wqb.db")

    tracker = StructuralVariantTracker(db_path=db_path)

    metrics = {}
    if args.sharpe is not None:
        metrics["sharpe"] = args.sharpe
    if args.fitness is not None:
        metrics["fitness"] = args.fitness
    if args.turnover is not None:
        metrics["turnover"] = args.turnover
    if args.two_year is not None:
        metrics["two_year_sharpe"] = args.two_year

    result = tracker.record_variant_result(
        region=args.region,
        wave=args.wave,
        variant_id=args.variant_id,
        original_expr=args.original,
        variant_expr=args.variant,
        strategy=args.strategy,
        alpha_id=args.alpha_id,
        metrics=metrics,
        status=args.status or ("complete" if metrics else "pending"),
    )

    print(f"[OK] 已记录: {result}")
    return 0


def cmd_report(args):
    """生成对比报告."""
    db_path = args.db or os.environ.get("WQB_DB_PATH")
    if not db_path:
        db_path = os.path.join(_REPO_ROOT, "data", "wqb.db")

    tracker = StructuralVariantTracker(db_path=db_path)
    report = tracker.generate_comparison_report(args.region, args.wave)

    print(report)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n报告已保存: {args.output}")

    return 0


def cmd_stats(args):
    """获取策略统计."""
    db_path = args.db or os.environ.get("WQB_DB_PATH")
    if not db_path:
        db_path = os.path.join(_REPO_ROOT, "data", "wqb.db")

    tracker = StructuralVariantTracker(db_path=db_path)
    stats = tracker.get_strategy_stats(region=args.region)

    print("策略统计")
    print("=" * 60)
    for strategy, s in sorted(stats.items()):
        print(f"\n{strategy}:")
        print(f"  样本数: {s['count']}")
        if s.get('avg_sharpe'):
            print(f"  平均 Sharpe: {s['avg_sharpe']:.2f}")
        if s.get('avg_fitness'):
            print(f"  平均 Fitness: {s['avg_fitness']:.2f}")

    return 0


def main():
    ap = argparse.ArgumentParser(
        description="结构重构命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--db", help="数据库路径（默认: data/wqb.db 或 WQB_DB_PATH）")

    sub = ap.add_subparsers(dest="cmd", required=True)

    # detect
    p_detect = sub.add_parser("detect", help="检测结构性冲突")
    p_detect.add_argument("--expr", required=True, help="待检测表达式")

    # generate
    p_gen = sub.add_parser("generate", help="生成结构重构变体")
    p_gen.add_argument("--base", required=True, help="基础信号表达式")
    p_gen.add_argument("--conflict", required=True, help="冲突信号表达式")
    p_gen.add_argument("--strategy", help="重构策略过滤")
    p_gen.add_argument("--region", help="区域代码")
    p_gen.add_argument("--output", "-o", help="输出报告文件")
    p_gen.add_argument("--json", action="store_true", help="输出 JSON")

    # record
    p_rec = sub.add_parser("record", help="记录变体回测结果")
    p_rec.add_argument("--region", required=True, help="区域代码")
    p_rec.add_argument("--wave", type=int, required=True, help="波次号")
    p_rec.add_argument("--variant-id", required=True, help="变体唯一标识")
    p_rec.add_argument("--original", required=True, help="原始表达式")
    p_rec.add_argument("--variant", required=True, help="变体表达式")
    p_rec.add_argument("--strategy", required=True, help="重构策略")
    p_rec.add_argument("--alpha-id", help="平台 alpha id")
    p_rec.add_argument("--sharpe", type=float, help="Sharpe 比率")
    p_rec.add_argument("--fitness", type=float, help="Fitness")
    p_rec.add_argument("--turnover", type=float, help="Turnover")
    p_rec.add_argument("--two-year", type=float, help="2Y Sharpe")
    p_rec.add_argument("--status", help="状态（默认: complete 如果有指标）")

    # report
    p_rep = sub.add_parser("report", help="生成对比报告")
    p_rep.add_argument("--region", required=True, help="区域代码")
    p_rep.add_argument("--wave", type=int, required=True, help="波次号")
    p_rep.add_argument("--output", "-o", help="输出报告文件")

    # stats
    p_stats = sub.add_parser("stats", help="获取策略统计")
    p_stats.add_argument("--region", help="区域代码（可选）")

    args = ap.parse_args()

    if args.cmd == "detect":
        return cmd_detect(args)
    elif args.cmd == "generate":
        return cmd_generate(args)
    elif args.cmd == "record":
        return cmd_record(args)
    elif args.cmd == "report":
        return cmd_report(args)
    elif args.cmd == "stats":
        return cmd_stats(args)
    else:
        ap.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
