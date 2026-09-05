# -*- coding: utf-8 -*-
"""diversity_enhancer.py - 多样性增强模块（嵌入 brain-simAlphasinBatch-and-track）

在 batch_simulator.py 提交前自动分析并增强表达式多样性。
"""
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple

# 添加项目根目录到路径（向上查找直到找到 src/wqb 目录）
SCRIPT_DIR = Path(__file__).resolve().parent
_project_root = SCRIPT_DIR
for _ in range(8):
    if (_project_root / "src" / "wqb").is_dir():
        break
    _project_root = _project_root.parent
sys.path.insert(0, str(_project_root / "src"))

try:
    from wqb.expression.diversity_enhancer import (
        analyze_diversity, enhance_expressions, DiversityMonitor
    )
    DIVERSITY_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] 多样性增强系统不可用: {e}")
    DIVERSITY_AVAILABLE = False


def enhance_if_needed(
    alpha_list: List[Dict[str, Any]], 
    mode: str = "auto", 
    verbose: bool = True,
    field_pool: List[str] = None
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    多样性增强入口
    
    Args:
        alpha_list: alpha 配置列表（含 settings/regular 等）
        mode: auto/always/never
        verbose: 是否打印详情
        field_pool: 战役数据集字段池（2026-08-18 起建议传入，None 回退通用字段）
    
    Returns:
        (增强后的 alpha_list, 多样性报告)
    """
    if not DIVERSITY_AVAILABLE or mode == "never":
        return alpha_list, {"status": "skipped", "reason": "disabled" if mode == "never" else "unavailable"}
    
    # 提取表达式
    exprs = []
    for alpha in alpha_list:
        expr = alpha.get("regular", "")
        if expr:
            exprs.append(expr)
    
    if not exprs:
        return alpha_list, {"status": "skipped", "reason": "no_expressions"}
    
    # 分析多样性
    report = analyze_diversity(exprs)
    
    if verbose:
        m = report.get("current_metrics", {})
        print(f"[diversity] 算子熵={m.get('operator_entropy', 0):.3f} "
              f"覆盖率={m.get('coverage_rate', 0):.2%} "
              f"新颖度={m.get('novelty_score', 0):.2%} "
              f"结构相似度={m.get('structural_similarity', 0):.2%}")
        
        if report.get("recommendations"):
            print("[diversity] 改进建议:")
            for rec in report["recommendations"]:
                print(f"  - {rec}")
    
    # 判断是否需要增强
    need_enhance = False
    if mode == "always":
        need_enhance = True
    elif mode == "auto":
        m = report.get("current_metrics", {})
        if (m.get('operator_entropy', 0) < 2.0 or
            m.get('coverage_rate', 0) < 0.5 or
            m.get('novelty_score', 0) < 0.8 or
            m.get('structural_similarity', 0) > 0.7):
            need_enhance = True
    
    if not need_enhance:
        if verbose:
            print(f"[diversity] 多样性良好，无需增强")
        return alpha_list, report
    
    # 执行增强
    if verbose:
        print(f"[diversity] 多样性不足，执行增强...")
    
    enhanced_exprs, enhance_report = enhance_expressions(exprs, target_count=len(exprs), field_pool=field_pool)
    
    # 2026-08-18 有效性校验（GBR 复盘）：指标零变化属假增强，enhanced 必须尊重 effective
    effective = enhance_report.get("effective", True)
    if not effective:
        if verbose:
            print("[diversity] 增强无效（签名无新增），保留原表达式")
        report["enhanced"] = False
        report["effective"] = False
        return alpha_list, report
    
    # 将增强后的表达式写回 alpha_list
    enhanced_alpha_list = []
    expr_idx = 0
    for alpha in alpha_list:
        if alpha.get("regular"):
            new_alpha = alpha.copy()
            new_alpha["regular"] = enhanced_exprs[expr_idx]
            # 标记已增强
            new_alpha["_diversity_enhanced"] = True
            enhanced_alpha_list.append(new_alpha)
            expr_idx += 1
        else:
            enhanced_alpha_list.append(alpha)
    
    if verbose:
        print(f"[diversity] 增强完成: {len(enhanced_exprs)} 个表达式")
        if "current_metrics" in enhance_report:
            m2 = enhance_report["current_metrics"]
            print(f"[diversity] 增强后: 算子熵={m2.get('operator_entropy', 0):.3f} "
                  f"覆盖率={m2.get('coverage_rate', 0):.2%} "
                  f"新颖度={m2.get('novelty_score', 0):.2%}")
    
    # 合并报告
    final_report = {
        **report,
        "enhanced": True,
        "effective": True,
        "enhance_report": enhance_report,
        "original_count": len(exprs),
        "enhanced_count": len(enhanced_exprs)
    }
    
    return enhanced_alpha_list, final_report


def get_diversity_report(alpha_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """获取多样性报告（不增强）"""
    if not DIVERSITY_AVAILABLE:
        return {"status": "unavailable"}
    
    exprs = [a.get("regular", "") for a in alpha_list if a.get("regular")]
    if not exprs:
        return {"status": "no_expressions"}
    
    return analyze_diversity(exprs)
