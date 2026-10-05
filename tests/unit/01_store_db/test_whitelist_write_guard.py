# -*- coding: utf-8 -*-
"""`s0_whitelist` 写入守卫（2026-10-01，KOR risk70 事故修法）的回归护栏。

契约：upsert_ledger_key 写 s0_whitelist 后，把 datasets 与判死证据求交（本区整集死/饱和/
跨区 ≥2 区 = high；跨区 1 区 = medium；本区族级死 = low），命中即在返回值带
`dead_intersection`——**非阻断**（写成功 + 告警并存），异常 fail-open 不影响写入。
"""
import importlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
for _p in (REPO, REPO / "src", REPO / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402


@pytest.fixture
def mcp(tmp_path, monkeypatch):
    db_path = tmp_path / "wqb.db"
    CampaignStore(str(db_path)).close()
    conn = sqlite3.connect(str(db_path))
    # 本区 TST：model1 整集判死（ledger）+ sat1 饱和 + fam1 族级死（registry）
    conn.execute("INSERT INTO ledger_kv (region, key, value, updated_at) VALUES ('TST','model1_dead','{}','2026-10-01')")
    conn.execute("INSERT INTO ledger_kv (region, key, value, updated_at) VALUES ('TST','saturated_datasets',?,'2026-10-01')",
                 (json.dumps({"datasets": {"sat1": {"reason": "prod 饱和"}}}),))
    conn.execute("INSERT INTO registry_empirical (region, layer, entry_id, payload, updated_at) "
                 "VALUES ('TST','dead_end','TST-FAM-DEAD',?,'2026-09-30')",
                 (json.dumps({"id": "TST-FAM-DEAD", "family": "f", "reason": "r", "rule": "u",
                              "dataset": "fam1"}),))
    # 跨区：xds 在 R1+R2 两区判死（high）；yds 只在 R1（medium）
    for reg in ("R1", "R2"):
        conn.execute("INSERT INTO registry_empirical (region, layer, entry_id, payload, updated_at) "
                     "VALUES (?,'dead_end',?,?,'2026-09-30')",
                     (reg, f"{reg}-XDS-DEAD", json.dumps({"id": "x", "family": "f", "reason": "r",
                                                          "rule": "u", "dataset": "xds"})))
    conn.execute("INSERT INTO registry_empirical (region, layer, entry_id, payload, updated_at) "
                 "VALUES ('R1','dead_end','R1-YDS-DEAD',?,'2026-09-30')",
                 (json.dumps({"id": "y", "family": "f", "reason": "r", "rule": "u", "dataset": "yds"}),))
    # zds：只在 entry_id 词元里出现（payload 不绑 dataset）——跨区扫描的第二条证据路
    for reg in ("R3", "R4"):
        conn.execute("INSERT INTO registry_empirical (region, layer, entry_id, payload, updated_at) "
                     "VALUES (?,'dead_end',?,?,'2026-09-30')",
                     (reg, f"{reg}-ZDS-NO-SIGNAL", json.dumps({"id": "z", "family": "zds 族",
                                                               "reason": "r", "rule": "u"})))
    conn.commit()
    conn.close()
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    mod.set_db_path(db_path)        # 读写同源；隔离失效由 get_db_path() 的结果闸兜住
    return mod


def _write(mcp, datasets):
    return mcp.upsert_ledger_key(region="TST", key="s0_whitelist",
                                 value={"datasets": datasets, "_schema_from": "whitelist"})


def test_hits_all_severity_tiers_and_write_still_succeeds(mcp):
    out = _write(mcp, ["good1", "model1", "sat1", "xds", "yds", "fam1"])
    assert out["action"] == "inserted"                          # 非阻断：写成功
    hits = {(h["dataset"], h["kind"], h["severity"]) for h in out["dead_intersection"]["hits"]}
    assert ("model1", "local_dead", "high") in hits
    assert ("sat1", "local_saturated", "high") in hits
    assert ("xds", "xregion_dead", "high") in hits              # 跨区 ≥2 区
    assert ("yds", "xregion_weak", "medium") in hits            # 跨区恰 1 区
    assert ("fam1", "local_family_dead", "low") in hits
    assert not any(h[0] == "good1" for h in hits)               # 干净集不出现在告警里
    assert out["dead_intersection"]["n_high"] == 3


def test_entry_id_token_matching_catches_unbound_xregion_deaths(mcp):
    """payload 没绑 dataset、只在 entry_id 里出现的跨区判死也能捞到（词元精确匹配）。"""
    out = _write(mcp, ["zds"])
    hits = out["dead_intersection"]["hits"]
    assert [ (h["kind"], h["severity"]) for h in hits ] == [("xregion_dead", "high")]


def test_clean_whitelist_has_no_guard_key(mcp):
    out = _write(mcp, ["good1", "good2"])
    assert out["action"] == "inserted" and "dead_intersection" not in out


def test_guard_does_not_touch_other_keys(mcp):
    out = mcp.upsert_ledger_key(region="TST", key="model1_dead", value={"note": "x"})
    assert out["action"] in ("inserted", "updated") and "dead_intersection" not in out


def test_guard_is_fail_open(mcp, monkeypatch):
    import wqb.ledger_whitelist as lw
    monkeypatch.setattr(lw, "normalize", lambda _v: (_ for _ in ()).throw(RuntimeError("boom")))
    out = _write(mcp, ["model1"])                               # 归一化炸了也只丢告警
    assert out["action"] in ("inserted", "updated") and "dead_intersection" not in out
