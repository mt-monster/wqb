# -*- coding: utf-8 -*-
"""批量诊断候选 alpha（只读）：指标 + IS checks 通过情况 + 双闸状态。

用法: python _diag_batch4.py <alpha_id>...
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

OUT = WQ_ROOT / "research-data" / "diag_batch4_20260901.json"


def _checks_summary(checks):
    out = {}
    for c in checks or []:
        name = c.get("name")
        out[name] = {"result": c.get("result"), "value": c.get("value"),
                     "limit": c.get("limit")}
    return out


async def main(ids):
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    report = {}
    for aid in ids:
        d = await brain.get_alpha_details(aid)
        if not d:
            print(f"{aid}: NOT_FOUND")
            report[aid] = {"error": "NOT_FOUND"}
            continue
        st = d.get("settings") or {}
        isd = d.get("is") or {}
        checks = _checks_summary(d.get("is") and d.get("is").get("checks"))
        # IS checks 也可能在顶层或 os 下
        if not checks:
            checks = _checks_summary(d.get("checks"))
        fails = [k for k, v in checks.items() if v.get("result") == "FAIL"]
        pend = [k for k, v in checks.items() if v.get("result") == "PENDING"]

        raw = d.get("regular")
        expr = raw.get("code") if isinstance(raw, dict) else raw

        report[aid] = {
            "status": d.get("status"), "stage": d.get("stage"), "type": d.get("type"),
            "region": st.get("region"), "universe": st.get("universe"),
            "neutralization": st.get("neutralization"), "delay": st.get("delay"),
            "decay": st.get("decay"),
            "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
            "turnover": isd.get("turnover"), "returns": isd.get("returns"),
            "drawdown": isd.get("drawdown"), "margin": isd.get("margin"),
            "dateCreated": d.get("dateCreated"),
            "checks": checks, "fails": fails, "pending": pend,
            "expression": expr,
        }
        print(f"\n=== {aid} ===")
        print(f"  status={d.get('status')} stage={d.get('stage')} type={d.get('type')}")
        print(f"  region={st.get('region')} univ={st.get('universe')} "
              f"neut={st.get('neutralization')} d{st.get('delay')} decay={st.get('decay')}")
        print(f"  sharpe={isd.get('sharpe')} fit={isd.get('fitness')} "
              f"to={isd.get('turnover')} ret={isd.get('returns')} dd={isd.get('drawdown')}")
        print(f"  FAIL={fails or '-'}  PENDING={pend or '-'}")
        if expr:
            print(f"  expr: {str(expr)[:160]}")
        # 金字塔/主题加成
        for k, v in checks.items():
            if k in ("MATCHES_PYRAMID", "MATCHES_THEMES") and v.get("result") != "PASS":
                print(f"  [{k}] {v.get('result')} {v.get('value')}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
