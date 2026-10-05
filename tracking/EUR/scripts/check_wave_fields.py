#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发批前硬闸：算子语法 + **字段存在性** + **双维度清点报告**。

⚠ 本脚本曾于 2026-10-05 被外部清理进程删除两次（连同 run_wave_single_fanout.py），
   故逻辑与「发批前双维度清点」（见当日日志 §77/§79）合并重建于此，一次到位。

来源与教训：
- wave320 因`qa_vader_neg`（漏 `ceo_`）→ 平台NO_ALPHA_ID status=ERROR，白跑一条。
- wave327 因 `quantime`（漏 `l`）→ 同上。**两波内抓到两次** ⇒ 这道闸已从可选变必过。
- 第一版误用 `RegionCatalog.datasets()`（不存在）导致字段并集=0 却"全部通过"，
  **一个永远绿灯的闸比没有闸更危险** ⇒ 并集为空必须返回非 0。

用法::

    python tracking/<R>/scripts/check_wave_fields.py tracking/<R>/candidates/eur_waveNNN_items.json \
        --region EUR [--strict] [--cartesian]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from wqb.expression.op_arity import check_expressions_strict, format_report  # noqa: E402

# ★ `wqb.region_catalog` 源文件也已被清理进程删除（只剩 __pycache__ 的 .pyc，
#   2026-10-05 实测）⇒ 不能 import 它。改为直接读 `data/wqb.db` 的字段表。
#   字段并集只是"防字段名笔误"的兜底，权威来源始终是平台 `get_datafields`。
try:
    from wqb.db_conn import connect  # noqa: E402
    _HAVE_DB = True
except Exception:  # pragma: no cover
    _HAVE_DB = False

# 非字段标识符白名单（算子 / 分组 / 关键字）
NON_FIELDS = {
    "rank", "group_rank", "group_zscore", "group_neutralize", "group_backfill",
    "zscore", "normalize", "scale", "quantile", "winsorize", "signed_power",
    "hump", "reverse", "subtract", "add", "divide", "multiply", "power", "log",
    "ts_mean", "ts_sum", "ts_delta", "ts_corr", "ts_rank", "ts_zscore", "ts_std_dev",
    "ts_decay_linear", "ts_backfill", "ts_product", "ts_scale", "ts_argmin", "ts_argmax",
    "trade_when", "if_else", "greater", "less", "and", "or", "not", "abs", "sign", "sqrt",
    "vector_neut", "vec_avg", "vec_sum", "vec_max", "vec_min", "vec_count",
    "industry", "subindustry", "sector", "country", "market", "std", "driver",
    "dense", "lookback", "constant", "nan", "rettype", "bucket", "quintile",
    "one", "first", "last", "lastbutone", "mean", "regression", "rank_by_side",
    "group_cartesian_product", "group_mean", "group_sum", "group_count",
    "group_std_dev", "group_scale", "group_normalize", "group_percentage",
    "group_backfill", "group_neutralize", "group_zscore", "group_rank",
    "volume", "returns", "close", "open", "high", "low", "vwap", "adv20",
}


def build_field_union(region: str) -> set:
    """取该 region 全量字段名并集（跨数据集），直接查 `data/wqb.db`。

    ⚠ 原实现用 `wqb.region_catalog.RegionCatalog`，该模块 2026-10-05 已被清理进程删除
      （只剩 __pycache__ 的 .pyc；接口确认为 `dataset_names`/`field_names`，
      底层就是 sqlite3 + `db_conn.connect`）⇒ 这里直接查同一张库，行为等价。

    ★ 真实 schema（2026-10-05 实测，猜错会「永远红灯」）：
        `regions`(18 行)     id / name   ← name 才是 'EUR' 字符串
        `datasets`(1.9k 行)  id / name / **region_id(数字外键→regions.id)**
        `fields`(285k 行)    id / **dataset_id** / **field_name** / field_type / coverage …
      ⇒ 三段联表：`fields JOIN datasets ON dataset_id  JOIN regions ON region_id`，
        用 `regions.name = ?` 过滤。
        （前一版三处都猜错：拿 `id` 当字段名、用字符串比`region_id`、
          漏了 regions 联表 ⇒ 把真实存在的字段误报"不存在"，16 条全红。
          **闸报假警报和永远绿灯一样有害**。）
    ⚠ 顺带发现：`regions.universe_legal`(EUR) = TOP2500/TOPCS1600/TOP1200/TOP800/TOP400/
      ILLIQUID_MINVOL1M，**与平台 `get_platform_setting_options` 一致** ⇒ 可作 universe 合法性校验源。
    """
    if not _HAVE_DB:
        return set()
    try:
        con = connect()
        cur = con.cursor()
        rows = cur.execute(
            "SELECT DISTINCT f.field_name "
            "FROM fields f "
            "JOIN datasets d ON d.id = f.dataset_id "
            "JOIN regions r ON r.id = d.region_id "
            "WHERE r.name = ?", (region.upper(),)).fetchall()
        return {r[0] for r in rows if r and r[0]}
    except Exception:
        return set()


