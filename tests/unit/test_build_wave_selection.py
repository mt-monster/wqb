# -*- coding: utf-8 -*-
"""build_wave.py 选波权威化 + --auto-coverage never 真正关闭注入（2026-09-12 GBR wave57）。

两个实测痛点：
  1. build_wave 只把 picked 写成 selected，落选的 gem/pending/enhanced 行原样留在波里，
     pipeline/gate 按波读表达式时分不清本波真正的选集；Agent 只能用 upsert_expressions
     回传全量正文去改状态（43 条 ≈ 3-4k token/次）。现在 picked 写 selected 的同一事务里
     把落选待选行归档为 superseded（settings_json.status_change 记 "not picked by
     build_wave <ts>"），dropped/selected/gated 与已回测行（alpha_id 非空）不碰。
  2. --auto-coverage never 此前只关"签发"，契约注入与 ④ 自愈照跑：group_backfill(x, sector, 20)
     / group_cartesian_product(sector, sector) / group_count(...) 无视开关进池，其中若干把
     MATRIX 字段当 group 用，平台报 unit 错误并整批取消 multisim。

端到端：子进程跑真 build_wave.py，隔离工作区（临时 wqb.db + 最小战役目录），绝不碰真库。
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO = Path(__file__).resolve().parents[2]
BUILD_WAVE = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts" / "build_wave.py"

# 同桶（ts_mean>atom）、同字段：分桶轮转退化为按 id 顺序取前 --size 条，picked 可预测
WAITING = [
    ("ts_mean(close, 5)", "gem"),         # picked
    ("ts_mean(close, 22)", "pending"),    # picked
    ("ts_mean(close, 66)", "enhanced"),   # 落选 → superseded
    ("ts_mean(close, 252)", "gem"),       # 落选 → superseded
]
UNTOUCHABLE = [
    ("ts_mean(close, 504)", "gem", "A1"),        # 已回测（alpha_id），不碰
    ("ts_mean(close, 1008)", "dropped", None),   # 纪律废弃，不碰（也不是候选）
    ("ts_mean(close, 1260)", "gated", None),     # 闸门链上，不碰
    ("ts_mean(close, 120)", "selected", None),   # 旧选集，不碰
]
CONTRACT_EXPRS = ["group_backfill(close, sector, 20)", "group_count(close, sector)"]


# ---------------------------------------------------------------------------
# 2026-09-25 优化落地（P1/P4）：qp 质量预估硬筛 + prod 饱和字段降权
# 用 stub 模块驱动 build_wave 的接线行为（真实估算器另有自己的单测）；
# 无 tools/ 目录时优雅降级（已由既有 22 例覆盖：默认行为不变）。
# ---------------------------------------------------------------------------

_QP_STUB = '''
def db_connect(path):
    import sqlite3
    return sqlite3.connect(path)


def predict_all(candidates, region, conn):
    out = []
    for e, ds in candidates:
        hard = "hardsig" in e
        out.append({"expr": e[:120],
                    "verdict": "HARD_REJECT" if hard else "DIRECT_SUBMIT",
                    "pred_sharpe": 0.1 if hard else 2.0,
                    "pred_fitness": 0.1 if hard else 1.5})
    return out, {}
'''

_PSAT_STUB = '''
def check_wave(exprs, region, dataset=None, db_path=None, thresholds=None):
    return {"status": "enforced", "passed": True, "saturated_fields": ["satfield"]}
'''


def _install_tool_stubs(c):
    tools_dir = Path(c.db).parent.parent / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    (tools_dir / "quality_predict.py").write_text(_QP_STUB, encoding="utf-8")
    (tools_dir / "prod_saturation_gate.py").write_text(_PSAT_STUB, encoding="utf-8")


def _seed_wave(c, wave, exprs):
    st = c.Store(c.db)
    try:
        st.upsert_expressions("TST", wave,
                              [{"expression": e, "status": "gem"} for e in exprs],
                              dataset="ds1")
    finally:
        st.close()


def _run_wave(c, wave, *extra):
    r = subprocess.run(
        [sys.executable, str(BUILD_WAVE), "--campaign-dir", c.dir, "--from-db",
         "--dataset", "ds1", "--wave", wave, "--size", "8", "--per-bucket", "8",
         "--enhance-diversity", "never", *extra],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=c.env, timeout=600)
    assert r.returncode == 0, f"build_wave 失败 rc={r.returncode}\nSTDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
    return r.stdout + r.stderr


def _wave_rows_ordered(c, wave):
    import sqlite3
    conn = sqlite3.connect(c.db)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM expressions WHERE region='TST' AND wave=? ORDER BY id", (wave,))]
    finally:
        conn.close()


def test_p4_qp_hard_drops_hard_reject_except_keep_probes(campaign):
    _install_tool_stubs(campaign)
    _seed_wave(campaign, "wqp", [
        "ts_mean(hardsig_a, 5)", "ts_mean(hardsig_b, 5)", "ts_mean(hardsig_c, 5)",
        "ts_mean(clean_a, 5)", "ts_mean(clean_b, 5)",
    ])
    out = _run_wave(campaign, "wqp", "--qp-mode", "hard", "--qp-keep", "1")
    assert "hard 筛" in out
    rows = [r for r in _wave_rows_ordered(campaign, "wqp") if r["status"] == "selected"]
    exprs = [r["expression"] for r in rows]
    # 2 条 clean 全入波；hardsig 只保留 --qp-keep 1 条
    assert sum(1 for e in exprs if "clean_" in e) == 2
    assert sum(1 for e in exprs if "hardsig" in e) == 1


def test_p1_prod_risk_orders_saturated_fields_last(campaign):
    """排序语义 = 截断取谁：size 不足时饱和字段表达式先出局（非 dispatch 顺序）。"""
    _install_tool_stubs(campaign)
    _seed_wave(campaign, "wps", [
        "ts_mean(satfield, 5)", "ts_mean(satfield, 22)", "ts_mean(coldfield, 5)",
    ])
    out = _run_wave(campaign, "wps", "--size", "1", "--qp-mode", "off",
                    "--prod-risk-order", "on")
    assert "饱和字段降权" in out
    rows = _wave_rows_ordered(campaign, "wps")
    selected = [r["expression"] for r in rows if r["status"] == "selected"]
    assert selected == ["ts_mean(coldfield, 5)"]  # 截断位给了非饱和表达式



@pytest.fixture
def campaign(tmp_path):
    cdir = tmp_path / "TST"
    (cdir / "config").mkdir(parents=True)
    (cdir / "config" / "settings.json").write_text(
        json.dumps({"region": "TST", "delay": 1, "universe": "TOP500"}), encoding="utf-8")
    (cdir / "config" / "thresholds.json").write_text("{}", encoding="utf-8")
    (tmp_path / "data").mkdir()
    db = str(tmp_path / "data" / "wqb.db")

    sys.path.insert(0, str(REPO / "src"))
    from wqb.store import CampaignStore
    st = CampaignStore(db)
    try:
        st.upsert_expressions("TST", "w1", [{"expression": e, "status": s} for e, s in WAITING]
                              + [{"expression": e, "status": s, "alpha_id": a} for e, s, a in UNTOUCHABLE],
                              dataset="ds1")
        # 别波（表达式必须不同于 w1 候选：全历史去重会把重复候选直接丢弃）
        st.upsert_expressions("TST", "w2", ["ts_mean(open, 5)"], dataset="ds1", status="gem")
    finally:
        st.close()

    env = dict(os.environ)
    env.update({
        "WQB_DB_PATH": db,                 # CampaignStore / RuleStore（经 get_store）
        "WQB_WORKSPACE": str(tmp_path),    # SqliteLedgerStore / WaveResultsStore → <ws>/data/wqb.db
        "WQB_ROOT": str(REPO),             # wqb_store.get_store 据此找 src/wqb（DB 仍走 WQB_DB_PATH）
        "PYTHONIOENCODING": "utf-8",
    })
    return SimpleNamespace(dir=str(cdir), db=db, env=env, Store=CampaignStore)


def _run(c, *extra):
    r = subprocess.run(
        [sys.executable, str(BUILD_WAVE), "--campaign-dir", c.dir, "--from-db",
         "--dataset", "ds1", "--wave", "w1", "--per-bucket", "8",
         "--enhance-diversity", "never", *extra],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=c.env, timeout=600)
    assert r.returncode == 0, f"build_wave 失败 rc={r.returncode}\nSTDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
    return r.stdout + r.stderr


def _rows(c, wave="w1"):
    import sqlite3
    conn = sqlite3.connect(c.db)
    conn.row_factory = sqlite3.Row
    try:
        return {r["expression"]: dict(r)
                for r in conn.execute("SELECT * FROM expressions WHERE region='TST' AND wave=?", (wave,))}
    finally:
        conn.close()


def _wave_meta(c, wave="w1"):
    st = c.Store(c.db)
    try:
        return st.get_ledger("TST", f"wave_meta_{wave}")
    finally:
        st.close()


def _seed_contract(c):
    """活跃 explore_contract（legacy expr 模板，无 skeleton）：auto 模式下必然注入。"""
    rule = {
        "rule_id": "explore_contract_TST_test", "type": "explore_contract", "status": "active",
        "trigger": {"region": "TST"}, "confidence": 1.0, "source": "test",
        "action": {
            "op": "inject_diversity", "required_operators": ["group_backfill", "group_count"],
            "skeleton_quota": {}, "per_batch_min_operators": 1, "expires_after_batches": 10,
            "exempt": ["repair"], "consumed_batches": [], "issued_at": "2026-09-12T00:00:00",
            "factor_templates": {
                "group_backfill": {"expr": CONTRACT_EXPRS[0]},
                "group_count": {"expr": CONTRACT_EXPRS[1]},
            },
        },
    }
    st = c.Store(c.db)
    try:
        st.upsert_methodology_rules("TST", {"version": 1, "rules": [rule]})
    finally:
        st.close()


# ---------------------------------------------------------------------------
# 1. 选波权威化
# ---------------------------------------------------------------------------

def test_build_wave_supersedes_unpicked_waiting_rows_in_same_wave(campaign):
    out = _run(campaign, "--size", "2", "--auto-coverage", "never")
    rows = _rows(campaign)

    assert rows["ts_mean(close, 5)"]["status"] == "selected"
    assert rows["ts_mean(close, 22)"]["status"] == "selected"
    for e in ("ts_mean(close, 66)", "ts_mean(close, 252)"):
        assert rows[e]["status"] == "superseded", (e, rows[e]["status"])
        sc = json.loads(rows[e]["settings_json"])["status_change"]
        assert sc["reason"].startswith("not picked by build_wave 20"), sc
        assert sc["to"] == "superseded" and sc["from"] in ("enhanced", "gem")
    for e, status, _alpha in UNTOUCHABLE:
        assert rows[e]["status"] == status, (e, rows[e]["status"])
    assert rows["ts_mean(close, 504)"]["alpha_id"] == "A1"
    assert _rows(campaign, "w2")["ts_mean(open, 5)"]["status"] == "gem"

    meta = _wave_meta(campaign)
    assert meta["selected"] == 2 and meta["superseded"] == 2
    assert meta["coverage_injected"] == 0 and meta["coverage_signed"] is None
    assert "superseded=2" in out

    # 幂等：同参再跑一遍，selected 不变、没有新的可归档行
    _run(campaign, "--size", "2", "--auto-coverage", "never")
    again = _rows(campaign)
    assert {e: r["status"] for e, r in again.items()} == {e: r["status"] for e, r in rows.items()}
    assert _wave_meta(campaign)["superseded"] == 0


# ---------------------------------------------------------------------------
# 2. --auto-coverage never 真正关闭契约注入（对照 auto 必注入，证明用例有分辨力）
# ---------------------------------------------------------------------------

def test_auto_coverage_never_injects_no_contract_expressions(campaign):
    _seed_contract(campaign)
    out = _run(campaign, "--size", "3", "--auto-coverage", "never")
    rows = _rows(campaign)
    assert not any("group_" in e for e in rows), [e for e in rows if "group_" in e]
    assert sum(1 for r in rows.values() if r["status"] == "selected") == 3 + 1  # 3 picked + 旧选集 120
    meta = _wave_meta(campaign)
    assert meta["coverage_injected"] == 0 and meta["coverage_signed"] is None
    assert "--auto-coverage never" in out


def test_auto_coverage_auto_still_injects_active_contract(campaign):
    """对照组：同一契约在 auto 模式下注入 —— 否则上面的 never 断言是空洞的。"""
    _seed_contract(campaign)
    _run(campaign, "--size", "4", "--auto-coverage", "auto")
    rows = _rows(campaign)
    injected = [e for e in CONTRACT_EXPRS if rows.get(e, {}).get("status") == "selected"]
    assert injected, {e: r["status"] for e, r in rows.items()}
    assert _wave_meta(campaign)["coverage_injected"] >= 1


def _bounded_source(c, target_status=None):
    expressions = [f"ts_mean(total_financing_cash_flow, {n})" for n in (5, 22, 66, 252)]
    st = c.Store(c.db)
    try:
        st.upsert_expressions("TST", "s2_ds1_d1", expressions, dataset="ds1", status="gem")
        if target_status:
            st.upsert_expressions("TST", "w3", expressions[:3], dataset="ds1", status=target_status)
    finally:
        st.close()
    return expressions


def _bounded_run(c, repeat):
    return subprocess.run([sys.executable, str(BUILD_WAVE), "--campaign-dir", c.dir,
        "--from-db", "--dataset", "ds1", "--wave", "w3", "--source-wave", "s2_ds1_d1",
        "--size", "4", "--expected-count", "4", "--max-field-repeat", str(repeat),
        "--auto-coverage", "never", "--enhance-diversity", "never"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=c.env, timeout=60)


def test_declared_four_mechanisms_cannot_silently_shrink_to_three(campaign):
    _bounded_source(campaign)
    failed = _bounded_run(campaign, 3)
    assert failed.returncode != 0
    assert "expected=4 selected=3" in failed.stderr
    assert "max_field_repeat" in failed.stderr
    assert _rows(campaign, "w3") == {}
    assert _wave_meta(campaign, "w3") is None


def test_explicit_source_expands_existing_three_to_four(campaign):
    expected = _bounded_source(campaign, "selected")
    result = _bounded_run(campaign, 4)
    assert result.returncode == 0, result.stdout + result.stderr
    rows = _rows(campaign, "w3")
    assert set(rows) == set(expected)
    assert all(r["status"] == "selected" for r in rows.values())
    assert _wave_meta(campaign, "w3")["selected"] == 4


def test_source_rebuild_does_not_claim_archived_rows_were_selected(campaign):
    _bounded_source(campaign, "superseded")
    before = _rows(campaign, "w3")
    result = _bounded_run(campaign, 4)
    assert result.returncode != 0
    assert "selection-state" in result.stderr
    assert _rows(campaign, "w3") == before
    assert _wave_meta(campaign, "w3") is None


def _plan(c, count=4):
    _bounded_source(c)
    rows = list(_rows(c, "s2_ds1_d1").values())
    plan = {"region": "TST", "dataset": "ds1", "delay": 1, "wave": "w3",
            "source_wave": "s2_ds1_d1", "required": [
                {"source_id": r["id"], "expression": r["expression"],
                 "role": "hypothesis" if i % 2 == 0 else "control",
                 "mechanism": f"question_{i // 2}", "rationale": "predeclared comparison"}
                for i, r in enumerate(rows[:count])]}
    _write_plan(c, plan)
    return plan


def _write_plan(c, plan):
    st = c.Store(c.db)
    try:
        st.upsert_ledger("TST", "selection_w3", plan)
    finally:
        st.close()


def _planned_run(c, *extra):
    return subprocess.run([sys.executable, str(BUILD_WAVE), "--campaign-dir", c.dir,
        "--from-db", "--dataset", "ds1", "--wave", "w3", "--size", "12",
        "--max-field-repeat", "12", "--auto-coverage", "never",
        "--enhance-diversity", "never", "--selection-contract-key", "selection_w3", *extra],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=c.env, timeout=60)


def test_plan_derives_count_and_preserves_unselected_source(campaign):
    plan = _plan(campaign, 2)
    before = _rows(campaign, "s2_ds1_d1")
    result = _planned_run(campaign)
    assert result.returncode == 0, result.stdout + result.stderr
    assert set(_rows(campaign, "w3")) == {r["expression"] for r in plan["required"]}
    assert _rows(campaign, "s2_ds1_d1") == before
    meta = _wave_meta(campaign, "w3")
    assert meta["expected_count"] == 2 and meta["requested_size"] == 12
    assert meta["selection_mode"] == "reviewed_plan"
    deferred = [r for r in meta["selection_audit"] if r["decision"] == "deferred"]
    assert len(deferred) == 2 and all(r["reason"] == "outside_reviewed_plan" for r in deferred)


@pytest.mark.parametrize("problem", ["missing", "replaced", "wrong_dataset", "wrong_delay",
                                    "duplicate", "archived", "simulated", "quota", "capacity",
                                    "count", "enhancement", "extra_target"])
def test_reviewed_plan_never_silently_changes_experiment(campaign, problem):
    plan = _plan(campaign)
    extra = []
    if problem == "missing":
        plan["required"][0]["source_id"] = 999999
    elif problem == "replaced":
        # Same count and valid ID; different expression identity must still fail.
        plan["required"][0]["expression"] = "ts_mean(total_financing_cash_flow, 999)"
    elif problem == "wrong_dataset":
        plan["dataset"] = "other"
    elif problem == "wrong_delay":
        plan["delay"] = 0
    elif problem == "duplicate":
        plan["required"][1] = plan["required"][0].copy()
    elif problem in ("archived", "simulated", "extra_target"):
        st = campaign.Store(campaign.db)
        try:
            if problem == "extra_target":
                st.upsert_expressions("TST", "w3", ["rank(unplanned_field)"],
                                      dataset="ds1", status="selected")
            else:
                st.connection.execute("UPDATE expressions SET status=?,alpha_id=? WHERE id=?",
                    ("superseded" if problem == "archived" else "gem",
                     "A123" if problem == "simulated" else None, plan["required"][0]["source_id"]))
                st.connection.commit()
        finally:
            st.close()
    else:
        extra = {"quota": ["--max-field-repeat", "3"], "capacity": ["--size", "3"],
                 "count": ["--expected-count", "8"],
                 "enhancement": ["--enhance-diversity", "always"]}[problem]
    _write_plan(campaign, plan)
    before = _rows(campaign, "w3")
    result = _planned_run(campaign, *extra)
    assert result.returncode != 0, result.stdout
    assert "selection-" in result.stderr, result.stderr
    assert _rows(campaign, "w3") == before
    assert _wave_meta(campaign, "w3") is None


def test_capacity_mode_can_legitimately_select_less_without_exact_contract(campaign):
    _bounded_source(campaign)
    result = subprocess.run([sys.executable, str(BUILD_WAVE), "--campaign-dir", campaign.dir,
        "--from-db", "--dataset", "ds1", "--wave", "w3", "--source-wave", "s2_ds1_d1",
        "--size", "8", "--max-field-repeat", "3", "--auto-coverage", "never",
        "--enhance-diversity", "never"], capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=campaign.env, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    assert len(_rows(campaign, "w3")) == 3
    meta = _wave_meta(campaign, "w3")
    assert meta["expected_count"] is None and meta["selection_shortfall"] == 5
    assert meta["selection_audit"][-1]["reason"] == "max_field_repeat"


@pytest.mark.parametrize("group", ["industry", "subindustry"])
def test_shared_group_axis_does_not_exhaust_signal_field_quota(campaign, group):
    st = campaign.Store(campaign.db)
    try:
        st.upsert_expressions("TST", "s2_ds1_d1",
            [f"group_rank(ts_backfill(distinct_signal_{i},252),{group})" for i in range(4)],
            dataset="ds1", status="gem")
    finally:
        st.close()
    plan = {"region": "TST", "dataset": "ds1", "delay": 1, "wave": "w3",
            "source_wave": "s2_ds1_d1", "required": [
                {"source_id": r["id"], "expression": r["expression"],
                 "mechanism": f"independent_{i}", "role": "hypothesis",
                 "rationale": "distinct signal with shared industry grouping"}
                for i, r in enumerate(_rows(campaign, "s2_ds1_d1").values())]}
    _write_plan(campaign, plan)
    result = _planned_run(campaign, "--max-field-repeat", "3")
    assert result.returncode == 0, result.stdout + result.stderr
    assert len(_rows(campaign, "w3")) == 4
    assert _wave_meta(campaign, "w3")["selection_rejections"] == {}
