# -*- coding: utf-8 -*-
"""2026-09-27 第二批 P1 的回归护栏（reports/ra_pipeline_stage_review_20260927.md §14.9）。

R22  停止规则 B 的"最近 K 个 closed 波"按波的开始时刻取，补记旧波 / 补写 findings 不改变窗口
R5   workflow_batch_track 与 campaign S2/S3 共用三道开波闸（只读 DB、干跑也走）；S4 解析 alpha 同样只读
R12  tools/ 下 CLI 找 skill 脚本走 skill_paths（~/.claude、~/.codex、仓库兜底）；
     门禁环境缺失（缺 verifier / ply / gate.py）退出码 2（ERROR），不再是 1（FAIL）；
     probe_batch_mode 的 CampaignStore 认 WQB_DB_PATH
R4   RN_EXPOSURE 行不进 near / salvage 池与组合候选（review_wave 与 pipeline review 同一判据）
（R3 Failed-count 单一实现见 test_r3_failed_count_single_source.py）
"""
import json
import os
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLKIT = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
for _p in (REPO_ROOT / "src", REPO_ROOT / "tools", TOOLKIT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402
from wqb.workflow.nodes import batch_track as bt  # noqa: E402
from wqb.workflow.nodes import campaign as C  # noqa: E402

_GATE_SWITCHES = ("WQB_DISABLE_SIGNAL_FLOOR_GATE", "WQB_DISABLE_STOP_RULES_GATE", "WQB_DISABLE_BACKLOG_GATE")


@pytest.fixture
def gates_on(monkeypatch):
    for k in _GATE_SWITCHES:
        monkeypatch.delenv(k, raising=False)
    return monkeypatch


def _campaign(tmp_path, region="TESTREG"):
    cdir = tmp_path / region
    (cdir / "config").mkdir(parents=True)
    (cdir / "config" / "thresholds.json").write_text("{}", encoding="utf-8")
    (cdir / "config" / "settings.json").write_text(json.dumps({"region": region}), encoding="utf-8")
    return cdir


def _minimal_db(tmp_path, verdicts):
    """最小库（无 waves / regions 表）：verdicts 首个最近；created_at 递减。"""
    db = tmp_path / "wqb_min.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE wave_results (id INTEGER PRIMARY KEY, region TEXT, wave_number TEXT, "
                 "verdict TEXT, status TEXT, created_at TEXT, updated_at TEXT)")
    conn.execute("CREATE TABLE backtest_results (id INTEGER PRIMARY KEY, region TEXT, sharpe REAL, fitness REAL)")
    conn.execute("CREATE TABLE ledger_kv (region TEXT, key TEXT, value TEXT)")
    for i, v in enumerate(verdicts):
        conn.execute("INSERT INTO wave_results (region, wave_number, verdict, status, created_at, updated_at) "
                     "VALUES ('TESTREG', ?, ?, 'closed', ?, ?)",
                     (str(100 - i), v, f"2026-09-{20 - i:02d} 00:00:00", f"2026-09-{20 - i:02d} 00:00:00"))
    conn.commit()
    conn.close()
    return db


def _full_db(tmp_path, waves, probes=()):
    """完整 schema 库。waves: (波号, 开始时刻 waves.created_at, verdict, wave_results 时间戳)；
    probes: (波号, verdict, wave_results.created_at) —— 没有表达式、只有结论行的波。"""
    db = tmp_path / "wqb_full.db"
    CampaignStore(str(db)).close()
    conn = sqlite3.connect(str(db))
    conn.execute("INSERT INTO regions (name) VALUES ('TESTREG')")
    rid = conn.execute("SELECT id FROM regions WHERE name='TESTREG'").fetchone()[0]
    for wave, started, verdict, wr_ts in waves:
        conn.execute("INSERT INTO waves (region_id, wave_number, created_at, updated_at) VALUES (?,?,?,?)",
                     (rid, wave, started, started))
        conn.execute("INSERT INTO wave_results (region, wave_number, verdict, status, created_at, updated_at) "
                     "VALUES ('TESTREG', ?, ?, 'closed', ?, ?)", (wave, verdict, wr_ts, wr_ts))
    for wave, verdict, created in probes:
        conn.execute("INSERT INTO wave_results (region, wave_number, verdict, status, created_at, updated_at) "
                     "VALUES ('TESTREG', ?, ?, 'closed', ?, ?)", (wave, verdict, created, created))
    conn.commit()
    conn.close()
    return db


