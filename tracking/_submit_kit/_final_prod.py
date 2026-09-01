#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""对 NEED_PROD 的候选跑 PROD 平台预检（~30s/颗，单并发）。

带 checkpoint 续跑：结果写入 prod_final_20260901.json，重启自动跳过已完成项。
PROD 预检零成本（不消耗提交配额）。

用法：
    python _final_prod.py              # 续跑，跑完所有
    FINAL_PROD_FRESH=1 python ...      # 强制全新
    FINAL_PROD_TOP=15 python ...       # 只跑前 15 颗（按 fitness 降序）
"""
import asyncio
import json
import os
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
RD = WQ_ROOT / "research-data"

POOL = RD / "final_pool_20260901.json"
CKPT = RD / "prod_final_20260901.json"

TOP = int(os.environ.get("FINAL_PROD_TOP", "0") or 0)
FRESH = os.environ.get("FINAL_PROD_FRESH") == "1"

pool = json.load(open(POOL, encoding="utf-8"))
targets = [r for r in pool if r.get("verdict") == "NEED_PROD"]
# 按 fitness 降序
targets.sort(key=lambda x: (-(x["fitness"] or 0), -(x["sharpe"] or 0)))
if TOP:
    targets = targets[:TOP]

done = {}
if CKPT.exists() and not FRESH:
    done = json.load(open(CKPT, encoding="utf-8"))
    done = {k: v for k, v in done.items() if "prod" in v}

todo = [r for r in targets if r["id"] not in done]
print(f"[INFO] 待检 {len(targets)} 颗，已完成 {len(targets) - len(todo)}，本轮跑 {len(todo)}")
print(f"[INFO] 预计耗时 ~{len(todo) * 32 / 60:.1f} 分钟")


def save():
    tmp = str(CKPT) + ".tmp"
    json.dump(done, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(tmp, CKPT)


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    for i, r in enumerate(todo, 1):
        aid = r["id"]
        for att in range(3):
            try:
                p = await brain.check_correlation(
                    aid, correlation_type="production", threshold=0.7)
                pc = (p.get("checks") or {}).get("production") or {}
                done[aid] = {
                    "prod": pc.get("max_correlation"),
                    "pass": pc.get("passes_check"),
                    "region": r["region"],
                    "sharpe": r["sharpe"], "fitness": r["fitness"],
                    "turnover": r["turnover"],
                    "self": (r.get("self") or {}).get("max"),
                }
                flag = "PASS" if pc.get("passes_check") else "FAIL"
                print(f"  [{i:>3}/{len(todo)}] {aid:<10} {str(r['region']):<4} "
                      f"fit={r['fitness']:>5.2f}  PROD={pc.get('max_correlation')} {flag}",
                      flush=True)
                break
            except Exception as e:
                if att == 2:
                    done[aid] = {"prod": None, "pass": None,
                                 "error": f"{type(e).__name__}",
                                 "region": r["region"]}
                    print(f"  [{i:>3}/{len(todo)}] {aid:<10} ERR {type(e).__name__}",
                          flush=True)
                else:
                    await asyncio.sleep(5)
        save()
        await asyncio.sleep(1.5)  # 平台节流

    save()
    print(f"\n[saved] {CKPT}")

    # 汇总
    ok = [(k, v) for k, v in done.items() if v.get("pass") is True]
    bad = [(k, v) for k, v in done.items() if v.get("pass") is False]
    err = [(k, v) for k, v in done.items() if v.get("pass") is None]
    print(f"\n=== PROD 预检汇总: PASS={len(ok)}  FAIL={len(bad)}  ERR={len(err)} ===")
    if ok:
        print("\n--- PASS（双闸全过，可提交） ---")
        print(f"{'id':<10} {'reg':<5} {'shrp':>5} {'fit':>5} {'to':>7} {'SELF':>6} {'PROD':>7}")
        for k, v in sorted(ok, key=lambda x: -(x[1].get("fitness") or 0)):
            print(f"{k:<10} {str(v.get('region')):<5} {v.get('sharpe',0):>5.2f} "
                  f"{v.get('fitness',0):>5.2f} {v.get('turnover',0):>7.4f} "
                  f"{v.get('self') or 0:>6.3f} {v.get('prod'):>7.4f}")
    print("\n--- FAIL（PROD >= 0.7） ---")
    for k, v in sorted(bad, key=lambda x: -(x[1].get("prod") or 0)):
        print(f"  {k:<10} {str(v.get('region')):<5} fit={v.get('fitness',0):>5.2f} "
              f"PROD={v.get('prod')}")
    if err:
        print("\n--- ERR ---")
        for k, v in err:
            print(f"  {k:<10} {v.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())
