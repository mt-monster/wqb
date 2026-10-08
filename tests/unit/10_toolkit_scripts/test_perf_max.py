# -*- coding: utf-8 -*-
"""perf_max.py（全闸通过 alpha 的业绩极致优化）守卫测试。

锁定五件事（全部离线，不触网）：
  1. baseline 解析与「闸保持」判定口径（fail 空 + ra_failed_checks 空 + turnover 平台区间）；
  2. 变体梯确定性与扫描维度纪律：禁 truncation、去重、算子预算过滤、EQ 优先于 POW/WIN/DECAY/CTRL；
  3. 外层剥取（signed_power / quantile / 无包裹三形态）与窗口微扫只动最外层；
  4. 目标指标打分与改进幅度（None 语义：未知不报 0、不除零）；
  5. plan.json 原子写/断点续跑与 harvest 收批 JSON 的 label 映射（表达式匹配 + 顺序兜底）。
"""
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "tools", "verdict"))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "src"))

import perf_max as P  # noqa: E402

CORE = ("if_else(greater(mean_estimate_targetprice_annual12_tribes, "
        "median_estimate_targetprice_annual12_tribes), "
        "stddev_estimate_fxadj_targetprice_annual12_tribes, "
        "reverse(stddev_estimate_fxadj_targetprice_annual12_tribes))")
BASE_Q = f"quantile(group_rank(ts_mean({CORE}, 10), subindustry), sigma=1.0)"
BASE_PLAIN = f"group_rank({CORE}, subindustry)"


def _fake_details(**over):
    d = {
        "id": "RR6bv6rz",
        "code": BASE_Q,
        "settings": {"region": "USA", "universe": "TOP3000", "delay": 1,
                     "decay": 500, "neutralization": "STATISTICAL",
                     "nanHandling": "ON", "maxTrade": "OFF", "truncation": 0.08},
        "metrics": {"sharpe": 2.04, "fitness": 1.2, "turnover": 0.0382,
                    "returns": 0.0432, "margin": 0.00226, "pnl": 4313390,
                    "two_year_sharpe": 1.71, "sub_universe_sharpe": 0.89},
        "checks": {"fail": [], "warning": [{"name": "CLUSTER_TEST"}],
                   "pass": ["LOW_SHARPE"], "pending": ["SELF_CORRELATION"]},
        "ra": {"failed_ra_count": 0, "ra_failed_checks": []},
    }
    d.update(over)
    return d


# ------------------------------------------------------------------ 1 解析与闸判定
def test_flatten_details_extracts_metrics_and_checks():
    snap = P.flatten_details(_fake_details())
    assert snap["alpha_id"] == "RR6bv6rz"
    assert snap["sharpe"] == 2.04 and snap["fitness"] == 1.2
    assert snap["checks_fail_names"] == [] and snap["failed_ra_count"] == 0


def test_gate_status_preserved_and_broken():
    ok = P.gate_status(P.flatten_details(_fake_details()))
    assert ok["preserved"] is True and ok["broken"] == []

    bad = P.flatten_details(_fake_details(
        checks={"fail": [{"name": "LOW_SUB_UNIVERSE_SHARPE", "value": 0.7, "limit": 0.8}]},
        ra={"failed_ra_count": 1, "ra_failed_checks": ["LOW_SUB_UNIVERSE_SHARPE"]}))
    g = P.gate_status(bad)
    assert g["preserved"] is False and "LOW_SUB_UNIVERSE_SHARPE" in g["broken"]

    tvr = P.gate_status(P.flatten_details(_fake_details(
        metrics={"turnover": 0.9, "fitness": 1.0})))
    assert tvr["preserved"] is False
    assert any(b.startswith("TURNOVER_OUT_OF_RANGE") for b in tvr["broken"])


# ------------------------------------------------------------------ 2 变体梯纪律
def test_generate_variants_deterministic_and_disciplined():
    base_settings = {"decay": 500, "nanHandling": "ON"}
    v1 = P.generate_variants(BASE_Q, base_settings, max_per_round=8)
    v2 = P.generate_variants(BASE_Q, base_settings, max_per_round=8)
    assert [x["label"] for x in v1] == [x["label"] for x in v2]      # 确定性

    labels = [x["label"] for x in v1]
    levers = [x["lever"] for x in v1]
    # 纪律：EQ 优先排前；禁 truncation；decay 档封顶 512；CTRL 在尾
    assert "EQ_SP05" in labels                                   # quantile 基线 → 等价替换含 SP05
    assert "EQ_QUANTILE" not in labels                           # 与基线同形者不生成
    assert levers == sorted(levers, key=lambda L: ["EQ", "POW", "WIN", "DECAY", "CTRL"].index(L))
    assert all("truncation" not in (x.get("settings_patch") or {}) for x in v1)
    decay_vars = [x for x in v1 if x["lever"] == "DECAY"]
    assert all((x["settings_patch"]["decay"] <= P.DECAY_CAP) for x in decay_vars)
    assert all(x["settings_patch"]["decay"] not in (0,) for x in decay_vars)
    assert all(x["expr"] is None or P.count_ops(x["expr"]) < P.OPS_BUDGET for x in v1)
    assert all(x["expr"] != BASE_Q for x in v1 if x.get("expr"))    # 去重


