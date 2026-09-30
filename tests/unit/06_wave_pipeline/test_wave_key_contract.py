# -*- coding: utf-8 -*-
"""P0-3 回归测试：wave 键约定统一（字符串波号）。

背景（2026-09-07 审计）：tools/wave_gate.py 曾用 `--wave type=int`，
而 toolkit pipeline.py / gate.py 与 waves.wave_number 均为字符串。
后果：'s2_pattern_scores_d1' 这类字符串波号的波无法进门禁编排器，
gate_results 0 行 → S2→S3 断链，全库 6100 条表达式无声积压。

本测试锁定三件事：
1. 字符串波号（含 's2_xxx_d1' 形态）在 store 层全链路可写可读；
2. gate_results.wave 与 waves.wave_number 同型对齐（str）；
3. ensure_schema 的 wave-key-check 对"有表达式但无 gate 记录"的
   活跃波打 WARN（断链可见性）。
"""

import io
from contextlib import redirect_stdout

from wqb.store import CampaignStore


def test_string_wave_number_roundtrip(tmp_path):
    """字符串波号 s2_xxx_d1 全链路：expressions 写入 → list 读回 → gate 结果对齐。"""
    store = CampaignStore(str(tmp_path / "k.db"))
    try:
        wave = "s2_pattern_scores_d1"
        store.upsert_expressions(
            "USA", wave,
            ["rank(a)", "rank(b)"], dataset="pattern_scores", status="pending",
        )
        rows = store.list_expressions("USA", wave, dataset="pattern_scores")
        assert len(rows) == 2

        # gate 结果以同一字符串波号写入（upsert_gate_result 内部 str() 透传）
        store.upsert_gate_result(
            "USA", wave, "pattern_scores", {"all_pass": True, "total": 2},
        )
        got = store.get_gate_result("USA", wave, "pattern_scores")
        assert got["all_pass"] is True

        # int 形态波号同样透传为 str（历史兼容）
        store.upsert_gate_result("USA", 97, "model219", {"all_pass": False})
        got2 = store.get_gate_result("USA", "97", "model219")
        assert got2["all_pass"] is False
    finally:
        store.close()


def test_wave_key_check_warns_on_orphan(tmp_path):
    """wave-key-check：有表达式的 pending 波若无 gate_results 记录 → 启动时 WARN。"""
    db_path = str(tmp_path / "k2.db")
    store = CampaignStore(db_path)
    try:
        # 建一个"断链波"：表达式入库但从不写 gate_results
        store.upsert_expressions(
            "USA", "s2_never_gated_d1",
            ["rank(x)"], dataset="foo", status="pending",
        )
    finally:
        store.close()

    # 重新打开触发 ensure_schema → wave-key-check 应打 WARN
    buf = io.StringIO()
    store2 = CampaignStore(db_path)
    try:
        with redirect_stdout(buf):
            # ensure_schema 在 __init__ 已跑过；手动再触发一次校验路径
            # （ensure_schema 是幂等的，重复调用安全）
            store2.ensure_schema()
    finally:
        store2.close()
    out = buf.getvalue()
    assert "wave-key-check" in out, f"期望断链 WARN，实际输出: {out!r}"
    assert "s2_never_gated_d1" in out
    assert "USA" in out


def test_wave_key_check_silent_when_gated(tmp_path):
    """正常波（gate 记录齐全）不触发 WARN。"""
    db_path = str(tmp_path / "k3.db")
    store = CampaignStore(db_path)
    try:
        store.upsert_expressions(
            "USA", "s2_gated_ok_d1",
            ["rank(y)"], dataset="bar", status="pending",
        )
        store.upsert_gate_result(
            "USA", "s2_gated_ok_d1", "bar", {"all_pass": True},
        )
    finally:
        store.close()

    buf = io.StringIO()
    store2 = CampaignStore(db_path)
    try:
        with redirect_stdout(buf):
            store2.ensure_schema()
    finally:
        store2.close()
    out = buf.getvalue()
    assert "wave-key-check" not in out or "WARN" not in out, (
        f"不应触发 WARN，实际输出: {out!r}"
    )
