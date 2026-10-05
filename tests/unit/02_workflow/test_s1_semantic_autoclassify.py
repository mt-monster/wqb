# -*- coding: utf-8 -*-
"""步3 断流修复 · 通气 B：S1 自动补做语义归类（2026-10-01）的回归护栏。

契约：`workflow_campaign(stage="S1")` 在 typed catalog 扫描之外，附带一次
`s1_semantic_<ds>` 覆盖检查——**缺台账 `missing_ledger` 或缺 L3.5 `families` 段
`missing_families`**，二者同等触发自动跑 `field_semantic_classify.py --write-ledger`
（本地零配额秒级）；台账齐备（含 families）才跳过。**fail-open**：任何失败只记
warning，不阻断 S1。

起因（实测）：全库 catalog 697 个，语义台账仅 33 个（4.7%），EUR/IND/GLB/JPN 为 0。
语义归类此前靠人工记忆单跑，导致步 5 闸 SEM 只能靠"阻断"而非"过滤"生效。

**缺 families 亦需补做（2026-10-01 修订）**：L3.5 族是 L4 形态构建五步法的第一步输入，
而 414 个台账里仅 76 个（18.4%）带 families、338 个是旧版。旧实现见台账存在即 return、
只提示不重跑 ⇒ L4 在 81.6% 的数据集上拿不到族，属**断流**而非"待优化"。
"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
for _p in (REPO, REPO / "src", REPO / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.workflow.nodes import campaign as camp_mod  # noqa: E402


@pytest.fixture
def db_with_ledger(tmp_path, monkeypatch):
    db_path = tmp_path / "wqb.db"
    from wqb.store import CampaignStore
    CampaignStore(str(db_path)).close()
    monkeypatch.setattr(camp_mod, "resolve_db_path", lambda *a, **k: str(db_path))
    return str(db_path)


def _insert_semantic(db, ds, payload):
    conn = sqlite3.connect(db)
    conn.execute("INSERT OR REPLACE INTO ledger_kv (region,key,value,updated_at) "
                 "VALUES ('KOR',?,?, '2026-10-01')",
                 (f"s1_semantic_{ds}", json.dumps(payload)))
    conn.commit()
    conn.close()


def test_existing_ledger_skips_subprocess(db_with_ledger, monkeypatch):
    """台账已有 → 不重复跑脚本（零成本）。"""
    _insert_semantic(db_with_ledger, "model1",
                     {"total_fields": 10, "blocked_field_count": 2,
                      "families": {"f": {"n": 2}}})
    called = []
    monkeypatch.setattr(camp_mod.subprocess, "run",
                        lambda *a, **k: called.append(a) or (_ for _ in ()).throw(AssertionError("不应调用")))
    step = camp_mod._semantic_coverage_check("KOR", "model1")
    assert step["success"] is True
    assert step["ledger"] is True
    assert step["blocked_field_count"] == 2
    assert step["has_families"] is True
    assert called == []


def test_old_ledger_without_families_triggers_autoclassify(db_with_ledger, monkeypatch):
    """旧版台账（无 L3.5 families 段）必须触发重跑——L4 形态构建的输入，只提示=断流。"""
    _insert_semantic(db_with_ledger, "model1", {"total_fields": 10, "blocked_field_count": 0})
    seen = {}

    class _P:
        returncode = 0
        stdout = "ok"
        stderr = ""

    def fake_run(cmd, **kw):
        seen["cmd"] = cmd
        return _P()

    monkeypatch.setattr(camp_mod.subprocess, "run", fake_run)
    step = camp_mod._semantic_coverage_check("KOR", "model1")
    assert step["ledger"] is True
    assert step["has_families"] is False
    assert step["success"] is True                      # 不阻断
    assert step.get("auto_ran") is True
    assert step.get("reason") == "missing_families"     # 与缺台账区分
    cmd = seen["cmd"]
    assert any("field_semantic_classify.py" in str(c) for c in cmd)
    assert "--write-ledger" in cmd and "model1" in cmd


def test_old_ledger_without_families_failure_is_fail_open(db_with_ledger, monkeypatch):
    """缺 families 的补做失败 → 只 warning，不阻断。"""

    class _P:
        returncode = 1
        stdout = ""
        stderr = "boom"

    _insert_semantic(db_with_ledger, "model1", {"total_fields": 10, "blocked_field_count": 0})
    monkeypatch.setattr(camp_mod.subprocess, "run", lambda *a, **k: _P())
    step = camp_mod._semantic_coverage_check("KOR", "model1")
    assert step["success"] is True
    assert "warning" in step
    assert "field_semantic_classify" in step["warning"]


def test_new_ledger_with_empty_families_skips_subprocess(db_with_ledger, monkeypatch):
    """新版台账（有 family_stats）但族为空 → **不重跑**。

    原生集（fundamental*/pv*/news*）字段名不带角色后缀，空族是**正确结果**；
    若按"族为空"判定补做，这些集永远达不到"完整"状态 ⇒ S1 每次都重跑、永不幂等。
    """
    _insert_semantic(db_with_ledger, "pv1", {
        "total_fields": 10, "blocked_field_count": 0,
        "families": {}, "family_stats": {"n_families": 0, "n_triclass": 0},
    })
    called = []
    monkeypatch.setattr(camp_mod.subprocess, "run",
                        lambda *a, **k: called.append(a) or (_ for _ in ()).throw(AssertionError("不应调用")))
    step = camp_mod._semantic_coverage_check("KOR", "pv1")
    assert step["ledger"] is True
    assert step["has_families"] is True        # 含 L3.5 能力
    assert step["family_count"] == 0           # 但确实无族
    assert called == []
    assert "退化" in step.get("info", ""), "族为空时应提示 L4 退化到 by_category"


def test_missing_ledger_triggers_autoclassify(db_with_ledger, monkeypatch):
    """缺台账 → 调 field_semantic_classify.py --write-ledger。"""
    seen = {}

    class _P:
        returncode = 0
        stdout = "ok"
        stderr = ""

    def fake_run(cmd, **kw):
        seen["cmd"] = cmd
        return _P()

    monkeypatch.setattr(camp_mod.subprocess, "run", fake_run)
    step = camp_mod._semantic_coverage_check("KOR", "brandnew")
    assert step["success"] is True
    assert step.get("auto_ran") is True
    assert step.get("reason") == "missing_ledger"
    cmd = seen["cmd"]
    assert any("field_semantic_classify.py" in str(c) for c in cmd)
    assert "--write-ledger" in cmd
    assert "brandnew" in cmd
    assert "KOR" in cmd


def test_autoclassify_failure_is_fail_open(db_with_ledger, monkeypatch):
    """脚本失败 → 只 warning，不阻断（把关在步 5 闸 SEM）。"""
    class _P:
        returncode = 1
        stdout = ""
        stderr = "boom"

    monkeypatch.setattr(camp_mod.subprocess, "run", lambda *a, **k: _P())
    step = camp_mod._semantic_coverage_check("KOR", "brandnew")
    assert step["success"] is True          # 不阻断
    assert "warning" in step
    assert "field_semantic_classify" in step["warning"]


def test_exception_is_fail_open(monkeypatch):
    """任意异常 → warning，不抛。"""
    monkeypatch.setattr(camp_mod, "resolve_db_path",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("no db")))
    step = camp_mod._semantic_coverage_check("KOR", "x")
    assert step["success"] is True
    assert "warning" in step


def test_no_dataset_is_noop(db_with_ledger):
    step = camp_mod._semantic_coverage_check("KOR", "")
    assert step["success"] is True and "跳过" in step.get("message", "")