def test_generate_variants_max_round_cap():
    v = P.generate_variants(BASE_Q, {"decay": 500}, max_per_round=3)
    assert len(v) <= 3


def test_plain_baseline_gets_wraps_and_signed_power_sweep():
    v = P.generate_variants(BASE_PLAIN, {"decay": 300}, max_per_round=8)
    labels = [x["label"] for x in v]
    assert "EQ_QUANTILE" in labels and "EQ_SP05" in labels          # 无包裹 → 全套 EQ


# ------------------------------------------------------------------ 3 外层剥取与窗口
def test_strip_outer_three_forms():
    inner, outer = P._strip_outer("signed_power(group_rank(x, industry), 0.5)")
    assert outer == "signed_power" and inner == "group_rank(x, industry), 0.5"
    assert P._first_positional(inner) == "group_rank(x, industry)"      # x 位取首位置参数
    inner, outer = P._strip_outer(f"group_rank({CORE}, subindustry)")
    assert outer == "group_rank"
    inner, outer = P._strip_outer("x + y")
    assert outer is None


def test_first_positional_skips_kwargs():
    assert P._first_positional("group_rank(x, subindustry), sigma=1.0") == "group_rank(x, subindustry)"
    assert P._first_positional("add(a, b), hump=0.01") == "add(a, b)"


def test_window_variants_touch_only_outer_window():
    base = f"group_rank(ts_mean({CORE}, 10), subindustry)"
    wins = P._window_variants(base)
    assert wins, "应生成窗口变体"
    for v in wins:
        assert v["expr"] == f"group_rank(ts_mean({CORE}, {'5' if 'HALF' in v['label'] else '20'}), subindustry)"
        assert v["expr"].count("(") == v["expr"].count(")")           # 括号平衡（曾漏右括号致整条被元数闸静默丢弃）

    base_q = f"quantile(group_rank(ts_mean({CORE}, 10), subindustry), sigma=1.0)"
    wins_q = P._window_variants(base_q)
    for v in wins_q:
        assert v["expr"].count("(") == v["expr"].count(")")
        assert v["expr"].endswith(", sigma=1.0)")


# ------------------------------------------------------------------ 4 打分与改进
def test_score_and_improvement_none_semantics():
    snap = P.flatten_details(_fake_details())
    assert P.score_variant(snap, "fitness") == pytest.approx(1.2)
    assert P.score_variant({}, "fitness") is None                    # 未知不报 0
    assert P.improvement({}, snap, "fitness") is None
    worse = P.flatten_details(_fake_details(metrics={"fitness": 1.0}))
    assert P.improvement(snap, worse, "fitness") == pytest.approx(-0.2)


# ------------------------------------------------------------------ 5 断点续跑与映射
def test_plan_atomic_save_and_resume(tmp_path):
    plan_dir = str(tmp_path)
    plan = {"alpha_id": "X", "variants": [{"label": "A", "expr": "x", "result": None}]}
    P.save_plan(plan_dir, plan)
    assert os.path.isfile(os.path.join(plan_dir, "plan.json"))
    assert not os.path.exists(os.path.join(plan_dir, "plan.json.tmp"))
    again = P.load_plan(plan_dir)
    assert again["variants"][0]["label"] == "A"


def test_match_from_harvest_expr_then_order():
    plan = {"variants": [
        {"label": "V1", "expr": "expr_one"},
        {"label": "V2", "expr": "expr_two"},
        {"label": "V3", "base_expr": "expr_three"},
    ]}
    rows = [{"alphas": [
        {"alpha_id": "id1", "code": "expr_one"},
        {"alpha_id": "id2", "code": "expr_two"},
        {"alpha_id": "id3", "code": "expr_three"},
    ]}]
    mapping = P._match_from_harvest(plan, rows)
    assert mapping == {"V1": "id1", "V2": "id2", "V3": "id3"}

    rows_no_code = [{"alpha_id": "z1"}, {"alpha_id": "z2"}, {"alpha_id": "z3"}]
    mapping2 = P._match_from_harvest(plan, rows_no_code)
    assert set(mapping2.values()) == {"z1", "z2", "z3"}              # 顺序兜底


