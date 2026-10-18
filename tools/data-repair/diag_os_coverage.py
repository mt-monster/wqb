"""诊断 OS 实盘数据覆盖 + 验证 osISSharpeRatio 字段（只读）。"""
import os
import sys
import asyncio
import json
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
WQB = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(WQB, "world-quant-brain-mcp"))
from brain_api import BrainApiClient
sys.path.insert(0, os.path.join(WQB, "src"))
from wqb.db_conn import connect as db_connect

DB = os.path.join(WQB, "data", "wqb.db")

con = db_connect(DB, readonly=True)
print("=== DB os_sharpe 覆盖（按区） ===")
for r in con.execute(
    "SELECT r.name reg, COUNT(*) n FROM alphas a JOIN regions r ON a.region_id=r.id "
    "WHERE a.os_sharpe IS NOT NULL GROUP BY r.name ORDER BY n DESC"):
    print(f"  {r[0]:>5}: {r[1]} 颗有 os_sharpe")

usa_ids = [r[0] for r in con.execute(
    "SELECT a.alpha_id FROM alphas a JOIN regions r ON a.region_id=r.id "
    "WHERE a.os_sharpe IS NOT NULL AND r.name='USA' LIMIT 3")]
print("\n=== 抽样 3 颗有旧 os_sharpe 的 USA alpha ===")
print("  ids:", usa_ids)
con.close()


async def main():
    b = BrainApiClient()
    await b.ensure_authenticated()
    for aid in usa_ids:
        a = await b.get_alpha_details(aid)
        st = a.get("settings") or {}
        isd = a.get("is") or {}
        osd = a.get("os") or {}
        is_sh = isd.get("sharpe")
        ratio = osd.get("osISSharpeRatio")
        preclose = osd.get("preCloseSharpeRatio")
        os_sh = (is_sh * ratio) if (is_sh and ratio) else None
        print(f"  {aid} {st.get('region')} dateSubmitted={a.get('dateSubmitted')} "
              f"IS_sh={is_sh} osISSharpeRatio={ratio} preCloseSharpeRatio={preclose} "
              f"=> OS_sh≈{round(os_sh,3) if os_sh else None}")
    # 再抽 3 颗非 USA、提交最早的 ACTIVE alpha 看是否有比值
    print("\n=== 抽样各非 USA 区提交最早的 ACTIVE alpha 的 osISSharpeRatio ===")
    con = db_connect(DB, readonly=True)
    for reg in ["IND", "KOR", "GLB", "GBR", "DEU"]:
        row = con.execute(
            "SELECT a.alpha_id, a.date_submitted FROM alphas a JOIN regions r ON a.region_id=r.id "
            "WHERE r.name=? AND a.platform_status='ACTIVE' AND a.date_submitted IS NOT NULL "
            "ORDER BY a.date_submitted ASC LIMIT 1", (reg,)).fetchone()
        if not row:
            print(f"  {reg}: 无 ACTIVE 提交记录")
            continue
        aid = row[0]
        a = await b.get_alpha_details(aid)
        st = a.get("settings") or {}
        isd = a.get("is") or {}
        osd = a.get("os") or {}
        is_sh = isd.get("sharpe")
        ratio = osd.get("osISSharpeRatio")
        os_sh = (is_sh * ratio) if (is_sh and ratio) else None
        print(f"  {reg} {aid} submitted={row[1]} IS_sh={is_sh} osISSharpeRatio={ratio} => OS_sh≈{round(os_sh,3) if os_sh else None}")
    con.close()

asyncio.run(main())
