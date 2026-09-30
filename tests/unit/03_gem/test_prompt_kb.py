# -*- coding: utf-8 -*-
"""提示词知识库（prompt_kb）单元测试（2026-09-30 新增）."""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT / "Claude" / "skills" / "brain-make-some-gem" / "scripts" / "trailSomeAlphas"))

import prompt_kb  # noqa: E402


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """临时数据库 fixture."""
    db_path = tmp_path / "test_prompt_kb.db"
    monkeypatch.setattr(prompt_kb, "DB_PATH", db_path)
    prompt_kb.init_prompt_kb_tables()
    yield db_path


class TestPromptKbTables:
    """提示词知识库表结构测试."""

    def test_init_tables(self, temp_db):
        """测试表结构初始化."""
        conn = sqlite3.connect(str(temp_db))
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [r[0] for r in c.fetchall()]
        conn.close()
        assert "prompt_templates" in tables
        assert "prompt_performance" in tables
        assert "prompt_ab_tests" in tables


class TestPromptTemplateCrud:
    """提示词模板 CRUD 测试."""

    def test_create_and_get_template(self, temp_db):
        """测试创建与获取模板."""
        template_id = prompt_kb.create_prompt_template(
            category="news",
            content="test content",
            metadata={"author": "test"},
        )
        assert template_id > 0

        template = prompt_kb.get_prompt_template("news", version=1)
        assert template is not None
        assert template["category"] == "news"
        assert template["version"] == 1
        assert template["content"] == "test content"
        assert template["metadata"]["author"] == "test"

    def test_get_latest_active_template(self, temp_db):
        """测试获取最新激活模板."""
        # 创建两个版本
        prompt_kb.create_prompt_template("news", "v1 content")
        prompt_kb.create_prompt_template("news", "v2 content")

        # 获取最新激活版本（应该是 v2）
        template = prompt_kb.get_prompt_template("news", active_only=True)
        assert template is not None
        assert template["version"] == 2
        assert template["content"] == "v2 content"

    def test_list_templates(self, temp_db):
        """测试列出模板."""
        prompt_kb.create_prompt_template("news", "news v1")
        prompt_kb.create_prompt_template("analyst", "analyst v1")

        templates = prompt_kb.list_prompt_templates()
        assert len(templates) == 2

        news_templates = prompt_kb.list_prompt_templates(category="news")
        assert len(news_templates) == 1
        assert news_templates[0]["category"] == "news"

    def test_deactivate_template(self, temp_db):
        """测试停用模板."""
        template_id = prompt_kb.create_prompt_template("news", "test content")
        success = prompt_kb.deactivate_prompt_template(template_id)
        assert success

        # 停用后应该获取不到（active_only=True）
        template = prompt_kb.get_prompt_template("news", active_only=True)
        assert template is None

        # 但应该能获取到（active_only=False）
        template = prompt_kb.get_prompt_template("news", active_only=False)
        assert template is not None
        assert template["is_active"] == 0


class TestPromptPerformance:
    """提示词性能记录测试."""

    def test_record_and_get_performance(self, temp_db):
        """测试记录与获取性能."""
        template_id = prompt_kb.create_prompt_template("news", "test content")

        record_id = prompt_kb.record_prompt_performance(
            template_id=template_id,
            region="KOR",
            dataset_id="news1",
            wave="w1",
            backtest_count=100,
            pass_count=50,
            avg_sharpe=1.5,
            best_sharpe=2.0,
        )
        assert record_id > 0

        records = prompt_kb.get_prompt_performance(template_id, region="KOR")
        assert len(records) == 1
        assert records[0]["pass_rate"] == 0.5
        assert records[0]["avg_sharpe"] == 1.5
        assert records[0]["best_sharpe"] == 2.0


class TestAbTest:
    """A/B 测试."""

    def test_create_and_complete_ab_test(self, temp_db):
        """测试创建与完成 A/B 测试."""
        template_a_id = prompt_kb.create_prompt_template("news", "content A")
        template_b_id = prompt_kb.create_prompt_template("news", "content B")

        test_id = "test-uuid-123"
        test_db_id = prompt_kb.create_ab_test(
            test_id=test_id,
            category="news",
            template_a_id=template_a_id,
            template_b_id=template_b_id,
            region="KOR",
            dataset_id="news1",
        )
        assert test_db_id > 0

        # 完成测试（A 获胜）
        success = prompt_kb.complete_ab_test(
            test_id=test_id,
            winner_id=template_a_id,
            confidence=0.95,
            metrics={"a_pass_rate": 0.6, "b_pass_rate": 0.4},
        )
        assert success

        # 获取测试结果
        test = prompt_kb.get_ab_test(test_id)
        assert test is not None
        assert test["status"] == "completed"
        assert test["winner_id"] == template_a_id
        assert test["confidence"] == 0.95
        assert test["metrics"]["a_pass_rate"] == 0.6


class TestPromptOptimization:
    """提示词自动优化测试."""

    def test_analyze_prompt_performance(self, temp_db):
        """测试分析提示词性能."""
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
        assert result["avg_sharpe"] == 1.8
        assert len(result["recommendations"]) > 0

    def test_optimize_prompt_template(self, temp_db):
        """测试自动优化提示词模板."""
        # 创建初始模板
        template_id = prompt_kb.create_prompt_template("news", "original content")

        # 自动优化
        new_template_id = prompt_kb.optimize_prompt_template(
            category="news",
            optimization_reason="基于历史回测结果加强高过闸率机制",
            performance_data={"avg_pass_rate": 0.6},
        )
        assert new_template_id is not None
        assert new_template_id != template_id

        # 新模板应该是 v2
        new_template = prompt_kb.get_prompt_template("news", version=2)
        assert new_template is not None
        assert new_template["metadata"]["optimization_reason"] == "基于历史回测结果加强高过闸率机制"
        assert new_template["metadata"]["parent_version"] == 1
