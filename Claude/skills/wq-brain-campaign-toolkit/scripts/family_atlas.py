# -*- coding: utf-8 -*-
"""family_atlas.py - 家族导航（2026-09-01 落地，G2）。

以「信号族」为主键的全局状态图（区别于数据集粒度的 S0 评分）：
  - 状态机：untried → has_signal → near_gate → submitted(active/saturated)
            → dead(local/xregion) → os_decay（G3 回流后）
  - 数据源：registry_empirical(win/dead/campaign) + expressions/backtest_results（信号强度）
            + distilled_red_families（G1） + os_feedback_latest（G3）
  - 用途：选波前先查图（哪个族未试？哪个族在邻区刚 win？哪个族 OS 衰减要避开？）

输出（region 可选，缺省全区域）：
  region   family                      state       evidence
  KOR      analyst_revision            ACTIVE      2 win / 4 dead / os_decay=0
  USA      emotion                     XREGION-DEAD  跨区铁律（GLB+USA 判死）
  IND      rsk68_residual              DEAD-LOCAL  1 dead（无正交破壁路径）

用法：
  python family_atlas.py --campaign-dir tracking/KOR            # KOR 视角
  python family_atlas.py --campaign-dir tracking/KOR --all      # 全区域
  python family_atlas.py --campaign-dir tracking/KOR --json     # 机器可读
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import add_campaign_arg, CampaignContext

STATE_ORDER = ["untried", "has_signal", "near_gate", "active", "saturated",
               "dead_local", "dead_xregion", "os_decay"]


def _db_path(ctx):
    for root in _workspace_roots(ctx):
        p = os.path.join(root, "data", "wqb.db")
        if os.path.isfile(p):
            return p
    raise SystemExit("未找到 data/wqb.db")


def _workspace_roots(ctx):
    cdir = getattr(ctx, "dir", None)
    here = os.path.dirname(os.path.abspath(__file__))
    roots = []
    if cdir:
        roots.append(os.path.abspath(os.path.join(cdir, "..", "..")))
    roots.append(os.path.abspath(os.path.join(here, "..", "..", "..", "..", "..")))
    env = os.environ.get("WQB_ROOT")
    if env:
        roots.insert(0, env)
    return [r for r in roots if os.path.isfile(os.path.join(r, "data", "wqb.db"))]


def _norm_family(f):
    return (f or "").strip().lower() or None


def load_families(db):
    """族级状态聚合。返回 {(region, family): state_dict}。"""
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    fams = {}
    # 1. registry win / dead
    for r in con.execute(
        "SELECT region, layer, family, entry_id FROM registry_empirical WHERE layer IN ('win','dead_end')"
    ):
        fam = _norm_family(r["family"])
        if not fam:
            continue
        d = fams.setdefault((r["region"], fam), {"win": 0, "dead": 0, "win_ids": [], "dead_ids": []})
        if r["layer"] == "win":
            d["win"] += 1
            d["win_ids"].append(r["entry_id"])
        else:
            d["dead"] += 1
            d["dead_ids"].append(r["entry_id"])
    # 2. campaign 层（untried/in_progress/exhausted 的数据集族）
    for r in con.execute(
        "SELECT region, entry_id, family, payload FROM registry_empirical WHERE layer='campaign'"
    ):
        try:
            p = json.loads(r["payload"]) if r["payload"] else {}
        except Exception:
            p = {}
        status = p.get("status") or (r["entry_id"].lower() if not p else None)
        ds = p.get("dataset") or r["family"] or r["entry_id"]
        fam = _norm_family(ds)
        if not fam:
            continue
        d = fams.setdefault((r["region"], fam), {"win": 0, "dead": 0, "win_ids": [], "dead_ids": []})
        d.setdefault("campaign_status", status)
    # 3. G1 蒸馏红灯族（GLOBAL 桶）
    row = con.execute("SELECT value FROM ledger_kv WHERE region='GLOBAL' AND key='distilled_red_families'").fetchone()
    red = {}
    if row:
        try:
            red = json.loads(row[0])
        except Exception:
            red = {}
    # 4. G3 OS 衰减（win 族的 os_decay 标记）
    for r in con.execute(
        "SELECT region, family, payload FROM registry_empirical WHERE layer='win'"
    ):
        fam = _norm_family(r["family"])
        if not fam:
            continue
        try:
            p = json.loads(r["payload"]) if r["payload"] else {}
        except Exception:
            p = {}
        if p.get("os_decay"):
            d = fams.setdefault((r["region"], fam), {"win": 0, "dead": 0, "win_ids": [], "dead_ids": []})
            d["os_decay"] = len(p["os_decay"])
    # 5. backtest 信号强度（近闸 = 有 sharpe>=1.3 但未达标）
    for r in con.execute(
        "SELECT region, dataset, MAX(sharpe) ms, COUNT(*) n FROM backtest_results "
        "WHERE sharpe IS NOT NULL GROUP BY region, dataset"
    ):
        fam = _norm_family(r["dataset"])
        if not fam:
            continue
        d = fams.setdefault((r["region"], fam), {"win": 0, "dead": 0, "win_ids": [], "dead_ids": []})
        d["max_sharpe"] = r["ms"]
        d["bt_count"] = r["n"]
    con.close()

    # 状态机判定
    out = {}
    for (region, fam), d in fams.items():
        cross_dead = any(x["family"] == fam for lst in red.get(region, []) for x in ([lst] if isinstance(lst, dict) else [])) if red.get(region) else False
        # red 结构 {region: [{family, dead_count}]}
        cross_dead = any(x.get("family") == fam for x in red.get(region, [])) if isinstance(red.get(region), list) else False
        if cross_dead:
            state = "dead_xregion"
        elif d.get("os_decay"):
            state = "os_decay"
        elif d["win"] > 0:
            state = "active" if d["win"] >= 3 else "submitted"
        elif d["dead"] >= 2:
            state = "dead_local"
        elif (d.get("max_sharpe") or 0) >= 1.58:
            state = "near_gate"
        elif (d.get("max_sharpe") or 0) >= 1.0:
            state = "has_signal"
        elif d.get("campaign_status") == "untried":
            state = "untried"
        else:
            state = "explored"
        out[(region, fam)] = {"state": state, **{k: v for k, v in d.items() if k != "state"}}
    return out, red


def main():
    ap = argparse.ArgumentParser(description="家族导航：信号族粒度全局状态图（选波前先查图）")
    add_campaign_arg(ap)
    ap.add_argument("--all", action="store_true", help="全区域（缺省仅当前战役 region）")
    ap.add_argument("--state", help="过滤状态（如 untried/near_gate/dead_xregion）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    db = _db_path(ctx)

    fams, red = load_families(db)
    regions = sorted({k[0] for k in fams}) if a.all else [ctx.region]
    rows = []
    for (region, fam), d in sorted(fams.items()):
        if region not in regions:
            continue
        if a.state and d["state"] != a.state:
            continue
        rows.append({"region": region, "family": fam, **d})

    if a.json:
        print(json.dumps({"generated_at": datetime.now().isoformat(timespec="seconds"),
                          "families": rows}, ensure_ascii=False, indent=1))
        return
    print(f"[atlas] {len(rows)} 个信号族（region={'ALL' if a.all else ctx.region}）")
    print(f"{'region':6s} {'family':30s} {'state':14s} evidence")
    for r in rows:
        ev = f"win={r.get('win',0)} dead={r.get('dead',0)}"
        if r.get("max_sharpe") is not None:
            ev += f" maxS={r['max_sharpe']:.2f}"
        if r.get("os_decay"):
            ev += f" os_decay={r['os_decay']}"
        if r.get("campaign_status"):
            ev += f" camp={r['campaign_status']}"
        print(f"{r['region']:6s} {r['family']:30s} {r['state']:14s} {ev}")


if __name__ == "__main__":
    main()
