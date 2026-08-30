# -*- coding: utf-8 -*-
"""ExpressionsMixin: expression CRUD for CampaignStore."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from ._common import ExprItem, _as_expr, _dumps, _loads, _now


class ExpressionsMixin:
    """Expression upsert/list/history methods."""

    def upsert_expressions(
        self,
        region: str,
        wave: str,
        items: Sequence[ExprItem],
        dataset: Optional[str] = None,
        status: str = "pending",
    ) -> Dict[str, Any]:
        wave_id = self._ensure_wave(region, str(wave), dataset)
        now = _now()
        n = 0
        cur = self.connection.cursor()
        # 冗余列 region/wave/dataset 必须从 wave_id 关联派生，避免与父表（waves→regions/datasets）漂移
        cur.execute(
            "SELECT r.name, w.wave_number, d.name FROM waves w "
            "JOIN regions r ON r.id=w.region_id "
            "LEFT JOIN datasets d ON d.id=w.dataset_id WHERE w.id=?",
            (wave_id,),
        )
        _wr = cur.fetchone()
        resolved_region = _wr["name"] if _wr else region
        resolved_wave = str(_wr["wave_number"]) if _wr else str(wave)
        resolved_dataset = _wr["name"] if _wr and _wr["name"] else (dataset or None)
        for raw in items:
            item = _as_expr(raw)
            expr = (item.get("expression") or "").strip()
            if not expr:
                continue
            st = item.get("status") or status
            settings = item.get("settings") or item.get("settings_json")
            settings_json = _dumps(settings) if isinstance(settings, (dict, list)) else settings
            cur.execute(
                "SELECT id FROM expressions WHERE wave_id=? AND expression=?",
                (wave_id, expr),
            )
            row = cur.fetchone()
            vals = (
                item.get("fingerprint"),
                st,
                item.get("alpha_id"),
                item.get("sharpe"),
                item.get("fitness"),
                item.get("margin"),
                item.get("turnover"),
                resolved_region,
                resolved_wave,
                resolved_dataset,
                settings_json,
                now,
            )
            if row:
                cur.execute(
                    """UPDATE expressions SET fingerprint=?, status=?, alpha_id=?,
                       sharpe=?, fitness=?, margin=?, turnover=?, region=?, wave=?,
                       dataset=?, settings_json=?, updated_at=? WHERE id=?""",
                    vals + (int(row[0]),),
                )
            else:
                cur.execute(
                    """INSERT INTO expressions
                       (wave_id, expression, fingerprint, status, alpha_id, sharpe,
                        fitness, margin, turnover, region, wave, dataset,
                        settings_json, created_at, updated_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (wave_id, expr) + vals + (now,),
                )
            n += 1
        cur.execute(
            "UPDATE waves SET expression_count=?, updated_at=? WHERE id=?",
            (n, now, wave_id),
        )
        self.connection.commit()
        return {"n": n, "region": region, "wave": str(wave), "dataset": dataset}

    def list_expressions(
        self,
        region: str,
        wave: str,
        dataset: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM expressions WHERE region=? AND wave=?"
        params: List[Any] = [region, str(wave)]
        if dataset:
            sql += " AND (dataset=? OR dataset IS NULL)"
            params.append(dataset)
        if status:
            sql += " AND status=?"
            params.append(status)
        sql += " ORDER BY id"
        cur = self.connection.cursor()
        cur.execute(sql, params)
        out = []
        for row in cur.fetchall():
            d = dict(row)
            if d.get("settings_json"):
                d["settings"] = _loads(d["settings_json"])
            out.append(d)
        if out:
            return out
        # fallback: old rows without denormalized region/wave
        rid = None
        cur.execute("SELECT id FROM regions WHERE name=?", (region,))
        r = cur.fetchone()
        if not r:
            return []
        rid = int(r[0])
        cur.execute(
            "SELECT id FROM waves WHERE region_id=? AND wave_number=?",
            (rid, str(wave)),
        )
        w = cur.fetchone()
        if not w:
            return []
        cur.execute(
            "SELECT * FROM expressions WHERE wave_id=? ORDER BY id",
            (int(w[0]),),
        )
        return [dict(row) for row in cur.fetchall()]

    def history_expressions(self, region: str, exclude_waves: Optional[Sequence[str]] = None) -> List[str]:
        cur = self.connection.cursor()
        cur.execute(
            "SELECT expression, wave, status FROM expressions WHERE region=?",
            (region,),
        )
        skip = {str(w) for w in (exclude_waves or [])}
        skip_status = {"gem", "raw"}
        out = []
        for r in cur.fetchall():
            if r[1] and str(r[1]) in skip:
                continue
            if (r[2] or "") in skip_status:
                continue
            if r[0]:
                out.append(r[0])
        return out

    save_wave_expressions = upsert_expressions
    load_wave_expressions = list_expressions
