# -*- coding: utf-8 -*-
"""tests/unit/01_store_db/test_region_query_guard.py — 区域查询守卫（2026-10-05）。

事故背景（2026-10-05 KOR 选集）
------------------------------
手工拼 ``SELECT ... FROM datasets WHERE name LIKE 'short%'`` **漏了 region 过滤**，
拿到 **25 个跨区并集**（KOR 实际只有 4 个），据此去 ``get_datafields`` 才发现
21 个在本区根本没有字段，白花一轮调研。

真因**不是**表结构问题（``datasets`` 有 ``region_id``，数据分区正确），
而是**查询习惯**：``fields`` 表没有 region 列，任何不 JOIN ``datasets`` 的字段查询
都会横跨全部区取并集（同 ``region_catalog`` docstring 记的 EUR wave282 事故）。

本守卫做**静态扫描**：活跃目录里出现 ``FROM datasets`` / ``FROM fields`` 的 SQL，
若附近既没有 ``region_id`` 也没有 ``JOIN datasets`` / ``JOIN regions``，即判违规。
正确姿势是走 :class:`wqb.region_catalog.RegionCatalog`（或同样带区过滤的封装）。

与 ``db_conn.DIRECT_CONNECT_WHITELIST`` 同款思路：白名单外一律不许裸查。
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]

#: 扫描的活跃目录（归档 attic/ 与第三方 .venv 不扫）。
#: ``logs/`` 是一次性排查脚本（临时、不入库），不作为回归约束对象。
SCAN_DIRS = ("src", "tools", "Claude/skills", "world-quant-brain-mcp")

#: 允许裸查的例外（**每条必须写理由**，否则守卫形同虚设）：
WHITELIST = {
    # 规范层本体：fields() 按 dataset_id 取字段前已先做区过滤；
    # dataset_ids(region=None) / explain() 故意做跨区诊断。
    "src/wqb/region_catalog.py": "规范层本体；跨区查询为其显式诊断能力",
    "src/wqb/db_conn.py": "连接工厂，不做业务查询",
    "src/wqb/store/_schema.py": "DDL（CREATE/ALTER），非 SELECT",
    # 一级查询已 `JOIN regions ... WHERE g.name=?`；裸查那行是**刻意降级 fallback**
    # （区查询无记录时才按名字兜底），且结果仅用于 category 前缀提示。
    "src/wqb/profiles/taxonomy.py": "一级查询已按区；裸查为刻意降级 fallback",
    # `SELECT DISTINCT dataset_id FROM fields WHERE field_name=?` 用于「字段名→dataset 投票」，
    # 跨区是刻意的，且后面 `if len(ds) == 1` 才计票（多区命中即弃权）⇒ 天然防跨区污染。
    "src/wqb/store/_backtest.py": "字段→dataset 投票；len(ds)==1 才计票，已防污染",
    # 库级体检：统计口径本就是全域（跨区是特性，不是漏过滤）。
    "src/wqb/step_eval.py": "库级体检，全域统计是特性",
    "tools/_db_quality_check.py": "库质量检查，全域统计是特性",
    # 字段存在性批量校验：跨区查是工具的功能本身。
    "tools/validate_fields_batch.py": "字段存在性校验，跨区查是功能",
    "tests/": "测试自身",
}

#: 命中即需检查的 SQL 形态：``FROM datasets`` / ``FROM fields``（含换行、别名）。
_SQL_FROM = re.compile(r"FROM\s+(datasets|fields)\b", re.IGNORECASE)

#: 视为「已按区定位」的证据：
#:   * ``region_id``            显式区过滤
#:   * ``JOIN datasets/regions`` 经 datasets 转发拿到区
#:   * ``dataset_id``           整数外键 —— ``fields.dataset_id -> datasets.id``，
#:                              而 ``datasets.id`` 是**区具体的行**，故按 dataset_id
#:                              过滤天然已区隔（这是安全的，不是漏网）。
_REGION_GUARD = re.compile(
    r"(region_id|JOIN\s+(datasets|regions)\b|dataset_id\s*(?:=|IN|!=))",
    re.IGNORECASE,
)
#: 已知错误写法（显式点名，便于报错信息可读）。
_BAD_LIKE = re.compile(r"dataset_id\s+LIKE", re.IGNORECASE)

#: 取违规点前后多大窗口找「已按区过滤」的证据。
_WINDOW = 400


def _iter_py_files():
    for d in SCAN_DIRS:
        base = REPO / d
        if not base.is_dir():
            continue
        for p in base.rglob("*.py"):
            rel = p.relative_to(REPO).as_posix()
            if any(rel.startswith(w) for w in WHITELIST):
                continue
            if "/node_modules/" in rel or "/.venv/" in rel or "__pycache__" in rel:
                continue
            yield p, rel


def _scan_offenders(text: str, rel: str):
    """返回 [(行号, 片段说明), ...]。"""
    out = []
    for m in _SQL_FROM.finditer(text):
        lo = max(0, m.start() - 120)
        hi = min(len(text), m.end() + _WINDOW)
        window = text[lo:hi]
        if _REGION_GUARD.search(window):
            continue
        line = text.count("\n", 0, m.start()) + 1
        snippet = re.sub(r"\s+", " ", text[max(0, m.start() - 60):m.end() + 60])
        out.append((line, snippet.strip()))
    # 显式点名 dataset_id LIKE
    for m in _BAD_LIKE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        snippet = re.sub(r"\s+", " ", text[max(0, m.start() - 60):m.end() + 60])
        out.append((line, f"[dataset_id LIKE] {snippet.strip()}"))
    return out


def test_no_regionless_datasets_or_fields_query():
    """活跃目录里不得出现不带区过滤的 datasets / fields 查询。"""
    offenders = []
    for p, rel in _iter_py_files():
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "FROM datasets" not in text and "FROM fields" not in text and "FROM FIELDS" not in text:
            # 大小写不敏感兜底
            if not re.search(r"FROM\s+(datasets|fields)", text, re.IGNORECASE):
                continue
        for line, snippet in _scan_offenders(text, rel):
            offenders.append(f"{rel}:{line}  {snippet}")

    assert not offenders, (
        "以下位置查 datasets/fields 时**没有按 region 过滤**（会拿到跨区并集）：\n  "
        + "\n  ".join(offenders[:15])
        + f"\n  （共 {len(offenders)} 处）\n"
        "修正：改用 `wqb.region_catalog.RegionCatalog`"
        "（`datasets_by_tower(region)` / `fields(name, region)` / `field_names(name, region)`），"
        "或至少 JOIN datasets 并按 region_id 过滤。"
    )


def test_region_catalog_entry_points_work():
    """规范层三个选集入口必须可用（守卫自身依赖它们）。"""
    import sys

    src = REPO / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    from wqb.region_catalog import RegionCatalog, RegionAmbiguityError

    with RegionCatalog() as rc:
        # 塔视角：KOR 必须有 MODEL/SHORTINTEREST 等塔，且能按字段数过滤
        towers = rc.tower_summary("KOR")
        assert towers, "KOR 塔概览不应为空"
        cats = {t["category"] for t in towers}
        assert {"MODEL", "SHORTINTEREST"} <= cats

        per = rc.datasets_by_tower("KOR", category="SHORTINTEREST")
        names = [i["name"] for i in per.get("SHORTINTEREST", [])]
        # KOR 的 shortinterest 塔只有 38 / 3 / 5 三个（不是跨区并集的 25 个）
        assert "shortinterest38" in names
        assert "shortinterest43" not in names, "shortinterest43 属别区，不应出现在 KOR"

        # 按区取字段：KOR 的 shrt38 应有 accum_* 字段
        fields = rc.field_names("shortinterest38", region="KOR")
        assert any(f.startswith("shrt38_accum_") for f in fields)

        # 未知区名必须显式抛错，而不是静默返回空/并集
        with pytest.raises(RegionAmbiguityError):
            rc.datasets_by_tower("NOPE_NOT_A_REGION")
