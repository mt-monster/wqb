# -*- coding: utf-8 -*-
"""零成本 prod 预检：POST /submit 读 403 checks。配额满时 REGULAR_SUBMISSION FAIL 会遮住 PROD，
故先看有无 PROD_CORRELATION 真值；若无则记录'配额遮挡'。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
IDS = sys.argv[1:]
KEY = ("SELF_CORRELATION","PROD_CORRELATION","POWER_POOL_CORRELATION","REGULAR_SUBMISSION",
       "POWER_POOL_SUBMISSION","POWER_POOL_MONTHLY_SUBMISSION","LOW_SUB_UNIVERSE_SHARPE","CONCENTRATED_WEIGHT")
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in IDS:
        r = await brain_client._request("POST", f"https://api.worldquantbrain.com/alphas/{aid}/submit")
        body = r.text.strip()
        print(f"=== {aid} POST {r.status_code} {'(空体=已受理)' if not body else ''}")
        if body:
            try:
                chks = r.json().get("is",{}).get("checks",[])
            except Exception:
                chks=[]
            for c in chks:
                if c.get("name") in KEY:
                    print("   ", json.dumps(c, ensure_ascii=False))
        await asyncio.sleep(2)
asyncio.run(main())
