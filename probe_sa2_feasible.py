import asyncio, json, sys
from collections import Counter
sys.path.insert(0, 'world-quant-brain-mcp')
from brain_api import BrainApiClient

async def main():
    b = BrainApiClient()
    await b.ensure_authenticated()

    # 1) 配额
    try:
        q = await b.get_submission_quota()
        print("=== QUOTA ===")
        print(json.dumps({k: q.get(k) for k in ("remaining","daily_remaining","daily_reset_utc","earliest_release_utc")}, ensure_ascii=False, default=str))
    except Exception as e:
        print("quota ERROR:", repr(e))

    # 2) REGULAR OS 池（按 region 统计）
    print("\n=== REGULAR OS pool by region ===")
    all_regs = []
    for offset in range(0, 400, 100):
        d = await b.get_user_alphas(stage="OS", limit=100, offset=offset, alpha_type="REGULAR", order="-dateSubmitted")
        res = d.get("results", [])
        if not res: break
        all_regs += res
    print("total REGULAR OS fetched:", len(all_regs))
    reg_by_region = Counter()
    mea_ids = []
    for r in all_regs:
        reg = r.get("region")
        reg_by_region[reg or "UNKNOWN"] += 1
        if (reg or "").upper() == "MEA":
            mea_ids.append(r.get("id"))
    print("by region:", dict(reg_by_region))
    print("MEA REGULAR OS count:", len(mea_ids))
    print("MEA ids:", mea_ids)

    # 3) 现有 MEA SA 3qlYKAaO 用的组件
    print("\n=== 3qlYKAaO components ===")
    try:
        d = await b.get_alpha_details("3qlYKAaO")
        comps = d.get("components") or d.get("componentAlphas") or []
        print("component field type:", type(comps).__name__, "len:", len(comps) if isinstance(comps, list) else "n/a")
        # 尝试提取 id
        comp_ids = []
        if isinstance(comps, list):
            for c in comps:
                if isinstance(c, dict):
                    comp_ids.append(c.get("id") or c.get("alphaId") or c.get("alpha_id"))
                else:
                    comp_ids.append(str(c))
        print("component ids:", comp_ids)
        # 也打印所有 key 看看有没有组件相关字段
        keys = [k for k in d.keys() if any(t in k.lower() for t in ("component","child","member","constitu"))]
        print("component-related keys in detail:", keys)
    except Exception as e:
        print("detail ERROR:", repr(e))

asyncio.run(main())
