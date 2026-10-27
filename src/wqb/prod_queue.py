"""prod correlation 串行队列（2026-10-26 新增）。

## 为什么需要

BRAIN 的 production correlation 是 **账号级单并发**：同一时刻只允许 1 个在飞计算。
本仓的查询散落在多个进程（MCP 服务、战役 pipeline、一次性脚本），
即使有跨进程锁（``wqb.correlation_slot``），**并发触发本身**仍会互相把对方顶成
``correlation_busy``，表现为"明明加了锁还是一直锁着"。

本模块提供最小落盘队列：把"待查 prod 的 alpha"登记下来，**串行取用**，
配合锁即形成"一次只触发一个、算完再取下一个"的节流。

## 用法

```python
from wqb.prod_queue import push, next_pending, mark, stats

push("abc123")                  # 登记（幂等）
aid = next_pending()            # 取一个待处理的；None = 队列空
if aid:
    r = ...                     # 查 prod（走 correlation_slot 锁）
    mark(aid, max_corr=r.get('max'), status='done')   # 写回
```

## 状态语义

- ``pending``         待处理
- ``done``            已拿到数值
- ``pending_timeout`` 超时（平台仍在算），下次可选重试
- ``error``           取数报错

## 存储

``cache/prod_queue.json``（运行期产物，gitignore）。原子写（tmp + os.replace）。
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Iterable, List, Optional

#: 队列文件相对仓库根的路径（调用方通常在仓库根运行，故用相对 ``cache/``）。
QUEUE_REL = os.path.join("cache", "prod_queue.json")

#: 单次取用后，同一条目的最长豁免期（秒）。超过则可被重复取用（避免卡死一条）。
LEASE_SEC = 900.0

#: 完成的条目保留天数（防文件无限增长）。
KEEP_DAYS = 14


def queue_path() -> str:
    """队列文件绝对路径。

    优先 ``WQB_PROD_QUEUE_PATH`` 环境变量；否则用仓库根下 ``cache/prod_queue.json``
    （以本文件 ``src/wqb/`` 上溯两级定位仓库根）。
    """
    env = os.environ.get("WQB_PROD_QUEUE_PATH")
    if env:
        return env
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(root, QUEUE_REL)


def _load() -> Dict[str, Any]:
    p = queue_path()
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        if not isinstance(d, dict):
            return {"items": {}}
        d.setdefault("items", {})
        if not isinstance(d["items"], dict):
            d["items"] = {}
        return d
    except Exception:
        return {"items": {}}


def _save(d: Dict[str, Any]) -> None:
    """原子写：tmp + os.replace（防中断损坏）。"""
    p = queue_path()
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    d["updated"] = time.time()
    # 清理过期已完成项
    cutoff = time.time() - KEEP_DAYS * 86400
    items = d.get("items") or {}
    for k in [
        k for k, v in items.items()
        if (v.get("status") in ("done", "error")) and (v.get("ts") or 0) < cutoff
    ]:
        items.pop(k, None)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, p)


def push(alpha_id: str, note: str = "") -> Dict[str, Any]:
    """登记一个待查 prod 的 alpha（幂等：已存在且未完成则只刷新时间戳）。"""
    d = _load()
    items = d["items"]
    cur = items.get(alpha_id) or {}
    if cur.get("status") == "done":
        return cur
    cur.update({
        "status": "pending",
        "ts": time.time(),
        "tries": int(cur.get("tries") or 0),
        "note": note or cur.get("note") or "",
    })
    items[alpha_id] = cur
    _save(d)
    return cur


def push_many(alpha_ids: Iterable[str], note: str = "") -> int:
    n = 0
    for a in alpha_ids:
        if a:
            push(str(a), note=note)
            n += 1
    return n


def next_pending() -> Optional[str]:
    """取一个待处理条目（最久未尝试者优先；租约过期可重取）。返回 None 表示队列空。"""
    d = _load()
    now = time.time()
    cands: List[Any] = []
    for aid, v in (d.get("items") or {}).items():
        st = v.get("status")
        if st not in ("pending", "pending_timeout"):
            continue
        last = float(v.get("lease_ts") or v.get("ts") or 0)
        if now - last < LEASE_SEC and v.get("lease_ts"):
            continue          # 仍在租约内，跳过
        cands.append((last, aid))
    if not cands:
        return None
    cands.sort()
    aid = cands[0][1]
    d["items"][aid]["lease_ts"] = now
    _save(d)
    return aid


def mark(alpha_id: str, max_corr: Optional[float] = None,
         status: str = "done", error: str = "") -> Dict[str, Any]:
    """写回结果。``status`` ∈ {done, pending_timeout, error}。"""
    d = _load()
    items = d["items"]
    cur = items.get(alpha_id) or {}
    cur["status"] = status
    cur["ts"] = time.time()
    cur["tries"] = int(cur.get("tries") or 0) + 1
    cur.pop("lease_ts", None)
    if max_corr is not None:
        try:
            cur["max"] = float(max_corr)
        except (TypeError, ValueError):
            pass
    if error:
        cur["error"] = str(error)[:200]
    items[alpha_id] = cur
    _save(d)
    return cur


def stats() -> Dict[str, Any]:
    """队列概况（按状态计数 + 待处理列表）。"""
    d = _load()
    items = d.get("items") or {}
    by: Dict[str, int] = {}
    pend: List[str] = []
    for aid, v in items.items():
        st = str(v.get("status") or "unknown")
        by[st] = by.get(st, 0) + 1
        if st in ("pending", "pending_timeout"):
            pend.append(aid)
    return {
        "total": len(items),
        "by_status": by,
        "pending": sorted(pend),
        "updated": d.get("updated"),
        "path": queue_path(),
    }


def clear(done_only: bool = True) -> int:
    """清队列。``done_only=True`` 只清已完成项；否则清空。"""
    d = _load()
    items = d.get("items") or {}
    before = len(items)
    if done_only:
        for k in [k for k, v in items.items() if v.get("status") == "done"]:
            items.pop(k, None)
    else:
        items.clear()
    d["items"] = items
    _save(d)
    return before - len(items)
