# -*- coding: utf-8 -*-
"""run_gbr_batch8.py - GBR 第 8 批回测启动脚本（实际提交版）

使用通用 pipeline 基础设施 + 直接 import MCP 提交。
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.core.mcp_integrated_pipeline import create_pipeline


def main():
    # 创建 GBR pipeline
    pipeline = create_pipeline("GBR")
    
    # 第 8 批：model106 数据集
    exprs_file = PROJECT_ROOT / "tracking" / "GBR" / "candidates" / "gbr_model106_batch8.txt"
    
    if not exprs_file.exists():
        print(f"[ERROR] 表达式文件不存在: {exprs_file}")
        return
    
    # 运行 pipeline（实际提交）
    result = pipeline.run(
        exprs_file=str(exprs_file),
        dataset="model106",
        wave="08",
        submit=True,  # 实际提交
        enhance_diversity="auto",
        fresh=True,
        dry_run=False  # 实际提交，非干跑
    )
    
    print("\n" + "="*50)
    print("Pipeline 运行结果:")
    print("="*50)
    import json
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
