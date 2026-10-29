"""按金字塔塔位反查数据集：哪个数据集实际产出过哪些塔的 alpha。

背景（2026-10-28）：点塔要求「同一座塔累计 N 颗」，但**塔位不能由数据集名或
category 推断**——平台权威口径是 alpha 详情里的 `ra.pyramid_short` / `pyramids.list`。
实证反例：
  * `insider_trx_matrix` 的 category 是 INSIDERS，产出的 alpha 却全部落在 **OTHER** 塔；
  * `macro_equity_signals` 名字带 macro，平台 category 实为 **MODEL**。
所以「找某座塔的第二来源」必须先有本表，不能靠猜。

数据源（唯一可用）：`tracking/mining/result_*.json`。
本地 `backtest_results.payload_json` **不含** `pyramid_short`（实测），`alphas` 表也没有
塔位列 —— 塔位只在平台 alpha 详情 / mining 原始结果文件里。故本工具扫 mining 文件，
从文件名反推数据集（`result_<dataset>[_<region>]_b<N>.json`）。

用法::

    python tools/query_tower_by_dataset.py --region USA
    python tools/query_tower_by_dataset.py --region USA --tower other --min-sharpe 1.5
    python tools/query_tower_by_dataset.py --region USA --tower other --list
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MINING_DIR = ROOT / "tracking" / "mining"

# result_risk65_usa_b120.json / result_option9_b43.json / result_si3_b203b_raw.json
_NAME_RE = re.compile(
    r"^result_(?P<ds>.+?)(?:_(?P<region>usa|chn|eur|asi|glb|ind|jpn|kor|twn|hkg|deu|gbr|amr|mea))?"
    r"_b\d+[a-z]*(?:_raw)?$"
)


def parse_dataset(path: Path) -> tuple[str, str | None]:
    stem = path.stem
    m = _NAME_RE.match(stem)
    if not m:
        return stem.replace("result_", "", 1), None
    return m.group("ds"), (m.group("region") or "").upper() or None


def load_rows(mining_dir: Path):
    out = []
    for path in sorted(mining_dir.glob("result_*.json")):
        ds, region = parse_dataset(path)
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(doc, dict):
            continue
        settings = doc.get("settings")
        if not isinstance(settings, dict):
            settings = {}
        reg = str(settings.get("region") or region or "").upper() or None
        for item in doc.get("results") or []:
            if not isinstance(item, dict):
                continue
            ra = item.get("ra") or {}
            tower = ra.get("pyramid_short")
            if not tower:
                continue
            met = item.get("metrics") or {}
            out.append(
                {
                    "alpha_id": item.get("alpha_id"),
                    "expression": item.get("expression") or item.get("code"),
                    "dataset": ds,
                    "region": reg,
                    "tower": str(tower).lower(),
                    "sharpe": met.get("sharpe"),
                    "fitness": met.get("fitness"),
                    "turnover": met.get("turnover"),
                    "two_year_sharpe": met.get("two_year_sharpe"),
                    "sub_universe_sharpe": met.get("sub_universe_sharpe"),
                    "failed_ra_count": ra.get("failed_ra_count"),
                    "ra_failed_checks": ra.get("ra_failed_checks") or [],
                    "file": path.name,
                }
            )
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="按塔位反查数据集（数据源：tracking/mining 的 pyramid_short）")
    ap.add_argument("--region", default=None, help="区域过滤，如 USA；省略=全部")
    ap.add_argument("--tower", default=None, help="只看某座塔，如 other / risk / option")
    ap.add_argument("--dataset", default=None, help="只看某数据集（子串匹配）")
    ap.add_argument("--min-sharpe", type=float, default=None)
    ap.add_argument("--min-fitness", type=float, default=None)
    ap.add_argument("--list", action="store_true", help="逐条列出（默认只出数据集汇总）")
    ap.add_argument("--mining-dir", default=str(MINING_DIR))
    args = ap.parse_args(argv)

    rows = load_rows(Path(args.mining_dir))
    if not rows:
        print(f"无带 pyramid_short 的 mining 结果（{args.mining_dir}）", file=sys.stderr)
        return 1

    if args.region:
        rows = [r for r in rows if r["region"] == args.region.upper()]
    if args.tower:
        rows = [r for r in rows if r["tower"] == args.tower.lower()]
    if args.dataset:
        needle = args.dataset.lower()
        rows = [r for r in rows if needle in r["dataset"].lower()]
    if args.min_sharpe is not None:
        rows = [r for r in rows if r["sharpe"] is not None and r["sharpe"] >= args.min_sharpe]
    if args.min_fitness is not None:
        rows = [r for r in rows if r["fitness"] is not None and r["fitness"] >= args.min_fitness]

    if not rows:
        print("过滤后无记录", file=sys.stderr)
        return 1

    by_ds = collections.defaultdict(list)
    towers_of = collections.defaultdict(set)
    for r in rows:
        by_ds[r["dataset"]].append(r)
        towers_of[r["dataset"]].add(r["tower"])

    scope = ", ".join(
        x
        for x in (
            f"region={args.region.upper()}" if args.region else None,
            f"tower={args.tower.lower()}" if args.tower else None,
        )
        if x
    ) or "all"
    print(f"{scope}  rows={len(rows)}  datasets={len(by_ds)}")
    print(f"{'dataset':32s} {'towers':20s} {'n':>4s} {'raClean':>7s}  {'best_S':>7s} {'F':>6s} {'tvr':>7s} {'2Y':>6s}  best_id")

    def best_key(r):
        return (r["sharpe"] if r["sharpe"] is not None else -9)

    for ds, rs in sorted(by_ds.items(), key=lambda kv: -max(best_key(r) for r in kv[1])):
        best = max(rs, key=best_key)
        n_clean = sum(1 for r in rs if r["failed_ra_count"] == 0)
        f = lambda v, w, p: (f"{v:{w}.{p}f}" if v is not None else " " * (w - 1) + "-")
        print(
            f"{ds:32s} {'/'.join(sorted(towers_of[ds])):20s} {len(rs):4d} {n_clean:7d}  "
            f"{f(best['sharpe'], 7, 2)} {f(best['fitness'], 6, 2)} {f(best['turnover'], 7, 4)} "
            f"{f(best['two_year_sharpe'], 6, 2)}  {best['alpha_id']}"
        )
        if args.list:
            for r in sorted(rs, key=best_key, reverse=True)[:20]:
                print(
                    f"    - {str(r['alpha_id']):10s} S={r['sharpe']} F={r['fitness']} "
                    f"tvr={r['turnover']} 2Y={r['two_year_sharpe']} "
                    f"fRA={r['failed_ra_count']} :: {str(r['expression'])[:90]}"
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
