# -*- coding: utf-8 -*-
"""sentiment26 补 S 探针：只要 +0.04。

现状（wp99v7qv，平台判定）
-------------------------
    if_else(greater(rank(dw), 0.85), dw, 0)
    dw = multiply(rank(ts_mean(ts_backfill(vec_sum(snt26_relpopularity1), 22), 5)),
                  rank(ts_mean(ts_backfill(vec_sum(snt26_relpopularity1), 22), 66)))
    TOPCS1600 / decay 4 / FAST / trunc 0.08

    唯一 FAIL：**LOW_SHARPE 1.54 / limit 1.58**
    全 PASS：F 1.12 ｜ 2Y 1.94 ｜ **rob 0.92** ｜ sub 1.14 ｜ TO 3.56% ｜ margin **36.8bp**
    非 FAIL：CLUSTER_TEST 1.39 WARNING

已得的门控单调性：gate 0.80 → S 1.46；gate 0.85 → **S 1.54**
⇒ 更稀疏应继续抬 S。本轮扫 0.875 / 0.90 / 0.925 + 去门控 + decay/宇宙。

判据：S ≥ 1.58 且 2Y ≥ 1.58 且 rob ≥ 0.70 ⇒ 立刻测 prod/self（那才是最后一关）。

用法：python tools/_snt26_probe.py [--dry-run]
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
CK = os.path.join(ROOT, "results", "_snt26_ck.json")
LEDGER = os.path.join(ROOT, "results", "_snt26_ledger.json")

sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

F = "vec_sum(snt26_relpopularity1)"
DW = ("multiply(rank(ts_mean(ts_backfill(%s, 22), 5)), "
      "rank(ts_mean(ts_backfill(%s, 22), 66)))" % (F, F))

COMMON = dict(region="EUR", delay="1", truncation="0.08",
              nan_handling="ON", max_trade="ON", mode="FULL")

def _dwf(field, ws=3, wl=66):
    e = "vec_sum(%s)" % field
    return ("multiply(rank(ts_mean(ts_backfill(%s, 22), %d)), "
            "rank(ts_mean(ts_backfill(%s, 22), %d)))" % (e, ws, e, wl))


def _gate(field, q="0.85", ws=3, wl=66):
    d = _dwf(field, ws, wl)
    return "if_else(greater(rank(%s), %s), %s, 0)" % (d, q, d)


SIG = _gate("snt26_relpopularity1")          # = JjejYA3e 的主体
DOM = "vec_sum(snt26_totaldomains)"
RANK = "vec_sum(snt26_avgranking)"

PLAN = [
    # ★ 第六轮（02:25）：热度类两字段 prod 都 0.75~0.77（机制地板）⇒ 换到**分布统计类**字段
    #   （kurtosis / skewness / dltcc / top10pct），机制不同 ⇒ prod 相关性应更低
    ("M_dist", dict(universe="TOPCS1600", decay="1", neutralization="FAST"),
     [("kurt", _gate("snt26_kurtosis")),
      ("skew", _gate("snt26_skewness")),
      ("dltcc", _gate("snt26_dltcc")),
      ("top10", _gate("snt26_top10pctranking"))]),
    # ★ 第五轮（02:10）：prod 0.7534 是机制地板（两字段 0.7534/0.7657，Δ0.012）
    #   最后一条真降法 = **改何时交易**（§6），且用同集字段做门控以保 ATOM=1
    ("L_timing", dict(universe="TOPCS1600", decay="1", neutralization="FAST"),
     [("tw_domvol", "trade_when(greater(rank(ts_std_dev(ts_backfill(%s, 22), 20)), 0.30), %s, -1)" % (DOM, SIG)),
      ("tw_domlvl", "trade_when(greater(rank(ts_mean(ts_backfill(%s, 22), 5)), 0.40), %s, -1)" % (DOM, SIG)),
      ("tw_rkvol", "trade_when(greater(rank(ts_std_dev(ts_backfill(%s, 22), 20)), 0.30), %s, -1)" % (RANK, SIG)),
      ("tw_domvol4", "trade_when(greater(rank(ts_std_dev(ts_backfill(%s, 22), 20)), 0.45), %s, -1)" % (DOM, SIG))]),
    # ★ 第四轮（01:40）：prod 0.7534 单点对手 ⇒ 换字段（同源副本优先）
    ("K_field", dict(universe="TOPCS1600", decay="1", neutralization="FAST"),
     [("relpop08", _gate("snt26_relpopularity08")),
      ("avgrank", _gate("snt26_avgranking")),
      ("top25rk", _gate("snt26_top25pctranking")),
      ("top50avg", _gate("snt26_top50pctrankingavg"))]),
    # ★ 第三轮（01:20）：只差 0.02，门控 0.85 尖峰附近细扫 + decay0 + 短窗
    ("G_fine", dict(universe="TOPCS1600", decay="1", neutralization="FAST"),
     [("g840", "if_else(greater(rank(%s), 0.840), %s, 0)" % (DW, DW)),
      ("g855", "if_else(greater(rank(%s), 0.855), %s, 0)" % (DW, DW)),
      ("g860", "if_else(greater(rank(%s), 0.860), %s, 0)" % (DW, DW)),
      ("w3_66", "if_else(greater(rank(multiply(rank(ts_mean(ts_backfill(%s, 22), 3)), rank(ts_mean(ts_backfill(%s, 22), 66)))), 0.85), multiply(rank(ts_mean(ts_backfill(%s, 22), 3)), rank(ts_mean(ts_backfill(%s, 22), 66))), 0)" % (F, F, F, F))]),
    ("H_decay0", dict(universe="TOPCS1600", decay="0", neutralization="FAST"),
     [("d0_g850", "if_else(greater(rank(%s), 0.85), %s, 0)" % (DW, DW)),
      ("d0_g855", "if_else(greater(rank(%s), 0.855), %s, 0)" % (DW, DW))]),
    # ★ 第二轮（01:30）：门控/宇宙已到极限，试 truncation / decay1 / 长窗口，只要 +0.03
    ("D_tr004", dict(universe="TOPCS1600", decay="2", neutralization="FAST", truncation="0.04"),
     [("tr004_g850", "if_else(greater(rank(%s), 0.85), %s, 0)" % (DW, DW)),
      ("tr004_g875", "if_else(greater(rank(%s), 0.875), %s, 0)" % (DW, DW))]),
    ("E_tr002", dict(universe="TOPCS1600", decay="2", neutralization="FAST", truncation="0.02"),
     [("tr002_g850", "if_else(greater(rank(%s), 0.85), %s, 0)" % (DW, DW)),
      ("tr002_g875", "if_else(greater(rank(%s), 0.875), %s, 0)" % (DW, DW))]),
    ("F_d1_w126", dict(universe="TOPCS1600", decay="1", neutralization="FAST"),
     [("d1_g850", "if_else(greater(rank(%s), 0.85), %s, 0)" % (DW, DW)),
      ("w126_g850", "if_else(greater(rank(multiply(rank(ts_mean(ts_backfill(%s, 22), 5)), rank(ts_mean(ts_backfill(%s, 22), 126)))), 0.85), multiply(rank(ts_mean(ts_backfill(%s, 22), 5)), rank(ts_mean(ts_backfill(%s, 22), 126))), 0)" % (F, F, F, F))]),
    ("A_gate", dict(universe="TOPCS1600", decay="4", neutralization="FAST"),
     [("g875", "if_else(greater(rank(%s), 0.875), %s, 0)" % (DW, DW)),
      ("g900", "if_else(greater(rank(%s), 0.900), %s, 0)" % (DW, DW)),
      ("g925", "if_else(greater(rank(%s), 0.925), %s, 0)" % (DW, DW)),
      ("nogate", DW)]),
    ("B_decay", dict(universe="TOPCS1600", decay="2", neutralization="FAST"),
     [("g850_d2", "if_else(greater(rank(%s), 0.85), %s, 0)" % (DW, DW)),
      ("g900_d2", "if_else(greater(rank(%s), 0.900), %s, 0)" % (DW, DW))]),
    ("C_univ", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("g850_u25", "if_else(greater(rank(%s), 0.85), %s, 0)" % (DW, DW)),
      ("g900_u25", "if_else(greater(rank(%s), 0.900), %s, 0)" % (DW, DW))]),
]


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
        elif n == "LOW_SUB_UNIVERSE_SHARPE": out["sub"] = c.get("value")
        elif n == "LOW_ROBUST_UNIVERSE_SHARPE": out["rob"] = c.get("value")
    out["fails"] = [c.get("name") for c in (i.get("checks") or []) if c.get("result") == "FAIL"]
    return out


def ids_of(sid):
    try:
        out = subprocess.run([PY, HARVEST, sid, "sentiment26", "camp"], capture_output=True,
                             text=True, timeout=600, cwd=ROOT).stdout
    except Exception:
        return []
    return [m.group(1) for m in (re.match(r"\s*\+\s+(\w+)\s+S=", ln) for ln in out.splitlines()) if m]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.dry_run:
        for tag, ov, ex in PLAN:
            log("%-9s %s n=%d" % (tag, ov, len(ex)))
        return

    ck = json.load(open(CK, encoding="utf-8")) if os.path.isfile(CK) else {"done": [], "results": []}
    done = set(ck["done"])
    from brain_api import brain_client
    asyncio.run(brain_client.ensure_authenticated())

    for tag, ov, ex in PLAN:
        if tag in done:
            log("### %s 已完成，跳过" % tag); continue
        st = dict(COMMON); st.update(ov)
        fn = os.path.join(ROOT, "cache", "_snt26_%s.txt" % tag)
        open(fn, "w", encoding="utf-8").write("\n".join(e for _, e in ex) + "\n")
        sid = None
        for t in range(3):
            sid = submit(fn, st)
            if sid:
                break
            log("  [retry] %s 第 %d 次失败，等 30s" % (tag, t + 1)); time.sleep(30)
        if not sid:
            log("### %s 三次均失败" % tag); continue
        log("### %s n=%d %s sim=%s" % (tag, len(ex), ov, sid))
        if not wait(sid):
            log("  [warn] %s 未到终态" % tag); continue
        aids = ids_of(sid)
        log("    收割 %d/%d" % (len(aids), len(ex)))
        for i, aid in enumerate(aids):
            d = read(aid)
            name = ex[i][0] if i < len(ex) else "?"
            ck["results"].append(dict(tag=tag, variant=name, alpha=aid, over=ov, **d))
        ck["done"].append(tag)
        for p, obj in ((CK, ck), (LEDGER, ck["results"])):
            tmp = p + ".tmp"
            json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.replace(tmp, p)
        time.sleep(3)

    log("\n=== sentiment26 探针（对照 wp99v7qv: S1.54 F1.12 2Y1.94 rob0.92 sub1.14）===")
    log("%-8s %-9s %6s %6s %7s %6s %6s %7s  %s" % ("批","变体","S","F","2Y","sub","rob","TO","判定"))
    for r in sorted(ck["results"], key=lambda x: -(x.get("S") or -9)):
        S, F, Y2 = r.get("S") or 0, r.get("F") or 0, r.get("Y2") or 0
        sub, rob = r.get("sub") or 0, r.get("rob") or 0
        ok = S >= 1.58 and F >= 1.0 and Y2 >= 1.58 and rob >= 0.70 and sub >= 0.53 * S
        log("%-8s %-9s %6.2f %6.2f %7.2f %6.2f %6.2f %7.3f  %s" % (
            r.get("tag"), r.get("variant"), S, F, Y2, sub, rob, r.get("TO") or 0,
            "★全过" if ok else ",".join(r.get("fails") or [])))


if __name__ == "__main__":
    main()
