# -*- coding: utf-8 -*-
"""S6→S0 饱和反馈写入口（skills 审查 RA-113 / IX-20）：`saturated_datasets` 此前只有读取方。

守两件事：① 合并语义（并入 / 更新 / 撤销，不丢已有条目）；② 写入形状能被 S0 的
`apply_saturation_demotion` 读回并降级（写入方与读取方对得上，防止再次出现「有读无写」）。
"""
import asyncio
import importlib.util
import json
import os
import sqlite3
import sys
import types

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _load_ci():
    spec = importlib.util.spec_from_file_location("campaign_intel_ms", os.path.join(REPO, "tools", "campaign_intel.py"))
    m = importlib.util.module_from_spec(spec)
    sys.modules["campaign_intel_ms"] = m
    spec.loader.exec_module(m)
    return m


def _load_score_datasets():
    path = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts", "score_datasets.py")
    scripts = os.path.dirname(path)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location("score_datasets_ms", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_merge_adds_updates_and_removes_without_dropping_others():
    ci = _load_ci()
    v1, ch1 = ci._merge_saturated({}, ["ds_a", "ds_b"], reason="prod≥0.9", wave="12", prod_corr=0.93, now="t1")
    assert sorted(ch1) == [("added", "ds_a"), ("added", "ds_b")]
    assert v1["datasets"]["ds_a"] == {"reason": "prod≥0.9", "updated": "t1", "source_wave": "12", "prod_corr": 0.93}

    v2, ch2 = ci._merge_saturated(v1, ["ds_a", "ds_c"], reason="again", now="t2")
    assert sorted(ch2) == [("added", "ds_c"), ("updated", "ds_a")]
    assert set(v2["datasets"]) == {"ds_a", "ds_b", "ds_c"}          # 已有条目不丢
    assert v2["datasets"]["ds_a"]["reason"] == "again"

    v3, ch3 = ci._merge_saturated(v2, ["ds_b", "nope"], remove=True)
    assert ch3 == [("removed", "ds_b")]                               # 不存在的 remove 静默忽略
    assert set(v3["datasets"]) == {"ds_a", "ds_c"}


def test_merge_tolerates_malformed_existing_value():
    ci = _load_ci()
    for bad in (None, [], "x", {"datasets": "oops"}):
        v, ch = ci._merge_saturated(bad, ["ds_a"], reason="r", now="t")
        assert set(v["datasets"]) == {"ds_a"} and ch == [("added", "ds_a")]


def _mk_db(path):
    con = sqlite3.connect(path)
    con.executescript(
        """
        CREATE TABLE ledger_kv (
            id INTEGER PRIMARY KEY AUTOINCREMENT, region VARCHAR(50) NOT NULL, key VARCHAR(200) NOT NULL,
            value JSON NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(region, key));
        """)
    con.commit()
    con.close()


def _args(**kw):
    base = dict(region="EUR", dataset=["model26"], reason="prod 墙", wave="12", prod_corr=0.91,
                remove=False, write_ledger=False)
    base.update(kw)
    return types.SimpleNamespace(**base)


def test_cmd_dry_run_then_write_then_remove(tmp_path, monkeypatch):
    ci = _load_ci()
    db = str(tmp_path / "wqb.db")
    _mk_db(db)
    monkeypatch.setenv("WQB_DB_PATH", db)

    def rows():
        con = sqlite3.connect(db)
        try:
            return con.execute("SELECT value FROM ledger_kv WHERE key='saturated_datasets'").fetchall()
        finally:
            con.close()

    assert asyncio.run(ci._cmd_mark_saturated(_args())) == 0
    assert rows() == []                                              # 缺省 dry-run 不写库

    assert asyncio.run(ci._cmd_mark_saturated(_args(write_ledger=True))) == 0
    val = json.loads(rows()[0][0])
    assert val["datasets"]["model26"]["reason"] == "prod 墙"

    assert asyncio.run(ci._cmd_mark_saturated(_args(dataset=["model26"], remove=True, write_ledger=True))) == 0
    assert json.loads(rows()[0][0])["datasets"] == {}


def test_cmd_requires_dataset_and_reason(tmp_path, monkeypatch):
    ci = _load_ci()
    db = str(tmp_path / "wqb.db")
    _mk_db(db)
    monkeypatch.setenv("WQB_DB_PATH", db)
    assert asyncio.run(ci._cmd_mark_saturated(_args(dataset=[]))) == 1
    assert asyncio.run(ci._cmd_mark_saturated(_args(reason=""))) == 1


def test_written_shape_is_consumed_by_s0_saturation_demotion():
    """写入形状 → S0 读取方：命中集降 excluded 并带 tier_note，未命中集不动。"""
    ci = _load_ci()
    sd = _load_score_datasets()
    val, _ = ci._merge_saturated({}, ["model26"], reason="prod 墙 0.93", wave="12", prod_corr=0.93, now="t")
    rows = [{"id": "model26", "tier": "tier1"}, {"id": "pv1", "tier": "tier1"}]
    n = sd.apply_saturation_demotion(rows, val["datasets"], {"saturation_demotion_enable": True})
    assert n == 1
    assert rows[0]["tier"] == "excluded" and rows[0]["tier_note"].startswith("saturated:prod 墙")
    assert rows[1]["tier"] == "tier1"
