import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in sys.argv[1:]:
        try:
            from tools_ops import submit_verdict
            r = await submit_verdict(aid)
            print(f"\n=== {aid} ===")
            print(json.dumps(r, ensure_ascii=False, indent=1)[:2600])
        except Exception as e:
            print(f"{aid} ERR {type(e).__name__}: {e}")
asyncio.run(main())
