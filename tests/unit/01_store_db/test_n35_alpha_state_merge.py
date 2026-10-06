# -*- coding: utf-8 -*-
"""N35（2026-09-28）：同一 alpha 再次入库时，alphas / backtest_results 按合并写，不清空、不回退。

此前 `CampaignStore.upsert_backtest_rows` 同步 alphas 时每一列都取行里的值：行里没带就写 NULL 或缺省值。
toolkit 评审行从不带 status / platform_status / date_submitted / 相关性，于是一次重评审就把已提交的
alpha 改回 UNSUBMITTED、清空提交时间与相关性，提交队列随后把它放回 READY。
`upsert_alpha_from_platform`（tools/sync_platform_alphas 的写入口）同样整行覆盖：sync 传
two_year_sharpe=None，本地回测写进来的 2Y 被清掉；字段投票失败时数据集被改回 _unknown。
backtest_results 的 ON CONFLICT 也把行里没带的指标（returns / drawdown / 多空数……）清成 NULL。
"""
import asyncio
import importlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT, REPO_ROOT / "src", REPO_ROOT / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402
from wqb.store.submit_queue import enqueue_from_alphas  # noqa: E402

FIXTURE = REPO_ROOT / "tests" / "fixtures" / "alpha_detail_cluster_sample.json"
SUBMITTED = {"platform_status": "ACTIVE", "stage": "OS", "date_submitted": "2026-09-20T09:30:00-04:00"}

#: toolkit 评审行（metrics_cache.row_from_alpha 的形态）：只有 IS 指标与 failed_checks
REVIEW_ROW = {"id": "A1", "code": "rank(ts_delta(x, 5))", "neut": "SUBINDUSTRY", "sharpe": 2.01, "fitness": 1.31,
              "two_year_sharpe": 1.9, "margin_bp": 12.3, "turnover_pct": 11.0, "failed_checks": []}
#: 收批行（wqb-db harvest_multisim_results 的形态）：带全指标
HARVEST_ROW = {"alpha_id": "A1", "code": "rank(ts_delta(x, 5))", "status": "COMPLETE", "sharpe": 2.0,
               "fitness": 1.3, "turnover": 0.11, "margin": 0.00123, "returns": 0.21, "drawdown": 0.04,
               "long_count": 310, "short_count": 290, "pnl": 1.2e6, "book_size": 2e7,
               "risk_neutralized_sharpe": 1.4, "universe": "TOP3000", "delay": 1, "neut": "SUBINDUSTRY",
               "failed_checks": [], "ra_failed_checks": []}


