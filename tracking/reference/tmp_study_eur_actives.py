# -*- coding: utf-8 -*-
"""学习 EUR 已 ACTIVE alpha 的 2Y 表现与表达式写法（用户要求的"先看别人怎么设计"）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    rows=[]; off=0
    while off < 600:
        r = await brain_client._request("GET", f"https://www.worldquantbrain.com/users/self/alphas?limit=100&offset={off}")
        if r.status_code != 200:
            r = await brain_client._request("GET", f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={off}")
        if r.status_code != 200: print("ERR",r.status_code); break
        d=r.json(); rs=d.get("results") or []
        if not rs: break
        rows+=rs
        if not d.get("next"): break
        off+=100
    print("total alphas:",len(rows))
    eur=[a for a in rows if ((a.get("settings") or {}).get("region")=="EUR")]
    print("EUR alphas:",len(eur))
    # 收集 ACTIVE 的
    act=[a for a in eur if a.get("status")=="ACTIVE"]
    print("EUR ACTIVE:",len(act))
    for a in act[:25]:
        s=a.get("settings") or {}; i=a.get("is") or {}
        chk={c["name"]:(c.get("result"),c.get("value")) for c in i.get("checks",[])}
        y2=chk.get("LOW_2Y_SHARPE")
        print(f"  {a.get('id')} S={i.get('sharpe')} F={i.get('fitness')} 2Y={y2} nu={s.get('neutralization')} d={s.get('decay')} u={s.get('universe')}")
        print(f"     expr: {str((a.get('regular') or {}).get('code'))[:150]}")
asyncio.run(main())
