# -*- coding: utf-8 -*-
"""r23 对照实验：基线形态 × 门控阈值（q=0.2/0.3），门控窗口固定 252。

设计（控制变量法）
------------------
* 因子 A：基线形态 —— ts_quantile+signed_power（leMn9jMA）／ ts_rank+signed_power（xA1LWjvg）
* 因子 B：门控阈值 q —— 0.2 / 0.3（r22 已测 0.4/0.5，本轮补低档）
* 对照组：无门控原株（主战役同设置同区间实测，见 CONTROL）
* 固定：窗口 252、EUR/TOPCS1600/delay1/decay4/FAST/trunc0.08/maxTrade ON/nanHandling ON

输出：logs/r23_exp.log（逐步 flush）＋ results/eur_r23_ledger.json
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

TERM = ("COMPLETE", "ERROR", "FAIL", "CANCELLED")
WIN = 252
QS = (0.2, 0.3)

# 无门控对照（主战役实测，同设置同区间）
CONTROL = {
    "leMn9jMA": {"S": 1.45, "Y2": 1.38, "sub": 0.77, "prod": 0.7423},
    "xA1LWjvg": {"S": 1.43, "Y2": 1.39, "sub": 0.76, "prod": 0.7393},
}
PLAN = [("leMn9jMA", "r23a"), ("xA1LWjvg", "r23b")]


def log(msg):
    print(msg, flush=True)


def build():
    codes = {}
    for aid in ("leMn9jMA", "xA1LWjvg"):
        j = brain_client.session.get("{}/alphas/{}".format(brain_client.base_url, aid)).json()
        codes[aid] = (j.get("regular") or {}).get("code")
        log("[code] {} = {}".format(aid, codes[aid]))
    out = []
    for aid, stem in PLAN:
        path = os.path.join(ROOT, "tracking", "EUR", "runs", stem + "_q23.txt")
        lines = [
            "# base={} code={}".format(aid, codes[aid]),
            "# r23 对照：门控窗口固定 {}，只改阈值 q（0.2/0.3）；对照=无门控原株".format(WIN),
        ]
        for q in QS:
            lines.append(
                "trade_when(greater(ts_rank({code}, {win}), {q}), {code}, -1)".format(
                    code=codes[aid], win=WIN, q=q))
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        out.append((aid, stem, path))
        log("[file] {}".format(path))
    return out


def submit(path):
    cmd = [PY, SB, "--path", path, "--region", "EUR", "--universe", "TOPCS1600",
           "--delay", "1", "--decay", "4", "--neutralization", "FAST",
           "--truncation", "0.08", "--max-trade", "ON", "--nan-handling", "ON",
           "--simulation-mode", "FULL"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    sids = list(dict.fromkeys(re.findall(r"/simulations/([A-Za-z0-9]+)", res.stdout)))
    if not sids:
        log("    SUBMIT FAIL " + (res.stdout or res.stderr)[-300:])
    return sids


def poll(sids, tag, rounds=140):
    alphas = set()
    for _ in range(rounds):
        done = True
        for sid in sids:
            j = brain_client.session.get("{}/simulations/{}".format(brain_client.base_url, sid)).json()
            if not isinstance(j, dict):
                done = False
                continue
            kids = j.get("children")
            if kids:
                objs = []
                for k in kids:
                    objs.append(brain_client.session.get(
                        "{}/simulations/{}".format(brain_client.base_url, k)).json())
                if not all(isinstance(x, dict) and x.get("status") in TERM for x in objs):
                    done = False
                for x in objs:
                    if isinstance(x, dict) and x.get("status") == "COMPLETE" and x.get("alpha"):
                        alphas.add(x["alpha"])
            else:
                st = j.get("status")
                if st in TERM:
                    if st == "COMPLETE" and j.get("alpha"):
                        alphas.add(j["alpha"])
                else:
                    done = False   # 只有 progress 也算未完成（r22 踩过这个坑）
        if done:
            log("[{}] 完成 alphas={}".format(tag, sorted(alphas)))
            return sorted(alphas)
        time.sleep(15)
    log("[{}] TIMEOUT".format(tag))
    return sorted(alphas)


def metrics(aid):
    j = brain_client.session.get("{}/alphas/{}".format(brain_client.base_url, aid)).json()
    i = j.get("is") or {}
    chk = {c.get("name"): c.get("value") for c in (i.get("checks") or [])}
    return {
        "S": i.get("sharpe"), "F": i.get("fitness"),
        "Y2": chk.get("LOW_2Y_SHARPE"),
        "sub": chk.get("LOW_SUB_UNIVERSE_SHARPE"),
        "rob": chk.get("LOW_ROBUST_UNIVERSE_SHARPE"),
        "TO": i.get("turnover"), "margin": i.get("margin"),
        "code": (j.get("regular") or {}).get("code"),
    }


def main():
    asyncio.run(brain_client.ensure_authenticated())
    plan = build()
    ledger = []
    # check_prod 在技能目录的包里（tools/wqb_campaign 已归档，不能从仓库根导入）
    sys.path.insert(0, os.path.join(
        os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-ra-eur", "scripts"))
    os.environ.setdefault("WQB_REPO_ROOT", ROOT)
    from wqb_campaign.audit import check_prod  # noqa: E402

    for base, stem, path in plan:
        sids = submit(path)
        log("### {} base={} sims={}".format(stem, base, sids))
        for aid in poll(sids, stem):
            m = metrics(aid)
            try:
                m["prod"] = check_prod(aid)
            except Exception as exc:  # noqa: BLE001
                m["prod"] = None
                log("    prod ERR {}".format(type(exc).__name__))
            q = 0.2 if "0.2" in (m["code"] or "") else 0.3
            ledger.append({"base": base, "q": q, "alpha": aid, **m})
            log("    {} q={} S={} F={} 2Y={} sub={} rob={} prod={} margin={}".format(
                aid, q, m["S"], m["F"], m["Y2"], m["sub"], m["rob"], m["prod"], m["margin"]))
        time.sleep(3)

    log("")
    log("=== 归因（相对无门控对照）===")
    for base, _stem, _p in plan:
        ctl = CONTROL[base]
        rows = [r for r in ledger if r["base"] == base]
        log("{} 对照 S={} 2Y={} prod={}".format(base, ctl["S"], ctl["Y2"], ctl["prod"]))
        for r in sorted(rows, key=lambda x: x["q"]):
            d_s = round((r["S"] or 0) - ctl["S"], 3)
            d_y = round((r["Y2"] or 0) - ctl["Y2"], 3)
            d_p = round((r["prod"] if r["prod"] is not None else 9) - ctl["prod"], 3)
            verdict = "prod 破闸" if (r["prod"] is not None and r["prod"] < 0.7) else "prod 仍墙"
            log("  q={} : dS {:+.3f} | d2Y {:+.3f} | dprod {:+.3f}  => {}".format(
                r["q"], d_s, d_y, d_p, verdict))

    out = os.path.join(ROOT, "results", "eur_r23_ledger.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(ledger, fh, ensure_ascii=False, indent=1)
    log("LEDGER " + out)


main()
