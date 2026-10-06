#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe_sa_candidates.py — SA（Super Alpha）候选与组件池现状盘点。

与 tools/verdict/submit_inventory.py 互补：后者盘 RA（REGULAR），本脚本盘 SA（SUPER）。

SA 关键事实（平台官方语义，见 world-quant-brain-mcp/super_alpha_tool.py）：
  * SA = 对「本账户该区域 ACTIVE 已提交 alpha」做 selection（按 weight 降序取前
    selectionLimit，最小 10）+ combo（每个被选 alpha 的日度权重，常量 1 = 等权）。
  * **硬前置**：同区域 ≥10 颗 ACTIVE REGULAR 组件，否则选不出 10 个 → 不可建 SA。
  * 组件 eligibility 只看「已提交且 ACTIVE」——IS 阶段 UNSUBMITTED 的 REGULAR
    **不计入**，因此「攒着可提交的 RA」必须先提交才能成为 SA 组件。
  * 配额：REGULAR 4/天/区，SUPER 1/天/区（独立计数，见 src/wqb/quota.py）。
  * SA 可提交的 selection 字段无 sharpe/fitness——只能按 turnover/decay/
    truncation/self_correlation/prod_correlation/category/datasets 等筛。

【缓存层（2026-10-05 新增）】
  平台翻页慢（10 区域 × IS+OS × 多页 ≈ 14min），但 SA 状态只在「提交 / 新建 alpha」
  时变化，盘点全程只读不提交 → 缓存安全且必要。
  - 主缓存：results/sa_probe_cache.json（固定路径，TTL 默认 6h，可用 env SA_PROBE_CACHE_TTL_HOURS 覆盖）。
  - 默认读缓存；--refresh 强制翻平台并覆写缓存；--no-cache 关读（仍写归档）。
  - 无主缓存时，自动把最近一份 sa_candidates_*.json（新鲜）提升为缓存，避免改完首跑仍等 14min。
  - ⚠ 提交 / 新建 SA 后，须 --refresh 才能拿到新状态（TTL 内不会自动失效；建议提交后立即 --refresh）。

用法:
  python tools/probe/probe_sa_candidates.py                      # 默认：优先缓存，命中即秒回
  python tools/probe/probe_sa_candidates.py --refresh            # 强制翻平台 + 刷新缓存
  python tools/probe/probe_sa_candidates.py --regions USA,KOR,IND
  python tools/probe/probe_sa_candidates.py --json results/sa_candidates.json

