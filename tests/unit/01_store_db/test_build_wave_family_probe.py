# -*- coding: utf-8 -*-
"""build_wave 族维度断流修复的回归（2026-10-01 P0/P1/P3）。

背景（步 4 S2 评估发现）：
  - 断流①：--from-db 主路径下 a.file=None、无 meta 文件 → load_family_map 恒返回 {}
    → 「每族 cap」静默失效。全库 15650 条 gem 行 family 列为空。
  - 断流②：「探针先于扩批」无机检。

修复：
  - P0：expressions 加 family 列；GEM 落库带 family；load_family_map 支持 DB 兜底。
  - P1：选波时该族「尚无已回测行」→ 该族 cap 收紧为 probe_cap（默认 1）。
  - P3：有 family 数据却读不到时打 WARN。

端到端：子进程跑真 build_wave.py，隔离工作区，绝不碰真库。
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO = Path(__file__).resolve().parents[3]
BUILD_WAVE = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts" / "build_wave.py"


def _seed(c, wave, items):
    st = c.Store(c.db)
    try:
        st.upsert_expressions("TST", wave, items, dataset="ds1", status="gem")
    finally:
        st.close()


def _run(c, wave, *extra):
    r = subprocess.run(
        [sys.executable, str(BUILD_WAVE), "--campaign-dir", c.dir, "--from-db",
         "--dataset", "ds1", "--wave", wave, "--per-bucket", "8",
         "--enhance-diversity", "never", "--auto-coverage", "never", *extra],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=c.env, timeout=600)
    assert r.returncode == 0, f"build_wave 失败 rc={r.returncode}\nSTDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
    return r.stdout + r.stderr


def _selected(c, wave):
    import sqlite3
    conn = sqlite3.connect(c.db)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM expressions WHERE region='TST' AND wave=? AND status='selected' "
            "ORDER BY id", (wave,))]
    finally:
        conn.close()


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
        # w1：给 family 锚点用的空波（避免 build_wave 因无候选报错的情形不在此触发）
        st.upsert_expressions("TST", "anchor", ["ts_mean(volume, 3)"], dataset="ds1", status="gem")
    finally:
        st.close()

    env = dict(os.environ)
    env.update({
        "WQB_DB_PATH": db,
        "WQB_WORKSPACE": str(tmp_path),
        "WQB_ROOT": str(REPO),
        "PYTHONIOENCODING": "utf-8",
    })
    return SimpleNamespace(dir=str(cdir), db=db, env=env, Store=CampaignStore)


# ---------------------------------------------------------------------------
# P0：family 从 DB 读取生效
# ---------------------------------------------------------------------------

def test_family_loaded_from_db_makes_family_cap_effective(campaign):
    """有 family 标签时，load_family_map 从 DB 读回，族 cap 生效。"""
    # 同族 cs_rel 放 8 条（size=4 时 max_per_family=max(2,4//6)=2 → 该族最多 2 条）
    items = [{"expression": f"group_rank(close_{i}, sector)", "family": "cs_rel"} for i in range(8)]
    _seed(campaign, "wfam", items)
    out = _run(campaign, "wfam", "--size", "4")
    assert "DB 载入" in out and "family 标签" in out, out
    sel = _selected(campaign, "wfam")
    fams = [r["family"] for r in sel]
    assert fams and all(f == "cs_rel" for f in fams)
    assert len([f for f in fams if f == "cs_rel"]) <= 2, fams  # 族 cap 生效（size//6=2）


def test_family_absent_no_crash_and_no_warn(campaign):
    """无 family 标签时不炸，也不误报 family 降级 WARN（库内本就没有 family 数据）。"""
    _seed(campaign, "wnofam", ["group_rank(close, sector)"])
    out = _run(campaign, "wnofam", "--size", "4")
    assert "[family] ⚠ WARN" not in out, out
    assert _selected(campaign, "wnofam")


# ---------------------------------------------------------------------------
# P1：探针先于扩批
# ---------------------------------------------------------------------------

def test_probe_cap_limits_unbacktested_family(campaign):
    """某族全部未回测 → 本波该族最多选 1 条（探针）。"""
    items = [{"expression": f"ts_mean(close_{i}, 5)"} for i in range(6)]
    # 手动打 family（模拟 GEM 落库带 family）
    st = campaign.Store(campaign.db)
    try:
        st.upsert_expressions("TST", "wprobe",
                              [{"expression": x["expression"], "family": "ts_chg"} for x in items],
                              dataset="ds1", status="gem")
    finally:
        st.close()
    out = _run(campaign, "wprobe", "--size", "6")
    assert "探针优先" in out, out
    sel = _selected(campaign, "wprobe")
    assert len(sel) == 1, [r["expression"] for r in sel]  # 只放 1 条探针


def test_probe_gate_off_restores_old_behavior(campaign):
    """WQB_PROBE_GATE=off 时恢复旧行为（族 cap 生效但不收紧为探针）。"""
    st = campaign.Store(campaign.db)
    try:
        st.upsert_expressions("TST", "wprobeoff",
                              [{"expression": f"ts_mean(open_{i}, 5)", "family": "ts_chg"} for i in range(6)],
                              dataset="ds1", status="gem")
    finally:
        st.close()
    env = dict(campaign.env)
    env["WQB_PROBE_GATE"] = "off"
    r = subprocess.run(
        [sys.executable, str(BUILD_WAVE), "--campaign-dir", campaign.dir, "--from-db",
         "--dataset", "ds1", "--wave", "wprobeoff", "--size", "6", "--per-bucket", "8",
         "--enhance-diversity", "never", "--auto-coverage", "never"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=env, timeout=600)
    assert r.returncode == 0, r.stderr
    out = r.stdout + r.stderr
    assert "探针优先" not in out, out
    sel = _selected(campaign, "wprobeoff")
    # 旧行为：族 cap = max(2, 6//6)=2 → 选 2 条
    assert len(sel) == 2, [x["expression"] for x in sel]


def test_family_with_backtested_row_allows_expansion(campaign):
    """该族已有已回测行（在历史波）→ 不受探针限制，可扩批（回到普通族 cap）。"""
    st = campaign.Store(campaign.db)
    try:
        # 历史波放 1 条已回测行（作为该族「已验证」的证据；不参与本波选取）
        st.upsert_expressions("TST", "w_hist",
                              [{"expression": "ts_rank(v_hist, 22)", "family": "momentum",
                                "alpha_id": "A_EXIST"}],
                              dataset="ds1", status="backtested")
        # 本波候选：同族、全未回测
        st.upsert_expressions("TST", "wexp",
                              [{"expression": f"ts_rank(v_{i}, 22)", "family": "momentum"} for i in range(5)],
                              dataset="ds1", status="gem")
    finally:
        st.close()
    out = _run(campaign, "wexp", "--size", "6")
    # 该族有已回测行 → 不应触发探针收紧
    assert "探针优先" not in out, out
    sel = _selected(campaign, "wexp")
    # 普通族 cap = max(2, 6//6)=2
    assert len(sel) == 2, [x["expression"] for x in sel]


# ---------------------------------------------------------------------------
# store 层契约：family 落库 + COALESCE 保底
# ---------------------------------------------------------------------------

def test_upsert_family_roundtrip_and_coalesce_guard(tmp_path):
    """family 落库/读取正确；UPDATE 不带 family 时保留原值（COALESCE 保底）。"""
    sys.path.insert(0, str(REPO / "src"))
    from wqb.store import CampaignStore
    st = CampaignStore(str(tmp_path / "f.db"))
    try:
        q = "SELECT family, alpha_id FROM expressions WHERE expression='rank(close)'"
        st.upsert_expressions("IND", "w1", [{"expression": "rank(close)", "family": "cs_rel"}],
                              dataset="ds1", status="gem")
        assert st.connection.execute(q).fetchone()["family"] == "cs_rel"
        # 回测回写（不带 family）→ 保留
        st.upsert_expressions("IND", "w1",
                              [{"expression": "rank(close)", "alpha_id": "A1", "status": "backtested"}],
                              dataset="ds1")
        r = st.connection.execute(q).fetchone()
        assert r["family"] == "cs_rel" and r["alpha_id"] == "A1"
        # 显式改 family → 覆盖
        st.upsert_expressions("IND", "w1", [{"expression": "rank(close)", "family": "ts_chg"}],
                              dataset="ds1", status="gem")
        assert st.connection.execute(q).fetchone()["family"] == "ts_chg"
    finally:
        st.close()


def test_columns_include_family(tmp_path):
    """expressions 表在首次 upsert 后即具备 family 列（幂等 ALTER）。"""
    sys.path.insert(0, str(REPO / "src"))
    from wqb.store import CampaignStore
    st = CampaignStore(str(tmp_path / "g.db"))
    try:
        st.upsert_expressions("IND", "w1", [{"expression": "rank(close)"}], dataset="ds1", status="gem")
        cols = {r[1] for r in st.connection.execute("PRAGMA table_info(expressions)")}
        assert "family" in cols
    finally:
        st.close()


# ---------------------------------------------------------------------------
# P2：字段池带 L3.5 族结构
# ---------------------------------------------------------------------------

def _seed_catalog_and_semantic(st):
    st.upsert_field_catalog("TST", {
        "dataset": "ds1",
        "fields": [
            {"field_name": "mdl264_eps_sur", "description": "earnings surprise", "alpha_count": 500},
            {"field_name": "mdl264_eps_sur_decay_l1", "description": "eps decay", "alpha_count": 400},
            {"field_name": "currency_code", "description": "currency code", "alpha_count": 10},
        ],
    })
    st.upsert_ledger("TST", "s1_semantic_ds1", {
        "total_fields": 3,
        "blocked_fields": [{"field": "currency_code", "reason": "货币代码"}],
        "signal_fields": ["mdl264_eps_sur", "mdl264_eps_sur_decay_l1"],
        "families": {
            "mdl264_eps_sur": {
                "n": 2, "kind": "三分类概率",
                "fields": ["mdl264_eps_sur", "mdl264_eps_sur_decay_l1"],
                "roles": [{"field": "mdl264_eps_sur", "role": "level"}],
                "cats": ["analyst"],
            }
        },
    })


def test_economic_pool_carries_families(tmp_path):
    """P2：经济学池 payload 带 families + family_stats（且只含池内族）。"""
    sys.path.insert(0, str(REPO / "src"))
    from wqb.store import CampaignStore
    st = CampaignStore(str(tmp_path / "p2.db"))
    try:
        _seed_catalog_and_semantic(st)
        p = st.build_economic_field_pool("TST", "ds1", persist=False)
        fams = p.get("families") or {}
        assert "mdl264_eps_sur" in fams, fams
        assert fams["mdl264_eps_sur"]["n"] >= 1
        assert p["family_stats"]["available"] is True
        assert p["builder_version"] == 6
    finally:
        st.close()


def test_fallback_pool_carries_families(tmp_path):
    """P2：回退路径（build_candidate_field_pool）同样带族结构，不丢。"""
    sys.path.insert(0, str(REPO / "src"))
    from wqb.store import CampaignStore
    st = CampaignStore(str(tmp_path / "p2f.db"))
    try:
        _seed_catalog_and_semantic(st)
        p = st.build_candidate_field_pool("TST", "ds1", persist=False)
        assert (p.get("families") or {}), p
        assert p.get("family_stats", {}).get("available") is True
    finally:
        st.close()


def test_families_fail_open_without_semantic_ledger(tmp_path):
    """无语义台账时不炸，families 为空 + available=False（fail-open）。"""
    sys.path.insert(0, str(REPO / "src"))
    from wqb.store import CampaignStore
    st = CampaignStore(str(tmp_path / "p2n.db"))
    try:
        st.upsert_field_catalog("TST", {
            "dataset": "ds2",
            "fields": [{"field_name": "f_a", "description": "x", "alpha_count": 5}],
        })
        p = st.build_economic_field_pool("TST", "ds2", persist=False)
        assert p.get("families") == {}
        assert p.get("family_stats", {}).get("available") is False
    finally:
        st.close()
