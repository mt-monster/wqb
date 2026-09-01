# -*- coding: utf-8 -*-
"""精确统计各区域 ACTIVE alpha 池（按 settings.region 客户端过滤）。

坑：/users/self/alphas 的 region 参数服务端不支持（仅客户端过滤），
必须按每条记录的 settings.region 自行分组。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

OUT = WQ_ROOT / "research-data" / "active_pool_by_region.json"


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    rows = []
    offset = 0
    while True:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"limit": 100, "offset": offset, "status": "ACTIVE",
                    "order": "-dateSubmitted"},
        )
        if r.status_code != 200:
            print(f"[ERR] {r.status_code} {r.text[:200]}")
            break
        j = r.json()
        batch = j.get("results") or []
        rows.extend(batch)
        if j.get("next") is None or not batch:
            break
        offset += len(batch)
        if offset >= 1000:
            print("[warn] offset 达 1000 上限（平台硬限制），结果可能不全")
            break

    print(f"平台 ACTIVE 总数（offset<1000 区间内）: {len(rows)}")

    by_region = {}
    no_region = []
    for a in rows:
        st = a.get("settings") or {}
        reg = st.get("region")
        if not reg:
            no_region.append(a.get("id"))
            continue
        by_region.setdefault(reg, []).append(a)

    print(f"无 region 字段: {len(no_region)} 颗")
    print()
    print(f"{'region':<8}{'REGULAR':>9}{'SUPER':>7}{'合计':>7}")
    for reg in sorted(by_region, key=lambda k: -len(by_region[k])):
        lst = by_region[reg]
        nr = sum(1 for x in lst if x.get("type") != "SUPER")
        ns = sum(1 for x in lst if x.get("type") == "SUPER")
        print(f"{reg:<8}{nr:>9}{ns:>7}{len(lst):>7}")

    # IND 明细
    ind = by_region.get("IND", [])
    print(f"\n=== IND ACTIVE 明细 ({len(ind)}) ===")
    print(f"{'alpha_id':<10}{'type':<9}{'sharpe':>7}{'fit':>6}{'turn':>8}{'date':>12}  univ/neut/delay")
    regs_ind = []
    for a in sorted(ind, key=lambda x: str(x.get("dateSubmitted") or "")):
        isd = a.get("is") or {}
        st = a.get("settings") or {}
        is_super = a.get("type") == "SUPER"
        print(f"{a.get('id'):<10}{'SUPER' if is_super else 'REGULAR':<9}"
              f"{str(isd.get('sharpe')):>7}{str(isd.get('fitness')):>6}"
              f"{str(isd.get('turnover')):>8}{str(a.get('dateSubmitted'))[:10]:>12}  "
              f"{st.get('universe')}/{st.get('neutralization')}/d{st.get('delay')}")
        if not is_super:
            regs_ind.append({
                "alpha_id": a.get("id"),
                "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
                "turnover": isd.get("turnover"), "returns": isd.get("returns"),
                "dateSubmitted": a.get("dateSubmitted"),
                "universe": st.get("universe"),
                "neutralization": st.get("neutralization"),
                "delay": st.get("delay"),
            })

    print(f"\n>> IND 可用于 SA 的 REGULAR 组件: {len(regs_ind)} 颗")
    print(f">> 组新 SA 需要 >=10 颗；现有 SA E5l23mrm 已占 10 颗（selection=1 全选）")
    print(f">> 若池 <= 19 颗，则无法再凑出第二个不重叠的 10 颗集合")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "total": len(rows),
        "counts": {k: len(v) for k, v in by_region.items()},
        "ind_regular_pool": regs_ind,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
