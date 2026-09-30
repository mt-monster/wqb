import asyncio,json,sys,os
sys.path.insert(0,r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    r = await brain_client.get_datafields(region="KOR", universe="TOP600", delay=1, dataset_id="risk59", filter_sharpe=False)
    res = r.get("results", r) if isinstance(r, dict) else r
    print("n=", len(res) if res else 0)
    for f in (res or []):
        print(f"  {f.get('id'):44s} {str(f.get('type')):10s} cov={f.get('coverage')} u={f.get('userCount')} a={f.get('alphaCount')} | {str(f.get('description',''))[:55]}")
    # dataset meta
    r2 = await brain_client.get_datasets(region="KOR", universe="TOP600", delay=1)
    for d in (r2.get("results", r2) if isinstance(r2,dict) else r2):
        if str(d.get("id"))=="risk59":
            print("META risk59:", {k:d.get(k) for k in ('id','category','coverage','userCount','alphaCount','fieldCount','pyramidMultiplier')})
asyncio.run(main())
