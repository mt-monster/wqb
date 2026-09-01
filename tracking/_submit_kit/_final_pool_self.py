#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""最终候选池：73 颗 REGULAR + MEA 补漏 6 颗 -> 合并 -> SELF 快筛（本地秒级）。

SELF 用本地 OS PnL 池，无并发锁，秒级；PASS(<0.7) 的才值得花 30s 跑 PROD。
"""
import asyncio
import json
import sys
from pathlib import Path
from collections import Counter

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
RD = WQ_ROOT / "research-data"

REG = RD / "submittable_regular_20260901.json"
MEA = RD / "mea7_cw_20260901.json"
PC1 = RD / "submittable_precheck_20260901.json"
PC2 = RD / "prod_batch2_20260901.json"
OUT = RD / "final_pool_20260901.json"

pool = json.load(open(REG, encoding="utf-8"))["regular"]
print(f"[INFO] REGULAR 池: {len(pool)}")

# --- 已知结果 ---
known_self, known_prod = {}, {}
pc1 = json.load(open(PC1, encoding="utf-8"))
for k, v in (pc1.get("self") or {}).items():
    known_self[k] = v
for k, v in (pc1.get("prod") or {}).items():
    known_prod[k] = v
for k, v in json.load(open(PC2, encoding="utf-8")).items():
    known_prod[k] = {"max": v["prod"], "pass": v["pass"]}
# MEA 已实测 PROD
MEA_KNOWN_PROD = {"qMjLYVVP": 0.5791, "Jj7ee6nO": 0.6320, "omqEE1pn": 0.6698}
for k, v in MEA_KNOWN_PROD.items():
    known_prod[k] = {"max": v, "pass": v < 0.7}

print(f"[INFO] 已知 SELF: {len(known_self)}  已知 PROD: {len(known_prod)}")

# --- 待补拉的 MEA 候选 ---
mea = json.load(open(MEA, encoding="utf-8"))
have = {r["id"] for r in pool}
add_ids = [k for k, v in mea.items()
           if k not in have and v.get("cw") == "PASS" and not v.get("fails")]
print(f"[INFO] MEA 需补入: {add_ids}")


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    # 补拉 MEA 候选详情
    sem = asyncio.Semaphore(3)

    async def one(aid):
        for att in range(3):
            try:
                async with sem:
                    resp = await brain._request(
                        "GET", f"{brain.base_url}/alphas/{aid}")
                j = resp.json()
            except Exception:
                if att == 2:
                    return None
                await asyncio.sleep(3)
                continue
            raw = j.get("regular")
            code = raw.get("code") if isinstance(raw, dict) else raw
            st = j.get("settings") or {}
            isd = j.get("is") or {}
            return {
                "id": aid,
                "type": j.get("type"),
                "region": st.get("region"),
                "sharpe": isd.get("sharpe"),
                "fitness": isd.get("fitness"),
                "turnover": isd.get("turnover"),
                "returns": isd.get("returns"),
                "universe": st.get("universe"),
                "delay": st.get("delay"),
                "neut": st.get("neutralization"),
                "decay": st.get("decay"),
                "trunc": st.get("truncation"),
                "expr": code or "",
                "fam_size": 1, "fam_members": [],
                "src": "mea_patch",
            }

    res = await asyncio.gather(*[one(a) for a in add_ids])
    added = [r for r in res if r and r.get("type") == "REGULAR"]
    for r in res:
        if r and r.get("type") != "REGULAR":
            print(f"  [skip] {r['id']} type={r.get('type')}")
    print(f"[INFO] MEA 补入 REGULAR: {len(added)}")

    full = pool + added
    # 去重
    seen, uniq = set(), []
    for r in full:
        if r["id"] not in seen:
            seen.add(r["id"])
            uniq.append(r)

    print(f"[INFO] 最终池: {len(uniq)} 颗  区域:",
          dict(Counter(r["region"] for r in uniq)))

    # --- SELF 快筛（只跑未测的） ---
    todo = [r for r in uniq if r["id"] not in known_self]
    print(f"[INFO] 需跑 SELF: {len(todo)}")

    sem2 = asyncio.Semaphore(4)

    async def do_self(r):
        for att in range(3):
            try:
                async with sem2:
                    s = await brain.check_self_correlation(r["id"])
                known_self[r["id"]] = {"max": s.get("max_correlation"),
                                       "pass": s.get("passes_check")}
                return
            except Exception:
                if att == 2:
                    known_self[r["id"]] = {"error": "timeout"}
                else:
                    await asyncio.sleep(3)

    await asyncio.gather(*[do_self(r) for r in todo])

    # 汇总
    for r in uniq:
        r["self"] = known_self.get(r["id"], {})
        r["prod"] = known_prod.get(r["id"], {})
        if not r["prod"] and r["self"].get("pass") is False:
            r["verdict"] = "SELF_FAIL"
        elif r["prod"].get("pass") is True:
            r["verdict"] = "READY"
        elif r["prod"].get("pass") is False:
            r["verdict"] = "PROD_FAIL"
        elif r["self"].get("pass") is True:
            r["verdict"] = "NEED_PROD"
        else:
            r["verdict"] = "UNKNOWN"

    vc = Counter(r["verdict"] for r in uniq)
    print("\n[INFO] 判定分布:", dict(vc))

    uniq.sort(key=lambda x: (-(x["fitness"] or 0), -(x["sharpe"] or 0)))
    json.dump(uniq, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[saved] {OUT}")

    # 打印 NEED_PROD（接下来要花 30s/颗 跑的）
    np_ = [r for r in uniq if r["verdict"] == "NEED_PROD"]
    print(f"\n=== 需跑 PROD 的候选: {len(np_)} ===")
    print(f"{'#':>3} {'id':<10} {'reg':<4} {'shrp':>5} {'fit':>5} {'to':>6} {'SELF':>6}")
    for i, r in enumerate(np_, 1):
        print(f"{i:>3} {r['id']:<10} {str(r['region']):<4} {r['sharpe']:>5.2f} "
              f"{r['fitness']:>5.2f} {r['turnover']:>6.4f} "
              f"{r['self'].get('max', 0):>6.3f}")

    print("\n=== 已判定 READY（双闸全过） ===")
    for r in uniq:
        if r["verdict"] == "READY":
            print(f"  {r['id']:<10} {str(r['region']):<4} shrp={r['sharpe']:>5.2f} "
                  f"fit={r['fitness']:>5.2f} to={r['turnover']:.4f} "
                  f"SELF={r['self'].get('max', 0):.4f} PROD={r['prod'].get('max')}")


if __name__ == "__main__":
    asyncio.run(main())
