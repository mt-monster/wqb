"""Unit tests for wqb.store.CampaignStore — campaign artifact DB writes."""

import pytest

from wqb.store import CampaignStore


@pytest.fixture
def store(tmp_path):
    db = CampaignStore(str(tmp_path / "camp.db"))
    yield db
    db.close()


def test_upsert_expressions_roundtrip(store):
    out = store.upsert_expressions(
        "EUR", "39", ["rank(close)", "rank(volume)"],
        dataset="multi_horizon_alpha", status="gem",
    )
    assert out["n"] == 2
    rows = store.list_expressions("EUR", "39", dataset="multi_horizon_alpha")
    assert [r["expression"] for r in rows] == ["rank(close)", "rank(volume)"]
    assert rows[0]["status"] == "gem"


def test_upsert_expressions_idempotent(store):
    store.upsert_expressions("EUR", "1", ["rank(a)"], status="pending")
    store.upsert_expressions("EUR", "1", [{"expression": "rank(a)", "status": "selected"}])
    rows = store.list_expressions("EUR", "1")
    assert len(rows) == 1
    assert rows[0]["status"] == "selected"


def test_upsert_expressions_denormalized_dataset_is_the_dataset_not_the_region(store):
    """2026-09-15 回归：派生 dataset 列曾恒等于区域名。

    upsert 里的 SELECT 同时选出 r.name 与 d.name 两个都叫 name 的列，sqlite3.Row["name"]
    取第一个 → resolved_dataset = 区域名。实测全库 13 847 行有 7 418 行 dataset==region
    （GBR wave57 写成 'GBR'，waves 表却是 pv47）；list_expressions(dataset=…) 全靠
    "旧行回退"分支才查得到，按 dataset 过滤的任何写路径都会静默漏行。
    """
    store.upsert_expressions("GBR", "57", ["rank(a)"], dataset="pv47", status="pending")
    cur = store.connection.cursor()
    cur.execute("SELECT region, wave, dataset FROM expressions WHERE region='GBR'")
    assert tuple(cur.fetchone()) == ("GBR", "57", "pv47")
    # 精确 dataset 过滤直接命中（不再依赖回退分支）
    rows = store.list_expressions("GBR", "57", dataset="pv47")
    assert [r["expression"] for r in rows] == ["rank(a)"] and rows[0]["dataset"] == "pv47"


def test_field_catalog_roundtrip(store):
    cat = {
        "dataset": "model238",
        "region": "EUR",
        "universe": "TOP2500",
        "delay": 1,
        "data_type": "MATRIX",
        "field_count": 2,
        "fields": [
            {"id": "mdl238_a", "type": "MATRIX", "coverage": 0.9, "userCount": 1, "alphaCount": 3},
            {"id": "mdl238_b", "type": "VECTOR", "coverage": 0.8, "userCount": 0, "alphaCount": 0},
        ],
    }
    store.upsert_field_catalog("EUR", cat)
    got = store.get_field_catalog("EUR", "model238")
    assert got["data_type"] == "MATRIX"
    ids = {f["id"] for f in got["fields"]}
    assert ids == {"mdl238_a", "mdl238_b"}


def test_field_prefix_clusters_roundtrip(store):
    cat = {
        "dataset": "analyst45",
        "region": "IND",
        "data_type": "MATRIX",
        "fields": [
            {"id": "anl_est_eps", "type": "MATRIX", "coverage": 0.91},
            {"id": "anl_rev_fy1", "type": "MATRIX", "coverage": 0.88},
            {"id": "news_sent_score", "type": "VECTOR", "coverage": 0.42},
            {"id": "pv_close", "type": "MATRIX", "coverage": 0.97},
        ],
    }
    store.upsert_field_catalog("IND", cat)

    built = store.build_field_prefix_clusters("IND", "analyst45", prefix_depth=1, top_n=3)
    assert built["total_fields"] == 4
    assert built["total_clusters"] == 3
    assert built["top_clusters"][0]["prefix"] == "anl"
    assert built["top_clusters"][0]["count"] == 2
    assert built["top_clusters"][0]["sample_fields"] == ["anl_est_eps", "anl_rev_fy1"]
    assert any(c["prefix"] == "news" and "vector_fields_present" in c["risk_flags"] for c in built["risk_clusters"])

    got = store.get_field_prefix_clusters("IND", "analyst45")
    assert got is not None
    assert got["dataset"] == "analyst45"
    assert got["total_fields"] == 4


