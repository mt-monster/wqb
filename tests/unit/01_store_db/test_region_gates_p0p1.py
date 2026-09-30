# -*- coding: utf-8 -*-
"""P0-1 开波闸下沉到 toolkit 入口（2026-09-17）.

背景（实测）：signal_floor / stop_rules / backlog 三道闸原先只由 workflow 的 S2/S3
节点调用，**直调 toolkit 脚本（build_wave.py / wave_gate.py）会完全绕过** ——
实证 JPN 2026-09-16：`_run_backlog_gate` 判定为拦截（conversion=0.0%），该区却照跑
完整波（gem 1,640 / 回测 0）。本模块把闸下沉到开波唯一入口。

本测试覆盖：
  1. `_lib.region_gates.run_region_gates` 的三种模式（off/warn/enforce）语义；
  2. `WQB_DISABLE_REGION_GATES=1` 逃生口；
  3. 破坏性回归：enforce 下必须 ok=False（否则下沉等于没做）；
  4. 2026-09-27：CLI 缺省模式按日期切换（WARN_SUNSET 之后 enforce）与解析优先级。
"""
import datetime
import io
import json
import sqlite3
import sys

import pytest

from wqb.workflow import _common

TK = _common.REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"


@pytest.fixture
def rg():
    if str(TK) not in sys.path:
        sys.path.insert(0, str(TK))
    from _lib import region_gates
    return region_gates


def _setup(tmp_path, monkeypatch, gem=300, backtested=20):
    """造一个"积压超限"的区：gem 远多于 backtested → conversion 低。"""
    campaign = tmp_path / "tracking" / "TESTREG"
    (campaign / "config").mkdir(parents=True)
    (campaign / "config" / "thresholds.json").write_text(
        json.dumps({"diversity": {}}, ensure_ascii=False), encoding="utf-8")

    db = tmp_path / "wqb_test.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE expressions (id INTEGER PRIMARY KEY, region TEXT, status TEXT)")
    conn.execute("CREATE TABLE ledger_kv (region TEXT, key TEXT, value TEXT)")
    conn.execute("CREATE TABLE wave_results (region TEXT, status TEXT, verdict TEXT, "
                 "created_at TEXT, updated_at TEXT)")
    conn.execute("CREATE TABLE backtest_results (id INTEGER PRIMARY KEY, region TEXT, "
                 "sharpe REAL, fitness REAL, wave TEXT)")
    for _ in range(gem):
        conn.execute("INSERT INTO expressions (region, status) VALUES ('TESTREG','gem')")
    for _ in range(backtested):
        conn.execute("INSERT INTO expressions (region, status) VALUES ('TESTREG','backtested')")
    conn.commit()
    conn.close()

    monkeypatch.setenv("WQB_DB_PATH", str(db))
    monkeypatch.setenv("WQB_WORKSPACE_ROOT", str(_common.REPO_ROOT))
    monkeypatch.delenv("WQB_DISABLE_REGION_GATES", raising=False)
    return campaign


def test_off_mode_skips_everything(rg, tmp_path, monkeypatch):
    campaign = _setup(tmp_path, monkeypatch)
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="off", out=io.StringIO())
    assert rep["ok"] is True
    assert rep["skipped_reason"] == "gate-mode=off"
    assert rep["results"] == {}


def test_env_escape_hatch_skips(rg, tmp_path, monkeypatch):
    campaign = _setup(tmp_path, monkeypatch)
    monkeypatch.setenv("WQB_DISABLE_REGION_GATES", "1")
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="enforce", out=io.StringIO())
    assert rep["ok"] is True
    assert "WQB_DISABLE_REGION_GATES" in str(rep["skipped_reason"])


def test_warn_mode_reports_hits_but_allows(rg, tmp_path, monkeypatch):
    """灰度默认：命中积压闸但不阻断（避免一上线就全池停摆）。"""
    campaign = _setup(tmp_path, monkeypatch)
    buf = io.StringIO()
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="warn", out=buf)
    assert rep["ok"] is True, "warn 模式不得阻断"
    assert "backlog" in rep["hits"], "gem 300/320 应命中积压闸"
    text = buf.getvalue()
    assert "灰度" in text and "未拦截" in text or "仅告警不阻断" in text


def test_enforce_mode_blocks(rg, tmp_path, monkeypatch):
    """enforce：同一场景必须 ok=False（这是"下沉"是否真正生效的判据）。"""
    campaign = _setup(tmp_path, monkeypatch)
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="enforce", out=io.StringIO())
    assert rep["ok"] is False
    assert "backlog" in rep["hits"]


def test_clean_region_passes_all_gates(rg, tmp_path, monkeypatch):
    """无积压的区在 enforce 下也应放行（不得误伤）。"""
    campaign = _setup(tmp_path, monkeypatch, gem=0, backtested=300)
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="enforce", out=io.StringIO())
    assert rep["ok"] is True, f"健全区被误拦: {rep.get('hits')}"


def test_load_gates_and_invalid_mode_falls_back(rg, tmp_path, monkeypatch):
    campaign = _setup(tmp_path, monkeypatch)
    C, err = rg.load_gates(str(campaign))
    assert C is not None, f"应能从 campaign_dir 推导工作区根: {err}"
    assert callable(C._run_backlog_gate)
    # 非法 mode 回落到按日期的缺省：灰度期内 = warn（不阻断）
    monkeypatch.setattr(rg, "_today", lambda: BEFORE)
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="bogus", out=io.StringIO())
    assert rep["mode"] == rg.MODE_WARN
    assert rep["ok"] is True


