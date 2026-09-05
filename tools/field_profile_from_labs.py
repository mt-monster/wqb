# -*- coding: utf-8 -*-
"""field_profile_from_labs.py - 把 BRAIN Labs 批量画像 JSON 入库 field_profile 表。

配套 tracking/<REGION>/scripts/labs_field_profile_batch.py 使用：
  1. Labs 里跑 labs_field_profile_batch.py → 写出 field_profile_<ds>_<region>.json；
  2. 本工具读该 JSON，upsert 进 data/wqb.db 的 field_profile 表（source=brain_labs）；
  3. 顺带把数据集级形状摘要写进 ledger s1_profile_<dataset>。

用法:
    python tools/field_profile_from_labs.py --input field_profile_shortinterest3_KOR.json
    python tools/field_profile_from_labs.py --input field_profile_shortinterest3_KOR.json --dry-run
"""
import argparse
import json
import os
import sys
from typing import Any, Dict, List

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_TOOLS_DIR)
sys.path.insert(0, os.path.join(_REPO_ROOT, "src"))


def _to_profile(f: Dict[str, Any]) -> Dict[str, Any] | None:
    """把 Labs 画像记录转成 field_profile 表行（跳过 error 记录）。"""
    if f.get("error"):
        return None
    fname = f.get("field_name") or f.get("field")
    if not fname:
        return None
    return {
        "field_name": fname,
        "shape": f.get("shape"),
        "coverage": f.get("coverage"),
        "skew": f.get("skew"),
        "kurt": f.get("kurt"),
        "integer": bool(f.get("integer")),
        "freq": f.get("freq"),
        "pos_ratio": f.get("pos_ratio"),
        "neg_ratio": f.get("neg_ratio"),
        "near_zero_ratio": f.get("near_zero_ratio"),
    }


def ingest(input_path: str, dry_run: bool = False, write_ledger: bool = True) -> Dict[str, Any]:
    from wqb.store.campaign import CampaignStore

    with open(input_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    # 兼容两种形态：{dataset, region, fields:[...]} 或直接 [...]
    if isinstance(payload, dict):
        dataset = payload.get("dataset") or payload.get("dataset_id")
        region = payload.get("region")
        records = payload.get("fields") or []
    else:
        dataset, region, records = None, None, payload

    if not dataset or not region:
        raise ValueError("input JSON 缺 dataset/region（需 labs_field_profile_batch.py 产出的包装格式）")

    profiles = [p for p in (_to_profile(r) for r in records) if p]
    skipped = len(records) - len(profiles)

    summary: Dict[str, Any] = {"dataset": dataset, "region": region,
                               "ingested": len(profiles), "skipped_error": skipped}
    if dry_run:
        import collections
        shapes = collections.Counter(p["shape"] for p in profiles)
        summary["shapes"] = dict(shapes)
        return summary

    store = CampaignStore.from_workspace(_REPO_ROOT)
    try:
        res = store.upsert_field_profile(region, dataset, profiles, source="brain_labs")
        summary["upsert_n"] = res["n"]
        if write_ledger:
            shape_sum = store.dataset_shape_summary(region, dataset)
            store.upsert_ledger(region, f"s1_profile_{dataset}", shape_sum)
            summary["dominant_shape"] = shape_sum.get("dominant_shape")
            summary["sparse_ratio"] = shape_sum.get("sparse_ratio")
    finally:
        store.close()
    return summary


def main():
    ap = argparse.ArgumentParser(description="BRAIN Labs 批量画像 JSON 入库 field_profile")
    ap.add_argument("--input", required=True, help="labs_field_profile_batch.py 产出的 JSON 路径")
    ap.add_argument("--dry-run", action="store_true", help="只打印不落库")
    ap.add_argument("--no-ledger", action="store_true", help="不写 s1_profile_<dataset> ledger")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    summary = ingest(args.input, dry_run=args.dry_run, write_ledger=not args.no_ledger)
    print(f"=== field_profile_from_labs {'(DRY-RUN)' if args.dry_run else ''} ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
