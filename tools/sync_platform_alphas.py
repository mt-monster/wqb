# -*- coding: utf-8 -*-
"""sync_platform_alphas.py — 把平台已提交（OS 池）alpha 同步进本地 alphas 表。

背景（2026-09-20 实测）：
  平台 OS 池 228 个已提交 alpha，本地 alphas 台账仅 94 —— 漏记 134 个
  （USA 124 + DEU 5 + IND 2 + EUR/KOR/GLB 各 1，提交时间 2025-03 ~ 2026-09）。
  漏记导致 S6 复盘、win recipe 沉淀、prod_corr 饱和反馈全部建立在不完整清单上。

同时补齐 OS（样本外）指标：平台 `os` 段此前从未落库，
  MCP `get_alpha_details` 的 `_slim_alpha()` 也只取 `is` 段。
  实测 124 个 alpha 有 OS 指标：IS sharpe 均值 1.53 → OS 0.55（衰减比 0.358）、22% OS<=0。

用法：
  python tools/sync_platform_alphas.py                      # 全量同步（分页拉取）
  python tools/sync_platform_alphas.py --region USA         # 只看某区（仍会拉全量，仅过滤统计）
  python tools/sync_platform_alphas.py --dry-run            # 只报告差异，不写库
  python tools/sync_platform_alphas.py --baseline           # 只打印 OS 衰减基线

设计：走 MCP venv（brain_api 客户端），禁止手写 requests。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from collections import Counter
from typing import Any, Dict, List

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MCP_DIR = os.path.join(REPO_ROOT, "world-quant-brain-mcp")
for p in (MCP_DIR, os.path.join(REPO_ROOT, "src")):
    if p not in sys.path:
        sys.path.insert(0, p)


def _pyra(py: Any) -> str:
    if not py:
        return ""
    items = py.get("list") if isinstance(py, dict) else py
    if not isinstance(items, list):
        return ""
    names = []
    for x in items:
        n = x.get("name") if isinstance(x, dict) else (x if isinstance(x, str) else None)
        if n:
            names.append(str(n).split("/")[-1].lower())
    return "/".join(names)


async def fetch_os_pool(limit: int = 100, max_pages: int = 10) -> List[Dict[str, Any]]:
    """分页拉取平台 OS 池全部 alpha（原始对象）。"""
    from brain_api import brain_client

    all_rows: List[Dict[str, Any]] = []
    offset = 0
    for _ in range(max_pages):
        r = await brain_client.get_user_alphas(stage="OS", limit=limit, offset=offset)
        payload = r["result"] if isinstance(r, dict) and isinstance(r.get("result"), dict) else r
        res = payload.get("results", []) or []
        if not res:
            break
        all_rows.extend(res)
        total = payload.get("count")
        print(f"  [fetch] offset={offset} got={len(res)} total={len(all_rows)}/{total}", file=sys.stderr)
        if not payload.get("next"):
            break
        offset += limit
    return all_rows


def to_store_payload(a: Dict[str, Any]) -> Dict[str, Any]:
    """平台 alpha 对象 → upsert_alpha_from_platform 期望的扁平字典。"""
    st = a.get("settings") or {}
    isd = a.get("is") or {}
    osd = a.get("os") or {}
    reg = a.get("regular")
    return {
        "alpha_id": a.get("id"),
        "region": st.get("region"),
        "expression": reg.get("code") if isinstance(reg, dict) else None,
        "universe": st.get("universe"),
        "delay": st.get("delay"),
        "neutralization": st.get("neutralization"),
        "sharpe": isd.get("sharpe"),
        "fitness": isd.get("fitness"),
        "turnover": isd.get("turnover"),
        "two_year_sharpe": None,  # 平台 is 段无此字段（本地从回测落）
        "prod_correlation": isd.get("prodCorrelation"),
        "self_correlation": isd.get("selfCorrelation"),
        "platform_status": a.get("status"),
        "stage": a.get("stage"),
        "alpha_type": a.get("type"),
        "date_submitted": a.get("dateSubmitted"),
        "status": "COMPLETE",
        "os_data": osd,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="同步平台 OS 池 alpha 到本地台账（含 OS 指标）")
    ap.add_argument("--dry-run", action="store_true", help="只报告差异，不写库")
    ap.add_argument("--baseline", action="store_true", help="只打印 OS 衰减基线")
    ap.add_argument("--region", default=None, help="统计视角限定区域（写库仍为全量）")
    ap.add_argument("--limit", type=int, default=100, help="分页大小")
    args = ap.parse_args()

    from wqb.store import CampaignStore

    db_path = os.path.join(REPO_ROOT, "data", "wqb.db")
    store = CampaignStore(path=db_path)

    if args.baseline:
        print(json.dumps(store.os_decay_baseline(args.region), ensure_ascii=False, indent=1))
        return 0

    print("[1/3] 拉取平台 OS 池 ...", file=sys.stderr)
    pool = asyncio.run(fetch_os_pool(limit=args.limit))
    print(f"      平台 OS 池: {len(pool)} 个", file=sys.stderr)

    cur = store.connection.cursor()
    cur.execute("SELECT alpha_id FROM alphas WHERE date_submitted IS NOT NULL")
    local_ids = {r[0] for r in cur.fetchall()}
    plat_ids = {a.get("id") for a in pool}
    missing = plat_ids - local_ids
    print(f"[2/3] 本地已提交台账: {len(local_ids)}；漏记: {len(missing)}", file=sys.stderr)
    if missing:
        reg_of = {a.get("id"): (a.get("settings") or {}).get("region") for a in pool}
        print(f"      漏记按区: {Counter(reg_of.get(i) for i in missing).most_common()}", file=sys.stderr)

    if args.dry_run:
        print("[dry-run] 未写库。", file=sys.stderr)
        return 0

    print("[3/3] 回填 ...", file=sys.stderr)
    stats = Counter()
    for a in pool:
        payload = to_store_payload(a)
        os_data = payload.pop("os_data")
        aid = payload.get("alpha_id")
        if not aid:
            stats["skip_no_id"] += 1
            continue
        try:
            if aid in missing:
                store.upsert_alpha_from_platform(payload)
                stats["backfilled_alpha"] += 1
            r = store.upsert_alpha_os_metrics(
                aid, os_data,
                region=payload.get("region"),
                submitted_info={
                    "platform_status": payload.get("platform_status"),
                    "stage": payload.get("stage"),
                    "alpha_type": payload.get("alpha_type"),
                    "date_submitted": payload.get("date_submitted"),
                    "expression": payload.get("expression"),
                },
            )
            stats[f"os_{r.get('action')}"] += 1
            if r.get("skipped") == "no_metrics":
                stats["os_no_metrics"] += 1
        except Exception as e:  # noqa: BLE001 — 单条失败不阻断全量
            stats["error"] += 1
            print(f"  [error] {aid}: {e}", file=sys.stderr)

    print("\n=== 同步结果 ===")
    for k, v in sorted(stats.items()):
        print(f"  {k}: {v}")
    print("\n=== OS 衰减基线（全量）===")
    print(json.dumps(store.os_decay_baseline(None), ensure_ascii=False, indent=1))
    if args.region:
        print(f"\n=== OS 衰减基线（{args.region}）===")
        print(json.dumps(store.os_decay_baseline(args.region), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
