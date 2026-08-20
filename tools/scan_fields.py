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


def build_catalog(dataset, settings, raw, sample_stock_count=None):
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
    
    # 横截面股票覆盖预估 (2026-08-18 wave34 教训)
    # 用 coverage 和 universe 大小预估 longCount+shortCount
    # 若预估值 < 100 → 标记 low_stock_coverage: true
    universe_size = _get_universe_size(settings.get("universe", "TOP3000"))
    avg_coverage = sum(f.get("coverage", 0) for f in raw) / len(raw) if raw else 0
    estimated_stock_count = int(universe_size * avg_coverage)
    
    # 若有实测 sample_stock_count, 优先使用实测值
    if sample_stock_count is not None:
        estimated_stock_count = sample_stock_count
        low_stock_coverage = estimated_stock_count < 100
    else:
        low_stock_coverage = estimated_stock_count < 100
    
    return {
        "dataset": dataset,
        "region": settings["region"],
        "universe": settings["universe"],
        "delay": settings["delay"],
        "data_type": data_type,
        "type_distribution": dict(types),
        "field_count": len(fields),
        "estimated_stock_count": estimated_stock_count,
        "low_stock_coverage": low_stock_coverage,
        "avg_coverage": round(avg_coverage, 4),
        "sample_stock_count": sample_stock_count,  # 实测值(若有)
        "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "fields": fields,
    }


def _get_universe_size(universe):
    """根据 universe 名称返回大致股票数"""
    size_map = {
        "TOP3000": 3000, "TOP2000": 2000, "TOP1000": 1000,
        "TOP800": 800, "TOP700": 700, "TOP600": 600,
        "TOP500": 500, "TOP400": 400, "TOP300": 300,
        "TOP200": 200, "TOP100": 100,
        "MINVOL1M": 1000, "TOP2000U": 2000,
    }
    return size_map.get(universe, 1000)


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
    ap.add_argument("--sample-field", help="用 sample 字段快速回测验证 longCount+shortCount (实测股票覆盖)")
    a = ap.parse_args()

    settings = load_settings(a.campaign_dir)
    e, pw = load_creds()
    api = Api()
    api.login(e, pw)
    raw = fetch_fields(api, a.dataset, settings, limit=a.limit)
    if a.zero_comp:
        raw = [f for f in raw if (f.get("userCount") or 0) == 0]
    
    # 实测股票覆盖 (2026-08-18 wave34 教训)
    # 若指定 --sample-field, 用该字段快速回测验证 longCount+shortCount
    sample_stock_count = None
    if a.sample_field:
        print(f"[sample] 用字段 {a.sample_field} 快速回测验证股票覆盖...", file=sys.stderr)
        try:
            # 构造简单表达式: rank(field)
            expr = f"rank({a.sample_field})"
            # 调用平台 API 快速回测
            # 注意: 这里需要集成 MCP create_simulation, 目前用占位实现
            print(f"[sample] 表达式: {expr}", file=sys.stderr)
            print(f"[sample] 需要集成 MCP create_simulation 实测 longCount+shortCount", file=sys.stderr)
            # TODO: 集成 MCP create_simulation
            # result = api.create_simulation(expr, settings)
            # sample_stock_count = result.get('longCount', 0) + result.get('shortCount', 0)
        except Exception as ex:
            print(f"[sample] 实测失败: {ex}", file=sys.stderr)
    
    cat = build_catalog(a.dataset, settings, raw, sample_stock_count=sample_stock_count)
    print(f"dataset={a.dataset} fields={cat['field_count']} data_type={cat['data_type']} "
          f"types={cat['type_distribution']}", file=sys.stderr)
    if cat.get('low_stock_coverage'):
        print(f"[WARN] 横截面股票覆盖不足: {cat['estimated_stock_count']} < 100", file=sys.stderr)
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
