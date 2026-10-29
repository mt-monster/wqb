# -*- coding: utf-8 -*-
"""通用相关性检查：给定 alpha id 列表，取 self + production 的最大相关性。

为什么单独写一个
----------------
临时脚本反复丢（`_corr_*.py` 被清理过多次）。本工具接受命令行参数，固定保留。

⚠ **prod 必须走 MCP `check_correlation` 的同一后端**（本工具直接用 brain_client，
  与 MCP 工具同源）；但**不要并发起多个**——PC 队列是单通道，多进程会互相打回
  `correlation_busy`。串行、单进程即可；要批量就交给 `--enqueue/--run-queue`
  （``wqb.prod_queue``，一次一条，算完再取下一个）。

用法
----
    python tools/corr_check.py --ids mLowboV5,mLowbo55
    python tools/corr_check.py --ids zq3Kk39K --types production
    python tools/corr_check.py --ids a,b --out results/_p.json --wait 40
    python tools/corr_check.py --ids a,b,c --enqueue          # 只登记队列，不查
    python tools/corr_check.py --run-queue --max-tries 2      # 串行消费队列
    python tools/corr_check.py --queue-stats                  # 队列概况

行为（2026-10-28 改：P0-3 / P1-2）
----------------------------------
1. **默认缓存优先**：``check_correlation(refresh=False)`` → 48h 权威缓存 / 预读
   ``is.prodCorrelation`` 命中即返回，**不触发平台计算**。``--refresh`` 才强制
   重测（终验语义：终验前必须拿到刚算的值）。
2. **按 retry_after 退避**：返回 busy/pending 时按其 ``retry_after`` 睡
   （封顶 ``--sleep-cap``，缺省 60s），不再固定 45s；``inflight=True`` 表示
   平台还在算同一条，等一个 join 窗口后重查即可（**不会二次触发**）。
3. **队列模式**：``--enqueue`` 登记 → ``--run-queue`` 串行消费；每条按自己的
   轮询结果写回 ``done / pending_timeout / error``，``--max-tries`` 封顶。
"""
import argparse
import asyncio
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
sys.path.insert(0, os.path.join(ROOT, "src"))


def _parse_ids(raw: str):
    return [x.strip() for x in (raw or "").split(",") if x.strip()]


async def _query(brain, aid, types, args, got):
    """查一个 alpha 的全部 types；返回本轮看到的 status 与最大 retry_after。"""
    statuses = {}
    retry_after = 0.0
    for ct in types:
        if (got.get(aid) or {}).get(ct):
            continue
        try:
            r = await brain.check_correlation(aid, correlation_type=ct,
                                              threshold=args.threshold,
                                              refresh=args.refresh)
        except Exception as e:  # noqa: BLE001 — 单条失败不中止整轮
            print("%s %s ERR %s %s" % (aid, ct, type(e).__name__, str(e)[:120]), flush=True)
            statuses[ct] = "error"
            continue
        r = r or {}
        chk = (r.get("checks") or {}).get(ct) or {}
        mx = chk.get("max_correlation")
        if mx is None:
            mx = (r.get("correlation") or {}).get("max")
        if mx is not None:
            got.setdefault(aid, {})[ct] = dict(
                max=mx,
                pass_=r.get("all_passed"),
                source=chk.get("source") or "platform",
                provisional=bool(chk.get("provisional")),
                from_cache=bool(chk.get("from_cache")),
            )
            print("%s %-10s = %s%s" % (
                aid, ct, mx,
                " (预读/缓存值，未重测)" if got[aid][ct]["provisional"] or
                got[aid][ct]["from_cache"] else ""), flush=True)
            continue
        st = r.get("status") or chk.get("status") or "unknown"
        statuses[ct] = st
        try:
            ra = float(r.get("retry_after") or chk.get("retry_after") or 0.0)
        except (TypeError, ValueError):
            ra = 0.0
        retry_after = max(retry_after, ra)
        print("%s %-10s status=%s%s%s" % (
            aid, ct, st,
            " retry_after=%gs" % ra if ra else "",
            " inflight(平台计算中，不要重触发)" if r.get("inflight") else ""), flush=True)
    return statuses, retry_after


def _all_done(got, aid, types):
    return all((got.get(aid) or {}).get(t) for t in types)


async def _poll_alpha(brain, aid, types, args, got):
    """一个 alpha 的「触发 + 按 retry_after 重查」循环；返回最后一轮的 statuses。"""
    statuses = {}
    ra = 0.0
    for rnd in range(max(1, args.wait + 1)):
        if _all_done(got, aid, types):
            break
        statuses, ra = await _query(brain, aid, types, args, got)
        if _all_done(got, aid, types) or rnd >= args.wait:
            break
        sleep_s = min(max(ra, args.min_sleep), args.sleep_cap)
        if "error" in statuses.values() and len(statuses) == len(types):
            break  # 全部报错，重试没有意义
        print("  ... %gs 后重查（第 %d/%d 轮）" % (sleep_s, rnd + 1, args.wait), flush=True)
        await asyncio.sleep(sleep_s)
    return statuses


