# -*- coding: utf-8 -*-
"""`wqb.profiles.evidence` 的数据集归类口径：复合（跨集组合）名必须能解析到成员集。

背景（2026-11-19 审计 + 实测）：`alphas.dataset_id` / `backtest_results.dataset` 里存在
**跨集组合**形态（`fundamental1+pv1` 367 行、`analyst_factor_signals+pv1` 215 行…；全库
1875 行 join 不到单集）。它们**不是**"未解析占位"，而是 AGENTS.md §7.7 合法跨集形态的归属。
不拆开 ⇒ 旧实现走「前缀猜类别」把这些行错归进 "other"，污染区域证据的分类统计。
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from wqb.profiles import evidence  # noqa: E402


TABLE = {"pv1": "PV", "fundamental1": "FUNDAMENTAL", "sentiment27": "SENTIMENT"}


def test_dataset_members_splits_composite_names():
    assert evidence._dataset_members("fundamental1+pv1") == ["fundamental1", "pv1"]
    assert evidence._dataset_members("pv1+sentiment27") == ["pv1", "sentiment27"]
    assert evidence._dataset_members("") == []
    assert evidence._dataset_members(None) == []


def test_composite_name_resolves_to_member_category():
    """复合名应落到**成员集**的类别，而不是前缀猜测出来的 other。"""
    assert evidence._cat_of_dataset("fundamental1+pv1", TABLE) == "FUNDAMENTAL"
    assert evidence._cat_of_dataset("pv1+sentiment27", TABLE) == "PV"
    # 成员顺序不同但都能解析 ⇒ 取第一个可解析成员
    assert evidence._cat_of_dataset("sentiment27+pv1", TABLE) == "SENTIMENT"


def test_plain_name_unchanged():
    assert evidence._cat_of_dataset("pv1", TABLE) == "PV"
    assert evidence._cat_of_dataset("", TABLE) == "unknown"
    assert evidence._cat_of_dataset("?", TABLE) == "unknown"


def test_unresolvable_composite_falls_back_to_prefix_rule():
    """成员都解析不出时，仍走既有的前缀猜测（不回归旧行为）。"""
    out = evidence._cat_of_dataset("someunknownset+otherunknownset", TABLE)
    assert isinstance(out, str) and out
