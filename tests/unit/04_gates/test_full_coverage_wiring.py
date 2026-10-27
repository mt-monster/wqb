# -*- coding: utf-8 -*-
"""tests/unit/04_gates/test_full_coverage_wiring.py — 全量覆盖闸（FCV）接线回归。

背景（2026-10-20 P0-1）：`tools/full_coverage_gate.py` 此前在 wave_gate / pipeline
整条可执行路径上**零调用点** ——「覆盖前置闸」只存在于文档。本接线契约：

1. **数据驱动激活**：战役目录存在 `reference/boundary_ops_<region小写>.json` 即启用
   （无区域字面量分支；`enabled: false` 显式关；配置损坏仍启用=fail-closed）。
2. **模式分层**：`--fcov-mode` > `WQB_FCOV_MODE` > 随区域闸按日缺省（`_rg.resolve_mode`
   → 2026-10-12 起 enforce）> 兜底 warn；显式降级到缺省之下 → 计入 waiver 检查
   （`waiver_full_coverage_<region>_<wave>`）。
3. **enforce 语义**：三闸（字段覆盖/模板族/边界算子）任一 FAIL → 折叠进 all_pass
   （exit 1）；字段全集/边界配置不可得 → exit 2（无门禁结论 ≠ 表达式不合格）。
   warn 档 FAIL 全部降级 WARN（exit 0）；off 档整闸跳过。
4. **字段全集解析**：战役 reference JSON 优先，缺席时回退本地 catalog（DB 的
   fields×datasets×regions，**必须 region 作用域**）；模板族历史 = 文件史 ∪ DB
   `expressions.family`（GEM skeleton 产物已入库，文件扫描对 DB-only 新波失明）。

断言字符串来源：2026-10-20 接线 recon（4 变体子进程实跑，TST 假战役 + 假库）。
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
_TOOLS = str(REPO / "tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import wave_gate  # noqa: E402
import full_coverage_gate as fcg  # noqa: E402

REGION = "TST"   # 假区域码：不撞任何真实区域战役目录 / ratchet 面
DATASET = "myds"


# ---------------------------------------------------------------- helpers


def _write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        path.write_text(data, encoding="utf-8")
    else:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def _mk_campaign(root: Path, *, with_fields: bool = True, with_candidates: bool = True,
                 boundary=None) -> Path:
    """最小战役脚手架（形态取自 2026-10-20 FCV 接线 recon 的可跑战役）。

    - settings.json：region/universe/delay（`_wv_region` 与 gate.py ctx 都读它）
    - reference/boundary_ops_tst.json：激活本闸的**唯一**凭据（内容可空）
    - reference/tst_myds_fields.json：字段全集（2 个字段，服务 FCV + gate.py catalog）
    - candidates/myds_wave1.json：文件史 3 个模板族（fam_a/b/c）
    """
    camp = root / REGION
    _write(camp / "config" / "settings.json",
           {"region": REGION, "universe": "TOP3000", "delay": 1})
    _write(camp / "config" / "thresholds.json", {})
    _write(camp / "reference" / f"boundary_ops_{REGION.lower()}.json",
           {"operators": {}, "_doc": "pytest stub"} if boundary is None else boundary)
    if with_fields:
        _write(camp / "reference" / f"{REGION.lower()}_{DATASET}_fields.json",
               {"dataset": DATASET, "region": REGION, "data_type": "MATRIX",
                "fields": [{"id": "f1", "type": "MATRIX"}, {"id": "f2", "type": "MATRIX"}]})
    if with_candidates:
        _write(camp / "candidates" / f"{DATASET}_wave1.json",
               {"expressions": [{"expr": "rank(f1)", "template_family": "fam_a"},
                                {"expr": "rank(f2)", "family_id": "fam_b"}],
                "family": "fam_c"})
    return camp


def _make_catalog_db(path: Path) -> str:
    """假目录库：fields×datasets×regions（字段全集回退）+ expressions(region,dataset,family)。

    TB2/myds 是**同名数据集跨区**的诱饵行：两条读取路径都必须带 region 作用域，
    否则会把 TB2 的 g1/fam_x 静默并进 TST（见 load_db_field_universe 的 docstring 事故复盘）。
    """
    conn = sqlite3.connect(str(path))
    try:
        conn.executescript(
            "CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT);"
            "CREATE TABLE datasets (id INTEGER PRIMARY KEY, region_id INTEGER, name TEXT);"
            "CREATE TABLE fields (id INTEGER PRIMARY KEY, dataset_id INTEGER, field_name TEXT);"
            "CREATE TABLE expressions (id INTEGER PRIMARY KEY, region TEXT, dataset TEXT,"
            " expression TEXT, family TEXT);"
        )
        conn.execute("INSERT INTO regions (id, name) VALUES (1,'TST'),(2,'TB2')")
        conn.execute("INSERT INTO datasets (id, region_id, name) VALUES (11,1,'myds'),(12,2,'myds')")
        conn.execute("INSERT INTO fields (id, dataset_id, field_name) VALUES (1,11,'f1'),(2,11,'f2'),(3,12,'g1')")
        conn.execute("INSERT INTO expressions (id, region, dataset, expression, family) VALUES "
                     "(1,'TST','myds','rank(f1)','fam_d'),(2,'TST','myds','rank(f2)','fam_d'),"
                     "(3,'TB2','myds','rank(g1)','fam_x')")
        conn.commit()
    finally:
        conn.close()
    return str(path)


@pytest.fixture(scope="module")
def campaign_full(tmp_path_factory) -> Path:
    return _mk_campaign(tmp_path_factory.mktemp("fcov_full"))


@pytest.fixture(scope="module")
def campaign_nofields(tmp_path_factory) -> Path:
    return _mk_campaign(tmp_path_factory.mktemp("fcov_nofields"), with_fields=False)


@pytest.fixture(scope="module")
def catalog_db(tmp_path_factory) -> str:
    return _make_catalog_db(tmp_path_factory.mktemp("fcov_catalog") / "cat.db")


# ---------------------------------------------------------------- 1. 纯函数：模式解析与激活


def test_resolve_fcov_mode_priority_cli_env_default():
    """CLI > 环境变量 > 随区域闸的按日缺省 > 兜底 warn。"""
    assert wave_gate.resolve_fcov_mode("off", env={"WQB_FCOV_MODE": "enforce"}) == "off"
    assert wave_gate.resolve_fcov_mode(None, env={"WQB_FCOV_MODE": "enforce"}) == "enforce"
    assert wave_gate.resolve_fcov_mode(None, env={}, default="enforce") == "enforce"
    assert wave_gate.resolve_fcov_mode(None, env={}) == "warn"
    assert wave_gate.FCOV_DEFAULT_MODE == "warn"


def test_resolve_fcov_mode_invalid_value_falls_back():
    """拼错的 mode 不能静默关掉把关：落回合法 default；default 也非法时落 warn。"""
    assert wave_gate.resolve_fcov_mode(None, env={"WQB_FCOV_MODE": "bogus"}) == "warn"
    assert wave_gate.resolve_fcov_mode(None, env={"WQB_FCOV_MODE": "bogus"},
                                       default="enforce") == "enforce"
    assert wave_gate.resolve_fcov_mode("off", env={"WQB_FCOV_MODE": "OFF"}) == "off"
    assert wave_gate.resolve_fcov_mode(None, env={"WQB_FCOV_MODE": "OFF"}) == "off"


def test_fcov_activation_requires_boundary_config(tmp_path):
    """无 boundary_ops 配置 → 不激活（其余区域零行为变化）。"""
    meta = wave_gate._fcov_activation(str(tmp_path / "no_such"), REGION)
    assert meta["active"] is False
    assert meta["config_path"].endswith(f"boundary_ops_{REGION.lower()}.json")


def test_fcov_activation_enabled_false_disables(tmp_path):
    """配置存在但 enabled=false → 显式关（配置层逃生口）。"""
    camp = tmp_path / REGION
    _write(camp / "reference" / f"boundary_ops_{REGION.lower()}.json", {"enabled": False})
    meta = wave_gate._fcov_activation(str(camp), REGION)
    assert meta["active"] is False
    assert meta.get("disabled_by_config") is True


def test_fcov_activation_corrupt_config_stays_active(tmp_path):
    """配置损坏仍激活：让闸内 load_boundary_config 报错 fail-closed，不能静默变'不存在'。"""
    camp = tmp_path / REGION
    _write(camp / "reference" / f"boundary_ops_{REGION.lower()}.json", "{ not json !!")
    assert wave_gate._fcov_activation(str(camp), REGION)["active"] is True


# ---------------------------------------------------------------- 2. _run_full_coverage_gate（进程内）


def _run_fcov(camp, mode, items):
    ns = argparse.Namespace(dataset=DATASET)
    meta = {"active": True, "mode": mode,
            "config_path": os.path.join(str(camp), "reference",
                                        f"boundary_ops_{REGION.lower()}.json")}
    return wave_gate._run_full_coverage_gate(ns, str(camp), items, REGION, meta)


_TWO = [("1", "rank(f1)"), ("2", "rank(f2)")]
_ONE = [("1", "rank(f1)")]


def test_inactive_returns_none(campaign_full):
    ns = argparse.Namespace(dataset=DATASET)
    assert wave_gate._run_full_coverage_gate(
        ns, str(campaign_full), _TWO, REGION, {"active": False, "mode": "enforce"}) is None


def test_off_mode_skips_with_notice(campaign_full, capsys):
    r = _run_fcov(campaign_full, "off", _ONE)
    assert r["status"] == "off"
    out = capsys.readouterr().out
    assert "全量覆盖闸已按 --fcov-mode=off / WQB_FCOV_MODE=off 显式跳过（无把关）" in out


def test_no_candidates_skips(campaign_full):
    r = _run_fcov(campaign_full, "enforce", [])
    assert r["status"] == "skip" and r["reason"] == "no-candidates"


def test_enforce_full_coverage_all_gates_pass(campaign_full, tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WQB_DB_PATH", str(tmp_path / "none.db"))  # 确定性：族读不到 DB
    r = _run_fcov(campaign_full, "enforce", _TWO)
    assert r["status"] == "ok" and r["ok"] is True
    assert r["db_families"] == []
    gates = {g["gate"]: g for g in r["gates"]}
    assert gates["field_coverage"]["verdict"] == "PASS"
    assert gates["field_coverage"]["covered"] == 2
    assert gates["template_family"]["verdict"] == "PASS"   # 文件史 3 族
    assert gates["boundary_ops"]["verdict"] == "PASS"
    out = capsys.readouterr().out
    assert "2/2 = 100.00%" in out and "（DB 0 族）" in out


def test_enforce_partial_coverage_fails(campaign_full, tmp_path, monkeypatch):
    monkeypatch.setenv("WQB_DB_PATH", str(tmp_path / "none.db"))
    r = _run_fcov(campaign_full, "enforce", _ONE)
    assert r["status"] == "fail" and r["ok"] is False
    gates = {g["gate"]: g for g in r["gates"]}
    assert gates["field_coverage"]["verdict"] == "FAIL"
    assert gates["field_coverage"]["missing_count"] == 1


def test_warn_partial_coverage_downgrades(campaign_full, tmp_path, monkeypatch):
    monkeypatch.setenv("WQB_DB_PATH", str(tmp_path / "none.db"))
    r = _run_fcov(campaign_full, "warn", _ONE)
    assert r["status"] == "ok" and r["ok"] is True
    gates = {g["gate"]: g for g in r["gates"]}
    assert gates["field_coverage"]["verdict"] == "WARN"


def test_enforce_no_field_source_exits_2(campaign_nofields, tmp_path, monkeypatch, capsys):
    """enforce + 字段全集不可得 → exit 2（无门禁结论，与区域闸同码）。"""
    monkeypatch.setenv("WQB_DB_PATH", str(tmp_path / "none.db"))
    with pytest.raises(SystemExit) as ei:
        _run_fcov(campaign_nofields, "enforce", _ONE)
    assert ei.value.code == 2
    err = capsys.readouterr().err
    assert "整波拦截（exit 2" in err


def test_warn_no_field_source_degrades(campaign_nofields, tmp_path, monkeypatch):
    monkeypatch.setenv("WQB_DB_PATH", str(tmp_path / "none.db"))
    r = _run_fcov(campaign_nofields, "warn", _ONE)
    assert r["status"] == "unavailable"
    assert "DB 回退" in r["reason"]


def test_enforce_corrupt_boundary_config_exits_2(tmp_path, monkeypatch, capsys):
    """边界配置不可读：enforce fail-closed（exit 2），不是静默放行。"""
    camp = _mk_campaign(tmp_path, boundary="{ not json !!")
    monkeypatch.setenv("WQB_DB_PATH", str(tmp_path / "none.db"))
    with pytest.raises(SystemExit) as ei:
        _run_fcov(camp, "enforce", _TWO)
    assert ei.value.code == 2
    err = capsys.readouterr().err
    assert "边界算子配置不可读" in err and "整波拦截（exit 2" in err


# ---------------------------------------------------------------- 3. DB 回退与族历史（P0-1 ②③）


def test_load_db_families_region_scoped(catalog_db):
    assert fcg.load_db_families(REGION, DATASET, db_path=catalog_db) == ["fam_d"]
    assert fcg.load_db_families("TB2", DATASET, db_path=catalog_db) == ["fam_x"]
    # region 作用域是硬约束：TST 结果里不得混入 TB2 的族
    assert "fam_x" not in fcg.load_db_families(REGION, DATASET, db_path=catalog_db)


def test_load_db_families_missing_db_returns_empty(tmp_path):
    assert fcg.load_db_families(REGION, DATASET, db_path=str(tmp_path / "no.db")) == []


def test_load_db_field_universe_region_scoped(catalog_db):
    fields, note = fcg.load_db_field_universe(REGION, DATASET, db_path=catalog_db)
    assert fields == {"f1", "f2"} and note.startswith("db:")
    fields2, _ = fcg.load_db_field_universe("TB2", DATASET, db_path=catalog_db)
    assert fields2 == {"g1"}


def test_resolve_field_source_prefers_campaign_json(campaign_full, catalog_db):
    ns = argparse.Namespace(fields_list=None, all_fields=None, region=REGION,
                            dataset=DATASET, campaign_dir=str(campaign_full),
                            db_path=catalog_db)
    fields, src = fcg.resolve_field_source(ns)
    assert fields == {"f1", "f2"}
    assert src.endswith(f"{REGION.lower()}_{DATASET}_fields.json")


def test_resolve_field_source_falls_back_to_db(campaign_nofields, catalog_db):
    """字段目录 JSON 缺席 → 回退 DB catalog（EUR/analyst7 形态：全集只在 DB 里）。"""
    ns = argparse.Namespace(fields_list=None, all_fields=None, region=REGION,
                            dataset=DATASET, campaign_dir=str(campaign_nofields),
                            db_path=catalog_db)
    fields, src = fcg.resolve_field_source(ns)
    assert fields == {"f1", "f2"}
    assert src.startswith("db:")


def test_db_fallback_feeds_family_gate(catalog_db, tmp_path, monkeypatch):
    """整合：JSON 缺席 + 无文件史（DB-only 新波形态）→ 字段全集与族历史都从 DB 取。"""
    camp = _mk_campaign(tmp_path, with_fields=False, with_candidates=False)
    monkeypatch.setenv("WQB_DB_PATH", catalog_db)
    r = _run_fcov(camp, "warn", _TWO)
    assert r["fields_source"].startswith("db:")
    assert r["db_families"] == ["fam_d"]
    gates = {g["gate"]: g for g in r["gates"]}
    assert gates["field_coverage"]["verdict"] == "PASS"
    fam = gates["template_family"]
    assert fam["verdict"] == "WARN"          # 1/3 < 3 → warn 降级
    assert fam["total"] == 1 and fam["used_families"] == ["fam_d"]


def test_store_written_family_readable_by_gate(tmp_path):
    """写读闭环：CampaignStore 写入的 family（GEM skeleton 落库路径）能被族闸读到。"""
    from wqb.store import CampaignStore

    db = str(tmp_path / "store.db")
    st = CampaignStore(db)
    try:
        st.upsert_expressions(REGION, "1", [{"expression": "rank(f1)", "family": "store_fam"}],
                              dataset=DATASET)
    finally:
        st.close()
    assert fcg.load_db_families(REGION, DATASET, db_path=db) == ["store_fam"]


# ---------------------------------------------------------------- 4. waiver 集成：降级必须留痕


def _waiver_args():
    return argparse.Namespace(skip_diversity_gate=False, skip_semantic_gate=False,
                              semantic_gate=None, prod_family_gate=True,
                              gate_mode=None, waiver_mode="off", wave="s2_pytest")


def test_waiver_phase_no_fcov_escape_when_inactive_or_not_downgraded(tmp_path, monkeypatch):
    monkeypatch.delenv("WQB_SEM_MODE", raising=False)
    args = _waiver_args()
    camp = str(tmp_path)
    assert wave_gate._waiver_phase(args, camp, REGION, "warn", None, None) == []
    assert wave_gate._waiver_phase(
        args, camp, REGION, "warn", None, {"active": True, "downgraded": False}) == []


def test_waiver_phase_records_downgrade_with_escape_flag(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("WQB_SEM_MODE", raising=False)
    meta = {"active": True, "downgraded": True, "escape_flag": "--fcov-mode warn"}
    decisions = wave_gate._waiver_phase(_waiver_args(), str(tmp_path), REGION, "warn", None, meta)
    assert len(decisions) == 1
    d = decisions[0]
    assert d.gate == "full_coverage" and d.flag == "--fcov-mode warn" and d.ok is True
    assert "被跳过" in capsys.readouterr().out


def test_waiver_phase_defaults_escape_flag_to_off(tmp_path, monkeypatch):
    monkeypatch.delenv("WQB_SEM_MODE", raising=False)
    meta = {"active": True, "downgraded": True, "escape_flag": None}
    decisions = wave_gate._waiver_phase(_waiver_args(), str(tmp_path), REGION, "warn", None, meta)
    assert [d.flag for d in decisions] == ["--fcov-mode off"]


# ---------------------------------------------------------------- 5. 子进程端到端（4 变体）


@pytest.fixture(scope="module")
def e2e(tmp_path_factory):
    root = tmp_path_factory.mktemp("fcov_e2e")
    camp = _mk_campaign(root)
    full = root / "full.txt"
    full.write_text("rank(f1)\nrank(f2)\n", encoding="utf-8")
    one = root / "one.txt"
    one.write_text("rank(f1)\n", encoding="utf-8")
    return {"root": root, "camp": camp, "full": full, "one": one}


def _run_e2e(e2e, tag, exprs_file, fcov_mode):
    """子进程实跑 wave_gate：独立库 + 仓库内 toolkit/verifier 钉死（hermetic）。

    注意：FCV 闸在候选入库**之前**跑（main 之序），故此处的族历史恒为
    「文件 3 族 + DB 0 族」——DB 侧由进程内用例覆盖。
    """
    env = {k: v for k, v in os.environ.items()
           if k not in ("WQB_FCOV_MODE", "WQ_TEMPLATE_FAMILY")}
    env.update({
        "WQB_DB_PATH": str(e2e["root"] / f"{tag}.db"),
        "WQ_TOOLKIT_DIR": str(REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"),
        "WQ_VALIDATOR_DIR": str(REPO / "Claude" / "skills" / "alpha-expression-verifier" / "scripts"),
    })
    cmd = [sys.executable, str(REPO / "tools" / "wave_gate.py"),
           "--campaign-dir", str(e2e["camp"]), "--region", REGION, "--dataset", DATASET,
           "--wave", tag, "--exprs-file", str(exprs_file),
           "--fcov-mode", fcov_mode,
           "--skip-diversity-gate", "--skip-quality", "--skip-semantic-gate",
           "--inspect-mode", "off", "--gate-mode", "warn", "--waiver-mode", "off"]
    return subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=300, env=env)


def test_e2e_enforce_full_coverage_passes(e2e):
    r = _run_e2e(e2e, "s2_pytest_fcov_a", e2e["full"], "enforce")
    out = (r.stdout or "") + (r.stderr or "")
    assert r.returncode == 0, out[-2500:]
    assert "2/2 = 100.00%" in out
    assert "FCov=PASS(mode=enforce)" in out
    assert "全量覆盖闸拦截" not in out
    assert "（DB 0 族）" in out


def test_e2e_enforce_partial_blocks_wave(e2e):
    """核心回归：gate.py 本身全过（all_pass=true），但 FCV enforce FAIL 折叠成整波 FAIL。"""
    r = _run_e2e(e2e, "s2_pytest_fcov_b", e2e["one"], "enforce")
    out = (r.stdout or "") + (r.stderr or "")
    assert r.returncode == 1, out[-2500:]
    assert "FAIL  1/2 = 50.00%（缺 1）" in out
    assert "全量覆盖闸拦截：field_coverage 未过" in out
    assert "gate all_pass=true" in out
    assert "FCov=FAIL(mode=enforce)" in out


def test_e2e_warn_partial_passes_with_warn_line(e2e):
    r = _run_e2e(e2e, "s2_pytest_fcov_c", e2e["one"], "warn")
    out = (r.stdout or "") + (r.stderr or "")
    assert r.returncode == 0, out[-2500:]
    assert "WARN  1/2 = 50.00%（缺 1）" in out
    assert "FCov=PASS(mode=warn)" in out


def test_e2e_off_skips_gate(e2e):
    r = _run_e2e(e2e, "s2_pytest_fcov_d", e2e["one"], "off")
    out = (r.stdout or "") + (r.stderr or "")
    assert r.returncode == 0, out[-2500:]
    assert "全量覆盖闸已按 --fcov-mode=off / WQB_FCOV_MODE=off 显式跳过（无把关）" in out
    assert "FCov=" not in out