# -*- coding: utf-8 -*-
"""收割 DEU 双塔 multi-sim 结果（两跳：children=sim_id -> GET sim -> alpha）。
用法: python tmp_harvest_deu.py
输出: tracking/DEU/candidates/wave_DEUDUAL_results.json
"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
CKPT = os.path.join(REPO, "tracking/DEU/candidates/wave_DEUDUAL_checkpoint.json")
OUT = os.path.join(REPO, "tracking/DEU/candidates/wave_DEUDUAL_results.json")


async def aid_of(bc, node):
    """node 可能是 alpha id 或 simulation id。"""
    if isinstance(node, dict):
        node = node.get("id") or node.get("alpha") or ""
    node = str(node)
    if not node:
        return None
    r = await bc._request("GET", f"https://api.worldquantbrain.com/simulations/{node}")
    if r.status_code != 200:
        return None
    d = r.json()
    if d.get("alpha"):
        return d["alpha"]
    if d.get("status") == "COMPLETE" and d.get("id") and not d.get("alpha"):
        return None
    return None


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    ck = json.load(open(CKPT, encoding="utf-8"))
    results = []
    for b in ck.get("done_batches", []):
        pid = b["progress_id"]
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{pid}")
        if r.status_code != 200:
            print(f"{b['label']} ERR {r.status_code}"); continue
        d = r.json()
        children = d.get("children") or []
        st = d.get("status")
        print(f"{b['label']} pid={pid} status={st} children={len(children)}")
        for i, ch in enumerate(children):
            aid = await aid_of(brain_client, ch)
            if not aid:
                continue
            rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
            if rr.status_code != 200:
                continue
            a = rr.json()
            is_ = a.get("is") or {}
            results.append({
                "label": b["ids"][i] if i < len(b["ids"]) else f"#{i}",
                "dataset": b.get("dataset"),
                "alpha_id": aid,
                "sharpe": is_.get("sharpe"), "fitness": is_.get("fitness"),
                "turnover": is_.get("turnover"), "margin": is_.get("margin"),
                "pyramids": a.get("pyramids"),
                "expr": b["exprs"][i] if i < len(b.get("exprs") or []) else None,
            })
            print(f"   {aid} S={is_.get('sharpe')} F={is_.get('fitness')} T={is_.get('turnover')} pyr={a.get('pyramids')}")
    json.dump(results, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nSAVED", OUT, "n=", len(results))
    # 排序展示
    ok = [x for x in results if (x.get("sharpe") or 0) >= 1.25]
    print(f"\nsharpe>=1.25: {len(ok)}/{len(results)}")
    for x in sorted(results, key=lambda z: -(z.get("sharpe") or -9))[:15]:
        print(f"  {x['alpha_id']} S={x['sharpe']} F={x['fitness']} T={x['turnover']} {x['label']}")


asyncio.run(main())
