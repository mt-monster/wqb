# -*- coding: utf-8 -*-
"""未点亮塔攻坚：跨集单腿探针 → 同集辅腿组合。

目标（用户 2026-10-27 12:10 指定）
--------------------------------
- **已点亮塔的候选先不提**（EUR 已点亮 = MODEL 3 / ANALYST 5），焦点在**未点亮塔**。
- 产出 **10 个 Regular Alpha**。

EUR D1 点亮状态（平台 `get_pyramid_alphas` 实测 2026-10-27 12:11）
    model 3 ✓ ｜ analyst 5 ✓ ｜ fundamental 2 ｜ risk 2 ｜ pv 1 ｜ insiders 1 ｜ other 1
    sentiment 0 ｜ earnings 0 ｜ institutions 0 ｜ news 0 ｜ socialmedia 0 ｜ imbalance 0 ｜ macro 0
⇒ 差 1 颗：**FUNDAMENTAL(2) / RISK(2)**；差 2 颗：PV/INSIDERS/OTHER(1)

可复用配方（今日 `rKRpEMWo` 已验证，prod 0.594 / FAIL 空）
------------------------------------------------------------
    add(add(sig(主腿), w1*sig(辅sub)), w2*sig(辅2Y))
    sig(F) = signed_power(rank(ts_backfill(F, 22)), 0.5)
关键：辅腿选**单独 ratio 高（偏小票）**的弱字段，另一条辅腿选**单独 2Y 高**的弱字段。
全部字段取同一数据集 ⇒ 保 ATOM（避免 `IS_LADDER_SHARPE`）。

阶段
----
1. `probe` 批：每集取 full 前 N 个字段跑单腿，看谁有信号（S ≥1.0 记下）
2. `blend` 批：对有信号的集做「主腿 + 两条弱辅腿」权重扫描

用法：python tools/_unlit_sweep.py --stage probe [--dry-run]
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
CK = os.path.join(ROOT, "results", "_unlit_ck.json")
LEDGER = os.path.join(ROOT, "results", "_unlit_ledger.json")
DB = os.path.join(ROOT, "data", "wqb.db")

sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-ra-eur", "scripts"))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
os.environ.setdefault("WQB_REPO_ROOT", ROOT)

COMMON = dict(region="EUR", delay="1", truncation="0.08",
              nan_handling="ON", max_trade="ON", mode="FULL")
BASE_SET = dict(universe="TOPCS1600", decay="4", neutralization="FAST")

# probe 批：(数据集, 取 full 前几个字段)
# 优先「差 1 颗点亮」的 FUNDAMENTAL / RISK，其次 PV / OTHER / NEWS / SENTIMENT
PROBE_PLAN = [
    ("P1_fund", [("fundamental23", 3), ("fundamental17", 3), ("fundamental6", 2), ("fundamental72", 2)]),
    ("P2_risk", [("risk62", 3), ("risk70", 3), ("risk68", 2), ("risk72", 2)]),
    ("P3_pv",   [("pv87", 3), ("pv20", 3), ("other455", 2), ("techindi_model", 2)]),
    ("P4_sent", [("news18", 2), ("news7", 2), ("sentiment21", 2), ("earnings6", 2), ("insider_agg_matrix", 2)]),
]


def log(m):
    print(m, flush=True)


def fields_of(ds, n, min_cov=0.5):
    from wqb_campaign.fields import select_fields
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=30000")
    con.row_factory = sqlite3.Row
    try:
        sel = select_fields(con, ds, field_min_cov=min_cov)
    finally:
        con.close()
    full = [r for r in sel if r.get("tier") == "full"]
    other = [r for r in sel if r.get("tier") != "full"]
    return (full + other)[:n]


def sig(f):
    return "signed_power(rank(ts_backfill(%s, 22)), 0.5)" % f


def build():
    plan = []
    for tag, specs in PROBE_PLAN:
        ex = []
        for ds, n in specs:
            fs = fields_of(ds, n)
            for r in fs:
                ex.append(("%s:%s" % (ds, r["field_name"][:26]), sig(r["field_name"]), ds))
        plan.append((tag, BASE_SET, ex))
    return plan


def submit(path, st):
    cmd = [PY, SUBMIT, "--path", path, "--region", st["region"],
           "--universe", st["universe"], "--delay", st["delay"], "--decay", st["decay"],
           "--neutralization", st["neutralization"], "--truncation", st["truncation"],
           "--nan-handling", st["nan_handling"], "--max-trade", st["max_trade"],
           "--simulation-mode", st["mode"]]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=ROOT)
        out = (p.stdout or "") + "\n" + (p.stderr or "")
    except Exception as ex:
        log("  [submit] 异常 %s" % ex); return None
    m = re.search(r"/simulations/([A-Za-z0-9]+)", out)
    if not m:
        log("  [submit] 失败 %s" % out.strip().splitlines()[-3:]); return None
    return m.group(1)


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
            if j.get("status") == "COMPLETE":
                return True
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


def read(aid):
    from brain_api import brain_client
    try:
        j = brain_client.session.get("%s/alphas/%s" % (brain_client.base_url, aid), timeout=30).json()
    except Exception:
        return {}
    i = j.get("is") or {}
    out = dict(S=i.get("sharpe"), F=i.get("fitness"), TO=i.get("turnover"),
               ret=i.get("returns"), margin=i.get("margin"))
    for c in (i.get("checks") or []):
        n = c.get("name")
        if n == "LOW_2Y_SHARPE": out["Y2"] = c.get("value")
        elif n == "LOW_SUB_UNIVERSE_SHARPE":
            out["sub"] = c.get("value"); out["sub_limit"] = c.get("limit")
        elif n == "LOW_ROBUST_UNIVERSE_SHARPE": out["rob"] = c.get("value")
    out["fails"] = [c.get("name") for c in (i.get("checks") or []) if c.get("result") == "FAIL"]
    return out


def ids_of(sid, ds):
    try:
        out = subprocess.run([PY, HARVEST, sid, ds, "camp"], capture_output=True,
                             text=True, timeout=600, cwd=ROOT).stdout
    except Exception:
        return []
    return [m.group(1) for m in (re.match(r"\s*\+\s+(\w+)\s+S=", ln) for ln in out.splitlines()) if m]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="probe")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    plan = build()
    if a.dry_run:
        for tag, ov, ex in plan:
            log("%-8s %s n=%d" % (tag, ov, len(ex)))
            for nm, e, ds in ex:
                log("   %-42s %s" % (nm, e))
        return

    ck = json.load(open(CK, encoding="utf-8")) if os.path.isfile(CK) else {"done": [], "results": []}
    done = set(ck["done"])
    from brain_api import brain_client
    asyncio.run(brain_client.ensure_authenticated())

    for tag, ov, ex in plan:
        if tag in done:
            log("### %s 已完成，跳过" % tag); continue
        st = dict(COMMON); st.update(ov)
        fn = os.path.join(ROOT, "cache", "_unlit_%s.txt" % tag)
        open(fn, "w", encoding="utf-8").write("\n".join(e for _, e, _ in ex) + "\n")
        sid = None
        for t in range(3):
            sid = submit(fn, st)
            if sid:
                break
            log("  [retry] %s 第 %d 次失败，等 30s" % (tag, t + 1)); time.sleep(30)
        if not sid:
            log("### %s 三次均失败" % tag); continue
        log("### %s n=%d sim=%s" % (tag, len(ex), sid))
        if not wait(sid):
            log("  [warn] %s 未到终态" % tag); continue
        # 同批可能含多个数据集，按集分别收割再合并
        all_ds = sorted({d for _, _, d in ex})
        got = []
        for d in all_ds:
            got.extend(ids_of(sid, d))
        log("    收割 %d/%d" % (len(got), len(ex)))
        for i, aid in enumerate(got):
            dd = read(aid)
            name = ex[i][0] if i < len(ex) else "?"
            ds = ex[i][2] if i < len(ex) else "?"
            ck["results"].append(dict(tag=tag, variant=name, dataset=ds, alpha=aid, over=ov, **dd))
        ck["done"].append(tag)
        for p, obj in ((CK, ck), (LEDGER, ck["results"])):
            tmp = p + ".tmp"
            json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.replace(tmp, p)
        time.sleep(3)

    log("\n=== 未点亮塔探针 ===")
    log("%-8s %-40s %6s %6s %7s %7s %7s" % ("批", "字段", "S", "F", "2Y", "sub", "ratio"))
    for r in sorted(ck["results"], key=lambda x: -(x.get("S") or -9)):
        S, sub = r.get("S") or 0, r.get("sub") or 0
        log("%-8s %-40s %6.2f %6.2f %7s %7s %7.3f" % (
            r.get("tag"), r.get("variant"), S, r.get("F") or 0, r.get("Y2"),
            r.get("sub"), (sub / S) if S else 0))


if __name__ == "__main__":
    main()
