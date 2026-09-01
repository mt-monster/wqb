# -*- coding: utf-8 -*-
"""诊断待提交 3 颗 alpha：区域/类型/指标/IS checks/配额，并估算双闸。
只读，不提交。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

TARGETS = ["d5jJebLv", "Jj7aRNKm", "2rlVPwdw"]


def fmt_checks(checks):
    out = []
    for c in (checks or []):
        out.append(f"      {c.get('name')}={c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}")
    return "\n".join(out)


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    report = {}
    for aid in TARGETS:
        d = await brain.get_alpha_details(aid)
        if not d:
            print(f"[ERROR] {aid}: get_alpha_details 返回空")
            continue
        st = d.get("status")
        stage = d.get("stage")
        reg = (d.get("settings") or {}).get("region")
        isd = d.get("is") or {}
        region = isd.get("region") or reg
        print(f"\n=== {aid} ===")
        print(f"  status={st} stage={stage} type={d.get('type')} region={region}")
        print(f"  sharpe={isd.get('sharpe')} fitness={isd.get('fitness')} "
              f"turnover={isd.get('turnover')} returns={isd.get('returns')} "
              f"drawdown={isd.get('drawdown')} margin={isd.get('margin')}")
        print(f"  dateSubmitted={d.get('dateSubmitted')}")
        sl = d.get("settings") or {}
        print(f"  settings: universe={sl.get('universe')} neut={sl.get('neutralization')} "
              f"delay={sl.get('delay')} decay={sl.get('decay')} truncation={sl.get('truncation')} "
              f"nan={sl.get('nanHandling')} lang={sl.get('language')}")
        print(f"  [IS checks]")
        print(fmt_checks(isd.get("checks")))
        # 顺带看顶层 checks（提交态）
        if d.get("checks"):
            print(f"  [top-level checks]")
            print(fmt_checks(d.get("checks")))
        # 平台直接给的相关
        pc = d.get("prod_correlation") or d.get("prodCorrelation")
        sc = d.get("self_correlation") or d.get("selfCorrelation")
        if pc is not None or sc is not None:
            print(f"  platform: prod_correlation={pc} self_correlation={sc}")
        raw = d.get("regular") or d.get("expression") or ""
        expr = raw.get("code") if isinstance(raw, dict) else raw
        if not isinstance(expr, str):
            expr = str(expr)
        print(f"  expr({len(expr)}): {expr[:180]}")

        report[aid] = {
            "status": st, "stage": stage, "region": region, "type": d.get("type"),
            "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
            "turnover": isd.get("turnover"), "returns": isd.get("returns"),
            "drawdown": isd.get("drawdown"), "margin": isd.get("margin"),
            "universe": sl.get("universe"), "neutralization": sl.get("neutralization"),
            "delay": sl.get("delay"), "decay": sl.get("decay"),
            "is_checks": isd.get("checks"),
            "top_checks": d.get("checks"),
            "prod_correlation": pc, "self_correlation": sc,
            "expression": expr,
        }

    # 配额
    print("\n=== 配额 ===")
    try:
        r = await brain._request("GET", f"{brain.base_url}/users/self/activities")
        if r.status_code == 200:
            j = r.json()
            print(json.dumps(j, ensure_ascii=False)[:2000])
        else:
            print(f"  status={r.status_code} {r.text[:300]}")
    except Exception as e:
        print(f"  quota fetch failed: {e}")

    Path(r"D:\coding\traeCN_project\wqb\research-data\submit3_diag.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(main())
