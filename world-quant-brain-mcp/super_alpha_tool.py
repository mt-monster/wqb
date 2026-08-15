"""SuperAlpha 工具：selection 预览 + SUPER 模拟创建。

用法:
  python super_alpha_tool.py select "<selection_expr>" [--limit N] [--handling POSITIVE|NON_ZERO|NON_NAN]
                                    [--region USA] [--delay 1] [--itype EQUITY]
  python super_alpha_tool.py sim --selection-file sel.txt --combo-file combo.txt
                                [--region USA --universe TOP3000 --delay 1 --decay 5
                                 --neut MARKET --trunc 0.08 --limit 20 --handling POSITIVE
                                 --test-period P0Y0M]

要点(平台官方语义):
  selection = 对"你所有 ACTIVE 已提交 alpha"逐个求值的表达式, 值即 selection weight,
              按降序取前 selectionLimit 个(最小 10)。可用字段: turnover/long_count/short_count/
              decay/truncation/neutralization/universe/operator_count/self_correlation/
              prod_correlation/tags/color/category/datasets/datafields/os_start_date ...
              注意: 没有 sharpe/fitness 字段可用!
  combo     = 对每个被选 alpha 的"日度权重"表达式。常量 1 = 等权基准。
              generate_stats(alpha) 返回日度统计(returns/pnl/turnover/drawdown/...)。
"""
import argparse
import asyncio
import json
import os
import sys

# 必须先清代理: 环境里的 http_proxy 会导致连 api.worldquantbrain.com 时 SSL UNEXPECTED_EOF
for _k in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from brain_api import BrainApiClient, SimulationData, SimulationSettings  # noqa: E402


def _f(v, nd=2):
    if v is None:
        return "-"
    try:
        return f"{float(v):.{nd}f}"
    except (TypeError, ValueError):
        return str(v)


async def cmd_select(args):
    client = BrainApiClient()
    await client.ensure_authenticated()
    print("[AUTH] ok", flush=True)

    params = {
        "selection": args.expr,
        "instrumentType": args.itype,
        "region": args.region,
        "delay": args.delay,
        "selectionLimit": args.limit,
        "selectionHandling": args.handling,
        "limit": 100,
        "offset": 0,
    }
    rows, count = [], None
    while True:
        resp = await client._request(
            "GET", f"{client.base_url}/simulations/super-selection", params=params
        )
        resp.raise_for_status()
        data = resp.json()
        if count is None:
            count = data.get("count")
        rows.extend(data.get("results") or [])
        if not data.get("next") or len(rows) >= (count or 0):
            break
        params["offset"] += 100

    print(f"\n[SELECTION] expr={args.expr!r}")
    print(f"[SELECTION] region={args.region} delay={args.delay} handling={args.handling} "
          f"limit={args.limit}")
    print(f"[SELECTION] count={count} fetched={len(rows)}")

    # 预览接口不按 region 过滤, 但真实 SUPER 模拟只会选中与 settings.region 匹配的 alpha。
    # --only-region 在本地复现这个过滤, 使预览等价于真实选择结果。
    if args.only_region:
        before = len(rows)
        rows = [r for r in rows
                if ((r.get("settings") or {}).get("region") or "").upper()
                == args.only_region.upper()]
        rows.sort(key=lambda r: -((r.get("selected") or {}).get("weight") or 0))
        rows = rows[:args.top]
        print(f"[SELECTION] only_region={args.only_region}: {before} -> {len(rows)} "
              f"(top {args.top})")
    print()

    hdr = (f"{'#':>3} {'id':<10} {'reg':<4} {'universe':<18} {'neut':<12} "
           f"{'w':>6} {'isSh':>6} {'isFit':>6} {'osSh':>6} {'to':>6} "
           f"{'pCorr':>6} {'sCorr':>6} {'ops':>4}  tags")
    print(hdr)
    print("-" * len(hdr))
    agg = {"is_sharpe": [], "is_fitness": [], "ops": 0}
    for i, a in enumerate(rows, 1):
        st = a.get("settings") or {}
        is_ = a.get("is") or {}
        os_ = a.get("os") or {}
        sel = a.get("selected") or {}
        reg = (a.get("regular") or {})
        ops = reg.get("operatorCount") or 0
        agg["ops"] += ops
        if is_.get("sharpe") is not None:
            agg["is_sharpe"].append(is_["sharpe"])
        if is_.get("fitness") is not None:
            agg["is_fitness"].append(is_["fitness"])
        print(f"{i:>3} {a.get('id',''):<10} {st.get('region',''):<4} "
              f"{st.get('universe',''):<18} {str(st.get('neutralization','')):<12} "
              f"{_f(sel.get('weight'),3):>6} {_f(is_.get('sharpe')):>6} "
              f"{_f(is_.get('fitness')):>6} {_f(os_.get('sharpe')):>6} "
              f"{_f(is_.get('turnover'),3):>6} {_f(is_.get('prodCorrelation'),3):>6} "
              f"{_f(is_.get('selfCorrelation'),3):>6} {ops:>4}  "
              f"{','.join(a.get('tags') or [])[:30]}")

    if agg["is_sharpe"]:
        n = len(agg["is_sharpe"])
        print(f"\n[AGG] n={n}  mean_isSharpe={sum(agg['is_sharpe'])/n:.2f}  "
              f"mean_isFitness={sum(agg['is_fitness'])/len(agg['is_fitness']):.2f}  "
              f"total_operators={agg['ops']} (limit 8000)")
    regions = {}
    for a in rows:
        r = ((a.get("settings") or {}).get("region")) or "?"
        regions[r] = regions.get(r, 0) + 1
    print(f"[AGG] regions={regions}")