def test_candidate_field_pool_roundtrip(store):
    cat = {
        "dataset": "analyst45",
        "region": "IND",
        "data_type": "MATRIX",
        "fields": [
            {"id": "anl_est_eps", "type": "MATRIX", "coverage": 0.91},
            {"id": "anl_rev_fy1", "type": "MATRIX", "coverage": 0.88},
            {"id": "news_sent_score", "type": "VECTOR", "coverage": 0.42},
            {"id": "pv_close", "type": "MATRIX", "coverage": 0.97},
        ],
    }
    store.upsert_field_catalog("IND", cat)
    payload = store.build_candidate_field_pool("IND", "analyst45")
    assert payload["dataset"] == "analyst45"
    assert payload["pool_size"] >= 2
    assert "anl_est_eps" in payload["candidate_field_pool"]
    got = store.get_candidate_field_pool("IND", "analyst45")
    assert got is not None
    assert got["dataset"] == "analyst45"
    assert got["pool_size"] == payload["pool_size"]


def test_candidate_field_pool_quality_ranked(store):
    """2026-09-13 口径统一：有 alphaCount/userCount 时按质量先验选池（族多样）。

    背景：旧实现按前缀簇采样，与 S1 概念字段（质量排序 + 族多样）口径分叉，
    GLB fundamental23 实测池 30 字段与 8 个概念字段交集仅 2 个。
    """
    cat = {
        "dataset": "fundamental23",
        "region": "GLB",
        "data_type": "MATRIX",
        "fields": [
            {"id": "anl_est_eps", "type": "MATRIX", "coverage": 0.9, "alphaCount": 500, "userCount": 40},
            {"id": "anl_rev_fy1", "type": "MATRIX", "coverage": 0.9, "alphaCount": 10, "userCount": 5},
            {"id": "news_sent", "type": "VECTOR", "coverage": 0.4, "alphaCount": 100, "userCount": 20},
            {"id": "pv_close", "type": "MATRIX", "coverage": 0.99, "alphaCount": 0, "userCount": 0},
        ],
    }
    store.upsert_field_catalog("GLB", cat)

    payload = store.build_candidate_field_pool("GLB", "fundamental23")
    # 2026-09-15 ⑤：跨簇轮转采样（簇=主体 token；簇按最高质量排序，簇内按质量）
    assert payload["source"] == "cross_cluster_quality"
    assert payload["builder_version"] >= 2
    # 质量先验：alphaCount 主信号 → anl 簇最强，anl_est_eps 居首
    assert payload["candidate_field_pool"][0] == "anl_est_eps"
    assert "anl_rev_fy1" in payload["candidate_field_pool"]
    assert payload["pool_size"] == 4
    assert payload["clusters_covered"] == 3  # anl / news / pv 三簇全覆盖

    # 强制关闭质量排序 → 仍跨簇轮转，簇按字段数排序
    legacy = store.build_candidate_field_pool("GLB", "fundamental23", rank_by_quality=False)
    assert legacy["source"] == "cross_cluster"
    assert len(legacy["candidate_field_pool"]) >= 1


