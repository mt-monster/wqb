# -*- coding: utf-8 -*-
"""test_structural_reconstruct.py - 结构重构功能测试."""

import os
import sys
import tempfile
import unittest

# 确保 src 在 path 中
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from src.wqb.workflow.structural_variants import (
    ReconstructionStrategy,
    StructuralVariantGenerator,
    detect_structural_conflict,
    generate_reconstruction_report,
)
from src.wqb.workflow.structural_variant_tracker import (
    StructuralVariantTracker,
    VariantMetrics,
)


class TestStructuralVariants(unittest.TestCase):
    """结构重构变体生成器测试."""

    def setUp(self):
        self.generator = StructuralVariantGenerator()
        self.base = "rank(anl45_est_revision)"
        self.conflict = "rank(ts_delta(close, 5))"

    def test_generate_all_strategies(self):
        """测试生成所有策略的变体."""
        result = self.generator.generate(
            base_signal=self.base,
            conflict_signal=self.conflict,
        )

        self.assertGreater(len(result.variants), 0)
        self.assertIsNotNone(result.recommended)
        self.assertIsNotNone(result.rationale)

        # 验证所有策略都有变体
        strategies = {v.strategy for v in result.variants}
        self.assertIn(ReconstructionStrategy.GEOMETRIC, strategies)
        self.assertIn(ReconstructionStrategy.NEUTRALIZATION, strategies)
        self.assertIn(ReconstructionStrategy.TEMPORAL, strategies)

    def test_generate_geometric_only(self):
        """测试只生成几何重构变体."""
        result = self.generator.generate(
            base_signal=self.base,
            conflict_signal=self.conflict,
            strategy=ReconstructionStrategy.GEOMETRIC,
        )

        for v in result.variants:
            self.assertEqual(v.strategy, ReconstructionStrategy.GEOMETRIC)
            # 验证不包含独立的 add(A,B) 混信号模式（divide 中的 add 是分母保护，允许）
            expr_lower = v.expression.lower()
            # 检查是否是独立的 add(信号A, 信号B) 模式
            import re
            # 匹配 add( 后面直接跟信号，而不是在 divide 内部作为分母保护
            independent_add = re.search(r'add\s*\(\s*[^,]*rank|add\s*\(\s*rank', expr_lower)
            if independent_add and 'divide' not in expr_lower:
                self.fail(f"表达式包含独立 add 混信号模式: {v.expression}")

    def test_geometric_templates_compliance(self):
        """测试几何重构模板的合规性（禁止 add(A,B)）."""
        result = self.generator.generate(
            base_signal=self.base,
            conflict_signal=self.conflict,
            strategy=ReconstructionStrategy.GEOMETRIC,
        )

        for v in result.variants:
            # 验证使用 subtract/divide 而非 add
            expr_lower = v.expression.lower()
            self.assertTrue(
                "subtract(" in expr_lower or "divide(" in expr_lower,
                f"表达式应使用 subtract/divide: {v.expression}"
            )

    def test_region_specific_recommendation(self):
        """测试区域特定推荐."""
        result = self.generator.generate(
            base_signal=self.base,
            conflict_signal=self.conflict,
            region="DEU",
        )

        # DEU 应该优先推荐 country 中性化或几何重构
        self.assertIsNotNone(result.recommended)
        self.assertIn(result.recommended.priority, [1, 2])


class TestDetectStructuralConflict(unittest.TestCase):
    """结构性冲突检测测试."""

    def test_detect_simple_add(self):
        """检测简单 add(A,B)."""
        expr = "add(rank(close), rank(volume))"
        result = detect_structural_conflict(expr)

        self.assertIsNotNone(result)
        self.assertEqual(result["pattern"], "simple_add")

    def test_detect_weighted_add_func(self):
        """检测函数式加权 add."""
        expr = "add(multiply(0.6, rank(revision)), multiply(0.4, rank(reversal)))"
        result = detect_structural_conflict(expr)

        self.assertIsNotNone(result)
        self.assertEqual(result["pattern"], "weighted_add_func")

    def test_detect_weighted_add_infix(self):
        """检测中缀式加权."""
        expr = "0.6 * rank(revision) + 0.4 * rank(reversal)"
        result = detect_structural_conflict(expr)

        self.assertIsNotNone(result)
        self.assertEqual(result["pattern"], "weighted_add_infix")

    def test_no_conflict_subtract(self):
        """subtract 不构成冲突."""
        expr = "subtract(rank(A), rank(B))"
        result = detect_structural_conflict(expr)

        self.assertIsNone(result)

    def test_no_conflict_single(self):
        """单信号不构成冲突."""
        expr = "rank(ts_delta(close, 5))"
        result = detect_structural_conflict(expr)

        self.assertIsNone(result)


