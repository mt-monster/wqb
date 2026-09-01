# -*- coding: utf-8 -*-
"""score_datasets.py - 数据集自动评分 + 探针电池接线（M1+M2）。

取代 record_whitelist_v2.py 的手写 tier 清单；并把 reference/kor_dataset_probe_battery.json
从"参考文档"接线为可执行的低成本预筛闭环（不烧正式 wave 配额）。

三种模式:
  1) 评分（默认）:
     python score_datasets.py
       直连 get_datasets 全量评分（自动排除台账 *_dead），写 reference/kor_dataset_ranking.json
  2) 探针计划（生成不提交）:
     python score_datasets.py --probe-plan behavioral_signals [--fields 6]
       读 typed catalog（缺则自动 scan_fields），按 8 探针模板生成批次，落 candidates/probe_<ds>_exprs.json
  3) 探针评分（评审回测结果）:
     python score_datasets.py --probe-score <multisim_id> [--dataset <ds>] [--mark-dead]
       按三灯公式判定 绿灯/黄灯/红灯，红灯可一键记 *_dead 台账
"""
import argparse, datetime, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from kor_fetch_metrics import Api, load_creds
import kor_ledger
import metrics_cache
import scan_fields

SETTINGS = json.load(open(os.path.join(ROOT, "config", "settings.json"), encoding="utf-8"))
THRESH = json.load(open(os.path.join(ROOT, "config", "thresholds.json"), encoding="utf-8"))
PAGE = 50

# ---------------- M1: 数据集自动评分 ----------------

def fetch_all_datasets(api):
    base = ("/data-sets?instrumentType={instrumentType}&region={region}"
            "&delay={delay}&universe={universe}&limit={pg}").format(pg=PAGE, **SETTINGS)
    out, offset = [], 0
    while True:
        j = json.load(api.get(f"{base}&offset={offset}"))
        rs = j.get("results", [])
        out.extend(rs)
        offset += len(rs)
        if not rs or offset >= j.get("count", 0):
            return out


def score(ds):
    cov = ds.get("coverage") or 0
    ac = ds.get("alphaCount") or 0
    fc = ds.get("fieldCount") or 0
    vs = ds.get("valueScore")
    return (0.40 * cov
            + 0.30 * (1.0 / (1.0 + math.log10(1 + ac)))
            + 0.20 * (math.log1p(fc) / math.log1p(1000))
            + 0.10 * (min(vs, 10) / 10.0 if vs is not None else 0.3))


def tier(ds):
    h = THRESH["dataset_health"]
    cov, ac, fc = ds.get("coverage") or 0, ds.get("alphaCount") or 0, ds.get("fieldCount") or 0
    if cov >= h["coverage_min"] and ac <= h["alpha_count_max"] and fc >= h["field_count_min"]:
        return "tier1"
    if cov >= h["coverage_min"] and ac <= 200 and fc >= 5:
        return "tier2"
    return "excluded"


def cmd_score():
    e, pw = load_creds()
    api = Api(); api.login(e, pw)
    dss = fetch_all_datasets(api)
    ledger = kor_ledger.load()
    dead = {k[:-5] for k in ledger if k.endswith("_dead")}
    rows = []
    for ds in dss:
        did = ds.get("id")
        rows.append({
            "id": did, "score": round(score(ds), 4), "tier": tier(ds),
            "coverage": ds.get("coverage"), "fieldCount": ds.get("fieldCount"),
            "alphaCount": ds.get("alphaCount"), "userCount": ds.get("userCount"),
            "valueScore": ds.get("valueScore"),
            "pyramidMultiplier": (ds.get("pyramidMultiplier") or {}).get("multiplier")
                if isinstance(ds.get("pyramidMultiplier"), dict) else ds.get("pyramidMultiplier"),
            "category": (ds.get("category") or {}).get("id") if isinstance(ds.get("category"), dict) else ds.get("category"),
            "dead": did in dead,
        })
    rows.sort(key=lambda r: -r["score"])
    alive = [r for r in rows if not r["dead"] and r["tier"] != "excluded"]
    out = os.path.join(ROOT, "reference", "kor_dataset_ranking.json")
    scan_fields.atomic_write(out, {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "region": SETTINGS["region"], "universe": SETTINGS["universe"],
        "total": len(rows), "dead_excluded": len(dead),
        "score_formula": "0.4*cov + 0.3/(1+log10(1+alphaCount)) + 0.2*log1p(fieldCount)/log1p(1000) + 0.1*valueScore/10",
        "tier_rule": f"tier1: cov>={THRESH['dataset_health']['coverage_min']} & alphaCount<={THRESH['dataset_health']['alpha_count_max']} & fieldCount>={THRESH['dataset_health']['field_count_min']}; tier2: cov>=0.85 & alphaCount<=200 & fieldCount>=5",
        "ranking": rows,
    })
    print(f"datasets={len(rows)} alive_ranked={len(alive)} dead_skipped={len(dead)}")
    print(f"{'rank':>4} {'score':>7} {'tier':>5}  {'id':28s} cov/fields/alphas")
    for i, r in enumerate(alive[:20], 1):
        print(f"{i:>4} {r['score']:>7} {r['tier']:>5}  {r['id']:28s} "
              f"{r['coverage']}/{r['fieldCount']}/{r['alphaCount']}")
    print(f"ranking -> {out}")


