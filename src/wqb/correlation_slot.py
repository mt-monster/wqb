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
2. **缩短占槽窗口**：单次轮询窗口 3600 → 900 → 120 → **240 s**（``WAIT_THRESHOLDS``
   ``prod_corr_timeout_s``）——窗口长度 = 单次持锁时长，一个卡住的 alpha 会把整账号的
   相关性查询堵住这么久。2026-10-28 从 120 回调到 240：一次**正常**的平台计算
   180–200 s，120s 窗口比它还短 ⇒ 每条真实查询都必然 pending 再叠一轮冷却。
   超时按 ``pending`` 返回（不缓存、不判死），调用方隔段时间重查。

2026-10-28 追加（P0-1 / P0-2）
-----------------------------
3. **冷却按结果分流**：``release(..., cooldown=, seconds=)`` —— 只有「真触发了一次
   计算」才写满 195s；算成功只留 5s 收尾；立即拿到既有值 / 4xx 终态 / 异常不写。
   旧的单参 ``release(token)`` 行为不变（仍 195s）。
4. **在飞 sidecar**：``inflight_mark/get/clear/all`` 记录「某 alpha 正在算」，
   TTL 内同 alpha 的新调用只预读轮询、不二次触发。它不是互斥锁（互斥仍是 token）。

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
#: 2026-10-26：3700 → 600。旧值 3700 的问题：进程崩溃/卡住时锁残留 62 分钟才自愈，
#: 期间全账号 correlation 不可用。
#: **硬要求只有一条：TTL > 单次最长持锁**（换进程后不会自愈回收一个仍在轮询的持有者）。
#: 最长持锁 ≈ 轮询窗口（``prod_corr_timeout_s``）+ 一个慢轮询台阶 30s + 抖动，
#: 2026-10-28 起窗口 240 ⇒ ≈ 270s，600 留 330s 绝对余量（2.2×）。
#: ⚠ 旧注释写的「TTL ≥ 5×窗口」是窗口 120 时凑出 600 的经验式，不是约束本身——
#: 照它办就得把 TTL 抬到 1200（崩溃残留 20 分钟），代价大于收益。
#: 调整窗口时**必须**复核：``DEFAULT_TTL_SEC >= 窗口 + 120``（守护测试
#: ``test_default_ttl_covers_max_single_hold``）。
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
#
# ★ 2026-10-28 P0-1：冷却改为**按结果分流**。旧实现 `release()` 无条件写满 195s，
#   把「平台已算好、一个 GET 就拿到值」与「真触发了一次计算」同等对待——实测 14h
#   日志里 117 次拿槽成功、其中只有部分是真实计算，其余立即返回；冷却却每次都写，
#   吞吐被硬压到 ~4 alpha/小时（195s × 4）。分流规则（证据见
#   ``reports/prod_corr_timing_20261028.md``）：
#     - 真触发计算 → 冷却 = 平台 Retry-After 或 195s；
#     - 计算成功后 → 只留 ``COOLDOWN_SETTLE_SEC``（5s）给平台收尾；
#     - 立即拿到既有值 / 4xx 终态 / 异常 → **不写冷却**（没有占槽理由）。
#   直接 ``release(token)`` 的默认仍是写 195s（向后兼容），MCP 侧显式传结果。
COOLDOWN_SEC_DEFAULT = 195.0
COOLDOWN_NAME = "correlation.cooldown.json"

#: 「算完了」之后留给平台释放账号槽的收尾时间（秒）。实测成功响应后平台仍会
#: 短暂报 busy，5s 足够；可用 ``WQB_CORR_SETTLE_SEC`` 覆盖。
COOLDOWN_SETTLE_SEC = 5.0


def cooldown_path() -> str:
    return os.path.join(_flock_dir(), COOLDOWN_NAME)


def _cooldown_sec() -> float:
    try:
        return float(os.environ.get("WQB_CORR_COOLDOWN_SEC", COOLDOWN_SEC_DEFAULT))
    except (TypeError, ValueError):
        return COOLDOWN_SEC_DEFAULT


