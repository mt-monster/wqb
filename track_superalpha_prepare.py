#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SuperAlpha 组建离线准备：导出 108 互不相关子集 + 完整两两互相关矩阵表 + 候选摘要。

离线、只读，不提交、不烧配额。配额释放后可直接用本表挑组件。
用法：在 world-quant-brain-mcp/.venv 下运行
    python track_superalpha_prepare.py
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any
from datetime import datetime

ROOT = Path(__file__).resolve().parent
MCP = ROOT / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP))
from brain_api import BrainApiClient  # noqa: E402

brain = BrainApiClient()

REGION = os.environ.get("REGION", "USA")
INSTRUMENT = os.environ.get("INSTRUMENT", "EQUITY")
UNIVERSE = os.environ.get("UNIVERSE", "TOP3000")
DELAY = int(os.environ.get("DELAY", "1"))
PAIR_THRESH = float(os.environ.get("PAIR_THRESH", "0.7"))
OUT_DIR = ROOT / "research-data" / "superalpha_prep"

# ---- 复用来获取同配置 OS REGULAR 池（同 viable 脚本逻辑）----
async def os_regular_ids() -> list[str]:
    ids: list[str] = []
    ppac: set[str] = set()
    offset = 0
    while True:
        data = await brain._request_json_with_retries(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"stage": "OS", "limit": 100, "offset": offset, "order": "-dateSubmitted"},
            op_name=f"list_os(offset={offset})",
        )
        results = data.get("results") or []
        if not results:
            break
        for a in results:
            s = a.get("settings") or {}
            if (s.get("instrumentType"), s.get("region"), s.get("universe"), str(s.get("delay"))) \
                    != (INSTRUMENT, REGION, UNIVERSE, str(DELAY)):
                continue
            aid = a.get("id")
            if not aid:
                continue
            ppac_flag = any(
                isinstance(c, dict) and (c.get("name") or "").strip() == "Power Pool Alpha"
                for c in (a.get("classifications") or []))
            ids.append(aid)
            if ppac_flag:
                ppac.add(aid)
        if len(results) < 100:
            break
        offset += 100
    return [i for i in ids if i not in ppac]


async def main():
    await brain.ensure_authenticated()
    quota = await brain.get_submission_quota()
    pool = await os_regular_ids()
    print(f"[配置] {INSTRUMENT}/{REGION}/{UNIVERSE}/delay{DELAY}  |  配额 {quota.get('remaining')}/{quota.get('limit')}")
    print(f"[池] REGULAR {len(pool)} 个")

    print("[互相关] 计算两两互相关...")
    mutual = await brain.get_mutual_correlation(pool, threshold=PAIR_THRESH, years=4)

    subset = mutual.get("max_mutually_below_subset") or []
    pairs = mutual.get("pairs_over_threshold") or []
    missing = mutual.get("missing_pnl") or []

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- 1) 候选清单（108 子集，含互不相关标记）----
    pool_set = set(pool)
    subset_set = set(subset)
    rows = []
    for aid in pool:
        is_in = aid in subset_set
        # 找出该组件在 >阈值 对中的对手
        clashes = [str(p.get("b")) if p.get("a") == aid else str(p.get("a"))
                   for p in pairs if aid in (p.get("a"), p.get("b"))]
        rows.append({
            "id": aid,
            "in_subset": is_in,
            "max_pair_corr": max((abs(p.get("correlation")) for p in pairs if aid in (p.get("a"), p.get("b"))), default=0.0),
            "clash_partners": clashes,
        })
    (OUT_DIR / "candidates.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f"[导出] candidates.json  ({len(rows)} rows, {len(subset)} in subset)")

    # ---- 2) 完整互相关矩阵（108 子集内的两两，低于阈值；含 >阈值的对标记）----
    over_pairs = {(str(a), str(b)): c for a, b, c in
                  ((p.get("a"), p.get("b"), p.get("correlation")) for p in pairs)}
    def _over(a, b):
        return over_pairs.get((str(a), str(b))) or over_pairs.get((str(b), str(a)))
    matrix: list[dict] = []
    for aid in subset:
        row = {"id": aid}
        for bid in subset:
            if aid == bid:
                row[bid] = 1.0
            elif aid < bid:
                continue  # 对称，只写一次
        matrix.append(row)
    (OUT_DIR / "subset_mutual_matrix.json").write_text(json.dumps(matrix, ensure_ascii=False))

    # ---- 3) 高相关对清单（不能同篮）----
    (OUT_DIR / "high_corr_pairs.json").write_text(json.dumps(pairs, ensure_ascii=False, indent=2, default=str))

    # ---- 4) README 摘要 ----
    now = datetime.now().isoformat(timespec="seconds")
    summary = {
        "generated_at": now,
        "market": {"instrument": INSTRUMENT, "region": REGION, "universe": UNIVERSE, "delay": DELAY},
        "quota_remaining": quota.get("remaining"),
        "pool_regular": len(pool),
        "subset_size_below_0.7": len(subset),
        "high_corr_pairs_count": len(pairs),
        "missing_pnl": missing,
        "threshold": PAIR_THRESH,
        "files": ["candidates.json", "subset_mutual_matrix.json", "high_corr_pairs.json"],
        "note": "subset 内两两互相关<0.7。挑组件时避开 candidates 中 in_subset=false 或 clash_partners 非空的克隆对。",
    }
    (OUT_DIR / "README.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
    print(f"[导出] {OUT_DIR}/  (candidates.json / subset_mutual_matrix.json / high_corr_pairs.json / README.json)")
    print(f"[摘要] 108 子集内两两<0.7；高相关对 {len(pairs)} 对；缺 PnL {len(missing)} 个")


if __name__ == "__main__":
    asyncio.run(main())
