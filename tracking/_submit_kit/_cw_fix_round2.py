# -*- coding: utf-8 -*-
"""CONCENTRATED_WEIGHT 根因拆解（第二轮）。

第一轮结论：中性化/truncation 全档无效（一律 WARNING），末端 rank 反使 FAIL。
对照事实：单信号 Xg73mNda = `rank(ts_mean(subtract(U30,D30),10))` 是 PASS，
而双信号 add(0.6*rank(diff30), 0.4*(-rank(ts_mean(RES,10)))) 是 WARNING。
→ 嫌疑：residualized_return_india_top500_equity 项制造权重集中。

本轮逐项拆解 + 归一化/去极值手段，目标：CONCENTRATED_WEIGHT=PASS 且 sharpe>=2.5 / fit>=2。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

OUT = WQ_ROOT / "research-data" / "cw_fix_round2_20260901.json"

U30 = "analyst_recommendation_upgrades_30d_medium_31"
D30 = "analyst_recommendation_downgrades_30d_medium_31"
RES = "residualized_return_india_top500_equity"

DIFF = f"subtract({U30}, {D30})"
A = f"rank({DIFF})"                      # 瞬时分析师修正净额
A_S = f"rank(ts_mean({DIFF}, 10))"       # 10 日平滑版（Xg73mNda 同款）
B = f"-rank(ts_mean({RES}, 10))"         # 残差收益反转项
ORIG = f"add(multiply(0.6, {A}), multiply(0.4, {B}))"

VARIANTS = [
    # name, neutralization, truncation, expression, 说明
    ("r2_a_only", "STATISTICAL", 0.08, A,
     "仅分析师项（无残差）"),
    ("r2_b_only", "STATISTICAL", 0.08, B.lstrip("-"),
     "仅残差反转项（正向）"),
    ("r2_a_smooth", "STATISTICAL", 0.08, A_S,
     "分析师项 10 日平滑（Xg73mNda 同款）"),
    ("r2_zscore", "STATISTICAL", 0.08, f"zscore({ORIG})",
     "末端 zscore 归一化"),
    ("r2_a_s_plus_b", "STATISTICAL", 0.08,
     f"add(multiply(0.6, {A_S}), multiply(0.4, {B}))",
     "平滑版 A + B"),
    ("r2_equal", "STATISTICAL", 0.08,
     f"add(multiply(0.5, {A}), multiply(0.5, {B}))",
     "等权 0.5/0.5"),
    ("r2_sub", "STATISTICAL", 0.08, f"subtract({A}, rank(ts_mean({RES}, 10)))",
     "A - rank(RES) 减法组合"),
    ("r2_tsrank", "STATISTICAL", 0.08, f"ts_rank({ORIG}, 120)",
     "末端 ts_rank 时间排名"),
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

    payloads = [payload_for(n, t, e) for _, n, t, e, _ in VARIANTS]
    res = await brain.batch_create_simulations(payloads)
    print(f"[batch] submitted {res.get('submitted')}/{res.get('total')}")

    sims = []
    for (name, neut, trunc, expr, note), item in zip(VARIANTS, res.get("results", [])):
        sims.append({
            "name": name, "neut": neut, "trunc": trunc, "expr": expr, "note": note,
            "ok": item.get("ok"), "simulation_id": item.get("simulation_id"),
            "error": item.get("error"),
        })
        print(f"  {name:<16} ok={item.get('ok')} sim={item.get('simulation_id')} "
              f"{str(item.get('error') or '')[:60]}")

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
                print(f"  [{s['name']}] {status}: {s['sim_error'][:110]}")
            else:
                still.append(s)
        pending = still
        if pending:
            await asyncio.sleep(15)

    print("\n=== 第二轮变体结果 ===")
    print(f"{'name':<16}{'sharpe':>7}{'fit':>6}{'to':>8}"
          f"{'CONC_WEIGHT':>14}{'alpha_id':>10}  说明")
    for s in sims:
        aid = s.get("alpha_id")
        if not aid:
            print(f"{s['name']:<16}{'--':>7}{'--':>6}{'--':>8}{'NO_ALPHA':>14}"
                  f"{'':>10}  {str(s.get('sim_error') or s.get('poll_error') or '')[:50]}")
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
        print(f"{s['name']:<16}{str(isd.get('sharpe')):>7}{str(isd.get('fitness')):>6}"
              f"{str(isd.get('turnover')):>8}{cw:>14}{aid:>10}  {s['note']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(sims, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