def test_dispatch_groups_by_settings_patch():
    plan = {"variants": [
        {"label": "A", "expr": "e1", "settings_patch": {}},
        {"label": "B", "expr": "e2", "settings_patch": {"decay": 250}},
        {"label": "C", "expr": "e3", "settings_patch": {"decay": 250}},
    ]}
    groups = P.dispatch_groups(plan)
    assert len(groups) == 2
    by_tag = {g["tag"]: g for g in groups}
    assert set(by_tag["decay250"]["labels"]) == {"B", "C"}
    assert by_tag["A"]["exprs"] == ["e1"]


# ------------------------------------------------------- 1b 平台原始形态（is/regular）
def _fake_raw_details(**over):
    d = {
        "id": "RR6bv6rz",
        "regular": {"code": BASE_Q, "operatorCount": 8},
        "settings": {"region": "USA", "universe": "TOP3000", "delay": 1, "decay": 500,
                     "neutralization": "STATISTICAL"},
        "is": {
            "sharpe": 2.04, "fitness": 1.2, "turnover": 0.0382,
            "returns": 0.0432, "margin": 0.00226, "pnl": 4313390,
            "checks": [
                {"name": "LOW_SHARPE", "result": "PASS", "limit": 1.58, "value": 2.04},
                {"name": "LOW_2Y_SHARPE", "result": "PASS", "limit": 1.0, "value": 1.71},
                {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PASS",
                 "limit": 0.88, "value": 0.89},
                {"name": "CONCENTRATED_WEIGHT", "result": "WARNING",
                 "limit": 0.1, "value": 0.12},
            ],
        },
    }
    d.update(over)
    return d


def test_flatten_raw_platform_shape():
    snap = P.flatten_details(_fake_raw_details())
    assert snap["alpha_id"] == "RR6bv6rz"
    assert snap["code"] == BASE_Q                      # regular.code
    assert snap["sharpe"] == 2.04 and snap["fitness"] == 1.2
    assert snap["two_year_sharpe"] == 1.71             # RA_2Y_NAMES 取值
    assert snap["sub_universe_sharpe"] == 0.89
    assert snap["failed_ra_count"] == 1                # WARNING 计失败（config 口径）
    assert snap["ra_failed_checks"] == ["CONCENTRATED_WEIGHT"]
    assert snap["checks_warn_names"] == ["CONCENTRATED_WEIGHT"]
    assert snap["ra_pending_count"] == 0


def test_pending_only_counts_in_ra_check_names():
    # 名单外 PENDING（SELF_CORRELATION）不计不卡；名单内（LOW_2Y_SHARPE）要计
    snap = P.flatten_details(_fake_details(
        checks={"fail": [], "warning": [],
                "pending": ["SELF_CORRELATION", "LOW_2Y_SHARPE"]}))
    assert snap["ra_pending_count"] == 1
    snap2 = P.flatten_details(_fake_details(
        checks={"fail": [], "warning": [], "pending": ["SELF_CORRELATION"]}))
    assert snap2["ra_pending_count"] == 0


# ------------------------------------------------------- 1b 平台原始形态（is/regular）
def _fake_raw_details(**over):
    d = {
        "id": "RR6bv6rz",
        "regular": {"code": BASE_Q, "operatorCount": 8},
        "settings": {"region": "USA", "universe": "TOP3000", "delay": 1, "decay": 500,
                     "neutralization": "STATISTICAL"},
        "is": {
            "sharpe": 2.04, "fitness": 1.2, "turnover": 0.0382,
            "returns": 0.0432, "margin": 0.00226, "pnl": 4313390,
            "checks": [
                {"name": "LOW_SHARPE", "result": "PASS", "limit": 1.58, "value": 2.04},
                {"name": "LOW_2Y_SHARPE", "result": "PASS", "limit": 1.0, "value": 1.71},
                {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PASS",
                 "limit": 0.88, "value": 0.89},
                {"name": "CONCENTRATED_WEIGHT", "result": "WARNING",
                 "limit": 0.1, "value": 0.12},
            ],
        },
    }
    d.update(over)
    return d


def test_flatten_raw_platform_shape():
    snap = P.flatten_details(_fake_raw_details())
    assert snap["alpha_id"] == "RR6bv6rz"
    assert snap["code"] == BASE_Q                      # regular.code
    assert snap["sharpe"] == 2.04 and snap["fitness"] == 1.2
    assert snap["two_year_sharpe"] == 1.71             # RA_2Y_NAMES 取值
    assert snap["sub_universe_sharpe"] == 0.89
    assert snap["failed_ra_count"] == 1                # WARNING 计失败（config 口径）
    assert snap["ra_failed_checks"] == ["CONCENTRATED_WEIGHT"]
    assert snap["checks_warn_names"] == ["CONCENTRATED_WEIGHT"]
    assert snap["ra_pending_count"] == 0


