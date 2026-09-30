# -*- coding: utf-8 -*-
"""step_events — 步级评估 T2 事件台账（append-only，2026-09-30 方案 B）。

## 定位（与 2026-09-17 下线的 step_metrics 的本质区别）

旧 step_metrics 五张表死于「调用方手传指标值」（编数）+「反事实估算入库」。
本台账只记**客观发生过的事件**（发生了就是发生了，没发生就没有行）：

- `event_type` 必须来自封闭词表 `EVENT_VOCAB`（拒收自由文本）；
- `source` 必填（埋点位置 `文件::函数`，审计可回放），R1 可审计；
- `dedupe_key` 幂等：钩子重复执行（节点重跑/断点续跑）不会重复计数；
- 值语义 = 事件次数/计数，**不接受**"accuracy=0.85" 式评估结论。

T1 推导指标不进本表（见 `step_eval.py`，只读既有表）；T3 反事实估算永不入库。
设计红线见 `tools/step_funnel.py` 头部与 `attic/step_metrics_20260917/README.md`。

## 表结构（唯一新表 step_events，命名不与任何既有物冲突）

    step_events(id, region, wave, step, event_type, value, source,
                dedupe_key, metadata, recorded_at)
    UNIQUE(region, wave, step, event_type, dedupe_key)  -- dedupe_key 为 NULL 时可重复追加
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

from wqb.db_conn import connect as _db_connect  # 规范工厂（禁裸 sqlite3.connect，test_db_write_guards 守护）

#: 封闭事件词表：event_type -> 语义（新增事件类型必须先在此登记）
EVENT_VOCAB: Dict[str, str] = {
    "cache_hit": "S0 calibrate / S2 assemble-priors 缓存命中（复用而非重算）",
    "calibrate_applied": "S0 calibrate 校准实际执行（未命中缓存）",
    "settings_prior_applied": "S3 settings prior 按实测过闸率改写本波 decay/中性化",
    "ghost_blocked": "幽灵算子硬闸拦截（按设计未进批、未烧配额）",
    "gate_blocked_expr": "门禁拦截表达式数（按设计未烧的配额）",
    "batch_error_cascade": "批内 ERROR 连坐/级联事件",
    "batch_cancelled": "整批 CANCELLED 事件",
    "retry_sent": "批次故障协议重发/拆批重试",
    "mode_b_blocked": "Mode B 资格线拦截（未达 sharpe/fitness 资格线判死）",
    "region_kb_refreshed": "波后 region_kb 自动刷新（recent_waves/gate_priors_local）",
    "salvage_collected": "salvage_pool 沉降（seal_dead_end / 收批分层）",
    "prescreen_rejected": "S4 预筛 REJECT 直接判死（不进 S4 评审链）",
}

#: 九步合法 step 名
STEP_NAMES = ("S-PRE", "S0", "S1", "S2", "S2->S3", "S3", "S4", "S4->S5", "S6")

_DDL = """
CREATE TABLE IF NOT EXISTS step_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT NOT NULL,
    wave TEXT,
    step TEXT NOT NULL,
    event_type TEXT NOT NULL,
    value REAL NOT NULL DEFAULT 1,
    source TEXT NOT NULL,
    dedupe_key TEXT,
    metadata TEXT,
    recorded_at TEXT NOT NULL,
    UNIQUE(region, wave, step, event_type, dedupe_key)
)
"""
_INDEX = "CREATE INDEX IF NOT EXISTS idx_step_events_scope ON step_events(region, wave, step)"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ensure_schema(conn: sqlite3.Connection) -> None:
    """幂等建表（仅在首次写事件时调用；读路径缺表按空处理，不建表）。"""
    conn.execute(_DDL)
    conn.execute(_INDEX)
    conn.commit()


def record_event(
    region: str,
    step: str,
    event_type: str,
    *,
    wave: Optional[str] = None,
    value: float = 1.0,
    source: str,
    dedupe_key: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    db_path: Optional[str] = None,
) -> Dict[str, Any]:
    """记录一条客观事件（append-only；带 dedupe_key 时幂等）。

    校验（违反即抛 ValueError，绝不静默收下）：
      - event_type ∈ EVENT_VOCAB（封闭词表）
      - step ∈ STEP_NAMES
      - source 非空（R1：每条事件可审计到埋点位置）
      - value 为有限数（拒绝 NaN/Inf）

    Returns:
        {"recorded": bool, "id": int|None, "reason": str|None}
        reason="duplicate" 表示幂等键命中、未重复计数。
    """
    if event_type not in EVENT_VOCAB:
        raise ValueError(f"event_type 不在封闭词表：{event_type!r}（可用：{sorted(EVENT_VOCAB)}）")
    if step not in STEP_NAMES:
        raise ValueError(f"step 非法：{step!r}（可用：{STEP_NAMES}）")
    if not source or not str(source).strip():
        raise ValueError("source 必填（埋点位置 文件::函数），R1 可审计")
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"value 必须是数值：{value!r}")
    if v != v or v in (float("inf"), float("-inf")):  # NaN / Inf
        raise ValueError(f"value 必须有限：{value!r}")

    if db_path is None:
        from wqb.workflow._common import resolve_db_path
        db_path = resolve_db_path()

    conn = _db_connect(str(db_path), timeout=30.0)
    try:
        ensure_schema(conn)
        params = (
            str(region).upper(), None if wave is None else str(wave), step, event_type,
            v, str(source).strip(), dedupe_key,
            json.dumps(metadata, ensure_ascii=False) if metadata else None, _now(),
        )
        if dedupe_key:
            # 先查后插：SQLite UNIQUE 里 NULL 不互等（wave/dedupe_key 为 NULL 时约束失效），
            # `IS` 匹配可正确处理 NULL；再叠 INSERT OR IGNORE 兼容非空列的原子防重。
            pre = conn.execute(
                "SELECT id FROM step_events WHERE region=? AND wave IS ? "
                "AND step=? AND event_type=? AND dedupe_key IS ?",
                (str(region).upper(), None if wave is None else str(wave),
                 step, event_type, dedupe_key),
            ).fetchone()
            if pre:
                return {"recorded": False, "id": pre[0], "reason": "duplicate"}
            cur = conn.execute(
                "INSERT OR IGNORE INTO step_events"
                "(region, wave, step, event_type, value, source, dedupe_key, metadata, recorded_at)"
                " VALUES (?,?,?,?,?,?,?,?,?)",
                params,
            )
            conn.commit()
            if cur.rowcount == 0:
                return {"recorded": False, "id": None, "reason": "duplicate"}
        else:
            cur = conn.execute(
                "INSERT INTO step_events"
                "(region, wave, step, event_type, value, source, dedupe_key, metadata, recorded_at)"
                " VALUES (?,?,?,?,?,?,?,?,?)",
                params,
            )
            conn.commit()
        return {"recorded": True, "id": cur.lastrowid, "reason": None}
    finally:
        conn.close()


def safe_record_event(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """埋点专用：record_event 的永不抛异常包装。

    事件台账是旁路观察者，记录失败**绝不阻塞**挖掘主流程（只 warning 后吞掉，
    返回 {"recorded": False, "reason": "suppressed:<err>"}）。校验错误（词表/必填）
    同样吞掉——但会留下 warning 日志供事后审计。
    """
    import logging
    try:
        return record_event(*args, **kwargs)
    except Exception as e:  # noqa: BLE001 — 旁路绝不打断主流程
        logging.getLogger(__name__).warning(
            "step_events record suppressed: %s (%r)", e, args[:3])
        return {"recorded": False, "id": None, "reason": f"suppressed:{e}"}


def query_events(
    region: Optional[str] = None,
    wave: Optional[str] = None,
    step: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = 500,
    db_path: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """查询事件（缺表/缺库返回 []，不建表不建库——只读契约）。"""
    if db_path is None:
        from wqb.workflow._common import resolve_db_path
        db_path = resolve_db_path()
    try:
        conn = _db_connect(str(db_path), timeout=30.0,
                           row_factory=sqlite3.Row, readonly=True)
    except sqlite3.OperationalError:
        return []  # 库文件不存在（readonly 不会悄悄建空库）
    try:
        exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='step_events'"
        ).fetchone()
        if not exists:
            return []
        sql = "SELECT * FROM step_events WHERE 1=1"
        params: List[Any] = []
        if region:
            sql += " AND region=?"
            params.append(str(region).upper())
        if wave is not None:
            sql += " AND wave=?"
            params.append(str(wave))
        if step:
            sql += " AND step=?"
            params.append(step)
        if event_type:
            sql += " AND event_type=?"
            params.append(event_type)
        sql += " ORDER BY id DESC LIMIT ?"
        params.append(int(limit))
        rows = conn.execute(sql, params).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            if d.get("metadata"):
                try:
                    d["metadata"] = json.loads(d["metadata"])
                except (json.JSONDecodeError, TypeError):
                    pass
            out.append(d)
        return out
    finally:
        conn.close()


def aggregate(
    region: str,
    wave: Optional[str] = None,
    db_path: Optional[str] = None,
) -> Dict[str, Any]:
    """按 (step, event_type) 聚合事件计数与值合计（供 step_eval 的 T2 指标消费）。"""
    if db_path is None:
        from wqb.workflow._common import resolve_db_path
        db_path = resolve_db_path()
    try:
        conn = _db_connect(str(db_path), timeout=30.0, readonly=True)
    except sqlite3.OperationalError:
        return {}  # 库文件不存在（readonly 不会悄悄建空库）
    try:
        return aggregate_conn(conn, region, wave)
    finally:
        conn.close()


def aggregate_conn(
    conn: sqlite3.Connection,
    region: str,
    wave: Optional[str] = None,
) -> Dict[str, Any]:
    """aggregate 的连接版（供已有连接的调用方复用，避免另开连接）。

    Returns:
        {"<step>": {"<event_type>": {"count": n, "sum": v}}, ...}
    """
    try:
        exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='step_events'"
        ).fetchone()
        if not exists:
            return {}
        sql = ("SELECT step, event_type, COUNT(*), SUM(value) FROM step_events "
               "WHERE region=?")
        params: List[Any] = [str(region).upper()]
        if wave is not None:
            sql += " AND wave=?"
            params.append(str(wave))
        sql += " GROUP BY step, event_type"
        out: Dict[str, Dict[str, Dict[str, Any]]] = {}
        for st, et, n, s in conn.execute(sql, params).fetchall():
            out.setdefault(st, {})[et] = {"count": int(n), "sum": float(s or 0)}
        return out
    except sqlite3.Error:
        return {}
    # 注：不 close —— 连接归调用方所有（aggregate 会自行 close）
