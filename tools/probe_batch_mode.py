# -*- coding: utf-8 -*-
"""probe_batch_mode.py - 2+6 探针批模式（早期判死机制）。

核心逻辑：
  1. 先跑 2 条探针（最强候选）
  2. 若 2 条全灭（Sharpe<0.5），判死数据集，跳过剩余 6 条
  3. 若 1 条达标（Sharpe>1.0），继续跑剩余 6 条

用法:
    python tools/probe_batch_mode.py --campaign-dir tracking/IND \
        --dataset pv70 --wave 125 --candidates candidates.json
"""
import argparse
import json
import os
import sys
from typing import Dict, List, Any, Tuple

# 添加 tools 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class ProbeBatchExecutor:
    """探针批执行器"""
    
    # 判死阈值
    PROBE_DEAD_THRESHOLD = 0.5  # 探针 Sharpe < 0.5 判死
    PROBE_PASS_THRESHOLD = 1.0  # 探针 Sharpe > 1.0 继续
    
    def __init__(self, campaign_dir: str, dataset: str, wave: int):
        self.campaign_dir = campaign_dir
        self.dataset = dataset
        self.wave = wave
        
    def select_probe_candidates(self, candidates: List[Dict], n: int = 2) -> List[Dict]:
        """
        选择最强探针候选
        
        策略：
        1. 优先选择质量预估 PASS 的候选
        2. 其次选择多样性最高的候选（不同算子/字段）
        3. 默认选择前 N 条
        """
        # 如果有质量预估结果，优先选择
        scored = []
        for c in candidates:
            score = 0
            # 质量预估加分
            if c.get("quality_verdict") == "EXPECTED_PASS":
                score += 100
            elif c.get("quality_verdict") == "REVIEW":
                score += 50
            # 多样性加分（简单启发式）
            expr = c.get("expression", "")
            if "ts_backfill" in expr:
                score += 10
            if "group_neutralize" in expr:
                score += 10
            if "rank" in expr:
                score += 5
            scored.append((score, c))
            
        # 按分数排序，取前 N
        scored.sort(key=lambda x: -x[0])
        return [c for _, c in scored[:n]]
        
    def analyze_probe_results(self, probe_results: List[Dict]) -> Tuple[str, str]:
        """
        分析探针结果，返回 (decision, reason)
        
        decision: "CONTINUE" | "DEAD" | "PARTIAL"
        """
        sharpes = [r.get("sharpe", 0) for r in probe_results]
        
        # 全灭判定
        if all(s < self.PROBE_DEAD_THRESHOLD for s in sharpes):
            return "DEAD", f"探针全灭: Sharpe={sharpes}, 均<{self.PROBE_DEAD_THRESHOLD}"
            
        # 有达标判定
        if any(s > self.PROBE_PASS_THRESHOLD for s in sharpes):
            return "CONTINUE", f"探针达标: max(Sharpe)={max(sharpes):.2f}>{self.PROBE_PASS_THRESHOLD}"
            
        # 部分存活
        return "PARTIAL", f"探针部分存活: Sharpe={sharpes}, 需完整批验证"
        
    def execute_probe_batch(self, candidates: List[Dict]) -> Dict[str, Any]:
        """
        执行探针批模式
        
        Returns:
            {
                "status": "PROBE_DEAD" | "PROBE_CONTINUE" | "COMPLETE",
                "probe_results": [...],
                "full_results": [...] or None,
                "saved_quota": int,
                "decision_reason": str
            }
        """
        # Phase 1: 探针批（2 条）
        probe_candidates = self.select_probe_candidates(candidates, n=2)
        probe_ids = [c["id"] for c in probe_candidates]
        
        print(f"[probe] 选择探针候选: {probe_ids}")
        for c in probe_candidates:
            print(f"  - {c['id']}: {c.get('expression', '')[:80]}...")
            
        # 模拟执行探针批（实际应调用 MCP create_multi_simulation）
        # 这里返回模拟结果，实际实现需要集成 MCP
        probe_results = self._simulate_batch(probe_candidates)
        
        # 分析探针结果
        decision, reason = self.analyze_probe_results(probe_results)
        
        result = {
            "status": f"PROBE_{decision}",
            "probe_results": probe_results,
            "full_results": None,
            "saved_quota": 0,
            "decision_reason": reason
        }
        
        if decision == "DEAD":
            # 判死，节省 6 条配额
            result["saved_quota"] = len(candidates) - 2
            print(f"[probe] 数据集判死: {reason}")
            print(f"[probe] 节省配额: {result['saved_quota']} 条")
            return result
            
        # Phase 2: 完整批（剩余 6 条）
        remaining = [c for c in candidates if c["id"] not in probe_ids][:6]
        print(f"[probe] 继续完整批: {len(remaining)} 条")
        
        full_results = self._simulate_batch(remaining)
        result["full_results"] = full_results
        result["status"] = "COMPLETE"
        
        return result
        
    def _simulate_batch(self, candidates: List[Dict]) -> List[Dict]:
        """
        模拟执行批量回测（实际应调用 MCP）
        
        TODO: 集成 mcp__wq-brain-http__create_multi_simulation
        """
        # 模拟结果
        results = []
        for c in candidates:
            # 这里应该实际调用 MCP 工具
            # 目前返回模拟数据用于测试
            results.append({
                "id": c["id"],
                "expression": c.get("expression", ""),
                "sharpe": 0.0,  # 模拟值
                "fitness": 0.0,
                "status": "SIMULATED"
            })
        return results


def main():
    ap = argparse.ArgumentParser(description="2+6 探针批模式")
    ap.add_argument("--campaign-dir", required=True)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--wave", type=int, required=True)
    ap.add_argument("--candidates", required=True, help="候选表达式 JSON")
    ap.add_argument("--probe-size", type=int, default=2, help="探针批大小")
    ap.add_argument("--full-size", type=int, default=6, help="完整批大小")
    args = ap.parse_args()
    
    # 加载候选
    with open(args.candidates, encoding='utf-8') as f:
        data = json.load(f)
    candidates = data if isinstance(data, list) else data.get("expressions", [])
    
    executor = ProbeBatchExecutor(args.campaign_dir, args.dataset, args.wave)
    result = executor.execute_probe_batch(candidates)
    
    # 输出结果
    print(f"\n{'='*60}")
    print(f"探针批模式结果 - Wave {args.wave} / {args.dataset}")
    print(f"{'='*60}")
    print(f"状态: {result['status']}")
    print(f"决策原因: {result['decision_reason']}")
    print(f"节省配额: {result['saved_quota']} 条")
    
    if result["full_results"]:
        print(f"\n完整批结果: {len(result['full_results'])} 条")
        
    # 保存结果
    out_path = os.path.join(args.campaign_dir, "cache", 
                           f"probe_wave{args.wave}_{args.dataset}.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存: {out_path}")
    
    # 退出码
    sys.exit(0 if result["status"] != "PROBE_DEAD" else 1)


if __name__ == "__main__":
    main()
