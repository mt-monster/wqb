# -*- coding: utf-8 -*-
"""883WZJ1W 提交后回写（修复版）：INSERT 补 region_id/universe/neutralization。"""
import json
import sqlite3
import sys
from datetime import datetime, timezone

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
ALPHA = "883WZJ1W"

import asyncio


async def fetch_settings():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    out = {}
    vres = json.load(open(r"D:\coding\traeCN_project\wqb\logs\_n1qmj_variants.json", encoding="utf-8"))
    for name, rec in vres["variants"].items():
        aid = rec.get("alpha_id")
        if not aid:
            continue
        d = await brain_client.get_alpha_details(aid)
        s = d.get("settings") or {}
        iss = d.get("is") or {}
        checks = {c.get("name"): c for c in (iss.get("checks") or [])}
        out[aid] = {
            "name": name,
            "code": (d.get("regular") or {}).get("code"),
            "region": s.get("region"), "universe": s.get("universe"),
            "neutralization": s.get("neutralization"), "delay": s.get("delay"),
            "sharpe": iss.get("sharpe"), "fitness": iss.get("fitness"),
            "margin": iss.get("margin"), "turnover": iss.get("turnover"),
            "two_year_sharpe": (checks.get("LOW_2Y_SHARPE") or {}).get("value"),
            "self_corr": (checks.get("SELF_CORRELATION") or {}).get("value"),
        }
    return out


def writeback(details):
    conn = sqlite3.connect(DB, timeout=20)
    cur = conn.cursor()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for aid, d in details.items():
        is_target = aid == ALPHA
        reg = cur.execute("SELECT id FROM regions WHERE name=?", (d["region"],)).fetchone()
        region_id = reg[0] if reg else None
        st = "ACTIVE" if is_target else "UNSUBMITTED"
        sg = "OS" if is_target else "IS"
        ex = cur.execute("SELECT id FROM alphas WHERE alpha_id=?", (aid,)).fetchone()
        if ex:
            cur.execute("""UPDATE alphas SET platform_status=?, stage=?,
                           two_year_sharpe=COALESCE(two_year_sharpe, ?),
                           self_correlation=COALESCE(self_correlation, ?),
                           date_submitted=COALESCE(date_submitted, ?), updated_at=?
                           WHERE alpha_id=?""",
                        (st, sg, d["two_year_sharpe"], d["self_corr"],
                         now if is_target else None, now, aid))
        else:
            cur.execute("""INSERT INTO alphas (alpha_id, expression, region_id, dataset_id, universe, delay,
                           neutralization, sharpe, fitness, margin, turnover, two_year_sharpe,
                           self_correlation, platform_status, stage, date_submitted,
                           created_at, updated_at)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (aid, d["code"], region_id, 292, d["universe"], d["delay"], d["neutralization"],
                         d["sharpe"], d["fitness"], d["margin"], d["turnover"],
                         d["two_year_sharpe"], d["self_corr"], st, sg,
                         now if is_target else None, now, now))
        print(f"[db] {aid} ({d['name']}) -> {st}/{sg} sh={d['sharpe']} fit={d['fitness']} "
              f"self={d['self_corr']} region_id={region_id}")
    conn.commit()
    n = cur.execute("SELECT COUNT(*) FROM alphas WHERE platform_status='ACTIVE' AND stage='OS'").fetchone()[0]
    chk = cur.execute("SELECT alpha_id, platform_status, stage, date_submitted, self_correlation "
                      "FROM alphas WHERE alpha_id=?", (ALPHA,)).fetchone()
    conn.close()
    print(f"[verify] {ALPHA} 行: {chk}")
    print(f"[verify] 本地 ACTIVE/OS 总数: {n}")


details = asyncio.run(fetch_settings())
writeback(details)
