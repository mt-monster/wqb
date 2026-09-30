# -*- coding: utf-8 -*-
"""规则 B 按轴计数（axis_scope，2026-09-23）.

背景：旧规则 B 是「全区最近 K=3 个 closed 波 verdict 全 FAIL → 停区」，实测 4 个缺陷：
换数据集后上一波的失败仍累计、零配额 FAIL（过了 gate 从未回测）也计数、有信息产出
（新 dead_end）的 FAIL 与纯烧槽位的 FAIL 同权、撞墙型 FAIL（信号存在但结构性不可
提交）没有路由提示。新语义（axis_scope=True 且 schema 齐备时）：
  B1 同轴熔断：开波 dataset 轴最近 closed 波序列连续可计数 FAIL ≥ K → 拦截；
  B2 区级多轴停：最近 axis_window 波窗口内无 PASS 且 ≥D 个不同轴全 FAIL → 停区；
  豁免：零配额 FAIL / 产出新 dead_end 的 FAIL 不计数（也不打断连续性）；
  撞墙提示：涉及波 max|sharpe| ≥ floor（signal_floor.max_sharpe_floor，缺省 0.5）
  时附路由提示；信号缺席拦截归 signal_floor 闸（本闸只在 evidence 标注）。
schema 不齐（旧夹具）或 axis_scope=False → 完全回落旧口径（见
test_stop_rules_verdict_p0p3.py / test_wiring_fixes_20260915.py，必须原样通过）。
"""
import json
import sqlite3

import pytest

from wqb.workflow.nodes import campaign as C


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


def _make_db(tmp_path, waves, backtests=(), gates=(), expressions=(), dead_ends=(),
             override=None):
    """建富 schema 库（按轴口径所需 6 表齐备）。

    waves: [(wave_number, verdict)]，首个 = 最近（created_at 递减，与闸的
           ORDER BY ... DESC 对齐）；
    backtests: [(wave, dataset, sharpe)]；gates: [(wave, dataset)]；
    expressions: [(wave, dataset, status)]；dead_ends: [(payload, created_at)]。
    """
    db = tmp_path / "wqb_test.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE wave_results (id INTEGER PRIMARY KEY, region TEXT, "
                 "wave_number TEXT, verdict TEXT, status TEXT, "
                 "created_at TEXT, updated_at TEXT)")
    conn.execute("CREATE TABLE backtest_results (id INTEGER PRIMARY KEY, region TEXT, "
                 "wave TEXT, dataset TEXT, sharpe REAL, fitness REAL)")
    conn.execute("CREATE TABLE expressions (id INTEGER PRIMARY KEY, region TEXT, "
                 "wave TEXT, dataset TEXT, status TEXT)")
    conn.execute("CREATE TABLE gate_results (id INTEGER PRIMARY KEY, region TEXT, "
                 "wave TEXT, dataset TEXT, all_pass INTEGER)")
    conn.execute("CREATE TABLE registry_empirical (id INTEGER PRIMARY KEY, region TEXT, "
                 "layer TEXT, entry_id TEXT, family TEXT, payload TEXT, dead_at TEXT, "
                 "created_at TEXT, updated_at TEXT)")
    conn.execute("CREATE TABLE ledger_kv (region TEXT, key TEXT, value TEXT)")
    for i, (wave, verdict) in enumerate(waves):
        ts = f"2026-09-{20 - i:02d} 00:00:00"
        conn.execute(
            "INSERT INTO wave_results (region, wave_number, verdict, status, "
            "created_at, updated_at) VALUES (?,? ,?,'closed',?,?)",
            ("TESTREG", str(wave), verdict, ts, ts),
        )
    for wave, dataset, sharpe in backtests:
        conn.execute(
            "INSERT INTO backtest_results (region, wave, dataset, sharpe, fitness) "
            "VALUES (?,?,?,?,?)",
            ("TESTREG", str(wave), dataset, sharpe, 0.4),
        )
    for wave, dataset in gates:
        conn.execute(
            "INSERT INTO gate_results (region, wave, dataset, all_pass) VALUES (?,?,?,0)",
            ("TESTREG", str(wave), dataset),
        )
    for wave, dataset, status in expressions:
        conn.execute(
            "INSERT INTO expressions (region, wave, dataset, status) VALUES (?,?,?,?)",
            ("TESTREG", str(wave), dataset, status),
        )
    for payload, created_at in dead_ends:
        conn.execute(
            "INSERT INTO registry_empirical (region, layer, entry_id, family, payload, "
            "created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
            ("TESTREG", "dead_end", "de_test", "fam", payload, created_at, created_at),
        )
    if override is not None:
        conn.execute("INSERT INTO ledger_kv VALUES ('TESTREG','stop_rules_override',?)",
                     (json.dumps(override, ensure_ascii=False),))
    conn.commit()
    conn.close()
    return db


