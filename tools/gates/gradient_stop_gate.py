#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""梯度**止损**闸 —— 「什么时候该停止调参」的机械判据（2026-11-23 用户「三、优化空间 全部落地」裁定）。

## 为什么有这只工具（与既有三只工具的分工）

| 工具 | 回答的问题 |
|---|---|
| `gates/gradient_gate.py` | **梯度痕迹在不在**（骨架厚度 / 层数 / 留痕档案） |
| `research/gradient_coverage.py` | **每层还缺哪些臂**（覆盖率 / 缺臂计划 / 算子元数 lint） |
| **`gates/gradient_stop_gate.py`（本工具）** | **这个模板还值不值得继续投臂** + **派发前的三查** |

前两只管「做得够不够」，本工具管「该不该停」和「批能不能发」。

## 为什么需要「止损」（本轮 ~450 臂的实证）

同一批战役里反复出现「信息层天花板已到、却继续按五层梯度烧臂」：
- insiders N5/N6/N8 三个模板 L1 天花板 0.54 / 0.49 / 0.60，若按完整五层各 40 臂算，
  会白烧约 **90 臂**；实际每个只投 10 臂就停。
- 反向教训：risk60 T4 的 L1 极差高达 0.78（0.82→0.04），一路做到 L5 才拿到 RA-1 件
  ⇒ **极差大 = 还有信息可挖；极差小 = 已到顶**。

## 四道判据（可单独调用，也可 `--all`）

### D1 `--l1-range`：L1 极差止损闸
`max_S < --min-s(1.0)` **且** `(max_S − min_S) < --max-range(0.7)` ⇒ **STOP**：
该模板在本数据集上「信息量不足」，不再投 L2–L5（记数据点后转下一个机制）。
反向：`max_S ≥ 1.0` 或极差 ≥ 0.7 ⇒ **CONTINUE**。

### D2 `--to-band`：配置层先行（TO 带）
高换手档的 S 是「不可交易的假高」。判据：先把 `turnover` 压进 `--to-min/--to-max`
（缺省 5%/20%，即内部严线 `GATES_INTERNAL`）再读 S。
输出 `in_band` / `out_of_band` 两组的 best S，以及 `verdict = READY_TO_JUDGE`（有带内臂）
或 `TO_FIRST`（全在带外 ⇒ 先调 decay/平滑，不许据带外 S 下结论）。

### D3 `--three-point`：三点检测（可交付性预筛）
分别取 `best S` / `best F` / `best 2Y` 三个冠军；三者**同一条** ⇒ `COINCIDE`（可交）；
不重合 ⇒ `SWING`（存在跷跷板，**该模板不可交付**，不必再调参）。
实证：risk60 三个模板与 insiders 五个模板全部 SWING；只有 risk60 T4 一件 COINCIDE（RA-1）。

### D4 `--lint-expr`：派发前三查（零配额）
1. **裸常数 UNITS 坑**：`add(x, 0.0001)` / `subtract(x, 常数)` ⇒ 平台 UNITS WARNING，
   整批读数作废（本轮 10/10 臂全废一次）。防除零应直接 `divide`（NaN 交给 `nanHandling=ON`）。
2. **已标准化字段再 zscore**：`ts_zscore(directional_indicator, d)` 这类
   「字段本身已无量纲（0/±1 指示器）」再 zscore ⇒ 近似常数 ⇒ **TO 0.00 / S 0.00**（实测归零）。
3. **VECTOR 未降维**（需 `--field-types`）：VECTOR 字段裸用 ⇒ 平台
   `Operator ... does not support event inputs`，整批 8 臂 ERROR。

