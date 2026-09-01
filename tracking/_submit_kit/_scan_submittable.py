# -*- coding: utf-8 -*-
"""全量可提交候选扫描（只读）。

筛选口径（含 2026-09-01 新增的隐形第四闸）：
  1) status = UNSUBMITTED
  2) IS checks 无 FAIL
  3) CONCENTRATED_WEIGHT = PASS（WARNING 的提交后必 FAIL，直接排除）
  4) 指标基本达标：sharpe >= 1.58(d1) / fitness >= 1.0 / turnover 在 (0.01, 0.4)

输出可提交清单（按 fitness 降序），并对 top N 做 SELF 本地预检。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

OUT = WQ_ROOT / "research-data" / "submittable_scan_20260901.json"

# 指标下限（平台 d1 常规口径）
MIN_SHARPE = 1.58
MIN_FIT = 1.0
TO_LO, TO_HI = 0.01, 0.4


async def fetch_unsubmitted(brain):
    rows = []
    offset = 0
    while True:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"limit": 100, "offset": offset, "status": "UNSUBMITTED",
                    "order": "-is.fitness"},
        )
        if r.status_code != 200:
            print(f"[ERR] {r.status_code} {r.text[:200]}")
            break
        j = r.json()
        batch = j.get("results") or []
        rows.extend(batch)
        if j.get("next") is None or not batch or offset >= 1000:
            break
        offset += len(batch)
    return rows


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    print("=== 拉取 UNSUBMITTED 全量 ===")
    rows = await fetch_unsubmitted(brain)
    print(f"共 {len(rows)} 颗")

    by_region = {}
    for a in rows:
        reg = (a.get("settings") or {}).get("region") or "?"
        by_region.setdefault(reg, []).append(a)
    print("区域分布：" + "  ".join(f"{k}={len(v)}" for k, v in
                                   sorted(by_region.items(), key=lambda x: -len(x[1]))))

    # 指标初筛（用列表里的 is 数据，省一次请求）
    pre = []
    for a in rows:
        isd = a.get("is") or {}
        st = a.get("settings") or {}
        sh, fit, to = isd.get("sharpe"), isd.get("fitness"), isd.get("turnover")
        if sh is None or fit is None:
            continue
        pre.append({
            "alpha_id": a.get("id"), "region": reg_of(a), "sharpe": sh,
            "fitness": fit, "turnover": to, "returns": isd.get("returns"),
            "universe": st.get("universe"), "delay": st.get("delay"),
            "neutralization": st.get("neutralization"),
            "dateCreated": a.get("dateCreated") or a.get("dateSubmitted"),
            "_metrics_ok": (
                (sh >= MIN_SHARPE if st.get("delay") == 1 else sh >= 2.0)
                and fit >= MIN_FIT
                and to is not None and TO_LO <= to <= TO_HI
            ),
        })
    print(f"有指标的：{len(pre)} 颗，其中指标达标：{sum(1 for x in pre if x['_metrics_ok'])} 颗")

    # 逐颗读 checks（只查指标达标的，省时）
    targets = [x for x in pre if x["_metrics_ok"]]
    print(f"\n=== 读取 {len(targets)} 颗的 IS checks ===")
    ok_list, cw_warn, fail_list = [], [], []
    for i, x in enumerate(targets, 1):
        try:
            d = await brain.get_alpha_details(x["alpha_id"])
        except Exception as e:
            x["_err"] = str(e)[:80]
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
        x["sub_univ"] = (checks.get("LOW_SUB_UNIVERSE_SHARPE") or {}).get("value")
        raw = d.get("regular")
        x["expr"] = (raw.get("code") if isinstance(raw, dict) else raw) or ""
        if fails:
            fail_list.append(x)
        elif cw != "PASS":
            cw_warn.append(x)
        else:
            ok_list.append(x)
        if i % 20 == 0:
            print(f"  ...已处理 {i}/{len(targets)}")

    ok_list.sort(key=lambda x: -(x.get("fitness") or 0))
    print(f"\n=== 结果 ===")
    print(f"  可提交（无 FAIL + CONC_WEIGHT=PASS）：{len(ok_list)} 颗")
    print(f"  CONCENTRATED_WEIGHT=WARNING（必 FAIL）：{len(cw_warn)} 颗")
    print(f"  其他 IS FAIL：{len(fail_list)} 颗")

    print(f"\n=== 可提交清单（按 fitness 降序） ===")
    print(f"{'alpha_id':<10}{'reg':<5}{'sharpe':>7}{'fit':>7}{'to':>8}"
          f"{'ladder':>7}{'robust':>7}{'cluster':>8}  univ/neut")
    for x in ok_list[:30]:
        print(f"{x['alpha_id']:<10}{x['region']:<5}{x['sharpe']:>7}"
              f"{x['fitness']:>7}{str(x['turnover']):>8}"
              f"{str(x.get('ladder')):>7}{str(x.get('robust')):>7}"
              f"{str(x.get('cluster')):>8}  {x['universe']}/{x['neutralization']}")

    if cw_warn:
        print(f"\n=== CONCENTRATED_WEIGHT=WARNING（排除，提交必 FAIL） ===")
        for x in cw_warn[:15]:
            print(f"  {x['alpha_id']:<10}{x['region']:<5}sharpe={x['sharpe']} "
                  f"fit={x['fitness']}  {x['universe']}/{x['neutralization']}")
    if fail_list:
        print(f"\n=== 其他 IS FAIL ===")
        for x in fail_list[:15]:
            print(f"  {x['alpha_id']:<10}{x['region']:<5}sharpe={x['sharpe']} "
                  f"fit={x['fitness']}  FAIL={x['fails'][:3]}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "total_unsubmitted": len(rows),
        "submittable": ok_list, "conc_warn": cw_warn, "is_fail": fail_list,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


def reg_of(a):
    return (a.get("settings") or {}).get("region") or "?"


if __name__ == "__main__":
    asyncio.run(main())
