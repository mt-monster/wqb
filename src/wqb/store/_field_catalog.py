# -*- coding: utf-8 -*-
"""FieldCatalogMixin: field catalog upsert/get for CampaignStore."""
from __future__ import annotations

import math
from statistics import median
from typing import Any, Dict, List, Optional

from ._common import _dumps, _loads, _now

#: S2 候选字段池构建算法版本。缓存 payload 的 builder_version 与之不符即视为过期重建——
#: 2026-09-13 把"前缀簇采样"改成"质量排序"后，已落库的旧池（如 GBR intraday_pv_feats：
#: 30 条全是 ask_price 族）永不失效，GEM 一直吃旧池。
POOL_BUILDER_VERSION = 2

#: 常见统计/时窗前缀（intraday_pv_feats 这类"统计量_主体_时窗"命名的数据集，首 token 是
#: mean/max/corr… 这种统计量而非主体；主体 token 才是经济含义所在）。
_STAT_TOKENS = frozenset("""
mean avg max min std stddev median sum count corr momentum momentum2 skew kurt first last
total abs rel pct delta diff ratio log net cum ewm ts rolling daily weekly monthly
""".split())


class FieldCatalogMixin:
    """Field catalog read/write methods."""

    @staticmethod
    def _field_name(field: Dict[str, Any]) -> Optional[str]:
        return field.get("id") or field.get("field_name") or field.get("name")

    @staticmethod
    def _field_type(field: Dict[str, Any]) -> Optional[str]:
        return field.get("type") or field.get("field_type")

    @staticmethod
    def _prefix_for(field_name: str, depth: int = 1) -> str:
        parts = [p for p in str(field_name).split("_") if p]
        if not parts:
            return str(field_name)
        depth = max(1, min(depth, len(parts)))
        return "_".join(parts[:depth])

    @staticmethod
    def _risk_flags(prefix: str, fields: List[Dict[str, Any]], coverages: List[float]) -> List[str]:
        flags: List[str] = []
        vector_count = sum(1 for f in fields if str(FieldCatalogMixin._field_type(f) or "").upper() == "VECTOR")
        if vector_count:
            flags.append("vector_fields_present")
        if coverages:
            med = median(coverages)
            if med < 0.5:
                flags.append("low_coverage_median")
        if prefix in {"news", "event", "vec", "vector"}:
            flags.append("sparse_or_complex_prefix")
        return flags

    def build_field_prefix_clusters(
        self,
        region: str,
        dataset: str,
        prefix_depth: int = 1,
        top_n: int = 10,
        samples_per_cluster: int = 5,
        coverage_high: float = 0.85,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """Build S1 field-prefix cluster summary from DB catalog and persist to ledger_kv."""
        catalog = self.get_field_catalog(region, dataset)
        if not catalog:
            return {"error": f"catalog not found: {region}/{dataset}"}

        fields = [f for f in (catalog.get("fields") or []) if self._field_name(f)]
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for field in fields:
            name = self._field_name(field)
            if not name:
                continue
            prefix = self._prefix_for(name, depth=prefix_depth)
            grouped.setdefault(prefix, []).append(field)

        clusters: List[Dict[str, Any]] = []
        for prefix, items in grouped.items():
            names = [self._field_name(f) for f in items if self._field_name(f)]
            coverages = [float(f.get("coverage")) for f in items if f.get("coverage") is not None]
            vector_count = sum(1 for f in items if str(self._field_type(f) or "").upper() == "VECTOR")
            high_cov = sum(1 for c in coverages if c >= coverage_high)
            clusters.append({
                "prefix": prefix,
                "count": len(items),
                "coverage_mean": round(sum(coverages) / len(coverages), 4) if coverages else None,
                "coverage_median": round(median(coverages), 4) if coverages else None,
                "high_coverage_count": high_cov,
                "vector_count": vector_count,
                "sample_fields": names[:samples_per_cluster],
                "risk_flags": self._risk_flags(prefix, items, coverages),
            })

        clusters.sort(key=lambda x: (-x["count"], x["prefix"]))
        risk_clusters = [c for c in clusters if c["risk_flags"]]
        payload = {
            "region": region,
            "dataset": dataset,
            "prefix_depth": prefix_depth,
            "total_fields": len(fields),
            "total_clusters": len(clusters),
            "top_clusters": clusters[:top_n],
            "risk_clusters": risk_clusters[:top_n],
            "source": "field_prefix_cluster_db",
            "updated_at": _now(),
        }
        if persist:
            self.upsert_ledger(region, f"s1_prefix_{dataset}", payload)
        return payload

    def get_field_prefix_clusters(self, region: str, dataset: str) -> Optional[Dict[str, Any]]:
        """Read persisted S1 field-prefix cluster summary from ledger_kv."""
        cached = self.get_ledger(region, f"s1_prefix_{dataset}")
        return cached if isinstance(cached, dict) else None

    @staticmethod
    def _field_int(field: Dict[str, Any], keys: tuple) -> int:
        """读取字段整数型平台指标，缺失/非数值返回 0。"""
        for key in keys:
            value = field.get(key)
            if value is None:
                continue
            try:
                return int(value)
            except (TypeError, ValueError):
                continue
        return 0

    @classmethod
    def _quality_score(cls, field: Dict[str, Any]) -> float:
        """字段质量先验评分（2026-09-13，与 S1 脚本 _quality_score 同口径）。

        alphaCount 为主信号（已挖 alpha 数 = 字段有 alpha 的最强证据），userCount
        辅助（权重减半），coverage 仅微调。两处公式必须保持一致——否则 S1 概念
        字段与候选池再次口径分叉（GLB fundamental23 实测：候选池 30 字段与 8 个
        概念字段交集仅 2 个，6 个概念在 GEM 绑定阶段被白名单静默丢弃）。
        """
        ac = cls._field_int(field, ("alphaCount", "alpha_count"))
        uc = cls._field_int(field, ("userCount", "user_count"))
        cov = field.get("coverage")
        try:
            cov = float(cov) if cov is not None else 0.0
        except (TypeError, ValueError):
            cov = 0.0
        return math.log1p(ac) + 0.5 * math.log1p(uc) + 0.1 * cov

    @classmethod
    def _pick_quality_diverse(cls, fields: List[Dict[str, Any]], n: int) -> List[str]:
        """按质量先验取前 n 个字段，并保证首前缀（字段族）多样性。

        与 brain-data-feature-engineering/scripts/feature_engineering.py::_pick_diverse
        同策略：第一遍每族取质量最高者，第二遍按质量补齐——保证池内既有质量排序，
        不因单一字段族霸榜而与 S1 概念字段（同族多样化选法）再次分叉。
        """
        ranked = sorted(fields, key=cls._quality_score, reverse=True)
        picked: List[str] = []
        seen_prefix = set()
        for field in ranked:
            name = cls._field_name(field)
            if not name or name in picked:
                continue
            prefix = name.split("_", 1)[0] if "_" in name else name
            if prefix in seen_prefix:
                continue
            seen_prefix.add(prefix)
            picked.append(name)
            if len(picked) >= n:
                return picked
        for field in ranked:
            name = cls._field_name(field)
            if not name or name in picked:
                continue
            picked.append(name)
            if len(picked) >= n:
                break
        return picked

    @classmethod
    def _has_quality_signals(cls, fields: List[Dict[str, Any]]) -> bool:
        """目录是否携带 alphaCount/userCount 质量信号（全 0/缺失则回退旧逻辑）。"""
        return any(
            cls._field_int(f, ("alphaCount", "alpha_count"))
            or cls._field_int(f, ("userCount", "user_count"))
            for f in fields
        )

    @staticmethod
    def _derive_candidate_field_pool(summary: Optional[Dict[str, Any]], max_fields: int = 30) -> List[str]:
        if not summary:
            return []
        pool: List[str] = []
        seen = set()
        for cluster in summary.get("top_clusters") or []:
            if cluster.get("risk_flags"):
                continue
            for name in cluster.get("sample_fields") or []:
                if name and name not in seen:
                    seen.add(name)
                    pool.append(name)
                if len(pool) >= max_fields:
                    return pool
        for cluster in summary.get("top_clusters") or []:
            for name in cluster.get("sample_fields") or []:
                if name and name not in seen:
                    seen.add(name)
                    pool.append(name)
                if len(pool) >= max_fields:
                    return pool
        return pool

    def build_candidate_field_pool(
        self,
        region: str,
        dataset: str,
        max_fields: int = 30,
        persist: bool = True,
        rank_by_quality: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Derive S2 candidate field pool and persist to ledger_kv.

        2026-09-13 口径统一（S1↔S2 接力修复）：优先按字段质量先验
        （alphaCount/userCount/coverage，与 S1 概念字段同一评分）从目录直接选池，
        不再默认按前缀簇采样——旧实现与 S1 概念的“质量排序”口径分叉，GLB
        fundamental23 实测候选池 30 字段与 8 个概念字段交集仅 2 个，其余 6 个概念
        在 GEM 绑定阶段被白名单静默丢弃。目录无质量信号（旧测试/离线目录）时
        自动回退旧前缀簇采样，行为与历史一致。

        Args:
            rank_by_quality: None=自动（有 alphaCount/userCount 即启用）；
                True/False 可强制指定（干跑对比、回归排查用）。
        """
        pool: List[str] = []
        source = "s1_prefix_summary"
        clusters_covered = 0
        catalog = self.get_field_catalog(region, dataset)
        if catalog and catalog.get("fields"):
            fields = [f for f in catalog["fields"] if self._field_name(f)]
            use_quality = (
                rank_by_quality if rank_by_quality is not None
                else self._has_quality_signals(fields)
            )
            if fields:
                # 2026-09-15 ⑤：跨簇轮转采样。旧两条路径（质量排序 / 前缀簇 sample_fields）
                # 都会被单一字段族霸榜——前缀簇按字母序取前 5 个样本，intraday_pv_feats 每个
                # 统计簇（mean/max/corr…）的前 5 个全是 *_ask_price_*，585 字段/21 簇只喂了
                # 1 个主体族给 GEM。现按"主体 token"分簇，簇间轮转、簇内按质量/子族展开。
                pool, clusters_covered = self._pick_cross_cluster(fields, max_fields, use_quality)
                source = "cross_cluster_quality" if use_quality else "cross_cluster"
        if not pool:
            summary = self.get_field_prefix_clusters(region, dataset)
            if not summary:
                summary = self.build_field_prefix_clusters(region, dataset, persist=True)
            if summary.get("error"):
                return summary
            pool = self._derive_candidate_field_pool(summary, max_fields=max_fields)
        payload = {
            "region": region,
            "dataset": dataset,
            "candidate_field_pool": pool,
            "pool_size": len(pool),
            "clusters_covered": clusters_covered,
            "source": source,
            "builder_version": POOL_BUILDER_VERSION,
            "updated_at": _now(),
        }
        if persist:
            self.upsert_ledger(region, f"s2_field_pool_{dataset}", payload)
        return payload

    def get_candidate_field_pool(self, region: str, dataset: str) -> Optional[Dict[str, Any]]:
        """Read persisted S2 candidate field pool from ledger_kv.

        builder_version 不等于当前 POOL_BUILDER_VERSION 的旧池视为过期（返回 None，
        调用方会重建）——否则算法修好了、旧池照样被 GEM 消费。
        """
        cached = self.get_ledger(region, f"s2_field_pool_{dataset}")
        if not isinstance(cached, dict):
            return None
        if int(cached.get("builder_version") or 0) != POOL_BUILDER_VERSION:
            return None
        return cached

    @classmethod
    def _subject_key(cls, name: str) -> str:
        """字段的"主体"簇键：跳过前导统计量 token（mean/max/corr/momentum…），取第一个
        非统计 token；全是统计 token 时退回首 token。mean_ask_price_30m → ask；
        corr_bid_price_with_volume → bid；anl_est_eps → anl；vwap_30m_post_open → vwap。"""
        parts = [p for p in str(name).lower().split("_") if p]
        for p in parts:
            if p not in _STAT_TOKENS and not p.isdigit():
                return p
        return parts[0] if parts else str(name)

    @classmethod
    def _pick_cross_cluster(cls, fields: List[Dict[str, Any]], n: int, use_quality: bool):
        """簇间轮转采样：按主体 token 分簇 → 簇按最高质量（或字段数）排序 →
        每轮每簇取 1 个（簇内先按质量、再保证子族=第二 token 不重复）直到凑满 n。
        返回 (pool, 覆盖簇数)。"""
        clusters: Dict[str, List[Dict[str, Any]]] = {}
        for f in fields:
            name = cls._field_name(f)
            if not name:
                continue
            clusters.setdefault(cls._subject_key(name), []).append(f)
        if not clusters:
            return [], 0

        def _ordered(items):
            if use_quality:
                items = sorted(items, key=cls._quality_score, reverse=True)
            # 簇内子族（主体之后的下一个非统计 token）先各取一个，再补齐
            seen_sub, first, rest = set(), [], []
            for f in items:
                name = cls._field_name(f)
                toks = [p for p in str(name).lower().split("_") if p]
                subj = cls._subject_key(name)
                after = toks[toks.index(subj) + 1:] if subj in toks else toks[1:]
                sub = next((t for t in after if t not in _STAT_TOKENS and not t.isdigit()), "")
                if sub in seen_sub:
                    rest.append(f)
                else:
                    seen_sub.add(sub)
                    first.append(f)
            return first + rest

        ordered = {k: _ordered(v) for k, v in clusters.items()}
        if use_quality:
            order = sorted(ordered, key=lambda k: (-cls._quality_score(ordered[k][0]), -len(ordered[k]), k))
        else:
            order = sorted(ordered, key=lambda k: (-len(ordered[k]), k))
        pool: List[str] = []
        seen = set()
        idx = {k: 0 for k in order}
        while len(pool) < n:
            progressed = False
            for k in order:
                items = ordered[k]
                while idx[k] < len(items):
                    name = cls._field_name(items[idx[k]])
                    idx[k] += 1
                    if name and name not in seen:
                        seen.add(name)
                        pool.append(name)
                        progressed = True
                        break
                if len(pool) >= n:
                    break
            if not progressed:
                break
        covered = len({cls._subject_key(p) for p in pool})
        return pool, covered

    def upsert_field_catalog(self, region: str, catalog: Dict[str, Any]) -> Dict[str, Any]:
        dataset = catalog.get("dataset") or catalog.get("id")
        if not dataset:
            raise ValueError("catalog missing dataset")
        fields = catalog.get("fields") or []
        extra = {
            "field_count": catalog.get("field_count", len(fields)),
            "data_type": catalog.get("data_type"),
            "catalog_json": _dumps(catalog),
            "status": "scanned",
        }
        ds_id = self._ensure_dataset(region, dataset, extra)
        cur = self.connection.cursor()
        n = 0
        for f in fields:
            fname = self._field_name(f)
            if not fname:
                continue
            cur.execute(
                "SELECT id FROM fields WHERE dataset_id=? AND field_name=?",
                (ds_id, fname),
            )
            row = cur.fetchone()
            vals = (
                self._field_type(f),
                f.get("coverage"),
                f.get("userCount") if "userCount" in f else f.get("user_count"),
                f.get("alphaCount") if "alphaCount" in f else f.get("alpha_count"),
                (f.get("description") or "")[:240],
                f.get("field_group"),
            )
            if row:
                cur.execute(
                    """UPDATE fields SET field_type=?, coverage=?, user_count=?,
                       alpha_count=?, description=?, field_group=? WHERE id=?""",
                    vals + (int(row[0]),),
                )
            else:
                cur.execute(
                    """INSERT INTO fields
                       (dataset_id, field_name, field_type, coverage, user_count,
                        alpha_count, description, field_group, created_at)
                       VALUES (?,?,?,?,?,?,?,?,?)""",
                    (ds_id, fname) + vals + (_now(),),
                )
            n += 1
        self.connection.commit()
        self.upsert_ledger(region, f"catalog_{dataset}", catalog)
        return {"n": n, "region": region, "dataset": dataset}

    def get_field_catalog(self, region: str, dataset: str) -> Optional[Dict[str, Any]]:
        cached = self.get_ledger(region, f"catalog_{dataset}")
        if isinstance(cached, dict) and cached.get("fields"):
            return cached
        rid = self._ensure_region(region)
        cur = self.connection.cursor()
        cur.execute(
            "SELECT id, data_type, catalog_json, field_count FROM datasets "
            "WHERE name=? AND region_id=?",
            (dataset, rid),
        )
        ds = cur.fetchone()
        if not ds:
            return None
        if ds["catalog_json"]:
            blob = _loads(ds["catalog_json"])
            if isinstance(blob, dict):
                return blob
        cur.execute(
            "SELECT field_name, field_type, coverage, user_count, alpha_count, "
            "description, field_group FROM fields WHERE dataset_id=?",
            (int(ds["id"]),),
        )
        fields = []
        for r in cur.fetchall():
            fields.append({
                "id": r["field_name"],
                "type": r["field_type"],
                "coverage": r["coverage"],
                "userCount": r["user_count"],
                "alphaCount": r["alpha_count"],
                "description": r["description"],
                "field_group": r["field_group"],
            })
        return {
            "dataset": dataset,
            "region": region,
            "data_type": ds["data_type"] or "MATRIX",
            "field_count": len(fields),
            "fields": fields,
        }
