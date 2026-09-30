import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
ALPHAS = sys.argv[1:]
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in ALPHAS:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        is_ = d.get("is") or {}
        ck = {c.get("name"):(c.get("result"),c.get("value"),c.get("limit")) for c in is_.get("checks",[])}
        def g(n): return ck.get(n,("?","?","?"))
        print(f"{aid} | S={g('LOW_SHARPE')[1]}({g('LOW_SHARPE')[0]}) "
              f"2Y={g('LOW_2Y_SHARPE')[1]}({g('LOW_2Y_SHARPE')[0]}) "
              f"F={g('LOW_FITNESS')[1]}({g('LOW_FITNESS')[0]}) "
              f"CW={g('CONCENTRATED_WEIGHT')[1]}({g('CONCENTRATED_WEIGHT')[0]}) "
              f"SUB={g('LOW_SUB_UNIVERSE_SHARPE')[1]}({g('LOW_SUB_UNIVERSE_SHARPE')[0]}) "
              f"| {str(d.get('regular',{}).get('code'))[:60]}")
asyncio.run(main())
