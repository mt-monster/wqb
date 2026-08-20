#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_diversity_system.py - 多样性增强系统集成测试

验证各个组件的功能和集成效果
"""

import json
import sys
import tempfile
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))
sys.path.insert(0, str(project_root / 'docs' / 'experience'))

from wqb.expression.diversity_enhancer import (
    DiversityEnhancer,
    OperatorQuotaManager,
    StructuralMutationEngine,
    DiversityMonitor,
    enhance_expressions,
    analyze_diversity
)


def test_operator_quota_manager():
    """测试算子配额管理器"""
    print("🧪 测试算子配额管理器...")
    
    manager = OperatorQuotaManager()
    
    # 测试表达式分析
    test_expr = "rank(ts_mean(group_rank(close, sector), 20))"
    categories = manager.analyze_expression(test_expr)
    print(f"   表达式: {test_expr}")
    print(f"   类别分布: {categories}")
    
    # 测试算子类别识别
    assert manager.get_operator_category('ts_mean') == 'ts_*'
    assert manager.get_operator_category('group_rank') == 'group_*'
    assert manager.get_operator_category('vec_avg') == 'vec_*'
    assert manager.get_operator_category('rank') == 'rank_*'
    assert manager.get_operator_category('add') == 'arithmetic'
    
    # 测试建议算子
    suggestions = manager.suggest_next_operators(count=5)
    print(f"   建议算子: {suggestions}")
    
    print("   ✅ 算子配额管理器测试通过\n")


def test_structural_mutation_engine():
    """测试结构变异引擎"""
    print("🧪 测试结构变异引擎...")
    
    engine = StructuralMutationEngine()
    
    # 测试表达式解析
    test_expr = "group_rank(ts_rank(close, 60), sector)"
    structure = engine.parse_expression_structure(test_expr)
    print(f"   表达式: {test_expr}")
    print(f"   骨架类型: {structure['skeleton_type']}")
    print(f"   深度: {structure['depth']}")
    print(f"   算子: {structure['operators']}")
    
    # 测试各种变异
    mutations = [
        ('swap_branches', "add(close, volume)"),
        ('change_window', "ts_mean(close, 20)"),
        ('insert_layer', "rank(close)"),
        ('add_condition', "ts_rank(volume, 60)"),
    ]
    
    for mutation_type, expr in mutations:
        mutated = engine.mutate_expression(expr, mutation_type)
        print(f"   {mutation_type}: {expr} → {mutated}")
    
    print("   ✅ 结构变异引擎测试通过\n")


def test_diversity_monitor():
    """测试多样性监控器"""
    print("🧪 测试多样性监控器...")
    
    monitor = DiversityMonitor()
    
    # 测试表达式集合
    test_expressions = [
        "rank(ts_mean(close, 20))",
        "group_rank(ts_rank(volume, 60), sector)",
        "ts_zscore(vec_avg(returns), 120)",
        "trade_when(volume > 1000, rank(close))",
        "add(ts_delta(close, 5), ts_delta(volume, 5))"
    ]
    
    metrics = monitor.calculate_metrics(test_expressions)
    print(f"   测试表达式数: {len(test_expressions)}")
    print(f"   算子熵: {metrics.operator_entropy:.3f}")
    print(f"   覆盖率: {metrics.coverage_rate:.2%}")
    print(f"   新颖度: {metrics.novelty_score:.2%}")
    print(f"   骨架分布: {metrics.skeleton_distribution}")
    
    # 获取报告
    report = monitor.get_diversity_report()
    if 'recommendations' in report:
        print(f"   建议: {report['recommendations']}")
    
    print("   ✅ 多样性监控器测试通过\n")


def test_diversity_enhancer():
    """测试多样性增强器"""
    print("🧪 测试多样性增强器...")
    
    enhancer = DiversityEnhancer()
    
    # 原始表达式（故意相似）
    original = [
        "rank(ts_mean(close, 20))",
        "rank(ts_mean(close, 40))",
        "rank(ts_mean(close, 60))",
        "rank(ts_mean(volume, 20))",
        "rank(ts_mean(volume, 40))"
    ]
    
    print(f"   原始表达式数: {len(original)}")
    
    # 分析原始多样性
    original_metrics = enhancer.monitor.calculate_metrics(original)
    print(f"   原始算子熵: {original_metrics.operator_entropy:.3f}")
    print(f"   原始覆盖率: {original_metrics.coverage_rate:.2%}")
    
    # 增强多样性
    enhanced = enhancer.enhance_diversity(original, target_count=10)
    
    print(f"   增强后表达式数: {len(enhanced)}")
    
    # 分析增强后多样性
    enhanced_metrics = enhancer.monitor.calculate_metrics(enhanced)
    print(f"   增强后算子熵: {enhanced_metrics.operator_entropy:.3f}")
    print(f"   增强后覆盖率: {enhanced_metrics.coverage_rate:.2%}")
    
    # 验证改进
    assert enhanced_metrics.operator_entropy > original_metrics.operator_entropy
    assert enhanced_metrics.coverage_rate >= original_metrics.coverage_rate
    
    print("   增强后的表达式示例:")
    for expr in enhanced[:3]:
        print(f"     • {expr}")
    
    print("   ✅ 多样性增强器测试通过\n")


def test_integration():
    """测试集成功能"""
    print("🧪 测试集成功能...")
    
    # 测试便捷函数
    test_expressions = [
        "rank(close)",
        "ts_mean(volume, 20)",
        "group_rank(returns, sector)"
    ]
    
    # 测试 analyze_diversity
    report = analyze_diversity(test_expressions)
    assert 'current_metrics' in report
    print(f"   analyze_diversity: 熵={report['current_metrics']['operator_entropy']:.3f}")
    
    # 测试 enhance_expressions
    enhanced, report = enhance_expressions(test_expressions, target_count=5)
    assert len(enhanced) >= len(test_expressions)
    print(f"   enhance_expressions: {len(test_expressions)} → {len(enhanced)}")
    
    print("   ✅ 集成功能测试通过\n")


def test_state_persistence():
    """测试状态持久化"""
    print("🧪 测试状态持久化...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        state_file = f.name
    
    try:
        # 创建增强器并处理一些表达式
        enhancer1 = DiversityEnhancer()
        enhancer1.enhance_diversity(["rank(close)", "ts_mean(volume, 20)"])
        
        # 保存状态
        enhancer1.save_state(state_file)
        print(f"   状态已保存到: {state_file}")
        
        # 创建新增强器并加载状态
        enhancer2 = DiversityEnhancer()
        enhancer2.load_state(state_file)
        
        # 验证状态已加载
        assert len(enhancer2.quota_manager.usage_history) > 0
        print(f"   加载的算子使用历史: {len(enhancer2.quota_manager.usage_history)} 个")
        
        print("   ✅ 状态持久化测试通过\n")
        
    finally:
        # 清理临时文件
        Path(state_file).unlink(missing_ok=True)


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🚀 多样性增强系统集成测试")
    print("=" * 60)
    print()
    
    try:
        test_operator_quota_manager()
        test_structural_mutation_engine()
        test_diversity_monitor()
        test_diversity_enhancer()
        test_integration()
        test_state_persistence()
        
        print("=" * 60)
        print("✅ 所有测试通过！系统运行正常")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
