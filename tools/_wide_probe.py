# -*- coding: utf-8 -*-
"""绕过 select_fields 的 8+12 预算，直接对全集取字段做探针。

为什么
------
`select_fields` 每集只返回 8 full + 12 probe = 20 个字段，但：
- `fundamental23` 有 **1662 个未测字段**
- `techindi_model` 有 **798 个**
今天已验证这两个集能出 IS 全过（FUND 4 颗 / OTHER 3 颗），但都集中在同一个字段
（bank_assets_investment / tm_16_*）⇒ 同族只出 1 席。要出多颗必须换字段族。

筛选口径
--------
- cov ≥ 0.5、ftype = MATRIX
- 排除元数据/文本（正则）
- 名字长度 ≤ 60
- 排掉已测过的（本脚本的 used 列表）

用法：python tools/_wide_probe.py --stage A [--dry-run]
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
CK = os.path.join(ROOT, "results", "_wide_ck.json")
DB = os.path.join(ROOT, "data", "wqb.db")

sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
COMMON = dict(region="EUR", delay="1", truncation="0.08",
              nan_handling="ON", max_trade="ON", mode="FULL")

BAD = re.compile(r"(form_of_statement|statement_type|_source_|topic_name|full_text|"
                 r"_label$|display_label|metadata|_flag$|currency_code|_code$|"
                 r"period_end|_date$|fiscal|_id$|indicator_code|_type$|"
                 r"^adv\d|adv\d+_extra|adv\d+_usd|_usd$|_extra$)", re.I)

# 已测过的字段（避免重复）
USED = {
    # fundamental23 第一批
    "fnd23_net_income", "fnd23_intfvalld1_swds", "fnd23_intfvalld1_fbbs",
    "fnd23_intfvalld1_vbts", "fnd23_ofc", "fnd23_annfvalld1_fltf",
    "fnd23_annfvalld1_ccns", "bank_assets_investment", "fnd23_tot_assets", "fnd23_roe",
    # techindi 第一批
    "probability_fifth_quantile_ten_day_bucket_one_141",
    "predicted_first_quantile_one_day_return_17", "tm_8_r1_r5_r10_rh_glb_d1_r1_q1",
    "tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q1", "tm_16_r1_r5_r10_rh_glb_d1_r5_q1",
    "tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p2",
    "predicted_first_quantile_ten_day_return_15",
    "tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q1",
    "probability_fourth_bucket_five_day_label_zero_15",
    "tm_16_r1_r5_r10_rh_glb_d1_r5_q4_p3",
}

SPEC = {
    "A": ("fundamental23", "TOP2500", 10),
    "B": ("techindi_model", "TOPCS1600", 10),
    "C": ("fundamental23", "TOP2500", 10),   # 第二批（跳过 A 用过的）
    # ★ 模型型候选：other455 是 node2vec+PCA 合成因子（prod 有希望像 model25 一样低）；
    #   pv20 是流动性/滑点类（跳过 adv* 规模因子，只取 alternative_slippage）
    "D": ("other455", "TOP2500", 10),
    "E": ("other455", "TOPCS1600", 8),
    # ★ other455 已标死（D+E 共 18 字段全弱，S -0.46~0.39）。转 PV 塔：
    "G": ("pv87", "TOPCS1600", 10),
    "H": ("pv20", "TOPCS1600", 10),
    "I": ("pv87", "TOP2500", 8),
}


def log(m):
    print(m, flush=True)


def sig(f):
    return "signed_power(rank(ts_backfill(%s, 22)), 0.5)" % f


def candidates(ds, n, skip):
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=30000")
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute("""
        select field, ftype, coverage from field_profile_perf
        where region='EUR' and dataset=? and coverage >= 0.5 and ftype='MATRIX'
        order by coverage desc, field""", (ds,))]
    con.close()
    out = []
    for r in rows:
        f = r["field"]
        if f in USED or f in skip or BAD.search(f) or len(f) > 60:
            continue
        out.append(f)
        if len(out) >= n:
            break
    return out


def build(plan_only=None):
    plan = []
    used_extra = set()
    for tag, (ds, univ, n) in SPEC.items():
        if plan_only and tag != plan_only:
            # 仍需累计 skip 集合，保证 C 与 A 不重复
            if tag < plan_only:
                used_extra.update(candidates(ds, n, used_extra)) if False else None
            continue
        fs = candidates(ds, n, used_extra)
        used_extra.update(fs)
        ov = dict(universe=univ, decay="4", neutralization="FAST")
        plan.append((tag, ds, ov, [(f, sig(f)) for f in fs]))
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


def wait(sid, rounds=120, gap=15):
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
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    plan = build()
    if a.dry_run:
        for tag, ds, ov, ex in plan:
            log("%-4s %-18s %-12s n=%d" % (tag, ds, ov.get("universe"), len(ex)))
            for f, e in ex:
                log("     %-50s %s" % (f[:50], e))
        return

    ck = json.load(open(CK, encoding="utf-8")) if os.path.isfile(CK) else {"done": [], "results": []}
    done = set(ck["done"])
    from brain_api import brain_client
    asyncio.run(brain_client.ensure_authenticated())

    for tag, ds, ov, ex in plan:
        if tag in done:
            log("### %s 已完成，跳过" % tag); continue
        st = dict(COMMON); st.update(ov)
        fn = os.path.join(ROOT, "cache", "_wide_%s.txt" % tag)
        open(fn, "w", encoding="utf-8").write("\n".join(e for _, e in ex) + "\n")
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
        aids = ids_of(sid, ds)
        log("    收割 %d/%d" % (len(aids), len(ex)))
        for i, aid in enumerate(aids):
            d = read(aid)
            f = ex[i][0] if i < len(ex) else "?"
            ck["results"].append(dict(tag=tag, dataset=ds, field=f, alpha=aid, over=ov, **d))
        ck["done"].append(tag)
        tmp = CK + ".tmp"
        json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, CK)
        time.sleep(3)

    log("\n=== 宽扫探针（找新字段族）===")
    log("%-4s %-18s %-50s %6s %6s %7s %7s %6s" % ("批", "集", "字段", "S", "F", "2Y", "sub", "ratio"))
    for r in sorted(ck["results"], key=lambda x: -(x.get("S") or -9)):
        S, sub = r.get("S") or 0, r.get("sub") or 0
        log("%-4s %-18s %-50s %6.2f %6.2f %7s %7s %6.3f" % (
            r.get("tag"), r.get("dataset"), (r.get("field") or "")[:50], S,
            r.get("F") or 0, r.get("Y2"), r.get("sub"), (sub / S) if S else 0))


if __name__ == "__main__":
    main()
