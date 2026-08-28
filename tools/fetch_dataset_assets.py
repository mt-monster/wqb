# -*- coding: utf-8 -*-
"""fetch_dataset_assets.py - 全 Region 数据集资产批量拉取与入库。

事件驱动基线建设：首次全量拉取，后续增量刷新。
输出: data/dataset_assets/<region>_datasets.json + <region>_<dataset>_fields.json
入库: wqb-db upsert_field_catalog + upsert_registry_empirical (PPA 预筛)
"""
import json
import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from api_client import Api, load_creds

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

OUT_DIR = "data/dataset_assets"
PAGE = 50


def ensure_dir():
    os.makedirs(OUT_DIR, exist_ok=True)


def fetch_datasets(api, region, universe, delay):
    """拉取指定 Region 的数据集列表。"""
    path = f"/data-sets?instrumentType=EQUITY&region={region}&delay={delay}&universe={universe}"
    j = json.load(api.get(path))
    return j.get("results", [])


def fetch_fields(api, region, universe, delay, dataset_id, limit=None):
    """分页拉取指定 dataset 的全部字段。"""
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


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    ensure_dir()
    email, password = load_creds()
    api = Api()
    api.login(email, password)
    print(f"[{datetime.now()}] 登录成功，开始拉取 {len(REGIONS)} 个 Region")

    all_stats = {}
    for region, cfg in REGIONS.items():
        print(f"\n=== {region} (universe={cfg['universe']}) ===")
        try:
            datasets = fetch_datasets(api, region, cfg["universe"], cfg["delay"])
            print(f"  数据集: {len(datasets)} 个")
            
            # 保存数据集列表
            ds_path = os.path.join(OUT_DIR, f"{region}_datasets.json")
            save_json({"region": region, "config": cfg, "datasets": datasets, "fetched_at": datetime.now().isoformat()}, ds_path)
            
            # PPA 预筛统计
            ppa_pass = [d for d in datasets if ppa_prefilter(d)["pass"]]
            all_stats[region] = {
                "total_datasets": len(datasets),
                "ppa_pass": len(ppa_pass),
                "ppa_pass_ids": [d["id"] for d in ppa_pass],
            }
            print(f"  PPA 预筛通过: {len(ppa_pass)} 个")
            
            # 拉取字段明细（仅对 PPA 通过或高价值数据集）
            high_value = [d for d in datasets if d.get("valueScore", 0) >= 4 or ppa_prefilter(d)["pass"]]
            print(f"  高价值/PPA通过数据集: {len(high_value)} 个，开始拉取字段...")
            
            for i, ds in enumerate(high_value, 1):
                ds_id = ds["id"]
                try:
                    fields = fetch_fields(api, region, cfg["universe"], cfg["delay"], ds_id)
                    field_path = os.path.join(OUT_DIR, f"{region}_{ds_id}_fields.json")
                    save_json({
                        "region": region,
                        "dataset": ds_id,
                        "dataset_meta": ds,
                        "ppa_prefilter": ppa_prefilter(ds),
                        "fields": fields,
                        "field_count": len(fields),
                        "fetched_at": datetime.now().isoformat(),
                    }, field_path)
                    print(f"    [{i}/{len(high_value)}] {ds_id}: {len(fields)} 字段")
                    time.sleep(0.5)  # 控制速率，避免 429
                except Exception as e:
                    print(f"    [{i}/{len(high_value)}] {ds_id}: ERROR - {e}")
                    
        except Exception as e:
            print(f"  Region {region} 失败: {e}")
            all_stats[region] = {"error": str(e)}
        
        time.sleep(1)  # Region 间间隔

    # 保存汇总
    summary_path = os.path.join(OUT_DIR, "_summary.json")
    save_json({"stats": all_stats, "fetched_at": datetime.now().isoformat()}, summary_path)
    print(f"\n[{datetime.now()}] 完成。汇总: {summary_path}")


if __name__ == "__main__":
    main()
