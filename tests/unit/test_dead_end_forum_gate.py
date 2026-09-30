# -*- coding: utf-8 -*-
"""seal_dead_end 判死取证闸守护（2026-09-29 fail-closed）。

背景：判死是**永久封存一条路**，误判代价高。此前 S6 判死前的 forum_recon 核对只是
「软提示」（无记录不拦写入），且 `tools/forum_recon.py` 把工具故障记成 `found=false`
落 `forum_recon_negative_*` —— 而 SOP 把 `found=false` 当作 decision-table D2
「论坛无解」的判死取证，等于**工具坏了 ≡ 论坛无解**（假阴性，实证 5 条中 2 条中招）。

现改为 fail-closed 硬闸，本文件守护其四态判定。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_DB_MCP = REPO_ROOT / "wqb_db_mcp.py"


def _load_db_mcp():
    """按文件路径加载 wqb_db_mcp（该模块 import 期会装配 MCP，不能走常规 import）。"""
    spec = importlib.util.spec_from_file_location("_wqb_db_mcp_for_gate", _DB_MCP)
    if spec is None or spec.loader is None:
        pytest.skip("无法构造 wqb_db_mcp 的 import spec")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception as e:  # 装配失败不应让闸逻辑失去守护
        pytest.skip(f"wqb_db_mcp 加载失败（环境依赖）：{type(e).__name__}")
    if not hasattr(mod, "_forum_recon_gate"):
        pytest.skip("wqb_db_mcp 未提供 _forum_recon_gate")
    return mod


@pytest.fixture(scope="module")
def gate():
    return _load_db_mcp()._forum_recon_gate


def test_gate_blocks_when_no_evidence(gate):
    """无取证记录 → 拒绝判死（未取证）。"""
    r = gate({})
    assert r["allowed"] is False and r["state"] == "missing"
    assert "未取证" in r["reason"]


def test_gate_blocks_on_tool_error(gate):
    """工具故障（found=null / status=error）→ 拒绝；**故障 ≠ 论坛无解**。

    这是本次修复的核心：旧行为会把这条当成「论坛无解」放行判死。
    """
    for payload in (
        {"forum_recon": {"found": None, "status": "error",
                         "error": "No module named 'requests'"}},
        {"forum_recon": {"status": "error", "error": "forum auth failed: load_creds"}},
    ):
        r = gate(payload)
        assert r["allowed"] is False, payload
        assert r["state"] == "error"
        assert "未取证" in r["reason"] or "故障" in r["reason"]


def test_gate_blocks_when_forum_has_solution(gate):
    """论坛有解法 → 拒绝判死（应转 salvage/Mode B 武器）。"""
    r = gate({"forum_recon": {"found": True, "question_key": "abc"}})
    assert r["allowed"] is False and r["state"] == "has_solution"
    assert "不得直接判死" in r["reason"]


def test_gate_allows_confirmed_no_solution(gate):
    """真实检索后确认无解 → 允许判死（D2 取证成立）。"""
    r = gate({"forum_recon": {"found": False, "question_key": "abc", "rounds": 8}})
    assert r["allowed"] is True and r["state"] == "no_solution"


def test_gate_distinguishes_false_from_none(gate):
    """found=False 与 found=None 必须给出**相反**结论——这是假阴性修复的关键断言。"""
    assert gate({"forum_recon": {"found": False}})["allowed"] is True
    assert gate({"forum_recon": {"found": None}})["allowed"] is False
