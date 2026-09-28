# -*- coding: utf-8 -*-
"""平台状态最终普查（v3）：分诊目标 alpha 逐个核平台真实状态并回写本地。"""
import asyncio
import json
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
OUT = r"D:\coding\traeCN_project\wqb\logs\_triage_platform_status_v3.json"

FINAL = ["Jj7ee6nO", "omqEE1pn", "E5l6mmqJ", "6XjqLn3J"]


def build_pool():
    """补查分诊范围里 platform_status 仍未确认的（含新入库变体）。"""
    conn = sqlite3.connect(DB)
    rows = conn.execute('''
        SELECT alpha_id FROM alphas
        WHERE sharpe IS NOT NULL AND fitness IS NOT NULL
          AND (platform_status IS NULL OR platform_status NOT IN ('ACTIVE','UNSUBMITTED','DECOMMISSIONED')
               OR stage IS NULL OR stage NOT IN ('OS','IS'))
          AND (sharpe>=1.58 AND fitness>=1.0 OR (two_year_sharpe>=1.40) OR is_ladder_sharpe IS NOT NULL)
    ''').fetchall()
    conn.close()
    pool = [r[0] for r in rows]
    for a in FINAL:
        if a not in pool:
            pool.append(a)
    return pool


async def main():
    from brain_api import brain_client
    brain = brain_client
    await brain.ensure_authenticated()

    done = set()
    try:
        done = set(json.load(open(OUT, encoding="utf-8")).keys())
    except Exception:
        pass
    pool = [a for a in build_pool() if a not in done]
    print(f"待普查: {len(pool)} 颗")
    res = {}
    try:
        res = json.load(open(OUT, encoding="utf-8"))
    except Exception:
        res = {}
    lit = 0
    for i, aid in enumerate(pool):
        try:
            d = await brain.get_alpha_details(aid)
            st, stage = d.get("status"), d.get("stage")
            res[aid] = f"{st}/{stage}"
            if st == "ACTIVE" or stage == "OS":
                lit += 1
        except Exception as e:
            res[aid] = f"ERROR:{str(e)[:60]}"
        if (i + 1) % 25 == 0:
            print(f"  进度 {i+1}/{len(pool)} 已点亮 {lit}")
            json.dump(res, open(OUT, "w", encoding="utf-8"), indent=1)
    json.dump(res, open(OUT, "w", encoding="utf-8"), indent=1)

    conn = sqlite3.connect(DB, timeout=20)
    now = datetime.now().isoformat(timespec="seconds")
    n = 0
    for aid, s in res.items():
        if s.startswith("ACTIVE"):
            conn.execute("UPDATE alphas SET platform_status='ACTIVE', stage='OS', updated_at=? WHERE alpha_id=?",
                         (now, aid)); n += 1
        elif s.startswith("UNSUBMITTED"):
            conn.execute("UPDATE alphas SET platform_status='UNSUBMITTED', stage=COALESCE(stage,'IS'), updated_at=? WHERE alpha_id=?",
                         (now, aid)); n += 1
    conn.commit()
    print(f"\n普查完成: {len(res)} 颗记录 | 已点亮 {lit} | 回写 {n}")
    for a in FINAL:
        print(f"  {a}: {res.get(a)}")
    conn.close()


asyncio.run(main())
