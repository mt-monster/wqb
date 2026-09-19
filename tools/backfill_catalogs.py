# -*- coding: utf-8 -*-
"""backfill_catalogs.py — 为白名单里缺 typed catalog 的数据集补 catalog（幂等）。

背景（2026-09-17 实测）：全库 70/93 白名单数据集有 catalog，缺 23 个——
集中 JPN 10/12、GBR 6/11、CHN 1/3。缺集无法过门禁（gate.load_whitelist 抛
FileNotFoundError），其波要么崩、要么积压成死库存；region_gates 的 catalog 前置闸
现在会把它们拦在开波前，但**根治是把 catalog 补上**。
本地 WebData ZIP 不含 JPN/DEU 条目（体检包无法离线生成），但 `scan_fields.py`
走**平台 API** 取字段元数据 —— 实测 JPN 可取，且零配额成本。

用法：
  python tools/backfill_catalogs.py                  # 只列出缺集（dry-run）
  python tools/backfill_catalogs.py --region JPN     # 只看/只补某区
  python tools/backfill_catalogs.py --apply          # 逐个跑 scan_fields
  python tools/backfill_catalogs.py --apply --limit 3
"""
import argparse
import contextlib
import io
import json
import os
import sqlite3
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TK = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")


def missing_pairs(region_filter=None):
    sys.path.insert(0, TK)
    from _lib.common import CampaignContext
    import gate

    conn = sqlite3.connect(os.path.join(REPO, "data", "wqb.db"))
    out = []
    ctxs = {}
    for reg, val in conn.execute(
            "SELECT region, value FROM ledger_kv WHERE key='s0_whitelist' ORDER BY region"):
        if region_filter and reg != region_filter:
            continue
        cdir = os.path.join(REPO, "tracking", reg)
        if not os.path.isdir(cdir):
            continue
        try:
            d = json.loads(val)
        except Exception:
            continue
        ds = d.get("datasets") or d.get("whitelist") or d.get("candidates") or []
        ds = [x if isinstance(x, str) else (x.get("id") or x.get("dataset") or "") for x in ds]
        ds = [x for x in ds if x]
        if not ds:
            continue
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                ctx = ctxs[reg] = CampaignContext(cdir)
        except Exception:
            continue
        for x in ds:
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    gate.load_whitelist(ctx, x)
            except Exception:
                out.append((reg, x))
    conn.close()
    return out


def main():
    ap = argparse.ArgumentParser(description="补缺失 catalog（scan_fields 批量；dry-run 默认）")
    ap.add_argument("--region", default=None)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--apply", action="store_true", help="实际执行 scan_fields（缺省只列）")
    a = ap.parse_args()

    pairs = missing_pairs(a.region)
    if a.limit:
        pairs = pairs[:a.limit]
    print(f"缺 catalog 的数据集 = {len(pairs)}")
    for reg, ds in pairs:
        print(f"  {reg:<5} {ds}")

    if not a.apply:
        print("\n[dry-run] 未执行。确认后加 --apply（逐个跑 scan_fields，零配额）。")
        return

    ok, fail = [], []
    for i, (reg, ds) in enumerate(pairs, 1):
        cmd = [sys.executable, os.path.join(TK, "scan_fields.py"),
               "--campaign-dir", os.path.join(REPO, "tracking", reg),
               "--dataset", ds]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if p.returncode == 0:
                ok.append((reg, ds))
                print(f"[{i}/{len(pairs)}] ✅ {reg}/{ds}")
            else:
                fail.append((reg, ds, (p.stderr or p.stdout or "").strip().splitlines()[-1:]))
                print(f"[{i}/{len(pairs)}] ❌ {reg}/{ds} rc={p.returncode}")
        except Exception as e:
            fail.append((reg, ds, str(e)[:120]))
            print(f"[{i}/{len(pairs)}] ❌ {reg}/{ds} {type(e).__name__}")
    print(f"\n完成：成功 {len(ok)} / 失败 {len(fail)}")
    for f in fail[:8]:
        print("  失败:", f)


if __name__ == "__main__":
    main()
