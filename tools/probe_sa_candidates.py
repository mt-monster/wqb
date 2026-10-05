#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe_sa_candidates.py — SA（Super Alpha）候选与组件池现状盘点。

与 tools/submit_inventory.py 互补：后者盘 RA（REGULAR），本脚本盘 SA（SUPER）。

SA 关键事实（平台官方语义，见 world-quant-brain-mcp/super_alpha_tool.py）：
  * SA = 对「本账户该区域 ACTIVE 已提交 alpha」做 selection（按 weight 降序取前
    selectionLimit，最小 10）+ combo（每个被选 alpha 的日度权重，常量 1 = 等权）。
  * **硬前置**：同区域 ≥10 颗 ACTIVE REGULAR 组件，否则选不出 10 个 → 不可建 SA。
  * 组件 eligibility 只看「已提交且 ACTIVE」——IS 阶段 UNSUBMITTED 的 REGULAR
    **不计入**，因此「攒着可提交的 RA」必须先提交才能成为 SA 组件。
  * 配额：REGULAR 4/天/区，SUPER 1/天/区（独立计数，见 src/wqb/quota.py）。
  * SA 可提交的 selection 字段无 sharpe/fitness——只能按 turnover/decay/
    truncation/self_correlation/prod_correlation/category/datasets 等筛。

用法:
  python tools/probe_sa_candidates.py
  python tools/probe_sa_candidates.py --regions USA,KOR,IND
  python tools/probe_sa_candidates.py --json results/sa_candidates.json