def _run(tmp_path, monkeypatch, dataset, waves, stop_rules=None, **dbkw):
    cdir = _make_campaign_dir(tmp_path, stop_rules)
    db = _make_db(tmp_path, waves, **dbkw)
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    return C._run_stop_rules_gate("TESTREG", dataset, str(cdir))


def _three_fail_waves_dsA(sharpe=0.3):
    """同轴 dsA 三连 FAIL（均真实回测过 → 可计数）。"""
    return dict(
        waves=[("216", "FAIL"), ("215", "FAIL"), ("214", "FAIL")],
        backtests=[("216", "dsA", sharpe), ("215", "dsA", sharpe), ("214", "dsA", sharpe)],
    )


# --------------------------------------------------------------------------- 1
def test_b1_same_axis_circuit_breaker(tmp_path, monkeypatch):
    """同轴 3 连 FAIL + 开波 dataset 同轴 → 拦截（报文含「轴」）。"""
    out = _run(tmp_path, monkeypatch, "dsA", **_three_fail_waves_dsA())
    assert out["success"] is False
    assert any("B:" in h and "轴" in h and "dsA" in h for h in out["hits"])
    assert out["evidence"]["axis_scope"] is True
    details = {w["wave"]: w for w in out["evidence"]["wave_details"]}
    assert details["216"]["axis"] == "dsA" and details["216"]["countable_fail"] is True


def test_b1_allows_new_axis(tmp_path, monkeypatch):
    """同轴 3 连 FAIL 但开波换不同 dataset，且窗口内不同轴数 < D → 放行。"""
    out = _run(tmp_path, monkeypatch, "dsB", **_three_fail_waves_dsA())
    assert out["success"] is True, out.get("hits")
    assert "hits" not in out


# --------------------------------------------------------------------------- 3
def test_b2_multi_axis_stop(tmp_path, monkeypatch):
    """B2：窗口内 4 个不同轴全 FAIL 无 PASS → 拦截（报文含「不同轴」）。"""
    out = _run(tmp_path, monkeypatch, None,
               waves=[("216", "FAIL"), ("215", "FAIL"), ("214", "FAIL"), ("213", "FAIL")],
               backtests=[("216", "dsA", 0.3), ("215", "dsB", 0.3),
                          ("214", "dsC", 0.3), ("213", "dsD", 0.3)])
    assert out["success"] is False
    assert any("不同轴" in h for h in out["hits"])
    assert any("多轴探索已证伪" in h for h in out["hits"])


def test_b2_not_triggered_with_pass_in_window(tmp_path, monkeypatch):
    """窗口内有 PASS 时 B2 不触发（区仍在产出）。"""
    out = _run(tmp_path, monkeypatch, None,
               waves=[("216", "PASS"), ("215", "FAIL"), ("214", "FAIL"),
                      ("213", "FAIL"), ("212", "FAIL")],
               backtests=[("216", "dsA", 2.0), ("215", "dsB", 0.3),
                          ("214", "dsC", 0.3), ("213", "dsD", 0.3), ("212", "dsE", 0.3)])
    assert out["success"] is True, out.get("hits")


