# -*- coding: utf-8 -*-
"""forum_recon 节点守护（2026-09-28 P4 节点化）.

覆盖：dry-run 契约（零 subprocess、命令含全部透传 flag）、参数校验短路、
退出码语义映射（0=有货 / 2=无解也是合法结局 / 其它=异常）、超时杀树回日志。
"""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from wqb.workflow.nodes import forum_recon as node  # noqa: E402


def _fake_run(rc=0, timed_out=False, tail="ok"):
    def _run(cmd, **kw):
        return {"log_path": "L.log", "elapsed_sec": 0.1, "tail": tail,
                "returncode": rc, "timed_out": timed_out}
    return _run


def test_dry_run_builds_cmd_without_subprocess(monkeypatch):
    def _boom(*a, **k):
        raise AssertionError("dry-run 不得 subprocess")

    monkeypatch.setattr(node, "run_logged_subprocess", _boom)
    out = node.run(question="GLB 墙有无破墙配方", context="region=GLB,wall=SHARPE",
                   out="ledger", limit=2, max_search_rounds=5, queries="a,b",
                   dry_run=True)
    assert out["success"] is True and out["dry_run"] is True
    cmd = out["cmd"]
    assert "forum_recon.py" in cmd[2]
    for flag, val in (("--question", "GLB 墙有无破墙配方"), ("--context", "region=GLB,wall=SHARPE"),
                      ("--out", "ledger"), ("--limit", "2"), ("--max-search-rounds", "5"),
                      ("--queries", "a,b")):
        i = cmd.index(flag)
        assert cmd[i + 1] == val
    assert "validate_argv" not in out.get("error", "")


def test_empty_question_short_circuits(monkeypatch):
    def _boom(*a, **k):
        raise AssertionError("参数不合法不得 subprocess")

    monkeypatch.setattr(node, "run_logged_subprocess", _boom)
    out = node.run(question="   ")
    assert out["success"] is False and "question 不能为空" in out["error"]


def test_bad_out_rejected(monkeypatch):
    def _boom(*a, **k):
        raise AssertionError("参数不合法不得 subprocess")

    monkeypatch.setattr(node, "run_logged_subprocess", _boom)
    out = node.run(question="q", out="stroll")
    assert out["success"] is False and "kb|ledger|negative" in out["error"]


def test_exit_codes_mapping(monkeypatch):
    monkeypatch.setattr(node, "run_logged_subprocess", _fake_run(rc=0))
    out = node.run(question="q")
    assert out["success"] is True and out["found"] is True

    monkeypatch.setattr(node, "run_logged_subprocess", _fake_run(rc=2))
    out = node.run(question="q")
    assert out["success"] is True and out["found"] is False      # 无解=合法结局
    assert "判死证据" in out["note"]

    monkeypatch.setattr(node, "run_logged_subprocess", _fake_run(rc=1))
    out = node.run(question="q")
    assert out["success"] is False and out["found"] is False


def test_timeout_reports_log(monkeypatch):
    monkeypatch.setattr(node, "run_logged_subprocess", _fake_run(timed_out=True))
    out = node.run(question="q")
    assert out["success"] is False and out["timed_out"] is True
    assert "超时" in out["error"] and "L.log" in out["error"]