def check_items(items, all_fields, region):
    """逐条抽出标识符并对照字段并集。返回疑似笔误列表。"""
    bad = []
    for it in items:
        for tok in set(re.findall(r"\b([a-z][a-z0-9_]{4,})\b", it["code"])):
            if tok in NON_FIELDS:
                continue
            if all_fields and tok not in all_fields:
                bad.append((it.get("note", "")[:26], tok))
    return bad


def cartesian_report(region: str, dataset: str | None) -> None:
    """打印「该 region 字段 / universe / neut」的历史使用分布，辅助双维度清点。"""
    import glob
    from collections import Counter as C

    neut_c, univ_c = C(), C()
    total = 0
    for p in glob.glob(f"tracking/{region}/results/wave*_checkpoint.json"):
        try:
            d = json.load(open(p, encoding="utf-8")).get("results", [])
        except Exception:
            continue
        total += len(d)
        for r in d:
            if r.get("neut"):
                neut_c[r["neut"]] += 1
            if r.get("universe"):
                univ_c[r["universe"]] += 1
    print(f"[清点] {region} 历史 {total} 条变体")
    print(f"  universe: {dict(univ_c)}")
    print(f"  neut    : {dict(neut_c)}")
    if dataset:
        print(f"  （本波数据集 = {dataset}；字段笛卡尔积清点请对照 get_datafields 返回清单）")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("items_path")
    ap.add_argument("--region", default="EUR")
    ap.add_argument("--strict", action="store_true", help="字段缺失即返回非 0")
    ap.add_argument("--cartesian", action="store_true", help="附带打印设置档使用分布")
    ap.add_argument("--dataset", default=None, help="配合 --cartesian 标注数据集名")
    args = ap.parse_args()

    items = json.load(open(args.items_path, encoding="utf-8"))
    codes = [it["code"] for it in items]
    print(format_report(check_expressions_strict(codes)))

    # 自查：重复项（同 code + 同设置档）会白占槽位
    keys = Counter(
        (i["code"], i.get("decay"), i.get("truncation"), i.get("neut"),
         i.get("universe"), i.get("maxTrade"), i.get("nanHandling"), i.get("pasteurization"))
        for i in items
    )
    dups = [k for k, v in keys.items() if v > 1]
    if dups:
        print(f"[!] 检出 {len(dups)} 组重复(同表达式+同设置档)变体，将白占槽位：")
        for k in dups:
            print(f"    {k[0][:50]}  decay={k[1]} neut={k[3]}")
    else:
        print("[ok] 无重复(同表达式+同设置档)变体")

    all_fields = build_field_union(args.region)
    print(f"[i] region={args.region} 字段并集 = {len(all_fields)}")
    if not all_fields:
        #★ 永远绿灯的闸比没有闸更危险 —— 取不到字段必须拒放行
        print("[x] 字段并集为 0，无法校验字段名，拒绝放行（防止假绿灯）")
        return 2

    bad = check_items(items, all_fields, args.region)
    if bad:
        print("[x] 疑似字段名错误（区域字段并集中不存在）：")
        for note, tok in sorted(set(bad)):
            print(f"    - {tok:56s}  <- {note}")
        return 1 if args.strict else 0
    print("[ok] 所有标识符均能在区域字段并集中找到")

    if args.cartesian:
        cartesian_report(args.region, args.dataset)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
