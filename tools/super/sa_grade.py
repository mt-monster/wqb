#!/usr/bin/env python
"""SA（SuperAlpha）提交准入分级器 —— 离线判定，零平台调用、零配额消耗。

判据（2026-11-18 用户定案，替代旧「三条件硬拦」）：

    红线   = prod >= 0.70 或 IS checks 有 FAIL          -> REDLINE  一律硬拦，不报
    准入   = S >= 5.0 且 F >= 5.0 且 prod <= 0.65        -> ADMIT    直接进提交建议
    可汇报 = prod <= 0.68 且区内 Pareto 不劣：
             F >= 区内最强 F * 0.95 且 S >= 区内最强 S * 0.95  -> REPORT   可汇报，标注缺口
    其余（过红线但无边际）                                -> NO_EDGE  不报，仅留档

判定顺序 REDLINE > ADMIT > REPORT > NO_EDGE；prod 未测 -> UNMEASURED（待测，不判死）。

「区内最强」= 该 region 已 ACTIVE SUPER 的 max(S) / max(F)，两者可取不同 alpha
（实测 IND 最强 S 与最强 F 分属不同件，合并成一颗会虚高基线）。

用法：
    PY=world-quant-brain-mcp/.venv/Scripts/python.exe
    $PY tools/super/sa_grade.py --input results/sa_scan_20261118/metrics.json \\
        --baseline results/sa_scan_20261118/super_list.json --md out.md

输入格式（两种都吃）：
    - list[dict]                    每项一颗，字段见 FIELDS
    - {"results": list[dict]}       batch_get_alpha_metrics 原始返回
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ---- 判据常量（改这里 = 改判据，勿散落在调用方）----
ADMIT_S = 5.0
ADMIT_F = 5.0
ADMIT_PROD_MAX = 0.65
REPORT_PROD_MAX = 0.68
REDLINE_PROD = 0.70
PARETO_K = 0.95

GRADE_ORDER = {"REDLINE": 0, "UNMEASURED": 1, "ADMIT": 2, "REPORT": 3, "NO_EDGE": 4}

# 字段别名：兼容 batch_get_alpha_metrics / get_alpha_details / super_list.json
FIELDS = {
    "alpha_id": ("alpha_id", "id"),
    "region": ("region",),
    "sharpe": ("sharpe", "S"),
    "fitness": ("fitness", "F"),
    "turnover": ("turnover", "TO"),
    "returns": ("returns", "R"),
    "prod": ("prod_correlation", "prod"),
    "self": ("self_correlation", "self"),
    "two_year": ("two_year_sharpe", "y2"),
    "checks_fail": ("checks_fail", "fails"),
    "status": ("status",),
}


def _pick(row: dict, key: str):
    for k in FIELDS[key]:
        if k in row:
            return row[k]
    return None


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def normalize(payload) -> list[dict]:
    rows = payload.get("results") if isinstance(payload, dict) else payload
    out = []
    for r in rows or []:
        if not isinstance(r, dict):
            continue
        fails = _pick(r, "checks_fail") or []
        if isinstance(fails, dict):  # {"fail": [...]} 形态
            fails = fails.get("fail") or []
        out.append(
            {
                "id": _pick(r, "alpha_id"),
                "region": (_pick(r, "region") or "").upper(),
                "S": _f(_pick(r, "sharpe")),
                "F": _f(_pick(r, "fitness")),
                "TO": _f(_pick(r, "turnover")),
                "R": _f(_pick(r, "returns")),
                "prod": _f(_pick(r, "prod")),
                "self": _f(_pick(r, "self")),
                "y2": _f(_pick(r, "two_year")),
                "fails": list(fails),
                "status": _pick(r, "status"),
            }
        )
    return [r for r in out if r["id"]]


def baselines(payload) -> dict[str, dict]:
    """每区已 ACTIVE SUPER 的 max(S) / max(F)（可来自不同件）。"""
    base: dict[str, dict] = {}
    for r in normalize(payload):
        reg = r["region"]
        if not reg:
            continue
        cur = base.setdefault(reg, {"maxS": None, "maxF": None, "idS": None, "idF": None, "n": 0})
        cur["n"] += 1
        if r["S"] is not None and (cur["maxS"] is None or r["S"] > cur["maxS"]):
            cur["maxS"], cur["idS"] = r["S"], r["id"]
        if r["F"] is not None and (cur["maxF"] is None or r["F"] > cur["maxF"]):
            cur["maxF"], cur["idF"] = r["F"], r["id"]
    return base


def grade(row: dict, base: dict | None) -> dict:
    """返回 {grade, reason, gaps}。"""
    b = base or {}
    maxS, maxF = b.get("maxS"), b.get("maxF")
    S, F, prod = row["S"], row["F"], row["prod"]
    gaps: dict[str, float | None] = {}

    # 1. 红线：平台行为，任何策略都不得越过
    if row["fails"]:
        return {"grade": "REDLINE", "reason": f"IS checks FAIL: {','.join(map(str, row['fails'][:3]))}", "gaps": gaps}
    if prod is None:
        return {"grade": "UNMEASURED", "reason": "prod 未实测（先跑 check_correlation）", "gaps": gaps}
    if prod >= REDLINE_PROD:
        return {"grade": "REDLINE", "reason": f"prod {prod:.4f} >= {REDLINE_PROD}（平台红线）", "gaps": gaps}

    # 2. 准入：三条件全达
    gaps = {
        "dS": None if S is None else round(S - ADMIT_S, 4),
        "dF": None if F is None else round(F - ADMIT_F, 4),
        "dProd": round(ADMIT_PROD_MAX - prod, 4),
    }
    if S is not None and F is not None and S >= ADMIT_S and F >= ADMIT_F and prod <= ADMIT_PROD_MAX:
        return {"grade": "ADMIT", "reason": "3/3 全达", "gaps": gaps}

    # 3. 可汇报：prod ≤ .68 且区内 Pareto 不劣（双项都须达 0.95×区内最强）
    if prod > REPORT_PROD_MAX:
        return {"grade": "NO_EDGE", "reason": f"prod {prod:.4f} > {REPORT_PROD_MAX}（超余量闸）", "gaps": gaps}
    if S is None or F is None:
        return {"grade": "NO_EDGE", "reason": "S/F 缺失", "gaps": gaps}
    if maxS is None or maxF is None:
        return {"grade": "NO_EDGE", "reason": "该区无 ACTIVE SUPER 基线（新区）", "gaps": gaps}

    needS, needF = maxS * PARETO_K, maxF * PARETO_K
    gaps.update({"needS": round(needS, 4), "needF": round(needF, 4), "baseMaxS": round(maxS, 4), "baseMaxF": round(maxF, 4)})
    if S >= needS and F >= needF:
        return {"grade": "REPORT", "reason": f"区内 Pareto 达标（S≥{needS:.2f}, F≥{needF:.2f}）", "gaps": gaps}
    bad = []
    if S < needS:
        bad.append(f"S {S:.2f} < {needS:.2f}（区内最强 {maxS:.2f}×{PARETO_K}，差 {needS - S:.2f}）")
    if F < needF:
        bad.append(f"F {F:.2f} < {needF:.2f}（区内最强 {maxF:.2f}×{PARETO_K}，差 {needF - F:.2f}）")
    return {"grade": "NO_EDGE", "reason": "；".join(bad), "gaps": gaps}


def render_md(graded: list[dict], base: dict) -> str:
    lines = [
        "| id | 区 | S | F | prod | self | 区内最强S/F | S比 | F比 | 分级 | 依据 |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for g in graded:
        r, gp = g["row"], g["gaps"]
        b = base.get(r["region"], {})
        maxS = f"{b['maxS']:.2f}" if b.get("maxS") is not None else "-"
        maxF = f"{b['maxF']:.2f}" if b.get("maxF") is not None else "-"
        sRatio = f"{r['S'] / b['maxS']:.3f}" if (r["S"] is not None and b.get("maxS")) else "-"
        fRatio = f"{r['F'] / b['maxF']:.3f}" if (r["F"] is not None and b.get("maxF")) else "-"
        fmt = lambda v, n=2: "-" if v is None else f"{v:.{n}f}"
        lines.append(
            f"| `{r['id']}` | {r['region'] or '-'} | {fmt(r['S'])} | {fmt(r['F'])} | {fmt(r['prod'], 4)} | "
            f"{fmt(r['self'], 4)} | {maxS} / {maxF} | {sRatio} | {fRatio} | **{g['grade']}** | {g['reason']} |"
        )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="SA 提交准入分级（离线，零平台调用）")
    ap.add_argument("--input", required=True, help="候选指标 JSON（list 或 batch_get_alpha_metrics 返回）")
    ap.add_argument("--baseline", required=True, help="已 ACTIVE SUPER 指标 JSON（同格式，最少含 id/region/S/F）")
    ap.add_argument("--json", dest="json_out", help="分级结果输出路径")
    ap.add_argument("--md", dest="md_out", help="Markdown 表输出路径")
    ap.add_argument("--only-reportable", action="store_true", help="只打印 ADMIT/REPORT")
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    base_payload = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    base = baselines(base_payload)

    graded = []
    for row in normalize(payload):
        g = grade(row, base.get(row["region"]))
        graded.append({"row": row, **g})
    graded.sort(key=lambda g: (GRADE_ORDER[g["grade"]], -(g["row"]["S"] or 0)))

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(graded, ensure_ascii=False, indent=1), encoding="utf-8")
    md = render_md(graded, base)
    if args.md_out:
        Path(args.md_out).write_text(md + "\n", encoding="utf-8")

    show = [g for g in graded if g["grade"] in ("ADMIT", "REPORT")] if args.only_reportable else graded
    print("判据: ADMIT S>=5 & F>=5 & prod<=.65 | REPORT prod<=.68 & 区内 Pareto(0.95) | REDLINE prod>=.70 或 checks FAIL")
    for g in show:
        print(f"[{g['grade']:11}] {g['row']['id']:10} {g['row']['region']:4} {g['reason']}")
    counts = {}
    for g in graded:
        counts[g["grade"]] = counts.get(g["grade"], 0) + 1
    print("\n汇总:", " ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda kv: GRADE_ORDER[kv[0]])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
