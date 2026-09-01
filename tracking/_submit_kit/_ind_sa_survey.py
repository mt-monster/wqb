# -*- coding: utf-8 -*-
"""IND 组 SA 前的完整现状核实（只读）：

1) 平台上 IND 全部 ACTIVE alpha（按 alpha_type 分 REGULAR / SUPER）
2) 每个已有 SUPER alpha 的 selection / combo 表达式（看是否吞掉全池）
3) SUPER_SUBMISSION 配额
4) 本地 DB 的 IND 组件池对照
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(WQ_ROOT / "src"))

OUT = WQ_ROOT / "research-data" / "ind_sa_survey.json"


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    # 1) 平台 IND ACTIVE
    print("=== 平台 IND ACTIVE alpha ===")
    rows = []
    offset = 0
    while True:
        r = await brain._request(
            "GET",
            f"{brain.base_url}/users/self/alphas",
            params={
                "limit": 100, "offset": offset,
                "status": "ACTIVE", "region": "IND",
                "order": "-dateSubmitted",
            },
        )
        if r.status_code != 200:
            print(f"  [ERR] {r.status_code} {r.text[:200]}")
            break
        j = r.json()
        batch = j.get("results") or []
        rows.extend(batch)
        if j.get("next") is None or not batch:
            break
        offset += len(batch)
        if offset >= 1000:
            print("  [warn] offset 达 1000 上限，可能未拉全")
            break

    print(f"  共 {len(rows)} 颗")
    regulars, supers = [], []
    for a in rows:
        aid = a.get("id")
        atype = a.get("type")
        isd = a.get("is") or {}
        item = {
            "alpha_id": aid, "type": atype,
            "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
            "turnover": isd.get("turnover"), "returns": isd.get("returns"),
            "dateSubmitted": a.get("dateSubmitted"),
            "universe": (a.get("settings") or {}).get("universe"),
            "neutralization": (a.get("settings") or {}).get("neutralization"),
            "delay": (a.get("settings") or {}).get("delay"),
        }
        if atype == "SUPER":
            supers.append(item)
        else:
            regulars.append(item)

    print(f"\n  -- REGULAR 组件池 ({len(regulars)}) --")
    print(f"  {'alpha_id':<10}{'sharpe':>7}{'fit':>6}{'turn':>8}{'date':>12}  univ/neut")
    for x in regulars:
        print(f"  {x['alpha_id']:<10}{str(x['sharpe']):>7}{str(x['fitness']):>6}"
              f"{str(x['turnover']):>8}{str(x['dateSubmitted'])[:10]:>12}  "
              f"{x['universe']}/{x['neutralization']}")

    print(f"\n  -- 已有 SUPER ({len(supers)}) --")
    for x in supers:
        print(f"  {x['alpha_id']:<10} sharpe={x['sharpe']} fit={x['fitness']} "
              f"to={x['turnover']} date={str(x['dateSubmitted'])[:10]}")

    # 2) 每个 SUPER 的 selection / combo
    sup_detail = {}
    for x in supers:
        aid = x["alpha_id"]
        d = await brain.get_alpha_details(aid)
        if not d:
            continue
        sel = d.get("selection") or {}
        cmb = d.get("combo") or {}
        st = d.get("settings") or {}
        sup_detail[aid] = {
            "selection_expr": sel.get("expression") or sel.get("code"),
            "combo_expr": cmb.get("expression") or cmb.get("code"),
            "selectionLimit": st.get("selectionLimit") or sel.get("selectionLimit"),
            "universe": st.get("universe"),
            "neutralization": st.get("neutralization"),
            "delay": st.get("delay"),
            "region": st.get("region"),
            "sel_desc_len": len(sel.get("description") or ""),
            "combo_desc_len": len(cmb.get("description") or ""),
        }
        print(f"\n  === SA {aid} 详情 ===")
        print(f"    selectionLimit = {sup_detail[aid]['selectionLimit']}")
        print(f"    selection expr = {sup_detail[aid]['selection_expr']}")
        print(f"    combo      expr = {sup_detail[aid]['combo_expr']}")
        print(f"    settings: {st.get('universe')}/{st.get('neutralization')}/d{st.get('delay')}")
        print(f"    desc: sel={sup_detail[aid]['sel_desc_len']} combo={sup_detail[aid]['combo_desc_len']}")

    # 3) 配额
    print("\n=== 配额 / 提交活动 ===")
    try:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/activities/submissions",
            params={"grouping": "SUBMISSION"},
        )
        print(f"  status={r.status_code} body={r.text[:600]}")
    except Exception as e:
        print(f"  {e}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "regulars": regulars, "supers": supers, "super_detail": sup_detail,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
