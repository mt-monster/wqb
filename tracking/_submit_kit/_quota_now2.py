# -*- coding: utf-8 -*-
"""配额实时核对 v2：尾部提交记录 + 实时已提交 alpha 列表 + 本地 DB ledger。"""
import asyncio
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
ET = timezone(timedelta(hours=-4))


def now_et():
    return datetime.now(ET)


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    ne = now_et()
    day_start = ne.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)
    print(f"[now] GMT+8={datetime.now():%Y-%m-%d %H:%M:%S}  ET={ne:%Y-%m-%d %H:%M:%S} ET")
    print(f"[ET 日] {day_start:%Y-%m-%d} 00:00 ~ {day_end:%Y-%m-%d} 00:00 ET")

    # 1) 尾部提交记录
    print("\n=== activities/submissions 尾部 20 条 ===")
    r = await brain._request(
        "GET", f"{brain.base_url}/users/self/activities/submissions",
        params={"grouping": "SUBMISSION"},
    )
    j = r.json()
    recs = ((j.get("records") or {}).get("records") or [])
    for x in recs[-20:]:
        # 统计今天 ET 日
        try:
            dt = datetime.fromisoformat(x[0].replace("Z", "+00:00")).astimezone(ET)
            tag = " <<TODAY" if day_start <= dt < day_end else ""
        except Exception:
            dt, tag = None, ""
        print(f"   {x}  ({dt:%Y-%m-%d %Z if dt else '?'}{tag})")

    def in_day(x):
        try:
            d = datetime.fromisoformat(x[0].replace('Z', '+00:00')).astimezone(ET)
            return day_start <= d < day_end
        except Exception:
            return False
    today_rec = [x for x in recs if in_day(x)]
    print(f"   => 今天 ET 日记录: {today_rec}  (合计 {sum(x[1] for x in today_rec)} 次)")

    # 2) 实时已提交 alpha（不分状态，按 dateSubmitted 倒序取近 40 条）
    print("\n=== /users/self/alphas 最近提交（按 dateSubmitted 倒序） ===")
    try:
        r2 = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"limit": 60, "offset": 0, "type": "REGULAR"},
        )
        j2 = r2.json()
        arr = j2.get("records") or j2.get("alphas") or []
        print(f"  REGULAR 总数（limit60）={len(arr)}")
        cnt_today_reg = cnt_today_sup = 0
        rows = []
        for a in arr:
            sets = a.get("settings") or {}
            typ = a.get("type") or sets.get("type") or "REGULAR"
            ds = a.get("dateSubmitted") or a.get("submittedDate")
            if ds:
                try:
                    dt = datetime.fromisoformat(ds.replace("Z", "+00:00")).astimezone(ET)
                except Exception:
                    dt = None
            else:
                dt = None
            rows.append((a.get("id"), typ, sets.get("region"), ds, dt))
        # 按 dateSubmitted 倒序
        rows.sort(key=lambda r: r[4] or datetime.min.replace(tzinfo=ET), reverse=True)
        for rid, typ, reg, ds, dt in rows[:25]:
            istoday = (dt and day_start <= dt < day_end)
            if istoday:
                if typ == "SUPER":
                    cnt_today_sup += 1
                else:
                    cnt_today_reg += 1
            print(f"   {rid:12s} {typ:8s} {str(reg):4s} ds={ds} {'<<TODAY' if istoday else ''}")
        print(f"  => 今天 ET 日: REGULAR={cnt_today_reg}  SUPER={cnt_today_sup}")
    except Exception as e:
        print(f"  ERR {e}")

    # 3) 本地 DB ledger
    print("\n=== 本地 DB submission_ledger（今天 ET 日） ===")
    try:
        import sqlite3
        db = WQ_ROOT / "data" / "wqb.db"
        con = sqlite3.connect(str(db))
        cur = con.cursor()
        # 找表
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabs = [r[0] for r in cur.fetchall()]
        print(f"  tables={tabs}")
        for t in ("submission_ledger", "alphas"):
            if t not in tabs:
                continue
            q = f"PRAGMA table_info({t})"
            cur.execute(q)
            cols = [c[1] for c in cur.fetchall()]
            print(f"  [{t}] cols={cols}")
            # 尝试按日期列过滤
            datecol = None
            for cand in ("date_submitted", "submitted_date", "dateSubmitted", "date", "ts"):
                if cand in cols:
                    datecol = cand
                    break
            if datecol:
                cur.execute(f"SELECT * FROM {t} WHERE {datecol} >= ? ORDER BY {datecol} DESC LIMIT 20",
                            (day_start.strftime("%Y-%m-%d"),))
                for row in cur.fetchall():
                    print(f"    {row}")
        con.close()
    except Exception as e:
        print(f"  ERR {e}")


if __name__ == "__main__":
    asyncio.run(main())
