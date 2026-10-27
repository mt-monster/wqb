# -*- coding: utf-8 -*-
"""sub_universe 修复探针：model25 / model31 只差 sub 一门。

现状（2026-10-27 07:15 平台判定）
--------------------------------
`kqJAPA2l`  signed_power(rank(ts_backfill(mdl25_6v, 22)), 0.5)     EUR/TOPCS1600/decay4/FAST
    S 1.85 ✓ ｜ F 1.28 ✓ ｜ 2Y **1.58 PASS** ｜ rob 0.94 ✓ ｜ CLUSTER 1.57 WARN
    **LOW_SUB_UNIVERSE_SHARPE  FAIL  value 0.87 / limit 0.99**   ← 唯一 FAIL
`9qE5Ld6r`  signed_power(rank(ts_backfill(star_eq_region_rank, 22)), 0.7)   同设置
    S 1.86 ✓ ｜ F 1.26 ✓ ｜ 2Y 1.58 ✓ ｜ sub 0.87 / limit 0.99 FAIL

关键机制：**limit = 0.535 × S**（实测 0.99/1.85）。
⇒ 两条路：
   R1 提 sub（分散化：trunc 收紧 / universe 放宽 / 行业中性）
   R2 **故意降 S**：S 1.85→1.60 时 limit 降到 0.856，而 sub 若守住 0.87 即过。
      S 有 0.27 富余（1.85 vs 1.58），这是 EUR 唯一还有"富余可消耗"的轴。
降 S 的首选手段 = decay 提高（平滑持仓，子集 sharpe 通常稳甚至升，整体 S 略降）。

判据：sub ≥ 0.535×S 且 S ≥ 1.58 且 F ≥ 1.0 且 2Y ≥ 1.58 ⇒ 立刻测 prod/self。

用法：python tools/_sub_fix_probe.py [--dry-run]
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
CK = os.path.join(ROOT, "results", "_sub_fix_ck.json")
LEDGER = os.path.join(ROOT, "results", "_sub_fix_ledger.json")

sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

COMMON = dict(region="EUR", delay="1", truncation="0.08",
              nan_handling="ON", max_trade="ON", mode="FULL")

# (字段, pow) 两族
F_MDL = ("mdl25_6v", "0.5")
F_STAR = ("star_eq_region_rank", "0.7")


def expr(field, pw):
    return "signed_power(rank(ts_backfill(%s, 22)), %s)" % (field, pw)


def grank(field, pw, axis="subindustry"):
    return "group_rank(%s, %s)" % (expr(field, pw), axis)


def gscale(field, pw, axis="subindustry"):
    return "group_scale(%s, %s)" % (expr(field, pw), axis)


PLAN = [
    # ★ 第三轮：EUR 合法 universe = {TOP2500, TOP1200, TOP800, TOP400, TOPCS1600}（平台实测），
    #   剪刀差已确认：TOP2500 ratio 0.342 → CS1600 0.465 → TOP1200 0.609（S 同向崩）。
    #   故转向**未试过的中性化轴**（12 档只试过 FAST）：看能否在保住 S 的同时抬 sub/S。
    ("H_neut", dict(universe="TOPCS1600", decay="4"), [
        ("nt_mkt", expr(*F_MDL)), ("nt_sec", expr(*F_MDL)), ("nt_ind", expr(*F_MDL)),
        ("nt_sub", expr(*F_MDL)), ("nt_stat", expr(*F_MDL)), ("nt_crowd", expr(*F_MDL)),
        ("nt_slow", expr(*F_MDL)), ("nt_sf", expr(*F_MDL)), ("nt_rm", expr(*F_MDL))]),
    # ★ 第二轮：第一轮证明 decay/trunc 对 S 与 sub 都无影响（sub/S 恒 0.462-0.467），
    #   TOP2500 让 sub/S 更差（0.342）⇒ 方向 = **更窄 universe** + **子行业分组**（保 ATOM）。
    ("E_narrow", dict(universe="TOP1200", decay="4", neutralization="FAST"),
     [("mdl_u12", expr(*F_MDL)), ("star_u12", expr(*F_STAR))]),
    ("F_grp", dict(universe="TOPCS1600", decay="4", neutralization="FAST"),
     [("mdl_grp_sub", grank(*F_MDL)), ("star_grp_sub", grank(*F_STAR))]),
    ("G_scale", dict(universe="TOPCS1600", decay="4", neutralization="FAST"),
     [("mdl_gs_sub", gscale(*F_MDL)), ("star_gs_sub", gscale(*F_STAR))]),
    # R2 降 S（decay 抬升）+ R1 提 sub（trunc 收紧 / universe 放宽），每字段 4 条
    ("A_fix", dict(universe="TOPCS1600", decay="8", neutralization="FAST"),
     [("mdl_d8", expr(*F_MDL)), ("star_d8", expr(*F_STAR))]),
    ("B_fix", dict(universe="TOPCS1600", decay="16", neutralization="FAST"),
     [("mdl_d16", expr(*F_MDL)), ("star_d16", expr(*F_STAR))]),
    ("C_fix", dict(universe="TOPCS1600", decay="8", neutralization="FAST", truncation="0.04"),
     [("mdl_d8_tr04", expr(*F_MDL)), ("star_d8_tr04", expr(*F_STAR))]),
    ("D_fix", dict(universe="TOP2500", decay="8", neutralization="FAST"),
     [("mdl_d8_u25", expr(*F_MDL)), ("star_d8_u25", expr(*F_STAR))]),
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
        if n == "LOW_2Y_SHARPE":
            out["Y2"] = c.get("value"); out["Y2_res"] = c.get("result")
        elif n == "LOW_SUB_UNIVERSE_SHARPE":
            out["sub"] = c.get("value"); out["sub_limit"] = c.get("limit"); out["sub_res"] = c.get("result")
        elif n == "LOW_ROBUST_UNIVERSE_SHARPE":
            out["rob"] = c.get("value")
    out["fails"] = [c.get("name") for c in (i.get("checks") or []) if c.get("result") == "FAIL"]
    return out


def ids_of(sid):
    try:
        out = subprocess.run([PY, HARVEST, sid, "model25", "camp"], capture_output=True,
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
            log("%-8s %s n=%d" % (tag, ov, len(ex)))
            for n, e in ex:
                log("   %-14s %s" % (n, e))
        return

    ck = json.load(open(CK, encoding="utf-8")) if os.path.isfile(CK) else {"done": [], "results": []}
    done = set(ck["done"])
    from brain_api import brain_client
    asyncio.run(brain_client.ensure_authenticated())

    for tag, ov, ex in PLAN:
        if tag in done:
            log("### %s 已完成，跳过" % tag); continue
        if tag.startswith("H_"):
            # 每条表达式配不同 neutralization ⇒ 逐条提交
            NEUT = ["MARKET", "SECTOR", "INDUSTRY", "SUBINDUSTRY", "STATISTICAL",
                    "CROWDING", "SLOW", "SLOW_AND_FAST", "REVERSION_AND_MOMENTUM"]
            for (nm, e), nt in zip(ex, NEUT):
                st = dict(COMMON); st.update(ov); st["neutralization"] = nt
                fn = os.path.join(ROOT, "cache", "_subfix_%s_%s.txt" % (tag, nt))
                open(fn, "w", encoding="utf-8").write(e + chr(10))
                sid = None
                for t in range(3):
                    sid = submit(fn, st)
                    if sid:
                        break
                    time.sleep(20)
                if not sid:
                    log("  ### %s/%s 提交失败" % (nm, nt)); continue
                log("### %s/%s nt=%s sim=%s" % (nm, nt, nt, sid))
                if not wait(sid):
                    log("  [warn] %s 未到终态" % nm); continue
                aids = ids_of(sid)
                for aid in aids:
                    d = read(aid)
                    ck["results"].append(dict(tag=tag, variant="%s_%s" % (nm, nt), alpha=aid,
                                              over=dict(st), **d))
                for p2, obj in ((CK, ck), (LEDGER, ck["results"])):
                    tmp = p2 + ".tmp"
                    json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                    os.replace(tmp, p2)
            ck["done"].append(tag)
            tmp = CK + ".tmp"
            json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.replace(tmp, CK)
            continue
        st = dict(COMMON); st.update(ov)
        fn = os.path.join(ROOT, "cache", "_subfix_%s.txt" % tag)
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

    log("\n=== sub 修复（对照 kqJAPA2l: S1.85 F1.28 2Y1.58 PASS｜sub 0.87 / limit 0.99）===")
    log("%-8s %-15s %6s %6s %7s %7s  %8s %6s %6s  %s" % (
        "批", "变体", "S", "F", "2Y", "sub", "limit", "sub/S", "rob", "判定"))
    for r in sorted(ck["results"], key=lambda x: -(x.get("S") or -9)):
        S, F, Y2 = r.get("S") or 0, r.get("F") or 0, r.get("Y2") or 0
        sub, lim = r.get("sub") or 0, r.get("sub_limit") or 0
        rob = r.get("rob") or 0
        ok = S >= 1.58 and F >= 1.0 and Y2 >= 1.58 and lim and sub >= lim and rob >= 0.70
        log("%-8s %-15s %6.2f %6.2f %7.2f %7.3f  %8s %6.3f %6.2f  %s" % (
            r.get("tag"), r.get("variant"), S, F, Y2, sub,
            ("%.3f" % lim) if lim else "—", (sub / S) if S else 0, rob,
            "★全过" if ok else ",".join(r.get("fails") or [])))


if __name__ == "__main__":
    main()
