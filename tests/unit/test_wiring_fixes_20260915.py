# -*- coding: utf-8 -*-
"""2026-09-15 接线修复回归（审计 ①②④⑤⑥⑦；纯本地，临时 DB，无网络无子进程）。

  ④ campaign S4 分支：从 backtest_results 解析 alpha_id 再拼 review_wave.py 命令；
     解析不到即 FAIL（干跑也 FAIL）——此前只传 --tag，实跑必 rc=2 而干跑报 success。
  ⑦ campaign S2/S3 前置停止规则闸（DB 判定）+ ledger stop_rules_override 放行。
  ② gem 节点 pipeline_mode 透传；S1 模板渲染文档（source=feature_engineering_node/standalone*）不再注入。
  ⑦ review_wave.walls()/passes() 接入 rn_sharpe（RN_EXPOSURE）。
  ⑦ wqb_db_mcp.upsert_wave_result verdict 强制枚举（前缀归一 / 无法辨认拒绝）。
  ① _lib/region_kb.settings_prior_recommendations 证据门槛（min_n / min_lift / pinned）。
"""
import importlib
import json
import os
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"

from wqb.workflow.nodes import campaign as cp  # noqa: E402
from wqb.workflow.nodes import gem as gem_node  # noqa: E402


# ---------------------------------------------------------------- fixtures

def _make_db(path: Path):
    conn = sqlite3.connect(str(path))
    conn.executescript(
        """
        CREATE TABLE backtest_results (id INTEGER PRIMARY KEY, expression_id INTEGER, alpha_id TEXT,
            status TEXT, sharpe REAL, fitness REAL, turnover REAL, margin REAL, returns REAL,
            drawdown REAL, two_year_sharpe REAL, sub_universe_sharpe REAL, long_count INTEGER,
            short_count INTEGER, pnl REAL, book_size REAL, ra_failed_checks TEXT, created_at TEXT,
            region TEXT, wave TEXT, dataset TEXT, code TEXT, payload_json TEXT,
            risk_neutralized_sharpe REAL);
        CREATE TABLE wave_results (id INTEGER PRIMARY KEY, region TEXT, wave_number TEXT, focus TEXT,
            context TEXT, key_findings TEXT, candidates TEXT, batches TEXT, verdict TEXT, status TEXT,
            source_file TEXT, archived INTEGER DEFAULT 0, created_at TEXT, updated_at TEXT,
            full_payload TEXT, region_id INTEGER);
        CREATE TABLE ledger_kv (id INTEGER PRIMARY KEY AUTOINCREMENT, region TEXT NOT NULL,
            key TEXT NOT NULL, value TEXT NOT NULL, created_at TEXT, updated_at TEXT,
            UNIQUE(region, key));
        """
    )
    conn.commit()
    return conn


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    db = tmp_path / "wqb.db"
    conn = _make_db(db)
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    monkeypatch.setenv("WQB_TASK_ROOT", str(tmp_path / "tasks"))
    yield conn
    conn.close()


@pytest.fixture
def campaign_dir(tmp_path):
    d = tmp_path / "tracking" / "TST"
    (d / "config").mkdir(parents=True)
    (d / "config" / "settings.json").write_text(json.dumps({
        "instrumentType": "EQUITY", "region": "TST", "universe": "TOP3000", "delay": 1,
        "neutralization": "SUBINDUSTRY", "decay": 4, "truncation": 0.08,
    }), encoding="utf-8")
    (d / "config" / "thresholds.json").write_text(json.dumps({
        "review": {"sharpe_min": 1.58, "fitness_min": 1.0, "two_year_sharpe_min": 1.58,
                   "margin_min": 0.001, "turnover_min": 0.01, "turnover_max": 0.7},
        "near": {"sharpe_min": 1.0},
        "diversity": {"signal_floor": {"enabled": False},
                      "stop_rules": {"yield_min_backtests": 5, "consecutive_fail_waves": 2}},
    }), encoding="utf-8")
    return d


def _seed_backtests(conn, region, wave, n, sharpe=0.3, fitness=0.2):
    for i in range(n):
        conn.execute(
            "INSERT INTO backtest_results (alpha_id, sharpe, fitness, region, wave, code, payload_json) "
            "VALUES (?,?,?,?,?,?,?)",
            (f"{wave}_A{i}", sharpe, fitness, region, wave, "rank(x)",
             json.dumps({"code": "rank(x)", "neut": "SUBINDUSTRY"})),
        )
    conn.commit()


def _seed_wave(conn, region, wave, verdict):
    conn.execute(
        "INSERT INTO wave_results (region, wave_number, verdict, status, created_at, updated_at) "
        "VALUES (?,?,?,?,datetime('now'),datetime('now'))", (region, wave, verdict, "closed"))
    conn.commit()


