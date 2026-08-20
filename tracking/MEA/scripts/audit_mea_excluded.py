# -*- coding: utf-8 -*-
"""audit_mea_excluded.py - MEA 区域被排除数据集回溯审计。

分析历史 ranking 中被硬排除的数据集，评估若下调 coverage 硬地板后的"救援"效果，
生成审计报告供决策参考。

用法:
  python audit_mea_excluded.py                    # 分析当前 ranking
  python audit_mea_excluded.py --simulate 0.45    # 模拟指定硬地板值
  python audit_mea_excluded.py --compare          # 对比多区域阈值效果
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TRACKING_ROOT = os.path.dirname(ROOT)
sys.path.insert(0, TRACKING_ROOT)

from region_thresholds import get_dataset_health_thresholds, get_backfill_band

RANKING_PATH = os.path.join(ROOT, "reference", "mea_dataset_ranking.json")


def load_ranking():
    """加载当前 MEA ranking。"""
    if not os.path.exists(RANKING_PATH):
        raise FileNotFoundError(f"ranking 文件不存在: {RANKING_PATH}")
    with open(RANKING_PATH, encoding="utf-8") as f:
        return json.load(f)


def simulate_threshold(datasets, coverage_hard_min, field_count_hard_min=3):
    """
    模拟指定硬地板值下的排除情况。
    
    Returns:
        dict: 包含 rescued/still_excluded/tier1/tier2 统计
    """
    h = get_dataset_health_thresholds("MEA")
    band = get_backfill_band("MEA")
    
    rescued = []  # 当前被排除，但新阈值下可救回
    still_excluded = []  # 新阈值下仍被排除
    tier1_candidates = []  # 新阈值下可进 tier1
    tier2_candidates = []  # 新阈值下可进 tier2
    
    for ds in datasets:
        cov = ds.get("coverage") or 0
        fc = ds.get("fieldCount") or 0
        ac = ds.get("alphaCount") or 0
        vs = ds.get("valueScore") or 0
        currently_excluded = ds.get("hard_excluded", False)
        
        # 新硬地板判定
        new_hard_excluded = cov < coverage_hard_min or fc < field_count_hard_min
        
        # 保底带判定
        backfill_eligible = False
        if band and new_hard_excluded:
            backfill_eligible = (band["coverage_min"] <= cov < band["coverage_max"]
                                and ac <= band["alpha_count_max"]
                                and vs >= band["value_score_min"])
        
        if currently_excluded and not new_hard_excluded:
            rescued.append(ds)
            # 进一步判定 tier
            if cov >= h["coverage_min"] and ac <= h["alpha_count_max"] and fc >= h["field_count_min"]:
                tier1_candidates.append(ds)
            elif cov >= h["tier2_coverage_min"] and ac <= h["tier2_alpha_count_max"] and fc >= h["tier2_field_count_min"]:
                tier2_candidates.append(ds)
        elif currently_excluded and new_hard_excluded and backfill_eligible:
            rescued.append(ds)
            tier2_candidates.append(ds)  # 保底带进 tier2
        elif new_hard_excluded and not backfill_eligible:
            still_excluded.append(ds)
    
    return {
        "rescued": rescued,
        "still_excluded": still_excluded,
        "tier1_candidates": tier1_candidates,
        "tier2_candidates": tier2_candidates,
        "rescued_count": len(rescued),
        "still_excluded_count": len(still_excluded),
    }


def print_dataset(ds, prefix="  "):
    """格式化打印数据集信息。"""
    print(f"{prefix}{ds['id']:28s} cov={ds.get('coverage', 0):.3f} "
          f"fc={ds.get('fieldCount', 0):4d} ac={ds.get('alphaCount', 0):5d} "
          f"vs={ds.get('valueScore', 0):.0f} score={ds.get('score', 0):.3f} "
          f"cat={ds.get('category', ''):>12}")


def cmd_audit(a):
    """审计主逻辑。"""
    data = load_ranking()
    datasets = data["ranking"]
    
    current_h = get_dataset_health_thresholds("MEA")
    usa_h = get_dataset_health_thresholds("USA")
    
    print("=" * 80)
    print("MEA 区域被排除数据集回溯审计")
    print("=" * 80)
    print(f"\n当前 MEA 硬地板: coverage>={current_h['coverage_hard_min']}, fieldCount>={current_h['field_count_hard_min']}")
    print(f"USA 硬地板(对照): coverage>={usa_h['coverage_hard_min']}, fieldCount>={usa_h['field_count_hard_min']}")
    
    # 当前被排除的数据集
    excluded = [d for d in datasets if d.get("hard_excluded")]
    print(f"\n当前被硬排除: {len(excluded)} / {len(datasets)} 个数据集")
    
    if a.simulate:
        # 模拟指定硬地板
        sim = simulate_threshold(datasets, a.simulate)
        print(f"\n{'=' * 80}")
        print(f"模拟: coverage_hard_min = {a.simulate}")
        print(f"{'=' * 80}")
        print(f"\n可救援: {sim['rescued_count']} 个")
        for ds in sim["rescued"]:
            print_dataset(ds, "  [救援] ")
        print(f"\n仍排除: {sim['still_excluded_count']} 个")
        for ds in sim["still_excluded"][:5]:  # 只显示前5个
            print_dataset(ds, "  [仍排除] ")
        if len(sim["still_excluded"]) > 5:
            print(f"  ... 还有 {len(sim['still_excluded']) - 5} 个")
        print(f"\n其中可进 tier1: {len(sim['tier1_candidates'])} 个")
        print(f"其中可进 tier2: {len(sim['tier2_candidates'])} 个")
    
    if a.compare:
        # 对比多区域阈值
        print(f"\n{'=' * 80}")
        print("多区域阈值对比")
        print(f"{'=' * 80}")
        
        thresholds_to_test = [
            ("USA", usa_h["coverage_hard_min"]),
            ("KOR", 0.60),
            ("MEA(建议)", 0.45),
            ("MEA(保守)", 0.50),
            ("MEA(激进)", 0.40),
        ]
        
        print(f"\n{'方案':>12} {'硬地板':>8} {'排除数':>8} {'救援数':>8} {'救援率':>8}")
        print("-" * 50)
        
        current_excluded = len([d for d in datasets if (d.get("coverage") or 0) < current_h["coverage_hard_min"]])
        
        for name, thr in thresholds_to_test:
            sim = simulate_threshold(datasets, thr)
            excluded_count = len([d for d in datasets if (d.get("coverage") or 0) < thr])
            rescued = current_excluded - excluded_count
            rescue_rate = rescued / current_excluded * 100 if current_excluded > 0 else 0
            print(f"{name:>12} {thr:>8.2f} {excluded_count:>8} {rescued:>8} {rescue_rate:>7.1f}%")
    
    # 默认输出：详细分析当前被排除的数据集
    if not a.simulate and not a.compare:
        print(f"\n{'=' * 80}")
        print("被排除数据集详细分析")
        print(f"{'=' * 80}")
        
        # 按 coverage 分层
        high_cov = [d for d in excluded if (d.get("coverage") or 0) >= 0.5]
        mid_cov = [d for d in excluded if 0.4 <= (d.get("coverage") or 0) < 0.5]
        low_cov = [d for d in excluded if (d.get("coverage") or 0) < 0.4]
        
        print(f"\n[0.5 <= cov < 0.7] 高覆盖被排除 ({len(high_cov)} 个) — 最可惜")
        for ds in sorted(high_cov, key=lambda x: -x.get("score", 0)):
            print_dataset(ds, "  ")
        
        print(f"\n[0.4 <= cov < 0.5] 中覆盖被排除 ({len(mid_cov)} 个) — 保底带可救")
        for ds in sorted(mid_cov, key=lambda x: -x.get("score", 0)):
            print_dataset(ds, "  ")
        
        print(f"\n[cov < 0.4] 低覆盖被排除 ({len(low_cov)} 个) — 确实稀疏")
        for ds in sorted(low_cov, key=lambda x: -x.get("score", 0))[:5]:
            print_dataset(ds, "  ")
        if len(low_cov) > 5:
            print(f"  ... 还有 {len(low_cov) - 5} 个")
        
        # 高价值被排除（score > 0.4）
        high_score_excluded = [d for d in excluded if d.get("score", 0) > 0.4]
        print(f"\n{'=' * 80}")
        print(f"高价值被排除（score > 0.4）: {len(high_score_excluded)} 个")
        print(f"{'=' * 80}")
        for ds in sorted(high_score_excluded, key=lambda x: -x.get("score", 0)):
            print_dataset(ds, "  ")
            # 标记若用 MEA 建议阈值是否可救
            cov = ds.get("coverage") or 0
            if cov >= 0.45:
                print(f"    -> 若 coverage_hard_min=0.45 可救援")
            elif cov >= 0.40:
                print(f"    -> 若 coverage_hard_min=0.40 可救援（保底带）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--simulate", type=float, metavar="THRESHOLD",
                    help="模拟指定 coverage 硬地板值")
    ap.add_argument("--compare", action="store_true",
                    help="对比多区域阈值效果")
    a = ap.parse_args()
    cmd_audit(a)


if __name__ == "__main__":
    main()
