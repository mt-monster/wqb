"""MCP 工具层单元测试 (venv) — 拆分不变量 / 瘦身助手 / 表达式字段校验 (无网络)。

- 63 工具注册数不变量 (防拆分丢工具)
- 单例 identity 跨 main/mcp_core/tools_* 一致
- 响应瘦身助手 (_truncate/_unwrap_result/_is_error/_ra_bad/_slim_alpha)
- _extract_field_candidates 算子关键字过滤
- validate_expressions / create_multi_simulation 字段预检 (monkeypatch get_datafields)
"""
import asyncio

import pytest

import mcp_core
import tools_data
import tools_sim
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

def test_tool_registry_count_matches_expected():
    """工具注册总数不变量（2026-09-02 更新：63，新增 tools_ops 5 工具 + preflight_expressions，删除 3 冗余工具）。"""
    import main  # noqa: F401 — 副作用注册全部 tools_*
    n = len(mcp_core.mcp._tool_manager._tools)
    assert n >= 63, f"工具数 {n} < 63，可能丢了工具（拆分回归）"


def test_brain_client_singleton_identity():
    import main  # noqa: F401
    import tools_submit
    assert tools_data.brain_client is mcp_core.brain_client
    assert tools_submit.brain_client is mcp_core.brain_client


def test_each_tool_module_registers_at_least_one_tool():
    import importlib
    expected = {
        "tools_config": 1, "tools_labs": 3, "tools_account": 13, "tools_sim": 6,
        "tools_alpha": 8, "tools_data": 10, "tools_submit": 0, "tools_corr": 3,
        "tools_forum": 4, "tools_spc": 4, "tools_ops": 5,
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


def test_operator_filter_prefers_verified_json():
    """第一层：verified.json 是权威过滤表（102 实时算子），不依赖 ~/.zcode catalog。"""
    ops = tools_data._verified_operator_names()
    # 工作区 data/operators_verified.json 存在且非空（S-PRE 审计快照）
    assert len(ops) >= 80, f"verified.json 算子数异常: {len(ops)}"
    # 新算子必须在过滤表（历史误判点）
    for op in ("ts_corr", "ts_kurtosis", "ts_av_diff", "days_from_last_change", "if_else", "bucket"):
        assert op in ops, f"{op} 不在 verified 算子表"


def test_extract_fields_new_operators_not_misjudged():
    """第一层回归：新算子不被误判为字段（2026-09-02 前 catalog 缺失时会误杀）。"""
    exprs = [
        "rank(ts_corr(a_field, b_field, 22))",
        "multiply(-1, rank(ts_kurtosis(ts_delta(a_field, 5), 66)))",
        "trade_when(days_from_last_change(g_field) < 5, rank(a_field), 0)",
        "if_else(a_field > b_field, rank(a_field), multiply(-1, rank(b_field)))",
    ]
    fields = tools_data._extract_field_candidates(exprs)
    # 只有真实字段，算子全被过滤
    assert sorted(fields) == ["a_field", "b_field", "g_field"]


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
        self.calls = []

    async def get_datafields(self, **kwargs):
        self.calls.append(kwargs)
        return {"results": [{"id": f} for f in self._known]}


class _TruncatedDumpClient:
    """Unscoped dump is first-page-only; targeted search can still hit dataset ids."""
    DUMP = {"close", "returns", "volume"}
    SEARCHABLE = DUMP | {
        "probability_label1_2quantile_20day_eur_ohlcma",
        "probability_label1_2quantile_5day_ohlcv",
    }

    def __init__(self):
        self.calls = []
        self.posted = False
        self.base_url = "https://api.worldquantbrain.com"

    async def ensure_authenticated(self):
        return None

    async def get_datafields(self, **kwargs):
        self.calls.append(kwargs)
        search = (kwargs.get("search") or "").strip()
        if search:
            hits = [f for f in self.SEARCHABLE if search in f]
            return {"results": [{"id": f} for f in hits], "count": len(hits)}
        return {"results": [{"id": f} for f in self.DUMP], "count": len(self.DUMP)}

    async def _request(self, method, url, **kwargs):
        self.posted = True

        class _Resp:
            status_code = 201
            headers = {"Location": "/simulations/abc123"}
            text = ""

        return _Resp()

    def _to_absolute_url(self, loc):
        return self.base_url + loc


def test_validate_expressions_known_and_unknown(monkeypatch):
    stub = _StubClient({"close", "returns", "ep_yield_pct_smest_fy1_3"})
    monkeypatch.setattr(tools_data, "brain_client", stub)
    v = asyncio.run(tools_data.validate_expressions(
        ["rank(ts_rank(close, 250))", "rank(nonexistent_field_xyz)"],
        region="EUR", universe="TOP2500", delay=1))
    assert v["valid"] is False
    assert v["unknown_fields"] == ["nonexistent_field_xyz"]
    assert "close" in v["fields_checked"]
    assert any(c.get("search") for c in stub.calls)


def test_validate_expressions_all_known(monkeypatch):
    stub = _StubClient({"close", "returns"})
    monkeypatch.setattr(tools_data, "brain_client", stub)
    v = asyncio.run(tools_data.validate_expressions(["close / returns"]))
    assert v["valid"] is True and v["unknown_fields"] == []


def test_validate_expressions_dataset_field_missing_from_truncated_dump(monkeypatch):
    """False-positive regression: dataset-specific ids exist via search, not in page-1 dump."""
    stub = _TruncatedDumpClient()
    monkeypatch.setattr(tools_data, "brain_client", stub)
    field = "probability_label1_2quantile_20day_eur_ohlcma"
    v = asyncio.run(tools_data.validate_expressions(
        [f"rank({field})", "rank(close)"],
        region="EUR", universe="TOP1200", delay=1))
    assert v["valid"] is True
    assert v["unknown_fields"] == []
    assert field in v["fields_checked"]
    assert any(c.get("search") == field for c in stub.calls)


def test_validate_expressions_lookup_error_fails_open(monkeypatch):
    class _Boom:
        async def get_datafields(self, **kwargs):
            raise TimeoutError("simulated lookup timeout")

    monkeypatch.setattr(tools_data, "brain_client", _Boom())
    # close 是内置字段直接放行不触发查询；用非内置字段触发 lookup error 路径
    v = asyncio.run(tools_data.validate_expressions(["rank(close)"]))
    assert v["valid"] is True
    assert v["unknown_fields"] == []
    assert "close" in v.get("builtin_fields", [])
    # 非内置字段触发平台查询，超时应 fails-open 并带 warning
    v2 = asyncio.run(tools_data.validate_expressions(["rank(custom_field_xyz)"]))
    assert v2["valid"] is True
    assert v2["unknown_fields"] == []
    assert "warning" in v2


def test_create_multi_simulation_accepts_dataset_fields_absent_from_dump(monkeypatch):
    stub = _TruncatedDumpClient()
    monkeypatch.setattr(tools_sim, "brain_client", stub)
    out = asyncio.run(tools_sim.create_multi_simulation(
        [
            "rank(probability_label1_2quantile_20day_eur_ohlcma)",
            "rank(probability_label1_2quantile_5day_ohlcv)",
        ],
        region="EUR", universe="TOP1200", delay=1,
        validate_fields=True, wait_for_completion=False,
    ))
    assert "unknown_fields" not in out
    assert out.get("success") is True
    assert stub.posted is True
    assert any(c.get("search") for c in stub.calls)


def test_create_multi_simulation_still_blocks_genuine_unknown(monkeypatch):
    stub = _TruncatedDumpClient()
    monkeypatch.setattr(tools_sim, "brain_client", stub)
    out = asyncio.run(tools_sim.create_multi_simulation(
        ["rank(close)", "rank(nonexistent_field_xyz)"],
        region="EUR", universe="TOP1200", delay=1, validate_fields=True,
    ))
    assert "unknown_fields" in out
    assert out["unknown_fields"] == ["nonexistent_field_xyz"]
    assert stub.posted is False


def test_create_multi_simulation_validate_fields_false_skips_lookup(monkeypatch):
    stub = _TruncatedDumpClient()
    monkeypatch.setattr(tools_sim, "brain_client", stub)
    out = asyncio.run(tools_sim.create_multi_simulation(
        ["rank(nonexistent_field_xyz)", "rank(also_fake_abc)"],
        region="USA", universe="TOP3000",
        validate_fields=False, wait_for_completion=False,
    ))
    assert stub.calls == []
    assert stub.posted is True
    assert out.get("success") is True


# ---------------------------------------------------------------------------
# batch_create_simulations（per-item settings 批量，2026-08-23 新增）
# ---------------------------------------------------------------------------

class _BatchStubClient:
    def __init__(self):
        self.payloads = None

    async def batch_create_simulations(self, payloads):
        self.payloads = payloads
        return {
            "submitted": len(payloads),
            "total": len(payloads),
            "results": [{"index": i, "ok": True, "location": f"/simulations/sim{i}",
                         "simulation_id": f"sim{i}"} for i in range(len(payloads))],
            "note": "stub",
        }


def test_batch_create_simulations_per_item_settings_merge(monkeypatch):
    stub = _BatchStubClient()
    monkeypatch.setattr(tools_sim, "brain_client", stub)
    out = asyncio.run(tools_sim.batch_create_simulations(
        items=[
            {"expression": "rank(close)", "tag": "A"},
            {"expression": "rank(close)", "tag": "B",
             "settings": {"decay": 16, "neutralization": "SECTOR"}},
        ],
        base_region="KOR", base_universe="TOP600", base_decay=4,
        base_neutralization="STATISTICAL"))
    assert out["submitted"] == 2 and out.get("async") is True
    p0, p1 = stub.payloads
    assert p0["settings"]["decay"] == 4 and p0["settings"]["neutralization"] == "STATISTICAL"
    assert p1["settings"]["decay"] == 16 and p1["settings"]["neutralization"] == "SECTOR"
    assert p1["settings"]["region"] == "KOR" and p0["regular"] == "rank(close)"
    assert [r["tag"] for r in out["results"]] == ["A", "B"]


def test_batch_create_simulations_requires_base_region(monkeypatch):
    stub = _BatchStubClient()
    monkeypatch.setattr(tools_sim, "brain_client", stub)
    out = asyncio.run(tools_sim.batch_create_simulations(
        items=[{"expression": "rank(close)"}]))
    assert "error" in out and stub.payloads is None


# ---------------------------------------------------------------------------
# validate_expressions 三层解法回归（2026-09-02）
# ---------------------------------------------------------------------------

def test_validate_expressions_unknown_soft_grading(monkeypatch):
    """第二层：dataset 前缀字段 unknown 分级为 soft（delay/区域差异），不硬拦。"""
    stub = _StubClient({"close"})  # oth496_returns250 不在平台
    monkeypatch.setattr(tools_data, "brain_client", stub)
    v = asyncio.run(tools_data.validate_expressions(
        ["rank(ts_backfill(oth496_returns250, 10))"], region="KOR", universe="TOP600", delay=1))
    # soft 分级：valid 仍 True（不硬拦），但 unknown_soft 标注原因
    assert v["valid"] is True
    assert v["unknown_fields"] == []
    assert len(v["unknown_soft"]) == 1
    assert v["unknown_soft"][0]["field"] == "oth496_returns250"
    assert "delay" in v["unknown_soft"][0]["reason"]


def test_validate_expressions_builtin_fields_skip_lookup(monkeypatch):
    """第二层：内置字段不触发平台查询，直接放行。"""
    stub = _StubClient(set())  # 平台无任何字段
    monkeypatch.setattr(tools_data, "brain_client", stub)
    v = asyncio.run(tools_data.validate_expressions(
        ["trade_when(volume > ts_mean(volume, 20), rank(close), 0)"]))
    assert v["valid"] is True
    assert v["unknown_fields"] == []
    assert set(v["builtin_fields"]) == {"volume", "close"}
    assert not stub.calls  # 内置字段未触发任何平台查询
