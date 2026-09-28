# -*- coding: utf-8 -*-
"""cluster 变体生成器守卫（2026-09-19，依据帖 43562853669655）。

锁定三件事：
  1. **配方形状**符合文章的 cluster 建房式（`rank(group_mean(x, cap, industry))`），
     且**绝不使用**文章点名的反例算子（`group_rank`/`group_zscore`/`group_scale`
     = 行业内选股；`group_neutralize` = 反 cluster）；
  2. **JPN 被拒**（闸2b：JPN 不支持 industry/sector/subindustry，平台 Invalid data field
     会整批连坐 —— 这是硬约束，不是偏好）；
  3. 产出的 settings **强制 neutralization=MARKET**（文章 §3.4：行业中性化按构造
     删除行业结构 → 用 INDUSTRY/SUBINDUSTRY 跑 cluster 线是自毁）。
"""
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))

import build_cluster_variants as B  # noqa: E402


# --------------------------------------------------------------------------- 1
def test_recipes_follow_cluster_construction():
    """核心形态：group_mean 聚合 + 市场级 rank 打分。"""
    cross = B.PER_SOURCE_RECIPES["cross"]
    assert cross == "rank(group_mean({sig}, cap, industry))"
    # equal：等权行业（M&G 1999：效应 0.43→0.81%/月）
    assert "group_normalize" in B.PER_SOURCE_RECIPES["equal"]
    assert B.PER_SOURCE_RECIPES["equal"].startswith("rank(")
    # guard：防薄行业
    assert "group_count" in B.PER_SOURCE_RECIPES["guard"]
    # timing：区域级轮动 × 择时
    assert "ts_delta(close, 126)" in B.REGION_RECIPES["timing"]
    assert "ts_mean(group_mean(returns, cap, industry), 22) > 0" in B.REGION_RECIPES["timing"]


@pytest.mark.parametrize("bad", ["group_rank", "group_zscore", "group_scale", "group_neutralize"])
def test_no_anti_cluster_operators_in_recipes(bad):
    """文章 §3.3 明确：这些算子是"行业内选股"或"反 cluster"，cluster 线里不得出现。"""
    all_recipes = list(B.PER_SOURCE_RECIPES.values()) + list(B.REGION_RECIPES.values())
    for r in all_recipes:
        assert bad not in r, f"配方里出现反 cluster/组内算子: {bad} → {r}"


def test_region_level_recipe_needs_no_source():
    """timing 是区域级配方（不依赖源信号）——避免逐源复制造成无意义重复。"""
    assert set(B.REGION_RECIPES) == {"timing"}
    assert "{sig}" not in B.REGION_RECIPES["timing"]


# --------------------------------------------------------------------------- 2
def test_jpn_is_refused(monkeypatch, tmp_path):
    """JPN 在闸2b 名单内（不支持 industry/sector/subindustry）→ 必须硬拒绝。"""
    assert "JPN" in B.BLOCKED_GROUP_REGIONS
    monkeypatch.setattr(sys, "argv", [
        "build_cluster_variants.py", "--region", "JPN",
        "--out", str(tmp_path / "o.json"),
        "--settings-json", str(tmp_path / "s.json"),
    ])
    with pytest.raises(SystemExit) as e:
        B.main()
    assert "闸2b" in str(e.value) or "Invalid data field" in str(e.value)


def test_low_bar_regions_match_article():
    """文章：KOR/JPS/TWN/HKG/IND/GBR/DEU 门槛 1.0（= 优先做 cluster 线的区域）。"""
    for r in ("IND", "DEU", "GBR", "KOR", "HKG", "JPS", "TWN"):
        assert r in B.LOW_BAR_REGIONS


# --------------------------------------------------------------------------- 3
def test_settings_force_market_neutralization(monkeypatch, tmp_path):
    """产出 settings 必须把 neutralization 覆盖为 MARKET（保留区域原值供对照）。"""
    out = tmp_path / "v.json"
    st = tmp_path / "s.json"
    monkeypatch.setattr(sys, "argv", [
        "build_cluster_variants.py", "--region", "IND", "--limit", "0",
        "--recipes", "timing", "--out", str(out), "--settings-json", str(st),
    ])
    B.main()
    cfg = json.loads(st.read_text(encoding="utf-8"))
    assert cfg["neutralization"] == "MARKET"
    assert "MARKET" in cfg["_note"]
    # 其余区域设置应继承（至少 universe/delay 保留）
    orig = json.loads((REPO and open(
        os.path.join(REPO, "tracking", "IND", "config", "settings.json"),
        encoding="utf-8").read()))
    assert cfg.get("universe") == orig.get("universe")
    assert cfg.get("delay") == orig.get("delay")
    assert out.exists()
