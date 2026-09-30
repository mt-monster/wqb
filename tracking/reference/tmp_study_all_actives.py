# -*- coding: utf-8 -*-
"""统计全区域 ACTIVE alpha 分布 + 各区域最佳 2Y（学习哪些区域/设置能过 2Y）。"""
import asyncio, json, sys, os
from collections import defaultdict
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    rows=[]; off=0
    while off < 2000:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={off}")
        if r.status_code != 200: break
        d=r.json(); rs=d.get("results") or []
        if not rs: break
        rows+=rs
        if not d.get("next"): break
        off+=100
    print("total:",len(rows))
    st=defaultdict(lambda: defaultdict(int))
    for a in rows:
        reg=(a.get("settings") or {}).get("region") or "?"
        st[reg][a.get("status")]+=1
    for reg in sorted(st):
        d=st[reg]
        print(f"  {reg:6s} total={sum(d.values()):4d} ACTIVE={d.get('ACTIVE',0):3d}  " +
              " ".join(f"{k}={v}" for k,v in sorted(d.items(), key=lambda x:-x[1])[:5]))
    # 所有 ACTIVE 的 2Y + 表达式
    print("\n=== ACTIVE alphas (all regions) ===")
    n=0
    for a in rows:
        if a.get("status")!="ACTIVE": continue
        s=a.get("settings") or {}; i=a.get("is") or {}
        chk={c["name"]:(c.get("result"),c.get("value")) for c in i.get("checks",[])}
        n+=1
        print(f"  {a.get('id')} {s.get('region')}/{s.get('universe')}/d{s.get('decay')}/{s.get('neutralization')} "
              f"S={i.get('sharpe')} F={i.get('fitness')} 2Y={chk.get('LOW_2Y_SHARPE')}")
        print(f"     {str((a.get('regular') or {}).get('code'))[:130]}")
    print("ACTIVE count:",n)
asyncio.run(main())
