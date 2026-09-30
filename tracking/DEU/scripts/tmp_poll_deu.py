import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    ck = json.load(open(os.path.join(REPO,"tracking/DEU/candidates/wave_DEUDUAL_checkpoint.json"),encoding="utf-8"))
    for b in ck["done_batches"]:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{b['progress_id']}")
        d = r.json()
        print(f"{b['label']:12s} status={d.get('status')} children={len(d.get('children') or [])} progress={d.get('progress')}")
asyncio.run(main())
