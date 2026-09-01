# -*- coding: utf-8 -*-
"""campaign_discipline.py - 战役纪律执行器：判死证据链闭环 + 数据集切换决策。

落实"有纪律地切换"原则：
  1. PROD 墙三档分类：<0.75 深耕 / 0.75-0.80 暂挂 / >0.80 判死
  2. 判死证据链闭环：设置空间穷尽 + 救援武器实测 + 结构变体无效
  3. 数据集切换触发器：满足判死条件自动生成切换建议
  4. 候选池状态跟踪：结构化记录每个数据集的挖掘状态

用法:
  python campaign_discipline.py assess --dataset chart_cnn_alpha --wave 16U
  python campaign_discipline.py decide --dataset chart_cnn_alpha
  python campaign_discipline.py pool --list
  python campaign_discipline.py pool --add insider_feats --status suspended
"""
import argparse, datetime, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# PROD 墙三档阈值
PROD_DEEP_MIN = 0.75      # <0.75: 深耕，继续优化
PROD_SUSPEND_MIN = 0.80   # 0.75-0.80: 暂挂，保留候选池
                          # >0.80: 判死封存

# 救援武器清单（论坛工具箱）
RESCUE_WEAPONS = [
    "ts_target_tvr_decay",           # 定目标换手
    "residual_diff_template",        # 残差差分模板 ts_zscore(A,63)-ts_zscore(group_neutralize(A,sector),63)
    "vec_avg_to_vec_max",            # vec_avg→vec_max 换聚合
    "neutralization_switch",         # 中性化切换
    "inner_outer_neutralization",    # 内细外粗二次中性化
    "weight_perturbation",           # 权重扰动
    "layer_switch",                  # 换层（rank→group_rank→quantile→signed_power）
    "subtract_structure",            # subtract 多空差结构
    "horizon_mix",                   # 跨 horizon 组合
    "decay_gradient",                # decay 梯度扫描
]


def load_campaign_state():
    """加载战役状态。"""
    path = os.path.join(ROOT, "kor_d1_campaign_state.json")
    if os.path.exists(path):
        # 使用 utf-8-sig 处理 BOM
        return json.load(open(path, encoding="utf-8-sig"))
    return {"waves": [], "dataset_pool": {}}


