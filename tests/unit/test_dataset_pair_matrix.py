# -*- coding: utf-8 -*-
"""数据集对矩阵分析单元测试（2026-10-01 新增）."""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from wqb.dataset_pair_matrix import (  # noqa: E402
    _extract_dataset_from_expression,
    _extract_dataset_pairs,
    analyze_dataset_pair_matrix,
    get_dataset_pair_recommendations,
)


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """临时数据库 fixture."""
    db_path = tmp_path / "test_dataset_pair_matrix.db"
    monkeypatch.setattr("wqb.dataset_pair_matrix.DB_PATH", db_path)
    
    # 创建测试表
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute("""
        CREATE TABLE backtest_results (
            id INTEGER PRIMARY KEY,
            region TEXT,
            code TEXT,
            sharpe REAL,
            fitness REAL
        )
    """)
    conn.commit()
    conn.close()
    
    yield db_path


class TestExtractDataset:
    """数据集提取测试."""

    def test_extract_dataset_from_expression(self):
        """测试从表达式中提取数据集 ID."""
        assert _extract_dataset_from_expression("rank(anl4_capex_flag)") == "anl4"
        assert _extract_dataset_from_expression("rank(fnd6_assets)") == "fnd6"
        assert _extract_dataset_from_expression("rank(pv1_close)") == "pv1"
        assert _extract_dataset_from_expression("rank(model10_score)") == "model10"
        assert _extract_dataset_from_expression("rank(news1_sentiment)") == "news1"
        assert _extract_dataset_from_expression("rank(unknown_field)") is None

    def test_extract_dataset_pairs(self):
        """测试从表达式中提取数据集对."""
        # 单数据集
        pairs = _extract_dataset_pairs("rank(anl4_capex_flag)")
        assert pairs == []
        
        # 跨数据集
        pairs = _extract_dataset_pairs("rank(anl4_capex_flag) - rank(fnd6_assets)")
        assert ("anl4", "fnd6") in pairs or ("fnd6", "anl4") in pairs
        
        # 多数据集
        pairs = _extract_dataset_pairs("rank(anl4_capex_flag) - rank(fnd6_assets) + rank(pv1_close)")
        assert len(pairs) == 3  # anl4-fnd6, anl4-pv1, fnd6-pv1


class TestDatasetPairMatrix:
    """数据集对矩阵分析测试."""

    def test_analyze_empty_matrix(self, temp_db):
        """测试空矩阵（无历史提交）."""
        result = analyze_dataset_pair_matrix("TEST")
        assert result["total_datasets"] == 0
        assert result["total_pairs"] == 0
        assert result["filled_pairs"] == 0
        assert result["empty_pairs"] == 0
        assert result["recommendations"] == []

    def test_analyze_matrix_with_data(self, temp_db):
        """测试有数据的矩阵."""
        # 插入测试数据
        conn = sqlite3.connect(str(temp_db))
        c = conn.cursor()
        c.execute("""
            INSERT INTO backtest_results (region, code, sharpe, fitness)
            VALUES (?, ?, ?, ?)
        """, ("TEST", "rank(anl4_capex_flag) - rank(fnd6_assets)", 1.5, 1.0))
        c.execute("""
            INSERT INTO backtest_results (region, code, sharpe, fitness)
            VALUES (?, ?, ?, ?)
        """, ("TEST", "rank(anl4_revision_flag) - rank(pv1_close)", 1.2, 0.9))
        conn.commit()
        conn.close()
        
        result = analyze_dataset_pair_matrix("TEST")
        assert result["total_datasets"] == 3  # anl4, fnd6, pv1
        assert result["filled_pairs"] == 2  # anl4-fnd6, anl4-pv1
        assert result["empty_pairs"] == 1  # fnd6-pv1
        assert len(result["recommendations"]) == 1
        assert result["recommendations"][0]["dataset_a"] in ("fnd6", "pv1")
        assert result["recommendations"][0]["dataset_b"] in ("fnd6", "pv1")

    def test_get_recommendations(self, temp_db):
        """测试获取推荐."""
        # 插入测试数据（需要至少 3 个数据集才能生成推荐）
        conn = sqlite3.connect(str(temp_db))
        c = conn.cursor()
        c.execute("""
            INSERT INTO backtest_results (region, code, sharpe, fitness)
            VALUES (?, ?, ?, ?)
        """, ("TEST", "rank(anl4_capex_flag) - rank(fnd6_assets)", 1.5, 1.0))
        c.execute("""
            INSERT INTO backtest_results (region, code, sharpe, fitness)
            VALUES (?, ?, ?, ?)
        """, ("TEST", "rank(anl4_revision_flag) - rank(pv1_close)", 1.2, 0.9))
        c.execute("""
            INSERT INTO backtest_results (region, code, sharpe, fitness)
            VALUES (?, ?, ?, ?)
        """, ("TEST", "rank(fnd6_assets) - rank(model10_score)", 1.3, 1.1))
        conn.commit()
        conn.close()
        
        recommendations = get_dataset_pair_recommendations("TEST", top_n=10)
        assert len(recommendations) > 0
        
        # 测试优先级过滤
        high_priority = get_dataset_pair_recommendations("TEST", top_n=10, priority="high")
        assert all(r["priority"] == "high" for r in high_priority)
