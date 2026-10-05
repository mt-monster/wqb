#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prod_scan.py — 耐心轮询 prod 相关性并落 wqb 库（2026-10-04）。

为什么不用 `tools/prod_bucket_scan.py`：那个只做 4 次 ×12s 的短重试，而平台 prod
是**单账号单并发**的异步计算（首次 GET 触发服务端计算），多会话/多 alpha 排队时
48s 往往不够 ⇒ 全部返回 None。

本脚本：
  1) 逐个 alpha 轮询 `GET /alphas/{id}/correlations/prod`（默认每颗最多 8 分钟，
     间隔 20s），拿到直方图后立刻停；
  2) 解析 `max` 与 `n[0.7,0.8)`，按「n=0 可扫 / n>=1 单钉子」给判定；
  3) **写入 `data/wqb.db::alpha_corr_cache`**（复用 store 层 CorrCacheMixin），
     下次查询即可秒回，且多进程共享；
  4) 已在缓存里的默认跳过（`--refresh` 可强刷）。

用法::

    python tools/probe/prod_scan.py A1 B2 C3
    python tools/probe/prod_scan.py --file ids.txt --max-wait 480
    python tools/probe/prod_scan.py --file ids.txt --refresh --no-persist
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(ROOT / "src"))


def bucket_n(records, lo=0.7, hi=0.8):
    """取 [lo,hi) 桶的计数（平台返回直方图 records）。"""
    for row in records or []:
        if isinstance(row, (list, tuple)) and len(row) >= 3:
            try:
                if abs(float(row[0]) - lo) < 1e-9 and abs(float(row[1]) - hi) < 1e-9:
                    return int(row[2])
            except (TypeError, ValueError):
                continue
    return None


async def poll_prod(brain, alpha_id, max_wait, interval, verbose=True):
    """轮询直到拿到直方图或超时。返回 (data|None, 说明)。"""
    import time
    deadline = time.time() + max_wait
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        try:
            r = await brain._request("GET", brain.base_url + f"/alphas/{alpha_id}/correlations/prod")
            if r.status_code < 400:
                text = (r.text or "").strip()
                if text:
                    d = r.json() or {}
                    if d.get("max") is not None:
                        if verbose:
                            print(f"    [prod ok] {alpha_id} 第 {attempt} 次取到 max={d['max']}")
                        return d, "ok"
        except Exception as e:
            if verbose and attempt % 5 == 1:
                print(f"    [warn] {alpha_id} 第 {attempt} 次异常 {type(e).__name__}")
        await asyncio.sleep(interval)
    return None, f"timeout after {max_wait}s"


async def main_async(a):
    # ★ 本文件从 tools/probe/prod_scan.py 拷来，后者依赖调用方已把 MCP 目录加进 sys.path；
    #   在 tracking/<R>/scripts/ 下独立跑时必须自己引导（见 run_wave_single_fanout.py 同款）。
    #   _pyenv 在 tools/ 下，提供 bootstrap_paths() 把 MCP 目录加进 sys.path。
    if "brain_api" not in sys.modules:
        try:
            import brain_api  # noqa: F401
        except ModuleNotFoundError:
            sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
            import _pyenv
            _pyenv.bootstrap_paths()
    from brain_api import brain_client as brain
    await brain.ensure_authenticated()

    store = None
    if a.persist:
        try:
            from wqb.store import CampaignStore
            store = CampaignStore.from_workspace()
        except Exception as e:
            print(f"[prod-scan] 落库不可用（{type(e).__name__}: {e}），仅打印")

    print(f"{'id':12s} {'prod_max':>9s} {'n[.7,.8)':>9s}  {'判定':<14s} note")
    for aid in a.alpha_ids:
        if store and not a.refresh:
            cached = store.get_corr_cache(aid)
            if cached and cached.get("prod_correlation") is not None:
                print(f"{aid:12s} {cached['prod_correlation']:>9.4f} {'(缓存)':>9s}  "
                      f"{'CACHE':<14s} src={cached.get('source')} at={cached.get('checked_at')}")
                continue
        data, note = await poll_prod(brain, aid, a.max_wait, a.interval)
        if data is None:
            print(f"{aid:12s} {'-':>9s} {'-':>9s}  {'PENDING':<14s} {note}")
            continue
        mx = data.get("max")
        recs = data.get("records") or []
        n = bucket_n(recs)
        verdict = "SCAN(过线可期)" if (n is not None and n == 0) else (
            "DEAD(单钉子)" if n is not None else "n=?")
        if mx is not None and mx < a.threshold:
            verdict = "PASS(<%.2f)" % a.threshold
        print(f"{aid:12s} {mx:>9.4f} {str(n):>9s}  {verdict:<14s} "
              f"min={data.get('min')} buckets={len(recs)}")
        if store and a.persist:
            store.set_corr_cache(aid, prod=mx, records=recs, source="platform")
    if store:
        store.close()
    return 0


def main():
    ap = argparse.ArgumentParser(description="耐心轮询 prod 相关性并落 wqb 库")
    ap.add_argument("alpha_ids", nargs="*", help="alpha id（可多个）")
    ap.add_argument("--file", help="从文件读 id（每行一个）")
    ap.add_argument("--max-wait", type=int, default=480, help="每颗最多等多少秒")
    ap.add_argument("--interval", type=int, default=20, help="轮询间隔秒")
    ap.add_argument("--threshold", type=float, default=0.7)
    ap.add_argument("--refresh", action="store_true", help="忽略本地缓存强刷")
    ap.add_argument("--no-persist", dest="persist", action="store_false", help="不落库")
    args = ap.parse_args()
    ids = list(args.alpha_ids)
    if args.file:
        ids += [ln.strip() for ln in Path(args.file).read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not ids:
        ap.error("需要 alpha id 或 --file")
    args.alpha_ids = ids
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
