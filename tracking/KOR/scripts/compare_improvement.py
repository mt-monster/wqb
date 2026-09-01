# -*- coding: utf-8 -*-
"""compare_improvement.py - 改进前后效率对比分析。

对比实施"有纪律地切换"流程前后的关键指标：
  1. 配额利用率：每轮回测的表达式数量 vs 实际产出
  2. 判死及时性：从首次撞 PROD 墙到判死封存的波次数
  3. 深耕收益：PROD < 0.75 数据集的 alpha 产出率
  4. 切换准确性：判死切换后新数据集的探索效率

数据来源：
  - 改进前：tracking/KOR/kor_d1_campaign_state.json 历史波次
  - 改进后：tracking/KOR/monitoring/discipline_monitor_*.json 监控数据
"""
import datetime, glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load_historical_waves():
    """加载改进前的历史波次数据。"""
    path = os.path.join(ROOT, "kor_d1_campaign_state.json")
    if not os.path.exists(path):
        return []
    
    state = json.load(open(path, encoding="utf-8-sig"))
    waves = state.get("waves", [])
    
    # 提取关键指标
    historical = []
    for w in waves:
        wave_data = {
            "wave": w.get("wave"),
            "dataset": w.get("dataset"),
            "multisims": len(w.get("multisims", [])),
            "verdict": w.get("verdict", ""),
            "switch_reason": w.get("switch_reason", ""),
        }
        
        # 从 verdict 中提取指标
        verdict = w.get("verdict", "")
        
        # 提取 COMPLETE 数
        m = re.search(r"(\d+)/(\d+)\s+COMPLETE", verdict)
        if m:
            wave_data["complete"] = int(m.group(1))
            wave_data["total"] = int(m.group(2))
        else:
            wave_data["complete"] = 0
            wave_data["total"] = 0
        
        # 提取 PROD 相关性
        prods = []
        for m in re.finditer(r"PC\s*0\.(\d+)", verdict):
            prods.append(float(f"0.{m.group(1)}"))
        for m in re.finditer(r"PROD相关[=:]?\s*0\.(\d+)", verdict):
            prods.append(float(f"0.{m.group(1)}"))
        wave_data["prod_min"] = min(prods) if prods else None
        wave_data["prod_max"] = max(prods) if prods else None
        
        # 提取候选数（sharpe > 1.58）
        candidates = 0
        for m in re.finditer(r"sh(\d+\.?\d*)", verdict):
            if float(m.group(1)) > 1.58:
                candidates += 1
        wave_data["candidates"] = candidates
        
        # 判断是否判死
        wave_data["is_dead"] = "判死" in verdict or "DEAD" in verdict
        wave_data["is_suspend"] = "暂挂" in verdict or "SUSPEND" in verdict
        
        historical.append(wave_data)
    
    return historical


def load_monitoring_waves():
    """加载改进后的监控波次数据。"""
    monitoring = []
    for f in sorted(glob.glob(os.path.join(ROOT, "monitoring", "discipline_monitor_*.json"))):
        try:
            data = json.load(open(f, encoding="utf-8-sig"))
            wave_data = {
                "wave": data.get("wave"),
                "dataset": data.get("dataset"),
                "total_exprs": data["efficiency_metrics"]["total_exprs"],
                "total_complete": data["efficiency_metrics"]["total_complete"],
                "total_candidates": data["efficiency_metrics"]["total_candidates"],
                "prod_classification": data["discipline_metrics"]["prod_classification"],
                "switch_triggered": data["discipline_metrics"]["switch_triggered"],
                "death_evidence": data["discipline_metrics"]["death_evidence_check"],
            }
            monitoring.append(wave_data)
        except Exception as e:
            print(f"[compare] 跳过损坏文件 {f}: {e}")
    
    return monitoring


def calculate_metrics(waves, label):
    """计算效率指标。"""
    if not waves:
        return None
    
    metrics = {
        "label": label,
        "total_waves": len(waves),
        "total_exprs": 0,
        "total_complete": 0,
        "total_candidates": 0,
        "prod_stats": {"DEEP": 0, "SUSPEND": 0, "DEAD": 0, "UNKNOWN": 0},
        "switch_count": 0,
        "datasets": set(),
    }
    
    for w in waves:
        # 改进前数据
        if "multisims" in w:
            metrics["total_exprs"] += w.get("total", 0)
            metrics["total_complete"] += w.get("complete", 0)
            metrics["total_candidates"] += w.get("candidates", 0)
            metrics["datasets"].add(w.get("dataset"))
            
            # PROD 分类
            prod_min = w.get("prod_min")
            if prod_min is None:
                metrics["prod_stats"]["UNKNOWN"] += 1
            elif prod_min < 0.75:
                metrics["prod_stats"]["DEEP"] += 1
            elif prod_min < 0.80:
                metrics["prod_stats"]["SUSPEND"] += 1
            else:
                metrics["prod_stats"]["DEAD"] += 1
            
            # 切换
            if w.get("is_dead") or w.get("switch_reason"):
                metrics["switch_count"] += 1
        
        # 改进后数据
        else:
            metrics["total_exprs"] += w.get("total_exprs", 0)
            metrics["total_complete"] += w.get("total_complete", 0)
            metrics["total_candidates"] += w.get("total_candidates", 0)
            metrics["datasets"].add(w.get("dataset"))
            
            # PROD 分类
            for cat, count in w.get("prod_classification", {}).items():
                metrics["prod_stats"][cat] += count
            
            # 切换
            if w.get("switch_triggered"):
                metrics["switch_count"] += 1
    
    # 计算比率
    if metrics["total_exprs"] > 0:
        metrics["complete_rate"] = metrics["total_complete"] / metrics["total_exprs"]
        metrics["candidate_rate"] = metrics["total_candidates"] / metrics["total_exprs"]
    else:
        metrics["complete_rate"] = 0
        metrics["candidate_rate"] = 0
    
    metrics["datasets"] = list(metrics["datasets"])
    
    return metrics


