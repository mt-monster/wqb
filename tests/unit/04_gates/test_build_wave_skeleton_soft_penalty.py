# -*- coding: utf-8 -*-
"""build_wave 的跨波死骨架软降权（只重排、不删除，2026-11-15 P2）。"""
from wqb.knowledge.select import dead_skeletons, deprioritize_dead_skeletons


def _exprs():
    return [
        "rank(ts_backfill(close, 66))",   # 死骨架
        "ts_corr(rank(open), rank(volume), 20)",  # 活
        "rank(ts_backfill(high, 66))",    # 死骨架
        "divide(rank(low), rank(vwap))",  # 活
    ]


def _stats(n=5, dead=True):
    return [{
        "skeleton": "rank ( ts_backfill ( F , N ) )",
        "n": n, "max_sharpe": 0.5, "dominant_wall": "CW",
        "dominant_wall_share": 0.9, "dead": dead,
    }]


def test_dead_skeletons_are_moved_to_tail_never_dropped():
    picked = _exprs()
    out, moved = deprioritize_dead_skeletons(picked, _stats())
    assert len(out) == len(picked)
    assert set(out) == set(picked)
    assert out[:2] == picked[1::2]       # 活表达式保持原相对顺序
    assert moved == set(picked[0::2])
    assert all(e in moved for e in out[2:])


def test_min_n_threshold_keeps_short_history_untouched():
    picked = _exprs()
    out, moved = deprioritize_dead_skeletons(picked, _stats(n=4))
    assert out == picked and moved == set()


def test_non_dead_or_empty_stats_is_noop():
    picked = _exprs()
    out, moved = deprioritize_dead_skeletons(picked, _stats(dead=False))
    assert out == picked and moved == set()
    out, moved = deprioritize_dead_skeletons(picked, None)
    assert out == picked and moved == set()


def test_dead_skeletons_ignores_unknown():
    assert dead_skeletons([{"skeleton": "_unknown", "n": 10, "dead": True}]) == set()
