# -*- coding: utf-8 -*-
"""查平台 EUR 区域 pattern_scores / 形态相似度 相关已存 alpha 的设置（学习既有成功配方）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    found = []
    off = 0
    while off < 300:
        r = await brain_client._request(
            "GET", f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={off}")
        if r.status_code != 200:
            print("ERR", r.status_code); break
        d = r.json()
        rs = d.get("results") or []
        if not rs:
            break
        for a in rs:
            reg = ((a.get("settings") or {}).get("region") or "")
            if reg != "EUR":
                continue
            expr = ((a.get("regular") or {}).get("code") or "")
            if not expr:
                continue
            if any(k in expr for k in ("similarity", "pattern", "wedge", "triangle", "reversal_",
                                        "breakaway", "gap_pattern")):
                s = a.get("settings") or {}
                is_ = a.get("is") or {}
                found.append({"id": a.get("id"), "S": is_.get("sharpe"), "F": is_.get("fitness"),
                              "T": is_.get("turnover"), "nu": s.get("neutralization"),
                              "decay": s.get("decay"), "uni": s.get("universe"),
                              "trunc": s.get("truncation"), "expr": expr[:180]})
        off += 100
        if not d.get("next"):
            break
    print(f"matched EUR pattern-like alphas: {len(found)}")
    found.sort(key=lambda x: -(x["S"] or -9))
    for f in found[:25]:
        print(json.dumps(f, ensure_ascii=False))


asyncio.run(main())
