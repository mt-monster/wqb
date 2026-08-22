#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SuperAlpha 组建可行性诊断（只读，不提交、不烧配额）。

对给定市场配置，诊断能否组出一个可提交的 SuperAlpha：
1. 认证 + 配额闸（48h 窗口剩余数）。
2. 拉取同配置 OS alpha 池（REGULAR，排除 POWER_POOL_ALPHA 分类），取 PnL。
3. 在候选池内算 4 年日收益互相关，报告：
   - 池规模、max_pair 互相关、超过阈值的对数
   - 贪婪"两两低于阈值的最大子集"大小（即理论上最多能取几个互不相关组件）
4. 给出结论：当前池是否具备"≥N 个互不相关组件"的基本条件。

用法（在 wqb/world-quant-brain-mcp/.venv 下）：
    python track_superalpha_viable.py
可选：设置环境变量覆盖市场配置，如
    REGION=USA UNIVERSE=TOP3000 DELAY=1 python track_superalpha_viable.py
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
MCP = ROOT / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP))

from brain_api import BrainApiClient  # noqa: E402

brain = BrainApiClient()

# ---------- 市场配置（与已有 SUPER KPGvRMg1/gJ8eVmNM 对齐：USA/EQUITY/TOP3000/delay1）----------
REGION = os.environ.get("REGION", "USA")
INSTRUMENT = os.environ.get("INSTRUMENT", "EQUITY")
UNIVERSE = os.environ.get("UNIVERSE", "TOP3000")
DELAY = int(os.environ.get("DELAY", "1"))
SELF_THRESH = float(os.environ.get("SELF_THRESH", "0.7"))  # 组件自身 self-correlation 上限（经验）
PAIR_THRESH = float(os.environ.get("PAIR_THRESH", "0.7"))  # 组件两两互相关上限（SUPER 硬闸近似）
MIN_COMPONENTS = int(os.environ.get("MIN_COMPONENTS", "4"))  # 最少组件数才认为"可组"
OUT_JSON = ROOT / "research-data" / "superalpha_viability.json"


async def list_os_regularity_pool() -> list[dict[str, Any]]:
    """拉取同配置 OS alpha 池，排除 Power Pool Alpha（分类名匹配），返回详情列表。"""
    all_ids: list[str] = []
    detail_map: dict[str, dict] = {}
    ppac_ids: set[str] = set()
    offset = 0
    PAGE = 100
    while True:
        params = {
            "stage": "OS",
            "limit": PAGE,
            "offset": offset,
            "order": "-dateSubmitted",
        }
        data = await brain._request_json_with_retries(
            "GET", f"{brain.base_url}/users/self/alphas",
            params=params, op_name=f"list_os(offset={offset})",
        )
        results = data.get("results") or []
        if not results:
            break
        for a in results:
            aid = a.get("id")
            if not aid:
                continue
            s = a.get("settings") or {}
            if s.get("instrumentType") != INSTRUMENT:
                continue
            if s.get("region") != REGION:
                continue
            if s.get("universe") != UNIVERSE:
                continue
            if str(s.get("delay")) != str(DELAY):
                continue
            is_ppac = any(
                (c.get("name") or "").strip() == "Power Pool Alpha"
                for c in (a.get("classifications") or [])
                if isinstance(c, dict)
            )
            all_ids.append(aid)
            if is_ppac:
                ppac_ids.add(aid)
            detail_map[aid] = a
        if len(results) < PAGE:
            break
        offset += PAGE
    return all_ids, detail_map, ppac_ids


async def main():
    await brain.ensure_authenticated()

    # 1) 配额
    quota = await brain.get_submission_quota()

    # 2) OS 池
    all_ids, detail_map, ppac_ids = await list_os_regularity_pool()
    reg_ids = [i for i in all_ids if i not in ppac_ids]

    report = {
        "market": {"instrument": INSTRUMENT, "region": REGION,
                   "universe": UNIVERSE, "delay": DELAY},
        "quota": quota,
        "os_pool_total": len(all_ids),
        "os_ppac_count": len(ppac_ids),
        "os_regular_count": len(reg_ids),
        "pair_threshold": PAIR_THRESH,
        "self_threshold": SELF_THRESH,
        "min_components": MIN_COMPONENTS,
        "verdict": "pending",
    }

    print(f"[配置] {INSTRUMENT}/{REGION}/{UNIVERSE}/delay{DELAY}")
    print(f"[配额] {quota.get('remaining')} / {quota.get('limit')} "
          f"(窗口内已用 {quota.get('used')}, 剩余 {quota.get('remaining')})")
    print(f"[OS池] 总 {len(all_ids)} = REGULAR {len(reg_ids)} + PPA {len(ppac_ids)}")

    if len(reg_ids) < MIN_COMPONENTS:
        report["verdict"] = ("NO_GO",
                             f"同配置 REGULAR 组件仅 {len(reg_ids)} 个 < {MIN_COMPONENTS}，"
                             "无法凑够 SuperAlpha 最小组件数")
        print(f"[结论] {report['verdict'][1]}")
        _save(report)
        return

    # 3) 互相关（4 年）
    print(f"[计算] 对 {len(reg_ids)} 个 REGULAR 组件做两两互相关 (threshold={PAIR_THRESH}, 4y)...")
    mutual = await brain.get_mutual_correlation(reg_ids, threshold=PAIR_THRESH, years=4)

    report["mutual"] = {
        "n": len(mutual.get("alpha_ids", [])),
        "max_pair": mutual.get("max_pair"),
        "pairs_over": len(mutual.get("pairs_over_threshold", [])),
        "all_below": mutual.get("all_below_threshold"),
        "max_mutually_below_size": mutual.get("max_mutually_below_subset_size"),
        "max_mutually_below_subset": mutual.get("max_mutually_below_subset"),
        "missing_pnl": mutual.get("missing_pnl"),
    }
    mp = mutual.get("max_pair") or {}
    print(f"[互相关] 池内最大互相关对 = {mp.get('correlation')} "
          f"({mp.get('a')} ~ {mp.get('b')})")
    print(f"[互相关] 两两低于 {PAIR_THRESH} 的最大子集大小 = "
          f"{mutual.get('max_mutually_below_subset_size')} / {len(reg_ids)}")

    max_sub = int(mutual.get("max_mutually_below_subset_size") or 0)
    if max_sub >= MIN_COMPONENTS:
        report["verdict"] = ("GO",
                             f"存在 {max_sub} 个两两互相关<{PAIR_THRESH} 的组件，"
                             f"达到 ≥{MIN_COMPONENTS} 的基本条件；可进入下一步（组件自检 self<0.7 + 组合回测 SHARPE）")
        print(f"[结论] {report['verdict'][1]}")
    else:
        report["verdict"] = ("NO_GO",
                             f"即使选最优子集，最多也只有 {max_sub} 个组件两两互相关<{PAIR_THRESH}，"
                             f"< {MIN_COMPONENTS}；当前同配置池同质化过高，难以组建 SUPER")
        print(f"[结论] {report['verdict'][1]}")

    _save(report)


def _save(report: dict):
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    print(f"[落盘] {OUT_JSON}")


if __name__ == "__main__":
    asyncio.run(main())
