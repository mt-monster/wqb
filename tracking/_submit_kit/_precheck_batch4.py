# -*- coding: utf-8 -*-
"""候选双闸预检 + 同族冲突检查（只读，不提交）。

1) SELF（本地 OS PnL 池，秒级）
2) PROD（平台生产池，~30s/颗）
3) 族内是否已有 ACTIVE 成员（按表达式关键词匹配）
"""
import asyncio
import json
import re
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

OUT = WQ_ROOT / "research-data" / "precheck_batch4_20260901.json"


async def main(ids):
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    # --- 同族检查：先取候选表达式关键词 ---
    exprs = {}
    for aid in ids:
        d = await brain.get_alpha_details(aid)
        raw = d.get("regular")
        exprs[aid] = raw.get("code") if isinstance(raw, dict) else raw

    # 提取候选用到的字段（fvl_/analyst_ 等前缀）
    def fields(e):
        return set(re.findall(r"\b([a-z][a-z0-9]*_[a-z0-9_]+)", e or ""))
    cand_fields = {aid: fields(e) for aid, e in exprs.items()}

    # 拉 IND ACTIVE 池，按 settings.region 过滤
    rows = []
    offset = 0
    while True:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"limit": 100, "offset": offset, "status": "ACTIVE",
                    "order": "-dateSubmitted"},
        )
        j = r.json()
        batch = j.get("results") or []
        rows.extend(batch)
        if j.get("next") is None or not batch or offset >= 1000:
            break
        offset += len(batch)
    ind_active = [a for a in rows if (a.get("settings") or {}).get("region") == "IND"
                  and a.get("type") != "SUPER"]

    print("=== 同族冲突检查（IND ACTIVE） ===")
    family_hits = {}
    for aid in ids:
        cf = cand_fields[aid]
        hits = []
        for a in ind_active:
            d = await brain.get_alpha_details(a.get("id"))
            raw = d.get("regular")
            e = raw.get("code") if isinstance(raw, dict) else raw
            if not isinstance(e, str):
                continue
            af = fields(e)
            inter = cf & af
            if inter:
                hits.append({"alpha_id": a.get("id"), "shared": sorted(inter)[:6],
                             "sharpe": (a.get("is") or {}).get("sharpe")})
        family_hits[aid] = hits
        print(f"  {aid}: 与 IND ACTIVE 共享字段的 {len(hits)} 颗")
        for h in hits[:6]:
            print(f"      vs {h['alpha_id']} sharpe={h['sharpe']}  shared={h['shared']}")

    # --- 双闸预检 ---
    report = {"family_hits": family_hits}
    print("\n=== SELF 预检（本地 OS PnL 池） ===")
    for aid in ids:
        try:
            s = await brain.check_self_correlation(aid)
            report.setdefault("self", {})[aid] = {"max": s.get("max_correlation"),
                                                  "pass": s.get("passes_check")}
            print(f"  {aid}: max={s.get('max_correlation')} pass={s.get('passes_check')}")
        except Exception as e:
            report.setdefault("self", {})[aid] = {"error": str(e)}
            print(f"  {aid}: ERROR {e}")

    print("\n=== PROD 预检（平台生产池） ===")
    for aid in ids:
        try:
            p = await brain.check_correlation(aid, correlation_type="production", threshold=0.7)
            pc = p.get("checks", {}).get("production", {})
            report.setdefault("prod", {})[aid] = {"max": pc.get("max_correlation"),
                                                  "pass": pc.get("passes_check")}
            print(f"  {aid}: max={pc.get('max_correlation')} pass={pc.get('passes_check')}")
        except Exception as e:
            report.setdefault("prod", {})[aid] = {"error": str(e)}
            print(f"  {aid}: ERROR {e}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
