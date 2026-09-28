# -*- coding: utf-8 -*-
"""`wave_results.verdict` 枚举契约守护（2026-09-26 新增）。

## 缘起

实测：930 行中 **73 行（68 种）是描述性值**（`8/8 过硬闸, 新高 3.58`、`FAIL — … prod 0.85-0.97` 等），
而 ra-pipeline 步 9 明令 verdict **强制枚举 PASS/FAIL/PARTIAL**。

更深一层的问题：`N/M 过硬闸` 这种形态存在**三套分类器**，且语义分歧
（`migrate_wave_verdict_enum.classify` 与 `wqb_db_mcp._normalize_wave_verdict` 说 N>0 → PASS，
而真正消费方 `campaign._normalize_verdict` 说 N>0 → **PARTIAL**——分歧实测 32/72 行）。
写路径归一成 A、读取方按 B 解释，才是这类漂移的真正根因。

本轮已：① 71 行迁移归一 + 1 行 SALVAGE→PARTIAL + 1 空壳行保持 NULL；
② 两个非权威分类器**对齐**到 campaign 规则。本模块防复发。
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DB = REPO_ROOT / "data" / "wqb.db"
ENUM = ("PASS", "FAIL", "PARTIAL")

pytestmark_db = pytest.mark.skipif(not DB.is_file(), reason="无 data/wqb.db")


def _classifiers():
    sys.path.insert(0, str(REPO_ROOT / "src"))
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    from migrate_wave_verdict_enum import classify as migrate_classify
    from wqb.workflow.nodes.campaign import _normalize_verdict as campaign_normalize
    from wqb.workflow.nodes import campaign as _camp

    return migrate_classify, campaign_normalize, _camp


def test_real_db_no_verdict_drift():
    """真实库：`wave_results.verdict` 只允许 PASS/FAIL/PARTIAL（NULL=空壳行放行）。

    描述性值（`N/M 过硬闸`、`FAIL — …`、`SALVAGE`）会让所有**直接读 verdict** 的消费者
    （step_funnel / get_mining_yield / 仪表盘）拿到不可判定的值。
    """
    conn = sqlite3.connect(str(DB))
    try:
        rows = conn.execute("SELECT id, region, wave_number, verdict FROM wave_results").fetchall()
    finally:
        conn.close()
    bad = [(i, r, w, v) for i, r, w, v in rows if v not in ENUM and v is not None]
    assert not bad, (
        f"wave_results.verdict 出现 {len(bad)} 行非枚举值（会削弱停止规则与漏斗统计）。"
        " 修复：python tools/migrate_wave_verdict_enum.py（先 --dry-run）"
        + "\n  " + "\n  ".join(f"id={i} {rg}/wave{w}: {str(v)[:70]}" for i, rg, w, v in bad[:8]))


def test_hard_gate_classifier_matches_campaign():
    """`N/M 过硬闸` 的三套分类器必须**同答**。

    2026-09-26 实证：迁移工具与 wqb_db_mcp 写路径说 N>0 → PASS，
    唯一消费方 campaign 说 N>0 → PARTIAL，分歧 32/72 行。
    写成 A、读成 B —— 这类"写读语义不一致"才是漂移的根因。
    """
    migrate_classify, campaign_normalize, _camp = _classifiers()
    samples = [f"{n}/{m} 过硬闸, 新高 2.18"
               for n, m in ((0, 8), (1, 8), (3, 9), (8, 8), (8, 15), (1, 1), (0, 6))]
    bad = []
    for s in samples:
        mval, _why = migrate_classify(s)
        cval = campaign_normalize(s)
        if (mval or "UNKNOWN") != cval:
            bad.append(f"{s!r}: migrate={mval} vs campaign={cval}")
    assert not bad, "过硬闸计数分类器与权威读取方（campaign）不一致：\n" + "\n".join(bad)


def test_db_write_path_classifier_matches_campaign():
    """写路径唯一实现 `wave_results_contract.normalize_verdict` 必须与 campaign 一致。

    2026-09-27 合并后 `wqb_db_mcp._normalize_wave_verdict` 是 contract 的别名（委托），
    `DirectDBWriter` 直写也走 contract——归一不再有三处内联实现。本守护盯两件事：
    ① contract 与 campaign 权威规则行为同答；② 委托关系不脱落（防内联实现复活）。
    """
    _, campaign_normalize, _camp = _classifiers()
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from wqb.wave_results_contract import normalize_verdict as contract_normalize

    # 行为同答：contract 与 campaign 权威规则（N>0 过硬闸 → PARTIAL，含 8/8）
    for s, want in (("0/8 过硬闸", "FAIL"), ("1/8 过硬闸", "PARTIAL"),
                    ("8/8 过硬闸", "PARTIAL"), ("PASS", "PASS"), ("FAIL", "FAIL")):
        got = contract_normalize(s)[0]
        assert got == want, f"contract 与 campaign 分歧：{s!r} → {got}（应为 {want}）"
        assert campaign_normalize(s) == want, f"campaign 权威规则被改动：{s!r}"

    # 防丢失：contract 源文件必须保留过硬闸计数规则（写路径归一的唯一实现处）
    src = (REPO_ROOT / "src" / "wqb" / "wave_results_contract.py").read_text(encoding="utf-8")
    assert "过硬闸" in src, "contract 丢失了过硬闸归一规则"
    assert 'return ("PASS" if int(m.group(1)) > 0 else "FAIL")' not in src, (
        "contract 仍把 N>0 过硬闸判成 PASS —— 与 campaign 读取方（PARTIAL）分歧")
    # 委托不脱落：wqb_db_mcp 必须引用 contract（防改回内联第二权威）
    mcp_src = (REPO_ROOT / "wqb_db_mcp.py").read_text(encoding="utf-8")
    assert "_wave_contract.normalize_verdict" in mcp_src, (
        "wqb_db_mcp 不再委托 wave_results_contract —— 归一实现出现第二权威")


def test_migration_preserved_original_text():
    """迁移必须把原值留痕进 key_findings（可回滚），不得静默覆盖。"""
    snap_path = REPO_ROOT / "logs" / "_wave_verdict_before_migration.json"
    if not snap_path.is_file():
        pytest.skip("无迁移前快照（迁移尚未在本机执行）")
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    conn = sqlite3.connect(str(DB))
    try:
        changed = [r for r in snap
                   if r["verdict"] not in ENUM and r["verdict"] is not None]
        missing = []
        for r in changed:
            row = conn.execute("SELECT verdict, key_findings FROM wave_results WHERE id=?",
                               (r["id"],)).fetchone()
            if not row:
                continue
            verdict, kf = row
            if verdict in ENUM and (not kf or str(r["verdict"]) not in str(kf)):
                missing.append(r["id"])
    finally:
        conn.close()
    assert not missing, (
        f"以下行的原 verdict 未留痕进 key_findings（回滚链断裂）：{missing}")


def test_mcp_batch_writer_normalizes_verdict():
    """`DirectDBWriter` 直写路径必须走 `wave_results_contract`（2026-09-27 起）。

    历史：它绕过 `wqb_db_mcp`（那条路径会校验并拒绝）直接 INSERT，导致描述性
    verdict 成批入库（实测 GBR wave108-116 共 10 行）。2026-09-26 先以内联
    `_normalize_verdict_for_write` 修复；2026-09-27 P0-1 统一委托 contract 后
    内联实现删除——本守护改为盯住「委托不脱落 + contract 行为同答 + 拒绝分支在」。
    """
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    import mcp_batch_writer as mbw  # noqa: F401  可导入即无孤儿引用

    src = (REPO_ROOT / "tools" / "mcp_batch_writer.py").read_text(encoding="utf-8")
    assert "contract.upsert_wave_result(" in src, (
        "upsert_wave_result 直写分支不再委托 wave_results_contract")
    assert "_normalize_verdict_for_write" not in src, (
        "内联归一实现已删除（唯一实现=contract），勿复活第二权威")

    # contract 行为（原内联 helper 的用例迁到这里；归一不了的值由 contract 拒绝）
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from wqb.wave_results_contract import normalize_verdict as f
    assert f("0/8 过硬闸, 新高 0.92") == ("FAIL", "过硬闸计数")
    assert f("2/8 过硬闸, 新高 1.80") == ("PARTIAL", "过硬闸计数")   # 与 campaign 权威规则同答
    assert f("8/8 过硬闸, 新高 3.58") == ("PARTIAL", "过硬闸计数")
    assert f("PASS") == ("PASS", "枚举") and f("fail") == ("FAIL", "枚举")
    assert f("RED: 5 全灭") == ("FAIL", "前缀") and f("YELLOW: 0 候选") == ("PARTIAL", "前缀")
    assert f("机制确认但天花板明确") == (None, "无匹配")   # 无法辨认 → 由调用方拒绝

    # 「归一不了即拒绝」分支必须仍在 contract（否则会静默写入非枚举值）
    csrc = (REPO_ROOT / "src" / "wqb" / "wave_results_contract.py").read_text(encoding="utf-8")
    assert "verdict 必须是 PASS/FAIL/PARTIAL" in csrc, (
        "contract 丢失了「归一不了即拒绝」分支")
