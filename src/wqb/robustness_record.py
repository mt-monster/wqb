# -*- coding: utf-8 -*-
"""wqb.robustness_record — 稳健性结论的台账落点与读取（skills 审查 RB-03 / T0-18）。

背景：`brain-alpha-robustness` 自称「S4→S5 必经闸」，但它的 PASS / CONDITIONAL / REJECT 只写 markdown
与 jsonl，**全仓库没有任何代码读取**——声明存在而实现缺位。现在把结论落到 ledger_kv：

    region = alpha 的区域，key = ``robustness_<alpha_id>``
    value  = {"alpha_id", "verdict": PASS|CONDITIONAL|REJECT, "failed_checks": [...], "soft_flags": [...],
              "checked_at": ISO 时间, "report_path": "tracking/..md"}

写入方 = agent（`mcp__wqb-db__upsert_ledger_key`，见 brain-alpha-robustness Phase D）；
读取方 = :mod:`wqb.submit_verdict_core` 经本模块（CLI / MCP / 批量三入口共用）：
``REJECT`` → 提交判定 BLOCKED（否决权威）；无记录 → 只提示、不拦（旧候选与非 RA 链候选不应被一刀切挡死）。
本模块**只读**，任何异常都返回 None（读不到不能让判定崩溃）。
"""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

KEY_PREFIX = "robustness_"
VERDICTS = ("PASS", "CONDITIONAL", "REJECT")


def key_for(alpha_id: str) -> str:
    return f"{KEY_PREFIX}{alpha_id}"


def normalize_record(raw: Any) -> Optional[Dict[str, Any]]:
    """把台账里读到的值规整成标准记录；verdict 不是枚举值（含大小写以外的写法）→ None。"""
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except ValueError:
            return None
    if not isinstance(raw, dict):
        return None
    verdict = str(raw.get("verdict") or "").strip().upper()
    if verdict not in VERDICTS:
        return None
    failed = raw.get("failed_checks") or []
    soft = raw.get("soft_flags") or []
    return {
        "alpha_id": raw.get("alpha_id"),
        "verdict": verdict,
        "failed_checks": [str(x) for x in failed] if isinstance(failed, (list, tuple)) else [str(failed)],
        "soft_flags": [str(x) for x in soft] if isinstance(soft, (list, tuple)) else [str(soft)],
        "checked_at": raw.get("checked_at"),
        "report_path": raw.get("report_path"),
    }


def read_record(alpha_id: str, region: Optional[str], db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """读 ledger_kv 里的稳健性记录；无记录 / 无库 / 任何异常 → None（只读，绝不写）。"""
    if not alpha_id or not region:
        return None
    try:
        from .db_conn import connect
        from .store._common import default_db_path
        conn = connect(db_path or default_db_path(), readonly=True)
        try:
            cur = conn.execute("SELECT value FROM ledger_kv WHERE region=? AND key=?",
                               (str(region).upper(), key_for(alpha_id)))
            row = cur.fetchone()
        finally:
            conn.close()
        return normalize_record(row[0]) if row else None
    except Exception:  # noqa: BLE001 —— 读不到不能让提交判定崩溃
        return None