退出码: 0=正常  3=平台/鉴权失败
"""
import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402

REPO = _pyenv.REPO_ROOT
RESULTS_DIR = REPO / "results"
MIN_ELIGIBLE = 10


def _bootstrap():
    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()


def _now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _is_super(a):
    """判 SUPER：settings 含 SA 专有键，或 type/is_super 显式标记。"""
    if not isinstance(a, dict):
        return False
    if str(a.get("type") or "").upper() == "SUPER":
        return True
    if a.get("is_super"):
        return True
    s = a.get("settings") or {}
    return any(k in s for k in ("selectionHandling", "selectionLimit", "componentActivation"))


async def _fetch_stage(brain, stage, alpha_type, limit_hint=950):
    """按 offset 翻页拉取某 stage 的 alpha 列表（平台 offset 窗口上限 ~1000）。"""
    out, off = [], 0
    while off < limit_hint:
        d = await brain.get_user_alphas(stage=stage, limit=50, alpha_type=alpha_type,
                                        order="-dateSubmitted", offset=off)
        res = d.get("results") or []
        if not res:
            break
        out.extend(res)
        if len(res) < 50:
            break
        off += 50
    return out


async def _component_pool(brain, region):
    """该区域 ACTIVE REGULAR 组件池（IS+OS 去重；只认 ACTIVE）。"""
    seen, pool = set(), []
    for stage in ("OS", "IS"):
        for a in await _fetch_stage(brain, stage, "REGULAR"):
            s = a.get("settings") or {}
            if (s.get("region") or a.get("region")) != region:
                continue
            if a["id"] in seen:
                continue
            seen.add(a["id"])
            pool.append({
                "id": a["id"], "stage": stage, "status": a.get("status"),
                "name": a.get("name"), "dateCreated": a.get("dateCreated"),
                "dateSubmitted": a.get("dateSubmitted"),
                "sharpe": (a.get("is") or {}).get("sharpe"),
                "fitness": (a.get("is") or {}).get("fitness"),
                "submitted": bool(a.get("dateSubmitted")),
            })
    return pool


async def _all_sups(brain):
    """本账户全部 SUPER alpha（IS+OS 去重）。"""
    seen, out = set(), []
    for stage in ("OS", "IS"):
        for a in await _fetch_stage(brain, stage, None):
            if not _is_super(a):
                continue
            if a["id"] in seen:
                continue
            seen.add(a["id"])
            s = a.get("settings") or {}
            out.append({
                "id": a["id"], "stage": stage, "status": a.get("status"),
                "region": s.get("region") or a.get("region"),
                "name": a.get("name"),
                "dateCreated": a.get("dateCreated"),
                "dateSubmitted": a.get("dateSubmitted"),
                "selectionLimit": s.get("selectionLimit"),
                "selectionHandling": s.get("selectionHandling"),
                "sharpe": (a.get("is") or {}).get("sharpe"),
                "fitness": (a.get("is") or {}).get("fitness"),
                "tags": a.get("tags") or [],
                "prod": a.get("prod"),
            })
    return out


def _group(rows, key):
    out = {}
    for r in rows:
        k = str(r.get(key) if r.get(key) is not None else "None")
        out.setdefault(k, []).append(r)
    return out


async def run(regions, out_json, min_eligible=MIN_ELIGIBLE):
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    report = {"generated_at": _now_iso(), "min_eligible": min_eligible,
              "regions": {}, "super_alphas": {}}

    # ---------- 1. 组件池 eligibility ----------
    print("=" * 92)
    print("SA 候选盘点 · 组件池 eligibility（硬前置 ≥%d 颗 ACTIVE REGULAR）" % min_eligible)
    print("=" * 92)
    print(f"{'区域':<5} {'ACTIVE':>7} {'UNSUBMITTED':>12} {'ACTIVE已提交':>12} "
          f"{'总计':>6}  verdict")
    go_regions = []
    for reg in regions:
        pool = await _component_pool(brain, reg)
        active = [p for p in pool if p["status"] == "ACTIVE"]
        active_sub = [p for p in active if p["submitted"]]
        unsubmitted = [p for p in pool if not p["submitted"] and p["status"] != "ACTIVE"]
        elig = len(active_sub)
        verdict = "GO" if elig >= min_eligible else "BLOCKED"
        if verdict == "GO":
            go_regions.append(reg)
        print(f"{reg:<5} {len(active):>7} {len(unsubmitted):>12} {elig:>12} "
              f"{len(pool):>6}  {verdict}"
              f"{'（差 %d 颗）' % (min_eligible - elig) if verdict == 'BLOCKED' else ''}")
        report["regions"][reg] = {
            "eligible_active_submitted": elig, "active": len(active),
            "unsubmitted_is": len(unsubmitted), "total_regular": len(pool),
            "verdict": verdict, "active_submitted_ids": [p["id"] for p in active_sub],
            "unsubmitted_is_ids": [p["id"] for p in unsubmitted],
        }
        print(f"      {'':<12}未提交 IS 组件候选 {len(unsubmitted)} 颗："
              f"{', '.join(p['id'] for p in sorted(unsubmitted, key=lambda x: str(x['dateCreated']), reverse=True)[:12])}"
              f"{' …' if len(unsubmitted) > 12 else ''}")
    print(f"\nGO 区域（可建 SA）：{', '.join(go_regions) if go_regions else '（无）'}")

    # ---------- 2. 已有 SA 全景 ----------
    print()
    print("=" * 92)
    print("本账户全部 SUPER alpha（IS+OS 去重）")
    print("=" * 92)
    sups = await _all_sups(brain)
    by_stage = _group(sups, "stage")
    by_status = _group(sups, "status")
    by_region = _group(sups, "region")
    print(f"总计 {len(sups)} 颗  |  stage: "
          + "  ".join(f"{k}={len(v)}" for k, v in sorted(by_stage.items())))
    print(f"               status: " + "  ".join(f"{k}={len(v)}" for k, v in sorted(by_status.items())))
    print(f"               region: " + "  ".join(f"{k}={len(v)}" for k, v in sorted(by_region.items())))

    active_sups = [s for s in sups if s["status"] == "ACTIVE"]
    unsubmitted_sups = [s for s in sups if not s["dateSubmitted"] and s["status"] != "ACTIVE"]
    report["super_alphas"] = {
        "total": len(sups),
        "by_stage": {k: len(v) for k, v in by_stage.items()},
        "by_status": {k: len(v) for k, v in by_status.items()},
        "by_region": {k: len(v) for k, v in by_region.items()},
        "active": active_sups, "unsubmitted_candidates": unsubmitted_sups,
        "all": sups,
    }

    print(f"\n【ACTIVE SA】{len(active_sups)} 颗（已提交上线）")
    print(f"  {'ID':<10} {'region':<6} {'selLimit':>8} {'handling':<9} {'name'}")
    for s in sorted(active_sups, key=lambda x: str(x["dateSubmitted"] or ""), reverse=True):
        print(f"  {s['id']:<10} {str(s['region']):<6} "
              f"{str(s['selectionLimit']):>8} {str(s['selectionHandling']):<9} "
              f"{str(s['name'])[:44]}  ({str(s['dateSubmitted'])[:10]})")

    print(f"\n【SA 候选】UNSUBMITTED SUPER {len(unsubmitted_sups)} 颗"
          "（已建未提交；提交需 SUPER 配额 1/天/区）")
    if unsubmitted_sups:
        print(f"  {'ID':<10} {'stage':<5} {'status':<12} {'region':<6} {'selLimit':>8} {'sharpe':>7} {'fitness':>7}  name")
        for s in sorted(unsubmitted_sups, key=lambda x: str(x["dateCreated"] or ""), reverse=True):
            print(f"  {s['id']:<10} {str(s['stage']):<5} {str(s['status']):<12} "
                  f"{str(s['region']):<6} {str(s['selectionLimit']):>8} "
                  f"{str(s['sharpe']):>7} {str(s['fitness']):>7}  "
                  f"{str(s['name'])[:38]} ({str(s['dateCreated'])[:10]})")
    else:
        print("  （无：当前没有「已建未提交」的 SA。要新增 SA 候选需先跑 selection+combo 仿真）")

    # ---------- 3. 结论 ----------
    print()
    print("=" * 92)
    print("结论")
    print("=" * 92)
    print(f"  1) 可建 SA 的区域：{', '.join(go_regions) if go_regions else '（无）'}")
    print(f"  2) 已 ACTIVE SA：{len(active_sups)} 颗（跨 "
          + "、".join(sorted(k for k in by_region if any(s['status'] == 'ACTIVE' for s in by_region[k]))) + "）")
    print(f"  3) 未提交 SA 候选：{len(unsubmitted_sups)} 颗")
    blocked = [r for r, v in report["regions"].items() if v["verdict"] == "BLOCKED"]
    if blocked:
        print("  4) 组件不足的区域：" + "；".join(
            f"{r}（{report['regions'][r]['eligible_active_submitted']}/{min_eligible}）"
            for r in blocked))
        print("     → 需先把该区域「攒着可提交的 RA」提交，ACTIVE 组件数才涨（IS 阶段不计入）")

    if out_json:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = RESULTS_DIR / out_json if "/" in out_json else RESULTS_DIR / f"sa_candidates_{stamp}.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n报告：{path}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="SA 候选与组件池盘点（与 submit_inventory 的 RA 盘点互补）")
    ap.add_argument("--regions", default="USA,IND,KOR,GBR,MEA,GLB,DEU,EUR,ASI,HKG",
                    help="逗号分隔区域列表")
    ap.add_argument("--min-eligible", type=int, default=MIN_ELIGIBLE, help="GO 阈值（默认 10）")
    ap.add_argument("--json", default=None, help="输出 JSON 路径（默认 results/sa_candidates_<ts>.json）")
    ap.add_argument("--save-json", action="store_true", help="保存到 results/（与 --json 二选一）")
    a = ap.parse_args()
    regions = [r.strip().upper() for r in a.regions.split(",") if r.strip()]
    try:
        return asyncio.run(run(regions,
                               a.json or ("sa_candidates.json" if a.save_json else None),
                               a.min_eligible))
    except Exception as e:  # noqa: BLE001
        print(f"盘点失败：{type(e).__name__}: {e}")
        return 3


if __name__ == "__main__":
    _bootstrap()
    sys.exit(main())
