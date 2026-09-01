# -*- coding: utf-8 -*-
"""discipline_monitor.py - 战役纪律改进实证监控器。

监控实施"有纪律地切换"流程后 10 轮回测的表现，验证改进是否有益。

监控指标：
  1. 配额利用率：每轮回测的表达式数量 vs 实际使用配额
  2. 判死及时性：从首次撞 PROD 墙到判死封存的波次数
  3. 深耕收益：PROD < 0.75 数据集的 alpha 产出率
  4. 切换准确性：判死切换后新数据集的探索效率
  5. 候选池质量：SUSPEND 数据集的候选 alpha 数量与质量

用法:
  python discipline_monitor.py start --wave 17A --dataset other455
  python discipline_monitor.py record --wave 17A --batch-id <id> --exprs 8 --complete 8 --candidates 2
  python discipline_monitor.py report --waves 10
"""
import argparse, collections, datetime, glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# 监控数据存储路径
MONITOR_DIR = os.path.join(ROOT, "monitoring")
os.makedirs(MONITOR_DIR, exist_ok=True)


def get_monitor_file(wave):
    """获取监控数据文件路径。"""
    return os.path.join(MONITOR_DIR, f"discipline_monitor_{wave}.json")


def load_monitor_data(wave):
    """加载监控数据。"""
    path = get_monitor_file(wave)
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8-sig"))
    return {
        "wave": wave,
        "started_at": None,
        "dataset": None,
        "batches": [],
        "discipline_metrics": {
            "prod_classification": {"DEEP": 0, "SUSPEND": 0, "DEAD": 0, "UNKNOWN": 0},
            "death_evidence_check": {"settings_exhausted": False, "structures_exhausted": False,
                                     "rescue_weapons_exhausted": False, "prod_wall_structural": False},
            "switch_triggered": False,
            "switch_reason": None,
            "deepen_strategies": [],
        },
        "efficiency_metrics": {
            "total_exprs": 0,
            "total_complete": 0,
            "total_candidates": 0,
            "total_quota_used": 0,
            "prod_wall_first_seen": None,
            "death_verdict_wave": None,
            "waves_to_death": None,
        },
        "completed_at": None,
    }