def test_candidate_field_pool_cross_cluster_not_dominated_by_one_family(store):
    """2026-09-15 ⑤ 回归：统计量_主体_时窗 命名（intraday_pv_feats 型）下，池不能被单一主体族霸榜。

    旧实现：前缀簇（首 token=mean/max/corr…）各取字母序前 5 个 → 全是 *_ask_price_*，
    585 字段/21 簇只喂 1 个主体族给 GEM（GBR 实证）。
    """
    names = []
    for stat in ("mean", "max", "min", "corr", "momentum", "std"):
        for subj in ("ask_price", "bid_price", "volume", "vwap", "trade_count"):
            for win in ("30m_post_open", "last_half", "daily"):
                names.append(f"{stat}_{subj}_{win}")
    cat = {"dataset": "intraday_pv_feats", "region": "GBR", "data_type": "MATRIX",
           "fields": [{"id": n, "type": "MATRIX", "coverage": 0.0} for n in names]}
    store.upsert_field_catalog("GBR", cat)
    payload = store.build_candidate_field_pool("GBR", "intraday_pv_feats", max_fields=30)
    pool = payload["candidate_field_pool"]
    assert len(pool) == 30
    subjects = {store._subject_key(p) for p in pool}
    assert {"ask", "bid", "volume", "vwap", "trade"} <= subjects
    assert payload["clusters_covered"] == 5
    # 单一主体族占比不得超过一半
    assert sum(1 for p in pool if "ask_price" in p) <= 15


def test_candidate_field_pool_stale_builder_version_is_ignored(store):
    """旧算法落库的池（无 builder_version / 版本落后）读取时视为过期 → None，迫使重建。"""
    store.upsert_ledger("GBR", "s2_field_pool_stale_ds", {
        "region": "GBR", "dataset": "stale_ds",
        "candidate_field_pool": ["mean_ask_price_30m_post_open"] * 1,
        "pool_size": 1, "source": "s1_prefix_summary",
    })
    assert store.get_candidate_field_pool("GBR", "stale_ds") is None


def test_gate_result_roundtrip(store):
    report = {"all_pass": True, "total": 8, "passed": 8}
    store.upsert_gate_result("EUR", "38", "shortinterest6", report)
    got = store.get_gate_result("EUR", "38", "shortinterest6")
    assert got["all_pass"] is True
    assert got["total"] == 8


def test_backtest_rows_and_alphas(store):
    store.upsert_expressions("EUR", "38", ["rank(x)"], dataset="mh")
    n = store.upsert_backtest_rows(
        "EUR", "38",
        [{"id": "abc123", "code": "rank(x)", "sharpe": 1.2, "fitness": 0.8,
          "two_year_sharpe": 1.1, "margin_bp": 12, "turnover_pct": 8}],
        dataset="mh",
    )
    assert n == 1
    rows = store.list_backtest_rows("EUR", "38")
    assert rows[0]["alpha_id"] == "abc123"
    assert abs(rows[0]["margin"] - 0.0012) < 1e-9


def test_checkpoint_and_ranking(store):
    store.upsert_checkpoint("EUR", "38", {"wave": "38", "batches": []})
    ck = store.get_checkpoint("EUR", "38")
    assert ck["wave"] == "38"
    store.upsert_ranking("EUR", {"ranking": [{"id": "ds1", "tier": "tier1"}]})
    rk = store.get_ranking("EUR")
    assert rk["ranking"][0]["id"] == "ds1"


def test_backtest_rows_persist_all_metrics(store):
    """2026-09-18：回测行须把全指标写入 alphas（含 prod/self 相关性）。"""
    store.upsert_expressions("KOR", "w1", ["rank(y)"], dataset="ds")
    store.upsert_backtest_rows(
        "KOR", "w1",
        [{"id": "aK1", "code": "rank(y)", "sharpe": 1.6, "fitness": 1.1,
          "turnover": 0.12, "margin": 0.0015, "two_year_sharpe": 1.7,
          "sub_universe_sharpe": 1.5, "returns": 0.22, "drawdown": 0.05,
          "long_count": 120, "short_count": 130,
          "concentrated_weight": 0.03, "cluster_test": 0.9,
          "prod_correlation": 0.43, "self_correlation": 0.31}],
        dataset="ds",
    )
    row = store.connection.execute(
        "SELECT sub_universe_sharpe, returns, drawdown, long_count, short_count, "
        "concentrated_weight, cluster_test, prod_correlation, self_correlation "
        "FROM alphas WHERE alpha_id='aK1'"
    ).fetchone()
    assert row is not None
    assert abs(row[0] - 1.5) < 1e-9      # sub_universe_sharpe
    assert abs(row[1] - 0.22) < 1e-9     # returns
    assert abs(row[2] - 0.05) < 1e-9     # drawdown
    assert row[3] == 120 and row[4] == 130
    assert abs(row[5] - 0.03) < 1e-9     # concentrated_weight
    assert abs(row[6] - 0.9) < 1e-9      # cluster_test
    assert abs(row[7] - 0.43) < 1e-9     # prod_correlation
    assert abs(row[8] - 0.31) < 1e-9     # self_correlation


