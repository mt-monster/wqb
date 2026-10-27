# -*- coding: utf-8 -*-
"""等待平台 prod 锁释放并测单个 alpha 的 prod（严格尊重 retry_after，不轮询轰炸）。

背景：prod 端点是**账号级单并发**，被占用时返回
  {"status":"correlation_busy","retry_after":180,"max":null}
旧 check_prod 每 10s 重打 ⇒ 自锁。本脚本按 retry_after 精确退避。

用法： python tools/prod_wait.py leMnPeJ2 [--minutes 45]
产出： results/prod_wait_<alpha>.json
"""
import argparse, asyncio, json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
from brain_api import BrainApiClient  # noqa: E402


def parse(j):
    if not isinstance(j, dict):
        return None
    sch = j.get("schema") or {}
    for v in ((sch or {}).get("max"), j.get("max"), j.get("max_correlation")):
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                pass
    mx = None
    for row in (j.get("records") or []):
        vals = row if isinstance(row, (list, tuple)) else list(row.values())
        for v in vals:
            if isinstance(v, (int, float)) and (mx is None or v > mx):
                mx = float(v)
    return mx


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alpha_id")
    ap.add_argument("--minutes", type=float, default=45)
    args = ap.parse_args()
    out = os.path.join(ROOT, "results", f"prod_wait_{args.alpha_id}.json")

    b = BrainApiClient(); await b.ensure_authenticated()
    deadline = time.time() + args.minutes * 60
    n = 0
    while time.time() < deadline:
        n += 1
        try:
            j = await b.get_production_correlation(args.alpha_id)
        except Exception as e:
            print(f"[{n}] EXC {type(e).__name__}: {str(e)[:120]}", flush=True)
            await asyncio.sleep(20); continue
        st = (j or {}).get("status") if isinstance(j, dict) else None
        if st == "correlation_busy":
            ra = float((j or {}).get("retry_after") or 180)
            wait = min(max(ra + 5, 30), 320)
            left = int(deadline - time.time())
            print(f"[{n}] busy，退避 {wait:.0f}s（剩余 {left}s）", flush=True)
            await asyncio.sleep(wait); continue
        v = parse(j)
        if v is not None:
            print(f"[{n}] ★ prod = {v}", flush=True)
            json.dump({"alpha_id": args.alpha_id, "prod": v, "at": time.strftime("%F %T")},
                      open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(f"已写 {out}", flush=True); return
        print(f"[{n}] status={st} 无值，20s 后重试", flush=True)
        await asyncio.sleep(20)
    print("超时未取到", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
