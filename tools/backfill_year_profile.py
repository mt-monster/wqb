# -*- coding: utf-8 -*-
"""回填 `year_profile`：修 fail-open 的历史遗留。

背景
----
`pipeline.py` 里 `year_profile` 只在 `max_s >= 1.2` 时计算（阈值 2026-10-24 已从 1.4 下调到 1.2）。
**旧阈值期跑完的集没有 yp**，而当时 `deliverable` 的写法是
    `and not (yp and yp.get("fragile"))`
—— `yp=None` 时 `not None` 恒真 ⇒ **yp 缺失反而放行**（fail-open）。
受害实例：`quant_factor_lib`（yp=null，实际首年 2020、仅 4 年）、`model25`（yp=null 被判 ALIVE）。

本脚本：对 `max_s >= 1.2` 且 `year_profile` 缺失的集，补算并回写。
另把 `fragile` 的集 verdict 标为 `INVALID_SAMPLE`（与 pipeline 新逻辑一致）。

用法
----
    WQB_REPO_ROOT=<repo> python tools/backfill_year_profile.py --dry-run
    WQB_REPO_ROOT=<repo> python tools/backfill_year_profile.py
"""
import argparse
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results", "full_template_campaign_results.json")
SKILL = os.path.join(os.path.expanduser("~"), ".workbuddy", "skills",
                     "wq-brain-ra-eur", "scripts")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--min-s", type=float, default=1.2)
    args = ap.parse_args()

    os.environ.setdefault("WQB_REPO_ROOT", ROOT)   # config.py 靠它定位仓库根
    sys.path.insert(0, SKILL)
    sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
    from wqb_campaign.audit import year_profile  # noqa: E402

    with open(RES, encoding="utf-8") as fh:
        doc = json.load(fh)
    res = doc.get("results") or {}

    todo = []
    for ds, v in res.items():
        if not isinstance(v, dict):
            continue
        if (v.get("max_s") or -9) < args.min_s:
            continue
        if isinstance(v.get("year_profile"), dict):
            continue
        al = [a for a in (v.get("alphas") or []) if a.get("s") is not None]
        if not al:
            continue
        best = max(al, key=lambda a: a["s"])
        todo.append((ds, best["alpha"], best["s"], v.get("verdict")))

    print("待回填 {} 个集（max_s>={} 且 yp 缺失）：".format(len(todo), args.min_s))
    for ds, aid, s, vd in sorted(todo, key=lambda x: -x[2]):
        print("  {:<24} S={:<5} alpha={:<10} verdict={}".format(ds, s, aid, vd))
    if args.dry_run or not todo:
        print("\n[dry-run] 未写盘")
        return

    changed = 0
    for ds, aid, s, vd in todo:
        try:
            yp = year_profile(aid)
        except Exception as exc:  # noqa: BLE001
            print("  [{}] 画像失败 {}: {}".format(ds, type(exc).__name__, exc))
            continue
        if not isinstance(yp, dict):
            print("  [{}] 画像返回空（{}）".format(ds, yp))
            continue
        v = res[ds]
        v["year_profile"] = yp
        v["yp_backfilled"] = True
        frag = bool(yp.get("fragile"))
        old_v = v.get("verdict")
        if frag and old_v in ("ALIVE", "BORDERLINE", "SPLIT"):
            v["verdict"] = "INVALID_SAMPLE"
        # fail-closed 重算 deliverable
        if frag or not isinstance(yp, dict):
            v["deliverable"] = False
        changed += 1
        print("  [{}] 首年={} 年数={} late_start={} fragile={}  verdict {} -> {}".format(
            ds, yp.get("first_year"), yp.get("n_years"), yp.get("late_start"),
            frag, old_v, v.get("verdict")))
        time.sleep(1)

    if changed:
        tmp = RES + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, ensure_ascii=False)
        os.replace(tmp, RES)
        print("\n已回写 {} 个集 -> {}".format(changed, RES))
    else:
        print("\n无变更")


main()
