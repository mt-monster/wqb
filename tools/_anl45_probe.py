# -*- coding: utf-8 -*-
"""analyst45 三门修复探针：S 1.28 / F 0.63 / robust 0.41。

已知（get_alpha_details, mLYWlvZp）
----------------------------------
    code  = rank(ts_backfill(vec_avg(anl45_net_market_exposure), 252))
    S 1.28 (limit 1.58) ｜ F 0.63 (limit 1.0) ｜ **robust 0.41 (limit 0.7, fail)**
    TO 7.06% ｜ returns 2.99% ｜ margin 8.5bp ｜ sub 0.79 ｜ 2Y 2.77

三个缺口各有对应杠杆，本轮每个杠杆单独一批（每批 2 条，避开单条空批）：

| 批 | 改动 | 想修什么 | 依据 |
|---|---|---|---|
| A | universe → **TOP2500** | robust（+ 可能 S/2Y） | other335 从 TOPCS1600→TOP2500 后 S 1.59→1.83、2Y 1.30→1.70 |
| B | decay 4 → **8** | F（TO↓ ⇒ F/S↑） | F/S 现 0.492，需 0.633；TO 降 40% 可补足 |
| C | neutralization → **SLOW_AND_FAST** | S | r28 实测 S +0.23 / 2Y −0.31（2Y 有 1.19 余量） |

同时每批都带一条 `signed_power(base, 0.5)`（今日 other335：指数↓ ⇒ S↑、2Y↓），
共 6 条 / 3 批。

⚠ 判死预判：robust 与 S 严格负相关（memory §3）。若 A 批 TOP2500 不能把 robust 抬过 0.7，
   而 C 批又把 robust 压低 ⇒ 该集应按「三门互斥」封闭，不再投入。

用法：python tools/_anl45_probe.py [--dry-run]
"""
import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
SUBMIT = os.path.join(ROOT, "tools", "submit_batch.py")
HARVEST = os.path.join(ROOT, "cache", "_harvest_safe.py")
CK = os.path.join(ROOT, "results", "_anl45_ck.json")
LEDGER = os.path.join(ROOT, "results", "_anl45_ledger.json")

sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

BASE = "rank(ts_backfill(vec_avg(anl45_net_market_exposure), 252))"
SP5 = "signed_power(rank(ts_backfill(vec_avg(anl45_net_market_exposure), 252)), 0.5)"

COMMON = dict(region="EUR", delay="1", truncation="0.08",
              nan_handling="ON", max_trade="ON", mode="FULL")

PLAN = [
    ("A_u2500", dict(universe="TOP2500", decay="4", neutralization="FAST")),
    ("B_decay8", dict(universe="TOPCS1600", decay="8", neutralization="FAST")),
    ("C_slowfast", dict(universe="TOPCS1600", decay="4", neutralization="SLOW_AND_FAST")),
]
EXPRS = [("base", BASE), ("sp05", SP5)]


def log(m):
    print(m, flush=True)


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
        log("  [submit] 异常 %s" % ex)
        return None
    m = re.search(r"/simulations/([A-Za-z0-9]+)", out)
    if not m:
        log("  [submit] 失败 %s" % out.strip().splitlines()[-3:])
        return None
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
            # ★ 单条表达式会建**单仿真**（children=0），COMPLETE 时必须返回 True。
            #   2026-10-27 踩过：只判 ERROR/FAIL/CANCELLED ⇒ COMPLETE 也继续 sleep，
            #   空转 27 分钟（110 轮 × 15s），仿真早完成但收不到结果。
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


def detail(aid):
    """直接读 alpha 详情（robust 只在 details 里）。"""
    from brain_api import brain_client
    try:
        j = brain_client.session.get("%s/alphas/%s" % (brain_client.base_url, aid), timeout=30).json()
    except Exception:
        return None
    i = j.get("is") or {}
    m = j.get("metrics") or {}
    return dict(S=m.get("sharpe", i.get("sharpe")), F=m.get("fitness", i.get("fitness")),
                Y2=m.get("two_year_sharpe"), sub=m.get("sub_universe_sharpe"),
                rob=m.get("robust_universe_sharpe"), TO=m.get("turnover"))


def harvest(sid):
    try:
        out = subprocess.run([PY, HARVEST, sid, "analyst45", "camp"], capture_output=True,
                             text=True, timeout=600, cwd=ROOT).stdout
    except Exception:
        return []
    ids = []
    for ln in out.splitlines():
        m = re.match(r"\s*\+\s+(\w+)\s+S=", ln)
        if m:
            ids.append(m.group(1))
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.dry_run:
        for tag, ov in PLAN:
            log("%-12s %s  n=%d" % (tag, ov, len(EXPRS)))
        log("base = " + BASE)
        return

    ck = json.load(open(CK, encoding="utf-8")) if os.path.isfile(CK) else {"done": [], "results": []}
    done = set(ck["done"])
    from brain_api import brain_client
    asyncio.run(brain_client.ensure_authenticated())

    for tag, ov in PLAN:
        if tag in done:
            log("### %s 已完成，跳过" % tag)
            continue
        st = dict(COMMON); st.update(ov)
        fn = os.path.join(ROOT, "cache", "_anl45_%s.txt" % tag)
        open(fn, "w", encoding="utf-8").write("\n".join(e for _, e in EXPRS) + "\n")
        sid = None
        for t in range(3):
            sid = submit(fn, st)
            if sid:
                break
            log("  [retry] %s 第 %d 次失败，等 30s" % (tag, t + 1)); time.sleep(30)
        if not sid:
            log("### %s 三次均失败，跳过" % tag); continue
        log("### %s n=%d %s sim=%s" % (tag, len(EXPRS), ov, sid))
        if not wait(sid):
            log("  [warn] %s 未到终态" % tag); continue
        ids = harvest(sid)
        log("    收割 %d/%d" % (len(ids), len(EXPRS)))
        for i, aid in enumerate(ids):
            d = detail(aid) or {}
            name = EXPRS[i][0] if i < len(EXPRS) else "?"
            ck["results"].append(dict(tag=tag, variant=name, alpha=aid, over=ov, **d))
        ck["done"].append(tag)
        for p, obj in ((CK, ck), (LEDGER, ck["results"])):
            tmp = p + ".tmp"
            json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.replace(tmp, p)
        time.sleep(3)

    log("\n=== analyst45 探针（对照 base: S1.28 / F0.63 / 2Y2.77 / sub0.79 / rob0.41 / TO7.06%）===")
    log("%-12s %-6s %6s %6s %7s %7s %7s %7s  %s" % ("批", "变体", "S", "F", "2Y", "sub", "rob", "TO", "闸"))
    for r in sorted(ck["results"], key=lambda x: -(x.get("S") or -9)):
        S = r.get("S") or 0; F = r.get("F") or 0; Y2 = r.get("Y2") or 0
        sub = r.get("sub") or 0; rob = r.get("rob") or 0
        ok = (S >= 1.58 and F >= 1.0 and Y2 >= 1.58 and rob >= 0.7 and sub >= 0.53 * S)
        tag = "★全过" if ok else ("rob✗" if rob < 0.7 else ("S✗" if S < 1.58 else ("F✗" if F < 1.0 else "")))
        log("%-12s %-6s %6.2f %6.2f %7.2f %7.2f %7.2f %7.3f  %s" % (
            r.get("tag"), r.get("variant"), S, F, Y2, sub, rob, r.get("TO") or 0, tag))


if __name__ == "__main__":
    main()
