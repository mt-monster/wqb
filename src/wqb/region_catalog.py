# -*- coding: utf-8 -*-
"""region_catalog — 区域安全的 dataset / field 查询层（2026-10-04）。

问题（真实事故，EUR wave282差点白跑一整波）
----------------------------------------------------
``data/wqb.db`` 的表结构是**区域合并**的：

* ``datasets`` 表：同一个 ``name``（如 ``risk70`` / ``pv1``）在不同 region
  各存一行，靠 ``region_id`` 区分。实测 ``risk70`` 有 **7 行**（region_id
  1,2,3,5,6,8,9），``pv1`` 有 **11 行**。
* ``fields`` 表：**没有 region 列**，只有 ``dataset_id``（存``datasets.id`
  这个数字）。信息其实是全的，只是必须经 ``datasets`` 转发才能定位区域。

于是任何形如::

    SELECT ... FROM fields WHERE dataset_id LIKE '%risk70%'   -- ✗ 错
    SELECT ... FROM fields WHERE field_name LIKE 'rsk70%'      -- ✗ 更错

的写法都会**横跨全部 7 个区域**把字段并进来。实测后果：

* ``rsk70_mfm2_euetrd_*``（EUR 口径）与 ``rsk70_mfm2_asetrd_*``（亚太口径）
  ``_mfm2_gemtrd_*``（GEM 口径）看上去是"可换口径的正交维度"，
  实际 **EUR 只提供 ``euetrd`` 一套**，另两套在该region 根本不存在。
* ``risk88`` / ``risk59`` 被本地选集脚本列为 tier1 白名单，
  实际在 EUR ``get_datafields`` 返回 ``count=0``——数据集层���同类污染。

本模块提供**唯一正确姿势**：任何按 dataset 名或 field 名查本地 catalog 的
动作，都必须先经region 过滤。查不到就明确返回"本地无该区记录"，
而不是静默返回跨区并集。

用法::

    from wqb.region_catalog import RegionCatalog

    rc = RegionCatalog()                      # 默认连 data/wqb.db
    rc.dataset_ids("risk70", region="EUR")    # -> [609]
    rc.fields("risk70", region="EUR")         # -> [<Row field_name ...>]
    rc.field_names("risk70", region="EUR")    # -> ['rsk70_mfm2_euetrd_...', ...]

    # 跨区显式查询（合法但需自己判断可用性）
    rc.dataset_ids("risk70")                  # -> {region: [id, ...]} 映射

**平台才是真相源**：本模块只解决"不要被本地表误导"，不解决"本地有就平台有"。
字段可用性仍须以 ``get_datafields(region=..., universe=...)`` 实测为准
（region 口径在数据集内也会再分叉，见模块 docstring）。
"""
from __future__ import annotations

import sqlite3
from typing import Dict, List, Optional, Sequence

from .db_conn import connect

__all__ = [
    "RegionCatalog",
    "RegionAmbiguityError",
    "resolve_dataset_ids",
    "dataset_names_in_region",
    "field_names_in_region",
]


class RegionAmbiguityError(ValueError):
    """跨区查询被显式拒绝时抛出（防止静默返回跨区并集）。"""


def _norm_region(region: Optional[str]) -> Optional[str]:
    return region.strip().upper() if region and region.strip() else None


def _norm_name(name: str) -> str:
    return name.strip().lower()


