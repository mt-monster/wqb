# -*- coding: utf-8 -*-
"""kor_pipeline_v2.py - 增强版 KOR 战役流水线（集成纪律监控）。

在 kor_pipeline.py 基础上集成：
  1. 战役纪律执行器（campaign_discipline.py）
  2. 纪律监控器（discipline_monitor.py）
  3. 波次规划器（wave_planner.py）

用法:
  python kor_pipeline_v2.py run --file candidates/x.json --dataset other455 --wave 17A [--submit] [--review]
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

# 导入原有模块
import gate as gate_mod
from kor_fetch_metrics import Api, load_creds

# 导入新增模块
from campaign_discipline import assess_dataset, decide_switch
from discipline_monitor import (
    start_monitoring, record_batch, record_discipline_decision,
    complete_monitoring, generate_report
)

SETTINGS = json.load(open(os.path.join(ROOT, "config", "settings.json"), encoding="utf-8"))
BATCH = SETTINGS.get("_multi_sim_batch_size", 8)


def run_pipeline_with_discipline(file_path, dataset, wave, submit=False, review=False, max_batches=99):
    """运行带纪律监控的流水线。"""
    # 1. 开始监控
    start_monitoring(wave, dataset)
    
    # 2. 评估数据集状态
    print(f"\n[pipeline] 评估数据集 {dataset} 状态...")
    evidence = assess_dataset(dataset)
    if evidence:
        print(f"[pipeline] 分类: {evidence['category']}")
        print(f"[pipeline] 建议: {evidence['recommendation']}")
        
        # 记录纪律决策
        record_discipline_decision(wave, "prod_classification", 
                                   {cat: 1 for cat in [evidence['category']]})
        record_discipline_decision(wave, "death_evidence", 
                                   evidence['death_criteria'])
        
        # 检查是否应该继续
        if evidence['category'] == 'DEAD' and evidence['death_score'] >= 3:
            print(f"[pipeline] 数据集 {dataset} 已判死，建议切换")
            decision = decide_switch(dataset)
            if decision and decision.get('switch_trigger'):
                record_discipline_decision(wave, "switch", {
                    "reason": decision['switch_reason'],
                    "next_targets": decision.get('next_targets', [])
                })
                print(f"[pipeline] 切换建议: {decision['switch_reason']}")
                complete_monitoring(wave)
                return
    
    # 3. 加载表达式
    d = json.load(open(file_path, encoding="utf-8"))
    exprs = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    exprs = [e for e in exprs if isinstance(e, str)]
    
    print(f"[pipeline] 加载 {len(exprs)} 个表达式")
    
    # 4. 门禁检查
    print(f"[pipeline] 门禁检查...")
    wl = gate_mod.load_whitelist(dataset)
    cons = json.load(open(os.path.join(ROOT, "reference", "kor_generation_constraints.json"),
                          encoding="utf-8"))
    poison = cons.get("poison_patterns", [])
    passed, failed = [], []
    for e in exprs:
        r = gate_mod.check_one(e, wl, dataset, poison)
        (passed if r["pass"] else failed).append({"expr": e, **({} if r["pass"] else {"issues": r["issues"]})})
    
    print(f"[pipeline] 门禁通过 {len(passed)}/{len(exprs)}")
    
    if not submit:
        print(f"[pipeline] 计划模式，不提交")
        complete_monitoring(wave)
        return
    
    # 5. 提交回测
    api = Api(); api.login(*load_creds())
    
    batches = [passed[i:i + BATCH] for i in range(0, len(passed), BATCH)]
    for bi, batch in enumerate(batches[:max_batches], 1):
        batch_exprs = [p["expr"] for p in batch]
        
        # 提交批次
        payloads = [{"type": "REGULAR", "settings": {k: v for k, v in SETTINGS.items()
                                                     if not k.startswith("_")},
                     "regular": e} for e in batch_exprs]
        body = payloads[0] if len(payloads) == 1 else payloads
        
        try:
            r = api.post("/simulations", body)
            loc = r.headers.get("Location") or ""
            msid = loc.rstrip("/").split("/")[-1]
            print(f"[pipeline] 提交批次 {bi}/{len(batches)} multisim={msid}")
            
            # 轮询到完成
            import time
            while True:
                time.sleep(20)
                d = json.load(api.get("/simulations/" + msid))
                status = d.get("status")
                if status in {"COMPLETE", "ERROR", "CANCELLED"}:
                    break
            
            # 记录批次结果
            children = d.get("children", [])
            complete_count = 0
            candidate_count = 0
            
            if status == "COMPLETE":
                alphas = []
                for c in children:
                    try:
                        sim = json.load(api.get("/simulations/" + c))
                        if sim.get("alpha"):
                            alphas.append(sim["alpha"])
                    except Exception:
                        pass
                complete_count = len(alphas)
                
                # 简单判断候选（sharpe > 1.58）
                for aid in alphas:
                    try:
                        alpha_detail = json.load(api.get(f"/alphas/{aid}"))
                        sharpe = alpha_detail.get("is", {}).get("sharpe")
                        if sharpe and sharpe > 1.58:
                            candidate_count += 1
                    except Exception:
                        pass
            
            record_batch(wave, msid, len(batch_exprs), complete_count, candidate_count)
            
        except Exception as e:
            print(f"[pipeline] 批次 {bi} 失败: {e}")
            record_batch(wave, f"batch_{bi}", len(batch_exprs), 0, 0)
    
    # 6. 完成监控
    complete_monitoring(wave)
    
    # 7. 生成报告
    if review:
        print(f"\n[pipeline] 生成监控报告...")
        generate_report(waves=10)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    
    p = sub.add_parser("run")
    p.add_argument("--file", required=True)
    p.add_argument("--dataset", required=True)
    p.add_argument("--wave", required=True)
    p.add_argument("--submit", action="store_true")
    p.add_argument("--review", action="store_true")
    p.add_argument("--max-batches", type=int, default=99)
    
    p = sub.add_parser("report")
    p.add_argument("--waves", type=int, default=10)
    
    a = ap.parse_args()
    
    if a.cmd == "run":
        run_pipeline_with_discipline(a.file, a.dataset, a.wave, a.submit, a.review, a.max_batches)
    elif a.cmd == "report":
        generate_report(a.waves)


if __name__ == "__main__":
    main()