# ---------------------------------------------------------------- ④ S4 alpha 解析

def test_s4_resolves_alpha_ids_from_backtests(tmp_db, campaign_dir):
    _seed_backtests(tmp_db, "TST", "61", 3, sharpe=1.2)
    ids, hit, _recent = cp._resolve_wave_alpha_ids("TST", "61", "ds1")
    assert ids == ["61_A0", "61_A1", "61_A2"] and hit == "61"


def test_s4_falls_back_to_gem_label(tmp_db, campaign_dir):
    _seed_backtests(tmp_db, "TST", "s2_ds1_d1", 2, sharpe=1.2)
    ids, hit, _ = cp._resolve_wave_alpha_ids("TST", "61", "ds1")
    assert len(ids) == 2 and hit == "s2_ds1_d1"


def test_s4_node_fails_when_no_backtests(tmp_db, campaign_dir, monkeypatch):
    """此前：只传 --tag → 实跑 rc=2、干跑 success。现在：干跑也 FAIL 且说明原因。"""
    monkeypatch.setattr(cp, "resolve_campaign_dir", lambda region, **kw: str(campaign_dir))
    monkeypatch.setattr(cp, "resolve_toolkit_dir", lambda: str(TOOLKIT_SCRIPTS))
    r = cp.run(region="TST", stage="S4", dataset="ds1", wave="61",
               _context={"store": None, "dry_run": True})
    assert r["success"] is False
    step = [s for s in r["steps"] if s["step"] == "resolve_s4_alphas"][0]
    assert step["success"] is False and "backtest_results" in step["error"]


def test_s4_node_builds_alphas_command(tmp_db, campaign_dir, monkeypatch):
    _seed_backtests(tmp_db, "TST", "61", 2, sharpe=1.2)
    monkeypatch.setattr(cp, "resolve_campaign_dir", lambda region, **kw: str(campaign_dir))
    monkeypatch.setattr(cp, "resolve_toolkit_dir", lambda: str(TOOLKIT_SCRIPTS))
    r = cp.run(region="TST", stage="S4", dataset="ds1", wave="61",
               _context={"store": None, "dry_run": True})
    assert r["success"] is True, r["steps"]
    cmd = [s for s in r["steps"] if s["step"] == "build_command"][0]["command"]
    assert "--alphas 61_A0 61_A1" in cmd and "--tag 61" in cmd and "--write-ledger" in cmd


# ---------------------------------------------------------------- ⑦ 停止规则闸

def test_stop_rules_blocks_zero_yield(tmp_db, campaign_dir):
    _seed_backtests(tmp_db, "TST", "1", 6, sharpe=0.4, fitness=0.3)  # ≥5 且 0 达标
    r = cp._run_stop_rules_gate("TST", None, str(campaign_dir))
    assert r["success"] is False and r["hits"][0].startswith("A:")
    assert "stop_rules_override" in r["error"]


def test_stop_rules_blocks_consecutive_fail_waves(tmp_db, campaign_dir):
    _seed_backtests(tmp_db, "TST", "1", 2, sharpe=2.0, fitness=1.5)  # 有达标，规则 A 不触发
    _seed_wave(tmp_db, "TST", "1", "FAIL")
    _seed_wave(tmp_db, "TST", "2", "FAIL")
    r = cp._run_stop_rules_gate("TST", None, str(campaign_dir))
    assert r["success"] is False and any(h.startswith("B:") for h in r["hits"])


def test_stop_rules_pass_when_healthy(tmp_db, campaign_dir):
    _seed_backtests(tmp_db, "TST", "1", 6, sharpe=2.0, fitness=1.5)
    _seed_wave(tmp_db, "TST", "1", "PASS")
    r = cp._run_stop_rules_gate("TST", None, str(campaign_dir))
    assert r["success"] is True and "hits" not in r


def test_stop_rules_override_releases_with_reason(tmp_db, campaign_dir):
    _seed_backtests(tmp_db, "TST", "1", 6, sharpe=0.4, fitness=0.3)
    tmp_db.execute("INSERT INTO ledger_kv (region, key, value) VALUES (?,?,?)",
                   ("TST", "stop_rules_override",
                    json.dumps({"reason": "用户明示继续", "until": "2099-01-01"})))
    tmp_db.commit()
    r = cp._run_stop_rules_gate("TST", None, str(campaign_dir))
    assert r["success"] is True and r["hits"] and "用户明示继续" in r["note"]


