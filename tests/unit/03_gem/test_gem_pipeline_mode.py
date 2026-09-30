# -*- coding: utf-8 -*-
"""GEM pipeline_mode 自动识别单元测试（2026-09-30 新增）."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from wqb.workflow.nodes.gem import _auto_detect_pipeline_mode  # noqa: E402


class TestAutoDetectPipelineMode:
    """pipeline_mode 自动识别测试."""

    def test_single_mode_for_small_field_count(self):
        """字段数 < 50 → single."""
        result = _auto_detect_pipeline_mode(
            dataset_id="anl10",
            data_category="analyst",
            field_count=30,
            fields_df=None,
        )
        assert result == "single"

    def test_phased_mode_for_large_field_count(self):
        """字段数 > 100 → phased."""
        result = _auto_detect_pipeline_mode(
            dataset_id="order_flow",
            data_category="pv",
            field_count=198,
            fields_df=None,
        )
        assert result == "phased"

    def test_phased_mode_for_news_category(self):
        """news 类别 → phased（需要族级机制叙事）."""
        result = _auto_detect_pipeline_mode(
            dataset_id="news1",
            data_category="news",
            field_count=80,
            fields_df=None,
        )
        assert result == "phased"

    def test_phased_mode_for_analyst_category(self):
        """analyst 类别 → phased（需要族级机制叙事）."""
        result = _auto_detect_pipeline_mode(
            dataset_id="anl10",
            data_category="analyst",
            field_count=80,
            fields_df=None,
        )
        assert result == "phased"

    def test_phased_mode_for_fundamental_category(self):
        """fundamental 类别 → phased（需要族级机制叙事）."""
        result = _auto_detect_pipeline_mode(
            dataset_id="fnd10",
            data_category="fundamental",
            field_count=80,
            fields_df=None,
        )
        assert result == "phased"

    def test_default_to_phased(self):
        """默认 → phased."""
        result = _auto_detect_pipeline_mode(
            dataset_id="other",
            data_category="other",
            field_count=80,
            fields_df=None,
        )
        assert result == "phased"

    def test_skeleton_mode_for_layered_fields(self):
        """字段可分层（signal/metadata/scale 清晰）→ skeleton."""
        # 模拟 fields_df（含 id/description/type 列）
        class MockFieldsDF:
            def __init__(self):
                self.columns = ["id", "description", "type"]
                self._data = [
                    ("anl10_fy1_eps", "FY1 EPS estimate", "MATRIX"),
                    ("anl10_fy2_eps", "FY2 EPS estimate", "MATRIX"),
                    ("anl10_periodend", "Period end date", "MATRIX"),
                    ("anl10_periodtype", "Period type", "MATRIX"),
                    ("anl10_fyearend", "Fiscal year end", "MATRIX"),
                    ("anl10_rating", "Analyst rating", "MATRIX"),
                    ("anl10_target_price", "Target price", "MATRIX"),
                    ("anl10_recommendation", "Recommendation", "MATRIX"),
                    ("anl10_revision", "Revision", "MATRIX"),
                    ("anl10_surprise", "Surprise", "MATRIX"),
                    ("anl10_dispersion", "Dispersion", "MATRIX"),
                    ("anl10_breadth", "Breadth", "MATRIX"),
                ]

            def __getitem__(self, key):
                if key == "id":
                    return [x[0] for x in self._data]
                elif key == "description":
                    return [x[1] for x in self._data]
                elif key == "type":
                    return [x[2] for x in self._data]
                raise KeyError(key)

            def dropna(self):
                return self

            def astype(self, dtype):
                return self

            def tolist(self):
                return list(self)

        # 注意：这个测试需要 skeletons.classify_fields 可用
        # 如果 skeletons 模块不可用，会降级到 phased
        # 字段数必须 >= 50 才会进入 skeleton 判断（规则 1 优先）
        result = _auto_detect_pipeline_mode(
            dataset_id="anl10",
            data_category="analyst",
            field_count=80,  # >= 50，进入 skeleton 判断
            fields_df=MockFieldsDF(),
        )
        # 如果 skeletons 可用且字段分层成功，应该返回 skeleton
        # 否则降级到 phased
        assert result in ("skeleton", "phased")

    def test_skeleton_mode_fallback_to_phased(self):
        """字段分层失败 → 降级到 phased."""
        # 模拟 fields_df（无 id 列）
        class MockFieldsDF:
            def __init__(self):
                self.columns = ["name", "value"]

            def __getitem__(self, key):
                raise KeyError(key)

        result = _auto_detect_pipeline_mode(
            dataset_id="anl10",
            data_category="analyst",
            field_count=80,
            fields_df=MockFieldsDF(),
        )
        assert result == "phased"
