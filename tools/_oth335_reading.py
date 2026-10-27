# -*- coding: utf-8 -*-
"""定向波 5：other335 —— 改「读数方式」降 prod（最后一轮）。

归因结论（2026-10-26 21:15）
---------------------------
`kqNxoL5d`（hedge, dw(5,126), TOP2500）IS 全闸通过，**prod = 0.8315**。
直方图：0.7–0.8 有 18 颗、**0.8–0.9 只有 3 颗** ⇒ 单点对手，不是成片拥挤
（memory §13：单点对手的去相关可行性高于整段抬升）。

已排除的两条路
  · 换字段：其余 4 个变体（mind/linear/shield/mktcap）**2Y 全崩**（1.22 / −0.06 / −0.81 / −0.21）
  · 换结构保 prod：同字段不同投影日收益相关 0.84–0.99，prod 动不了

本轮只改「读数方式」（memory §6 三类真降之一），字段与设置不变：
    zs126    zscore 读数代替 level
    dev     短均 − 长均（偏离自身长期水平）
    mom      短均的 21 日动量
    gsec/gin/gsub  分组中性化 sector/industry/subindustry（分组字段是 ATOM 六豁免之一）
    gate     短均 >0.5 才持仓（改「何时交易」）
    sp07     signed_power 0.7（压缩极端）

判据：任一条 S≥1.58 且 F≥1.0 且 2Y≥1.60 ⇒ 立刻测它的 prod。
用法：python tools/_oth335_reading.py [--dry-run]
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
CK = os.path.join(ROOT, "results", "_oth335_read_ck.json")
LEDGER = os.path.join(ROOT, "results", "_oth335_read_ledger.json")
DS = "other335"
F = "oth335_combined_all_region_hedge"

sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

SETTINGS = dict(region="EUR", universe="TOP2500", delay="1", decay="4",
                neutralization="FAST", truncation="0.08",
                nan_handling="ON", max_trade="ON", mode="FULL")

SM5 = "ts_mean(ts_backfill(%s, 22), 5)" % F
SM126 = "ts_mean(ts_backfill(%s, 22), 126)" % F
DW = "multiply(rank(%s), rank(%s))" % (SM5, SM126)

PLAN = [
    ("zs126", "rank(ts_zscore(ts_backfill(%s, 22), 126))" % F),
    ("dev", "rank(subtract(%s, %s))" % (SM5, SM126)),
    ("mom", "rank(ts_delta(%s, 21))" % SM5),
    ("gsec", "group_rank(%s, sector)" % DW),
    ("gin", "group_rank(%s, industry)" % DW),
    ("gsub", "group_rank(%s, subindustry)" % DW),
    ("gate", "if_else(greater(rank(%s), 0.5), %s, 0)" % (SM5, DW)),
    ("sp07", "signed_power(%s, 0.7)" % DW),
]


def log(m):
    print(m, flush=True)


def load():
    if os.path.isfile(CK):
        try:
            return json.load(open(CK, encoding="utf-8"))
        except Exception:
            pass
    return {"done": [], "results": []}


def save(ck):
    for p, obj in ((CK, ck), (LEDGER, ck["results"])):
        tmp = p + ".tmp"
        json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, p)


def submit(path, tag):
    cmd = [PY, SUBMIT, "--path", path, "--region", SETTINGS["region"],
           "--universe", SETTINGS["universe"], "--delay", SETTINGS["delay"],
           "--decay", SETTINGS["decay"], "--neutralization", SETTINGS["neutralization"],
           "--truncation", SETTINGS["truncation"],
           "--nan-handling", SETTINGS["nan_handling"],
           "--max-trade", SETTINGS["max_trade"],
           "--simulation-mode", SETTINGS["mode"]]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=ROOT)
        out = (p.stdout or "") + "\n" + (p.stderr or "")
    except Exception as ex:
        log("  [submit] %s 异常 %s" % (tag, ex))
        return None
    m = re.search(r"/simulations/([A-Za-z0-9]+)", out)
    if not m:
        log("  [submit] %s 失败 %s" % (tag, out.strip().splitlines()[-3:]))
        return None
    return m.group(1)


def wait(sid, rounds=100, gap=15):
    from brain_api import brain_client
    for _ in range(rounds):
        try:
            j = brain_client.session.get("%s/simulations/%s" % (brain_client.base_url, sid),
                                         timeout=30).json()
        except Exception:
            time.sleep(gap); continue
        kids = j.get("children") or []
        if not kids:
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


def harvest(sid):
    try:
        out = subprocess.run([PY, HARVEST, sid, DS, "camp"], capture_output=True,
                             text=True, timeout=600, cwd=ROOT).stdout
    except Exception:
        return []
    rows = []
    for ln in out.splitlines():
        m = re.match(r"\s*\+\s+(\w+)\s+S=([-\d.]+)\s+F=([-\d.]+).*?2Y=([-\d.]+)\s+sub=([-\d.]+)", ln)
        if m:
            rows.append(dict(alpha=m.group(1), S=float(m.group(2)), F=float(m.group(3)),
                             Y2=float(m.group(4)), sub=float(m.group(5))))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.dry_run:
        for t, e in PLAN:
            log("%-6s %s" % (t, e[:120]))
        return

    ck = load()
    if "reading" not in ck["done"]:
        from brain_api import brain_client
        asyncio.run(brain_client.ensure_authenticated())
        exprs = [e for _, e in PLAN]
        fn = os.path.join(ROOT, "cache", "_oth335_read.txt")
        open(fn, "w", encoding="utf-8").write("\n".join(exprs) + "\n")
        sid = submit(fn, "reading")
        if not sid:
            log("提交失败")
            return
        log("### reading n=%d sim=%s" % (len(exprs), sid))
        if not wait(sid):
            log("未到终态")
            return
        rows = harvest(sid)
        log("收割 %d/%d" % (len(rows), len(exprs)))
        for i, r in enumerate(rows):
            if i < len(exprs):
                r.update(tag=PLAN[i][0], expr=exprs[i])
            ck["results"].append(r)
        ck["done"].append("reading")
        save(ck)

    log("\n=== 改读数结果（对照 kqNxoL5d: S1.82 F1.02 2Y1.70 prod0.8315）===")
    log("%-6s %6s %6s %6s %6s %-10s %s" % ("tag", "S", "F", "2Y", "sub", "alpha", "判定"))
    for r in sorted(ck["results"], key=lambda x: -((x.get("S") or 0))):
        ok = (r.get("S") or 0) >= 1.58 and (r.get("F") or 0) >= 1.0 and (r.get("Y2") or 0) >= 1.60
        log("%-6s %6.2f %6.2f %6.2f %6.2f %-10s %s" % (
            r.get("tag"), r.get("S") or 0, r.get("F") or 0, r.get("Y2") or 0,
            r.get("sub") or 0, r.get("alpha"), "★仍过闸→测 prod" if ok else ""))


if __name__ == "__main__":
    main()
