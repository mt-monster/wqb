# -*- coding: utf-8 -*-
"""提示词知识库集成单元测试（2026-09-30 新增）."""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT / "Claude" / "skills" / "brain-make-some-gem" / "scripts" / "trailSomeAlphas"))
sys.path.insert(0, str(ROOT / "src"))

import prompt_kb  # noqa: E402
from economic_priors import category_forbidden_text, concept_first_rules  # noqa: E402


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """临时数据库 fixture."""
    db_path = tmp_path / "test_prompt_kb_integration.db"
    monkeypatch.setattr(prompt_kb, "DB_PATH", db_path)
    prompt_kb.init_prompt_kb_tables()
    yield db_path


class TestCategoryForbiddenIntegration:
    """类别定制禁止事项集成测试."""

    def test_category_forbidden_text_news(self):
        """测试 news 类别的禁止事项."""
        text = category_forbidden_text("news")
        assert "CATEGORY-SPECIFIC FORBIDDEN" in text
        assert "ts_entropy" in text
        assert "ts_skewness" in text

    def test_category_forbidden_text_pv(self):
        """测试 pv 类别的禁止事项."""
        text = category_forbidden_text("pv")
        assert "CATEGORY-SPECIFIC FORBIDDEN" in text
        assert "加权混合" in text

    def test_category_forbidden_text_other(self):
        """测试 other 类别（无禁止事项）."""
        text = category_forbidden_text("other")
        assert text == ""

    def test_concept_first_rules_with_category(self):
        """测试 concept_first_rules 传递 category 参数."""
        rules = concept_first_rules(data_profile=None, category="news", use_kb=False)
        assert "CATEGORY-SPECIFIC FORBIDDEN" in rules
        assert "ts_entropy" in rules

    def test_concept_first_rules_without_category(self):
        """测试 concept_first_rules 不传 category 参数."""
        rules = concept_first_rules(data_profile=None, category=None, use_kb=False)
        assert "CATEGORY-SPECIFIC FORBIDDEN" not in rules


class TestPromptKbIntegration:
    """提示词知识库集成测试."""

    def test_record_performance_integration(self, temp_db):
        """测试记录提示词性能集成."""
        # 创建模板
        template_id = prompt_kb.create_prompt_template(
            category="news",
            content="test content",
        )

        # 记录性能（模拟 gem.py::_collect_results() 的调用）
        record_id = prompt_kb.record_prompt_performance(
            template_id=template_id,
            region="KOR",
            dataset_id="news1",
            wave="s2_news1_d1",
            backtest_count=100,
            pass_count=60,
            avg_sharpe=1.8,
            best_sharpe=2.2,
            metrics={"fitness": 1.2, "turnover": 0.15, "coverage": 0.85},
        )
        assert record_id > 0

        # 验证性能记录
        records = prompt_kb.get_prompt_performance(template_id, region="KOR")
        assert len(records) == 1
        assert records[0]["pass_rate"] == 0.6
        assert records[0]["avg_sharpe"] == 1.8
        assert records[0]["best_sharpe"] == 2.2
        assert records[0]["metrics"]["fitness"] == 1.2

    def test_analyze_and_optimize_integration(self, temp_db):
        """测试分析与自动优化集成."""
        # 创建两个模板
        template_a_id = prompt_kb.create_prompt_template("news", "content A")
        template_b_id = prompt_kb.create_prompt_template("news", "content B")

        # 记录性能（A 表现好，B 表现差）
        prompt_kb.record_prompt_performance(
            template_a_id, "KOR", "news1", "w1", 100, 60, 1.8, 2.2,
        )
        prompt_kb.record_prompt_performance(
            template_b_id, "KOR", "news1", "w1", 100, 30, 1.0, 1.2,
        )

        # 分析性能
        result = prompt_kb.analyze_prompt_performance("news", region="KOR", min_backtest_count=50)
        assert "error" not in result
        assert result["best_template_id"] == template_a_id
        assert result["avg_pass_rate"] == 0.6

        # 自动优化（性能不佳时触发）
        if result["avg_pass_rate"] < 0.5:
            new_template_id = prompt_kb.optimize_prompt_template(
                category="news",
                optimization_reason="基于历史回测结果加强高过闸率机制",
                performance_data=result,
            )
            assert new_template_id is not None
            assert new_template_id != template_a_id

    def test_concept_first_rules_with_kb(self, temp_db):
        """测试 concept_first_rules 使用知识库."""
        # 创建模板
        template_id = prompt_kb.create_prompt_template(
            category="news",
            content="You design WorldQuant BRAIN Regular Alpha CONCEPTS from knowledge base...",
        )

        # 使用知识库加载
        rules = concept_first_rules(data_profile=None, category="news", use_kb=True)
        assert "from knowledge base" in rules

        # 不使用知识库（降级到内置默认提示词）
        rules = concept_first_rules(data_profile=None, category="news", use_kb=False)
        assert "from knowledge base" not in rules
        assert "You design WorldQuant BRAIN Regular Alpha CONCEPTS" in rules
