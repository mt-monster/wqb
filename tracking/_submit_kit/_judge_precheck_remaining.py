# -*- coding: utf-8 -*-
"""judge 前置证据采集（2026-09-01 13:0x，队列 4 颗已入池后）：
1) 队列 6 颗平台状态核实
2) 剩余可提交池新鲜双闸（self 本地 + prod 平台 refresh=True）
   —— 重点：0mwVnbkG 与已 ACTIVE 的 RR7OWQKd 同腿孪生风险
3) 补 RR7OWQKd submission_ledger 落账
输出：research-data/judge_precheck_20260901.json
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(WQ_ROOT / "src"))

RD = WQ_ROOT / "research-data"
OUT = RD / "judge_precheck_20260901.json"

SUBMITTED = ["RR7OWQKd", "P07Ra2zJ", "58lEQMo1", "qMjLYVVP"]
REMAINING = ["1YzOz8ZM", "0mwVnbkG", "Jj7ee6nO", "58kALa11", "pwjpKGJ3", "omqEE1pn"]


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    report = {"submitted": {}, "remaining": {}}

    print("=== 1) 已提交 4 颗状态核实 ===")
    for aid in SUBMITTED:
        d = await brain.get_alpha_details(aid)
        isd = d.get("is") or {}
        report["submitted"][aid] = {
            "status": d.get("status"), "stage": d.get("stage"),
            "dateSubmitted": d.get("dateSubmitted"),
            "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
        }
        print(f"  {aid}: {d.get('status')}/{d.get('stage')} "
              f"dateSubmitted={d.get('dateSubmitted')} "
              f"sh={isd.get('sharpe')} fit={isd.get('fitness')}")

    print("\n=== 2) 剩余候选新鲜双闸 ===")
    for aid in REMAINING:
        d = await brain.get_alpha_details(aid)
        if not d or d.get("status") != "UNSUBMITTED":
            report["remaining"][aid] = {"status": d.get("status") if d else "NOT_FOUND"}
            print(f"  {aid}: status={report['remaining'][aid]['status']}（跳过）")
            continue
        try:
            s = await brain.check_self_correlation(aid, threshold=0.7)
            s_max = s.get("max_correlation")
            s_pass = s.get("passes_check")
        except Exception as e:
            s_max, s_pass = None, f"err={type(e).__name__}"
        try:
            p = await brain.check_correlation(aid, correlation_type="production",
                                              threshold=0.7, refresh=True)
            pc = (p.get("checks") or {}).get("production") or {}
            p_max, p_pass = pc.get("max_correlation"), pc.get("passes_check")
        except Exception as e:
            p_max, p_pass = None, f"err={type(e).__name__}"
        report["remaining"][aid] = {
            "status": d.get("status"), "self": s_max, "self_pass": s_pass,
            "prod": p_max, "prod_pass": p_pass,
        }
        print(f"  {aid}: SELF={s_max}({s_pass})  PROD={p_max}({p_pass})", flush=True)
        await asyncio.sleep(1.5)

    print("\n=== 3) 补 RR7OWQKd ledger ===")
    try:
        from wqb.store.campaign import CampaignStore
        store = CampaignStore(str(WQ_ROOT / "data" / "wqb.db"))
        store.record_submission(
            alpha_id="RR7OWQKd", region="IND", submission_type="REGULAR",
            status="ACTIVE",
            verdict={"note": "queue submit#1 201 async accepted; #2 403 already-submitted",
                     "os_flipped": "2026-09-01T00:00:59-04:00"},
            quota_used=1)
        store.close()
        report["rr7owqkd_ledger"] = "recorded"
        print("  RR7OWQKd ledger recorded")
    except Exception as e:
        report["rr7owqkd_ledger"] = f"failed: {e}"
        print(f"  ledger FAILED: {e}")

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
