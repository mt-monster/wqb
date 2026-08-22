import asyncio, json, sys
sys.path.insert(0, 'world-quant-brain-mcp')
from brain_api import BrainApiClient

async def main():
    b = BrainApiClient()
    await b.ensure_authenticated()
    ids = ["3qlYKAaO", "A1lb2KpR", "88lr21xo"]
    for aid in ids:
        try:
            d = await b.get_alpha_details(aid)
        except Exception as e:
            print(aid, "ERROR", repr(e)); continue
        print("="*70)
        print("id:", aid)
        print("name:", d.get("name"))
        print("type:", d.get("type"), "| status:", d.get("status"), "| stage:", d.get("stage"), "| region:", d.get("region"))
        print("dateCreated:", d.get("dateCreated"), "| dateSubmitted:", d.get("dateSubmitted"))
        print("settings:", json.dumps(d.get("settings", {}), ensure_ascii=False))
        expr = d.get("regular") or d.get("combo") or d.get("selection") or (d.get("code") or {})
        # 取表达式
        for k in ("regular","combo","selection","expression"):
            if d.get(k):
                print(f"[{k}]:", str(d.get(k))[:300])
        print("is:", json.dumps(d.get("is", {}), ensure_ascii=False)[:400])
        print("os:", json.dumps(d.get("os", {}), ensure_ascii=False)[:400])

asyncio.run(main())