def test_pending_only_counts_in_ra_check_names():
    # 名单外 PENDING（SELF_CORRELATION）不计不卡；名单内（LOW_2Y_SHARPE）要计
    snap = P.flatten_details(_fake_details(
        checks={"fail": [], "warning": [],
                "pending": ["SELF_CORRELATION", "LOW_2Y_SHARPE"]}))
    assert snap["ra_pending_count"] == 1
    snap2 = P.flatten_details(_fake_details(
        checks={"fail": [], "warning": [], "pending": ["SELF_CORRELATION"]}))
    assert snap2["ra_pending_count"] == 0


def test_plan_spec_carries_full_baseline_settings(tmp_path):
    # spec 条目 = 全量 baseline 设置 + patch（只写 patch 会让 decay 退回工具缺省 → 400）
    src = tmp_path / "baseline.json"
    src.write_text(json.dumps(_fake_details()), encoding="utf-8")
    plan_dir = tmp_path / "plan"
    rc = P.main(["plan", "--baseline-json", str(src),
                 "--plan-dir", str(plan_dir), "--objective", "fitness"])
    assert rc == 0
    spec = json.loads((plan_dir / "dispatch_spec.json").read_text(encoding="utf-8"))
    by_tag = {os.path.basename(e["path"]): e for e in spec}
    base_entry = by_tag["variants_EQ_SP05.txt"]        # 空 patch 组以首 label 命名
    assert base_entry["decay"] == 500 and base_entry["neutralization"] == "STATISTICAL"
    assert base_entry["universe"] == "TOP3000" and base_entry["nanHandling"] == "ON"
    decay_entry = by_tag["variants_decay250.txt"]
    assert decay_entry["decay"] == 250                 # patch 覆盖 baseline
    assert decay_entry["neutralization"] == "STATISTICAL"
    nan_entry = by_tag["variants_nanHandlingOFF.txt"]
    assert nan_entry["nanHandling"] == "OFF" and nan_entry["decay"] == 500


# ------------------------------------------------------- 2 submit_ready 入队（可交付必入）
def test_build_enqueue_record_fills_all_fields():
    rec = P.build_enqueue_record(P.flatten_details(_fake_raw_details()),
                                 {"alpha_id": "RR6bv6rz", "region": "USA"})
    assert rec["alpha_id"] == "RR6bv6rz" and rec["region"] == "USA"
    assert rec["decay"] == 500 and rec["neutralization"] == "STATISTICAL"
    assert rec["expr"] == BASE_Q
    assert rec["sharpe"] == 2.04 and rec["two_year"] == 1.71 and rec["sub_universe"] == 0.89
    assert rec["margin"] == 0.00226                 # pnl 不进 submit_ready（无该列）
    assert rec["towers"] == "[]" or rec["towers"].startswith("[")
    assert rec["family"]                          # 族名派生不为空
    assert "prod" in rec and "self" in rec


def test_enqueue_deliverables_only_gate_preserved(tmp_path):
    db = str(tmp_path / "q.db")
    plan = {"alpha_id": "RR6bv6rz", "region": "USA", "variants": [
        {"label": "WIN_DBL_20", "alpha_id": "pw5RbrYX",
         "result": dict(P.flatten_details(_fake_raw_details()), alpha_id="pw5RbrYX",
                        gate={"preserved": True, "broken": []})},
        {"label": "BROKEN", "alpha_id": "bad00001",
         "result": dict(P.flatten_details(_fake_raw_details()), alpha_id="bad00001",
                        gate={"preserved": False, "broken": ["LOW_SUB_UNIVERSE_SHARPE"]})},
    ]}
    out = P.enqueue_deliverables(plan, fetch_corr=lambda aid: (0.55, 0.30),
                                 db_path=db)
    assert [x["label"] for x in out] == ["WIN_DBL_20"]      # 破闸的不入队
    assert out[0]["gate"] and out[0]["status"] == "READY"
    import sqlite3
    con = sqlite3.connect(db)
    rows = con.execute("SELECT alpha_id, prod, self, status FROM submit_ready").fetchall()
    con.close()
    assert rows == [("pw5RbrYX", 0.55, 0.30, "READY")]


def test_enqueue_deliverables_dry_run_rolls_back(tmp_path):
    db = str(tmp_path / "q.db")
    plan = {"alpha_id": "X", "region": "USA", "variants": [
        {"label": "A", "alpha_id": "a1",
         "result": dict(P.flatten_details(_fake_raw_details()), alpha_id="a1",
                        gate={"preserved": True, "broken": []})}]}
    out = P.enqueue_deliverables(plan, fetch_corr=lambda aid: (None, None),
                                 dry_run=True, db_path=db)
    assert out and out[0]["status"] == "READY"               # 演练里看得到
    import sqlite3
    con = sqlite3.connect(db)
    n = con.execute("SELECT COUNT(*) FROM submit_ready").fetchone()[0]
    con.close()
    assert n == 0                                            # 但没落盘


