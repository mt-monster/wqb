# -*- coding: utf-8 -*-
"""tests/unit/01_store_db/test_region_catalog.py — 区域安全 catalog 守卫（2026-10-04）。

事故背景（EUR wave282 差点白跑一整波）
--------------------------------------
``data/wqb.db`` 的 ``datasets`` 表**同名 dataset 跨 region 重复**（risk70 有 7 行、
pv1 有 11 行），而 ``fields`` 表**没有 region 列**、只有 ``dataset_id``
（=``datasets.id`` 数字）。于是::

    SELECT ... FROM fields WHERE dataset_id LIKE '%risk70%'   -- 横跨 7 区
    SELECT ... FROM fields WHERE field_name LIKE 'rsk70%'      -- 更糟，155 个字段

都会静默返回跨区并集。实测把 123 个「EUR 根本不存在的亚太 `mfm2_asetrd_*` 字段」
误认成"可换口径的正交维度"，而平台 ``get_datafields(EUR)`` 只有 87 个字段。

四类守卫：
  1. **行为**：按区取字段必须与跨区取字段严格不同（子集关系）
  2. **真实库**：EUR risk70 = 87 字段、且**不含** asetrd/gemtrd 口径
  3. **真实库**：risk88/risk59 在 EUR 必须为空（曾被本地选集误列为 tier1）
  4. **静态禁裸跨区查询**：活跃目录禁止 `fields` 表的 LIKE 模糊匹配
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wqb.region_catalog import RegionCatalog, RegionAmbiguityError  # noqa: E402


@pytest.fixture(scope="module")
def rc():
    if not (REPO / "data" / "wqb.db").exists():
        pytest.skip("data/wqb.db 不存在（CI/轻量环境）")
    catalog = RegionCatalog()
    yield catalog
    catalog.close()


# ---------------- 1. 行为：按区 vs 跨区 ----------------

class TestRegionScoping:
    def test_dataset_ids_none_returns_region_map(self, rc):
        per = rc.dataset_ids("risk70", region=None)
        assert isinstance(per, dict), "不传 region 必须返回 {region: [ids]} 映射"
        assert "EUR" in per, "risk70 应至少在 EUR 有记录"

    def test_dataset_ids_region_is_subset(self, rc):
        per = rc.dataset_ids("risk70", region=None)
        eur = rc.dataset_ids("risk70", region="EUR")
        assert set(eur).issubset(set(sum(per.values(), []))), \
            "按区取到的 id 必须是跨区并集的子集"

    def test_cross_region_is_strictly_larger(self, rc):
        """核心回归断言：跨区并集必须严格大于单区，否则事故不会复发。"""
        eur_n = len(rc.field_names("risk70", "EUR"))
        all_ids = sum(rc.dataset_ids("risk70", region=None).values(), [])
        con = rc._conn
        qs = ",".join("?" * len(all_ids))
        cross_n = con.execute(
            f"SELECT COUNT(DISTINCT field_name) FROM fields WHERE dataset_id IN ({qs})",
            all_ids,
        ).fetchone()[0]
        assert cross_n > eur_n, (
            f"跨区并集 {cross_n} 应严格大于 EUR 单区 {eur_n}；"
            "若相等说明 fixture 数据已变，需重估本守卫"
        )

    def test_unknown_region_raises(self, rc):
        with pytest.raises(RegionAmbiguityError):
            rc.dataset_ids("risk70", region="XXX")

    def test_absent_dataset_returns_empty_not_all(self, rc):
        """EUR 不存在的 dataset 必须返回空 list，绝不能回退成跨区并集。"""
        assert rc.field_names("risk88", "EUR") == []
        assert rc.dataset_ids("risk88", region="EUR") == []


# ---------------- 2/3. 真实库：平台一致性 ----------------

class TestRealDbMatchesPlatform:
    """这些断言锁死 2026-10-04 平台实测值，改库会红→ 说明 catalog 语义变了。"""

    def test_eur_risk70_field_count_is_87(self, rc):
        assert len(rc.field_names("risk70", "EUR")) == 87

    def test_eur_risk70_has_no_foreign_calibers(self, rc):
        """asetrd(亚太) / gemtrd(GEM) 口径在 EUR 根本不存在。"""
        fn = rc.field_names("risk70", "EUR")
        assert not any("asetrd" in x for x in fn), "混入了亚太口径字段"
        assert not any("gemtrd" in x for x in fn), "混入了 GEM 口径字段"

    def test_eur_risk70_keeps_euetrd_caliber(self, rc):
        fn = rc.field_names("risk70", "EUR")
        assert sum(1 for x in fn if "mfm2_euetrd_" in x) == 28

    @pytest.mark.parametrize("ds,expected", [("risk88", 0), ("risk59", 0)])
    def test_eur_absent_datasets_have_no_fields(self, rc, ds, expected):
        """risk88 / risk59 曾被本地白名单误列为 EUR tier1，实际平台 count=0。"""
        assert len(rc.field_names(ds, "EUR")) == expected

    @pytest.mark.parametrize("ds,expected", [
        ("risk70", 87), ("risk68", 5), ("risk72", 40), ("risk60", 5),
    ])
    def test_eur_available_datasets_field_counts(self, rc, ds, expected):
        assert len(rc.field_names(ds, "EUR")) == expected

    def test_explain_reports_all_regions(self, rc):
        txt = rc.explain("risk70")
        assert "EUR" in txt and "USA" in txt
        assert "必须经本模块按区取" in txt


# ---------------- 4. 静态禁裸跨区查询 ----------------

#: 允许直接写 fields 表 SQL 的文件（治理主体自身+ 明确知情的迁移脚本）。
_ALLOW = (
    "src/wqb/region_catalog.py",
    "src/wqb/region_profile.py",
    "src/wqb/dataset_pair_matrix.py",
)

#: 匹配「fields 表 + LIKE 模糊匹配」的跨区污染模式。
_BAD_PATTERNS = (
    re.compile(r"FROM\s+fields\b[^;]*?dataset_id\s+LIKE", re.I | re.S),
    re.compile(r"FROM\s+fields\b[^;]*?field_name\s+LIKE", re.I | re.S),
)

_SCAN_DIRS = ("src/wqb", "tools", "Claude/skills/wq-brain-campaign-toolkit/scripts")


def test_no_bare_cross_region_fields_query():
    """活跃目录禁止对 fields 表做 LIKE模糊匹配（region 污染主闸）。

    正确姿势：``from wqb.region_catalog import RegionCatalog``。
    """
    offenders = []
    for d in _SCAN_DIRS:
        base = REPO / d
        if not base.is_dir():
            continue
        for p in base.rglob("*.py"):
            rel = p.relative_to(REPO).as_posix()
            if rel in _ALLOW:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for pat in _BAD_PATTERNS:
                if pat.search(text):
                    offenders.append(rel)
                    break
    assert not offenders, (
        "检测到对 fields 表的跨区 LIKE 查询（会把多区域字段并进来）：\n  "
        + "\n  ".join(sorted(set(offenders)))
        + "\n修复：改用 wqb.region_catalog.RegionCatalog 按 (dataset, region) 取。"
    )


# ---------------- 5. 榜单跨区污染 ----------------

class TestRankingRegionScoping:
    """``s0_ranking`` 同一 key 下堆了多region 榜单，取错就是全盘污染。

    实测 8 份：KOR(#191658,最新) / GLB / **EUR(#173740)** / USA / GBR / HKG /
    DEU / AMR。``ORDER BY id DESC LIMIT 1`` 取到的是 KOR —— 这正是
    ``risk88``/``risk59`` 被误列为 "EUR tier1" 的根因。
    """

    def test_s0_ranking_contains_multiple_regions(self, rc):
        from wqb.region_catalog import _norm_region
        seen = {}
        for row in rc._conn.execute(
            "SELECT id, value FROM ledger_kv WHERE key='s0_ranking' ORDER BY id DESC"
        ):
            try:
                data = json.loads(row["value"])
            except Exception:
                continue
            r = _norm_region(data.get("region") or "")
            if r:
                seen.setdefault(r, []).append(int(row["id"]))
        assert len(seen) > 1, (
            f"s0_ranking 只有 {list(seen)} 一个区；本守卫假设多region 榜单，"
            "若DB 已重构请重估"
        )

    def test_find_ranking_for_picks_right_region(self, rc):
        sys.path.insert(0, str(REPO / "tools" / "rotation"))
        from region_whitelist import find_ranking_for, load_s0_rankings

        eur = find_ranking_for(rc, "EUR")
        assert eur is not None, "应能找到 EUR 榜单"
        assert eur["region"] == "EUR"
        assert eur["universe"] == "TOPCS1600", "EUR 榜单 universe 应为 TOPCS1600"

        # 最新一份不是 EUR（若此假设变化则本守卫需重估）
        all_b = load_s0_rankings(rc)
        if all_b and all_b[0]["region"] != "EUR":
            assert eur["ledger_id"] != all_b[0]["ledger_id"], \
                "find_ranking_for 必须能越过其他区间的更新榜单"

    def test_build_excludes_datasets_absent_in_region(self, rc):
        sys.path.insert(0, str(REPO / "tools" / "rotation"))
        from region_whitelist import build

        res = build(rc, "EUR", category="risk")
        names = {r["dataset"] for r in res["rows"]}
        assert "risk88" not in names, "risk88 不在 EUR，不得出现在 EUR 选集"
        assert "risk59" not in names, "risk59 不在 EUR，不得出现在 EUR 选集"
        assert "risk70" in names, "risk70 是 EUR 主力数据集，必须在"
        for r in res["rows"]:
            assert r["exists_in_region"], f"{r['dataset']} 标记存在但实际不在 EUR"
