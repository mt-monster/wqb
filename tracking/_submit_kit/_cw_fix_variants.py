# -*- coding: utf-8 -*-
"""qMja95Q2 的 CONCENTRATED_WEIGHT 修复变体回测。

原配置：IND / TOP500 / d1 / decay6 / STATISTICAL / truncation 0.08
提交后硬闸 FAIL 于 CONCENTRATED_WEIGHT（IS 阶段为 WARNING）。
官方口径：单股权重上限 <10%，建议用中性化分散权重。

变体矩阵：truncation 0.08→0.02/0.01；neutralization STATISTICAL→MARKET/SECTOR/INDUSTRY/SUBINDUSTRY；
末端 rank / scale 均匀化；组合降 truncation + 换中性化。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

OUT = WQ_ROOT / "research-data" / "cw_fix_variants_20260901.json"

U30 = "analyst_recommendation_upgrades_30d_medium_31"
D30 = "analyst_recommendation_downgrades_30d_medium_31"
RES = "residualized_return_india_top500_equity"

BASE = (f"add(multiply(0.6, rank(subtract({U30}, {D30}))), "
        f"multiply(0.4, -rank(ts_mean({RES}, 10))))")

VARIANTS = [
    # name, neutralization, truncation, expression
    ("v_trunc02", "STATISTICAL", 0.02, BASE),
    ("v_trunc01", "STATISTICAL", 0.01, BASE),
    ("v_market", "MARKET", 0.08, BASE),
    ("v_sector", "SECTOR", 0.08, BASE),
    ("v_industry", "INDUSTRY", 0.08, BASE),
    ("v_subindustry", "SUBINDUSTRY", 0.08, BASE),
    ("v_rankfinal", "STATISTICAL", 0.08, f"rank({BASE})"),
    ("v_scalefinal", "STATISTICAL", 0.08, f"scale({BASE}, 1)"),
    ("v_market_trunc02", "MARKET", 0.02, BASE),
]

BASE_SETTINGS = {
    "instrumentType": "EQUITY",
    "region": "IND",
    "universe": "TOP500",
    "delay": 1,
    "decay": 6,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "maxTrade": "OFF",
    "maxPosition": "OFF",
    "language": "FASTEXPR",
    "visualization": False,
}


def payload_for(neut, trunc, expr):
    st = dict(BASE_SETTINGS)
    st["neutralization"] = neut
    st["truncation"] = trunc
    return {"type": "REGULAR", "settings": st, "regular": expr}


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    payloads = [payload_for(n, t, e) for _, n, t, e in VARIANTS]
    res = await brain.batch_create_simulations(payloads)
    print(f"[batch] submitted {res.get('submitted')}/{res.get('total')}")

    sims = []
    for (name, neut, trunc, expr), item in zip(VARIANTS, res.get("results", [])):
        sims.append({
            "name": name, "neut": neut, "trunc": trunc, "expr": expr,
            "ok": item.get("ok"), "simulation_id": item.get("simulation_id"),
            "error": item.get("error"),
        })
        print(f"  {name:<18} ok={item.get('ok')} sim={item.get('simulation_id')} "
              f"{item.get('error') or ''}")

    # 轮询
    pending = [s for s in sims if s.get("ok") and s.get("simulation_id")]
    for rnd in range(40):
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
            s["status"] = status
            if status in ("COMPLETE", "DONE") or j.get("alpha"):
                s["alpha_id"] = j.get("alpha")
                print(f"  [{s['name']}] DONE -> {s['alpha_id']}")
            elif status in ("ERROR", "FAIL", "FAILED"):
                s["alpha_id"] = None
                s["sim_error"] = (j.get("message") or j.get("error") or "")[:200]
                print(f"  [{s['name']}] {status}: {s['sim_error'][:120]}")
            else:
                still.append(s)
        pending = still
        if pending:
            await asyncio.sleep(15)

    # 取指标
    print("\n=== 变体结果 ===")
    print(f"{'name':<18}{'neut':<13}{'trunc':>6}{'sharpe':>7}{'fit':>6}"
          f"{'to':>8}{'CONCENTRATED_WEIGHT':>22}{'alpha_id':>10}")
    for s in sims:
        aid = s.get("alpha_id")
        if not aid:
            print(f"{s['name']:<18}{s['neut']:<13}{s['trunc']:>6}"
                  f"{'--':>7}{'--':>6}{'--':>8}{'NO_ALPHA':>22}"
                  f"{str(s.get('sim_error') or s.get('poll_error') or s.get('error') or '')[:10]:>10}")
            continue
        d = await brain.get_alpha_details(aid)
        isd = d.get("is") or {}
        checks = {c.get("name"): c.get("result") for c in (isd.get("checks") or [])}
        cw = checks.get("CONCENTRATED_WEIGHT", "?")
        s["metrics"] = {
            "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
            "turnover": isd.get("turnover"), "returns": isd.get("returns"),
            "checks": checks,
        }
        print(f"{s['name']:<18}{s['neut']:<13}{s['trunc']:>6}"
              f"{str(isd.get('sharpe')):>7}{str(isd.get('fitness')):>6}"
              f"{str(isd.get('turnover')):>8}{cw:>22}{aid:>10}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(sims, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
