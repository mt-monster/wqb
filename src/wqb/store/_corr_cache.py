# -*- coding: utf-8 -*-
"""CorrCacheMixin — 平台相关性查询结果的本地区缓存（2026-10-04）。

动机：BRAIN 的相关性接口是**单账号单并发**，每颗 alpha 首次计算要 1-5 分钟。
MCP 侧的自相关（self）有文件缓存（``downloads/os_pnl_pool_*.pkl``），但
**prod 结果的唯一缓存后端是 Redis**；本机 Redis 常未启动 →
``redis_client=None`` → 缓存整条失效 → 多会话各自重复打平台单并发队列，
表现为「每次多会话查都要等很久」。

本模块把 prod/self 结果落到 ``data/wqb.db`` 的 ``alpha_corr_cache`` 表：

- **与 ``alphas`` 表解耦**：仿真 alpha（UNSUBMITTED）不在 ``alphas`` 里
  （实测 ``E5RaV7Rr`` / ``O08kz5Mv`` 均 NOT IN alphas），用独立表才能缓存；
- **SQLite 天生跨进程共享**：多个 MCP 进程读同一份文件，无需 Redis；
- **让「查过就有」成立**：避免重复占用平台单并发队列。

契约（与 :meth:`BacktestMixin.persist_correlation` 同口径）：

- 相关性值须落在 ``[0, 1]``，否则按「没有」处理（防空值与异常值污染）；
- :meth:`set_corr_cache` 幂等：同值重复写不改变结果。
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from ._common import _now
from ._backtest import _corr_value

_CACHE_COLUMNS = (
    "alpha_id, prod_correlation, self_correlation, prod_records, source, checked_at"
)


class CorrCacheMixin:
    """``alpha_corr_cache`` 表的读写。

    与 ``alphas`` 表分开存：仿真阶段的 alpha 尚未进 ``alphas``，
    但仍需要缓存其相关性取值。
    """

    def get_corr_cache(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """读一条缓存；不存在返回 ``None``。

        ``max`` 字段与 ``check_correlation`` 的返回口径对齐，便于直接回填。
        """
        if not alpha_id:
            return None
        cur = self.connection.cursor()
        cur.execute(
            f"SELECT {_CACHE_COLUMNS} FROM alpha_corr_cache WHERE alpha_id=?",
            (str(alpha_id),),
        )
        row = cur.fetchone()
        if not row:
            return None
        prod = _corr_value(row[1])
        self_corr = _corr_value(row[2])
        records: Optional[List[Any]] = None
        if row[3]:
            try:
                records = json.loads(row[3])
            except (TypeError, ValueError):
                records = None
        return {
            "alpha_id": row[0],
            "max": prod,
            "prod_correlation": prod,
            "self_correlation": self_corr,
            "records": records,
            "source": row[4],
            "checked_at": row[5],
        }

    def set_corr_cache(
        self,
        alpha_id: str,
        prod: Optional[float] = None,
        self_: Optional[float] = None,
        records: Any = None,
        source: str = "platform",
    ) -> Dict[str, Any]:
        """写一条缓存（upsert，幂等）。

        任一列传入 ``None`` 时**保留旧值**（``COALESCE``），
        这样「只补 prod」不会把已存的 self 抹掉。
        """
        if not alpha_id:
            return {"skipped": "no_alpha_id"}

        p = _corr_value(prod)
        s = _corr_value(self_)
        recs_json: Optional[str] = None
        if records is not None:
            try:
                recs_json = json.dumps(records, ensure_ascii=False)
            except (TypeError, ValueError):
                recs_json = None

        if p is None and s is None and recs_json is None:
            return {"skipped": "no_valid_value", "alpha_id": str(alpha_id)}

        now = _now()
        cur = self.connection.cursor()
        cur.execute(
            "INSERT INTO alpha_corr_cache "
            "(alpha_id, prod_correlation, self_correlation, prod_records, "
            " source, checked_at, created_at, updated_at) "
            "VALUES (?,?,?,?,?,?,?,?) "
            "ON CONFLICT(alpha_id) DO UPDATE SET "
            "  prod_correlation=COALESCE(excluded.prod_correlation, prod_correlation),"
            "  self_correlation=COALESCE(excluded.self_correlation, self_correlation),"
            "  prod_records=COALESCE(excluded.prod_records, prod_records),"
            "  source=excluded.source,"
            "  checked_at=excluded.checked_at,"
            "  updated_at=excluded.updated_at",
            (str(alpha_id), p, s, recs_json, source, now, now, now),
        )
        self.connection.commit()
        return {
            "action": "upserted",
            "alpha_id": str(alpha_id),
            "prod_correlation": p,
            "self_correlation": s,
            "source": source,
            "checked_at": now,
        }

    def list_corr_cache(self, alpha_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """批量读缓存，返回 ``{alpha_id: 记录}``（缺失的键不出现）。"""
        ids = [str(a) for a in (alpha_ids or []) if a]
        if not ids:
            return {}
        out: Dict[str, Dict[str, Any]] = {}
        cur = self.connection.cursor()
        # 分块避免 SQLite 变量上限（默认 999）
        for i in range(0, len(ids), 500):
            chunk = ids[i:i + 500]
            marks = ",".join("?" * len(chunk))
            cur.execute(
                f"SELECT {_CACHE_COLUMNS} FROM alpha_corr_cache WHERE alpha_id IN ({marks})",
                chunk,
            )
            for row in cur.fetchall():
                prod = _corr_value(row[1])
                records = None
                if row[3]:
                    try:
                        records = json.loads(row[3])
                    except (TypeError, ValueError):
                        records = None
                out[row[0]] = {
                    "alpha_id": row[0],
                    "max": prod,
                    "prod_correlation": prod,
                    "self_correlation": _corr_value(row[2]),
                    "records": records,
                    "source": row[4],
                    "checked_at": row[5],
                }
        return out
