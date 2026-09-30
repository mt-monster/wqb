# -*- coding: utf-8 -*-
"""`tools/kor_opportunity_scan.py` 跨区/大小写死路检查回归测试（2026-09-28）。

背景（两个真实误判，各白烧一轮回测）：
  1. **region-scoped 死路检查**：S-PRE 只查 `region='KOR'` 的 dead_end，漏掉
     `IND-RISK70-NO-SIGNAL` / `GLB-RISK70-STYLE-HF-MINVOL1M-FASTKILL`
     → KOR 白烧 114 次回测才发现 risk70 是跨三区死族。
  2. **大小写敏感**：临场用 `entry_id LIKE '%shortinterest3%'` 命不中
     `KOR-SHORTINTEREST3-DEAD`（大写字面量）→ "无死路"列表出现假阴性。

本测试守护三件事：
  ① 扫描输出的 playable 集合里不含任何被 dead_end 命中的数据集（跨区、大小写不敏感）
  ② 已点亮类别（ANALYST/MODEL/OTHER/PV）不得出现在 playable
  ③ 红榜族类别（NEWS/SENTIMENT）不得出现在 playable
"""
from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "tools" / "kor_opportunity_scan.py"
DB = REPO / "data" / "wqb.db"
PY = sys.executable


def _run_scan(tmp_path):
    out = tmp_path / "opp.json"
    r = subprocess.run([PY, str(TOOL), "--region", "KOR", "--json", str(out)],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=300)
    assert r.returncode == 0, f"扫描应成功:\n{r.stdout[-800:]}\n{r.stderr[-800:]}"
    return json.loads(out.read_text(encoding="utf-8"))


def _dead_blob():
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        return [(row[1] + " " + (row[2] or "")).lower()
                for row in c.execute(
                    "SELECT region, entry_id, COALESCE(payload,'') "
                    "FROM registry_empirical WHERE layer='dead_end'")]
    finally:
        c.close()


def test_playable_excludes_all_dead_end_hits(tmp_path):
    """核心契约（2026-09-28 修订）：playable 数据集不得命中**数据集级**死路。

    2026-09-28 起扫描区分两级：死路 `rule` **只禁特定构造**（含 skeleton/bare/骨架/
    构造/multi-field 等标记）属**构造级死路**——数据集仍可挖（换构造即可），但扫描
    记录必须带 `construction_constraints` 说明。实证：shortinterest38 被 wave96
    bare-skeleton 死路误杀，而论坛 2026-09 换构造后 Sharpe 2.43 全闸通过并提交。
    数据集级死路（rule 未限定构造，如 "do not re-mine shortinterest3"）仍然封锁。
    """
    opp = _run_scan(tmp_path)
    markers = ("skeleton", "bare", "骨架", "构造", "multi-field combos",
               "with multi-field", "event-gating", "event-")
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        dead = [(row[1], row[2] or "") for row in c.execute(
            "SELECT region, entry_id, COALESCE(payload,'') "
            "FROM registry_empirical WHERE layer='dead_end'")]
    finally:
        c.close()
    by_name = {r["dataset"].lower(): r for r in opp["playable"]}
    offenders = []
    for entry_id, payload in dead:
        blob = (entry_id + " " + payload).lower()
        try:
            obj = json.loads(payload) if payload.lstrip().startswith("{") else {}
        except Exception:
            obj = {}
        scope_blob = (str(obj.get("rule", "")) + " " + str(obj.get("reason", ""))).lower()
        scoped = any(m in scope_blob for m in markers)
        for ds, rec in by_name.items():
            if ds in blob:
                if scoped:
                    assert "construction_constraints" in rec, (
                        f"{rec['dataset']} 命中构造级死路 {entry_id} 但扫描未记录约束")
                else:
                    offenders.append((rec["dataset"], entry_id))
    assert not offenders, (
        f"数据集级死路漏检（region-scoped / 大小写敏感 / 构造级误判为数据集级的旧缺陷回归）: {offenders}")


def test_playable_excludes_lit_categories(tmp_path):
    """已点亮类别（SOP 硬规则 0）不得作主数据集。"""
    opp = _run_scan(tmp_path)
    lit = {k.upper() for k in opp["lit_categories"]}
    bad = [r for r in opp["playable"] if (r["category"] or "").upper() in lit]
    assert not bad, f"已点亮类别混入 playable: {[r['dataset'] for r in bad]}"


def test_playable_excludes_red_family_categories(tmp_path):
    """KOR 红榜族 news_sentiment → NEWS/SENTIMENT 类别不得作主数据集。"""
    opp = _run_scan(tmp_path)
    bad = [r for r in opp["playable"] if (r["category"] or "").upper() in ("NEWS", "SENTIMENT")]
    assert not bad, f"红榜类别混入 playable: {[r['dataset'] for r in bad]}"


def test_scan_tool_uses_case_insensitive_matching():
    """静态守卫：匹配逻辑必须做 lower() 归一，且不得用 region= 过滤。"""
    src = TOOL.read_text(encoding="utf-8")
    assert ".lower()" in src, "死路匹配必须大小写归一（否则 shortinterest3 命不中大写 entry_id）"
    # 死路查询本身不得带 region 条件（跨区检查是本工具存在的理由）
    m = re.search(r"SELECT region, entry_id.*?FROM registry_empirical\s+WHERE layer='dead_end'",
                  src, re.S)
    assert m, "应存在不限 region 的 dead_end 查询"
    assert "region=" not in m.group(0), "dead_end 查询不得加 region 过滤（会漏跨区负先验）"