async def cmd_sim(args):
    selection = open(args.selection_file, encoding="utf-8").read().strip()
    combo = open(args.combo_file, encoding="utf-8").read().strip()

    client = BrainApiClient()
    await client.ensure_authenticated()
    print("[AUTH] ok", flush=True)

    settings = SimulationSettings(
        instrumentType=args.itype,
        region=args.region,
        universe=args.universe,
        delay=args.delay,
        decay=args.decay,
        neutralization=args.neut,
        truncation=args.trunc,
        testPeriod=args.test_period,
        language="FASTEXPR",
        visualization=False,
        pasteurization="ON",
        maxTrade="OFF",
        selectionHandling=args.handling,
        selectionLimit=args.limit,
        componentActivation="IS",
        unitHandling="VERIFY",
        nanHandling="ON",
    )
    if args.no_guard:
        # brain_api 的 validate_super_selection_rules 强制 USA SUPER 的 selection 必须含
        # "(prod_correlation > 0)"，但实测该条件会把 USA 池从 125 个砍到 12 个
        # (多数 alpha 的 prodCorrelation 为空)。model_construct 跳过本地校验。
        sim_data = SimulationData.model_construct(
            type="SUPER", settings=settings, regular=None,
            combo=combo, selection=selection,
        )
    else:
        sim_data = SimulationData(
            type="SUPER", settings=settings, combo=combo, selection=selection
        )
    print("[SELECTION]", selection)
    print("[COMBO]", combo.replace("\n", " | "))
    print("[CREATE] posting SUPER simulation ...", flush=True)
    result = await client.create_simulation(sim_data)

    aid = result.get("id") or result.get("alpha")
    is_ = result.get("is") or {}
    print(f"\n[DONE] alpha_id={aid}")
    print(f"[IS] sharpe={_f(is_.get('sharpe'))} fitness={_f(is_.get('fitness'))} "
          f"turnover={_f(is_.get('turnover'),4)} returns={_f(is_.get('returns'),4)} "
          f"drawdown={_f(is_.get('drawdown'),4)} "
          f"selfCorr={_f(is_.get('selfCorrelation'),3)} "
          f"prodCorr={_f(is_.get('prodCorrelation'),3)}")
    for c in (is_.get("checks") or []):
        print(f"  {c.get('result','?'):<8} {c.get('name','')} "
              f"value={c.get('value','-')} limit={c.get('limit','-')}")
    out = os.path.join(HERE, f"super_alpha_result_{aid}.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, default=str)
    print(f"[SAVED] {out}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("select")
    s.add_argument("expr")
    s.add_argument("--limit", type=int, default=1000)
    s.add_argument("--handling", default="POSITIVE")
    s.add_argument("--region", default="USA")
    s.add_argument("--delay", type=int, default=1)
    s.add_argument("--itype", default="EQUITY")
    s.add_argument("--only-region", default=None,
                   help="本地按 region 过滤并重排, 复现真实 SUPER 选择结果")
    s.add_argument("--top", type=int, default=30, help="配合 --only-region 显示前 N 个")

    m = sub.add_parser("sim")
    m.add_argument("--selection-file", required=True)
    m.add_argument("--combo-file", required=True)
    m.add_argument("--region", default="USA")
    m.add_argument("--universe", default="TOP3000")
    m.add_argument("--delay", type=int, default=1)
    m.add_argument("--decay", type=int, default=5)
    m.add_argument("--neut", default="MARKET")
    m.add_argument("--trunc", type=float, default=0.08)
    m.add_argument("--limit", type=int, default=20)
    m.add_argument("--handling", default="POSITIVE")
    m.add_argument("--test-period", default="P0Y0M")
    m.add_argument("--itype", default="EQUITY")
    m.add_argument("--no-guard", action="store_true",
                   help="跳过 brain_api 本地强制的 (prod_correlation > 0) selection 校验")

    args = ap.parse_args()
    asyncio.run(cmd_select(args) if args.cmd == "select" else cmd_sim(args))


if __name__ == "__main__":
    main()
