# -*- coding: utf-8 -*-
"""ExpressionsMixin: expression CRUD for CampaignStore."""
from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List, Optional, Sequence

from ._common import ExprItem, _as_expr, _dumps, _loads, _now


def expression_fingerprint(expr: str) -> str:
    """表达式规范指纹：去空白 + 小写后取 sha1 前 12 位。

    2026-09-06：此前 fingerprint 完全依赖调用方传入，而绝大多数调用方不传 ——
    实测 9 924 行里 3 059 行（30.8%）为 NULL，KOR 单区就有 1 008 行。任何按
    fingerprint 做的去重/查重都会静默漏掉这三成，全库重复表达式 1 833 行（18.5%）。

    归一化口径对齐 toolkit `_lib/common.py:norm_expr`（去全部空白），另加小写，
    使 `rank(Close)` 与 `rank( close )` 同指纹。取 12 位与库中既有指纹等宽。
    """
    normalized = re.sub(r"\s+", "", expr or "").lower()
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:12]


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
                # 调用方没给就现算，杜绝 NULL 指纹（去重全靠它）
                item.get("fingerprint") or expression_fingerprint(expr),
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
        else:
            # 默认排除 superseded（2026-09-01：表达式更新留档态不参与选波/回测）
            sql += " AND status != 'superseded'"
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

    def history_expressions(
        self,
        region: str,
        exclude_waves: Optional[Sequence[str]] = None,
        include_generated: bool = True,
    ) -> List[str]:
        """本区已出现过的表达式，供 build_wave 做全历史去重。

        2026-09-06：原实现无条件排除 `status in ('gem','raw')`。那是个过宽的钝器 ——
        它想解决的是"别把本波自己的输入过滤掉"，而这件事 `exclude_waves`
        （当前波 + `s2_<dataset>_d<delay>` 源波）已经精确解决了。按状态全局排除的
        代价是：**其他波次**生成过的表达式对去重完全隐形，同一条可以一波一波重复生成。

        实测：1 681 条 gem/raw 行里有 759 条与本区其他行重复（EUR 350 / IND 213 /
        KOR 182），正是全库 18.5% 重复率的主要来源之一。

        `include_generated=False` 可回到旧行为（应急逃生用，会重新放大重复）。
        """
        cur = self.connection.cursor()
        cur.execute(
            "SELECT expression, wave, status FROM expressions WHERE region=?",
            (region,),
        )
        skip = {str(w) for w in (exclude_waves or [])}
        skip_status = set() if include_generated else {"gem", "raw"}
        out = []
        for r in cur.fetchall():
            if r[1] and str(r[1]) in skip:
                continue
            if skip_status and (r[2] or "") in skip_status:
                continue
            if r[0]:
                out.append(r[0])
        return out

    save_wave_expressions = upsert_expressions
    load_wave_expressions = list_expressions
