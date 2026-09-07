#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""体检→表达式硬门（S2→S3 第二道硬门）的可执行接线。

背景（2026-09-06 审计）：`wq-brain-ra-pipeline` 步 5 把
`check_batch → check_expr_against_inspect → wave_gate` 写成"回测前必过"的双硬门，
但 `check_expr_against_inspect` 在整个可执行路径上**零调用方** —— 函数躺在
`tools/webdata_quality.py:327`，没有任何脚本调它；它需要的体检数据包
（`tracking/mining/field_inspect_<region>_<dataset>.json`）现存两份且 `fields`
全为空。于是这道闸只存在于散文里：低覆盖字段没被强制 `ts_backfill`、厚尾没被强制
`rank/winsorize`、稀疏事件没被强制 `trade_when` —— 而这些正是 CONCENTRATED_WEIGHT
与 OS 衰减的结构性来源，本该在花掉仿真槽位之前就拦下。

本模块负责把它接进 `tools/wave_gate.py`。设计上区分三种状态，
**绝不把"没有数据"伪装成"检查通过"**：

  enforced   —— 找到体检包且覆盖了表达式用到的字段：逐条校验，违规即 FAIL
  partial    —— 找到体检包但部分字段无体检记录：已覆盖的照查，未覆盖的列出来
  unavailable—— 没有体检包：不阻断，但明确报告"本闸未生效"并给出生成命令

用法（库）：
    from field_inspect_gate import check_expressions
    report = check_expressions(exprs, region="USA", dataset="model267")

用法（CLI 自查）：
    python tools/field_inspect_gate.py --region USA --dataset model267 \
        --expr "rank(ts_backfill(fnd6_x, 120))"
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, Iterable, List, Optional

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSPECT_DIR = os.path.join(REPO_ROOT, "tracking", "mining")

#: 体检包命名：field_inspect_<region 小写>_<dataset>.json
#: （与 wq-brain-ra-pipeline 步 5 正文一致；历史文档里的
#: `tracking/field_inspect_<region>.json` 是旧写法，已不存在这样的文件）
_PACK_TEMPLATE = "field_inspect_{region}_{dataset}.json"

_IDENT_RE = re.compile(r"\b([a-z_][a-z0-9_]*)\b")
#: 表达式里出现的算子名不是字段名，靠"后面跟左括号"排除
_CALL_RE = re.compile(r"\b([a-z_][a-z0-9_]*)\s*\(")
#: 具名参数（`winsorize(x, std=4)` 的 std）也不是字段
_KWARG_RE = re.compile(r"\b([a-z_][a-z0-9_]*)\s*=")
#: 分组变量/常量等保留字，永远不是数据字段
_RESERVED = {
    "true", "false", "nan", "industry", "subindustry", "sector", "market",
    "country", "exchange", "and", "or", "not",
}


def pack_path(region: str, dataset: str) -> str:
    return os.path.join(
        INSPECT_DIR,
        _PACK_TEMPLATE.format(region=region.strip().lower(), dataset=dataset.strip()),
    )


def load_pack(region: str, dataset: str) -> Optional[Dict[str, Any]]:
    """读体检包；不存在或 fields 为空返回 None（视作"无数据"）。"""
    path = pack_path(region, dataset)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None

    # 展平 {"fields": {"<ds>": {"<field>": entry}}} → {"<field>": entry}
    flat: Dict[str, Any] = {}
    for _ds, fields in (data.get("fields") or {}).items():
        if isinstance(fields, dict):
            flat.update(fields)
    if not flat:
        return None
    return flat


def expression_fields(expr: str) -> List[str]:
    """粗提表达式里的字段名。

    所有标识符减去：函数调用名、具名参数名（`winsorize(x, std=4)` 的 std）、
    分组变量与常量保留字。
    """
    called = set(_CALL_RE.findall(expr))
    kwargs = set(_KWARG_RE.findall(expr))
    idents = set(_IDENT_RE.findall(expr))
    return sorted(idents - called - kwargs - _RESERVED)


def _load_checker():
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    from webdata_quality import check_expr_against_inspect  # noqa
    return check_expr_against_inspect


