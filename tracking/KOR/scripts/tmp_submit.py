# -*- coding: utf-8 -*-
"""提交 qMxaLJpv → POST /alphas/{id}/submit（三态响应 + 异步补发）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
AID = sys.argv[1] if len(sys.argv)>1 else "qMxaLJpv"
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    r = await brain_client._request("POST", f"https://api.worldquantbrain.com/alphas/{AID}/submit")
    print("STATUS", r.status_code)
    body = r.text.strip()
    print("BODY", body[:1500] if body else "(空体)")
    if r.status_code == 201 or (r.status_code==200 and not body):
        print("→ 已受理，轮询 status")
        for i in range(30):
            await asyncio.sleep(20)
            rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{AID}")
            d = rr.json()
            st = d.get("status")
            print(f"  poll{i}: status={st}")
            if st in ("ACTIVE","FAIL","ERROR"):
                is_ = d.get("is") or {}
                print("  checks:", json.dumps([{c.get('name'):c.get('result')} for c in is_.get('checks',[])], ensure_ascii=False))
                break
asyncio.run(main())
