# -*- coding: utf-8 -*-
"""模板实验：`group_rank(<base>, market)` 是否真的「抬地板」。

背景
----
E1（2026-10-26）同字段配对实测：
    pv87   : group_rank(lvl_rk, market) vs 裸 lvl_rk  → Δ 均值 +0.156（最高 0.60→0.81）
    other545: signed_power(dw, 0.7) vs 裸 dw          → Δ 均值 +0.170
而 A/B（同日）证明 `signed_power(dw,0.7) ≈ dw`（0.18≈0.25、0.76≈0.74）⇒ 那个 +0.17 其实是
dw 本身的水平差异，不是压缩带来的。

⇒ 真正改「读数方式」的是 **分组内相对位置**（group_rank），它会产生新信息；
   单调压缩（signed_power）不产生。

设计（3 臂 × 8 字段 × 2 集 = 48 条，5 批）
------------------------------------------
| 臂 | 表达式 | 对照（已有，不需重跑） |
|---|---|---|
| grp_rk | `group_rank(rank(ts_backfill(F,22)), market)` | lvl_rk = `rank(...)`：other571 **0.15** / insider **0.80** |
| grp_tr | `group_rank(ts_rank(ts_backfill(F,22),126), market)` | lvl_tr 历史：other571 **0.78** / insider **0.24** |
| grp_zs | `group_rank(ts_zscore(ts_backfill(F,22),126), market)` | lvl_zs 历史：other571 **0.83** / insider **0.23** |

对照值可信的依据：同日 A/B 的 lvl_rk/lvl_zs/lvl_qt/lvl_sc 实测值与历史逐位一致
（0.15/0.15、0.80/0.80、0.83/0.83、0.23/0.23）。

判据：某臂 maxS 显著高于其对照（+0.15 以上）⇒ group_rank 值得进模板；
      三臂全部与对照持平 ⇒ 「抬地板」这个方向在 EUR 上不成立，模板不再动。

用法：python tools/_grp_rank_probe.py [--dry-run]
"""
import argparse
import asyncio
import json
import os
import re
import sqlite3
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
SUBMIT = os.path.join(ROOT, "tools", "submit_batch.py")
HARVEST = os.path.join(ROOT, "cache", "_harvest_safe.py")
CK = os.path.join(ROOT, "results", "_grp_rank_ck.json")
LEDGER = os.path.join(ROOT, "results", "_grp_rank_ledger.json")

os.environ.setdefault("WQB_REPO_ROOT", ROOT)
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-ra-eur", "scripts"))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

from wqb_campaign.fields import select_fields   # noqa: E402

DATASETS = ["other571", "insider_matrix"]
BATCH = 10
SETTINGS = dict(region="EUR", universe="TOPCS1600", delay="1", decay="4",
                neutralization="FAST", truncation="0.08",
                nan_handling="ON", max_trade="ON", mode="FULL")

ARMS = {
    "grp_rk": ("group_rank(rank(ts_backfill(%s, 22)), market)", "lvl_rk"),
    "grp_tr": ("group_rank(ts_rank(ts_backfill(%s, 22), 126), market)", "lvl_tr"),
    "grp_zs": ("group_rank(ts_zscore(ts_backfill(%s, 22), 126), market)", "lvl_zs"),
}
BASE_MAXS = {  # 历史/AB 实测的同字段对照（other571, insider_matrix）
    "lvl_rk": (0.15, 0.80),
    "lvl_tr": (0.78, 0.24),
    "lvl_zs": (0.83, 0.23),
}


def log(m):
    print(m, flush=True)


def build():
    con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db")); con.execute("PRAGMA busy_timeout=30000")
    con.row_factory = sqlite3.Row
    plan = []
    for ds in DATASETS:
        _all = select_fields(con, ds, field_min_cov=0.6)
        _full = [r for r in _all if r.get("tier") == "full"]
        _probe = [r for r in _all if r.get("tier") != "full"]
        sel = (_full + _probe)[:8]
        log("[%s] 字段 %d 个" % (ds, len(sel)))
        for arm, (tpl, _base) in ARMS.items():
            for r in sel:
                if r.get("field_type") == "VECTOR":
                    continue   # rank() 套在 VECTOR 上非法，跳过（两集无 VECTOR，此处仅防御）
                plan.append(dict(ds=ds, arm=arm, field=r["field_name"],
                                 expr=tpl % r["field_name"]))
    con.close()
    return plan


def load():
    if os.path.isfile(CK):
        try:
            return json.load(open(CK, encoding="utf-8"))
        except Exception:
            pass
    return {"done": [], "results": []}


def save(ck):
    for p, obj in ((CK, ck), (LEDGER, ck["results"])):
        tmp = p + ".tmp"
        json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, p)


