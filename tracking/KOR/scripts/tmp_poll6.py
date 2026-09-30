import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
W = {"G1":"1KJCn33yP4UmawzkXUtYuRA","G2":"NjtNcqu4oQbKbK4mkXmQ9","G3":"3O8dcob3L4TdciWfiatrxPM",
     "G4":"3pmYeBaxL59fcao17Aa9Mhjb","G5":"47ApLVeGe4IAcuXJMLlUEe9"}
async def main():
    from brain_api import brain_client
    from tools_ops import batch_status
    await brain_client.ensure_authenticated()
    r = await batch_status(list(W.values()))
    for b in r.get("batches", []):
        nm=[k for k,v in W.items() if v==b.get('batch_id')]
        print(f"== {nm[0] if nm else b.get('batch_id')} child={b.get('child_count')} term={b.get('all_terminal')}")
        for c in b.get("children",[]):
            print(f"   {str(c.get('status')):11s} alpha={c.get('alpha')}")
asyncio.run(main())
