# -*- coding: utf-8 -*-
"""set_expression_status / supersede_unpicked：只传 id/状态过滤的批量改状态写路径。

背景（2026-09-12 GBR wave57 实测）：改一波 43 条候选的状态，唯一写路径是
upsert_expressions —— 必须把 43 条完整表达式原样回传，服务端 3 ms，MCP 侧却要吐
3-4k token。成本在载荷不在库。本文件锁定新写路径的契约：
  1. 无过滤（ids/from_status 都缺）拒绝；ids 与 from_status 同给取交集；region+wave 限定
  2. 已回测行（alpha_id 非空）只有 to_status 为终态归档（superseded/dropped）才会被改，
     否则跳过并以 n_protected 回报（不静默）
  3. reason 合并进 settings_json.status_change，不清空既有 decay/neutralization 等键；
     list_expressions 的 settings 视图不含该审计键（它不是回测设置，tools_sim /
     pipeline per-item overrides 会把 settings 的每个键原样并进平台 payload）
  4. MCP 包装：注册名 set_expression_status；ValueError 转 {"error": ...}
  5. supersede_unpicked（build_wave 选波权威化的存储层）：keep 不动、只动
     gem/pending/enhanced、alpha_id 非空不动、可与 upsert_expressions(commit=False)
     合成一个事务
"""
import importlib.util
import json
from pathlib import Path

import pytest

from wqb.store import CampaignStore
from wqb.store._expressions import STATUS_CHANGE_KEY, TERMINAL_STATUSES

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def store(tmp_path):
    db = CampaignStore(str(tmp_path / "status.db"))
    yield db
    db.close()


def _seed_wave(store, region="TST", wave="7"):
    """一波 4 行：pending×2（其一带 sim settings）、pending+alpha_id（已回测）、gem。"""
    store.upsert_expressions(region, wave, [
        {"expression": "rank(a)", "settings": {"decay": 4, "neutralization": "SUBINDUSTRY"}},
        {"expression": "rank(b)"},
        {"expression": "rank(c)", "alpha_id": "ABC123", "sharpe": 1.7},
        {"expression": "rank(d)", "status": "gem"},
    ], dataset="ds", status="pending")
    return {r["expression"]: r for r in store.list_expressions(region, wave)}


def _by_expr(store, region="TST", wave="7"):
    # status=None 时 list_expressions 默认排除 superseded/dropped，这里要看全貌
    cur = store.connection.cursor()
    cur.execute("SELECT * FROM expressions WHERE region=? AND wave=? ORDER BY id", (region, wave))
    return {r["expression"]: dict(r) for r in cur.fetchall()}


# ---------------------------------------------------------------------------
# 1. 过滤契约
# ---------------------------------------------------------------------------

def test_refuses_unfiltered_update(store):
    _seed_wave(store)
    with pytest.raises(ValueError):
        store.set_expression_status("TST", "7", "gated")
    with pytest.raises(ValueError):
        store.set_expression_status("TST", "7", "gated", ids=[])
    with pytest.raises(ValueError):
        store.set_expression_status("TST", "7", "", from_status="pending")
    # 拒绝 = 什么都没改
    assert {r["status"] for r in _by_expr(store).values()} == {"pending", "gem"}


def test_from_status_is_scoped_to_region_and_wave(store):
    _seed_wave(store)
    store.upsert_expressions("TST", "8", ["rank(z)"], status="pending")
    store.upsert_expressions("EUR", "7", ["rank(y)"], status="pending")

    out = store.set_expression_status("TST", "7", "gated", from_status="pending", reason="gate all_pass")
    assert out["n_updated"] == 2  # rank(a)、rank(b)；rank(c) 已回测受保护；rank(d) 是 gem
    assert out["n_protected"] == 1
    assert out["n_requested"] is None
    assert (out["region"], out["wave"], out["from_status"], out["to_status"]) == ("TST", "7", "pending", "gated")

    rows = _by_expr(store)
    assert rows["rank(a)"]["status"] == rows["rank(b)"]["status"] == "gated"
    assert rows["rank(c)"]["status"] == "pending"
    assert rows["rank(d)"]["status"] == "gem"
    # 其他波 / 其他区域纹丝不动
    assert _by_expr(store, "TST", "8")["rank(z)"]["status"] == "pending"
    assert _by_expr(store, "EUR", "7")["rank(y)"]["status"] == "pending"


def test_ids_and_from_status_intersect_and_ids_outside_wave_are_ignored(store):
    rows = _seed_wave(store)
    store.upsert_expressions("TST", "8", ["rank(z)"], status="pending")
    other = _by_expr(store, "TST", "8")["rank(z)"]["id"]

    # ids 含别波的 id + 本波 gem 行；from_status=pending 再收窄 → 只剩 rank(a)
    out = store.set_expression_status(
        "TST", "7", "dropped",
        ids=[rows["rank(a)"]["id"], rows["rank(d)"]["id"], other],
        from_status="pending",
    )
    assert out["n_updated"] == 1
    assert out["n_requested"] == 3  # 调用方据此发现有 id 未命中（越界 / 状态不符）
    after = _by_expr(store)
    assert after["rank(a)"]["status"] == "dropped"
    assert after["rank(d)"]["status"] == "gem"
    assert _by_expr(store, "TST", "8")["rank(z)"]["status"] == "pending"


