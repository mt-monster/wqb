"""KOR SuperAlpha 可行性诊断：
1) 拉全 KOR REGULAR 池（跨 IS/OS 阶段），统计数量与构成
2) 识别是否够 >=10 个组件
3) 提示互相相关性风险（同族 -> 高 self_correlation）
"""
import asyncio, json, sys
sys.path.insert(0, 'world-quant-brain-mcp')
from brain_api import BrainApiClient

REGION = "KOR"

async def main():
    b = BrainApiClient()
    await b.ensure_authenticated()

    pool = []
    for stage in ["OS", "IS"]:
        off = 0
        while off < 950:  # platform caps offset window ~1000; recent KOR alphas near front
            d = await b.get_user_alphas(
                stage=stage, limit=50, alpha_type="REGULAR",
                order="-dateSubmitted", offset=off)
            res = d.get("results") or []
            if not res:
                break
            for r in res:
                s = r.get("settings") or {}
                if (s.get("region") or r.get("region")) != REGION:
                    continue
                pool.append({
                    "id": r["id"],
                    "stage": stage,
                    "name": r.get("name"),
                    "status": r.get("status"),
                    "type": r.get("type"),
                    "is": r.get("is") or {},
                    "sharpe": (r.get("is") or {}).get("sharpe"),
                    "fitness": (r.get("is") or {}).get("fitness"),
                    "dateSubmitted": r.get("dateSubmitted"),
                })
            if len(res) < 50:
                break  # last page
            off += 50

    # dedup by id (same alpha may appear? no, IS/OS distinct)
    by_stage = {}
    for a in pool:
        by_stage.setdefault(a["stage"], []).append(a)

    print(f"=== KOR REGULAR pool total: {len(pool)} ===")
    for st in ["OS", "IS"]:
        lst = by_stage.get(st, [])
        print(f"\n--- stage={st}: {len(lst)} ---")
        for a in lst:
            print(f"  {a['id']}  status={a['status']}  sharpe={a.get('sharpe')}  fitness={a.get('fitness')}  sub={a.get('dateSubmitted')}")

    # ACTIVE count (stage IS or OS both mean ACTIVE regular eligible as components)
    active = [a for a in pool if a["status"] == "ACTIVE" or a["stage"] in ("IS", "OS")]
    print(f"\n=== eligible (REGULAR/ACTIVE) count: {len(active)} (need >=10) ===")
    print("VERDICT:", "GO" if len(active) >= 10 else f"BLOCKED (need {10-len(active)} more)")

    with open("research-data/kor_sa_pool.json", "w") as f:
        json.dump(pool, f, ensure_ascii=False, indent=2, default=str)
    print("\nwrote research-data/kor_sa_pool.json")

asyncio.run(main())
