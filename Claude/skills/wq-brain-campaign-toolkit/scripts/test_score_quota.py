# -*- coding: utf-8 -*-
"""S0 pyramid quota + category-weight cap (EUR Wave35–40 复盘)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_datasets import apply_pyramid_quota, category_weight


def test_pyramid_quota_promotes_non_model():
    rows = [
        {"id": "m1", "category": "model", "tier": "tier1", "score": 1.2,
         "hard_excluded": False, "dead": False},
        {"id": "m2", "category": "model", "tier": "tier1", "score": 1.1,
         "hard_excluded": False, "dead": False},
        {"id": "pv1", "category": "pv", "tier": "tier2", "score": 0.65,
         "hard_excluded": False, "dead": False},
        {"id": "news1", "category": "news", "tier": "excluded", "score": 0.64,
         "hard_excluded": False, "dead": False},
        {"id": "dead_pv", "category": "pv", "tier": "tier2", "score": 0.9,
         "hard_excluded": False, "dead": True},
    ]
    n = apply_pyramid_quota(rows, {"pyramid_quota_non_model_min": 2})
    assert n == 2
    assert rows[2]["tier"] == "tier1"
    assert rows[2]["tier_note"] == "pyramid_quota"
    assert rows[3]["tier"] == "tier1"
    assert rows[4]["tier"] == "tier2"  # dead skipped


def test_pyramid_quota_default_on():
    rows = [
        {"id": "m1", "category": "model", "tier": "tier1", "score": 1.0,
         "hard_excluded": False, "dead": False},
        {"id": "pv1", "category": "pv", "tier": "tier2", "score": 0.5,
         "hard_excluded": False, "dead": False},
        {"id": "n1", "category": "news", "tier": "tier2", "score": 0.4,
         "hard_excluded": False, "dead": False},
    ]
    assert apply_pyramid_quota(rows, {}) == 2


def test_category_weight_clamped_even_if_config_says_13():
    h = {"category_weight_enable": True, "category_weights": {"model": 1.3, "pv": 0.7}}
    assert category_weight({"category": "model"}, h) == 1.15
    assert category_weight({"category": "pv"}, h) == 0.9
