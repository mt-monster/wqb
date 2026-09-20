# -*- coding: utf-8 -*-
"""补 2Y：IND 2 颗 + 异常 4 颗（无 backtest_results 记录）。

在 backfill_2y_from_platform.py 基础上扩展：
- 2Y / ladder 从 is.checks 提取（LOW_2Y_SHARPE / IS_LADDER_SHARPE）
- margin 从 is.margin 补（4 颗异常记录缺）
- universe / neutralization / region 从 settings 补（异常记录缺 wave/code，先补基础设置）
- 顺带回填 platform_status / stage 快照（UNSUBMITTED/IS）
"""
import asyncio
import json
import shutil
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
TARGETS = ["Jj7aRNKm", "2rlVPwdw", "qMja95Q2", "3qlKQ1qX", "WjPjXARx", "N1QMJ10q"]


async def main():
    from brain_api import BrainApiClient

    brain = BrainApiClient()
    await brain.ensure_authenticated()

    results = {}
    for aid in TARGETS:
        try:
            d = await brain.get_alpha_details(aid)
            checks = (d.get("is") or {}).get("checks") or []
            two_y = ladder = None
            for c in checks:
                val = c.get("value")
                if val is None:
                    continue
                if c.get("name") == "LOW_2Y_SHARPE":
                    two_y = val
                elif c.get("name") == "IS_LADDER_SHARPE":
                    ladder = val
            iss = d.get("is") or {}
            st = d.get("settings") or {}
            results[aid] = {
                "two_year_sharpe": two_y,
                "is_ladder_sharpe": ladder,
                "margin": iss.get("margin"),
                "sharpe": iss.get("sharpe"),
                "fitness": iss.get("fitness"),
                "universe": st.get("universe"),
                "neutralization": st.get("neutralization"),
                "region": st.get("region"),
                "delay": st.get("delay"),
                "platform_status": d.get("status"),
                "stage": d.get("stage"),
            }
            print(f"{aid}: 2Y={two_y} ladder={ladder} mgn={iss.get('margin')} "
                  f"uni={st.get('universe')} reg={st.get('region')} status={d.get('status')}/{d.get('stage')}")
        except Exception as e:
            results[aid] = {"error": str(e)[:200]}
            print(f"{aid}: ERROR {str(e)[:120]}")

    json.dump(results, open(r"D:\coding\traeCN_project\wqb\logs\_backfill_2y_six_results.json",
                            "w", encoding="utf-8"), indent=1)

    # 备份后写库
    bak = DB + ".bak_backfill_six_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, bak)
    print(f"备份: {bak}")

    conn = sqlite3.connect(DB, timeout=20)
    cur = conn.cursor()
    ts = datetime.now().isoformat(timespec="seconds")
    n = 0
    for aid, r in results.items():
        if "error" in r:
            continue
        sets, vals = ["updated_at=?"], [ts]
        for k in ("two_year_sharpe", "is_ladder_sharpe", "margin", "universe",
                  "neutralization", "platform_status", "stage"):
            if r.get(k) is not None:
                sets.append(f"{k}=?")
                vals.append(r[k])
        cur.execute(f"UPDATE alphas SET {', '.join(sets)} WHERE alpha_id=?", vals + [aid])
        n += cur.rowcount
    conn.commit()

    print("\n=== 写库后核验 ===")
    for aid in TARGETS:
        row = cur.execute(
            "SELECT alpha_id, sharpe, fitness, two_year_sharpe, margin, universe, "
            "platform_status, stage FROM alphas WHERE alpha_id=?", (aid,)).fetchone()
        print(f"  {row}")
    conn.close()
    print(f"\n更新 {n} 颗完成")


asyncio.run(main())
