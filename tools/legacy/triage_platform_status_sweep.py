# -*- coding: utf-8 -*-
"""平台状态普查：分诊涉及的全部本地候选逐个拉 get_alpha_details，
把真实 platform_status/stage 写回 alphas（修复历史回写缺口）。
输出 lit / unlit 两份名单。"""
import asyncio
import json
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
OUT = r"D:\coding\traeCN_project\wqb\logs\_triage_platform_status.json"


def targets():
    conn = sqlite3.connect(DB)
    rows = conn.execute('''
        SELECT alpha_id FROM alphas
        WHERE sharpe IS NOT NULL AND fitness IS NOT NULL
          AND (platform_status IS NULL OR platform_status NOT IN ('ACTIVE','UNSUBMITTED','DECOMMISSIONED')
               OR (stage IS NULL OR stage NOT IN ('OS','IS')))
          AND (sharpe >= 1.58 AND fitness >= 1.0
               OR (two_year_sharpe IS NOT NULL AND two_year_sharpe >= 1.40)
               OR is_ladder_sharpe IS NOT NULL)
    ''').fetchall()
    conn.close()
    done = set()
    try:
        done = set(json.load(open(OUT, encoding="utf-8")).keys())
    except Exception:
        pass
    return [r[0] for r in rows if r[0] not in done]


async def main():
    from brain_api import brain_client
    brain = brain_client
    await brain.ensure_authenticated()

    ids = targets()
    print(f"普查目标: {len(ids)} 颗")
    res = {}
    lit, unlit = [], []
    for i, aid in enumerate(ids):
        try:
            d = await brain.get_alpha_details(aid)
            st, stage = d.get("status"), d.get("stage")
            res[aid] = f"{st}/{stage}"
            is_os = (st == "ACTIVE" or stage == "OS")
            (lit if is_os else unlit).append(aid)
        except Exception as e:
            res[aid] = f"ERROR:{str(e)[:80]}"
        if (i + 1) % 25 == 0:
            print(f"  进度 {i+1}/{len(ids)} 已点亮 {len(lit)}")
            json.dump(res, open(OUT, "w", encoding="utf-8"), indent=1)

    json.dump(res, open(OUT, "w", encoding="utf-8"), indent=1)
    conn = sqlite3.connect(DB, timeout=20)
    now = datetime.now().isoformat(timespec="seconds")
    n = 0
    for aid, s in res.items():
        if s.startswith("ACTIVE"):
            conn.execute("UPDATE alphas SET platform_status='ACTIVE', stage='OS', updated_at=? WHERE alpha_id=?",
                         (now, aid))
            n += 1
        elif s.startswith("UNSUBMITTED"):
            conn.execute("UPDATE alphas SET platform_status='UNSUBMITTED', stage=COALESCE(stage,'IS'), updated_at=? WHERE alpha_id=?",
                         (now, aid))
    conn.commit(); conn.close()
    print(f"\n普查完成: 已点亮 {len(lit)} | 未提交 {len(unlit)} | 回写 {n} 颗")
    print("已点亮名单:", lit)


asyncio.run(main())