# --------------------------------------------------------------------------- 4
def test_dead_end_exemption_payload_mention(tmp_path, monkeypatch):
    """dead_end 豁免：3 连 FAIL 中一波的 registry_empirical payload 提及该波号 → 放行。"""
    out = _run(tmp_path, monkeypatch, "dsA",
               dead_ends=[('{"wave": 215, "reason": "coverage wall"}', "2026-09-25 00:00:00")],
               **_three_fail_waves_dsA())
    assert out["success"] is True, out.get("hits")
    details = {w["wave"]: w for w in out["evidence"]["wave_details"]}
    assert details["215"]["dead_end_productive"] is True
    assert details["215"]["countable_fail"] is False
    assert details["216"]["dead_end_productive"] is False
    assert details["214"]["dead_end_productive"] is False


def test_dead_end_exemption_time_window(tmp_path, monkeypatch):
    """dead_end 豁免（时间窗分支）：created_at 落在 [波 created, updated+2d] 即豁免。"""
    # 波 created/updated：216=09-20 / 215=09-19 / 214=09-18 → 窗口分别为
    # [09-20,09-22] / [09-19,09-21] / [09-18,09-20]。dead 行 09-20 12:00 落入
    # 216 与 215 的窗口（214 的窗口 09-20 00:00 已截止）→ 两波豁免，
    # 连续可计数 FAIL 只剩 214 → 不拦截。
    out = _run(tmp_path, monkeypatch, "dsA",
               dead_ends=[('{"reason": "turnover wall"}', "2026-09-20 12:00:00")],
               **_three_fail_waves_dsA())
    assert out["success"] is True, out.get("hits")
    details = {w["wave"]: w for w in out["evidence"]["wave_details"]}
    assert details["216"]["dead_end_productive"] is True
    assert details["215"]["dead_end_productive"] is True
    assert details["214"]["dead_end_productive"] is False


# --------------------------------------------------------------------------- 5
def test_zero_cost_exemption(tmp_path, monkeypatch):
    """零配额豁免：3 连 FAIL 但中间一波只有 gate_results 无 backtest → 不拦截。"""
    out = _run(tmp_path, monkeypatch, "dsA",
               waves=[("216", "FAIL"), ("215", "FAIL"), ("214", "FAIL")],
               backtests=[("216", "dsA", 0.3), ("214", "dsA", 0.3)],
               gates=[("215", "dsA")],
               expressions=[("215", "dsA", "gated")])  # axis 经 expressions 回落
    assert out["success"] is True, out.get("hits")
    details = {w["wave"]: w for w in out["evidence"]["wave_details"]}
    assert details["215"]["zero_cost"] is True
    assert details["215"]["axis"] == "dsA"       # expressions 回落取轴
    assert details["215"]["countable_fail"] is False
    assert details["216"]["zero_cost"] is False


def test_zero_cost_counts_when_switch_off(tmp_path, monkeypatch):
    """exempt_zero_cost_waves=False 时零配额 FAIL 恢复计数（3 连 → 拦截）。"""
    out = _run(tmp_path, monkeypatch, "dsA",
               stop_rules={"exempt_zero_cost_waves": False},
               waves=[("216", "FAIL"), ("215", "FAIL"), ("214", "FAIL")],
               backtests=[("216", "dsA", 0.3), ("214", "dsA", 0.3)],
               gates=[("215", "dsA")],
               expressions=[("215", "dsA", "gated")])
    assert out["success"] is False
    assert any("轴" in h for h in out["hits"])


# --------------------------------------------------------------------------- 6
def test_wall_routing_hint(tmp_path, monkeypatch):
    """撞墙提示：拦截涉及波 max|sharpe| ≥ floor 时，hits 含路由提示文字。"""
    out = _run(tmp_path, monkeypatch, "dsA",
               waves=[("216", "FAIL"), ("215", "FAIL"), ("214", "FAIL")],
               backtests=[("216", "dsA", 1.76), ("215", "dsA", 1.60), ("214", "dsA", 0.3)])
    assert out["success"] is False
    assert any("信号存在但结构性不可提交" in h for h in out["hits"])
    assert any("prod-first" in h for h in out["hits"])
    # evidence 标注 wall / signal_absent 分类（信号缺席拦截归 signal_floor 闸）
    details = {w["wave"]: w for w in out["evidence"]["wave_details"]}
    assert details["216"]["signal_class"] == "wall"
    assert details["214"]["signal_class"] == "signal_absent"


