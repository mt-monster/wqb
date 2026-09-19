# -*- coding: utf-8 -*-
"""catalog 前置闸（第 0 道）守卫测试（S123 报告建议③，2026-09-17）。

背景（实测）：全库 25% 白名单数据集（23/93）无 typed catalog——这些集的波在
gate.py 必崩 FileNotFoundError（异常式失败而非干净拒绝），或积压成无门禁死库存
（385 波 / 6,311 条从未过闸；JPN 白名单 12 集缺 10）。

修复：`_lib/region_gates.py` 新增第 0 道 `catalog` 闸——判定单源 =
`gate.load_whitelist`（与真门禁同一条解析路径），在开波/开区前拒绝。
本测试锁定：
  1. 单数据集语义：有 catalog 放行 / 缺 catalog 命中（错误信息含修复入口）；
  2. 开区语义（dataset=None）：白名单全覆盖检查，缺集进 evidence.missing；
  3. enforce 模式阻断 + C 模块不可用时 catalog 结果仍落 report（三闸缺检不吞 catalog）；
  4. s0_whitelist 归一走 wqb.ledger_whitelist 单源（JPN 型 datasets 键直认）。
"""
import json
import os
import sqlite3
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TK_SCRIPTS = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")


@pytest.fixture(scope="module")
def rg():
    sys.path.insert(0, TK_SCRIPTS)
    from _lib import region_gates as _rg  # noqa: PLC0415
    return _rg


def _make_campaign(tmp_path, datasets_in_whitelist, with_catalog=()):
    """构造最小战役区：tracking/TST/{config,reference} + data/wqb.db（s0_whitelist）。"""
    cdir = tmp_path / "tracking" / "TST"
    (cdir / "config").mkdir(parents=True)
    (cdir / "reference").mkdir(parents=True)
    (cdir / "config" / "settings.json").write_text(
        json.dumps({"region": "TST"}), encoding="utf-8")
    (cdir / "config" / "thresholds.json").write_text("{}", encoding="utf-8")
    # typed catalog 文件（gate.load_whitelist 的第 2 优先解析源）
    for ds in with_catalog:
        (cdir / "reference" / f"tst_{ds}_fields.json").write_text(
            json.dumps({"data_type": "MATRIX",
                        "fields": [{"id": "f1", "type": "MATRIX"}]}),
            encoding="utf-8")
    # 工作区标记 data/wqb.db + ledger s0_whitelist（resolve_workspace_root 的认据）
    db = tmp_path / "data" / "wqb.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE ledger_kv (id INTEGER PRIMARY KEY, region TEXT, key TEXT,"
                 " value TEXT, created_at TEXT, updated_at TEXT)")
    if datasets_in_whitelist is not None:
        conn.execute("INSERT INTO ledger_kv (region, key, value) VALUES (?,?,?)",
                     ("TST", "s0_whitelist",
                      json.dumps({"datasets": datasets_in_whitelist,
                                  "generated_at": "2026-09-17"})))
    conn.commit()
    conn.close()
    return str(cdir), str(db)


# --------------------------------------------------------------------------- 1
def test_single_dataset_missing_is_hit(rg, tmp_path):
    cdir, _ = _make_campaign(tmp_path, ["ds_a"])
    r = rg._run_catalog_gate("TST", "ds_missing", cdir)
    assert r["success"] is False
    assert "scan_fields.py" in r["error"], "错误信息必须给出修复入口"
    assert r["evidence"]["missing"] == ["ds_missing"]


def test_single_dataset_present_passes(rg, tmp_path):
    cdir, _ = _make_campaign(tmp_path, ["ds_a"], with_catalog=["ds_a"])
    r = rg._run_catalog_gate("TST", "ds_a", cdir)
    assert r["success"] is True, r
    assert r["evidence"]["have_catalog"] == 1


# --------------------------------------------------------------------------- 2
def test_region_scope_reports_missing(rg, tmp_path):
    cdir, _ = _make_campaign(tmp_path, ["ds_ok", "ds_bad1", "ds_bad2"],
                             with_catalog=["ds_ok"])
    r = rg._run_catalog_gate("TST", None, cdir)
    assert r["success"] is False
    assert r["scope"].startswith("TST")
    assert r["evidence"] == {"datasets": 3, "have_catalog": 1,
                             "missing": ["ds_bad1", "ds_bad2"]}


def test_region_scope_no_whitelist_warns_not_blocks(rg, tmp_path):
    cdir, _ = _make_campaign(tmp_path, None)  # 不写 s0_whitelist
    r = rg._run_catalog_gate("TST", None, cdir)
    assert r["success"] is True, "读不到白名单必须告警放行（环境问题不阻断）"
    assert "warning" in r


# --------------------------------------------------------------------------- 3
def test_enforce_blocks_on_catalog_even_without_workflow_module(rg, tmp_path, monkeypatch):
    """C 模块不可用（tmp 无 src/wqb）时：三道区域闸缺检要显式告警，
    但 catalog 命中仍须让 enforce 的 ok=False —— 缺检不能吞掉已判定的命中。"""
    monkeypatch.delenv("WQB_DISABLE_REGION_GATES", raising=False)
    cdir, _ = _make_campaign(tmp_path, ["ds_missing"])
    out = __import__("io").StringIO()
    rep = rg.run_region_gates(cdir, "TST", mode="enforce", dataset="ds_missing", out=out)
    assert rep["results"]["catalog"]["success"] is False
    assert "catalog" in rep["hits"]
    assert rep["ok"] is False
    assert rep.get("skipped_reason"), "三闸缺检原因必须显式留痕"


def test_enforce_passes_when_catalog_present(rg, tmp_path, monkeypatch):
    monkeypatch.delenv("WQB_DISABLE_REGION_GATES", raising=False)
    cdir, _ = _make_campaign(tmp_path, ["ds_a"], with_catalog=["ds_a"])
    out = __import__("io").StringIO()
    rep = rg.run_region_gates(cdir, "TST", mode="enforce", dataset="ds_a", out=out)
    assert rep["results"]["catalog"]["success"] is True
    assert "catalog" not in rep.get("hits", [])
    assert rep["ok"] is True


# --------------------------------------------------------------------------- 4
def test_whitelist_reader_uses_jpn_style_datasets_key(rg, tmp_path, monkeypatch):
    """归一主路径：wqb.ledger_whitelist（P0-4）能吃 JPN 型顶层 datasets 键。"""
    cdir, _ = _make_campaign(tmp_path, ["x1", "x2"])
    datasets, err = rg._region_whitelist_datasets(cdir, "TST")
    assert err is None
    assert datasets == ["x1", "x2"]
