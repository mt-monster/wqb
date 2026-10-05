# -*- coding: utf-8 -*-
"""N30（2026-09-27）：wave_results 的两个自动写入方都走写入契约，波号保留原字符串。

收批级联 `wqb_db_mcp._cascade_wave_result`（`harvest_multisim_results` 调用）
  此前：波号取 int(首个数字)（`s2_<ds>_d1` → 2、`91c` → 91），verdict 写自由文本 "N/M 过硬闸"，
  直接 UPDATE 覆盖已有 verdict，只看最后一批。
  现在：原字符串波号；判定表枚举 verdict（FAIL 只在没有一条过区域 near 线时给）；只改自己写的结论；
  同一波多批按 alpha_id 合并后重算。
评审写入 toolkit `_lib/wave_results`（review_wave / pipeline 的 auto_upsert_from_review）
  此前：同样按首个数字入库（冲突顺延 max+1），INSERT OR REPLACE 整行重建，created_at 每次被重置——
  停止规则 B 的窗口（R22，按波的开始时刻）因此把重评的旧 s2 波当成最新波。
  现在：原字符串波号、合并写入、旧数字行按 full_payload.wave 认领改名、非评审的 findings 保留。
归一：停止闸 `_normalize_verdict` 与写入契约同一张表。
"""
import importlib
import json
import sqlite3
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
for _p in (REPO_ROOT, REPO_ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402
from wqb import wave_results_contract as contract  # noqa: E402
from wqb.workflow.nodes import campaign as C  # noqa: E402

WEAK = [{"alpha_id": f"w{i}", "sharpe": 0.4 + i * 0.1, "fitness": 0.3, "two_year_sharpe": 0.5}
        for i in range(4)]
NEAR = [{"alpha_id": "n1", "sharpe": 1.3, "fitness": 0.8, "two_year_sharpe": 1.1}]
GOOD = [{"alpha_id": "g1", "sharpe": 1.9, "fitness": 1.2, "two_year_sharpe": 2.0}]


# ---------------------------------------------------------------- fixtures / helpers

@pytest.fixture
def db_path(tmp_path, monkeypatch):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()
    monkeypatch.setenv("WQB_DB_PATH", str(path))
    return path


@pytest.fixture
def campaign(tmp_path, monkeypatch):
    """区域战役目录（near 线 1.2），并让 resolve_campaign_dir 指向它。"""
    cdir = tmp_path / "tracking" / "KOR"
    (cdir / "config").mkdir(parents=True)
    (cdir / "config" / "thresholds.json").write_text(
        json.dumps({"near": {"sharpe_min": 1.2}, "diversity": {}}), encoding="utf-8")
    monkeypatch.setenv("WQB_CAMPAIGN_DIR", str(cdir))
    return cdir


@pytest.fixture
def db_mcp(db_path, campaign, monkeypatch):
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    mod.set_db_path(db_path)
    return mod


def _lib_modules():
    return [m for m in sys.modules if m == "_lib" or m.startswith("_lib.")]


@pytest.fixture
def wr_mod(monkeypatch):
    """仓库那份 toolkit `_lib.wave_results`（不取安装位，结论不随同步状态变）。

    用完还原 sys.path 与 `_lib*` 模块：不把本文件加载的那份留给后面的用例。
    """
    for m in _lib_modules():
        monkeypatch.delitem(sys.modules, m)
    monkeypatch.syspath_prepend(str(TOOLKIT))
    yield importlib.import_module("_lib.wave_results")
    for m in _lib_modules():
        sys.modules.pop(m)


def _row(db_path, wave, region="KOR"):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        r = conn.execute("SELECT * FROM wave_results WHERE region=? AND wave_number=?",
                         (region, str(wave))).fetchone()
        return dict(r) if r else None
    finally:
        conn.close()


def _write(db_path, wave, **fields):
    conn = sqlite3.connect(str(db_path))
    try:
        out = contract.upsert_wave_result(conn, "KOR", wave, "2026-09-27T10:00:00", **fields)
        conn.commit()
        return out
    finally:
        conn.close()


# ---------------------------------------------------------------- 收批级联

def test_cascade_keys_by_original_wave_string(db_mcp, db_path):
    db_mcp._cascade_wave_result("KOR", "s2_ml_factor_proj_d1", WEAK)
    db_mcp._cascade_wave_result("KOR", "91c", WEAK)
    for wave in ("s2_ml_factor_proj_d1", "91c"):
        r = _row(db_path, wave)
        assert r and r["verdict"] in contract.VERDICT_OK and r["status"] == "closed"
        assert r["source_file"] == db_mcp.HARVEST_SOURCE
    assert _row(db_path, "2") is None and _row(db_path, "91") is None      # 此前写进"第 2 波""第 91 波"


def test_cascade_does_not_clobber_the_wave_its_number_resembles(db_mcp, db_path):
    # 真实的第 2 波已有评审结论 PASS；此前收一批 s2_other_d1 会把它改成 "0/4 过硬闸"
    _write(db_path, "2", verdict="PASS", source_file="pipeline:auto")
    db_mcp._cascade_wave_result("KOR", "s2_other_d1", WEAK)
    assert _row(db_path, "2")["verdict"] == "PASS"
    assert _row(db_path, "s2_other_d1")["verdict"] == "FAIL"


def test_cascade_merges_batches_and_recomputes(db_mcp, db_path):
    seen = []
    for batch in (WEAK, NEAR, GOOD):
        db_mcp._cascade_wave_result("KOR", "s2_x_d1", batch)
        r = _row(db_path, "s2_x_d1")
        seen.append((r["verdict"], len(json.loads(r["candidates"]))))
    assert seen == [("FAIL", 4), ("PARTIAL", 5), ("PASS", 6)]   # 此前只看最后一批


def test_cascade_fail_only_below_region_near_line(db_mcp, db_path):
    # near 线 1.2（战役目录 thresholds.json）：1.1 → FAIL；1.25 → PARTIAL
    db_mcp._cascade_wave_result("KOR", "w_a", [{"alpha_id": "a", "sharpe": 1.1, "fitness": 0.9}])
    db_mcp._cascade_wave_result("KOR", "w_b", [{"alpha_id": "b", "sharpe": 1.25, "fitness": 0.9}])
    assert _row(db_path, "w_a")["verdict"] == "FAIL"
    assert _row(db_path, "w_b")["verdict"] == "PARTIAL"
    harvest = json.loads(_row(db_path, "w_b")["full_payload"])["harvest"]
    assert harvest["near_line"] == 1.2 and harvest["n_near"] == 1


def test_cascade_never_overrides_review_or_human_verdicts(db_mcp, db_path):
    _write(db_path, "97", verdict="FAIL", source_file="pipeline:auto")          # 评审结论
    assert db_mcp._cascade_wave_result("KOR", "97", GOOD).startswith("kept")
    assert _row(db_path, "97")["verdict"] == "FAIL"

    db_mcp._cascade_wave_result("KOR", "98", WEAK)                              # 级联自己写的 FAIL
    db_mcp.upsert_wave_result("KOR", "98", verdict="PARTIAL")                   # 人工改判（不带 source）
    assert db_mcp._cascade_wave_result("KOR", "98", GOOD).startswith("kept")
    assert _row(db_path, "98")["verdict"] == "PARTIAL"

    _write(db_path, "99", status="open", focus="结论未定")                        # 显式 open
    assert db_mcp._cascade_wave_result("KOR", "99", WEAK).startswith("kept")
    r = _row(db_path, "99")
    assert (r["status"], r["verdict"]) == ("open", None)


def test_cascade_fills_hollow_closed_legacy_row(db_mcp, db_path):
    conn = sqlite3.connect(str(db_path))
    conn.execute("INSERT INTO wave_results (region, wave_number, status, key_findings, created_at, updated_at) "
                 "VALUES ('KOR', '93', 'closed', '[\"人工备注\"]', '2026-09-01T00:00:00', '2026-09-01T00:00:00')")
    conn.commit()
    conn.close()
    assert db_mcp._cascade_wave_result("KOR", "93", WEAK).startswith("updated")
    r = _row(db_path, "93")
    assert r["verdict"] == "FAIL" and r["created_at"] == "2026-09-01T00:00:00"
    findings = json.loads(r["key_findings"])
    assert findings[0].startswith("[harvest]") and "人工备注" in findings


def _legacy_review_row(db_path, key, wave, verdict="FAIL"):
    """旧版 toolkit 评审写下的行：数字键、原字符串只在 full_payload.wave。"""
    conn = sqlite3.connect(str(db_path))
    conn.execute("INSERT INTO wave_results (region, wave_number, verdict, status, source_file, full_payload, "
                 "created_at, updated_at) VALUES ('KOR', ?, ?, 'closed', 'pipeline:auto', ?, "
                 "'2026-09-10 02:00:00', '2026-09-10 02:00:00')", (key, verdict, json.dumps({"wave": wave})))
    conn.commit()
    conn.close()


def test_cascade_adopts_legacy_review_row_instead_of_forking(db_mcp, db_path):
    # 旧版评审把 s2_x_d1 记在 5 号；此前（只有 toolkit 会认领）收批另起一行，5 号成为窗口里的幽灵波
    _legacy_review_row(db_path, "5", "s2_x_d1")
    out = db_mcp._cascade_wave_result("KOR", "s2_x_d1", GOOD)
    assert out.startswith("kept") and "wave_number=5" in out
    r = _row(db_path, "s2_x_d1")
    assert (r["verdict"], r["source_file"], r["created_at"]) == ("FAIL", "pipeline:auto", "2026-09-10 02:00:00")
    assert _row(db_path, "5") is None


def test_adopt_legacy_row_leaves_two_coexisting_rows_alone(db_path):
    _legacy_review_row(db_path, "5", "s2_x_d1")
    _write(db_path, "s2_x_d1", verdict="PARTIAL")
    conn = sqlite3.connect(str(db_path))
    try:
        assert contract.adopt_legacy_row(conn, "KOR", "s2_x_d1") is None      # 两行并存：留给人工，不猜
    finally:
        conn.close()
    assert _row(db_path, "5")["verdict"] == "FAIL" and _row(db_path, "s2_x_d1")["verdict"] == "PARTIAL"


def test_harvest_tool_writes_same_key_as_backtest_rows(db_mcp, db_path):
    # 平台收批的 alpha 都带表达式（backtest_rows 按表达式挂 expressions 行，没有表达式的行不入库）
    alphas = [dict(a, expression=f"rank(ts_delta(x{i}, 5))") for i, a in enumerate(WEAK + NEAR)]
    out = db_mcp.harvest_multisim_results("KOR", "s2_ml_factor_proj_d1", alphas)
    assert out["upserted"] == 5 and "暂定 verdict=PARTIAL" in out["wave_result"]
    conn = sqlite3.connect(str(db_path))
    try:
        bt_waves = {w for (w,) in conn.execute("SELECT DISTINCT wave FROM backtest_results WHERE region='KOR'")}
        wr_waves = {w for (w,) in conn.execute("SELECT wave_number FROM wave_results WHERE region='KOR'")}
        pool = json.loads(conn.execute("SELECT value FROM ledger_kv WHERE region='KOR' "
                                       "AND key='salvage_pool'").fetchone()[0])
    finally:
        conn.close()
    assert bt_waves == wr_waves == {"s2_ml_factor_proj_d1"}
    assert {e["wave"] for e in pool["entries"]} == {"s2_ml_factor_proj_d1"}


# ---------------------------------------------------------------- 评审写入（toolkit）

def _rows(n, sharpe=1.4):
    return [{"id": f"a{i}", "sharpe": sharpe, "fitness": 1.1, "two_year_sharpe": 1.2} for i in range(n)]


def test_review_writer_keys_by_string_and_adopts_legacy_row(wr_mod, db_path):
    conn = sqlite3.connect(str(db_path))
    conn.execute("INSERT INTO wave_results (region, wave_number, verdict, status, source_file, full_payload, "
                 "created_at, updated_at) VALUES ('KOR', 5, 'FAIL', 'closed', 'pipeline:auto', ?, "
                 "'2026-09-10 02:00:00', '2026-09-10 02:00:00')", (json.dumps({"wave": "s2_x_d1"}),))
    rid = conn.execute("SELECT id FROM wave_results WHERE wave_number='5'").fetchone()[0]
    conn.commit()
    conn.close()
    st = wr_mod.WaveResultsStore("KOR", db_path=str(db_path))
    out = st.auto_upsert_from_review("s2_x_d1", _rows(2), [], [{"id": "a0", "sharpe": 1.4, "walls": []}])
    assert out["wave_number"] == "s2_x_d1" and out["legacy_wave_number"] == "5"
    r = _row(db_path, "s2_x_d1")
    assert r["id"] == rid and r["created_at"] == "2026-09-10 02:00:00" and r["verdict"] == "PARTIAL"
    assert _row(db_path, "5") is None


def test_review_rewrite_keeps_created_at_and_foreign_findings(wr_mod, db_path):
    _write(db_path, "94", verdict="FAIL", key_findings=["[pyramid] ANALYST 2/3", "人工：换数据集"])
    created = _row(db_path, "94")["created_at"]
    st = wr_mod.WaveResultsStore("KOR", db_path=str(db_path))
    for _ in range(2):                                   # 重跑评审：评审行整组替换、不重复
        st.auto_upsert_from_review("94", _rows(3), _rows(1), [])
    r = _row(db_path, "94")
    findings = json.loads(r["key_findings"])
    assert r["created_at"] == created and r["verdict"] == "PASS"
    assert findings[0].startswith("GREEN:") and sum(f.startswith("GREEN:") for f in findings) == 1
    assert findings[-2:] == ["[pyramid] ANALYST 2/3", "人工：换数据集"]


def test_review_supersedes_harvest_provisional_verdict(wr_mod, db_mcp, db_path):
    db_mcp._cascade_wave_result("KOR", "s2_y_d1", GOOD)                  # 暂定 PASS
    st = wr_mod.WaveResultsStore("KOR", db_path=str(db_path))
    st.auto_upsert_from_review("s2_y_d1", _rows(2), [], [])             # 评审：0 达标 0 near → FAIL
    r = _row(db_path, "s2_y_d1")
    assert (r["verdict"], r["source_file"]) == ("FAIL", "pipeline:auto")
    assert not any(f.startswith("[harvest]") for f in json.loads(r["key_findings"]))
    assert db_mcp._cascade_wave_result("KOR", "s2_y_d1", GOOD).startswith("kept")


def test_toolkit_cli_accepts_string_wave(wr_mod, db_path, tmp_path, capsys):
    ctx = SimpleNamespace(region="KOR", dir=str(tmp_path))
    assert wr_mod.cli_main(ctx, ["upsert", "--wave", "s2_z_d1", "--verdict", "FAIL", "--status", "closed"]) == 0
    assert wr_mod.cli_main(ctx, ["get", "--wave", "s2_z_d1"]) == 0
    assert "verdict=FAIL" in capsys.readouterr().out


def test_toolkit_cli_status_default_never_reopens_a_closed_wave(wr_mod, db_path, tmp_path):
    # 此前 --status 缺省 open：合并写入下只补 focus 就会把结案波改回 open（停止规则 B 从此看不到它）
    ctx = SimpleNamespace(region="KOR", dir=str(tmp_path))
    steps = (["--focus", "新开一波"], ["--verdict", "FAIL"], ["--focus", "补写 focus"])
    seen = []
    for extra in steps:
        assert wr_mod.cli_main(ctx, ["upsert", "--wave", "s2_q_d1"] + extra) == 0
        r = _row(db_path, "s2_q_d1")
        seen.append((r["status"], r["verdict"], r["focus"]))
    assert seen == [("open", None, "新开一波"), ("closed", "FAIL", "新开一波"), ("closed", "FAIL", "补写 focus")]


# ---------------------------------------------------------------- 与停止规则 B（R22）的联动

def _waves_with_start_times(db_path, starts):
    conn = sqlite3.connect(str(db_path))
    conn.execute("INSERT OR IGNORE INTO regions (name) VALUES ('KOR')")
    rid = conn.execute("SELECT id FROM regions WHERE name='KOR'").fetchone()[0]
    for wave, started in starts:
        conn.execute("INSERT INTO waves (region_id, wave_number, created_at, updated_at) VALUES (?,?,?,?)",
                     (rid, wave, started, started))
    conn.commit()
    conn.close()


def test_rereview_of_old_s2_wave_does_not_release_rule_b(wr_mod, db_path, campaign, monkeypatch):
    for k in ("WQB_DISABLE_STOP_RULES_GATE",):
        monkeypatch.delenv(k, raising=False)
    _waves_with_start_times(db_path, [("s2_old_d1", "2026-09-01T10:00:00"), ("95", "2026-09-10T10:00:00"),
                                      ("96", "2026-09-12T10:00:00"), ("97", "2026-09-14T10:00:00")])
    st = wr_mod.WaveResultsStore("KOR", db_path=str(db_path))
    st.auto_upsert_from_review("s2_old_d1", _rows(2), _rows(1), [])     # 旧波：PASS
    for w in ("95", "96", "97"):
        st.auto_upsert_from_review(w, _rows(2), [], [])                  # 连续三波全灭：FAIL
    st.auto_upsert_from_review("s2_old_d1", _rows(2), _rows(1), [])     # 事后重评旧波
    out = C._run_stop_rules_gate("KOR", None, str(campaign))
    # 此前：重评把旧波写到数字键、created_at 重置成"现在"，与 waves 对不上 → 顶进窗口、规则 B 解除
    assert out["evidence"]["recent_closed_waves"] == ["97", "96", "95"]
    assert out["success"] is False


# ---------------------------------------------------------------- 点塔进度回写（auto_pyramid）

PYRAMID_OUT = "category ...\n\n[key_findings] KOR/D1 点塔 2/7 已点亮(analyst,model) 未点亮(pv,news)\n"


def test_pyramid_embed_goes_through_contract_and_replaces_its_own_line(db_path):
    from wqb.workflow.nodes import auto_pyramid as P
    _write(db_path, "97", verdict="FAIL", key_findings=["RED: 6 全灭", "[pyramid] KOR/D1 点塔 1/7 旧"])
    created = _row(db_path, "97")["created_at"]
    for _ in range(2):                                   # 此前每跑一次追加一条，且写的是进度 dict 的 repr
        out = P._embed_pyramid("KOR", "97", PYRAMID_OUT.splitlines()[-1])
        assert out["embedded"] is True
    r = _row(db_path, "97")
    assert json.loads(r["key_findings"]) == ["RED: 6 全灭", "[pyramid] KOR/D1 点塔 2/7 已点亮(analyst,model) 未点亮(pv,news)"]
    assert (r["verdict"], r["status"], r["created_at"]) == ("FAIL", "closed", created)


def test_pyramid_embed_reports_instead_of_pretending(db_path):
    from wqb.workflow.nodes import auto_pyramid as P
    assert P._embed_pyramid("KOR", "s2_none_d1", "[key_findings] x")["embedded"] is False     # 没有这一行
    conn = sqlite3.connect(str(db_path))
    conn.execute("INSERT INTO wave_results (region, wave_number, status, key_findings) "
                 "VALUES ('KOR', '93', 'closed', '[\"人工备注\"]')")               # 结案却没有 verdict 的旧空壳行
    conn.commit()
    conn.close()
    out = P._embed_pyramid("KOR", "93", "[key_findings] x")
    assert out["embedded"] is False and "verdict" in out["error"]
    assert json.loads(_row(db_path, "93")["key_findings"]) == ["人工备注"]
    assert P._embed_pyramid("KOR", "93", "")["embedded"] is False                            # 没有 [key_findings] 单行


def test_pyramid_node_reports_embed_outcome_and_survives_auto_embed_false(db_path, monkeypatch):
    from wqb.workflow.nodes import auto_pyramid as P
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0, stdout=PYRAMID_OUT, stderr=""))
    out = P.run("KOR", "s2_none_d1")                        # 本波还没有结论行：此前 embedded=True、success=True
    assert out["success"] is False and "未嵌入" in out["error"]
    out = P.run("KOR", "s2_none_d1", auto_embed=False)      # 此前 steps[2] IndexError → 整个节点失败
    assert out["success"] is True and "report" in out["steps"][-1]
    _write(db_path, "s2_none_d1", verdict="PARTIAL")
    out = P.run("KOR", "s2_none_d1")
    assert out["success"] is True and out["steps"][1]["embedded"] is True


