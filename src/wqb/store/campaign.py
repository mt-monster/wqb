# -*- coding: utf-8 -*-
"""CampaignStore: denormalized campaign writes on data/wqb.db.

Existing tables (expressions/fields/waves/datasets/regions/…) keep their
FK layout. This module adds region/wave/dataset columns where missing and
a gate_results table, then upserts by (region, wave, expression).

Architecture (2026-08-29 refactor): the original 1240-line monolith was
split into focused mixins, mirroring the brain_api decomposition pattern.
CampaignStore inherits all mixins; public API is unchanged.

    CampaignStore
      ├── SchemaMixin          (_schema.py)         ensure_schema, _ensure_region/dataset/wave
      ├── LedgerMixin          (_ledger.py)         upsert/get_ledger
      ├── ExpressionsMixin     (_expressions.py)    upsert/list/history_expressions
      ├── FieldCatalogMixin    (_field_catalog.py)  upsert/get_field_catalog
      ├── FieldProfileMixin   (_field_profile.py)  upsert/get_field_profile
      ├── GateMixin            (_gate.py)           upsert/get_gate_result
      ├── BacktestMixin        (_backtest.py)       upsert_backtest_rows, record_submission
      ├── CorrCacheMixin       (_corr_cache.py)     get/set_corr_cache（相关性查询缓存）
      ├── DiversityMixin       (_diversity.py)      diversity, ranking, checkpoint, rules, ideas
      ├── AlphasMixin          (_alphas.py)         get/list/search alphas
      └── SubmissionsMixin     (_submissions.py)    upsert/get/list_submissions, quota_status

Shared utilities (ExprItem, default_db_path, _now, _dumps, _loads, _as_expr)
live in _common.py and are re-exported here for backward compatibility.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
from wqb.config import is_pseudo_alpha  # 伪 alpha 黑名单（经济学池生成侧剔除，单源）

# Re-export shared utilities for backward compatibility
# (callers may do `from wqb.store.campaign import default_db_path, ExprItem, …`)
from ._common import (  # noqa: F401
    ExprItem,
    _DEFAULT_REL,
    _as_expr,
    _dumps,
    _loads,
    _now,
    default_db_path,
)

# Import mixins
from ._schema import SchemaMixin
from ._ledger import LedgerMixin
from ._expressions import ExpressionsMixin
from ._field_catalog import FieldCatalogMixin, POOL_BUILDER_VERSION
from ._field_economic import build_economic_field_pool, classify_fields
from ._field_patterns import (
    extract_field_patterns,
    build_field_combination_rules,
    persist_field_patterns,
    merge_field_patterns_across_waves,
)
from ._field_profile import FieldProfileMixin
from ._gate import GateMixin
from ._backtest import BacktestMixin
from ._corr_cache import CorrCacheMixin
from ._diversity import DiversityMixin
from ._alphas import AlphasMixin
from ._submissions import SubmissionsMixin


class CampaignStore(
    SchemaMixin,
    LedgerMixin,
    ExpressionsMixin,
    FieldCatalogMixin,
    FieldProfileMixin,
    GateMixin,
    BacktestMixin,
    CorrCacheMixin,
    DiversityMixin,
    AlphasMixin,
    SubmissionsMixin,
):
    """SQLite campaign artifact store.

    All table-specific CRUD methods are inherited from focused mixins.
    This class only manages connection lifecycle and schema initialization.
    """

    # ---- 经济学字段归类（2026-09-25 落地） ----

    def build_economic_field_pool(
        self,
        region: str,
        dataset: str,
        max_fields: int = 30,
        min_per_category: int = 2,
        max_per_category: int = 8,
        persist: bool = True,
        data_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """按经济学含义构建字段池（替代/增强旧 _pick_cross_cluster）。

        与旧方法的区别：
        - 旧：按"主体 token"分簇（mean_ask_price → ask），无经济学含义
        - 新：按经济学类别分簇（value/growth/quality/...），有经济学约束

        2026-10-01（步3 断流修复 · 止血 A）：建池前先按 ledger `s1_semantic_<ds>`
        的 `blocked_fields`（货币代码 / 汇率叉乘 / 标识符 / 分类码 / 日期口径）
        剔除**非信号字段**。此前语义归类的结果只被步 5 闸 SEM 消费、生成侧完全不读，
        等于「先生成后治理」——KOR/IND 实测有 `transaction_currency_code` 这类字段
        进了 GEM 绑定池。**fail-open**：台账缺失/读不到即不剔除（不阻断生成，也不改变
        闸 SEM 原有的 fail-closed 契约）——语义过滤是**减负**，不是新的把关点。

        2026-10-02 v6（GLB/analyst69 混合集首波归因）：新增 `data_type` 过滤 +
        `field_type=signal` 偏好。起因——analyst69 是 **VECTOR/MATRIX 混合集**
        （GLB: 515 VECTOR + 264 MATRIX）。旧池按经济学关键词归类，**完全不看字段
        `type`** → 30 字段池里混了 16 VECTOR + 14 MATRIX。GEM 被传 `data_type=MATRIX`
        后只筛出那 14 个 MATRIX，且恰是 `*_expected_report_time` /
        `*_best_cur_fiscal_qtr_period` 这类 **metadata 字段**（field_type=date/metadata）
        → ideas 里引用的真实信号字段（`anl69_best_ebit_median` 等）全不在白名单
        → 155/155 模板因占位符无法绑定被丢弃，整波归零。
        **要点：池的类型必须与 GEM 被告知的 `data_type` 一致**；混合集上这个一致性
        不会自动成立（rollup data_type 是多数票，会把少数派类型整波裁掉）。
        `data_type=None` 保持旧行为（不过滤），向后兼容。
        """
        catalog = self.get_field_catalog(region, dataset)
        if not catalog or not catalog.get("fields"):
            return {"error": f"catalog not found: {region}/{dataset}"}

        fields = [f for f in catalog["fields"] if self._field_name(f)
                  and not is_pseudo_alpha(self._field_name(f))]  # 剔除 riskfree/beta/基准伪 alpha
        fields, sem_meta = self._drop_semantic_blocked(region, dataset, fields)
        # 2026-10-02 v6：类型一致性过滤（混合集关键；data_type=None 时跳过）
        type_meta = {"requested": data_type, "before_n": len(fields),
                     "after_n": len(fields), "dropped_n": 0, "by_type": {}}
        if data_type:
            _want = str(data_type).strip().upper()
            kept, dropped = [], []
            for f in fields:
                _t = str(self._field_type(f) or "").strip().upper()
                # 字段无 type 信息时保留（fail-open：不让缺元数据误杀）
                if not _t or _t == _want:
                    kept.append(f)
                else:
                    dropped.append(self._field_name(f))
            fields = kept
            type_meta.update({
                "after_n": len(fields), "dropped_n": len(dropped),
                "dropped_sample": dropped[:8],
            })
        # 2026-10-02 v6：优先保留 field_type=signal 的字段（metadata/date/scale 排后）
        _sig, _non = [], []
        for f in fields:
            _ft = str(f.get("field_type") or "").strip().lower()
            (_sig if _ft in ("", "signal") else _non).append(f)
        if _sig:
            fields = _sig + _non  # 信号字段优先入池；非信号仅在信号不足时补位
            type_meta["field_type_split"] = {"signal_pref": len(_sig), "other": len(_non)}
        pool, stats = build_economic_field_pool(
            fields, max_fields=max_fields,
            min_per_category=min_per_category,
            max_per_category=max_per_category,
        )

        # 2026-10-01 P2：把 L3.5 族结构并入字段池 payload，供 GEM 概念优先消费。
        #   此前字段池只到「经济学归类」粒度，族/形态假设（L3.5/L4）不进池 →
        #   GEM 的「概念优先」实质是 LLM 自由发挥。族结构来自语义台账 families 段。
        families_meta = self._extract_families(region, dataset, pool)

        payload = {
            "region": region,
            "dataset": dataset,
            "candidate_field_pool": pool,
            "pool_size": len(pool),
            "economic_stats": stats,
            "source": "economic_category",
            "semantic_filter": sem_meta,
            "type_filter": type_meta,
            "families": families_meta["families"],
            "family_stats": families_meta["stats"],
            # 必须与 _field_catalog.POOL_BUILDER_VERSION 同步（get_candidate_field_pool
            # 按版本判缓存新鲜度，硬编码不一致 → 经济学池缓存永不命中，每次重建）
            "builder_version": POOL_BUILDER_VERSION,
            "updated_at": _now(),
        }
        if persist:
            self.upsert_ledger(region, f"s2_field_pool_{dataset}", payload)
        return payload

    def _drop_semantic_blocked(self, region: str, dataset: str,
                               fields: List[Dict[str, Any]]):
        """按 `s1_semantic_<ds>` 台账剔除非信号字段（fail-open）。

        返回 (fields', meta)；meta = {ledger, blocked_n, dropped_n, dropped:[...]}。
        台账缺失 / 解析失败 / 无 blocked_fields → 原样返回并标注 ledger=False。
        """
        meta = {"ledger": False, "blocked_n": 0, "dropped_n": 0, "dropped": []}
        try:
            sem = self.get_ledger(region, f"s1_semantic_{dataset}")
        except Exception:
            return fields, meta
        if not isinstance(sem, dict):
            return fields, meta
        raw = sem.get("blocked_fields") or []
        blocked = set()
        for b in raw:
            name = b.get("field") if isinstance(b, dict) else b
            if name:
                blocked.add(str(name))
        meta["ledger"] = True
        meta["blocked_n"] = len(blocked)
        if not blocked:
            return fields, meta
        kept, dropped = [], []
        for f in fields:
            n = self._field_name(f)
            if n and str(n) in blocked:
                dropped.append(str(n))
            else:
                kept.append(f)
        meta["dropped_n"] = len(dropped)
        meta["dropped"] = dropped[:20]
        return kept, meta

    def _extract_families(self, region: str, dataset: str,
                          pool: List[str]) -> Dict[str, Any]:
        """从 `s1_semantic_<ds>` 提取 L3.5 族结构，剔到字段池内的族（P2，fail-open）。

        返回 {"families": {族键: {n, kind, roles:[{field,role}], cats}}, "stats": {...}}。
        语义台账缺失 / 无 families 段 / 解析失败 → 返回空 families + stats.available=False。
        **只保留与字段池有交集的族**：池外的族对本次生成无意义，带上会稀释 prompt。
        """
        out: Dict[str, Any] = {"families": {}, "stats": {
            "available": False, "n_families_total": 0, "n_families_in_pool": 0}}
        try:
            sem = self.get_ledger(region, f"s1_semantic_{dataset}")
        except Exception:
            return out
        if not isinstance(sem, dict):
            return out
        fams = sem.get("families")
        if not isinstance(fams, dict) or not fams:
            return out
        pool_set = set(pool or [])
        out["stats"]["n_families_total"] = len(fams)
        kept: Dict[str, Any] = {}
        for key, v in fams.items():
            if not isinstance(v, dict):
                continue
            flds = [f for f in (v.get("fields") or []) if f in pool_set]
            if not flds:
                continue  # 该族在字段池里无代表字段 → 不进 payload
            roles = [r for r in (v.get("roles") or [])
                     if isinstance(r, dict) and r.get("field") in pool_set]
            kept[str(key)] = {
                "n": len(flds),
                "kind": v.get("kind"),
                "cats": v.get("cats") or [],
                "fields": flds[:12],
                "roles": roles[:12],
            }
        out["families"] = kept
        out["stats"]["n_families_in_pool"] = len(kept)
        out["stats"]["available"] = bool(kept)
        return out

    def classify_dataset_fields(
        self,
        region: str,
        dataset: str,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """对数据集字段做经济学含义聚类并持久化。"""
        catalog = self.get_field_catalog(region, dataset)
        if not catalog or not catalog.get("fields"):
            return {"error": f"catalog not found: {region}/{dataset}"}

        fields = [f for f in catalog["fields"] if self._field_name(f)]
        clusters = classify_fields(fields)

        payload = {
            "region": region,
            "dataset": dataset,
            "total_fields": len(fields),
            "categories": {
                cat: {
                    "count": len(fields),
                    "top_fields": [
                        self._field_name(f) for f in fields[:5]
                    ],
                    "avg_quality": round(
                        sum(self._quality_score(f) for f in fields) / len(fields), 3
                    ) if fields else 0,
                }
                for cat, fields in clusters.items()
            },
            "updated_at": _now(),
        }
        if persist:
            self.upsert_ledger(region, f"s1_economic_clusters_{dataset}", payload)
        return payload

    # ---- S6 字段组合规律挖掘（2026-09-25 落地） ----

    def extract_wave_field_patterns(
        self,
        region: str,
        wave: str,
        min_sharpe: float = 0.5,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """从指定波的回测结果中提取字段组合规律。"""
        cur = self.connection.cursor()
        # 2026-09-25 修复：backtest_results 表达式列是 code（非 expression）；
        # code 为空的行回退 expression_id → expressions 表。
        cur.execute(
            "SELECT COALESCE(b.code, e.expression) AS expr, b.sharpe, b.fitness "
            "FROM backtest_results b LEFT JOIN expressions e ON b.expression_id = e.id "
            "WHERE b.region=? AND b.wave=? AND b.sharpe IS NOT NULL",
            (region, str(wave)),
        )
        rows = [
            {"expression": r[0], "sharpe": r[1], "fitness": r[2]}
            for r in cur.fetchall() if r[0]
        ]
        if not rows:
            return {"error": f"no backtest results for {region}/{wave}"}

        patterns = extract_field_patterns(rows, min_sharpe=min_sharpe)
        rules = build_field_combination_rules(patterns)

        if persist:
            persist_field_patterns(self, region, str(wave), patterns, rules)

        return {
            "region": region,
            "wave": wave,
            "total_rows": len(rows),
            "patterns": patterns,
            "rules": rules,
        }

    def merge_region_field_patterns(
        self,
        region: str,
        waves: Optional[List[str]] = None,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """合并多波字段组合规律，找跨波稳定模式。"""
        if waves is None:
            # 自动获取最近 10 波
            cur = self.connection.cursor()
            cur.execute(
                "SELECT DISTINCT wave FROM backtest_results WHERE region=? "
                "ORDER BY id DESC LIMIT 10",
                (region,),
            )
            waves = [str(r[0]) for r in cur.fetchall()]

        merged = merge_field_patterns_across_waves(self, region, waves)
        if persist and "error" not in merged:
            self.upsert_ledger(region, f"s6_field_patterns_{region}_merged", merged)
        return merged

    def __init__(self, path: Optional[str] = None):
        self.path = path or default_db_path()
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = db_connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")
        self.connection.execute("PRAGMA cache_size=-64000")
        self.ensure_schema()

    @classmethod
    def from_workspace(cls, workspace_root: Optional[str] = None) -> "CampaignStore":
        return cls(default_db_path(workspace_root))

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def __enter__(self) -> "CampaignStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def get_database_integration(workspace_root: Optional[str] = None) -> CampaignStore:
    """Compatibility alias for pipeline / inspect / diversity_extract."""
    return CampaignStore.from_workspace(workspace_root)
