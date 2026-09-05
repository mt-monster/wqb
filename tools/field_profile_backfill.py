# -*- coding: utf-8 -*-
"""field_profile_backfill.py - 从 WebDataScope zip 解析字段画像并回填 data/wqb.db。

字段画像（shape/skew/kurt/integer/freq/正负比/near_zero）是「字段→模板族」匹配的
硬约束数据源（形状为主、类别为辅）。本工具把 zip 里 .bin 的 10 年体检解析为结构化
画像，写入 field_profile 表，并把数据集级形状摘要写进 ledger（s1_profile_<dataset>）。

用法:
    # 回填指定 region 的全部数据集（zip 内覆盖到的）
    python tools/field_profile_backfill.py --zip research-data/WebData_20260219_V0.10.9.zip --region KOR

    # 只回填指定数据集
    python tools/field_profile_backfill.py --zip research-data/WebData_20260219_V0.10.9.zip --region KOR --datasets analyst25

    # dry-run：只打印不落库
    python tools/field_profile_backfill.py --zip research-data/WebData_20260219_V0.10.9.zip --region KOR --dry-run
"""
import argparse
import json
import os
import re
import sys
import zipfile
from typing import Any, Dict, List, Optional

# tools 目录 + src 目录注入（CampaignStore 在 src/wqb）
_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_TOOLS_DIR)
sys.path.insert(0, _TOOLS_DIR)
sys.path.insert(0, os.path.join(_REPO_ROOT, "src"))

from webdata_quality import (  # noqa: E402
    load_bin,
    parse_yearly_distribution,
    classify_distribution,
    mean_year,
)


def _shape_of(fdata: Dict[str, Any]) -> str:
    yd = fdata.get("yearly_distribution", "")
    if isinstance(yd, str) and (yd.startswith("{") or yd.startswith("[")):
        dist = parse_yearly_distribution(yd)
        if dist:
            shape, _ = classify_distribution(dist)
            return shape
    return "unknown"


def _profile_of(field_name: str, fdata: Dict[str, Any]) -> Dict[str, Any]:
    """把单字段 .bin 体检数据解析为结构化画像。"""
    cr = fdata.get("CoverageRatio", [])
    pos_r = fdata.get("IndicativePositiveRatio", [])
    neg_r = fdata.get("IndicativeNegativeRatio", [])
    int_s = fdata.get("IntegerStatus", [])
    freq = fdata.get("frequency", [])
    skew = fdata.get("skenewss", [])
    kurt = fdata.get("kurtosis", [])

    f0 = None
    if freq:
        f0 = freq[0] if isinstance(freq[0], str) else str(freq[0])

    # near_zero_ratio：从分布直方图 [0,0.1) 占比推导（与 classify 的 zero_inflated 同口径）
    near_zero = None
    yd = fdata.get("yearly_distribution", "")
    if isinstance(yd, str) and (yd.startswith("{") or yd.startswith("[")):
        dist = parse_yearly_distribution(yd)
        if dist:
            total = sum(fr for _, _, fr in dist)
            if total > 0:
                near_zero = round(sum(fr for lo, hi, fr in dist if hi <= 0.1) / total, 4)

    return {
        "field_name": field_name,
        "shape": _shape_of(fdata),
        "coverage": round(mean_year(cr), 4) if cr else None,
        "skew": round(mean_year(skew), 3) if skew else None,
        "kurt": round(mean_year(kurt), 3) if kurt else None,
        "integer": bool(any(int_s)),
        "freq": f0,
        "pos_ratio": round(mean_year(pos_r), 4) if pos_r else None,
        "neg_ratio": round(mean_year(neg_r), 4) if neg_r else None,
        "near_zero_ratio": near_zero,
    }


def _parse_dataset_folder(bin_name: str) -> Optional[Dict[str, str]]:
    """'data/<dataset>_<REGION>_<UNIVERSE>_Delay<N>.bin' → {dataset, region, universe, delay}.

    delay 规范化为数字字符串（提取前导数字）；非标准 delay（如 '1_wrong'）返回 None 跳过。"""
    base = os.path.basename(bin_name)
    if base.endswith(".bin"):
        base = base[:-4]
    if "_Delay" not in base:
        return None
    head, delay = base.rsplit("_Delay", 1)
    parts = head.split("_")
    if len(parts) < 3:
        return None
    universe = parts[-1]
    region = parts[-2]
    dataset = "_".join(parts[:-2])
    # delay 规范化：提取前导数字（'1_wrong' → '1'；无数字 → None 跳过）
    m = re.match(r"^(\d+)", str(delay))
    if not m:
        return None
    delay_norm = m.group(1)
    return {"dataset": dataset, "region": region, "universe": universe, "delay": delay_norm}