# ---------------------------------------------------------------- 归一与表结构

@pytest.mark.parametrize("raw", ["FAIL", "pass", "3/8 过硬闸, 新高 2.10", "0/8 过硬闸", "GREEN: 2 候选达标",
                                 "YELLOW: 0 候选", "RED: 5 全灭", "GATE_FAIL", "全灭", "过硬闸情况未知", "", None])
def test_gate_normalizer_is_the_contract(raw):
    assert C._normalize_verdict(raw) == (contract.normalize_verdict(raw)[0] or "UNKNOWN")


def test_campaign_store_adds_created_at_to_legacy_table(tmp_path):
    db = tmp_path / "legacy.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE wave_results (id INTEGER PRIMARY KEY AUTOINCREMENT, region VARCHAR(50) NOT NULL, "
                 "wave_number INTEGER NOT NULL, focus TEXT, context TEXT, key_findings JSON, candidates JSON, "
                 "batches JSON, verdict TEXT, status VARCHAR(20), source_file VARCHAR(500), "
                 "archived INTEGER DEFAULT 0, full_payload JSON, "
                 "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(region, wave_number))")
    conn.commit()
    conn.close()
    CampaignStore(str(db)).close()
    conn = sqlite3.connect(str(db))
    try:
        assert "created_at" in {r[1] for r in conn.execute("PRAGMA table_info(wave_results)")}
        assert contract.upsert_wave_result(conn, "KOR", "s2_a_d1", "2026-09-27T10:00:00",
                                           verdict="FAIL")["action"] == "inserted"
    finally:
        conn.close()
