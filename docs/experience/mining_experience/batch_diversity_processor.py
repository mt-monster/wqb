#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_diversity_processor.py - 批量多样性处理和监控系统

用于：
1. 批量处理现有表达式，提升多样性
2. 监控多样性趋势
3. 生成多样性报告
4. 自适应调整生成策略
"""

import argparse
import json
import sys
import glob
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wqb.expression.diversity_enhancer import (
    DiversityEnhancer,
    DiversityMonitor,
    analyze_diversity,
    enhance_expressions
)


class BatchDiversityProcessor:
    """批量多样性处理器"""
    
    def __init__(self, tracking_dir: str = "tracking"):
        self.tracking_dir = Path(tracking_dir)
        self.enhancer = DiversityEnhancer()
        self.monitor = DiversityMonitor()
        self.history_file = self.tracking_dir / "diversity_history.json"
        self.report_dir = self.tracking_dir / "diversity_reports"
        self.report_dir.mkdir(exist_ok=True)
        
        # 加载历史数据
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """加载历史多样性数据"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_history(self):
        """保存历史数据"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
    
    def process_batch_files(self, pattern: str = "**/*batch*.json") -> Dict[str, Any]:
        """处理批量文件"""
        files = list(self.tracking_dir.glob(pattern))
        print(f"找到 {len(files)} 个批次文件")
        
        all_expressions = []
        file_results = {}
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 提取表达式
                expressions = []
                if isinstance(data, dict):
                    expressions = data.get('alpha_expressions', []) or \
                                 data.get('expressions', []) or \
                                 data.get('exprs', [])
                elif isinstance(data, list):
                    expressions = data
                
                if expressions:
                    # 分析多样性
                    metrics = self.monitor.calculate_metrics(expressions)
                    
                    # 增强多样性
                    enhanced, report = enhance_expressions(expressions)
                    
                    file_results[str(file_path)] = {
                        'original_count': len(expressions),
                        'enhanced_count': len(enhanced),
                        'metrics': {
                            'operator_entropy': metrics.operator_entropy,
                            'coverage_rate': metrics.coverage_rate,
                            'novelty_score': metrics.novelty_score,
                            'unique_structures': metrics.unique_structures
                        },
                        'report': report
                    }
                    
                    all_expressions.extend(expressions)
                    
                    print(f"处理 {file_path.name}: "
                          f"熵={metrics.operator_entropy:.2f}, "
                          f"覆盖率={metrics.coverage_rate:.2%}, "
                          f"新颖度={metrics.novelty_score:.2%}")
                    
            except Exception as e:
                print(f"处理 {file_path} 时出错: {e}")
        
        # 整体分析
        if all_expressions:
            overall_metrics = self.monitor.calculate_metrics(all_expressions)
            
            # 记录历史
            self.history.append({
                'timestamp': datetime.now().isoformat(),
                'total_expressions': len(all_expressions),
                'unique_expressions': len(set(all_expressions)),
                'operator_entropy': overall_metrics.operator_entropy,
                'coverage_rate': overall_metrics.coverage_rate,
                'novelty_score': overall_metrics.novelty_score,
                'skeleton_distribution': overall_metrics.skeleton_distribution,
                'operator_distribution': overall_metrics.operator_distribution
            })
            
            self._save_history()
            
            return {
                'files_processed': len(file_results),
                'total_expressions': len(all_expressions),
                'overall_metrics': overall_metrics,
                'file_results': file_results
            }
        
        return {'files_processed': 0, 'total_expressions': 0}
    
    def generate_trend_report(self) -> str:
        """生成多样性趋势报告"""
        if not self.history:
            return "无历史数据"
        
        df = pd.DataFrame(self.history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('多样性趋势分析', fontsize=16)
        
        # 1. 算子熵趋势
        ax = axes[0, 0]
        ax.plot(df['timestamp'], df['operator_entropy'], marker='o')
        ax.set_title('算子熵趋势')
        ax.set_xlabel('时间')
        ax.set_ylabel('熵值')
        ax.grid(True)
        
        # 2. 覆盖率趋势
        ax = axes[0, 1]
        ax.plot(df['timestamp'], df['coverage_rate'], marker='s', color='green')
        ax.set_title('算子覆盖率趋势')
        ax.set_xlabel('时间')
        ax.set_ylabel('覆盖率')
        ax.grid(True)
        
        # 3. 新颖度趋势
        ax = axes[1, 0]
        ax.plot(df['timestamp'], df['novelty_score'], marker='^', color='orange')
        ax.set_title('表达式新颖度趋势')
        ax.set_xlabel('时间')
        ax.set_ylabel('新颖度')
        ax.grid(True)
        
        # 4. 表达式数量
        ax = axes[1, 1]
        ax.bar(df['timestamp'], df['total_expressions'], alpha=0.7, label='总数')
        ax.bar(df['timestamp'], df['unique_expressions'], alpha=0.7, label='唯一')
        ax.set_title('表达式数量统计')
        ax.set_xlabel('时间')
        ax.set_ylabel('数量')
        ax.legend()
        ax.grid(True)
        
        plt.tight_layout()
        
        # 保存图表
        chart_path = self.report_dir / f"diversity_trend_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        # 生成文本报告
        report_lines = [
            "=" * 60,
            "多样性趋势报告",
            "=" * 60,
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"历史记录数: {len(self.history)}",
            "",
            "最新指标:",
            "-" * 40
        ]
        
        if self.history:
            latest = self.history[-1]
            report_lines.extend([
                f"  算子熵: {latest['operator_entropy']:.3f}",
                f"  覆盖率: {latest['coverage_rate']:.2%}",
                f"  新颖度: {latest['novelty_score']:.2%}",
                f"  总表达式: {latest['total_expressions']}",
                f"  唯一表达式: {latest['unique_expressions']}",
                ""
            ])
            
            # 趋势分析
            if len(self.history) > 1:
                prev = self.history[-2]
                entropy_change = latest['operator_entropy'] - prev['operator_entropy']
                coverage_change = latest['coverage_rate'] - prev['coverage_rate']
                
                report_lines.extend([
                    "趋势变化:",
                    "-" * 40,
                    f"  熵变化: {entropy_change:+.3f} {'↑' if entropy_change > 0 else '↓'}",
                    f"  覆盖率变化: {coverage_change:+.2%} {'↑' if coverage_change > 0 else '↓'}",
                    ""
                ])
            
            # 骨架分布
            if 'skeleton_distribution' in latest:
                report_lines.extend([
                    "骨架分布:",
                    "-" * 40
                ])
                for skeleton, count in latest['skeleton_distribution'].items():
                    report_lines.append(f"  {skeleton}: {count}")
                report_lines.append("")
            
            # 改进建议
            report_lines.extend([
                "改进建议:",
                "-" * 40
            ])
            
            if latest['operator_entropy'] < 2.0:
                report_lines.append("  • 算子多样性不足，建议引入更多算子类别")
            if latest['coverage_rate'] < 0.5:
                report_lines.append("  • 算子覆盖率不足50%，需要探索未使用的算子")
            if latest['novelty_score'] < 0.8:
                report_lines.append("  • 表达式重复度过高，建议增加变异率")
            
            # 找出使用最少的算子
            if 'operator_distribution' in latest:
                op_dist = latest['operator_distribution']
                if op_dist:
                    min_ops = sorted(op_dist.items(), key=lambda x: x[1])[:5]
                    report_lines.append(f"  • 使用最少的算子: {', '.join([op for op, _ in min_ops])}")
        
        report_lines.extend([
            "",
            f"图表已保存: {chart_path}",
            "=" * 60
        ])
        
        report_text = "\n".join(report_lines)
        
        # 保存文本报告
        report_path = self.report_dir / f"diversity_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        return report_text
    
    def adaptive_strategy_adjustment(self) -> Dict[str, Any]:
        """自适应策略调整"""
        if not self.history or len(self.history) < 2:
            return {"status": "insufficient_data"}
        
        latest = self.history[-1]
        adjustments = {
            "mutation_rate": 0.3,  # 默认变异率
            "exploration_rate": 0.2,  # 默认探索率
            "quota_enforcement": False,  # 是否强制配额
            "focus_areas": []
        }
        
        # 根据熵值调整变异率
        if latest['operator_entropy'] < 1.5:
            adjustments['mutation_rate'] = 0.5
            adjustments['focus_areas'].append("增加算子多样性")
        elif latest['operator_entropy'] < 2.0:
            adjustments['mutation_rate'] = 0.4
        
        # 根据覆盖率调整探索率
        if latest['coverage_rate'] < 0.3:
            adjustments['exploration_rate'] = 0.4
            adjustments['quota_enforcement'] = True
            adjustments['focus_areas'].append("强制算子配额")
        elif latest['coverage_rate'] < 0.5:
            adjustments['exploration_rate'] = 0.3
        
        # 根据新颖度调整
        if latest['novelty_score'] < 0.7:
            adjustments['mutation_rate'] = min(adjustments['mutation_rate'] + 0.1, 0.7)
            adjustments['focus_areas'].append("增加结构变异")
        
        # 分析骨架分布
        if 'skeleton_distribution' in latest:
            skeleton_dist = latest['skeleton_distribution']
            if skeleton_dist:
                max_skeleton = max(skeleton_dist.values())
                total = sum(skeleton_dist.values())
                if max_skeleton / total > 0.5:
                    adjustments['focus_areas'].append(f"减少对 '{max(skeleton_dist, key=skeleton_dist.get)}' 骨架的依赖")
        
        return adjustments


def main():
    parser = argparse.ArgumentParser(
        description="批量多样性处理和监控系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --process --pattern "**/*batch*.json"
  %(prog)s --report
  %(prog)s --adjust-strategy
  %(prog)s --full-cycle
        """
    )
    
    parser.add_argument("--tracking-dir", default="tracking",
                        help="跟踪目录路径 (默认: tracking)")
    parser.add_argument("--process", action="store_true",
                        help="处理批量文件")
    parser.add_argument("--pattern", default="**/*batch*.json",
                        help="文件匹配模式 (默认: **/*batch*.json)")
    parser.add_argument("--report", action="store_true",
                        help="生成趋势报告")
    parser.add_argument("--adjust-strategy", action="store_true",
                        help="生成自适应策略调整建议")
    parser.add_argument("--full-cycle", action="store_true",
                        help="执行完整周期（处理+报告+调整）")
    
    args = parser.parse_args()
    
    processor = BatchDiversityProcessor(args.tracking_dir)
    
    if args.full_cycle:
        # 完整周期
        print("=== 执行完整多样性处理周期 ===\n")
        
        # 1. 处理批量文件
        print("步骤 1: 处理批量文件")
        results = processor.process_batch_files(args.pattern)
        print(f"处理了 {results['files_processed']} 个文件，"
              f"共 {results['total_expressions']} 个表达式\n")
        
        # 2. 生成报告
        print("步骤 2: 生成趋势报告")
        report = processor.generate_trend_report()
        print(report)
        print()
        
        # 3. 策略调整
        print("步骤 3: 生成策略调整建议")
        adjustments = processor.adaptive_strategy_adjustment()
        print(json.dumps(adjustments, indent=2, ensure_ascii=False))
        
    else:
        # 单独执行
        if args.process:
            results = processor.process_batch_files(args.pattern)
            print(f"\n处理完成: {results['files_processed']} 个文件，"
                  f"{results['total_expressions']} 个表达式")
            
            if 'overall_metrics' in results:
                metrics = results['overall_metrics']
                print(f"\n整体指标:")
                print(f"  算子熵: {metrics.operator_entropy:.3f}")
                print(f"  覆盖率: {metrics.coverage_rate:.2%}")
                print(f"  新颖度: {metrics.novelty_score:.2%}")
        
        if args.report:
            report = processor.generate_trend_report()
            print(report)
        
        if args.adjust_strategy:
            adjustments = processor.adaptive_strategy_adjustment()
            print("自适应策略调整建议:")
            print(json.dumps(adjustments, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
