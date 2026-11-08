"""prod correlation 串行队列（2026-10-26 新增）。

## 为什么需要

BRAIN 的 production correlation 是 **账号级单并发**：同一时刻只允许 1 个在飞计算。
本仓的查询散落在多个进程（MCP 服务、战役 pipeline、一次性脚本），
即使有跨进程锁（``wqb.correlation_slot``），**并发触发本身**仍会互相把对方顶成
``correlation_busy``，表现为"明明加了锁还是一直锁着"。

本模块提供最小落盘队列：把"待查 prod 的 alpha"登记下来，**串行取用**，
配合锁即形成"一次只触发一个、算完再取下一个"的节流。

## 族代表串行与优先级（2026-11-04）

账号槽一次计算 ≈ 200s ⇒ 吞吐上限 ~17 alpha/小时。省时间的根本是**少触发计算**：

- **族代表串行**：同 ``family`` 标签的成员，队列只放行**最早入队的那颗**（代表），
  其余挂起（``held``），代表出结果（``done``/``error``）后自动解除、下一颗顶上。
  动机：代表 prod 已 ≥0.7 时整族大概率同死（window-valley 直方图判族法），
  没必要把账号槽烧在注定失败的兄弟颗上；而代表干净时，兄弟颗照常逐颗实测。
  消费侧（``corr_check.py --run-queue``）会在代表出值时打印族提示，
  ``--family-cull`` 可选地自动把兄弟颗标 error（默认关，防误埋可救候选）。
- **优先级**：``priority`` 数值大的先消费（跨族排序键；如 ATOM 候选优先）。
  无 ``family`` 的条目自成一组，行为与旧版完全一致（键 = 自身 id）。

## 用法

```python
from wqb.prod_queue import push, next_pending, mark, stats

push("abc123")                  # 登记（幂等）
push("def456", family="ds17:skel3", priority=5)   # 族代表 + 高优先级
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


def push(alpha_id: str, note: str = "", force: bool = False,
         family: str = None, priority: float = None) -> Dict[str, Any]:
    """登记一个待查 prod 的 alpha（幂等：已存在且未完成则只刷新时间戳）。

    ``force=True``：已完成的条目也重新置回 ``pending``（重查用，2026-10-28）。
    ``family`` / ``priority``：族标签与优先级（2026-11-04）。重登记时**不传则保留
    旧值**（与 ``note`` 同语义）——重复 enqueue 同一颗不应抹掉它的族归属。
    """
    d = _load()
    items = d["items"]
    cur = items.get(alpha_id) or {}
    if cur.get("status") == "done" and not force:
        return cur
    cur.update({
        "status": "pending",
        "ts": time.time(),
        "tries": int(cur.get("tries") or 0),
        "note": note or cur.get("note") or "",
    })
    if family:
        cur["family"] = str(family)
    if priority is not None:
        cur["priority"] = float(priority)
    items[alpha_id] = cur
    _save(d)
    return cur


def get(alpha_id: str) -> Dict[str, Any]:
    """读单个条目（不存在 → ``{}``）。只读，不取租约。"""
    return dict((_load().get("items") or {}).get(alpha_id) or {})


def items() -> Dict[str, Dict[str, Any]]:
    """队列全部条目的快照（只读）。"""
    return {k: dict(v or {}) for k, v in (_load().get("items") or {}).items()}


def push_many(alpha_ids: Iterable[str], note: str = "",
              family: str = None, priority: float = None) -> int:
    n = 0
    for a in alpha_ids:
        if a:
            push(str(a), note=note, family=family, priority=priority)
            n += 1
    return n


def family_holds() -> Dict[str, List[str]]:
    """族持有表：``{代表id: [被持有的同族兄弟id]}``（仅活跃条目）。

    代表 = 该族内 ``ts`` 最早（最久先入队）的活跃成员；其余活跃成员视为被持有。
    代表 done/error 后自愈——下一轮该族的代表自然换人，无需手工干预。
    """
    d = _load()
    now = time.time()
    active: List[Any] = []
    for aid, v in (d.get("items") or {}).items():
        if v.get("status") not in ("pending", "pending_timeout"):
            continue
        active.append((str(v.get("family") or "") or aid, aid,
                       float(v.get("ts") or 0)))
    groups: Dict[str, List[Any]] = {}
    for fam, aid, ts in active:
        groups.setdefault(fam, []).append((ts, aid))
    holds: Dict[str, List[str]] = {}
    for fam, members in groups.items():
        members.sort()
        rep = members[0][1]
        held = sorted(a for _, a in members[1:])
        if held:
            holds[rep] = held
    return holds


def next_pending() -> Optional[str]:
    """取一个待处理条目（2026-11-04 起带族代表串行与优先级）。

    规则：
    1. **族分组**：按 ``family`` 分组（无 family 的条目自成一组，键 = 自身 id），
       每组只放行**代表**（组内 ``ts`` 最早的活跃成员），兄弟被持有不取——
       同族相关性同源，代表没定论前查兄弟大概率白烧一个 240s 窗口。
    2. **代表自愈**：代表 done/error 后即退出活跃集，下一轮组内剩余成员里
       ts 最早的自动接任代表，无需任何干预。
    3. **优先级**：跨族排序键 ``(-priority, ts, aid)``——priority 大者先（如
       ATOM 候选插队），同优先级仍是最久先入队者优先。
    4. **租约**：代表的租约未过期则整组跳过（租约过期可重取，防卡死）。
    返回 None 表示没有可取条目。
    """
    d = _load()
    now = time.time()
    active: List[Any] = []
    for aid, v in (d.get("items") or {}).items():
        st = v.get("status")
        if st not in ("pending", "pending_timeout"):
            continue
        last = float(v.get("lease_ts") or v.get("ts") or 0)
        leased = bool(v.get("lease_ts")) and now - last < LEASE_SEC
        active.append((str(v.get("family") or "") or aid, aid,
                       float(v.get("ts") or 0), leased,
                       float(v.get("priority") or 0.0)))
    # 族 → 代表（组内 ts 最早者）；代表已持有效租约则整组本轮不可取。
    groups: Dict[str, Any] = {}
    for fam, aid, ts, leased, pri in active:
        groups.setdefault(fam, []).append((ts, aid, leased, pri))
    cands: List[Any] = []
    for fam, members in groups.items():
        members.sort(key=lambda m: (m[0], m[1]))
        ts, aid, leased, pri = members[0]
        if leased:
            continue
        cands.append((-pri, ts, aid))
    if not cands:
        return None
    cands.sort()
    aid = cands[0][2]
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
        "held": family_holds(),
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
