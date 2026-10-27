# -*- coding: utf-8 -*-
"""gem_pilot_sample.py — 从 GEM 已生成表达式池里分层抽样，用于「结构质量」打样回测。

背景（2026-10-24）：EUR 有 3515 条 GEM 表达式躺在 expressions 表里从未回测，
而 GEM 的结构维度比我方模板矩阵宽 8 个（subtract/bucket/group_neutralize/ts_std_dev/
trade_when/vector_neut/quantile/group_zscore）。本脚本按**结构层**分层抽样，
其中 `plain` 层作为**对照组**（最接近我方矩阵能力），其余层覆盖缺失维度。

用法：
    python tools/gem_pilot_sample.py                 # 默认 48 条分层抽样
    python tools/gem_pilot_sample.py --quota 20      # plain/subtract 各 20，其余按比例
    python tools/gem_pilot_sample.py --out cache/x.json
"""
import argparse
import collections
import json
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POOL = os.path.join(ROOT, "cache", "gem_eur_dedup.json")
DB = os.path.join(ROOT, "data", "wqb.db")

# 连接一律走规范工厂（只读：本脚本不写库）。
sys.path.insert(0, os.path.join(ROOT, "src"))
from wqb.db_conn import connect as db_connect  # noqa: E402

MISSING_OPS = ("subtract", "bucket", "group_neutralize", "ts_std_dev",
               "trade_when", "vector_neut", "quantile", "group_zscore")

_OP_PREFIX = ("ts_", "vec_", "group_", "if_", "tail", "bucket", "trade_", "signed_",
              "reverse", "quantile", "winsorize", "hump", "vector_", "regression_")
_OP_WORDS = {"rank", "add", "multiply", "divide", "subtract", "greater", "less",
             "and", "or", "not", "abs", "log", "exp", "sign", "min", "max", "sum",
             "std", "mean", "count", "scale", "power", "backfill", "delta", "decay",
             "ir", "zscore", "quantile"}


def stratum(e):
    """表达式 → 结构层标签（用到的、我方矩阵缺失的算子组合）。"""
    tags = []
    if "subtract(" in e:
        tags.append("subtract")
    if "bucket(" in e:
        tags.append("bucket")
    if "group_neutralize(" in e:
        tags.append("grpneut")
    if "ts_std_dev(" in e:
        tags.append("tsstd")
    if "trade_when(" in e:
        tags.append("tradewhen")
    if "vector_neut(" in e:
        tags.append("vecneut")
    if "quantile(" in e and "ts_quantile" not in e:
        tags.append("quantile")
    if "group_zscore(" in e:
        tags.append("grpzs")
    return "+".join(tags) if tags else "plain"


def field_ids(e):
    """粗提表达式里的候选字段 id（排除算子名）。"""
    ids = set(re.findall(r"(?<![a-z_])([a-z][a-z0-9_]*(?:_[a-z0-9]+){1,})(?![a-z0-9_]*\()", e))
    out = set()
    for i in ids:
        if i.startswith(_OP_PREFIX) or i in _OP_WORDS:
            continue
        out.add(i)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", default=POOL)
    ap.add_argument("--db", default=DB)
    ap.add_argument("--out", default=os.path.join(ROOT, "cache", "gem_pilot_sample.json"))
    ap.add_argument("--quota", type=int, default=10,
                    help="每个结构层的基础配额；plain/subtract 层取 2 倍")
    ap.add_argument("--top-strata", type=int, default=0,
                    help="只抽最大的 N 个结构层（0=全部）。打样用 6 ⇒ 约 48 条")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    random.seed(a.seed)

    pool = json.load(open(a.pool, encoding="utf-8"))
    by = collections.defaultdict(list)
    for x in pool:
        by[stratum(x["e"])].append(x)

    # 配额：plain（对照组）与 subtract（GEM 主力结构）各 2 倍，其余 1 倍
    keys = sorted(by, key=lambda x: -len(by[x]))
    if a.top_strata:
        keys = keys[:a.top_strata]
    sample = []
    for k in keys:
        q = a.quota * (2 if k in ("plain", "subtract") else 1)
        sample += random.sample(by[k], min(q, len(by[k])))

    con = db_connect(a.db, readonly=True)
    valid = {r[0] for r in con.execute(
        "SELECT f.field_name FROM fields f JOIN datasets d ON f.dataset_id=d.id "
        "JOIN regions g ON d.region_id=g.id WHERE g.name='EUR'")}

    ok, bad = [], []
    for x in sample:
        miss = [i for i in field_ids(x["e"]) if i not in valid]
        (bad if miss else ok).append((x, miss))

    print(f"池 {len(pool)} 条 / {len(by)} 个结构层")
    print(f"抽样 {len(sample)} 条 → 字段名校验通过 {len(ok)} / 失败 {len(bad)}")
    for x, m in bad[:8]:
        print(f"  x {x['ds']}: 缺字段 {m[:3]}")

    rows = [{"ds": x["ds"], "e": x["e"], "expo": x["expo"], "stratum": stratum(x["e"])}
            for x, _ in ok]
    json.dump(rows, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    cc = collections.Counter(r["stratum"] for r in rows)
    print(f"\n打样本 {len(rows)} 条，结构层分布：")
    for k, v in cc.most_common():
        print(f"  {k:28s} {v:>3}")
    print(f"\n对照组 plain = {cc.get('plain', 0)} 条；缺失维度合计 "
          f"{sum(v for k, v in cc.items() if k != 'plain')} 条")
    print(f"已存 {a.out}")


if __name__ == "__main__":
    main()
