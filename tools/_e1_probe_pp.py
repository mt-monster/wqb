"""E1：同字段 A/B —— pp 是否真的优于 lvl_rk。

对象：pv87（lvl_rk 0.93 / dw 0.53）、other545（lvl_rk 0.92 / dw 0.90）
      全池仅剩的 2 个「pp 从未跑过 且 lvl_rk >= 0.8」的集。

设计（每字段 2 条，8 字段/集）：
  A = signed_power(dw, 0.7)          pp ∘ dw      （新模板要加到探针的那条）
  B = group_rank(lvl_rk, market)      pp ∘ lvl_rk  （高档 pp 的另一个赢家变体）
对照 = 该集已有的 lvl_rk / dw 实测（同设置同区间，来自 campaign 台账）

设置与 campaign 基线完全一致：EUR / TOPCS1600 / delay1 / decay4 / trunc0.08
                              / maxTrade ON / nanHandling ON / FAST
不测 prod（避免账号级 corr 锁争用，见 2026-10-26 事故记录）。

用法：
  python tools/_e1_probe_pp.py --dry-run    # 只打印表达式与批次
  python tools/_e1_probe_pp.py              # 派发 + 轮询 + 汇总
"""
import argparse
import asyncio
import collections
import json
import os
import re
import sqlite3
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-ra-eur", "scripts")
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
SB = os.path.join(ROOT, "tools", "submit_batch.py")
os.environ["WQB_REPO_ROOT"] = ROOT
sys.path.insert(0, SK)
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

from brain_api import brain_client                      # noqa: E402
from wqb_campaign.fields import select_fields           # noqa: E402
from wqb_campaign.generate import build_one_family, DS_FREQ  # noqa: E402

TARGETS = ["pv87", "other545"]
QUARTERLY_CATS = ("ANALYST", "FUNDAMENTAL", "INSIDERS", "INSTITUTIONS", "EARNINGS", "MACRO")
BASELINE = {  # 来自 results/full_template_campaign_results.json（同设置同区间）
    "pv87": {"lvl_rk": 0.93, "dw": 0.53},
    "other545": {"lvl_rk": 0.92, "dw": 0.90},
}
OUT_DIR = os.path.join(ROOT, "tracking", "EUR", "runs")
TERM = ("COMPLETE", "ERROR", "FAIL", "CANCELLED")


def log(m):
    print(m, flush=True)


def build():
    """返回 [(stem, path, [codes])]，每集两个文件（A/B 分开，便于归因）。"""
    con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db")); con.execute("PRAGMA busy_timeout=30000")
    con.row_factory = sqlite3.Row
    plan = []
    for ds in TARGETS:
        cat = (con.execute("select category from dataset_profile where region='EUR' and dataset=?",
                           (ds,)).fetchone() or {"category": ""})["category"]
        freq = DS_FREQ.get(ds, "quarterly" if (cat or "").upper() in QUARTERLY_CATS else "daily")
        # ⚠ 这两个集来自「低覆盖波」（集级 cov 0.50 / 0.542），按 0.6 筛会返回空集，
        #   必须与它们当初跑的那一波同口径（--min-cov 0.5），否则比不了。
        sel = [r for r in select_fields(con, ds, field_min_cov=0.5) if r.get("tier") == "full"]
        a_codes, b_codes = [], []
        for r in sel:
            dw = build_one_family("dw", r, freq)
            if dw:
                a_codes.append(f"signed_power({dw}, 0.7)")
            lr = build_one_family("lvl_rk", r, freq)
            if lr:
                b_codes.append(f"group_rank({lr}, market)")
        for tag, codes in (("A_ppdw", a_codes), ("B_grlr", b_codes)):
            stem = f"e1_{ds}_{tag}"
            p = os.path.join(OUT_DIR, stem + ".txt")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(f"# E1 {ds} {tag} freq={freq}\n")
                fh.write("\n".join(codes) + "\n")
            plan.append((stem, p, codes))
    con.close()
    return plan


