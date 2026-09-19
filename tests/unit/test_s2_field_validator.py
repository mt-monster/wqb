# -*- coding: utf-8 -*-
"""s2_field_validator：S1 候选池成员校验（2026-09-13 S1↔S2 接力修复）。

背景：该闸长期读 S1 ledger 的 `main_candidates` 键，而现行 S1 节点/S2 回写
都只产 `field_whitelist`/`candidate_field_pool` → 闸永远静默"跳过校验"。

覆盖功能点：
1. field_whitelist 命中 → 池内占比判定（池内 pass / 池外 majority fail）；
2. candidate_field_pool 与历史 main_candidates 键的回退兼容；
3. 无 S1 记录时不阻塞（pass=True）；
4. risk_notes 禁用字段命中 → FAIL。
"""

import json
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import s2_field_validator as V  # noqa: E402


def _make_db(tmp_path, region, key, value, name="wqb.db"):
    db = tmp_path / name
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE ledger_kv (region TEXT, key TEXT, value TEXT)")
    conn.execute(
        "INSERT INTO ledger_kv (region, key, value) VALUES (?,?,?)",
        (region, key, json.dumps(value, ensure_ascii=False)),
    )
    conn.commit()
    conn.close()
    return str(db)


def test_wave_inside_pool_passes(tmp_path):
    db = _make_db(tmp_path, "GLB", "s1_f23_d1", {"field_whitelist": ["fnd_a", "fnd_b", "fnd_c"]})
    r = V.validate_wave_fields("GLB", "w1", "f23", ["rank(fnd_a)", "ts_mean(fnd_b, 22)"], db)
    assert r["pass"] is True
    assert r["coverage"] == 1.0
    assert r["extra"] == []
    assert r["s1_key"] == "s1_f23_d1"
    assert "池内占比" in r["message"]


def test_wave_outside_pool_fails(tmp_path):
    db = _make_db(tmp_path, "GLB", "s1_f23_d1", {"field_whitelist": ["fnd_a"]})
    r = V.validate_wave_fields("GLB", "w1", "f23", ["rank(rogue_x)", "rank(rogue_y)"], db)
    assert r["pass"] is False
    assert r["coverage"] == 0.0
    assert set(r["extra"]) == {"rogue_x", "rogue_y"}


def test_pool_key_fallbacks(tmp_path):
    """candidate_field_pool / 历史 main_candidates 键均可命中。"""
    db = _make_db(tmp_path, "GLB", "s1_f23_d1", {"candidate_field_pool": ["fnd_a"]})
    r = V.validate_wave_fields("GLB", "w1", "f23", ["rank(fnd_a)"], db)
    assert r["pass"] is True and r["coverage"] == 1.0

    db2 = _make_db(tmp_path, "GLB", "s1_f24_d1", {"main_candidates": ["fnd_z"]}, name="wqb2.db")
    r2 = V.validate_wave_fields("GLB", "w1", "f24", ["rank(fnd_z)"], db2)
    assert r2["pass"] is True and r2["coverage"] == 1.0
    assert r2["s1_key"] == "s1_f24_d1"


def test_no_s1_record_non_blocking(tmp_path):
    db = _make_db(tmp_path, "GLB", "s1_other_d1", {"field_whitelist": ["x_a"]})
    r = V.validate_wave_fields("GLB", "w1", "f23", ["rank(anything)"], db)
    assert r["pass"] is True
    assert "跳过校验" in r["message"]


def test_forbidden_field_blocks(tmp_path):
    db = _make_db(
        tmp_path, "GLB", "s1_f23_d1",
        {"field_whitelist": ["revise_value_x", "fnd_a"], "risk_notes": "revise_value family dead"},
    )
    r = V.validate_wave_fields("GLB", "w1", "f23", ["rank(revise_value_x)"], db)
    assert r["pass"] is False
    assert r["forbidden"] == ["revise_value_x"]
