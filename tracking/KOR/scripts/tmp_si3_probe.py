import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    # 数据集元信息
    try:
        r = await brain_client.get_datasets(region="KOR", universe="TOP600", delay=1)
        res = r.get("results", r) if isinstance(r, dict) else r
        for d in res:
            if str(d.get("id","")).startswith("shortinterest"):
                print(f"{d.get('id'):22s} cat={d.get('category',{}).get('name') if isinstance(d.get('category'),dict) else d.get('category')}  alphaCnt={d.get('alphaCount')}  fields={d.get('fieldCount')}  cov={d.get('coverage')}  users={d.get('userCount')}  mult={d.get('pyramidMultiplier')}")
    except Exception as e:
        print("dataset ERR", e)
asyncio.run(main())
