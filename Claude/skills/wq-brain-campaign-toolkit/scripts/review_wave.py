# -*- coding: utf-8 -*-
"""review_wave.py - 通用指标评审与达标筛选。

  - 指标走 metrics_cache 读穿缓存（可复现、可迁移、省配额）
  - 门槛集中 config/thresholds.json（review / near 节）
  - near 池自动诊断卡在哪堵墙（CW/2Y/SHARPE/FITNESS/TVR/MARGIN/RA）
  - missing != fail：指标缺失标 *_UNKNOWN，不误判
  - --write-ledger 自动回写台账 submit_ready / near_pool / salvage_pool（幂等）；
    salvage_pool 收录快达标 combo 候选，供 Mode B 组合腿救援消费（get_salvage_pool）

用法:
  python review_wave.py --campaign-dir <DIR> --multisim <id> [--tag wave01A] [--write-ledger]
  python review_wave.py --campaign-dir <DIR> --alphas KPGZmLMl xxx [--tag manual] [--write-ledger]
"""
import argparse
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import CampaignContext, add_campaign_arg, atomic_write
from _lib.ledger import LedgerStore, make_ledger_store, today
from _lib import rules as rules_mod
from _lib.wqb_store import get_store
import metrics_cache


def walls(r, t):
    """诊断未达标行卡在哪堵墙。指标缺失（None）不算败、单独标 *_UNKNOWN，避免误判。"""
    w = []
    if r.get("sharpe") is None:
        return ["NO_DATA"]
    if r["sharpe"] <= t["sharpe_min"]:
        w.append("SHARPE")
    if r.get("fitness") is None:
        w.append("FIT_UNKNOWN")
    elif r["fitness"] <= t["fitness_min"]:
        w.append("FITNESS")
    if r.get("two_year_sharpe") is None:
        w.append("2Y_UNKNOWN")  # 平台未返回 LOW_2Y_SHARPE，不能算 2Y 败
    elif r["two_year_sharpe"] <= t["two_year_sharpe_min"]:
        w.append("2Y")
    if r.get("margin_bp") is None:
        w.append("MARGIN_UNKNOWN")
    elif r["margin_bp"] <= t["margin_min"] * 10000:
        w.append("MARGIN")
    tv = r.get("turnover_pct")
    if tv is None:
        w.append("TVR_UNKNOWN")
    elif not (t["turnover_min"] * 100 < tv < t["turnover_max"] * 100):
        w.append("TVR")
    for fc in r.get("failed_checks") or []:
        w.append("CW" if "CONCENTRATED" in fc else fc)
    return w or ["RA_OTHER"]


def passes(r, t):
    return (r.get("sharpe") is not None and r["sharpe"] > t["sharpe_min"]
            and (r.get("fitness") or 0) > t["fitness_min"]
            and (r.get("two_year_sharpe") or 0) > t["two_year_sharpe_min"]
            and (r.get("margin_bp") or 0) > t["margin_min"] * 10000
            and r.get("turnover_pct") is not None
            and t["turnover_min"] * 100 < r["turnover_pct"] < t["turnover_max"] * 100
            and not r.get("failed_checks"))


def combo_candidate(r, t):
    """P0-1 组合候选池（2026-08-31）：中等信号可进 Mode B 组合提升，而非仅 near 池。

    判据：S>=combo_sharpe_min（默认 1.0，低于 review.sharpe_min=1.58）
    且 prod_corr<combo_prod_corr_max（默认 0.5，结构性墙前兆反向指标）
    且无 CONCENTRATED_WEIGHT 硬失败。
    IND 实证：单字段 S 1.0-1.5 的信号经低相关组合后常跃升到 1.58+。
    """
    if r.get("sharpe") is None:
        return False
    if r["sharpe"] <= t.get("combo_sharpe_min", 1.0):
        return False
    pc = r.get("prod_corr")
    if pc is not None and pc >= t.get("combo_prod_corr_max", 0.5):
        return False
    for fc in r.get("failed_checks") or []:
        if "CONCENTRATED" in fc:
            return False
    return True


