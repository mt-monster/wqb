# -*- coding: utf-8 -*-
"""validate_fields_batch.py - 批量字段可用性验证器（区域无关）。

核心优化：把"逐字段搜索验证"（validate_gbr_fields.py 的旧模式：每字段 1 次 API + 0.5s
延迟，535 字段 ~5 分钟）改成"按数据集批量灌 + 本地比对"（每个数据集 1 次分页请求，
13 个数据集 = 13 次请求），结果落库可复用。

工作机制：
  1. 对指定区域的每个真实数据集，用 GET /data-fields?dataset.id=<name> 分页拉全量字段
     （复用 scan_fields.fetch_fields 的正确姿势；注意必须用 dataset.id=，裸 dataset= 会被
     平台静默忽略）。
  2. 平台返回的字段集合 与 本地 fields 表比对：
     - 平台有、本地有  → verified=1
     - 本地有、平台无  → verified=-1（该区域上下文不可用）
  3. 写回 fields.verified / verified_context / verified_at。
  4. 断点续跑：默认跳过 verified_at 已非空且 verified_context 匹配的数据集；
     --fresh 强制重验。

用法：
  # 探针：只验 IND 的 analyst4 一个数据集
  python tools/validate_fields_batch.py --region IND --dataset analyst4

  # IND 全量
  python tools/validate_fields_batch.py --region IND

  # 强制重验（忽略断点）
  python tools/validate_fields_batch.py --region IND --fresh

  # 只看统计不写库
  python tools/validate_fields_batch.py --region IND --dry-run
"""
import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from api_client import Api, load_creds

PAGE = 50
DB = "data/wqb.db"
CHECKPOINT = "data/field_validation_checkpoint.json"


def _now():
    return datetime.now().isoformat(timespec="seconds")


def fetch_fields(api, dataset, region, universe, delay, limit=None):
    """分页拉取指定 dataset 在某区域上下文的全部字段。"""
    base = ("/data-fields?instrumentType=EQUITY&region={region}"
            "&delay={delay}&universe={universe}&dataset.id={ds}&limit={pg}").format(
                region=region, delay=delay, universe=universe, ds=dataset, pg=PAGE)
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


def get_region_config(cur, region):
    row = cur.execute(
        "SELECT universe_legal, delay_legal FROM regions WHERE name=?", (region,)).fetchone()
    if not row:
        raise ValueError(f"区域 {region} 不在 regions 表")
    universes = json.loads(row[0] or "[]")
    delays = json.loads(row[1] or "[1]")
    universe = universes[0] if universes else "TOP3000"
    delay = delays[0] if delays else 1
    return universe, delay


def get_datasets(cur, region, only=None, only_with_fields=False):
    q = """SELECT d.id, d.name FROM datasets d JOIN regions rg ON rg.id=d.region_id
           WHERE rg.name=? AND d.field_count>0"""
    params = [region]
    if only_with_fields:
        # 只处理 fields 表里真有字段记录的数据集(跳过 field_count 登记值但无记录的空壳)
        q += " AND d.id IN (SELECT DISTINCT dataset_id FROM fields)"
    if only:
        q += " AND d.name=?"
        params.append(only)
    return cur.execute(q + " ORDER BY d.field_count DESC", params).fetchall()


