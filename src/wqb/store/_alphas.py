# -*- coding: utf-8 -*-
"""AlphasMixin: alpha query methods for CampaignStore."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ._common import _now


class AlphasMixin:
    """Alpha query methods."""

    def get_alpha_by_id(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """根据 alpha_id 查询 alpha 详情（含 region 名）。"""
        cur = self.connection.cursor()
        cur.execute(
            "SELECT a.*, r.name AS region FROM alphas a "
            "JOIN regions r ON a.region_id = r.id "
            "WHERE a.alpha_id=?",
            (alpha_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def list_alphas_by_region(self, region: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出某 region 的全部 alpha（可选 status 过滤）。"""
        cur = self.connection.cursor()
        sql = (
            "SELECT a.*, r.name AS region FROM alphas a "
            "JOIN regions r ON a.region_id = r.id "
            "WHERE r.name=?"
        )
        params: List[Any] = [region]
        if status:
            sql += " AND a.status=?"
            params.append(status)
        sql += " ORDER BY a.updated_at DESC"
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def search_alphas_by_sharpe(
        self,
        region: Optional[str] = None,
        min_sharpe: float = 1.0,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """按 sharpe 搜索 alpha（sharpe >= min_sharpe）。"""
        cur = self.connection.cursor()
        sql = (
            "SELECT a.*, r.name AS region FROM alphas a "
            "JOIN regions r ON a.region_id = r.id "
            "WHERE a.sharpe >= ?"
        )
        params: List[Any] = [min_sharpe]
        if region:
            sql += " AND r.name=?"
            params.append(region)
        sql += " ORDER BY a.sharpe DESC LIMIT ?"
        params.append(limit)
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def upsert_alpha_os_metrics(self, alpha_id: str, os_data: Dict[str, Any],
                                region: Optional[str] = None,
                                submitted_info: Optional[Dict[str, Any]] = None,
                                overwrite: bool = False) -> Dict[str, Any]:
        """把平台 `os`（样本外）段指标落库到 alphas（2026-09-20 新增）。

        背景：平台 alpha 对象的 `os` 段此前从未落库，MCP `get_alpha_details`
        的 `_slim_alpha()` 也只取 `is` 段 —— 已提交 alpha 的样本外表现在本地
        完全不可查。本方法 + `sync_platform_alphas` 补上这条链路。

        契约：
          - alpha 不存在且未提供 region → {"skipped": "not_found"}
          - alpha 不存在但提供 region → 插入骨架行（platform_status/date_submitted 等）
          - overwrite=False（默认）→ 只填 NULL 的 os_* 列（保留既有值）
          - overwrite=True → 覆盖（用于平台修正）
          - os 段无任何指标（仅 startDate）→ 记 os_start_date 后 skipped=no_metrics
            （近期提交常见：平台尚未积累 OS 样本）

        os_data 期望键（平台 os 段原生字段名）：startDate / sharpe / fitness /
        turnover / returns / drawdown / margin / sharpe60 / sharpe125 / sharpe250 /
        sharpe500 / preCloseSharpe / osISSharpeRatio / preCloseSharpeRatio
        """
        if not alpha_id:
            return {"skipped": "no_alpha_id"}
        os_data = os_data or {}

        def _f(v: Any) -> Optional[float]:
            try:
                return float(v) if v is not None and v != "" else None
            except (TypeError, ValueError):
                return None

        mapping = {
            "os_start_date": os_data.get("startDate"),
            "os_sharpe": _f(os_data.get("sharpe")),
            "os_fitness": _f(os_data.get("fitness")),
            "os_turnover": _f(os_data.get("turnover")),
            "os_returns": _f(os_data.get("returns")),
            "os_drawdown": _f(os_data.get("drawdown")),
            "os_margin": _f(os_data.get("margin")),
            "os_sharpe60": _f(os_data.get("sharpe60")),
            "os_sharpe125": _f(os_data.get("sharpe125")),
            "os_sharpe250": _f(os_data.get("sharpe250")),
            "os_sharpe500": _f(os_data.get("sharpe500")),
            "os_preclose_sharpe": _f(os_data.get("preCloseSharpe")),
            "os_is_sharpe_ratio": _f(os_data.get("osISSharpeRatio")),
            "os_preclose_sharpe_ratio": _f(os_data.get("preCloseSharpeRatio")),
        }
        # 指标列与窗口起点分开处理：只有 startDate 不算"有 OS 指标"
        metric_cols = {k: v for k, v in mapping.items() if k != "os_start_date"}
        has_metrics = any(v is not None for v in metric_cols.values())
        start_date = mapping["os_start_date"]

        cur = self.connection.cursor()
        now = _now()
        cur.execute("SELECT id FROM alphas WHERE alpha_id=?", (alpha_id,))
        row = cur.fetchone()

        if row:
            target_id = int(row[0])
        else:
            if not region:
                return {"skipped": "not_found", "alpha_id": alpha_id}
            rid = self._ensure_region(region)
            ds_id = self._ensure_dataset(region, "_unknown")
            info = submitted_info or {}
            # expression 是 NOT NULL：平台同步时 code 可能缺失（列表端点精简返回），
            # 用空串占位；后续 upsert_alpha_from_platform 带 code 时会覆盖。
            cur.execute(
                "INSERT OR IGNORE INTO alphas (alpha_id, expression, region_id, dataset_id, "
                "status, platform_status, stage, alpha_type, date_submitted, created_at, updated_at) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (alpha_id, info.get("expression") or "", rid, ds_id,
                 info.get("status") or "COMPLETE",
                 info.get("platform_status") or "ACTIVE", info.get("stage") or "OS",
                 info.get("alpha_type"), info.get("date_submitted"), now, now),
            )
            if not cur.rowcount:
                cur.execute("SELECT id FROM alphas WHERE alpha_id=?", (alpha_id,))
                r2 = cur.fetchone()
                if not r2:
                    return {"skipped": "insert_failed", "alpha_id": alpha_id}
                target_id = int(r2[0])
            else:
                target_id = int(cur.lastrowid)
            # 骨架行刚建，os 列全空，直接写
            sets = ", ".join(f"{k}=?" for k in mapping)
            cur.execute(f"UPDATE alphas SET {sets}, os_synced_at=? WHERE id=?",
                        list(mapping.values()) + [now, target_id])
            self.connection.commit()
            return {"action": "inserted_skeleton", "alpha_id": alpha_id,
                    "has_metrics": has_metrics}

        if not overwrite:
            # 只填 NULL 列
            existing = self.connection.execute(
                "SELECT " + ", ".join(metric_cols.keys()) + " FROM alphas WHERE id=?",
                (target_id,),
            ).fetchone()
            updates = {k: v for i, (k, v) in enumerate(metric_cols.items())
                       if v is not None and existing[i] is None}
        else:
            updates = {k: v for k, v in metric_cols.items() if v is not None}

        if not has_metrics:
            # 平台还没给指标（近期提交常见）：记下 OS 窗口起点 + 同步时间即可
            cur.execute(
                "UPDATE alphas SET os_start_date=COALESCE(os_start_date, ?), "
                "os_synced_at=?, updated_at=? WHERE id=?",
                (start_date, now, now, target_id),
            )
            self.connection.commit()
            return {"action": "start_date_only", "skipped": "no_metrics",
                    "alpha_id": alpha_id, "os_start_date": start_date}

        if not updates:
            return {"action": "no_change", "alpha_id": alpha_id}

        sets = ", ".join(f"{k}=?" for k in updates)
        vals = list(updates.values())
        if start_date is not None:
            sets += ", os_start_date=COALESCE(os_start_date, ?)"
            vals.append(start_date)
        cur.execute(f"UPDATE alphas SET {sets}, os_synced_at=?, updated_at=? WHERE id=?",
                    vals + [now, now, target_id])
        self.connection.commit()
        return {"action": "updated", "alpha_id": alpha_id,
                "fields": sorted(updates.keys()), "has_metrics": has_metrics}

    def os_decay_baseline(self, region: Optional[str] = None) -> Dict[str, Any]:
        """OS 衰减基线统计（供 KB / 步 7 IS 阈值校准消费）。

        口径：只统计 os_sharpe 非空的行（有真实 OS 样本）。
        """
        cur = self.connection.cursor()
        sql = ("SELECT COUNT(*) n, AVG(a.sharpe) is_sh, AVG(a.os_sharpe) os_sh, "
               "AVG(a.os_is_sharpe_ratio) ratio, "
               "SUM(CASE WHEN a.os_sharpe > 1.58 THEN 1 ELSE 0 END) above_gate, "
               "SUM(CASE WHEN a.os_sharpe > 1.0 THEN 1 ELSE 0 END) above_one, "
               "SUM(CASE WHEN a.os_sharpe <= 0 THEN 1 ELSE 0 END) nonpos "
               "FROM alphas a JOIN regions r ON a.region_id = r.id "
               "WHERE a.os_sharpe IS NOT NULL")
        params: List[Any] = []
        if region:
            sql += " AND r.name=?"
            params.append(region)
        cur.execute(sql, params)
        row = cur.fetchone()
        if row is None:
            return {"n": 0, "note": "无 OS 样本（先跑 sync_platform_alphas 同步）"}
        n = int(row[0] or 0)
        if not n:
            return {"n": 0, "note": "无 OS 样本（先跑 sync_platform_alphas 同步）"}
        return {
            "n": n,
            "is_sharpe_mean": round(float(row[1] or 0), 4),
            "os_sharpe_mean": round(float(row[2] or 0), 4),
            "os_is_sharpe_ratio_mean": round(float(row[3] or 0), 4),
            "above_gate_1_58": int(row[4] or 0),
            "above_one": int(row[5] or 0),
            "non_positive": int(row[6] or 0),
            "non_positive_pct": round(int(row[6] or 0) / n * 100, 2),
        }
