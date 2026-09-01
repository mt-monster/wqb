# -*- coding: utf-8 -*-
"""wave_planner.py - 波次规划器：基于判死证据链自动规划下一波次。

落实"有纪律地切换"原则：
  1. 检查当前数据集是否满足判死条件
  2. 满足判死条件时自动推荐下一数据集
  3. 不满足判死条件时生成深耕策略（设置空间/结构变体/救援武器）
  4. 与 build_wave.py 集成，自动生成下一波次候选

用法:
  python wave_planner.py next --current-dataset chart_cnn_alpha [--wave 17A]
  python wave_planner.py status --dataset chart_cnn_alpha
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from campaign_discipline import assess_dataset, decide_switch, RESCUE_WEAPONS, PROD_DEEP_MIN, PROD_SUSPEND_MIN


def load_dataset_pool():
    """加载数据集候选池。"""
    path = os.path.join(ROOT, "kor_d1_campaign_state.json")
    if os.path.exists(path):
        state = json.load(open(path, encoding="utf-8"))
        return state.get("dataset_pool", {})
    return {}


def get_unexplored_datasets():
    """获取未探索的数据集列表（从字段扫描结果）。"""
    # 这里可以扩展为从字段扫描结果中读取
    # 目前返回硬编码的候选列表
    return [
        {"dataset": "other455", "priority": 1, "reason": "1500字段未侦察"},
        {"dataset": "insider_feats", "priority": 2, "reason": "PROD 0.78 地板，最接近 0.7"},
        {"dataset": "ai_equity_alpha", "priority": 3, "reason": "二轮翻转/聚合变体"},
        {"dataset": "news79", "priority": 4, "reason": "新闻情绪数据集"},
        {"dataset": "analyst39", "priority": 5, "reason": "分析师数据集"},
        {"dataset": "fundamental21", "priority": 6, "reason": "基本面数据集"},
    ]


def generate_deepen_strategy(dataset, evidence):
    """生成深耕策略（当不满足判死条件时）。"""
    strategies = []
    
    # 设置空间未穷尽
    if not evidence["death_criteria"]["settings_exhausted"]:
        tried = set(evidence["settings_tried"])
        all_settings = {"SECTOR d4 t0.08", "SECTOR d6 t0.06", "SECTOR d8 t0.06", 
                       "SUBINDUSTRY d4 t0.08", "SUBINDUSTRY d6 t0.06",
                       "STATISTICAL d4 t0.08", "STATISTICAL d6 t0.06",
                       "INDUSTRY d4 t0.08", "MARKET d4 t0.08"}
        remaining = all_settings - tried
        if remaining:
            strategies.append({
                "type": "settings_space",
                "priority": 1,
                "description": f"设置空间未穷尽，剩余 {len(remaining)} 种组合",
                "candidates": sorted(remaining)[:4],
            })
    
    # 结构变体未穷尽
    if not evidence["death_criteria"]["structures_exhausted"]:
        tried = set(evidence["structures_tried"])
        all_structures = {"rank", "group_rank", "quantile", "signed_power", 
                         "subtract", "linear_mix", "event_gated", "ratio"}
        remaining = all_structures - tried
        if remaining:
            strategies.append({
                "type": "structure_variant",
                "priority": 2,
                "description": f"结构变体未穷尽，剩余 {len(remaining)} 种",
                "candidates": sorted(remaining),
            })
    
    # 救援武器未实测
    if evidence["rescue_weapons_remaining"]:
        strategies.append({
            "type": "rescue_weapon",
            "priority": 3,
            "description": f"救援武器未实测 {len(evidence['rescue_weapons_remaining'])} 种",
            "candidates": evidence["rescue_weapons_remaining"][:3],
        })
    
    return strategies


def plan_next_wave(current_dataset, wave_tag=None):
    """规划下一波次。"""
    # 评估当前数据集
    evidence = assess_dataset(current_dataset)
    if not evidence:
        print(f"[plan] 数据集 {current_dataset} 无历史数据，建议直接开始探针")
        return {
            "action": "probe",
            "dataset": current_dataset,
            "reason": "无历史数据，开始探针阶段",
        }
    
    # 检查是否满足判死条件
    if evidence["category"] == "DEAD" and evidence["death_score"] >= 3:
        # 判死，推荐切换
        decision = decide_switch(current_dataset)
        unexplored = get_unexplored_datasets()
        
        # 过滤掉已判死的数据集
        pool = load_dataset_pool()
        available = [u for u in unexplored 
                    if u["dataset"] not in pool or pool[u["dataset"]].get("status") != "dead"]
        
        if available:
            next_ds = available[0]
            return {
                "action": "switch",
                "from_dataset": current_dataset,
                "to_dataset": next_ds["dataset"],
                "reason": f"{current_dataset} 满足判死条件（PROD {evidence['prod_stats']['min']:.3f} > {PROD_SUSPEND_MIN}，"
                         f"death_score={evidence['death_score']}/4），切换至 {next_ds['dataset']}",
                "switch_reason": next_ds["reason"],
                "death_evidence": evidence,
            }
        else:
            return {
                "action": "halt",
                "dataset": current_dataset,
                "reason": "所有候选数据集已穷尽，战役结束",
            }
    
    elif evidence["category"] == "SUSPEND":
        # 暂挂，保留候选池
        return {
            "action": "suspend",
            "dataset": current_dataset,
            "reason": f"PROD {evidence['prod_stats']['min']:.3f} 在 {PROD_DEEP_MIN}-{PROD_SUSPEND_MIN} 区间，"
                     f"暂挂保留候选池，待异源杠杆",
            "candidates_to_keep": evidence.get("candidates", []),
        }
    
    else:
        # 深耕，生成策略
        strategies = generate_deepen_strategy(current_dataset, evidence)
        return {
            "action": "deepen",
            "dataset": current_dataset,
            "reason": f"PROD {evidence['prod_stats']['min']:.3f} < {PROD_DEEP_MIN}，有突破空间，继续深耕",
            "strategies": strategies,
            "recommended_wave_size": 8 * len(strategies) if strategies else 8,
        }


def print_plan(plan):
    """打印波次规划。"""
    print(f"\n{'='*60}")
    print(f"波次规划: {plan['action'].upper()}")
    print(f"{'='*60}")
    print(f"数据集: {plan.get('dataset', plan.get('from_dataset', '-'))}")
    print(f"原因: {plan['reason']}")
    
    if plan["action"] == "switch":
        print(f"\n切换: {plan['from_dataset']} -> {plan['to_dataset']}")
        print(f"切换原因: {plan['switch_reason']}")
        de = plan.get("death_evidence", {})
        if de:
            print(f"\n判死证据:")
            print(f"  PROD 墙: {de['prod_stats']['min']:.3f} (min) / {de['prod_stats']['avg']:.3f} (avg)")
            print(f"  设置空间: {len(de['settings_tried'])} 种已尝试")
            print(f"  结构变体: {len(de['structures_tried'])} 种已尝试")
            print(f"  救援武器: {len(de['rescue_weapons_tried'])}/{len(RESCUE_WEAPONS)} 种已实测")
    
    elif plan["action"] == "deepen":
        strategies = plan.get("strategies", [])
        print(f"\n深耕策略 ({len(strategies)} 条):")
        for s in strategies:
            print(f"  [{s['priority']}] {s['type']}: {s['description']}")
            if s.get("candidates"):
                print(f"      候选: {', '.join(s['candidates'][:3])}")
        print(f"\n建议波次大小: {plan.get('recommended_wave_size', 8)}")
    
    elif plan["action"] == "suspend":
        print(f"\n候选池保留: {len(plan.get('candidates_to_keep', []))} 个 alpha")
    
    print(f"{'='*60}\n")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    
    p = sub.add_parser("next")
    p.add_argument("--current-dataset", required=True)
    p.add_argument("--wave")
    
    p = sub.add_parser("status")
    p.add_argument("--dataset", required=True)
    
    a = ap.parse_args()
    
    if a.cmd == "next":
        plan = plan_next_wave(a.current_dataset, a.wave)
        print_plan(plan)
        
        # 保存规划结果
        out = os.path.join(ROOT, "results", f"wave_plan_{a.wave or 'next'}.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        json.dump(plan, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"规划已保存: {out}")
    
    elif a.cmd == "status":
        evidence = assess_dataset(a.dataset)
        if evidence:
            print(json.dumps(evidence, ensure_ascii=False, indent=2))
        else:
            print(f"数据集 {a.dataset} 无历史数据")


if __name__ == "__main__":
    main()
