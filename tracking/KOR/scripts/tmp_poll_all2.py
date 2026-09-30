import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    pids = sys.argv[1:]
    for _ in range(40):
        done=0
        states=[]
        for pid in pids:
            r = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{pid}")
            d=r.json(); st=d.get("status")
            ch=d.get("children") or []
            states.append(f"{pid[:8]}={st}/{len(ch)}")
            if st in ("COMPLETE","ERROR","FAIL"): done+=1
        print(" | ".join(states))
        if done==len(pids): break
        await asyncio.sleep(15)
asyncio.run(main())