def save_campaign_state(state):
    """保存战役状态。"""
    path = os.path.join(ROOT, "kor_d1_campaign_state.json")
    tmp = path + ".tmp"
    json.dump(state, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def get_dataset_waves(state, dataset):
    """获取指定数据集的所有波次。
    
    注意：campaign state 中的 wave 结构可能有两种格式：
    1. 顶层 wave 对象包含 dataset 字段
    2. wave 编号作为键，dataset 在嵌套结构中
    """
    waves = []
    for w in state.get("waves", []):
        # 格式1：顶层 dataset 字段
        if w.get("dataset") == dataset:
            waves.append(w)
        # 格式2：检查嵌套的 multisims 中的 dataset
        elif any(ms.get("dataset") == dataset for ms in w.get("multisims", [])):
            waves.append(w)
    return waves


def extract_prod_correlations(waves):
    """从波次中提取所有 PROD 相关性数据。"""
    prods = []
    for w in waves:
        verdict = w.get("verdict", "")
        # 提取 PC0.xxxx 模式
        for m in re.finditer(r"PC\s*0\.(\d+)", verdict):
            prods.append(float(f"0.{m.group(1)}"))
        # 提取 PROD相关=0.xxxx 模式
        for m in re.finditer(r"PROD相关[=:]?\s*0\.(\d+)", verdict):
            prods.append(float(f"0.{m.group(1)}"))
        # 提取 PROD 0.xxxx 模式
        for m in re.finditer(r"PROD\s+0\.(\d+)", verdict):
            prods.append(float(f"0.{m.group(1)}"))
    return prods


def extract_settings_tried(waves):
    """提取已尝试的设置组合。"""
    settings = set()
    for w in waves:
        for ms in w.get("multisims", []):
            s = ms.get("setting", "")
            if s:
                settings.add(s)
    return settings


def extract_structures_tried(waves):
    """提取已尝试的结构类型。"""
    structures = set()
    for w in waves:
        for ms in w.get("multisims", []):
            style = ms.get("style", "")
            if "rank" in style.lower():
                structures.add("rank")
            if "group_rank" in style.lower():
                structures.add("group_rank")
            if "quantile" in style.lower():
                structures.add("quantile")
            if "signed_power" in style.lower():
                structures.add("signed_power")
            if "subtract" in style.lower():
                structures.add("subtract")
            if "linear" in style.lower() or "mix" in style.lower():
                structures.add("linear_mix")
            if "trade_when" in style.lower():
                structures.add("event_gated")
    return structures


def assess_dataset(dataset, wave_tag=None):
    """评估数据集的挖掘状态，生成判死证据链报告。"""
    state = load_campaign_state()
    waves = get_dataset_waves(state, dataset)
    
    if not waves:
        print(f"[assess] 数据集 {dataset} 无历史波次")
        return None
    
    # 提取关键指标
    prods = extract_prod_correlations(waves)
    settings = extract_settings_tried(waves)
    structures = extract_structures_tried(waves)
    
    # 统计
    total_waves = len(waves)
    total_multisims = sum(len(w.get("multisims", [])) for w in waves)
    
    # PROD 墙分析
    prod_min = min(prods) if prods else None
    prod_max = max(prods) if prods else None
    prod_avg = sum(prods) / len(prods) if prods else None
    
    # 判死证据链评估
    evidence = {
        "dataset": dataset,
        "total_waves": total_waves,
        "total_multisims": total_multisims,
        "prod_stats": {
            "min": prod_min,
            "max": prod_max,
            "avg": prod_avg,
            "count": len(prods),
        },
        "settings_tried": sorted(settings),
        "structures_tried": sorted(structures),
        "rescue_weapons_tried": [],
        "rescue_weapons_remaining": [],
        "verdicts": [w.get("verdict", "")[:200] for w in waves[-3:]],  # 最近3个verdict
    }
    
    # 检查救援武器实测情况
    verdict_text = " ".join(w.get("verdict", "") for w in waves)
    for weapon in RESCUE_WEAPONS:
        if weapon.replace("_", "") in verdict_text.replace("_", "").lower():
            evidence["rescue_weapons_tried"].append(weapon)
        else:
            evidence["rescue_weapons_remaining"].append(weapon)
    
    # 判死判定
    death_criteria = {
        "prod_wall_structural": prod_min is not None and prod_min > PROD_SUSPEND_MIN,
        "settings_exhausted": len(settings) >= 4,  # 至少4种设置组合
        "structures_exhausted": len(structures) >= 5,  # 至少5种结构
        "rescue_weapons_exhausted": len(evidence["rescue_weapons_remaining"]) == 0,
    }
    evidence["death_criteria"] = death_criteria
    evidence["death_score"] = sum(death_criteria.values())
    
    # 三档分类
    if prod_min is None:
        evidence["category"] = "UNKNOWN"
        evidence["recommendation"] = "需要更多 PROD 相关性数据"
    elif prod_min < PROD_DEEP_MIN:
        evidence["category"] = "DEEP"
        evidence["recommendation"] = f"PROD 墙 {prod_min:.3f} < {PROD_DEEP_MIN}，有突破空间，建议深耕"
    elif prod_min < PROD_SUSPEND_MIN:
        evidence["category"] = "SUSPEND"
        evidence["recommendation"] = f"PROD 墙 {prod_min:.3f} 在 {PROD_DEEP_MIN}-{PROD_SUSPEND_MIN} 区间，建议暂挂保留候选池"
    else:
        evidence["category"] = "DEAD"
        evidence["recommendation"] = f"PROD 墙 {prod_min:.3f} > {PROD_SUSPEND_MIN}，建议判死封存"
    
    # 判死证据链完整性检查
    if evidence["category"] == "DEAD":
        missing = []
        if not death_criteria["settings_exhausted"]:
            missing.append("设置空间未穷尽（<4种）")
        if not death_criteria["structures_exhausted"]:
            missing.append("结构变体未穷尽（<5种）")
        if not death_criteria["rescue_weapons_exhausted"]:
            missing.append(f"救援武器未实测：{', '.join(evidence['rescue_weapons_remaining'][:3])}")
        if missing:
            evidence["death_evidence_gap"] = missing
            evidence["recommendation"] += f"，但证据链不完整：{'；'.join(missing)}"
    
    return evidence


def decide_switch(dataset):
    """生成数据集切换决策建议。"""
    evidence = assess_dataset(dataset)
    if not evidence:
        return None
    
    decision = {
        "dataset": dataset,
        "category": evidence["category"],
        "death_score": evidence["death_score"],
        "recommendation": evidence["recommendation"],
        "switch_trigger": False,
        "next_targets": [],
    }
    
    # 切换触发条件
    if evidence["category"] == "DEAD" and evidence["death_score"] >= 3:
        decision["switch_trigger"] = True
        decision["switch_reason"] = "满足判死条件，建议切换下一数据集"
        
        # 推荐下一目标（从战役状态中获取）
        state = load_campaign_state()
        pool = state.get("dataset_pool", {})
        for ds, info in pool.items():
            if ds != dataset and info.get("status") in ("unexplored", "suspended"):
                decision["next_targets"].append({
                    "dataset": ds,
                    "status": info.get("status"),
                    "priority": info.get("priority", 99),
                })
        decision["next_targets"].sort(key=lambda x: x["priority"])
    
    return decision


def pool_manage(action, dataset=None, status=None, priority=None):
    """管理数据集候选池。"""
    state = load_campaign_state()
    pool = state.setdefault("dataset_pool", {})
    
    if action == "list":
        print(f"{'dataset':<30} {'status':<12} {'priority':<8} {'last_wave':<10} notes")
        print("-" * 80)
        for ds, info in sorted(pool.items(), key=lambda x: x[1].get("priority", 99)):
            print(f"{ds:<30} {info.get('status', 'unknown'):<12} "
                  f"{info.get('priority', 99):<8} {info.get('last_wave', '-'):<10} "
                  f"{info.get('notes', '')[:40]}")
        return
    
    if action == "add" and dataset:
        pool[dataset] = {
            "status": status or "unexplored",
            "priority": priority or 99,
            "added_at": datetime.date.today().isoformat(),
            "notes": "",
        }
        save_campaign_state(state)
        print(f"[pool] 添加 {dataset} status={status} priority={priority}")
        return
    
    if action == "update" and dataset:
        if dataset in pool:
            if status:
                pool[dataset]["status"] = status
            if priority is not None:
                pool[dataset]["priority"] = priority
            pool[dataset]["updated_at"] = datetime.date.today().isoformat()
            save_campaign_state(state)
            print(f"[pool] 更新 {dataset} status={status} priority={priority}")
        else:
            print(f"[pool] 数据集 {dataset} 不存在")
        return


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    
    p = sub.add_parser("assess")
    p.add_argument("--dataset", required=True)
    p.add_argument("--wave")
    
    p = sub.add_parser("decide")
    p.add_argument("--dataset", required=True)
    
    p = sub.add_parser("pool")
    p.add_argument("--list", action="store_true")
    p.add_argument("--add")
    p.add_argument("--update")
    p.add_argument("--status")
    p.add_argument("--priority", type=int)
    
    a = ap.parse_args()
    
    if a.cmd == "assess":
        evidence = assess_dataset(a.dataset, a.wave)
        if evidence:
            print(json.dumps(evidence, ensure_ascii=False, indent=2))
    
    elif a.cmd == "decide":
        decision = decide_switch(a.dataset)
        if decision:
            print(json.dumps(decision, ensure_ascii=False, indent=2))
    
    elif a.cmd == "pool":
        if a.list:
            pool_manage("list")
        elif a.add:
            pool_manage("add", a.add, a.status, a.priority)
        elif a.update:
            pool_manage("update", a.update, a.status, a.priority)


if __name__ == "__main__":
    main()
