# -*- coding: utf-8 -*-
"""回归测试：骨架签名与生成期同族去重（2026-09-17 #5）。

## 背景（实测）
| 组 | 条数 | 唯一骨架 | 复用率 | ≥8 条大簇覆盖 |
|---|---|---|---|---|
| 8月 `source=gem` | 1,663 | 121 | 13.7 | 89.2% |
| **近 3 天** | **8,317** | **661** | **12.6** | **89.2%** |

即 89.2% 的产出落在"同一骨架 ≥8 条"的大簇里 —— 同骨架换字段的**兄弟变体**。
这类变体在平台 SELF 相关 0.9+（`alphas.self_correlation` 最高实测 0.9445），会自相残杀。

本模块锁定：签名口径正确（字段折叠、元数保留）、去重上限生效、配额与既有
`gate.py` 的 5 分类族级 `skeleton_quota` **互补而非重复**。
"""

import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "src"))

from wqb.expression.skeleton import (  # noqa: E402
    DEFAULT_MAX_PER_SKELETON,
    dedup_by_skeleton,
    skeleton_distribution,
    structural_signature,
)


# ---- 签名口径 -------------------------------------------------------------

def test_fields_collapse_to_placeholder():
    """同骨架换字段必须折叠为同一签名（这是识别兄弟变体的前提）。"""
    a = structural_signature("rank(ts_backfill(close, 66))")
    b = structural_signature("rank(ts_backfill(open, 66))")
    assert a == b
    assert "F" in a and "close" not in a and "open" not in a


def test_numbers_collapse_to_N():
    assert structural_signature("ts_mean(f, 66)") == structural_signature("ts_mean(f, 22)")
    assert "N" in structural_signature("ts_mean(f, 66)")


def test_arity_is_preserved():
    """元数不同 = 结构不同，不得折叠（否则会误删真正不同的形态）。"""
    assert structural_signature("divide(a, b)") != structural_signature("divide(a, b, c)")


def test_operator_detected_by_trailing_paren_not_whitelist():
    """算子判定靠"后是否紧跟 `(`"，不依赖任何算子目录 —— 不会随目录漂移而失准。"""
    sig = structural_signature("my_unlisted_op(ts_backfill(x, 5))")
    assert "my_unlisted_op" in sig and "ts_backfill" in sig


def test_punctuation_kept_so_structure_is_visible():
    assert "," in structural_signature("ts_corr(a, b, 20)")
    assert "(" in structural_signature("rank(a)")


def test_empty_and_garbage_are_safe():
    assert structural_signature("") == ""
    assert structural_signature(None or "") == ""
    # 不抛异常即可
    structural_signature("(((,,,")
    assert structural_signature("rank(close)") != ""


# ---- 去重 -----------------------------------------------------------------

def _items(sigs):
    return [{"expression": s} for s in sigs]


def test_dedup_caps_per_skeleton():
    items = _items([f"rank(ts_backfill(f{i}, 66))" for i in range(10)])
    kept, dropped = dedup_by_skeleton(items, max_per_skeleton=3, max_share=None)
    assert len(kept) == 3 and len(dropped) == 7


def test_dedup_keeps_input_order_deterministically():
    """保留先出现的（GEM 输出已按概念优先级排序，不引入额外假设）。"""
    items = _items([f"rank(f{i})" for i in range(5)])
    kept, _ = dedup_by_skeleton(items, max_per_skeleton=2, max_share=None)
    assert [k["expression"] for k in kept] == ["rank(f0)", "rank(f1)"]


def test_dedup_keeps_distinct_skeletons():
    items = _items(["rank(a)", "ts_corr(a,b,20)", "divide(a,b)", "group_rank(a,sector)"])
    kept, dropped = dedup_by_skeleton(items, max_per_skeleton=3, max_share=None)
    assert len(kept) == 4 and not dropped


def test_share_cap_is_the_stricter_bound():
    """max_share 与 max_per_skeleton 同时施加，取更严者（10 条 × 25% = 2）。"""
    items = _items([f"rank(f{i})" for i in range(10)])
    kept, _ = dedup_by_skeleton(items, max_per_skeleton=99, max_share=0.25)
    assert len(kept) == 2


def test_defaults_are_sane():
    assert DEFAULT_MAX_PER_SKELETON >= 1
    items = _items([f"rank(f{i})" for i in range(100)])
    kept, _ = dedup_by_skeleton(items)
    assert 1 <= len(kept) <= 100


def test_signature_sink_records_every_input():
    items = _items(["rank(a)", "rank(b)", "ts_corr(a,b,20)"])
    sink = []
    dedup_by_skeleton(items, max_per_skeleton=1, max_share=None, signature_sink=sink)
    assert len(sink) == 3
    assert sum(1 for r in sink if r["kept"]) == 2
    assert all("signature" in r and "index" in r for r in sink)


def test_empty_input():
    kept, dropped = dedup_by_skeleton([])
    assert kept == [] and dropped == []


# ---- 分布统计 -------------------------------------------------------------

def test_distribution_flags_degenerate_batch():
    """10 条同骨架 → 复用率 10、最大簇 100% —— 应当被一眼看出。"""
    st = skeleton_distribution(_items([f"rank(f{i})" for i in range(10)]))
    assert st["n"] == 10 and st["unique"] == 1
    assert st["reuse_rate"] == pytest.approx(10.0)
    assert st["top_share"] == pytest.approx(1.0)
    assert st["big_cluster_share"] == pytest.approx(1.0)


def test_distribution_empty():
    st = skeleton_distribution([])
    assert st["n"] == 0 and st["unique"] == 0


# ---- 与既有族级配额互补 ---------------------------------------------------

def test_dedup_is_finer_grained_than_family_quota():
    """既有 skeleton_quota 是 5 分类**族级**；本模块是**结构签名级**。

    实测近 3 天 Top3 骨架（ts_corr / subtract(rank,rank) / divide）分属不同族，
    族级配额**已满足**，但结构级复用仍极端 —— 故本模块是补空白而非重复。
    """
    toolkit = os.path.join(
        REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts", "_lib", "common.py"
    )
    src = open(toolkit, encoding="utf-8").read()
    # 族级实现只做 5 分类
    for fam in ("event_gated", "group", "ratio", "linear_mix", "single"):
        assert fam in src, f"族级 skeleton 缺分类 {fam}"
    # 而结构签名会把同族的两个不同骨架区分开（族级做不到）
    a = structural_signature("divide(rank(a), rank(b))")
    b = structural_signature("divide(subtract(a,b), add(abs(a),abs(b)))")
    assert a != b
