#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发批前硬闸：算子语法 + **字段存在性**（本工作区 `op_arity` 只查算子，字段笔误会静默 DROP）。

教训来源：2026-10-05 wave320 的 P5 因 `qa_vader_neg`（漏了 `ceo_`）而被平台返回
`NO_ALPHA_ID status=ERROR`，白跑一条。见 `.workbuddy/memory/2026-10-04.md §65.3`。

用法::

    python tracking/EUR/scripts/check_wave_fields.py tracking/EUR/candidates/eur_wave321_news_items.json --region EUR
    # 跨数据集：自动把候选里出现的所有 `<prefix>_...` 标识符按 region 全量字段并集校验
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from wqb.expression.op_arity import check_expressions_strict, format_report  # noqa: E402
from wqb.region_catalog import RegionCatalog  # noqa: E402

# 非字段标识符白名单（算子/分组/关键字）
NON_FIELDS = {
    "rank", "group_rank", "group_zscore", "group_neutralize", "zscore", "normalize", "scale",
    "quantile", "winsorize", "signed_power", "hump", "reverse", "subtract", "add", "divide",
    "multiply", "vector_neut", "vec_avg", "vec_sum", "vec_max", "vec_min", "ts_mean", "ts_sum",
    "ts_delta", "ts_corr", "ts_rank", "ts_zscore", "ts_std_dev", "ts_decay_linear", "ts_backfill",
    "trade_when", "if_else", "greater", "less", "and", "or", "not", "abs", "sign", "log", "sqrt",
    "industry", "subindustry", "sector", "country", "market", "std", "driver", "hump", "dense",
    "lookback", "k", "constant", "nan", "rettype",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("items_path")
    ap.add_argument("--region", default="EUR")
    ap.add_argument("--strict", action="store_true", help="字段缺失即返回非 0")
    args = ap.parse_args()

    items = json.load(open(args.items_path, encoding="utf-8"))
    codes = [it["code"] for it in items]
    print(format_report(check_expressions_strict(codes)))

    rc = RegionCatalog()
    # 该 region 全量字段并集（跨数据集）
    all_fields = set()
    names = rc.dataset_names(args.region)          # ← 正确接口（`datasets()` 不存在）
    for name in names:
        try:
            all_fields |= set(rc.field_names(name, args.region))
        except Exception:
            pass
    print(f"[i] region={args.region} 数据集 {len(names)} 个 / 字段并集 = {len(all_fields)}")
    if not all_fields:
        # ★ 关键：并集为空说明取字段失败 —— 必须报错，绝不能静默放行（假绿灯）
        print("[x] 字段并集为空，无法校验 —— 拒绝放行（检查 region 名与本地区 catalog）")
        return 2

    bad = []
    for it in items:
        for tok in set(re.findall(r"\b([a-z][a-z0-9_]{4,})\b", it["code"])):
            if tok in NON_FIELDS:
                continue
            if all_fields and tok not in all_fields:
                bad.append((it.get("note", "")[:26], tok))
    if bad:
        print("[x] 疑似字段名错误（区域字段并集中不存在）：")
        for note, tok in bad:
            print(f"    - {tok:52s}  <- {note}")
        return 1 if args.strict else 0
    print("[ok] 所有标识符均能在区域字段并集中找到")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