def submit(path):
    cmd = [PY, SUBMIT, "--path", path, "--region", SETTINGS["region"],
           "--universe", SETTINGS["universe"], "--delay", SETTINGS["delay"],
           "--decay", SETTINGS["decay"], "--neutralization", SETTINGS["neutralization"],
           "--truncation", SETTINGS["truncation"],
           "--nan-handling", SETTINGS["nan_handling"],
           "--max-trade", SETTINGS["max_trade"],
           "--simulation-mode", SETTINGS["mode"]]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=ROOT)
        out = (p.stdout or "") + "\n" + (p.stderr or "")
    except Exception as ex:
        log("  [submit] 异常 %s" % ex)
        return None
    m = re.search(r"/simulations/([A-Za-z0-9]+)", out)
    return m.group(1) if m else None


def wait(sid, rounds=110, gap=15):
    from brain_api import brain_client
    for _ in range(rounds):
        try:
            j = brain_client.session.get("%s/simulations/%s" % (brain_client.base_url, sid),
                                         timeout=30).json()
        except Exception:
            time.sleep(gap); continue
        kids = j.get("children") or []
        if not kids:
            if j.get("status") in ("ERROR", "FAIL", "CANCELLED"):
                return False
            time.sleep(gap); continue
        sts = []
        for k in kids:
            try:
                kk = brain_client.session.get("%s/simulations/%s" % (brain_client.base_url, k),
                                              timeout=30).json()
                sts.append((kk or {}).get("status"))
            except Exception:
                sts.append(None)
        if all(x in ("COMPLETE", "ERROR", "FAIL", "CANCELLED") for x in sts):
            return True
        time.sleep(gap)
    return False


def harvest(sid, ds):
    try:
        out = subprocess.run([PY, HARVEST, sid, ds, "camp"], capture_output=True,
                             text=True, timeout=600, cwd=ROOT).stdout
    except Exception:
        return []
    rows = []
    for ln in out.splitlines():
        m = re.match(r"\s*\+\s+(\w+)\s+S=([-\d.]+)\s+F=([-\d.]+).*?2Y=([-\d.]+)\s+sub=([-\d.]+)", ln)
        if m:
            rows.append(dict(alpha=m.group(1), S=float(m.group(2)), F=float(m.group(3)),
                             Y2=float(m.group(4)), sub=float(m.group(5))))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    plan = build()
    log("表达式 %d 条（%d 批）" % (len(plan), (len(plan) + BATCH - 1) // BATCH))
    if a.dry_run:
        for p in plan[:4]:
            log("   %s/%s  %s" % (p["ds"], p["arm"], p["expr"]))
        return

    ck = load()
    done = set(ck["done"])
    from brain_api import brain_client
    asyncio.run(brain_client.ensure_authenticated())

    for bi in range(0, len(plan), BATCH):
        chunk = plan[bi:bi + BATCH]
        key = "g%02d" % (bi // BATCH)
        if key in done:
            log("### %s 已完成，跳过" % key)
            continue
        fn = os.path.join(ROOT, "cache", "_grp_%s.txt" % key)
        open(fn, "w", encoding="utf-8").write("\n".join(p["expr"] for p in chunk) + "\n")
        sid = None
        for t in range(3):
            sid = submit(fn)
            if sid:
                break
            log("  [retry] %s 第 %d 次提交失败，等 30s" % (key, t + 1))
            time.sleep(30)
        if not sid:
            log("### %s 三次提交均失败，停止" % key)
            break
        log("### %s n=%d sim=%s" % (key, len(chunk), sid))
        if not wait(sid):
            log("  [warn] %s 未到终态，跳过" % key)
            continue
        rows = harvest(sid, chunk[0]["ds"])
        log("    收割 %d/%d" % (len(rows), len(chunk)))
        for i, r in enumerate(rows):
            if i < len(chunk):
                r.update(ds=chunk[i]["ds"], arm=chunk[i]["arm"], field=chunk[i]["field"])
            ck["results"].append(r)
        ck["done"].append(key)
        save(ck)
        time.sleep(3)

    log("\n" + "=" * 90)
    log("=== group_rank 实验（对照 = 同字段裸 base 的历史/AB 实测）===")
    log("%-16s %-8s %4s %7s %9s %9s %8s" % ("dataset", "arm", "n", "maxS", "对照maxS", "Δ", "判定"))
    import collections
    agg = collections.defaultdict(list)
    for r in ck["results"]:
        if r.get("S") is not None:
            agg[(r["ds"], r["arm"])].append(r["S"])
    for di, ds in enumerate(DATASETS):
        for arm, (_t, base) in ARMS.items():
            v = agg.get((ds, arm)) or []
            ctl = BASE_MAXS[base][di]
            if not v:
                log("%-16s %-8s %4d %7s %9.2f %9s %8s" % (ds, arm, 0, "—", ctl, "—", ""))
                continue
            mx = max(v)
            d = mx - ctl
            verdict = "★抬升" if d >= 0.15 else ("持平" if d > -0.05 else "变差")
            log("%-16s %-8s %4d %7.2f %9.2f %+9.2f %8s" % (ds, arm, len(v), mx, ctl, d, verdict))
        log("-" * 90)
    log("断点 %s" % CK)


if __name__ == "__main__":
    main()
