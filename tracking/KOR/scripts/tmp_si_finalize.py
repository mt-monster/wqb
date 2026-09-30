# -*- coding: utf-8 -*-
"""SI-FINAL —— KOR Short Interest 专项收尾。

对 4 颗候选逐颗 POST /submit，读取平台真值：
  - 201 空体 → 已受理，轮询 status 直到 ACTIVE/FAIL
  - 403 + checks → 取全量 checks；区分 REGULAR_SUBMISSION 配额撞顶 vs 真实闸失败
输出落台账 tracking/KOR/candidates/wave_SIFINAL_ledger.json
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

CANDS = ["KPNo2lgl", "E5pjx9q0", "mLmGQEq9", "d5bMPkWY"]
LEDGER = os.path.join(REPO, "tracking/KOR/candidates/wave_SIFINAL_ledger.json")


async def post_submit(bc, aid):
    r = await bc._request("POST", f"https://api.worldquantbrain.com/alphas/{aid}/submit")
    body = r.text.strip()
    out = {"id": aid, "post_status": r.status_code, "ts": time.strftime("%Y-%m-%d %H:%M:%S")}
    if r.status_code in (200, 201) and not body:
        out["accepted"] = True
    else:
        out["accepted"] = False
        try:
            out["checks"] = r.json().get("is", {}).get("checks", [])
        except Exception:
            out["raw"] = body[:500]
    return out


async def poll(bc, aid, n=25):
    for i in range(n):
        await asyncio.sleep(20)
        rr = await bc._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = rr.json()
        st = d.get("status")
        if st in ("ACTIVE", "FAIL", "ERROR"):
            is_ = d.get("is") or {}
            return st, {c.get("name"): c.get("result") for c in is_.get("checks", [])}
    return "TIMEOUT", {}


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    led = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "region": "KOR", "dataset": "shrt38",
           "theme": "SHORT_INTEREST", "results": []}
    for aid in CANDS:
        # 先读当前状态
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        cur = d.get("status")
        if cur == "ACTIVE":
            print(f"{aid}: 已 ACTIVE，跳过")
            led["results"].append({"id": aid, "final": "ACTIVE", "note": "已于本日提交成功"})
            continue
        print(f"{aid}: 当前 {cur} → POST submit")
        res = await post_submit(brain_client, aid)
        if res["accepted"]:
            st, chk = await poll(brain_client, aid)
            res["final"] = st
            res["final_checks"] = chk
            print(f"   → {st}")
        else:
            fails = [c for c in res.get("checks", []) if c.get("result") == "FAIL"]
            res["final"] = "BLOCKED"
            res["fails"] = [f.get("name") for f in fails]
            for f in fails:
                print(f"   FAIL {f.get('name')}: value={f.get('value')} limit={f.get('limit')}")
        led["results"].append(res)
        await asyncio.sleep(2)
    with open(LEDGER, "w", encoding="utf-8") as f:
        json.dump(led, f, ensure_ascii=False, indent=1)
    print("LEDGER saved:", LEDGER)


asyncio.run(main())
