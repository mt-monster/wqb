import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
ALPHAS = sys.argv[1:] if len(sys.argv)>1 else []
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in ALPHAS:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        is_ = d.get("is") or {}
        m = is_.get("metrics") or {}
        print(f"{aid}: S={m.get('sharpe')} F={m.get('fitness')} T={m.get('turnover')} "
              f"RT={m.get('returns')} DD={m.get('drawdown')} MC={m.get('margin')} "
              f"LC={m.get('longCount')} SC={m.get('shortCount')} "
              f"checks={[(c.get('name'),c.get('result'),c.get('value'),c.get('limit')) for c in is_.get('checks',[])]}")
asyncio.run(main())
