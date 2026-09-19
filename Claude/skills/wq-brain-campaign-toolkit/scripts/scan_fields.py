# -*- coding: utf-8 -*-
"""scan_fields.py - 统一字段扫描器：直连 GET /data-fields 落 typed catalog。

typed catalog = gate 闸2/3 的数据源：每条字段带 {id, type, coverage, userCount,
alphaCount, description}；数据集级带 data_type（由字段类型众数推断）/region/universe/delay/fetched_at。

⚠️ 过滤参数必须是 dataset.id=<id>；裸 dataset=<id> 会被平台静默忽略
（返回全宇宙 10000 条上限，KOR 2026-08-15 实测）。

用法:
  python scan_fields.py --campaign-dir <DIR> --dataset model219                 # 全量落 catalog
  python scan_fields.py --campaign-dir <DIR> --dataset model219 --limit 5       # 快速冒烟
  python scan_fields.py --campaign-dir <DIR> --dataset model219 --zero-comp     # 只保留 userCount==0 字段
"""
import argparse
import collections
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import (CampaignContext, add_campaign_arg, load_credentials)
from _lib.api import Api
from _lib.wqb_store import save_catalog
from _lib.field_catalog_cache import get_cache_manager

PAGE = 50


def fetch_fields(api, settings, dataset, limit=None):
    """分页拉取指定 dataset 的全部字段。过滤必须 dataset.id=<id>（裸 dataset= 被静默忽略）。"""
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


# 2026-09-04 新增：字段类型自动标注 + 算子类别推荐
# 与 field_operator_pattern.md 适配矩阵对齐，S1 扫描时自动标注字段类型并推荐算子

_FIELD_TYPE_KEYWORDS = {
    "signal": ["score", "rank", "rating", "estimate", "surprise", "prediction", "signal", "alpha"],
    "scale": ["shares", "market cap", "market value", "enterprise value", "total assets", "total equity", "volume", "turnover"],
    "metadata": ["periodend", "periodtype", "fyearend", "periodnum", "analyststart", "curfperiod", "curperiod", "_date", "_dt", "fiscalend", "reportdate"],
    "date": ["date", "period end", "fiscal year end", "announcement", "timestamp"],
}

_FIELD_TYPE_OP_RECOMMEND = {
    "signal": ["rank", "ts_delta", "ts_mean", "ts_zscore", "group_zscore"],
    "scale": ["rank", "ts_mean", "group_scale"],
    "metadata": [],  # 禁用
    "date": [],      # 禁用
}


def _classify_field(field_id, description=""):
    """按字段名/描述推断字段类型（signal/scale/metadata/date）。"""
    fid_lower = field_id.lower()
    desc_lower = description.lower()
    
    # metadata 优先（永不应入表达式）
    for kw in _FIELD_TYPE_KEYWORDS["metadata"]:
        if kw in fid_lower or kw in desc_lower:
            return "metadata"
    
    # date 次之
    for kw in _FIELD_TYPE_KEYWORDS["date"]:
        if kw in fid_lower or kw in desc_lower:
            return "date"
    
    # scale 再次
    for kw in _FIELD_TYPE_KEYWORDS["scale"]:
        if kw in fid_lower or kw in desc_lower:
            return "scale"
    
    # signal 兜底
    return "signal"


def _recommend_operators(field_type, data_type="MATRIX"):
    """按字段类型推荐算子类别。"""
    base_ops = _FIELD_TYPE_OP_RECOMMEND.get(field_type, [])
    if data_type == "VECTOR":
        # VECTOR 字段必须先聚合
        return ["vec_avg", "vec_stddev", "vec_count"] + base_ops
    return base_ops


def build_catalog(settings, dataset, raw):
    types = collections.Counter((f.get("type") or "UNKNOWN") for f in raw)
    data_type = types.most_common(1)[0][0] if types else "UNKNOWN"
    fields = [{
        "id": f.get("id"),
        "type": f.get("type"),
        "coverage": f.get("coverage"),
        "userCount": f.get("userCount"),
        "alphaCount": f.get("alphaCount"),
        "description": (f.get("description") or "")[:120],
        # 2026-09-04 新增：字段类型标注 + 算子推荐
        "field_type": _classify_field(f.get("id", ""), f.get("description", "")),
        "recommended_operators": _recommend_operators(
            _classify_field(f.get("id", ""), f.get("description", "")),
            data_type
        ),
    } for f in raw]
    
    # 字段类型分布统计
    field_type_dist = collections.Counter(f["field_type"] for f in fields)
    
    return {
        "dataset": dataset,
        "region": settings["region"],
        "universe": settings["universe"],
        "delay": settings["delay"],
        "data_type": data_type,
        "type_distribution": dict(types),
        "field_type_distribution": dict(field_type_dist),  # 2026-09-04 新增
        "field_count": len(fields),
        "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "fields": fields,
    }


def main():
    ap = argparse.ArgumentParser(description="typed catalog 字段扫描")
    add_campaign_arg(ap)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--zero-comp", action="store_true", help="只保留 userCount==0 的零竞争字段")
    ap.add_argument("--stdout", action="store_true", help="只打印不落盘")
    ap.add_argument("--force-refresh", action="store_true", help="强制刷新缓存")
    ap.add_argument("--cache-ttl", type=int, default=86400, help="缓存有效期（秒），默认 24 小时")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)

    # 初始化缓存管理器
    cache_manager = get_cache_manager(ctx, a.cache_ttl)
    
    # 1. 检查缓存（除非强制刷新）
    if not a.force_refresh:
        cached = cache_manager.get_cached_catalog(a.dataset)
        if cached:
            print(f"[cache] 使用缓存的字段目录（{len(cached.get('fields', []))} 个字段，"
                  f"缓存时间: {cached.get('cache_metadata', {}).get('cached_at', 'unknown')})")
            if a.stdout:
                print(json.dumps(cached, ensure_ascii=False, indent=1))
            else:
                save_catalog(ctx, cached)  # 确保 DB 同步
                print(f"catalog -> db fields/{ctx.region}/{a.dataset} ({cached['field_count']}) [cached]")
            return

    # 2. 缓存未命中或强制刷新，执行平台扫描
    print(f"[cache] 缓存未命中或强制刷新，从平台扫描 {a.dataset}...")
    e, pw = load_credentials()
    api = Api()
    api.login(e, pw)
    raw = fetch_fields(api, ctx.settings, a.dataset, limit=a.limit)
    if a.zero_comp:
        raw = [f for f in raw if (f.get("userCount") or 0) == 0]
    cat = build_catalog(ctx.settings, a.dataset, raw)
    
    print(f"dataset={a.dataset} fields={cat['field_count']} data_type={cat['data_type']} "
          f"types={cat['type_distribution']}", file=sys.stderr)
    
    if a.stdout:
        print(json.dumps(cat, ensure_ascii=False, indent=1))
        return
    
    # 3. 保存到缓存和 DB
    save_catalog(ctx, cat)
    cache_manager.save_catalog_cache(a.dataset, cat)
    print(f"catalog -> db fields/{ctx.region}/{a.dataset} ({cat['field_count']}) [fresh]")


if __name__ == "__main__":
    import os as _os_sc; _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    main()
