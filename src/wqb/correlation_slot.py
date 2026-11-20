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

2026-11-17 追加（残留锁事故）
---------------------------
5. **冷却标记的脏值自愈**：``cooldown_remaining`` 改为走 ``cooldown_info``——
   半写/非 JSON 的标记、以及 ``until`` 远超 ``max(195s, env)*3`` 的远期值（时钟跳变或
   被手改）一律**退役为 ``.stale`` 并返回 0**，不再让一条脏记录把账号锁几小时。
   ``clear_cooldown`` 同样改为改名退役（``os.replace``），不再 ``unlink``——避开
   沙箱 safe-delete 守卫，且事后可追溯。
6. **``acquire`` 的 busy 分因**：返回值新增 ``reason``（``cooldown`` /
   ``token_busy`` / ``platform_unavailable`` / ``ok`` / ``degraded``）与
   ``holder`` 快照（pid/tag/alive）。此前三者都是 ``busy=True``，调用方只能一律
   fail-closed——``tools/super_build.py`` 的 prod 闸就因此在一个**已知时长**的
   冷却上直接放弃（2026-11-17 实测：提交首跑 attempts=0 退出，人工等 195s 后重跑
   成功）。现在 cooldown 可被等掉，存活持有者仍 fail-fast、不排队。
7. **短持槽不写冷却 + 冷却审计**：``release`` 现在按**持槽时长**自查——持槽 < 60s
   （平台一次真计算要 180–200s，不可能这么快）⇒ 本次只是既有值直读、没占账号槽
   ⇒ **不写 195s 冷却**；同时把每次冷却写入/跳过记进
   ``logs/_dblock/correlation.cooldown.audit.jsonl``（tag / held_s / action）。
   事故来源已定位：``WorkBuddy/Claw`` 面板「自动终验」每 **30 min** 用
   ``wq_prod_backfill.py --alpha <id>`` 查一颗（tag ``prod_backfill(<id>)``），
   单次持槽 21s 却写满 195s ⇒ 账号每 30 min 有 3.25 min 处于伪冷却。

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

#: **持槽时长低于该值 ⇒ 平台根本没跑过新计算**，本次只是「既有值直读」，
#: 不写 195s 冷却（2026-11-17 事故）。
#:
#: 依据：一次真实的 prod/self 计算平台侧要 180–200s（本模块头注释与
#: ``_corr_cache.CORR_FRESH_HOURS`` 同源实测）。若调用方 20s 就拿到值并释放，
#: 只可能是平台**已缓存**的既有值 ⇒ 账号槽没被本次调用占用，此时再挂 195s
#: 冷却纯属自伤——2026-11-17 实测：面板「自动终验」每 30 min 查一颗，单次
#: 持槽 **21s** 却写满 195s，导致账号每 30 min 有 3.25 分钟处于伪冷却，
#: SUPER 提交首跑就撞在这段窗口上。
#:
#: 反向保证：真触发计算的调用**必然会**在槽里等候（≥180s），持槽时长自动过阈值，
#: 冷却照写——阈值只能放过「没算过」的调用，不会放过「算过」的调用。
#: 可用 ``WQB_CORR_MIN_HOLD_FOR_COOLDOWN`` 覆盖。
MIN_HOLD_FOR_COOLDOWN_SEC = 60.0


def min_hold_for_cooldown() -> float:
    """持槽时长的冷却判定阈值（秒），见 :data:`MIN_HOLD_FOR_COOLDOWN_SEC`。"""
    try:
        return float(os.environ.get("WQB_CORR_MIN_HOLD_FOR_COOLDOWN",
                                    MIN_HOLD_FOR_COOLDOWN_SEC))
    except (TypeError, ValueError):
        return MIN_HOLD_FOR_COOLDOWN_SEC


