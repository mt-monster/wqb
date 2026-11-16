# -*- coding: utf-8 -*-
"""KnowledgeMixin: 逐条回测经验索引（attempt_knowledge）的读写。

设计边界（2026-11-15）：
- 本表**只存派生解释**（骨架 / 主墙 / 失败类别 / outcome / 知识版本）；
  指标与表达式的事实源仍是 `backtest_results` / `expressions`。
- 唯一写入方是 `wqb.knowledge.capture.refresh_attempt_knowledge`（经本 mixin），
  两条收批路径（pipeline stage_review / MCP harvest_multisim_results）都只调它；
  因此本表可随时由 `tools/knowledge/rebuild.py` 幂等重建。
- 合并式写入：行里没带的列不覆盖已有值（同 `_backtest.py` 的 N35 纪律）。
  `created_at` 取回测行时间（rebuild 会纠正历史回填的插入时间）；`updated_at` 每次刷新。
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Sequence

from ._common import _dumps, _now

#: 可由 capture 写入的列（顺序稳定，便于测试与 diff）
KNOWLEDGE_COLUMNS = (
    "attempt_id",
    "alpha_id",
    "expression_id",
    "region",
    "wave",
    "dataset",
    "expression",
    "skeleton",
    "family",
    "mechanism",
    "source",
    "expected_exposure",
    "settings_json",
    "metrics_json",
    "walls_json",
    "primary_wall",
    "failure_class",
    "is_structural",
    "ra_failed_json",
    "checks_json",
    "outcome",
    "next_action",
    "priors_sha",
    "rules_sha",
    "knowledge_version",
    "evidence_ref",
    "created_at",
    "updated_at",
)

_JSON_COLUMNS = frozenset({
    "settings_json", "metrics_json", "walls_json", "ra_failed_json", "checks_json",
})


def _decode(row: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(row)
    for col in _JSON_COLUMNS:
        v = out.get(col)
        if isinstance(v, str) and v:
            try:
                out[col] = json.loads(v)
            except Exception:
                pass
    return out


class KnowledgeMixin:
    """attempt_knowledge 的批量合并写与查询。"""

    def upsert_attempt_knowledge(self, rows: Sequence[Dict[str, Any]]) -> int:
        """按 attempt_id 合并式 upsert；返回处理行数。空行/无 id 跳过。"""
        cur = self.connection.cursor()
        now = _now()
        n = 0
        cur.execute("BEGIN")
        try:
            for r in rows:
                if not isinstance(r, dict):
                    continue
                aid = r.get("attempt_id") or r.get("alpha_id")
                if not aid:
                    continue
                # JSON 列统一序列化；None 不写（保留旧值）
                vals: Dict[str, Any] = {}
                for col in KNOWLEDGE_COLUMNS:
                    if col in ("attempt_id", "updated_at"):
                        continue
                    v = r.get(col)
                    if v is None or v == "":
                        continue
                    if col in _JSON_COLUMNS and not isinstance(v, str):
                        v = _dumps(v)
                    vals[col] = v
                vals["attempt_id"] = str(aid)
                vals["updated_at"] = now
                exists = cur.execute(
                    "SELECT 1 FROM attempt_knowledge WHERE attempt_id=?", (str(aid),)
                ).fetchone()
                if exists:
                    sets = ", ".join(f"{k}=?" for k in vals if k != "attempt_id")
                    cur.execute(
                        f"UPDATE attempt_knowledge SET {sets} WHERE attempt_id=?",
                        tuple(v for k, v in vals.items() if k != "attempt_id") + (str(aid),),
                    )
                else:
                    vals["created_at"] = r.get("created_at") or now
                    cols = list(vals)
                    cur.execute(
                        f"INSERT INTO attempt_knowledge ({','.join(cols)}) "
                        f"VALUES ({','.join('?' * len(cols))})",
                        tuple(vals[c] for c in cols),
                    )
                n += 1
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        return n

    def list_attempt_knowledge(
        self,
        region: Optional[str] = None,
        wave: Optional[str] = None,
        dataset: Optional[str] = None,
        family: Optional[str] = None,
        skeleton: Optional[str] = None,
        outcome: Optional[str] = None,
        limit: int = 5000,
    ) -> List[Dict[str, Any]]:
        where, params = [], []
        for col, val in (("region", region), ("wave", wave), ("dataset", dataset),
                         ("family", family), ("skeleton", skeleton), ("outcome", outcome)):
            if val is not None:
                where.append(f"{col}=?")
                params.append(str(val))
        sql = "SELECT * FROM attempt_knowledge"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY wave, attempt_id LIMIT ?"
        params.append(int(limit))
        rows = self.connection.execute(sql, tuple(params)).fetchall()
        return [_decode(dict(r)) for r in rows]

    def get_attempt_knowledge(self, attempt_id: str) -> Optional[Dict[str, Any]]:
        row = self.connection.execute(
            "SELECT * FROM attempt_knowledge WHERE attempt_id=?", (str(attempt_id),)
        ).fetchone()
        return _decode(dict(row)) if row else None