def submit(path):
    cmd = [PY, SB, "--path", path, "--region", "EUR", "--universe", "TOPCS1600",
           "--delay", "1", "--decay", "4", "--neutralization", "FAST",
           "--truncation", "0.08", "--max-trade", "ON", "--nan-handling", "ON",
           "--simulation-mode", "FULL"]
    o = subprocess.run(cmd, capture_output=True, text=True)
    sids = list(dict.fromkeys(re.findall(r"/simulations/([A-Za-z0-9]+)", o.stdout)))
    if not sids:
        log("    FAIL " + (o.stdout or o.stderr)[-300:])
    return sids


def poll(sids, tag, rounds=120):
    alphas = set()
    for _ in range(rounds):
        done = True
        for sid in sids:
            j = brain_client.session.get(f"{brain_client.base_url}/simulations/{sid}", timeout=30).json()
            if not isinstance(j, dict):
                done = False
                continue
            kids = j.get("children")
            if kids:
                objs = [brain_client.session.get(f"{brain_client.base_url}/simulations/{k}",
                                                 timeout=30).json() for k in kids]
                if not all((x.get("status") in TERM) for x in objs if isinstance(x, dict)):
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
                    done = False
        if done:
            return sorted(alphas)
        time.sleep(15)
    log(f"[{tag}] TIMEOUT")
    return sorted(alphas)


def metrics(aid):
    j = brain_client.session.get(f"{brain_client.base_url}/alphas/{aid}", timeout=30).json()
    i = j.get("is") or {}
    chk = {c.get("name"): c.get("value") for c in (i.get("checks") or [])}
    return {"S": i.get("sharpe"), "F": i.get("fitness"), "Y2": chk.get("LOW_2Y_SHARPE"),
            "sub": chk.get("LOW_SUB_UNIVERSE_SHARPE"), "TO": i.get("turnover"),
            "code": (j.get("regular") or {}).get("code")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="只跑指定 stem（补派失败批用），逗号分隔")
    a = ap.parse_args()

    plan = build()
    if a.only:
        keep = {x.strip() for x in a.only.split(",") if x.strip()}
        plan = [p for p in plan if p[0] in keep]
        log(f"[only] 只跑 {sorted(keep)} → {len(plan)} 批")
    log("=== E1 计划 ===")
    for stem, path, codes in plan:
        log(f"  {stem:<22} {len(codes)} 条")
        for c in codes[:2]:
            log(f"      {c[:130]}")
    if a.dry_run:
        log("\n（dry-run，不派发）")
        return

    asyncio.run(brain_client.ensure_authenticated())
    ledger = []
    for stem, path, codes in plan:
        sids = submit(path)
        log(f"### {stem} sims={sids}")
        ids = poll(sids, stem)
        ds, tag = stem.split("_")[1], "_".join(stem.split("_")[2:])
        for aid in ids:
            m = metrics(aid)
            ledger.append({"ds": ds, "variant": tag, "alpha": aid, **m})
            log(f"    {aid} {tag} S={m['S']} F={m['F']} 2Y={m['Y2']} sub={m['sub']} TO={m['TO']}")
        time.sleep(3)

    out = os.path.join(ROOT, "results", "eur_e1_ledger.json")
    # 合并写入（--only 补派时不能把已有结果冲掉）
    try:
        old_rows = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else []
    except Exception:
        old_rows = []
    seen = {(r.get("alpha")) for r in old_rows}
    merged = old_rows + [r for r in ledger if r.get("alpha") not in seen]
    json.dump(merged, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ledger = merged

    log("\n=== E1 归因（对照 campaign 台账的同字段 lvl_rk / dw）===")
    for ds in TARGETS:
        base = BASELINE[ds]
        rows = [r for r in ledger if r["ds"] == ds and r.get("S") is not None]
        if not rows:
            log(f"{ds}: 无结果")
            continue
        best = collections.defaultdict(lambda: {"S": -9, "alpha": None})
        for r in rows:
            if r["S"] > best[r["variant"]]["S"]:
                best[r["variant"]] = r
        log(f"{ds}  对照 lvl_rk={base['lvl_rk']} / dw={base['dw']}")
        for v, b in sorted(best.items()):
            log(f"    {v:<8} 最高 S={b['S']:.2f} ({b['alpha']})"
                f"  vs lvl_rk {b['S'] - base['lvl_rk']:+.2f} / vs dw {b['S'] - base['dw']:+.2f}")
    log("LEDGER " + out)


main()
