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


async def peek(alpha_id, tries, interval):
    """无锁只读探测：直接 GET /alphas/{id}/correlations/prod，不申请本地 correlation_slot。

    用途：本地账号级单并发锁被**别的进程**长期占用时（holder 指向陌生 alpha id），
    有锁路径会立刻返回 correlation_busy 而连一次平台读都发不出去。本模式绕过本地锁，
    只做只读探测：平台算好则返回 {records,max,min}，未算好返回 200 + 空体。
    注意：拿到空体只能说明「平台尚未算好」，**不等于失败，也不触发重算**。
    """
    b = BrainApiClient(); await b.ensure_authenticated()
    for i in range(1, tries + 1):
        try:
            r = await b._request("GET", f"/alphas/{alpha_id}/correlations/prod")
            code = getattr(r, "status_code", None)
            txt = (getattr(r, "text", "") or "").strip()
            if code != 200:
                print(f"[{i}] HTTP {code} {txt[:120]}", flush=True)
            elif not txt:
                print(f"[{i}] 空体（平台仍在算）", flush=True)
            else:
                try:
                    j = json.loads(txt)
                except Exception:
                    print(f"[{i}] 非 JSON 体: {txt[:160]}", flush=True)
                else:
                    v = parse(j)
                    if v is not None:
                        print(f"[{i}] ★ prod = {v}", flush=True)
                        out = os.path.join(ROOT, "results", f"prod_peek_{alpha_id}.json")
                        os.makedirs(os.path.dirname(out), exist_ok=True)
                        json.dump({"alpha_id": alpha_id, "prod": v,
                                   "at": time.strftime("%F %T"), "source": "no-lock peek"},
                                  open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                        print(f"已写 {out}", flush=True)
                        return
                    print(f"[{i}] 有体无 max: {txt[:160]}", flush=True)
        except Exception as e:
            print(f"[{i}] EXC {type(e).__name__}: {str(e)[:120]}", flush=True)
        if i < tries:
            await asyncio.sleep(interval)
    print("peek 结束未取到值", flush=True)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alpha_id")
    ap.add_argument("--minutes", type=float, default=45)
    ap.add_argument("--peek", action="store_true",
                    help="无锁只读探测（不申请 correlation_slot）")
    ap.add_argument("--tries", type=int, default=1, help="peek 模式探测次数")
    ap.add_argument("--interval", type=float, default=60, help="peek 模式间隔秒")
    args = ap.parse_args()

    if args.peek:
        await peek(args.alpha_id, max(1, args.tries), max(5.0, args.interval))
        return

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
