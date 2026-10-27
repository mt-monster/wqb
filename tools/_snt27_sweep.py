# -*- coding: utf-8 -*-
"""sentiment27 定向波：验证 sentiment26 的配方能否移植（兄弟集）。

背景（2026-10-27 03:00 结论）
----------------------------
sentiment26 的唯一过闸形态 `JjejYA3e`：
    if_else(greater(rank(dw), 0.85), dw, 0)
    dw = multiply(rank(ts_mean(backfill(vec_sum(snt26_relpopularity1),22), WS=3)),
                  rank(ts_mean(backfill(...,22), 66)))
    EUR / TOPCS1600 / decay 1 / FAST / trunc 0.08   → S 1.60 / F 1.18 / 2Y 1.92 / rob 0.98
    prod 0.7534（单点对手）⇒ sentiment26 封闭。

两条杠杆（本轮要验证能否移植）：
  L1 **短窗 WS 5→3**：S 1.54→1.60，且 F/2Y/rob/sub 五项同步改善（不是此消彼长）
  L2 **门控甜点极窄**：0.80→1.46 ｜ 0.85→1.54 ｜ 0.875→1.38（±0.025 掉 0.16）

sentiment27 是兄弟集：30 字段全 VECTOR、cov 1.00、字段名与 snt26 同名同源
（relpopularity1 / relpopularity08 / avgranking / top50pctranking / totaldomains…）。
旧 campaign 最强只有 pp 1.31（且样本 2019 起、fragile）—— **从未试过这套配方**。

本波只做 pilot：4 字段 × {WS 3, 5}，先回答「同源吗 / WS 杠杆成立吗 / relpop08 排序如何」。
判据：任一 (S≥1.58 且 F≥1.0 且 2Y≥1.58 且 rob≥0.70) ⇒ 立刻测 prod/self。

用法：python tools/_snt27_sweep.py [--dry-run]
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
CK = os.path.join(ROOT, "results", "_snt27_ck.json")
LEDGER = os.path.join(ROOT, "results", "_snt27_ledger.json")

sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

DS = "sentiment27"
COMMON = dict(region="EUR", delay="1", truncation="0.08",
              nan_handling="ON", max_trade="ON", mode="FULL")


def _dwf(field, ws=3, wl=66, ds=DS):
    e = "vec_sum(%s)" % field
    return ("multiply(rank(ts_mean(ts_backfill(%s, 22), %d)), "
            "rank(ts_mean(ts_backfill(%s, 22), %d)))" % (e, ws, e, wl))


def _gate(field, q="0.85", ws=3, wl=66, ds=DS):
    d = _dwf(field, ws, wl, ds)
    return "if_else(greater(rank(%s), %s), %s, 0)" % (d, q, d)


def P(field, **kw):
    return _gate("%s_%s" % (DS.replace("sentiment", "snt"), field), **kw)


PLAN = [
    # pilot：只要 3 个判断 —— 同源性 / WS 杠杆 / relpop08 排序
    ("P1_pilot", dict(universe="TOPCS1600", decay="1", neutralization="FAST"),
     [("rp1_ws3_g850", P("relpopularity1")),
      ("rp1_ws5_g850", P("relpopularity1", ws=5)),
      ("rp08_ws3_g850", P("relpopularity08")),
      ("avgrk_ws3_g850", P("avgranking")),
      ("top50avg_ws3_g850", P("top50pctrankingavg")),
      ("rp1_ws2_g850", P("relpopularity1", ws=2))]),
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
        out = subprocess.run([PY, HARVEST, sid, DS, "camp"], capture_output=True,
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
            for n, e in ex:
                log("   %-18s %s" % (n, e[:120]))
        return

    ck = json.load(open(CK, encoding="utf-8")) if os.path.isfile(CK) else {"done": [], "results": []}
    done = set(ck["done"])
    from brain_api import brain_client
    asyncio.run(brain_client.ensure_authenticated())

    for tag, ov, ex in PLAN:
        if tag in done:
            log("### %s 已完成，跳过" % tag); continue
        st = dict(COMMON); st.update(ov)
        fn = os.path.join(ROOT, "cache", "_snt27_%s.txt" % tag)
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

    log("\n=== sentiment27 pilot（对照 snt26 JjejYA3e: S1.60 F1.18 2Y1.92 rob0.98 sub1.21）===")
    log("%-9s %-19s %6s %6s %7s %6s %6s %7s  %s" % ("批", "变体", "S", "F", "2Y", "sub", "rob", "TO", "判定"))
    for r in sorted(ck["results"], key=lambda x: -(x.get("S") or -9)):
        S, F, Y2 = r.get("S") or 0, r.get("F") or 0, r.get("Y2") or 0
        sub, rob = r.get("sub") or 0, r.get("rob") or 0
        ok = S >= 1.58 and F >= 1.0 and Y2 >= 1.58 and rob >= 0.70 and sub >= 0.53 * S
        log("%-9s %-19s %6.2f %6.2f %7.2f %6.2f %6.2f %7.4f  %s" % (
            r.get("tag"), r.get("variant"), S, F, Y2, sub, rob, r.get("TO") or 0,
            "★全过" if ok else ",".join(r.get("fails") or [])))


if __name__ == "__main__":
    main()
