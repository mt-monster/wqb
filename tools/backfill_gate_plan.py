# -*- coding: utf-8 -*-
"""backfill_gate_plan.py — 存量无门禁波的补门禁规划器（只读，2026-09-17）。

背景（S123 报告建议⑤）：全库有大量表达式**从未过门禁**（无 gate_results 记录）
——门禁断链或未执行。这些表达式无法合法进入回测，且堆积成死库存
（2026-09-17 实测：活跃无门禁组 339 波 / 5,612 条）。

本工具**只读**盘点并分类，不写任何状态：
  A. gateable   —— 数据集有 typed catalog，可立即用 wave_gate 补门禁
                   （生成逐组精确命令，--commands-file 落盘）
  B. no_catalog —— 缺 catalog，先跑 scan_fields 补 catalog（catalog 前置闸③的修复入口）
  C. no_dataset —— expressions.dataset 为 NULL，需先归因补 dataset 才能门禁
  D. no_campaign —— 区域目录不存在，无法判定

用法：
  python tools/backfill_gate_plan.py                     # 汇总到 stdout
  python tools/backfill_gate_plan.py --json plan.json    # 完整计划（逐组）
  python tools/backfill_gate_plan.py --commands-file run_backfill.bat
  python tools/backfill_gate_plan.py --region EUR        # 只看某区

执行（确认后）：用 --commands-file 生成的命令逐组跑 wave_gate 即可；
批量执行属写状态操作，须用户显式确认后进行。
"""
import argparse
import collections
import contextlib
import io
import json
import os
import sqlite3
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TK_SCRIPTS = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")

#: 活跃状态集（与 wave_gate 健康检查口径一致；backtested/dropped/superseded 不需补门禁）
ACTIVE_STATUSES = ("pending", "gated", "gem", "selected")


def load_catalog_checker():
    """单源复用 gate.load_whitelist 判 catalog 有无；ctx 初始化的健康检查输出静音。"""
    if TK_SCRIPTS not in sys.path:
        sys.path.insert(0, TK_SCRIPTS)
    import gate as gate_mod                      # noqa: PLC0415
    from _lib.common import CampaignContext      # noqa: PLC0415

    ctxs = {}

    def check(region, dataset):
        """True=有 catalog；False=缺；None=区域目录不可用。"""
        ctx = ctxs.get(region)
        if ctx is None:
            cdir = os.path.join(REPO, "tracking", region)
            if not os.path.isdir(cdir):
                ctxs[region] = False
                return None
            try:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    ctx = CampaignContext(cdir)
                ctxs[region] = ctx
            except SystemExit:
                ctxs[region] = False
                return None
        if ctx is False:
            return None
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                gate_mod.load_whitelist(ctx, dataset)
            return True
        except Exception:
            return False

    return check


def scan(conn):
    """返回 ungated 组 {(region, wave, dataset): {status: n}}（只读）。"""
    placeholders = ",".join("?" * len(ACTIVE_STATUSES))
    rows = conn.execute(
        f"SELECT region, wave, dataset, status, COUNT(*) n FROM expressions "
        f"WHERE status IN ({placeholders}) AND expression IS NOT NULL AND expression<>'' "
        f"GROUP BY region, wave, dataset, status", ACTIVE_STATUSES).fetchall()
    gated = {(r[0], str(r[1]), r[2] or "")
             for r in conn.execute("SELECT DISTINCT region, wave, dataset FROM gate_results")}
    groups = collections.defaultdict(collections.Counter)
    for reg, wave, ds, st, n in rows:
        key = (reg, str(wave), ds or "")
        if key in gated:
            continue
        groups[key][st] += n
    return groups


def main():
    ap = argparse.ArgumentParser(description="存量无门禁波补门禁规划器（只读）")
    ap.add_argument("--db", default=os.path.join(REPO, "data", "wqb.db"))
    ap.add_argument("--region", default=None, help="只看某区")
    ap.add_argument("--json", dest="json_out", default=None, help="完整计划 JSON 落盘")
    ap.add_argument("--commands-file", default=None,
                    help="把 A 类（可立即补门禁）逐组命令写入该文件（按表达式数降序）")
    a = ap.parse_args()

    conn = sqlite3.connect(a.db)
    groups = scan(conn)
    conn.close()
    if a.region:
        groups = {k: v for k, v in groups.items() if k[0] == a.region}

    check = load_catalog_checker()
    # dataset 级判定缓存（同一 dataset 跨波复用）
    ds_verdict = {}

    plan = []   # 逐组：{region, wave, dataset, n, status_breakdown, class}
    for (reg, wave, ds), br in groups.items():
        n = sum(br.values())
        reg = reg or "(none)"
        ds = ds or ""
        if not ds:
            cls = "C_no_dataset"
        else:
            if (reg, ds) not in ds_verdict:
                ds_verdict[(reg, ds)] = check(reg, ds)
            v = ds_verdict[(reg, ds)]
            cls = ("A_gateable" if v else
                   ("B_no_catalog" if v is False else "D_no_campaign"))
        plan.append({"region": reg, "wave": wave, "dataset": ds, "n": n,
                     "status": dict(br), "class": cls})

    plan.sort(key=lambda g: (-g["n"], g["region"], g["wave"]))
    by_cls = collections.Counter(g["class"] for g in plan)
    n_by_cls = collections.Counter()
    for g in plan:
        n_by_cls[g["class"]] += g["n"]

    print(f"无门禁组 = {len(plan)}  表达式 = {sum(g['n'] for g in plan)}"
          f"（口径：status ∈ {ACTIVE_STATUSES} 且无 gate_results 记录）")
    for cls in ("A_gateable", "B_no_catalog", "C_no_dataset", "D_no_campaign"):
        print(f"  {cls:<14} {by_cls.get(cls, 0):>4} 组  {n_by_cls.get(cls, 0):>5} 条")
    print()
    by_region = collections.Counter()
    for g in plan:
        by_region[g["region"]] += g["n"]
    print("按区表达式数:", dict(by_region.most_common()))
    print()
    print("Top10 组：")
    for g in plan[:10]:
        print(f"  {g['class']:<14} {g['region']:<5} {g['wave']:<28} "
              f"{(g['dataset'] or '(none)'):<30} {g['n']:>5}")

    if a.commands_file:
        cmds = [f"python tools{os.sep}wave_gate.py --campaign-dir tracking{os.sep}{g['region']} "
                f"--dataset {g['dataset']} --wave {g['wave']} --from-db"
                for g in plan if g["class"] == "A_gateable"]
        with open(a.commands_file, "w", encoding="utf-8") as f:
            f.write("\n".join(cmds) + ("\n" if cmds else ""))
        print(f"\nA 类命令已写入 {a.commands_file}（{len(cmds)} 条，按表达式数降序）")

    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as f:
            json.dump({"summary": {"groups": len(plan),
                                   "by_class_groups": dict(by_cls),
                                   "by_class_exprs": dict(n_by_cls)},
                       "plan": plan}, f, ensure_ascii=False, indent=1)
        print(f"完整计划已写入 {a.json_out}")


if __name__ == "__main__":
    main()
