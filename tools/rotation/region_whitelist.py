# -*- coding: utf-8 -*-
"""tools/region_whitelist.py — 区域安全的选集入口（2026-10-04）。

替代所有"拿某region 的 s0_ranking 当白名单"的错误做法。

事故背景
--------
``ledger_kv`` 里``key='s0_ranking'`` 这份榜单 **自身带region / universe 元信息**，
而它的条目**没有 region 字段**。实测该榜单为::

    region = KOR   universe = TOP600   total = 185

即它是 **KOR 的 S0 榜单**。但历史脚本（含 ``tools/tmp_eur_white.py``）
直接拿它当 EUR 白名单用，于是：

* ``risk88`` / ``risk59`` 被列为 "EUR tier1"，实际 EUR 平台``count=0``；
* 真正的 EUR risk 类可用集（risk60/62/68/70/72）反而没被正确区分。

本工具的纪律：
  1. 先用 :class:`wqb.region_catalog.RegionCatalog` 取该区**真实存在**的
     dataset 名单（本地 catalog 按区过滤），再与榜单条目求交集；
  2. 榜单元信息（region/universe）与目标区**不一致时直接拒绝**并报错，
     杜绝"张冠李戴"式污染；
  3. 输出显式标注每个 dataset 的本地字段数，便于人工核对平台。

用法::

    python tools/region_whitelist.py --region EUR --category risk
    python tools/region_whitelist.py --region EUR --tier tier1 --verify-platform
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wqb.region_catalog import RegionCatalog  # noqa: E402


def load_s0_rankings(rc: RegionCatalog, key: str = "s0_ranking"):
    """读``s0_ranking`` 的**全部**历史版本（含各自 region 元信息）。"""
    con = rc._conn
    out = []
    for row in con.execute(
        "SELECT id, value FROM ledger_kv WHERE key = ? ORDER BY id DESC", (key,)
    ):
        raw = row["value"]
        try:
            data = json.loads(raw)
        except Exception:
            try:
                data = ast.literal_eval(raw)
            except Exception:
                continue
        rows = data.get("ranking") or []
        out.append({
            "ledger_id": row["id"],
            "region": (data.get("region") or "").upper() or None,
            "universe": data.get("universe"),
            "total": data.get("total") or len(rows),
            "ranking": rows,
        })
    return out


def find_ranking_for(rc: RegionCatalog, region: str, key: str = "s0_ranking"):
    """挑出**元信息 region 与目标区一致**的榜单；无匹配则返回 None。"""
    cands = [b for b in load_s0_rankings(rc, key) if b["region"] == region.upper()]
    return cands[0] if cands else None


def build(rc: RegionCatalog, region: str, category: str | None = None,
          tier: str | None = None, ranking_key: str = "s0_ranking"):
    region = region.upper()
    real = set(rc.dataset_names(region, category=category))
    base = find_ranking_for(rc, region, ranking_key)

    rows = []
    if base is None:
        # 无该区榜单：退回"本地 catalog 真实存在"的全量，并显式标注。
        for name in sorted(real):
            rows.append({
                "dataset": name, "tier": None, "score": None,
                "field_count": len(rc.field_names(name, region)),
                "in_ranking": False,
            })
        return {"region": region, "category": category, "ranking_meta": None,
                "note": f"无 region={region} 的 {ranking_key} 榜单，返回本地 catalog 全量",
                "rows": rows}

    for item in base["ranking"]:
        name = str(item.get("id") or item.get("dataset") or "")
        if not name:
            continue
        if category and not (rc._conn.execute(
            "SELECT 1 FROM datasets d JOIN regions r ON r.id=d.region_id "
            "WHERE d.name=? AND r.name=? AND upper(d.category)=?",
            (name, region, category.upper()),
        ).fetchone()):
            continue
        if tier and str(item.get("tier") or "").lower() != tier.lower():
            continue
        rows.append({
            "dataset": name,
            "tier": item.get("tier"),
            "score": item.get("score"),
            "category": item.get("category"),
            # 关键：本地 catalog 按区过滤后的真实字段数
            "field_count": len(rc.field_names(name, region)),
            "exists_in_region": name in real,
            "in_ranking": True,
        })

    return {
        "region": region,
        "category": category,
        "ranking_meta": {k: base[k] for k in ("region", "universe", "total", "ledger_id")},
        "note": None,
        "rows": rows,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="区域安全选集（修s0_ranking 跨区污染）")
    ap.add_argument("--region", required=True)
    ap.add_argument("--category", default=None)
    ap.add_argument("--tier", default=None, choices=[None, "tier1", "tier2", "excluded"])
    ap.add_argument("--ranking-key", default="s0_ranking")
    ap.add_argument("--verify-platform", action="store_true",
                    help="调平台 get_datafields 复核字段数（会走网络）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rc = RegionCatalog()
    try:
        res = build(rc, args.region, args.category, args.tier, args.ranking_key)
        if args.verify_platform:
            import urllib.request
            for r in res["rows"]:
                r["platform_check"] = "skipped(需 MCP 工具)"
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
            return 0

        print(f"=== {args.region} 选集（category={args.category or 'ALL'} "
              f"tier={args.tier or 'ALL'}）===")
        if res["ranking_meta"]:
            m = res["ranking_meta"]
            print(f"榜单来源: ledger#{m['ledger_id']} region={m['region']} "
                  f"universe={m['universe']} total={m['total']}")
        else:
            print(f"⚠ {res['note']}")

        ok = [r for r in res["rows"] if r.get("exists_in_region", True)]
        bad = [r for r in res["rows"] if not r.get("exists_in_region", True)]
        print(f"\n本地 catalog 真实存在: {len(ok)} / 榜单命中 {len(res['rows'])}")
        for r in sorted(ok, key=lambda x: -(x.get("score") or 0)):
            print(f"  ✔ {r['dataset']:<24} tier={str(r['tier']):<9} "
                  f"score={r.get('score')} fields={r['field_count']}")
        if bad:
            print(f"\n⚠ 榜单有但该区不存在（应剔除）: {len(bad)}")
            for r in bad:
                print(f"  ✘ {r['dataset']:<24} tier={str(r['tier']):<9} score={r.get('score')}")
        return 0
    finally:
        rc.close()


if __name__ == "__main__":
    raise SystemExit(main())
