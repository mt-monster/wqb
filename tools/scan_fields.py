# -*- coding: utf-8 -*-
"""scan_fields.py - 通用字段扫描器（区域无关）。

取代 KOR 专用版，支持任意战役目录。输出 typed catalog 到 <campaign-dir>/reference/<region>_<dataset>_fields.json。

用法:
  python tools/scan_fields.py --campaign-dir tracking/EUR --dataset ai_equity_alpha
  python tools/scan_fields.py --campaign-dir tracking/KOR --dataset model219 --limit 5
"""
import argparse
import collections
import datetime
import json
import os
import sys

# 添加 tools/lib 到路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from api_client import Api, load_creds

PAGE = 50


def load_settings(campaign_dir):
    """从战役目录加载 settings.json。"""
    p = os.path.join(campaign_dir, "config", "settings.json")
    if not os.path.exists(p):
        raise FileNotFoundError(f"settings.json 不存在: {p}")
    return json.load(open(p, encoding="utf-8"))


def fetch_fields(api, dataset, settings, limit=None):
    """分页拉取指定 dataset 的全部字段。"""
    base = ("/data-fields?instrumentType={instrumentType}&region={region}"
            "&delay={delay}&universe={universe}&dataset.id={ds}&limit={pg}").format(
                pg=PAGE, ds=dataset, **settings)
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


def build_catalog(dataset, settings, raw):
    types = collections.Counter((f.get("type") or "UNKNOWN") for f in raw)
    data_type = types.most_common(1)[0][0] if types else "UNKNOWN"
    fields = [{
        "id": f.get("id"),
        "type": f.get("type"),
        "coverage": f.get("coverage"),
        "userCount": f.get("userCount"),
        "alphaCount": f.get("alphaCount"),
        "description": (f.get("description") or "")[:120],
    } for f in raw]
    return {
        "dataset": dataset,
        "region": settings["region"],
        "universe": settings["universe"],
        "delay": settings["delay"],
        "data_type": data_type,
        "type_distribution": dict(types),
        "field_count": len(fields),
        "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "fields": fields,
    }


def atomic_write(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign-dir", required=True, help="战役根目录 (如 tracking/EUR)")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--zero-comp", action="store_true", help="只保留 userCount==0 的零竞争字段")
    ap.add_argument("--stdout", action="store_true", help="只打印不落盘")
    a = ap.parse_args()

    settings = load_settings(a.campaign_dir)
    e, pw = load_creds()
    api = Api()
    api.login(e, pw)
    raw = fetch_fields(api, a.dataset, settings, limit=a.limit)
    if a.zero_comp:
        raw = [f for f in raw if (f.get("userCount") or 0) == 0]
    cat = build_catalog(a.dataset, settings, raw)
    print(f"dataset={a.dataset} fields={cat['field_count']} data_type={cat['data_type']} "
          f"types={cat['type_distribution']}", file=sys.stderr)
    if a.stdout:
        print(json.dumps(cat, ensure_ascii=False, indent=1))
        return
    out_dir = os.path.join(a.campaign_dir, "reference")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{settings['region'].lower()}_{a.dataset}_fields.json")
    atomic_write(out, cat)
    print(f"catalog -> {out}")


if __name__ == "__main__":
    main()
