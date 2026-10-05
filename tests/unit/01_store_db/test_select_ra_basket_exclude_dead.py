# -*- coding: utf-8 -*-
"""select_ra_basket 判死/饱和剔除（2026-10-01 P1 断流修复）的回归护栏。

断流原状：篮子选择不消费判死/饱和台账 → 「IS 过闸但所属集已判死」的候选带进篮子，
烧完步 7 诊断链到步 8 才被 prod 挡掉。修复后**默认开启**（workflow 节点 `inventory_scan`
不传任何标志也会走到），`--no-exclude-dead` 仅供调试。
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
for _p in (REPO, REPO / "src", REPO / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402

import select_ra_basket as sb  # noqa: E402
from wqb.profile_drift import dead_dataset_index  # noqa: E402


@pytest.fixture
def conn(tmp_path):
    db = tmp_path / "wqb.db"
    CampaignStore(str(db)).close()
    c = sqlite3.connect(str(db))
    # 区 + 数据集 + 字段
    c.execute("INSERT INTO regions (id, name) VALUES (1, 'TST')")
    for i, name in ((10, "good_ds"), (11, "dead_ds"), (12, "sat_ds"), (13, "fam_ds")):
        c.execute("INSERT INTO datasets (id, name, region_id) VALUES (?,?,1)", (i, name))
    for did, fname in ((10, "good_field_a"), (11, "dead_field_a"), (12, "sat_field_a"), (13, "fam_field_a")):
        c.execute("INSERT INTO fields (dataset_id, field_name) VALUES (?,?)", (did, fname))
    # 整集判死（ledger *_dead）+ 饱和（saturated_datasets）+ 族级死（registry dead_end 绑定）
    c.execute("INSERT INTO ledger_kv (region, key, value, updated_at) VALUES ('TST','dead_ds_dead','{}','2026-10-01')")
    c.execute("INSERT INTO ledger_kv (region, key, value, updated_at) VALUES ('TST','saturated_datasets',?,'2026-10-01')",
              (json.dumps({"datasets": {"sat_ds": {"reason": "prod 饱和"}}}),))
    c.execute("INSERT INTO registry_empirical (region, layer, entry_id, payload, updated_at) "
              "VALUES ('TST','dead_end','TST-FAM-DEAD',?,'2026-09-30')",
              (json.dumps({"id": "TST-FAM-DEAD", "family": "f", "reason": "r", "rule": "u",
                           "dataset": "fam_ds"}),))
    c.commit()
    yield c
    c.close()


def _cand(aid, code):
    return {"id": aid, "region": "TST", "delay": 1, "code": code, "pyramids": {"list": []}}


def test_dead_dataset_index_three_tiers(conn):
    idx = sb.__dict__ and dead_dataset_index(conn, "TST")
    assert idx["dataset_dead"] == {"dead_ds"}
    assert idx["saturated"] == {"sat_ds"}
    assert idx["family_dead"] == {"fam_ds"}


def test_exclusion_drops_hard_dead_and_saturated_keeps_family_and_unattributed(conn):
    cands = [
        _cand("GOOD", "rank(good_field_a)"),
        _cand("DEAD", "ts_zscore(dead_field_a, 22)"),
        _cand("SAT", "rank(sat_field_a)"),
        _cand("FAM", "rank(fam_field_a)"),          # 族级死：保留但计数
        _cand("UNKN", "rank(zzz_unknown_field)"),   # 查不到归属：fail-open 保留
    ]
    kept, dropped, stats = sb.apply_dead_exclusions(conn, cands)
    assert [c["id"] for c in kept] == ["GOOD", "FAM", "UNKN"]
    assert [d["id"] for d in dropped] == ["DEAD", "SAT"]
    assert dropped[0]["datasets"] == ["dead_ds"] and dropped[1]["datasets"] == ["sat_ds"]
    assert stats["family_dead_hits"] == 1 and stats["unattributed"] == 1


def test_exclusion_is_scoped_per_region(conn):
    """别区判死不影响本区候选（region 作用域）。"""
    other = _cand("X1", "rank(dead_field_a)")
    other["region"] = "USA"                        # USA 无 dead_ds_dead 台账
    kept, dropped, _stats = sb.apply_dead_exclusions(conn, [other])
    assert not dropped and kept[0]["id"] == "X1"


def test_default_on_and_opt_out_flag_registered():
    """默认开启是机制生效的前提（节点不传标志）——回归钉死，防退回 opt-in。"""
    src = (REPO / "tools" / "select_ra_basket.py").read_text(encoding="utf-8")
    assert re.search(r'"--exclude-dead"[^)]*?default=True', src, re.S)
    assert '"--no-exclude-dead"' in src
