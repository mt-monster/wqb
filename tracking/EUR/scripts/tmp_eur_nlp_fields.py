import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def fetch(bc, ds, region="EUR", uni="TOPCS1600"):
    rows=[]; off=0
    while True:
        url=(f"https://api.worldquantbrain.com/data-fields?instrumentType=EQUITY&region={region}"
             f"&delay=1&universe={uni}&dataset.id={ds}&limit=50&offset={off}")
        r = await bc._request("GET", url)
        if r.status_code != 200:
            print(f"[{ds}] ERR {r.status_code} {r.text[:120]}"); return rows
        d=r.json(); rs=d.get("results") or []; rows.extend(rs)
        if not rs or off+50>=(d.get("count") or 0): break
        off+=50
    return rows
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for ds in ["news_sentiment_nlp","news_sentiment_dl"]:
        rows = await fetch(brain_client, ds)
        print(f"\n=== {ds}: {len(rows)} fields ===")
        for x in rows[:30]:
            print(f"  {x.get('id'):42s} {x.get('type'):8s} cov={(x.get('coverage') or 0):.3f} u={x.get('userCount')} a={x.get('alphaCount')}")
asyncio.run(main())
