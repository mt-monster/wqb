import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
WAVES = {"SI38AGG":"3CL18C5K25hcc0v9P9wJ5ct","RSK59B_a":"3Ag2ARcy54TG9q917P1fV9Qb","RSK59B_b":"15D7pP7Sq4yabRQbTFrlmXf"}
async def main():
    from brain_api import brain_client
    from tools_ops import batch_status
    await brain_client.ensure_authenticated()
    r = await batch_status(list(WAVES.values()))
    for b in r.get("batches", []):
        nm = [k for k,v in WAVES.items() if v==b.get('batch_id')]
        print(f"\n== {nm[0] if nm else b.get('batch_id')} child={b.get('child_count')} term={b.get('all_terminal')}")
        for c in b.get("children",[]):
            print(f"   {str(c.get('status')):11s} alpha={c.get('alpha')} err={str(c.get('error'))[:50]}")
asyncio.run(main())