def save_monitor_data(data):
    """保存监控数据。"""
    path = get_monitor_file(data["wave"])
    tmp = path + ".tmp"
    json.dump(data, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def start_monitoring(wave, dataset):
    """开始监控一个波次。"""
    data = load_monitor_data(wave)
    data["started_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    data["dataset"] = dataset
    save_monitor_data(data)
    print(f"[monitor] 开始监控 wave={wave} dataset={dataset}")
    print(f"[monitor] 数据文件: {get_monitor_file(wave)}")


def record_batch(wave, batch_id, exprs, complete, candidates, prod_stats=None):
    """记录一个批次的回测结果。"""
    data = load_monitor_data(wave)
    
    batch = {
        "batch_id": batch_id,
        "exprs": exprs,
        "complete": complete,
        "candidates": candidates,
        "recorded_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    
    if prod_stats:
        batch["prod_stats"] = prod_stats
        # 更新 PROD 分类统计
        for cat, count in prod_stats.items():
            if cat in data["discipline_metrics"]["prod_classification"]:
                data["discipline_metrics"]["prod_classification"][cat] += count
    
    data["batches"].append(batch)
    
    # 更新效率指标
    data["efficiency_metrics"]["total_exprs"] += exprs
    data["efficiency_metrics"]["total_complete"] += complete
    data["efficiency_metrics"]["total_candidates"] += candidates
    data["efficiency_metrics"]["total_quota_used"] += exprs  # 简化计算
    
    save_monitor_data(data)
    print(f"[monitor] 记录批次 wave={wave} batch={batch_id} exprs={exprs} complete={complete} candidates={candidates}")


def record_discipline_decision(wave, decision_type, details):
    """记录纪律决策。"""
    data = load_monitor_data(wave)
    
    if decision_type == "prod_classification":
        data["discipline_metrics"]["prod_classification"] = details
    elif decision_type == "death_evidence":
        data["discipline_metrics"]["death_evidence_check"] = details
    elif decision_type == "switch":
        data["discipline_metrics"]["switch_triggered"] = True
        data["discipline_metrics"]["switch_reason"] = details.get("reason")
    elif decision_type == "deepen":
        data["discipline_metrics"]["deepen_strategies"] = details.get("strategies", [])
    elif decision_type == "prod_wall_first_seen":
        data["efficiency_metrics"]["prod_wall_first_seen"] = details.get("wave")
    elif decision_type == "death_verdict":
        data["efficiency_metrics"]["death_verdict_wave"] = details.get("wave")
        # 计算判死及时性
        first_seen = data["efficiency_metrics"].get("prod_wall_first_seen")
        if first_seen:
            # 简化计算：假设 wave 编号是连续的
            data["efficiency_metrics"]["waves_to_death"] = details.get("wave_num", 0) - first_seen
    
    save_monitor_data(data)
    print(f"[monitor] 记录纪律决策 wave={wave} type={decision_type}")


def complete_monitoring(wave):
    """完成监控。"""
    data = load_monitor_data(wave)
    data["completed_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    save_monitor_data(data)
    print(f"[monitor] 完成监控 wave={wave}")


def generate_report(waves=10):
    """生成实证报告。"""
    # 收集所有监控数据
    all_data = []
    for f in sorted(glob.glob(os.path.join(MONITOR_DIR, "discipline_monitor_*.json"))):
        try:
            data = json.load(open(f, encoding="utf-8-sig"))
            all_data.append(data)
        except Exception as e:
            print(f"[report] 跳过损坏文件 {f}: {e}")
    
    if not all_data:
        print("[report] 无监控数据")
        return
    
    # 取最近 N 个波次
    recent = all_data[-waves:] if len(all_data) > waves else all_data
    
    # 计算汇总指标
    summary = {
        "total_waves": len(recent),
        "total_exprs": sum(d["efficiency_metrics"]["total_exprs"] for d in recent),
        "total_complete": sum(d["efficiency_metrics"]["total_complete"] for d in recent),
        "total_candidates": sum(d["efficiency_metrics"]["total_candidates"] for d in recent),
        "prod_classification": collections.Counter(),
        "switch_triggered_count": sum(1 for d in recent if d["discipline_metrics"]["switch_triggered"]),
        "avg_waves_to_death": None,
        "datasets": list(set(d["dataset"] for d in recent if d["dataset"])),
    }
    
    for d in recent:
        for cat, count in d["discipline_metrics"]["prod_classification"].items():
            summary["prod_classification"][cat] += count
    
    # 计算平均判死波次数
    waves_to_death = [d["efficiency_metrics"]["waves_to_death"] 
                      for d in recent if d["efficiency_metrics"]["waves_to_death"] is not None]
    if waves_to_death:
        summary["avg_waves_to_death"] = sum(waves_to_death) / len(waves_to_death)
    
    # 计算效率指标
    if summary["total_exprs"] > 0:
        summary["complete_rate"] = summary["total_complete"] / summary["total_exprs"]
        summary["candidate_rate"] = summary["total_candidates"] / summary["total_exprs"]
    else:
        summary["complete_rate"] = 0
        summary["candidate_rate"] = 0
    
    # 生成报告
    report = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "summary": summary,
        "wave_details": recent,
        "conclusion": generate_conclusion(summary),
    }
    
    # 保存报告
    report_path = os.path.join(MONITOR_DIR, f"discipline_report_{datetime.date.today().isoformat()}.json")
    json.dump(report, open(report_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    
    # 打印报告
    print_report(summary, report_path)
    
    return report


def generate_conclusion(summary):
    """生成结论。"""
    conclusions = []
    
    # 判死及时性
    if summary["avg_waves_to_death"] is not None:
        if summary["avg_waves_to_death"] <= 3:
            conclusions.append("判死及时性优秀：平均 %.1f 波次内完成判死" % summary["avg_waves_to_death"])
        elif summary["avg_waves_to_death"] <= 5:
            conclusions.append("判死及时性良好：平均 %.1f 波次内完成判死" % summary["avg_waves_to_death"])
        else:
            conclusions.append("判死及时性待改进：平均 %.1f 波次才完成判死" % summary["avg_waves_to_death"])
    
    # PROD 分类分布
    pc = summary["prod_classification"]
    total_classified = sum(pc.values())
    if total_classified > 0:
        deep_pct = pc.get("DEEP", 0) / total_classified * 100
        suspend_pct = pc.get("SUSPEND", 0) / total_classified * 100
        dead_pct = pc.get("DEAD", 0) / total_classified * 100
        conclusions.append("PROD 分类分布: DEEP %.1f%% / SUSPEND %.1f%% / DEAD %.1f%%" % 
                          (deep_pct, suspend_pct, dead_pct))
        
        if dead_pct > 50:
            conclusions.append("判死比例较高，说明纪律执行严格，避免了配额浪费")
        elif deep_pct > 50:
            conclusions.append("深耕比例较高，说明候选数据集质量较好")
    
    # 切换准确性
    if summary["switch_triggered_count"] > 0:
        conclusions.append("切换触发 %d 次，说明判死证据链闭环有效" % summary["switch_triggered_count"])
    
    # 候选率
    if summary["candidate_rate"] > 0.1:
        conclusions.append("候选率 %.1f%%，说明挖掘效率良好" % (summary["candidate_rate"] * 100))
    elif summary["candidate_rate"] > 0.05:
        conclusions.append("候选率 %.1f%%，说明挖掘效率一般" % (summary["candidate_rate"] * 100))
    else:
        conclusions.append("候选率 %.1f%%，说明挖掘效率待改进" % (summary["candidate_rate"] * 100))
    
    return conclusions


def print_report(summary, report_path):
    """打印报告。"""
    print("\n" + "=" * 60)
    print("战役纪律改进实证报告")
    print("=" * 60)
    print(f"监控波次数: {summary['total_waves']}")
    print(f"总表达式数: {summary['total_exprs']}")
    print(f"总完成数: {summary['total_complete']}")
    print(f"总候选数: {summary['total_candidates']}")
    print(f"完成率: {summary['complete_rate']*100:.1f}%")
    print(f"候选率: {summary['candidate_rate']*100:.1f}%")
    print(f"\nPROD 分类分布:")
    for cat, count in summary["prod_classification"].items():
        print(f"  {cat}: {count}")
    print(f"\n切换触发次数: {summary['switch_triggered_count']}")
    if summary["avg_waves_to_death"] is not None:
        print(f"平均判死波次数: {summary['avg_waves_to_death']:.1f}")
    print(f"\n涉及数据集: {', '.join(summary['datasets'])}")
    print("\n结论:")
    for c in generate_conclusion(summary):
        print(f"  - {c}")
    print("=" * 60)
    print(f"报告已保存: {report_path}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    
    p = sub.add_parser("start")
    p.add_argument("--wave", required=True)
    p.add_argument("--dataset", required=True)
    
    p = sub.add_parser("record")
    p.add_argument("--wave", required=True)
    p.add_argument("--batch-id", required=True)
    p.add_argument("--exprs", type=int, required=True)
    p.add_argument("--complete", type=int, required=True)
    p.add_argument("--candidates", type=int, required=True)
    
    p = sub.add_parser("decision")
    p.add_argument("--wave", required=True)
    p.add_argument("--type", required=True, choices=["prod_classification", "death_evidence", "switch", "deepen", "prod_wall_first_seen", "death_verdict"])
    p.add_argument("--details", required=True, help="JSON 格式的详细信息")
    
    p = sub.add_parser("complete")
    p.add_argument("--wave", required=True)
    
    p = sub.add_parser("report")
    p.add_argument("--waves", type=int, default=10)
    
    a = ap.parse_args()
    
    if a.cmd == "start":
        start_monitoring(a.wave, a.dataset)
    elif a.cmd == "record":
        record_batch(a.wave, a.batch_id, a.exprs, a.complete, a.candidates)
    elif a.cmd == "decision":
        details = json.loads(a.details)
        record_discipline_decision(a.wave, a.type, details)
    elif a.cmd == "complete":
        complete_monitoring(a.wave)
    elif a.cmd == "report":
        generate_report(a.waves)


if __name__ == "__main__":
    main()
