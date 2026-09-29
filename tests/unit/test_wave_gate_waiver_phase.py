# -*- coding: utf-8 -*-
"""wave_gate 的逃生口 → waiver 检查（skills 审查 X-8）：用了 --skip-* 等逃生口就得有 waiver，
缺省 warn 只告警、enforce 拒绝；用了逃生口的事实必须进首屏，不能静默。"""
import argparse
import datetime as dt
import json
import os
import sqlite3
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "src"))

import wave_gate  # noqa: E402


def _args(**kw):
    base = dict(skip_diversity_gate=False, skip_semantic_gate=False, semantic_gate=None,
                prod_family_gate=True, gate_mode=None, wave="0", waiver_mode=None, region="KOR")
    base.update(kw)
    return argparse.Namespace(**base)


class _RG:
    """区域闸模块的最小替身：resolve_mode / default_mode。"""
    def __init__(self, resolved="warn", default="warn"):
        self._r, self._d = resolved, default

    def resolve_mode(self, cli):
        return (cli or self._r), "note"

    def default_mode(self):
        return self._d


@pytest.fixture()
def db(tmp_path, monkeypatch):
    path = tmp_path / "w.db"
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE ledger_kv (region TEXT, key TEXT, value TEXT, "
                 "created_at TEXT, updated_at TEXT, PRIMARY KEY (region, key))")
    conn.commit()
    monkeypatch.setenv("WQB_DB_PATH", str(path))
    monkeypatch.delenv("WQB_SEM_MODE", raising=False)
    monkeypatch.delenv("WQB_WAIVER_MODE", raising=False)
    yield conn
    conn.close()


def _put_waiver(conn, gate, region="KOR", wave="all", **kw):
    today = dt.date.today()
    v = {"gate": gate, "reason_code": "REPAIR_BATCH", "reason": "repair 批", "approved_by": "agent",
         "created_at": today.isoformat(), "expires_at": (today + dt.timedelta(days=2)).isoformat()}
    v.update(kw)
    conn.execute("INSERT INTO ledger_kv (region, key, value) VALUES (?,?,?)",
                 (region, f"waiver_{gate}_{region}_{wave}", json.dumps(v)))
    conn.commit()


def test_no_escape_hatch_means_no_check(db, capsys):
    assert wave_gate._waiver_phase(_args(), "tracking/KOR", "KOR", "warn", _RG()) == []
    assert capsys.readouterr().out == ""


def test_escape_hatch_without_waiver_warns_on_first_screen_but_proceeds(db, capsys):
    got = wave_gate._waiver_phase(_args(skip_diversity_gate=True, skip_semantic_gate=True),
                                  "tracking/KOR", "KOR", "warn", _RG())
    out = capsys.readouterr()
    assert {d.gate for d in got} == {"diversity", "semantic"} and all(d.ok for d in got)
    assert "无 waiver 记录" in out.out and "waiver_diversity_KOR_all" in out.out
    assert out.err == ""


def test_escape_hatch_with_active_waiver_is_named_in_banner(db, capsys):
    _put_waiver(db, "diversity")
    got = wave_gate._waiver_phase(_args(skip_diversity_gate=True), "tracking/KOR", "KOR", "warn", _RG())
    out = capsys.readouterr().out
    assert got[0].waiver is not None and got[0].waiver.active
    assert "已有 waiver" in out and "REPAIR_BATCH/agent" in out


def test_enforce_mode_exits_2_without_waiver_and_passes_with_it(db, capsys):
    with pytest.raises(SystemExit) as e:
        wave_gate._waiver_phase(_args(skip_semantic_gate=True, waiver_mode="enforce"),
                                "tracking/KOR", "KOR", "warn", _RG())
    assert e.value.code == 2
    assert "拒绝开波" in capsys.readouterr().err
    _put_waiver(db, "semantic", reason_code="NO_INPUT_AVAILABLE", evidence="classify 无描述文")
    got = wave_gate._waiver_phase(_args(skip_semantic_gate=True, waiver_mode="enforce"),
                                  "tracking/KOR", "KOR", "warn", _RG())
    assert got[0].ok