#: 冷却写入/跳过审计（JSONL，append-only）。用于事后回答「谁占的槽、占多久、
#: 为什么写/不写冷却」——2026-11-17 排查「每 30 min 一条 195s」花了半小时，
#: 有这个文件就只需一眼。超 ``COOLDOWN_AUDIT_MAX_BYTES`` 轮转到 ``.1``。
COOLDOWN_AUDIT_NAME = "correlation.cooldown.audit.jsonl"
COOLDOWN_AUDIT_MAX_BYTES = 512 * 1024


def cooldown_path() -> str:
    return os.path.join(_flock_dir(), COOLDOWN_NAME)


def _cooldown_sec() -> float:
    try:
        return float(os.environ.get("WQB_CORR_COOLDOWN_SEC", COOLDOWN_SEC_DEFAULT))
    except (TypeError, ValueError):
        return COOLDOWN_SEC_DEFAULT


#: 冷却标记的「可信上限」倍数（2026-11-17 残留锁事故）。
#: 正常冷却 ≤ ``max(195s, WQB_CORR_COOLDOWN_SEC)``；记录里的 ``until`` 远超它 ⇒
#: 只可能是系统时钟跳变 / 被手改成远期值 / 半写脏数据，**不是**真实的平台占槽，
#: 按陈旧标记退役（改名 ``.stale``），绝不让人为脏值把账号锁死几小时。
COOLDOWN_SANE_FACTOR = 3.0


def _cooldown_sane_max() -> float:
    return max(COOLDOWN_SEC_DEFAULT, _cooldown_sec()) * COOLDOWN_SANE_FACTOR


def _retire(path: str) -> None:
    """退役标记文件：改名 ``<path>.stale`` 而非删除（与 ``db_write_lock._retire`` 同姿势）。

    删除在沙箱 safe-delete 守卫下会被截获（见 ``db_write_lock._retire`` 注释），
    且留 ``.stale`` 可事后追溯「谁写过一个远期脏值」。改名后标记即视为无主。
    """
    try:
        os.replace(path, path + ".stale")
    except OSError:
        pass  # 已被其它进程退役 / 不存在


def settle_seconds() -> float:
    """计算成功后留给平台释放账号槽的收尾冷却（``WQB_CORR_SETTLE_SEC``）。"""
    try:
        return float(os.environ.get("WQB_CORR_SETTLE_SEC", COOLDOWN_SETTLE_SEC))
    except (TypeError, ValueError):
        return COOLDOWN_SETTLE_SEC


def cooldown_info() -> dict:
    """冷却标记的完整快照（诊断用；不含任何判定）。

    Returns:
        ``{"remaining": float, "until": float, "sec": float, "pid": int|None,
           "at": str, "stale": bool}``；无标记 → ``remaining=0``。
        ``stale=True`` 表示该标记已被判定为脏值并退役（本次不阻塞）。
    """
    import json
    import time
    p = cooldown_path()
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        if not isinstance(d, dict):
            raise ValueError("cooldown record is not an object")
        until = float(d.get("until") or 0)
    except FileNotFoundError:
        return {"remaining": 0.0, "stale": False}
    except Exception:
        # 半写 / 截断 / 非 JSON ⇒ 脏标记，退役，不阻塞（2026-11-17）
        _retire(p)
        return {"remaining": 0.0, "stale": True}
    rem = until - time.time()
    if rem > _cooldown_sane_max():
        # 时钟跳变 / 远期脏值 ⇒ 退役（否则一次手改能把账号锁几小时）
        _retire(p)
        return {"remaining": 0.0, "stale": True, "until": until}
    out = {"remaining": max(0.0, rem), "until": until, "stale": False}
    for k in ("sec", "pid", "at"):
        if d.get(k) is not None:
            out[k] = d.get(k)
    return out


def cooldown_remaining() -> float:
    """距冷却结束还剩多少秒；≤0 表示已可抢槽（脏值会被退役并返回 0）。"""
    return float(cooldown_info().get("remaining") or 0.0)


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
    """清掉冷却标记（幂等；改名 ``.stale`` 退役，不 unlink —— 避开 safe-delete 守卫）。"""
    _retire(cooldown_path())


