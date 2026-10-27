#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""campaign_report.py — 全量流水线「跑完一个数据集就汇报」的增量汇报器。

设计要点
--------
* **唯一事实源** = `results/campaign_digest.md`（每跑完一个集追加一行，同集重跑会替换原行）。
* **增量**：状态存 `cache/campaign_report_state.json` 的最后已汇报集数，只打印新增行。
* **可等**：`--wait-secs N` 在有新集前最多阻塞 N 秒（轮询 15s），便于「跑完一个就报」。
* **带明细**：对新增集从 `results/full_template_campaign_results.json` 取模板级最佳、
  prod_top、距交付（逐 alpha S≥1.5 & 2Y≥1.58，EUR sub 闸 0.53×S）。

用法
----
  python tools/campaign_report.py                 # 只报新增，不等
  python tools/campaign_report.py --wait-secs 480 # 最多等 8 分钟直到有新集
  python tools/campaign_report.py --reset         # 清状态，下次数全部
"""
import json
import os
import re
import sys
import time
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIGEST = os.path.join(ROOT, "results", "campaign_digest.md")
RESULTS = os.path.join(ROOT, "results", "full_template_campaign_results.json")
CKPT = os.path.join(ROOT, "results", "full_template_campaign_checkpoint.json")
STATE = os.path.join(ROOT, "cache", "campaign_report_state.json")
TOTAL = 169

LINE_RE = re.compile(r"^- (\d\d-\d\d \d\d:\d\d) \*\*(.+?)\*\*\((\S+?)\) → (\S+) "
                     r"S=(\S+) 2Y=(\S+) joint=(\S+) n=(\S+) prod=(\S+)")


def load_state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {"reported_lines": 0, "last_report_at": None}


def save_state(st):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    tmp = STATE + ".tmp"
    json.dump(st, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, STATE)


def digest_lines():
    if not os.path.exists(DIGEST):
        return []
    with open(DIGEST, encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f if l.startswith("- ")]


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def report_one(raw, res, done_n):
    m = LINE_RE.match(raw)
    out = []
    if not m:
        out.append(raw)
        return out
    ts, ds, cat, verdict, S, Y2, joint, n, prod = m.groups()
    sv, y2, pv = num(S.replace("None", "")), num(Y2.replace("None", "")), num(prod.replace("None", ""))
    tag = {"ALIVE": "ALIVE", "BORDERLINE": "BORDER", "DEAD": "DEAD",
           "SKIPPED_LOW_COV": "SKIP-COV", "SKIPPED_TOO_FEW_FIELDS": "SKIP-FIELDS",
           "SIM_FAIL": "SIM-FAIL"}.get(verdict, verdict)
    head = f"[{done_n}/{TOTAL}] {ds} ({cat}) → {tag}"
    if sv is not None:
        head += f"  S={sv}  2Y={y2 if y2 is not None else '-'}"
    if pv is not None:
        head += f"  prod={pv}" + ("  ⚠撞墙" if pv >= 0.7 else "")
    out.append(head)

    v = (res.get("results") or {}).get(ds) or {}
    # 模板级最佳
    alphas = [a for a in (v.get("alphas") or []) if a.get("s") is not None]
    if alphas:
        alphas.sort(key=lambda a: -a["s"])
        top = alphas[:3]
        for a in top:
            sub = a.get("sub")
            sub_ok = "" if sub is None else ("  sub✓" if sub >= 0.53 * a["s"] else "  sub✗")
            out.append(f"      {a.get('tpl','?'):8s} {str(a.get('alpha')):10s} "
                       f"S={a.get('s')} F={a.get('f')} 2Y={a.get('y2')} sub={sub}{sub_ok}")
        joint_al = [a for a in alphas if (a["s"] or 0) >= 1.5
                    and (a.get("f") or 0) >= 1.0 and (a.get("y2") or 0) >= 1.58]
        if joint_al:
            out.append(f"      ★ 联合过闸 {len(joint_al)} 颗: "
                       + ", ".join(f"{a['alpha']}(S{a['s']}/2Y{a['y2']})" for a in joint_al[:4]))
    sp = v.get("settings_sweep")
    if sp:
        out.append(f"      设置轴补扫 {len(sp)} 组: "
                   + ", ".join(f"{k}={x.get('max_s')}" for k, x in list(sp.items())[:5]))
    if v.get("coverage") is not None and sv is None:
        out.append(f"      coverage={round(v['coverage'], 3)}")
    return out


def main():
    wait_secs = 0
    for i, a in enumerate(sys.argv):
        if a == "--wait-secs":
            wait_secs = int(sys.argv[i + 1])
        if a == "--reset":
            save_state({"reported_lines": 0, "last_report_at": None})
            print("[campaign_report] state reset")
            return

    st = load_state()
    t0 = time.time()
    while True:
        lines = digest_lines()
        if len(lines) > st.get("reported_lines", 0) or time.time() - t0 > wait_secs:
            break
        time.sleep(15)

    lines = digest_lines()
    prev = st.get("reported_lines", 0)
    new = lines[prev:]
    try:
        res = json.load(open(RESULTS, encoding="utf-8"))
    except Exception:
        res = {}
    try:
        ck = json.load(open(CKPT, encoding="utf-8"))
        done_n = len(ck.get("done") or [])
    except Exception:
        done_n = prev

    if not new:
        print(f"[campaign_report] 无新完成集（已汇报 {prev} 行，等待 {int(time.time()-t0)}s）")
        return

    print(f"=== 新增完成 {len(new)} 个集｜累计 {done_n}/{TOTAL}"
          f"（{done_n/TOTAL:.1%}）｜{datetime.now():%H:%M} ===")
    base = done_n - len(new)
    for k, raw in enumerate(new, 1):
        for l in report_one(raw, res, base + k):
            print(l)
        print("")

    st["reported_lines"] = len(lines)
    st["last_report_at"] = datetime.now().isoformat(timespec="seconds")
    save_state(st)
    print(f"[campaign_report] 状态已存：reported_lines={len(lines)}")


if __name__ == "__main__":
    main()