def backfill(
    zip_path: str,
    region: Optional[str] = None,
    datasets: Optional[List[str]] = None,
    delay: Optional[int] = None,
    dry_run: bool = False,
    write_ledger: bool = True,
) -> Dict[str, Any]:
    from wqb.store.campaign import CampaignStore

    zf = zipfile.ZipFile(zip_path)
    names = set(zf.namelist())
    bin_names = [n for n in names if n.startswith("data/") and n.endswith(".bin")
                 and not n.endswith("dataSetList.json")]

    store = None if dry_run else CampaignStore.from_workspace(_REPO_ROOT)
    summary: Dict[str, Any] = {"datasets": {}, "total_fields": 0, "skipped": []}

    try:
        for bn in sorted(bin_names):
            meta = _parse_dataset_folder(bn)
            if not meta:
                continue
            if region and meta["region"] != region:
                continue
            if datasets and meta["dataset"] not in datasets:
                continue
            if delay is not None and meta["delay"] != str(delay):
                continue

            try:
                ds_data = load_bin(zf, bn)
            except Exception as exc:
                summary["skipped"].append({"bin": bn, "reason": f"load_bin failed: {exc}"})
                continue

            profiles = [_profile_of(f, fdata) for f, fdata in ds_data.items()]
            key = f"{meta['dataset']}_{meta['region']}_{meta['universe']}_Delay{meta['delay']}"

            if dry_run:
                import collections
                shapes = collections.Counter(p["shape"] for p in profiles)
                summary["datasets"][key] = {"fields": len(profiles), "shapes": dict(shapes)}
                summary["total_fields"] += len(profiles)
                continue

            # 落库 field_profile
            res = store.upsert_field_profile(meta["region"], meta["dataset"], profiles,
                                             source="webdatascope")
            # 数据集级形状摘要 → ledger s1_profile_<dataset>
            shape_sum = store.dataset_shape_summary(meta["region"], meta["dataset"])
            shape_sum["universe"] = meta["universe"]
            shape_sum["delay"] = int(meta["delay"])
            if write_ledger:
                store.upsert_ledger(meta["region"], f"s1_profile_{meta['dataset']}", shape_sum)

            summary["datasets"][key] = {
                "fields": res["n"],
                "dominant_shape": shape_sum.get("dominant_shape"),
                "sparse_ratio": shape_sum.get("sparse_ratio"),
                "shape_counts": shape_sum.get("shape_counts"),
            }
            summary["total_fields"] += res["n"]
    finally:
        zf.close()
        if store is not None:
            store.close()

    return summary


def main():
    ap = argparse.ArgumentParser(description="WebDataScope 字段画像回填 field_profile 表")
    ap.add_argument("--zip", required=True, help="WebDataScope 数据包 zip 路径")
    ap.add_argument("--region", default=None, help="只回填该 region（默认全部）")
    ap.add_argument("--datasets", default=None, help="逗号分隔数据集列表（默认该 region 全部）")
    ap.add_argument("--delay", type=int, default=None, help="只回填该 delay（默认全部）")
    ap.add_argument("--dry-run", action="store_true", help="只打印不落库")
    ap.add_argument("--no-ledger", action="store_true", help="不写 s1_profile_<dataset> ledger")
    ap.add_argument("--json-out", default=None, help="摘要输出到 JSON 文件")
    args = ap.parse_args()

    zip_path = args.zip
    if not os.path.isabs(zip_path):
        zip_path = os.path.join(_REPO_ROOT, zip_path)
    if not os.path.isfile(zip_path):
        print(f"ERROR: zip not found: {zip_path}", file=sys.stderr)
        sys.exit(1)

    ds_list = [d.strip() for d in args.datasets.split(",")] if args.datasets else None
    summary = backfill(
        zip_path,
        region=args.region,
        datasets=ds_list,
        delay=args.delay,
        dry_run=args.dry_run,
        write_ledger=not args.no_ledger,
    )

    print(f"=== field_profile backfill {'(DRY-RUN)' if args.dry_run else ''} ===")
    print(f"datasets: {len(summary['datasets'])}, total_fields: {summary['total_fields']}")
    for key, info in summary["datasets"].items():
        if args.dry_run:
            print(f"  {key}: {info['fields']} fields, shapes={info['shapes']}")
        else:
            print(f"  {key}: {info['fields']} fields, dominant={info['dominant_shape']}, "
                  f"sparse_ratio={info['sparse_ratio']}")
    if summary["skipped"]:
        print(f"skipped: {len(summary['skipped'])}")
        for s in summary["skipped"][:10]:
            print(f"  {s['bin']}: {s['reason']}")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"summary written: {args.json_out}")


if __name__ == "__main__":
    main()