# ---------------------------------------------------------------------------
# 2. 已回测行保护
# ---------------------------------------------------------------------------

def test_backtested_rows_protected_unless_terminal(store):
    rows = _seed_wave(store)
    cid = rows["rank(c)"]["id"]

    out = store.set_expression_status("TST", "7", "selected", ids=[cid])
    assert (out["n_updated"], out["n_protected"]) == (0, 1)
    assert _by_expr(store)["rank(c)"]["status"] == "pending"

    for terminal in TERMINAL_STATUSES:
        out = store.set_expression_status("TST", "7", terminal, ids=[cid], reason="archive")
        assert (out["n_updated"], out["n_protected"]) == (1, 0)
        assert _by_expr(store)["rank(c)"]["status"] == terminal
    # 归档不抹指标 / alpha_id
    assert _by_expr(store)["rank(c)"]["alpha_id"] == "ABC123"


# ---------------------------------------------------------------------------
# 3. settings_json 合并 + settings 视图去审计键
# ---------------------------------------------------------------------------

def test_reason_merges_into_settings_json_without_clobbering(store):
    _seed_wave(store)
    store.connection.execute("UPDATE expressions SET updated_at='2000-01-01T00:00:00'")
    store.connection.commit()

    store.set_expression_status("TST", "7", "gated", from_status="pending", reason="gate all_pass")

    raw = _by_expr(store)
    a = json.loads(raw["rank(a)"]["settings_json"])
    assert a["decay"] == 4 and a["neutralization"] == "SUBINDUSTRY"  # 既有键原样
    assert a[STATUS_CHANGE_KEY]["from"] == "pending"  # 记的是 UPDATE 前的旧值
    assert a[STATUS_CHANGE_KEY]["to"] == "gated"
    assert a[STATUS_CHANGE_KEY]["reason"] == "gate all_pass"
    assert a[STATUS_CHANGE_KEY]["at"] == raw["rank(a)"]["updated_at"]
    assert raw["rank(a)"]["updated_at"] != "2000-01-01T00:00:00"
    b = json.loads(raw["rank(b)"]["settings_json"])  # 原本 NULL → 从 {} 起步
    assert set(b) == {STATUS_CHANGE_KEY}
    # 未命中的行 settings_json/updated_at 不动
    assert raw["rank(d)"]["settings_json"] is None
    assert raw["rank(d)"]["updated_at"] == "2000-01-01T00:00:00"

    # list_expressions：settings 视图只剩回测设置，审计键提到行顶层
    view = {r["expression"]: r for r in store.list_expressions("TST", "7")}
    assert view["rank(a)"]["settings"] == {"decay": 4, "neutralization": "SUBINDUSTRY"}
    assert view["rank(a)"][STATUS_CHANGE_KEY]["reason"] == "gate all_pass"
    assert view["rank(b)"]["settings"] == {}
    assert STATUS_CHANGE_KEY not in (view["rank(d)"].get("settings") or {})


def test_reason_omitted_still_stamps_from_to_at(store):
    _seed_wave(store)
    store.set_expression_status("TST", "7", "gated", from_status="gem")
    sc = json.loads(_by_expr(store)["rank(d)"]["settings_json"])[STATUS_CHANGE_KEY]
    assert sc["from"] == "gem" and sc["to"] == "gated" and sc["reason"] is None and sc["at"]


def test_malformed_settings_json_does_not_break_the_update(store):
    rows = _seed_wave(store)
    store.connection.execute("UPDATE expressions SET settings_json='not json' WHERE id=?",
                             (rows["rank(b)"]["id"],))
    store.connection.execute("UPDATE expressions SET settings_json='[1,2]' WHERE id=?",
                             (rows["rank(a)"]["id"],))
    store.connection.commit()
    out = store.set_expression_status("TST", "7", "gated", from_status="pending", reason="r")
    assert out["n_updated"] == 2
    for e in ("rank(a)", "rank(b)"):
        assert json.loads(_by_expr(store)[e]["settings_json"])[STATUS_CHANGE_KEY]["to"] == "gated"


# ---------------------------------------------------------------------------
# 4. MCP 包装（wqb_db_mcp.py 注册 + 错误转 dict）
# ---------------------------------------------------------------------------

