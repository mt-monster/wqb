# -*- coding: utf-8 -*-
"""r24：对 KPmV08Vx（S1.48/F0.76/2Y1.78/sub0.86/prod0.5583）做**单因子**设置/结构扫。

为什么是这颗
------------
ai_equity_alpha 里 prod 唯一有大量余量的一颗：prod 0.5583（离 0.70 还有 0.14）。
缺口只有 S(+0.10) 与 F(+0.24)，而 F = S·sqrt(|ret|/max(TO,0.125))，抬 S 会连带抬 F。
⇒ 可以承受「抬 S 但顺带升 prod」的手段，这正是 fundamental23 做不到的。

为什么现在才扫
--------------
主战役的 settings_sweep 触发条件按**集级 max_s**∈[1.2,1.58) 判；
ai_equity_alpha 的 max_s=1.62（ALIVE）⇒ 扫被跳过，而这颗真正在带内的 alpha 从未被扫过。
（流水线缺陷，已记录。）

设计：每次只改一维（对照 = 原株 FAST/TOPCS1600/decay4/ts_rank126/group_rank(market)）
输出：logs/r24_sweep.log ＋ results/eur_r24_ledger.json
"""
import asyncio
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # tools/*.py -> 仓库根，勿写死盘符
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
SB = os.path.join(ROOT, "tools", "submit_batch.py")
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
from brain_api import brain_client  # noqa: E402

F = "ts_backfill(vec_avg(financial_statement_volatility_factor), 22)"

# 基线（实测）：S 1.48 / F 0.76 / 2Y 1.78 / sub 0.86 / prod 0.5583
BASE = dict(universe="TOPCS1600", decay="4", neutralization="FAST")

VARIANTS = [
    # name, expression, settings override
    ("w63",   "group_rank(ts_rank({F}, 63), market)".format(F=F), {}),
    ("w252",  "group_rank(ts_rank({F}, 252), market)".format(F=F), {}),
    ("d8",    "group_rank(ts_rank({F}, 126), market)".format(F=F), {"decay": "8"}),
    ("d2",    "group_rank(ts_rank({F}, 126), market)".format(F=F), {"decay": "2"}),
    ("gsec",  "group_rank(ts_rank({F}, 126), sector)".format(F=F), {}),
    ("gsub",  "group_rank(ts_rank({F}, 126), subindustry)".format(F=F), {}),
]

TERM = ("COMPLETE", "ERROR", "FAIL", "CANCELLED")


def log(m):
    print(m, flush=True)


def write_expr(name, expr):
    p = os.path.join(ROOT, "tracking", "EUR", "runs", "r24_" + name + ".txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("# r24 单因子扫：{}\n# 对照=KPmV08Vx（FAST/TOPCS1600/decay4/ts_rank126/group_rank(market)）\n".format(name))
        fh.write(expr + "\n")
    return p


def submit(path, over):
    st = dict(BASE)
    st.update(over)
    cmd = [PY, SB, "--path", path, "--region", "EUR", "--universe", st["universe"],
           "--delay", "1", "--decay", st["decay"], "--neutralization", st["neutralization"],
           "--truncation", "0.08", "--max-trade", "ON", "--nan-handling", "ON",
           "--simulation-mode", "FULL"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    sids = list(dict.fromkeys(re.findall(r"/simulations/([A-Za-z0-9]+)", r.stdout)))
    if not sids:
        log("    SUBMIT FAIL " + (r.stdout or r.stderr)[-250:])
    return sids, st


def poll(sids, tag, rounds=120):
    got = set()
    for _ in range(rounds):
        done = True
        for sid in sids:
            j = brain_client.session.get("{}/simulations/{}".format(brain_client.base_url, sid)).json()
            if not isinstance(j, dict):
                done = False
                continue
            kids = j.get("children")
            if kids:
                objs = [brain_client.session.get("{}/simulations/{}".format(brain_client.base_url, k)).json() for k in kids]
                if not all(isinstance(x, dict) and x.get("status") in TERM for x in objs):
                    done = False
                for x in objs:
                    if isinstance(x, dict) and x.get("status") == "COMPLETE" and x.get("alpha"):
                        got.add(x["alpha"])
            else:
                st = j.get("status")
                if st in TERM:
                    if st == "COMPLETE" and j.get("alpha"):
                        got.add(j["alpha"])
                else:
                    done = False
        if done:
            return sorted(got)
        time.sleep(15)
    log("[{}] TIMEOUT".format(tag))
    return sorted(got)


def metr(aid):
    j = brain_client.session.get("{}/alphas/{}".format(brain_client.base_url, aid)).json()
    i = j.get("is") or {}
    chk = {c.get("name"): c.get("value") for c in (i.get("checks") or [])}
    return {"S": i.get("sharpe"), "F": i.get("fitness"),
            "Y2": chk.get("LOW_2Y_SHARPE"), "sub": chk.get("LOW_SUB_UNIVERSE_SHARPE"),
            "rob": chk.get("LOW_ROBUST_UNIVERSE_SHARPE"), "TO": i.get("turnover"),
            "margin": i.get("margin")}


def main():
    asyncio.run(brain_client.ensure_authenticated())
    sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".workbuddy",
                                    "skills", "wq-brain-ra-eur", "scripts"))
    os.environ.setdefault("WQB_REPO_ROOT", ROOT)
    from wqb_campaign.audit import check_prod  # noqa: E402

    ledger = []
    for i in range(0, len(VARIANTS), 2):          # 并发 2
        batch = VARIANTS[i:i + 2]
        for name, expr, over in batch:
            p = write_expr(name, expr)
            sids, st = submit(p, over)
            log("### {} settings={} sims={}".format(name, st, sids))
            for aid in poll(sids, name):
                m = metr(aid)
                try:
                    m["prod"] = check_prod(aid)
                except Exception as exc:  # noqa: BLE001
                    m["prod"] = None
                    log("   prod ERR {}".format(type(exc).__name__))
                ledger.append({"variant": name, "settings": st, "alpha": aid, **m})
                log("    {} S={} F={} 2Y={} sub={} rob={} TO={} prod={} margin={}".format(
                    aid, m["S"], m["F"], m["Y2"], m["sub"], m["rob"], m["TO"], m["prod"], m["margin"]))
        time.sleep(3)

    log("")
    log("=== 归因（对照 KPmV08Vx: S1.48 F0.76 2Y1.78 sub0.86 prod0.5583）===")
    for r in ledger:
        log("  {:<5} dS {:+.2f} | dF {:+.2f} | d2Y {:+.2f} | prod {} {}".format(
            r["variant"], (r["S"] or 0) - 1.48, (r["F"] or 0) - 0.76, (r["Y2"] or 0) - 1.78,
            r["prod"], "✓" if (r["prod"] is not None and r["prod"] < 0.7) else "✗"))

    out = os.path.join(ROOT, "results", "eur_r24_ledger.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(ledger, fh, ensure_ascii=False, indent=1)
    log("LEDGER " + out)


main()
