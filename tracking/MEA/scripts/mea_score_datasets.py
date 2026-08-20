# -*- coding: utf-8 -*-
"""mea_score_datasets.py - MEA 区域数据集自动评分（区域差异化阈值版）。

基于 KOR score_datasets.py 重构，使用 region_thresholds.py 加载 MEA 专属阈值，
解决 0.7 coverage 硬地板对新兴市场数据集的结构性误杀问题。

关键差异（vs KOR 版）:
  - coverage_hard_min: 0.45 (vs 0.70)
  - coverage_min: 0.60 (vs 0.85)
  - field_count_hard_min: 3 (vs 5)
  - 支持保底带（backfill_band）：低覆盖高价值数据集可进 tier2

用法:
  python mea_score_datasets.py              # 全量评分
  python mea_score_datasets.py --audit      # 审计模式：标记被误杀的数据集
"""
import argparse
import datetime
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TRACKING_ROOT = os.path.dirname(ROOT)
sys.path.insert(0, TRACKING_ROOT)

from region_thresholds import (
    get_dataset_health_thresholds,
    get_backfill_band,
    is_backfill_eligible,
)

SETTINGS = json.load(open(os.path.join(ROOT, "config", "settings.json"), encoding="utf-8"))
REGION = SETTINGS["region"]  # "MEA"
PAGE = 50


def fetch_all_datasets(api):
    """分页拉取全部数据集。"""
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
    """数据集评分公式（与 KOR 版一致）。"""
    cov = ds.get("coverage") or 0
    ac = ds.get("alphaCount") or 0
    fc = ds.get("fieldCount") or 0
    vs = ds.get("valueScore")
    return (0.40 * cov
            + 0.30 * (1.0 / (1.0 + math.log10(1 + ac)))
            + 0.20 * (math.log1p(fc) / math.log1p(1000))
            + 0.10 * (min(vs, 10) / 10.0 if vs is not None else 0.3))


def tier_with_region_thresholds(ds, region=REGION):
    """
    使用区域差异化阈值判定 tier。
    
    Returns:
        tuple: (tier, tier_note, hard_excluded)
            tier: "tier1" / "tier2" / "excluded"
            tier_note: 判定说明（如 "backfill_band"）
            hard_excluded: 是否被硬地板排除
    """
    h = get_dataset_health_thresholds(region)
    cov = ds.get("coverage") or 0
    ac = ds.get("alphaCount") or 0
    fc = ds.get("fieldCount") or 0
    vs = ds.get("valueScore") or 0
    
    # 硬地板检查
    hard_excluded = cov < h["coverage_hard_min"] or fc < h["field_count_hard_min"]
    
    if hard_excluded:
        # 检查保底带（仅 MEA 等有配置的区域）
        if is_backfill_eligible(ds, region):
            return "tier2", "backfill_band", False
        return "excluded", "hard_floor", True
    
    # tier1: 高覆盖 + 低竞争 + 多字段
    if cov >= h["coverage_min"] and ac <= h["alpha_count_max"] and fc >= h["field_count_min"]:
        return "tier1", "standard", False
    
    # tier2: 中等覆盖 + 可接受竞争 + 最少字段
    if cov >= h["tier2_coverage_min"] and ac <= h["tier2_alpha_count_max"] and fc >= h["tier2_field_count_min"]:
        return "tier2", "standard", False
    
    return "excluded", "below_tier2", False


