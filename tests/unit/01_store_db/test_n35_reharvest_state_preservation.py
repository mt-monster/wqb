# -*- coding: utf-8 -*-
"""N35（reports/ra_pipeline_stage_review_20260927.md §14.12.3）回归。

re-review / re-harvest 的回测行 upsert 不得清空已提交状态与实测相关性，
也不得把已提交 alpha 重新塞回 submit 队列。

根因：``CampaignStore.upsert_backtest_rows`` 与 ``upsert_alpha_from_platform`` 的
UPDATE 分支此前整行覆盖 ``alphas`` —— toolkit 复盘行（``metrics_cache.row_from_alpha``）
与 MCP 收批行（``harvest_multisim_results``）都不带 status / platform_status / stage /
date_submitted / prod / self，缺列被写成 NULL 或默认 ``UNSUBMITTED``，已提交 alpha
因此被打回，再被 ``enqueue_from_alphas`` 当未提交复活入队。
"""
import pytest

from wqb.store import CampaignStore
from wqb.store import submit_queue as sq


@pytest.fixture
def store(tmp_path, monkeypatch):
    # enqueue_from_alphas 内部按表达式反查数据集时可能回落默认库路径；
    # 固定到临时库，避免测试触碰仓库 data/wqb.db。
    path = str(tmp_path / "camp.db")
    monkeypatch.setenv("WQB_DB_PATH", path)
    db = CampaignStore(path)
    # enqueue_from_alphas 的 WHERE 依赖 alphas.soft_deleted / disposition。新库已在
    # ensure_schema 里补齐；此处用幂等 _add_column 兜底，使本回归在两种库版本下都能驱动步 4。
    db._add_column("alphas", "soft_deleted", "INTEGER DEFAULT 0")
    db._add_column("alphas", "disposition", "TEXT")
    db.connection.commit()
    yield db
    db.close()


def _alpha_state(store, aid):
    return store.connection.execute(
        "SELECT status, platform_status, date_submitted, stage, "
        "prod_correlation, self_correlation, prod_corr_source, sharpe "
        "FROM alphas WHERE alpha_id=?", (aid,)
    ).fetchone()


def test_reharvest_upsert_preserves_submission_state_and_correlations(store):
    """§14.12.3 复现步骤 1–4：re-review 后已提交状态/相关性存活，且不复活入队。"""
    # 步 1：toolkit 复盘行（只带 sharpe/fitness，无 status/平台态/相关性）建 A1
    store.upsert_expressions("USA", "w1", ["rank(x)"], dataset="ds")
    store.upsert_backtest_rows(
        "USA", "w1",
        [{"id": "A1", "code": "rank(x)", "sharpe": 2.0, "fitness": 1.3}],
        dataset="ds",
    )

    # 步 2：平台回写把 A1 标为已提交（走 upsert_alpha_from_platform 的 UPDATE 分支）
    store.upsert_alpha_from_platform({
        "alpha_id": "A1", "region": "USA", "expression": "rank(x)",
        "sharpe": 2.0, "fitness": 1.3,
        "status": "ACTIVE", "platform_status": "ACTIVE", "stage": "OS",
        "date_submitted": "2026-09-20T00:00:00",
        "prod_correlation": 0.55, "self_correlation": 0.31,
    })
    s2 = _alpha_state(store, "A1")
    assert (s2["status"], s2["platform_status"], s2["stage"]) == ("ACTIVE", "ACTIVE", "OS")
    assert s2["date_submitted"] == "2026-09-20T00:00:00"
    assert s2["prod_correlation"] == pytest.approx(0.55)
    assert s2["self_correlation"] == pytest.approx(0.31)
    assert s2["prod_corr_source"] == "platform_sync"   # 平台相关性溯源一致

    # 步 3：再次 upsert 同一条 toolkit 复盘行（含空 failed_checks，模拟复盘刷新）
    store.upsert_backtest_rows(
        "USA", "w1",
        [{"id": "A1", "code": "rank(x)", "sharpe": 2.4, "fitness": 1.5, "failed_checks": []}],
        dataset="ds",
    )
    s3 = _alpha_state(store, "A1")
    # 已提交状态与实测相关性存活（旧实现此处全被打回 UNSUBMITTED / NULL）
    assert (s3["status"], s3["platform_status"], s3["stage"]) == ("ACTIVE", "ACTIVE", "OS")
    assert s3["date_submitted"] == "2026-09-20T00:00:00"
    assert s3["prod_correlation"] == pytest.approx(0.55)
    assert s3["self_correlation"] == pytest.approx(0.31)
    assert s3["prod_corr_source"] == "platform_sync"
    # 回测行确实携带的指标仍照常刷新
    assert s3["sharpe"] == pytest.approx(2.4)

    # 对照组：一条真正未提交、达标的 alpha 仍应能正常入队（证明 enqueue 通路有效）
    store.upsert_backtest_rows(
        "USA", "w1",
        [{"id": "A2", "code": "rank(y)", "sharpe": 2.0, "fitness": 1.3}],
        dataset="ds",
    )

    # 步 4：离线批量入队。已提交的 A1 不得复活入队；未提交的 A2 应入队。
    sq.enqueue_from_alphas(region="USA", db_path=store.path, dedup=False)
    ready = {r["alpha_id"]: r["status"]
             for r in sq.list_ready(region="USA", db_path=store.path, all_status=True)}
    assert "A1" not in ready              # 已提交 —— 绝不重新入队（N35 核心）
    assert ready.get("A2") == sq.STATUS_READY


def test_backtest_upsert_does_not_downgrade_submitted_via_complete_row(store):
    """harvest 收批行携带 status='COMPLETE'；对已提交（platform_status=ACTIVE）的 alpha
    不得覆盖平台态/日期/相关性（本地 status 也不因回测行回退）。"""
    store.upsert_expressions("USA", "w2", ["rank(z)"], dataset="ds")
    store.upsert_backtest_rows(
        "USA", "w2", [{"id": "B1", "code": "rank(z)", "sharpe": 1.9, "fitness": 1.2}],
        dataset="ds",
    )
    # 平台同步口径：本地 status='COMPLETE' + platform_status='ACTIVE'（见 tools/sync_platform_alphas）
    store.upsert_alpha_from_platform({
        "alpha_id": "B1", "region": "USA", "expression": "rank(z)",
        "status": "COMPLETE", "platform_status": "ACTIVE", "stage": "OS",
        "date_submitted": "2026-09-15T00:00:00",
        "prod_correlation": 0.60, "self_correlation": 0.20,
    })
    # 再收批：harvest 行携带 status='COMPLETE'，但不带平台态/相关性
    store.upsert_backtest_rows(
        "USA", "w2",
        [{"id": "B1", "code": "rank(z)", "status": "COMPLETE",
          "sharpe": 1.95, "fitness": 1.25}],
        dataset="ds",
    )
    s = _alpha_state(store, "B1")
    assert s["platform_status"] == "ACTIVE"
    assert s["date_submitted"] == "2026-09-15T00:00:00"
    assert s["prod_correlation"] == pytest.approx(0.60)
    assert s["self_correlation"] == pytest.approx(0.20)
    assert s["sharpe"] == pytest.approx(1.95)   # 指标刷新
