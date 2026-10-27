#!/usr/bin/env python
"""各区「IS → OS 实盘衰减」复盘，用于判断某个 scope 的纸面质量是否可信。

## 为什么需要这个脚本

Daily Osmosis Rank = 各已分配 scope 的 rank **算术平均**，所以「该不该把某个 scope
加进来」取决于它的预期 rank。我们一直用 `wavg_inv`（investability Sharpe 加权）
作为代理 —— 但那是**纸面值**。

2026-10-21 实证：USA 是**唯一**有 OS（out-of-sample 实盘）数据的区，
41 颗 ACTIVE REGULAR 里 23 颗有 OS 值，IS 均值 2.043 → OS 均值 0.530，**衰减 74%**。
而其余 9 个区（含正在用的 5 个）OS 数据全为 0 颗 ⇒ 它们的 `wavg_inv` 全部是纸面分，
真实衰减未知。

## 本脚本做什么

1. 拉平台 OS 池（status/type/inv 以平台为准）
2. 从 DB `alphas.os_sharpe` 补 OS 值（平台 `os.osISSharpeRatio` 现已恒为 null）
3. 按区算：颗数 / 有OS颗数 / avg_IS / avg_OS / 衰减 / 最后同步时间
4. 给出 **OS 折算系数** `os_factor = avg_os / avg_is`，以及折算后的实盘质量
   `inv_live = wavg_inv × os_factor` —— 这是唯一能跨区比较「实盘质量」的口径
5. 判定：某区若新出现 OS 数据，直接告出它比 USA（os_factor≈0.26）更好还是更差

## 用法

  python tools/data-repair/review_os_decay.py            # 全量
  python tools/data-repair/review_os_decay.py --json     # 机器可读（供定时任务消费）
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sqlite3          # 仅用于 sqlite3.Row（连接本身一律走 db_connect）
import sys
from collections import defaultdict

_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, os.path.join(_ROOT, "world-quant-brain-mcp"))

from wqb.db_conn import connect as db_connect  # noqa: E402

_DB = os.path.join(_ROOT, "data", "wqb.db")

# 2026-10-21 基线：USA 是第一个（也是当时唯一）跑出 OS 的区，作为衰减参照点
BASELINE_REGION = "USA"


async def fetch_platform() -> list:
    from brain_api import brain_client
    rows: list = []
    off = 0
    for _ in range(200):
        r = await brain_client.get_user_alphas(stage="OS", limit=100, offset=off)
        pl = r["result"] if isinstance(r, dict) and isinstance(r.get("result"), dict) else r
        res = pl.get("results", []) or []
        if not res:
            break
        rows.extend(res)
        if not pl.get("next"):
            break
        off += 100
    return rows


def load_db_os() -> tuple[dict, dict, dict]:
    """返回 (os_sharpe 映射, os_synced_at 映射, sync 时间戳集合)。"""
    con = db_connect(_DB, readonly=True)
    con.row_factory = sqlite3.Row
    cur = con.execute(
        "SELECT alpha_id, os_sharpe, os_synced_at FROM alphas WHERE os_sharpe IS NOT NULL"
    )
    os_map, sync_map, stamps = {}, {}, defaultdict(int)
    for r in cur.fetchall():
        os_map[r["alpha_id"]] = r["os_sharpe"]
        s = r["os_synced_at"]
        sync_map[r["alpha_id"]] = s
        if s:
            stamps[str(s)[:10]] += 1
    con.close()
    return os_map, sync_map, dict(stamps)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="输出 JSON（供定时任务消费）")
    args = ap.parse_args()

    pool = asyncio.run(fetch_platform())
    db_os, db_sync, stamps = load_db_os()

    by: dict = defaultdict(lambda: {"n": 0, "n_os": 0, "is": [], "os": [], "inv": []})
    for x in pool:
        if x.get("status") != "ACTIVE" or x.get("type") != "REGULAR":
            continue
        st = x.get("settings") or {}
        isd = x.get("is") or {}
        prod = isd.get("prodCorrelation")
        if prod is None:
            prod = x.get("prod")
        # 与分配器一致：prod>=0.70 不参与（合规红线）
        if prod is not None and prod >= 0.70:
            continue
        reg = st.get("region")
        b = by[reg]
        b["n"] += 1
        isv = isd.get("sharpe")
        if isv is not None:
            b["is"].append(isv)
        inv = (isd.get("investabilityConstrained") or {}).get("sharpe")
        if inv is not None:
            b["inv"].append(inv)
        # OS：平台 os 段已恒 null，优先取 DB
        osv = (x.get("os") or {}).get("sharpe")
        if osv is None:
            osv = db_os.get(x.get("id"))
        if osv is not None:
            b["n_os"] += 1
            b["os"].append(osv)

    rows = []
    for reg, b in by.items():
        if not b["n"]:
            continue
        avg_is = sum(b["is"]) / len(b["is"]) if b["is"] else None
        avg_os = sum(b["os"]) / len(b["os"]) if b["os"] else None
        avg_inv = sum(b["inv"]) / len(b["inv"]) if b["inv"] else None
        factor = (avg_os / avg_is) if (avg_os is not None and avg_is) else None
        inv_live = (avg_inv * factor) if (avg_inv is not None and factor is not None) else None
        neg = sum(1 for v in b["os"] if v < 0)
        rows.append({
            "region": reg,
            "n": b["n"],
            "n_os": b["n_os"],
            "avg_is": round(avg_is, 3) if avg_is is not None else None,
            "avg_os": round(avg_os, 3) if avg_os is not None else None,
            "avg_inv": round(avg_inv, 3) if avg_inv is not None else None,
            "decay": round((1 - factor) * 100, 1) if factor is not None else None,
            "os_factor": round(factor, 3) if factor is not None else None,
            "inv_live": round(inv_live, 3) if inv_live is not None else None,
            "os_neg": neg,
        })
    rows.sort(key=lambda r: (-r["n_os"], -r["n"]))

    if args.json:
        out = {
            "generated_at": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
            "db_sync_dates": stamps,
            "baseline_region": BASELINE_REGION,
            "scopes": rows,
            "regions_with_os": [r["region"] for r in rows if r["n_os"] > 0],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    print("\n=== 各区 IS → OS 实盘衰减 ===")
    print(f"{'区':<7}{'n':>5}{'有OS':>6}{'avg_IS':>9}{'avg_OS':>9}{'衰减':>8}"
          f"{'os_factor':>11}{'avg_inv':>9}{'inv_live':>10}{'OS<0':>6}")
    print("=" * 82)

    def cell(v, width: int, pct: bool = False) -> str:
        if v is None:
            return "-".rjust(width)
        return (f"{v}%" if pct else f"{v:.3f}").rjust(width)

    for r in rows:
        print(f"{r['region']:<7}{r['n']:>5}{r['n_os']:>6}"
              f"{cell(r['avg_is'], 9)}{cell(r['avg_os'], 9)}"
              f"{cell(r['decay'], 8, pct=True)}"
              f"{cell(r['os_factor'], 11)}{cell(r['avg_inv'], 9)}"
              f"{cell(r['inv_live'], 10)}{r['os_neg']:>6}")

    with_os = [r for r in rows if r["n_os"] > 0]
    print()
    if with_os:
        base = next((r for r in with_os if r["region"] == BASELINE_REGION), with_os[0])
        print(f"有 OS 数据的区: {len(with_os)} 个 —— {', '.join(r['region'] for r in with_os)}")
        print(f"参照 {base['region']}: os_factor={base['os_factor']} "
              f"（IS {base['avg_is']} → OS {base['avg_os']}，衰减 {base['decay']}%）")
        for r in with_os:
            if r["region"] == base["region"]:
                continue
            d = (r["os_factor"] or 0) - (base["os_factor"] or 0)
            verdict = "实盘更可信 ✔" if d > 0.05 else ("与参照相当" if d > -0.05 else "实盘更差 ✘")
            print(f"  {r['region']}: os_factor={r['os_factor']} vs {base['region']} {base['os_factor']} "
                  f"→ 差 {d:+.3f}（{verdict}）")
    else:
        print("⚠ 当前无任何区有 OS 数据 —— 所有 wavg_inv 均为纸面值，跨区比较不可信。")

    no_os = [r["region"] for r in rows if r["n_os"] == 0]
    if no_os:
        print(f"\n仍无 OS 数据（纸面分，未知衰减）: {', '.join(no_os)}")
    if stamps:
        print(f"DB OS 快照同步日: {', '.join(f'{k}({v}颗)' for k, v in sorted(stamps.items()))}")
        print("  ⚠ 平台 os.osISSharpeRatio 已恒为 null ⇒ 无法再刷新，DB 是存量快照。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
