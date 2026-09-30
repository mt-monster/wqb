#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_field_index.py — 构建/补齐「平台级字段→数据集索引」（降低 atom 判定的 unknown）。

背景：atom/combined 判定依赖「字段→数据集」映射。本地 `fields` 表已收录 27 万字段，
但部分数据集未扫 → 引用其字段的表达式被判 unknown。本工具用平台 API 按数据集补齐：
  /data-sets   → 该区数据集清单（含 fieldCount）
  /data-fields → 指定 dataset.id 的字段（分页；注意 /data-fields 无 dataset 过滤时
                 offset 上限 10000，故**必须按 dataset.id 取**）

补齐后运行 `tools/atom_labeler.py --backfill --apply` 即自动降 unknown。

用法：
  python tools/build_field_index.py --regions GLB --dry-run        # 只统计工作量
  python tools/build_field_index.py --regions GLB --apply          # 只补有缺口的数据集
  python tools/build_field_index.py --regions GLB --all --apply --limit-datasets 5
  python tools/build_field_index.py --regions ALL --apply          # 全部有数据的区域

断点续跑：checkpoint 落在 data/field_index_ckpt.json（按 region+dataset 记录已完成），
重启自动跳过；平台设置变更用 --fresh 忽略续跑。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB = os.path.join(REPO_ROOT, "data", "wqb.db")
CKPT = os.path.join(REPO_ROOT, "data", "field_index_ckpt.json")

sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "lib"))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))


def _get(api, path, retries=5):
    """GET + 退避重试（平台会 429 限流）。"""
    from urllib.error import HTTPError
    for i in range(retries):
        try:
            return json.load(api.get(path))
        except HTTPError as ex:
            if ex.code in (429, 500, 502, 503, 504):
                time.sleep(2.0 * (2 ** i))
                continue
            raise
    raise RuntimeError(f"retries exhausted: {path}")


def _paginate(api, base, limit_page=50, max_items=None, sleep=0.15):
    out, offset = [], 0
    while True:
        j = _get(api, f"{base}&limit={limit_page}&offset={offset}")
        res = j.get("results", [])
        out.extend(res)
        if max_items and len(out) >= max_items:
            return out[:max_items]
        offset += len(res)
        if not res or offset >= j.get("count", 0):
            return out
        time.sleep(sleep)


def region_settings(region):
    from wqb import config
    cfg = config.REGIONS.get(region)
    universe = (cfg or {}).get("default_universe") or "TOP3000"
    return {"instrumentType": "EQUITY", "region": region, "delay": 1, "universe": universe}


def fetch_datasets(api, st, sleep=0.4):
    base = ("/data-sets?instrumentType={instrumentType}&region={region}&delay={delay}"
            "&universe={universe}").format(**st)
    return _paginate(api, base, sleep=sleep)


def fetch_dataset_fields(api, st, ds_id, sleep=0.4):
    base = ("/data-fields?instrumentType={instrumentType}&region={region}&delay={delay}"
            "&universe={universe}&dataset.id={ds}").format(ds=ds_id, **st)
    return _paginate(api, base, sleep=sleep)


def build_catalog(region, ds_name, raw):
    fields = [{
        "id": f.get("id"),
        "type": f.get("type"),
        "coverage": f.get("coverage"),
        "userCount": f.get("userCount"),
        "alphaCount": f.get("alphaCount"),
        "description": (f.get("description") or "")[:120],
    } for f in raw if f.get("id")]
    return {
        "dataset": ds_name,
        "region": region,
        "data_type": (raw[0].get("type") if raw else "MATRIX"),
        "field_count": len(fields),
        "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": "platform_build_field_index",
        "fields": fields,
    }


def load_ckpt(fresh=False):
    if fresh or not os.path.exists(CKPT):
        return {}
    try:
        return json.load(open(CKPT, encoding="utf-8"))
    except Exception:
        return {}


def save_ckpt(ckpt):
    tmp = CKPT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(ckpt, f, ensure_ascii=False, indent=0)
    os.replace(tmp, CKPT)