def settle_seconds() -> float:
    """计算成功后留给平台释放账号槽的收尾冷却（``WQB_CORR_SETTLE_SEC``）。"""
    try:
        return float(os.environ.get("WQB_CORR_SETTLE_SEC", COOLDOWN_SETTLE_SEC))
    except (TypeError, ValueError):
        return COOLDOWN_SETTLE_SEC


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


def write_cooldown(seconds=None) -> None:
    """写冷却标记。``seconds=None`` 走缺省 195s；``<=0`` 等于清除。"""
    import json
    import time
    sec = _cooldown_sec() if seconds is None else float(seconds)
    if sec <= 0:
        clear_cooldown()
        return
    p = cooldown_path()
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"until": time.time() + sec,
                       "sec": round(sec, 1),
                       "pid": os.getpid(),
                       "at": time.strftime("%F %T")}, f)
        os.replace(tmp, p)
    except Exception:
        pass


def clear_cooldown() -> None:
    """清掉冷却标记（幂等）。"""
    try:
        os.remove(cooldown_path())
    except OSError:
        pass


def _write_cooldown() -> None:  # 历史私有名，保留给既有调用点
    write_cooldown()


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


def release(token, cooldown: bool = True, seconds=None) -> None:
    """释放槽（幂等；仅当持有者是本进程时才退役，防误删他人 token）。

    ★ 2026-10-26：释放后**写冷却标记**——平台在该次计算结束后仍会占槽 ~180s，
    本地若立刻放行下一个调用者，它必然撞 ``correlation_busy``。

    ★ 2026-10-28 P0-1：冷却**按结果分流**。调用方能判断结果时显式传：
      - ``cooldown=False`` ⇒ 不写冷却（立即拿到既有值 / 4xx 终态 / 异常路径）；
      - ``seconds=x`` ⇒ 写 x 秒（触发计算后按平台 Retry-After 或 195s；
        计算成功后用 ``COOLDOWN_SETTLE_SEC``）。
    不传参的旧调用点保持 195s 语义不变。
    """
    if token:
        _flock_release(token)
    if cooldown:
        write_cooldown(seconds)


@contextmanager
def slot(op_name: str, ttl_sec: float = DEFAULT_TTL_SEC,
         cooldown: bool = True, seconds=None) -> Iterator[Dict[str, object]]:
    """账号级相关性槽上下文管理器。

    ``with slot(...) as s:`` —— ``s["acquired"]`` 为 ``False`` 表示槽被他人占用，
    **调用方必须自己处理**（不要继续打平台）。

    调用方可在块内覆写 ``s["write_cooldown"] = False`` / ``s["cooldown_seconds"] = x``
    来按本次结果调整冷却（P0-1 分流）；不覆写则用入参缺省值。
    """
    info = acquire(op_name, ttl_sec=ttl_sec)
    try:
        yield info
    finally:
        # ⚠ 没抢到槽就**不得改写冷却**：旧实现无条件 ``release(None)`` →
        # 每次 busy 轮询都顺手把冷却续期 195s，越查越堵（与 P0-1 同族）。
        # 注意不要写成 ``return`` —— contextmanager 的 finally 里 return 会吞异常。
        if info.get("acquired"):
            use_cd = info.get("write_cooldown", cooldown)
            sec = info.get("cooldown_seconds", seconds)
            release(info.get("token"), cooldown=bool(use_cd), seconds=sec)


