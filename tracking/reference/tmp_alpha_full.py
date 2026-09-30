# -*- coding: utf-8 -*-
"""打印 alpha 完整 IS 指标 + checks + 年度统计。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    aid = sys.argv[1]
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
    a = r.json()
    is_ = a.get("is") or {}
    print("status:", a.get("status"))
    print("checks:")
    for c in is_.get("checks", []):
        print(f"  {c.get('name'):32s} {c.get('result'):8s} value={c.get('value')} limit={c.get('limit')}")
    print("metrics:", json.dumps({k: is_.get(k) for k in
        ("sharpe","fitness","turnover","returns","drawdown","margin","longCount","shortCount")},
        ensure_ascii=False))
    print("settings:", json.dumps(a.get("settings"), ensure_ascii=False))
    print("pyramids:", json.dumps(a.get("pyramids"), ensure_ascii=False)[:400])
    # yearly
    r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/recordsets/yearly-stats")
    if r2.status_code == 200:
        y = r2.json()
        for row in (y.get("records") or []):
            print("  year:", row)
asyncio.run(main())
