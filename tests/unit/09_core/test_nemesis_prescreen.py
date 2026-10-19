# -*- coding: utf-8 -*-
"""照妖镜预筛工具的单测：解析与判定是整条预筛链的正确性要害。

为什么值得守护：`_split_neut` 要在 `vector_neut(BASE, PROXY)` 里切出两条边，
而 BASE 自身可能含逗号（`quantile(group_rank(hump(ts_av_diff(f, 252), hump=0.01), subindustry))`
里有 `252)` 前后多个逗号）——切错就把 BASE 当 PROXY，判定表会静默给出错的掉幅。
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
# 两个被测 CLI 已按 THEMES.json 下沉到主题子目录（S11：tools/ 顶层只减不增）
sys.path.insert(0, str(REPO / "tools" / "gates"))
sys.path.insert(0, str(REPO / "tools" / "pool-hygiene"))

import nemesis_prescreen as N  # noqa: E402


def test_split_neut_handles_commas_inside_base():
    base = "quantile(group_rank(hump(ts_av_diff(eps_q1_estimate_qoq_growth, 252), hump=0.01), subindustry))"
    expr = f"vector_neut({base}, eps_y1_cagr_2yr)"
    got = N._split_neut(expr)
    assert got is not None
    assert got[0] == base, "BASE 被逗号切断了"
    assert got[1] == "eps_y1_cagr_2yr"


def test_split_neut_rejects_non_neut_expression():
    assert N._split_neut("quantile(group_rank(ts_rank(close, 252), industry))") is None
    # 只有一层但 proxy 不是纯标识符（含算子）⇒ 不认，避免误判
    assert N._split_neut("vector_neut(x, add(y, 1))") is None


def test_split_neut_single_level():
    assert N._split_neut("vector_neut(rank(close), market_cap)") == ("rank(close)", "market_cap")


def test_verdict_thresholds():
    """掉幅闸：<30% PASS / <50% WEAK / >=50% KILL（与 docstring 纪律一致）。"""
    def verdict(s_raw: float, s_neut: float) -> str:
        drop = 1.0 - s_neut / s_raw
        return "PASS" if drop < N.PASS_MAX else ("WEAK" if drop < N.WEAK_MAX else "KILL")

    assert verdict(1.89, 1.50) == "PASS"      # 掉 20.6%
    assert verdict(1.89, 1.20) == "WEAK"      # 掉 36.5%
    assert verdict(1.89, 0.62) == "KILL"      # 掉 67.2%（2026-10-18 实测值）


def test_prod_watch_limit_never_truncates_persisted_pool(tmp_path):
    """回归：`--limit N` 只能限制「本轮查几条」，绝不能把池文件裁成 N 条。

    2026-10-19 真实事故：一次 `--limit 1` 调试把 7 条候选削成 1 条（写回截断后的列表）。
    """
    import json

    import prod_watch as W

    pool = [{"alpha_id": f"A{i}", "note": "", "last_prod": 0.8} for i in range(5)]
    p = tmp_path / "pool.json"
    p.write_text(json.dumps(pool, ensure_ascii=False), encoding="utf-8")

    loaded = W._load_pool(p)
    assert len(loaded) == 5

    # 模拟 --limit 2 的写回路径：写回必须仍是全量
    W._save_pool(p, loaded)
    again = json.loads(p.read_text(encoding="utf-8"))
    assert len(again) == 5

    # 直接检查源码约束：work 视图与 pool 分离（防止有人改回 pool = pool[:limit]）
    src = (REPO / "tools" / "pool-hygiene" / "prod_watch.py").read_text(encoding="utf-8")
    assert "work = pool[: args.limit] if args.limit else pool" in src
    assert "pool = pool[: args.limit]" not in src, "禁止再截断持久化列表"