def check_expressions(
    expressions: Iterable[str],
    region: str,
    dataset: str,
) -> Dict[str, Any]:
    """对一批表达式跑体检硬门。

    返回 {status, enforced, violations, uncovered_fields, hint, ...}。
    status ∈ {"enforced", "partial", "unavailable"}；只有出现 violations 时
    才应当阻断 —— "没有体检数据" 不是拒绝理由，但必须被看见。
    """
    expressions = list(expressions)
    report: Dict[str, Any] = {
        "gate": "field_inspect",
        "region": region,
        "dataset": dataset,
        "total_expressions": len(expressions),
        "violations": [],
        "uncovered_fields": [],
        "checked_expressions": 0,
    }

    pack = load_pack(region, dataset)
    if pack is None:
        report["status"] = "unavailable"
        report["enforced"] = False
        report["hint"] = (
            f"体检包缺失或为空：{pack_path(region, dataset)}。"
            f"生成命令：python tools/webdata_quality.py --zip <WebDataScope数据包> "
            f"--export-expr {pack_path(region, dataset)}。"
            f"在此之前本闸不生效（低覆盖/厚尾/稀疏事件的预处理约束无人把关）。"
        )
        return report

    try:
        checker = _load_checker()
    except Exception as e:
        report["status"] = "unavailable"
        report["enforced"] = False
        report["hint"] = f"无法加载 check_expr_against_inspect：{e}"
        return report

    uncovered: set = set()
    checked = 0
    for expr in expressions:
        fields = expression_fields(expr)
        hit = [f for f in fields if f in pack]
        uncovered.update(f for f in fields if f not in pack)
        if not hit:
            continue
        checked += 1
        for field in hit:
            try:
                verdict = checker(expr, pack[field])
            except Exception as e:  # 单字段体检数据损坏不拖垮整批
                report.setdefault("errors", []).append(
                    {"expression": expr, "field": field, "error": str(e)}
                )
                continue
            if not verdict.get("ok", True):
                report["violations"].append({
                    "expression": expr,
                    "field": field,
                    "violations": verdict.get("violations", []),
                })

    report["checked_expressions"] = checked
    report["uncovered_fields"] = sorted(uncovered)
    report["enforced"] = True
    report["status"] = "partial" if uncovered else "enforced"
    if uncovered:
        report["hint"] = (
            f"{len(uncovered)} 个字段无体检记录，这些字段上的预处理约束未被校验："
            f"{sorted(uncovered)[:10]}"
        )
    return report


def format_report(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    status = report.get("status")
    if status == "unavailable":
        lines.append(f"[inspect] 体检硬门未生效（{report.get('region')}/{report.get('dataset')}）")
        lines.append(f"          {report.get('hint', '')}")
        return "\n".join(lines)

    n_v = len(report.get("violations", []))
    errors = report.get("errors", [])
    lines.append(
        f"[inspect] 体检硬门 {status}："
        f"校验 {report.get('checked_expressions')}/{report.get('total_expressions')} 条，"
        f"违规 {n_v} 条"
        + (f"，体检数据异常 {len(errors)} 处" if errors else "")
    )
    for v in report.get("violations", [])[:20]:
        lines.append(f"          FAIL {v['field']}: {'; '.join(v['violations'])}")
        lines.append(f"               {v['expression'][:110]}")
    # 体检记录残缺（缺 metadata 键等）必须可见 —— 否则"查不了"会被读成"查过了"
    for e in errors[:10]:
        lines.append(f"          SKIP {e['field']}: 体检记录不可用（{e['error']}）")
    if report.get("hint"):
        lines.append(f"          {report['hint']}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--region", required=True)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--expr", action="append", default=[], help="待校验表达式，可多次")
    ap.add_argument("--exprs-file", help="每行一条表达式的 txt")
    a = ap.parse_args()

    exprs = list(a.expr)
    if a.exprs_file:
        with open(a.exprs_file, "r", encoding="utf-8") as f:
            exprs.extend(line.strip() for line in f if line.strip())
    if not exprs:
        print("未提供表达式（--expr / --exprs-file）", file=sys.stderr)
        return 2

    report = check_expressions(exprs, a.region, a.dataset)
    print(format_report(report))
    return 1 if report.get("violations") else 0


if __name__ == "__main__":
    raise SystemExit(main())
