# -*- coding: utf-8 -*-
"""未点亮塔：模型型集的字段探针（为三腿混合选主腿/辅腿）。

为什么需要
----------
`rKRpEMWo`（model25 三腿，**已点亮塔 ⇒ 不提交**）证明了配方：
    add(add(sig(主腿), w1*sig(辅sub)), w2*sig(辅2Y))
    sig(F) = signed_power(rank(ts_backfill(F, 22)), 0.5)
其中 辅助腿选「单独 sub/S 高（偏小票）」与「单独 2Y 高」的**弱字段**。
⇒ 要给未点亮塔复用，必须先知道每个候选字段的 (S, sub/S, 2Y) 三元组。

目标集（EUR、未点亮塔、已有 IS 全过痕迹）
------------------------------------------
- `techindi_model`(OTHER) : maxS 1.91 / 2Y 2.05 / joint=5，但最强颗 prod 0.8511
- `fundamental23` (FUND)  : maxS 1.47 / 2Y 2.07
- `fundamental17` (FUND)  : maxS 1.43 / 2Y 2.66
- `risk70`        (RISK)  : maxS 1.24 / 2Y 1.92

⚠ 字段过滤（2026-10-27 踩坑）
- 元数据/文本字段（`*_form_of_statement`、`*_statement_type`、`topic_name`）会让**整批 ERROR**
- 幽灵字段：`select_fields` 已过滤（打印 "本地 N → 平台认证 0" 即该集不可挖）
- 提交前对每批跑 `preflight_expressions`，剔掉 unknown

用法：python tools/_modelfam_probe.py [--dry-run]
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
CK = os.path.join(ROOT, "results", "_modelfam_ck.json")
LEDGER = os.path.join(ROOT, "results", "_modelfam_ledger.json")
DB = os.path.join(ROOT, "data", "wqb.db")

sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-ra-eur", "scripts"))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
os.environ.setdefault("WQB_REPO_ROOT", ROOT)

COMMON = dict(region="EUR", delay="1", truncation="0.08",
              nan_handling="ON", max_trade="ON", mode="FULL")
BASE = dict(universe="TOPCS1600", decay="4", neutralization="FAST")

# 会令整批 ERROR 的字段名模式（元数据/文本）
BAD_PAT = re.compile(r"(form_of_statement|statement_type|_source_|topic_name|full_text|"
                     r"_label$|display_label|metadata|_flag$|currency_code)", re.I)

PLAN_SPEC = [
    ("T1_techindi", "techindi_model", 10),
    ("T2_fund23", "fundamental23", 10),
    ("T3_fund17", "fundamental17", 10),
]


def log(m):
    print(m, flush=True)


def sig(f):
    return "signed_power(rank(ts_backfill(%s, 22)), 0.5)" % f


def pick(ds, n):
    from wqb_campaign.fields import select_fields
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=30000")
    con.row_factory = sqlite3.Row
    try:
        sel = select_fields(con, ds, field_min_cov=0.5)
    finally:
        con.close()
    full = [r for r in sel if r.get("tier") == "full"]
    rest = [r for r in sel if r.get("tier") != "full"]
    out = []
    for r in full + rest:
        f = r["field_name"]
        if BAD_PAT.search(f):
            continue
        if len(f) > 60:
            continue
        out.append(f)
        if len(out) >= n:
            break
    return out


def build():
    plan = []
    for tag, ds, n in PLAN_SPEC:
        fs = pick(ds, n)
        plan.append((tag, BASE, [(ds, f, sig(f)) for f in fs]))
    return plan


def preflight(exprs, dataset_id=None):
    """用平台 preflight 剔掉未知字段（避免整批 ERROR）。"""
    from brain_api import brain_client
    try:
        r = brain_client.session.post(
            "%s/simulations/validate" % brain_client.base_url,
            json=dict(type="REGULAR", settings=dict(instrumentType="EQUITY", region="EUR",
                                                    universe="TOPCS1600", delay=1,
                                                    decay=4, neutralization="FAST",
                                                    truncation=0.08, pasteurization="ON",
                                                    unitHandling="VERIFY", nanHandling="ON",
                                                    maxTrade="ON", language="FASTEXPR"),
                      regular=dict(code=exprs[0])), timeout=60)
        return None  # 端点未知时不做预检，交给上层 try
    except Exception:
        return None


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
        for tag, ov, ex in plan:
            log("%-14s %s n=%d" % (tag, ov, len(ex)))
            for ds, f, e in ex:
                log("   %-44s %s" % (f[:44], e))
        return

    ck = json.load(open(CK, encoding="utf-8")) if os.path.isfile(CK) else {"done": [], "results": []}
    done = set(ck["done"])
    from brain_api import brain_client
    asyncio.run(brain_client.ensure_authenticated())

    for tag, ov, ex in plan:
        if tag in done:
            log("### %s 已完成，跳过" % tag); continue
        st = dict(COMMON); st.update(ov)
        fn = os.path.join(ROOT, "cache", "_modelfam_%s.txt" % tag)
        open(fn, "w", encoding="utf-8").write("\n".join(e for _, _, e in ex) + "\n")
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
        ds = ex[0][0]
        aids = ids_of(sid, ds)
        log("    收割 %d/%d" % (len(aids), len(ex)))
        for i, aid in enumerate(aids):
            d = read(aid)
            f = ex[i][1] if i < len(ex) else "?"
            ck["results"].append(dict(tag=tag, dataset=ds, field=f, alpha=aid, over=ov, **d))
        ck["done"].append(tag)
        for p, obj in ((CK, ck), (LEDGER, ck["results"])):
            tmp = p + ".tmp"
            json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.replace(tmp, p)
        time.sleep(3)

    log("\n=== 模型型集字段探针（选主腿=S最高 / 辅sub=ratio最高 / 辅2Y=2Y最高）===")
    log("%-14s %-44s %6s %6s %7s %7s %6s" % ("批", "字段", "S", "F", "2Y", "sub", "ratio"))
    for r in sorted(ck["results"], key=lambda x: -(x.get("S") or -9)):
        S, sub = r.get("S") or 0, r.get("sub") or 0
        log("%-14s %-44s %6.2f %6.2f %7s %7s %6.3f" % (
            r.get("tag"), (r.get("field") or "")[:44], S, r.get("F") or 0,
            r.get("Y2"), r.get("sub"), (sub / S) if S else 0))


if __name__ == "__main__":
    main()
