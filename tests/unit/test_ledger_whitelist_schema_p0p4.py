# -*- coding: utf-8 -*-
"""P0-4 `s0_whitelist` 契约统一（2026-09-17）.

背景（实测）：同一 ledger 键在 13 个区域有 5 种形态，3 个消费者各按己见解析且
**全部 fail-open**（读不懂就当空集）：
  - tools/campaign_intel.py            只认 candidates[].dataset（命中 4/13）
  - score_datasets.py P3 universe 守卫   DEU/JPN/MEA/USA/GLB 未记 universe → 静默跳过
  - workflow/nodes/campaign.py           只认 filter_criteria（全区域不存在 = 死代码）
  - tracking/USA/batch_dryrun_driver.py  硬取 ["whitelist"]（迁移后会 KeyError）

修复：`src/wqb/ledger_whitelist.py` 提供容错归一（单一契约入口）+ 迁移脚本
`tools/normalize_ledger_whitelist.py`（幂等 / _legacy 备份 / 断点续跑）。

本测试覆盖：
  1. 5 种历史形态全部可归一（含 GBR 式"双重编码 + 内层截断"抢救）；
  2. 读不懂时 ok=False + reason（**不得**伪装成空集）；
  3. 真实库中不该再有形态漂移（防第 6 种形态再生）。
"""
import json
import os
import sqlite3

import pytest

from wqb import ledger_whitelist as LW
from wqb.workflow import _common

DB = os.path.join(str(_common.REPO_ROOT), "data", "wqb.db")


# --------------------------------------------------------------------- 1
def test_normalize_candidates_shape():
    rec = LW.normalize(json.dumps({
        "candidates": [{"dataset": "model101", "override": {"reason": "x"}},
                       {"dataset": "pv13"}],
        "settings": {"universe": "TOP2000U"},
    }))
    assert rec["ok"] and rec["schema"] == "candidates"
    assert rec["datasets"] == ["model101", "pv13"]
    assert rec["universe"] == "TOP2000U"
    assert rec["entries"] and rec["entries"][0]["override"] == {"reason": "x"}


def test_normalize_whitelist_shape_string_list():
    rec = LW.normalize(json.dumps({"whitelist": ["a1", "b2"], "universe": "TOP800"}))
    assert rec["ok"] and rec["schema"] == "whitelist"
    assert rec["datasets"] == ["a1", "b2"]
    assert rec["universe"] == "TOP800"


def test_normalize_datasets_shape():
    rec = LW.normalize(json.dumps({"datasets": ["x1"], "universe": "TOP500", "delay": 1}))
    assert rec["ok"] and rec["schema"] == "datasets"
    assert rec["datasets"] == ["x1"] and rec["delay"] == 1


def test_normalize_inferred_shape_from_other_lists():
    """ASI/GLB 形态：无标准键，需从其它列表字段推断。"""
    rec = LW.normalize(json.dumps({
        "counts": [{"dataset": "zz1"}, {"dataset": "zz2"}],
        "gate": {"x": 1}, "delay": 1,
    }))
    assert rec["ok"] and rec["schema"] == "inferred"
    assert set(rec["datasets"]) == {"zz1", "zz2"}


# --------------------------------------------------------------------- 2
def test_recover_truncated_double_encoded():
    """GBR 形态：JSON 串内再包一层 JSON，且内层被截断 → 必须按字段正则抢救。"""
    inner = ('{"generated_at": "2026-09-12T20:05", "universe": "TOP700", "delay": 1, '
             '"whitelist": ["pv47", "model250", "option1"], "note": ["cut off here')
    raw = json.dumps(inner)          # 双重编码
    rec = LW.normalize(raw)
    assert rec["double_encoded"] is True
    assert rec["ok"] is True, f"损坏记录未抢救成功: {rec['reason']}"
    assert rec["universe"] == "TOP700"
    assert set(rec["datasets"]) == {"pv47", "model250", "option1"}


def test_unparsable_returns_explicit_failure_not_empty():
    """核心回归：读不懂必须显式失败，绝不能静默返回空集（fail-open）。"""
    for bad in (None, 123, "not json at all", json.dumps(["a", "b"]),
                json.dumps({"totally": "unrelated", "keys": 1})):
        rec = LW.normalize(bad)
        assert rec["ok"] is False, f"{bad!r} 不应被当作可读"
        assert rec["reason"], "失败必须带原因，供调用方 WARN"


def test_empty_list_key_reports_reason():
    rec = LW.normalize(json.dumps({"whitelist": []}))
    assert rec["ok"] is False
    assert "无有效数据集" in rec["reason"]


def test_to_canonical_keeps_legacy_and_source():
    rec = LW.normalize(json.dumps({"whitelist": ["d1"], "universe": "TOP1600"}))
    canon = LW.to_canonical(rec, keep_legacy="ORIGINAL")
    assert canon["datasets"] == ["d1"]
    assert canon["universe"] == "TOP1600"
    assert canon["_legacy"] == "ORIGINAL"
    assert canon["_schema_from"] == "whitelist"


# --------------------------------------------------------------------- 3
pytestmark_db = pytest.mark.skipif(not os.path.isfile(DB), reason="无 data/wqb.db")


@pytestmark_db
def test_real_db_all_regions_normalizable():
    """真实库：每个区域的白名单都必须可读（禁止 fail-open 回归）。"""
    conn = sqlite3.connect(DB)
    try:
        rows = conn.execute(
            "SELECT region, value FROM ledger_kv WHERE key='s0_whitelist'").fetchall()
    finally:
        conn.close()
    assert rows, "库中应有 s0_whitelist 记录"
    bad = []
    for region, raw in rows:
        rec = LW.normalize(raw)
        if not rec["ok"] or not rec["datasets"]:
            bad.append((region, rec["reason"]))
    assert not bad, f"以下区域白名单不可读（需人工修复）：{bad}"


@pytestmark_db
def test_real_db_no_schema_drift():
    """防第 6 种形态再生：真实库中不应再有非 `datasets` 契约的记录。

    失败时按提示跑迁移脚本即可（幂等、带 _legacy 备份、可断点续跑）：
        python tools/normalize_ledger_whitelist.py --apply --db-backup
    """
    conn = sqlite3.connect(DB)
    try:
        rows = conn.execute(
            "SELECT region, value FROM ledger_kv WHERE key='s0_whitelist'").fetchall()
    finally:
        conn.close()
    drifted = {}
    for region, raw in rows:
        try:
            obj = json.loads(raw) if isinstance(raw, (str, bytes)) else raw
        except Exception:
            obj = None
        if not isinstance(obj, dict) or "datasets" not in obj or "_schema_from" not in obj:
            rec = LW.normalize(raw)
            drifted[region] = rec["schema"]
    assert not drifted, (
        f"检测到白名单契约漂移：{drifted}。请跑 "
        f"`python tools/normalize_ledger_whitelist.py --apply --db-backup` 归一。"
    )