# ---------------------------------------------------------------------------
# 在飞标记（2026-10-28 P0-2）
# ---------------------------------------------------------------------------
# 实测缺口：轮询窗口超时后返回 ``pending``（旧窗口 120s 时几乎每条真实计算都会超时），
# 同一 alpha 往往**立刻**被再次触发（21/48 次超时在下一分钟就重新抢锁）。
# 平台侧那一次其实还在算，重触发只是
# 把账号槽继续占住。⇒ 用一个 sidecar 记录「这个 alpha 正在算」，TTL 内同 alpha
# 的新调用**只做预读轮询**，不再二次触发（``get_production_correlation`` 消费）。
#
# 形态：``{"items": {alpha_id: {started_at, expires_at, pid, base_max, n}}}``。
# 单文件、原子替换；过期条目读取时顺手清。**只是提示，不是互斥**——互斥仍由
# 上面的 lock token 承担，侧车丢失不会造成并发打平台。
INFLIGHT_NAME = "correlation.inflight.json"
INFLIGHT_TTL_SEC_DEFAULT = 300.0


def inflight_path() -> str:
    return os.path.join(_flock_dir(), INFLIGHT_NAME)


def _inflight_ttl_sec() -> float:
    try:
        return float(os.environ.get("WQB_CORR_INFLIGHT_TTL_SEC", INFLIGHT_TTL_SEC_DEFAULT))
    except (TypeError, ValueError):
        return INFLIGHT_TTL_SEC_DEFAULT


def _inflight_read() -> Dict[str, dict]:
    import json
    try:
        with open(inflight_path(), encoding="utf-8") as f:
            items = json.load(f).get("items") or {}
    except Exception:
        return {}
    return items if isinstance(items, dict) else {}


def _inflight_write(items: Dict[str, dict]) -> None:
    import json
    p = inflight_path()
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"items": items}, f)
        os.replace(tmp, p)
    except Exception:
        pass


def _inflight_prune(items: Dict[str, dict]) -> Dict[str, dict]:
    import time
    now = time.time()
    out = {}
    for aid, rec in items.items():
        try:
            if float((rec or {}).get("expires_at") or 0) > now:
                out[aid] = rec
        except (TypeError, ValueError):
            continue
    return out


def inflight_all() -> Dict[str, dict]:
    """当前未过期的在飞记录（顺手清理过期项）。"""
    items = _inflight_read()
    alive = _inflight_prune(items)
    if len(alive) != len(items):
        _inflight_write(alive)
    return alive


def inflight_get(alpha_id: str) -> dict:
    """该 alpha 的在飞记录；不存在/已过期 → ``{}``。"""
    return inflight_all().get(str(alpha_id)) or {}


def inflight_mark(alpha_id: str, base_max=None, ttl_sec=None) -> dict:
    """标记该 alpha 正在计算。已存在则只续期并 ``n+1``（保留首次 started_at）。"""
    import time
    aid = str(alpha_id)
    items = _inflight_prune(_inflight_read())
    now = time.time()
    ttl = _inflight_ttl_sec() if ttl_sec is None else float(ttl_sec)
    prev = items.get(aid) or {}
    rec = {
        "started_at": float(prev.get("started_at") or now),
        "expires_at": now + ttl,
        "pid": os.getpid(),
        "base_max": prev.get("base_max") if prev else base_max,
        "n": int(prev.get("n") or 0) + 1,
    }
    items[aid] = rec
    _inflight_write(items)
    return rec


def inflight_clear(alpha_id: str) -> bool:
    """清除该 alpha 的在飞标记；返回是否真的清掉了。"""
    aid = str(alpha_id)
    items = _inflight_read()
    if aid not in items:
        return False
    items.pop(aid, None)
    _inflight_write(items)
    return True


# ---------------------------------------------------------------------------
# 持有者识别（2026-10-28 P1-1 用）
# ---------------------------------------------------------------------------
def holder_tag():
    """读当前 lock token 的 tag（形如 ``corr:get_production_correlation(<aid>)``）。

    无持有者 / 读不到 → ``None``。**只读、不做任何判定**——同一 alpha 的判定
    在调用侧（比对 op_name）。token 可能在他进程手上，读到的是即时快照。
    """
    import json
    try:
        with open(slot_path(), encoding="utf-8") as f:
            tag = json.load(f).get("tag")
    except Exception:
        return None
    return tag if isinstance(tag, str) else None