class RegionCatalog:
    """区域安全的 dataset / field 读取器。"""

    def __init__(self, db: Optional[str] = None, conn: Optional[sqlite3.Connection] = None):
        # 只读口径：绝不因查询而改写库文件（WAL 是库级持久属性）。
        # row_factory 默认 sqlite3.Row，本模块所有取字段均按下标名访问。
        if conn is not None:
            self._conn = conn
        else:
            self._conn = connect(db, readonly=True, row_factory=sqlite3.Row)
        self._owns = conn is None
        self._region_ids: Optional[Dict[str, int]] = None

    # ---------- 生命周期 ----------
    def close(self) -> None:
        if self._owns:
            self._conn.close()

    def __enter__(self) -> "RegionCatalog":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    # ---------- 区域名<-> id ----------
    def region_map(self) -> Dict[str, int]:
        """``{'EUR': 6, 'USA': 1, ...}``（缓存于实例）。"""
        if self._region_ids is None:
            rows = self._conn.execute("SELECT id, name FROM regions").fetchall()
            self._region_ids = {str(r[1]).upper(): int(r[0]) for r in rows}
        return self._region_ids

    def region_id(self, region: str) -> Optional[int]:
        return self.region_map().get(_norm_region(region))

    # ---------- dataset解析 ----------
    def dataset_ids(self, name: str, region: Optional[str] = None) -> List[int]:
        """按名字取 ``datasets.id``。

        Args:
            name: dataset 名（大小写不敏感）。
            region: **必填语义**。给 ``None`` 时返回
                ``{region_name: [id, ...]}`` 映射（跨区显式查询）；
                给定 region 时只返回该区的 id 列表（可能为空 list）。

        Returns:
            region 为 None -> ``Dict[str, List[int]]``；
            region 给定   -> ``List[int]``（该区命中，可能为空）。

        Raises:
            RegionAmbiguityError: region 给了但库里没有该区。
        """
        key = _norm_name(name)
        if region is None:
            rows = self._conn.execute(
                "SELECT r.name, d.id FROM datasets d JOIN regions r ON r.id = d.region_id "
                "WHERE lower(d.name) = ?",
                (key,),
            ).fetchall()
            out: Dict[str, List[int]] = {}
            for rname, did in rows:
                out.setdefault(str(rname).upper(), []).append(int(did))
            for v in out.values():
                v.sort()
            return out

        rid = self.region_id(region)
        if rid is None:
            raise RegionAmbiguityError(
                f"未知 region {region!r}；库内region = {sorted(self.region_map())}"
            )
        rows = self._conn.execute(
            "SELECT id FROM datasets WHERE lower(name) = ? AND region_id = ?",
            (key, rid),
        ).fetchall()
        return [int(r[0]) for r in rows]

    def region_of_dataset(self, name: str) -> Dict[str, List[int]]:
        """``dataset_ids(name)`` 的语义化别名（region 必填时返回该区）。"""
        return self.dataset_ids(name, region=None)

    def dataset_names(self, region: str, category: Optional[str] = None) -> List[str]:
        """列出某区（可选按 category 过滤）的全部 dataset 名。"""
        rid = self.region_id(region)
        if rid is None:
            raise RegionAmbiguityError(f"未知 region {region!r}")
        sql = "SELECT d.name FROM datasets d WHERE d.region_id = ?"
        args: List[object] = [rid]
        if category:
            sql += " AND upper(d.category) = ?"
            args.append(_norm_region(category))
        sql += " ORDER BY d.name"
        return [str(r[0]) for r in self._conn.execute(sql, args).fetchall()]

    # ---------- field 读取（核心修复点） ----------
    def fields(
        self,
        name: str,
        region: str,
        *,
        with_stats: bool = False,
    ) -> List[sqlite3.Row]:
        """取某区某 dataset 的字段行。

        这是**替代** ``WHERE dataset_id LIKE '%name%'`` 的正确姿势。
        """
        ids = self.dataset_ids(name, region=region)
        if not ids:
            return []
        qs = ",".join("?" * len(ids))
        sql = f"SELECT * FROM fields WHERE dataset_id IN ({qs}) ORDER BY field_name"
        rows = self._conn.execute(sql, ids).fetchall()
        return rows

    # ---------- 塔（category）视角：选集第一入口 ----------
    def datasets_by_tower(
        self,
        region: str,
        *,
        category: Optional[str] = None,
        min_fields: Optional[int] = None,
        max_alpha_count: Optional[int] = None,
        sort: str = "alpha_count",
    ) -> Dict[str, List[Dict[str, object]]]:
        """按塔（``category``）分组列出某区数据集 —— **选集第一入口**。

        动机（2026-10-05 事故）：手工拼 ``SELECT ... FROM datasets WHERE name LIKE
        '%short%'`` 会因**漏 region 过滤**而拿到 25 个跨区并集（KOR 实际只有 4 个），
        据此去 ``get_datafields`` 才发现 21 个在本区根本没有字段。本方法把
        「某区 × 某塔」的正确清单一次给全，省掉手搓 SQL 与踩坑。

        Args:
            region: 区域名（如 ``"KOR"``）。
            category: 只看某个塔（``"MODEL"``/``"ANALYST"``…）；``None`` = 全部塔。
            min_fields: 只保留 ``field_count >= min_fields`` 的数据集（过滤空集壳）。
            max_alpha_count: 只保留 ``alpha_count <= max_alpha_count`` 的数据集
                （用于找**未被挖过**的白空间）。
            sort: ``"alpha_count"``（默认，降序=越靠前越拥挤）或 ``"field_count"``。

        Returns:
            ``{category: [{name, id, field_count, alpha_count, value_score, tier,
            data_type, coverage}, ...]}``；category 内按 ``sort`` 降序。
            ``None`` 值原样保留（本地表可能缺统计），不臆造 0。

        ⚠️ 仍只是**本地线索**：本区有记录 ≠ 平台有字段。正式选集前必须对候选
        dataset 调 ``get_datafields(region=..., universe=...)`` 实测（见模块 docstring
        的「平台才是真相源」）。
        """
        rid = self.region_id(region)
        if rid is None:
            raise RegionAmbiguityError(
                f"未知 region {region!r}；库内region = {sorted(self.region_map())}"
            )
        sql = (
            "SELECT id, name, category, field_count, alpha_count, value_score, "
            "tier, data_type, coverage FROM datasets WHERE region_id = ?"
        )
        args: List[object] = [rid]
        if category:
            sql += " AND upper(category) = ?"
            args.append(_norm_region(category))
        if min_fields is not None:
            sql += " AND COALESCE(field_count, 0) >= ?"
            args.append(int(min_fields))
        if max_alpha_count is not None:
            sql += " AND COALESCE(alpha_count, 0) <= ?"
            args.append(int(max_alpha_count))

        key = "field_count" if sort == "field_count" else "alpha_count"
        # None 排在最后：COALESCE 到 -1 参与排序，但输出保留原值。
        sql += f" ORDER BY COALESCE({key}, -1) DESC, name"

        out: Dict[str, List[Dict[str, object]]] = {}
        for r in self._conn.execute(sql, args).fetchall():
            item = {
                "name": r[1],
                "id": int(r[0]),
                "field_count": r[3],
                "alpha_count": r[4],
                "value_score": r[5],
                "tier": r[6],
                "data_type": r[7],
                "coverage": r[8],
            }
            out.setdefault(str(r[2] or "UNCATEGORIZED"), []).append(item)
        return out

    def tower_summary(self, region: str) -> List[Dict[str, object]]:
        """各塔的数据集数量概览（快速看该区还有哪些塔/资源多少）。

        Returns:
            ``[{category, n_datasets, n_fields, max_alpha_count}, ...]``，按 n_datasets 降序。
        """
        per = self.datasets_by_tower(region)
        rows = []
        for cat, items in per.items():
            rows.append({
                "category": cat,
                "n_datasets": len(items),
                "n_fields": sum(int(i["field_count"] or 0) for i in items),
                "max_alpha_count": max((i["alpha_count"] or 0) for i in items) if items else 0,
            })
        rows.sort(key=lambda x: (-x["n_datasets"], x["category"]))
        return rows

    def field_names(self, name: str, region: str) -> List[str]:
        """某区某 dataset 的字段名列表（去重、保序）。"""
        seen, out = set(), []
        for r in self.fields(name, region=region):
            fn = str(r["field_name"])
            if fn not in seen:
                seen.add(fn)
                out.append(fn)
        return out

    def field_exists(self, field_name: str, region: str) -> bool:
        """字段是否在「该区该dataset」下存在。

        ⚠️ 调用方须先知道 dataset 名；本方法在该区**所有** dataset 里找，
        命中即True。仅用于"排除平台不存在"，不能替代平台实测。
        """
        rid = self.region_id(region)
        if rid is None:
            raise RegionAmbiguityError(f"未知 region {region!r}")
        row = self._conn.execute(
            "SELECT 1 FROM fields f JOIN datasets d ON d.id = f.dataset_id "
            "WHERE d.region_id = ? AND f.field_name = ? LIMIT 1",
            (rid, field_name),
        ).fetchone()
        return row is not None

    def explain(self, name: str) -> str:
        """诊断：打印某 dataset 名在各区的分布（排查"字段从哪来"）。"""
        per = self.dataset_ids(name, region=None)
        lines = [f"dataset {name!r} 在库中的区域分布（共 {len(per)} 区）："]
        for rname in sorted(per):
            ids = per[rname]
            n = 0
            for did in ids:
                n += self._conn.execute(
                    "SELECT COUNT(*) FROM fields WHERE dataset_id = ?", (did,)
                ).fetchone()[0]
            lines.append(f"  {rname:<6} ids={ids}  fields={n}")
        lines.append(
            "  ⚠️ 不带 region 查询会返回以上全部并集——必须经本模块按区取。"
        )
        return "\n".join(lines)


# ---------- 模块级便捷函数（薄封装） ----------
def resolve_dataset_ids(name: str, region: str, db: Optional[str] = None) -> List[int]:
    with RegionCatalog(db) as rc:
        return rc.dataset_ids(name, region=region)


def dataset_names_in_region(region: str, db: Optional[str] = None) -> List[str]:
    with RegionCatalog(db) as rc:
        return rc.dataset_names(region)


def field_names_in_region(name: str, region: str, db: Optional[str] = None) -> List[str]:
    with RegionCatalog(db) as rc:
        return rc.field_names(name, region=region)