def test_stop_rules_expired_override_does_not_release(tmp_db, campaign_dir):
    _seed_backtests(tmp_db, "TST", "1", 6, sharpe=0.4, fitness=0.3)
    tmp_db.execute("INSERT INTO ledger_kv (region, key, value) VALUES (?,?,?)",
                   ("TST", "stop_rules_override",
                    json.dumps({"reason": "过期覆盖", "until": "2000-01-01"})))
    tmp_db.commit()
    r = cp._run_stop_rules_gate("TST", None, str(campaign_dir))
    assert r["success"] is False


def test_stop_rules_disabled_by_thresholds(tmp_db, campaign_dir):
    th = json.loads((campaign_dir / "config" / "thresholds.json").read_text(encoding="utf-8"))
    th["diversity"]["stop_rules"]["enabled"] = False
    (campaign_dir / "config" / "thresholds.json").write_text(json.dumps(th), encoding="utf-8")
    _seed_backtests(tmp_db, "TST", "1", 6, sharpe=0.4, fitness=0.3)
    r = cp._run_stop_rules_gate("TST", None, str(campaign_dir))
    assert r["success"] is True and "skipped" in r


# ---------------------------------------------------------------- ② gem 节点

def test_gem_template_source_detection():
    assert gem_node.is_template_ideas_source("feature_engineering_node")
    assert gem_node.is_template_ideas_source("standalone_v2")
    assert gem_node.is_template_ideas_source(
        "feature_engineering_node (whitelist restored to full catalog by agent 2026-09-13)")
    assert not gem_node.is_template_ideas_source("s2_nested")
    assert not gem_node.is_template_ideas_source("manual")
    assert not gem_node.is_template_ideas_source(None)


class _GemStore:
    def __init__(self, s1):
        self._s1 = s1

    def get_ledger(self, region, key):
        return self._s1 if key.startswith("s1_") else None

    def get_field_prefix_clusters(self, region, dataset):
        return None

    def get_candidate_field_pool(self, region, dataset):
        return {"candidate_field_pool": ["f1"], "pool_size": 1, "builder_version": 2}


