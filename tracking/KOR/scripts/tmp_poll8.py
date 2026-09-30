import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
W = {"X1":"2KpHMh4Fq4GkazeDvOIfc6F","X2":"XzrJlnO4OIcfWpy7albtP","X3":"PTQpc2Kc4Ajcbo1hAXOyI9F",
     "E_d30":"40BWuIchC4CWbLszXhDeQ4M","E_d40":"1MiiDqe5L4KIaDuYOdsfOvY","E_d60":"4fBqOM34V4uc9zC166Ptueqa","E_t02":"4EINdUdq65e59IbyIR1GOkK"}
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