## 用法

    # 收批后判「还要不要继续这个模板」
    python tools/gates/gradient_stop_gate.py --metrics batch.json --all
    python tools/gates/gradient_stop_gate.py --metrics batch.json --l1-range --json
    # 三点检测单独跑
    python tools/gates/gradient_stop_gate.py --metrics batch.json --three-point
    # 派发前三查
    python tools/gates/gradient_stop_gate.py --lint-expr arms.txt
    python tools/gates/gradient_stop_gate.py --lint-expr arms.txt \
        --field-types fields.json --standardized directional_indicator,directional_indicator_2

`--metrics` 吃 `batch_get_alpha_metrics` 的原始返回（`{"results": [...]}`）或裸 list；
每项读 `sharpe` / `fitness` / `two_year_sharpe` / `turnover` / `sub_universe_sharpe` /
`failed_ra_count`，可选 `alpha_id` / `tag`。

## 退出码

    0 = 全部 CONTINUE / COINCIDE / READY_TO_JUDGE / 无 lint 问题
    2 = 命中 STOP / SWING / TO_FIRST / 有 lint 问题（闸未过）

只读、零平台 API、零 DB 写入。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional, Sequence, Tuple

# 让 `python tools/gates/gradient_stop_gate.py` 直跑时也能 import wqb（D5 用 prod_verdict）
_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

# ── D4 默认的「已标准化字段」（再 zscore 会塌缩）—— 可用 --standardized 覆盖/追加
DEFAULT_STANDARDIZED: Tuple[str, ...] = (
    "directional_indicator",
    "directional_indicator_2",
)

# 只对这几个算子检查「第二个位置参数是裸常数」
CONST_TRAP_OPS: Tuple[str, ...] = ("add", "subtract")

NUM_RE = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$")


