# -*- coding: utf-8 -*-
"""KOR 十年覆盖批量探针（带断点续跑）。

按用户 2026-10-25 指令：「先跑探针拿到候选池后再跑战役流水线」。
复用 `tools/kor_year_probe.py` 的 probe()/pick_field()/build_expr()，
但改为：单客户端 + 信号量并发 + 逐条落盘 + 重启跳过已完成。

为什么要有这个驱动：`kor_year_probe.py` 一次只跑一个集、每次调用重新认证
（164 个集 × ~5s 认证 ≈ 14 分钟纯握手），且无续跑。

用法：
  python tools/kor_year_sweep.py --from-db --conc 2          # 从 dataset_profile 取池子
  python tools/kor_year_sweep.py --datasets a,b,c            # 指定集
  python tools/kor_year_sweep.py --from-db --conc 3 --fresh  # 忽略续跑强制重跑

输出：`results/kor_year_probe.jsonl`（每行一条 JSON），最后打印分层统计。
"""
import argparse
import asyncio
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import kor_year_probe as kp  # noqa: E402
from brain_api import BrainApiClient  # noqa: E402
from wqb.db_conn import connect as db_connect  # noqa: E402

DB = os.path.join(ROOT, "data", "wqb.db")
AUDIT = os.path.join(ROOT, "results", "campaign_year_audit.json")


def _audited():
    """已有完整逐年画像的集（campaign_year_audit 覆盖），不必再探。"""
    try:
        a = json.load(open(AUDIT, encoding="utf-8"))
        rows = a.get("rows") or a.get("datasets") or []
        return {r["dataset"] for r in rows if r.get("dataset")}
    except Exception:
        return set()


def _pool_from_db():
    con = db_connect(DB, readonly=True)
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT DISTINCT dataset FROM dataset_profile WHERE region='KOR' AND n_fields>=3")
        return [r[0] for r in cur.fetchall()]
    finally:
        con.close()


#: 只有这些判定算「已完成」，ERROR / SIM_FAILED（429 等）一律重试。
DONE_VERDICTS = {"PASS_10Y", "REJECT_MISSING_YEAR", "REJECT_NO_FIELDS"}


def load_done(path):
    """已探过的集（只认确凿判定；ERROR/SIM_FAILED 留待重试）。"""
    done = set()
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            v = r.get("verdict") or r.get("status")
            if r.get("dataset") and v in DONE_VERDICTS:
                done.add(r["dataset"])
    return done


def append(path, rec):
    line = json.dumps(rec, ensure_ascii=False)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", default=None, help="逗号分隔；与 --from-db 二选一")
    ap.add_argument("--from-db", action="store_true", help="从 dataset_profile 取 KOR 池子")
    ap.add_argument("--conc", type=int, default=2, help="并发探针数（默认 2）")
    ap.add_argument("--out", default=os.path.join(ROOT, "results", "kor_year_probe.jsonl"))
    ap.add_argument("--decay", type=float, default=4)
    ap.add_argument("--neutralization", default="STATISTICAL")
    ap.add_argument("--truncation", type=float, default=0.08)
    ap.add_argument("--fresh", action="store_true", help="忽略续跑，强制重跑")
    ap.add_argument("--keep-audited", action="store_true",
                    help="连 campaign_year_audit 已画像的集也重探（默认跳过）")
    args = ap.parse_args()

    if args.datasets:
        pool = [d.strip() for d in args.datasets.split(",") if d.strip()]
    elif args.from_db:
        pool = _pool_from_db()
        if not args.keep_audited:
            pool = [d for d in pool if d not in _audited()]
    else:
        ap.error("需要 --datasets 或 --from-db")

    done = set() if args.fresh else load_done(args.out)
    todo = [d for d in pool if d not in done]
    print(f"[sweep] 池子 {len(pool)}｜已完成 {len(done)}｜待跑 {len(todo)}｜并发 {args.conc}",
          flush=True)
    if not todo:
        print("[sweep] 无事可做")
        return

    kw = {"decay": args.decay, "neutralization": args.neutralization,
          "truncation": args.truncation}
    client = BrainApiClient()
    await client.ensure_authenticated()

    sem = asyncio.Semaphore(args.conc)
    lock = asyncio.Lock()
    counter = {"n": 0, "pass": 0}

    async def one(ds):
        async with sem:
            rec = None
            # 429 退避重试：平台在飞上限是共享的（IND 线同跑时会撞），
            # 旧版一遇 429 就把整集记 SIM_FAILED ⇒ 假阴性，白白丢掉候选集。
            for attempt in range(4):
                try:
                    field, _raw = await kp.pick_field(client, ds, None)
                    if not field:
                        rec = {"tag": "sweep", "dataset": ds,
                               "verdict": "REJECT_NO_FIELDS"}
                    else:
                        expr = kp.build_expr(field["id"], field.get("type"))
                        rec = await kp.probe(client, ds, field, expr, "sweep", kw)
                except Exception as e:
                    rec = {"tag": "sweep", "dataset": ds, "verdict": "ERROR",
                           "error": f"{type(e).__name__}: {e}"}
                blob = json.dumps(rec, ensure_ascii=False)
                if "429" in blob and "CONCURRENT" in blob.upper() and attempt < 3:
                    wait = 30 * (2 ** attempt)
                    print(f"  [retry] {ds} 撞 429，{wait}s 后第 {attempt + 2} 次重试",
                          flush=True)
                    await asyncio.sleep(wait)
                    continue
                break

            async with lock:
                append(args.out, rec)
                counter["n"] += 1
                if rec.get("verdict") == "PASS_10Y":
                    counter["pass"] += 1
                v = rec.get("verdict") or rec.get("status") or "?"
                mark = "★" if v == "PASS_10Y" else " "
                print(f"{mark}[{counter['n']}/{len(todo)}] {ds:26s} {v:22s} "
                      f"n_years={rec.get('n_years')} S={rec.get('sharpe')}",
                      flush=True)

    await asyncio.gather(*(one(d) for d in todo))

    # 分层统计（全量；同一集多次探时只认最后一条）
    latest = {}
    if os.path.exists(args.out):
        for line in open(args.out, encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("dataset"):
                latest[r["dataset"]] = r
    allrecs = list(latest.values())
    from collections import Counter
    print("\n=== verdict 分布（按集去重）===")
    for k, n in Counter(r.get("verdict") or r.get("status") or "?"
                        for r in allrecs).most_common():
        print(f"  {k:26s} {n}")
    passes = [r["dataset"] for r in allrecs
              if (r.get("verdict") or r.get("status")) == "PASS_10Y"]
    print(f"\n=== 十年齐备（PASS_10Y）共 {len(passes)} 个 ===")
    print("  " + ", ".join(sorted(passes)))
    print(f"\n候选池已写入 {args.out}")


if __name__ == "__main__":
    asyncio.run(main())
