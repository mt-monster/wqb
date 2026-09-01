#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""最终裁决（只读）：现在到底还有哪些可以提交。

输入：prod_final_20260901.json（双闸实测）+ final_pool（expr/家族）+ 08-31 READY 3 颗。
步骤：
  1) 12 颗候选（10 双闸过 + 2 边缘）逐颗 get_alpha_details：
     status 必须 UNSUBMITTED、IS checks 无 FAIL、抓 expr/settings
  2) 配额精算：ACTIVE 池 dateSubmitted 时间戳 → 48h 滚动窗口内 REGULAR/SUPER 已用数
     + 下一个名额释放时间；用 78jYpn0Z→释放 反推 SUPER 窗口
  3) 同区候选 expr 家族去重（归一化比较），防止"提 1 颗顶死同族其余"
输出：research-data/final_verdict_20260901.json
"""
import asyncio
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
RD = WQ_ROOT / "research-data"
OUT = RD / "final_verdict_20260901.json"

prod_final = json.load(open(RD / "prod_final_20260901.json", encoding="utf-8"))
pool = {x["id"]: x for x in json.load(open(RD / "final_pool_20260901.json", encoding="utf-8"))}

# 双闸 PASS（prod_final）+ 08-31 平台已验 READY 3 颗（MEA，book 未变仍有效）
READY_0831 = {
    "qMjLYVVP": {"prod": 0.5791, "self": 0.4508},
    "Jj7ee6nO": {"prod": 0.632, "self": 0.6086},
    "omqEE1pn": {"prod": 0.6698, "self": 0.6218},
}
FINALISTS = {k: v for k, v in prod_final.items() if v.get("pass") is True}
for k, v in READY_0831.items():
    if k not in FINALISTS:
        base = pool.get(k, {})
        FINALISTS[k] = {"prod": v["prod"], "self": v["self"],
                        "region": base.get("region", "MEA"),
                        "sharpe": base.get("sharpe"), "fitness": base.get("fitness"),
                        "turnover": base.get("turnover"), "src": "ready_0831"}
# 边缘（过线但余量 <0.02，仅供监控，不建议排队列）
EDGE = ["ak7KQoXv", "E5l6mmqJ"]


def norm_expr(e):
    return "".join((e or "").split()).lower()


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    report = {"finalists": {}, "edge": {}, "quota": {}, "family": {}}

    # ---------- 1) 候选状态复核 ----------
    print("=== 1) 候选状态复核 ===")
    dead = []
    for aid, meta in list(FINALISTS.items()) + [(a, {}) for a in EDGE]:
        try:
            d = await brain.get_alpha_details(aid)
        except Exception as e:
            print(f"  {aid}: ERR {e}")
            continue
        if not d:
            dead.append((aid, "NOT_FOUND"))
            continue
        status = d.get("status")
        isd = d.get("is") or {}
        checks = {c.get("name"): c for c in (isd.get("checks") or [])}
        fails = [n for n, c in checks.items() if c.get("result") == "FAIL"]
        cw = (checks.get("CONCENTRATED_WEIGHT") or {}).get("result")
        raw = d.get("regular")
        expr = (raw.get("code") if isinstance(raw, dict) else raw) or ""
        st = d.get("settings") or {}
        row = {
            "status": status, "region": st.get("region"),
            "universe": st.get("universe"), "delay": st.get("delay"),
            "neutralization": st.get("neutralization"),
            "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
            "turnover": isd.get("turnover"),
            "conc_weight": cw, "is_fails": fails,
            "expr": expr,
            "prod": meta.get("prod"), "self": meta.get("self"),
        }
        if status != "UNSUBMITTED":
            dead.append((aid, f"status={status}"))
            print(f"  {aid}: ⚠️ status={status}（退出候选）")
            if aid in FINALISTS:
                FINALISTS.pop(aid)
                report["finalists"][aid] = row
            continue
        if fails:
            print(f"  {aid}: ⚠️ 新增 IS FAIL {fails}（退出候选）")
            dead.append((aid, f"is_fails={fails}"))
            if aid in FINALISTS:
                FINALISTS.pop(aid)
            report["edge" if aid in EDGE else "finalists"][aid] = row
            continue
        tgt = "edge" if aid in EDGE else "finalists"
        report[tgt][aid] = row
        print(f"  {aid}: OK status=UNSUBMITTED CW={cw} "
              f"sh={isd.get('sharpe')} fit={isd.get('fitness')} "
              f"PROD={meta.get('prod')} SELF={meta.get('self')}")
    if dead:
        report["dead"] = dead

    # ---------- 2) 配额精算 ----------
    print("\n=== 2) 48h 滚动配额精算 ===")
    rows = []
    offset = 0
    while True:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"limit": 100, "offset": offset, "status": "ACTIVE",
                    "order": "-dateSubmitted"})
        if r.status_code != 200:
            print(f"  [ERR] {r.status_code} {r.text[:150]}")
            break
        j = r.json()
        batch = j.get("results") or []
        rows.extend(batch)
        if j.get("next") is None or not batch or offset >= 300:
            break
        offset += len(batch)

    now = datetime.now(timezone.utc)
    win = timedelta(hours=48)
    reg_used, sup_used = [], []
    for a in rows:
        ds = a.get("dateSubmitted")
        if not ds:
            continue
        try:
            t = datetime.fromisoformat(ds)
        except ValueError:
            continue
        if now - t <= win:
            (sup_used if a.get("type") == "SUPER" else reg_used).append(
                {"id": a.get("id"), "at_et": ds, "at_utc": t.astimezone(timezone.utc).isoformat()})
    reg_used.sort(key=lambda x: x["at_utc"])
    sup_used.sort(key=lambda x: x["at_utc"])
    print(f"  现在 UTC={now.isoformat()} (ET {now.astimezone(timezone(timedelta(hours=-4))).strftime('%m-%d %H:%M')})")
    print(f"  REGULAR 48h 已用 {len(reg_used)}/4:")
    for x in reg_used:
        free_at = (datetime.fromisoformat(x["at_utc"]) + win).astimezone(
            timezone(timedelta(hours=-4)))
        print(f"    {x['id']:<10} {x['at_et']} → 释放 ET {free_at.strftime('%m-%d %H:%M')}"
              f"（GMT+8 {free_at.astimezone(timezone(timedelta(hours=8))).strftime('%m-%d %H:%M')}）")
    print(f"  SUPER 48h 已用 {len(sup_used)}/1:")
    for x in sup_used:
        free_at = (datetime.fromisoformat(x["at_utc"]) + win).astimezone(
            timezone(timedelta(hours=8)))
        print(f"    {x['id']:<10} {x['at_et']} → 释放 GMT+8 {free_at.strftime('%m-%d %H:%M')}")
    report["quota"] = {"now_utc": now.isoformat(), "reg_used_48h": reg_used,
                       "sup_used_48h": sup_used}

    # ---------- 3) 同区 expr 家族去重 ----------
    print("\n=== 3) 同区候选 expr 家族检查 ===")
    all_rows = {**report.get("finalists", {}), **report.get("edge", {})}
    by_reg = {}
    for aid, row in all_rows.items():
        by_reg.setdefault(row.get("region"), []).append(aid)
    for reg, aids in by_reg.items():
        if len(aids) < 2:
            continue
        groups = []
        for aid in aids:
            e = norm_expr(all_rows[aid].get("expr"))
            hit = None
            for g in groups:
                a0 = norm_expr(all_rows[g[0]].get("expr"))
                if e and a0 and (e == a0):
                    hit = g
                    break
            if hit:
                hit.append(aid)
            else:
                groups.append([aid])
        report["family"][reg] = groups
        for g in groups:
            tag = " ⚠️ 同族（只提 1 颗）" if len(g) > 1 else ""
            print(f"  [{reg}] {g}{tag}")

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
