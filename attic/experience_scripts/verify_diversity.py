#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单的多样性系统验证脚本"""

import sys
import os
from pathlib import Path

# 设置输出编码
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加路径
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent.parent
src_path = project_root / 'src'

# 添加到Python路径
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 直接导入模块
sys.path.insert(0, str(src_path / 'wqb' / 'expression'))
import diversity_enhancer as de

print("[TEST] Diversity Enhancement System Verification")
print("=" * 60)

# 1. 测试算子配额管理器
print("\n[1] Testing Operator Quota Manager")
manager = de.OperatorQuotaManager()
test_expr = "rank(ts_mean(group_rank(close, sector), 20))"
categories = manager.analyze_expression(test_expr)
print(f"   表达式: {test_expr}")
print(f"   类别分布: {categories}")
suggestions = manager.suggest_next_operators(count=5)
print(f"   建议算子: {suggestions}")

# 2. 测试结构变异引擎
print("\n[2] Testing Structural Mutation Engine")
engine = de.StructuralMutationEngine()
test_expr = "group_rank(ts_rank(close, 60), sector)"
structure = engine.parse_expression_structure(test_expr)
print(f"   原始表达式: {test_expr}")
print(f"   骨架类型: {structure['skeleton_type']}")
mutated = engine.mutate_expression(test_expr, 'change_window')
print(f"   变异后: {mutated}")

# 3. 测试多样性监控器
print("\n[3] Testing Diversity Monitor")
monitor = de.DiversityMonitor()
test_expressions = [
    "rank(ts_mean(close, 20))",
    "group_rank(ts_rank(volume, 60), sector)",
    "ts_zscore(vec_avg(returns), 120)",
    "trade_when(volume > 1000, rank(close))",
    "add(ts_delta(close, 5), ts_delta(volume, 5))"
]
metrics = monitor.calculate_metrics(test_expressions)
print(f"   算子熵: {metrics.operator_entropy:.3f}")
print(f"   覆盖率: {metrics.coverage_rate:.2%}")
print(f"   新颖度: {metrics.novelty_score:.2%}")
print(f"   骨架分布: {metrics.skeleton_distribution}")

# 4. 测试多样性增强器
print("\n[4] Testing Diversity Enhancer")
enhancer = de.DiversityEnhancer()
original = [
    "rank(ts_mean(close, 20))",
    "rank(ts_mean(close, 40))",
    "rank(ts_mean(close, 60))"
]
print(f"   原始表达式数: {len(original)}")
enhanced = enhancer.enhance_diversity(original, target_count=6)
print(f"   增强后表达式数: {len(enhanced)}")
print("   增强后的表达式:")
for i, expr in enumerate(enhanced[:3], 1):
    print(f"     {i}. {expr}")

# 5. 测试多样性报告
print("\n[5] Diversity Report")
report = enhancer.get_diversity_report()
if 'current_metrics' in report:
    metrics = report['current_metrics']
    print(f"   算子熵: {metrics['operator_entropy']:.3f}")
    print(f"   覆盖率: {metrics['coverage_rate']:.2%}")
    print(f"   新颖度: {metrics['novelty_score']:.2%}")
if 'recommendations' in report and report['recommendations']:
    print("   改进建议:")
    for rec in report['recommendations']:
        print(f"     • {rec}")

print("\n" + "=" * 60)
print("[SUCCESS] Diversity Enhancement System Verification Complete!")
print("=" * 60)

# 演示如何使用
print("\n[USAGE] Quick Start Examples:")
print("   1. Generate diverse expressions:")
print("      python quick_start_diversity.py generate --count 30")
print("   2. Analyze existing file:")
print("      python quick_start_diversity.py analyze batch.json")
print("   3. Enhance expressions:")
print("      python quick_start_diversity.py enhance input.json -o output.json")
print("   4. Run monitoring:")
print("      python quick_start_diversity.py monitor")