# ---------------------------------------------------------------- R22：窗口按波的开始时刻

def test_rule_b_window_ignores_backfill_of_old_wave(tmp_path, gates_on):
    # KOR 真实复现的形态：91c 早于 95–97，事后按 R20 建议补记 PASS（结论行时间戳最新）
    db = _full_db(tmp_path, [
        ("91c", "2026-09-01T10:00:00", "PASS", "2026-09-27T12:00:00"),
        ("95", "2026-09-10T10:00:00", "FAIL", "2026-09-10T12:00:00"),
        ("96", "2026-09-12T10:00:00", "FAIL", "2026-09-12T12:00:00"),
        ("97", "2026-09-14T10:00:00", "FAIL", "2026-09-14T12:00:00"),
    ])
    gates_on.setenv("WQB_DB_PATH", str(db))
    out = C._run_stop_rules_gate("TESTREG", None, str(_campaign(tmp_path)))
    assert out["evidence"]["recent_closed_waves"] == ["97", "96", "95"]
    assert out["success"] is False and any(h.startswith("B:") for h in out["hits"])   # 仍拦截


def test_rule_b_window_probe_without_expressions_uses_result_row(tmp_path, gates_on):
    db = _full_db(tmp_path,
                  [("96", "2026-09-12T10:00:00", "FAIL", "2026-09-12T12:00:00"),
                   ("97", "2026-09-14T10:00:00", "FAIL", "2026-09-14T12:00:00")],
                  probes=[("s2_ds_d1", "FAIL", "2026-09-20T10:00:00")])
    gates_on.setenv("WQB_DB_PATH", str(db))
    out = C._run_stop_rules_gate("TESTREG", None, str(_campaign(tmp_path)))
    assert out["evidence"]["recent_closed_waves"] == ["s2_ds_d1", "97", "96"]


@pytest.mark.skipif(not hasattr(time, "tzset"), reason="time.tzset 仅 POSIX 可用")
def test_rule_b_window_compares_utc_and_local_clocks(tmp_path, gates_on):
    # waves.created_at 是本地 isoformat（T 分隔）；toolkit 写的结论行是 SQLite UTC（空格分隔）。
    # 东八区：探针波 UTC 02:00 = 本地 10:00，晚于 97 的本地 09:00 → 应排在最前（按字符串比会排到后面）
    gates_on.setenv("TZ", "Asia/Shanghai")
    time.tzset()
    try:
        db = _full_db(tmp_path,
                      [("96", "2026-09-20T08:00:00", "FAIL", "2026-09-20T08:30:00"),
                       ("97", "2026-09-20T09:00:00", "FAIL", "2026-09-20T09:30:00")],
                      probes=[("probe", "FAIL", "2026-09-20 02:00:00")])
        gates_on.setenv("WQB_DB_PATH", str(db))
        out = C._run_stop_rules_gate("TESTREG", None, str(_campaign(tmp_path)))
        assert out["evidence"]["recent_closed_waves"] == ["probe", "97", "96"]
    finally:
        gates_on.undo()
        time.tzset()


def test_rule_b_window_minimal_db_without_waves_table(tmp_path, gates_on):
    db = _minimal_db(tmp_path, ["FAIL", "PASS", "FAIL", "FAIL"])
    gates_on.setenv("WQB_DB_PATH", str(db))
    out = C._run_stop_rules_gate("TESTREG", None, str(_campaign(tmp_path)))
    assert out["evidence"]["recent_closed_waves"] == ["100", "99", "98"]
    assert out["success"] is True                                   # 窗口里有 PASS，不拦


# ---------------------------------------------------------------- R5：batch_track 过三道开波闸