@pytest.fixture
def store(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    yield st
    st.close()


def _alpha(store, aid="A1"):
    row = store.connection.execute(
        "SELECT a.*, d.name AS dataset FROM alphas a LEFT JOIN datasets d ON d.id=a.dataset_id "
        "WHERE a.alpha_id=?", (aid,)).fetchone()
    return dict(row) if row else None


def _bt(store, aid="A1"):
    return dict(store.connection.execute("SELECT * FROM backtest_results WHERE alpha_id=?", (aid,)).fetchone())


def _submitted(store, aid="A1", region="USA", **extra):
    store.upsert_alpha_from_platform({"alpha_id": aid, "region": region, "expression": "rank(ts_delta(x, 5))",
                                      "status": "ACTIVE", "prod_correlation": 0.55, "self_correlation": 0.31,
                                      **SUBMITTED, **extra})


# ---------------------------------------------------------------- 复现（报告 §14.12.3 N35）

def test_rereview_keeps_submission_state_correlation_and_dataset(store):
    store.upsert_backtest_rows("USA", "w1", [HARVEST_ROW], dataset="dsA")
    _submitted(store)
    before = _alpha(store)
    assert (before["status"], before["platform_status"], before["prod_corr_source"]) == ("ACTIVE", "ACTIVE",
                                                                                          "platform_sync")
    store.upsert_backtest_rows("USA", "w1", [REVIEW_ROW])                 # toolkit 重评审，没点名数据集
    a = _alpha(store)
    for col in ("status", "platform_status", "date_submitted", "stage", "prod_correlation", "self_correlation",
                "prod_corr_source", "corr_checked_at", "returns", "drawdown", "long_count", "short_count"):
        assert a[col] == before[col], col                                 # 此前：UNSUBMITTED / 全部 NULL
    assert a["dataset"] == "dsA"                                          # 此前：_unknown
    assert (a["sharpe"], a["fitness"], a["two_year_sharpe"]) == (2.01, 1.31, 1.9)   # 行里带了的照常更新
    assert a["margin"] == pytest.approx(0.00123) and a["turnover"] == pytest.approx(0.11)


def test_rereview_does_not_put_a_submitted_alpha_back_in_the_queue(store, tmp_path):
    store.upsert_backtest_rows("USA", "w1", [HARVEST_ROW], dataset="dsA")
    _submitted(store)
    store.upsert_backtest_rows("USA", "w1", [REVIEW_ROW])
    # 提交队列的入队查询要 soft_deleted / disposition（N33 起 CampaignStore 建表已自带两列；
    # 对更老结构的库保留防御性补列，故按 PRAGMA 判存再 ALTER——N33 合入后无条件 ALTER 会 duplicate column）
    _cols = {r[1] for r in store.connection.execute("PRAGMA table_info(alphas)").fetchall()}
    if "soft_deleted" not in _cols:
        store.connection.execute("ALTER TABLE alphas ADD COLUMN soft_deleted INTEGER DEFAULT 0")
    if "disposition" not in _cols:
        store.connection.execute("ALTER TABLE alphas ADD COLUMN disposition TEXT")
    store.connection.commit()
    enqueue_from_alphas(db_path=str(tmp_path / "wqb.db"), dedup=False)
    got = store.connection.execute("SELECT alpha_id, gate, status FROM submit_ready").fetchall()
    assert [tuple(r) for r in got] == []                                  # 此前：('A1', 'IS_ONLY', 'READY')


# ---------------------------------------------------------------- 规则

def test_lifecycle_moves_forward_but_never_back(store):
    store.upsert_backtest_rows("USA", "w1", [{**HARVEST_ROW, "platform_status": "UNSUBMITTED", "stage": "IS"}])
    a = _alpha(store)
    assert (a["status"], a["platform_status"], a["stage"], a["date_submitted"]) == ("COMPLETE", "UNSUBMITTED",
                                                                                    "IS", None)
    store.upsert_backtest_rows("USA", "w1", [{**HARVEST_ROW, **SUBMITTED, "status": "ACTIVE"}])   # 平台说已提交
    a = _alpha(store)
    assert (a["status"], a["platform_status"], a["stage"]) == ("ACTIVE", "ACTIVE", "OS")
    assert a["date_submitted"] == SUBMITTED["date_submitted"]
    # 旧的收批结果重放：未提交类的值不把它改回去
    store.upsert_backtest_rows("USA", "w1", [{**HARVEST_ROW, "platform_status": "UNSUBMITTED", "stage": "IS"}])
    a = _alpha(store)
    assert (a["status"], a["platform_status"], a["stage"]) == ("ACTIVE", "ACTIVE", "OS")
    # 已提交态之间照常变化
    store.upsert_alpha_from_platform({"alpha_id": "A1", "region": "USA", "platform_status": "DECOMMISSIONED"})
    assert _alpha(store)["platform_status"] == "DECOMMISSIONED"


def test_dataset_attribution_changes_only_when_named(store):
    store.upsert_backtest_rows("USA", "w1", [HARVEST_ROW], dataset="dsA")
    store.upsert_backtest_rows("USA", "w1", [REVIEW_ROW])                 # 没点名
    assert _alpha(store)["dataset"] == "dsA" and _bt(store)["dataset"] == "dsA"
    store.upsert_backtest_rows("USA", "w2", [REVIEW_ROW], dataset="_unknown")
    assert _alpha(store)["dataset"] == "dsA"
    store.upsert_backtest_rows("USA", "w3", [REVIEW_ROW], dataset="dsB")  # 点名了就改
    assert _alpha(store)["dataset"] == "dsB" and _bt(store)["dataset"] == "dsB"
    # 平台同步按字段投票推断数据集：推断只补 _unknown，不改已有归属
    ds_c = store._ensure_dataset("USA", "dsC")
    store.connection.execute("INSERT INTO fields (dataset_id, field_name) VALUES (?, 'close_ratio_x')", (ds_c,))
    store.connection.commit()
    store.upsert_alpha_from_platform({"alpha_id": "A1", "region": "USA", "expression": "rank(close_ratio_x)"})
    assert _alpha(store)["dataset"] == "dsB"
    store.upsert_alpha_from_platform({"alpha_id": "B1", "region": "USA", "expression": "rank(ts_mean(y, 22))"})
    assert _alpha(store, "B1")["dataset"] == "_unknown"                   # 新行：推断不出归 _unknown（同此前）
    store.upsert_alpha_from_platform({"alpha_id": "B1", "region": "USA", "expression": "rank(close_ratio_x)"})
    assert _alpha(store, "B1")["dataset"] == "dsC"                        # 原来没有归属：推断补上


def test_correlation_is_written_with_provenance_and_never_wiped(store):
    store.upsert_backtest_rows("USA", "w1", [{**HARVEST_ROW, "prod_correlation": 0.62}])
    a = _alpha(store)
    assert (a["prod_correlation"], a["self_correlation"], a["prod_corr_source"]) == (0.62, None, "platform_sync")
    assert a["corr_checked_at"] is not None                               # 此前：来源与时间都不记
    store.upsert_backtest_rows("USA", "w1", [REVIEW_ROW])
    assert (_alpha(store)["prod_correlation"], _alpha(store)["prod_corr_source"]) == (0.62, "platform_sync")
    store.persist_correlation("A1", prod=0.71, self_=0.4, source="triage_local", overwrite=True)
    store.upsert_backtest_rows("USA", "w1", [{**REVIEW_ROW, "prod_correlation": 1.7}])   # 越界值不算数
    a = _alpha(store)
    assert (a["prod_correlation"], a["self_correlation"], a["prod_corr_source"]) == (0.71, 0.4, "triage_local")
    store.upsert_backtest_rows("USA", "w1", [{**REVIEW_ROW, "self_corr": 0.0}])          # 0.0 是真值
    a = _alpha(store)
    assert (a["prod_correlation"], a["self_correlation"], a["prod_corr_source"]) == (0.71, 0.0, "platform_sync")


def test_platform_sync_payload_keeps_local_backtest_values(store):
    """tools/sync_platform_alphas.to_store_payload 的真实转换：status=COMPLETE，2Y/sub 从 is.checks[] 抽。

    2026-10-06：此前 `to_store_payload` 把 two_year_sharpe 硬编码 None（假设"平台 is 段无此字段"），
    与平台实证相反——真值就藏在 `is.checks[LOW_2Y_SHARPE/LOW_SUB_UNIVERSE_SHARPE].value` 里
    （见 `backfill_alpha_metrics_from_platform.extract_is_metrics`）。断言随之更新为「抽得到」。
    """
    from sync_platform_alphas import to_store_payload

    raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
    raw.update(status="ACTIVE", stage="OS", dateSubmitted=SUBMITTED["date_submitted"],
               regular={"code": "rank(ts_delta(x, 5))"})
    raw["is"].update(prodCorrelation=0.48, selfCorrelation=0.22)
    payload = to_store_payload(raw)
    payload.pop("os_data")
    # 2026-10-06：2Y/sub 不再被硬编码丢弃，而是从 is.checks[] 抽出（fixture 里为 3.59 / 1.88）
    assert payload["two_year_sharpe"] == 3.59 and payload["status"] == "COMPLETE"
    assert payload["sub_universe_sharpe"] == 1.88 and payload["is_ladder_sharpe"] is None
    aid, region = payload["alpha_id"], payload["region"]
    store.upsert_backtest_rows(region, "w1", [{**HARVEST_ROW, "alpha_id": aid, "two_year_sharpe": 3.59}],
                               dataset="dsA")
    store.upsert_alpha_from_platform(payload)
    a = _alpha(store, aid)
    assert a["two_year_sharpe"] == 3.59 and a["dataset"] == "dsA"         # 此前：NULL、_unknown
    assert (a["platform_status"], a["stage"], a["date_submitted"]) == ("ACTIVE", "OS", SUBMITTED["date_submitted"])
    assert (a["prod_correlation"], a["self_correlation"], a["prod_corr_source"]) == (0.48, 0.22, "platform_sync")
    assert (a["sharpe"], a["fitness"]) == (3.67, 2.96)                    # 平台给了的照常写
    assert (a["returns"], a["long_count"]) == (0.21, 310)                 # 平台没给的保留


def test_backtest_row_keeps_known_metrics_and_updates_ra_only_when_known(store):
    store.upsert_backtest_rows("USA", "w1", [{**HARVEST_ROW, "ra_failed_checks": ["LOW_2Y_SHARPE"]}], dataset="dsA")
    store.upsert_backtest_rows("USA", "w1", [REVIEW_ROW])                 # failed_checks=[] → 这一行说得清：RA 全过
    b = _bt(store)
    assert (b["returns"], b["drawdown"], b["long_count"], b["short_count"], b["pnl"], b["book_size"],
            b["risk_neutralized_sharpe"]) == (0.21, 0.04, 310, 290, 1.2e6, 2e7, 1.4)   # 此前：全部 NULL
    assert (b["sharpe"], b["two_year_sharpe"]) == (2.01, 1.9)
    assert b["ra_failed_checks"] is None                                  # 已知全过：旧名单清掉
    assert "returns" not in json.loads(b["payload_json"])                 # payload 仍是最近一次入库的原始行
    store.upsert_backtest_rows("USA", "w1", [{**REVIEW_ROW, "failed_checks": ["LOW_SHARPE"]}])
    assert _bt(store)["ra_failed_checks"] == '["LOW_SHARPE"]'
    unknown = {k: v for k, v in REVIEW_ROW.items() if k != "failed_checks"}
    store.upsert_backtest_rows("USA", "w1", [unknown])                    # 说不清 RA → 不动
    assert _bt(store)["ra_failed_checks"] == '["LOW_SHARPE"]'


def test_new_rows_keep_their_defaults(store):
    store.upsert_backtest_rows("USA", "w1", [REVIEW_ROW])
    a = _alpha(store)
    assert (a["status"], a["platform_status"], a["dataset"], a["prod_corr_source"]) == ("UNSUBMITTED", None,
                                                                                        "_unknown", None)
    store.upsert_alpha_from_platform({"alpha_id": "P1", "region": "USA"})
    p = _alpha(store, "P1")
    assert (p["status"], p["expression"], p["dataset"]) == ("UNSUBMITTED", "", "_unknown")


# ---------------------------------------------------------------- SOP 步 6 的收批入口（经 MCP）

def test_mcp_reharvest_of_a_submitted_alpha_keeps_it_submitted(tmp_path, monkeypatch):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()
    monkeypatch.setenv("WQB_DB_PATH", str(path))
    cdir = tmp_path / "tracking" / "IND"
    (cdir / "config").mkdir(parents=True)
    monkeypatch.setenv("WQB_CAMPAIGN_DIR", str(cdir))
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    mod.set_db_path(path)
    raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
    raw.update(id="S1", status="ACTIVE", regular={"code": "rank(ts_delta(x, 5))"})
    st = CampaignStore(str(path))
    try:
        st.upsert_backtest_rows("IND", "w1", [{**HARVEST_ROW, "alpha_id": "S1"}], dataset="dsA")
        _submitted(st, "S1", region="IND")
    finally:
        st.close()
    out = asyncio.run(mod.mcp.call_tool("harvest_multisim_results", {"region": "IND", "wave": "w1", "alphas": [raw]}))
    out = out[1] if isinstance(out, tuple) else out
    assert (out.get("result", out) if isinstance(out, dict) else json.loads(out[0].text))["upserted"] == 1
    conn = sqlite3.connect(str(path))
    try:
        got = conn.execute("SELECT a.status, a.platform_status, a.date_submitted, a.prod_correlation, d.name "
                           "FROM alphas a JOIN datasets d ON d.id=a.dataset_id WHERE a.alpha_id='S1'").fetchone()
    finally:
        conn.close()
    assert got == ("ACTIVE", "ACTIVE", SUBMITTED["date_submitted"], 0.55, "dsA")
