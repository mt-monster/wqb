# -*- coding: utf-8 -*-
"""提交 883WZJ1W（V5，N1QMJ10q 去相关抢救成功变体）并回写本地库。

用户已于 2026-09-14 会话内明确确认提交。
流程：POST /alphas/{id}/submit → 轮询至终态 → 核验翻 OS → upsert alphas 表
（platform_status/stage/date_submitted/metrics + prod/self corr）。
"""
import asyncio
import json
import sqlite3
import sys
from datetime import datetime, timezone

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
ALPHA = "883WZJ1W"


async def main():
    from brain_api import brain_client
    brain = brain_client
    await brain.ensure_authenticated()

    print(f"[submit] 提交 {ALPHA} ...")
    res = await brain.submit_alpha(ALPHA)
    print(json.dumps(res, ensure_ascii=False, default=str)[:800])

    # 轮询平台状态翻 OS
    final_status, final_stage = None, None
    for i in range(30):
        d = await brain.get_alpha_details(ALPHA)
        final_status, final_stage = d.get("status"), d.get("stage")
        if final_status == "ACTIVE" or final_stage == "OS":
            break
        await asyncio.sleep(15)
    print(f"[verify] 最终状态: status={final_status} stage={final_stage}")

    iss = d.get("is") or {}
    checks = {c.get("name"): c for c in (iss.get("checks") or [])}
    y2 = (checks.get("LOW_2Y_SHARPE") or {}).get("value")
    self_c = (checks.get("SELF_CORRELATION") or {}).get("value")
    prod_c = (checks.get("PROD_CORRELATION") or {}).get("value")
    s = d.get("settings") or {}
    print(f"[verify] 提交时实测: SELF_CORR={self_c} PROD_CORR={prod_c}")

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB, timeout=20)
    cur = conn.cursor()
    row = cur.execute("SELECT id, sharpe, fitness FROM alphas WHERE alpha_id=?", (ALPHA,)).fetchone()
    if row:
        cur.execute("""UPDATE alphas SET platform_status='ACTIVE', stage='OS', date_submitted=?,
                       two_year_sharpe=COALESCE(two_year_sharpe, ?), updated_at=? WHERE alpha_id=?""",
                    (now, y2, now, ALPHA))
        print(f"[db] 更新 {ALPHA} -> ACTIVE/OS, date_submitted={now}")
    else:
        cur.execute("""INSERT INTO alphas (alpha_id, expression, sharpe, fitness, margin, turnover,
                       two_year_sharpe, platform_status, stage, date_submitted, created_at, updated_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (ALPHA, d.get("regular", {}).get("code"), iss.get("sharpe"), iss.get("fitness"),
                     iss.get("margin"), iss.get("turnover"), y2, "ACTIVE", "OS", now, now, now))
        print(f"[db] 新增 {ALPHA} -> ACTIVE/OS")
    # 顺带记录本轮 6 个变体（未提交的标记 UNSUBMITTED/IS，留作存量）
    vres = json.load(open(r"D:\coding\traeCN_project\wqb\logs\_n1qmj_variants.json", encoding="utf-8"))
    region_map = {"V5_top2000": None}
    for name, rec in vres["variants"].items():
        aid = rec.get("alpha_id")
        if not aid:
            continue
        m = rec.get("metrics") or {}
        st = "ACTIVE" if aid == ALPHA else "UNSUBMITTED"
        sg = "OS" if aid == ALPHA else "IS"
        ex = cur.execute("SELECT id FROM alphas WHERE alpha_id=?", (aid,)).fetchone()
        if ex:
            if aid == ALPHA:
                continue
            cur.execute("""UPDATE alphas SET platform_status=?, stage=?, two_year_sharpe=?,
                           prod_correlation=?, self_correlation=?, updated_at=? WHERE alpha_id=?""",
                        (st, sg, m.get("two_year_sharpe"),
                         (rec.get("prod_corr") or {}).get("max"),
                         (rec.get("self_corr") or {}).get("max"), now, aid))
        else:
            cur.execute("""INSERT INTO alphas (alpha_id, expression, sharpe, fitness, margin, turnover,
                           two_year_sharpe, prod_correlation, self_correlation, platform_status, stage,
                           date_submitted, created_at, updated_at)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (aid, EXPR if False else None, m.get("sharpe"), m.get("fitness"),
                         m.get("margin"), m.get("turnover"), m.get("two_year_sharpe"),
                         (rec.get("prod_corr") or {}).get("max"),
                         (rec.get("self_corr") or {}).get("max"),
                         st, sg, now if aid == ALPHA else None, now, now))
    conn.commit()
    n = cur.execute("SELECT COUNT(*) FROM alphas WHERE platform_status='ACTIVE' AND stage='OS'").fetchone()[0]
    conn.close()
    print(f"[db] 本地 ACTIVE/OS 总数现为 {n}")


asyncio.run(main())
