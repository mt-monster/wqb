#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""梯度回测完备性闸——「梯度回测必做」的机械守卫（2026-11-21 用户指令）。

## 为什么有这只工具

用户 2026-11-21 原话：「把梯度回测嵌入到回测的流程中必做」。
此前梯度纪律只写在文档里（原本还是「按需工具」），后果可查：
GBR institutions6 跑了 154 臂但全是多骨架横向扫描、没有一次严格单维梯度，
于是只能记 PROVISIONAL；而 institutions1 做了 91→16 变体的真梯度才出 S1.63 全闸件。
**没有任何机制检查「这个数据集到底跑没跑过梯度」——全靠 agent 自觉。**

本闸把 `wq-brain-ra-pipeline` 步 7「梯度回测（必做）」+ `references/step7-diagnose.md` §7.10
的三道验收落成机械判据。它不判信号好坏，只判「梯度痕迹在不在」。

## 判据（三道，全部满足 = GRADIENT_DONE）

1. **骨架变体厚度**：`expressions` 表按 `skeleton` 分组，**最大骨架的变体数 ≥ --min-variants**
   （缺省 3）——单点试错（每个骨架只 1 条）不算梯度。
2. **层数**：有 ≥2 个变体的**不同骨架数 ≥ --min-layers**（缺省 2）——近似「至少两层」
   （内层信号→外层包装；语义层级无法自动判定，用骨架多样性作代理）。
3. **留痕**：`tracking/<R>/waves/*_gradient_<dataset>.md` Δ 表档案存在
   （`--require-archive` 开启时；缺省开）。

> 判 PARTIAL / MISSING 都 exit 2：**未完成梯度的数据集，「天花板 / 判死」只能记 PROVISIONAL**
> （见 SOP）。脚本只读，零平台 API。

## 用法

    # 单个数据集
    python tools/gates/gradient_gate.py --region GBR --dataset institutions1 --field-prefix inst1_
    # 全库已测数据集批量
    python tools/gates/gradient_gate.py --region GBR --all
    # 只判厚度不要求档案（早期数据集）
    python tools/gates/gradient_gate.py --region GBR --dataset institutions6 --require-archive off

退出码：0 = GRADIENT_DONE；2 = PARTIAL / MISSING（未完成梯度）；1 = 参数 / DB 错误。
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = REPO_ROOT / "data" / "wqb.db"
_SRC = REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


def _connect_ro(db_path: Path) -> sqlite3.Connection:
    """只读连接：统一走 wqb.db_conn.connect(readonly=True)（规范：只读工具必须传 True）。"""
    if not db_path.exists():
        raise FileNotFoundError(f"DB not found: {db_path}")
    from wqb.db_conn import connect as _wqb_connect  # 规范只读入口
    return _wqb_connect(str(db_path), readonly=True, row_factory=sqlite3.Row)


def _resolve_matching(con: sqlite3.Connection, region: str, dataset: str,
                      field_prefix: Optional[str]) -> Tuple[str, str]:
    """返回 (匹配 SQL 条件, 匹配口径说明)。优先级 dataset 列 → field 前缀。"""
    has_expr = con.execute(
        "select name from sqlite_master where type='table' and name='expressions'"
    ).fetchone()
    if has_expr:
        n = con.execute(
            "select count(*) from expressions where region=? and dataset=?",
            (region, dataset),
        ).fetchone()[0]
        if n:
            return "region=? and dataset=?", f"expressions.dataset={dataset}"
    if field_prefix:
        return "region=? and expression like ?", f"expression LIKE %{field_prefix}%"
    raise SystemExit(
        f"[gradient_gate] {region}/{dataset}: expressions.dataset 无行且未给 --field-prefix；"
        "无法定位该集的回测记录（exit 1）"
    )


