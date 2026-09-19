# -*- coding: utf-8 -*-
"""P0-2 积压闸"未消费"口径（2026-09-17）.

背景（实测）：旧口径只算 `pending`+`gated`，**漏掉 gem/selected**（数量最大的两类
积压）。DEU 实测 conversion=10.3%≥10%、pending+gated=6.6%<30% → **通过**，但其
gem 存量 1198 条占全区表达式 72% —— 典型的"假通过"。JPN 首日 gem=1640 而
pending+gated=0，若非 conversion 恰好为 0，积压将完全不可见。

本测试覆盖：
  1. evidence 必须报出 gem/selected/unconsumed/unconsumed_ratio；
  2. 灰度默认（unconsumed_enforce=False）：只报不拦（DEU 场景仍 success=True + warnings）；
  3. 置 unconsumed_enforce=True：同样场景转为拦截（假通过消除）。
"""
import json
import sqlite3

from wqb.workflow.nodes import campaign as C


def _setup(tmp_path, monkeypatch, status_counts, backlog_cfg=None):
    cdir = tmp_path / "tracking" / "TESTREG"
    (cdir / "config").mkdir(parents=True)
    div = {}
    if backlog_cfg is not None:
        div["backlog_gate"] = backlog_cfg
    (cdir / "config" / "thresholds.json").write_text(
        json.dumps({"diversity": div}, ensure_ascii=False), encoding="utf-8")

    db = tmp_path / "wqb_test.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE expressions (id INTEGER PRIMARY KEY, region TEXT, status TEXT)")
    conn.execute("CREATE TABLE ledger_kv (region TEXT, key TEXT, value TEXT)")
    for status, n in status_counts.items():
        for _ in range(n):
            conn.execute("INSERT INTO expressions (region, status) VALUES ('TESTREG',?)", (status,))
    conn.commit()
    conn.close()
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    return str(cdir)


# DEU 实测形态：有回测、pending+gated 低，但 gem 巨大
_DEU_LIKE = {"backtested": 171, "gem": 1198, "pending": 43, "gated": 66, "dropped": 172, "simulating": 8}


def test_evidence_reports_unconsumed_breakdown(tmp_path, monkeypatch):
    cdir = _setup(tmp_path, monkeypatch, _DEU_LIKE)
    out = C._run_backlog_gate("TESTREG", None, cdir)
    ev = out["evidence"]
    assert ev["gem"] == 1198
    assert ev["selected"] == 0
    assert ev["unconsumed"] == 1198 + 109          # gem + selected + pending+gated
    assert ev["unconsumed_ratio"] > 0.78
    assert ev["unconsumed_enforced"] is False


def test_gray_mode_reports_but_does_not_block_deu_like(tmp_path, monkeypatch):
    """灰度默认：DEU 形态（conversion 10.3%、pg 6.6%）仍放行，但必须告警。"""
    cdir = _setup(tmp_path, monkeypatch, _DEU_LIKE)
    out = C._run_backlog_gate("TESTREG", None, cdir)
    assert out["success"] is True, "灰度阶段不应拦截"
    assert out.get("warnings"), "必须输出灰度告警"
    assert "未消费积压" in out["warnings"][0]
    assert "未拦截" in out["warnings"][0]


def test_enforce_mode_blocks_deu_like(tmp_path, monkeypatch):
    """置 unconsumed_enforce=True：同一场景转为拦截（消除假通过）。"""
    cdir = _setup(tmp_path, monkeypatch, _DEU_LIKE, backlog_cfg={"unconsumed_enforce": True})
    out = C._run_backlog_gate("TESTREG", None, cdir)
    assert out["success"] is False
    assert any("未消费积压" in h for h in out["hits"])
    assert out["evidence"]["unconsumed_enforced"] is True


def test_jpn_like_gem_only_visible_via_unconsumed(tmp_path, monkeypatch):
    """JPN 形态：pending+gated=0（旧口径完全看不见），未消费比 94%。"""
    cdir = _setup(tmp_path, monkeypatch,
                  {"gem": 1640, "selected": 48, "dropped": 48, "probe": 48})
    out = C._run_backlog_gate("TESTREG", None, cdir)
    ev = out["evidence"]
    assert ev["pending_gated"] == 0
    assert ev["unconsumed"] == 1688
    assert ev["unconsumed_ratio"] > 0.94
    # conversion=0 仍由既有口径拦截，但 evidence 现在同时暴露了 gem 真相
    assert out["success"] is False


def test_threshold_override_disables_gate(tmp_path, monkeypatch):
    """enabled:false 仍可整闸关闭（保留既有逃生口）。"""
    cdir = _setup(tmp_path, monkeypatch, _DEU_LIKE, backlog_cfg={"enabled": False})
    out = C._run_backlog_gate("TESTREG", None, cdir)
    assert out["success"] is True
    assert out.get("skipped")


def test_small_region_below_min_expressions_not_judged(tmp_path, monkeypatch):
    """表达式总量 < min_expressions(200) 的新区不判。"""
    cdir = _setup(tmp_path, monkeypatch, {"gem": 10})
    out = C._run_backlog_gate("TESTREG", None, cdir)
    assert out["success"] is True
    assert "min" in str(out.get("skipped"))