# ────────────────────────── 表达式扫描（平衡括号） ──────────────────────────
def _find_calls(expr: str, names: Sequence[str]) -> List[Tuple[str, int, int]]:
    """返回 [(name, arg_start, arg_end)]，arg 区间为括号内文本。"""
    out: List[Tuple[str, int, int]] = []
    for m in re.finditer(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", expr):
        name = m.group(1)
        if name not in names:
            continue
        start = m.end()  # '(' 之后
        depth = 1
        i = start
        while i < len(expr) and depth:
            ch = expr[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            i += 1
        if depth == 0:
            out.append((name, start, i - 1))
    return out


def _split_args(arg_text: str) -> List[str]:
    """按顶层逗号切分参数（忽略嵌套括号内的逗号）。"""
    parts: List[str] = []
    depth = 0
    cur: List[str] = []
    for ch in arg_text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    tail = "".join(cur).strip()
    if tail:
        parts.append(tail)
    return parts


def lint_expression(
    expr: str,
    standardized: Sequence[str] = DEFAULT_STANDARDIZED,
    field_types: Optional[Dict[str, str]] = None,
) -> List[Dict[str, str]]:
    """派发前三查。返回 issue 列表（空 = 通过）。"""
    issues: List[Dict[str, str]] = []

    # 1) 裸常数 UNITS 坑
    for name, s, e in _find_calls(expr, CONST_TRAP_OPS):
        for arg in _split_args(expr[s:e]):
            if NUM_RE.match(arg):
                issues.append(
                    {
                        "code": "BARE_CONSTANT_UNITS",
                        "detail": (
                            f"{name}(..., {arg}) 含裸常数 ⇒ 平台会报 "
                            "Incompatible unit for input ⇒ 整批读数作废。"
                            "防除零请直接用 divide(x, y)（NaN 交给 nanHandling=ON），"
                            "或用字段对字段的 greater(total, avg) 代替 > 1。"
                        ),
                    }
                )
                break

    # 2) 已标准化字段再 zscore
    for _name, s, e in _find_calls(expr, ("ts_zscore",)):
        args = _split_args(expr[s:e])
        if not args:
            continue
        head = args[0]
        for fld in standardized:
            if re.search(rf"\b{re.escape(fld)}\b", head):
                issues.append(
                    {
                        "code": "ZSCORE_ON_STANDARDIZED",
                        "detail": (
                            f"ts_zscore({fld}, ...) —— 该字段本身已无量纲（0/±1 型指示器），"
                            "再 zscore 会近似常数 ⇒ 实测 TO 0.00 / S 0.00。改用它本身的 rank 或直接比较。"
                        ),
                    }
                )
                break

    # 3) VECTOR 未降维（需要字段类型表）
    if field_types:
        vec_fields = [f for f, t in field_types.items() if str(t).upper() == "VECTOR"]
        for fld in vec_fields:
            for m in re.finditer(rf"\b{re.escape(fld)}\b", expr):
                before = expr[max(0, m.start() - 30) : m.start()]
                if re.search(r"\bvec_[a-z_]+\s*\(\s*$", before):
                    continue  # 已包 vec_*
                issues.append(
                    {
                        "code": "VECTOR_NOT_REDUCED",
                        "detail": (
                            f"{fld} 是 VECTOR，裸用会使平台报 "
                            "`Operator ... does not support event inputs`（整批 ERROR）。先包 vec_avg/vec_sum。"
                        ),
                    }
                )
                break

    return issues


# ────────────────────────── 指标侧判据 ──────────────────────────
def _load_metrics(path: str) -> List[dict]:
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    if isinstance(raw, dict):
        rows = raw.get("results") or raw.get("alphas") or raw.get("rows") or []
    elif isinstance(raw, list):
        rows = raw
    else:
        rows = []
    out = []
    for i, r in enumerate(rows):
        if not isinstance(r, dict) or r.get("error"):
            continue
        out.append(
            {
                "idx": i,
                "label": r.get("alpha_id") or r.get("id") or r.get("tag") or f"#{i}",
                "S": r.get("sharpe"),
                "F": r.get("fitness"),
                "Y2": r.get("two_year_sharpe"),
                "TO": r.get("turnover"),
                "sub": r.get("sub_universe_sharpe"),
                "RA": r.get("failed_ra_count"),
            }
        )
    return out


def _num(v) -> Optional[float]:
    return float(v) if isinstance(v, (int, float)) else None


def judge_l1_range(
    rows: List[dict], min_s: float = 1.0, max_range: float = 0.7
) -> dict:
    vals = [(r["label"], _num(r["S"])) for r in rows]
    vals = [(l, v) for l, v in vals if v is not None]
    if not vals:
        return {"check": "l1_range", "verdict": "NO_DATA", "detail": "没有可用的 sharpe 读数"}
    hi = max(vals, key=lambda x: x[1])
    lo = min(vals, key=lambda x: x[1])
    rng = hi[1] - lo[1]
    stop = (hi[1] < min_s) and (rng < max_range)
    return {
        "check": "l1_range",
        "verdict": "STOP" if stop else "CONTINUE",
        "max_S": round(hi[1], 4),
        "max_by": hi[0],
        "min_S": round(lo[1], 4),
        "min_by": lo[0],
        "range": round(rng, 4),
        "criteria": {"min_s": min_s, "max_range": max_range},
        "detail": (
            "max_S < 1.0 且极差 < 0.7 ⇒ 该模板信息量不足，不投 L2–L5（转下一个机制）"
            if stop
            else "仍有信息可挖（max_S ≥ 1.0 或极差 ≥ 0.7）⇒ 继续梯度"
        ),
    }


def judge_to_band(
    rows: List[dict], to_min: float = 0.05, to_max: float = 0.20
) -> dict:
    inb, out = [], []
    for r in rows:
        to, s = _num(r["TO"]), _num(r["S"])
        if to is None or s is None:
            continue
        rec = {"label": r["label"], "S": round(s, 4), "TO": round(to, 4)}
        (inb if to_min <= to <= to_max else out).append(rec)
    best_in = max(inb, key=lambda x: x["S"]) if inb else None
    best_out = max(out, key=lambda x: x["S"]) if out else None
    verdict = "READY_TO_JUDGE" if inb else ("TO_FIRST" if out else "NO_DATA")
    return {
        "check": "to_band",
        "verdict": verdict,
        "band": [to_min, to_max],
        "in_band": inb,
        "best_in_band": best_in,
        "best_out_of_band": best_out,
        "detail": (
            "有带内臂 ⇒ 可以据带内 S 下结论"
            if verdict == "READY_TO_JUDGE"
            else "全部臂的 TO 都在带外 ⇒ 先调 decay/平滑把换手压进带内，不许据带外 S 下结论"
            if verdict == "TO_FIRST"
            else "没有同时具备 S 与 TO 的臂"
        ),
    }


def judge_three_point(rows: List[dict]) -> dict:
    s_rows = [r for r in rows if _num(r["S"]) is not None]
    if not s_rows:
        return {"check": "three_point", "verdict": "NO_DATA"}
    bS = max(s_rows, key=lambda r: _num(r["S"]))
    f_rows = [r for r in rows if _num(r["F"]) is not None]
    bF = max(f_rows, key=lambda r: _num(r["F"])) if f_rows else None
    y_rows = [r for r in rows if _num(r["Y2"]) is not None]
    bY = max(y_rows, key=lambda r: _num(r["Y2"])) if y_rows else None
    labels = {bS["label"], (bF or {}).get("label"), (bY or {}).get("label")} - {None}
    coincide = len(labels) == 1
    return {
        "check": "three_point",
        "verdict": "COINCIDE" if coincide else "SWING",
        "best_S": {"label": bS["label"], "S": _num(bS["S"])},
        "best_F": {"label": (bF or {}).get("label"), "F": _num((bF or {}).get("F"))},
        "best_2Y": {"label": (bY or {}).get("label"), "Y2": _num((bY or {}).get("Y2"))},
        "detail": (
            "S/F/2Y 三个冠军是同一条 ⇒ 该模板可交付性成立"
            if coincide
            else "三个冠军分散在 %d 条臂上 ⇒ 存在跷跷板，该模板不可交付，不必再调参" % len(labels)
        ),
    }


# ────────────────────────── D5 prod 前置闸 ──────────────────────────
#: prod 硬墙阈值：本次 imb5 实证（三颗 near prod 0.967–0.973，全部撞已提交母件）
#: ⇒ prod ≥ 0.9 属"密墙"，同数据集换骨架基本无效，应先换集/换信息源。
PROD_DENSE_WALL = 0.90


def judge_prod_precheck(
    prod_result,
    threshold: Optional[float] = None,
    dense_wall: float = PROD_DENSE_WALL,
) -> dict:
    """D5：把 prod 相关性前置为"还值不值得投臂"的判据（消费 check_correlation 返回体）。

    判据（语义层完全委托 :func:`wqb.prod_verdict.prod_verdict`，本函数只做决策映射）：

    * prod 不可用（pending/busy/预读/非实时）⇒ ``PROD_UNAVAILABLE`` —— **不可判闸**，
      先补 ``refresh=True`` 实测，不要据缓存值继续或停止。
    * ``value >= dense_wall(0.90)`` ⇒ ``TRANSFER`` —— 密墙：同集换骨架基本无效
      （本轮 imb5 幂次/decay/中性化全扫仍 0.967–0.973），应换数据集或换信息源。
    * ``threshold(0.70) <= value < dense_wall`` ⇒ ``STOP`` —— 撞红线，不投更深梯度；
      若要救须换内核造新 PnL 形态。
    * ``value < threshold`` ⇒ ``CONTINUE``。

    为什么前置：本轮 imb5 的 prod 是在 86 臂梯度**跑完之后**才查的，若在 L1 探针后即查，
    可省掉后续 ~70 臂（同骨架 prod 全部落在 0.967–0.973 窄带内）。
    """
    from wqb.prod_verdict import prod_verdict  # 延迟导入，保证零平台 API

    pv = prod_verdict(prod_result, threshold)
    val = pv.get("value")
    usable = bool(pv.get("usable")) or pv.get("passes") is False
    if not usable or val is None:
        return {
            "check": "prod_precheck",
            "verdict": "PROD_UNAVAILABLE",
            "prod": val,
            "provenance": pv.get("provenance"),
            "threshold": pv.get("threshold"),
            "detail": (
                f"prod 不可判闸（provenance={pv.get('provenance')}, status={pv.get('status')}）"
                " ⇒ 先 check_correlation(refresh=True) 实测，不得据缓存/预读值决策"
            ),
        }
    thr = float(pv.get("threshold"))
    if val >= dense_wall:
        verdict, detail = "TRANSFER", (
            f"prod {val} ≥ {dense_wall}（密墙）⇒ 同集换骨架基本无效（本轮 imb5 幂次/decay/"
            "中性化全扫仍 0.967–0.973），应换数据集或换信息源，不再投更深梯度"
        )
    elif val >= thr:
        verdict, detail = "STOP", (
            f"prod {val} ≥ {thr}（红线）⇒ 不投更深梯度；若要救须换内核造新 PnL 形态"
            "（同骨架换幂次/decay 无效）"
        )
    else:
        verdict, detail = "CONTINUE", f"prod {val} < {thr} ⇒ prod 侧不构成障碍，可继续投臂"
    return {
        "check": "prod_precheck",
        "verdict": verdict,
        "prod": val,
        "provenance": pv.get("provenance"),
        "threshold": thr,
        "dense_wall": dense_wall,
        "detail": detail,
    }


# ────────────────────────── CLI ──────────────────────────
def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="梯度止损闸 / 三点检测 / 派发前三查（只读，零平台 API）"
    )
    ap.add_argument("--metrics", help="batch_get_alpha_metrics 返回的 JSON 路径")
    ap.add_argument("--l1-range", action="store_true", help="D1 L1 极差止损闸")
    ap.add_argument("--to-band", action="store_true", help="D2 配置层先行（TO 带）")
    ap.add_argument("--three-point", action="store_true", help="D3 三点检测")
    ap.add_argument("--all", action="store_true", help="D1+D2+D3（+有 --prod 时含 D5）全跑")
    ap.add_argument("--prod", help="D5：check_correlation 返回体 JSON 路径（prod 前置闸）")
    ap.add_argument("--prod-threshold", type=float, default=None,
                    help="D5 红线（缺省取自 wqb.config.PRODCORR_CEILING=0.7）")
    ap.add_argument("--prod-dense-wall", type=float, default=PROD_DENSE_WALL,
                    help=f"D5 密墙阈值（缺省 {PROD_DENSE_WALL}）")
    ap.add_argument("--lint-expr", help="D4 派发前三查（表达式文件，一行一条）")
    ap.add_argument("--field-types", help="字段类型 JSON（{field: type}），用于 VECTOR 检查")
    ap.add_argument(
        "--standardized",
        default=",".join(DEFAULT_STANDARDIZED),
        help="已标准化字段清单（逗号分隔），zscore 会塌缩",
    )
    ap.add_argument("--min-s", type=float, default=1.0)
    ap.add_argument("--max-range", type=float, default=0.7)
    ap.add_argument("--to-min", type=float, default=0.05)
    ap.add_argument("--to-max", type=float, default=0.20)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    reports: List[dict] = []
    blocked = False

    # D4 先跑（零成本，能省整批）
    if args.lint_expr:
        std = [s.strip() for s in args.standardized.split(",") if s.strip()]
        ftypes = None
        if args.field_types:
            with open(args.field_types, encoding="utf-8") as fh:
                ftypes = json.load(fh)
            if isinstance(ftypes, dict) and "results" in ftypes:  # 兼容 get_datafields 返回
                ftypes = {f["id"]: f.get("type") for f in ftypes["results"]}
        exprs = []
        with open(args.lint_expr, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    exprs.append(line)
        bad = 0
        details = []
        for e in exprs:
            iss = lint_expression(e, std, ftypes)
            if iss:
                bad += 1
                details.append({"expr": e, "issues": iss})
        reports.append(
            {
                "check": "lint_expr",
                "verdict": "BLOCK" if bad else "PASS",
                "total": len(exprs),
                "failed": bad,
                "details": details,
            }
        )
        if bad:
            blocked = True

    # D5 prod 前置（给 --prod 就跑；不占平台 API，只解析已落盘的 check_correlation 结果）
    if args.prod:
        with open(args.prod, encoding="utf-8") as fh:
            prod_raw = json.load(fh)
        r = judge_prod_precheck(prod_raw, args.prod_threshold, args.prod_dense_wall)
        reports.append(r)
        blocked |= r["verdict"] in ("STOP", "TRANSFER", "PROD_UNAVAILABLE")

    # 指标类判据
    need_metrics = args.all or args.l1_range or args.to_band or args.three_point
    if need_metrics:
        if not args.metrics:
            print("[ERR] --l1-range/--to-band/--three-point 需要 --metrics", file=sys.stderr)
            return 2
        rows = _load_metrics(args.metrics)
        if args.all or args.l1_range:
            r = judge_l1_range(rows, args.min_s, args.max_range)
            reports.append(r)
            blocked |= r["verdict"] == "STOP"
        if args.all or args.to_band:
            r = judge_to_band(rows, args.to_min, args.to_max)
            reports.append(r)
            blocked |= r["verdict"] == "TO_FIRST"
        if args.all or args.three_point:
            r = judge_three_point(rows)
            reports.append(r)
            blocked |= r["verdict"] == "SWING"

    if not reports:
        ap.print_help()
        return 2

    if args.json:
        print(json.dumps({"reports": reports, "blocked": blocked}, ensure_ascii=False, indent=2))
    else:
        for r in reports:
            chk = r["check"]
            print(f"\n=== {chk} :: {r['verdict']} ===")
            if chk == "l1_range":
                print(
                    f"  max_S {r['max_S']} ({r['max_by']}) / min_S {r['min_S']} ({r['min_by']})"
                    f" / 极差 {r['range']}"
                )
            elif chk == "to_band":
                bi, bo = r.get("best_in_band"), r.get("best_out_of_band")
                print(f"  带内 {len(r['in_band'])} 条 / 带外 {len(r['best_out_of_band'] and [1] or [])} 组")
                if bi:
                    print(f"  带内最佳 S {bi['S']} @TO {bi['TO']*100:.1f}% ({bi['label']})")
                if bo:
                    print(f"  带外最佳 S {bo['S']} @TO {bo['TO']*100:.1f}% ({bo['label']}) ← 不可交易")
            elif chk == "three_point":
                print(
                    f"  best S {r['best_S']['S']} ({r['best_S']['label']}) · "
                    f"best F {r['best_F']['F']} ({r['best_F']['label']}) · "
                    f"best 2Y {r['best_2Y']['Y2']} ({r['best_2Y']['label']})"
                )
            elif chk == "lint_expr":
                print(f"  {r['total']} 条表达式，{r['failed']} 条命中")
                for d in r["details"]:
                    print(f"  ✗ {d['expr'][:110]}")
                    for it in d["issues"]:
                        print(f"      [{it['code']}] {it['detail']}")
            elif chk == "prod_precheck":
                print(
                    f"  prod={r['prod']} provenance={r.get('provenance')} "
                    f"threshold={r['threshold']} dense_wall={r.get('dense_wall')}"
                )
            print(f"  → {r.get('detail', '')}")
        print(f"\n结论：{'BLOCKED（闸未过）' if blocked else 'PASS（可继续）'}")

    return 2 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