# ---------------- M2: 探针电池接线 ----------------

FAMILY_KW = {
    "change": ["change", "delta", "revision", "chg", "momentum", "diff", "surprise"],
    "level": ["level", "value", "score", "rank", "pct", "ratio", "yield", "price"],
    "quality": ["quality", "confidence", "std", "vol", "sigma", "skew"],
}


def pick_fields(cat, n):
    """按 变化/水平/质量 三族各选代表（coverage 优先，零竞争优先）。"""
    def fam(f):
        txt = (f["id"] + " " + (f.get("description") or "")).lower()
        for name, kws in FAMILY_KW.items():
            if any(k in txt for k in kws):
                return name
        return "level"
    buckets = {"change": [], "level": [], "quality": []}
    for f in sorted(cat["fields"], key=lambda x: (-(x.get("coverage") or 0),
                                                  (x.get("userCount") or 0))):
        buckets[fam(f)].append(f)
    per = max(1, n // 3)
    picked = buckets["change"][:per] + buckets["level"][:per] + buckets["quality"][:per]
    rest = [f for b in buckets.values() for f in b if f not in picked]
    return (picked + rest)[:n]


STAGE_A_PROBES = {"P1_水平正", "P2_水平镜像", "P4_均值差分", "P5_衰减水平"}  # 信息量/成本比最高（model219 P4 实证 0.3→1.08）


def render_probes(cat, fields):
    battery = json.load(open(os.path.join(ROOT, "reference", "kor_dataset_probe_battery.json"),
                             encoding="utf-8"))["probe_battery"]
    is_vector = cat.get("data_type") == "VECTOR"
    stage_a, stage_b = [], []
    for f in fields:
        fid = f["id"]
        F = f"vec_avg({fid})" if is_vector else fid  # VECTOR 先聚合（含 P8 ts_backfill）
        for p in battery:
            item = {"probe": p["probe"], "field": fid, "expr": p["expr"].replace("F", F)}
            (stage_a if p["probe"] in STAGE_A_PROBES else stage_b).append(item)
    return stage_a, stage_b


def cmd_probe_plan(a):
    cat_path = os.path.join(ROOT, "reference", f"kor_{a.probe_plan}_fields.json")
    if not os.path.exists(cat_path):
        print(f"catalog 缺失，先跑 scan_fields --dataset {a.probe_plan}", file=sys.stderr)
        e, pw = load_creds()
        api = Api(); api.login(e, pw)
        raw = scan_fields.fetch_fields(api, a.probe_plan)
        scan_fields.atomic_write(cat_path, scan_fields.build_catalog(a.probe_plan, raw))
    cat = json.load(open(cat_path, encoding="utf-8"))
    fields = pick_fields(cat, a.fields)
    stage_a, stage_b = render_probes(cat, fields)
    bs = SETTINGS["_multi_sim_batch_size"]

    def batches_of(lst):
        return [[x["expr"] for x in lst[i:i + bs]] for i in range(0, len(lst), bs)]

    all_exprs = stage_a + stage_b
    out = os.path.join(ROOT, "candidates", f"probe_{a.probe_plan}_exprs.json")
    scan_fields.atomic_write(out, {
        "dataset": a.probe_plan, "data_type": cat.get("data_type"),
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "settings": SETTINGS, "fields": [f["id"] for f in fields],
        "stageA": {"probes": sorted(STAGE_A_PROBES), "batches": batches_of(stage_a),
                   "early_stop_rule": f"Stage A 完成即 --probe-score --stage A 评分：max|sh|<{THRESH['probe_scoring_v2']['early_red_sh']} 且无镜像 -> EARLY RED，不跑 Stage B（省 {len(batches_of(stage_b))} 批）"},
        "stageB": {"probes": sorted(set(p['probe'] for p in stage_b)), "batches": batches_of(stage_b)},
        "expressions": [x["expr"] for x in all_exprs],
        "batches": batches_of(all_exprs),
        "note": "两段式探针：先提 Stage A 批，评分非 EARLY RED 再提 Stage B；multisim id 交给 --probe-score",
    })
    print(f"dataset={a.probe_plan} data_type={cat.get('data_type')} fields={len(fields)} "
          f"stageA={len(stage_a)}式/{len(batches_of(stage_a))}批 "
          f"stageB={len(stage_b)}式/{len(batches_of(stage_b))}批")
    print(f"probe plan(v2 两段式) -> {out}")


# ---------------- 三灯 v2 ----------------

def score_v1(rows):
    """原公式（保留对照；修复 2y None 误判）。"""
    valid = [r for r in rows if r.get("sharpe") is not None]
    max_sh = max((abs(r["sharpe"]) for r in valid), default=0)
    mirror = any(r["sharpe"] < -0.5 for r in valid)
    margin_ok = any((r.get("margin_bp") or 0) > 5 for r in valid)
    tvr_ok = any(5 <= (r.get("turnover_pct") or 0) <= 30 for r in valid)
    potential = max_sh * 2 + (0.5 if mirror else 0) + (0.3 if margin_ok else 0) + (0.2 if tvr_ok else 0)
    g, y = THRESH["probe_scoring"]["green_min"], THRESH["probe_scoring"]["yellow_min"]
    return potential, ("GREEN" if potential >= g else ("YELLOW" if potential >= y else "RED"))


def score_v2(rows, stage="all"):
    """联合评估 + 广度 + CW 罚分 + tvr 结构性墙 + Stage A 早停。返回结构化判定。"""
    cfg = THRESH["probe_scoring_v2"]
    valid = [r for r in rows if r.get("sharpe") is not None]
    if not valid:
        return {"light": "RED", "potential": 0, "action": "无有效指标，判死", "components": {}}
    best = max(valid, key=lambda r: abs(r["sharpe"]))
    abs_sh = abs(best["sharpe"])
    mirror = any(r["sharpe"] < -0.5 for r in valid)
    breadth = sum(1 for r in valid if abs(r["sharpe"]) >= cfg["breadth_bar"])
    mg, tv, rn, fit = best.get("margin_bp"), best.get("turnover_pct"), best.get("rn_sharpe"), best.get("fitness")
    cw_fail = any("CONCENTRATED" in c for c in best.get("failed_checks") or [])
    comps = {
        "sharpe": round(cfg["w_sharpe"] * abs_sh, 3),
        "fitness": round(cfg["w_fitness"] * (fit or 0), 3),
        "mirror": cfg["w_mirror"] if mirror else 0,
        "margin": cfg["w_margin"] if (mg is not None and mg > 5) else 0,
        "tvr": cfg["w_tvr"] if (tv is not None and cfg["tvr_low"] <= tv <= cfg["tvr_high"]) else 0,
        "rn": cfg["w_rn"] if (rn is not None and rn >= cfg["rn_bar"]) else 0,
        "breadth": round(cfg["w_breadth"] * min(breadth, 4) / 4, 3),
        "cw_penalty": -cfg["cw_penalty"] if cw_fail else 0,
    }
    potential = round(sum(comps.values()), 3)
    light = "GREEN" if potential >= cfg["green_min"] else ("YELLOW" if potential >= cfg["yellow_min"] else "RED")

    # Stage A 早停
    if stage == "A" and abs_sh < cfg["early_red_sh"] and not mirror:
        return {"light": "EARLY_RED", "potential": potential, "best": best["id"],
                "action": f"Stage A 无信号(max|sh|={abs_sh:.2f}<{cfg['early_red_sh']}且无镜像)，不跑 Stage B，判死",
                "components": comps}

    # 2Y 红灯（仅当平台返回值；None 不判——v1 把 None 当 0 会误判）
    two_y = best.get("two_year_sharpe")
    red_2y = (two_y is not None and abs_sh >= cfg["red_2y_sh_abs_min"] and two_y < cfg["red_2y_max"])

    # tvr 结构性墙：全部探针同侧出界
    tvrs = [r["turnover_pct"] for r in valid if r.get("turnover_pct") is not None]
    tvr_struct = None
    if tvrs and all(t < cfg["tvr_low"] for t in tvrs):
        tvr_struct = "LOW"
    elif tvrs and all(t > cfg["tvr_high"] for t in tvrs):
        tvr_struct = "HIGH"

    if red_2y:
        light, action = "RED", f"2Y红灯：最强式2y={two_y:.2f}<{cfg['red_2y_max']}（近2年衰减），判死不深挖"
    elif tvr_struct and light == "GREEN":
        light = "YELLOW"
        action = ("结构性低tvr（全族<5%，multi_source_model 教训）：先 trade_when/decay 拉 tvr 再评，限2批"
                  if tvr_struct == "LOW" else
                  "结构性高tvr（全族>30%，news_sentiment_transfer 教训）：拉长窗口/加大 decay 压 tvr，限2批")
    elif light == "GREEN" and cw_fail:
        action = "绿灯(带CW修复)：深挖，骨架直接上跨Category rank加法（CW手册类型三）"
    elif light == "GREEN":
        action = "绿灯：深度挖掘（骨架融合/FE假设族/参数精磨）"
    elif light == "YELLOW":
        action = "黄灯：只做镜像腿与两两融合，限2批"
    else:
        action = "红灯：判死入台账，不回头" + ("（镜像偏强，可选留1批镜像验证）" if mirror else "")
    return {"light": light, "potential": potential, "best": best["id"],
            "best_metrics": {"sharpe": best["sharpe"], "fitness": fit, "2y": two_y,
                             "margin_bp": mg, "tvr_pct": tv, "rn": rn, "cw_fail": cw_fail},
            "breadth": breadth, "tvr_struct": tvr_struct, "red_2y": red_2y,
            "action": action, "components": comps}


def cmd_probe_score(a):
    if a.from_json:
        rows = [json.loads(l) for l in open(a.from_json, encoding="utf-8") if l.strip()]
    else:
        f = metrics_cache.MetricsFetcher()  # 单登录复用
        ids = f.multisim_alpha_ids(a.probe_score)
        rows = [f.fetch(aid) for aid in ids]
        rows.sort(key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99))
    v2 = score_v2(rows, stage=a.stage)
    v1p, v1l = score_v1(rows)
    src = a.from_json or a.probe_score
    print(f"src={src} stage={a.stage}")
    print(f"[v2] {v2['light']}  potential={v2['potential']}  (v1 对照: {v1l} {v1p:.2f})")
    print(f"  components: {json.dumps(v2['components'], ensure_ascii=False)}")
    if v2.get("best_metrics"):
        print(f"  best={v2['best']} {json.dumps(v2['best_metrics'], ensure_ascii=False)} "
              f"breadth={v2['breadth']} tvr_struct={v2['tvr_struct']}")
    print(f"  action: {v2['action']}")
    if v2["light"] in ("RED", "EARLY_RED") and a.mark_dead and a.dataset:
        kor_ledger.update(lambda d: d.__setitem__(f"{a.dataset}_dead", {
            "dataset": a.dataset,
            "reason": f"探针三灯v2判死 potential={v2['potential']} light={v2['light']}",
            "dead_at": datetime.date.today().isoformat()}))
        print(f"ledger: {a.dataset}_dead written")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe-plan", metavar="DATASET")
    ap.add_argument("--probe-score", metavar="MULTISIM_ID")
    ap.add_argument("--from-json", metavar="FILE", help="从本地 JSON lines 指标文件评分（离线/校准用）")
    ap.add_argument("--stage", choices=["A", "B", "all"], default="all",
                    help="Stage A 评分启用早停判定")
    ap.add_argument("--dataset", help="--probe-score 时指定数据集（用于 --mark-dead）")
    ap.add_argument("--fields", type=int, default=6)
    ap.add_argument("--mark-dead", action="store_true")
    a = ap.parse_args()
    if a.probe_plan:
        cmd_probe_plan(a)
    elif a.probe_score or a.from_json:
        cmd_probe_score(a)
    else:
        cmd_score()


if __name__ == "__main__":
    main()
