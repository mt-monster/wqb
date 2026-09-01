# -*- coding: utf-8 -*-
"""success_formula_engine.py - 成功配方推广引擎。

基于已验证的成功配方（如 58l2or1N），生成同族变体。

用法:
    python tools/success_formula_engine.py --formula IND-ANALYST-FUNDAMENTAL-WIN \
        --field-families data/field_families.json --output variants.json
"""
import argparse
import json
from typing import Dict, List, Any


class SuccessFormulaEngine:
    """成功配方推广引擎"""
    
    # 已验证成功配方库
    SUCCESS_FORMULAS = {
        "IND-ANALYST-FUNDAMENTAL-WIN": {
            "primary_family": "analyst_revision",
            "primary_field": "analyst_revision_percentile_score_long_4",
            "primary_weight": 0.6,
            "secondary_family": "fundamental",
            "secondary_field": "fnd86_earnings_score",
            "secondary_weight": 0.4,
            "structure": "add(multiply({pw}, {primary}), multiply({sw}, {secondary}))",
            "neutralization": "INDUSTRY",
            "preprocessing": "group_neutralize(quantile(ts_backfill({field}, 66)), industry)",
            "metrics": {
                "sharpe": 2.17,
                "fitness": 1.78,
                "two_year_sharpe": 2.53,
                "prod_correlation": 0.6617
            }
        }
    }
    
    # 字段族映射
    FIELD_FAMILIES = {
        "analyst_revision": [
            "analyst_revision_percentile_score_long_4",
            "analyst_revision_percentile_score_short_4",
            "analyst_revision_breadth_score_4",
            "analyst_revision_momentum_score_4"
        ],
        "fundamental": [
            "fnd86_earnings_score",
            "fnd86_value_score",
            "fnd86_quality_score",
            "fnd94_operating_margin",
            "fnd94_roe"
        ]
    }
    
    def __init__(self):
        pass
        
    def generate_variants(self, formula_id: str, 
                         field_families: Dict[str, List[str]] = None,
                         max_variants: int = 8) -> List[Dict[str, Any]]:
        """
        基于成功配方生成变体
        
        Args:
            formula_id: 成功配方 ID
            field_families: 字段族映射（可选，覆盖默认）
            max_variants: 最大变体数
            
        Returns:
            变体候选列表
        """
        if formula_id not in self.SUCCESS_FORMULAS:
            raise ValueError(f"未知配方: {formula_id}")
            
        formula = self.SUCCESS_FORMULAS[formula_id]
        families = field_families or self.FIELD_FAMILIES
        
        primary_fields = families.get(formula["primary_family"], [])
        secondary_fields = families.get(formula["secondary_family"], [])
        
        variants = []
        variant_id = 1
        
        # 生成主信号变体
        for pf in primary_fields[:3]:  # 最多 3 个主信号
            for sf in secondary_fields[:3]:  # 最多 3 个辅助信号
                if len(variants) >= max_variants:
                    break
                    
                # 构建表达式
                primary_expr = formula["preprocessing"].format(field=pf)
                secondary_expr = formula["preprocessing"].format(field=sf)
                
                expr = formula["structure"].format(
                    pw=formula["primary_weight"],
                    sw=formula["secondary_weight"],
                    primary=primary_expr,
                    secondary=secondary_expr
                )
                
                variants.append({
                    "id": f"V{variant_id}",
                    "expression": expr,
                    "primary_field": pf,
                    "secondary_field": sf,
                    "formula_source": formula_id,
                    "expected_sharpe": formula["metrics"]["sharpe"] * 0.9,  # 预期略低于原配方
                    "gem_generated": True,
                    "concept": f"{formula['primary_family']}+{formula['secondary_family']}",
                    "mechanism": "双信号加权混合"
                })
                variant_id += 1
                
        return variants
        
    def generate_diversity_variants(self, formula_id: str,
                                   neutralizations: List[str] = None,
                                   decays: List[int] = None) -> List[Dict[str, Any]]:
        """
        生成多样性变体（不同中性化/decay）
        
        用于七槽填槽的批间差异化
        """
        if formula_id not in self.SUCCESS_FORMULAS:
            raise ValueError(f"未知配方: {formula_id}")
            
        formula = self.SUCCESS_FORMULAS[formula_id]
        neut_list = neutralizations or ["INDUSTRY", "SUBINDUSTRY", "STATISTICAL"]
        decay_list = decays or [4, 6, 8]
        
        variants = []
        variant_id = 1
        
        for neut in neut_list:
            for decay in decay_list:
                # 修改预处理中的中性化
                primary_expr = formula["preprocessing"].format(
                    field=formula["primary_field"]
                ).replace("industry", neut.lower())
                
                secondary_expr = formula["preprocessing"].format(
                    field=formula["secondary_field"]
                ).replace("industry", neut.lower())
                
                expr = formula["structure"].format(
                    pw=formula["primary_weight"],
                    sw=formula["secondary_weight"],
                    primary=primary_expr,
                    secondary=secondary_expr
                )
                
                variants.append({
                    "id": f"D{variant_id}",
                    "expression": expr,
                    "neutralization": neut,
                    "decay": decay,
                    "formula_source": formula_id,
                    "batch_tag": f"neut_{neut}_decay_{decay}",
                    "gem_generated": True
                })
                variant_id += 1
                
        return variants


def main():
    ap = argparse.ArgumentParser(description="成功配方推广引擎")
    ap.add_argument("--formula", required=True, help="成功配方 ID")
    ap.add_argument("--field-families", help="字段族 JSON")
    ap.add_argument("--output", required=True, help="输出变体 JSON")
    ap.add_argument("--max-variants", type=int, default=8)
    ap.add_argument("--diversity-mode", action="store_true", 
                   help="生成多样性变体（不同中性化/decay）")
    args = ap.parse_args()
    
    # 加载字段族
    field_families = None
    if args.field_families:
        with open(args.field_families, encoding='utf-8') as f:
            field_families = json.load(f)
            
    # 生成变体
    engine = SuccessFormulaEngine()
    
    if args.diversity_mode:
        variants = engine.generate_diversity_variants(args.formula)
    else:
        variants = engine.generate_variants(args.formula, field_families, args.max_variants)
        
    # 输出
    print(f"\n{'='*60}")
    print(f"成功配方推广 - {args.formula}")
    print(f"{'='*60}")
    print(f"生成变体: {len(variants)} 条")
    
    for v in variants:
        print(f"\n{v['id']}:")
        print(f"  表达式: {v['expression'][:100]}...")
        if 'primary_field' in v:
            print(f"  主信号: {v['primary_field']}")
            print(f"  辅助信号: {v['secondary_field']}")
        if 'neutralization' in v:
            print(f"  中性化: {v['neutralization']}, decay={v['decay']}")
            
    # 保存
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(variants, f, ensure_ascii=False, indent=2)
    print(f"\n变体已保存: {args.output}")


if __name__ == "__main__":
    main()
