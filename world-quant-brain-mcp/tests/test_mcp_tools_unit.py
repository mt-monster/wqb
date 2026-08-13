"""MCP 工具层单元测试 (venv) — 拆分不变量 / 瘦身助手 / 表达式字段校验 (无网络)。

- 51 工具注册数不变量 (防拆分丢工具)
- 单例 identity 跨 main/mcp_core/tools_* 一致
- 响应瘦身助手 (_truncate/_unwrap_result/_is_error/_ra_bad/_slim_alpha)
- _extract_field_candidates 算子关键字过滤
- validate_expressions 离线验证 (monkeypatch brain_client.get_datafields)
"""
import asyncio

import pytest

import mcp_core
import tools_data
from mcp_core import (
    _is_error,
    _ra_bad,
    _rewrap,
    _slim_alpha,
    _truncate,
    _unwrap_result,
)


# ---------------------------------------------------------------------------
# 拆分不变量
# ---------------------------------------------------------------------------

def test_tool_registry_count_is_51():
    import main  # noqa: F401 — 副作用注册全部 tools_*
    assert len(mcp_core.mcp._tool_manager._tools) == 51


def test_brain_client_singleton_identity():
    import main  # noqa: F401
    import tools_submit
    assert tools_data.brain_client is mcp_core.brain_client
    assert tools_submit.brain_client is mcp_core.brain_client


def test_each_tool_module_registers_at_least_one_tool():
    import importlib
    expected = {
        "tools_config": 1, "tools_labs": 3, "tools_account": 13, "tools_sim": 4,
        "tools_alpha": 7, "tools_data": 10, "tools_submit": 2, "tools_corr": 3,
        "tools_forum": 4, "tools_spc": 4,
    }
    for mod, n in expected.items():
        m = importlib.import_module(mod)
        tools = [x for x in dir(m) if not x.startswith("_")]
        # 校验: 模块内 @mcp.tool 注册的函数名与 main 注册表一致
        registered = set(mcp_core.mcp._tool_manager._tools.keys())
        count = sum(1 for name in tools if name in registered)
        assert count == n, f"{mod}: {count} != {n}"


# ---------------------------------------------------------------------------
# 瘦身助手
# ---------------------------------------------------------------------------

def test_truncate():
    out = _truncate("x" * 300, 160)
    assert out.startswith("x" * 160) and out.endswith("…")


def test_is_error():
    assert _is_error({"error": "boom"}) is True
    assert _is_error({"ok": 1}) is False


def test_unwrap_result_plain():
    obj = {"is": {"sharpe": 2.0}}
    payload, wrapped = _unwrap_result(obj)
    assert payload == obj and wrapped is False


def test_unwrap_result_wrapped():
    obj = {"result": {"is": {"sharpe": 2.0}}}
    payload, wrapped = _unwrap_result(obj)
    assert payload["is"]["sharpe"] == 2.0 and wrapped is True


def test_rewrap_roundtrip():
    obj = {"result": {"a": 1}}
    payload, w = _unwrap_result(obj)
    assert _rewrap(payload, w) == {"result": {"a": 1}}


def test_ra_bad_tristate():
    # WebDataScope 规则: 只有 PASS/PENDING 算好, 其余 (FAIL/WARNING) 均计失败
    assert _ra_bad("FAIL") is True
    assert _ra_bad("WARNING") is True
    assert _ra_bad("PASS") is False
    assert _ra_bad("PENDING") is False


def test_slim_alpha_keeps_core_keys():
    slim = _slim_alpha({"id": "abc", "name": "n", "color": "GREEN", "tags": ["t"],
                        "extra_noise": {"big": "x" * 5000}})
    assert slim["id"] == "abc"
    assert "extra_noise" not in slim


# ---------------------------------------------------------------------------
# _extract_field_candidates (tools_data)
# ---------------------------------------------------------------------------

def test_extract_fields_basic():
    fields = tools_data._extract_field_candidates(
        ["rank(ts_rank(close, 250)) + reverse(returns)"])
    assert set(fields) == {"close", "returns"}


def test_extract_fields_excludes_operator_keywords():
    fields = tools_data._extract_field_candidates(
        ["ts_delta(ts_backfill(ep_yield_pct_smest_fy1_3, 66), 22)"])
    # ts_delta/ts_backfill 是算子关键字; ep_yield_pct_smest_fy1_3 是字段
    assert fields == ["ep_yield_pct_smest_fy1_3"]


def test_extract_fields_pure_operator_expression():
    # 回归测试: ts_returns 是 catalog 真算子, 必须被过滤 (2026-08-13 修复前
    # 手写关键字清单缺 ts_returns → validate_expressions 误报 unknown_fields)
    fields = tools_data._extract_field_candidates(["rank(ts_returns(1))"])
    assert fields == []


def test_extract_fields_reduce_operator_filtered():
    fields = tools_data._extract_field_candidates(["rank(reduce_ir(x, 5))"])
    assert fields == ["x"]


def test_extract_fields_group_dimensions_excluded():
    fields = tools_data._extract_field_candidates(
        ["group_rank(ts_rank(fnd6_pe, 60), industry)"])
    assert fields == ["fnd6_pe"]  # group_rank/ts_rank/industry 均非字段


# ---------------------------------------------------------------------------
# validate_expressions 离线验证 (monkeypatch 平台字段)
# ---------------------------------------------------------------------------

class _StubClient:
    def __init__(self, known):
        self._known = known

    async def get_datafields(self, **kwargs):
        return {"results": [{"id": f} for f in self._known]}


def test_validate_expressions_known_and_unknown(monkeypatch):
    stub = _StubClient({"close", "returns", "ep_yield_pct_smest_fy1_3"})
    monkeypatch.setattr(tools_data, "brain_client", stub)
    v = asyncio.run(tools_data.validate_expressions(
        ["rank(ts_rank(close, 250))", "rank(nonexistent_field_xyz)"],
        region="EUR", universe="TOP2500", delay=1))
    assert v["valid"] is False
    assert v["unknown_fields"] == ["nonexistent_field_xyz"]
    assert "close" in v["fields_checked"]


def test_validate_expressions_all_known(monkeypatch):
    stub = _StubClient({"close", "returns"})
    monkeypatch.setattr(tools_data, "brain_client", stub)
    v = asyncio.run(tools_data.validate_expressions(["close / returns"]))
    assert v["valid"] is True and v["unknown_fields"] == []
