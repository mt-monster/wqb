# -*- coding: utf-8 -*-
"""P0-3 停止闸输入完整性（2026-09-17）.

背景（实测）：`wave_results.verdict` 不是干净枚举 —— 除 FAIL/PARTIAL/PASS 外还存有
`0/6 过硬闸, 新高 0.31` 这类自由文本，以及 None/''。旧规则 B 用 `all(v == "FAIL")`
判定，这些形态一律**静默不算 FAIL** → 停止闸失效（EUR 最近 3 个 closed 波
verdict 恰为三条 `0/N 过硬闸` 自由文本，本应停区却放行）。

本测试覆盖：
  1. `_normalize_verdict` 的归一表（含自由文本、空值）；
  2. 规则 B 对自由文本形态能正确拦截（回归 EUR 场景）；
  3. 空 verdict 不据此拦截，但必须输出 WARN（不把"没写"当"通过"）；
  4. 可选更严口径 `strict_no_pass=True`：最近 K 波"无任何 PASS"即停。
"""
import json
import sqlite3

import pytest

from wqb.workflow.nodes import campaign as C


# --------------------------------------------------------------------------- 1
@pytest.mark.parametrize("raw,expected", [
    ("FAIL", "FAIL"),
    ("fail", "FAIL"),
    ("PARTIAL", "PARTIAL"),
    ("PASS", "PASS"),
    ("0/6 过硬闸, 新高 0.31", "FAIL"),      # 实测 EUR 形态：0 条过硬闸 = 全被硬闸拦下
    ("0/8 过硬闸, 新高 0.43", "FAIL"),
    ("3/8 过硬闸, 新高 2.10", "PARTIAL"),    # 有通过但未全过
    ("过硬闸情况未知", "UNKNOWN"),
    ("", "UNKNOWN"),
    (None, "UNKNOWN"),
    ("   ", "UNKNOWN"),
])
def test_normalize_verdict_table(raw, expected):
    assert C._normalize_verdict(raw) == expected


# --------------------------------------------------------------------------- 夹具
def _make_campaign_dir(tmp_path, stop_rules=None):
    cdir = tmp_path / "tracking" / "TESTREG"
    (cdir / "config").mkdir(parents=True)
    div = {}
    if stop_rules is not None:
        div["stop_rules"] = stop_rules
    (cdir / "config" / "thresholds.json").write_text(
        json.dumps({"diversity": div}, ensure_ascii=False), encoding="utf-8")
    return cdir


def _make_db(tmp_path, verdicts, n_backtested=0, n_passed=0, override=None):
    """建最小库：wave_results(closed) + backtest_results + ledger_kv。

    注意必须建 `ledger_kv`：闸会读 `stop_rules_override`；缺表会抛异常并被
    降级成 warning（success 仍 True），从而让"应拦截"的用例假通过。
    """
    db = tmp_path / "wqb_test.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE wave_results (id INTEGER PRIMARY KEY, region TEXT, "
                 "wave_number TEXT, verdict TEXT, status TEXT, "
                 "created_at TEXT, updated_at TEXT)")
    conn.execute("CREATE TABLE backtest_results (id INTEGER PRIMARY KEY, region TEXT, "
                 "sharpe REAL, fitness REAL)")
    conn.execute("CREATE TABLE ledger_kv (region TEXT, key TEXT, value TEXT)")
    # verdicts 列表首个 = 最近（created_at 递减，与闸的 ORDER BY ... DESC 对齐）
    for i, v in enumerate(verdicts):
        conn.execute(
            "INSERT INTO wave_results (region, wave_number, verdict, status, created_at) "
            "VALUES (?,?,?,'closed',?)",
            ("TESTREG", str(100 - i), v, f"2026-09-{20 - i:02d} 00:00:00"),
        )
    for i in range(n_backtested):
        passed = i < n_passed
        conn.execute("INSERT INTO backtest_results (region, sharpe, fitness) VALUES (?,?,?)",
                     ("TESTREG", 2.0 if passed else 0.3, 1.5 if passed else 0.4))
    if override is not None:
        conn.execute("INSERT INTO ledger_kv VALUES ('TESTREG','stop_rules_override',?)",
                     (json.dumps(override, ensure_ascii=False),))
    conn.commit()
    conn.close()
    return db


def _run(tmp_path, monkeypatch, verdicts, stop_rules=None, override=None, **dbkw):
    cdir = _make_campaign_dir(tmp_path, stop_rules)
    db = _make_db(tmp_path, verdicts, override=override, **dbkw)
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    return C._run_stop_rules_gate("TESTREG", None, str(cdir))