退出码: 0=正常  3=平台/鉴权失败
"""
import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # 同主题目录的兄弟脚本
sys.path.insert(0, os.path.dirname(_HERE))       # tools/（_pyenv 在此；2026-10-06 下沉到主题目录后必需）
import _pyenv  # noqa: E402

REPO = _pyenv.REPO_ROOT
RESULTS_DIR = REPO / "results"
MIN_ELIGIBLE = 10

# ---- SA 缓存层 ----
CACHE_PATH = RESULTS_DIR / "sa_probe_cache.json"
# 默认 6h：SA 状态只在「提交 / 新建 alpha」时变化，但一天可能多次提交，
# 故 TTL 比 24h 更紧；可用 env SA_PROBE_CACHE_TTL_HOURS 覆盖（如设 1 表示每次提交后 1h 内必 --refresh）。
DEFAULT_TTL_HOURS = float(os.environ.get("SA_PROBE_CACHE_TTL_HOURS", "6"))


def _bootstrap():
    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()


def _now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _iso_to_dt(s):
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def _cache_fresh(path, ttl_hours):
    """判断某 JSON 报告是否仍在 TTL 内（按 generated_at）。"""
    if not path or not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    gen = _iso_to_dt(data.get("generated_at", ""))
    if gen is None:
        return False
    age_h = (datetime.now().astimezone() - gen).total_seconds() / 3600.0
    return age_h <= ttl_hours


def _load_report(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _save_cache(report, path=CACHE_PATH):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")


def _seed_from_latest(ttl_hours):
    """无主缓存时，返回最近一份仍在 TTL 内的 sa_candidates_*.json。"""
    cands = sorted(RESULTS_DIR.glob("sa_candidates_*.json"), key=lambda p: p.name, reverse=True)
    for c in cands:
        if _cache_fresh(c, ttl_hours):
            return c
    return None


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


async def _build_report(brain, regions, min_eligible=MIN_ELIGIBLE):
    """翻平台构建 report dict（不打印）。"""
    report = {"generated_at": _now_iso(), "min_eligible": min_eligible,
              "regions": {}, "super_alphas": {}}

    # ---------- 1. 组件池 eligibility ----------
    for reg in regions:
        pool = await _component_pool(brain, reg)
        active = [p for p in pool if p["status"] == "ACTIVE"]
        active_sub = [p for p in active if p["submitted"]]
        unsubmitted = [p for p in pool if not p["submitted"] and p["status"] != "ACTIVE"]
        elig = len(active_sub)
        verdict = "GO" if elig >= min_eligible else "BLOCKED"
        report["regions"][reg] = {
            "eligible_active_submitted": elig, "active": len(active),
            "unsubmitted_is": len(unsubmitted), "total_regular": len(pool),
            "verdict": verdict, "active_submitted_ids": [p["id"] for p in active_sub],
            "unsubmitted_is_ids": [p["id"] for p in unsubmitted],
        }

    # ---------- 2. 已有 SA 全景 ----------
    sups = await _all_sups(brain)
    by_stage = _group(sups, "stage")
    by_status = _group(sups, "status")
    by_region = _group(sups, "region")
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
    return report


def _print_report(report, regions):
    min_eligible = report["min_eligible"]
    reg = report["regions"]

    # ---------- 1. 组件池 eligibility ----------
    print("=" * 92)
    print("SA 候选盘点 · 组件池 eligibility（硬前置 ≥%d 颗 ACTIVE REGULAR）" % min_eligible)
    print("=" * 92)
    print(f"{'区域':<5} {'ACTIVE':>7} {'UNSUBMITTED':>12} {'ACTIVE已提交':>12} "
          f"{'总计':>6}  verdict")
    go_regions = []
    for r in regions:
        rv = reg.get(r, {})
        elig = rv.get("eligible_active_submitted", 0)
        verdict = rv.get("verdict", "BLOCKED")
        if verdict == "GO":
            go_regions.append(r)
        print(f"{r:<5} {rv.get('active',0):>7} {rv.get('unsubmitted_is',0):>12} {elig:>12} "
              f"{rv.get('total_regular',0):>6}  {verdict}"
              f"{'（差 %d 颗）' % (min_eligible - elig) if verdict == 'BLOCKED' else ''}")
        unsub = rv.get("unsubmitted_is_ids", [])
        if unsub:
            print(f"      {'':<12}未提交 IS 组件候选 {len(unsub)} 颗："
                  f"{', '.join(sorted(unsub, key=lambda x: str(x), reverse=True)[:12])}"
                  f"{' …' if len(unsub) > 12 else ''}")
    print(f"\nGO 区域（可建 SA）：{', '.join(go_regions) if go_regions else '（无）'}")

    # ---------- 2. 已有 SA 全景 ----------
    sa = report["super_alphas"]
    print()
    print("=" * 92)
    print("本账户全部 SUPER alpha（IS+OS 去重）")
    print("=" * 92)
    print(f"总计 {sa['total']} 颗  |  stage: "
          + "  ".join(f"{k}={v}" for k, v in sorted(sa.get('by_stage', {}).items())))
    print(f"               status: " + "  ".join(f"{k}={v}" for k, v in sorted(sa.get('by_status', {}).items())))
    print(f"               region: " + "  ".join(f"{k}={v}" for k, v in sorted(sa.get('by_region', {}).items())))

    active_sups = sa.get("active", [])
    unsubmitted_sups = sa.get("unsubmitted_candidates", [])
    print(f"\n【ACTIVE SA】{len(active_sups)} 颗（已提交上线）")
    print(f"  {'ID':<10} {'region':<6} {'selLimit':>8} {'handling':<9} {'name'}")
    for s in sorted(active_sups, key=lambda x: str(x.get("dateSubmitted") or ""), reverse=True):
        print(f"  {s['id']:<10} {str(s.get('region')):<6} "
              f"{str(s.get('selectionLimit')):>8} {str(s.get('selectionHandling')):<9} "
              f"{str(s.get('name'))[:44]}  ({str(s.get('dateSubmitted'))[:10]})")

    print(f"\n【SA 候选】UNSUBMITTED SUPER {len(unsubmitted_sups)} 颗"
          "（已建未提交；提交需 SUPER 配额 1/天/区）")
    if unsubmitted_sups:
        print(f"  {'ID':<10} {'stage':<5} {'status':<12} {'region':<6} {'selLimit':>8} {'sharpe':>7} {'fitness':>7}  name")
        for s in sorted(unsubmitted_sups, key=lambda x: str(x.get("dateCreated") or ""), reverse=True):
            print(f"  {s['id']:<10} {str(s.get('stage')):<5} {str(s.get('status')):<12} "
                  f"{str(s.get('region')):<6} {str(s.get('selectionLimit')):>8} "
                  f"{str(s.get('sharpe')):>7} {str(s.get('fitness')):>7}  "
                  f"{str(s.get('name'))[:38]} ({str(s.get('dateCreated'))[:10]})")
    else:
        print("  （无：当前没有「已建未提交」的 SA。要新增 SA 候选需先跑 selection+combo 仿真）")

    # ---------- 3. 结论 ----------
    print()
    print("=" * 92)
    print("结论")
    print("=" * 92)
    print(f"  1) 可建 SA 的区域：{', '.join(go_regions) if go_regions else '（无）'}")
    active_regions = sorted({str(s.get('region')) for s in active_sups})
    print(f"  2) 已 ACTIVE SA：{len(active_sups)} 颗（跨 " + "、".join(active_regions) + "）")
    print(f"  3) 未提交 SA 候选：{len(unsubmitted_sups)} 颗")
    blocked = [r for r, v in reg.items() if v.get("verdict") == "BLOCKED"]
    if blocked:
        print("  4) 组件不足的区域：" + "；".join(
            f"{r}（{reg[r]['eligible_active_submitted']}/{min_eligible}）"
            for r in blocked))
        print("     → 需先把该区域「攒着可提交的 RA」提交，ACTIVE 组件数才涨（IS 阶段不计入）")


async def run(regions, out_json, min_eligible=MIN_ELIGIBLE,
              use_cache=True, force_refresh=False, ttl_hours=DEFAULT_TTL_HOURS):
    from brain_api import BrainApiClient

    cache_hit = None
    if use_cache and not force_refresh and _cache_fresh(CACHE_PATH, ttl_hours):
        report = _load_report(CACHE_PATH)
        cache_hit = f"主缓存 {CACHE_PATH.name}（generated_at={report.get('generated_at')}）"
    elif use_cache and not force_refresh and (seed := _seed_from_latest(ttl_hours)):
        report = _load_report(seed)
        _save_cache(report)  # 提升为正式缓存
        cache_hit = f"历史全量探针 {seed.name}（新鲜，已提升为主缓存）"
    else:
        if force_refresh:
            print("【--refresh】强制翻平台刷新缓存…")
        elif not use_cache:
            print("【--no-cache】跳过缓存读取，直接翻平台…")
        else:
            print("【无新鲜缓存】首次翻平台取数（约 14min）…")
        brain = BrainApiClient()
        await brain.ensure_authenticated()
        report = await _build_report(brain, regions, min_eligible)
        _save_cache(report)
        print(f"\n（已写入主缓存 {CACHE_PATH.name}，下次盘点免翻平台）")

    if cache_hit:
        print("=" * 92)
        print(f"SA 探针命中本地缓存：{cache_hit}")
        print("（跳过平台翻页，节省约 14min；数据仅在提交/新建后变化，如需刷新用 --refresh）")
        print("=" * 92)

    _print_report(report, regions)

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
    ap.add_argument("--refresh", action="store_true", help="强制翻平台并刷新缓存（忽略 TTL）")
    ap.add_argument("--no-cache", action="store_true", help="跳过缓存读取（仍写归档+缓存）")
    ap.add_argument("--cache-ttl-hours", type=float, default=DEFAULT_TTL_HOURS,
                    help="缓存新鲜度窗口小时数（默认 6，可用 env SA_PROBE_CACHE_TTL_HOURS 覆盖）")
    a = ap.parse_args()
    regions = [r.strip().upper() for r in a.regions.split(",") if r.strip()]
    try:
        return asyncio.run(run(regions,
                               a.json or ("sa_candidates.json" if a.save_json else None),
                               a.min_eligible,
                               use_cache=not a.no_cache,
                               force_refresh=a.refresh,
                               ttl_hours=a.cache_ttl_hours))
    except Exception as e:  # noqa: BLE001
        print(f"盘点失败：{type(e).__name__}: {e}")
        return 3


if __name__ == "__main__":
    _bootstrap()
    sys.exit(main())