def _archive_layers(archive_path: Path, min_rows_per_layer: int = 3):
    """解析档案：返回 (完成的层数, 单层最大表格数据行数)。"""
    """从梯度档案解析「完成的层数」：`## Layer N` 标题 + 该段内表格数据行 ≥ min_rows_per_layer。

    机械可查的是**流程留痕**：梯度是流程动作（每层一批 Δ 表），
    DB 的骨架分组无法区分「同层横向替换」与「纵向下层」，故层数从档案读。
    空壳层（表头/分隔行/占位「待收」）不计。
    """
    import re
    try:
        text = archive_path.read_text(encoding="utf-8")
    except OSError:
        return 0
    lines = text.splitlines()
    layer_idx = [i for i, ln in enumerate(lines)
                 if re.match(r"^#{2,4}\s*Layer\s*\d+", ln)]
    if not layer_idx:
        return 0
    done = 0
    max_rows = 0
    for k, start in enumerate(layer_idx):
        end = layer_idx[k + 1] if k + 1 < len(layer_idx) else len(lines)
        rows = 0                 # 第一张表的数据行（含表头，表头 + N 数据 ⇒ rows = N+1）
        first_table_closed = False
        for ln in lines[start:end]:
            if not ln.strip().startswith("|"):
                if rows > 0:
                    first_table_closed = True   # 第一张表结束，后面的表（如排除清单）不计
                continue
            if first_table_closed:
                break
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells if c):
                continue  # 分隔行
            if any("待收" in c or "TODO" in c or "TBD" in c for c in cells):
                continue  # 占位行（未收割）
            rows += 1
        # rows = 表头(1) + 数据行；需 ≥ min_rows_per_layer 个数据行
        max_rows = max(max_rows, rows - 1)
        if rows - 1 >= min_rows_per_layer:
            done += 1
    return done, max_rows


