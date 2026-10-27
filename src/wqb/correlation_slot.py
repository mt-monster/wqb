# -*- coding: utf-8 -*-
"""correlation_slot — 平台 prod 相关性「账号级单并发槽」的跨进程互斥（2026-10-22）。

背景（实测 bug，2026-10-22）
----------------------------
平台 ``GET /alphas/{id}/correlations/prod`` 是**每账号仅 1 个在飞**的接口：账号里
任何进程在查 prod，其它进程拿到的都是**空体**（= 仍在算）。本仓的相关性查询散落在
**多个进程**：MCP 常驻服务（``brain_mixin_*``）、``tools/campaign_intel.py prod-first``、
``tools/probe/prod_bucket_scan.py``、``tools/super_build.py``（SUPER 提交闸）、
``tools/pool-hygiene/prod_watch.py``、各类一次性脚本。它们**各自**新建
``BrainApiClient`` ⇒ 进程内 asyncio 锁互不相识。

于是本次事故的链条是（实测，非推演）：
  1. 另一个会话的 prod 队列脚本卡在某个目标上（``58jgRYWX``），
  2. 它对平台的请求一直没结束 ⇒ **账号的单并发槽被占住**，
  3. 本会话的查询全部拿空体，空转到 800s+ 仍无结果（``vROYv3EA`` 实测 1499s 才出数），
  4. 杀掉那个作业后，本会话同一条立刻出数。

修复要点（两处，缺一不可）
--------------------------
1. **跨进程互斥**：槽位由**文件 token**（``logs/_dblock/correlation.lock.json``）守护，
   拿不到就**立即返回 busy**（fail-fast），不排队、不降级放行——降级放行等于让第二个
   进程也去打这个单并发接口，正是事故形态。token 用 ``O_CREAT|O_EXCL`` 原子创建，
   带 TTL 自愈 + 死持有者按 pid 回收 + ``.stale`` 退役（复用 ``wqb.db_write_lock``）。
2. **缩短占槽窗口**：单次轮询窗口从 3600 s 降到 900 s（``WAIT_THRESHOLDS``
   ``prod_corr_timeout_s``）——一个卡住的 alpha 占槽 60 分钟会把整账号的相关性查询
   堵死一小时。超时按 ``pending`` 返回（不缓存、不判死），调用方隔段时间重查。

⚠ **同 pid 重入的语义**：``db_write_lock`` 把「同 pid 再 acquire」当**续约**。
所以**同一进程内的并发互斥不能靠本模块**——那要用进程内 ``asyncio.Lock``
（MCP 侧见 ``brain_mixin_transport._try_acquire_brain_correlation_lock``，
它**先**拿进程内锁、**后**拿本模块的跨进程锁，顺序不可换）。

用法::

    from wqb.correlation_slot import slot

    with slot("prod:alpha123", ttl_sec=900) as s:
        if not s["acquired"]:
            return "busy"          # 另一进程/协程正占着账号槽
        ...                          # 平台查询（≤ ttl_sec）
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Dict, Iterator

from wqb.db_write_lock import acquire as _flock_acquire
from wqb.db_write_lock import lock_dir as _flock_dir
from wqb.db_write_lock import release as _flock_release

#: token 文件名。与写库锁（``dbwrite.lock.json``）**分开**：两种锁 TTL 不同，
#: 共用一个文件会让短 TTL 的写锁回收长 TTL 的相关性锁 token（两个进程同时自认持有）。
LOCK_NAME = "correlation.lock.json"

#: 默认 TTL（秒）。必须 ≥ 单次平台轮询窗口，否则长轮询期间 token 被 TTL 自愈回收
#: ⇒ 第二个进程以为拿到槽、实际并发打平台（本次要修的 bug 的反面）。
#:
#: 2026-10-26：3700 → 600。配套把轮询窗口 900 → 120（见 ``WAIT_THRESHOLDS``）。
#: 旧值 3700 的问题：进程崩溃/卡住时锁残留 62 分钟才自愈，期间全账号 correlation 不可用。
#: 现 600s = 5×轮询窗口（120s），足够覆盖单次轮询 + 平台收尾，崩溃残留降到 10 分钟。
#: ⚠ 调整时**必须同步** ``WAIT_THRESHOLDS["prod_corr_timeout_s"]``，保持 TTL ≥ 5×窗口。
DEFAULT_TTL_SEC = 600.0


def slot_path() -> str:
    """token 文件绝对路径（``<lock_dir>/correlation.lock.json``）。"""
    return os.path.join(_flock_dir(), LOCK_NAME)


# ---------------------------------------------------------------------------
# 冷却窗口（2026-10-26 新增）
# ---------------------------------------------------------------------------
# 实测缺口：本模块只做「跨进程互斥」，**拿到结果后立即 release**；
# 但平台侧的账号级槽位在计算结束后仍要再占 ``retry_after=180s``。
# 于是下一个进程（或同一进程的下一次调用）**本地锁一拿到手，就撞平台 correlation_busy**
# —— 表现就是「明明加了锁，多会话还是锁着」。
#
# ⇒ 在 release 时留下一个冷却标记，acquire 先检查它。
#   冷却时长默认 195s（略大于平台 retry_after=180），可用环境变量覆盖。
COOLDOWN_SEC_DEFAULT = 195.0
COOLDOWN_NAME = "correlation.cooldown.json"


def cooldown_path() -> str:
    return os.path.join(_flock_dir(), COOLDOWN_NAME)


def _cooldown_sec() -> float:
    try:
        return float(os.environ.get("WQB_CORR_COOLDOWN_SEC", COOLDOWN_SEC_DEFAULT))
    except (TypeError, ValueError):
        return COOLDOWN_SEC_DEFAULT


def cooldown_remaining() -> float:
    """距冷却结束还剩多少秒；≤0 表示已可抢槽。"""
    import json
    import time
    p = cooldown_path()
    try:
        with open(p, encoding="utf-8") as f:
            until = float(json.load(f).get("until") or 0)
    except Exception:
        return 0.0
    return max(0.0, until - time.time())


def _write_cooldown() -> None:
    import json
    import time
    p = cooldown_path()
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"until": time.time() + _cooldown_sec(),
                       "pid": os.getpid(),
                       "at": time.strftime("%F %T")}, f)
        os.replace(tmp, p)
    except Exception:
        pass


def acquire(op_name: str, ttl_sec: float = DEFAULT_TTL_SEC) -> Dict[str, object]:
    """抢账号级相关性槽。**fail-fast**：被他人持有时立即返回 ``busy``。

    Returns:
        ``{"acquired": bool, "busy": bool, "token": path|None, "degraded": bool}``
        - ``acquired=False, busy=True`` ⇒ 他人持有（**不放行**，调用方应稍后重试）
        - ``degraded=True`` ⇒ 锁目录不可写等异常 → 无法承担跨进程互斥，
          此时 ``acquired=True``（降级放行，与 ``db_write_lock`` 的既有降级语义一致）
    """
    # 0) 冷却窗口：上一次调用刚结束，平台槽位还没释放 ⇒ 直接 busy，不去撞平台
    _cd = cooldown_remaining()
    if _cd > 0:
        return {
            "acquired": False,
            "busy": True,
            "cooldown": True,
            "retry_after": round(_cd, 1),
            "token": None,
            "degraded": False,
        }

    info = _flock_acquire(
        tag=f"corr:{op_name}",
        ttl_sec=float(ttl_sec),
        wait_timeout=0.0,
        name=LOCK_NAME,
        fail_fast=True,
    )
    return {
        "acquired": bool(info.get("ok")),
        "busy": bool(info.get("busy")),
        "token": info.get("token"),
        "degraded": bool(info.get("degraded")),
    }


def release(token) -> None:
    """释放槽（幂等；仅当持有者是本进程时才退役，防误删他人 token）。

    ★ 2026-10-26：释放后**写冷却标记**——平台在该次计算结束后仍会占槽 ~180s，
    本地若立刻放行下一个调用者，它必然撞 ``correlation_busy``。
    """
    if token:
        _flock_release(token)
    _write_cooldown()


@contextmanager
def slot(op_name: str, ttl_sec: float = DEFAULT_TTL_SEC) -> Iterator[Dict[str, object]]:
    """账号级相关性槽上下文管理器。

    ``with slot(...) as s:`` —— ``s["acquired"]`` 为 ``False`` 表示槽被他人占用，
    **调用方必须自己处理**（不要继续打平台）。
    """
    info = acquire(op_name, ttl_sec=ttl_sec)
    try:
        yield info
    finally:
        release(info.get("token"))
