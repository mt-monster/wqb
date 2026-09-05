# -*- coding: utf-8 -*-
"""FieldProfileMixin: per-field statistical profile (shape/skew/kurt/integer/freq) store.

字段画像是「字段→模板族」匹配的硬约束数据源（形状为主、类别为辅）。
画像来自 WebDataScope 数据包 `.bin` 的 10 年体检，经 tools/field_profile_backfill.py
解析后写入本表；GEM 生成环节按 field_profile_match 条件过滤绑定字段。

表设计独立于 fields 表（不动既有 6 维 catalog，避免影响 313 单测）：
    field_profile(dataset_id, field_name, shape, coverage, skew, kurt,
                  integer, freq, pos_ratio, neg_ratio, near_zero_ratio, source, updated_at)
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ._common import _now


class FieldProfileMixin:
    """Field statistical profile read/write methods."""

    def upsert_field_profile(
        self,
        region: str,
        dataset: str,
        profiles: List[Dict[str, Any]],
        source: str = "webdatascope",
    ) -> Dict[str, Any]:
        """批量写入某数据集字段画像（幂等 upsert）。

        profiles: [{field_name, shape, coverage, skew, kurt, integer, freq,
                    pos_ratio, neg_ratio, near_zero_ratio}, ...]
        """
        ds_id = self._ensure_dataset(region, dataset)
        cur = self.connection.cursor()
        n = 0
        now = _now()
        for p in profiles:
            fname = p.get("field_name") or p.get("field") or p.get("id")
            if not fname:
                continue
            cur.execute(
                "SELECT id FROM field_profile WHERE dataset_id=? AND field_name=?",
                (ds_id, fname),
            )
            row = cur.fetchone()
            vals = (
                p.get("shape"),
                p.get("coverage"),
                p.get("skew"),
                p.get("kurt"),
                1 if p.get("integer") else 0,
                p.get("freq"),
                p.get("pos_ratio"),
                p.get("neg_ratio"),
                p.get("near_zero_ratio"),
                source,
                now,
            )
            if row:
                cur.execute(
                    """UPDATE field_profile SET shape=?, coverage=?, skew=?, kurt=?,
                       integer=?, freq=?, pos_ratio=?, neg_ratio=?, near_zero_ratio=?,
                       source=?, updated_at=? WHERE id=?""",
                    vals + (int(row[0]),),
                )
            else:
                cur.execute(
                    """INSERT INTO field_profile
                       (dataset_id, field_name, shape, coverage, skew, kurt, integer,
                        freq, pos_ratio, neg_ratio, near_zero_ratio, source, updated_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (ds_id, fname) + vals,
                )
            n += 1
        self.connection.commit()
        return {"n": n, "region": region, "dataset": dataset, "source": source}

    def get_field_profile(self, region: str, dataset: str) -> List[Dict[str, Any]]:
        """读取某数据集全部字段画像（list of dict）。"""
        rid = self._ensure_region(region)
        cur = self.connection.cursor()
        cur.execute(
            "SELECT id FROM datasets WHERE name=? AND region_id=?",
            (dataset, rid),
        )
        ds = cur.fetchone()
        if not ds:
            return []
        cur.execute(
            """SELECT field_name, shape, coverage, skew, kurt, integer, freq,
                      pos_ratio, neg_ratio, near_zero_ratio, source
               FROM field_profile WHERE dataset_id=?""",
            (int(ds[0]),),
        )
        out = []
        for r in cur.fetchall():
            out.append({
                "field_name": r["field_name"],
                "shape": r["shape"],
                "coverage": r["coverage"],
                "skew": r["skew"],
                "kurt": r["kurt"],
                "integer": bool(r["integer"]),
                "freq": r["freq"],
                "pos_ratio": r["pos_ratio"],
                "neg_ratio": r["neg_ratio"],
                "near_zero_ratio": r["near_zero_ratio"],
                "source": r["source"],
            })
        return out

    def get_field_profile_map(self, region: str, dataset: str) -> Dict[str, Dict[str, Any]]:
        """读取画像并索引为 {field_name: profile}，供 GEM 绑定时 O(1) 查询。"""
        return {p["field_name"]: p for p in self.get_field_profile(region, dataset)}

    def dataset_shape_summary(self, region: str, dataset: str) -> Dict[str, Any]:
        """数据集级形状分布摘要（用于 S1 ledger 与模板族分流）。"""
        profiles = self.get_field_profile(region, dataset)
        counts: Dict[str, int] = {}
        for p in profiles:
            s = p.get("shape") or "unknown"
            counts[s] = counts.get(s, 0) + 1
        total = len(profiles)
        dominant = max(counts.items(), key=lambda kv: kv[1])[0] if counts else None
        sparse = counts.get("zero_inflated", 0) + counts.get("point_mass", 0)
        return {
            "region": region,
            "dataset": dataset,
            "total_fields": total,
            "shape_counts": counts,
            "dominant_shape": dominant,
            "sparse_ratio": round(sparse / total, 4) if total else 0.0,
        }
