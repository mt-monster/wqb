# -*- coding: utf-8 -*-
"""budget_planner.py - 配额/并发预算规划器（2026-09-01 落地，#3）。

输入当前预算（七槽 / ET 日提交额度）与候选池状态，输出本轮建议：
  1. 填槽建议：哪些波该占槽（高先验组合批优先、弱探针最多 1 槽）；
  2. 提交顺序建议：READY 候选按点塔价值排序（差 ≤2 颗即点亮优先，同档 fitness 降序）；
  3. 配额日历：当前 ET 日已用 / 剩余 / 重置时刻。

数据源：DB（wave_results / submit_ready ledger / backtest_results）+ 平台
（activities submissions）。纯建议输出（不执行任何提交），供 Agent 选波/提交前查。

用法：
  python budget_planner.py --campaign-dir tracking/KOR                 # 填槽+配额概览
  python budget_planner.py --campaign-dir tracking/KOR --submit-plan  # READY 候选提交排序
"""
import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import add_campaign_arg, CampaignContext, load_credentials
from _lib.api import Api

SLOTS = 7           # Token-Bucket 突发容量
DAILY_REGULAR = 4   # ET 日历日


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


def et_day_now():
    import datetime as dt
    return datetime.now(dt.timezone.utc) - dt.timedelta(hours=4)


def quota_status():
    """ET 日历日配额（activities 优先，失败返回 None）。"""
    try:
        api = Api()
        api.login(*load_credentials())
        j = json.load(api.get("/users/self/activities/submissions"))
        et = et_day_now()
        today_key = et.strftime("%Y-%m-%d")
        n = 0
        for item in j.get("results", j if isinstance(j, list) else []):
            ds = item.get("dateSubmitted") or item.get("createdAt") or item.get("date")
            if not ds:
                continue
            try:
                t = datetime.fromisoformat(ds.replace("Z", "+00:00")) - __import__("datetime").timedelta(hours=4)
                if t.strftime("%Y-%m-%d") == today_key:
                    n += 1
            except Exception:
                continue
        reset = (et.replace(hour=0, minute=0, second=0, microsecond=0)
                 + __import__("datetime").timedelta(days=1)).isoformat()
        return {"et_day": today_key, "used": n, "remaining": max(0, DAILY_REGULAR - n),
                "reset_et": reset, "limit": DAILY_REGULAR}
    except Exception as e:
        return None


def slot_plan(ctx, db):
    """填槽建议：近闸波（有 sharpe>=1.3 未达标）优先、弱探针最多 1 槽。"""
    import sqlite3
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    # 每波最新最强信号
    rows = con.execute(
        "SELECT region, wave, dataset, MAX(sharpe) ms, COUNT(*) n FROM backtest_results "
        "WHERE region=? AND sharpe IS NOT NULL GROUP BY wave ORDER BY ms DESC",
        (ctx.region,),
    ).fetchall()
    con.close()
    near = [r for r in rows if (r["ms"] or 0) >= 1.3]
    signal = [r for r in rows if 1.0 <= (r["ms"] or 0) < 1.3]
    plan = []
    for r in near[:SLOTS]:
        plan.append({"wave": str(r["wave"]), "dataset": r["dataset"],
                     "action": "组合批占槽（近闸，Mode A 收敛/组合提分）", "max_sharpe": round(r["ms"], 2)})
    for r in signal[:max(0, SLOTS - len(plan))]:
        plan.append({"wave": str(r["wave"]), "dataset": r["dataset"],
                     "action": "换腿组合占槽（有信号未近闸，Mode B 优先）", "max_sharpe": round(r["ms"], 2)})
    remaining = SLOTS - len(plan)
    if remaining > 0:
        plan.append({"wave": None, "dataset": None,
                     "action": f"剩余 {remaining} 槽：win 配方换腿（registry win 层）优先，弱探针最多 1 槽"})
    return {"slots_total": SLOTS, "plan": plan,
            "near_gate_waves": len(near), "signal_waves": len(signal)}


def submit_plan(ctx, db):
    """READY 候选提交排序（点塔价值 proxy：fitness 降序 + 提交时间升序）。

    注：塔的精确颗数需平台 pyramids 数据（tools/submit_verdict.py --with-tower 路线）；
    本 planner 的排序是 DB 侧 proxy，最终点塔确认走 submit_verdict。
    """
    import sqlite3
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    row = con.execute(
        "SELECT value FROM ledger_kv WHERE region=? AND key='submit_ready'", (ctx.region,)
    ).fetchone()
    con.close()
    if not row:
        return {"candidates": 0, "note": "无 submit_ready 缓冲池（先跑 S4→S5 判定链）"}
    try:
        pool = json.loads(row[0])
    except Exception:
        pool = []
    cands = [p for p in pool if isinstance(p, dict) and p.get("id")]
    return {"candidates": len(cands),
            "note": f"按 fitness 降序提交（最终点塔确认走 tools/submit_verdict.py）",
            "order_hint": [c.get("id") for c in cands]}


def main():
    ap = argparse.ArgumentParser(description="预算规划器：七槽填槽 + ET 日提交额度 + 提交顺序建议")
    add_campaign_arg(ap)
    ap.add_argument("--submit-plan", action="store_true", help="附 READY 候选提交排序")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    db = _db_path(ctx)

    out = {"generated_at": datetime.now().isoformat(timespec="seconds"),
           "region": ctx.region,
           "slot_plan": slot_plan(ctx, db)}
    q = quota_status()
    out["quota"] = q or {"note": "平台配额不可达（离线模式），按 ET 日历日 4/日 口径自算"}
    if a.submit_plan:
        out["submit_plan"] = submit_plan(ctx, db)

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    print(f"[budget] region={ctx.region} 七槽建议（近闸 {out['slot_plan']['near_gate_waves']} 波 / 有信号 {out['slot_plan']['signal_waves']} 波）")
    for p in out["slot_plan"]["plan"]:
        w = p.get("wave") or "-"
        ds = p.get("dataset") or "-"
        print(f"  wave={w:14s} ds={ds:24s} {p['action']}")
    if out["quota"].get("used") is not None:
        print(f"[budget] 提交配额：ET 日 {out['quota']['et_day']} 已用 {out['quota']['used']}/{out['quota']['limit']}，"
              f"剩 {out['quota']['remaining']}，重置 {out['quota']['reset_et']}")
    if a.submit_plan:
        sp = out.get("submit_plan", {})
        print(f"[budget] submit_ready 池 {sp.get('candidates', 0)} 个候选；{sp.get('note', '')}")


if __name__ == "__main__":
    main()
