# -*- coding: utf-8 -*-
"""run_batch_with_diversity.py - 多样性增强桥接脚本

在调用 brain-simAlphasinBatch-and-track 前执行多样性增强。
零侵入现有 skill，立即可用。

用法:
  python run_batch_with_diversity.py --input <表达式文件> --output <增强后文件> [--mode auto]
"""
import sys
import json
from pathlib import Path

# 添加项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

try:
    from wqb.expression.diversity_enhancer import analyze_diversity, enhance_expressions
    DIVERSITY_AVAILABLE = True
except ImportError as e:
    print(f"[ERROR] 多样性增强系统不可用: {e}")
    print(f"[ERROR] 请确保 src/wqb/expression/diversity_enhancer.py 存在")
    DIVERSITY_AVAILABLE = False


def main():
    import argparse
    ap = argparse.ArgumentParser(description="多样性增强桥接脚本")
    ap.add_argument("--input", required=True, help="输入表达式文件")
    ap.add_argument("--output", required=True, help="输出增强后表达式文件")
    ap.add_argument("--mode", default="auto", choices=["auto", "always", "never"],
                    help="增强模式: auto=自动判断, always=强制增强, never=禁用")
    args = ap.parse_args()
    
    if not DIVERSITY_AVAILABLE:
        # 直接复制输入到输出
        import shutil
        shutil.copy(args.input, args.output)
        print(f"[fallback] 多样性系统不可用，直接复制: {args.input} -> {args.output}")
        return
    
    # 读取表达式
    with open(args.input, encoding="utf-8") as f:
        exprs = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    print(f"[load] 加载 {len(exprs)} 个表达式从 {args.input}")
    
    # 多样性分析
    report = analyze_diversity(exprs)
    m = report["current_metrics"]
    print(f"[diversity] 算子熵={m['operator_entropy']:.3f} "
          f"覆盖率={m['coverage_rate']:.2%} "
          f"新颖度={m['novelty_score']:.2%} "
          f"结构相似度={m['structural_similarity']:.2%}")
    
    # 打印建议
    if report.get("recommendations"):
        print("[diversity] 改进建议:")
        for rec in report["recommendations"]:
            print(f"  - {rec}")
    
    # 判断是否需要增强
    need_enhance = False
    if args.mode == "always":
        need_enhance = True
        print(f"[diversity] 强制增强模式")
    elif args.mode == "auto":
        if (m['operator_entropy'] < 2.0 or
            m['coverage_rate'] < 0.5 or
            m['novelty_score'] < 0.8 or
            m['structural_similarity'] > 0.7):
            need_enhance = True
            print(f"[diversity] 自动检测: 多样性不足，需要增强")
        else:
            print(f"[diversity] 自动检测: 多样性良好，无需增强")
    
    if need_enhance:
        print(f"[diversity] 执行增强...")
        exprs, enhance_report = enhance_expressions(exprs, target_count=len(exprs))
        
        # 打印增强后指标
        if "current_metrics" in enhance_report:
            m2 = enhance_report["current_metrics"]
            print(f"[diversity] 增强后: 算子熵={m2['operator_entropy']:.3f} "
                  f"覆盖率={m2['coverage_rate']:.2%} "
                  f"新颖度={m2['novelty_score']:.2%}")
        
        print(f"[diversity] 增强完成: {len(exprs)} 个表达式")
    
    # 写入输出
    with open(args.output, "w", encoding="utf-8") as f:
        for expr in exprs:
            f.write(expr + "\n")
    
    print(f"[output] 已写入 {args.output}")
    print(f"")
    print(f"下一步: 使用 brain-simAlphasinBatch-and-track 提交")
    print(f"  Set-Location \".qoder/skills/brain-simAlphasinBatch-and-track\"")
    print(f"  python scripts/batch_simulator.py --alpha-json {args.output} ...")


if __name__ == "__main__":
    main()
