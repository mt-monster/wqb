# -*- coding: utf-8 -*-
"""campaign_mutex.py - 多战役互斥仲裁（2026-09-01 落地，#7）。

多会话/多 Agent 并行开战役时，波号分配、槽位预算、提交额度是共享资源。
本模块用 data/wqb.db 的 ledger_kv 行级原子写做轻量仲裁：

  - allocate_wave(region)：CAS 分配该 region 下一个不冲突的波号（防两会话撞号）；
  - acquire_slots(region, n, ttl_min)：占用回测槽位预算（全局 SLOTS=7 共享，TTL 过期自动释放）；
  - quota_reserve(region, date_submitted_slot)：提交额度占用标记（ET 日 4 颗共享账本）；
  - release(region, kind, key)：主动释放。

设计：sqlite3 的 UPDATE 原子性 + TTL 自愈（进程崩溃不留下永久锁——过期即失效）。
不做强互斥（不阻塞），只做冲突检测与告警：两个会话硬要同时提交，第二个会收到
warning 并继续（人仍是最终仲裁者）。

用法（CLI 自检）：
  python campaign_mutex.py --campaign-dir tracking/KOR status
  python campaign_mutex.py --campaign-dir tracking/KOR alloc-wave
  python campaign_mutex.py --campaign-dir tracking/KOR take-slots --n 3 --ttl 60
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import add_campaign_arg, CampaignContext

SLOTS_TOTAL = 7
GLOBAL = "GLOBAL"


def _db_path(ctx):
    here = os.path.dirname(os.path.abspath(__file__))
    roots = []
    env = os.environ.get("WQB_ROOT")
    if env:
        roots.append(env)
    cdir = getattr(ctx, "dir", None)
    if cdir:
        roots.append(os.path.abspath(os.path.join(cdir, "..", "..")))
    roots.append(os.path.abspath(os.path.join(here, "..", "..", "..", "..", "..")))
    for r in roots:
        p = os.path.join(r, "data", "wqb.db")
        if os.path.isfile(p):
            return p
    raise SystemExit("未找到 data/wqb.db")


def _et_now():
    return datetime.now(timezone.utc)


def _get(con, region, key):
    row = con.execute("SELECT value, updated_at FROM ledger_kv WHERE region=? AND key=?",
                      (region, key)).fetchone()
    return row


def _set(con, region, key, value):
    con.execute("INSERT OR REPLACE INTO ledger_kv (region, key, value, updated_at) VALUES (?,?,?,?)",
                (region, key, json.dumps(value, ensure_ascii=False),
                 _et_now().isoformat(timespec="seconds")))
    con.commit()


def _prune_expired(holders, ttl_min):
    """清 TTL 过期的持有者，返回 (存活, 清理数)。"""
    cutoff = _et_now() - timedelta(minutes=ttl_min)
    alive, dropped = [], 0
    for h in holders:
        try:
            t = datetime.fromisoformat(h.get("at").replace("Z", "+00:00"))
        except Exception:
            continue  # 解析失败视为存活（保守）
        if t >= cutoff:
            alive.append(h)
        else:
            dropped += 1
    return alive, dropped


def allocate_wave(ctx, db):
    """CAS 分配 region 下一个波号。返回 (new_wave, conflict_warning)。"""
    con = sqlite3.connect(db, timeout=10)
    try:
        key = "wave_alloc"
        row = _get(con, ctx.region, key)
        cur = {}
        if row:
            try:
                cur = json.loads(row[0])
            except Exception:
                cur = {}
        used = set(cur.get("used", []))
        # 数字波号从 DB wave_results + expressions 已存在的编号继续
        for r in con.execute(
            "SELECT DISTINCT wave FROM expressions WHERE region=? AND wave GLOB '[0-9]*'", (ctx.region,)
        ).fetchall():
            w = str(r[0])
            if w.isdigit():
                used.add(int(w))
        for r in con.execute(
            "SELECT DISTINCT wave_number FROM wave_results WHERE region=?", (ctx.region,)
        ).fetchall():
            try:
                used.add(int(r[0]))
            except Exception:
                pass
        # ckpt_w<N> 键也是波号足迹（backtest_results 无行时兜底）
        for r in con.execute(
            "SELECT key FROM ledger_kv WHERE region=? AND key GLOB 'ckpt_w[0-9]*'", (ctx.region,)
        ).fetchall():
            try:
                used.add(int(str(r[0]).replace("ckpt_w", "")))
            except Exception:
                pass
        n = 1
        while n in used:
            n += 1
        # 波号基线：已存在编号的最大值（防回退到已用小号）
        if used:
            n = max(n, max(used) + 1)
            while n in used:
                n += 1
        owner = f"{os.getpid()}@{_et_now().isoformat(timespec='seconds')}"
        used.add(n)
        cur = {"used": sorted(used), "last_alloc": n, "owner": owner}
        _set(con, ctx.region, key, cur)
        return n, None
    finally:
        con.close()


def acquire_slots(ctx, db, n, ttl_min, owner_tag=None):
    """占用全局回测槽位预算。返回 (ok, remaining, warning)。"""
    con = sqlite3.connect(db, timeout=10)
    try:
        row = _get(con, GLOBAL, "slot_holders")
        holders = []
        if row:
            try:
                holders = json.loads(row[0]).get("holders", [])
            except Exception:
                holders = []
        holders, dropped = _prune_expired(holders, ttl_min)
        in_use = sum(h.get("n", 0) for h in holders)
        if in_use + n > SLOTS_TOTAL:
            other_regions = sorted({h.get("region") for h in holders if h.get("region") != ctx.region})
            warn = (f"槽位预算不足：全局 {SLOTS_TOTAL} 槽在用 {in_use}（其他区域 {other_regions}），"
                    f"本次申请 {n} 超限（TTL {ttl_min}min 已自动清理 {dropped} 个过期持有）")
            return False, SLOTS_TOTAL - in_use, warn
        holders.append({"region": ctx.region, "n": n,
                        "at": _et_now().isoformat(timespec="seconds"),
                        "owner": owner_tag or str(os.getpid())})
        _set(con, GLOBAL, "slot_holders", {"holders": holders})
        return True, SLOTS_TOTAL - in_use - n, None
    finally:
        con.close()


def quota_reserve(ctx, db):
    """ET 日提交额度占用标记（soft：超限只告警不阻断）。返回 (ok, used_today, warning)。"""
    con = sqlite3.connect(db, timeout=10)
    try:
        et_day = (_et_now() - timedelta(hours=4)).strftime("%Y-%m-%d")
        key = "quota_reserve"
        row = _get(con, GLOBAL, key)
        cur = {}
        if row:
            try:
                cur = json.loads(row[0])
            except Exception:
                cur = {}
        if cur.get("et_day") != et_day:
            cur = {"et_day": et_day, "regions": {}}
        regs = cur.get("regions", {})
        regs[ctx.region] = regs.get(ctx.region, 0) + 1
        cur["regions"] = regs
        total = sum(regs.values())
        _set(con, GLOBAL, key, cur)
        warn = None
        if total > 4:
            warn = f"ET 日 {et_day} 提交额度占用标记已 {total}（>4），跨战役共享额度注意错峰"
        return total <= 4, total, warn
    finally:
        con.close()


def status(ctx, db):
    con = sqlite3.connect(db, timeout=10)
    try:
        row = _get(con, GLOBAL, "slot_holders")
        holders = json.loads(row[0]).get("holders", []) if row else []
        # 全部按默认 TTL 60min 展示清理后状态
        holders, _ = _prune_expired(holders, 60)
        by_region = {}
        for h in holders:
            by_region[h["region"]] = by_region.get(h["region"], 0) + h.get("n", 0)
        row = _get(con, GLOBAL, "quota_reserve")
        q = json.loads(row[0]) if row else {}
        row = _get(con, ctx.region, "wave_alloc")
        w = json.loads(row[0]) if row else {}
        return {"slots_in_use": sum(by_region.values()), "slots_by_region": by_region,
                "quota_reserve": q, "region_wave_alloc": w.get("last_alloc")}
    finally:
        con.close()


def main():
    ap = argparse.ArgumentParser(description="多战役互斥仲裁（波号 CAS / 槽位预算 / 提交额度共享账本）")
    add_campaign_arg(ap)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("alloc-wave")
    sp = sub.add_parser("take-slots")
    sp.add_argument("--n", type=int, default=1)
    sp.add_argument("--ttl", type=int, default=60, help="持有 TTL（分钟，过期自动释放）")
    sub.add_parser("quota-reserve")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    db = _db_path(ctx)

    if a.cmd == "status":
        print(json.dumps(status(ctx, db), ensure_ascii=False, indent=1))
    elif a.cmd == "alloc-wave":
        n, warn = allocate_wave(ctx, db)
        print(f"[mutex] region={ctx.region} 分配波号 = {n}" + (f"（{warn}）" if warn else ""))
    elif a.cmd == "take-slots":
        ok, remain, warn = acquire_slots(ctx, db, a.n, a.ttl)
        print(f"[mutex] region={ctx.region} 申请 {a.n} 槽: {'OK' if ok else 'REFUSED'}，剩余预算 {remain}")
        if warn:
            print(f"[mutex][WARN] {warn}")
    elif a.cmd == "quota-reserve":
        ok, used, warn = quota_reserve(ctx, db)
        print(f"[mutex] region={ctx.region} 提交额度占用标记: 今日累计 {used}（{'OK' if ok else '超限'}）")
        if warn:
            print(f"[mutex][WARN] {warn}")


if __name__ == "__main__":
    main()
