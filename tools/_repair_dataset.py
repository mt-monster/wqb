# -*- coding: utf-8 -*-
"""从已完成的仿真把某个集的结果补写进 results / checkpoint（进程卡死后的修复）。

背景（2026-10-27 00:35）：`eur_main --datasets other401,analyst45` 跑 67 分钟、
CPU 仅 2.7s、无任何子进程，`done` 停在 112 —— 11 批仿真全部 COMPLETE 却没收割。
同时 `logs/*.log` 被外部动作整体删除（`logs/` mtime 00:27、同目录出现 test-results.xml，
说明有另一个会话在同一仓库跑 pytest / retention）。

本脚本不依赖 campaign 进程：直接遍历 checkpoint 里该集的 sim，用 `_harvest_safe.py`
收数、算 maxS/max2Y/joint/verdict，写回 results 并把该集加入 done。

用法：python tools/_repair_dataset.py other401
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
HARVEST = os.path.join(ROOT, "cache", "_harvest_safe.py")
CK = os.path.join(ROOT, "results", "full_template_campaign_checkpoint.json")
RS = os.path.join(ROOT, "results", "full_template_campaign_results.json")

os.environ.setdefault("WQB_REPO_ROOT", ROOT)
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))


def harvest(sid, ds):
    try:
        out = subprocess.run([PY, HARVEST, sid, ds, "camp"], capture_output=True,
                             text=True, timeout=600, cwd=ROOT).stdout
    except Exception:
        return []
    rows = []
    for ln in out.splitlines():
        m = re.match(r"\s*\+\s+(\w+)\s+S=([-\d.]+)\s+F=([-\d.]+)\s+tvr=([-\d.]+)\s+2Y=([-\d.]+)\s+sub=([-\d.]+)", ln)
        if m:
            rows.append(dict(alpha=m.group(1), S=float(m.group(2)), F=float(m.group(3)),
                             Y2=float(m.group(5)), sub=float(m.group(6))))
    return rows


def main():
    ds = sys.argv[1]
    ck = json.load(open(CK, encoding="utf-8"))
    sims = ck.get("sims") or {}
    entries = list(sims.get(ds) or []) + list(sims.get(ds + "@rep") or []) + list(sims.get(ds + "@cx") or [])
    print("该集 sim 条目 =", len(entries))
    all_rows, seen = [], set()
    for e in entries:
        if not (e and e[0]):
            continue
        tpl = e[1] if len(e) > 1 else "?"
        rows = harvest(e[0], ds)
        print("  %-8s 收割 %d 条" % (tpl, len(rows)))
        for r in rows:
            if r["alpha"] in seen:
                continue
            seen.add(r["alpha"])
            r["tpl"] = tpl
            all_rows.append(r)
    if not all_rows:
        print("无结果，放弃")
        return

    all_rows.sort(key=lambda r: -r["S"])
    max_s = max(r["S"] for r in all_rows)
    max_2y = max(r["Y2"] for r in all_rows)
    joint = [r for r in all_rows if r["S"] >= 1.58 and r["Y2"] >= 1.58]
    if joint:
        verdict = "ALIVE"
    elif max_s >= 1.58 and max_2y >= 1.58:
        verdict = "SPLIT"
    elif max_s >= 1.35 or max_2y >= 1.58:
        verdict = "BORDERLINE"
    else:
        verdict = "DEAD"
    print("\nmaxS=%.2f  max2Y=%.2f  joint=%d  α=%d ⇒ %s" % (max_s, max_2y, len(joint), len(all_rows), verdict))
    print("%-10s %-8s %6s %6s %7s %7s" % ("alpha", "tpl", "S", "F", "2Y", "sub"))
    for r in all_rows[:10]:
        print("%-10s %-8s %6.2f %6.2f %7.2f %7.2f" % (r["alpha"], r["tpl"], r["S"], r["F"], r["Y2"], r["sub"]))

    # 年度画像（按 max-2Y 颗算，S 弱 2Y 强的集必须这样看）
    yp = None
    try:
        from wqb_campaign.audit import year_profile
        best_2y = max(all_rows, key=lambda r: r["Y2"])
        yp = year_profile(best_2y["alpha"])
        if isinstance(yp, dict):
            print("\nyp（按 max-2Y 颗 %s）：首年=%s 年数=%s fragile=%s"
                  % (best_2y["alpha"], yp.get("first_year"), yp.get("n_years"), yp.get("fragile")))
    except Exception as e:
        print("\nyp 取不到:", type(e).__name__)

    doc = json.load(open(RS, encoding="utf-8"))
    res = doc.get("results") or {}
    old = res.get(ds) or {}
    res[ds] = dict(old)
    res[ds].update(dict(
        verdict=verdict, alphas=all_rows, max_s=max_s, max_2y=max_2y,
        n_joint=len(joint), year_profile=yp, deliverable=False,
        note="2026-10-27 00:35 由 _repair_dataset.py 从已完成的 sim 补写（campaign 进程卡死）",
    ))
    doc["results"] = res
    tmp = RS + ".tmp"
    json.dump(doc, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, RS)

    if ds not in (ck.get("done") or []):
        ck.setdefault("done", []).append(ds)
    tmp = CK + ".tmp"
    json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, CK)
    print("\n已写回 results 并加入 done（done=%d）" % len(ck["done"]))


if __name__ == "__main__":
    main()