def _write_cooldown() -> None:  # 历史私有名，保留给既有调用点
    write_cooldown()


#: sidecar 读改写锁（与互斥 token 分开，TTL 短）。2026-11-10 审查 P1-12。
SIDECAR_LOCK_NAME = "correlation.sidecar.lock.json"


@contextmanager
def _sidecar_lock():
    """保护 sidecar 的「读-改-写」原子性。

    旧实现 ``inflight_mark`` / ``inflight_clear`` 直接 read→modify→write，多进程并发
    会丢 ``n`` 或互相覆盖。本锁 TTL 15s、最多等 5s；拿不到也继续执行——sidecar 只是
    提示，不承担互斥（互斥仍由 lock token 负责），故不能因它阻断主流程。
    """
    try:
        info = _flock_acquire(tag="corr:sidecar", ttl_sec=15.0, wait_timeout=5.0,
                              name=SIDECAR_LOCK_NAME, fail_fast=False) or {}
    except Exception:  # noqa: BLE001
        info = {}
    try:
        yield
    finally:
        tok = info.get("token")
        if tok:
            try:
                _flock_release(tok)
            except Exception:  # noqa: BLE001
                pass


# ---------------------------------------------------------------------------
# 账号级熔断（2026-11-10 审查第三批）
# ---------------------------------------------------------------------------
# 实测事故（2026-11-09 夜 KOR）：平台 prod 服务停摆时，本地机制会**自我放大等待**——
# 一次 240s 轮询 → pending → 写 195s 冷却 + 保留 inflight(300s) → 下一次调用 busy →
# 再触发 240s。三颗 alpha 各空转 241s，holder 还在不同 alpha 间轮替，没有任何短路。
#
# ⇒ 连续 N 次 pending（默认 3）即认定「平台侧不可用」，写一个账号级熔断标记；
#   期间所有调用**直接返回 platform_unavailable**，不抢锁、不发请求、不写冷却。
#   拿到任何一次成功结果即清除。这是提示性熔断（sidecar），不承担互斥。
UNAVAILABLE_NAME = "correlation.unavailable.json"
UNAVAILABLE_STREAK_DEFAULT = 3
UNAVAILABLE_SEC_DEFAULT = 600.0


def unavailable_path() -> str:
    return os.path.join(_flock_dir(), UNAVAILABLE_NAME)


def _unavailable_streak_limit() -> int:
    try:
        return max(1, int(os.environ.get("WQB_CORR_UNAVAILABLE_STREAK",
                                         UNAVAILABLE_STREAK_DEFAULT)))
    except (TypeError, ValueError):
        return UNAVAILABLE_STREAK_DEFAULT


def _unavailable_sec() -> float:
    try:
        return max(0.0, float(os.environ.get("WQB_CORR_UNAVAILABLE_SEC",
                                             UNAVAILABLE_SEC_DEFAULT)))
    except (TypeError, ValueError):
        return UNAVAILABLE_SEC_DEFAULT


def _unavailable_read() -> dict:
    import json
    try:
        with open(unavailable_path(), encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return {}
    return d if isinstance(d, dict) else {}


def unavailable_remaining() -> float:
    """距熔断结束还剩多少秒；≤0 表示未熔断。"""
    import time
    try:
        until = float(_unavailable_read().get("until") or 0)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, until - time.time())


def note_pending_streak(alpha_id: str = "") -> dict:
    """记一次 pending；连续达到阈值即写熔断标记。返回当前状态（供日志/返回体）。"""
    import json
    import time
    with _sidecar_lock():
        d = _unavailable_read()
        streak = int(d.get("streak") or 0) + 1
        rec = {"streak": streak, "last_alpha": str(alpha_id or ""),
               "at": time.strftime("%F %T"), "pid": os.getpid()}
        limit = _unavailable_streak_limit()
        if streak >= limit:
            sec = _unavailable_sec()
            rec["until"] = time.time() + sec
            rec["sec"] = round(sec, 1)
            rec["reason"] = f"连续 {streak} 次 pending（阈值 {limit}）⇒ 平台侧不可用"
        else:
            rec["until"] = float(d.get("until") or 0)
        p = unavailable_path()
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            tmp = p + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(rec, f)
            os.replace(tmp, p)
        except Exception:
            pass
    return rec


