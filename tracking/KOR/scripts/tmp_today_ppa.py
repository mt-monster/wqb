# -*- coding: utf-8 -*-
"""查今日（ET）已提交的 PP alpha（验证单日 limit=1 假说）。"""
import asyncio, json, sys, os
from datetime import datetime, timedelta, timezone
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    # ET = UTC-4（夏令时）
    et = timezone(timedelta(hours=-4))
    now = datetime.now(et)
    start = now.strftime("%Y-%m-%d")
    end = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"ET 今天: {start}")
    out=[]; off=0
    while True:
        url = (f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={off}"
               f"&status!=UNSUBMITTED%1FIS_FAIL"
               f"&dateSubmitted%3E={start}T00:00:00-04:00"
               f"&dateSubmitted%3C{end}T00:00:00-04:00")
        r = await brain_client._request('GET', url)
        if r.status_code != 200:
            print('HTTP', r.status_code, r.text[:200]); break
        j=r.json(); res=j.get('results',[])
        out.extend(res)
        if len(out)>=j.get('count',0) or not res: break
        off+=100
    print(f"今日已提交: {len(out)}")
    for a in out:
        ids=[c.get('id') for c in a.get('classifications',[])]
        has_pp=any('POWER_POOL' in i for i in ids)
        has_reg=any('REGULAR' in i for i in ids)
        tag = 'PP+REG' if (has_pp and has_reg) else ('纯PP' if has_pp else ('REGULAR' if has_reg else 'other'))
        print(f"  {a.get('id')} | {a['settings'].get('region')}/{a['settings'].get('delay')} | {tag} | {a.get('name')} | {a.get('dateSubmitted')}")

asyncio.run(main())
