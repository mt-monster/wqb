# -*- coding: utf-8 -*-
"""review_wave.py - 通用指标评审与达标筛选（M15/M16）。

取代 review_wave1/3/5.py（硬编 .qoder-cn 会话 cache、阈值散落、逐波复制）：
  - 指标走 metrics_cache 读穿缓存（可复现、可迁移、省配额）
  - 门槛集中 config/thresholds.json
  - near 池自动诊断卡在哪堵墙（CW/2Y/SHARPE/FITNESS/TVR/MARGIN/RA）
  - --write-ledger 自动回写台账 submit_ready / near_pool

用法:
  python review_wave.py --multisim <id> [--tag wave36A] [--write-ledger]
  python review_wave.py --alphas KPGZmLMl xxx [--tag manual] [--write-ledger]
"""
import argparse, datetime, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import kor_ledger
import metrics_cache

THRESH = json.load(open(os.path.join(ROOT, "config", "thresholds.json"), encoding="utf-8"))


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
        w.append("2Y_UNKNOWN")  # 平台未返回 LOW_2Y_SHARPE（如 KPGZmLMl），不能算 2Y 败
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--multisim")
    ap.add_argument("--alphas", nargs="+")
    ap.add_argument("--tag")
    ap.add_argument("--write-ledger", action="store_true")
    ap.add_argument("--refresh", action="store_true", help="绕过缓存强制回源")
    a = ap.parse_args()

    if a.multisim:
        ids = metrics_cache.MetricsFetcher().multisim_alpha_ids(a.multisim)
        tag = a.tag or a.multisim
    elif a.alphas:
        ids, tag = a.alphas, (a.tag or "manual")
    else:
        ap.error("need --multisim or --alphas")

    t = THRESH["review"]
    rows = metrics_cache.fetch_rows(ids, refresh=a.refresh)
    candidates = [r for r in rows if passes(r, t)]
    near = []
    for r in rows:
        if r in candidates or r.get("sharpe") is None:
            continue
        if r["sharpe"] > THRESH["near"]["sharpe_min"]:
            rr = dict(r)
            rr["walls"] = walls(r, t)
            near.append(rr)

    print(f"{'id':10s} {'sh':>6} {'fit':>5} {'2y':>5} {'mg_bp':>7} {'tvr%':>6} {'rn':>5} walls")
    for r in rows:
        w = [] if r in candidates else walls(r, t)
        print(f"{r['id']:10s} {r.get('sharpe') or 0:6.2f} {r.get('fitness') or 0:5.2f} "
              f"{r.get('two_year_sharpe') or 0:5.2f} {r.get('margin_bp') or 0:7.2f} "
              f"{r.get('turnover_pct') or 0:6.2f} {r.get('rn_sharpe') or 0:5.2f} {','.join(w) or 'PASS'}")

    out = os.path.join(ROOT, "reviews", f"kor_review_{tag}.json")
    payload = {"tag": tag, "reviewed_at": datetime.datetime.now().isoformat(timespec="seconds"),
               "thresholds": t, "all": rows, "candidates": candidates, "near": near}
    tmp = out + ".tmp"
    json.dump(payload, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, out)
    print(f"\ntotal={len(rows)} candidates={len(candidates)} near={len(near)}")
    print(f"review -> {out}")

    if a.write_ledger:
        def mut(d):
            sr = d.setdefault("submit_ready", [])
            for c in candidates:
                if not any((x.get("id") if isinstance(x, dict) else x) == c["id"] for x in sr):
                    sr.append({"id": c["id"], "note": f"review {tag} 全门槛过",
                               "queued_at": datetime.date.today().isoformat()})
            d.setdefault("near_pool", []).append({
                "tag": tag, "at": datetime.date.today().isoformat(),
                "near": [{"id": n["id"], "sharpe": n["sharpe"], "walls": n["walls"]} for n in near]})
        kor_ledger.update(mut)
        print(f"ledger: submit_ready +{len(candidates)}, near_pool +{len(near)}")


if __name__ == "__main__":
    main()
