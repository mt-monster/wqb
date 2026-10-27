"""field-profile 子命令：workflow 路由 + toolkit 分发 + 生成器落盘。"""
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from wqb.store.campaign import CampaignStore

ROOT = Path(__file__).resolve().parents[3]
TOOLKIT = ROOT / "Claude/skills/wq-brain-campaign-toolkit/scripts"

_PERF_DDL = """CREATE TABLE IF NOT EXISTS field_profile_perf (
    region TEXT, dataset TEXT, field TEXT, ftype TEXT, coverage REAL, family TEXT,
    n_tests INTEGER, to_med REAL, best_s REAL, best_2y REAL, best_sub REAL, best_f REAL,
    verdict TEXT, best_s_sg REAL, best_2y_sg REAL, best_sub_sg REAL, n_sg INTEGER,
    n_skeletons INTEGER, skeleton_fams TEXT)"""


@pytest.fixture
def db(tmp_path):
    """最小画像库：region/datasets/fields + 1 条 COMPLETE 回测 + 1 条 ALIVE 画像。"""
    path = tmp_path / "wqb.db"
    with CampaignStore(str(path)) as store:
        store.upsert_field_catalog("EUR", {"dataset": "sample", "fields": [
            {"id": "cash", "type": "MATRIX", "coverage": .8, "userCount": 2,
             "description": "cash balance"},
            {"id": "assets", "type": "MATRIX", "coverage": .9, "userCount": 1,
             "description": "total assets"},
        ]})
        store.upsert_backtest_rows("EUR", "S6TEST", [{
            "id": "A", "code": "rank(cash)", "status": "COMPLETE", "sharpe": 1.6,
            "fitness": 1.0, "two_year_sharpe": 1.8, "turnover": .02, "delay": 1,
            "universe": "TOP3000", "neutralization": "SUBINDUSTRY",
        }], dataset="sample")
    with sqlite3.connect(path) as con:
        # CampaignStore 的 datasets 表没有 delay 列（生产库由迁移补）；生成器要读它。
        if "delay" not in {r[1] for r in con.execute("PRAGMA table_info(datasets)")}:
            con.execute("ALTER TABLE datasets ADD COLUMN delay INTEGER")
        con.execute(_PERF_DDL)
        con.execute(
            "INSERT INTO field_profile_perf "
            "(region,dataset,field,ftype,coverage,family,n_tests,best_s,best_s_sg,verdict) "
            "VALUES ('EUR','sample','cash','MATRIX',0.8,'cash',3,1.3,1.62,'ALIVE')")
    return path


def test_campaign_route_has_dataset_and_no_wave(monkeypatch):
    from wqb.workflow.nodes import campaign

    monkeypatch.setattr(campaign, "resolve_toolkit_dir", lambda: str(TOOLKIT))
    result = campaign.run(
        region="EUR", stage="S6", subcommand="field-profile",
        dataset="sample", wave="S6TEST", _context={"dry_run": True})
    assert result["success"], result
    command = next(s["command"] for s in result["steps"] if s["step"] == "build_command")
    assert command.count(" field-profile") == 1
    assert "--dataset sample" in command
    # 字段画像是区域级产物：节点不得把 --wave 拼进命令（目标脚本也不认）
    assert "--wave" not in command


def test_toolkit_dispatch_writes_docs_and_strips_wave(db, tmp_path):
    out = tmp_path / "docs"
    proc = subprocess.run([
        sys.executable, "-X", "utf8", str(TOOLKIT / "campaign.py"),
        "--campaign-dir", str(ROOT / "tracking/EUR"), "field-profile",
        "--dataset", "sample", "--db", str(db), "--out-dir", str(out),
        "--wave", "S6TEST"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=60)
    assert proc.returncode == 0, proc.stderr

    doc = (out / "sample_field_profile.md").read_text(encoding="utf-8")
    assert "BEGIN WQB FIELD PROFILE" in doc
    assert "`cash`" in doc and "`assets`" in doc
    assert "`A`" in doc                      # 本地 COMPLETE 回测被读到

    readme = (out / "README.md").read_text(encoding="utf-8")
    assert "EUR 数据集字段画像索引" in readme
    assert "sample_field_profile.md" in readme


def test_toolkit_dispatch_dry_run_has_no_output_side_effects(db, tmp_path):
    out = tmp_path / "never-created"
    proc = subprocess.run([
        sys.executable, "-X", "utf8", str(TOOLKIT / "campaign.py"),
        "--campaign-dir", str(ROOT / "tracking/EUR"), "field-profile",
        "--dataset", "sample", "--db", str(db), "--out-dir", str(out), "--dry-run"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert not out.exists()


def test_dispatcher_requires_region_or_campaign_dir(tmp_path):
    """没有 --campaign-dir 且工作目录不在仓库内 → 明确报错，不猜区域。"""
    proc = subprocess.run([
        sys.executable, "-X", "utf8", str(TOOLKIT / "dataset_profile_doc.py")],
        cwd=str(tmp_path), capture_output=True, text=True, encoding="utf-8", timeout=30)
    assert proc.returncode != 0
    assert "--campaign-dir" in proc.stderr or "--campaign-dir" in proc.stdout


def _load_dispatcher():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "wqb_test_toolkit_dataset_profile_doc", TOOLKIT / "dataset_profile_doc.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_region_prefers_campaign_settings_json(tmp_path):
    """区域优先取 campaign 目录的 config/settings.json（toolkit 纪律的唯一来源）。"""
    mod = _load_dispatcher()
    cdir = tmp_path / "EUR"
    (cdir / "config").mkdir(parents=True)
    (cdir / "config" / "settings.json").write_text(
        '{"region": "EUR", "delay": 1}', encoding="utf-8")
    assert mod._region_from_settings(str(cdir)) == "EUR"

    # 坏 JSON / 缺 region 键 ⇒ None（交调用方退回目录名，不静默猜错区）
    (cdir / "config" / "settings.json").write_text("{ broken", encoding="utf-8")
    assert mod._region_from_settings(str(cdir)) is None
    (cdir / "config" / "settings.json").write_text('{"delay": 1}', encoding="utf-8")
    assert mod._region_from_settings(str(cdir)) is None
    assert mod._region_from_settings(str(tmp_path / "nope")) is None
    assert mod._region_from_settings(None) is None