def local_field_counts(store):
    """dataset 名 → 本地 fields 行数。先对 fields 单次聚合再 join datasets——
    避免 `datasets LEFT JOIN fields GROUP BY d.id` 在无 fields(dataset_id) 索引时
    退化成 数据集数 × 字段数 的全表扫描（实测在 27 万字段库上要数分钟）。"""
    cur = store.connection.cursor()
    counts = {int(dsid): n for dsid, n in cur.execute(
        "SELECT dataset_id, COUNT(*) FROM fields GROUP BY dataset_id")}
    out = {}
    for dsid, dsname, rname in cur.execute(
            "SELECT d.id, d.name, r.name FROM datasets d JOIN regions r ON r.id=d.region_id"):
        out[(rname, dsname)] = counts.get(int(dsid), 0)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="构建平台级字段→数据集索引")
    ap.add_argument("--regions", default="ALL", help="逗号分隔区域，或 ALL（有 unknown 的区域）")
    ap.add_argument("--all", action="store_true", help="拉取该区所有数据集（默认只补有缺口的）")
    ap.add_argument("--apply", action="store_true", help="真正写库（默认 dry-run）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit-datasets", type=int, help="每区最多处理的数据集数（调试）")
    ap.add_argument("--sleep", type=float, default=0.4, help="API 调用间隔秒")
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--fresh", action="store_true", help="忽略 checkpoint 重新开始")
    a = ap.parse_args()

    from api_client import Api, load_creds
    from wqb.store import CampaignStore

    store = CampaignStore(a.db)
    e, pw = load_creds()
    if not e:
        print("[error] 未发现平台凭据（~/.brain_mcp_config.json / MCP .env）", file=sys.stderr)
        return 2
    api = Api(); api.login(e, pw)

    if a.regions == "ALL":
        cur = store.connection.cursor()
        regions = [r[0] for r in cur.execute(
            "SELECT DISTINCT region FROM expressions WHERE atom_flag='unknown' "
            "AND region IS NOT NULL ORDER BY region")]
    else:
        regions = [r.strip() for r in a.regions.split(",") if r.strip()]

    ckpt = load_ckpt(a.fresh)
    local_counts = local_field_counts(store)
    total_new_fields = 0
    total_datasets_done = 0

    for region in regions:
        try:
            st = region_settings(region)
        except Exception as ex:
            print(f"[{region}] 跳过：{ex}", file=sys.stderr)
            continue
        try:
            datasets = fetch_datasets(api, st, sleep=a.sleep)
        except Exception as ex:
            print(f"[{region}] /data-sets 失败：{repr(ex)[:120]}", file=sys.stderr)
            continue
        done = ckpt.setdefault(region, {})
        todo = []
        for d in datasets:
            dsid, dsname, fcnt = d.get("id"), d.get("name"), int(d.get("fieldCount") or 0)
            if not dsid:
                continue
            if str(dsid) in done:
                continue
            # 本地 datasets.name 存的是数据集 id（analyst14/model264…），
            # 平台 /data-sets 的 name 是长描述名 → 一律以 **id** 作为本地数据集名匹配。
            have = local_counts.get((region, dsid), 0)
            if a.all or have < fcnt:
                todo.append((dsid, dsname, fcnt, have))
        if a.limit_datasets:
            todo = todo[:a.limit_datasets]
        print(f"[{region}] universe={st['universe']} datasets={len(datasets)} "
              f"待补={len(todo)}（已有完成 {len(done)}）")
        if not a.apply:
            for dsid, dsname, fcnt, have in todo[:30]:
                print(f"  [{region}/{dsid}] {dsname[:34]:34s} 平台={fcnt} 本地={have} → 待补 {fcnt - have}")
            continue
        for dsid, dsname, fcnt, have in todo:
            try:
                raw = fetch_dataset_fields(api, st, dsid, sleep=a.sleep)
            except Exception as ex:
                print(f"  [{region}/{dsname}] 取字段失败：{repr(ex)[:100]}", file=sys.stderr)
                continue
            cat = build_catalog(region, dsid, raw)   # 以数据集 id 作为本地数据集名
            delta = len(cat["fields"]) - have
            print(f"  [{region}/{dsid}] 平台={fcnt} 本地={have} 拉到={len(cat['fields'])} (+{max(delta,0)})")
            if a.apply:
                try:
                    store.upsert_field_catalog(region, cat)
                except Exception as ex:
                    print(f"    写库失败：{repr(ex)[:100]}", file=sys.stderr)
                    continue
                done[str(dsid)] = True
                save_ckpt(ckpt)
                total_new_fields += max(delta, 0)
                total_datasets_done += 1
                local_counts[(region, dsid)] = len(cat["fields"])

    print(f"\n[summary] {'applied' if a.apply else 'dry-run'} "
          f"datasets_done={total_datasets_done} new_fields≈{total_new_fields}")
    if a.apply:
        print("下一步：python tools/atom_labeler.py --backfill --apply   # 重算 unknown")
    store.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
