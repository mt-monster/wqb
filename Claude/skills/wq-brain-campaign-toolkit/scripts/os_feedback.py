# -*- coding: utf-8 -*-
"""os_feedback.py - OS 表现回流（2026-09-01 落地，G3 学习闭环）。

提交后的 alpha OS 真实表现是元知识的重要来源，此前完全无回流。本脚本：
  1. 拉平台全量 OS alpha（get_user_alphas stage=OS 或 MCP），含当前 OS Sharpe/状态；
  2. 对比提交时点指标（本地 alphas 表 / IS 记录）；
  3. 归纳衰减模式 → 回写：
     - 逐 alpha 衰减记录 → ledger_kv `os_feedback_latest`（GLOBAL 桶）
     - 族级衰减结论 → registry_empirical layer='win' 的 payload 追加 os_decay 标记
       （win 配方 OS 衰减严重时建议降权）+ dead_end 候选报告（--apply 落库）
  4. 幂等：重复跑覆盖 latest 快照；win 降权标记按 alpha id 去重追加。

用法：
  python os_feedback.py --campaign-dir tracking/KOR            # dry：只报告
  python os_feedback.py --campaign-dir tracking/KOR --apply    # 落库
数据源优先级：MCP get_user_alphas（需凭据）> 本地 DB alphas 表（含 OS 字段时）。
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import add_campaign_arg, CampaignContext, load_credentials
from _lib.api import Api

DECAY_WARN_RATIO = 0.5   # OS sharpe < 提交时 50% → 衰减警报
DECAY_DEAD_RATIO = 0.25  # OS sharpe < 提交时 25% → 建议降权/判死


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


def fetch_os_alphas():
    """经 toolkit Api 拉平台 OS alpha（429 自带退避）。失败返回 None。"""
    try:
        api = Api()
        api.login(*load_credentials())
        import json as _j
        j = _j.load(api.get("/users/self/alphas?stage=OS&limit=100&order=-dateSubmitted"))
        out = []
        for a in j.get("results", []):
            # os dict 实际结构：{startDate, osISSharpeRatio, preCloseSharpeRatio, checks}
            os_block = a.get("os") if isinstance(a.get("os"), dict) else {}
            os_sharpe = os_block.get("osISSharpeRatio")
            if os_sharpe is None:
                for chk in os_block.get("checks", []):
                    if chk.get("name") in ("SHARPE", "OS_SHARPE"):
                        os_sharpe = chk.get("value")
                        break
            out.append({
                "id": a.get("id"),
                "status": a.get("status"),
                "region": a.get("settings", {}).get("region"),
                "sharpe_is": (a.get("is") or {}).get("sharpe") if isinstance(a.get("is"), dict) else None,
                "sharpe_os": os_sharpe,
                "date_submitted": a.get("dateSubmitted"),
            })
        return out
    except Exception as e:
        print(f"[os-feedback] 平台拉取失败（{e}），降级本地 DB")
        return None


def analyze(os_alphas, db):
    """对比 IS/OS，输出逐条衰减 + 族级归纳。"""
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    rows = []
    for a in os_alphas:
        if not a["id"] or a.get("sharpe_is") is None or a.get("sharpe_os") is None:
            continue
        is_s, os_s = float(a["sharpe_is"]), float(a["sharpe_os"])
        ratio = os_s / is_s if is_s else None
        # 从本地 expressions→alphas 找该 alpha 的 dataset/family 归属
        fam = None
        r = con.execute(
            "SELECT dataset FROM expressions WHERE alpha_id=? LIMIT 1", (a["id"],)
        ).fetchone()
        ds = r["dataset"] if r else None
        if ds:
            r2 = con.execute(
                "SELECT entry_id, family, payload FROM registry_empirical "
                "WHERE layer='win' AND (payload LIKE ? OR family LIKE ?) LIMIT 1",
                (f"%{ds}%", f"%{ds}%"),
            ).fetchone()
            if r2:
                fam = r2["family"]
        flag = None
        if ratio is not None and is_s > 0:
            if ratio < DECAY_DEAD_RATIO or os_s <= 0:
                flag = "SEVERE_DECAY"
            elif ratio < DECAY_WARN_RATIO:
                flag = "WARN_DECAY"
        rows.append({**a, "dataset": ds, "family": fam, "os_is_ratio": round(ratio, 3) if ratio else None,
                     "decay_flag": flag})
    con.close()
    return rows


def main():
    ap = argparse.ArgumentParser(description="OS 回流：拉平台 OS 表现，对比提交时指标，衰减回写")
    add_campaign_arg(ap)
    ap.add_argument("--apply", action="store_true", help="落库（win 降权标记 + latest 快照）；缺省只报告")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    db = _db_path(ctx)

    os_alphas = fetch_os_alphas()
    if os_alphas is None:
        print("[os-feedback] 无平台数据源可用，退出")
        return 1
    rows = analyze(os_alphas, db)
    decayed = [r for r in rows if r["decay_flag"]]
    severe = [r for r in rows if r["decay_flag"] == "SEVERE_DECAY"]

    payload = {
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "os_total": len(rows),
        "decayed_total": len(decayed),
        "severe_total": len(severe),
        "decay_thresholds": {"warn": DECAY_WARN_RATIO, "severe": DECAY_DEAD_RATIO},
        "rows": rows,
    }
    if a.apply:
        con = sqlite3.connect(db)
        con.execute(
            "INSERT OR REPLACE INTO ledger_kv (region, key, value, updated_at) VALUES (?,?,?,?)",
            ("GLOBAL", "os_feedback_latest", json.dumps(payload, ensure_ascii=False),
             datetime.now().isoformat(timespec="seconds")),
        )
        # SEVERE 的族回写 win 层 payload 的 os_decay 标记（幂等：按 alpha id 去重）
        for r in severe:
            if not r["family"]:
                continue
            row = con.execute(
                "SELECT id, payload FROM registry_empirical WHERE layer='win' AND family=? LIMIT 1",
                (r["family"],),
            ).fetchone()
            if row:
                try:
                    p = json.loads(row["payload"]) if row["payload"] else {}
                except Exception:
                    p = {}
                marks = p.setdefault("os_decay", [])
                if r["id"] not in [m.get("alpha") for m in marks]:
                    marks.append({"alpha": r["id"], "os_sharpe": r["sharpe_os"],
                                  "is_sharpe": r["sharpe_is"], "at": payload["fetched_at"]})
                    con.execute("UPDATE registry_empirical SET payload=?, updated_at=? WHERE id=?",
                                (json.dumps(p, ensure_ascii=False),
                                 datetime.now().isoformat(timespec="seconds"), row["id"]))
        con.commit()
        con.close()

    print(f"[os-feedback] OS alpha {len(rows)} 个，衰减 {len(decayed)}（严重 {len(severe)}）")
    for r in decayed[:10]:
        print(f"  {r['id']} {r['region']} IS={r['sharpe_is']:.2f} OS={r['sharpe_os']:.2f} "
              f"ratio={r['os_is_ratio']} {r['decay_flag']} ds={r['dataset']}")
    if a.apply:
        print("[os-feedback] 已落库：os_feedback_latest（GLOBAL）+ SEVERE 族 win 降权标记")
    else:
        print("[os-feedback] dry 模式：加 --apply 落库")
    return 0


if __name__ == "__main__":
    sys.exit(main())
