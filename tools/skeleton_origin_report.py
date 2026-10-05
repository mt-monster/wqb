# -*- coding: utf-8 -*-
"""骨架来源过闸率报告：forum（论坛来源） vs native（原生）对比。

## 为什么需要这个

2026-10-02 接线了 4 条论坛来源骨架（`skeletons_data_forum.py`）。它们只经过
「经济学上说得通 + 算子/闸0/复杂度四道自检」，**没有本区实证**。本工具用来在
跑完 1–2 波后回答一件事：**论坛骨架的过闸率到底有没有比原生骨架差？**
差就降级，不差才扩批。

## 归因口径（重要）

`_load_skeleton_stats`（run_pipeline.py）依赖 ledger `s2_*_idea.skeleton_metas`，
实测 232 条 ledger **0 条含该字段**（骨架模式的 metas 只写进了本地 JSON，未落 DB）
⇒ 内建反馈闭环自 2026-09-13 起从未生效。

本工具改用**结构签名归因**：`src/wqb/expression/skeleton.structural_signature`
把表达式归一成 `ts_corr ( F , F , N )` 形状串，而 `expressions.skeleton` 列存的
正是这个串（覆盖率≈100%，十万级样本）。把库内骨架 render 后取签名即可对齐历史数据。

## pass 口径（与内建一致）

`sharpe >= 1.58 且 fitness >= 1.0`（见 run_pipeline.py:129）。

## 用法

    python tools/skeleton_origin_report.py                    # 全部区域汇总
    python tools/skeleton_origin_report.py --region GLB
    python tools/skeleton_origin_report.py --region GLB --top 15
    python tools/skeleton_origin_report.py --json out.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict

import sys as _sys, os as _os
_sys.path.insert(0, str(_os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), '..', 'src')))
from wqb.db_conn import connect as db_connect  # 规范工厂（禁裸 sqlite3.connect）

MIN_SHARPE = 1.58
MIN_FITNESS = 1.0

#: render_skeleton 只替换 {x}/{y}/{W}/{W2}；三字段骨架（econ_vol_surface /
#: econ_sentiment 等 45 条）会残留 {z}。形状只关心 F/N/算子，故补哑元即可，
#: 不去改生成路径的 render_skeleton。
_Z_TOKEN = "fld_c"
_PLACEHOLDER_RE = re.compile(r"\{[A-Za-z0-9_]+\}")


def _default_db() -> str:
    root = os.environ.get("WQB_ROOT") or os.getcwd()
    return os.environ.get("WQB_DB_PATH") or os.path.join(root, "data", "wqb.db")


def _load_library():
    """加载骨架库（仓库副本优先）。"""
    here = os.path.dirname(os.path.abspath(__file__))
    cand = os.path.join(here, "..", "Claude", "skills", "brain-make-some-gem",
                        "scripts", "trailSomeAlphas")
    cand = os.path.normpath(cand)
    if os.path.isdir(cand):
        sys.path.insert(0, cand)
    src = os.path.normpath(os.path.join(here, "..", "src"))
    if os.path.isdir(src):
        sys.path.insert(0, src)
    import skeletons                                    # noqa: E402
    from wqb.expression.skeleton import structural_signature  # noqa: E402
    return skeletons, structural_signature


def _render_for_shape(skeletons, skel, sig):
    """render 一条骨架并补齐残留占位符，返回形状串（失败返回 None）。"""
    fx = "fld_a"
    fy = "fld_b" if skel.get("n_fields", 1) >= 2 else None
    w = 21 if skel.get("needs_window") else None
    try:
        expr = skeletons.render_skeleton(skel["id"], fx, fy, w, 1)
    except Exception:                                    # noqa: BLE001
        return None
    # 残留窗口占位符 → 数字（N）；其余（{z} 等）→ 哑元字段（F）
    expr = re.sub(r"\{W2?\}", "21", expr)
    expr = _PLACEHOLDER_RE.sub(_Z_TOKEN, expr)
    return sig(expr)


def build_shape_index(skeletons, sig) -> dict:
    """skeleton_id -> shape；以及 shape -> [skeleton_id]。"""
    id2shape, shape2ids = {}, defaultdict(list)
    for s in skeletons.SKELETONS:
        sh = _render_for_shape(skeletons, s, sig)
        if not sh:
            continue
        id2shape[s["id"]] = sh
        shape2ids[sh].append(s["id"])
    return id2shape, shape2ids


def collect_metrics(conn, regions: list) -> tuple:
    """(shape -> [指标]) ；口径与 _load_skeleton_stats 一致。

    返回 (shape_metrics, expr_to_shape)。
    """
    expr_to_shape = {}
    where = "WHERE skeleton IS NOT NULL AND skeleton<>''"
    args: list = []
    if regions:
        where += " AND region IN (%s)" % ",".join("?" * len(regions))
        args += regions
    for r in conn.execute(
            f"SELECT expression, skeleton FROM expressions {where}", args):
        e = str(r[0] or "").strip()
        sh = str(r[1] or "").strip()
        if e and sh:
            expr_to_shape[e] = sh

    # 指标：backtest_results.code 兜底 + expressions 覆盖（同 key 取 expressions 值）
    metrics = {}
    bwhere = "WHERE 1=1"
    bargs: list = []
    if regions:
        bwhere += " AND region IN (%s)" % ",".join("?" * len(regions))
        bargs += regions
    for r in conn.execute(
            f"SELECT code, sharpe, fitness FROM backtest_results {bwhere}", bargs):
        e = str(r[0] or "").strip()
        if e and e not in metrics:
            metrics[e] = {"sharpe": r[1], "fitness": r[2]}
    for r in conn.execute(
            f"SELECT expression, sharpe, fitness FROM expressions {bwhere}", bargs):
        e = str(r[0] or "").strip()
        if e:
            metrics[e] = {"sharpe": r[1], "fitness": r[2]}

    agg = {}
    for e, sh in expr_to_shape.items():
        m = metrics.get(e)
        if not m or not isinstance(m.get("sharpe"), (int, float)):
            continue
        a = agg.setdefault(sh, {"n": 0, "pass": 0, "best": None, "sum": 0.0})
        sp = float(m["sharpe"])
        ft = m.get("fitness")
        a["n"] += 1
        if sp >= MIN_SHARPE and isinstance(ft, (int, float)) and ft >= MIN_FITNESS:
            a["pass"] += 1
        a["sum"] += sp
        if a["best"] is None or sp > a["best"]:
            a["best"] = sp
    for sh, a in agg.items():
        a["pass_rate"] = round(a["pass"] / a["n"], 4)
        a["avg_sharpe"] = round(a["sum"] / a["n"], 3)
        a["best_sharpe"] = round(a["best"], 3)
    return agg, expr_to_shape


def main() -> int:
    ap = argparse.ArgumentParser(description="骨架来源过闸率报告（forum vs native）")
    ap.add_argument("--region", action="append", default=[],
                    help="区域，可重复；缺省=全部区域")
    ap.add_argument("--min-n", type=int, default=5,
                    help="下结论所需的最小样本数（默认 5）")
    ap.add_argument("--top", type=int, default=10, help="明细表显示条数")
    ap.add_argument("--json", default="", help="额外把结果写成 JSON 文件")
    args = ap.parse_args()

    db = _default_db()
    if not os.path.isfile(db):
        print(f"[report] 找不到 DB：{db}", file=sys.stderr)
        return 1
    skeletons, sig = _load_library()
    id2shape, shape2ids = build_shape_index(skeletons, sig)

    conn = db_connect(db, readonly=True)     # 只读工具必须 readonly=True
    try:
        agg, _ = collect_metrics(conn, [r.upper() for r in args.region])
    finally:
        conn.close()

    # 形状 → skeleton_id（多 id 共享形状时，统计计入每个 id）
    per_skel = {}
    for s in skeletons.SKELETONS:
        sh = id2shape.get(s["id"])
        if not sh:
            continue
        a = agg.get(sh)
        per_skel[s["id"]] = {
            "origin": s.get("origin") or "native",
            "family": s.get("family", ""),
            "shape": sh,
            "n": a["n"] if a else 0,
            "pass": a["pass"] if a else 0,
            "pass_rate": a["pass_rate"] if a else None,
            "avg_sharpe": a["avg_sharpe"] if a else None,
            "best_sharpe": a["best_sharpe"] if a else None,
        }

    by_origin = defaultdict(lambda: {"n": 0, "pass": 0, "skels": 0, "with_data": 0})
    for sid, st in per_skel.items():
        o = by_origin[st["origin"]]
        o["skels"] += 1
        if st["n"]:
            o["with_data"] += 1
            o["n"] += st["n"]
            o["pass"] += st["pass"]
    for o in by_origin.values():
        o["pass_rate"] = round(o["pass"] / o["n"], 4) if o["n"] else None

    regions = ",".join(r.upper() for r in args.region) or "全部区域"
    print(f"[report] 区域={regions} | DB={db} | pass 口径 sharpe>={MIN_SHARPE} 且 fitness>={MIN_FITNESS}")
    print(f"[report] 骨架库 {len(skeletons.SKELETONS)} 条 → {len(set(id2shape.values()))} 个去重形状")
    print()
    print("== 按来源汇总 ==")
    print(f"{'来源':8s} {'骨架数':>6s} {'有样本':>6s} {'样本n':>7s} {'过闸':>6s} {'过闸率':>8s}")
    for o in ("forum", "native"):
        d = by_origin.get(o)
        if not d:
            continue
        pr = f"{d['pass_rate']:.2%}" if d["pass_rate"] is not None else "—"
        print(f"{o:8s} {d['skels']:>6d} {d['with_data']:>6d} {d['n']:>7d} {d['pass']:>6d} {pr:>8s}")

    print()
    print(f"== forum 骨架明细（{len([1 for v in per_skel.values() if v['origin']=='forum'])} 条）==")
    for sid, st in sorted(per_skel.items(), key=lambda kv: -kv[1]["n"]):
        if st["origin"] != "forum":
            continue
        pr = f"{st['pass_rate']:.2%}" if st["pass_rate"] is not None else "—"
        print(f"  {sid}")
        print(f"     shape={st['shape']}")
        print(f"     n={st['n']} pass={st['pass']} pass_rate={pr} "
              f"best={st['best_sharpe']} avg={st['avg_sharpe']}")

    print()
    print(f"== native 骨架 TOP {args.top}（按样本量）==")
    rows = [ (sid, st) for sid, st in per_skel.items()
             if st["origin"] == "native" and st["n"] ]
    rows.sort(key=lambda kv: -kv[1]["n"])
    for sid, st in rows[:args.top]:
        pr = f"{st['pass_rate']:.2%}" if st["pass_rate"] is not None else "—"
        print(f"  {sid:52s} n={st['n']:>5d} pass_rate={pr:>7s} best={st['best_sharpe']}")

    # ---- 结论 ----
    print()
    print("== 结论 ==")
    f, n = by_origin.get("forum"), by_origin.get("native")
    if not f or f["n"] < args.min_n:
        print(f"  ⚠ forum 样本 n={f['n'] if f else 0} < {args.min_n}：样本不足，**勿下结论**。")
        print("    这 4 条骨架目前只有经济学与静态自检背书，需跑完波次再评估。")
    else:
        fr, nr = f["pass_rate"], (n["pass_rate"] if n and n["n"] else 0.0)
        print(f"  forum 过闸率 {fr:.2%} vs native {nr:.2%}")
        if nr and fr < 0.5 * nr:
            print("  ⇒ forum 显著低于原生（<50%）：**建议降级，不扩批**。")
        elif nr and fr < nr:
            print("  ⇒ forum 低于原生但未达半数：**保持现规模观察，先不扩批**。")
        else:
            print("  ⇒ forum 不劣于原生：**可考虑扩批**。")

    if args.json:
        payload = {"regions": regions, "per_skeleton": per_skel,
                   "by_origin": {k: dict(v) for k, v in by_origin.items()}}
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print(f"\n[report] 已写出 {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
