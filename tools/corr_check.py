# -*- coding: utf-8 -*-
"""通用相关性检查：给定 alpha id 列表，取 self + production 的最大相关性。

为什么单独写一个
----------------
临时脚本反复丢（`_corr_*.py` 被清理过多次）。本工具接受命令行参数，固定保留。

⚠ **prod 必须走 MCP `check_correlation` 的同一后端**（本工具直接用 brain_client，
  与 MCP 工具同源）；但**不要并发起多个**——PC 队列是单通道，多进程会互相打回
  `correlation_busy`。串行、单进程即可。

用法
----
    python tools/corr_check.py --ids mLowboV5,mLowbo55
    python tools/corr_check.py --ids zq3Kk39K --types production
    python tools/corr_check.py --ids a,b --out results/_p.json --wait 40

行为
----
1. 先 `refresh=True` 触发计算（平台异步，触发时通常返回 busy/None）
2. 再按 `--wait` 轮询 `refresh=False` 读缓存，每轮 45s
3. 打印 max + passes，并把含直方图的结果写到 --out
"""
import argparse
import asyncio
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True, help="逗号分隔的 alpha id")
    ap.add_argument("--types", default="production,self", help="默认 production,self")
    ap.add_argument("--out", default=os.path.join(ROOT, "results", "_corr_out.json"))
    ap.add_argument("--wait", type=int, default=45, help="轮询轮数（每轮 45s）")
    ap.add_argument("--threshold", type=float, default=0.7)
    a = ap.parse_args()

    ids = [x.strip() for x in a.ids.split(",") if x.strip()]
    types = [x.strip() for x in a.types.split(",") if x.strip()]
    from brain_api import brain_client
    await brain_client.ensure_authenticated()

    got = {}
    print("=== 触发计算 ===", flush=True)
    for aid in ids:
        for ct in types:
            try:
                r = await brain_client.check_correlation(aid, correlation_type=ct,
                                                        threshold=a.threshold, refresh=True)
                c = (r or {}).get("correlation") or {}
                if c.get("max") is not None:
                    got.setdefault(aid, {})[ct] = dict(max=c.get("max"),
                                                      pass_=(r or {}).get("all_passed"),
                                                      hist=c.get("histogram_nonzero"))
                    print("%s %-10s = %s" % (aid, ct, c.get("max")), flush=True)
                else:
                    print("%s %-10s 触发 status=%s" % (aid, ct, (r or {}).get("status")), flush=True)
            except Exception as e:
                print("%s %s ERR %s %s" % (aid, ct, type(e).__name__, str(e)[:80]), flush=True)

    for _ in range(a.wait):
        pending = [(i, t) for i in ids for t in types
                   if not ((got.get(i) or {}).get(t))]
        if not pending:
            break
        for aid, ct in pending:
            try:
                r = await brain_client.check_correlation(aid, correlation_type=ct,
                                                        threshold=a.threshold, refresh=False)
            except Exception:
                continue
            c = (r or {}).get("correlation") or {}
            if c.get("max") is not None:
                got.setdefault(aid, {})[ct] = dict(max=c.get("max"),
                                                  pass_=(r or {}).get("all_passed"),
                                                  hist=c.get("histogram_nonzero"))
                print("%s %-10s = %s" % (aid, ct, c.get("max")), flush=True)
        if len(pending) == 0:
            break
        await asyncio.sleep(45)

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(got, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n=== 汇总 ===", flush=True)
    for aid in ids:
        d = got.get(aid) or {}
        pr = (d.get("production") or {}).get("max")
        se = (d.get("self") or {}).get("max")
        verdict = "✓ 过" if (pr is not None and pr < a.threshold
                            and (se is None or se < a.threshold)) else ""
        print("  %-12s prod=%-8s self=%-8s %s" % (aid, pr, se, verdict), flush=True)
    print("saved", a.out, flush=True)


if __name__ == "__main__":
    asyncio.run(main())
