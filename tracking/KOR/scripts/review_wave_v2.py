# -*- coding: utf-8 -*-
"""review_wave_v2.py - 增强版波次评审：PROD 墙三档分类 + 判死证据链闭环。

在 review_wave.py 基础上增加：
  1. PROD 墙三档分类：<0.75 深耕 / 0.75-0.80 暂挂 / >0.80 判死
  2. 判死证据链检查：设置空间/结构变体/救援武器是否穷尽
  3. 数据集切换建议：满足判死条件时自动生成切换建议
  4. 候选池状态更新：自动回写 dataset_pool

用法:
  python review_wave_v2.py --multisim <id> [--tag wave36A] [--dataset chart_cnn_alpha] [--write-ledger]
"""
import argparse, collections, datetime, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import kor_ledger
import metrics_cache
from campaign_discipline import assess_dataset, decide_switch, PROD_DEEP_MIN, PROD_SUSPEND_MIN

THRESH = json.load(open(os.path.join(ROOT, "config", "thresholds.json"), encoding="utf-8"))


def walls(r, t):
    """诊断未达标行卡在哪堵墙。"""
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
        w.append("2Y_UNKNOWN")
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


def prod_category(prod_corr):
    """PROD 墙三档分类。"""
    if prod_corr is None:
        return "UNKNOWN", "需查 PROD 相关性"
    if prod_corr < PROD_DEEP_MIN:
        return "DEEP", f"PROD {prod_corr:.3f} < {PROD_DEEP_MIN}，有突破空间"
    if prod_corr < PROD_SUSPEND_MIN:
        return "SUSPEND", f"PROD {prod_corr:.3f} 在 {PROD_DEEP_MIN}-{PROD_SUSPEND_MIN}，暂挂"
    return "DEAD", f"PROD {prod_corr:.3f} > {PROD_SUSPEND_MIN}，判死"


def review_with_discipline(rows, dataset, tag, write_ledger=False):
    """带纪律的评审：PROD 分类 + 判死证据链 + 切换建议。"""
    t = THRESH["review"]
    candidates = [r for r in rows if passes(r, t)]
    near = []
    prod_stats = {"DEEP": [], "SUSPEND": [], "DEAD": [], "UNKNOWN": []}
    
    for r in rows:
        if r in candidates or r.get("sharpe") is None:
            continue
        if r["sharpe"] > THRESH["near"]["sharpe_min"]:
            rr = dict(r)
            rr["walls"] = walls(r, t)
            # PROD 分类
            prod_corr = r.get("prod_correlation")
            cat, cat_note = prod_category(prod_corr)
            rr["prod_category"] = cat
            rr["prod_note"] = cat_note
            prod_stats[cat].append(r["id"])
            near.append(rr)
    
    # 判死证据链评估
    discipline_report = None
    if dataset:
        discipline_report = assess_dataset(dataset)
    
    # 切换决策
    switch_decision = None
    if dataset and discipline_report:
        switch_decision = decide_switch(dataset)
    
    # 输出
    print(f"{'id':10s} {'sh':>6} {'fit':>5} {'2y':>5} {'mg_bp':>7} {'tvr%':>6} {'rn':>5} {'PC':>6} {'cat':>8} walls")
    for r in rows:
        w = [] if r in candidates else walls(r, t)
        prod_corr = r.get("prod_correlation")
        cat, _ = prod_category(prod_corr)
        pc_str = f"{prod_corr:.3f}" if prod_corr else "--"
        print(f"{r['id']:10s} {r.get('sharpe') or 0:6.2f} {r.get('fitness') or 0:5.2f} "
              f"{r.get('two_year_sharpe') or 0:5.2f} {r.get('margin_bp') or 0:7.2f} "
              f"{r.get('turnover_pct') or 0:6.2f} {r.get('rn_sharpe') or 0:5.2f} "
              f"{pc_str:>6} {cat:>8} {','.join(w) or 'PASS'}")
    
    print(f"\ntotal={len(rows)} candidates={len(candidates)} near={len(near)}")
    print(f"PROD 分类: DEEP={len(prod_stats['DEEP'])} SUSPEND={len(prod_stats['SUSPEND'])} "
          f"DEAD={len(prod_stats['DEAD'])} UNKNOWN={len(prod_stats['UNKNOWN'])}")
    
    if discipline_report:
        print(f"\n[纪律评估] {dataset}: {discipline_report['category']} - {discipline_report['recommendation']}")
        if discipline_report.get("death_evidence_gap"):
            print(f"  证据链缺口: {'; '.join(discipline_report['death_evidence_gap'])}")
    
    if switch_decision and switch_decision.get("switch_trigger"):
        print(f"\n[切换建议] {switch_decision['switch_reason']}")
        for nt in switch_decision.get("next_targets", [])[:3]:
            print(f"  下一目标: {nt['dataset']} (status={nt['status']}, priority={nt['priority']})")
    
    # 保存评审结果
    out = os.path.join(ROOT, "reviews", f"kor_review_{tag}.json")
    payload = {
        "tag": tag,
        "dataset": dataset,
        "reviewed_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "thresholds": t,
        "all": rows,
        "candidates": candidates,
        "near": near,
        "prod_stats": {k: len(v) for k, v in prod_stats.items()},
        "discipline_report": discipline_report,
        "switch_decision": switch_decision,
    }
    tmp = out + ".tmp"
    json.dump(payload, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, out)
    print(f"\nreview -> {out}")
    
    # 回写台账
    if write_ledger:
        def mut(d):
            sr = d.setdefault("submit_ready", [])
            for c in candidates:
                if not any((x.get("id") if isinstance(x, dict) else x) == c["id"] for x in sr):
                    sr.append({"id": c["id"], "note": f"review {tag} 全门槛过",
                               "queued_at": datetime.date.today().isoformat()})
            d.setdefault("near_pool", []).append({
                "tag": tag, "at": datetime.date.today().isoformat(),
                "near": [{"id": n["id"], "sharpe": n["sharpe"], "walls": n["walls"],
                          "prod_category": n.get("prod_category")} for n in near]})
            # 更新数据集状态
            if dataset and discipline_report:
                pool = d.setdefault("dataset_pool", {})
                pool[dataset] = {
                    "status": discipline_report["category"].lower(),
                    "last_review": tag,
                    "prod_min": discipline_report["prod_stats"]["min"],
                    "death_score": discipline_report["death_score"],
                    "updated_at": datetime.date.today().isoformat(),
                }
        kor_ledger.update(mut)
        print(f"ledger: submit_ready +{len(candidates)}, near_pool +{len(near)}, dataset_pool[{dataset}] updated")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--multisim")
    ap.add_argument("--alphas", nargs="+")
    ap.add_argument("--tag")
    ap.add_argument("--dataset", help="数据集名称（用于纪律评估）")
    ap.add_argument("--write-ledger", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()

    if a.multisim:
        ids = metrics_cache.MetricsFetcher().multisim_alpha_ids(a.multisim)
        tag = a.tag or a.multisim
    elif a.alphas:
        ids, tag = a.alphas, (a.tag or "manual")
    else:
        ap.error("need --multisim or --alphas")

    rows = metrics_cache.fetch_rows(ids, refresh=a.refresh)
    review_with_discipline(rows, a.dataset, tag, a.write_ledger)


if __name__ == "__main__":
    main()
