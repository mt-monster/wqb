#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_diverse_expressions.py - 带多样性增强的表达式生成器

集成多样性增强系统到现有的启发式生成器中，提供：
1. 算子配额强制轮换
2. 结构变异增强
3. 实时多样性监控
4. 自适应探索率调整
"""

import argparse
import json
import sys
import random
from pathlib import Path
from typing import List, Dict, Any

# 添加项目路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mining_experience.heuristic_engine import (
    HeuristicEngine,
    get_engine,
    get_preferred_templates,
    get_region_recommendations,
    score_expression,
)
from wqb.expression.diversity_enhancer import (
    DiversityEnhancer,
    OperatorQuotaManager,
    StructuralMutationEngine,
    DiversityMonitor,
    enhance_expressions,
    analyze_diversity
)


class DiverseExpressionGenerator:
    """带多样性增强的表达式生成器"""
    
    def __init__(self, region: str = "USA", universe: str = "TOP3000", delay: int = 1):
        self.region = region
        self.universe = universe
        self.delay = delay
        self.engine = get_engine()
        self.enhancer = DiversityEnhancer()
        self.state_file = Path(f"diversity_state_{region}_{universe}.json")
        
        # 加载历史状态
        if self.state_file.exists():
            self.enhancer.load_state(str(self.state_file))
    
    def generate_with_diversity(self, fields: List[str], count: int = 50, 
                               diversity_weight: float = 0.3) -> List[Dict[str, Any]]:
        """
        生成具有多样性保证的表达式
        
        Args:
            fields: 字段列表
            count: 生成数量
            diversity_weight: 多样性权重 (0-1)
        """
        print(f"=== 多样性增强生成模式 ===")
        print(f"Region: {self.region}/{self.universe}/D{self.delay}")
        print(f"目标数量: {count}, 多样性权重: {diversity_weight}")
        print()
        
        # 1. 获取推荐模板
        templates = get_preferred_templates(self.region, self.universe)
        print(f"推荐模板: {templates[:5]}...")
        
        # 2. 分析当前多样性状态
        if hasattr(self.enhancer, 'monitor') and self.enhancer.monitor.history:
            last_metrics = self.enhancer.monitor.history[-1]
            print(f"历史多样性指标:")
            print(f"  - 算子熵: {last_metrics.operator_entropy:.3f}")
            print(f"  - 覆盖率: {last_metrics.coverage_rate:.3f}")
            print(f"  - 新颖度: {last_metrics.novelty_score:.3f}")
            print()
        
        # 3. 生成基础表达式
        base_expressions = []
        
        # 3a. 使用模板生成
        template_exprs = self._generate_from_templates(fields, templates, count // 2)
        base_expressions.extend(template_exprs)
        
        # 3b. 使用配额管理器生成（确保算子覆盖）
        quota_exprs = self._generate_with_quota(fields, count // 4)
        base_expressions.extend(quota_exprs)
        
        # 3c. 使用结构变异生成
        mutation_exprs = self._generate_with_mutation(template_exprs[:10], count // 4)
        base_expressions.extend(mutation_exprs)
        
        # 4. 应用多样性增强
        print(f"应用多样性增强...")
        enhanced_exprs = self.enhancer.enhance_diversity(
            [e['expression'] for e in base_expressions],
            target_count=count
        )
        
        # 5. 评分和排序
        results = []
        for expr in enhanced_exprs:
            score_info = score_expression(expr, self.region, self.universe)
            
            # 计算多样性分数
            diversity_score = self._calculate_diversity_score(expr)
            
            # 综合分数
            final_score = (1 - diversity_weight) * score_info['total_score'] + \
                         diversity_weight * diversity_score
            
            results.append({
                'expression': expr,
                'score': final_score,
                'heuristic_score': score_info['total_score'],
                'diversity_score': diversity_score,
                'risk': score_info['os_decay_risk'],
                'template': score_info.get('template_match', 'custom'),
                'recommendations': score_info.get('recommendations', [])
            })
        
        # 按综合分数排序
        results.sort(key=lambda x: -x['score'])
        
        # 6. 保存状态
        self.enhancer.save_state(str(self.state_file))
        
        # 7. 生成多样性报告
        diversity_report = self.enhancer.get_diversity_report()
        
        print(f"\n=== 多样性报告 ===")
        print(json.dumps(diversity_report, indent=2, ensure_ascii=False))
        
        return results[:count]
    
    def _generate_from_templates(self, fields: List[str], templates: List[str], 
                                 count: int) -> List[Dict[str, Any]]:
        """使用模板生成表达式"""
        results = []
        windows = self.engine._rules.get("window_recommendations", {})
        
        for field in fields:
            for template in templates:
                if len(results) >= count:
                    break
                expr = self.engine._apply_template(field, template, windows)
                if expr:
                    results.append({
                        'expression': expr,
                        'template': template,
                        'field': field
                    })
        
        return results
    
    def _generate_with_quota(self, fields: List[str], count: int) -> List[Dict[str, Any]]:
        """使用算子配额生成表达式"""
        quota_manager = OperatorQuotaManager()
        results = []
        
        # 获取建议的算子
        suggested_ops = quota_manager.suggest_next_operators(count=10)
        print(f"配额建议算子: {suggested_ops[:5]}...")
        
        # 为每个建议算子生成表达式
        for op in suggested_ops:
            if len(results) >= count:
                break
                
            field = random.choice(fields)
            
            # 根据算子类型生成表达式
            if op.startswith('ts_'):
                window = random.choice([20, 60, 120, 250])
                expr = f"{op}({field}, {window})"
            elif op.startswith('group_'):
                group = random.choice(['sector', 'industry', 'subindustry'])
                expr = f"{op}({field}, {group})"
            elif op.startswith('vec_'):
                expr = f"{op}({field})"
            elif op in ['add', 'subtract', 'multiply', 'divide']:
                # 需要两个参数
                field2 = random.choice(fields)
                expr = f"{op}({field}, {field2})"
            else:
                expr = f"{op}({field})"
            
            # 包装一层
            expr = f"rank({expr})"
            
            results.append({
                'expression': expr,
                'template': f'quota_{op}',
                'field': field
            })
        
        return results
    
    def _generate_with_mutation(self, base_expressions: List[Dict[str, Any]], 
                                count: int) -> List[Dict[str, Any]]:
        """使用结构变异生成表达式"""
        mutation_engine = StructuralMutationEngine()
        results = []
        
        for base in base_expressions:
            if len(results) >= count:
                break
            
            # 应用1-3个变异
            expr = base['expression']
            num_mutations = random.randint(1, 3)
            
            for _ in range(num_mutations):
                expr = mutation_engine.mutate_expression(expr)
            
            results.append({
                'expression': expr,
                'template': f"mutated_{base['template']}",
                'field': base['field'],
                'mutations': num_mutations
            })
        
        return results
    
    def _calculate_diversity_score(self, expression: str) -> float:
        """计算表达式的多样性分数"""
        score = 50.0
        
        # 检查算子多样性
        ops = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', expression)
        unique_ops = len(set(ops))
        score += unique_ops * 5
        
        # 检查结构复杂度
        depth = expression.count('(')
        if 2 <= depth <= 4:
            score += 20
        elif depth > 4:
            score += 10
        
        # 检查是否包含未充分使用的算子类别
        quota_manager = OperatorQuotaManager()
        categories_used = set()
        for op in ops:
            category = quota_manager.get_operator_category(op)
            categories_used.add(category)
        
        score += len(categories_used) * 10
        
        # 检查是否有创新组合
        if 'vec_' in expression and 'ts_' in expression:
            score += 15  # 向量+时间序列组合
        if 'group_' in expression and 'ts_' in expression:
            score += 10  # 分组+时间序列组合
        if 'trade_when' in expression or 'if_else' in expression:
            score += 20  # 条件逻辑
        
        return min(score, 100)  # 最高100分


def main():
    parser = argparse.ArgumentParser(
        description="多样性增强的alpha表达式生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --region USA --universe TOP3000 --datasets fnd6 --count 50
  %(prog)s --region USA --universe TOP3000 --datasets mdl177 --count 100 --diversity-weight 0.5
  %(prog)s --analyze-only --input expressions.json
        """
    )
    
    parser.add_argument("--region", default="USA", help="区域代码 (默认: USA)")
    parser.add_argument("--universe", default="TOP3000", help="股票池 (默认: TOP3000)")
    parser.add_argument("--delay", type=int, default=1, help="数据延迟 (默认: 1)")
    parser.add_argument("--datasets", nargs="+", default=["fnd6"],
                        help="数据集前缀 (默认: fnd6)")
    parser.add_argument("--count", type=int, default=50, help="生成表达式数量 (默认: 50)")
    parser.add_argument("--diversity-weight", type=float, default=0.3,
                        help="多样性权重 0-1 (默认: 0.3)")
    parser.add_argument("--output", "-o", help="输出文件路径 (JSON)")
    parser.add_argument("--analyze-only", action="store_true",
                        help="仅分析现有表达式的多样性")
    parser.add_argument("--input", help="输入表达式文件 (用于分析)")
    
    args = parser.parse_args()
    
    if args.analyze_only:
        # 仅分析模式
        if not args.input:
            print("错误: --analyze-only 需要 --input 指定输入文件")
            return
        
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
            expressions = data if isinstance(data, list) else data.get('expressions', [])
        
        print(f"分析 {len(expressions)} 个表达式的多样性...")
        report = analyze_diversity(expressions)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        
    else:
        # 生成模式
        generator = DiverseExpressionGenerator(args.region, args.universe, args.delay)
        
        # 构建字段列表
        recs = get_region_recommendations(args.region, args.universe)
        fields = []
        for ds_prefix in args.datasets:
            src_info = recs.get("data_sources", {}).get(ds_prefix, {})
            if src_info.get("best_fields"):
                for f in src_info["best_fields"]:
                    fields.append(f"{ds_prefix}_{f}" if not f.startswith(ds_prefix) else f)
            else:
                fields.append(f"{ds_prefix}_FIELD")
        
        # 生成表达式
        results = generator.generate_with_diversity(
            fields, 
            count=args.count,
            diversity_weight=args.diversity_weight
        )
        
        # 输出结果
        if args.output:
            output_data = {
                'metadata': {
                    'region': args.region,
                    'universe': args.universe,
                    'delay': args.delay,
                    'datasets': args.datasets,
                    'count': len(results),
                    'diversity_weight': args.diversity_weight
                },
                'expressions': results,
                'diversity_report': generator.enhancer.get_diversity_report()
            }
            
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"\n已保存 {len(results)} 个表达式到 {args.output}")
        else:
            print(f"\n=== 生成的表达式 (Top {min(10, len(results))}) ===")
            print(f"{'#':>3} {'Score':>6} {'Div':>6} {'Risk':>6} {'Template':<25} Expression")
            print("-" * 120)
            for i, r in enumerate(results[:10]):
                print(f"{i+1:>3} {r['score']:>6.1f} {r['diversity_score']:>6.1f} "
                      f"{r['risk']:>6} {r['template']:<25} {r['expression'][:60]}")


if __name__ == "__main__":
    import re  # 需要在这里导入，因为_calculate_diversity_score使用了
    main()
