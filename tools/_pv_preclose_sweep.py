# -*- coding: utf-8 -*-
"""定向波：intraday_pv_feats 的 *_pre_close_2 子族扫描。

动机（2026-10-26 实测）
----------------------
主战役在 `intraday_pv_feats` 上跑 44 条 α，max S = 1.20，前三名是**同一结构同一子族**：
    ts_rank(ts_backfill(F, 22), 126)
      mean_vwap_30m_pre_close_2            S 1.20 F 0.79
      high_price_last_interval             S 1.17 F 0.76
      last_trade_price_30m_pre_close_2     S 1.08 F 0.68
而该集 585 个字段里 `*_pre_close_2` 子族有 **70 个**（覆盖率中位 0.985），
其中**只测过 1 个**。若同子族同质，这是最省预算的加宽路径。

本轮只改一个轴：把 ts_rank 窗口在 126 与 252 之间扫一遍（其余设置与主战役完全一致）。
判据：出现 S ≥ 1.5 的字段 ⇒ 该集从 DEAD 转为可定向；全 ≤1.3 ⇒ 子族同质但天花板就是 1.2，封集。

用法
----
    python tools/_pv_preclose_sweep.py            # 断点续跑
    python tools/_pv_preclose_sweep.py --dry-run  # 只打印计划
    python tools/_pv_preclose_sweep.py --fresh    # 忽略断点
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
CKDIR = os.path.join(ROOT, "results")
CK = os.path.join(CKDIR, "_pv_preclose_ck.json")
LEDGER = os.path.join(CKDIR, "_pv_preclose_ledger.json")
DS = "intraday_pv_feats"
WINDOWS = (126, 252)
BATCH = 10
SETTINGS = dict(region="EUR", universe="TOPCS1600", delay="1", decay="4",
                neutralization="FAST", truncation="0.08",
                nan_handling="ON", max_trade="ON", mode="FULL")

sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))


def log(m):
    print(m, flush=True)


def fields():
    con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db")); con.execute("PRAGMA busy_timeout=30000")
    rows = [r[0] for r in con.execute(
        "select field from field_profile_perf where region='EUR' and dataset=? "
        "and field like '%\\_pre\\_close\\_2' escape '\\' and coverage >= 0.6 "
        "order by field", (DS,))]
    con.close()
    return rows


def expr(f, win):
    return "ts_rank(ts_backfill(%s, 22), %d)" % (f, win)


def load_ck(fresh=False):
    if fresh or not os.path.isfile(CK):
        return {"done": [], "results": []}
    try:
        return json.load(open(CK, encoding="utf-8"))
    except Exception:
        return {"done": [], "results": []}


def save_ck(ck):
    tmp = CK + ".tmp"
    json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, CK)
    tmp = LEDGER + ".tmp"
    json.dump(ck["results"], open(tmp, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    os.replace(tmp, LEDGER)


def submit(path, tag):
    cmd = [PY, SUBMIT, "--path", path, "--region", SETTINGS["region"],
           "--universe", SETTINGS["universe"], "--delay", SETTINGS["delay"],
           "--decay", SETTINGS["decay"], "--neutralization", SETTINGS["neutralization"],
           "--truncation", SETTINGS["truncation"],
           "--nan-handling", SETTINGS["nan_handling"],
           "--max-trade", SETTINGS["max_trade"],
           "--simulation-mode", SETTINGS["mode"]]
    out = ""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=ROOT)
        out = (p.stdout or "") + "\n" + (p.stderr or "")
    except Exception as e:
        log("  [submit] %s 异常 %s" % (tag, e))
    m = re.search(r"/simulations/([A-Za-z0-9]+)", out)
    if not m:
        log("  [submit] %s 失败：%s" % (tag, out.strip().splitlines()[-3:]))
        return None
    return m.group(1)


def wait(sid, rounds=90, gap=15):
    from brain_api import brain_client
    for _ in range(rounds):
        try:
            j = brain_client.session.get("%s/simulations/%s" % (brain_client.base_url, sid),
                                         timeout=30).json()
        except Exception:
            time.sleep(gap)
            continue
        kids = j.get("children") or []
        if not kids:
            st = j.get("status")
            if st in ("ERROR", "FAIL", "CANCELLED"):
                return False
            time.sleep(gap)
            continue
        states = []
        for k in kids:
            try:
                kk = brain_client.session.get("%s/simulations/%s" % (brain_client.base_url, k),
                                              timeout=30).json()
                states.append(kk if isinstance(kk, dict) else {})
            except Exception:
                states.append({})
        if all(x.get("status") in ("COMPLETE", "ERROR", "FAIL", "CANCELLED") for x in states):
            return True
        time.sleep(gap)
    log("  [wait] %s 超时" % sid)
    return False


def harvest(sid):
    try:
        out = subprocess.run([PY, HARVEST, sid, DS, "camp"], capture_output=True,
                             text=True, timeout=600, cwd=ROOT).stdout
    except Exception as e:
        log("  [harvest] 异常 %s" % e)
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
    ap.add_argument("--fresh", action="store_true")
    a = ap.parse_args()

    fs = fields()
    log("字段 %d 个（*_pre_close_2, cov>=0.6）" % len(fs))
    plan = [(f, w) for w in WINDOWS for f in fs]
    ck = load_ck(a.fresh)
    done = set(ck["done"])
    todo = [x for x in plan if "%s|%d" % x not in done]
    log("计划 %d 条｜已完成 %d｜待跑 %d" % (len(plan), len(done), len(todo)))
    if a.dry_run:
        for i, (f, w) in enumerate(todo[:6]):
            log("   %-50s %d  ->  %s" % (f, w, expr(f, w)))
        return

    from brain_api import brain_client
    asyncio.run(brain_client.ensure_authenticated())

    for bi in range(0, len(todo), BATCH):
        chunk = todo[bi:bi + BATCH]
        fn = os.path.join(ROOT, "cache", "_pvpc_%02d.txt" % (bi // BATCH))
        with open(fn, "w", encoding="utf-8") as fh:
            fh.write("\n".join(expr(f, w) for f, w in chunk) + "\n")
        tag = "pvpc_%02d" % (bi // BATCH)
        sid = submit(fn, tag)
        if not sid:
            log("  [abort] 该批提交失败，停止（断点已保留）")
            break
        log("### %s n=%d sim=%s" % (tag, len(chunk), sid))
        if not wait(sid):
            log("  [warn] %s 未拿到终态，跳过该批（不写入断点，下次重试）" % tag)
            continue
        rows = harvest(sid)
        log("    收割 %d/%d 条" % (len(rows), len(chunk)))
        # 批次内顺序 = chunk 顺序（多仿真 children 顺序与 payload 一致）
        for i, r in enumerate(rows):
            if i < len(chunk):
                f, w = chunk[i]
                r.update(field=f, win=w)
            ck["results"].append(r)
        for f, w in chunk:
            ck["done"].append("%s|%d" % (f, w))
        save_ck(ck)
        time.sleep(3)

    rows = [r for r in ck["results"] if r.get("S") is not None]
    rows.sort(key=lambda r: -r["S"])
    log("\n=== Top 12（S 降序）===")
    log("%-50s %4s %7s %7s %7s %7s" % ("field", "win", "S", "F", "2Y", "sub"))
    for r in rows[:12]:
        log("%-50s %4d %7.2f %7.2f %7.2f %7.2f" % (r.get("field", "?"), r.get("win", 0),
                                                   r["S"], r.get("F") or 0,
                                                   r.get("Y2") or 0, r.get("sub") or 0))
    top = rows[0]["S"] if rows else None
    log("\n最高 S = %s｜≥1.5 的条数 = %d｜≥1.3 的条数 = %d"
        % (top, sum(1 for r in rows if r["S"] >= 1.5), sum(1 for r in rows if r["S"] >= 1.3)))
    log("断点 %s" % CK)


if __name__ == "__main__":
    main()
