# -*- coding: utf-8 -*-
"""region_catalog — 区级字段目录**唯一入口**（防跨区串号）。

## 为什么必须有这个模块（2026-10-06 事故复盘）

`fields` 表**没有 region 列**，region 只能经 `datasets.region_id` 关联；
而**同名数据集在最多 13 个区各有一个 dataset_id**（`model38` 就有 9 个：
GBR=264 / KOR=1233 / ASI=1699 / IND=1381 / EUR=1518 / GLB=893 / HKG=711 / DEU=1059 / USA=1854）。

后果：任何漏掉 region 过滤的 `FROM fields` 查询都会**静默串区**。
实测踩坑：用 `LIKE '%star_val%'` 不带 region，命中了 GLB/EUR/DEU 的行，
于是误判「GBR `model38` 有 `star_val_*` 字段」；补上 `region_id=7` 后又查不到，
进一步被误读成「数据被并发会话重写」。**真相只是查询串了区。**

⇒ **纪律：不要裸写 `FROM fields`。一律经本模块（或显式带 `region_id`）。**
静态检查：``python <repo>/../wqb-scripts/wqb_tools.py catalog-guard``

## 用法

    from wqb.region_catalog import RegionCatalog
    with RegionCatalog() as rc:
        rc.dataset_names("GBR")                  # 该区数据集名
        rc.field_names("model28", "GBR")         # 该区该数据集的字段名
        rc.fields("GBR", "model28")              # 完整字段行
        rc.explain("model38")                    # 该名在哪些区存在（排错用）
"""
from __future__ import annotations

import sqlite3
from typing import Dict, Iterable, List, Optional, Sequence

from wqb.db_conn import connect

__all__ = [
    "RegionAmbiguityError",
    "RegionCatalog",
    "resolve_dataset_ids",
    "dataset_names_in_region",
    "field_names_in_region",
]


class RegionAmbiguityError(ValueError):
    """数据集名在多个区都存在，但调用方没指定 region（会静默串区）。"""


def _norm_region(region: str) -> str:
    return str(region).strip().upper()


def _norm_name(name: str) -> str:
    return str(name).strip().lower()


