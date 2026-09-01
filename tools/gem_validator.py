# -*- coding: utf-8 -*-
"""gem_validator.py - GEM 候选池强制校验。

确保 S2 候选池来自 brain-makeSomeGem 管道，而非手写。

用法:
    python tools/gem_validator.py --candidates candidates.json --wave 129
"""
import argparse
import json
import sys
from typing import Dict, List, Any


class GEMValidator:
    """GEM 候选池校验器"""
    
    # GEM 候选必须包含的元数据字段
    GEM_REQUIRED_FIELDS = ["concept", "mechanism", "field_source", "gem_generated"]
    
    def __init__(self):
        pass
        
    def is_gem_generated(self, candidate: Dict) -> bool:
        """
        判断候选是否来自 GEM 管道
        
        GEM 候选特征：
        1. 包含 concept/mechanism/field_source 元数据
        2. 或包含 gem_generated=True 标记
        3. 或表达式结构符合 GEM 模板特征
        """
        # 检查元数据
        if candidate.get("gem_generated") is True:
            return True
            
        # 检查必需字段
        has_metadata = all(f in candidate for f in ["concept", "mechanism"])
        if has_metadata:
            return True
            
        # 检查表达式结构（GEM 模板特征）
        expr = candidate.get("expression", "")
        gem_patterns = [
            "group_neutralize",  # GEM 常用中性化
            "ts_backfill",       # GEM 常用预处理
            "quantile",          # GEM 常用分位数
        ]
        pattern_count = sum(1 for p in gem_patterns if p in expr)
        
        # 如果包含 2+ GEM 特征，认为是 GEM 生成
        return pattern_count >= 2
        
    def validate_wave(self, candidates: List[Dict], wave: int, 
                      min_gem_ratio: float = 0.8) -> Dict[str, Any]:
        """
        校验波次候选池
        
        Args:
            candidates: 候选列表
            wave: 波次编号
            min_gem_ratio: 最小 GEM 占比（默认 80%）
            
        Returns:
            {
                "wave": int,
                "total": int,
                "gem_count": int,
                "gem_ratio": float,
                "pass": bool,
                "non_gem_candidates": [...],
                "error": str or None
            }
        """
        total = len(candidates)
        gem_count = 0
        non_gem = []
        
        for c in candidates:
            if self.is_gem_generated(c):
                gem_count += 1
            else:
                non_gem.append({
                    "id": c.get("id"),
                    "expression": c.get("expression", "")[:100]
                })
                
        gem_ratio = gem_count / total if total > 0 else 0
        passed = gem_ratio >= min_gem_ratio
        
        result = {
            "wave": wave,
            "total": total,
            "gem_count": gem_count,
            "gem_ratio": round(gem_ratio, 3),
            "min_required": min_gem_ratio,
            "pass": passed,
            "non_gem_candidates": non_gem,
            "error": None
        }
        
        if not passed:
            result["error"] = (
                f"Wave {wave}: GEM 候选占比不足 "
                f"({gem_count}/{total} = {gem_ratio:.1%} < {min_gem_ratio:.0%})"
            )
            
        return result


def main():
    ap = argparse.ArgumentParser(description="GEM 候选池强制校验")
    ap.add_argument("--candidates", required=True, help="候选表达式 JSON")
    ap.add_argument("--wave", type=int, required=True)
    ap.add_argument("--min-gem-ratio", type=float, default=0.8)
    args = ap.parse_args()
    
    # 加载候选
    with open(args.candidates, encoding='utf-8') as f:
        data = json.load(f)
    candidates = data if isinstance(data, list) else data.get("expressions", [])
    
    # 校验
    validator = GEMValidator()
    result = validator.validate_wave(candidates, args.wave, args.min_gem_ratio)
    
    # 输出
    print(f"\n{'='*60}")
    print(f"GEM 候选池校验 - Wave {args.wave}")
    print(f"{'='*60}")
    print(f"总候选: {result['total']}")
    print(f"GEM 候选: {result['gem_count']} ({result['gem_ratio']:.1%})")
    print(f"最低要求: {result['min_required']:.0%}")
    print(f"判定: {'PASS' if result['pass'] else 'FAIL'}")
    
    if not result["pass"]:
        print(f"\n非 GEM 候选 ({len(result['non_gem_candidates'])} 条):")
        for c in result["non_gem_candidates"][:5]:
            print(f"  - {c['id']}: {c['expression']}...")
        if len(result["non_gem_candidates"]) > 5:
            print(f"  ... 还有 {len(result['non_gem_candidates']) - 5} 条")
            
    # 退出码
    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