def test_batch_track_dry_run_blocked_by_stop_rules(tmp_path, gates_on):
    gates_on.setenv("WQB_DB_PATH", str(_minimal_db(tmp_path, ["FAIL", "FAIL", "FAIL"])))
    out = bt.run(region="TESTREG", wave="w1", dataset="ds1", campaign_dir=str(_campaign(tmp_path)),
                 _context={"dry_run": True})
    assert out["success"] is False and "停止规则拦截" in out["error"]
    assert [s["step"] for s in out["steps"]] == ["signal_floor_gate", "stop_rules_gate"]
    assert "--submit" in out["command"]                               # 被拦时仍带回将要执行的命令


def test_batch_track_real_run_blocked_before_launch(tmp_path, gates_on):
    gates_on.setenv("WQB_DB_PATH", str(_minimal_db(tmp_path, ["FAIL", "FAIL", "FAIL"])))
    launched = []
    gates_on.setattr(bt.subprocess, "Popen", lambda *a, **k: launched.append(a))
    gates_on.setattr(bt.subprocess, "run", lambda *a, **k: launched.append(a))
    store = SimpleNamespace(list_expressions=lambda *a, **k: [{"expression": "rank(close)"}])
    out = bt.run(region="TESTREG", wave="w1", dataset="ds1", campaign_dir=str(_campaign(tmp_path)),
                 _context={"store": store})
    assert out["success"] is False and "停止规则拦截" in out["error"]
    assert launched == []                                             # 此前照样发批（带 --submit）


def test_batch_track_dry_run_passes_gates_and_reports_them(tmp_path, gates_on):
    gates_on.setenv("WQB_DB_PATH", str(_minimal_db(tmp_path, ["PASS", "FAIL", "FAIL"])))
    out = bt.run(region="TESTREG", wave="w1", dataset="ds1", campaign_dir=str(_campaign(tmp_path)),
                 _context={"dry_run": True})
    assert out["success"] is True, out.get("error")
    assert [s["step"] for s in out["steps"]] == ["signal_floor_gate", "stop_rules_gate", "backlog_gate"]
    assert bt.run_open_wave_gates is C.run_open_wave_gates           # 与 campaign S2/S3 同一实现


def test_open_wave_gates_never_create_db(tmp_path, gates_on):
    absent = tmp_path / "absent.db"
    gates_on.setenv("WQB_DB_PATH", str(absent))
    steps, err = C.run_open_wave_gates("TESTREG", "ds1", str(_campaign(tmp_path)))
    assert err is None and len(steps) == 3
    assert not absent.exists()                                        # 只读打开：不再悄悄建空库


def test_s4_alpha_resolution_never_creates_db(tmp_path, monkeypatch):
    # 同一类纯读路径：S4 解析本波 alpha（dry-run 也走）此前 sqlite3.connect 会在缺库时建空库
    absent = tmp_path / "absent.db"
    monkeypatch.setenv("WQB_DB_PATH", str(absent))
    assert C._resolve_wave_alpha_ids("TESTREG", "1", "ds1") == ([], "1", [])
    assert not absent.exists()


# ---------------------------------------------------------------- R12：skill 目录解析 + 环境缺失 exit 2