def load_checkpoint():
    if os.path.exists(CHECKPOINT):
        try:
            return json.load(open(CHECKPOINT, encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_checkpoint(ck):
    tmp = CHECKPOINT + ".tmp"
    json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(tmp, CHECKPOINT)


def validate_dataset(api, cur, conn, ds_id, ds_name, region, universe, delay,
                     dry_run, backfill=False):
    """验证单个数据集，返回 (n_platform, n_valid, n_invalid, n_backfilled)。

    关键：必须按 dataset_id 精确匹配本地字段（不能按 d.name），因为数据集名在
    多区域共享（如 model28 在 EUR/GBR/USA/IND 各有一份），按 name 会误标其他区域的字段。

    backfill=True 时：平台返回但本地 fields 表缺失的字段会直接插入并标 verified=1
    （用于 KOR/EUR 这类 fields 表从未灌入的区域，一步完成"灌字段+验证"）。
    """
    raw = fetch_fields(api, ds_name, region, universe, delay)
    platform = {f.get("id"): f for f in raw if f.get("id")}
    platform_ids = set(platform)
    context = f"{region}/{universe}/D{delay}"

    # 本地该数据集(精确 dataset_id)的全部字段
    local = cur.execute(
        "SELECT id, field_name FROM fields WHERE dataset_id=?",
        (ds_id,)).fetchall()
    local_names = {fname for _, fname in local}

    n_valid = n_invalid = 0
    for fid, fname in local:
        verified = 1 if fname in platform_ids else -1
        if verified == 1:
            n_valid += 1
        else:
            n_invalid += 1
        if not dry_run:
            cur.execute(
                """UPDATE fields SET verified=?, verified_context=?, verified_at=?
                   WHERE id=?""",
                (verified, context, _now(), fid))

    # backfill: 平台有但本地缺失的字段插入 fields 表
    n_backfilled = 0
    if backfill:
        for fname in platform_ids - local_names:
            meta = platform[fname]
            if not dry_run:
                cur.execute(
                    """INSERT INTO fields
                       (dataset_id, field_name, field_type, coverage,
                        user_count, alpha_count, description,
                        verified, verified_context, verified_at)
                       VALUES (?,?,?,?,?,?,?,1,?,?)""",
                    (ds_id, fname, meta.get("type"), meta.get("coverage"),
                     meta.get("userCount"), meta.get("alphaCount"),
                     (meta.get("description") or "")[:500],
                     context, _now()))
            n_backfilled += 1
            n_valid += 1

    if not dry_run:
        conn.commit()
    return len(platform_ids), n_valid, n_invalid, n_backfilled


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True)
    ap.add_argument("--dataset", default=None, help="只验单个数据集（探针）")
    ap.add_argument("--fresh", action="store_true", help="忽略断点强制重验")
    ap.add_argument("--dry-run", action="store_true", help="只统计不写库")
    ap.add_argument("--db", default=DB)
    ap.add_argument("--sleep", type=float, default=1.0, help="数据集间隔秒数(防限流)")
    ap.add_argument("--universe", default=None, help="覆盖 regions 表推断的 universe")
    ap.add_argument("--delay", type=int, default=None, help="覆盖 regions 表推断的 delay")
    ap.add_argument("--backfill", action="store_true",
                    help="平台有但本地 fields 表缺失的字段直接插入并标 verified=1 (灌字段+验证一步完成)")
    ap.add_argument("--only-with-fields", action="store_true",
                    help="只处理 fields 表里有字段记录的数据集(跳过空壳, 适合 GBR 这种大量登记空壳的区域)")
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    universe, delay = get_region_config(cur, args.region)
    if args.universe:
        universe = args.universe
    if args.delay is not None:
        delay = args.delay
    datasets = get_datasets(cur, args.region, args.dataset, args.only_with_fields)
    if not datasets:
        print(f"区域 {args.region} 无真实数据集(field_count>0)")
        return

    # 断点：已验证且 context 匹配的数据集跳过
    context = f"{args.region}/{universe}/D{delay}"
    ck = {} if args.fresh else load_checkpoint()
    done = set(ck.get(context, []))

    print(f"区域={args.region} universe={universe} delay={delay} context={context}")
    print(f"待验数据集={len(datasets)}  已完成(断点)={len(done)}  dry_run={args.dry_run}  backfill={args.backfill}\n")

    api = Api()
    email, pw = load_creds()
    api.login(email, pw)
    print("[AUTH] OK\n")

    tot_platform = tot_valid = tot_invalid = tot_backfilled = 0
    newly_done = []
    for i, (ds_id, ds_name) in enumerate(datasets, 1):
        if ds_name in done and not args.fresh:
            print(f"[{i}/{len(datasets)}] SKIP {ds_name} (已验证)")
            continue
        try:
            n_plat, n_valid, n_invalid, n_bf = validate_dataset(
                api, cur, conn, ds_id, ds_name, args.region, universe, delay,
                args.dry_run, args.backfill)
            tot_platform += n_plat
            tot_valid += n_valid
            tot_invalid += n_invalid
            tot_backfilled += n_bf
            newly_done.append(ds_name)
            status = "DRY" if args.dry_run else "OK"
            bf = f"  回填={n_bf:>4}" if args.backfill else ""
            print(f"[{i}/{len(datasets)}] {status} {ds_name:16s} "
                  f"平台字段={n_plat:>4}  本地可用={n_valid:>4}  不可用={n_invalid:>4}{bf}")
            # 更新断点
            if not args.dry_run:
                ck.setdefault(context, [])
                if ds_name not in ck[context]:
                    ck[context].append(ds_name)
                save_checkpoint(ck)
            time.sleep(args.sleep)
        except Exception as e:
            print(f"[{i}/{len(datasets)}] ERROR {ds_name}: {e}")
            time.sleep(args.sleep * 2)

    print(f"\n=== 汇总 ===")
    print(f"平台返回字段总数={tot_platform}  本地可用={tot_valid}  不可用={tot_invalid}  回填={tot_backfilled}")
    if not args.dry_run:
        print(f"断点已更新: {CHECKPOINT} (context={context}, 已完成 {len(done)+len(newly_done)} 个数据集)")
    conn.close()


if __name__ == "__main__":
    main()
