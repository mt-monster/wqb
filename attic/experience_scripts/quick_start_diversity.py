#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quick_start_diversity.py - 多样性增强系统快速启动脚本

提供简单的命令行接口来快速使用多样性增强功能
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gen_diverse_expressions import DiverseExpressionGenerator
from batch_diversity_processor import BatchDiversityProcessor
from wqb.expression.diversity_enhancer import analyze_diversity, enhance_expressions


def quick_generate(region="USA", universe="TOP3000", dataset="fnd6", count=20):
    """快速生成多样性表达式"""
    print(f"🚀 快速生成 {count} 个多样性表达式")
    print(f"   区域: {region}/{universe}")
    print(f"   数据集: {dataset}")
    print()
    
    generator = DiverseExpressionGenerator(region, universe)
    
    # 构建字段列表
    fields = [f"{dataset}_FIELD_{i}" for i in range(1, 6)]  # 示例字段
    
    # 生成表达式
    results = generator.generate_with_diversity(
        fields=fields,
        count=count,
        diversity_weight=0.4  # 较高的多样性权重
    )
    
    print(f"\n✅ 生成完成！")
    print(f"\n📊 多样性指标:")
    report = generator.enhancer.get_diversity_report()
    
    if 'current_metrics' in report:
        metrics = report['current_metrics']
        print(f"   算子熵: {metrics['operator_entropy']:.3f}")
        print(f"   覆盖率: {metrics['coverage_rate']:.2%}")
        print(f"   新颖度: {metrics['novelty_score']:.2%}")
        print(f"   唯一结构: {metrics['unique_structures']}")
    
    print(f"\n🔝 Top 5 表达式:")
    for i, r in enumerate(results[:5], 1):
        print(f"{i}. [{r['score']:.1f}分] {r['expression']}")
        if r.get('recommendations'):
            print(f"   💡 {r['recommendations'][0]}")
    
    return results


def quick_analyze(file_path):
    """快速分析现有表达式的多样性"""
    print(f"🔍 分析文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取表达式
    if isinstance(data, list):
        expressions = data
    elif isinstance(data, dict):
        expressions = data.get('alpha_expressions', []) or \
                     data.get('expressions', []) or \
                     data.get('exprs', [])
    else:
        print("❌ 无法识别的文件格式")
        return
    
    print(f"   找到 {len(expressions)} 个表达式")
    print()
    
    # 分析多样性
    report = analyze_diversity(expressions)
    
    print("📊 多样性分析结果:")
    if 'current_metrics' in report:
        metrics = report['current_metrics']
        print(f"   算子熵: {metrics['operator_entropy']:.3f} {'✅' if metrics['operator_entropy'] > 2.0 else '⚠️'}")
        print(f"   覆盖率: {metrics['coverage_rate']:.2%} {'✅' if metrics['coverage_rate'] > 0.5 else '⚠️'}")
        print(f"   新颖度: {metrics['novelty_score']:.2%} {'✅' if metrics['novelty_score'] > 0.8 else '⚠️'}")
        print(f"   结构相似度: {metrics['structural_similarity']:.2%} {'✅' if metrics['structural_similarity'] < 0.7 else '⚠️'}")
    
    if 'recommendations' in report:
        print(f"\n💡 改进建议:")
        for rec in report['recommendations']:
            print(f"   • {rec}")
    
    return report


def quick_enhance(input_file, output_file=None):
    """快速增强现有表达式文件的多样性"""
    print(f"🔧 增强文件: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取表达式
    if isinstance(data, list):
        expressions = data
    elif isinstance(data, dict):
        expressions = data.get('alpha_expressions', []) or \
                     data.get('expressions', []) or \
                     data.get('exprs', [])
    else:
        print("❌ 无法识别的文件格式")
        return
    
    print(f"   原始表达式: {len(expressions)} 个")
    
    # 增强多样性
    enhanced, report = enhance_expressions(expressions)
    
    print(f"   增强后表达式: {len(enhanced)} 个")
    print()
    
    print("📊 增强效果:")
    if 'current_metrics' in report:
        metrics = report['current_metrics']
        print(f"   算子熵: {metrics['operator_entropy']:.3f}")
        print(f"   覆盖率: {metrics['coverage_rate']:.2%}")
        print(f"   新颖度: {metrics['novelty_score']:.2%}")
    
    # 保存结果
    if output_file:
        output_data = {
            'original_count': len(expressions),
            'enhanced_count': len(enhanced),
            'expressions': enhanced,
            'diversity_report': report
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 已保存到: {output_file}")
    
    return enhanced, report


def main():
    parser = argparse.ArgumentParser(
        description="多样性增强系统快速启动",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s generate --count 30                    # 快速生成30个表达式
  %(prog)s analyze tracking/USA/batch01.json      # 分析现有文件
  %(prog)s enhance input.json -o output.json      # 增强并保存
  %(prog)s monitor                                # 运行监控
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # generate 命令
    gen_parser = subparsers.add_parser('generate', help='生成多样性表达式')
    gen_parser.add_argument('--region', default='USA', help='区域 (默认: USA)')
    gen_parser.add_argument('--universe', default='TOP3000', help='股票池 (默认: TOP3000)')
    gen_parser.add_argument('--dataset', default='fnd6', help='数据集 (默认: fnd6)')
    gen_parser.add_argument('--count', type=int, default=20, help='生成数量 (默认: 20)')
    
    # analyze 命令
    ana_parser = subparsers.add_parser('analyze', help='分析表达式多样性')
    ana_parser.add_argument('file', help='要分析的JSON文件')
    
    # enhance 命令
    enh_parser = subparsers.add_parser('enhance', help='增强表达式多样性')
    enh_parser.add_argument('input', help='输入JSON文件')
    enh_parser.add_argument('-o', '--output', help='输出JSON文件')
    
    # monitor 命令
    mon_parser = subparsers.add_parser('monitor', help='运行多样性监控')
    mon_parser.add_argument('--tracking-dir', default='tracking', help='跟踪目录')
    
    args = parser.parse_args()
    
    if args.command == 'generate':
        quick_generate(args.region, args.universe, args.dataset, args.count)
    
    elif args.command == 'analyze':
        quick_analyze(args.file)
    
    elif args.command == 'enhance':
        quick_enhance(args.input, args.output)
    
    elif args.command == 'monitor':
        processor = BatchDiversityProcessor(args.tracking_dir)
        
        print("🔄 运行多样性监控...")
        results = processor.process_batch_files()
        
        if results['files_processed'] > 0:
            print(f"\n📈 处理了 {results['files_processed']} 个文件")
            
            # 生成报告
            report = processor.generate_trend_report()
            print(report)
            
            # 策略调整建议
            adjustments = processor.adaptive_strategy_adjustment()
            if adjustments.get('focus_areas'):
                print("\n🎯 建议关注:")
                for area in adjustments['focus_areas']:
                    print(f"   • {area}")
        else:
            print("❌ 未找到需要处理的文件")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