def _salvage_entry(r, tag):
    """review 行 -> salvage_pool entry（结构对齐 wqb_db_mcp._salvage_to_pool）。

    入池对象 = combo_candidates（快达标：S>=1.0 且 prod_corr<0.5）+ near 补充；
    标注 boost_dims 供 Mode B 组合腿救援按卡点消费（get_salvage_pool boost_dim）。
    """
    sh, fit = r.get("sharpe"), r.get("fitness")
    ty, tvr_pct = r.get("two_year_sharpe"), r.get("turnover_pct")
    tvr = (tvr_pct / 100.0) if isinstance(tvr_pct, (int, float)) else None
    code = r.get("code") or ""
    boost = []
    if isinstance(ty, (int, float)) and ty >= 1.0:
        boost.append("boost_2y")
    if isinstance(tvr, (int, float)) and tvr <= 0.25:
        boost.append("boost_tvr")
    if isinstance(sh, (int, float)) and sh >= 0.5:
        boost.append("boost_sharpe")
    if not any("CONCENTRATED" in (fc or "") for fc in r.get("failed_checks") or []):
        boost.append("boost_cw")  # 无权重集中失败 -> 可作子宇宙稳健补强腿
    m = re.search(r"(anl\d+|fnd\d+|pv\d+|risk\d+|shortinterest\d+|intraday_\w+|mmp_\w+|news\d+|model\d+)", code)
    return {"alpha_id": r["id"], "expression": code,
            "dataset": m.group(1) if m else None,
            "wave": str(tag), "sharpe": sh, "fitness": fit,
            "two_year_sharpe": ty, "turnover": tvr,
            "boost_dims": boost, "walls": r.get("walls") or [],
            "source": f"review {tag}", "salvaged_at": today()}


