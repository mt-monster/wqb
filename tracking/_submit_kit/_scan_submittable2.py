# -*- coding: utf-8 -*-
"""补漏扫描：按 dateCreated 倒序再拉 1000 颗，覆盖首轮（按 fitness 降序）被 offset 截断的部分。

首轮 bug：UNSUBMITTED 总量 >1100，order=-is.fitness 时 offset 到达平台硬限 1000 后 break，
导致 fitness 排名靠后的候选（如 MEA 那批 1.55~1.89）被整体遗漏。

本轮聚焦非 USA 区域（USA 1033 颗里绝大多数是 OLD_SIMULATION 废案，性价比低）。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

OUT = WQ_ROOT / "research-data" / "submittable_scan2_20260901.json"

MIN_SHARPE_D1 = 1.58
MIN_FIT = 1.0
TO_LO, TO_HI = 0.01, 0.4
SKIP_REGIONS = {"USA"}  # 首轮已扫，且多为 OLD_SIMULATION 废案


async def fetch(brain, order):
    rows = []
    offset = 0
    while offset < 1000:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"limit": 100, "offset": offset, "status": "UNSUBMITTED",
                    "order": order},
        )
        if r.status_code != 200:
            print(f"  [ERR] {r.status_code} {r.text[:150]}")
            break
        j = r.json()
        batch = j.get("results") or []
        rows.extend(batch)
        if j.get("next") is None or not batch:
            break
        offset += len(batch)
    return rows


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    print("=== 按 dateCreated 倒序拉取 ===")
    rows = await fetch(brain, "-dateCreated")
    print(f"拉到 {len(rows)} 颗")

    # 非 USA
    cand = [a for a in rows
            if ((a.get("settings") or {}).get("region") or "?") not in SKIP_REGIONS]
    print(f"非 USA 候选：{len(cand)} 颗")

    by_region = {}
    for a in cand:
        by_region.setdefault((a.get("settings") or {}).get("region") or "?", []).append(a)
    print("区域分布：" + "  ".join(f"{k}={len(v)}" for k, v in
                                   sorted(by_region.items(), key=lambda x: -len(x[1]))))

    # 指标初筛
    pre = []
    for a in cand:
        isd = a.get("is") or {}
        st = a.get("settings") or {}
        sh, fit, to = isd.get("sharpe"), isd.get("fitness"), isd.get("turnover")
        if sh is None or fit is None or to is None:
            continue
        if not (sh >= MIN_SHARPE_D1 and fit >= MIN_FIT and TO_LO <= to <= TO_HI):
            continue
        pre.append({"alpha_id": a.get("id"),
                    "region": st.get("region"),
                    "sharpe": sh, "fitness": fit, "turnover": to,
                    "returns": isd.get("returns"),
                    "universe": st.get("universe"), "delay": st.get("delay"),
                    "neutralization": st.get("neutralization"),
                    "dateCreated": a.get("dateCreated")})
    print(f"指标达标：{len(pre)} 颗")

    # 读 checks
    print(f"\n=== 读取 IS checks ===")
    ok_list, cw_warn, fail_list = [], [], []
    for i, x in enumerate(pre, 1):
        try:
            d = await brain.get_alpha_details(x["alpha_id"])
        except Exception as e:
            x["_err"] = str(e)[:60]
            continue
        if not d:
            continue
        isd = d.get("is") or {}
        checks = {c.get("name"): c for c in (isd.get("checks") or [])}
        cw = (checks.get("CONCENTRATED_WEIGHT") or {}).get("result") or "?"
        fails = [n for n, c in checks.items() if c.get("result") == "FAIL"]
        x["conc_weight"] = cw
        x["fails"] = fails
        x["ladder"] = (checks.get("IS_LADDER_SHARPE") or {}).get("value")
        x["robust"] = (checks.get("LOW_ROBUST_UNIVERSE_SHARPE") or {}).get("value")
        x["cluster"] = (checks.get("CLUSTER_TEST") or {}).get("value")
        raw = d.get("regular")
        x["expr"] = (raw.get("code") if isinstance(raw, dict) else raw) or ""
        if fails:
            fail_list.append(x)
        elif cw != "PASS":
            cw_warn.append(x)
        else:
            ok_list.append(x)
        if i % 25 == 0:
            print(f"  ...{i}/{len(pre)}")

    ok_list.sort(key=lambda x: -(x.get("fitness") or 0))
    print(f"\n=== 结果 ===")
    print(f"  可提交（无 FAIL + CW=PASS）：{len(ok_list)} 颗")
    print(f"  CW=WARNING：{len(cw_warn)} 颗")
    print(f"  其他 FAIL：{len(fail_list)} 颗")

    print(f"\n=== 可提交清单（非 USA，按 fitness 降序） ===")
    print(f"{'alpha_id':<10}{'reg':<5}{'sharpe':>7}{'fit':>7}{'to':>8}"
          f"{'ladder':>7}{'robust':>7}  univ/neut")
    for x in ok_list:
        print(f"{x['alpha_id']:<10}{x['region']:<5}{x['sharpe']:>7}"
              f"{x['fitness']:>7}{x['turnover']:>8}"
              f"{str(x.get('ladder')):>7}{str(x.get('robust')):>7}  "
              f"{x['universe']}/{x['neutralization']}")

    if cw_warn:
        print(f"\n=== CW=WARNING（提交必 FAIL） ===")
        for x in cw_warn[:12]:
            print(f"  {x['alpha_id']:<10}{x['region']:<5}sharpe={x['sharpe']} fit={x['fitness']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"submittable": ok_list, "cw_warn": cw_warn,
                               "is_fail": fail_list},
                              ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