def test_env_waiver_mode_enforce(db, monkeypatch):
    monkeypatch.setenv("WQB_WAIVER_MODE", "enforce")
    with pytest.raises(SystemExit):
        wave_gate._waiver_phase(_args(skip_diversity_gate=True), "tracking/KOR", "KOR", "warn", _RG())


def test_wave_specific_waiver_does_not_cover_other_waves(db):
    _put_waiver(db, "diversity", wave="31")
    a = _args(skip_diversity_gate=True, wave="32", waiver_mode="enforce")
    with pytest.raises(SystemExit):
        wave_gate._waiver_phase(a, "tracking/KOR", "KOR", "warn", _RG())
    a = _args(skip_diversity_gate=True, wave="31", waiver_mode="enforce")
    assert wave_gate._waiver_phase(a, "tracking/KOR", "KOR", "warn", _RG())[0].ok


@pytest.mark.parametrize("kw,inspect_mode,gate", [
    ({"semantic_gate": "off"}, "warn", "semantic"),
    ({"prod_family_gate": False}, "warn", "prod_family"),
    ({}, "off", "inspect"),
])
def test_each_escape_hatch_maps_to_its_gate(db, kw, inspect_mode, gate):
    got = wave_gate._waiver_phase(_args(**kw), "tracking/KOR", "KOR", inspect_mode, _RG())
    assert [d.gate for d in got] == [gate]


def test_sem_mode_env_off_counts_but_explicit_cli_mode_overrides(db, monkeypatch):
    monkeypatch.setenv("WQB_SEM_MODE", "off")
    assert [d.gate for d in wave_gate._waiver_phase(_args(), "c", "KOR", "warn", _RG())] == ["semantic"]
    assert wave_gate._waiver_phase(_args(semantic_gate="enforce"), "c", "KOR", "warn", _RG()) == []


def test_region_gate_downgrade_is_an_escape_only_after_the_sunset(db):
    # 灰度期缺省 warn：不是逃生口
    assert wave_gate._waiver_phase(_args(), "c", "KOR", "warn", _RG("warn", "warn")) == []
    # 灰度期结束后（缺省 enforce）显式回退 warn / off：是逃生口
    got = wave_gate._waiver_phase(_args(gate_mode="warn"), "c", "KOR", "warn", _RG("warn", "enforce"))
    assert [d.gate for d in got] == ["region_gates"]
    got = wave_gate._waiver_phase(_args(gate_mode="off"), "c", "KOR", "warn", _RG("off", "warn"))
    assert [d.gate for d in got] == ["region_gates"]
    # 显式 enforce 不是
    assert wave_gate._waiver_phase(_args(gate_mode="enforce"), "c", "KOR", "warn", _RG("enforce", "enforce")) == []


def test_waiver_mode_off_skips_the_lookup(db, capsys):
    got = wave_gate._waiver_phase(_args(skip_diversity_gate=True, waiver_mode="off"),
                                  "c", "KOR", "warn", _RG())
    assert got[0].ok and "未检查" in capsys.readouterr().out


def test_unreadable_db_is_reported_and_enforce_fails_closed(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WQB_DB_PATH", str(tmp_path / "missing.db"))
    got = wave_gate._waiver_phase(_args(skip_diversity_gate=True), "c", "KOR", "warn", _RG())
    assert got[0].ok and "台账不可读" in capsys.readouterr().err
    with pytest.raises(SystemExit):
        wave_gate._waiver_phase(_args(skip_diversity_gate=True, waiver_mode="enforce"),
                                "c", "KOR", "warn", _RG())


def test_cli_declares_waiver_mode_flag():
    src = open(os.path.join(REPO, "tools", "wave_gate.py"), encoding="utf-8").read()
    assert '"--waiver-mode"' in src and "_waiver_phase(a, campaign" in src
    assert 'report["waivers"]' in src