# --------------------------------------------------------------------------- 7
def test_axis_scope_false_goes_legacy(tmp_path, monkeypatch):
    """axis_scope=False 时即便 schema 齐全也走旧口径（最近 K 波全 FAIL 即拦）。"""
    out = _run(tmp_path, monkeypatch, None,
               stop_rules={"axis_scope": False},
               waves=[("216", "FAIL"), ("215", "FAIL"), ("214", "FAIL")],
               backtests=[("216", "dsA", 0.3), ("215", "dsB", 0.3), ("214", "dsC", 0.3)])
    assert out["success"] is False
    assert any("verdict 全 FAIL" in h for h in out["hits"])
    assert "axis_scope" not in out["evidence"]  # 证明未走按轴路径


# --------------------------------------------------------------------------- 8
def test_unknown_does_not_block_but_warns(tmp_path, monkeypatch):
    """UNKNOWN 在新路径仍不拦截 + WARN（打断同轴连续失败计数）。"""
    out = _run(tmp_path, monkeypatch, "dsA",
               waves=[("216", "FAIL"), ("215", None), ("214", "FAIL")],
               backtests=[("216", "dsA", 0.3), ("215", "dsA", 0.3), ("214", "dsA", 0.3)])
    assert out["success"] is True, out.get("hits")
    assert "UNKNOWN" in out["evidence"]["recent_closed_verdicts"]
    assert out["warning"] and "回写 verdict" in out["warning"]


def test_strict_no_pass_still_works(tmp_path, monkeypatch):
    """strict_no_pass=True 在新路径仍生效：最近 K 波无任何 PASS 即停。"""
    out = _run(tmp_path, monkeypatch, None,
               stop_rules={"strict_no_pass": True},
               waves=[("216", "FAIL"), ("215", "PARTIAL"), ("214", "FAIL")],
               backtests=[("216", "dsA", 0.3), ("215", "dsB", 0.3), ("214", "dsC", 0.3)])
    assert out["success"] is False
    assert any("无任何 PASS" in h for h in out["hits"])


def test_strict_no_pass_allows_when_pass_present(tmp_path, monkeypatch):
    out = _run(tmp_path, monkeypatch, None,
               stop_rules={"strict_no_pass": True},
               waves=[("216", "FAIL"), ("215", "PASS"), ("214", "FAIL")],
               backtests=[("216", "dsA", 0.3), ("215", "dsB", 2.0), ("214", "dsC", 0.3)])
    assert out["success"] is True, out.get("hits")


# --------------------------------------------------------------------------- 附加
def test_override_releases_on_axis_path(tmp_path, monkeypatch):
    """ledger stop_rules_override 在按轴路径同样放行（机制保持现状）。"""
    out = _run(tmp_path, monkeypatch, "dsA",
               override={"reason": "用户显式要求继续"},
               **_three_fail_waves_dsA())
    assert out["success"] is True
    assert out.get("override", {}).get("reason") == "用户显式要求继续"
    assert "stop_rules_override" in out.get("note", "")


def test_rule_a_still_works_on_axis_path(tmp_path, monkeypatch):
    """规则 A（≥100 回测且达标 0）在按轴路径不受影响。"""
    waves = [("216", "PASS"), ("215", "PASS"), ("214", "PASS")]
    backtests = [(str(200 + i), "dsA", 0.3) for i in range(120)]  # 规则 A 需 ≥100 样本
    out = _run(tmp_path, monkeypatch, None, waves=waves, backtests=backtests)
    assert out["success"] is False
    assert any(h.startswith("A:") for h in out["hits"])