class TestStructuralVariantTracker(unittest.TestCase):
    """结构重构效果追踪器测试."""

    def setUp(self):
        # 使用临时数据库
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.tracker = StructuralVariantTracker(db_path=self.temp_db.name)

    def tearDown(self):
        os.unlink(self.temp_db.name)

    def test_record_and_retrieve(self):
        """测试记录和检索变体结果."""
        self.tracker.record_variant_result(
            region="DEU",
            wave=95,
            variant_id="geo_spread",
            original_expr="add(rank(A), rank(B))",
            variant_expr="subtract(rank(A), rank(B))",
            strategy="geometric",
            alpha_id="test123",
            metrics={"sharpe": 1.45, "fitness": 0.92},
            status="complete",
        )

        variants = self.tracker.get_wave_variants("DEU", 95)
        self.assertEqual(len(variants), 1)
        self.assertEqual(variants[0].variant_id, "geo_spread")
        self.assertEqual(variants[0].metrics.sharpe, 1.45)

    def test_compare_with_original(self):
        """测试对比分析."""
        # 记录多个变体
        self.tracker.record_variant_result(
            region="DEU", wave=95, variant_id="v1",
            original_expr="add(A,B)", variant_expr="subtract(A,B)",
            strategy="geometric", alpha_id="a1",
            metrics={"sharpe": 1.5, "fitness": 0.9},
            status="complete",
        )
        self.tracker.record_variant_result(
            region="DEU", wave=95, variant_id="v2",
            original_expr="add(A,B)", variant_expr="divide(A,B)",
            strategy="geometric", alpha_id="a2",
            metrics={"sharpe": 1.3, "fitness": 0.85},
            status="complete",
        )

        comparison = self.tracker.compare_with_original(
            region="DEU", wave=95,
            original_metrics={"sharpe": 1.2, "fitness": 0.8},
        )

        self.assertEqual(comparison.verdict, "IMPROVED")
        self.assertIsNotNone(comparison.best_variant)
        self.assertEqual(comparison.best_variant.variant_id, "v1")
        self.assertGreater(comparison.improvement.get("sharpe", 0), 0)

    def test_strategy_stats(self):
        """测试策略统计."""
        self.tracker.record_variant_result(
            region="DEU", wave=95, variant_id="v1",
            original_expr="add(A,B)", variant_expr="subtract(A,B)",
            strategy="geometric", alpha_id="a1",
            metrics={"sharpe": 1.5, "fitness": 0.9},
            status="complete",
        )
        self.tracker.record_variant_result(
            region="DEU", wave=96, variant_id="v2",
            original_expr="add(A,B)", variant_expr="divide(A,B)",
            strategy="geometric", alpha_id="a2",
            metrics={"sharpe": 1.3, "fitness": 0.85},
            status="complete",
        )

        stats = self.tracker.get_strategy_stats()
        self.assertIn("geometric", stats)
        self.assertEqual(stats["geometric"]["count"], 2)
        self.assertAlmostEqual(stats["geometric"]["avg_sharpe"], 1.4)


class TestReportGeneration(unittest.TestCase):
    """报告生成测试."""

    def test_generate_reconstruction_report(self):
        """测试重构报告生成."""
        generator = StructuralVariantGenerator()
        result = generator.generate(
            base_signal="rank(A)",
            conflict_signal="rank(B)",
        )

        report = generate_reconstruction_report(result)

        self.assertIn("# 结构重构变体报告", report)
        self.assertIn("原始表达式", report)
        self.assertIn("推荐", report)


if __name__ == "__main__":
    unittest.main()
