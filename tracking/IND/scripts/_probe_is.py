import asyncio, sys, json
sys.path.insert(0, "world-quant-brain-mcp")
from brain_api import brain_client as brain

async def main(aid):
    await brain.ensure_authenticated()
    r = await brain._request("GET", f"{brain.base_url}/alphas/{aid}")
    d = r.json()
    isd = d.get("is") or {}
    print("top keys:", list(d.keys()))
    print("is keys:", list(isd.keys()))
    for k in ("sharpe","fitness","turnover","two_year_sharpe","sub_universe_sharpe",
              "robust_universe_sharpe","margin","selfCorrelation","prodCorrelation",
              "self_correlation","prod_correlation","longCount","shortCount"):
        if k in isd: print(f"  {k} = {isd[k]}")
    print("checks:", [(c.get('name'), c.get('result')) for c in (isd.get('checks') or [])])

asyncio.run(main(sys.argv[1]))
