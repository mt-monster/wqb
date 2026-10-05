# -*- coding: utf-8 -*-
"""fetch_dataset_assets.py - 全 Region 数据集资产拉取（**直连入库**，不落 JSON）。

2026-10-01 改造：原实现为「拉取 → data/dataset_assets/*.json → 另一个脚本再入库」的两步式中转
（历史原因：当时库层 upsert_field_catalog 未稳定）。现库层 API 已完备，改为一次到位：
平台 API → 内存 catalog → CampaignStore 直写 `datasets` / `fields` 表。
- 字段明细：`store.upsert_field_catalog(region, catalog)`
- 数据集级（含尚未拉字段的数据集）：`store.upsert_dataset_meta(region, meta)`

用法：
  python tools/fetch_dataset_assets.py --regions USA --apply
  python tools/fetch_dataset_assets.py --regions ALL --apply --max-datasets 40
  python tools/fetch_dataset_assets.py --regions USA            # dry-run（默认）

REGIONS 常量保留 2026-08-26/27 的初始范围（USA + MEA）；扩区用 `--regions` 覆盖，或直接用
`tools/build_field_index.py`（按 config.REGIONS 取 universe，带断点续跑 + 429 退避）。
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "lib"))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

from api_client import Api, load_creds  # noqa: E402

DEFAULT_DB = os.path.join(REPO_ROOT, "data", "wqb.db")

# 全 Region 配置（来自 get_platform_setting_options）
# 2026-08-26 用户调整：先仅拉 USA，其他 Region 暂缓
# 2026-08-27 用户要求：追加 MEA
REGIONS = {
    "USA": {"universe": "TOP3000", "delay": 1},
    "MEA": {"universe": "TOP400", "delay": 1},
    # "GLB": {"universe": "TOP3000", "delay": 1},
    # "EUR": {"universe": "TOP2500", "delay": 1},
    # "ASI": {"universe": "MINVOL1M", "delay": 1},
    # "CHN": {"universe": "TOP2000U", "delay": 1},
    # "KOR": {"universe": "TOP600", "delay": 1},
    # "HKG": {"universe": "TOP800", "delay": 1},
    # "IND": {"universe": "TOP500", "delay": 1},
    # "DEU": {"universe": "TOP500", "delay": 1},
    # "GBR": {"universe": "TOP700", "delay": 1},
}

PAGE = 50


def fetch_datasets(api, region, universe, delay):
    """分页拉取指定 Region 的数据集列表。"""
    base = (f"/data-sets?instrumentType=EQUITY&region={region}"
            f"&delay={delay}&universe={universe}&limit={PAGE}")
    out, offset = [], 0
    while True:
        j = json.load(api.get(f"{base}&offset={offset}"))
        results = j.get("results", [])
        out.extend(results)
        offset += len(results)
        if not results or offset >= j.get("count", 0):
            return out


def fetch_fields(api, region, universe, delay, dataset_id, limit=None):
    """分页拉取指定 dataset 的全部字段（必须 dataset.id=，裸 dataset= 会被静默忽略）。"""
    base = (f"/data-fields?instrumentType=EQUITY&region={region}"
            f"&delay={delay}&universe={universe}&dataset.id={dataset_id}&limit={PAGE}")
    out, offset = [], 0
    while True:
        j = json.load(api.get(f"{base}&offset={offset}"))
        results = j.get("results", [])
        out.extend(results)
        if limit and len(out) >= limit:
            return out[:limit]
        offset += len(results)
        if not results or offset >= j.get("count", 0):
            return out


def ppa_prefilter(ds):
    """PPA 预筛: coverage>=0.6 / alphaCount<=200 / fieldCount>=10 (2026-08-26 用户调整)"""
    cov = ds.get("coverage", 0)
    ac = ds.get("alphaCount", 999999)
    fc = ds.get("fieldCount", 0)
    return {
        "pass": cov >= 0.6 and ac <= 200 and fc >= 10,
        "coverage": cov,
        "alphaCount": ac,
        "fieldCount": fc,
        "valueScore": ds.get("valueScore", 0),
        "pyramidMultiplier": ds.get("pyramidMultiplier", 1.0),
    }


def build_catalog(region, universe, delay, ds, raw_fields):
    """平台字段原始返回 → typed catalog（与 toolkit scan_fields.build_catalog 同构）。"""
    types = {}
    for f in raw_fields:
        t = f.get("type") or "UNKNOWN"
        types[t] = types.get(t, 0) + 1
    data_type = max(types, key=types.get) if types else "UNKNOWN"
    fields = [{
        "id": f.get("id"),
        "type": f.get("type"),
        "coverage": f.get("coverage"),
        "userCount": f.get("userCount"),
        "alphaCount": f.get("alphaCount"),
        "description": (f.get("description") or "")[:500],
    } for f in raw_fields]
    return {
        "dataset": ds["id"],
        "region": region,
        "universe": universe,
        "delay": delay,
        "data_type": data_type,
        "type_distribution": types,
        "field_count": len(fields),
        "ppa_prefilter": ppa_prefilter(ds),
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "fields": fields,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="数据集资产拉取（直连入库）")
    ap.add_argument("--regions", default=",".join(REGIONS),
                    help="逗号分隔区域；默认 " + ",".join(REGIONS))
    ap.add_argument("--apply", action="store_true", help="真正写库（默认 dry-run）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-datasets", type=int, help="每区最多拉取字段的数据集数（调试）")
    ap.add_argument("--min-value-score", type=float, default=4.0,
                    help="拉字段的价值分阈值；PPA 预筛通过的数据集始终拉取")
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--sleep", type=float, default=0.5, help="字段请求间隔秒（防 429）")
    a = ap.parse_args()
    apply = a.apply and not a.dry_run

    from wqb.store import CampaignStore

    regions = [r.strip().upper() for r in a.regions.split(",") if r.strip()]
    store = CampaignStore(a.db)
    print(f"数据库: {a.db}  region={'/'.join(regions)}  mode={'APPLY' if apply else 'dry-run'}")

    email, password = load_creds()
    api = Api()
    api.login(email, password)

    stats_all = {}
    for region in regions:
        cfg = REGIONS.get(region) or {"universe": "TOP3000", "delay": 1}
        universe, delay = cfg["universe"], cfg["delay"]
        print(f"\n=== {region} (universe={universe}, delay={delay}) ===")
        try:
            datasets = fetch_datasets(api, region, universe, delay)
        except Exception as e:
            print(f"  拉取失败: {e}")
            stats_all[region] = {"error": str(e)}
            continue
        ppa_pass = [d for d in datasets if ppa_prefilter(d)["pass"]]
        high_value = [d for d in datasets
                      if d.get("valueScore", 0) >= a.min_value_score or ppa_prefilter(d)["pass"]]
        if a.max_datasets:
            high_value = high_value[:a.max_datasets]
        print(f"  数据集={len(datasets)}  PPA 预筛通过={len(ppa_pass)}  拉字段={len(high_value)}")

        if not apply:
            for d in datasets[:8]:
                pf = ppa_prefilter(d)
                print(f"    [DRY] {str(d.get('id')):28s} fields={d.get('fieldCount')} "
                      f"cov={pf['coverage']} alphaCount={pf['alphaCount']} "
                      f"ppa={'PASS' if pf['pass'] else '-'}")
            stats_all[region] = {"total_datasets": len(datasets),
                                 "ppa_pass": len(ppa_pass),
                                 "to_fetch": len(high_value)}
            continue

        # 1) 数据集级快照：全部数据集建行/刷新（不拉字段）
        n_ds = 0
        for d in datasets:
            try:
                pf = ppa_prefilter(d)
                # tier 沿用原 ingest 口径：PPA 预筛通过 → PPA_PASS，否则 STANDARD
                store.upsert_dataset_meta(
                    region, dict(d, delay=delay,
                                 tier="PPA_PASS" if pf["pass"] else "STANDARD"))
                n_ds += 1
            except Exception as e:
                print(f"    {d.get('id')}: 元数据入库失败 {e}")
        # 2) 字段明细：高价值 / PPA 通过的数据集
        n_fields = 0
        for i, d in enumerate(high_value, 1):
            ds_id = d["id"]
            try:
                raw = fetch_fields(api, region, universe, delay, ds_id)
                cat = build_catalog(region, universe, delay, d, raw)
                store.upsert_field_catalog(region, cat)
                n_fields += len(cat["fields"])
                print(f"    [{i}/{len(high_value)}] {ds_id}: {len(cat['fields'])} 字段"
                      f" ({cat['data_type']})")
            except Exception as e:
                print(f"    [{i}/{len(high_value)}] {ds_id}: ERROR - {e}")
            time.sleep(a.sleep)
        stats_all[region] = {"total_datasets": len(datasets),
                             "ppa_pass": len(ppa_pass),
                             "meta_rows_written": n_ds,
                             "fields_written": n_fields}
        print(f"  入库: 数据集行={n_ds} 字段={n_fields}")

    print(f"\n[{datetime.now()}] {'完成' if apply else 'dry-run 完成'}")
    print(json.dumps(stats_all, ensure_ascii=False, indent=1))
    store.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