def inspect_dataset(con: sqlite3.Connection, region: str, dataset: str,
                    field_prefix: Optional[str], min_variants: int,
                    min_layers: int, require_archive: bool,
                    archive_root: Optional[Path] = None) -> Dict:
    cond, how = _resolve_matching(con, region, dataset, field_prefix)
    params: List = [region]
    if "dataset=?" in cond:
        params.append(dataset)
    elif "like" in cond:
        params.append(f"%{field_prefix}%")

    rows = con.execute(
        f"select skeleton, count(*) n from expressions where {cond} "
        "and skeleton is not null and skeleton != '' group by skeleton order by n desc",
        params,
    ).fetchall()
    dominant_n = rows[0]["n"] if rows else 0
    dominant_sk = (rows[0]["skeleton"] or "")[:90] if rows else ""
    layered = [r for r in rows if r["n"] >= 2]
    n_layered = len(layered)
    total = sum(r["n"] for r in rows)

    archive = None
    archive_layers = 0
    archive_max_rows = 0
    if require_archive:
        root = archive_root if archive_root is not None else (REPO_ROOT / "tracking")
        waves_dir = root / region / "waves"
        hits = sorted(waves_dir.glob(f"*_gradient_{dataset}*.md")) if waves_dir.exists() else []
        if hits:
            try:
                archive = str(hits[-1].relative_to(REPO_ROOT))
            except ValueError:
                archive = str(hits[-1])
            archive_layers, archive_max_rows = _archive_layers(hits[-1])

    checks = {
        # 厚度双源：DB 骨架主导变体数 或 档案单层最大数据行数（MCP 直跑臂未入库时以档案为准）
        "dominant_variants_ok": (dominant_n >= min_variants) or (archive_max_rows >= min_variants),
        # 层数：档案模式从 `## Layer N` 结构解析（流程留痕）；关档案时回退骨架多样性近似
        "layers_ok": (archive_layers >= min_layers) if require_archive else (n_layered >= min_layers),
        "archive_ok": (archive is not None) if require_archive else True,
    }
    if all(checks.values()):
        verdict = "GRADIENT_DONE"
    elif total == 0:
        verdict = "MISSING"
    else:
        verdict = "PARTIAL"

    return {
        "region": region,
        "dataset": dataset,
        "match_by": how,
        "expressions_total": total,
        "dominant_skeleton_variants": dominant_n,
        "dominant_skeleton": dominant_sk,
        "layered_skeletons": n_layered,
        "archive": archive,
        "archive_layers": archive_layers,
        "archive_max_rows": archive_max_rows,
        "checks": checks,
        "verdict": verdict,
    }


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="梯度回测完备性闸（必做项机械守卫，只读）",
        epilog="exit 0 = GRADIENT_DONE；exit 2 = PARTIAL/MISSING；exit 1 = 参数/DB 错误",
    )
    ap.add_argument("--region", required=True, help="区域，如 GBR")
    ap.add_argument("--dataset", help="数据集 id（--all 时忽略）")
    ap.add_argument("--field-prefix", help="可选：字段前缀（dataset 列无行时的回退匹配，如 inst1_）")
    ap.add_argument("--all", action="store_true", help="扫该区 expressions 里出现过的全部 dataset")
    ap.add_argument("--min-variants", type=int, default=3, help="最大骨架变体数下限（缺省 3）")
    ap.add_argument("--min-layers", type=int, default=2, help="有 ≥2 变体的骨架数下限（缺省 2）")
    ap.add_argument("--require-archive", choices=["on", "off"], default="on",
                    help="是否要求 Δ 表档案（缺省 on）")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="DB 路径（测试用）")
    ap.add_argument("--archive-root", default=None,
                    help="Δ 表档案根（缺省 <repo>/tracking；测试用）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args(argv)

    require_archive = args.require_archive == "on"
    try:
        con = _connect_ro(Path(args.db))
    except Exception as e:  # noqa: BLE001
        print(f"[gradient_gate] {e}", file=sys.stderr)
        return 1

    try:
        if args.all:
            ds_rows = con.execute(
                "select distinct dataset from expressions "
                "where region=? and dataset is not null and dataset != '' order by dataset",
                (args.region,),
            ).fetchall()
            datasets = [r["dataset"] for r in ds_rows]
            if not datasets:
                print(f"[gradient_gate] {args.region}: expressions.dataset 无任何行", file=sys.stderr)
                return 1
        else:
            if not args.dataset:
                print("[gradient_gate] 需 --dataset 或 --all", file=sys.stderr)
                return 1
            datasets = [args.dataset]

        results = []
        for ds in datasets:
            try:
                results.append(inspect_dataset(
                    con, args.region, ds, args.field_prefix,
                    args.min_variants, args.min_layers, require_archive,
                    Path(args.archive_root) if args.archive_root else None,
                ))
            except SystemExit:
                raise
            except Exception as e:  # noqa: BLE001
                print(f"[gradient_gate] {ds}: {e}", file=sys.stderr)
                return 1
    finally:
        con.close()

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        print(f"[gradient_gate] region={args.region} "
              f"min_variants={args.min_variants} min_layers={args.min_layers} "
              f"archive={'required' if require_archive else 'off'}")
        for r in results:
            c = r["checks"]
            flags = "".join([
                "V" if c["dominant_variants_ok"] else "v",
                "L" if c["layers_ok"] else "l",
                "A" if c["archive_ok"] else "a",
            ])
            print(f"  [{r['verdict']:<13}] {r['dataset']:<28} "
                  f"dom={r['dominant_skeleton_variants']:>3} layers={r['layered_skeletons']:>2} "
                  f"arc_layers={r['archive_layers']:>2} arc_rows={r['archive_max_rows']:>2} total={r['expressions_total']:>4} "
                  f"flags={flags} by={r['match_by']}")
            if r["dominant_skeleton"]:
                print(f"      dominant: {r['dominant_skeleton']}")
            if r["archive"]:
                print(f"      archive:  {r['archive']}")

    bad = [r for r in results if r["verdict"] != "GRADIENT_DONE"]
    if bad:
        print(f"[gradient_gate] NOT_DONE {len(bad)}/{len(results)} —— "
              "未完成梯度的数据集，「天花板/判死」只能记 PROVISIONAL", file=sys.stderr)
        return 2
    if args.json:
        print(f"[gradient_gate] all {len(results)} dataset(s) GRADIENT_DONE", file=sys.stderr)
    else:
        print(f"[gradient_gate] all {len(results)} dataset(s) GRADIENT_DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())