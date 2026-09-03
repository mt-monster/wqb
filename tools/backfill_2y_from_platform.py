# -*- coding: utf-8 -*-
"""回填 v2：two_year_sharpe 从 is.checks 的 LOW_2Y_SHARPE.value 提取（PASS 的 value 也可用）。

关键发现：
- 平台 is 段无独立 twoYearSharpe 字段；2Y 数值藏在 is.checks 的 LOW_2Y_SHARPE.value。
- PASS 状态的 check 也可能带 value（qMja95Q2 的 IS_LADDER_SHARPE=2.97 就是 PASS 且有值）。
- 顺带回填 IS_LADDER_SHARPE（is_ladder_sharpe 列）。
"""
import asyncio
import json
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
TARGETS = r"D:\coding\traeCN_project\wqb\logs\_backfill_2y_targets.json"


async def main():
    from brain_api import BrainApiClient

    targets = [t["alpha_id"] for t in json.load(open(TARGETS, encoding="utf-8"))]
    print(f"待拉取 {len(targets)} 颗")

    brain = BrainApiClient()
    await brain.ensure_authenticated()

    results = {}
    ok2y = okladder = 0
    for i, aid in enumerate(targets):
        try:
            d = await brain.get_alpha_details(aid)
            checks = (d.get("is") or {}).get("checks") or []
            two_y = ladder = None
            for c in checks:
                name = c.get("name")
                val = c.get("value")
                if val is None:
                    continue
                if name == "LOW_2Y_SHARPE":
                    two_y = val
                elif name == "IS_LADDER_SHARPE":
                    ladder = val
            results[aid] = {"two_year_sharpe": two_y, "is_ladder_sharpe": ladder}
            if two_y is not None:
                ok2y += 1
            if ladder is not None:
                okladder += 1
        except Exception as e:
            results[aid] = {"error": str(e)[:150]}
        if (i + 1) % 20 == 0:
            print(f"  进度 {i+1}/{len(targets)} 2Y={ok2y} ladder={okladder}")

    print(f"拉取完成: 2Y={ok2y}/{len(targets)} ladder={okladder}/{len(targets)}")
    json.dump(results, open(r"D:\coding\traeCN_project\wqb\logs\_backfill_2y_results.json", "w", encoding="utf-8"), indent=1)

    # 写库
    conn = sqlite3.connect(DB, timeout=15)
    cur = conn.cursor()
    ts = datetime.now().isoformat(timespec="seconds")
    n = 0
    for aid, r in results.items():
        if "error" in r:
            continue
        sets, vals = ["updated_at=?"], [ts]
        for k in ("two_year_sharpe", "is_ladder_sharpe"):
            if r.get(k) is not None:
                sets.append(f"{k}=?")
                vals.append(r[k])
        cur.execute(f"UPDATE alphas SET {', '.join(sets)} WHERE alpha_id=?", vals + [aid])
        n += cur.rowcount
    conn.commit()
    r2 = cur.execute(
        "SELECT COUNT(*), SUM(CASE WHEN two_year_sharpe IS NOT NULL THEN 1 ELSE 0 END), "
        "SUM(CASE WHEN is_ladder_sharpe IS NOT NULL THEN 1 ELSE 0 END) "
        "FROM alphas WHERE platform_status='UNSUBMITTED' AND stage='IS'"
    ).fetchone()
    conn.close()
    print(f"写库更新 {n} 颗")
    print(f"IS 层现状: 总量={r2[0]} 2Y有值={r2[1]} ladder有值={r2[2]}")


asyncio.run(main())