def test_persist_correlation_null_only_by_default(store):
    store.upsert_expressions("EUR", "1", ["rank(z)"])
    store.upsert_backtest_rows("EUR", "1", [{"id": "e1", "code": "rank(z)", "sharpe": 1.0}])

    r = store.persist_correlation("e1", prod=0.55, self_=0.44, source="triage_local")
    assert r["prod_correlation"] == 0.55
    assert r["self_correlation"] == 0.44
    assert r["source"] == "triage_local"

    # 第二次不同值：默认不覆盖
    r2 = store.persist_correlation("e1", prod=0.11, source="triage_local")
    assert r2.get("skipped") == "already_set"

    row = store.connection.execute(
        "SELECT prod_correlation, self_correlation, prod_corr_source "
        "FROM alphas WHERE alpha_id='e1'"
    ).fetchone()
    assert abs(row[0] - 0.55) < 1e-9
    assert abs(row[1] - 0.44) < 1e-9
    assert row[2] == "triage_local"


def test_persist_correlation_overwrite_and_validation(store):
    store.upsert_expressions("EUR", "2", ["rank(w)"])
    store.upsert_backtest_rows("EUR", "2", [{"id": "e2", "code": "rank(w)", "sharpe": 1.0}])
    store.persist_correlation("e2", prod=0.55, source="triage_local")

    # overwrite=True 覆盖为平台权威值
    r = store.persist_correlation("e2", prod=0.83, source="platform_sync", overwrite=True)
    assert r["prod_correlation"] == 0.83
    row = store.connection.execute(
        "SELECT prod_correlation, prod_corr_source FROM alphas WHERE alpha_id='e2'"
    ).fetchone()
    assert abs(row[0] - 0.83) < 1e-9
    assert row[1] == "platform_sync"

    # 越界值被拒绝
    r2 = store.persist_correlation("e2", prod=1.5, overwrite=True)
    assert r2.get("skipped") == "no_valid_value"
    r3 = store.persist_correlation("e2", prod=-0.1, overwrite=True)
    assert r3.get("skipped") == "no_valid_value"

    # 不存在的 alpha
    r4 = store.persist_correlation("nope", prod=0.5)
    assert r4.get("skipped") == "not_found"


def test_persist_correlation_idempotent(store):
    store.upsert_expressions("EUR", "3", ["rank(v)"])
    store.upsert_backtest_rows("EUR", "3", [{"id": "e3", "code": "rank(v)", "sharpe": 1.0}])
    first = store.persist_correlation("e3", prod=0.4, self_=0.3)
    assert "alpha_id" in first
    # 同值重跑：已有值 → already_set（零变化）
    second = store.persist_correlation("e3", prod=0.4, self_=0.3)
    assert second.get("skipped") == "already_set"
    row = store.connection.execute(
        "SELECT prod_correlation, self_correlation FROM alphas WHERE alpha_id='e3'"
    ).fetchone()
    assert abs(row[0] - 0.4) < 1e-9 and abs(row[1] - 0.3) < 1e-9


def test_methodology_rules_and_idea(store):
    store.upsert_methodology_rules("EUR", {"version": 1, "rules": [{"rule_id": "a"}]})
    rules = store.get_methodology_rules("EUR")
    assert rules["rules"][0]["rule_id"] == "a"
    store.upsert_idea("EUR", "mh", 1, {"template": "t", "idea": "i", "expression_list": ["rank(a)"]})
    idea = store.get_idea("EUR", "mh", 1)
    assert idea["expression_list"] == ["rank(a)"]


def test_history_expressions_across_waves(store):
    store.upsert_expressions("EUR", "1", ["rank(a)"])
    store.upsert_expressions("EUR", "2", ["rank(b)"])
    hist = set(store.history_expressions("EUR"))
    assert hist == {"rank(a)", "rank(b)"}
