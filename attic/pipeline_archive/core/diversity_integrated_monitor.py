# -*- coding: utf-8 -*-
"""pipeline/core/diversity_integrated_monitor.py - 多样性评估集成监控器

将对比分析融入每 10 轮的多样性评估流程，实现：
  1. 每 10 轮回测后自动生成多样性评估报告
  2. 对比分析改进前后的效率指标
  3. 生成综合的多样性+纪律评估报告

用法:
  from pipeline.core.diversity_integrated_monitor import DiversityIntegratedMonitor
  
  monitor = DiversityIntegratedMonitor(
      region="KOR",
      ledger_path="tracking/KOR/kor_d1_campaign_state.json",
      monitor_dir="tracking/KOR/monitoring"
  )
  
  # 每 10 轮回测后调用
  report = monitor.generate_integrated_report(waves=10)
"""
import datetime
import json
import os
from typing import Dict, List, Optional

from .campaign_discipline import CampaignDiscipline
from .discipline_monitor import DisciplineMonitor
from .improvement_comparator import ImprovementComparator


class DiversityIntegratedMonitor:
    """多样性评估集成监控器"""
    
    def __init__(self, region: str, ledger_path: str, monitor_dir: str):
        """初始化
        
        Args:
            region: 区域代码（KOR/USA/EUR...）
            ledger_path: 台账文件路径
            monitor_dir: 监控数据目录
        """
        self.region = region
        self.ledger_path = ledger_path
        self.monitor_dir = monitor_dir
        
        # 初始化子模块
        self.discipline = CampaignDiscipline(ledger_path)
        self.monitor = DisciplineMonitor(monitor_dir)
        self.comparator = ImprovementComparator(ledger_path, monitor_dir)
    
    def generate_integrated_report(self, waves: int = 10) -> Dict:
        """生成综合的多样性+纪律评估报告
        
        Args:
            waves: 评估的波次数
            
        Returns:
            综合报告，包含多样性评估、纪律评估、对比分析
        """
        print(f"\n[integrated] 生成 {self.region} 区域 {waves} 轮综合评估报告...")
        
        # 1. 生成纪律监控报告
        print("[integrated] 1/3 生成纪律监控报告...")
        discipline_report = self.monitor.generate_report(waves=waves)
        
        # 2. 生成对比分析报告
        print("[integrated] 2/3 生成对比分析报告...")
        comparison_report = self.comparator.generate_comparison_report()
        
        # 3. 生成多样性评估（从台账中获取）
        print("[integrated] 3/3 生成多样性评估...")
        diversity_metrics = self._extract_diversity_metrics(waves)
        
        # 综合报告
        integrated_report = {
            "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "region": self.region,
            "waves_evaluated": waves,
            "discipline_report": discipline_report,
            "comparison_report": comparison_report,
            "diversity_metrics": diversity_metrics,
            "integrated_conclusion": self._generate_integrated_conclusion(
                discipline_report, comparison_report, diversity_metrics
            ),
        }
        
        # 保存综合报告
        report_path = os.path.join(
            self.monitor_dir,
            f"integrated_report_{self.region}_{datetime.date.today().isoformat()}.json"
        )
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(integrated_report, f, ensure_ascii=False, indent=1)
        
        # 打印综合报告
        self._print_integrated_report(integrated_report, report_path)
        
        return integrated_report
    
    def _extract_diversity_metrics(self, waves: int) -> Dict:
        """从台账中提取多样性指标"""
        try:
            with open(self.ledger_path, encoding="utf-8-sig") as f:
                ledger = json.load(f)
            
            # 获取最近的多样性历史
            diversity_history = ledger.get("diversity_history", [])
            recent = diversity_history[-waves:] if len(diversity_history) > waves else diversity_history
            
            if not recent:
                return {"status": "no_data"}
            
            # 计算平均多样性指标
            avg_metrics = {
                "operator_entropy": sum(d.get("metrics", {}).get("operator_entropy", 0) for d in recent) / len(recent),
                "coverage_rate": sum(d.get("metrics", {}).get("coverage_rate", 0) for d in recent) / len(recent),
                "novelty_score": sum(d.get("metrics", {}).get("novelty_score", 0) for d in recent) / len(recent),
                "structural_similarity": sum(d.get("metrics", {}).get("structural_similarity", 0) for d in recent) / len(recent),
            }
            
            return {
                "status": "ok",
                "waves_analyzed": len(recent),
                "avg_metrics": avg_metrics,
                "latest": recent[-1] if recent else None,
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _generate_integrated_conclusion(self, discipline_report: Dict, 
                                        comparison_report: Optional[Dict],
                                        diversity_metrics: Dict) -> List[str]:
        """生成综合结论"""
        conclusions = []
        
        # 纪律评估结论
        if discipline_report and "summary" in discipline_report:
            summary = discipline_report["summary"]
            conclusions.append(f"纪律评估: 候选率 {summary.get('candidate_rate', 0)*100:.1f}%, "
                             f"切换触发 {summary.get('switch_triggered_count', 0)} 次")
        
        # 对比分析结论
        if comparison_report and "improvement" in comparison_report:
            imp = comparison_report["improvement"]
            if imp.get("candidate_rate_change", 0) > 10:
                conclusions.append(f"改进效果: 候选率提升 {imp['candidate_rate_change']:.1f}%")
            if imp.get("dead_classification_change", 0) > 10:
                conclusions.append(f"判死及时性: DEAD 分类比例提升 {imp['dead_classification_change']:.1f}%")
        
        # 多样性评估结论
        if diversity_metrics.get("status") == "ok":
            avg = diversity_metrics["avg_metrics"]
            conclusions.append(f"多样性评估: 算子熵 {avg['operator_entropy']:.2f}, "
                             f"覆盖率 {avg['coverage_rate']:.1%}, "
                             f"新颖度 {avg['novelty_score']:.1%}")
            
            # 多样性健康度判断
            if avg['operator_entropy'] < 2.0:
                conclusions.append("多样性警告: 算子熵偏低，建议增加算子多样性")
            if avg['coverage_rate'] < 0.5:
                conclusions.append("多样性警告: 覆盖率偏低，建议扩大字段覆盖")
            if avg['novelty_score'] < 0.8:
                conclusions.append("多样性警告: 新颖度偏低，建议引入新骨架")
        
        return conclusions
    
    def _print_integrated_report(self, report: Dict, report_path: str):
        """打印综合报告"""
        print("\n" + "=" * 70)
        print(f"{self.region} 区域 {report['waves_evaluated']} 轮综合评估报告")
        print("=" * 70)
        
        # 纪律评估
        if report.get("discipline_report") and "summary" in report["discipline_report"]:
            summary = report["discipline_report"]["summary"]
            print(f"\n【纪律评估】")
            print(f"  监控波次数: {summary['total_waves']}")
            print(f"  总表达式数: {summary['total_exprs']}")
            print(f"  候选率: {summary['candidate_rate']*100:.1f}%")
            print(f"  切换触发次数: {summary['switch_triggered_count']}")
        
        # 对比分析
        if report.get("comparison_report") and "improvement" in report["comparison_report"]:
            imp = report["comparison_report"]["improvement"]
            print(f"\n【改进效果】")
            if imp.get("candidate_rate_change"):
                print(f"  候选率变化: {imp['candidate_rate_change']:+.1f}%")
            if imp.get("dead_classification_change"):
                print(f"  DEAD 分类变化: {imp['dead_classification_change']:+.1f}%")
        
        # 多样性评估
        if report.get("diversity_metrics", {}).get("status") == "ok":
            avg = report["diversity_metrics"]["avg_metrics"]
            print(f"\n【多样性评估】")
            print(f"  算子熵: {avg['operator_entropy']:.3f}")
            print(f"  覆盖率: {avg['coverage_rate']:.2%}")
            print(f"  新颖度: {avg['novelty_score']:.2%}")
            print(f"  结构相似度: {avg['structural_similarity']:.2%}")
        
        # 综合结论
        print(f"\n【综合结论】")
        for c in report.get("integrated_conclusion", []):
            print(f"  - {c}")
        
        print("=" * 70)
        print(f"报告已保存: {report_path}")