def _load_db_mcp(tmp_path):
    spec = importlib.util.spec_from_file_location("_wqb_db_mcp_status", str(REPO_ROOT / "wqb_db_mcp.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.DB_PATH = tmp_path / "mcp.db"  # _store() 每次读模块级 DB_PATH，绝不碰真库
    return mod


def test_mcp_tool_registered_and_wraps_value_error(tmp_path):
    import asyncio

    mod = _load_db_mcp(tmp_path)
    names = {t.name for t in asyncio.run(mod.mcp.list_tools())}
    assert "set_expression_status" in names

    mod.upsert_expressions("TST", "w9", ["rank(a)", "rank(b)"], dataset="ds", status="pending")
    err = mod.set_expression_status("TST", "w9", "gated")
    assert "error" in err and "ids" in err["error"]

    out = mod.set_expression_status("TST", "w9", "gated", from_status="pending", reason="via mcp")
    assert out["n_updated"] == 2 and out["to_status"] == "gated"
    rows = mod.list_expressions("TST", "w9")
    assert {r["status"] for r in rows} == {"gated"}
    assert all(r[STATUS_CHANGE_KEY]["reason"] == "via mcp" for r in rows)
    assert all(STATUS_CHANGE_KEY not in (r.get("settings") or {}) for r in rows)


# ---------------------------------------------------------------------------
# 5. supersede_unpicked（build_wave 选波权威化）
# ---------------------------------------------------------------------------

def _seed_selection_wave(store):
    store.upsert_expressions("TST", "w1", [
        {"expression": "ts_mean(close, 5)", "status": "gem"},         # picked
        {"expression": "ts_mean(close, 22)", "status": "pending"},    # picked
        {"expression": "ts_mean(close, 66)", "status": "enhanced"},   # → superseded
        {"expression": "ts_mean(close, 252)", "status": "gem"},       # → superseded
        {"expression": "ts_mean(close, 504)", "status": "gem", "alpha_id": "A1"},  # 已回测，不碰
        {"expression": "ts_mean(close, 1008)", "status": "dropped"},  # 纪律废弃，不碰
        {"expression": "ts_mean(close, 1260)", "status": "gated"},    # 闸门链上，不碰
        {"expression": "ts_mean(close, 120)", "status": "selected"},  # 旧选集，不碰
    ], dataset="ds1")
    store.upsert_expressions("TST", "w2", ["ts_mean(close, 5)"], dataset="ds1", status="gem")  # 别波


def test_supersede_unpicked_archives_only_waiting_rows(store):
    _seed_selection_wave(store)
    picked = ["ts_mean(close, 5)", "ts_mean(close, 22)"]
    store.upsert_expressions("TST", "w1", [{"expression": e, "status": "selected"} for e in picked],
                             dataset="ds1", status="selected")
    n = store.supersede_unpicked("TST", "w1", picked,
                                 reason="not picked by build_wave 2026-09-12T10:00:00")
    assert n == 2
    rows = _by_expr(store, "TST", "w1")
    assert rows["ts_mean(close, 5)"]["status"] == rows["ts_mean(close, 22)"]["status"] == "selected"
    for e in ("ts_mean(close, 66)", "ts_mean(close, 252)"):
        assert rows[e]["status"] == "superseded"
        sc = json.loads(rows[e]["settings_json"])[STATUS_CHANGE_KEY]
        assert sc["reason"].startswith("not picked by build_wave ") and sc["to"] == "superseded"
    assert rows["ts_mean(close, 504)"]["status"] == "gem"
    assert rows["ts_mean(close, 1008)"]["status"] == "dropped"
    assert rows["ts_mean(close, 1260)"]["status"] == "gated"
    assert rows["ts_mean(close, 120)"]["status"] == "selected"
    assert _by_expr(store, "TST", "w2")["ts_mean(close, 5)"]["status"] == "gem"
    # 幂等：再来一遍没有可归档的行
    assert store.supersede_unpicked("TST", "w1", picked) == 0


def test_supersede_unpicked_composes_one_transaction_with_upsert(store):
    _seed_selection_wave(store)
    picked = ["ts_mean(close, 5)", "ts_mean(close, 22)"]
    store.upsert_expressions("TST", "w1", [{"expression": e, "status": "selected"} for e in picked],
                             dataset="ds1", status="selected", commit=False)
    assert store.supersede_unpicked("TST", "w1", picked, commit=False) == 2
    store.connection.rollback()  # 两步同属一个事务：回滚后 selected 与 superseded 都不存在
    statuses = {e: r["status"] for e, r in _by_expr(store, "TST", "w1").items()}
    assert statuses["ts_mean(close, 5)"] == "gem" and statuses["ts_mean(close, 22)"] == "pending"
    assert statuses["ts_mean(close, 66)"] == "enhanced" and statuses["ts_mean(close, 252)"] == "gem"

    store.upsert_expressions("TST", "w1", [{"expression": e, "status": "selected"} for e in picked],
                             dataset="ds1", status="selected", commit=False)
    store.supersede_unpicked("TST", "w1", picked, commit=False)
    store.connection.commit()
    statuses = {e: r["status"] for e, r in _by_expr(store, "TST", "w1").items()}
    assert statuses["ts_mean(close, 5)"] == "selected" and statuses["ts_mean(close, 66)"] == "superseded"
