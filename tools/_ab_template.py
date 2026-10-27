# -*- coding: utf-8 -*-
"""P3 验证：新模板（删 5 族 + pp 统一）vs 旧模板 —— 同字段同设置的真 A/B。

为什么要真 A/B
--------------
不能拿「新跑的结果」和「历史结果」比：历史那批是 13 族 × 12.2 条/字段，
新批是 8 族 × 6.3 条/字段，α 数量不同，maxS 天然不可比。

设计（只跑两版**差异部分**，共有的 8 族不重跑）
----------------------------------------------
| 臂 | 族 | 说明 |
|---|---|---|
| 旧独有 | `lvl_zs` `lvl_qt` `lvl_sc` `ir_pl` `dsp_rk` | 2026-10-26 从 FAMILIES 删除的 5 个零产出族 |
| 新独有 | `pp` | 新增 / 统一为 `signed_power(dw, 0.7)` |
| 对照 | `lvl_rk` | 两版都有，用于确认「字段集与设置与历史一致」 |

对象：`other571`（历史 maxS 0.99 / 71 α / DEAD）与 `insider_matrix`（0.98 / 52 α / DEAD）
—— 都是 OTHER 类里「差一点点」的旧 DEAD 集，最能看出模板改动有没有用。

判据：
  · 新臂 `pp` 的 maxS > 5 个旧臂的最大值 ⇒ 新模板更优（同等预算产生更强构造）
  · 旧 5 臂里任一条超 `pp` ⇒ 删族有损失，需要回补
  · 5 个旧臂全部低于 `lvl_rk` 对照 ⇒ 确认「零产出」不是偶然

已知问题（记录在案）：`dsp_rk` 生成 `rank(ts_backfill(vec_stddev(F), 22))`，
对 MATRIX 字段非法（vec_stddev 只接受 VECTOR）⇒ 该臂对非 VECTOR 字段跳过并计数。

用法：python tools/_ab_template.py [--dry-run] [--fresh]
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
CK = os.path.join(ROOT, "results", "_ab_template_ck.json")
LEDGER = os.path.join(ROOT, "results", "_ab_template_ledger.json")

os.environ.setdefault("WQB_REPO_ROOT", ROOT)
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-ra-eur", "scripts"))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

from wqb_campaign.fields import select_fields          # noqa: E402
from wqb_campaign.generate import build_one_family, DS_FREQ, FAMILIES  # noqa: E402

DATASETS = ["other571", "insider_matrix"]
OLD_ARMS = ["lvl_zs", "lvl_qt", "lvl_sc", "ir_pl", "dsp_rk"]
NEW_ARMS = ["pp"]
CTRL = ["lvl_rk"]
BATCH = 10
SETTINGS = dict(region="EUR", universe="TOPCS1600", delay="1", decay="4",
                neutralization="FAST", truncation="0.08",
                nan_handling="ON", max_trade="ON", mode="FULL")


def log(m):
    print(m, flush=True)


def build():
    con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db")); con.execute("PRAGMA busy_timeout=30000")
    con.row_factory = sqlite3.Row
    plan, skipped = [], []
    for ds in DATASETS:
        _all = select_fields(con, ds, field_min_cov=0.6)
        _full = [r for r in _all if r.get("tier") == "full"]
        _probe = [r for r in _all if r.get("tier") != "full"]
        # full 只有 3 个太少（insider_matrix/other571 都只有 3 个）⇒ 用 probe 补到 8 个，
        # A/B 只比「同一字段集上的不同臂」，与历史是否跑过无关。
        sel = (_full + _probe)[:8]
        freq = DS_FREQ.get(ds, "daily")
        log("[%s] full 字段 %d 个  freq=%s" % (ds, len(sel), freq))
        for arm in OLD_ARMS + NEW_ARMS + CTRL:
            for r in sel:
                is_vec = (r.get("field_type") == "VECTOR")
                if arm == "dsp_rk" and not is_vec:
                    skipped.append((ds, arm, r["field_name"]))
                    continue
                e = build_one_family(arm, r, freq)
                if not e:
                    skipped.append((ds, arm, r["field_name"]))
                    continue
                plan.append(dict(ds=ds, arm=arm, field=r["field_name"], expr=e))
    con.close()
    return plan, skipped


def load(fresh=False):
    if fresh or not os.path.isfile(CK):
        return {"done": [], "results": []}
    try:
        return json.load(open(CK, encoding="utf-8"))
    except Exception:
        return {"done": [], "results": []}


def save(ck):
    for p, obj in ((CK, ck), (LEDGER, ck["results"])):
        tmp = p + ".tmp"
        json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, p)


def submit(path):
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


def harvest(sid, ds):
    try:
        out = subprocess.run([PY, HARVEST, sid, ds, "camp"], capture_output=True,
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
    ap.add_argument("--fresh", action="store_true")
    a = ap.parse_args()

    plan, skipped = build()
    log("表达式 %d 条｜跳过 %d 条（dsp_rk 对非 VECTOR 字段非法等）" % (len(plan), len(skipped)))
    by_arm = {}
    for p in plan:
        by_arm.setdefault((p["ds"], p["arm"]), 0)
        by_arm[(p["ds"], p["arm"])] += 1
    for k in sorted(by_arm):
        log("   %-16s %-8s %d 条" % (k[0], k[1], by_arm[k]))
    if skipped:
        log("   跳过样例: %s" % (skipped[:3],))
    if a.dry_run:
        for p in plan[:3] + plan[-2:]:
            log("   %s/%s  %s" % (p["ds"], p["arm"], p["expr"][:100]))
        return

    ck = load(a.fresh)
    done = set(ck["done"])
    from brain_api import brain_client
    asyncio.run(brain_client.ensure_authenticated())

    for bi in range(0, len(plan), BATCH):
        chunk = plan[bi:bi + BATCH]
        key = "b%02d" % (bi // BATCH)
        if key in done:
            log("### %s 已完成，跳过" % key)
            continue
        fn = os.path.join(ROOT, "cache", "_ab_%s.txt" % key)
        open(fn, "w", encoding="utf-8").write("\n".join(p["expr"] for p in chunk) + "\n")
        # 提交重试：2026-10-26 实测 submit_batch 会因账号并发/瞬时 429 返回无 Location，
        # 单次失败就 break 会让整轮停在半路（b01 就是这样丢的）。
        sid = None
        for _try in range(3):
            sid = submit(fn)
            if sid:
                break
            log("  [retry] %s 第 %d 次提交失败，等 30s" % (key, _try + 1))
            time.sleep(30)
        if not sid:
            log("### %s 三次提交均失败，停止（断点保留）" % key)
            break
        ds0 = chunk[0]["ds"]
        log("### %s n=%d ds=%s sim=%s" % (key, len(chunk), ds0, sid))
        if not wait(sid):
            log("  [warn] %s 未到终态，跳过" % key)
            continue
        rows = harvest(sid, ds0)
        log("    收割 %d/%d" % (len(rows), len(chunk)))
        for i, r in enumerate(rows):
            if i < len(chunk):
                r.update(ds=chunk[i]["ds"], arm=chunk[i]["arm"], field=chunk[i]["field"])
            ck["results"].append(r)
        ck["done"].append(key)
        save(ck)
        time.sleep(3)

    log("\n" + "=" * 92)
    log("=== A/B 汇总（同字段同设置，只比两版差异臂）===")
    log("%-16s %-8s %4s %7s %7s %7s" % ("dataset", "arm", "n", "maxS", "≥1.3", "≥1.58"))
    for ds in DATASETS:
        for arm in OLD_ARMS + NEW_ARMS + CTRL:
            rs = [r for r in ck["results"] if r.get("ds") == ds and r.get("arm") == arm
                  and r.get("S") is not None]
            if not rs:
                log("%-16s %-8s %4d %7s %7s %7s" % (ds, arm, 0, "—", 0, 0))
                continue
            ss = [r["S"] for r in rs]
            tag = "  ← 新" if arm in NEW_ARMS else ("  ← 对照" if arm in CTRL else "")
            log("%-16s %-8s %4d %7.2f %7d %7d%s" % (
                ds, arm, len(rs), max(ss), sum(1 for s in ss if s >= 1.3),
                sum(1 for s in ss if s >= 1.58), tag))
        log("-" * 92)
    log("断点 %s" % CK)


if __name__ == "__main__":
    main()
