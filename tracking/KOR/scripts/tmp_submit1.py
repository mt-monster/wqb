# -*- coding: utf-8 -*-
"""单颗提交 + 403/201 判读 + 轮询状态。用法: python tmp_submit1.py <alpha_id>
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


async def main():
    aid = sys.argv[1]
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    r = await brain_client._request("POST", f"https://api.worldquantbrain.com/alphas/{aid}/submit")
    body = r.text.strip()
    print(f"POST {aid} -> {r.status_code} body_len={len(body)}")
    if r.status_code in (200, 201) and not body:
        print("  (空体=已受理，补发确认)")
        await asyncio.sleep(5)
        r2 = await brain_client._request("POST", f"https://api.worldquantbrain.com/alphas/{aid}/submit")
        print(f"  补发 {r2.status_code}: {r2.text.strip()[:300]}")
    elif body:
        try:
            j = r.json()
            for c in (j.get("is") or {}).get("checks", []):
                if c.get("result") != "PASS":
                    print("  ", json.dumps(c, ensure_ascii=False))
        except Exception:
            print("  ", body[:400])
    # 轮询状态
    for i in range(30):
        await asyncio.sleep(20)
        rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        st = rr.json().get("status")
        print(f"  [{i*20}s] status={st}")
        if st in ("ACTIVE", "FAIL", "REJECTED"):
            break


asyncio.run(main())
