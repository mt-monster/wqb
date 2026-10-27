# -*- coding: utf-8 -*-
"""GEM priors 过期拦截（2026-10-20 P1-5）。

背景：`_priors_snapshot_freshness` 早已能识别「快照落后于 KB 源」（S6 回写 /
判死封存 / 登记 win 之后没重组 priors），但只发 warning —— 自动化链会在无人
察觉时整波沿用旧先验。本测试守护升级后的语义：

  1. step 上标 `stale`（True=快照落后于 KB 源；缺快照不算 stale——子进程自身 fail-closed）
  2. **实跑** stale 即 success=False + 修复指令（含 assemble-priors 与放行开关名）
  3. **干跑**只告警（统一 dry-run 语义：回答"链能不能跑通"，不回答"先验新不新"）
  4. 显式 `allow_stale_priors=True` 放行，并在结果上留痕 `priors_stale_overridden`
"""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT, REPO_ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402

import json  # noqa: E402
import sqlite3  # noqa: E402


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()
    return path


def _ledger(db_path, region, key, updated_at):
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "INSERT INTO ledger_kv (region, key, value, created_at, updated_at) VALUES (?,?,?,?,?)",
        (region, key, json.dumps({"wins": [], "dead_ends": []}), updated_at, updated_at),
    )
    conn.commit()
    conn.close()


def _stale_db(db_path):
    """快照 09-20 写、region_kb 09-21 更新 → stale。"""
    _ledger(db_path, "KOR", "priors_snapshot_kor", "2026-09-20T10:00:00")
    _ledger(db_path, "KOR", "region_kb", "2026-09-21T09:00:00")


def test_step_flags_stale_true(db_path, monkeypatch):
    from wqb.workflow.nodes import gem

    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    _stale_db(db_path)
    step = gem._priors_snapshot_freshness("KOR")
    assert step["stale"] is True
    assert step["stale_sources"]


def test_step_fresh_and_missing_not_stale(db_path, monkeypatch):
    from wqb.workflow.nodes import gem

    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    _ledger(db_path, "KOR", "region_kb", "2026-09-21T09:00:00")
    _ledger(db_path, "KOR", "priors_snapshot_kor", "2026-09-21T09:05:00")
    assert gem._priors_snapshot_freshness("KOR")["stale"] is False

    _ledger(db_path, "EUR", "region_kb", "2026-09-21T09:00:00")  # 无快照
    step = gem._priors_snapshot_freshness("EUR")
    assert step["stale"] is False
    assert "fail-closed" in step["warning"]


def test_real_run_blocked_when_stale(db_path, monkeypatch):
    """实跑 stale：Step 1.5 直接拦下，不找 skill、不建命令、不起进程。"""
    from wqb.workflow.nodes import gem

    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    _stale_db(db_path)
    result = gem.run(region="KOR", dataset_id="analyst44", delay=1, universe="TOP600",
                     data_category="analyst", _context={})
    assert result["success"] is False
    assert "早于其 KB 源" in result["error"]
    assert "assemble-priors" in result["error"]
    assert "allow_stale_priors" in result["error"]
    assert result["priors_stale"] is True
    assert result.get("command") is None, "被拦时不应构建出命令"
    step = next(s for s in result["steps"] if s.get("step") == "priors_snapshot_check")
    assert step["stale"] is True


def test_dry_run_only_warns_when_stale(db_path, monkeypatch):
    from wqb.workflow.nodes import gem

    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    _stale_db(db_path)
    # 显式 data_category：infer_data_category 会走 _common._platform_category、
    # 不认 WQB_DB_PATH（同 test_p0_fixes_20260927 的既有注释）
    result = gem.run(region="KOR", dataset_id="analyst44", delay=1, universe="TOP600",
                     data_category="analyst", _context={"dry_run": True})
    step = next(s for s in result["steps"] if s.get("step") == "priors_snapshot_check")
    assert step["stale"] is True
    assert step["warning"] in result.get("warnings", [])
    assert result["priors_stale"] is True
    # 干跑不被拦截：拦截错误（含放行开关指引）不出现
    assert "确需用旧先验继续" not in str(result.get("error"))
    assert "allow_stale_priors" not in str(result.get("error"))


def test_allow_stale_priors_overrides_block(db_path, monkeypatch, tmp_path):
    """显式 allow_stale_priors=True：越过拦截点（用假 skill 目录 + 假执行收口，不起进程）。"""
    from wqb.workflow.nodes import gem

    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    _stale_db(db_path)

    fake_gem = tmp_path / "gem"
    runner = fake_gem / "scripts" / "headless_runner"
    runner.mkdir(parents=True)
    (runner / "run.py").write_text("# dispatcher, no argparse\n", encoding="utf-8")
    (runner / "config.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(gem, "resolve_skill_dir", lambda name: str(fake_gem))

    calls = {}
    def _fake_execute(*a, **k):
        calls["executed"] = True
        return False  # 收口，不做产物检查
    monkeypatch.setattr(gem, "_execute_gem", _fake_execute)

    result = gem.run(region="KOR", dataset_id="analyst44", delay=1, universe="TOP600",
                     data_category="analyst", allow_stale_priors=True, _context={})
    assert calls.get("executed") is True, "override 后应走到执行步"
    assert result.get("priors_stale_overridden") is True
    assert result["priors_stale"] is True