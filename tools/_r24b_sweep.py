# -*- coding: utf-8 -*-
"""r24b：KPmV08Vx 单因子扫（剩余 5 个变体）。每完成一个变体就增量落 ledger，
避免进程被回收时丢结果。

对照（实测 KPmV08Vx）：S 1.48 / F 0.76 / 2Y 1.78 / sub 0.86 / prod 0.5583
已完成：w63 -> A1QAR6kl（ts_rank 126→63）
"""
import asyncio
import json
import os
import re
import subprocess
import sys
import time

def _bootstrap_src():
    """把 `src/` 放上 sys.path：向上探测双标记，与文件层数无关（AGENTS.md §8.13）。

    2026-10-27：此前本文件把仓库根写死成 `D:\\coding\\...`（S4 硬编码盘符），
    换机 / 换目录即静默指错。
    """
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(here, "pyproject.toml")) and os.path.isdir(
                os.path.join(here, "src", "wqb")):
            src = os.path.join(here, "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
        parent = os.path.dirname(here)
        if parent == here:
            raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")
        here = parent


_bootstrap_src()
from wqb.paths import find_repo_root  # noqa: E402

ROOT = str(find_repo_root(__file__))
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
SB = os.path.join(ROOT, "tools", "submit_batch.py")
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
from brain_api import brain_client  # noqa: E402

F = "ts_backfill(vec_avg(financial_statement_volatility_factor), 22)"
BASE = dict(universe="TOPCS1600", decay="4", neutralization="FAST")
VARIANTS = [
    ("w252", "group_rank(ts_rank({F}, 252), market)".format(F=F), {}),
    ("d8",   "group_rank(ts_rank({F}, 126), market)".format(F=F), {"decay": "8"}),
    ("d2",   "group_rank(ts_rank({F}, 126), market)".format(F=F), {"decay": "2"}),
    ("gsec", "group_rank(ts_rank({F}, 126), sector)".format(F=F), {}),
    ("gsub", "group_rank(ts_rank({F}, 126), subindustry)".format(F=F), {}),
]
TERM = ("COMPLETE", "ERROR", "FAIL", "CANCELLED")
LEDGER = os.path.join(ROOT, "results", "eur_r24_ledger.json")


def log(m):
    print(m, flush=True)


def save(rows):
    with open(LEDGER + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1)
    os.replace(LEDGER + ".tmp", LEDGER)


def load():
    try:
        with open(LEDGER, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return []


def write_expr(name, expr):
    p = os.path.join(ROOT, "tracking", "EUR", "runs", "r24_" + name + ".txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("# r24 单因子：{}\n".format(name))
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


def poll(sids, tag, rounds=100):
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
    return {"S": i.get("sharpe"), "F": i.get("fitness"), "Y2": chk.get("LOW_2Y_SHARPE"),
            "sub": chk.get("LOW_SUB_UNIVERSE_SHARPE"),
            "rob": chk.get("LOW_ROBUST_UNIVERSE_SHARPE"),
            "TO": i.get("turnover"), "margin": i.get("margin")}


def main():
    asyncio.run(brain_client.ensure_authenticated())
    sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".workbuddy",
                                    "skills", "wq-brain-ra-eur", "scripts"))
    os.environ.setdefault("WQB_REPO_ROOT", ROOT)
    from wqb_campaign.audit import check_prod  # noqa: E402

    rows = load()
    # 先补 w63（已完成的 alpha）
    if not any(r.get("variant") == "w63" for r in rows):
        m = metr("A1QAR6kl")
        try:
            m["prod"] = check_prod("A1QAR6kl")
        except Exception:  # noqa: BLE001
            m["prod"] = None
        rows.append({"variant": "w63", "alpha": "A1QAR6kl", "settings": BASE, **m})
        save(rows)
        log("w63(补) S={} F={} 2Y={} sub={} prod={}".format(m["S"], m["F"], m["Y2"], m["sub"], m["prod"]))

    for i in range(0, len(VARIANTS), 2):        # 并发 2
        for name, expr, over in VARIANTS[i:i + 2]:
            p = write_expr(name, expr)
            sids, st = submit(p, over)
            log("### {} settings={} sims={}".format(name, st, sids))
            for aid in poll(sids, name):
                m = metr(aid)
                try:
                    m["prod"] = check_prod(aid)
                except Exception:  # noqa: BLE001
                    m["prod"] = None
                rows.append({"variant": name, "alpha": aid, "settings": st, **m})
                save(rows)                      # 增量落盘
                log("    {} S={} F={} 2Y={} sub={} rob={} TO={} prod={} margin={}".format(
                    aid, m["S"], m["F"], m["Y2"], m["sub"], m["rob"], m["TO"], m["prod"], m["margin"]))
        time.sleep(3)

    log("")
    log("=== 归因（对照 S1.48 F0.76 2Y1.78 sub0.86 prod0.5583）===")
    for r in sorted(rows, key=lambda x: (x["variant"])):
        log("  {:<5} S={} F={} 2Y={} sub={} prod={}  dS={:+.2f} dF={:+.2f}".format(
            r["variant"], r["S"], r["F"], r["Y2"], r["sub"], r["prod"],
            (r["S"] or 0) - 1.48, (r["F"] or 0) - 0.76))
    log("LEDGER " + LEDGER)


main()
