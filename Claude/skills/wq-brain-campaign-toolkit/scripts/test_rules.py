# -*- coding: utf-8 -*-
"""test_rules.py - 方法论自学习规则引擎（_lib/rules.py）L1-L4 契约测试。

运行（toolkit scripts 目录）：
  python -m pytest test_rules.py -q
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import rules as R


@pytest.fixture()
def store(tmp_path):
    (tmp_path / "reference").mkdir()
    # 注入不存在的临时全局库路径，隔离真实 toolkit config/methodology_rules.json
    return R.RuleStore(str(tmp_path), global_path=str(tmp_path / "_no_global.json"))


@pytest.fixture()
def dual_store(tmp_path):
    """全局 + 区域双层库（全局库预置一条 region=* 规则）。"""
    (tmp_path / "reference").mkdir()
    gpath = tmp_path / "global_rules.json"
    gpath.write_text('{"version":1,"rules":[{"rule_id":"g_strat","type":"strategy",'
                     '"trigger":{"region":"*"},"action":{"op":"x","message":"gm"},'
                     '"confidence":0.8,"status":"active"}]}', encoding="utf-8")
    return R.RuleStore(str(tmp_path), global_path=str(gpath))


class Ctx:
    def __init__(self, d, region="EUR", global_path=None):
        self.dir = str(d)
        self.region = region
        if global_path is not None:
            self.global_path = global_path


# ---------------- L2：存储与查询 ----------------

def test_upsert_and_get(store):
    r = {"rule_id": "r1", "type": "strategy",
         "trigger": {"region": "EUR"}, "action": {"op": "x", "message": "m"}}
    store.upsert(r)
    got = store.get("r1")
    assert got["rule_id"] == "r1"
    assert got["confidence"] == 0.8
    assert got["status"] == "active"
    assert got["times_applied"] == 0


def test_upsert_idempotent_merge(store):
    store.upsert({"rule_id": "r1", "type": "strategy", "confidence": 0.5,
                  "trigger": {}, "action": {}})
    store.upsert({"rule_id": "r1", "confidence": 0.7})
    got = store.get("r1")
    assert got["confidence"] == 0.7
    assert got["type"] == "strategy"  # 未给字段保留原值


def test_query_trigger_match(store):
    store.upsert({"rule_id": "eur_only", "type": "strategy",
                  "trigger": {"region": "EUR"}, "action": {}})
    store.upsert({"rule_id": "all_region", "type": "strategy",
                  "trigger": {"region": "*"}, "action": {}})
    eur = store.query(rule_type="strategy", region="EUR")
    assert {r["rule_id"] for r in eur} == {"eur_only", "all_region"}
    kor = store.query(rule_type="strategy", region="KOR")
    assert {r["rule_id"] for r in kor} == {"all_region"}


def test_query_status_filter(store):
    store.upsert({"rule_id": "a", "type": "strategy", "status": "active",
                  "trigger": {}, "action": {}})
    store.upsert({"rule_id": "c", "type": "strategy", "status": "contested",
                  "trigger": {}, "action": {}})
    assert {r["rule_id"] for r in store.query(rule_type="strategy")} == {"a"}


# ---------------- L3：universe 杠杆拦截 ----------------

def test_universe_lever_block(store):
    store.upsert({"rule_id": "dead800", "type": "universe_lever",
                  "trigger": {"universe": "TOP800", "region": "EUR"},
                  "action": {"dead_universe": "TOP800", "message": "判死"}})
    ctx = Ctx(store.dir, "EUR")
    ok, msgs = R.check_universe_lever(ctx, "TOP800")
    assert not ok and msgs
    ok2, _ = R.check_universe_lever(ctx, "TOP2500")
    assert ok2


def test_universe_lever_contested_not_block(store):
    # contested 状态不参与拦截（query 默认只取 active）
    store.upsert({"rule_id": "dead800", "type": "universe_lever", "status": "contested",
                  "trigger": {"universe": "TOP800"}, "action": {"dead_universe": "TOP800"}})
    ok, _ = R.check_universe_lever(Ctx(store.dir), "TOP800")
    assert ok


# ---------------- L1：信号提取 ----------------

def test_detect_dilution_monotonic():
    rows = [{"weight": 0.7, "prod_corr": 0.82}, {"weight": 0.5, "prod_corr": 0.76},
            {"weight": 0.4, "prod_corr": 0.68}]
    sig = R._detect_dilution(rows)
    assert sig and sig["type"] == "strategy"
    assert sig["status"] == "active"


def test_detect_dilution_not_monotonic():
    rows = [{"weight": 0.7, "prod_corr": 0.68}, {"weight": 0.5, "prod_corr": 0.82},
            {"weight": 0.4, "prod_corr": 0.76}]
    assert R._detect_dilution(rows) is None


def test_detect_universe_collapse():
    rows = [{"sharpe": 0.3}, {"sharpe": 0.42}, {"sharpe": 0.1}]
    sig = R._detect_universe_collapse(rows, {"universe": "TOP800", "region": "EUR"})
    assert sig and sig["type"] == "universe_lever"
    assert sig["status"] == "contested"  # 自动判死先 contested
    assert sig["action"]["dead_universe"] == "TOP800"


def test_detect_universe_no_collapse_when_strong():
    rows = [{"sharpe": 1.5}, {"sharpe": 0.4}, {"sharpe": 0.3}]
    assert R._detect_universe_collapse(rows, {"universe": "TOP800"}) is None


# ---------------- L4：验证（证伪/强化） ----------------

def test_validate_falsify(store):
    store.upsert({"rule_id": "dead800", "type": "universe_lever", "confidence": 0.9,
                  "trigger": {"universe": "TOP800"}, "action": {"dead_universe": "TOP800"}})
    ctx = Ctx(store.dir, global_path=store.global_path)
    rep = R.validate_rules(ctx, [{"sharpe": 1.5}], {"universe": "TOP800"})
    assert "dead800" in rep["falsified"]
    r = store.get("dead800")
    assert r["status"] == "contested"
    assert r["confidence"] == round(0.9 * 0.7, 3)


def test_validate_reinforce(store):
    store.upsert({"rule_id": "dead800", "type": "universe_lever", "confidence": 0.9,
                  "trigger": {"universe": "TOP800"}, "action": {"dead_universe": "TOP800"}})
    ctx = Ctx(store.dir, global_path=store.global_path)
    rep = R.validate_rules(ctx, [{"sharpe": 0.3}], {"universe": "TOP800"})
    assert "dead800" in rep["reinforced"]
    r = store.get("dead800")
    assert r["confidence"] == 0.95  # +0.05
    assert r["status"] == "active"


def test_validate_contested_recover(store):
    store.upsert({"rule_id": "dead800", "type": "universe_lever", "status": "contested",
                  "confidence": 0.68, "trigger": {"universe": "TOP800"},
                  "action": {"dead_universe": "TOP800"}})
    ctx = Ctx(store.dir, global_path=store.global_path)
    R.validate_rules(ctx, [{"sharpe": 0.3}], {"universe": "TOP800"})
    r = store.get("dead800")
    assert r["confidence"] == 0.73
    assert r["status"] == "active"  # 复核通过转正


# ---------------- 双层库：全局 + 区域合并与路由 ----------------

def test_dual_layer_merge(dual_store):
    """全局规则自动合并进任意战役（跨 region 通用）。"""
    dual_store.upsert({"rule_id": "r_local", "type": "strategy",
                       "trigger": {"region": "EUR"}, "action": {}}, global_scope=False)
    data = dual_store.load()
    ids = {r["rule_id"] for r in data["rules"]}
    assert ids == {"g_strat", "r_local"}
    assert data["_global_count"] == 1 and data["_region_count"] == 1


def test_region_overrides_global(dual_store):
    """同 rule_id 区域覆盖全局。"""
    dual_store.upsert({"rule_id": "g_strat", "confidence": 0.3,
                       "trigger": {"region": "EUR"}, "action": {"message": "local"}},
                      global_scope=False)
    r = dual_store.get("g_strat")
    assert r["confidence"] == 0.3 and r["action"]["message"] == "local"


def test_upsert_auto_route_global(dual_store):
    """trigger.region='*' 自动路由到全局库。"""
    dual_store.upsert({"rule_id": "auto_g", "type": "strategy",
                       "trigger": {"region": "*"}, "action": {}})
    # 全局库应有，区域库应无
    gids = {r["rule_id"] for r in dual_store._load_file(dual_store.global_path)["rules"]}
    rids = {r["rule_id"] for r in dual_store._load_file(dual_store.path)["rules"]}
    assert "auto_g" in gids and "auto_g" not in rids


def test_upsert_auto_route_region(dual_store):
    """trigger.region='EUR' 自动路由到区域库。"""
    dual_store.upsert({"rule_id": "auto_r", "type": "universe_lever",
                       "trigger": {"region": "EUR", "universe": "TOP800"},
                       "action": {"dead_universe": "TOP800"}})
    gids = {r["rule_id"] for r in dual_store._load_file(dual_store.global_path)["rules"]}
    rids = {r["rule_id"] for r in dual_store._load_file(dual_store.path)["rules"]}
    assert "auto_r" in rids and "auto_r" not in gids


def test_validate_no_global_pollution(dual_store):
    """L4 校验区域规则后不污染全局库（合并视图不得整体写回）。"""
    dual_store.upsert({"rule_id": "dead800", "type": "universe_lever", "confidence": 0.9,
                       "trigger": {"region": "EUR", "universe": "TOP800"},
                       "action": {"dead_universe": "TOP800"}}, global_scope=False)
    R.validate_rules(Ctx(dual_store.dir, global_path=dual_store.global_path),
                     [{"sharpe": 1.5}], {"universe": "TOP800"})
    # 全局库仍只有 g_strat，dead800 只在区域库
    gids = {r["rule_id"] for r in dual_store._load_file(dual_store.global_path)["rules"]}
    assert gids == {"g_strat"}
    assert dual_store.get("dead800")["status"] == "contested"


# ---------------- explore_contract：多样性注入契约融合 ----------------

@pytest.fixture()
def cctx(tmp_path):
    """携带隔离全局路径的契约测试 ctx。"""
    (tmp_path / "reference").mkdir()
    return Ctx(str(tmp_path), "GBR", global_path=str(tmp_path / "_no_global.json"))


def test_issue_and_get_active_contract(cctx):
    rid = R.issue_contract(cctx, required_operators=["ts_rank", "group_zscore"],
                           skeleton_quota={"event_gated": 1}, region="GBR")
    act = R.get_active_contract(cctx, batch_type="explore")
    assert act is not None
    assert act["_rule_id"] == rid
    assert act["required_operators"] == ["ts_rank", "group_zscore"]
    assert act["skeleton_quota"] == {"event_gated": 1}


def test_contract_exempt_repair(cctx):
    R.issue_contract(cctx, ["ts_rank"], {}, "GBR", exempt=["repair"])
    assert R.get_active_contract(cctx, batch_type="repair") is None
    assert R.get_active_contract(cctx, batch_type="explore") is not None


def test_contract_expiry(cctx):
    rid = R.issue_contract(cctx, ["ts_rank"], {}, "GBR", expires_after_batches=2)
    R.consume_contract(cctx, rid, "d1")
    R.consume_contract(cctx, rid, "d2")
    assert R.get_active_contract(cctx) is None  # 满 2 批过期


def test_consume_contract_idempotent(cctx):
    rid = R.issue_contract(cctx, ["ts_rank"], {}, "GBR")
    R.consume_contract(cctx, rid, "d1")
    R.consume_contract(cctx, rid, "d1")  # 重复 digest 不重复计
    act = R.get_active_contract(cctx)
    assert act["consumed_batches"].count("d1") == 1


def test_issue_contract_deprecates_old(cctx):
    rid1 = R.issue_contract(cctx, ["ts_rank"], {}, "GBR")
    rid2 = R.issue_contract(cctx, ["group_zscore"], {}, "GBR")
    store = R._store_for(cctx)
    assert store.get(rid1)["status"] == "deprecated"
    assert store.get(rid2)["status"] == "active"
    # 只有新契约生效
    assert R.get_active_contract(cctx)["_rule_id"] == rid2


def test_reconcile_landing_full(cctx):
    import collections
    rid = R.issue_contract(cctx, ["ts_rank", "group_zscore"], {"event_gated": 1}, "GBR")
    ops = collections.Counter({"ts_rank": 3, "group_zscore": 2})
    skel = collections.Counter({"event_gated": 2})
    rep = R.reconcile_contract_landing(cctx, "GBR", ops, skel)
    assert rep["landing_rate"] == 1.0
    assert rep["contract_rule_id"] == rid
    # 全落地 -> confidence +0.05
    assert R._store_for(cctx).get(rid)["confidence"] == 1.0  # 封顶


def test_reconcile_landing_low_marks_contested(cctx):
    import collections
    rid = R.issue_contract(cctx, ["ts_rank", "group_zscore", "ts_corr", "hump"], {}, "GBR")
    ops = collections.Counter({"ts_rank": 1})  # 仅 1/4 落地
    rep = R.reconcile_contract_landing(cctx, "GBR", ops, collections.Counter())
    assert rep["landing_rate"] == 0.25
    r = R._store_for(cctx).get(rid)
    assert r["status"] == "contested"
    assert r["confidence"] == round(1.0 * 0.8, 3)


def test_reconcile_no_contract(cctx):
    import collections
    assert R.reconcile_contract_landing(cctx, "GBR", collections.Counter(),
                                        collections.Counter()) is None


# ---------------- P1：verdict 自动推荐 ----------------

@pytest.fixture()
def rctx(tmp_path):
    """推荐引擎测试 ctx（隔离全局库）。"""
    (tmp_path / "reference").mkdir()
    return Ctx(str(tmp_path), "EUR", global_path=str(tmp_path / "_no_global.json"))


def _row(id, sharpe=None, walls=None, **kw):
    r = {"id": id, "sharpe": sharpe, "walls": walls or []}
    r.update(kw)
    return r


def test_recommend_universe_dead(rctx):
    """当前 universe 命中判死规则 -> 最高优先级换 universe。"""
    store = R._store_for(rctx)
    store.upsert({"rule_id": "dead800", "type": "universe_lever",
                  "trigger": {"universe": "TOP800", "region": "EUR"},
                  "action": {"op": "block_universe", "dead_universe": "TOP800",
                             "message": "TOP800 判死"},
                  "evidence": {"correct_universe": "TOP2500"},
                  "status": "active"}, global_scope=False)
    rows = [_row("a", 0.4, ["SHARPE"]), _row("b", 0.3, ["SHARPE"]),
            _row("c", 0.42, ["SHARPE"])]
    recs = R.recommend_next_wave(rctx, rows, wave_meta={"region": "EUR", "universe": "TOP800"})
    assert recs and recs[0]["priority"] == 100
    assert "TOP800" in recs[0]["direction"]
    assert "TOP2500" in recs[0]["action_hint"]
    assert recs[0]["source_rule"] == "dead800"


def test_recommend_prod_wall_dilution(rctx):
    """IS 强 + prod>0.7 -> 稀释策略推荐 + rnf 警告。"""
    store = R._store_for(rctx)
    store.upsert({"rule_id": "dil", "type": "strategy", "trigger": {"region": "*"},
                  "action": {"op": "gradient_dilute",
                             "params": {"corr_threshold": 0.3, "weight_step": 0.1},
                             "message": "梯度稀释"},
                  "status": "active"}, global_scope=True)
    store.upsert({"rule_id": "rnf", "type": "diagnosis", "trigger": {"region": "*"},
                  "action": {"op": "warn_rnf_drop", "message": "rnf 随稀释降"},
                  "status": "active"}, global_scope=True)
    rows = [_row("a", 1.8, ["2Y"], prod_corr=0.85), _row("b", 1.5, ["2Y"], prod_corr=0.8)]
    recs = R.recommend_next_wave(rctx, rows, wave_meta={"region": "EUR"})
    dirs = [r["direction"] for r in recs]
    assert any("稀释" in d for d in dirs)
    assert any("rnf" in d for d in dirs)
    dil = next(r for r in recs if "稀释" in r["direction"])
    assert dil["source_rule"] == "dil" and dil["priority"] == 90


def test_recommend_sharpe_weak_structural(rctx):
    """多数卡 SHARPE 且 max<1.0 -> 结构层重构。"""
    rows = [_row("a", 0.6, ["SHARPE"]), _row("b", 0.5, ["SHARPE"]),
            _row("c", 0.7, ["SHARPE"]), _row("d", 0.4, ["SHARPE"])]
    recs = R.recommend_next_wave(rctx, rows, wave_meta={"region": "EUR"})
    assert recs and "结构层重构" in recs[0]["direction"]
    assert recs[0]["source_rule"] is None


def test_recommend_near_param_tune(rctx):
    """near 池卡 2Y 墙 -> 参数层调优。"""
    rows = [_row("a", 1.3, ["2Y"], fitness=1.1), _row("b", 1.2, ["2Y"], fitness=1.05)]
    near = list(rows)
    recs = R.recommend_next_wave(rctx, rows, near=near, wave_meta={"region": "EUR"})
    assert any("参数层调优" in r["direction"] and "2Y" in r["direction"] for r in recs)


def test_recommend_cw_wall(rctx):
    """多数卡 CW -> 集中度墙骨架多样性。"""
    rows = [_row("a", 1.4, ["CW"]), _row("b", 1.3, ["CW"]), _row("c", 1.2, ["CW"])]
    recs = R.recommend_next_wave(rctx, rows, wave_meta={"region": "EUR"})
    assert any("集中度墙" in r["direction"] for r in recs)


def test_recommend_all_pass_submit(rctx):
    """全部达标 -> 提交评审推荐。"""
    rows = [_row("a", 1.8, []), _row("b", 1.6, [])]
    recs = R.recommend_next_wave(rctx, rows, wave_meta={"region": "EUR"})
    assert recs and "提交评审" in recs[0]["direction"]
    assert recs[0]["priority"] == 95


def test_recommend_priority_order(rctx):
    """推荐按优先级降序。"""
    store = R._store_for(rctx)
    store.upsert({"rule_id": "dead800", "type": "universe_lever",
                  "trigger": {"universe": "TOP800", "region": "EUR"},
                  "action": {"op": "block_universe", "dead_universe": "TOP800", "message": "m"},
                  "evidence": {"correct_universe": "TOP2500"}, "status": "active"},
                 global_scope=False)
    rows = [_row("a", 0.4, ["SHARPE"]), _row("b", 0.3, ["SHARPE"]), _row("c", 0.35, ["SHARPE"])]
    recs = R.recommend_next_wave(rctx, rows, wave_meta={"region": "EUR", "universe": "TOP800"})
    prios = [r["priority"] for r in recs]
    assert prios == sorted(prios, reverse=True)
    assert recs[0]["priority"] == 100  # universe 判死优先于结构重构


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
