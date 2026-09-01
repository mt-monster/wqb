# -*- coding: utf-8 -*-
"""populate_external_fields.py - 灌 external_fields 表。

扫描某区域全部 alpha 表达式，提取引用但**不在本区域 fields 表**的字段（外部/跨区/未灌字段），
写入 external_fields 表，标注：
  - in_local_db: 1=本地 fields 表存在(跨区共享, 如 mdl238_global_rank 在 EUR/USA) / 0=本地未灌(平台字段)
  - source_regions: 本地表里该字段实际归属的区域
  - use_count / first_seen_alpha

这些字段是 token-name 隐患的重灾区：在表达式里能跑，但本地 fields 表没有，用前必须确认。

用法：
  python tools/populate_external_fields.py --region IND
  python tools/populate_external_fields.py --region IND --dry-run
"""
import argparse
import json
import re
import sqlite3
from collections import defaultdict
from datetime import datetime

DB = "data/wqb.db"

# 已知运算符/关键字（非字段），避免误提取
OPS = set('''rank ts_rank zscore ts_zscore add subtract multiply divide power log sqrt abs sign
max min ts_max ts_min ts_arg_max ts_arg_min ts_sum ts_mean ts_stddev ts_skewness ts_kurtosis
delta delay decay_linear ts_corr ts_covariance winsorize truncate if_else and or not gt lt ge le eq ne
group_rank group_zscore group_neutralize group_mean scale normalize quantile vector_neut hump
signed_power ts_av_diff ts_backfill ts_irr ts_product ts_quantile ts_regression ts_returns ts_scale
kth_element last_diff_value clamp keep purge trade_when bucket filter_winsorize_days
vec_avg vec_sum vec_op vec_count vec_choose vec_norm vec_range vec_stddev vec_skew
ts_delta ts_std_dev ts_ir ts_back reverse ts_decay_linear greater less
industry sector subindustry country region market true false null nan
div0 e3 sh s ni1w ni1w0'''.split())

TOK = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')


def _now():
    return datetime.now().isoformat(timespec="seconds")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--db", default=DB)
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    # 本区域 fields 表已有字段
    local_fields = {r[0] for r in cur.execute(
        """SELECT f.field_name FROM fields f
           JOIN datasets d ON d.id=f.dataset_id JOIN regions rg ON rg.id=d.region_id
           WHERE rg.name=?""", (args.region,))}

    # 全库字段 -> 归属区域（判定跨区来源）
    field_regions = defaultdict(set)
    for name, rname in cur.execute(
        """SELECT f.field_name, rg.name FROM fields f
           JOIN datasets d ON d.id=f.dataset_id JOIN regions rg ON rg.id=d.region_id"""):
        field_regions[name].add(rname)

    # 本区域 alpha 表达式
    alphas = cur.execute(
        """SELECT a.alpha_id, a.expression FROM alphas a
           JOIN regions rg ON rg.id=a.region_id
           WHERE rg.name=? AND a.expression IS NOT NULL""", (args.region,)).fetchall()

    ext = {}  # field -> [count, first_alpha]
    for aid, expr in alphas:
        for t in set(TOK.findall(expr or "")):
            if t in OPS or t.isdigit() or t in local_fields:
                continue
            # 过滤纯数字尾巴/过短 token
            if len(t) < 3:
                continue
            if t not in ext:
                ext[t] = [0, aid]
            ext[t][0] += 1

    print(f"区域={args.region}  本地字段={len(local_fields)}  alpha数={len(alphas)}")
    print(f"外部/未灌字段={len(ext)}\n")

    n_insert = 0
    for fname, (cnt, first_aid) in sorted(ext.items(), key=lambda kv: -kv[1][0]):
        in_db = 1 if fname in field_regions else 0
        src = sorted(field_regions.get(fname, []))
        if args.dry_run:
            print(f"  {fname[:46]:48s} ×{cnt:<3} in_db={in_db} src={src}")
        else:
            cur.execute(
                """INSERT INTO external_fields
                   (field_name, region, source_regions, in_local_db, verified,
                    first_seen_alpha, use_count, created_at, updated_at)
                   VALUES (?,?,?,?,0,?,?,?,?)
                   ON CONFLICT(field_name, region) DO UPDATE SET
                     source_regions=excluded.source_regions,
                     in_local_db=excluded.in_local_db,
                     use_count=excluded.use_count,
                     updated_at=excluded.updated_at""",
                (fname, args.region, json.dumps(src), in_db, first_aid, cnt, _now(), _now()))
            n_insert += 1

    if not args.dry_run:
        conn.commit()
        print(f"已写入/更新 external_fields: {n_insert} 条")
        # 汇总
        for r in cur.execute(
            "SELECT in_local_db, COUNT(*) FROM external_fields WHERE region=? GROUP BY in_local_db",
            (args.region,)):
            tag = "跨区共享(本地有)" if r[0] == 1 else "平台字段(本地未灌)"
            print(f"  {tag}: {r[1]} 个")
    conn.close()


if __name__ == "__main__":
    main()
