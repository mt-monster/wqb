#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 wqb.db fields 表生成降级版体检包（P1-4 HKG 解锁，2026-09-07）。

背景：HKG 无 WebDataScope 数据包（zip 内 9 区域组合无 HKG），
field_profile 表 HKG 0 行 → 完整体检包（含 skew/kurt/shape）不可得。
但 HKG fields 表自带 coverage（25648 字段，8298 个 ≥0.85）——
足以构建**降级版体检包**：只执行 coverage 硬门（低覆盖 cr<0.4
必须 ts_backfill），skew/kurt/shape 维度缺省不查。

field_inspect_gate 的三态设计天然支持这种包：
  - coverage_ratio 有值 → 低覆盖闸生效
  - skewness/kurtosis 为 None → 高偏度/厚尾闸跳过（不误报）
  - distribution_shape 缺省 → 稀疏事件闸跳过

用法：
    python tools/gen_inspect_from_db.py --region HKG            # 全部数据集
    python tools/gen_inspect_from_db.py --region HKG --dataset news18
    python tools/gen_inspect_from_db.py --region HKG --dry-run  # 只列出将生成什么
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(REPO_ROOT, "data", "wqb.db")
OUT_DIR = os.path.join(REPO_ROOT, "tracking", "mining")


def build_pack(region: str, dataset: str, conn: sqlite3.Connection) -> dict:
    """从 fields 表构建单数据集降级体检包。"""
    rows = conn.execute(
        """SELECT f.field_name, f.coverage, f.field_type, f.description
           FROM fields f JOIN datasets d ON f.dataset_id = d.id
           JOIN regions r ON d.region_id = r.id
           WHERE r.name = ? AND d.name = ?""",
        (region, dataset),
    ).fetchall()
    if not rows:
        return {}

    fields_inner = {}
    for name, cov, ftype, desc in rows:
        cov_val = float(cov) if cov is not None else None
        advices = []
        if cov_val is not None and cov_val < 0.4:
            advices.append(
                f"低覆盖({cov_val:.2f}<0.4) → 必须含 ts_backfill(x, N)")
        elif cov_val is not None and cov_val < 0.6:
            advices.append(
                f"中低覆盖({cov_val:.2f}) → 建议 ts_backfill + 短窗慎用")
        fields_inner[name] = {
            "field": name,
            "metadata": {
                "coverage_ratio": cov_val,
                # 降级包不携带：field_inspect_gate 遇 None 自动跳过对应闸
                "skewness": None,
                "kurtosis": None,
                "frequency": None,
                "distribution_shape": None,
            },
            "advices": advices,
            "_degraded": True,  # 标记降级来源，区分完整包
        }
    return {
        "region_delay": f"{region}/D1",
        "neutralization": None,
        "delay": 1,
        "source": "wqb.db fields (degraded: coverage-only)",
        "fields": {dataset: fields_inner},
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="从 DB fields 表生成降级版体检包")
    ap.add_argument("--region", required=True)
    ap.add_argument("--dataset", default=None, help="只生成指定数据集（默认全部）")
    ap.add_argument("--min-fields", type=int, default=5,
                    help="字段数低于此值的数据集跳过（默认 5）")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    conn = sqlite3.connect(DB_PATH)
    if a.dataset:
        datasets = [a.dataset]
    else:
        datasets = [
            r[0] for r in conn.execute(
                """SELECT d.name FROM datasets d
                   JOIN regions r ON d.region_id = r.id
                   WHERE r.name = ? ORDER BY d.name""",
                (a.region,),
            ).fetchall()
        ]

    n_gen = n_skip = 0
    for ds in datasets:
        existing = os.path.join(
            OUT_DIR, f"field_inspect_{a.region.lower()}_{ds}.json")
        if os.path.isfile(existing):
            # 已有完整包（WebDataScope 来源）不覆盖
            n_skip += 1
            continue
        pack = build_pack(a.region, ds, conn)
        if not pack or len(pack["fields"][ds]) < a.min_fields:
            n_skip += 1
            continue
        if a.dry_run:
            print(f"  [dry] {a.region}/{ds}: {len(pack['fields'][ds])} 字段")
            n_gen += 1
            continue
        out = os.path.join(
            OUT_DIR, f"field_inspect_{a.region.lower()}_{ds}.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(pack, f, ensure_ascii=False)
        n_gen += 1
    conn.close()

    verb = "将生成" if a.dry_run else "已生成"
    print(f"[db-pack] {verb} {n_gen} 个降级体检包（跳过 {n_skip}：已有完整包或字段不足）"
          f" → {OUT_DIR}")


if __name__ == "__main__":
    main()