def _gem_dry(monkeypatch, tmp_path, s1, **kw):
    gem_root = tmp_path / "brain-make-some-gem"
    runner = gem_root / "scripts" / "headless_runner"
    runner.mkdir(parents=True)
    (runner / "run.py").write_text("import argparse\n", encoding="utf-8")
    (runner / "config.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(gem_node, "resolve_skill_dir", lambda name: str(gem_root))
    monkeypatch.setattr(gem_node, "validate_argv", lambda cmd: (True, None))
    monkeypatch.setattr(gem_node, "resolve_db_path", lambda: str(tmp_path / "wqb.db"))
    return gem_node.run(region="TST", dataset_id="ds1", delay=1, universe="TOP3000",
                        data_category="pv", data_type="MATRIX",
                        _context={"store": _GemStore(s1), "dry_run": True}, **kw)


def test_gem_skips_template_ideas_doc(monkeypatch, tmp_path):
    ideas = tmp_path / "TST_delay1_ds1_ideas.md"
    ideas.write_text("**Concept**: x\n- **Implementation Example**: `rank({a})`\n", encoding="utf-8")
    r = _gem_dry(monkeypatch, tmp_path,
                 {"ideas_md_path": str(ideas), "source": "feature_engineering_node"})
    assert r["success"] is True, r["steps"]
    step = [s for s in r["steps"] if s["step"] == "s1_ledger_check"][0]
    assert step["auto_inject"] is False and "模板渲染" in step["skipped_reason"]
    assert "--ideas-file" not in r["command"]


def test_gem_injects_llm_ideas_doc_and_pipeline_mode(monkeypatch, tmp_path):
    ideas = tmp_path / "TST_delay1_ds1_ideas.md"
    ideas.write_text("**Concept**: x\n- **Implementation Example**: `rank({a})`\n", encoding="utf-8")
    r = _gem_dry(monkeypatch, tmp_path,
                 {"ideas_md_path": str(ideas), "source": "s2_nested"}, pipeline_mode="phased")
    assert r["success"] is True, r["steps"]
    assert "--ideas-file" in r["command"] and "--pipeline-mode phased" in r["command"]


def test_gem_skeleton_mode_drops_ideas_file(monkeypatch, tmp_path):
    ideas = tmp_path / "TST_delay1_ds1_ideas.md"
    ideas.write_text("**Concept**: x\n- **Implementation Example**: `rank({a})`\n", encoding="utf-8")
    r = _gem_dry(monkeypatch, tmp_path,
                 {"ideas_md_path": str(ideas), "source": "s2_nested"}, pipeline_mode="skeleton")
    assert r["success"] is True, r["steps"]
    assert "--pipeline-mode skeleton" in r["command"] and "--ideas-file" not in r["command"]


def test_gem_rejects_bad_pipeline_mode(monkeypatch, tmp_path):
    r = _gem_dry(monkeypatch, tmp_path, None, pipeline_mode="turbo")
    assert r["success"] is False and "pipeline_mode" in r["error"]


# ---------------------------------------------------------------- ⑦ rn 墙

def _review_mod():
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    for m in ("review_wave", "metrics_cache", "_lib.rules", "_lib.wqb_store",
              "_lib.ledger", "_lib.common", "_lib"):
        sys.modules.pop(m, None)
    return importlib.import_module("review_wave")


def test_rn_exposure_is_a_wall_and_blocks_candidate():
    rw = _review_mod()
    t = {"sharpe_min": 1.58, "fitness_min": 1.0, "two_year_sharpe_min": 1.58,
         "margin_min": 0.001, "turnover_min": 0.01, "turnover_max": 0.7}
    good = {"sharpe": 2.0, "fitness": 1.2, "two_year_sharpe": 1.9, "margin_bp": 15,
            "turnover_pct": 20, "failed_checks": [], "rn_sharpe": 1.1}
    exposed = dict(good, rn_sharpe=-0.4)
    unknown = dict(good, rn_sharpe=None)
    assert rw.passes(good, t) and rw.passes(unknown, t)      # rn 缺失不算败
    assert not rw.passes(exposed, t)
    assert "RN_EXPOSURE" in rw.walls(exposed, t)
    assert rw.rn_exposure(exposed, dict(t, rn_sharpe_min=-1.0)) is False  # 阈值可调


# ---------------------------------------------------------------- ⑦ verdict 枚举（MCP 写入口）

def _load_db_mcp(monkeypatch, db_path):
    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    sys.modules.pop("wqb_db_mcp", None)
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    return importlib.import_module("wqb_db_mcp")


def test_normalize_wave_verdict_rules(monkeypatch, tmp_path):
    m = _load_db_mcp(monkeypatch, tmp_path / "x.db")
    f = m._normalize_wave_verdict
    assert f("PASS")[0] == "PASS" and f("fail")[0] == "FAIL"
    assert f("PASS_READY_x2：双双过闸")[0] == "PASS"
    assert f("PARTIAL_BREAKTHROUGH：首个候选")[0] == "PARTIAL"
    assert f("CLOSED_DEAD_END_DATASET：判死")[0] == "FAIL"
    assert f("GATE_BLOCKED_SATURATION")[0] == "FAIL"
    assert f("0/8 过硬闸, 新高 0.99")[0] == "FAIL" and f("3/4 过硬闸, 新高 1.98")[0] == "PASS"
    assert f("RED: 14 全灭")[0] == "FAIL" and f("YELLOW: 0 候选, 1 near")[0] == "PARTIAL"
    assert f("机制确认但天花板明确")[0] is None


# ---------------------------------------------------------------- ① settings prior

def test_settings_prior_recommendation_thresholds(tmp_path, monkeypatch):
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    for m in ("_lib.region_kb", "_lib.ledger", "_lib.common", "_lib"):
        sys.modules.pop(m, None)
    rk = importlib.import_module("_lib.region_kb")

    class Ctx:
        region = "TST"
        settings = {"decay": 4, "neutralization": "SUBINDUSTRY"}

        def thresh(self, section, default=None):
            return {}

    kb = {"gate_priors": {
        "by_decay": {"4": {"rate": 0.039, "n": 408}, "14": {"rate": 0.283, "n": 46},
                     "20": {"rate": 0.9, "n": 3}},                       # n<30 不采信
        "by_neutralization": {"SUBINDUSTRY": {"rate": 0.0665, "n": 361},
                              "INDUSTRY": {"rate": 0.0725, "n": 400}},   # lift 1.09 不改
    }}
    monkeypatch.setattr(rk, "load_region_kb", lambda ctx: kb)
    recs = {r["dim"]: r for r in rk.settings_prior_recommendations(Ctx())}
    assert recs["decay"]["recommended"] == 14 and recs["decay"]["apply"] is True
    assert recs["neutralization"]["apply"] is False

    ctx = Ctx()
    applied = rk.apply_settings_prior(ctx, pinned=set(), log=lambda *_: None)
    assert ctx.settings["decay"] == 14 and [a["dim"] for a in applied] == ["decay"]

    ctx2 = Ctx()
    ctx2.settings = {"decay": 4, "neutralization": "SUBINDUSTRY"}
    rk.apply_settings_prior(ctx2, pinned={"decay"}, log=lambda *_: None)
    assert ctx2.settings["decay"] == 4  # 显式钉住不动
