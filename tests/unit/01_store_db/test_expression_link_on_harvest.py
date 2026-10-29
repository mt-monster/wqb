# -*- coding: utf-8 -*-
"""expressions 行在收批时的 alpha_id / status 回填（2026-10-29 修）。

根因：``CampaignStore.upsert_backtest_rows`` 只在「表达式行不存在」时才顺手写入
alpha_id；主链路是 ``upsert_expressions`` 先预登记（alpha_id=NULL, status=pending），
再 dispatch → harvest。此时 ``UPDATE expressions ... WHERE alpha_id=?`` 匹配 0 行，
expressions.alpha_id/status 永久停在 null/pending。

实测口径（DEU，2026-10-29）：backtest_results 与 expressions 可 join 的 3002 行里，
194 行属于这种形态（含当日 news104/news17 三波 14 条）。

两条不变量：
1. 回填 alpha_id 且 status 从「运行前态」推进到 backtested；
2. 终态（dropped / superseded / submitted）不因再次收批而回落。
"""
import pytest

from wqb.store import CampaignStore


@pytest.fixture
def store(tmp_path, monkeypatch):
    path = str(tmp_path / "camp.db")
    monkeypatch.setenv("WQB_DB_PATH", path)
    db = CampaignStore(path)
    yield db
    db.close()


def _expr_row(store, wave, expression):
    return store.connection.execute(
        "SELECT alpha_id, status, sharpe, fitness, turnover, margin "
        "FROM expressions WHERE wave=? AND expression=?",
        (wave, expression),
    ).fetchone()


def test_preregistered_expression_gets_linked_and_marked_backtested(store):
    store.upsert_expressions("DEU", "w1", ["rank(a)"], dataset="ds", status="pending")
    assert _expr_row(store, "w1", "rank(a)")[0] is None

    store.upsert_backtest_rows(
        "DEU", "w1",
        [{"id": "A1", "code": "rank(a)", "sharpe": 1.57, "fitness": 1.33,
          "turnover": 0.0333, "margin": 0.005376}],
        dataset="ds",
    )

    alpha_id, status, sharpe, fitness, turnover, margin = _expr_row(store, "w1", "rank(a)")
    assert alpha_id == "A1"
    assert status == "backtested"
    assert (sharpe, fitness) == (1.57, 1.33)
    assert turnover == pytest.approx(0.0333)
    assert margin == pytest.approx(0.005376)


@pytest.mark.parametrize("terminal", ["dropped", "superseded"])
def test_terminal_status_not_regressed_by_reharvest(store, terminal):
    store.upsert_expressions("DEU", "w1", ["rank(a)"], dataset="ds", status="pending")
    store.set_expression_status("DEU", "w1", terminal, from_status="pending")
    assert _expr_row(store, "w1", "rank(a)")[1] == terminal

    store.upsert_backtest_rows(
        "DEU", "w1",
        [{"id": "A1", "code": "rank(a)", "sharpe": 1.2}],
        dataset="ds",
    )

    alpha_id, status, *_ = _expr_row(store, "w1", "rank(a)")
    # alpha_id 仍应补上（幂等 COALESCE），但纪律终态不许被写成 backtested
    assert alpha_id == "A1"
    assert status == terminal


def test_selected_status_advances_to_backtested(store):
    store.upsert_expressions("DEU", "w1", ["rank(a)"], dataset="ds", status="selected")
    store.upsert_backtest_rows(
        "DEU", "w1", [{"id": "A1", "code": "rank(a)", "sharpe": 0.9}], dataset="ds",
    )
    assert _expr_row(store, "w1", "rank(a)")[1] == "backtested"