async def _run_queue(brain, types, args, got):
    from wqb import prod_queue as q
    while True:
        aid = q.next_pending()
        if not aid:
            break
        rec = q.get(aid)
        tries = int(rec.get("tries") or 0)
        if tries >= args.max_tries:
            q.mark(aid, status="error", error="max tries (%d) reached" % args.max_tries)
            print("%s 跳过：已达 max-tries=%d" % (aid, args.max_tries), flush=True)
            continue
        print("=== 队列取用 %s（第 %d 次尝试）===" % (aid, tries + 1), flush=True)
        statuses = {}
        try:
            statuses = await _poll_alpha(brain, aid, types, args, got)
        except Exception as e:  # noqa: BLE001
            q.mark(aid, status="error", error="%s: %s" % (type(e).__name__, e))
            print("%s ERROR %s" % (aid, e), flush=True)
            continue
        if _all_done(got, aid, types):
            prod_mx = (got.get(aid) or {}).get("production", {}).get("max")
            self_mx = (got.get(aid) or {}).get("self", {}).get("max")
            q.mark(aid, max_corr=prod_mx if prod_mx is not None else self_mx, status="done")
        elif "data_unavailable" in statuses.values():
            q.mark(aid, status="error", error="data_unavailable（4xx 终态，重试无益）")
        else:
            q.mark(aid, status="pending_timeout",
                   error="; ".join("%s=%s" % kv for kv in statuses.items()))


async def main():
    ap = argparse.ArgumentParser(description="查 self/prod 相关性（缓存优先 + 可选队列消费）")
    ap.add_argument("--ids", default="", help="逗号分隔的 alpha id")
    ap.add_argument("--types", default="production,self", help="默认 production,self")
    ap.add_argument("--out", default=os.path.join(ROOT, "results", "_corr_out.json"))
    ap.add_argument("--wait", type=int, default=45, help="重查轮数上限（每轮按 retry_after 睡）")
    ap.add_argument("--threshold", type=float, default=0.7)
    ap.add_argument("--refresh", action="store_true",
                    help="强制平台重测（终验用）；缺省缓存/预读优先，不触发计算")
    ap.add_argument("--min-sleep", type=float, default=10.0, help="重查间隔下限（秒）")
    # 缺省 260：必须盖住「pending 写完的冷却 195s」与「槽被占的忙提示 240s」，
    # 否则每轮都被截短后再撞一次 busy（2026-10-28 前是 60，一轮 pending 要空转 4 次）。
    ap.add_argument("--sleep-cap", type=float, default=260.0,
                    help="重查间隔上限（秒；缺省 260 ≥ 冷却 195 / 忙提示 240）")
    ap.add_argument("--enqueue", action="store_true", help="只把 --ids 登记进 prod_queue")
    ap.add_argument("--run-queue", action="store_true", help="串行消费 prod_queue")
    ap.add_argument("--queue-stats", action="store_true", help="打印队列概况后退出")
    ap.add_argument("--max-tries", type=int, default=2, help="队列条目最多尝试次数")
    ap.add_argument("--note", default="", help="入队备注")
    ap.add_argument("--clear-done", action="store_true", help="消费前清掉已完成条目")
    a = ap.parse_args()

    from wqb import prod_queue as q
    if a.queue_stats:
        print(json.dumps(q.stats(), ensure_ascii=False, indent=1))
        return

    ids = _parse_ids(a.ids)
    if a.enqueue:
        if not ids:
            ap.error("--enqueue 需要 --ids")
        n = q.push_many(ids, note=a.note)
        print("已登记 %d 条 → %s" % (n, q.queue_path()))
        return

    types = [x.strip() for x in a.types.split(",") if x.strip()]

    from brain_api import brain_client
    await brain_client.ensure_authenticated()

    got = {}
    if a.run_queue:
        if a.clear_done:
            print("清理已完成条目：%d" % q.clear(done_only=True))
        await _run_queue(brain_client, types, a, got)
    else:
        if not ids:
            ap.error("需要 --ids（或用 --run-queue / --queue-stats）")
        print("=== 查询（refresh=%s）===" % a.refresh, flush=True)
        for aid in ids:
            await _poll_alpha(brain_client, aid, types, a, got)

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(got, f, ensure_ascii=False, indent=1)

    print("\n=== 汇总 ===", flush=True)
    for aid in ids or sorted(got):
        d = got.get(aid) or {}
        pr = (d.get("production") or {}).get("max")
        se = (d.get("self") or {}).get("max")
        verdict = "✓ 过" if (pr is not None and pr < a.threshold
                            and (se is None or se < a.threshold)) else ""
        print("  %-12s prod=%-8s self=%-8s %s" % (aid, pr, se, verdict), flush=True)
    print("saved", a.out, flush=True)


if __name__ == "__main__":
    asyncio.run(main())
