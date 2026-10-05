# -*- coding: utf-8 -*-
"""步3 断流修复 · 止血 A：字段池消费 `s1_semantic_<ds>` 的回归护栏（2026-10-01）。

契约：`build_economic_field_pool` / `build_candidate_field_pool` 在建池前，按
ledger `s1_semantic_<ds>` 的 `blocked_fields` 剔除非信号字段（货币代码 / 汇率叉乘 /
标识符 / 分类码 / 日期口径），并在 payload 带 `semantic_filter` 元数据。

起因（实测）：`s2_field_pool_insiders1` 的池里含 `transaction_currency_code`——
语义黑名单字段进了 GEM 绑定池。语义归类此前只被步 5 闸 SEM 消费、生成侧完全不读。

**fail-open 是契约的一部分**：台账缺失 / 解析失败 / 无 blocked_fields → 原样返回，
不阻断生成（过滤是减负，不是新的把关点；把关在步 5 闸 SEM）。
"""
import importlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
for _p in (REPO, REPO / "src", REPO / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402


def _seed(tmp_path, *, semantic=None, fields=None):
    db_path = tmp_path / "wqb.db"
    store = CampaignStore(str(db_path))
    store.close()
    conn = sqlite3.connect(str(db_path))
    ds = "tstd1"
    conn.execute("INSERT OR IGNORE INTO regions (name) VALUES ('TST')")
    rid = conn.execute("SELECT id FROM regions WHERE name='TST'").fetchone()[0]
    conn.execute("INSERT INTO datasets (name, region_id) VALUES (?,?)", (ds, rid))
    did = conn.execute("SELECT id FROM datasets WHERE name=?", (ds,)).fetchone()[0]
    conn.execute(
        "INSERT INTO ledger_kv (region, key, value, updated_at) VALUES ('TST', ?, ?, '2026-10-01')",
        (f"catalog_{ds}", json.dumps({
            "region": "TST", "dataset": ds, "field_count": len(fields),
            "fields": [{"id": f, "type": "MATRIX", "coverage": 0.9,
                        "userCount": 0, "alphaCount": 1, "description": ""} for f in fields],
        })))
    for f in fields:
        conn.execute(
            "INSERT INTO fields (dataset_id, field_name, field_type, coverage, user_count, alpha_count, description) "
            "VALUES (?,?,?,?,?,?,?)", (did, f, "MATRIX", 0.9, 0, 1, ""))
    if semantic is not None:
        conn.execute(
            "INSERT INTO ledger_kv (region, key, value, updated_at) VALUES ('TST', ?, ?, '2026-10-01')",
            (f"s1_semantic_{ds}", json.dumps(semantic)))
    conn.commit()
    conn.close()
    return str(db_path), ds


def _sem(*blocked):
    total = len(blocked or [])
    return {"region": "TST", "total_fields": total,
            "blocked_fields": [{"field": b, "reason": "非信号"} for b in blocked]}


def test_blocked_fields_are_dropped_from_economic_pool(tmp_path):
    """核心：语义黑名单字段不得进池（IND insiders1 的 transaction_currency_code 类）。"""
    fields = ["good_alpha_1", "transaction_currency_code", "good_alpha_2", "usd_to_rep_exrate"]
    db, ds = _seed(tmp_path, semantic=_sem("transaction_currency_code", "usd_to_rep_exrate"),
                   fields=fields)
    store = CampaignStore(db)
    try:
        payload = store.build_economic_field_pool("TST", ds, persist=False)
        pool = payload["candidate_field_pool"]
        assert "transaction_currency_code" not in pool
        assert "usd_to_rep_exrate" not in pool
        assert payload["semantic_filter"]["ledger"] is True
        assert payload["semantic_filter"]["blocked_n"] == 2
        assert payload["semantic_filter"]["dropped_n"] == 2
    finally:
        store.close()


def test_fallback_pool_also_filters(tmp_path):
    """回退路径 build_candidate_field_pool 必须同口径——否则经济学池不可用时过滤被绕过。"""
    fields = ["good_alpha_1", "transaction_currency_code", "good_alpha_2"]
    db, ds = _seed(tmp_path, semantic=_sem("transaction_currency_code"), fields=fields)
    store = CampaignStore(db)
    try:
        payload = store.build_candidate_field_pool("TST", ds, persist=False)
        assert "transaction_currency_code" not in payload["candidate_field_pool"]
        assert payload["semantic_filter"]["dropped_n"] == 1
    finally:
        store.close()


def test_missing_ledger_is_fail_open(tmp_path):
    """缺台账 → 不剔除、不阻断，池照建（fail-open 契约）。"""
    fields = ["good_alpha_1", "transaction_currency_code", "good_alpha_2"]
    db, ds = _seed(tmp_path, semantic=None, fields=fields)
    store = CampaignStore(db)
    try:
        payload = store.build_economic_field_pool("TST", ds, persist=False)
        pool = payload["candidate_field_pool"]
        assert payload["semantic_filter"]["ledger"] is False
        assert len(pool) == len(fields)          # 一个都没剔
        assert pool                              # 池非空，生成不被阻断
    finally:
        store.close()


def test_empty_blocked_list_is_fail_open(tmp_path):
    """台账在但 blocked_fields 为空（如 KOR/model109、other466）→ 同全量。"""
    fields = ["good_alpha_1", "good_alpha_2"]
    db, ds = _seed(tmp_path, semantic=_sem(), fields=fields)
    store = CampaignStore(db)
    try:
        payload = store.build_economic_field_pool("TST", ds, persist=False)
        assert payload["semantic_filter"]["ledger"] is True
        assert payload["semantic_filter"]["dropped_n"] == 0
        assert len(payload["candidate_field_pool"]) == 2
    finally:
        store.close()


def test_corrupt_ledger_is_fail_open(tmp_path):
    """台账 JSON 损坏 → 不抛异常、不阻断。"""
    fields = ["good_alpha_1", "good_alpha_2"]
    db, ds = _seed(tmp_path, fields=fields)
    conn = sqlite3.connect(db)
    conn.execute("INSERT INTO ledger_kv (region,key,value,updated_at) VALUES ('TST',?,?, '2026-10-01')",
                 (f"s1_semantic_{ds}", "{not valid json"))
    conn.commit()
    conn.close()
    store = CampaignStore(db)
    try:
        payload = store.build_economic_field_pool("TST", ds, persist=False)
        assert payload["semantic_filter"]["ledger"] is False
        assert len(payload["candidate_field_pool"]) == 2
    finally:
        store.close()


def test_filter_helper_is_reportable(tmp_path):
    """_drop_semantic_blocked 直接调用的契约（供节点/诊断复用）。"""
    fields = ["a_good", "bad_code", "b_good"]
    db, ds = _seed(tmp_path, semantic=_sem("bad_code"), fields=fields)
    store = CampaignStore(db)
    try:
        kept, meta = store._drop_semantic_blocked("TST", ds, [{"id": f} for f in fields])
        assert [store._field_name(f) for f in kept] == ["a_good", "b_good"]
        assert meta["dropped"] == ["bad_code"]
        assert meta["blocked_n"] == 1
    finally:
        store.close()


def test_stale_pool_is_invalidated_by_version_bump(tmp_path):
    """★ 版本护栏：语义过滤是**内容**变化，旧池（含非信号字段）必须被判过期。

    实测 IND/insiders1 的 v3 旧池含 transaction_currency_code / insd1_gvkey。
    若未来再改过滤逻辑却忘升 POOL_BUILDER_VERSION，已落库旧池会继续被 GEM 消费，
    过滤形同虚设——本测把「过滤生效必须伴随版本递增」钉死。
    """
    from wqb.store._field_catalog import POOL_BUILDER_VERSION
    assert POOL_BUILDER_VERSION >= 4, "语义过滤落地后必须 >=4（v3 旧池含非信号字段）"
    fields = ["a_good", "b_good"]
    db, ds = _seed(tmp_path, semantic=_sem(), fields=fields)
    conn = sqlite3.connect(db)
    conn.execute("INSERT INTO ledger_kv (region,key,value,updated_at) VALUES ('TST',?,?, '2026-10-01')",
                 (f"s2_field_pool_{ds}", json.dumps(
                     {"candidate_field_pool": ["a_good", "transaction_currency_code"],
                      "builder_version": 3})))
    conn.commit()
    conn.close()
    store = CampaignStore(db)
    try:
        assert store.get_candidate_field_pool("TST", ds) is None, "v3 旧池必须判过期"
    finally:
        store.close()
