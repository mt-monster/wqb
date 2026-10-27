# -*- coding: utf-8 -*-
"""回溯归因：把 `results/full_template_campaign_results.json` 里已有的变体矩阵
一次性算成归因台账，并输出跨集轴效应汇总。

用途
----
1. 补齐历史（流水线接入归因之前跑的集没有台账）
2. 产出一张「哪个轴最常成为赢家、效应多大」的全局表
3. 满足 Stop 钩子的归因完整性校验（`guard_attribution`）

用法
----
    WQB_REPO_ROOT=<repo> python tools/attribution_scan.py [--dry-run] [--min-s 1.2]
"""
import argparse
import collections
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(os.path.expanduser("~"), ".workbuddy", "skills",
                     "wq-brain-ra-eur", "scripts")
RES = os.path.join(ROOT, "results", "full_template_campaign_results.json")
OUT_MD = os.path.join(ROOT, "output_report", "attribution_matrix_20261026.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--min-s", type=float, default=1.2)
    args = ap.parse_args()

    os.environ.setdefault("WQB_REPO_ROOT", ROOT)
    sys.path.insert(0, SKILL)
    from wqb_campaign.attribution import build_record, append_record, LEDGER

    doc = json.load(open(RES, encoding="utf-8"))
    res = doc.get("results") or {}

    def _norm(a):
        """兼容两种键名风格：`{s,f,y2,...}` 与 `{S,F,Y2,sub,tpl}`。

        历史 campaign 结果混用大小写（如 other401 全用大写 S/F/Y2），
        `families()` 只认小写 `s`，不归一化会让该集整集被跳过 ⇒ 归因台账缺条目 ⇒ Stop 钩子一直拦。
        """
        if not isinstance(a, dict):
            return a
        if a.get("s") is None and a.get("S") is not None:
            a = dict(a)
            a["s"] = a["S"]
        if a.get("f") is None and a.get("F") is not None:
            a = dict(a)
            a["f"] = a["F"]
        return a

    recs, skipped = [], []
    for ds, v in res.items():
        if not isinstance(v, dict):
            continue
        al = [_norm(a) for a in (v.get("alphas") or [])]
        al = [a for a in al if isinstance(a, dict) and a.get("s") is not None]
        if not al:
            continue
        if (v.get("max_s") or -9) < args.min_s:
            skipped.append(ds)
            continue
        rec = build_record(ds, al, verdict=v.get("verdict"),
                           yp=v.get("year_profile"), sweep=v.get("settings_sweep") or {})
        if rec:
            recs.append(rec)

    print("可归因 {} 个集（max_s>={}；跳过 {} 个低 S 集）".format(
        len(recs), args.min_s, len(skipped)))
    if args.dry_run:
        print("[dry-run] 未写盘")
    else:
        # 重写台账（回溯是幂等的：以本次扫描为准）
        tmp = LEDGER + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            for r in recs:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(tmp, LEDGER)
        print("台账已重写：{}（{} 条）".format(LEDGER, len(recs)))

    # ---- 全局汇总 ----
    fam_win = collections.Counter()
    axis_win = collections.Counter()
    axis_delta = collections.defaultdict(list)
    for r in recs:
        w = r.get("winner")
        # ① 先把**所有**族的 ΔS 记进轴统计（不能 break，否则只剩赢家那条 0 值）
        for f in (r.get("families") or []):
            axis_delta[f["axis"]].append(f.get("delta_vs_best") or 0.0)
        # ② 再单独记赢家
        for f in (r.get("families") or []):
            if f["tpl"] == w:
                fam_win[f["tpl"]] += 1
                axis_win[f["axis"]] += 1
                break
    spreads = [r["spread"] for r in recs if isinstance(r.get("spread"), (int, float))]

    print()
    print("=== 赢家族 Top10 ===")
    for tpl, n in fam_win.most_common(10):
        print("  {:<10} {} 次".format(tpl, n))
    print()
    print("=== 赢轴 Top10（语义） ===")
    for ax, n in axis_win.most_common(10):
        print("  {:<24} {} 次".format(ax, n))
    print()
    print("=== 各轴相对赢家的平均差距（越接近 0 说明该轴越不拖后腿） ===")
    rows = []
    for ax, ds in axis_delta.items():
        if len(ds) < 5:
            continue
        rows.append((ax, len(ds), sum(ds) / len(ds)))
    for ax, n, mean in sorted(rows, key=lambda x: -x[2]):
        print("  {:<24} n={:<4} 平均 ΔS={:+.3f}".format(ax, n, mean))
    print()
    if spreads:
        print("族间跨度：均值 {:.2f}｜最大 {:.2f}（跨度大 = 该字段对轴极敏感）".format(
            sum(spreads) / len(spreads), max(spreads)))

    # ---- markdown ----
    if not args.dry_run:
        L = ["# EUR 变体轴归因矩阵（回溯）", "",
             "生成：2026-10-26　｜　可归因集：{}（max_s≥{}）".format(len(recs), args.min_s), "",
             "## 赢家族 Top10", "", "| 模板族 | 成为赢家次数 | 轴语义 |", "|---|---|---|"]
        from wqb_campaign.attribution import axis_of
        for tpl, n in fam_win.most_common(10):
            L.append("| `{}` | {} | {} |".format(tpl, n, axis_of(tpl)))
        L += ["", "## 各轴平均差距（相对族内赢家）", "",
              "| 轴 | 样本数 | 平均 ΔS |", "|---|---|---|"]
        for ax, n, mean in sorted(rows, key=lambda x: -x[2]):
            L.append("| {} | {} | {:+.3f} |".format(ax, n, mean))
        L += ["", "## 逐集明细（按族间跨度降序，跨度大=该字段对轴敏感）", "",
              "| 集 | verdict | maxS | 赢家族 | 跨度 | 归因结论 |", "|---|---|---|---|---|---|"]
        for r in sorted(recs, key=lambda x: -(x.get("spread") or 0))[:40]:
            L.append("| `{}` | {} | {} | `{}` | {} | {} |".format(
                r["dataset"], r.get("verdict"), r.get("max_s"),
                r.get("winner"), r.get("spread"), r.get("note")))
        with open(OUT_MD, "w", encoding="utf-8") as fh:
            fh.write("\n".join(L) + "\n")
        print()
        print("矩阵已写：", OUT_MD)


main()