def test_skill_script_dirs_follow_skill_roots(monkeypatch):
    import skill_paths

    monkeypatch.delenv("WQ_TOOLKIT_DIR", raising=False)
    dirs = skill_paths.skill_script_dirs("wq-brain-campaign-toolkit", "WQ_TOOLKIT_DIR")
    home = os.path.expanduser("~")
    claude = os.path.join(home, ".claude", "skills", "wq-brain-campaign-toolkit", "scripts")
    qoder = os.path.join(home, ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")
    assert dirs.index(claude) < dirs.index(qoder)                     # 此前根本不含 ~/.claude
    assert dirs[-1] == str(REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts")
    monkeypatch.setenv("WQ_TOOLKIT_DIR", "/explicit/toolkit")
    assert skill_paths.skill_script_dirs("wq-brain-campaign-toolkit", "WQ_TOOLKIT_DIR")[0] == "/explicit/toolkit"


def test_wave_gate_finds_verifier_without_env(monkeypatch):
    import skill_paths
    import wave_gate

    monkeypatch.delenv("WQ_VALIDATOR_DIR", raising=False)
    found = wave_gate.find_script(skill_paths.skill_script_dirs("alpha-expression-verifier", "WQ_VALIDATOR_DIR"),
                                  "validator.py")
    assert os.path.isfile(found)


def test_wave_gate_missing_ply_exits_2(tmp_path):
    fake = tmp_path / "verifier"
    fake.mkdir()
    # alpha-expression-verifier 缺 ply 时的真实行为：import 阶段打印提示并 sys.exit(1)
    (fake / "validator.py").write_text('import sys\nprint("错误: 需要安装PLY库。")\nsys.exit(1)\n',
                                       encoding="utf-8")
    camp = _campaign(tmp_path, "TST")
    ef = tmp_path / "exprs.txt"
    ef.write_text("rank(close)\n", encoding="utf-8")
    db = tmp_path / "data" / "wqb.db"
    CampaignStore(str(db)).close()
    env = {k: v for k, v in os.environ.items() if k not in ("WQB_ROOT", "WQ_PROJECT_ROOT", "WQB_WORKSPACE")}
    env.update({"WQ_VALIDATOR_DIR": str(fake), "WQB_DB_PATH": str(db), "PYTHONIOENCODING": "utf-8"})
    r = subprocess.run([sys.executable, str(REPO_ROOT / "tools" / "wave_gate.py"), "--campaign-dir", str(camp),
                        "--dataset", "stubds", "--wave", "g1", "--exprs-file", str(ef), "--inspect-mode", "off"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
                       cwd=str(tmp_path), timeout=300)
    assert r.returncode == 2, r.stdout[-2000:] + r.stderr[-2000:]    # 此前 exit 1 = 被读成"表达式不合格"
    assert "门禁环境缺失" in r.stdout


def test_probe_batch_store_honors_wqb_db_path(tmp_path, monkeypatch):
    # R12 让 probe_batch_mode 找得到 toolkit 之后，构造器会走到 _wqb_store()；此前写死 <repo>/data/wqb.db
    import probe_batch_mode

    db = tmp_path / "wqb.db"
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    store = probe_batch_mode._wqb_store()
    try:
        assert Path(store.path) == db
    finally:
        store.close()


# ---------------------------------------------------------------- R4：RN_EXPOSURE 不进 near / salvage

_T = {"sharpe_min": 1.58, "fitness_min": 1.0, "two_year_sharpe_min": 1.0, "margin_min": 0.0,
      "turnover_min": 0.01, "turnover_max": 0.7, "rn_sharpe_min": 0.0,
      "combo_sharpe_min": 1.0, "combo_prod_corr_max": 0.5}
_T_NEAR = {"sharpe_min": 1.0, "robust_min_ratio": 0.5}


def _row(**kw):
    base = {"id": "X", "sharpe": 1.4, "fitness": 0.9, "two_year_sharpe": 1.2, "turnover_pct": 20.0,
            "margin_bp": 5.0, "prod_corr": 0.3, "robust_sharpe": 1.2, "robust_limit": 1.0,
            "rn_sharpe": 0.8, "failed_checks": []}
    base.update(kw)
    return base


def test_near_block_wall_excludes_rn_exposure():
    import review_wave as rw

    assert rw.near_block_wall(_row(rn_sharpe=-0.2), _T, _T_NEAR) == "RN_EXPOSURE"
    assert rw.near_block_wall(_row(rn_sharpe=-0.2, robust_sharpe=0.2), _T, _T_NEAR) == "ROBUST_STRUCTURAL"
    assert rw.near_block_wall(_row(), _T, _T_NEAR) is None
    assert rw.near_block_wall(_row(rn_sharpe=None), _T, _T_NEAR) is None     # rn 缺失不算败


def test_combo_candidate_excludes_rn_exposure():
    import review_wave as rw

    assert rw.combo_candidate(_row(), _T) is True
    assert rw.combo_candidate(_row(rn_sharpe=-0.2), _T) is False     # combo 候选会进 salvage_pool


def test_pipeline_review_uses_the_same_near_rule():
    src = (TOOLKIT / "pipeline.py").read_text(encoding="utf-8")
    assert "review_mod.near_block_wall(" in src and "review_mod.structurally_dead(" not in src
