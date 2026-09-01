# -*- coding: utf-8 -*-
"""单信号变体回测（第三轮）：绕开 CONCENTRATED_WEIGHT。

已确认的因果链：
  add(0.6*rank(analyst_diff), 0.4*(-rank(ts_mean(RES,10)))) 双信号加权
    -> IS 阶段 CONCENTRATED_WEIGHT=WARNING -> 提交后 FAIL（qMja95Q2、3qlKQ1qX 双证）
  单信号 rank(...) 形式 -> PASS（Xg73mNda 已 ACTIVE）
  换 neutralization / 降 truncation 对本闸无效（第一轮全档仍 WARNING）

本轮只回测单信号形态，筛选 CONCENTRATED_WEIGHT=PASS 且指标 > Xg73mNda(1.79/1.28) 的候选，
并对已 ACTIVE 的同族 Xg73mNda 做 SELF 预检（同族连测会自相残杀）。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

OUT = WQ_ROOT / "research-data" / "cw_fix_round3_20260901.json"

U30 = "analyst_recommendation_upgrades_30d_medium_31"
D30 = "analyst_recommendation_downgrades_30d_medium_31"
U14 = "analyst_recommendation_upgrades_14d_medium_4"
D14 = "analyst_recommendation_downgrades_14d_medium_4"
RES = "residualized_return_india_top500_equity"

D30E = f"subtract({U30}, {D30})"
D14E = f"subtract({U14}, {D14})"

VARIANTS = [
    ("s_inst30", f"rank({D30E})", "30d 净额瞬时 rank"),
    ("s_mean5", f"rank(ts_mean({D30E}, 5))", "30d 净额 5 日平滑"),
    ("s_mean20", f"rank(ts_mean({D30E}, 20))", "30d 净额 20 日平滑"),
    ("s_inst14", f"rank({D14E})", "14d 净额瞬时 rank"),
    ("s_mean14_10", f"rank(ts_mean({D14E}, 10))", "14d 净额 10 日平滑"),
    ("s_sum10", f"rank(ts_sum({D30E}, 10))", "30d 净额 10 日求和"),
    ("s_res", f"multiply(-1, rank(ts_mean({RES}, 10)))", "纯残差反转单信号"),
    ("s_tsrank60", f"ts_rank({D30E}, 60)", "30d 净额 60 日时间排名"),
]

BASE_SETTINGS = {
    "instrumentType": "EQUITY",
    "region": "IND",
    "universe": "TOP500",
    "delay": 1,
    "decay": 6,
    "neutralization": "STATISTICAL",
    "truncation": 0.08,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "maxTrade": "OFF",
    "maxPosition": "OFF",
    "language": "FASTEXPR",
    "visualization": False,
}


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    payloads = [{"type": "REGULAR", "settings": dict(BASE_SETTINGS), "regular": e}
                for _, e, _ in VARIANTS]
    res = await brain.batch_create_simulations(payloads)
    print(f"[batch] submitted {res.get('submitted')}/{res.get('total')}")

    sims = []
    for (name, expr, note), item in zip(VARIANTS, res.get("results", [])):
        sims.append({"name": name, "expr": expr, "note": note, "ok": item.get("ok"),
                     "simulation_id": item.get("simulation_id"),
                     "error": item.get("error")})
        print(f"  {name:<14} ok={item.get('ok')} sim={item.get('simulation_id')} "
              f"{str(item.get('error') or '')[:50]}")

    pending = [s for s in sims if s.get("ok") and s.get("simulation_id")]
    for _ in range(40):
        if not pending:
            break
        still = []
        for s in pending:
            r = await brain._request(
                "GET", f"{brain.base_url}/simulations/{s['simulation_id']}")
            if r.status_code != 200:
                s["poll_error"] = f"{r.status_code}:{r.text[:120]}"
                continue
            j = r.json()
            status = (j.get("status") or "").upper()
            if status in ("COMPLETE", "DONE") or j.get("alpha"):
                s["alpha_id"] = j.get("alpha")
                print(f"  [{s['name']}] DONE -> {s['alpha_id']}")
            elif status in ("ERROR", "FAIL", "FAILED"):
                s["alpha_id"] = None
                s["sim_error"] = (j.get("message") or j.get("error") or "")[:200]
                print(f"  [{s['name']}] {status}: {s['sim_error'][:110]}")
            else:
                still.append(s)
        pending = still
        if pending:
            await asyncio.sleep(15)

    print("\n=== 第三轮：单信号变体 ===")
    print(f"{'name':<14}{'sharpe':>7}{'fit':>6}{'to':>8}{'CONC_WEIGHT':>14}"
          f"{'SELF':>8}{'alpha_id':>10}  说明")
    for s in sims:
        aid = s.get("alpha_id")
        if not aid:
            print(f"{s['name']:<14}{'--':>7}{'--':>6}{'--':>8}{'NO_ALPHA':>14}{'--':>8}"
                  f"{'':>10}  {str(s.get('sim_error') or s.get('poll_error') or '')[:45]}")
            continue
        d = await brain.get_alpha_details(aid)
        isd = d.get("is") or {}
        checks = {c.get("name"): c.get("result") for c in (isd.get("checks") or [])}
        cw = checks.get("CONCENTRATED_WEIGHT", "?")
        # SELF 本地预检（含已 ACTIVE 的同族 Xg73mNda）
        self_max = None
        try:
            sc = await brain.check_self_correlation(aid)
            self_max = sc.get("max_correlation")
        except Exception as e:
            self_max = f"ERR:{str(e)[:20]}"
        s["metrics"] = {
            "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
            "turnover": isd.get("turnover"), "returns": isd.get("returns"),
            "checks": checks, "self_max": self_max,
        }
        sm = f"{self_max:.4f}" if isinstance(self_max, float) else str(self_max)
        print(f"{s['name']:<14}{str(isd.get('sharpe')):>7}{str(isd.get('fitness')):>6}"
              f"{str(isd.get('turnover')):>8}{cw:>14}{sm:>8}{aid:>10}  {s['note']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(sims, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