# --------------------------------------------------------------------------- 2
def test_rule_b_catches_freetext_zero_wall_verdicts(tmp_path, monkeypatch):
    """回归 EUR 场景：三条 `0/N 过硬闸` 自由文本必须判为全 FAIL 并拦截。

    旧实现 `all(v == "FAIL")` 对此恒为 False → 静默放行。
    """
    out = _run(tmp_path, monkeypatch, [
        "0/6 过硬闸, 新高 0.31",
        "0/8 过硬闸, 新高 0.48",
        "0/8 过硬闸, 新高 0.43",
    ])
    assert out["success"] is False, "自由文本全 FAIL 应被拦截"
    assert out["evidence"]["recent_closed_verdicts"] == ["FAIL", "FAIL", "FAIL"]
    assert any("B:" in h for h in out["hits"])


def test_rule_b_still_blocks_canonical_fail(tmp_path, monkeypatch):
    out = _run(tmp_path, monkeypatch, ["FAIL", "FAIL", "FAIL"])
    assert out["success"] is False
    assert any("B:" in h for h in out["hits"])


# --------------------------------------------------------------------------- 3
def test_empty_verdict_does_not_block_but_warns(tmp_path, monkeypatch):
    """空 verdict＝UNKNOWN：不据此拦截（避免台账缺写误停区），但必须 WARN。"""
    out = _run(tmp_path, monkeypatch, ["FAIL", None, "FAIL"])
    assert out["success"] is True, "UNKNOWN 不应导致拦截"
    assert "UNKNOWN" in out["evidence"]["recent_closed_verdicts"]
    assert out["warning"], "空 verdict 必须输出 WARN，不得静默"
    assert "回写 verdict" in out["warning"]


def test_partial_alone_does_not_block_by_default(tmp_path, monkeypatch):
    """默认口径沿用"全 FAIL"，故 (FAIL, PARTIAL, FAIL) 不拦截。"""
    out = _run(tmp_path, monkeypatch, ["FAIL", "PARTIAL", "FAIL"])
    assert out["success"] is True


# --------------------------------------------------------------------------- 4
def test_strict_no_pass_blocks_on_mixed_non_pass(tmp_path, monkeypatch):
    """strict_no_pass=True：最近 K 波"无任何 PASS"即停（含 PARTIAL/FAIL 混合）。"""
    out = _run(tmp_path, monkeypatch, ["FAIL", "PARTIAL", "FAIL"],
               stop_rules={"strict_no_pass": True})
    assert out["success"] is False
    assert any("无任何 PASS" in h for h in out["hits"])


def test_strict_no_pass_allows_when_a_pass_present(tmp_path, monkeypatch):
    out = _run(tmp_path, monkeypatch, ["FAIL", "PASS", "FAIL"],
               stop_rules={"strict_no_pass": True})
    assert out["success"] is True


# --------------------------------------------------------------------------- 5
def test_rule_a_zero_yield_still_works(tmp_path, monkeypatch):
    """规则 A 未被本次改动破坏：回测≥100 且达标 0 → 拦截。"""
    out = _run(tmp_path, monkeypatch, ["PASS", "PASS", "PASS"],
               n_backtested=120, n_passed=0)
    assert out["success"] is False
    assert any(h.startswith("A:") for h in out["hits"])


def test_override_ledger_releases(tmp_path, monkeypatch):
    """ledger stop_rules_override 有 reason 时命中即放行并留痕。"""
    out = _run(tmp_path, monkeypatch, ["FAIL", "FAIL", "FAIL"],
               override={"reason": "用户显式要求继续"})
    assert out["success"] is True
    assert out.get("override", {}).get("reason") == "用户显式要求继续"


# --------------------------------------------------------------------------- 6
# 测试/沙箱隔离口（2026-09-17 补齐）：三道闸的 WQB_DISABLE_* kill switch
# 背景：fake_toolkit fixture 此前只有 WQB_DISABLE_BACKLOG_GATE，stop_rules 与
# signal_floor 裸读真库——USA 真实近 2 批 max_sharpe=0.88 曾让命令拼装类单测
# 因环境（而非被测行为）失败。两个开关与 backlog 闸同款：env=1 → skipped。
def test_stop_rules_gate_env_kill_switch(tmp_path, monkeypatch):
    from wqb.workflow._common import REPO_ROOT
    monkeypatch.setenv("WQB_DISABLE_STOP_RULES_GATE", "1")
    out = C._run_stop_rules_gate("USA", None, str(REPO_ROOT / "tracking" / "USA"))
    assert out["success"] is True
    assert "WQB_DISABLE_STOP_RULES_GATE" in out.get("skipped", "")


def test_signal_floor_gate_env_kill_switch(tmp_path, monkeypatch):
    from wqb.workflow._common import REPO_ROOT
    monkeypatch.setenv("WQB_DISABLE_SIGNAL_FLOOR_GATE", "1")
    out = C._run_signal_floor_gate("USA", None, str(REPO_ROOT / "tracking" / "USA"))
    assert out["success"] is True
    assert "WQB_DISABLE_SIGNAL_FLOOR_GATE" in out.get("skipped", "")