class RegionCatalog:
    """区级只读目录。所有查询都强制 region 作用域。"""

    def __init__(self, db: Optional[str] = None, readonly: bool = True):
        self._conn: sqlite3.Connection = connect(db=db, row_factory=sqlite3.Row,
                                                 readonly=readonly)
        self._close_conn = True

    def close(self) -> None:
        if self._close_conn and self._conn is not None:
            try:
                self._conn.close()
            finally:
                self._conn = None

    def __enter__(self) -> "RegionCatalog":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def region_map(self) -> Dict[str, int]:
        """``{区域码: region_id}``（区域码大写）。"""
        return {str(r["name"]).upper(): int(r["id"])
                for r in self._conn.execute("SELECT id, name FROM regions")}

    def region_id(self, region: str) -> int:
        rid = self.region_map().get(_norm_region(region))
        if rid is None:
            raise ValueError(f"未知区域 {region!r}；已知 {sorted(self.region_map())}")
        return rid

    def dataset_ids(self, region: str, category: Optional[str] = None) -> List[int]:
        rid = self.region_id(region)
        sql = "SELECT id FROM datasets WHERE region_id=?"
        args: List[object] = [rid]
        if category:
            sql += " AND category=?"
            args.append(category)
        return [int(r["id"]) for r in self._conn.execute(sql, args)]

    def region_of_dataset(self, dataset: object) -> Optional[str]:
        """由 dataset_id 或数据集名反查区域码。"""
        if isinstance(dataset, int) or (isinstance(dataset, str) and dataset.isdigit()):
            row = self._conn.execute(
                "SELECT r.name AS n FROM datasets d JOIN regions r ON r.id=d.region_id "
                "WHERE d.id=?", (int(dataset),)).fetchone()
        else:
            rows = self._conn.execute(
                "SELECT DISTINCT r.name AS n FROM datasets d JOIN regions r ON r.id=d.region_id "
                "WHERE lower(d.name)=?", (_norm_name(dataset),)).fetchall()
            if len(rows) == 1:
                return str(rows[0]["n"]).upper()
            if len(rows) > 1:
                raise RegionAmbiguityError(
                    f"数据集 {dataset!r} 存在于多个区 {sorted(str(x['n']) for x in rows)}；"
                    f"必须显式指定 region（用 rc.explain() 查看）")
            return None
        return str(row["n"]).upper() if row else None

    def dataset_names(self, region: str, category: Optional[str] = None) -> List[str]:
        rid = self.region_id(region)
        sql = "SELECT name FROM datasets WHERE region_id=?"
        args: List[object] = [rid]
        if category:
            sql += " AND category=?"
            args.append(category)
        sql += " ORDER BY name"
        return [str(r["name"]) for r in self._conn.execute(sql, args)]

    def _dataset_id(self, dataset: str, region: str) -> int:
        rid = self.region_id(region)
        row = self._conn.execute(
            "SELECT id FROM datasets WHERE region_id=? AND lower(name)=?",
            (rid, _norm_name(dataset))).fetchone()
        if not row:
            raise KeyError(f"region {_norm_region(region)} 下无数据集 {dataset!r}")
        return int(row["id"])

    def fields(self, region: str, dataset: str) -> List[Dict[str, object]]:
        """完整字段行（含 field_type / coverage / alpha_count / description）。"""
        did = self._dataset_id(dataset, region)
        return [dict(r) for r in self._conn.execute(
            "SELECT * FROM fields WHERE dataset_id=? ORDER BY field_name", (did,))]

    def field_names(self, dataset: str, region: str,
                    category: Optional[str] = None) -> List[str]:
        """字段名。**注意参数顺序 = (dataset, region)**，与调用方既有契约一致。"""
        rid = self.region_id(region)
        sql = ("SELECT f.field_name AS n FROM fields f JOIN datasets d ON d.id=f.dataset_id "
               "WHERE d.region_id=? AND lower(d.name)=?")
        args: List[object] = [rid, _norm_name(dataset)]
        if category:
            sql += " AND d.category=?"
            args.append(category)
        sql += " ORDER BY f.field_name"
        return [str(r["n"]) for r in self._conn.execute(sql, args)]

    def field_exists(self, region: str, dataset: str, field: str) -> bool:
        return _norm_name(field) in {_norm_name(x) for x in self.field_names(dataset, region)}

    def datasets_by_tower(self, region: str, tower: str) -> List[str]:
        """塔（category）下的数据集名。"""
        return self.dataset_names(region, category=tower)

    def tower_summary(self, region: str) -> Dict[str, Dict[str, int]]:
        """``{category: {datasets, fields}}`` —— 区级塔画像。"""
        rid = self.region_id(region)
        out: Dict[str, Dict[str, int]] = {}
        for r in self._conn.execute(
                """SELECT COALESCE(d.category,'(none)') AS cat,
                          COUNT(DISTINCT d.id) AS nds,
                          COUNT(f.id) AS nf
                     FROM datasets d LEFT JOIN fields f ON f.dataset_id=d.id
                    WHERE d.region_id=? GROUP BY cat ORDER BY nf DESC""", (rid,)):
            out[str(r["cat"])] = {"datasets": int(r["nds"]), "fields": int(r["nf"])}
        return out

    def explain(self, dataset: str) -> str:
        """排错用：该数据集名在哪些区存在、各自 dataset_id / field_count / 本地字段行数。"""
        rows = self._conn.execute(
            """SELECT r.name AS region, d.id AS did, d.field_count AS fc, d.alpha_count AS ac,
                      d.category AS cat,
                      (SELECT COUNT(*) FROM fields f WHERE f.dataset_id=d.id) AS nf
                 FROM datasets d JOIN regions r ON r.id=d.region_id
                WHERE lower(d.name)=? ORDER BY r.name""", (_norm_name(dataset),)).fetchall()
        if not rows:
            return f"{dataset!r}: 本地 catalog 无任何区存在"
        lines = [f"{dataset!r} 存在于 {len(rows)} 个区 —— 查询必须带 region：",
                 f"  {'region':<6}{'ds_id':>8}{'平台字段':>9}{'本地行':>8}{'aCnt':>8}  category"]
        for r in rows:
            lines.append(f"  {str(r['region']):<6}{int(r['did']):>8}{int(r['fc'] or 0):>9}"
                         f"{int(r['nf']):>8}{int(r['ac'] or 0):>8}  {r['cat']}")
        return "\n".join(lines)


def resolve_dataset_ids(name: str, region: Optional[str] = None,
                        db: Optional[str] = None) -> List[int]:
    """把数据集名解析为 dataset_id 列表；不给 region 且跨区存在时抛 RegionAmbiguityError。"""
    with RegionCatalog(db=db) as rc:
        if region:
            try:
                return [rc._dataset_id(name, region)]
            except (KeyError, ValueError):
                return []      # 该区不存在 / 该区无此数据集 ⇒ 空结果（查询语义，非错误）
        rows = rc._conn.execute(
            "SELECT id FROM datasets WHERE lower(name)=?", (_norm_name(name),)).fetchall()
        if len(rows) > 1:
            raise RegionAmbiguityError(
                f"{name!r} 存在于多个区；必须指定 region\n{rc.explain(name)}")
        return [int(r["id"]) for r in rows]


def dataset_names_in_region(region: str, category: Optional[str] = None,
                            db: Optional[str] = None) -> List[str]:
    with RegionCatalog(db=db) as rc:
        return rc.dataset_names(region, category)


def field_names_in_region(dataset: str, region: str,
                          db: Optional[str] = None) -> List[str]:
    with RegionCatalog(db=db) as rc:
        return rc.field_names(dataset, region)