def cmd_score(a):
    """全量评分主逻辑。"""
    # 延迟导入，避免无 API 环境报错
    from kor_fetch_metrics import Api, load_creds
    import scan_fields
    
    e, pw = load_creds()
    api = Api()
    api.login(e, pw)
    dss = fetch_all_datasets(api)
    
    # 加载台账（若存在）
    ledger_path = os.path.join(ROOT, "reference", "mea_ledger.json")
    dead = set()
    if os.path.exists(ledger_path):
        ledger = json.load(open(ledger_path, encoding="utf-8"))
        dead = {k[:-5] for k in ledger if k.endswith("_dead")}
    
    rows = []
    audit_rows = []  # 审计模式：记录被误杀的数据集
    
    for ds in dss:
        did = ds.get("id")
        tier, tier_note, hard_excluded = tier_with_region_thresholds(ds)
        
        row = {
            "id": did,
            "score": round(score(ds), 4),
            "tier": tier,
            "tier_note": tier_note,
            "coverage": ds.get("coverage"),
            "fieldCount": ds.get("fieldCount"),
            "usableFieldCount": ds.get("fieldCount"),  # MEA 暂用 raw
            "fieldCount_src": "raw",
            "alphaCount": ds.get("alphaCount"),
            "userCount": ds.get("userCount"),
            "valueScore": ds.get("valueScore"),
            "pyramidMultiplier": (ds.get("pyramidMultiplier") or {}).get("multiplier")
                if isinstance(ds.get("pyramidMultiplier"), dict) else ds.get("pyramidMultiplier"),
            "category": (ds.get("category") or {}).get("id") if isinstance(ds.get("category"), dict) else ds.get("category"),
            "dead": did in dead,
            "hard_excluded": hard_excluded,
        }
        rows.append(row)
        
        # 审计模式：记录被硬地板排除但高价值的数据集
        if a.audit and hard_excluded and row["score"] > 0.35:
            audit_rows.append(row)
    
    rows.sort(key=lambda r: -r["score"])
    alive = [r for r in rows if not r["dead"] and r["tier"] != "excluded"]
    
    # 输出 ranking
    h = get_dataset_health_thresholds(REGION)
    out = os.path.join(ROOT, "reference", "mea_dataset_ranking.json")
    
    # 构建 tier_rule 说明
    tier_rule = (
        f"tier1: cov>={h['coverage_min']} & alphaCount<={h['alpha_count_max']} & fieldCount>={h['field_count_min']}; "
        f"tier2: cov>={h['tier2_coverage_min']} & alphaCount<={h['tier2_alpha_count_max']} & fieldCount>={h['tier2_field_count_min']}; "
        f"硬地板: cov>={h['coverage_hard_min']} & fieldCount>={h['field_count_hard_min']}"
    )
    band = get_backfill_band(REGION)
    if band:
        tier_rule += f"; 保底带: {band['coverage_min']}<=cov<{band['coverage_max']} & alphaCount<={band['alpha_count_max']} & valueScore>={band['value_score_min']}→tier2[需ts_backfill]"
    
    scan_fields.atomic_write(out, {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "region": REGION,
        "universe": SETTINGS["universe"],
        "total": len(rows),
        "dead_excluded": len(dead),
        "mode": "general",
        "tier_method": "region_thresholds",
        "score_formula": "0.4*cov + 0.3/(1+log10(1+alphaCount)) + 0.2*log1p(fieldCount)/log1p(1000) + 0.1*valueScore/10",
        "tier_rule": tier_rule,
        "ranking": rows,
    })
    
    print(f"region={REGION} datasets={len(rows)} alive_ranked={len(alive)} dead_skipped={len(dead)}")
    print(f"{'rank':>4} {'score':>7} {'tier':>6} {'note':>14}  {'id':28s} cov/fields/alphas")
    for i, r in enumerate(alive[:20], 1):
        print(f"{i:>4} {r['score']:>7} {r['tier']:>6} {r['tier_note']:>14}  {r['id']:28s} "
              f"{r['coverage']:.3f}/{r['fieldCount']}/{r['alphaCount']}")
    print(f"ranking -> {out}")
    
    # 审计模式输出
    if a.audit:
        print(f"\n=== 审计：被硬地板排除但高分的数据集（score>0.35）===")
        print(f"{'score':>7} {'cov':>6} {'fc':>4} {'ac':>5} {'vs':>3}  {'id':28s} {'category':>12}")
        for r in audit_rows:
            print(f"{r['score']:>7} {r['coverage']:>6.3f} {r['fieldCount']:>4} {r['alphaCount']:>5} "
                  f"{r['valueScore']:>3.0f}  {r['id']:28s} {r.get('category', ''):>12}")
        
        # 对比：若用 USA 阈值会排除多少
        usa_h = get_dataset_health_thresholds("USA")
        usa_excluded = [r for r in rows if (r["coverage"] or 0) < usa_h["coverage_hard_min"]]
        mea_excluded = [r for r in rows if r["hard_excluded"]]
        print(f"\n=== 阈值对比 ===")
        print(f"USA 硬地板(cov>={usa_h['coverage_hard_min']}): 排除 {len(usa_excluded)} 个")
        print(f"MEA 硬地板(cov>={h['coverage_hard_min']}): 排除 {len(mea_excluded)} 个")
        print(f"少排除 {len(usa_excluded) - len(mea_excluded)} 个（新兴市场宽容度）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true", help="审计模式：标记被误杀的数据集")
    a = ap.parse_args()
    cmd_score(a)


if __name__ == "__main__":
    main()
