# -*- coding: utf-8 -*-
"""scan_fields.py - 统一字段扫描器（M3/M4）。

取代 kor_scan_fields.py/2/3、scan_aieq.py/scan_aieq2.py（它们硬编 .qoder-cn 会话
cache 且从不取 type 列——wave2 acquisition_model 24/24 ERROR 的根因）。

直连平台 GET /data-fields，落 typed catalog：reference/kor_<dataset>_fields.json
canonical schema：每条字段带 {id, type, coverage, userCount, alphaCount, description}；
数据集级带 data_type（由字段类型众数推断）/region/universe/delay/fetched_at。

用法:
  python scan_fields.py --dataset model219                 # 全量落 catalog
  python scan_fields.py --dataset model219 --limit 5       # 快速冒烟
  python scan_fields.py --dataset model219 --zero-comp     # 只保留 userCount==0 字段
"""
import argparse, collections, datetime, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from kor_fetch_metrics import Api, load_creds

SETTINGS = json.load(open(os.path.join(ROOT, "config", "settings.json"), encoding="utf-8"))
PAGE = 50


def fetch_fields(api, dataset, limit=None):
    """分页拉取指定 dataset 的全部字段。
    注意：过滤参数必须是 dataset.id=<id>；裸 dataset=<id> 会被平台静默忽略
    （返回全宇宙 10000 条上限，2026-08-15 实测）。"""
    base = ("/data-fields?instrumentType={instrumentType}&region={region}"
            "&delay={delay}&universe={universe}&dataset.id={ds}&limit={pg}").format(
                pg=PAGE, ds=dataset, **SETTINGS)
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


def build_catalog(dataset, raw):
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
        "region": SETTINGS["region"],
        "universe": SETTINGS["universe"],
        "delay": SETTINGS["delay"],
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
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--zero-comp", action="store_true", help="只保留 userCount==0 的零竞争字段")
    ap.add_argument("--stdout", action="store_true", help="只打印不落盘")
    a = ap.parse_args()

    e, pw = load_creds()
    api = Api()
    api.login(e, pw)
    raw = fetch_fields(api, a.dataset, limit=a.limit)
    if a.zero_comp:
        raw = [f for f in raw if (f.get("userCount") or 0) == 0]
    cat = build_catalog(a.dataset, raw)
    print(f"dataset={a.dataset} fields={cat['field_count']} data_type={cat['data_type']} "
          f"types={cat['type_distribution']}", file=sys.stderr)
    if a.stdout:
        print(json.dumps(cat, ensure_ascii=False, indent=1))
        return
    out = os.path.join(ROOT, "reference", f"kor_{a.dataset}_fields.json")
    atomic_write(out, cat)
    print(f"catalog -> {out}")


if __name__ == "__main__":
    main()
