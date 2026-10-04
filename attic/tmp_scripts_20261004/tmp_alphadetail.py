import asyncio, os, sys, json
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in sys.argv[1:]:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        if r.status_code != 200:
            print(aid, "HTTP", r.status_code); continue
        d = r.json()
        is_ = d.get("is", {}) or {}
        print(f"=== {aid} ===")
        print("  checks:")
        for c in is_.get("checks", []):
            print(f"    {c['name']:32s} {c.get('result'):8s} {c.get('value')} (limit {c.get('limit')})")
        print("  prod_corr in checks?", [c for c in is_.get("checks", []) if 'CORRELATION' in c['name'].upper()])
asyncio.run(main())