def clear_unavailable() -> None:
    """拿到成功结果 ⇒ 清除熔断与计数（幂等）。"""
    with _sidecar_lock():
        try:
            os.remove(unavailable_path())
        except OSError:
            pass


def _holder_snapshot() -> dict:
    """读锁 token 的持有者快照（pid / tag / 是否存活）；读不到 → ``{}``。

    只用于**诊断与日志**：判定逻辑不依赖它（死持有者由 ``db_write_lock`` 回收）。
    """
    import json
    try:
        with open(slot_path(), encoding="utf-8") as f:
            d = json.load(f)
        if not isinstance(d, dict):
            return {}
    except Exception:
        return {}
    pid = d.get("pid")
    try:
        from wqb.db_write_lock import _pid_alive  # noqa: WPS433 —— 复用同一判活实现

        alive = bool(_pid_alive(pid))
    except Exception:  # pragma: no cover - 判活失败按存活处理（保守）
        alive = True
    return {"pid": pid, "tag": d.get("tag"), "alive": alive}


def acquire(op_name: str, ttl_sec: float = DEFAULT_TTL_SEC) -> Dict[str, object]:
    """抢账号级相关性槽。**fail-fast**：被他人持有时立即返回 ``busy``。

    Returns:
        ``{"acquired": bool, "busy": bool, "token": path|None, "degraded": bool,
           "reason": str}``
        - ``acquired=False, busy=True`` ⇒ 他人持有（**不放行**，调用方应稍后重试）
        - ``degraded=True`` ⇒ 锁目录不可写等异常 → 无法承担跨进程互斥，
          此时 ``acquired=True``（降级放行，与 ``db_write_lock`` 的既有降级语义一致）

        ``reason`` 区分**三种不同的 busy**（调用方的处置完全不同，2026-11-17）：
        - ``"cooldown"`` ⇒ 上一次计算刚结束、平台仍占槽，``retry_after`` 是**已知
          时长**，可等它到期后重试（``super_build`` 的 prod 闸据此等待而非直接放弃）；
        - ``"token_busy"`` ⇒ 另一个**存活**进程正持有互斥 token（附 ``holder``
          快照：pid/tag/alive），按原设计 fail-fast、不排队；
        - ``"platform_unavailable"`` ⇒ 账号级熔断中，直接放弃。
    """
    # 0) 账号级熔断（2026-11-10）：平台侧连续 pending ⇒ 直接短路，不抢锁不发请求。
    # 避免「240s 轮询 → 195s 冷却 → inflight 残留 → busy → 再 240s」的自我放大等待。
    _ua = unavailable_remaining()
    if _ua > 0:
        return {
            "acquired": False,
            "busy": True,
            "unavailable": True,
            "reason": "platform_unavailable",
            "retry_after": round(_ua, 1),
            "token": None,
            "degraded": False,
        }

    # 0) 冷却窗口：上一次调用刚结束，平台槽位还没释放 ⇒ 直接 busy，不去撞平台
    _cd = cooldown_info()
    _cd_rem = float(_cd.get("remaining") or 0.0)
    if _cd_rem > 0:
        return {
            "acquired": False,
            "busy": True,
            "cooldown": True,
            "reason": "cooldown",
            "retry_after": round(_cd_rem, 1),
            "cooldown_pid": _cd.get("pid"),
            "cooldown_at": _cd.get("at"),
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
    out = {
        "acquired": bool(info.get("ok")),
        "busy": bool(info.get("busy")),
        "token": info.get("token"),
        "degraded": bool(info.get("degraded")),
        "reason": ("ok" if info.get("ok") else
                   ("token_busy" if info.get("busy") else "degraded")),
    }
    if out["busy"]:
        # 诊断：谁占着槽、还活着吗（token 死持有者已由 db_write_lock 回收，
        # 走到这里说明持有者**存活**；仍带上快照便于定位是哪个进程）
        out["holder"] = _holder_snapshot()
    return out


def _token_snapshot(token) -> dict:
    """读 token 文件的快照（``pid``/``tag``/``at``）；读不到返回 ``{}``。

    必须在 ``_flock_release`` **之前**读——退役会把 token 改名成 ``.stale``。
    """
    import json
    try:
        with open(token, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError, TypeError):
        return {}


def audit_cooldown(action: str, snap: dict, held=None, seconds=None) -> None:
    """记一条冷却审计（best-effort，失败绝不影响主流程）。

    ``action``：``write`` / ``skip_short``（持槽太短，没算过）/ ``skip_by_caller``。
    """
    import json
    import time
    try:
        d = _flock_dir()
        p = os.path.join(d, COOLDOWN_AUDIT_NAME)
        try:
            if os.path.getsize(p) > COOLDOWN_AUDIT_MAX_BYTES:
                os.replace(p, p + ".1")
        except OSError:
            pass
        rec = {
            "at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pid": os.getpid(),
            "action": action,
            "tag": snap.get("tag"),
            "holder_pid": snap.get("pid"),
            "held_s": None if held is None else round(float(held), 1),
            "cooldown_s": None if seconds is None else round(float(seconds), 1),
        }
        with open(p, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001  审计是附加物，绝不能因它中断释放
        pass


def release(token, cooldown: bool = True, seconds=None) -> None:
    """释放槽（幂等；仅当持有者是本进程时才退役，防误删他人 token）。

    ★ 2026-10-26：释放后**写冷却标记**——平台在该次计算结束后仍会占槽 ~180s，
    本地若立刻放行下一个调用者，它必然撞 ``correlation_busy``。

    ★ 2026-10-28 P0-1：冷却**按结果分流**。调用方能判断结果时显式传：
      - ``cooldown=False`` ⇒ 不写冷却（立即拿到既有值 / 4xx 终态 / 异常路径）；
      - ``seconds=x`` ⇒ 写 x 秒（触发计算后按平台 Retry-After 或 195s；
        计算成功后用 ``COOLDOWN_SETTLE_SEC``）。
    不传参的旧调用点保持 195s 语义不变。

    ★ 2026-11-17：**没算过就不写冷却**。``seconds`` 缺省（= 走 195s 那条路）时，
    若持槽时长 < :func:`min_hold_for_cooldown`（60s），说明平台侧根本没跑新计算
    （真计算 180–200s，20s 拿到值只能是既有值直读）⇒ 跳过冷却并记审计。
    显式传 ``seconds`` / ``cooldown=False`` 的调用点语义不变（调用方比本模块更懂结果）。

    每次释放都会往 ``logs/_dblock/correlation.cooldown.audit.jsonl`` 记一行
    （action / tag / held_s / cooldown_s），排查「谁在占槽」不必再猜。
    """
    snap = _token_snapshot(token) if token else {}
    held = None
    try:
        _at = float(snap.get("at") or 0)
        if _at > 0:
            import time
            held = max(0.0, time.time() - _at)
    except (TypeError, ValueError):
        held = None
    if token:
        _flock_release(token)
    if not cooldown:
        audit_cooldown("skip_by_caller", snap, held, seconds)
        return
    if seconds is None and held is not None and held < min_hold_for_cooldown():
        audit_cooldown("skip_short", snap, held, None)
        return
    write_cooldown(seconds)
    audit_cooldown("write", snap, held,
                   _cooldown_sec() if seconds is None else seconds)


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
    with _sidecar_lock():
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
    now = time.time()
    ttl = _inflight_ttl_sec() if ttl_sec is None else float(ttl_sec)
    with _sidecar_lock():
        items = _inflight_prune(_inflight_read())
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
    with _sidecar_lock():
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
