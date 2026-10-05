#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""verify_region_op.py — 逐区核验「平台 ACTIVE」的两种口径。

口径（见大纲 §7 / 整合报告 §8）：
  * 平台 strict-active = status=ACTIVE 且 osmosisPoints>0（已分配 OP），排除 DECOMMISSIONED。
  * 探针 eligibility 用的 `active` = status=ACTIVE（不区分 OP），是宽松口径。

本脚本扫 OS+IS 阶段 get_user_alphas(alpha_type="REGULAR")，客户端按 region 过滤，
逐区统计：
  - active_total : status==ACTIVE 的 REGULAR 数（= 探针 `active` 口径）
  - active_op    : 其中 osmosisPoints>0 的数（strict-active）
  - decom        : status==DECOMMISSIONED 的数
并交叉校验 active_total 是否与探针缓存里的 `active` 一致。

用法:
  python tools/verify_region_op.py                 # 全部 10 区
  python tools/verify_region_op.py --regions USA,KOR,IND
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
ALL_REGIONS = ["USA", "IND", "KOR", "GBR", "MEA", "GLB", "DEU", "EUR", "ASI", "HKG"]


async def _fetch_stage(brain, stage, alpha_type, limit_hint=950):
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


def _region_of(a):
    return (a.get("settings") or {}).get("region") or a.get("region")


def _op(a):
    v = a.get("osmosisPoints")
    if v is None:
        return 0
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0


async def run(regions):
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    # 一次拉取全部 OS / IS REGULAR（与探针同口径：limit_hint=950；若全局 >950 末尾会告警）
    seen, all_alphas = set(), []
    for stage in ("OS", "IS"):
        for a in await _fetch_stage(brain, stage, "REGULAR"):
            aid = a.get("id")
            if aid in seen:
                continue
            seen.add(aid)
            all_alphas.append(a)

    # 逐区统计
    stats = {}
    for r in regions:
        active_total = active_op = decom = 0
        for a in all_alphas:
            if _region_of(a) != r:
                continue
            st = a.get("status")
            if st == "ACTIVE":
                active_total += 1
                if _op(a) > 0:
                    active_op += 1
            elif st == "DECOMMISSIONED":
                decom += 1
        stats[r] = {
            "region": r,
            "active_total": active_total,
            "active_op": active_op,
            "decom": decom,
            "active_no_op": active_total - active_op,
        }

    # 交叉校验：与 SA 探针缓存里的 `active` 对比
    cache_path = RESULTS_DIR / "sa_probe_cache.json"
    probe_active = {}
    if cache_path.exists():
        try:
            rep = json.loads(cache_path.read_text(encoding="utf-8"))
            for r, v in (rep.get("regions") or {}).items():
                probe_active[r] = v.get("active")
        except Exception:
            pass

    print("=" * 92)
    print("区域 ACTIVE 两种口径核验（status=ACTIVE vs ACTIVE 且 OP>0）")
    print("=" * 92)
    print(f"{'region':6} {'active(宽松)':>12} {'active+OP>0':>12} {'no_OP':>7} {'DECOM':>7} {'vs探针active':>12}")
    for r in regions:
        s = stats[r]
        pa = probe_active.get(r)
        flag = "" if pa is None or pa == s["active_total"] else f" ⚠探针={pa}"
        print(f"{r:6} {s['active_total']:>12} {s['active_op']:>12} {s['active_no_op']:>7} {s['decom']:>7} {(str(pa) if pa is not None else '-'):>12}{flag}")
    print("-" * 92)
    print("说明：eligibility GO/BLOCKED 当前按宽松口径(active 宽松≥10)；严格口径(active+OP>0)仅作参考。")
    print("若某区 active+OP>0 < 10，则该区在严格口径下不可建 SA。")

    out = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "stage": "OS+IS",
        "regions": stats,
        "probe_active": probe_active,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = RESULTS_DIR / f"region_op_verify_{stamp}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n报告已写：{path}")
    return 0


def main():
    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()
    ap = argparse.ArgumentParser()
    ap.add_argument("--regions", default=",".join(ALL_REGIONS),
                    help="逗号分隔区域，默认全部 10 区")
    args = ap.parse_args()
    regions = [x.strip().upper() for x in args.regions.split(",") if x.strip()]
    try:
        asyncio.run(run(regions))
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