def generate_comparison_report():
    """生成对比报告。"""
    # 加载数据
    historical = load_historical_waves()
    monitoring = load_monitoring_waves()
    
    # 计算指标
    before = calculate_metrics(historical, "改进前")
    after = calculate_metrics(monitoring, "改进后")
    
    if not before or not after:
        print("[compare] 数据不足，无法生成对比报告")
        return None
    
    # 生成报告
    report = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "before": before,
        "after": after,
        "improvement": {},
    }
    
    # 计算改进幅度
    if before["complete_rate"] > 0:
        report["improvement"]["complete_rate_change"] = (
            (after["complete_rate"] - before["complete_rate"]) / before["complete_rate"] * 100
        )
    if before["candidate_rate"] > 0:
        report["improvement"]["candidate_rate_change"] = (
            (after["candidate_rate"] - before["candidate_rate"]) / before["candidate_rate"] * 100
        )
    
    # PROD 分类改进
    before_dead_pct = before["prod_stats"]["DEAD"] / max(1, sum(before["prod_stats"].values())) * 100
    after_dead_pct = after["prod_stats"]["DEAD"] / max(1, sum(after["prod_stats"].values())) * 100
    report["improvement"]["dead_classification_change"] = after_dead_pct - before_dead_pct
    
    # 切换及时性
    report["improvement"]["switch_count_change"] = after["switch_count"] - before["switch_count"]
    
    # 保存报告
    report_path = os.path.join(ROOT, "monitoring", f"improvement_comparison_{datetime.date.today().isoformat()}.json")
    json.dump(report, open(report_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    
    # 打印报告
    print_comparison(report, report_path)
    
    return report


def print_comparison(report, report_path):
    """打印对比报告。"""
    before = report["before"]
    after = report["after"]
    improvement = report["improvement"]
    
    print("\n" + "=" * 70)
    print("战役纪律改进前后对比报告")
    print("=" * 70)
    
    print(f"\n{'指标':<30} {'改进前':<20} {'改进后':<20} {'变化':<15}")
    print("-" * 70)
    
    # 基础指标
    print(f"{'总波次数':<30} {before['total_waves']:<20} {after['total_waves']:<20} {'-':<15}")
    print(f"{'总表达式数':<30} {before['total_exprs']:<20} {after['total_exprs']:<20} {'-':<15}")
    print(f"{'总完成数':<30} {before['total_complete']:<20} {after['total_complete']:<20} {'-':<15}")
    print(f"{'总候选数':<30} {before['total_candidates']:<20} {after['total_candidates']:<20} {'-':<15}")
    
    # 效率指标
    complete_change = improvement.get("complete_rate_change", 0)
    candidate_change = improvement.get("candidate_rate_change", 0)
    print(f"{'完成率':<30} {before['complete_rate']*100:>6.1f}%{'':<13} {after['complete_rate']*100:>6.1f}%{'':<13} {complete_change:>+6.1f}%{'':<8}")
    print(f"{'候选率':<30} {before['candidate_rate']*100:>6.1f}%{'':<13} {after['candidate_rate']*100:>6.1f}%{'':<13} {candidate_change:>+6.1f}%{'':<8}")
    
    # PROD 分类
    print(f"\n{'PROD 分类':<30} {'改进前':<20} {'改进后':<20} {'变化':<15}")
    print("-" * 70)
    for cat in ["DEEP", "SUSPEND", "DEAD", "UNKNOWN"]:
        before_count = before["prod_stats"].get(cat, 0)
        after_count = after["prod_stats"].get(cat, 0)
        print(f"{cat:<30} {before_count:<20} {after_count:<20} {after_count - before_count:>+6}{'':<9}")
    
    # 切换
    switch_change = improvement.get("switch_count_change", 0)
    print(f"\n{'切换触发次数':<30} {before['switch_count']:<20} {after['switch_count']:<20} {switch_change:>+6}{'':<9}")
    
    # 结论
    print("\n" + "=" * 70)
    print("结论")
    print("=" * 70)
    
    conclusions = []
    
    if candidate_change > 10:
        conclusions.append(f"候选率显著提升 {candidate_change:.1f}%，说明纪律执行有效提高了挖掘效率")
    elif candidate_change > 0:
        conclusions.append(f"候选率略有提升 {candidate_change:.1f}%，说明纪律执行有一定效果")
    elif candidate_change < -10:
        conclusions.append(f"候选率显著下降 {candidate_change:.1f}%，说明纪律执行可能过于严格")
    else:
        conclusions.append(f"候选率基本不变 {candidate_change:.1f}%，说明纪律执行对效率影响不大")
    
    if improvement.get("dead_classification_change", 0) > 10:
        conclusions.append(f"DEAD 分类比例提升 {improvement['dead_classification_change']:.1f}%，说明判死及时性提高")
    
    if switch_change > 0:
        conclusions.append(f"切换触发次数增加 {switch_change} 次，说明判死证据链闭环有效")
    
    for c in conclusions:
        print(f"  - {c}")
    
    print("=" * 70)
    print(f"报告已保存: {report_path}")


def main():
    generate_comparison_report()


if __name__ == "__main__":
    main()