def main():
    ap = argparse.ArgumentParser(description="指标评审与达标筛选")
    add_campaign_arg(ap)
    ap.add_argument("--multisim")
    ap.add_argument("--alphas", nargs="+")
    ap.add_argument("--tag")
    ap.add_argument("--write-ledger", action="store_true")
    ap.add_argument("--refresh", action="store_true", help="绕过缓存强制回源")
    ap.add_argument("--out", default=None, help="输出文件重定向（默认 reviews/<region>_review_<tag>.json）")
    ap.add_argument("--coverage-writeback", default="auto", choices=["auto", "never"],
                    help="L4 算子回写：auto=评审后自动回写每算子最佳 sharpe 到覆盖台账（默认）；never=禁用")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)

    if a.multisim:
        ids = metrics_cache.MetricsFetcher(ctx).multisim_alpha_ids(a.multisim)
        tag = a.tag or a.multisim
    elif a.alphas:
        ids, tag = a.alphas, (a.tag or "manual")
    else:
        ap.error("need --multisim or --alphas")

    t = ctx.thresh("review")
    rows = metrics_cache.fetch_rows(ctx, ids, refresh=a.refresh)
    candidates = [r for r in rows if passes(r, t)]
    # P0-1 组合候选池：中等信号（S>=1.0 且 prod_corr<0.5）可进 Mode B 组合提升
    combo_candidates = [r for r in rows if r not in candidates and combo_candidate(r, t)]
    # 给所有行填 walls（candidates 为空表），供推荐引擎与打印共用
    for r in rows:
        r["walls"] = [] if r in candidates else walls(r, t)
    near = []
    for r in rows:
        if r in candidates or r.get("sharpe") is None:
            continue
        if r["sharpe"] > ctx.thresh("near")["sharpe_min"]:
            near.append(r)

    print(f"{'id':10s} {'sh':>6} {'fit':>5} {'2y':>5} {'mg_bp':>7} {'tvr%':>6} {'rn':>5} walls")
    for r in rows:
        w = r["walls"]
        print(f"{r['id']:10s} {r.get('sharpe') or 0:6.2f} {r.get('fitness') or 0:5.2f} "
              f"{r.get('two_year_sharpe') or 0:5.2f} {r.get('margin_bp') or 0:7.2f} "
              f"{r.get('turnover_pct') or 0:6.2f} {r.get('rn_sharpe') or 0:5.2f} {','.join(w) or 'PASS'}")

    # ---- P1 verdict 自动推荐（规则 -> 下波方向，仅建议非强制） ----
    wave_meta = {"region": ctx.region,
                 "universe": (ctx.settings or {}).get("universe"),
                 "dataset": (ctx.settings or {}).get("dataset")}
    recs = rules_mod.recommend_next_wave(ctx, rows, near=near, wave_meta=wave_meta)
    if recs:
        print("\n=== 下波方向推荐（规则驱动，仅建议） ===")
        for i, rc in enumerate(recs, 1):
            src = f" [规则:{rc['source_rule']}]" if rc.get("source_rule") else ""
            print(f"  {i}. [{rc['priority']}] {rc['direction']}{src}")
            print(f"      依据: {rc['rationale']}")
            print(f"      建议: {rc['action_hint']}")

    payload = {"tag": tag, "region": ctx.region,
               "reviewed_at": datetime.datetime.now().isoformat(timespec="seconds"),
               "thresholds": t, "all": rows, "candidates": candidates,
               "combo_candidates": combo_candidates, "near": near,
               "next_wave_recommendations": recs}
    st = get_store(ctx)
    try:
        st.upsert_review(ctx.region, str(tag), payload)
    finally:
        st.close()
    if a.out:
        atomic_write(a.out, payload)  # 仅显式 --out 时写文件（测试）
        print(f"review -> {a.out}")
    print(f"\ntotal={len(rows)} candidates={len(candidates)} combo_candidates={len(combo_candidates)} near={len(near)}")
    print(f"review -> db ledger_kv/{ctx.region}/review_{tag}")

    # ---- wave_results 表入库（DB 为主，JSON 仅排障留痕） ----
    try:
        from _lib.wave_results import WaveResultsStore
        wr = WaveResultsStore(ctx.region)
        ms_ids = [a.multisim] if a.multisim else []
        out_wr = wr.auto_upsert_from_review(
            tag, rows, candidates, near,
            settings=ctx.settings, multisim_ids=ms_ids)
        if out_wr.get("skipped"):
            print(f"[wave_results] 跳过: {out_wr.get('reason')}")
        else:
            print(f"[wave_results] wave{out_wr['wave_number']} -> {out_wr['status']} "
                  f"(findings={out_wr['key_findings_n']} candidates={out_wr['candidates_n']})")
    except Exception as e:
        print(f"[wave_results] 入库异常（不阻断）: {e}")

    # ---- L4 算子覆盖回写（③c，region 无关）：每算子本波最佳 sharpe 沉淀到覆盖台账 ----
    # 2026-08-18：从本波 rows 的表达式提取算子 × sharpe，调 update_from_results 回写，
    # 供下一波 plan_coverage_wave 按遗忘度+算子级偏好排序。code 截断 110 字符影响有限
    # （仅少记尾部算子，不错记）。
    if a.coverage_writeback != "never":
        try:
            from _lib import operator_coverage as oc
            op_sh = {}
            for r in rows:
                sh = r.get("sharpe")
                if not isinstance(sh, (int, float)):
                    continue
                for op in oc._extract_ops(r.get("code") or ""):
                    if op not in op_sh or abs(sh) > abs(op_sh[op]):
                        op_sh[op] = sh
            if op_sh:
                stats = oc.update_from_results(ctx, op_sh)
                print(f"[coverage] L4 回写 {len(op_sh)} 算子最佳 sharpe，"
                      f"覆盖度 {stats['used']}/{stats['total']} ({stats['coverage_rate']*100:.1f}%)")
        except Exception as _we:
            print(f"[coverage] L4 回写跳过：{_we}")

    if a.write_ledger:
        store = make_ledger_store(ctx)

        def mut(d):
            sr = d.setdefault("submit_ready", [])
            for c in candidates:
                if not any((x.get("id") if isinstance(x, dict) else x) == c["id"] for x in sr):
                    sr.append({"id": c["id"], "note": f"review {tag} 全门槛过",
                               "queued_at": today()})
            d.setdefault("near_pool", []).append({
                "tag": tag, "at": today(),
                "near": [{"id": n["id"], "sharpe": n["sharpe"], "walls": n["walls"]} for n in near]})
            # salvage_pool：快达标因子（combo_candidates + near 补充）幂等入池，
            # 供 Mode B 组合腿救援消费（区域无关通用机制；结构对齐 _salvage_to_pool）。
            pool = d.setdefault("salvage_pool", {"entries": [], "updated_at": None})
            pool.setdefault("entries", [])
            known = {e.get("alpha_id") for e in pool["entries"] if e.get("alpha_id")}
            combo_ids = {c["id"] for c in combo_candidates}
            salvage_src = list(combo_candidates) + [n for n in near if n["id"] not in combo_ids]
            for r in salvage_src:
                if r["id"] not in known:
                    pool["entries"].append(_salvage_entry(r, tag))
                    known.add(r["id"])
            pool["updated_at"] = today()
        d = store.update(mut)
        sp = d.get("salvage_pool", {}).get("entries", [])
        print(f"ledger: submit_ready +{len(candidates)}, near_pool +{len(near)}, "
              f"salvage_pool={len(sp)} entries")


if __name__ == "__main__":
    main()