# ---------------------------------------------------------------------------
# 2026-09-27：CLI 缺省模式按日期切换（报告 §14.9.7）——灰度期至 WARN_SUNSET，次日起 enforce
# ---------------------------------------------------------------------------
BEFORE = datetime.date(2026, 10, 11)
AFTER = datetime.date(2026, 10, 12)


class _Stop(Exception):
    """桩 run_region_gates 记下模式后抛出，CLI 不再往下跑。"""


def test_sunset_date_and_default_mode(rg):
    # 定案日期；改期要同步两份 SKILL.md 与 AGENTS.md §8.1——这条断言提醒同步
    assert rg.WARN_SUNSET == datetime.date(2026, 10, 11)
    assert rg.default_mode(BEFORE) == rg.MODE_WARN
    assert rg.default_mode(AFTER) == rg.MODE_ENFORCE


def test_resolve_mode_precedence(rg):
    assert rg.resolve_mode("off", env={"WQB_GATE_MODE": "enforce"}, today=AFTER)[0] == "off"
    assert rg.resolve_mode(None, env={"WQB_GATE_MODE": "warn"}, today=AFTER)[0] == "warn"   # 过期后的显式回退
    assert rg.resolve_mode(None, env={}, today=BEFORE)[0] == "warn"
    assert rg.resolve_mode(None, env={}, today=AFTER)[0] == "enforce"
    mode, note = rg.resolve_mode(None, env={"WQB_GATE_MODE": "enfroce"}, today=AFTER)
    assert mode == "enforce" and "enfroce" in note                                      # 拼错不降级成 warn
    assert "2026-10-12 起缺省 enforce" in rg.resolve_mode(None, env={}, today=BEFORE)[1]


def test_after_sunset_default_and_invalid_mode_block(rg, tmp_path, monkeypatch):
    campaign = _setup(tmp_path, monkeypatch)
    monkeypatch.setattr(rg, "_today", lambda: AFTER)
    for mode in (None, "bogus"):
        rep = rg.run_region_gates(str(campaign), "TESTREG", mode=mode, out=io.StringIO())
        assert rep["mode"] == rg.MODE_ENFORCE and rep["ok"] is False, mode


def test_warn_output_shows_mode_source_and_countdown(rg, tmp_path, monkeypatch):
    campaign = _setup(tmp_path, monkeypatch)
    monkeypatch.setattr(rg, "_today", lambda: BEFORE)
    mode, note = rg.resolve_mode(None, env={})
    buf = io.StringIO()
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode=mode, out=buf, mode_note=note)
    text = buf.getvalue()
    assert rep["ok"] is True
    assert "gate-mode=warn（按日期缺省；灰度期至 2026-10-11" in text
    assert "2026-10-12 起同样命中将阻断开波" in text


def test_build_wave_cli_default_follows_sunset(rg, tmp_path, monkeypatch):
    campaign = _setup(tmp_path, monkeypatch)
    (campaign / "config" / "settings.json").write_text(json.dumps({"region": "TESTREG"}), encoding="utf-8")
    import build_wave as bw

    seen = []

    def fake_run(campaign_dir, region, mode=None, dataset=None, out=None, mode_note=None):
        seen.append((mode, mode_note))
        raise _Stop

    monkeypatch.setattr(bw.rg, "run_region_gates", fake_run)
    monkeypatch.setattr(bw.rg, "_today", lambda: AFTER)
    base = ["build_wave.py", "--campaign-dir", str(campaign), "--wave", "w1"]
    for argv, env_mode, want in ((base, None, "enforce"),
                                 (base + ["--gate-mode", "warn"], None, "warn"),
                                 (base, "warn", "warn")):
        if env_mode:
            monkeypatch.setenv("WQB_GATE_MODE", env_mode)
        else:
            monkeypatch.delenv("WQB_GATE_MODE", raising=False)
        monkeypatch.setattr(sys, "argv", argv)
        with pytest.raises(_Stop):
            bw.main()
        assert seen[-1][0] == want, (argv, env_mode, seen[-1])
    assert "灰度期已于 2026-10-11 结束" in seen[0][1]


def test_wave_gate_cli_default_follows_sunset(rg, tmp_path, monkeypatch):
    campaign = _setup(tmp_path, monkeypatch)
    tools = str(_common.REPO_ROOT / "tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    import wave_gate

    seen = []

    class _RG:
        MODE_WARN = rg.MODE_WARN

        @staticmethod
        def resolve_mode(cli_mode=None, env=None, today=None):
            return rg.resolve_mode(cli_mode, env=env, today=AFTER)

        @staticmethod
        def run_region_gates(campaign_dir, region, mode=None, dataset=None, out=None, mode_note=None):
            seen.append(mode)
            raise _Stop

    monkeypatch.setattr(wave_gate, "_load_region_gates", lambda: _RG)
    base = ["wave_gate.py", "--campaign-dir", str(campaign), "--dataset", "ds1", "--wave", "w1",
            "--region", "TESTREG", "--expr", "rank(close)"]
    for argv, env_mode, want in ((base, None, "enforce"),
                                 (base + ["--gate-mode", "warn"], None, "warn"),
                                 (base, "warn", "warn")):
        if env_mode:
            monkeypatch.setenv("WQB_GATE_MODE", env_mode)
        else:
            monkeypatch.delenv("WQB_GATE_MODE", raising=False)
        monkeypatch.setattr(sys, "argv", argv)
        with pytest.raises(_Stop):
            wave_gate.main()
        assert seen[-1] == want, (argv, env_mode, seen[-1])
