import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
WAVES = {
 "SI3M (main族)":"3BUj3Ytc4Z8aUSMpe5tNcC",
 "SI5 isolate":"1ggjEleGh50ec8Q9hZ9xlO7",
 "SI3U (util深化)":"2pMINdbKM4U19hnojBKl0Lp",
}
async def main():
    from brain_api import brain_client
    from tools_ops import batch_status
    await brain_client.ensure_authenticated()
    r = await batch_status(list(WAVES.values()))
    for b in r.get("batches", []):
        nm = [k for k,v in WAVES.items() if v==b.get('batch_id')]
        print(f"\n== {nm[0] if nm else b.get('batch_id')} child={b.get('child_count')} term={b.get('all_terminal')} err={b.get('errors')}")
        for c in b.get("children",[]):
            print(f"   {str(c.get('status')):11s} alpha={c.get('alpha')} err={str(c.get('error'))[:60]}")
asyncio.run(main())
