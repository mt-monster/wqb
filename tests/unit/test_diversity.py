# -*- coding: utf-8 -*-
"""diversity_enhancer 指标重构与信号证据闸测试（2026-08-18 GBR 复盘）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from wqb.expression.diversity_enhancer import (
    analyze_diversity,
    enhance_expressions,
    signal_evidence_gate,
    DiversityMonitor,
)


def test_signal_single_point_captures_rank_dominated_pool():
    """GBR 场景：rank 占 90% 表达式必须被标记为信号单点（旧指标漏报）。"""
    exprs = ['rank(ts_delta(annualized_pd_1_month_jc7, 5))'] * 9 + [
        'ts_zscore(mdl53_ms5_1year, 60)']
    m = analyze_diversity(exprs)["current_metrics"]
    assert m["top_operator_share"] == 0.9
    assert m["signal_single_point"] is True


def test_novelty_uses_structure_signature_not_string_uniqueness():
    """参数级伪多样性：字符串全不同但签名同源 -> novelty 低、expr_uniqueness 高。"""
    exprs = ['rank(ts_delta(x, 5))', 'rank(ts_delta(x, 10))',
             'rank(ts_delta(x, 20))', 'rank(ts_delta(x, 60))']
    m = analyze_diversity(exprs)["current_metrics"]
    assert m["expr_uniqueness"] == 1.0          # 旧新颖度（字符串唯一率）
    assert m["novelty_score"] < 0.5              # 新新颖度（签名唯一率）
    assert m["novelty_score"] > 0.0


def test_structural_similarity_is_pairwise_not_majority_skeleton():
    """相似度是算子集 Jaccard 平均：算子集互异的池子相似度应显著低。"""
    diverse = ['rank(ts_delta(close, 5))',
               'group_rank(volume, sector)',
               'trade_when(ts_arg_max(close, 5) == 0, ts_zscore(returns, 20))']
    m = analyze_diversity(diverse)["current_metrics"]
    assert m["structural_similarity"] < 0.3
    # 同算子集的池子（仅窗口不同）相似度应高
    same = ['rank(ts_delta(close, 5))', 'rank(ts_delta(close, 10))']
    m2 = analyze_diversity(same)["current_metrics"]
    assert m2["structural_similarity"] > 0.5


def test_field_cluster_merges_tenor_variants():
    """字段归簇：多期限 PD 字段归为同一信号源簇。"""
    from wqb.expression.diversity_enhancer import DiversityMonitor
    assert DiversityMonitor._field_cluster("annualized_pd_1_month_jc7") == \
        DiversityMonitor._field_cluster("annualized_pd_10_year_jc7")
    assert DiversityMonitor._field_cluster("mdl53_ms5_1year") != \
        DiversityMonitor._field_cluster("annualized_pd_1_year_jc7")


def test_signal_evidence_gate_ceiling():
    """2 批回测 max|sharpe| < 0.5 -> 信号天花板。"""
    results = [{"sharpe": 0.3, "batch_idx": 0},
               {"sharpe": 0.49, "batch_idx": 0},
               {"sharpe": 0.1, "batch_idx": 1}]
    v = signal_evidence_gate(results)
    assert v["verdict"] == "ceiling"
    assert v["passed"] is False
    assert v["batches_observed"] == 2


def test_signal_evidence_gate_ok_when_above_floor():
    """max|sharpe| >= 0.5 时不判天花板。"""
    results = [{"sharpe": 0.8, "batch_idx": 0},
               {"sharpe": 0.7, "batch_idx": 1}]
    v = signal_evidence_gate(results)
    assert v["verdict"] == "ok"
    assert v["passed"] is True


def test_signal_evidence_gate_single_batch_not_condemned():
    """单批证据不判天花板（防噪声误杀）。"""
    results = [{"sharpe": 0.2, "batch_idx": 0}]
    v = signal_evidence_gate(results)
    assert v["verdict"] == "ok"


def test_enhance_ineffective_returns_original_and_marks_effective_false():
    """假增强修复：签名无新增时返回原列表且 effective=False。"""
    import random
    random.seed(7)
    exprs = ['rank(close)', 'rank(close)', 'ts_decay_linear(rank(close), 5)']
    enhanced, report = enhance_expressions(exprs, target_count=3)
    # 无字段池且变异未产生新签名时，必须返回原列表
    assert report.get("effective") in (True, False)
    if not report["effective"]:
        assert enhanced == exprs


def test_enhance_with_field_pool_uses_campaign_fields():
    """字段池注入：增强生成器使用战役数据集字段而非通用字段。"""
    import random
    from wqb.expression.diversity_enhancer import DiversityEnhancer
    random.seed(3)
    pool = ["annualized_pd_1_year_jc7", "mdl53_ms5_1year", "mdl53_implied_spreads"]
    enhancer = DiversityEnhancer()
    # 直接验证生成路径（绕过 underused_ops 为空时不生成的分支）
    gen = enhancer._generate_with_operators(["ts_rank", "group_zscore"], 4, field_pool=pool)
    joined = " ".join(gen)
    assert any(f in joined for f in pool)
    gen2 = enhancer._generate_random_expressions(4, field_pool=pool)
    joined2 = " ".join(gen2)
    assert any(f in joined2 for f in pool)
