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
